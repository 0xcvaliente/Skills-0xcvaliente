---
name: improve-animations
description: "Audit existing motion across a requested codebase or subsystem and produce prioritized, self-contained improvement plans. Use for a motion roadmap; use review-animations for a single diff, animate for a focused implementation, and animation-performance for frame-drop diagnosis."
license: MIT
---

# Improve Animations

Read [Agent adaptation notes](references/agent-notes.md), then the relevant
sections of [the detailed guide](references/guide.md). Keep the requested scope
and existing project conventions. Supporting examples are defaults, not runtime guarantees.

## Workflow

1. Pin audit scope, interaction frequency, and current motion stack.
2. Read AUDIT.md and inventory actual motion implementations, shared tokens, and repeated defects.
3. Prioritize removal, simplification, responsiveness, interruption, accessibility, and measured performance before decoration.
4. Use PLAN-TEMPLATE.md for actionable plans with paths, observed issues, proposed changes, and acceptance checks.
5. Leave application source unchanged unless implementation was also requested.

## Result

Prioritized findings and implementation plans, distinguishing inspected code, runtime proof, and uncovered areas.

## Supporting resources

- [AUDIT.md](AUDIT.md).
- [PLAN-TEMPLATE.md](PLAN-TEMPLATE.md).

For source revisions and retained material, see [provenance](references/provenance.md).
