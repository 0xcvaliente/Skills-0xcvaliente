---
name: find-animation-opportunities
description: "Inspect a UI for state changes that would benefit from purposeful motion and identify places that should remain immediate. Use for a read-only motion opportunity pass; use animate to implement selected opportunities."
license: MIT
---

# Find Animation Opportunities

Read [Claude Code adaptation notes](references/claude-notes.md), then the relevant
sections of [the detailed guide](references/guide.md). Keep the requested scope
and existing project conventions. Supporting examples are defaults, not runtime guarantees.

## Workflow

1. Inspect actual states, triggers, frequency, user attention, and current motion.
2. Read the guide’s discovery gates and reject motion with no clear feedback, orientation, or continuity purpose.
3. Recommend a small prioritized set with element, trigger, purpose, properties, timing, and reduced-motion behavior.
4. Name frequent actions and reading surfaces that should remain immediate.

## Result

A scoped opportunity report and deliberate no-animation decisions. No source edits unless requested.

For source revisions and retained material, see [provenance](references/provenance.md).
