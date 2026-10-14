# Improve Animations

Audit existing motion across a requested codebase or subsystem and produce prioritized, self-contained improvement plans. Use for a motion roadmap; use review-animations for a single diff, animate for a focused implementation, and animation-performance for frame-drop diagnosis.

Adapted for Agent Skills–compatible agents from [Emil Kowalski’s skills](https://github.com/emilkowalski/skills),
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
Use the improve-animations skill: audit motion in this package and create prioritized implementation plans without changing app code.
```

Compatible agents can also select the skill automatically when a request matches its
description.

Install the whole package by copying its directory into any
[Agent Skills](https://agentskills.io)-compatible location. `~/.agents/skills/`
is read by several agents; each host also has its own folder (see
[INSTALL.md](../../INSTALL.md)):

```bash
cp -R improve-animations ~/.agents/skills/
```

Use the project-level equivalent (for example `.agents/skills/`) for a
project-scoped install. Preserve local edits before replacing an existing copy.

## Agent behavior and requirements

The skill uses existing project tools, the shell, and whatever browser/app tooling
is available (for example a Playwright MCP server, a browser extension, or a built-in
browser pane). It does not install a runtime by being loaded.
Read-only requests produce findings; requested fixes proceed within their scope.
Dependencies and version-sensitive APIs must match the actual project.
Physical-device, release build, and performance claims require corresponding
evidence. The agent selects the skill automatically from its scoped description;
naming the skill explicitly (for example "use the improve-animations skill") identifies the desired workflow.

An audit or review is a report by default. If fixes were requested in the same
request, implement and verify them rather than imposing another permission step.

## Package contents

- [SKILL.md](SKILL.md): concise routing, workflow, and output.
- [Detailed guide](references/guide.md): the complete working guidance, loaded by relevant section.
- [Agent notes](references/agent-notes.md): scope, tools, versions, input semantics, and verification.
- [Original entrypoint](references/upstream-SKILL.md.source): exact upstream source without nested skill discovery.
- [Source manifest](references/source-manifest.json) and [provenance](references/provenance.md).
- [AUDIT.md](AUDIT.md).
- [PLAN-TEMPLATE.md](PLAN-TEMPLATE.md).

## Validation and license

From the root of the `Skills-0xcvaliente` repository, run
`python3 scripts/validate.py skills/<name>` to check the structure of this package.

Structural validation and source hashes do not establish runtime UI quality.
Verify the actual target interaction for real work. MIT, copyright 2026 Emil
Kowalski; the exact [license](LICENSE) is retained.
