# Complete pstack catalog

Read [Host runtime adaptation](host-runtime.md) before using source
procedures. Use [Native workflows](workflows.md), [Native playbooks](playbooks.md),
or [Benny on any host](benny.md) for execution. Every link below points to a retained
original. Source `SKILL.md` filenames are stored as `SKILL.md.source`.

## Workflows

| Name | Full upstream procedure and scope |
|---|---|
| [architect](upstream/skills/architect/SKILL.md.source) | Sketch types, signatures, and module structure before code, then stay in the loop while implementation fills in. Use for /architect, 'architect this', 'design this', or non-trivial work where jumping to code would lock in the wrong shape. |
| [arena](upstream/skills/arena/SKILL.md.source) | Spawn N parallel candidates at the same task, pick a base, graft the strongest parts of the losers into it. Use for /arena, 'arena this', 'throw it in the arena', or when one attempt at a non-trivial artifact would lock in the wrong shape. |
| [automate-me](upstream/skills/automate-me/SKILL.md.source) | Use for "automate me", "create/update/refresh my -mode skill", "turn/capture my preferences or working style into a skill", or wanting agents to follow how the user works. Drafts or revises a personal -mode skill via create-skill + unslop, optionally pulling fresh evidence from recent transcripts. |
| [benchmark-checklist](upstream/skills/benchmark-checklist/SKILL.md.source) | Vet a perf measurement (limiter, tuning, limits, errors, repeatability, relevance, and whether the work happened) before you report or act on it. Use when you run a benchmark or report a speedup or regression you measured. |
| [blast-radius](upstream/skills/blast-radius/SKILL.md.source) | Find what a change could break somewhere else before it ships, beyond the diff, and prove the one fact it's safe because of by running real code instead of writing it up. Use for 'blast radius of X', 'what could this break', or reviewing a small diff you don't trust. |
| [bro](upstream/skills/bro/SKILL.md.source) | Restate the last message in plain human language, with no jargon. |
| [correct](upstream/skills/correct/SKILL.md.source) | Find the mistakes agents keep repeating in this repo and make each one impossible. Try architecture first, then types, then a lint whose error names the fix, then a test, and write docs last. Prove each check fails on a real past mistake. Repeat this each time the operator corrects you. Use for /correct. |
| [create-verification-skill](upstream/skills/create-verification-skill/SKILL.md.source) | Generate a project-local verification skill that drives your app the way a user does — any language, framework, or platform. Use for /create-verification-skill, "make a control skill for this repo", or when a project has no scripted way to prove UI/CLI/service behavior. |
| [figure-it-out](upstream/skills/figure-it-out/SKILL.md.source) | Design an auditable playbook when no narrower one fits: a large migration, an ambitious multi-part change, or work a human reviews after stepping away. Scales rigor to the task, runs a hypothesis loop, and logs decisions via show-me-your-work. Use for /figure-it-out, 'figure it out', a large migration, or when no narrower playbook applies. |
| [how](upstream/skills/how/SKILL.md.source) | Use for "how does X work", code walkthroughs before changing something, and placement / ownership / layering questions ("where should this live", "which package owns this", "is this the right layer"). Explains subsystem architecture, runtime flow, onboarding mental models. Use why for motivation. |
| [in-your-own-words](upstream/skills/in-your-own-words/SKILL.md.source) | Restate in your own words what you think the user's goals are and what problem they're trying to solve. Explicit request only: upstream marks it `disable-model-invocation: true`, which has no effect here, so apply it only when the user asks. |
| [interrogate](upstream/skills/interrogate/SKILL.md.source) | Use for "interrogate", "adversarial review", "multi-model review", "challenge this", "stress test this code", "find blind spots", or "tear this apart". Multiple LLM reviewers challenge changes from independent angles. |
| [ketchup](upstream/skills/ketchup/SKILL.md.source) | Read-only plain-language catch-up on what changed in this chat since the user's last message: under 150 words, small visuals where the host can make them, two lines per action item (the decision with a recommendation, then what happens if the user does not answer; unasked irreversible steps get one). Explicit request only (same frontmatter note as above); autopilot playbooks use it for their final reply. |
| [maintain-verification-skill](upstream/skills/maintain-verification-skill/SKILL.md.source) | Periodic pass that keeps a project's verification skill and feature map honest: parallel source readers per feature, one live session driving every feature, at most one PR of proven corrections. Use for /maintain-verification-skill or "audit the verify skill". |
| [make-bot-ui](upstream/skills/make-bot-ui/SKILL.md.source) | Use when building a custom UI (page, dashboard, buttons) that should wake a Grok Bot over a webhook, when the user must provide a webhook sender key, or when exposing that UI on Tailscale. |
| [no-comments](upstream/skills/no-comments/SKILL.md.source) | Spawn Comment Sicko, fix accepted findings, and offer encodings for claimed constraints. |
| [poteto-help](upstream/skills/poteto-help/SKILL.md.source) | Guides users through pstack setup, /poteto-mode, and picking the skill, playbook, or principle for a task. Type /poteto-help with a question. |
| [poteto-mode](upstream/skills/poteto-mode/SKILL.md.source) | poteto's agent style for concise, detailed responses, deliberate subagents, unslopped prose, simple code, and verified work. Use for poteto, /poteto-mode, or requests to work in this style. |
| [recall](upstream/skills/recall/SKILL.md.source) | Reconstruct your recent working context from your own chat history, live state, and the shared record (user reports, prior fixes, incidents), then hand back a tight current-state brief. Use for 'recall my work on X', 'catch me up', 'what have I been working on', 'where did I leave off', before starting or resuming work. |
| [reflect](upstream/skills/reflect/SKILL.md.source) | Spawn three parallel review subagents over the active transcript, surface learnings, and route each to a concrete edit on an existing skill. Use when the user says reflect. |
| [setup-pstack](upstream/skills/setup-pstack/SKILL.md.source) | Configure which models pstack uses per role and at what reasoning budget. Detects your available models and writes an always-applied rule that overrides the skill defaults. Use for /setup-pstack, "configure pstack models", "pstack budget", or changing pstack's model choices. |
| [sharpen](upstream/skills/sharpen/SKILL.md.source) | Before starting, ask how a top expert would approach the task, what the user is really after, and whether the task is over- or underspecified; fold in only what improves the work and keep one outside check. Explicit request only (same frontmatter note as above). |
| [show-me-your-work](upstream/skills/show-me-your-work/SKILL.md.source) | Keep a reviewable decision trail for long-running or unattended work: a TSV log with one row per decision (what, why, evidence, result). Local by default; commit it when a reviewer needs the trail to trust the result. Use for /show-me-your-work, autonomous or multi-phase runs, or work a human reviews after stepping away. |
| [swarm](upstream/skills/swarm/SKILL.md.source) | Fan out N parallel workers, drain them, and return one report. Use for /swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration. |
| [tdd](upstream/skills/tdd/SKILL.md.source) | Use only when the user explicitly asks for TDD, a failing test, or a regression test, OR when the bug has an obvious cheap local test target. Skip when the test path is unclear, expensive, integration-heavy, or not requested. |
| [teach](upstream/skills/teach/SKILL.md.source) | Explain a body of work plainly so a person actually understands it. Runs the `how` and `why` skills and weaves what they find into one clear explanation. Use for 'teach me this', 'help me really understand X', 'explain this change or subsystem to me'. |
| [technical-writing](upstream/skills/technical-writing/SKILL.md.source) | Layered technical-writing standard: Diátaxis structure, Google developer style sentences, STE instruction rules, Global English syntax. Use for /technical-writing or when writing or reviewing docs, RFCs, readmes, PR descriptions, or commit messages. |
| [typescript-best-practices](upstream/skills/typescript-best-practices/SKILL.md.source) | TypeScript best practices. Use when reading or editing any .ts or .tsx file. |
| [unslop](upstream/skills/unslop/SKILL.md.source) | Cut AI tells from any writing. |
| [why](upstream/skills/why/SKILL.md.source) | Use for 'why does X work this way', 'why we picked Y', design rationale, regressions, postmortems, or data-backed thresholds. Discovers available MCPs and queries each evidence category (source control, issue tracker, long-form docs, real-time chat, infrastructure observability, error tracking, product analytics warehouse) in parallel, then returns a cited read on decisions and tradeoffs. Use how for runtime behavior. |

