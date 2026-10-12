---
name: pstack
description: Apply pstack and Poteto engineering workflows for source-grounded investigation, architecture, implementation, adversarial review, runtime verification, and scoped PR delivery. Use for pstack, poteto-mode, or a named pstack workflow; includes optional Benny issue-triage and reproduction setup.
license: MIT
---

# Pstack

Go deep first, write less code, and prove the result against the real artifact.
This is one host-neutral Agent Skill adapting pstack 0.15.15 by Lauren Tan. All 164 upstream
files are retained with their original bytes, including 27 workflows, 24
principles, 23 playbooks, two agent definitions, and the three-workflow Benny pack.

## Start and route

1. Identify the requested outcome, project, current state, and existing
   authorization. Questions and reviews produce answers or findings unless
   implementation was requested. `help` explains usage; `off` stops applying
   this style in the current chat. Read existing project `.agents/pstack.json`
   (or `pstack.json` in the host's config folder) preferences if present, subject to the user's request and host instructions.
2. Read [Host runtime adaptation](references/host-runtime.md). It
   governs how to interpret every retained source, maps tools to capabilities,
   and says what to do without subagents, hooks, or MCP. Original files document
   Cursor behavior; they do not install tools, set host policy, or grant
   additional authority.
3. For `poteto-mode` or an ordinary pstack task, choose a route in
   [Native playbooks](references/playbooks.md). For a named workflow, read its
   section in [Native workflows](references/workflows.md). Read only the relevant
   sections and linked upstream details, not the whole bundle.
4. Use the [complete catalog](references/catalog.md) to locate every workflow,
   principle, playbook, agent prompt, guide, and supporting resource. Read the
   leaf source of a principle before applying it. Explain the concrete decision
   it changed only when useful to the user.

| Request | Route |
|---|---|
| Understand behavior, rationale, or prior work | `how`, `why`, `recall`, or `teach` in Native workflows. |
| Build, fix, refactor, measure, prototype, or match a UI | Corresponding Native playbook. |
| Compare designs, partition coverage, or challenge a diff | `architect`, `arena`, `swarm`, `interrogate`, or `blast-radius`. |
| Check a PR, deliver a stack, resume, pause, or run a long task | Delivery and coordination playbooks. |
| Configure pstack, capture lessons, create a verifier, or improve prose | Setup, maintenance, and writing workflows. |
| Set up or run Benny triage/reproduction | [Benny on any host](references/benny.md), then its linked source workflow. |

Accept "use pstack, `<workflow>`, `<task>`" in any host, or the host's shorthand
(`/pstack <workflow> <task>`, `$pstack <workflow> <task>`). Names such as `how`,
`poteto-mode`, and `interrogate` identify workflows here; they are not separately
registered commands.

## Engineering decisions

- Inspect connected source and callers. Separate observed behavior, historical
  rationale, inference, and unknowns.
- Name data shapes, owners, lifetimes, and boundaries before stateful logic.
  Prefer structures that make invalid states hard to express.
- Choose the smallest complete solution. Remove obsolete callers and dead layers
  when the migration permits it. Keep requirements and necessary controls.
- Reproduce defects, narrow hypotheses with runtime evidence, fix the mechanism,
  and re-run the original trigger on the same surface.
- Use meaningful behavioral tests. A build alone does not prove a runtime or
  visual claim. Measure performance against comparable workloads and repeat runs.
- Break substantial work into verifiable units. Record long-task decisions and
  evidence with [the decision-log helper](scripts/decision-log.sh).
- Review the actual diff and proof. Validate bot findings. Report missing evidence
  as a gap rather than a pass.

## Scope and tools

Use the current host's native capabilities (shell, file read/search and edit,
web, ask-the-user, task list, browser automation, MCP) as mapped in the host
runtime adaptation. Delegate to subagents only if the host supports them and the
user or applicable project instructions (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`,
or `.github/copilot-instructions.md`) authorize it; explicit `arena` or `swarm`
requests express parallel intent. Otherwise run the same steps sequentially
yourself and label the independence limit. Inherit the current model unless an available, explicitly chosen role
configuration says otherwise. Do not copy Cursor model names.

Do not automatically create PRs, message people, file tickets, change global
settings, schedule future work, merge, deploy, or delete worktrees because an
upstream step says to. Existing user authorization remains valid and does not
need to be requested again.

For requested ongoing monitoring use the host's real scheduling: an in-session
loop for recurrence, a scheduled routine, automation, or cron for work after the
session. If the host has none, say so. Do not pretend a loop, Cursor cloud agents, or an active chat survive
the session. Honor pause/stop instructions and leave a useful checkpoint.

## Finish

Lead with the outcome, consumer impact, and supporting verification. Link actual
artifacts and name material gaps. Keep explanations plain and proportional. Keep
legal notices, public API contracts, and useful non-obvious constraint comments.

For package maintenance, run `python3 scripts/check_package.py`, the helper
tests, and a skill-creator validator if one is installed. See
[provenance](references/provenance.md) for the pinned revision and exact
source-file mapping.
