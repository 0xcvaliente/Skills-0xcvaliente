# Pstack

Pstack's engineering workflows adapted into one installable, host-neutral Agent Skill
(Claude Code, Codex, Gemini CLI, Cursor, GitHub Copilot, OpenCode, or plain chat).
Based on [Lauren Tan's pstack](https://github.com/cursor/plugins/tree/main/pstack)
0.15.15. Go deep first, write less code, and verify the result against the real artifact.

The package includes native host-neutral routing and **all 164 original upstream files**:

| Material | Included |
|---|---|
| Main and situational workflows | 27, including poteto-mode, how, why, architect, arena, swarm, interrogate, recall, and writing/verification maintenance. |
| Engineering principles | All 24 full principle sources. |
| Poteto playbooks | All 23 originals plus host-neutral execution guidance for each. |
| Agent definitions | Poteto Agent and Comment Sicko as reference prompts. |
| Benny | Setup, triage, reproduction/fix, templates, control contracts, and routing/feature-map examples. |
| Documentation and assets | Full upstream README, ten-chapter guide, illustrations, logo, manifest, and license. |
| Tools | Original Bun orchestration store, PR watcher, tests, plan checker, worktree audit, bootstrap, and lockfile. |
| Native helpers | Portable decision logger and an offline complete-source integrity checker. |

The [complete catalog](references/catalog.md) links to every workflow and
playbook. The [source manifest](references/upstream-manifest.json) records each
original path, stored path, executable mode, and SHA-256. Only original filenames
`SKILL.md` become `SKILL.md.source`; every original file's bytes are unchanged.
This prevents nested Cursor skills from becoming unintended skill entrypoints.

## Install

Copy the whole directory into a skills folder your host reads. Locations vary by
host and release; `~/.agents/skills` is the shared user-level folder most hosts
see, and `.agents/skills` is the shared project-level folder:

```bash
mkdir -p ~/.agents/skills
cp -R pstack ~/.agents/skills/
```

Host-specific folders also work: `~/.claude/skills` or `.claude/skills` (Claude
Code), `.cursor/skills` (Cursor), `.gemini/skills` (Gemini CLI),
`.github/skills` (Copilot). Preserve an existing installation and its local edits
when updating. Copy the complete package so references and helpers remain
together. Start a new session and check that the skill is discovered. For a host
without skills support, paste `SKILL.md` and the reference sections it names
into chat or the project's instruction file.

## Use

```text
(Shorthand shown as /pstack; use $pstack in Codex, or write "use the pstack skill to ..." anywhere.)

/pstack fix this bug: reproduce it, trace the cause, and verify the fix.

/pstack how does cancellation flow through this subsystem?

/pstack why was this caching boundary chosen?

/pstack architect this API before implementing it.

/pstack interrogate this branch for correctness and lifetime bugs.

/pstack arena compare two isolated implementation candidates.

/pstack benchmark-checklist assess these before/after measurements.

/pstack babysit check PR 123 and report outstanding blockers.

/pstack create-verification-skill for this app using its existing harness.

/pstack help choose a workflow for this task.

/pstack off
```

Use `pstack poteto-mode <task>` for the main router, or name a workflow
directly. Original `/how` and similar names are aliases within this skill, not
separate registered commands. The host can also pick the skill automatically
from its description; explicit invocation makes the intended workflow clear.

## Host behavior

The [host runtime adapter](references/host-runtime.md),
[native playbooks](references/playbooks.md), and
[native workflows](references/workflows.md) replace Cursor-specific execution.

The default inherits your current model and needs no setup. Optional setup
records agreed project workflow preferences in `.agents/pstack.json`, not global
host model settings. Delegation to subagents (when the host has them) requires
user or project authorization; without subagents the same passes run sequentially. Arena/swarm requests express parallel intent.
The package respects host concurrency, reports serial/same-model limitations,
and reviews actual artifacts.

GitHub (MCP server or `gh`), browser, terminal, worktree, and scheduling
tools are used when the host provides them. A check request reports
status; a read-only investigation stays read-only. PR publication, messages, tickets, merging, deployment, and future
monitoring follow the user's actual authorization. No Cursor rule files,
instruction-file edits, hooks, loop runs, or scheduled routines are installed by
loading the skill.

The [Benny guide](references/benny.md) adapts the optional automation pack. It
requires configured Slack/tracker access, exact source-thread coordinates, an
app-control adapter, feature maps, and action authorization. Installation alone
does not enable it. Missing required configuration prevents writes. Reproduction
requires before/after proof and produces bounded draft PRs, never automatic merges.

The original make-bot-ui workflow depends on a supported webhook service. Scheduled
routines alone do not supply its Cursor/Grok Bot endpoint or secret
card. The native workflow states that dependency explicitly.

## Files and requirements

`SKILL.md` is the only discoverable skill. Native references provide host-neutral
behavior; `references/upstream/` is a pinned, unchanged source reference. Original source links mentioning `SKILL.md`
resolve to `SKILL.md.source`; use the catalog for clickable local navigation.

Core engineering work needs the target project's source, tools, and appropriate
verification harness. The integrity checker uses Python 3.9+ and the standard
library. The logger uses Bash and ordinary command-line utilities. Neither
requires Bun, Node, a separate LLM service, or the original Cursor plugin.

The retained Bun/forge helpers are source material with their original runtime
requirements. They have not been ported or executed as host integrations.
Their preservation is separate from the native workflow's operational coverage.

## Verification and maintenance

From this package:

```bash
python3 scripts/check_package.py
python3 -m unittest discover -s tests -v
bash scripts/decision-log.sh work/decisions.tsv fix "Chosen change" \
  "Reason" "Evidence path" "Verified result"
```

For an independent comparison with the original checkout:

```bash
python3 scripts/check_package.py --source /path/to/cursor-plugins/pstack
```

If you have a skill-creator skill with a frontmatter validator installed, run
it on this directory as well.

The helper tests check source corruption/omission, accidental nested discovery,
and append-safe/sanitized decision records. Structural and integrity checks do
not prove every engineering workflow or external automation in a real project.
No host-specific performance benchmark or live Benny integration is claimed.

To update, review upstream changes against the pinned revision, preserve local
adaptation decisions, refresh the complete source manifest, and rerun checks.
Installed copies do not automatically update when GitHub changes.

## License and provenance

MIT, copyright 2026 Lauren Tan. The [original license](LICENSE) is retained in
the package and source snapshot. Reviewed revision:
[`ccb5507cec1546dc88135c1139c811e6c59115ba`](https://github.com/cursor/plugins/tree/ccb5507cec1546dc88135c1139c811e6c59115ba/pstack),
2026-10-08. See [provenance and adaptation notes](references/provenance.md).
This is a personal host-neutral adaptation, derived from earlier Codex and Claude Code ports;
no affiliation or endorsement is claimed.