## Principles

Read the complete leaf when applying a principle.

| Principle | When it applies |
|---|---|
| [attack-the-premise](upstream/skills/principle-attack-the-premise/SKILL.md.source) | Apply when two or more fixes that share one premise have failed the same gate. Take a census of which actors hold the imbalance before the next fix, then question the premise instead of writing another fix that assumes it. |
| [boundary-discipline](upstream/skills/principle-boundary-discipline/SKILL.md.source) | Apply when wiring validation, error handling, or framework adapters. Concentrate guards at system boundaries (CLI, config, network, external APIs); trust internal types and keep business logic in pure functions. |
| [build-the-lever](upstream/skills/principle-build-the-lever/SKILL.md.source) | Apply to any non-trivial work, not just bulk work: edits, migrations, analyses, checks. Build the tool that does it or proves it (codemod, script, generator, or a skill your subagents follow) instead of working by hand. The tool is the artifact a reviewer can rerun. |
| [encode-lessons-in-structure](upstream/skills/principle-encode-lessons-in-structure/SKILL.md.source) | Apply when you catch yourself writing the same instruction a second time, or notice a recurring correction. Encode the rule as a lint, metadata flag, runtime check, or script instead of more text. |
| [exhaust-the-design-space](upstream/skills/principle-exhaust-the-design-space/SKILL.md.source) | Apply when facing a novel UI interaction or architectural decision with no precedent in the codebase. Build 2-3 competing prototypes and compare side by side before committing. |
| [experience-first](upstream/skills/principle-experience-first/SKILL.md.source) | Apply when product, UX, or feature-scope tradeoffs come up. Choose user delight over implementation convenience; ship fewer polished features over more rough ones. |
| [explain-the-number](upstream/skills/principle-explain-the-number/SKILL.md.source) | Apply before you trust, report, or act on a number you measured: a speedup, a regression, a throughput, a latency, or an eval result. Find what limits it, and rule out that it measured something other than the work you think. |
| [fix-root-causes](upstream/skills/principle-fix-root-causes/SKILL.md.source) | Apply when debugging. Trace each symptom to its root cause and fix it there; reproduce first, ask why until you reach it, resist nil-check guards that silence crashes. |
| [foundational-thinking](upstream/skills/principle-foundational-thinking/SKILL.md.source) | Apply before writing logic: choosing core types and data structures, sequencing scaffold-vs-feature work, asking what concurrent actors share. Get the data structures right so downstream code becomes obvious. |
| [guard-the-context-window](upstream/skills/principle-guard-the-context-window/SKILL.md.source) | Apply when context is filling up: large outputs, long files, repeated reads, fan-out planning. Route bulk to subagents; keep summaries in the main thread, not raw payloads. |
| [laziness-protocol](upstream/skills/principle-laziness-protocol/SKILL.md.source) | Apply when refactoring, evaluating diff size, or tempted to add abstractions, layers, or signal threading. Bias toward deletion and the smallest change that solves the problem. |
| [make-operations-idempotent](upstream/skills/principle-make-operations-idempotent/SKILL.md.source) | Apply when designing commands, lifecycle steps, or processing loops that run amid crashes, restarts, and retries. Converge to the same end state regardless of partial prior runs. |
| [migrate-callers-then-delete-legacy-apis](upstream/skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md.source) | Apply when introducing a new internal API while old callers still exist. Migrate callers and delete the old API in the same wave instead of preserving compatibility layers. |
| [minimize-reader-load](upstream/skills/principle-minimize-reader-load/SKILL.md.source) | Apply when reviewing or shaping code that's hard to trace. Count layers between question and answer, and hidden state in the reader's head; collapse one-caller wrappers and shrink mutable scope. |
| [model-the-domain](upstream/skills/principle-model-the-domain/SKILL.md.source) | Apply when writing stateful logic, or when code branches a lot or repeats a shape assumption across files. Encode the domain in a structure instead of scattered conditionals. |
| [never-block-on-the-human](upstream/skills/principle-never-block-on-the-human/SKILL.md.source) | Apply when tempted to ask 'should I do X?' on reversible work. Proceed, present the result, let the human course-correct after the fact; reserve confirmation for irreversible actions. |
| [outcome-oriented-execution](upstream/skills/principle-outcome-oriented-execution/SKILL.md.source) | Apply during planned rewrites and migrations with explicit phase boundaries. Converge on the target architecture; don't preserve smooth intermediate states with throwaway compatibility code. |
| [prove-it-works](upstream/skills/principle-prove-it-works/SKILL.md.source) | Apply after completing a task, before declaring done. Verify against the real artifact (run the feature, read the actual value, inspect the diff), not a proxy, self-report, or 'it compiles.' |
| [redesign-from-first-principles](upstream/skills/principle-redesign-from-first-principles/SKILL.md.source) | Apply when integrating a new requirement into an existing design. Redesign as if the requirement had been a foundational assumption from day one, instead of bolting it on. |
| [separate-before-serializing-shared-state](upstream/skills/principle-separate-before-serializing-shared-state/SKILL.md.source) | Apply when concurrent actors might write to the same file, branch, key, or state object. Eliminate the sharing first; serialize structurally only when one shared writer is a real invariant. |
| [sequence-verifiable-units](upstream/skills/principle-sequence-verifiable-units/SKILL.md.source) | Apply to multi-step work (sweeps, migrations, runs of similar edits) and to how you stack commits and PRs. Break work into small units that each end in a verifiable state, check each before the next, and order delivery so the sequence proves itself to a reviewer. |
| [subtract-before-you-add](upstream/skills/principle-subtract-before-you-add/SKILL.md.source) | Apply when sequencing an addition, refactor, or rewrite. Remove dead code, redundant validators, and stub references first, then build on the simpler base. |
| [test-behavior-not-implementation](upstream/skills/principle-test-behavior-not-implementation/SKILL.md.source) | Apply when you write, change, or keep a test. Call the code the way its users do and assert the result they observe against a literal expected value. If the test would still pass when every imported function returns undefined, rewrite the assertion or delete the test. |
| [type-system-discipline](upstream/skills/principle-type-system-discipline/SKILL.md.source) | Apply when designing types, reviewing a function signature, or writing code in any statically-typed language. Make illegal states unrepresentable, brand semantic primitives, parse external data at boundaries, refuse to lie to the compiler, exhaust variants, derive from authoritative schemas. |

