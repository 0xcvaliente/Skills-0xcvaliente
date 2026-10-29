# Native workflows

Use [Host runtime adaptation](host-runtime.md), then read the selected full
source and supporting prompts through the [catalog](catalog.md). These sections
replace host mechanics while retaining pstack's engineering methods.

## poteto-mode and poteto-help

`poteto-mode` selects a playbook and relevant principles. `poteto-help` answers
the immediate usage question and supplies a concrete `/pstack <workflow>
<task>` prompt. It mentions `create-verification-skill` when no way to drive the
app exists and the question is about proof, and `create-formal-verification-skill`
when none exists for a race, invariant, or case tests rarely hit (or
`maintain-formal-verification-skill` when the covered code changed after the
recorded sync commit). Explain capabilities and missing dependencies as needed. No
global persistent mode or mandatory setup is implied.

## sharpen, in-your-own-words, and ketchup

Explicit-request workflows (`ketchup-video`, `statechart` and the two formal verification workflows below follow the same rule). Upstream marks each `disable-model-invocation: true`;
that flag has no effect here, so run them only when the user names them.

- `sharpen`: make the prompt deeper, not bigger, then return the rewrite. The
  input is a prompt the user is about to send, not a task to start. Before
  rewriting, say what a top professional in the field would do that the prompt
  does not ask for, name the rawest material they would start from instead of
  what has already been digested, name the specific methods and tools they would
  use, and say what other than the agent or the user would show the result is
  right. Then rewrite the prompt to ask for exactly that and leave the user's
  choices open. Return only the rewritten prompt; do not do the task, and do not
  add scope, actions, or authorization the user did not give.
- `in-your-own-words`: restate what you think the user's goals are and the problem
  they are solving, then wait for correction unless they asked you to proceed.
- `ketchup`: a read-only catch-up on what changed since the user's last own message
  (notifications and subagent results are not theirs). Help them understand each
  change, then lay out every call waiting on them so they can decide from the
  reply alone. Plain short sentences, no hashes, paths, or commands unless the
  user needs one to act. Spend words on the calls, not the story: what happened
  in under 100 words (pictures not counted), about 30 words per item, and a reply
  that grows with the number of items. Never cut or shrink items to fit a count,
  and never substitute a link for an item. Open with one short sentence naming
  what waits on the user. Show screenshots and videos inline first, then a diagram
  only where a picture beats sentences (a stack with each PR's state, a
  before/after, options side by side), then one short bullet per thing they asked
  for. For each call give your pick, what it changes for users, the evidence, and
  its risk ("unknown" for a missing fact), riskiest first; a call between options
  lists every option weighed with its gain and cost. Never draw a status list or
  disconnected boxes. A visual is a picture, not a table. If a visible change has
  no screenshot, mark its line "No screenshot yet". Never invent numbers or draw
  a screen you did not capture, mark work done that waits on the user, or take new
  actions while catching up.
- `ketchup-video`: follow `ketchup`, but show what happened as a short silent video of slides instead of its summary and visuals, with the calls waiting on the user as text under it. The window starts at the user's last own message before `ketchup-video`. Write and render the video outside the project; that is the one exception to `ketchup`'s read-only rule. Reply with ketchup's opening sentence, the video, one line naming any work left that you can do yourself, and the action items. Name each option as the video names it. If no tool can render slides to video, or the render fails, say so in one line and give only the calls.

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
recent work. Use the current conversation and the host's accessible session
history (see the runtime mapping), reading deeper only as needed.
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
until the winner is verified. Run workers as subagents if the host supports them, otherwise run the slices
sequentially yourself; do not start separate user sessions as subagent substitutes.

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

Unslop removes AI patterns from writing: scan for the listed patterns, then
rewrite, preserving meaning and matching the intended tone. Poteto-mode applies it to
the final reply too. Bro restates
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

## statechart

