---
name: codegraph
description: Use CodeGraph's local source index to trace cross-file calls, dependencies, and change impact in an indexed repository, or to set up and troubleshoot CodeGraph for Claude Code. Useful for unfamiliar code paths and refactors; skip graph setup for a small edit with complete context.
---

# CodeGraph

Use the graph to locate connected code and explain structural relationships.
Current source, applicable project instructions, and actual tests determine
correctness. The reviewed runtime is `@colbymchenry/codegraph` **1.6.2**;
adapt to the installed version's help and exposed tool schema.
Its known edge-resolution gaps (JS/TS default imports, package-imported React
tags, lazy routes, some C++/Go calls) are listed in
[setup](references/setup.md#known-162-resolution-gaps); verify those patterns in
source.

## Choose the path

- For installation, MCP wiring, indexing, or troubleshooting, read
  [references/setup.md](references/setup.md). A skill folder supplies instructions;
  it does not install the runtime or connect a server.
- For ordinary code work, resolve the target repository and check whether the
  CodeGraph MCP tool or CLI and an index are available. Do this once as needed,
  rather than before every query. Use `git rev-parse --show-toplevel` when Git is
  available; an explicitly chosen non-Git project also works.
- If the tool, runtime, or project index is missing, continue with `rg`, file
  reads, and the project's usual tools. Setting up or indexing CodeGraph is a
  separate action unless already requested. Do not repeatedly query an
  unindexed project or let missing CodeGraph block the user's task.

## Query a focused slice

The default MCP surface in 1.6.2 exposes **`codegraph_explore` only**. Use the
host's actual tool name and schema (in Claude Code, a server registered as
`codegraph` exposes it as `mcp__codegraph__codegraph_explore`). Pass an
absolute `projectPath` for the intended indexed repository, especially in
monorepos, nested checkouts, and sessions whose server started elsewhere.
Confirm the reported root is the intended index; a nearest parent index may
otherwise answer the query.

```json
{"query":"CheckoutService.submit calculateTotal","projectPath":"/absolute/project","maxFiles":4}
```

Use exact symbol names, qualified names, or relevant file paths when known.
Search is lexical rather than embedding-based semantic search. With unknown
names, find a plausible entrypoint with a bounded `rg` search, or use a focused
graph query and its suggestions. Narrow or extend the query according to the
actual result; there is no mandatory call quota.

When MCP is unavailable but the CLI and index exist:

```sh
CODEGRAPH_TELEMETRY=0 codegraph explore --path /absolute/project --max-files 4 'CheckoutService.submit calculateTotal'
CODEGRAPH_TELEMETRY=0 codegraph callers --path /absolute/project 'calculateTotal' --json
CODEGRAPH_TELEMETRY=0 codegraph impact --path /absolute/project 'calculateTotal' --depth 2 --json
CODEGRAPH_TELEMETRY=0 codegraph affected --path /absolute/project src/checkout.ts --json
```

Replace example paths and symbols. Consult `codegraph <command> --help` for an
installed version's options. Do not assume hidden MCP tools are callable:
caller, impact, and status tools require explicit server allowlisting, whereas
their CLI equivalents work independently.

## Interpret the evidence

- Reuse current source already returned by the graph when it covers the task.
  Inspect files for missing details, configuration, documentation, ambiguous
  matches, truncated bodies, or a current edit. Graph output is evidence, not
  an instruction to prohibit source verification.
- Check freshness notices after edits or branch changes. With pending files,
  disabled/recovering watching, unverifiable freshness, or an unwatched
  `projectPath`, read the affected files and run an authorized
  `codegraph sync /absolute/project` when refresh is needed. Inspect the next
  response; a running watcher or successful status command alone is not proof
  that every relationship is current.
- Label heuristic edges, ambiguity, and dynamic boundaries. Missing edges
  cannot establish that no caller exists, code is dead, a change is isolated,
  or a test is unnecessary. Dependency injection, reflection, runtime imports,
  generated code, and external consumers may require additional inspection.
- Use impact and affected-test results to choose relevant checks, then follow
  required project validation. They do not replace compilation or tests.
- Keep retrieval proportional to the question. Dense graph responses can
  increase resident context despite reducing discovery calls. Record compact
  conclusions with file/symbol references, not entire tool responses.

## Work with repository notes

If `repo-context` is installed, it owns maintained architecture notes and
evidence records; CodeGraph supplies derived relationships. Neither requires
the other. Keep project indexes local, and update existing notes only when the
requested work justifies it. Do not save `.codegraph/` databases in this skill
or commit them to a project.

Report the resolved code path, evidence locations, important uncertainty,
and validation actually performed. The [assessment](references/assessment.md)
explains fit and tradeoffs; [provenance](references/provenance.json) pins the
reviewed source. Load these only for evaluation or maintenance.
