---
name: animation-performance
description: "Diagnose and fix web animations that drop frames, stutter, or feel choppy: choose composite-only properties (transform, opacity), keep motion off a busy main thread with CSS or WAAPI, avoid per-frame React state and inherited CSS variable recalculation, bound blur cost, and use will-change only when measured. Use when an animation is janky, when picking which property to animate, or when choosing CSS vs JS motion on performance grounds. Use animate to implement motion, review-animations for critique, ui-animation for recording-based jank diagnosis, animate-expo for React Native, and vercel-react-best-practices for general React performance."
license: MIT
---

# Animation Performance

Read [Agent adaptation notes](references/agent-notes.md), then the relevant
sections of [the detailed guide](references/guide.md). Keep the requested scope
and existing project conventions. Supporting examples are defaults, not runtime guarantees.

## Workflow

1. List every animation in scope with its driver, animated properties, and what the page is doing while it plays.
2. Match the symptom in the guide's symptom table; name the cause before proposing any change.
3. Work the diagnosis order: properties, busy main thread, per-frame React state, inherited CSS variables, animated variables, blur, then `will-change` last.
4. Separate findings verified from source from those needing a profiler recording on a real mid-range device.
5. Report before editing unless fixes were requested.

## Result

Per finding: element and file location, cause, before and after, and verified-from-code versus needs-device-recording. Order by cost (layout before paint, busy main thread before idle).

For source revisions and retained material, see [provenance](references/provenance.md).
