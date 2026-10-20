# Benny on any host

Benny is pstack's optional issue-triage and bounded reproduction/fix pack. The
entire [original pack](upstream/automations/benny/README.md) is preserved. Installing
this skill does not enable Benny, connect services, or create schedules. The
original pack runs on Cursor Automations and upstream describes it as Cursor-only;
on another host its triggers, wakes, and schedules need that host's own scheduling
and must be requested and authorized explicitly.

Use [Host runtime adaptation](host-runtime.md), then read the relevant source:

- [Setup](upstream/automations/benny/skills/setup-benny/SKILL.md.source).
- [Triage](upstream/automations/benny/skills/triage-issue-reports/SKILL.md.source).
- [Reproduce and fix](upstream/automations/benny/skills/reproduce-and-fix-issues/SKILL.md.source).
- [Configuration](upstream/automations/benny/templates/configuration.example.yaml).
- [Control adapter](upstream/automations/benny/skills/reproduce-and-fix-issues/references/control-adapter.md).
- [Verify existing fixes](upstream/automations/benny/skills/reproduce-and-fix-issues/references/verify-existing-fix.md).
- [Routing example](upstream/automations/benny/skills/triage-issue-reports/references/routing.example.md).

## Setup

Resolve repository/default branch, exact source/optional operations channels,
tracker target, routing, app-control adapter, feature map, budgets, identities,
and authorized external actions. Validate actual capabilities and runtime targets.
Missing/uncertain required configuration prevents writes; never guess identifiers.

Keep secret-free project configuration and feature/routing maps outside the
retained pack, for example `.agents/benny/`. This is project data, not a host
settings schema. Merge existing configuration while preserving local edits.
Use supported secret storage/runtime environment, never committed credentials.
Do not add Cursor plugin settings.

Use native workflows or a project-local skill wrapper. Verify the
execution environment can read configuration, source, and feature maps. Remote runs cannot
use local-only paths; install/commit suitable dependencies there before enabling.

Create/change future work only on request, using the host's scheduling:
cloud routines, automations, or OS cron running the agent headlessly. Inspect
existing routines and jobs before creating duplicates. Do not use `/automate`
or claim Slack event triggers when only scheduling is available. For scheduled
polling, persist cursors/idempotency records in project-owned storage with one
coordinator. Keep notification preferences in the routine or job settings.
Stay quiet on unchanged/non-actionable runs unless periodic status was requested.

## Triage

Freeze exact source channel and root-thread coordinates from configured input.
Confirm the channel is allowed, the root is accessible, and a permalink exists
before tracker writes. Read relevant replies/media and trace enough source/history
to avoid misrouting a symptom. Label hypotheses.

Classify bug, performance, feature request, question/feedback, or reroute.
Apply configured routing/ping rules. Dedupe by source permalink, signature,
trigger, symptom, and history. Uncertain matches do not earn new tickets.
Resolve tracker fields and confirm compensation is possible if Slack handoff fails.

Create only for clear new live defects passing every original creation gate.
Recheck the source root immediately before the one substantive verdict reply,
when posting is explicitly authorized. Never post a root message, cross-post,
broadcast, DM, or switch coordinates. One coordinator posts; workers return
read-only evidence without credentials. If isolation cannot enforce it, work locally.

## Reproduce and fix

Select only eligible triaged work under configured wait/budget limits. Read
the issue, thread/media, feature map, and control adapter. Confirm build/environment.
Check merged commits and open PRs for existing fixes and verify those on the
current surface before duplicating implementation.

Observe failure through relevant mapped entry points and preserve before evidence.
Root-cause and make a bounded fix, use a cheap red-first test when appropriate,
then rerun the exact trigger on the same surface and preserve after evidence.
Missing or inconclusive proof is blocked. Open a bounded draft PR only after
proof and within authorization. Link created PRs. Do not merge or deploy.

Status/operations messages require authorization and exact configured destinations.
Keep rejection, follow-up, fix, and polling limits bounded. Inspect existing
records before resuming partial external writes instead of retrying blindly.
