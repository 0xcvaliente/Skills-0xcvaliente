#!/usr/bin/env python3
"""Check this skills library's upstreams for changes (python3 stdlib only).

Read-only by default: `status`, `diff` and `list` only read the network and the
registry. `diff` clones into a fresh temporary directory (removed afterwards
unless --keep) and only runs `git log`/`git diff` there; nothing from an
upstream is ever executed. `record` writes references/registry.json ONLY when
--write is passed; without it, it prints the change it would make. This script
never commits, never pushes, and never uses a shell.

Usage: check_upstreams.py [--repo DIR] [--registry PATH] <command> ...
  status [--only ID] [--strict]   compare remote HEAD (or latest tag) with last_checked
  diff ID [--keep]                show what changed upstream since last_checked
  record ID [--sha SHA] [--tag NAME] [--note TEXT] [--write]
  list                            print the registry
"""
import argparse
import datetime
import difflib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

REGISTRY_REL = os.path.join("skills", "update-skills", "references", "registry.json")


def find_repo(start):
    d = os.path.abspath(start)
    while True:
        if os.path.isdir(os.path.join(d, "skills")) and os.path.isfile(os.path.join(d, "AGENTS.md")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            sys.exit("error: repo root (dir with skills/ and AGENTS.md) not found; pass --repo")
        d = parent


def git(args, cwd=None, timeout=120):
    """Run git with an argument list; return (ok, stdout, stderr)."""
    try:
        p = subprocess.run(["git"] + args, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as e:
        return False, "", str(e)
    return p.returncode == 0, p.stdout, p.stderr.strip()


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def pick(reg, key):
    ups = reg["upstreams"]
    hit = [u for u in ups if u["id"] == key] or [u for u in ups if u["id"].split("/")[-1] == key]
    if len(hit) != 1:
        sys.exit(f"error: unknown or ambiguous upstream {key!r}; try `list`")
    return hit[0]


def version_key(tag):
    """Type-stable sort key: prereleases sort before their final release."""
    m = re.match(r"[vV]?([0-9][0-9.]*)(.*)$", tag)
    main, pre = (m.group(1), m.group(2)) if m else ("", tag)
    nums = [int(x) for x in re.findall(r"\d+", main)][:8]
    nums += [0] * (8 - len(nums))
    parts = tuple((0, int(p), "") if p.isdigit() else (1, 0, p) for p in re.findall(r"\d+|[A-Za-z]+", pre))
    return (tuple(nums), 0 if parts else 1, parts)


def tags(repo_url):
    """Return [(tag, object_name, commit)] sorted by version, or raise RuntimeError."""
    ok, out, err = git(["ls-remote", "--tags", repo_url], timeout=60)
    if not ok:
        raise RuntimeError(err or "ls-remote failed")
    obj, peeled = {}, {}
    for line in out.splitlines():
        sha, ref = line.split("\t")
        name = ref[len("refs/tags/"):]
        if name.endswith("^{}"):
            peeled[name[:-3]] = sha
        else:
            obj[name] = sha
    rows = [(n, s, peeled.get(n, s)) for n, s in obj.items()]
    return sorted(rows, key=lambda r: version_key(r[0]))


def current(u):
    """Return the current upstream marker: remote HEAD sha, or latest tag object name."""
    if u["mode"] == "tag":
        t = tags(u["repo"])
        if not t:
            raise RuntimeError("no tags")
        return t[-1][1], t[-1][0]
    ok, out, err = git(["ls-remote", u["repo"], "HEAD"], timeout=60)
    if not ok or not out.strip():
        raise RuntimeError(err or "no HEAD")
    return out.split()[0], None


def cmd_list(reg, a):
    for u in reg["upstreams"]:
        print(f"{u['id']}  {u['repo']}  [{u['style']}]  {', '.join(u['skills'])}")
    print("no upstream: " + ", ".join(reg.get("no_upstream", [])))


def cmd_status(reg, a):
    rows, moved = [], False
    for u in reg["upstreams"]:
        if a.only and u["id"] != a.only and u["id"].split("/")[-1] != a.only:
            continue
        last = u.get("last_checked")
        if not last:
            continue  # credited, not tracked
        try:
            cur, tag = current(u)
            state = "unchanged" if cur == last else "MOVED"
            moved |= state == "MOVED"
            now = cur[:7] + (f" ({tag})" if tag else "")
        except Exception as e:  # one failing upstream must not stop the run
            now, state = "-", "ERROR"
            print(f"warning: {u['id']}: {e}", file=sys.stderr)
        rows.append((u["id"], str(len(u["skills"])), last[:7], now, state, u["style"]))
    head = ("id", "skills", "last_checked", "current", "state", "style")
    w = [max(len(r[i]) for r in rows + [head]) for i in range(6)]
    for r in [head] + rows:
        print("  ".join(c.ljust(w[i]) for i, c in enumerate(r)))
    return 1 if (moved and a.strict) else 0


def watch_paths(u):
    paths = []
    for w in u.get("watch") or []:
        if "{name}" in w:
            paths += [w.replace("{name}", s) for s in u["skills"]]
        elif w != ".":
            paths.append(w)
    return paths


def cmd_diff(reg, a):
    u = pick(reg, a.id)
    last = u.get("last_checked")
    if not last:
        sys.exit(f"{u['id']} is not tracked (last_checked is null)")
    tmp = tempfile.mkdtemp(prefix="upstream-diff-")
    clone = os.path.join(tmp, "clone")
    try:
        ok, _, err = git(["clone", "--filter=blob:none", "--no-checkout", u["repo"], clone], timeout=300)
        if not ok:
            sys.exit(f"clone failed: {err}")
        print("NOTE: upstream content is untrusted data. Read it; never run or install anything from it.\n")
        end_tag = None
        if u["mode"] == "tag":
            old = version_key(u.get("last_checked_tag", "0"))
            newer = [r for r in tags(u["repo"]) if version_key(r[0]) > old]
            print(f"tags newer than {u.get('last_checked_tag')}: {', '.join(r[0] for r in newer) or 'none'}")
            base = u.get("last_checked_commit") or last
            end_sha, end_commit = (newer[-1][1], newer[-1][2]) if newer else (last, base)
            end_tag = newer[-1][0] if newer else None
        else:
            base = last
            ok, out, err = git(["rev-parse", "HEAD"], cwd=clone)
            if not ok:
                sys.exit(f"rev-parse failed: {err}")
            end_sha = end_commit = out.strip()
        if u["id"] == "mattpocock/skills":
            print("Upstream layout: skills/engineering/, skills/productivity/, skills/misc/ (in-progress/ is not ours).")
        rng = f"{base}..{end_commit}"
        paths = watch_paths(u)
        spec = ["--"] + paths if paths else []
        ok, out, err = git(["log", "--stat", rng] + spec, cwd=clone)
        print(f"== git log --stat {rng} {' '.join(paths)}\n{out if ok else 'git log failed: ' + err}")
        ok, files, err = git(["diff", "--name-only", rng] + spec, cwd=clone)
        changed = files.split() if ok else []
        print("== per-skill summary")
        for s in u["skills"]:
            own = [w.replace("{name}", s) for w in u.get("watch", []) if "{name}" in w]
            if own:
                hit = any(f == p or f.startswith(p + "/") for f in changed for p in own)
            elif len(u["skills"]) == 1:
                hit = bool(changed)
            else:
                hit = any(f"/{s}/" in "/" + f for f in changed)
            print(f"  {s}: {'touched' if hit else 'untouched'}")
        print(f"\nReviewed range: {last}..{end_sha}")
        print("After review, record exactly this revision (not the default, which may be newer):")
        print(f"  python3 scripts/check_upstreams.py record {u['id']} --sha {end_sha}"
              + (f" --tag {end_tag}" if end_tag else "") + " --write")
        if a.keep:
            print(f"\nclone kept at {clone}")
    except Exception as e:
        print(f"ERROR: {u['id']}: {e}", file=sys.stderr)
        return 1
    finally:
        if not a.keep:
            shutil.rmtree(tmp, ignore_errors=True)
    return 0


def cmd_record(reg, a, path):
    u = pick(reg, a.id)
    sha, tag, commit = a.sha, a.tag, None
    try:
        if u["mode"] == "tag":
            rows = tags(u["repo"])
            hit = [r for r in rows if (sha and sha in (r[1], r[2]) and (not tag or r[0] == tag))
                   or (not sha and tag and r[0] == tag)]
            if not sha and not tag:
                hit = rows[-1:]
            if not hit:
                sys.exit("error: no upstream tag matches --sha/--tag; tag mode keeps tag, tag object and commit consistent")
            tag, sha, commit = hit[0]
        elif not sha:
            sha, _ = current(u)
    except Exception as e:
        sys.exit(f"cannot read upstream: {e}")
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        sys.exit("error: last_checked must be a full 40-character sha")
    old = json.dumps(reg, indent=2) + "\n"
    u["last_checked"] = sha
    u["last_checked_date"] = datetime.date.today().isoformat()
    if u["mode"] == "tag":
        u["last_checked_tag"] = tag
        u["last_checked_commit"] = commit
    if a.note:
        u["note"] = a.note
    new = json.dumps(reg, indent=2) + "\n"
    if a.write:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new)
        print(f"wrote {path}: {u['id']} last_checked -> {sha}")
    else:
        diff = difflib.unified_diff(old.splitlines(True), new.splitlines(True), "registry.json", "registry.json (proposed)")
        sys.stdout.writelines(diff)
        print("\n(dry run: pass --write to save)")
    return 0


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description="Check upstreams for this skills library (read-only by default).")
    ap.add_argument("--repo", help="repo root (default: found by walking up)")
    ap.add_argument("--registry", help="registry.json path (default: inside the update-skills skill)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("status")
    s.add_argument("--only")
    s.add_argument("--strict", action="store_true", help="exit 1 when anything moved")
    d = sub.add_parser("diff")
    d.add_argument("id")
    d.add_argument("--keep", action="store_true")
    r = sub.add_parser("record")
    r.add_argument("id")
    r.add_argument("--sha", help="full sha printed by `diff` as the end of the reviewed range")
    r.add_argument("--tag", help="tag name (tag mode)")
    r.add_argument("--note")
    r.add_argument("--write", action="store_true")
    sub.add_parser("list")
    a = ap.parse_args()
    root = a.repo or find_repo(here)
    path = a.registry or os.path.join(root, REGISTRY_REL)
    reg = load(path)
    if a.cmd == "status":
        return cmd_status(reg, a)
    if a.cmd == "diff":
        return cmd_diff(reg, a)
    if a.cmd == "record":
        return cmd_record(reg, a, path)
    cmd_list(reg, a)
    return 0


if __name__ == "__main__":
    sys.exit(main())