## Playbooks

| Playbook | Complete original |
|---|---|
| authoring-a-skill | [Read source](upstream/skills/poteto-mode/playbooks/authoring-a-skill.md) |
| autonomous-run | [Read source](upstream/skills/poteto-mode/playbooks/autonomous-run.md) |
| autopilot-full | [Read source](upstream/skills/poteto-mode/playbooks/autopilot-full.md) |
| autopilot-stack | [Read source](upstream/skills/poteto-mode/playbooks/autopilot-stack.md) |
| babysit | [Read source](upstream/skills/poteto-mode/playbooks/babysit.md) |
| bug-fix | [Read source](upstream/skills/poteto-mode/playbooks/bug-fix.md) |
| eval | [Read source](upstream/skills/poteto-mode/playbooks/eval.md) |
| feature | [Read source](upstream/skills/poteto-mode/playbooks/feature.md) |
| hillclimb | [Read source](upstream/skills/poteto-mode/playbooks/hillclimb.md) |
| investigation | [Read source](upstream/skills/poteto-mode/playbooks/investigation.md) |
| multi-phase-plan | [Read source](upstream/skills/poteto-mode/playbooks/multi-phase-plan.md) |
| opening-a-pr | [Read source](upstream/skills/poteto-mode/playbooks/opening-a-pr.md) |
| orchestrate | [Read source](upstream/skills/poteto-mode/playbooks/orchestrate.md) |
| pause-safely | [Read source](upstream/skills/poteto-mode/playbooks/pause-safely.md) |
| perf-issue | [Read source](upstream/skills/poteto-mode/playbooks/perf-issue.md) |
| prototype | [Read source](upstream/skills/poteto-mode/playbooks/prototype.md) |
| refactoring | [Read source](upstream/skills/poteto-mode/playbooks/refactoring.md) |
| runtime-forensics | [Read source](upstream/skills/poteto-mode/playbooks/runtime-forensics.md) |
| session-pickup | [Read source](upstream/skills/poteto-mode/playbooks/session-pickup.md) |
| shipping | [Read source](upstream/skills/poteto-mode/playbooks/shipping.md) |
| trace-forensics | [Read source](upstream/skills/poteto-mode/playbooks/trace-forensics.md) |
| visual-parity | [Read source](upstream/skills/poteto-mode/playbooks/visual-parity.md) |
| worktree-cleanup | [Read source](upstream/skills/poteto-mode/playbooks/worktree-cleanup.md) |

