---
name: update-mattpocock-skills
description: Check the mattpocock/skills repo for upstream changes and integrate them into the user's installed copies. Use when the user asks to update, sync, or refresh the Matt Pocock skills, or to add or remove a skill from that set.
---

# Update Matt Pocock skills

Source of truth: `~/.claude/skill-sources/mattpocock-skills/` (`upstream/` git clone, `manifest.txt` list of picked skills, `PINNED` last-synced commit, `overlay/<skill>/` local file overrides, `sync.sh`). Installed copies in `~/.claude/skills/` are generated: never edit them directly, put customisations in `overlay/<skill>/<same path>`.

## Steps

1. Run `~/.claude/skill-sources/mattpocock-skills/sync.sh status`.
2. If up to date, say so and stop.
3. Otherwise read the actual diffs for the picked skills (`git -C <source>/upstream diff <pinned> <latest> -- skills/<path>`) and the upstream `CHANGELOG.md` entries. Summarise per skill what changed in behaviour, in a few lines each. Flag:
   - overlay files whose upstream changed (merge by hand before applying),
   - picked skills moved, removed, or deprecated upstream,
   - new engineering/productivity skills not in the manifest: recommend add or skip against the user's existing skills (`orchestration`, `pstack`, `ponytail`, built-in `code-review`) and the issue-tracker dependency noted in the README.
4. Apply changes to `manifest.txt` the user approves (adding, removing, or renaming a skill). For a removed skill, also delete its dir in `~/.claude/skills/` after confirming it has `UPSTREAM.md`.
5. Run `sync.sh apply`. Then spot-check that each synced `SKILL.md` has valid frontmatter and that skills it references by name still exist.
6. Report old to new commit and what changed. Don't commit or push anything.
