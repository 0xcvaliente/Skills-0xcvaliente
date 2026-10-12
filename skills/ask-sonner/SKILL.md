---
name: ask-sonner
description: "Configure, style, or troubleshoot Sonner toasts in React: Toaster setup, promise/loading updates, dismissal, themes, stacking, positioning, and multiple instances. Use when the project uses or explicitly requests Sonner."
license: MIT
---

# Ask Sonner

Read [Agent adaptation notes](references/agent-notes.md), then the relevant
sections of [the detailed guide](references/guide.md). Keep the requested scope
and existing project conventions. Supporting examples are defaults, not runtime guarantees.

## Workflow

1. Inspect installed Sonner/framework versions, Toaster ownership, providers, theme, and overlay layering.
2. Read the matching guide/API.md section and verify current version-specific options in official docs when needed.
3. Use the right toast lifecycle and avoid duplicate Toasters or duplicate action/event delivery.
4. Preserve accessible announcements, understandable failure feedback, and the project’s visual tokens.
5. Exercise the actual trigger, loading/success/error transitions, dismissal, dark mode, and modal interactions as relevant.

## Result

A focused integration or fix, with observable lifecycle checks and remaining gaps.

## Supporting resources

- [API.md](API.md).

For source revisions and retained material, see [provenance](references/provenance.md).
