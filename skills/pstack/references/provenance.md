# Provenance and adaptation

Upstream: [cursor/plugins, pstack](https://github.com/cursor/plugins/tree/ccb5507cec1546dc88135c1139c811e6c59115ba/pstack).
Author: Lauren Tan. Version: 0.15.15. Reviewed on 2026-10-08.
Pinned commit: `ccb5507cec1546dc88135c1139c811e6c59115ba`.

## Complete preservation

All **164 tracked files** under `pstack/` at the pinned commit are included.
There are **27 workflows**, **24 principle skills**, **23 playbooks**, **two agent
definitions**, and **three Benny workflows**, together with every supporting
reference, script, test, template, guide, hidden configuration file, license,
lockfile, and binary asset. No upstream file was omitted.

Original file bytes and executable modes are preserved under `upstream/`.
The 54 original `SKILL.md` filenames alone become `SKILL.md.source` to prevent
recursive discovery of Cursor entrypoints. The manifest records both names.
Contents, including unsupported source frontmatter, are unchanged.

The [manifest](upstream-manifest.json) records the original Git blob ID and
SHA-256 for every source file. `python3 scripts/check_package.py`, run from the
package root, verifies the retained set and one live skill. `--source` additionally
compares an independent original directory, including omissions. This checker
does not contact GitHub or refresh the baseline.

## Codex adaptation

- One discoverable `pstack-codex` entrypoint replaces a plugin with many slash skills.
- Native guidance covers every original playbook/workflow and links the complete procedures.
- Cursor Task/model defaults become authorized native collaboration with parent inheritance.
- Global model rules become optional, explicitly requested project workflow data.
- Internal control/deslop/create-skill dependencies become available native tools and Codex skill-creator.
- Cursor transcript paths become scoped accessible chat history.
- Loops and automation setup become actual requested Codex schedules; no persistence is assumed.
- Forge/worktree steps use current native capabilities and preserve user authorization and recoverable work.
- Benny preserves source-thread identity, dedupe, bounded proof, draft-only delivery, and fail-closed writes while replacing Cursor setup mechanics.
- Make-bot-ui keeps its real external webhook dependency visible; no Codex webhook is invented.
- Comment review keeps useful/legal/API rationale and does not force theatrical output or blind deletion.
- The portable logger is copied unchanged to `scripts/decision-log.sh`. Other upstream tools are retained reference implementations, not claimed Codex ports.

The original guide still describes Cursor. The package README and native references
are the maintained Codex documentation. Retained sources are loaded selectively;
they do not change host policy or expand the user's task.

## Licensing

Original content is MIT, copyright 2026 Lauren Tan. The exact license appears
in [the package](../LICENSE) and [source snapshot](upstream/LICENSE). New adaptation
files are distributed under the same MIT terms. This personal adaptation does
not imply affiliation with or endorsement by Lauren Tan or Cursor.

## Maintenance

Inspect changes since the pinned commit before updating. Rebuild the complete
source snapshot/manifest, review host-specific mechanics and native guidance,
update counts/catalog/docs, and rerun integrity, helper, and structural checks.
Do not silently replace locally customized installed files. This package does
not schedule upstream monitoring or automatically advance its reviewed revision.

## Claude Code port

Ported on 2026-10-10 from the Codex version (`pstack-codex` in
`0xcvaliente/codex-skills`) to the Claude Code skill `pstack`. The skill was
renamed, `references/codex-runtime.md` became `references/claude-runtime.md`,
and `$pstack-codex` invocations became `/pstack`. Where the Codex version had
translated pstack's Claude-style mechanics, they map back to Claude Code
features: the Agent tool (subagents) for `Task`, AskUserQuestion and the todo
list, `CLAUDE.md` for always-on instructions, `/loop`, `/schedule`, or cron for
recurring work, Claude Code session transcripts for recall, and `.claude/` for
project data (`.claude/pstack.json`, `.claude/benny/`). The Codex installer and
validator commands and the `agents/openai.yaml` UI metadata were removed.
Retained upstream files and the manifest are unchanged.

## Host-neutral adaptation

Adapted on 2026-10-12 from the Claude Code port above into a host-neutral Agent
Skill. `references/claude-runtime.md` became `references/host-runtime.md`, which
maps tools to a capability vocabulary (shell, file read/search/edit, web,
ask-the-user, subagents, task list, browser automation, MCP) and documents what
degrades without subagents, hooks, or MCP, plus invocation across hosts. Claude
Code-only names (Agent tool, AskUserQuestion, TodoWrite, `/loop`, `/schedule`,
`.claude/` paths, `CLAUDE.md`) became capability wording or lists of hosts' files;
project data moved from `.claude/pstack.json` and `.claude/benny/` to
`.agents/pstack.json` and `.agents/benny/`. Retained upstream files, the manifest,
and the license are unchanged.

## Upstream sync 2026-10-15

Refreshed on 2026-10-15 from `ccb5507cec1546dc88135c1139c811e6c59115ba` (0.15.15)
to `1e5c90a4b6f249917bd21fe361b3a2a7deb741b8` (short `1e5c90a`, 0.15.24), the latest
commit touching `pstack/` in cursor/plugins. No upstream file was deleted or renamed.

- `references/upstream/` and `references/upstream-manifest.json` were rebuilt from
  the new revision with the same layout: 169 files (was 164), 57 `SKILL.md`
  entrypoints stored as `SKILL.md.source` (was 54), bytes and modes unchanged.
  Added: `skills/sharpen`, `skills/in-your-own-words`, `skills/ketchup` (each
  `disable-model-invocation: true` upstream), the root `plugin.json`, and
  `skills/poteto-mode/scripts/check-plan.test.ts`. 82 other files changed, including
  the orchestrate and shipping playbooks (Graphite removed, one stacker, workers never
  retarget or merge, per-job subagent effort), poteto-mode and poteto-agent
  (the receiving chat runs the playbook; delegates only), worktree-audit and
  worktree-cleanup (MERGED against a chosen base ref), check-plan (fenced code),
  watch-pr (review-thread pagination), the orch store rewrite,
  create-verification-skill, the unslop description, the Comment Sicko agent id,
  and prompt trims across many skills.
- `scripts/decision-log.sh` is a runnable copy of upstream
  `skills/show-me-your-work/scripts/log.sh`; that file is unchanged in this range,
  so the copy stays byte-identical. No other runnable upstream copy ships outside
  `references/upstream/`.
- Local host-neutral layer merged by hand: `SKILL.md`, `README.md`,
  `references/catalog.md`, `workflows.md`, `playbooks.md`, `host-runtime.md`, and
  the file count in `tests/test_helpers.py`. Cursor mechanics (Task, `subagent_type`,
  `generalPurpose`, Graphite, model slugs, cloud environments) were mapped to
  capability vocabulary rather than copied.
- Skipped: Cursor plugin metadata and frontmatter keys (no effect here); the
  `disable-model-invocation` flag (these skills run only on explicit request by
  instruction); Cursor-specific `.cursor/` paths and cloud-agent mechanics; model
  slug changes. Retained scripts were not ported or executed. The `SKILL.md`
  description is unchanged.

## Upstream sync 2026-10-20

Refreshed on 2026-10-20 from `1e5c90a4b6f249917bd21fe361b3a2a7deb741b8` (0.15.24)
to `88d47514b82e7c44f00f2b2a72ff6dd12158038c` (short `88d4751`, plugin manifests
read 0.15.29), the latest commit touching `pstack/` in cursor/plugins. The most
recent version-bump commit message said 0.15.28; the manifests at this revision say
0.15.29, which is the version recorded. No upstream file was deleted or renamed.

- `references/upstream/` and `references/upstream-manifest.json` were rebuilt from
  the new revision with the same layout: 172 files (was 169), 59 `SKILL.md`
  entrypoints stored as `SKILL.md.source` (was 57), bytes and modes unchanged.
  Added: `skills/create-formal-verification-skill`,
  `skills/maintain-formal-verification-skill` (each `disable-model-invocation: true`
  upstream), and `docs/harness/claude-code.md`. 32 other files changed: the root and
  Cursor plugin manifests (version), the README and all guide chapters, correct,
  ketchup, sharpen (restored to the original prompt: it rewrites the prompt and
  returns only the rewrite instead of doing the task), swarm (intro paragraph, the
  set-N step, and a duplicate result-table line removed), setup-pstack (new step 8
  offering a formal verification skill), poteto-help and its recipes, poteto-mode,
  make-bot-ui and poteto-mode (frontmatter `name` now matches the folder name), the
  principle skills (attack-the-premise, fix-root-causes, make-operations-idempotent,
  migrate-callers-then-delete-legacy-apis, test-behavior-not-implementation,
  type-system-discipline), typescript-best-practices (brands come from a verifying
  type guard, not `as`), and interrogate's lead-judgment reference (two sections
  trimmed). ketchup now helps the user understand each change and lists every call
  waiting on them with a pick, evidence, and risk, and the reply grows with the
  number of items.
