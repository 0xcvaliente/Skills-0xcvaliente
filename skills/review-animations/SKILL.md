---
name: review-animations
description: "Review a scoped animation diff or component for justified motion, responsiveness, timing, origins, interruption, performance, and accessibility. Return evidence-backed corrections and a calibrated verdict; use improve-animations for a whole-codebase roadmap, animation-performance to diagnose dropped frames, and remove-animations to delete motion that should not exist."
license: MIT
---

# Review Animations

Read [Agent adaptation notes](references/agent-notes.md), then the relevant
sections of [the detailed guide](references/guide.md). Keep the requested scope
and existing project conventions. Supporting examples are defaults, not runtime guarantees.

## Workflow

1. Pin files/diff and product frequency; inspect connected triggers and state transitions.
2. Read STANDARDS.md and the guide review/correction hierarchy; check all relevant standards.
3. Remove unjustified motion before polishing its ingredients. Respect intentional project tokens and user requirements.
4. Validate suspected defects with source and playback where possible; distinguish taste preferences from blocking failures.
5. Report before editing unless fixes were requested.

## Result

Before / After / Why findings with file locations, then Block or Approve for the verified scope. Name missing runtime proof.

## Supporting resources

- [STANDARDS.md](STANDARDS.md).

For source revisions and retained material, see [provenance](references/provenance.md).
