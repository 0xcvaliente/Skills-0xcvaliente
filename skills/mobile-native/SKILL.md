---
name: mobile-native
description: "Fix mobile web and PWA platform details such as sticky hover, viewport units, input zoom, touch feedback, scrolling, safe areas, keyboard layout, and theme chrome. Use for web apps that feel wrong on a phone; use animate-expo for React Native."
license: MIT
---

# Mobile Native Web

Read [Claude Code adaptation notes](references/claude-notes.md), then the relevant
sections of [the detailed guide](references/guide.md). Keep the requested scope
and existing project conventions. Supporting examples are defaults, not runtime guarantees.

## Workflow

1. Match the reported symptom to the guide and inspect the existing viewport, styles, and support matrix.
2. Apply capability queries, suitable viewport units, safe-area padding, and input/gesture semantics where their rationale applies.
3. Keep zoom and selectable content available. Separate immediate press feedback from action activation.
4. Avoid global scroll/selection suppression on document content and preserve native link behavior.
5. Verify available browser/keyboard states and state which behaviors still require a physical device.

## Result

Focused CSS/meta/interaction fixes with reasons and honest hardware-validation limits.

For source revisions and retained material, see [provenance](references/provenance.md).
