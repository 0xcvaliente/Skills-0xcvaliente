# Codebase Design

`codebase-design` provides a vocabulary and method for designing deep modules: substantial behavior behind an interface that callers can understand and use without learning its internal machinery. It applies at different scales, from a function or class to a package or a slice that spans application layers.

The key question is how much useful behavior an interface exposes for the knowledge it requires. Interface here includes ordering rules, invariants, configuration, error behavior, and performance expectations as well as types and method signatures.

## When to use it

Use it when simplifying a module, choosing where a dependency can be substituted, improving testability, or deciding whether an abstraction earns its maintenance cost. It is also useful when several developers or agents need a shared vocabulary for an architectural discussion.

The skill distinguishes a **module**, its **interface**, its **implementation**, a **seam** where behavior can vary, and an **adapter** that satisfies that interface. Depth gives callers more capability and keeps maintenance knowledge concentrated in fewer places.

## How it works

Review what callers must know, then ask whether the module can hide more of that complexity. The deletion test helps: if deleting an abstraction spreads complexity back across callers, it was doing useful work. If the complexity simply disappears, the abstraction may have been a pass-through.

For testability, the guidance favors explicit dependencies, small interfaces, and tests that cross the same seam as real callers. It discourages speculative seams when nothing actually varies. Internally composed implementations can still be deep; internal seams do not all need to become public concepts.

Two companion documents extend the method. `DEEPENING.md` examines dependency categories and how to reshape a cluster. `DESIGN-IT-TWICE.md` describes comparing radically different interface designs, including a parallel-agent approach when that workflow is appropriate and available.

## Requirements and output

There are no executable helpers or library dependencies. Useful input includes the target code, representative callers, dependency constraints, and the behavior tests must exercise.

Outputs can include an interface proposal, a comparison of seams, a refactoring plan, or an implemented restructuring when requested. The skill supplies design criteria rather than an automatic code analyzer.

## Example requests

```text
/codebase-design review this payment module's interface and propose
a smaller surface that hides retry and provider-specific behavior.

/codebase-design compare two seam locations for storage access,
using the existing callers and tests as evidence.
```

## Package guide

- [SKILL.md](SKILL.md): glossary, depth principles, and testability guidance.
- [DEEPENING.md](DEEPENING.md): dependency-aware module improvement.
- [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md): exploration of alternative interfaces.

[Domain Modeling](../domain-modeling/README.md) complements this skill when the problem concerns business terminology. Install by copying this directory to `~/.claude/skills/codebase-design/` (for example `cp -R codebase-design ~/.claude/skills/`). Claude Code then uses it automatically when a request matches, or you can invoke it directly with `/codebase-design`. See the [Claude Code skills documentation](https://docs.claude.com/en/docs/claude-code/skills).
