# Native playbooks

Choose the smallest matching route. Keep meaningful steps in the todo list for
substantial work. Use [Host runtime adaptation](host-runtime.md), then
read the complete selected source playbook through the [catalog](catalog.md)
for detailed guidance.

## Investigation

Pin the question and subsystem. Trace behavior with `how`, historical motivation
with `why`, and test load-bearing claims when feasible. Return a cited answer
and uncertainties. Keep a question read-only unless changes were requested.

## Bug fix

Reproduce on the affected surface. Narrow hypotheses with source, history, and
runtime instrumentation until the mechanism is observed. Design the smallest
root-cause fix, including callers and lifetimes. Add a cheap behavioral regression
test when useful. Re-run the original trigger on the same surface. Missing
reproduction is a gap, not a pass. Deliver code and evidence.

## Perf issue

Record workload, build, limiter, metric, and a repeatable baseline. Profile the
actual slow path. Change the evidenced bottleneck and repeat comparable
measurements, including errors and end-to-end impact. Apply benchmark-checklist
before reporting a speedup.

## Hillclimb

Define one metric, target, stopping limits, workload, and correctness constraints.
Log each hypothesis, intervention, and measurement. Keep verified gains and revert
losses. Revisit assumptions at a plateau. Record accepted units in separate
commits when committing is part of the task. Do not relax the target to claim success.

## Runtime forensics

Diagnose the symptom on the correct build. Distinguish allocation, retention,
scheduling, polling, rendering, and resource ownership as applicable. Correlate
concrete observations with the mechanism. Deliver a diagnosis and verification
path; implement a fix only if requested.

## Trace forensics

Identify artifact format, capture window, workload, and sampling limits. Read
the trace/profile with appropriate tools. Distinguish self/inclusive time,
waiting, and repeated work; connect frames/events to source. Report evidence
and confidence limits without inventing unseen runtime state.

## Feature

Trace the subsystem and settle caller-facing data shapes, ownership, interfaces,
and failures. For substantial work identify dependencies, independent slices,
shared writers, and proof for each slice. Build with project patterns and the
requested UX. Verify real entry points and relevant tests. Compare alternatives
when they materially change the result. Delegation follows native runtime rules.

## Refactoring

Define behavior to preserve and inventory callers/boundaries. Migrate connected
callers and remove obsolete internal APIs in the same verified wave where
feasible. Check behavior and public compatibility obligations. Avoid temporary
adapters for intermediate states the project does not need.

## Prototype

Name the empirical question and cheapest observable experiment. Isolate disposable
work. Compare competing shapes when useful and preserve the reason for the
choice. Product preferences remain with the user when observation cannot decide them.

## Visual parity

Pin reference, viewport, theme, state, content, fonts, and build. Capture both
implementations in matching conditions. Compare layout, typography, spacing,
color, and interaction states. Iterate with rendered evidence. Report unmatched
states or missing references instead of declaring pixel parity.

## Authoring a skill

Follow Agent Skills conventions (`SKILL.md` with `name` and `description`
frontmatter), using a skill-creator skill if installed. Keep selection metadata
precise and conditional detail in linked references. Validate frontmatter and resources. Test changed helpers
and meaningful behavior when warranted. Install/publish to requested destinations.

## Eval

Define observable success and a judge-only rubric. Use the same organic prompt
in isolated environments. Hide model labels and intended answers from judges.
Inspect raw outputs and available tool evidence, not self-reports. Parallelism
requires authorization and capability. Label serial/same-model evaluation accurately.

## Babysit

Declare `check`, `threads-only`, `drive`, or a requested background monitor.
`Check on PR` means one status pass; `threads-only` limits work to review
feedback; `drive` resolves authorized blockers until merge-ready. Requested
monitoring uses the host's in-session loop or a scheduled routine/cron beyond it,
if the host offers them.

Inspect current head, mergeability, required checks, reviews, and unresolved
threads. Work the lowest unmerged dependency first. One owner coordinates a
stack; unrelated workers do not rewrite topology. Batch validated fixes.
Classify CI failures before retriggering; one evidenced infrastructure retry
differs from repeatedly retrying code failures. Validate bot reports. Posting
replies follows message authorization. Stop at merge-ready unless merge is authorized.

## Shipping

Confirm merge scope and user-owned gates. Verify each PR at its exact current
head with relevant behavioral proof, checks, and review. Recheck mergeability
and base drift immediately before merge. Land only the contiguous verified run
from the root in dependency order. Changed patches need renewed verification.
A pure rebase preserves evidence only after checking patch equivalence and
affected dependencies; CI/mergeability still reflect the new head. Respect protections.

## Autonomous run

State the completion predicate and boundaries. Iterate the smallest evidenced
change, verification, and decision-log checkpoint until done or genuinely blocked.
Use a host scheduled routine or cron for requested later wakeups. Do not promise
persistence from an active turn; an in-session loop recurs only while the session is open.

## Orchestrate

For an authorized program, maintain dependencies, owners, branch/worktree
pointers, exact heads, proof, and operator gates. Partition writes and respect
concurrency. Count commits, PR changes, and artifacts as progress. Preserve a
stuck worker's state before replacement. Standing cadence needs a requested
host scheduled routine or in-session loop, not an assumed Cursor cloud fleet.

## Autopilot-full

Requires execution scope covering the independent queue and intended merges.
Stating a plan does not start execution. Keep one owner/branch per independent
change. Verify code-ready heads, inspect artifacts, absorb relevant base drift,
and recheck CI/mergeability before authorized merges. Preserve operator gates;
stop all writes on a hold instruction.

## Autopilot-stack

Build and verify a dependent queue as one linear stack for the user to land.
One coordinator owns topology; implementers own slices. Record exact parents
and heads. Re-verify affected proof after conflicts or patch changes. Deliver
ordered PRs and evidence. Do not merge or arm auto-merge. Rewrites still require
authorization even when using force-with-lease.

## Session pickup

Read the state capsule or relevant accessible prior chat. Inspect artifacts,
branch, worktree, dirty files, processes, and checks. Distinguish planned,
attempted, verified, and published work. Carry later corrections and boundaries
forward; verify prior done claims against actual state.

## Pause safely

Stop new writes. Record goal, branch/worktree, dirty files, heads, processes or
workers, evidence, blockers, and next move. Stop/handoff owned processes as
appropriate without deleting recoverable work. Pause scheduled activity when
part of the user's request and report actual status.

## Multi-phase plan

Order phases by dependencies and user-visible proof. Name files/ownership, build
work, observable behavior, tests, live verification, applicable performance
measures, and delivery gates. Keep inapplicable checks explicit. Scale lanes to
the actual task; ten agents and performance boxes are not universal requirements.

## Worktree cleanup

Inventory attached managed and ordinary Git worktrees. Inspect tracked,
untracked, ignored, unpushed, and nested-repository work. Check PR/merge evidence;
age or a closed PR does not prove disposability. For requested managed cleanup,
use the host's managed-worktree tools and preserve needed ignored files separately. Do
not prune other chats' work or remove simulators incidentally.

## Opening a PR

Use only when publication is requested or already authorized. Inspect the final
diff and meaningful checks. Describe the concrete problem, resulting behavior,
validation, and gaps using repository conventions. Pass multiline prose as
structured data or a body file. Confirm the URL, report it, and attach the PR
through the host's PR tool when one is available.
