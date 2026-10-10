#!/usr/bin/env python3
"""Small, local repository inventory and evidence tracker. Python 3.9+ and Git.

No network, model API, third-party packages, source execution, Git writes, or
background process. Inventory uses paths and stat metadata, not source contents.
Only explicitly named note/evidence files are read and hashed for review checks.
"""
from __future__ import annotations

import argparse
from collections import Counter
import fnmatch
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import tempfile
from typing import Any

CONTEXT = "docs/agent-context"
LOCAL = CONTEXT + "/.local"
MAX_HASH_BYTES = 2 * 1024 * 1024
MAX_MAP_BYTES = 12_000
EXCLUDED_DIRS = {
    ".git", "node_modules", "vendor", ".venv", "venv", "__pycache__",
    ".next", ".nuxt", ".output", "dist", "build", "target", "coverage",
    ".cache", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".turbo",
    ".terraform", ".aws", ".ssh", "secrets", "credentials",
}
SECRET_PATTERNS = (
    ".env", ".env.*", "*.pem", "*.key", "*.p12", "*.pfx", "*.keystore",
    "id_rsa*", "id_ed25519*", "credentials*", "secrets*", "*.tfstate*",
    ".npmrc", ".pypirc", ".netrc", "service-account*.json", "*.log",
)
MANIFESTS = {
    "package.json", "pyproject.toml", "requirements.txt", "Cargo.toml", "go.mod",
    "pom.xml", "build.gradle", "build.gradle.kts", "composer.json", "Gemfile",
    "mix.exs", "pubspec.yaml", "Package.swift", "deno.json", "deno.jsonc",
    "pnpm-workspace.yaml", "turbo.json", "nx.json", "CMakeLists.txt",
}


def git(root: Path, *args: str, optional: bool = False) -> bytes:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args], stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, timeout=45, check=False,
            env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ValueError("Git is unavailable or timed out.") from exc
    if result.returncode and not optional:
        raise ValueError("Git command failed; select an accessible Git working tree.")
    return result.stdout if result.returncode == 0 else b""


def repo_root(value: str) -> Path:
    start = Path(value).expanduser().resolve()
    if not start.is_dir():
        raise ValueError("--repo must point to an existing directory.")
    raw = git(start, "rev-parse", "--show-toplevel").strip()
    if not raw:
        raise ValueError("A Git working tree is required; no filesystem fallback scan is used.")
    return Path(os.fsdecode(raw)).resolve()


def normalize(value: str) -> str:
    p = PurePosixPath(value)
    if p.is_absolute() or ".." in p.parts or "\\" in value:
        raise ValueError("Use a repository-relative path without '..' or backslashes.")
    if any(ord(c) < 32 or ord(c) == 127 for c in value):
        raise ValueError("Control characters in paths are not supported.")
    return p.as_posix()


def safe_path(root: Path, relative: str) -> Path:
    rel = normalize(relative)
    current = root
    for part in PurePosixPath(rel).parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("Symlinked paths are not supported: " + rel)
    return root / rel


def is_source_path(relative: str) -> bool:
    parts = PurePosixPath(relative).parts
    if not parts or relative == ".":
        return False
    if relative == CONTEXT or relative.startswith(CONTEXT + "/"):
        return False
    if relative.startswith((".agents/skills/repo-context/", ".claude/skills/repo-context/")):
        return False
    if any(p.lower() in EXCLUDED_DIRS for p in parts[:-1]):
        return False
    name = parts[-1].lower()
    return not any(fnmatch.fnmatchcase(name, pat) for pat in SECRET_PATTERNS)


def inventory(root: Path) -> dict[str, list[int]]:
    # Git applies ignore rules to untracked files. Tracked files remain eligible
    # even if a later .gitignore pattern matches them. Extra exclusions still apply.
    raw = git(root, "ls-files", "--cached", "--others", "--exclude-standard", "-z")
    result: dict[str, list[int]] = {}
    for entry in raw.split(b"\0"):
        if not entry:
            continue
        rel = os.fsdecode(entry)
        try:
            normalize(rel)
            if not is_source_path(rel):
                continue
            p = safe_path(root, rel)
            s = p.stat()
            if stat.S_ISREG(s.st_mode):
                result[rel] = [s.st_size, s.st_mtime_ns, s.st_ctime_ns, s.st_mode]
        except (OSError, ValueError):
            # Omit inaccessible, deleted, unusual-path, symlink, and submodule entries.
            continue
    return dict(sorted(result.items()))


def head(root: Path) -> str:
    return git(root, "rev-parse", "--verify", "HEAD", optional=True).decode().strip() or "unborn"


