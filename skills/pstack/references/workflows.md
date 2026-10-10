# Native workflows

Use [Claude Code runtime adaptation](claude-runtime.md), then read the selected full
source and supporting prompts through the [catalog](catalog.md). These sections
replace host mechanics while retaining pstack's engineering methods.

## poteto-mode and poteto-help

`poteto-mode` selects a playbook and relevant principles. `poteto-help` answers
the immediate usage question and supplies a concrete `/pstack <workflow>
<task>` prompt. Explain capabilities and missing dependencies as needed. No
global persistent mode or mandatory setup is implied.

## how

Trace real entry points, data flow, owners, layering, lifetimes, and exits.
Ground the walkthrough in files and symbols. Separate exploration/explanation
passes when useful, using retained prompts for substantial subsystems. Delegate
to subagents only when authorized. Answer placement questions from callers and boundaries.

## why

Inventory available evidence sources. Search relevant source control, issues,
documents, chats, observability, errors, or analytics only when accessible and
in scope. Use retained source playbooks and epistemic guidance. Distinguish
documented intent, mechanism, inference, conflict, and missing evidence. Return
citations and tradeoffs. Missing connectors are coverage gaps; independent
source readers are conditional on authorization.

## recall

Pin topic, project, and time window; default to seven days for unspecified
recent work. Use the current conversation and relevant Claude Code session
transcripts (see the runtime mapping), reading deeper only as needed.
Sweep shared records through `why` for the named topic and verify branches/PRs.
Return a compact capsule, per-thread status, recurring problems, and next action.
Do not replace an explicit all-history request with a narrow window.

## teach

Combine `how` and `why` into an explanation built from concrete behavior to
mechanisms and tradeoffs. Use diagrams/examples when helpful. Ground facts in
source and keep unknown historical intent explicit.

## blast-radius

Inventory consumers, callers, persistence formats, lifetime/ownership boundaries,
and alternate entry points beyond the diff. Identify the load-bearing safety
assumption and try to disprove it with an executable probe. Report tested
protection and uncovered paths. Static assertions are not runtime proof.

## architect

Start with caller usage, domain types, signatures, and module ownership. Read
the retained design-red-flags checklist and rationale template. Compare shapes
when the boundary is consequential; use arena only with authorized parallelism.
Prefer designs whose local examples guide contributors toward globally correct
use. Revisit the design as implementation reveals real constraints.

## arena

Define a common brief and judge-only rubric. Give authorized candidates isolated
writable locations and the same organic request. Wait for outputs before
judging under sanitized labels. Select a base and graft demonstrated strengths
from alternatives. Read every artifact and verify the synthesis. Use different
models only when available and chosen. Label serial alternatives accurately
when parallel agents are unavailable.

## swarm

Define coverage, race, gauntlet, or exploration slices, each with an invariant,
proof contract, and write ownership. Respect concurrency. Drain results, resolve
contradictions, and return one report. Keep losing race artifacts recoverable
until the winner is verified. Run workers through the Agent tool; do not start
separate user sessions as subagent substitutes.

## interrogate

Pin the diff and connected code. Assign skeptical lenses such as correctness,
lifetimes/concurrency, consumer compatibility, and code quality using retained
reviewer prompts/rubric. Review independently when authorized; label serial
review otherwise. Validate findings and distinguish confirmed defects from
hypotheses. Report findings by default; edits require an implementation request.

## tdd

Use for explicit TDD/regression tests or a defect with a cheap local test.
Observe the failure first, make the smallest correction, and rerun it plus
relevant checks. Assert literal user-visible results rather than mirroring the
implementation. Avoid inventing integration infrastructure for an unclear test path.

## benchmark-checklist

Identify the limiter and prove the intended work happened. Check tuning,
resource caps, warmup, caches, errors, repetitions, variance, and comparable
inputs. Explain a microbenchmark's relationship to end-to-end behavior. Report
workload and uncertainty with the number.

## typescript-best-practices

