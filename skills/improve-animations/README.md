# Improve Animations

Audit existing motion across a requested codebase or subsystem and produce prioritized, self-contained improvement plans. Use for a motion roadmap; use review-animations for a single diff and animate for a focused implementation.

Adapted for Claude Code from [Emil Kowalski’s skills](https://github.com/emilkowalski/skills),
pinned to [`e8a175de22ae`](https://github.com/emilkowalski/skills/tree/e8a175de22ae1e49370fc144c1f3bb9aeedf988d).

## Workflow

1. Pin audit scope, interaction frequency, and current motion stack.
2. Read AUDIT.md and inventory actual motion implementations, shared tokens, and repeated defects.
3. Prioritize removal, simplification, responsiveness, interruption, accessibility, and measured performance before decoration.
4. Use PLAN-TEMPLATE.md for actionable plans with paths, observed issues, proposed changes, and acceptance checks.
5. Leave application source unchanged unless implementation was also requested.

## Output

Prioritized findings and implementation plans, distinguishing inspected code, runtime proof, and uncovered areas.

## Use

```text
/improve-animations audit motion in this package and create prioritized implementation plans without changing app code.
```

Claude can also pick the skill automatically when a request matches its
description.

Install the whole package as a personal Claude Code skill by copying its
directory:

```bash
cp -R improve-animations ~/.claude/skills/
```

Claude Code then discovers it at `~/.claude/skills/improve-animations/`; copy it into a
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
`/improve-animations` identifies the desired workflow.

An audit or review is a report by default. If fixes were requested in the same
request, implement and verify them rather than imposing another permission step.

## Package contents

- [SKILL.md](SKILL.md): concise routing, workflow, and output.
- [Detailed guide](references/guide.md): the complete working guidance, loaded by relevant section.
- [Claude Code notes](references/claude-notes.md): scope, tools, versions, input semantics, and verification.
- [Original entrypoint](references/upstream-SKILL.md.source): exact upstream source without nested skill discovery.
- [Source manifest](references/source-manifest.json) and [provenance](references/provenance.md).
- [AUDIT.md](AUDIT.md).
- [PLAN-TEMPLATE.md](PLAN-TEMPLATE.md).

## Validation and license

The structural validator ships with the source collection, not with this
package. From the root of a clone of `0xcvaliente/codex-skills`, with Python
and PyYAML, point it at the installed copy:

```bash
python3 .system/skill-creator/scripts/quick_validate.py ~/.claude/skills/improve-animations
```

Structural validation and source hashes do not establish runtime UI quality.
Verify the actual target interaction for real work. MIT, copyright 2026 Emil
Kowalski; the exact [license](LICENSE) is retained.
