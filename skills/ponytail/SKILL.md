---
name: ponytail
description: >-
  Apply Ponytail's smallest-complete-change approach to coding tasks,
  bug fixes, refactors, dependency choices, and over-engineering reviews.
  Also handles Ponytail lite/full/ultra modes, change reviews, repository
  audits, and shortcut ledgers. Use for "ponytail", "simplest
  solution", "YAGNI", or reducing code bloat. Does not activate for unrelated
  prose or creative work.
license: MIT
---

# Ponytail

Solve the whole problem with the least new code a reader can understand.
Read enough to know what a complete solution requires before choosing how
small it can be. Adapted from [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail).

## Select the request

Name the skill ("use the ponytail skill: …"; hosts may also offer a `/ponytail` or `$ponytail` shorthand) or let the host select it automatically. The words after it select the workflow; they are arguments to
this skill, not separate commands.

| Request | Action |
|---|---|
| A coding task, optionally `lite`, `full`, or `ultra` | Apply the coding workflow below. Default to `full`. |
| `review` with a diff, branch, PR, or files | Read [review and audit](references/review-and-audit.md), then report on that change. |
| `audit` with a repository or folder | Read [review and audit](references/review-and-audit.md), then assess the named scope. |
| `debt`, `debt <marker>`, or "list the shortcuts" | Read [shortcut ledger](references/debt.md). |
| `gain` or "what does Ponytail save?" | Read [benchmark context](references/benchmark.md). Attribute the published figures and their limits. |
| `help` | Explain this table and the levels briefly, using "use the ponytail skill: …" examples. |
| `off`, "stop ponytail", or "normal mode" | Stop applying this skill in the current chat until the user resumes it. |

Treat a user-selected level as a preference in the current chat while that
context is available. A one-shot review, audit, debt, gain, or help request
does not change the level. Installation supplies instructions; it does not
guarantee activation in every future turn or install lifecycle hooks. Do not
write global settings, mode files, or project instructions to emulate that.

## Before editing

Read the task, repository instructions, and connected code. Trace the actual
input, state changes, and output. Identify every affected caller, test,
fixture, configuration value, and export. For bug fixes, use `rg` to find
callers of the shared function before fixing the root cause.

Check what could break: exposed or destroyed data, changed contracts, and
behavior existing users depend on. Those consequences define required work;
unrequested features do not. A broad request gets the smallest version that
fully serves the stated need. Preserve specific requirements and the
project's architecture and conventions.

## Choose the smallest complete solution

Take the first option that fully meets the requirements:

1. Remove work the need does not justify. Briefly identify a material omission.
2. Reuse an existing helper, component, service, or established project pattern.
3. Use a standard-library or native platform feature when no project equivalent fits.
4. Use a suitable installed dependency before adding another one. A new
   dependency needs a concrete benefit beyond replacing a few clear lines.
5. Write a direct expression when a reader can understand it at a glance.
6. Otherwise write the minimum clear implementation that does the whole job.

Finish the required callers, fixtures, exports, and documentation together.
Prefer deletion when behavior permits it. Avoid speculative wrappers,
abstractions, options, conversions, and configuration. Preserve useful module
boundaries; merging unrelated jobs to shrink a diff is not simplification.
Keep comments for reasons the code cannot express.

Never trade away trust-boundary validation, data-loss prevention, security,
accessibility, required hardware calibration, or requested behavior. Moved or
merged code keeps its error handling. Among equally simple solutions, choose
the one that handles the relevant edge cases correctly.

Run the project's required checks and verification appropriate to the change.
For risky logic, parsers, money, security, or a demonstrated bug, use a focused
regression test or meaningful self-check that detects a wrong result. A
branch alone is not a reason to create a test. Trivial reversible edits and
tests that merely repeat the implementation need no new test. Report a check
that could not run accurately; do not call it passed.

A deliberate shortcut with a known ceiling gets a comment in the project's
syntax: `shortcut: <limit>; revisit when <trigger>; upgrade by <smallest next step>`.
Honor an existing project marker or a request to omit these comments; older
`ponytail:` markers remain valid.
Record only actual accepted limits. A shortcut cannot waive a requirement or
a necessary safety control.

## Levels and replies

| Level | Behavior |
|---|---|
| `lite` | Implement the requested approach. Mention a worthwhile smaller alternative briefly; do not replace the user's choice. |
| `full` | Apply the smallest complete solution. Default. |
| `ultra` | Also challenge parts the need does not justify. Explain a concrete tradeoff, then continue authorized work; honor explicit requirements and an informed user choice. |

Lead with what changed and why, then relevant verification. Keep the reply
proportional to the task. Close with a brief material limitation, skipped
check, or remaining risk when one exists. Do not invent omissions, risks,
line savings, or cost savings to fill a template. A requested review or audit
still receives enough evidence to act on its findings.

For the pinned source revision and deliberate changes, see
[provenance](references/provenance.md).