def load_json(root: Path, relative: str) -> dict[str, Any]:
    p = safe_path(root, relative)
    if not p.exists():
        return {}
    try:
        if p.stat().st_size > 50_000_000:
            raise ValueError("State file is too large: " + relative)
        value = json.loads(p.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError("State must be a JSON object: " + relative)
        return value
    except (json.JSONDecodeError, UnicodeError) as exc:
        raise ValueError("Invalid local state: " + relative) from exc


def atomic_write(root: Path, relative: str, content: str) -> None:
    p = safe_path(root, relative)
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists() and p.read_text(encoding="utf-8") == content:
        return
    fd, temporary = tempfile.mkstemp(prefix=".repo-context-", dir=p.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        os.replace(temporary, p)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def save_json(root: Path, relative: str, value: dict[str, Any]) -> None:
    atomic_write(root, relative, json.dumps(value, sort_keys=True, indent=2) + "\n")


def matches_scope(path: str, scope: str) -> bool:
    return scope == "." or path == scope or path.startswith(scope.rstrip("/") + "/")


def fingerprint(files: dict[str, list[int]], scope: str) -> str:
    subset = {p: s for p, s in files.items() if matches_scope(p, scope)}
    return hashlib.sha256(json.dumps(subset, sort_keys=True).encode()).hexdigest()


def sha_file(root: Path, relative: str) -> str:
    p = safe_path(root, relative)
    if not p.is_file() or p.stat().st_size > MAX_HASH_BYTES:
        raise ValueError("Evidence must be a regular file no larger than 2 MiB: " + relative)
    # Bounded read also catches files that grow after stat(). Contents are never printed.
    with p.open("rb") as f:
        data = f.read(MAX_HASH_BYTES + 1)
    if len(data) > MAX_HASH_BYTES:
        raise ValueError("Evidence grew beyond 2 MiB: " + relative)
    return hashlib.sha256(data).hexdigest()


def note_path(value: str) -> str:
    rel = normalize(value)
    if (not rel.startswith(CONTEXT + "/") or not rel.endswith(".md")
            or "/.local/" in rel or rel.endswith("MAP.generated.md")):
        raise ValueError("A review note must be a non-generated .md file under " + CONTEXT)
    return rel


def show_paths(title: str, paths: list[str], limit: int) -> None:
    print(f"{title}: {len(paths)}")
    for path in paths[:limit]:
        print("  " + json.dumps(path, ensure_ascii=True))
    if len(paths) > limit:
        print(f"  ... {len(paths) - limit} omitted; narrow --scope or --match.")


def make_map(files: dict[str, list[int]], commit: str) -> str:
    paths = list(files)
    groups = Counter("/".join(PurePosixPath(p).parts[:2])
                     if len(PurePosixPath(p).parts) > 2 else
                     (PurePosixPath(p).parts[0] if "/" in p else "(root files)")
                     for p in paths)
    manifests = [p for p in paths if PurePosixPath(p).name in MANIFESTS]
    entries = [p for p in paths if PurePosixPath(p).name.lower() in {
        "main.py", "app.py", "manage.py", "main.go", "main.rs", "lib.rs",
        "index.ts", "index.tsx", "main.ts", "server.ts", "app.ts", "app.tsx",
        "index.js", "server.js", "middleware.ts", "schema.prisma", "dockerfile",
        "compose.yaml", "docker-compose.yml", "makefile", "readme.md",
    }]
    tests = [p for p in paths if any(x in {"test", "tests", "__tests__", ".github"}
                                     for x in PurePosixPath(p).parts)]
    lines = ["# Repository inventory (generated)", "",
             "Filename-based navigation only, NOT a verified architecture or dependency graph.",
             f"Snapshot HEAD: `{commit}`. Eligible regular files: {len(paths)}.",
             "Ignores common generated/secret paths; omits symlinks and submodule contents.",
             "A file not listed here may still exist. Use the scoped `files` command.",
             "Do not edit this file by hand. Refreshing it does NOT revalidate notes.", "",
             "## Directory groups (file counts)"]
    for group, count in sorted(groups.items(), key=lambda x: (-x[1], x[0]))[:45]:
        lines.append(f"- {json.dumps(group)}: {count}")
    if len(groups) > 45:
        lines.append(f"- {len(groups) - 45} more groups omitted.")
    for title, selection, cap in [("Manifests / workspace configuration", manifests, 35),
                                  ("Possible entry points / navigation hints", entries, 35),
                                  ("Test / CI path hints", tests, 20)]:
        lines += ["", "## " + title]
        lines += ["- " + json.dumps(p, ensure_ascii=True) for p in selection[:cap]] or ["- None found by filename heuristic."]
        if len(selection) > cap:
            lines.append(f"- {len(selection) - cap} more paths omitted.")
    trailer = "\n\nOutput is bounded. Scope further exploration to the task; verify current source.\n"
    bounded: list[str] = []
    used = len(trailer.encode()) + 60  # Reserve room for the truncation notice.
    for line in lines:
        size = len((line + "\n").encode())
        if used + size > MAX_MAP_BYTES:
            bounded.append("[Remaining inventory omitted at byte limit.]")
            break
        bounded.append(line)
        used += size
    return "\n".join(bounded) + trailer


def run(args: argparse.Namespace) -> int:
    root = repo_root(args.repo)
    files = inventory(root)
    commit = head(root)
    if args.command == "refresh":
        # Local machine state is deliberately separate from versioned notes.
        ignore = safe_path(root, CONTEXT + "/.gitignore")
        text = ignore.read_text(encoding="utf-8") if ignore.exists() else ""
        if ".local/" not in text.splitlines():
            atomic_write(root, CONTEXT + "/.gitignore", text.rstrip() + "\n.local/\n")
        generated = make_map(files, commit)
        atomic_write(root, CONTEXT + "/MAP.generated.md", generated)
        save_json(root, LOCAL + "/map-state.json", {"version": 1, "head": commit, "files": files})
        print(f"Wrote {CONTEXT}/MAP.generated.md ({len(generated.encode())} bytes).")
        print("Architecture notes and review records were not modified.")
        return 0
    if args.command == "files":
        scope = normalize(args.scope)
        selection = [p for p in files if matches_scope(p, scope)
                     and (not args.match or fnmatch.fnmatchcase(p, args.match))]
        show_paths("Matching eligible files", selection, args.limit)
        return 0
    if args.command == "status":
        state = load_json(root, LOCAL + "/map-state.json")
        if not state:
            print("No local map snapshot. Run refresh once; architecture notes remain unreviewed.")
            return 0
        previous = state.get("files", {})
        scope = normalize(args.scope)
        added = [p for p in files.keys() - previous.keys() if matches_scope(p, scope)]
        removed = [p for p in previous.keys() - files.keys() if matches_scope(p, scope)]
        changed = [p for p in files.keys() & previous.keys()
                   if files[p] != previous[p] and matches_scope(p, scope)]
        print(f"HEAD {'unchanged' if state.get('head') == commit else 'changed'} since map snapshot.")
        show_paths("Added", sorted(added), args.limit)
        show_paths("Removed", sorted(removed), args.limit)
        show_paths("Metadata changed", sorted(changed), args.limit)
        print("Metadata is a navigation hint, not proof of unchanged behavior. Check relevant notes/source.")
        return 0
    if args.command in {"review", "check"}:
        note = note_path(args.note)
        reviews = load_json(root, LOCAL + "/reviews.json")
        records = reviews.get("notes", {})
        if not isinstance(records, dict):
            raise ValueError("Invalid review records.")
        if args.command == "review":
            evidence = sorted(set(normalize(p) for p in args.evidence))
            scopes = sorted(set(normalize(p) for p in args.scope))
            if len(evidence) > 24 or len(scopes) > 12:
                raise ValueError("Keep a note focused: at most 24 evidence files and 12 scopes.")
            for p in evidence:
                if p not in files:
                    raise ValueError("Evidence is missing, ignored, excluded, or symlinked: " + p)
            for scope in scopes:
                if not any(matches_scope(p, scope) for p in files):
                    raise ValueError("Review scope has no eligible files: " + scope)
            records[note] = {"head": commit, "note_sha256": sha_file(root, note),
                             "evidence": {p: sha_file(root, p) for p in evidence},
                             "scopes": {s: fingerprint(files, s) for s in scopes}}
            save_json(root, LOCAL + "/reviews.json", {"version": 1, "notes": records})
            print("Recorded review evidence for " + note)
            print("This records your completed review; it does not validate architectural claims.")
            return 0
        record = records.get(note)
        if not record:
            print("UNREVIEWED: " + note + ". Validate its claims against current source before relying on it.")
            return 2
        reasons: list[str] = []
        try:
            if sha_file(root, note) != record.get("note_sha256"):
                reasons.append("note text changed")
        except (ValueError, OSError):
            reasons.append("note is missing or unreadable")
        for p, expected in record.get("evidence", {}).items():
            try:
                if p not in files or sha_file(root, p) != expected:
                    reasons.append("evidence changed: " + p)
            except (ValueError, OSError):
                reasons.append("evidence unavailable: " + p)
        for scope, expected in record.get("scopes", {}).items():
            if fingerprint(files, scope) != expected:
                reasons.append("scope layout/metadata changed: " + scope)
        if reasons:
            print("RECHECK: " + note)
            for reason in reasons:
                print("  " + reason)
            return 2
        print("UNCHANGED RECORDED EVIDENCE: " + note)
        print("Not a correctness guarantee; dependencies outside the recorded evidence/scopes may change.")
        return 0
    raise ValueError("Unknown command.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Any directory inside the target Git working tree")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("refresh", help="Regenerate filename map and its LOCAL metadata snapshot")
    status = sub.add_parser("status", help="List changes since the map snapshot; no file contents")
    listing = sub.add_parser("files", help="List bounded filename matches")
    for p in (status, listing):
        p.add_argument("--scope", default=".", help="Repository-relative directory or file")
        p.add_argument("--limit", type=int, default=30)
    listing.add_argument("--match", default="", help="Filename glob against full relative paths")
    review = sub.add_parser("review", help="Record evidence AFTER actually reviewing a note")
    review.add_argument("note")
    review.add_argument("--evidence", nargs="+", required=True)
    review.add_argument("--scope", nargs="+", required=True,
                        help="Relevant source directories, including cross-cutting dependencies")
    check = sub.add_parser("check", help="Check a single note's recorded evidence for staleness")
    check.add_argument("note")
    args = parser.parse_args()
    if hasattr(args, "limit") and not 1 <= args.limit <= 200:
        parser.error("--limit must be between 1 and 200")
    try:
        return run(args)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print("repo-context: " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
