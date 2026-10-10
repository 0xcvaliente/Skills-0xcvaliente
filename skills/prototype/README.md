# Prototype UI Variants

Build genuinely different UI variants in an isolated prototype route or standalone page with a working picker. Use when the user requests alternatives to compare; promote a selected variant only when selection or integration is authorized.

Adapted for Claude Code from [Emil Kowalski’s skills](https://github.com/emilkowalski/skills),
pinned to [`e8a175de22ae`](https://github.com/emilkowalski/skills/tree/e8a175de22ae1e49370fc144c1f3bb9aeedf988d).

## Workflow

1. Respect the requested scope; inspect stack, tokens, personality, and surrounding context.
2. Choose distinct named directions on meaningful layout, density, interaction, or motion axes; use the user’s requested count.
3. Read PICKER.md and build a keyboard-accessible comparison harness isolated from production.
4. Verify every variant, realistic states, and picker controls in the browser when available.
5. Present honest tradeoffs and leave selection to the user unless already delegated. Promote and clean up only within that authorization.

## Output

A working picker, distinct alternatives, verified interactions, and the relevant selection/integration state.

## Use

```text
/prototype build three distinct pricing-card variants in an isolated route with a visual picker.
```

Claude can also pick the skill automatically when a request matches its
description.

Install the whole package as a personal Claude Code skill by copying its
directory:

```bash
cp -R prototype ~/.claude/skills/
```

Claude Code then discovers it at `~/.claude/skills/prototype/`; copy it into a
project's `.claude/skills/` instead for a project-scoped install. Preserve
local edits before replacing an existing copy. See the
[official skills documentation](https://docs.claude.com/en/docs/claude-code/skills).

## Claude Code behavior and requirements

The skill uses existing project tools, Bash, and whatever browser/app tooling
is available (for example Claude in Chrome, a Playwright MCP server, or the
desktop app's browser pane). It does not install a runtime by being loaded.
Read-only requests produce findings; requested fixes proceed within their scope.
Dependencies and version-sensitive APIs must match the actual project.
Physical-device, release build, and performance claims require corresponding
evidence. Claude selects the skill automatically from its scoped description;
explicit invocation with
`/prototype` identifies the desired workflow.

Exploration stays isolated from production. The user selects a winner unless
selection was already delegated; integration and cleanup preserve requested work.

## Package contents

- [SKILL.md](SKILL.md): concise routing, workflow, and output.
- [Detailed guide](references/guide.md): the complete working guidance, loaded by relevant section.
- [Claude Code notes](references/claude-notes.md): scope, tools, versions, input semantics, and verification.
- [Original entrypoint](references/upstream-SKILL.md.source): exact upstream source without nested skill discovery.
- [Source manifest](references/source-manifest.json) and [provenance](references/provenance.md).
- [PICKER.md](PICKER.md).

## Validation and license

The structural validator ships with the source collection, not with this
package. From the root of a clone of `0xcvaliente/codex-skills`, with Python
and PyYAML, point it at the installed copy:

```bash
python3 .system/skill-creator/scripts/quick_validate.py ~/.claude/skills/prototype
```

Structural validation and source hashes do not establish runtime UI quality.
Verify the actual target interaction for real work. MIT, copyright 2026 Emil
Kowalski; the exact [license](LICENSE) is retained.
