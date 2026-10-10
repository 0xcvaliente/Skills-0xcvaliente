---
name: animate-expo
description: "Build or fix React Native and Expo animations, gestures, sheets, screen transitions, and haptics. Use the project’s compatible Reanimated, Gesture Handler, and navigation APIs; use animate for web motion."
license: MIT
---

# Animate Expo

Read [Claude Code adaptation notes](references/claude-notes.md), then the relevant
sections of [the detailed guide](references/guide.md). Keep the requested scope
and existing project conventions. Supporting examples are defaults, not runtime guarantees.

## Workflow

1. Inspect Expo SDK, React Native, architecture, Reanimated/Worklets, gesture, and navigation versions before choosing APIs.
2. Name purpose and frequency, then choose compatible native primitives and a UI-runtime motion path for continuous gestures.
3. Read the matching guide/RECIPES.md section; preserve velocity and interruption, reduce motion, and accessible alternatives.
4. Keep per-frame updates out of React state. Add dependencies only when needed and compatible with the existing SDK.
5. Build and check the target platform; distinguish simulator/emulator results from release-build physical-device evidence.

## Result

Native code, relevant build/probe results, and explicit device-only validation gaps.

## Supporting resources

- [RECIPES.md](RECIPES.md).

For source revisions and retained material, see [provenance](references/provenance.md).
