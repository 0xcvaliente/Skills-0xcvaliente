# Apple Design

Apply Apple-inspired interface and fluid-motion principles when the user requests that direction or is designing gestures, sheets, momentum, spatial continuity, and translucent materials. Adapt the principles to the target platform and existing brand.

Adapted for Claude Code from [Emil Kowalski’s skills](https://github.com/emilkowalski/skills),
pinned to [`e8a175de22ae`](https://github.com/emilkowalski/skills/tree/e8a175de22ae1e49370fc144c1f3bb9aeedf988d).

## Workflow

1. Establish the requested platform, design direction, existing components, and accessibility needs.
2. Read the relevant guide sections for continuity, feedback, hierarchy, gestures, typography, materials, or springs.
3. During direct manipulation keep the element attached to the input; transfer release velocity into compatible settling motion.
4. Use platform-appropriate reduced motion and maintain contrast, keyboard access, and understandable navigation.
5. Verify rendered states, interruption, and device behavior; treat platform-derived numeric values as starting points.

## Output

An implementation or scoped critique grounded in the requested direction, with verification and tradeoffs.

## Use

```text
/apple-design refine this sheet’s drag and release behavior using physical continuity and reduced motion.
```

Claude can also pick the skill automatically when a request matches its
description.

Install the whole package as a personal Claude Code skill by copying its
directory:

```bash
cp -R apple-design ~/.claude/skills/
```

Claude Code then discovers it at `~/.claude/skills/apple-design/`; copy it into a
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
`/apple-design` identifies the desired workflow.

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
python3 .system/skill-creator/scripts/quick_validate.py ~/.claude/skills/apple-design
```

Structural validation and source hashes do not establish runtime UI quality.
Verify the actual target interaction for real work. MIT, copyright 2026 Emil
Kowalski; the exact [license](LICENSE) is retained.
