# Emil Design Engineering

Polish or review interface details using Emil Kowalski’s design engineering guidance: component feedback, spacing, typography, shadows, motion, and interaction continuity. Use for UI craft or Emil-style polish; keep brand direction with frontend-design and project audits with ui-design.

Adapted for Claude Code from [Emil Kowalski’s skills](https://github.com/emilkowalski/skills),
pinned to [`e8a175de22ae`](https://github.com/emilkowalski/skills/tree/e8a175de22ae1e49370fc144c1f3bb9aeedf988d).

## Workflow

1. Inspect the brief, design system, components, and current rendered states.
2. Read only the relevant guide sections for the named craft problem; use the performance cheatsheet for performance diagnosis.
3. Improve concrete details while preserving visual identity, accessible semantics, and user constraints.
4. Use animate for motion construction, review-animations for critique, and mobile-native for mobile browser behavior when installed.
5. Verify the actual affected states and report measured results separately from craft judgment.

## Output

Requested UI changes, or a Before / After / Why review with concrete locations and verification limits.

## Use

```text
/emil-design-eng polish this settings panel while preserving its visual identity and existing components.
```

Claude can also pick the skill automatically when a request matches its
description.

Install the whole package as a personal Claude Code skill by copying its
directory:

```bash
cp -R emil-design-eng ~/.claude/skills/
```

Claude Code then discovers it at `~/.claude/skills/emil-design-eng/`; copy it into a
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
`/emil-design-eng` identifies the desired workflow.

## Package contents

- [SKILL.md](SKILL.md): concise routing, workflow, and output.
- [Detailed guide](references/guide.md): the complete working guidance, loaded by relevant section.
- [Claude Code notes](references/claude-notes.md): scope, tools, versions, input semantics, and verification.
- [Original entrypoint](references/upstream-SKILL.md.source): exact upstream source without nested skill discovery.
- [Source manifest](references/source-manifest.json) and [provenance](references/provenance.md).

- [Performance cheatsheet](references/performance-cheatsheet.md).

## Validation and license

The structural validator ships with the source collection, not with this
package. From the root of a clone of `0xcvaliente/codex-skills`, with Python
and PyYAML, point it at the installed copy:

```bash
python3 .system/skill-creator/scripts/quick_validate.py ~/.claude/skills/emil-design-eng
```

Structural validation and source hashes do not establish runtime UI quality.
Verify the actual target interaction for real work. MIT, copyright 2026 Emil
Kowalski; the exact [license](LICENSE) is retained.
