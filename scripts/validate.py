#!/usr/bin/env python3
"""Validate Agent Skills packages: frontmatter, name/folder match, local links,
and leftover host-specific wording in active (non-provenance) files.

Host wording: the skills listed in CLAUDE_FLAVORED are Claude Code skills kept as
imported, and those in VERBATIM_UPSTREAM are host-neutral skills vendored verbatim.
Host-specific wording in them is a WARNING and does not fail the run;
everywhere else it is an error. Pass --strict to treat warnings as errors.

Catalog: every skill under ./skills needs exactly one README.md table row whose first
cell links skills/<name>. With no argument, rows naming a missing folder also fail.

Usage: validate.py [--strict] [skills/<name> ...]   (default: every skill under ./skills)
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
# Files that record upstream origin or license text may keep original wording.
# This also covers provenance.json beside SKILL.md (its created_by names the creating tool).
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
# Host-neutral skills vendored verbatim from upstream: their text cannot be edited
# without breaking the pin, so host wording (an optional Claude Code hook, brand
# names in icon data) is a warning, not an error.
VERBATIM_UPSTREAM = {"design-taste-frontend"}
LINK_RE = re.compile(r"\]\((?!https?:|mailto:|#)([^)#\s]+)")

# README catalog: every folder under skills/ needs exactly one table row whose
# first cell links skills/<name>, and every such row must name an existing folder.
ROW_LINK_RE = re.compile(r"\]\((?:\./)?skills/([^)/#\s]+)/?\)")


def catalog_rows():
    """Map skill name -> number of README table rows whose first cell links skills/<name>."""
    counts = {}
    readme = os.path.join(ROOT, "README.md")
    if not os.path.isfile(readme):
        return counts
    for line in open(readme, encoding="utf-8"):
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = line.split("|")
        first = cells[1] if len(cells) > 2 else ""
        for name in set(ROW_LINK_RE.findall(first)):
            counts[name] = counts.get(name, 0) + 1
    return counts


def check_catalog(names, all_rows):
    """Errors for skills in `names` without exactly one row; with all_rows, also rows naming no folder."""
    errs = []
    counts = catalog_rows()
    for name in names:
        n = counts.get(name, 0)
        if n != 1:
            errs.append(f"README.md: skills/{name} has {n} catalog rows (needs exactly 1)")
    if all_rows:
        for name in sorted(counts):
            if not os.path.isdir(os.path.join(ROOT, "skills", name)):
                errs.append(f"README.md: catalog row names skills/{name}, which does not exist")
    return errs


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
                    (warns if name in CLAUDE_FLAVORED or name in VERBATIM_UPSTREAM else errs).append(msg)
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
    skills_dir = os.path.join(ROOT, "skills")
    names = [os.path.basename(os.path.abspath(t).rstrip("/")) for t in targets
             if os.path.dirname(os.path.abspath(t).rstrip("/")) == skills_dir]
    cat_errs = check_catalog(names, all_rows=not argv)
    for e in cat_errs:
        print(e)
    print(f"{len(targets)} skills checked, {bad} with problems, {nwarn} warnings, {len(cat_errs)} catalog problems")
    return 1 if bad or cat_errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
