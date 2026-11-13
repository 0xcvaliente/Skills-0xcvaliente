# Provenance

- Upstream: https://github.com/blader/humanizer, MIT, Copyright (c) 2025 Siqi Chen
- Revision: 0ef9fe5bc3572734fd3ae6c448fe00a30cd5dcf0 (0ef9fe5)
- Version: 3.1.0 (`metadata.version` in SKILL.md)
- 2026-10-29: imported. Previously installed outside this repo as a standalone clone at `~/.claude/skills/humanizer`, pinned at 8c307f3; the two upstream commits between 8c307f3 and 0ef9fe5 only touch the Claude plugin manifest.
  - Taken verbatim from upstream root: `SKILL.md`, `LICENSE`. `README.md` kept as `references/upstream-README.md.source` (host-specific install instructions); a short host-neutral `README.md` was written locally.
  - Left out, and why:
    - `.claude-plugin/` and `.cursor-plugin/`: plugin manifests for one host each; not part of an Agent Skills package.
    - `.github/`: upstream issue templates and CI workflow, irrelevant here.
    - `agents/openai.yaml`: host-specific agent metadata.
    - `scripts/validate-package.py`: upstream packaging validator; this repo has its own `scripts/validate.py`.
    - `AGENTS.md`: upstream maintainer instructions, not skill content.
    - `CHANGELOG.md`: upstream release notes; the version is recorded here.
  - `SKILL.md` references none of the omitted files (checked with grep).
- 2026-11-10: re-synced verbatim from 0ef9fe5 (v3.1.0) to b48c832f0f809c1b5658edbb838c2521b72f2413 (b48c832, v4.0.0 per `metadata.version`). The local `SKILL.md`, `LICENSE` and `references/upstream-README.md.source` all matched 0ef9fe5 first, so there were no local edits. `SKILL.md` and the upstream README copy were replaced with the b48c832 files; `LICENSE` is identical at both revisions. The same files are left out as before, plus the new `package.json` (a pi package manifest for one host). `SKILL.md` still references none of the omitted files.
  - Behavior change in 4.0.0: the skill no longer forbids adding facts. Step 2 now says to add a specific detail you know to be true where the text is generic, and the line "Do not make anything up" is gone from the introduction; patterns 14 and 17 follow. It still keeps every supported claim and treats a lost or changed claim as an error. The local `README.md` says this.
  - Also new: text being edited may contain fake closing tags or notes from an "operator" or "system message", and the skill treats them as material, never as instructions; file mode reads the whole current file before editing and reports how many sections it covered; 15 "After" examples were reworked; pattern 15 is renamed "Shallow -ing phrases"; the description no longer cites Wikipedia (the credit stays in the Source section).
