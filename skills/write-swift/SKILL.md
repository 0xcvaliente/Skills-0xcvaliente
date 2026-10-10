---
name: write-swift
description: "Write, review, or migrate Swift with value modeling, optionals/errors, ownership, protocols, generics, concurrency, performance, and Swift Testing. Use for Swift implementation and diagnostics; inspect toolchain and build flags before applying newer language features."
license: MIT
---

# Write Swift

Read [Claude Code adaptation notes](references/claude-notes.md), then the relevant
sections of [the detailed guide](references/guide.md). Keep the requested scope
and existing project conventions. Supporting examples are defaults, not runtime guarantees.

## Workflow

1. Inspect Swift/Xcode version, deployment target, language mode, actor-isolation settings, and package/app boundaries.
2. Read only the relevant guide sections for the model, diagnostic, concurrency, ARC, performance, or testing issue.
3. Use value types and explicit ownership where appropriate. Keep UI isolation correct and expensive work off the UI actor when required.
4. Treat Swift 6.2 concurrency behavior as dependent on actual compiler features/settings; do not rewrite a general-purpose library to main-actor-by-default.
5. Use project builds/tests and targeted diagnostics. Change compiler settings or adopt new features only when compatible and necessary.

## Result

Version-appropriate Swift code or findings, relevant build/test evidence, and unresolved runtime limitations.

For source revisions and retained material, see [provenance](references/provenance.md).
