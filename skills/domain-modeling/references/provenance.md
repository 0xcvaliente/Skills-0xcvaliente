# Provenance

Original source: [mattpocock/skills](https://github.com/mattpocock/skills/tree/b0618bc436ad893b3c5e84e55fba86586d34a404/skills/engineering/domain-modeling),
reviewed 2026-10-09 at `b0618bc436ad893b3c5e84e55fba86586d34a404`.
The upstream MIT [license](../LICENSE) is retained. Adopts the upstream GLOSSARY naming while retaining existing CONTEXT paths and the legacy format file; project records are not migrated automatically.

## Claude Code port

Ported from the Codex version on 2026-10-10. The README's install and usage sections target `~/.claude/skills/domain-modeling/` and `/domain-modeling`, and the reference to the removed Codex `agents/openai.yaml` metadata was dropped. Skill content is unchanged.

## Host-neutral adaptation

Made host-neutral for the Agent Skills standard on 2026-10-12. README install and examples are host-neutral (`~/.agents/skills/`, "use the skill" phrasing). Skill guidance is unchanged.

## Upstream review 2026-10-20

Checked against mattpocock/skills `5beb35b040e3de97e54fa9e386d7e42d15c295c2`: no changes to `skills/engineering/domain-modeling` since `b0618bc436ad893b3c5e84e55fba86586d34a404`.

## Upstream review 2026-10-29

Checked against mattpocock/skills `a496f5513d4a4cf889bc48e189e579f4b0bdf6aa` (a496f55), from `5beb35b`. No change to `skills/engineering/domain-modeling`. The only related upstream edit is to the docs page `docs/engineering/domain-modeling.md` (FAQ answer on GLOSSARY.md vs CONTEXT.md naming, now referencing `/setup-matt-pocock-skills`); that page is not shipped here and the skill has no matching FAQ, so it was skipped.