## Benny workflows

| Workflow | Full source and scope |
|---|---|
| [reproduce-and-fix-issues](upstream/automations/benny/skills/reproduce-and-fix-issues/SKILL.md.source) | Reproduce triaged Slack bugs through a configured app-control adapter, verify existing fixes, and open a bounded draft pull request only after before-and-after proof. Use only from the configured Benny repro automation. |
| [setup-benny](upstream/automations/benny/skills/setup-benny/SKILL.md.source) | Configure Benny and prepare its triage and repro automations. Use when installing Benny or changing its Slack, tracker, repository, routing, control, model, or budget settings. |
| [triage-issue-reports](upstream/automations/benny/skills/triage-issue-reports/SKILL.md.source) | Triage Slack issue reports with one thread-only verdict, evidence review, cause-aware routing, tracker dedupe, and fail-closed ticket creation. Use only from the configured Benny triage automation. |

## Agent definitions

- [Poteto Agent](upstream/agents/poteto-agent.md). Delegate persona for code-writing and helper slices spawned during a poteto-mode run; pass it as a subagent prompt when authorized. It is not the runner of poteto-mode, and it is not a registered subagent type on any host; see the host runtime notes for using it.
- [Comment Sicko](upstream/agents/comment-sicko.md). Original read-only comment-review criteria.

