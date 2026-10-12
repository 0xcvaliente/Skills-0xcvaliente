---
name: apple-design
description: "Apply Apple-inspired interface and fluid-motion principles when the user requests that direction or is designing gestures, sheets, momentum, spatial continuity, and translucent materials. Adapt the principles to the target platform and existing brand."
license: MIT
---

# Apple Design

Read [Agent adaptation notes](references/agent-notes.md), then the relevant
sections of [the detailed guide](references/guide.md). Keep the requested scope
and existing project conventions. Supporting examples are defaults, not runtime guarantees.

## Workflow

1. Establish the requested platform, design direction, existing components, and accessibility needs.
2. Read the relevant guide sections for continuity, feedback, hierarchy, gestures, typography, materials, or springs.
3. During direct manipulation keep the element attached to the input; transfer release velocity into compatible settling motion.
4. Use platform-appropriate reduced motion and maintain contrast, keyboard access, and understandable navigation.
5. Verify rendered states, interruption, and device behavior; treat platform-derived numeric values as starting points.

## Result

An implementation or scoped critique grounded in the requested direction, with verification and tradeoffs.

For source revisions and retained material, see [provenance](references/provenance.md).