Explicit-request workflow. Draw how a system moves between states, in the words of the
person who owns the behavior (a PM, designer, engineer or reviewer), as a Mermaid
statechart generated from a TLA+ model so the picture and the checked model cannot
drift apart. Label states by what the reader can observe and steps by the event that
moves the system; keep variable and action names out of labels. Each rule the reader
agrees to becomes one invariant carrying their sentence; never weaken a rule to make
the chart pass. Each bug the model checker finds is a numbered path in the reader's
words, and each state is marked works, still wrong, or fixed by a proposed change.
Two directions: `from-spec` (a model exists, or the code or design is concrete enough
to model; when the code already has a TLA+ spec, copy it, add the variables the labels
need, and pass the original unchanged as the thing to audit against) and `from-chart`
(no model yet: agree on a chart first, write a `%% never` line per rule, then add the
real code's guards and ask the reader about every difference). When a model describes
code, tie every variable and action to code a reviewer can open, and replay each bug's
story against the real code through entry points a user or client reaches; if a bug
does not reproduce, the model is wrong, not the rule. For a design with no code yet,
say the counterexample is the only evidence. Look at every rendered PNG before handing
off. Work in a scratch folder outside the repo. The scripts need Node, and the first
run installs TLC and Java with mise (about 305 MB, network); say so before running, and
use an existing TLC and Java if the user has them. Hand off the PNG and Mermaid source
of each chart, one line per bug (rule broken, its steps, whether it reproduced, whether
the proposed fix fixes it), the generated stories file, the command that regenerates
everything, and what the model leaves out. Take every count you quote from the
generated summary. The retained scripts are reference implementations; run them only on
the user's request.

## create-formal-verification-skill

Explicit-request workflow. Find the part of the repo where a break harms users and
tests reach the least (races, retries, state machines, parsers, unsafe code); ask
only what the code cannot answer. Choose the tool that answers the question at
the lowest cost: a model checker (TLA+ is the default for ordering questions in
any language), a code-level verifier, or a proof for properties that must hold at
every size. If no verifier runs on the language, say so and test the real code
with generated inputs rather than a hand model. Every part of the model points at
code a reviewer can open, and each property is shown failing on a broken variant.
When the current code breaks the property, report the counterexample in the
code's terms; do not weaken the property or model, and do not change product
code unless asked. State scope, bounds, and assumptions honestly. Write a
project-local skill (same placement as `create-verification-skill`) with
frontmatter, a coverage record of files and functions, one rerun command, and the
commit at which the verification was last confirmed to describe them. Follow it
once on a scratch break, then drop the break. Hand off the property, tool and
why, bounds, findings, how to run it, and what it does not cover. When the check is a
TLA+ model, tell the next agent to read each result with the `statechart` workflow
and to refer to it by name, never copying its commands, options or paths into the
generated skill or its scripts, since they change between releases and machines.

## maintain-formal-verification-skill

Explicit-request workflow for a verify skill that runs a model checker, prover, or
code-level verifier against named code, including one `create-formal-verification-skill`
made. Find each check and its recorded sync commit (else the last commit that
changed the verification files, and say so). Run it as is first, then read every
change to covered code since the sync commit, including moved code and new code
that touches guarded state, and classify each as no effect, verification no longer
describes the code, promise changed on purpose (cite evidence), or promise possibly
broken. Update the verification from the code, not from the result; change a
property only for an evidenced intended change and record old and new wording.
Rerun: a pass needs a deliberate break to show it can still fail, and a failure is
replayed against the real code to decide drift versus bug. Report each check as
in sync, updated, bug, or blocked. Edit only verification files unless the user
asks otherwise, never weaken a property to pass, move the sync commit only after
confirming the code at that commit, and keep verification updates in a change of
their own.

## create-verification-skill

Inspect how the project starts, resets, authenticates, and can be driven. Reuse
its harness. Write a project-local `verify-<app>` skill in the host's project
skill folder (for example `.agents/skills/verify-<app>/SKILL.md`; also `.claude/skills/`,
`.cursor/skills/`, or `.gemini/skills/` as the host requires) or the user's chosen
location, using a skill-creator skill if one is installed. Include doctor/start/reset, driving commands,
proof capture, cleanup, and an observed feature map. Adapt retained examples.
Launch must reach a usable state from an empty data directory (migrations and
seed data included); "ready" means the app is usable, not that a process or
health check answers. When seed data lacks a precondition a journey needs, report
the failure in that feature's notes instead of weakening the journey.
Exercise a real feature before claiming the verifier works. If it was proved in a
stand-in (a container for a fresh VM, a local stack for a remote one), list the
setup steps the stand-in did that the real target will not; they stay unverified.

## maintain-verification-skill

Compare the verifier/feature map with source, then run a live pass across
relevant entry points. Partition source readers only when authorized. Make
evidenced corrections, preserving conventions. Use at most one maintenance PR
when publication is requested. Missing access remains a verification gap.

## setup-pstack

Use optional project configuration from Host runtime adaptation. Inspect
existing choices/capabilities; default roles to inherit. Resolve only material
missing preferences for delegation, supported models, or verification commands.
Preserve unrelated settings. Explain that the file is workflow data, not a
host setting such as a settings file or a model command. After configuration,
offer once each (never push) to generate a verification skill and a formal
verification skill for the project, unless it already has one; accepting runs the
matching create workflow.

## automate-me

Create/update a personal working-style skill; the name alone does not request
scheduling. Find an existing matching skill. Use explicit preferences and relevant
accessible history, separating durable habits from one-off corrections. Remove
duplicated policy and author it as an Agent Skill (a personal folder such as `~/.agents/skills/<name>/`,
or a project folder such as `.agents/skills/<name>/`; use the host's own folder if it differs), using a skill-creator skill if
installed. Preserve requested placement and invocation policy. Do not scan unrelated history or invent persistent modes.

## reflect and correct

Reflect extracts concrete lessons and routes narrow improvements to existing
skills/tools. Retained tooling, judgment, divergent-review, and synthesis prompts
provide lenses; delegation follows native rules. Correct fixes recurring mistake
classes at the strongest useful level: architecture, types, lint, tests, then
docs. Prove enforcement catches a real example. Avoid universal rules from one incident.

## make-bot-ui

The original targets a specific Cursor/Grok Bot webhook service. The host's
scheduling or loop features do not provide its webhook or secret-request card. Identify an available service
and actual credential flow first. Without one, explain the dependency and build
only the requested reviewable UI/server integration boundary.

Keep credentials server-side and payloads untrusted. Verify the real request
contract. Never invent Cursor URLs or put secrets in chat/client code. Use
project deployment/private-network conventions; do not install Tailscale or
expose listeners incidentally. Test a harmless authorized payload before claiming
the bot wakes. External messages still need authorization.