- `scripts/decision-log.sh` is a runnable copy of upstream
  `skills/show-me-your-work/scripts/log.sh`; that file is unchanged in this range,
  so the copy stays byte-identical.
- Local host-neutral layer merged by hand: `SKILL.md` (counts, version, routing row
  for formal verification, root-cause and behavioral-test wording), `README.md`,
  `references/catalog.md` (two new workflows, changed descriptions, the Claude Code
  adapter file), `workflows.md` (new sharpen and ketchup behavior, two new workflow
  sections, setup offers, poteto-help mentions), `playbooks.md` (autopilot-full
  wording), `host-runtime.md` (explicit-request list, adapter note), `benny.md`
  (Cursor-only note), and the file count in `tests/test_helpers.py`. Cursor
  mechanics were mapped to the capability vocabulary rather than copied.
- Skipped: the Claude Code install steps, `pstack:` command prefixes, the generated
  `harness/pstack/` tree, and the adapter's tool, subagent-field, model, and
  `~/.claude/rules` mappings (the host-neutral capability vocabulary already covers
  them; the file is retained as reference only); Cursor plugin metadata and
  frontmatter keys; the `disable-model-invocation` flag (these skills run only on
  explicit request by instruction); Cursor-only features (Automations, Bugbot,
  cloud agents); the swarm trims and the interrogate lead-judgment trims (the local
  guidance never carried that text); typescript-best-practices snippet changes
  (retained source covers them). Retained scripts were not ported or executed. The
  `SKILL.md` description is unchanged.

