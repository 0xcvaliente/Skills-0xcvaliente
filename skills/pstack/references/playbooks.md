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
if the host offers them. A PR with more than 100 review threads needs paginated
thread reads; the retained watcher was fixed for this, so a hand-rolled query must
page too.

Inspect current head, mergeability, required checks, reviews, and unresolved
threads. Work the lowest unmerged dependency first. One owner coordinates a
stack; unrelated workers do not rewrite topology. Batch validated fixes.
Classify CI failures before retriggering; one evidenced infrastructure retry
differs from repeatedly retrying code failures. Validate bot reports. Posting
replies follows message authorization. Stop at merge-ready unless merge is authorized.

## Shipping

Confirm merge scope and user-owned gates. Use the project's forge CLI or
integration (GitHub by default); never require Graphite or any particular stacking tool.
Verify each PR at its exact current head with relevant behavioral proof, checks,
and review. Only a verdict from a reviewer or verifier that did not write the
code counts, because an author checks what it meant to build. Green CI and a bot
approval are inputs, not a verdict. Land only the contiguous verified run
from the root in dependency order, one PR at a time, bottom first; a verified
PR above an unverified one waits. Read each PR back after merging, since a
merge queue can report success while only queueing, and a requested auto-merge
is not a merge. Changed patches need renewed verification. A pure rebase
preserves evidence only after checking patch equivalence (for example
`git patch-id`) and affected dependencies; CI/mergeability still reflect the new
head. After a merge, retarget the next PR to trunk and push the rebased patch
with force-with-lease only where those rewrites are authorized. Leave the
stack alone while it lands, stop at the ceiling of the verified run, and respect protections.

## Autonomous run

State the completion predicate and boundaries. Iterate the smallest evidenced
change, verification, and decision-log checkpoint until done or genuinely blocked.
Use a host scheduled routine or cron for requested later wakeups. Do not promise
persistence from an active turn; an in-session loop recurs only while the session is open.

## Orchestrate

For an authorized program, the coordinating chat decides which agent does each
piece of work and checks what each one produces; it does not author code, and it
runs this playbook itself rather than handing it to a delegate. It keeps state in
a tracker file and store, subscribes to PR and CI events when the host has them,
calls no scripts, runs no polling loops, and does not relay messages between
agents. One owner per PR is the only writer of its branch (pushes, rebases,
retargets); conflicted merges, chain rebases and fixes go to owners. Give each
independent task a fresh worker whose kickoff carries everything it needs (goal,
paths it may and may not write, forbidden actions, each upstream report in full,
and the evidence that proves it done). Add a sub-coordinator only when one area has
many parallel workers, stop at three levels, and keep about ten workers in flight per
coordinator. Give each PR a verifier that is not its author, on a different model
family where available; merge only on a pass at the current head. Start with one
unit through kickoff, owner, verifier and merge before fanning out. Read the diff or
artifact rather than a summary; green CI is an input, not a verdict, and a verdict
covers one head SHA. Send back drift from scope, check a PR's live state with the
forge CLI before reporting, stop or replace a stalled worker by its pushes and PR
activity, and ask the user only for a real decision or blocker. Choose each
delegate's reasoning effort and speed for the job (see the runtime notes).
Count commits, PR changes, and artifacts as progress. Preserve a stuck worker's
state before replacement. Standing cadence needs a requested host scheduled routine
or in-session loop, not an assumed Cursor cloud fleet.

## Autopilot-full

Requires execution scope covering the independent queue and intended merges.
Stating a plan does not start execution. Keep one owner/branch per independent
change. Verify code-ready heads, inspect artifacts, absorb relevant base drift
(including a known concurrent change to the same files),
and recheck CI/mergeability before authorized merges. Preserve operator gates;
stop all writes on a hold instruction. Every later change to a verified patch
needs a fresh check, except that a wording-only change needs no verifier. Block a PR
only for a problem you can show (a failing run at the head, or a doc line the PR
made wrong); a problem its base already has does not block unless the PR copies it or
newly reaches it, and everything else goes in a follow-up. Write the final reply as a
`ketchup` catch-up: each PR's state and verdict, what merged, countersigns, every open
operator gate as a call with your pick, parked follow-ups, and links.

## Autopilot-stack

Autopilot-full without the merge. Build and verify the queue of PRs with the same
owners, stop when each PR is verified and green at its current head, and hand them
to the user to land; after the handoff nobody pushes without the user's go. Stack a
PR only when it builds on another PR: base it on that PR's branch, rebase it onto
its parent, and rebase the stack root onto trunk. A new head on a lower PR restacks
those above it, and a PR whose patch-id is unchanged keeps its verdict. Write the
final reply as a `ketchup` catch-up listing each PR with its verdict. Do not merge or
arm auto-merge. Rewrites still require authorization even when using
force-with-lease.

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
untracked, ignored, unpushed, and nested-repository work. Check PR/merge evidence
against the branch PRs actually merge into (the retained auditor takes a base ref
and otherwise assumes the remote's default branch);
age or a closed PR does not prove disposability. For requested managed cleanup,
use the host's managed-worktree tools and preserve needed ignored files separately. Do
not prune other chats' work or remove simulators incidentally.

## Opening a PR

Use only when publication is requested or already authorized. Inspect the final
diff and meaningful checks. Describe the concrete problem, resulting behavior,
validation, and gaps using repository conventions. Pass multiline prose as
structured data or a body file. Confirm the URL, report it, and attach the PR
through the host's PR tool when one is available.
