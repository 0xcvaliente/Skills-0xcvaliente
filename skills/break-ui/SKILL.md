---
name: break-ui
description: "Stress-test a component or screen with schema-backed and realistic worst-case data, empty/one/large collections, locales, and missing media. Build dev-only fixtures and report rendered failures; fix them only when requested."
license: MIT
---

# Break UI

Read [Claude Code adaptation notes](references/claude-notes.md), then the relevant
sections of [the detailed guide](references/guide.md). Keep the requested scope
and existing project conventions. Supporting examples are defaults, not runtime guarantees.

## Workflow

1. Map every rendered field, its boundary, schema limits, optionality, and collection states.
2. Read CATALOG.md; construct plausible worst-case, empty, one-item, and relevant large-list fixtures.
3. Inject fixtures through the component’s real data boundary and expose a dev-only toggle or isolated route.
4. Render the original component at representative sizes and inspect overflow, clipping, wrapping, hierarchy, and performance.
5. Report findings and proposed corrections. Apply and recheck fixes when the user requested them.

## Result

Reviewable fixture controls, actual rendered failures, locations, and scoped corrections or proposals.

## Supporting resources

- [CATALOG.md](CATALOG.md).

For source revisions and retained material, see [provenance](references/provenance.md).