## Upstream sync 2026-10-26

Refreshed on 2026-10-26 from `88d47514b82e7c44f00f2b2a72ff6dd12158038c` (0.15.29)
to `99b609a72323b70204eab407c622f436e858e112` (short `99b609a`, 0.15.32), the latest
commit touching `pstack/` in cursor/plugins. No upstream file was deleted or renamed.

- `references/upstream/` and `references/upstream-manifest.json` were rebuilt from
  the new revision with the same layout: 200 files (was 172), 61 `SKILL.md`
  entrypoints stored as `SKILL.md.source` (was 59), bytes and modes unchanged.
  Added: `skills/statechart` (a `SKILL.md`, 21 scripts including the renderer and
  the TLC converters, and 5 test files) and `skills/ketchup-video/SKILL.md`, each
  `disable-model-invocation: true` upstream. Other changed files: both plugin
  manifests (version), the README (Claude Code auto-update note, two new rows), the
  verify-and-ship and recipes guide chapters, `create-formal-verification-skill`
  (read each TLA+ result with `/statechart`), `poteto-help`, `reflect` (never edit
  a skill under the plugin cache), `swarm` (Phase A numbering and a dangling table
  reference), and fixes in `poteto-mode` scripts: `check-plan` (matching inline-code
  delimiters), `orch/store` (prefer the active PR over branch history), `watch-pr`
  (cap polling sleeps at the deadline, tell fork heads apart during stack discovery)
  and `worktree-audit.sh` (GNU `stat` and `date` flags).
- `scripts/decision-log.sh` is a runnable copy of upstream
  `skills/show-me-your-work/scripts/log.sh`; that file is unchanged in this range,
  so the copy stays byte-identical.
- Local host-neutral layer merged by hand: `SKILL.md` (counts, version, routing rows
  for `statechart` and `ketchup-video`), `README.md` (counts, version, reviewed
  revision), `references/catalog.md` (two new workflows), `workflows.md` (new
  `statechart` section, `ketchup-video` bullet, and the `/statechart` pointer in
  `create-formal-verification-skill`), `host-runtime.md` (explicit-request list), and
  the file count in `tests/test_helpers.py`. Cursor mechanics were mapped to the
  capability vocabulary rather than copied.
- Skipped: Cursor plugin metadata and frontmatter keys; the `disable-model-invocation`
  flag (these skills run only on explicit request by instruction); the Claude Code
  auto-update note; the `reflect` cache-path rule (Cursor plugin layout); the `swarm`
  step renumbering (the local guidance carries no numbered steps). Retained scripts
  were not ported or executed; `statechart` downloads about 305 MB (TLC and Java via
  mise) on first run, so it is documented as an explicit, network-using request. The
  `SKILL.md` description is unchanged.

