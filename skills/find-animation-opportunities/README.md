# Find Animation Opportunities

Inspect a UI for state changes that would benefit from purposeful motion and identify places that should remain immediate. Use for a read-only motion opportunity pass; use animate to implement selected opportunities.

Adapted for Claude Code from [Emil Kowalski’s skills](https://github.com/emilkowalski/skills),
pinned to [`e8a175de22ae`](https://github.com/emilkowalski/skills/tree/e8a175de22ae1e49370fc144c1f3bb9aeedf988d).

## Workflow

1. Inspect actual states, triggers, frequency, user attention, and current motion.
2. Read the guide’s discovery gates and reject motion with no clear feedback, orientation, or continuity purpose.
3. Recommend a small prioritized set with element, trigger, purpose, properties, timing, and reduced-motion behavior.
4. Name frequent actions and reading surfaces that should remain immediate.

## Output

A scoped opportunity report and deliberate no-animation decisions. No source edits unless requested.

## Use

```text
/find-animation-opportunities find useful motion opportunities in this UI and tell me which interactions should stay instant.
```

Claude can also pick the skill automatically when a request matches its
description.

Install the whole package as a personal Claude Code skill by copying its
directory:

```bash
cp -R find-animation-opportunities ~/.claude/skills/
```

Claude Code then discovers it at `~/.claude/skills/find-animation-opportunities/`; copy it into a
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
`/find-animation-opportunities` identifies the desired workflow.

An audit or review is a report by default. If fixes were requested in the same
request, implement and verify them rather than imposing another permission step.

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
python3 .system/skill-creator/scripts/quick_validate.py ~/.claude/skills/find-animation-opportunities
```

Structural validation and source hashes do not establish runtime UI quality.
Verify the actual target interaction for real work. MIT, copyright 2026 Emil
Kowalski; the exact [license](LICENSE) is retained.
