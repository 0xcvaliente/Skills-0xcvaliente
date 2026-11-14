# Provenance

Adapted from [emilkowalski/skills](https://github.com/emilkowalski/skills/tree/e8a175de22ae1e49370fc144c1f3bb9aeedf988d/skills/pick-ui-library)
at `e8a175de22ae1e49370fc144c1f3bb9aeedf988d`, reviewed 2026-10-08. MIT, copyright 2026 Emil Kowalski.

The original complete entrypoint is retained byte for byte as
[upstream-SKILL.md.source](upstream-SKILL.md.source). All supporting files are
preserved in their original package layout. [The manifest](source-manifest.json)
records every original path and SHA-256. [The license](../LICENSE) is unchanged.

The Codex entrypoint adds precise routing, proportional verification, and scoped
outputs. The detailed working guide removes the canned readiness greeting and
frontmatter, adds navigation to long guides, adjusts resource links for their
reference location, and is interpreted
through local Codex notes. Cursor-only invocation metadata is replaced by normal
Codex selection metadata. No hooks, global settings, runtime libraries, or
background jobs are installed by the instruction package.

Timing and frequency tables remain authored craft defaults. User requirements,
project tokens, version compatibility, accessibility, and measured behavior govern
application. Full original content remains available for audit. No affiliation
or endorsement is claimed.

## Claude Code port

Ported from the Codex version (`0xcvaliente/codex-skills`) to Claude Code on
2026-10-10. `references/codex-notes.md` was renamed to
[agent-notes.md](agent-notes.md) (formerly claude-notes.md) and retitled "Claude Code adaptation notes",
with tool wording mapped to Claude Code (Bash, Read, WebSearch/WebFetch,
AskUserQuestion, the Agent tool, available browser tooling); links in SKILL.md,
README.md, and the guide were updated. README usage now shows `/pick-ui-library`, and
install and validation instructions target `~/.claude/skills/`. Retained
upstream files and the source manifest are unchanged.

## Host-neutral adaptation

Made host-neutral for the Agent Skills standard on 2026-10-12. `references/agent-notes.md` and the README were reworded for readability and neutrality (shell, file/image reading, ask-the-user capability). Upstream files and the source manifest are unchanged.
2026-11-14: Reviewed upstream f7ce8c02d6e3c8f0d980a44c57bcc41a40254349..0f2e23b32bb1265e84cff8d3e75785fec953fb1b (fixes to wrong APIs and cross-skill contradictions). Adopted the changed SKILL.md lines in references/guide.md; the frontmatter description change was skipped because the local description is its own. The upstream-SKILL.md.source and source-manifest.json pins are unchanged.
