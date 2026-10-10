---
name: animate
description: "Build web UI animations and transitions with purposeful timing, interruption, exits, and reduced motion. Use for implementing motion in a component; use review-animations for critique, improve-animations for a motion roadmap, and animate-expo for React Native."
license: MIT
---

# Animate

Read [Claude Code adaptation notes](references/claude-notes.md), then the relevant
sections of [the detailed guide](references/guide.md). Keep the requested scope
and existing project conventions. Supporting examples are defaults, not runtime guarantees.

## Workflow

1. Inspect the interaction, frequency, existing tokens, and component behavior; keep focus and repeated actions immediate.
2. Name the motion purpose. Prefer no added motion when it provides no useful feedback or continuity.
3. Choose the smallest suitable implementation: CSS, WAAPI, or the project motion library. Read the guide decision sequence and RECIPES.md for the component.
4. Choose properties, easing, duration or spring, origin, interruption, exit, hover gating, and reduced motion together.
5. Implement and inspect rapid reversals, keyboard/touch behavior, and the rendered result.

## Result

Implementation, a concise rationale, and actual verification or remaining visual gaps.

## Supporting resources

- [RECIPES.md](RECIPES.md).

For source revisions and retained material, see [provenance](references/provenance.md).
