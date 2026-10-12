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
