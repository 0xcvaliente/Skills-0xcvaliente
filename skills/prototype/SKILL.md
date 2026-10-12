---
name: prototype
description: "Build genuinely different UI variants in an isolated prototype route or standalone page with a working picker. Use when the user requests alternatives to compare; promote a selected variant only when selection or integration is authorized."
license: MIT
---

# Prototype UI Variants

Read [Agent adaptation notes](references/agent-notes.md), then the relevant
sections of [the detailed guide](references/guide.md). Keep the requested scope
and existing project conventions. Supporting examples are defaults, not runtime guarantees.

## Workflow

1. Respect the requested scope; inspect stack, tokens, personality, and surrounding context.
2. Choose distinct named directions on meaningful layout, density, interaction, or motion axes; use the user’s requested count.
3. Read PICKER.md and build a keyboard-accessible comparison harness isolated from production.
4. Verify every variant, realistic states, and picker controls in the browser when available.
5. Present honest tradeoffs and leave selection to the user unless already delegated. Promote and clean up only within that authorization.

## Result

A working picker, distinct alternatives, verified interactions, and the relevant selection/integration state.

## Supporting resources

- [PICKER.md](PICKER.md).

For source revisions and retained material, see [provenance](references/provenance.md).