Read retained patterns for typed boundaries and state models. Make invalid
states unrepresentable, exhaust variants, derive types from schemas, and parse
external data at boundaries. Avoid casts/suppressions hiding real mismatches.
Fit the installed TypeScript version and project conventions.

## no-comments

Use retained Comment Sicko criteria without its theatrical opening or a deletion
quota. Keep legal headers, API contracts, verified external constraints, and
useful issue/RFC rationale. Remove narration, dead code, and stale claims.
Inspect rules and behavior before deleting warnings/suppressions. Identify
structural fixes for underlying surprises. Report first unless cleanup was requested.

## unslop, bro, and technical-writing

Unslop tightens requested prose without losing evidence/meaning. Bro restates
the last response plainly. Technical-writing uses the retained layered standard
to match reader/task, choose document type, order explanations, and write precise
instructions. Preserve terms, links, and requirements. Do not impose pstack
punctuation rules on unrelated tasks or user-owned copy.

## show-me-your-work

Append consequential decisions to a local TSV with phase, decision, reason,
evidence, and result using `scripts/decision-log.sh`. Keep separate logs per
concurrent writer. Commit only when the task's audit needs and conventions
warrant it, and sanitize private information before publication.

## figure-it-out

For unmatched work, define a bespoke sequence around outcome, uncertainties,
dependencies, evidence gates, and stopping conditions. Experiment on empirical
forks, log decisions, and revise hypotheses when observations disagree. Use a
simpler bundled route when it fits.

## create-verification-skill

Inspect how the project starts, resets, authenticates, and can be driven. Reuse
its harness. Write a project-local `verify-<app>` skill in Claude Code's project
skill directory (`.claude/skills/verify-<app>/SKILL.md`) or the user's chosen
location, using a skill-creator skill if one is installed. Include doctor/start/reset, driving commands,
proof capture, cleanup, and an observed feature map. Adapt retained examples.
Exercise a real feature before claiming the verifier works.

## maintain-verification-skill

Compare the verifier/feature map with source, then run a live pass across
relevant entry points. Partition source readers only when authorized. Make
evidenced corrections, preserving conventions. Use at most one maintenance PR
when publication is requested. Missing access remains a verification gap.

## setup-pstack

Use optional project configuration from Claude Code runtime adaptation. Inspect
existing choices/capabilities; default roles to inherit. Resolve only material
missing preferences for delegation, supported models, or verification commands.
Preserve unrelated settings. Explain that the file is workflow data, not a
Claude Code setting such as `settings.json` or `/model`.

## automate-me

Create/update a personal working-style skill; the name alone does not request
scheduling. Find an existing matching skill. Use explicit preferences and relevant
accessible history, separating durable habits from one-off corrections. Remove
duplicated policy and author it as a Claude Code skill (`~/.claude/skills/<name>/`
personal, `.claude/skills/<name>/` project), using a skill-creator skill if
installed. Preserve requested placement and invocation policy. Do not scan unrelated history or invent persistent modes.

## reflect and correct

Reflect extracts concrete lessons and routes narrow improvements to existing
skills/tools. Retained tooling, judgment, divergent-review, and synthesis prompts
provide lenses; delegation follows native rules. Correct fixes recurring mistake
classes at the strongest useful level: architecture, types, lint, tests, then
docs. Prove enforcement catches a real example. Avoid universal rules from one incident.

## make-bot-ui

The original targets a specific Cursor/Grok Bot webhook service. Claude Code
`/schedule` routines and `/loop` do not provide its webhook or secret-request card. Identify an available service
and actual credential flow first. Without one, explain the dependency and build
only the requested reviewable UI/server integration boundary.

Keep credentials server-side and payloads untrusted. Verify the real request
contract. Never invent Cursor URLs or put secrets in chat/client code. Use
project deployment/private-network conventions; do not install Tailscale or
expose listeners incidentally. Test a harmless authorized payload before claiming
the bot wakes. External messages still need authorization.
