# Domain Modeling

`domain-modeling` helps a project develop precise language for its business concepts and record consequential decisions. It is an active modeling workflow: challenge ambiguous terms, test relationships with concrete scenarios, compare the discussion with implemented behavior, and capture resolved definitions as the work proceeds.

A shared glossary prevents the same word from quietly referring to different concepts. For example, “account” might mean a customer organization, a person's login, or a billing relationship. The skill makes those distinctions explicit before they spread into APIs and product behavior.

## When to use it

Use it when defining or revising codebase terminology, writing a `GLOSSARY.md` or existing `CONTEXT.md`, untangling domain relationships, or recording an architectural decision record (ADR). Merely reading an existing glossary does not require the full workflow.

It can work with one project context or several. In a multi-context repository, a root `GLOSSARY-MAP.md` (or existing `CONTEXT-MAP.md`) identifies where each context lives. New files are created only when there is a resolved term or decision worth recording.

## How it works

1. Read the relevant glossary and identify conflicting or overloaded language.
2. Propose canonical terms and discuss concrete edge cases that expose the differences.
3. Check the code when a claim describes existing behavior; report contradictions rather than assuming either source is correct.
4. Update the established glossary when a definition is resolved, using the supplied format.
5. Record an ADR only for a decision that is costly to reverse, surprising without context, and based on a real tradeoff.

The glossary remains focused on domain language. Implementation decisions belong elsewhere. This keeps a compact vocabulary useful to developers and business participants without turning it into a changing specification or scratchpad.

## Requirements and output

No scripts, packages, or external services are required. Access to the project documents and relevant code is useful; some distinctions require the user or domain owner to clarify intended behavior.

The result is a sharper domain model, updated glossary entries, and selectively created ADRs. The skill does not imply that every routine implementation choice needs a formal decision record.

## Example requests

```text
Use the domain-modeling skill: clarify the difference between a Customer, User,
and Billing Account in this repository and update its glossary.

Use the domain-modeling skill: test partial cancellation against the current
Order model and record the decision if it meets the ADR criteria.
```

## Package guide

- [SKILL.md](SKILL.md): modeling workflow and criteria for recording decisions.
- [GLOSSARY-FORMAT.md](GLOSSARY-FORMAT.md): format for new glossaries.
- [CONTEXT-FORMAT.md](CONTEXT-FORMAT.md): format retained for existing context files.
- [ADR-FORMAT.md](ADR-FORMAT.md): decision-record format.

[Codebase Design](../codebase-design/README.md) covers module interfaces; [Repo Context](../repo-context/README.md) covers repository navigation. Install by copying this directory into any [Agent Skills](https://agentskills.io)-compatible location, for example `cp -R domain-modeling ~/.agents/skills/` (see [INSTALL.md](../../INSTALL.md) for each host's folder). Compatible agents select it automatically when a request matches its description, or you can name it explicitly ("use the domain-modeling skill").

## Upstream update — 2026-10-09

New domain glossaries use `GLOSSARY.md` and `GLOSSARY-MAP.md`. Existing `CONTEXT.md` records retain their paths and format; ordinary modeling work does not migrate or duplicate them. See [provenance](references/provenance.md) for the pinned original source.
