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
