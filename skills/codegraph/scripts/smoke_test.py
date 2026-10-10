#!/usr/bin/env python3
"""Exercise an installed CodeGraph in temporary non-Git fixtures. Python 3.9+."""

import argparse
import json
import os
from pathlib import Path
import queue
import shutil
import signal
import subprocess
import tempfile
import threading
import time


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def run_cli(executable, env, cwd, *args):
    process = subprocess.Popen(
        [executable, *args], cwd=cwd, env=env, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True, start_new_session=(os.name != "nt"),
    )
    try:
        output, errors = process.communicate(timeout=60)
    except subprocess.TimeoutExpired:
        if os.name != "nt":
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        else:
            process.kill()
        process.communicate()
        raise
    require(process.returncode == 0,
            "CLI failed: {}\n{}\n{}".format(args, output, errors))
    return output


class MCPClient:
    """Minimal newline-delimited stdio client; no SDK or LLM dependency."""

    def __init__(self, executable, env, cwd):
        self.errors = tempfile.TemporaryFile(mode="w+")
        self.process = subprocess.Popen(
            [executable, "serve", "--mcp", "--no-watch"],
            cwd=cwd, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=self.errors, text=True, bufsize=1,
            start_new_session=(os.name != "nt"),
        )
        self.messages = queue.Queue()
        self.next_id = 0
        self.reader = threading.Thread(target=self.read, daemon=True)
        self.reader.start()

    def read(self):
        try:
            for line in self.process.stdout:
                try:
                    self.messages.put(json.loads(line))
                except json.JSONDecodeError:
                    self.messages.put({"protocol_error": line.strip()})
        finally:
            self.messages.put(None)

    def send(self, method, params=None, request_id=None):
        message = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            message["params"] = params
        if request_id is not None:
            message["id"] = request_id
        self.process.stdin.write(json.dumps(message) + "\n")
        self.process.stdin.flush()

    def request(self, method, params=None):
        self.next_id += 1
        request_id = self.next_id
        self.send(method, params, request_id)
        deadline = time.monotonic() + 30
        while True:
            remaining = deadline - time.monotonic()
            require(remaining > 0, "MCP timeout: " + method)
            try:
                message = self.messages.get(timeout=remaining)
            except queue.Empty as exc:
                raise RuntimeError("MCP timeout: " + method) from exc
            if message is None:
                self.errors.seek(0)
                raise RuntimeError("MCP exited: " + self.errors.read()[-4000:])
            require("protocol_error" not in message,
                    "Non-JSON output on MCP stdout: " + str(message))
            if "method" in message:
                if "id" in message:
                    # The server may request workspace roots from its client.
                    reply = {"jsonrpc": "2.0", "id": message["id"]}
                    if message["method"] == "roots/list":
                        reply["result"] = {"roots": []}
                    else:
                        reply["error"] = {"code": -32601, "message": "Unsupported"}
                    self.process.stdin.write(json.dumps(reply) + "\n")
                    self.process.stdin.flush()
                continue
            if message.get("id") == request_id:
                require("error" not in message, "MCP error: " + str(message))
                return message["result"]

    def close(self):
        try:
            self.process.stdin.close()
            self.process.wait(timeout=5)
        except (OSError, subprocess.TimeoutExpired):
            if os.name != "nt":
                try:
                    os.killpg(self.process.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
            else:
                self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                if os.name != "nt":
                    os.killpg(self.process.pid, signal.SIGKILL)
                else:
                    self.process.kill()
                self.process.wait(timeout=5)
        finally:
            self.reader.join(timeout=2)
            self.process.stdout.close()
            self.errors.close()


def text_result(result):
    require(not result.get("isError"), "Tool failed: " + str(result))
    return "\n".join(item.get("text", "") for item in result.get("content", [])
                     if item.get("type") == "text")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codegraph", default="codegraph",
                        help="Installed command or executable path; never downloads it")
    args = parser.parse_args()
    executable = shutil.which(args.codegraph)
    require(executable is not None, "CodeGraph is not installed: " + args.codegraph)
    executable = os.path.abspath(executable)
    env = os.environ.copy()
    # Do not alter HOME or global agent settings. Remove inherited query overrides.
    for key in ("CODEGRAPH_DIR", "CODEGRAPH_MCP_TOOLS", "CODEGRAPH_EXPLORE_DEDUP",
                "CODEGRAPH_HOST_PPID"):
        env.pop(key, None)
    env.update(CODEGRAPH_TELEMETRY="0", CODEGRAPH_NO_DOWNLOAD="1",
               CODEGRAPH_NO_DAEMON="1", CODEGRAPH_NO_WATCH="1", NO_COLOR="1")
    checks = []
    with tempfile.TemporaryDirectory(prefix="codegraph-skill-") as temp:
        scratch = Path(temp)
        project = scratch / "project"
        project.mkdir()
        # No .git directory: disabled-watch init cannot install Git hooks.
        totals = project / "totals.ts"
        totals.write_text("export function calcTotal(amount: number): number {\n"
                          "  return amount * 2 + 71;\n}\n")
        (project / "checkout.ts").write_text(
            "import { calcTotal } from './totals';\n"
            "export function checkout(amount: number): number {\n"
            "  return calcTotal(amount);\n}\n")
        (project / "checkout.test.ts").write_text(
            "import { checkout } from './checkout';\n"
            "export function testCheckout(): number { return checkout(5); }\n")
        (project / "pricing.py").write_text(
            "def calc_python_cost(amount):\n    return amount * 3 + 19\n")
        (project / "python_order.py").write_text(
            "from pricing import calc_python_cost\n\n"
            "def python_order(amount):\n    return calc_python_cost(amount)\n")
        version = run_cli(executable, env, scratch, "--version").strip()
        run_cli(executable, env, scratch, "init", str(project), "--yes")
        require((project / ".codegraph").is_dir(), "Init did not create project index")
        checks.append("isolated_initial_index")
        for symbol, caller in (("calcTotal", "checkout"),
                               ("calc_python_cost", "python_order")):
            matches = json.loads(run_cli(executable, env, scratch, "query", symbol,
                                          "--path", str(project), "--json"))
            require(symbol in json.dumps(matches), "Symbol not retrieved: " + symbol)
            callers = json.loads(run_cli(executable, env, scratch, "callers", symbol,
                                          "--path", str(project), "--json"))
            require(caller in json.dumps(callers), "Cross-file caller missing: " + caller)
        checks.append("typescript_and_python_cross_file_callers")
        output = run_cli(executable, env, scratch, "explore", "checkout calcTotal",
                         "--path", str(project), "--max-files", "4")
        require("calcTotal(amount)" in output and "amount * 2 + 71" in output,
                "Explore did not retrieve entrypoint and callee source")
        checks.append("cli_explore_source")
        impact = json.loads(run_cli(executable, env, scratch, "impact", "calcTotal",
                                    "--path", str(project), "--depth", "2", "--json"))
        require("checkout" in json.dumps(impact), "Impact missed the dependent caller")
        affected = json.loads(run_cli(executable, env, scratch, "affected", "totals.ts",
                                      "--path", str(project), "--json"))
        require("checkout.test.ts" in json.dumps(affected),
                "Affected-test discovery missed the transitive dependent test")
        checks.append("cli_impact_and_transitive_affected_test")
        totals.write_text(totals.read_text().replace("+ 71", "+ 97"))
        run_cli(executable, env, scratch, "sync", str(project))
        output = run_cli(executable, env, scratch, "explore", "calcTotal",
                         "--path", str(project))
        require("amount * 2 + 97" in output and "amount * 2 + 71" not in output,
                "Sync did not refresh edited source")
        checks.append("explicit_sync_after_edit")
        client = MCPClient(executable, env, scratch)
        try:
            initialized = client.request("initialize", {
                "protocolVersion": "2024-11-05", "capabilities": {},
                "clientInfo": {"name": "codegraph-skill-smoke", "version": "1.0"},
            })
            require(initialized.get("serverInfo"), "Missing MCP server identity")
            client.send("notifications/initialized")
            tools = client.request("tools/list")["tools"]
            require([tool["name"] for tool in tools] == ["codegraph_explore"],
                    "Unexpected default MCP menu: " + str([t["name"] for t in tools]))
            require("projectPath" in tools[0]["inputSchema"]["properties"],
                    "MCP schema has no projectPath")
            checks.append("mcp_unindexed_root_default_explore_schema")
            def explore(path):
                return text_result(client.request("tools/call", {
                    "name": "codegraph_explore",
                    "arguments": {"query": "checkout calcTotal",
                                  "projectPath": str(path), "maxFiles": 4},
                }))
            output = explore(project)
            require("calcTotal(amount)" in output and "amount * 2 + 97" in output,
                    "MCP projectPath did not retrieve the intended fresh source")
            checks.append("mcp_explicit_project_path")
            missing = scratch / "unindexed"
            missing.mkdir()
            guidance = explore(missing).lower()
            require("not indexed" in guidance or "not initialized" in guidance
                    or "no .codegraph" in guidance,
                    "Missing unindexed-project guidance: " + guidance[:600])
            require("amount * 2 + 97" in explore(project),
                    "Unindexed query prevented a later indexed query")
            require(not (missing / ".codegraph").exists(),
                    "Querying an unindexed project created an index")
            checks.append("mcp_unindexed_project_guidance_and_recovery")
        finally:
            client.close()
    print(json.dumps({"status": "passed", "runtime_version": version,
                      "checks": checks}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, subprocess.TimeoutExpired, OSError, ValueError) as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, indent=2))
        raise SystemExit(1)
