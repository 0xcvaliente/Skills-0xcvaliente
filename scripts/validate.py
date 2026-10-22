#!/usr/bin/env python3
"""Validate Agent Skills packages: frontmatter, name/folder match, local links,
and leftover host-specific wording in active (non-provenance) files.

Host wording: the skills listed in CLAUDE_FLAVORED are Claude Code skills kept as
imported. Host-specific wording in them is a WARNING and does not fail the run;
everywhere else it is an error. Pass --strict to treat warnings as errors.

Usage: validate.py [--strict] [skills/<name> ...]   (default: every skill under ./skills)
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
# Files that record upstream origin or license text may keep original wording.
PRESERVED = re.compile(r"(provenance|upstream-SKILL|source-manifest|LICENSE|NOTICE|\.source$)|/upstream/|/licenses/")
TEXT = re.compile(r"\.(md|py|sh|json|yaml|yml|txt|mjs|js|ts)$")
# Wording that ties an active file to one host. Allowed only in lines that
# deliberately list several hosts (see ALLOW_LINE).
HOST_RE = re.compile(
    r"Claude Code|Claude in Chrome|claude-in-chrome|~/\.claude|AskUserQuestion|"
    r"\bTask tool\b|\bSkill tool\b|TodoWrite|mcp__|\bAnthropic\b"
)
ALLOW_LINE = re.compile(r"[Ee]xample|observed|headless|ran on Claude Code|writes host-specific|auto-allow permissions|Claude Code (only|target)|CLAUDE\.md|GEMINI\.md|AGENTS\.md|\.claude/skills|~/\.claude/skills|Claude Code[`,)]? *(,|and|or)|(Codex|Gemini|Cursor|Copilot|OpenCode)")
# Claude Code flavored skills: host wording is a warning, not an error.
CLAUDE_FLAVORED = {
    "diagnosing-bugs", "git-guardrails-claude-code", "grill-me", "grilling", "handoff",
    "pptx-deck", "reverse-engineer-anything", "tdd", "to-questionnaire", "update-mattpocock-skills",
    "wait-what", "writing-for-agents",
}
LINK_RE = re.compile(r"\]\((?!https?:|mailto:|#)([^)#\s]+)")


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fm = {}
    key = None
    for line in m.group(1).split("\n"):
        k = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if k:
            key = k.group(1)
            fm[key] = k.group(2).strip().strip('"').strip("'")
            if fm[key] in (">", ">-", "|", "|-"):
                fm[key] = ""
        elif key and line.startswith((" ", "\t")):
            fm[key] = (fm[key] + " " + line.strip()).strip()
    return fm


def check(skill_dir):
    errs = []
    warns = []
    name = os.path.basename(skill_dir.rstrip("/"))
    path = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(path):
        return [f"{name}: missing SKILL.md"], []
    text = open(path, encoding="utf-8").read()
    fm = frontmatter(text)
    if fm is None:
        return [f"{name}: SKILL.md has no frontmatter"], []
    if fm.get("name") != name:
        errs.append(f"{name}: frontmatter name {fm.get('name')!r} != folder")
    if not NAME_RE.match(fm.get("name", "")) or len(fm.get("name", "")) > 64:
        errs.append(f"{name}: invalid name (lowercase letters, digits, hyphens; max 64)")
    d = fm.get("description", "")
    if not d:
        errs.append(f"{name}: empty description")
    elif len(d) > 1024:
        errs.append(f"{name}: description is {len(d)} chars (max 1024)")
    for r, _, fs in os.walk(skill_dir):
        for f in fs:
            p = os.path.join(r, f)
            rel = os.path.relpath(p, ROOT)
            if f.endswith(".md") and not PRESERVED.search(rel):
                base = os.path.dirname(p)
                body = re.sub(r"```.*?```", "", open(p, encoding="utf-8", errors="ignore").read(), flags=re.S)
                for link in LINK_RE.findall(body):
                    target = os.path.normpath(os.path.join(base, link.split("?")[0]))
                    if not os.path.exists(target):
                        errs.append(f"{rel}: broken link {link}")
            if PRESERVED.search(rel) or not TEXT.search(f):
                continue
            for i, line in enumerate(open(p, encoding="utf-8", errors="ignore"), 1):
                if HOST_RE.search(line) and not ALLOW_LINE.search(line):
                    msg = f"{rel}:{i}: host-specific wording: {line.strip()[:90]}"
                    (warns if name in CLAUDE_FLAVORED else errs).append(msg)
    return errs, warns


def main(argv):
    strict = "--strict" in argv
    argv = [a for a in argv if a != "--strict"]
    targets = argv or sorted(
        os.path.join(ROOT, "skills", d) for d in os.listdir(os.path.join(ROOT, "skills"))
        if os.path.isdir(os.path.join(ROOT, "skills", d))
    )
    bad = nwarn = 0
    for t in targets:
        errs, warns = check(os.path.realpath(t))
        if strict:
            errs, warns = errs + warns, []
        for e in errs:
            print(e)
        for w in warns:
            print("warning: " + w)
        bad += bool(errs)
        nwarn += len(warns)
    print(f"{len(targets)} skills checked, {bad} with problems, {nwarn} warnings")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
