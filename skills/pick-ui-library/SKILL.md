---
name: pick-ui-library
description: "Choose an appropriate library for a requested frontend capability using Emil Kowalski’s curated shortlist and the project’s existing dependencies. Use for an explicit library choice or recommendation; do not replace working dependencies without a migration request."
license: MIT
---

# Pick UI Library

Read [Agent adaptation notes](references/agent-notes.md), then the relevant
sections of [the detailed guide](references/guide.md). Keep the requested scope
and existing project conventions. Supporting examples are defaults, not runtime guarantees.

## Workflow

1. Identify the requested capability and inspect installed libraries, framework, versions, and constraints.
2. Read the relevant curated category and check the candidate’s current official docs, compatibility, maintenance, and license.
3. Prefer an existing suitable primitive over dependency churn; honor a user-chosen product.
4. Recommend the best fit with the relevant tradeoff. Install/integrate only when part of the task.

## Result

One grounded recommendation or requested integration, with current compatibility evidence.

For source revisions and retained material, see [provenance](references/provenance.md).
