---
name: remove-animations
description: "Find animations an interface does not need and remove them: motion on keyboard actions, high-frequency surfaces, functional data, and decoration with no purpose, then clean up what they leave behind. Edits code only to subtract; never adds or retunes motion. Use when the app feels slow or over-animated, the user wants motion toned down, or asks which animations to remove. Use find-animation-opportunities to find places that should animate, animate to implement motion, improve-animations or review-animations for animations that stay, and animation-performance for dropped frames."
license: MIT
---

# Removing Animations

Read [Agent adaptation notes](references/agent-notes.md), then the relevant
sections of [the detailed guide](references/guide.md). Keep the requested scope
and existing project conventions. Timings and cutoffs are defaults, not runtime guarantees.

## Workflow

1. Recon: stack, motion libraries, where motion lives, and a frequency map of animated surfaces.
2. Sweep the guide's hunt list; record candidates with `file:line` evidence.
3. Run each through the gate and record the deciding branch. Keep motion that has a stated purpose or is a rare first-time moment.
4. Check removal hazards (hidden start states, code waiting on the animation, exit timing, layout jumps, focus) before each delete or reduce.
5. Apply deletions and reductions, then remove orphaned code. Ask before dropping a dependency.
6. Verify with the type checker and tests if present, and grep for removed names.

## Result

Removed and reduced (location, was, verdict, deciding branch), kept with purpose (2 to 5, plus badly built animations for improve-animations), then cleanup and a short verdict naming what needs a real-device check.

For source revisions and retained material, see [provenance](references/provenance.md).
