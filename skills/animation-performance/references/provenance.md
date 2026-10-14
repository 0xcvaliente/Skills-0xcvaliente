# Provenance

Adapted from [emilkowalski/skills](https://github.com/emilkowalski/skills/tree/2d228630ba1446365f614a108cb8252f1feda202/skills/animation-performance)
at `2d228630ba1446365f614a108cb8252f1feda202`, reviewed 2026-10-15. The skill was added upstream in
`6465079742eb019bc419caf2c352ecda03f5dfd8`; `2d228630` is the revision whose text is retained. MIT, copyright 2026 Emil Kowalski.

The original complete entrypoint is retained byte for byte as
[upstream-SKILL.md.source](upstream-SKILL.md.source). [The manifest](source-manifest.json)
records the original path and SHA-256. [The license](../LICENSE) is copied unchanged from the upstream repository.

The entrypoint adds precise routing and a short workflow. The detailed working
guide removes the canned readiness greeting and frontmatter, adds a contents list,
names sibling skills explicitly, and replaces browser-specific panel names
(DevTools Performance and Animations panels, remote debugging) with neutral
wording (the browser's performance profiler, animation inspector, and remote
inspection). It is interpreted through [agent-notes.md](agent-notes.md), copied from the sibling Emil-derived
skills. No hooks, global settings, runtime libraries, or background jobs are
installed by the instruction package.

Frame-budget numbers and the property tiers remain authored defaults; browser
support for compositor-only properties changes between versions, so profile the
target workload. No affiliation or endorsement is claimed.