## Original guide

- [Guide index](upstream/docs/guide/README.md). Original Cursor instructions, retained for reference.
- [01-setup](upstream/docs/guide/01-setup.md).
- [02-poteto-mode](upstream/docs/guide/02-poteto-mode.md).
- [03-understand](upstream/docs/guide/03-understand.md).
- [04-design](upstream/docs/guide/04-design.md).
- [05-build-and-clean](upstream/docs/guide/05-build-and-clean.md).
- [06-verify-and-ship](upstream/docs/guide/06-verify-and-ship.md).
- [07-overnight](upstream/docs/guide/07-overnight.md).
- [08-principles](upstream/docs/guide/08-principles.md).
- [09-make-it-yours](upstream/docs/guide/09-make-it-yours.md).
- [10-recipes-and-pitfalls](upstream/docs/guide/10-recipes-and-pitfalls.md).

## Tools, prompts, templates, and assets

- [Poteto tools package](upstream/skills/poteto-mode/scripts/package.json), [lockfile](upstream/skills/poteto-mode/scripts/bun.lock), and [bootstrap](upstream/skills/poteto-mode/scripts/bootstrap.ts).
- [Orchestration CLI](upstream/skills/poteto-mode/scripts/orch/orch.ts), [store](upstream/skills/poteto-mode/scripts/orch/store.ts), and [tests](upstream/skills/poteto-mode/scripts/orch/orch.test.ts).
- [PR watcher entrypoint](upstream/skills/poteto-mode/scripts/watch-pr/watch-pr), [CLI](upstream/skills/poteto-mode/scripts/watch-pr/cli.ts), [policy](upstream/skills/poteto-mode/scripts/watch-pr/policy.ts), and all adjacent sources/tests.
- [Original plan checker](upstream/skills/poteto-mode/scripts/check-plan.mjs) (with its [test](upstream/skills/poteto-mode/scripts/check-plan.test.ts)) and [worktree auditor](upstream/skills/poteto-mode/scripts/worktree-audit.sh). These retain Cursor-specific assumptions.
- [Decision logger](../scripts/decision-log.sh) and [original TSV template](upstream/skills/show-me-your-work/references/decision-log-template.tsv).
- [Bugbot triage rubric](upstream/skills/poteto-mode/references/bugbot-triage.md).
- [Original plugin manifests](upstream/.cursor-plugin/plugin.json) and [root manifest](upstream/plugin.json), [README](upstream/README.md), [logo](upstream/assets/logo.png), and [license](../LICENSE).
- Each workflow directory retains all its supporting prompts, patterns, examples, and references. Benny retains all automation prompt/configuration templates.
- [Complete file manifest](upstream-manifest.json) lists all 169 files, their exact stored locations, modes, source blob IDs, and SHA-256 values.