## Upstream sync 2026-10-29

Refreshed on 2026-10-29 from `99b609a72323b70204eab407c622f436e858e112` (0.15.32)
to `1ba91fc25c0977741dd0e267849e6234b037ed0a` (short `1ba91fc`, 0.15.36), the
current head of cursor/plugins for `pstack/`. The range covers seven commits (the
statechart compiler port, two version bumps, two statechart fixes, a skill-update
port, and the agentic Orchestrate change). 464 upstream paths changed: 406 added,
33 deleted, 25 modified.

- `references/upstream/` and `references/upstream-manifest.json` were rebuilt from
  the new revision with the same layout, taken from `git archive` of the pinned
  commit: 573 files (was 200), 61 `SKILL.md` entrypoints stored as `SKILL.md.source`
  (unchanged), bytes and modes unchanged (6 executables). Deletions were applied:
  the old statechart `.mjs` scripts and `test/band.mmd` (26 files), the four
  `interrogate/references/` prompts (code-quality-review, lead-judgment,
  reviewer-prompt, rubric), and `poteto-mode/scripts/orch/` (`orch.ts`, `store.ts`,
  `orch.test.ts`). Added: the TypeScript statechart rewrite (`statechart` launcher,
  `statechart.ts`, `pipeline.ts`, `ir.ts`, `run.ts`, backends, frontends, passes,
  `references/render.md`, a `package.json`) and its test corpus (about 370 files).
- Guidance changes in the rest of the range: `statechart` is rewritten around a
  single `statechart SPEC.tla` command with a view module (the `from-chart`,
  `--against`, `--png`, and `stories.md` flows are gone; rendering uses the npm package
  `pele`; first run still installs TLC and Java with mise, with no size stated);
  `interrogate` is rewritten so adversaries try to break a change with a run and only
  verified findings survive (no Act on / Consider / Noted / Dismissed buckets, Output
  is Intent, Findings, Dropped); `orchestrate` is agentic and calls no scripts;
  `autopilot-stack` is "Autopilot-full without the merge" and stacks a PR only on a PR
  it builds on, with `babysit`, `multi-phase-plan`, `opening-a-pr`, and the guide
  chapters following; `autopilot-full` gains a blocking rule, no verifier for a
  wording-only change, a rebase on a known concurrent change, and parked follow-ups in
  the reply; `arena` takes a judge only from a different family and may skip it;
  `ketchup-video` becomes subtitled; `poteto-mode` adds a first-message restatement of
  the goal, background steers and resumes, and fallbacks for rejected model slugs;
  `explain-the-number` applies before measuring; `setup-pstack` explains cross-judge
  ordering; `create-formal-verification-skill`, `poteto-help`, both plugin manifests
  (version), the README, and four guide chapters follow.
- `scripts/decision-log.sh` is a runnable copy of upstream
  `skills/show-me-your-work/scripts/log.sh`; that file is unchanged in this range,
  so the copy stays byte-identical.
- Local host-neutral layer merged by hand: `SKILL.md` (version, counts, goal
  restatement bullet, statechart routing row), `README.md` (version, count, reviewed
  revision), `references/catalog.md` (count, changed descriptions for `interrogate`,
  `ketchup-video`, `statechart`, `explain-the-number`, and the orchestration CLI
  bullet), `workflows.md` (`ketchup-video` subtitles, `interrogate` and `statechart`
  rewritten, `arena` judge-family rule), `playbooks.md` (`Orchestrate`,
  `Autopilot-full`, `Autopilot-stack`), `host-runtime.md` (background steers), and the
  file count in `tests/test_helpers.py`. Cursor mechanics were mapped to the
  capability vocabulary rather than copied.
- Skipped: Cursor plugin metadata and frontmatter keys; the `disable-model-invocation`
  flag (these skills run only on explicit request by instruction); the `arena` and
  `poteto-mode` model-slug fallback chains and `setup-pstack` cross-judge ordering
  (Cursor model slugs and the `pstack-models` rule are not used here; inherit the
  parent model); the `orch` store layout and brief template (deleted upstream, and the
  host-neutral Orchestrate section never carried them). Retained scripts, including the
  new statechart TypeScript and its tests, were not ported or executed. `statechart`
  stays an explicit-request, network-using workflow (mise installs TLC and Java, and
  rendering fetches `pele`); the "about 305 MB" figure is kept as measured at 0.15.32
  because upstream stopped stating it. The `SKILL.md` description is unchanged.
