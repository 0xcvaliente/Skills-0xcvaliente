# Animate

Build web UI animations and transitions with purposeful timing, interruption, exits, and reduced motion. Use for implementing motion in a component; use review-animations for critique, improve-animations for a motion roadmap, and animate-expo for React Native.

Adapted for Claude Code from [Emil Kowalski’s skills](https://github.com/emilkowalski/skills),
pinned to [`e8a175de22ae`](https://github.com/emilkowalski/skills/tree/e8a175de22ae1e49370fc144c1f3bb9aeedf988d).

## Workflow

1. Inspect the interaction, frequency, existing tokens, and component behavior; keep focus and repeated actions immediate.
2. Name the motion purpose. Prefer no added motion when it provides no useful feedback or continuity.
3. Choose the smallest suitable implementation: CSS, WAAPI, or the project motion library. Read the guide decision sequence and RECIPES.md for the component.
4. Choose properties, easing, duration or spring, origin, interruption, exit, hover gating, and reduced motion together.
5. Implement and inspect rapid reversals, keyboard/touch behavior, and the rendered result.

## Output

Implementation, a concise rationale, and actual verification or remaining visual gaps.

## Use

```text
/animate animate this drawer with interruptible entry and exit, preserving our tokens and keyboard focus.
```

Claude can also pick the skill automatically when a request matches its
description.

Install the whole package as a personal Claude Code skill by copying its
directory:

```bash
cp -R animate ~/.claude/skills/
```

Claude Code then discovers it at `~/.claude/skills/animate/`; copy it into a
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
`/animate` identifies the desired workflow.

## Package contents

- [SKILL.md](SKILL.md): concise routing, workflow, and output.
- [Detailed guide](references/guide.md): the complete working guidance, loaded by relevant section.
- [Claude Code notes](references/claude-notes.md): scope, tools, versions, input semantics, and verification.
- [Original entrypoint](references/upstream-SKILL.md.source): exact upstream source without nested skill discovery.
- [Source manifest](references/source-manifest.json) and [provenance](references/provenance.md).
- [RECIPES.md](RECIPES.md).

## Validation and license

The structural validator ships with the source collection, not with this
package. From the root of a clone of `0xcvaliente/codex-skills`, with Python
and PyYAML, point it at the installed copy:

```bash
python3 .system/skill-creator/scripts/quick_validate.py ~/.claude/skills/animate
```

Structural validation and source hashes do not establish runtime UI quality.
Verify the actual target interaction for real work. MIT, copyright 2026 Emil
Kowalski; the exact [license](LICENSE) is retained.
