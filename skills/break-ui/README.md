# Break UI

Stress-test a component or screen with schema-backed and realistic worst-case data, empty/one/large collections, locales, and missing media. Build dev-only fixtures and report rendered failures; fix them only when requested.

Adapted for Claude Code from [Emil Kowalski’s skills](https://github.com/emilkowalski/skills),
pinned to [`e8a175de22ae`](https://github.com/emilkowalski/skills/tree/e8a175de22ae1e49370fc144c1f3bb9aeedf988d).

## Workflow

1. Map every rendered field, its boundary, schema limits, optionality, and collection states.
2. Read CATALOG.md; construct plausible worst-case, empty, one-item, and relevant large-list fixtures.
3. Inject fixtures through the component’s real data boundary and expose a dev-only toggle or isolated route.
4. Render the original component at representative sizes and inspect overflow, clipping, wrapping, hierarchy, and performance.
5. Report findings and proposed corrections. Apply and recheck fixes when the user requested them.

## Output

Reviewable fixture controls, actual rendered failures, locations, and scoped corrections or proposals.

## Use

```text
/break-ui stress-test this member list with worst-case data and report layout failures.
```

Claude can also pick the skill automatically when a request matches its
description.

Install the whole package as a personal Claude Code skill by copying its
directory:

```bash
cp -R break-ui ~/.claude/skills/
```

Claude Code then discovers it at `~/.claude/skills/break-ui/`; copy it into a
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
`/break-ui` identifies the desired workflow.

An audit or review is a report by default. If fixes were requested in the same
request, implement and verify them rather than imposing another permission step.

## Package contents

- [SKILL.md](SKILL.md): concise routing, workflow, and output.
- [Detailed guide](references/guide.md): the complete working guidance, loaded by relevant section.
- [Claude Code notes](references/claude-notes.md): scope, tools, versions, input semantics, and verification.
- [Original entrypoint](references/upstream-SKILL.md.source): exact upstream source without nested skill discovery.
- [Source manifest](references/source-manifest.json) and [provenance](references/provenance.md).
- [CATALOG.md](CATALOG.md).

## Validation and license

The structural validator ships with the source collection, not with this
package. From the root of a clone of `0xcvaliente/codex-skills`, with Python
and PyYAML, point it at the installed copy:

```bash
python3 .system/skill-creator/scripts/quick_validate.py ~/.claude/skills/break-ui
```

Structural validation and source hashes do not establish runtime UI quality.
Verify the actual target interaction for real work. MIT, copyright 2026 Emil
Kowalski; the exact [license](LICENSE) is retained.
