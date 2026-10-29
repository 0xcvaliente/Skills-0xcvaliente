# Provenance

Adapted from [emilkowalski/skills](https://github.com/emilkowalski/skills/tree/a81dbca07f2217b7103e510c0f13f8d5b017afc9/skills/remove-animations)
at `a81dbca07f2217b7103e510c0f13f8d5b017afc9`, reviewed 2026-10-29. The skill was added upstream in that same commit
("add remove-animations skill", 2026-10-28). MIT, copyright 2026 Emil Kowalski.

The original complete entrypoint is retained byte for byte as
[upstream-SKILL.md.source](upstream-SKILL.md.source). [The manifest](source-manifest.json)
records the original path and SHA-256. [The license](../LICENSE) is copied unchanged from the upstream repository.

The entrypoint adds precise routing and a short workflow. The detailed working
guide removes the canned readiness greeting and frontmatter and adds a contents list.
It is interpreted through [agent-notes.md](agent-notes.md), copied from the sibling
Emil-derived skills. No hooks, global settings, runtime libraries, or background
jobs are installed by the instruction package.

The same upstream commit added a root `ui-cheatsheet.md` and a README line. The skill
does not reference the cheatsheet, so it is not imported. Durations, frequency cutoffs, and
reduction targets remain authored defaults. No affiliation or endorsement is claimed.
