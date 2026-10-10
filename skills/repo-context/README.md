# Repo Context

`repo-context` helps an agent navigate a repository using compact, maintained architecture notes and a local evidence-checking helper. Its goal is to reduce repeated discovery while keeping current source and tests authoritative.

The helper creates filename-based maps and checks recorded evidence for changes. It does not infer imports, runtime architecture, or data flows, and an unchanged evidence record does not prove that a note's claims are correct.

The optional [CodeGraph companion](../codegraph/README.md) supplies parsed callers,
dependencies, and candidate change impact when its runtime and project index
are available. Repo Context continues to own maintained notes and evidence
records. Both packages work independently; neither mandates setting up the other.

## When to use it

Use it when entering an unfamiliar repository, resuming substantial work, locating related areas for a multi-file change, or maintaining a small project map. Skip the full workflow for a trivial edit whose context is already supplied.

Existing README and architecture documents come first. If the project has `docs/agent-context/INDEX.md`, follow the relevant links instead of loading every note. Create additional notes only for useful knowledge that is not already maintained elsewhere.

## How it works

1. Resolve the repository root and applicable instructions.
2. Check a bounded summary of changes since the local map snapshot.
3. Check an applicable note's recorded evidence before relying on it.
4. Inspect source and tests when a note is unreviewed, stale, or insufficient.
5. Keep concise navigation, architecture, module, and recent-work records in the project.
6. Record evidence only after actually verifying a note against real files and relevant scopes.

`UNREVIEWED` and `RECHECK` call for targeted inspection. `UNCHANGED RECORDED EVIDENCE` describes file state, not semantic correctness. Local review records remain local so another clone begins with an honest unreviewed state.

## Helper commands

From the repository you are studying, run the installed helper by its full path:

```bash
python3 "$HOME/.claude/skills/repo-context/scripts/repo_context.py" status --limit 20
python3 "$HOME/.claude/skills/repo-context/scripts/repo_context.py" files --scope src --match '*auth*' --limit 25
```

Other subcommands include `refresh`, `check`, and `review`; [SKILL.md](SKILL.md) explains their use. Adjust scopes to real project paths.

## Requirements and output

The helper requires Python 3.9+ and Git. It does not require a network service or an external memory database. Outputs include repository notes and local map or review metadata.

The skill preserves existing edits and avoids storing secrets, personal records, or raw logs in notes. Committing, pushing, global configuration changes, hooks, and watchers require separate authorization under its instructions.

## Example request

```text
/repo-context orient me to this repository's authentication area,
check the relevant architecture note, and update only stale claims.
```

## Package guide

- [SKILL.md](SKILL.md): navigation, evidence, and note-maintenance workflow.
- [scripts/repo_context.py](scripts/repo_context.py): map, inventory, and evidence helper.
- [references/note-template.md](references/note-template.md): note format.

Install it as a personal Claude Code skill by copying this directory to `~/.claude/skills/repo-context/` (for example `cp -R repo-context ~/.claude/skills/`); the helper commands above assume that location. Invoke it with `/repo-context` or let Claude pick it from its description. See [Claude Code skills](https://docs.claude.com/en/docs/claude-code/skills).
