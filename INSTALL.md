# Install

Skills follow the open [Agent Skills](https://agentskills.io) format: a folder with a `SKILL.md` (frontmatter `name` + `description`) and optional `references/`, `scripts/`, `assets/`. Any compatible host can load them.

## Where hosts look

| Host | User-level folder | Project-level folder |
|---|---|---|
| Codex | `~/.agents/skills` | `.agents/skills` |
| Gemini CLI | `~/.gemini/skills`, `~/.agents/skills` | `.gemini/skills`, `.agents/skills` |
| GitHub Copilot | `~/.copilot/skills`, `~/.agents/skills` | `.github/skills`, `.claude/skills`, `.agents/skills` |
| OpenCode | `~/.config/opencode/skills`, `~/.claude/skills`, `~/.agents/skills` | `.opencode/skills`, `.claude/skills`, `.agents/skills` |
| pi | `~/.agents/skills` | `.agents/skills` (searched up to the repo root) |
| Cursor | (see Cursor docs) | `.cursor/skills`, `.agents/skills` |
| Claude Code | `~/.claude/skills` | `.claude/skills` |

`~/.agents/skills` is the shared location: install there once and most hosts see it. Add the Claude Code folder separately. Locations change between host releases; check your host's skills documentation if a skill does not appear.

## Script install

```sh
git clone https://github.com/0xcvaliente/agent-skills-0xcvaliente.git
cd agent-skills-0xcvaliente

scripts/install.sh --list                      # skills and targets
scripts/install.sh --target agents             # ~/.agents/skills (Codex, Gemini CLI, Copilot, OpenCode)
scripts/install.sh --target claude             # ~/.claude/skills
scripts/install.sh --target agents,claude ui-design animate   # only some skills
scripts/install.sh --target project --dest ./.agents/skills   # into a project
scripts/install.sh --copy --target agents      # copy instead of symlink
```

By default each skill is **symlinked**, so `git pull` updates installed skills. Existing destinations are skipped, never overwritten. Pass `--force` to replace.

Start a new session after installing; most hosts read skills at startup.

## Manual install

```sh
cp -R skills/ui-design ~/.agents/skills/
```

Copy the whole folder so relative links and bundled scripts keep working.

## Hosts without skills support

Paste the skill's `SKILL.md` and the `references/` files it names into the chat or into the project's instruction file (`AGENTS.md`, `GEMINI.md`, `.github/copilot-instructions.md`). Skills are plain Markdown and avoid host-specific syntax. Scripts need Python 3 and are optional unless a skill's requirements say otherwise.

## Check an install

```sh
python3 scripts/validate.py                 # every skill
python3 scripts/validate.py skills/animate  # one skill
```
