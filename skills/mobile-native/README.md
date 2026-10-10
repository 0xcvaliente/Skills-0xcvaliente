# Mobile Native Web

Fix mobile web and PWA platform details such as sticky hover, viewport units, input zoom, touch feedback, scrolling, safe areas, keyboard layout, and theme chrome. Use for web apps that feel wrong on a phone; use animate-expo for React Native.

Adapted for Claude Code from [Emil Kowalski’s skills](https://github.com/emilkowalski/skills),
pinned to [`e8a175de22ae`](https://github.com/emilkowalski/skills/tree/e8a175de22ae1e49370fc144c1f3bb9aeedf988d).

## Workflow

1. Match the reported symptom to the guide and inspect the existing viewport, styles, and support matrix.
2. Apply capability queries, suitable viewport units, safe-area padding, and input/gesture semantics where their rationale applies.
3. Keep zoom and selectable content available. Separate immediate press feedback from action activation.
4. Avoid global scroll/selection suppression on document content and preserve native link behavior.
5. Verify available browser/keyboard states and state which behaviors still require a physical device.

## Output

Focused CSS/meta/interaction fixes with reasons and honest hardware-validation limits.

## Use

```text
/mobile-native fix this mobile web screen’s viewport, input zoom, safe areas, and sticky hover behavior.
```

Claude can also pick the skill automatically when a request matches its
description.

Install the whole package as a personal Claude Code skill by copying its
directory:

```bash
cp -R mobile-native ~/.claude/skills/
```

Claude Code then discovers it at `~/.claude/skills/mobile-native/`; copy it into a
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
`/mobile-native` identifies the desired workflow.

## Package contents

- [SKILL.md](SKILL.md): concise routing, workflow, and output.
- [Detailed guide](references/guide.md): the complete working guidance, loaded by relevant section.
- [Claude Code notes](references/claude-notes.md): scope, tools, versions, input semantics, and verification.
- [Original entrypoint](references/upstream-SKILL.md.source): exact upstream source without nested skill discovery.
- [Source manifest](references/source-manifest.json) and [provenance](references/provenance.md).

## Validation and license

The structural validator ships with the source collection, not with this
package. From the root of a clone of `0xcvaliente/codex-skills`, with Python
and PyYAML, point it at the installed copy:

```bash
python3 .system/skill-creator/scripts/quick_validate.py ~/.claude/skills/mobile-native
```

Structural validation and source hashes do not establish runtime UI quality.
Verify the actual target interaction for real work. MIT, copyright 2026 Emil
Kowalski; the exact [license](LICENSE) is retained.
