#!/usr/bin/env python3
"""Static audit of MCP client config files (stdlib only).

Usage: audit_mcp_config.py CONFIG.json [CONFIG.json ...]

Finds server entries under any "mcpServers" / "servers" key and flags risky
settings, tagged by CIA property. Secret values are never printed.
Exit code 1 if any HIGH finding, 2 if a file cannot be read.
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

SECRET_KEY = re.compile(r"key|token|secret|passw|bearer|credential|authorization", re.I)
SECRET_VALUE = re.compile(
    r"sk-[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}"
    r"|xox[abprs]-[A-Za-z0-9-]{10,}|eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]+\."
)
SECRET_ARG = re.compile(r"^--?[\w-]*(token|key|secret|passw)[\w-]*=[^$]+", re.I)
SHELLS = {"sh", "bash", "zsh", "dash", "cmd", "cmd.exe", "powershell", "powershell.exe", "pwsh"}
PINNED = re.compile(r"(?:@|==)\d[^@/]*$")
LOOPBACK = {"localhost", "127.0.0.1", "::1"}
DOCKER_RISKS = [
    (r"--privileged", "privileged container"),
    (r"--(net|network)[ =]host", "host networking"),
    (r"docker\.sock", "Docker socket mounted (host takeover)"),
    (r"(-v|--volume)[ =]/(:|\s|$)", "host root filesystem mounted"),
]
ORDER = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}


def servers(node):
    if isinstance(node, dict):
        for key in ("mcpServers", "servers"):
            block = node.get(key)
            if isinstance(block, dict):
                for name, cfg in block.items():
                    if isinstance(cfg, dict) and ("command" in cfg or "url" in cfg):
                        yield name, cfg
        for value in node.values():
            yield from servers(value)
    elif isinstance(node, list):
        for value in node:
            yield from servers(value)


def audit(name, cfg):
    found = []

    def add(sev, cia, msg):
        found.append((sev, name, cia, msg))

    cmd = str(cfg.get("command", ""))
    args = [str(a) for a in cfg.get("args", []) if isinstance(a, (str, int, float))]
    line = " ".join([cmd, *args])
    exe = Path(cmd.replace("\\", "/")).name.lower()

    if exe in ("npx", "bunx", "pnpx", "uvx"):
        pkg = next((a for a in args if not a.startswith("-")), "")
        if "--from" in args and args.index("--from") + 1 < len(args):
            pkg = args[args.index("--from") + 1]
        if pkg and not PINNED.search(pkg):
            add("MEDIUM", "I", f"unpinned package '{pkg}' (pin an exact version)")

    if exe in SHELLS and any(a.lower() in ("-c", "/c", "-command") for a in args):
        add("HIGH", "I", "shell wrapper runs an arbitrary string; call the server binary directly")
    if re.search(r"(curl|wget)[^|]*\|\s*(ba|z)?sh", line):
        add("HIGH", "I", "pipes a download into a shell")

    if exe == "docker":
        for pattern, msg in DOCKER_RISKS:
            if re.search(pattern, line):
                add("HIGH", "C/I/A", msg)

    if re.search(r"0\.0\.0\.0", line):
        add("HIGH", "C/A", "binds to all interfaces; bind 127.0.0.1")

    url = cfg.get("url") or cfg.get("serverUrl")
    if isinstance(url, str):
        u = urlparse(url)
        if u.scheme == "http" and u.hostname not in LOOPBACK:
            add("HIGH", "C", "plaintext HTTP to a non-local host; use HTTPS")
        if u.username or u.password or re.search(
            r"[?&](token|key|api_?key|access_token|secret)=", "?" + u.query, re.I
        ):
            add("HIGH", "C", "credentials embedded in URL")

    for field in ("env", "headers"):
        values = cfg.get(field)
        if not isinstance(values, dict):
            continue
        for key, val in values.items():
            if (
                isinstance(val, str)
                and val.strip()
                and "$" not in val
                and (SECRET_VALUE.search(val) or SECRET_KEY.search(key))
            ):
                add("HIGH", "C", f"hard-coded secret in {field}.{key} (use an env reference)")

    if any(SECRET_VALUE.search(a) or SECRET_ARG.match(a) for a in args):
        add("HIGH", "C", "secret-like value in args (visible in process list)")

    home = str(Path.home())
    if any(
        a and not a.startswith("-") and (a.rstrip("/") in ("", "~", "$HOME", home) or re.fullmatch(r"[A-Za-z]:\\?", a))
        for a in args
    ):
        add("MEDIUM", "C/I", "server granted a broad root (/, home, or drive); limit to needed directories")

    return found


def main(paths):
    if not paths:
        print(__doc__)
        return 2
    findings, status = [], 0
    for path in paths:
        try:
            data = json.loads(Path(path).read_text())
        except (OSError, ValueError) as exc:
            print(f"{path}: cannot read ({exc})", file=sys.stderr)
            status = 2
            continue
        count = 0
        for name, cfg in servers(data):
            count += 1
            findings += [(path, *f) for f in audit(name, cfg)]
        print(f"{path}: {count} server(s)")
    for path, sev, name, cia, msg in sorted(findings, key=lambda f: (ORDER[f[1]], f[0], f[2])):
        print(f"[{sev}] ({cia}) {name} - {msg}   <{path}>")
    if not findings:
        print("No findings (heuristic check only; not a substitute for review).")
    return 1 if any(f[1] == "HIGH" for f in findings) else status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
