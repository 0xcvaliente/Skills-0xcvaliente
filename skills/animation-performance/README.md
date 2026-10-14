# Animation Performance

Diagnose and fix web animations that drop frames, stutter, or feel choppy: choose composite-only properties (transform, opacity), keep motion off a busy main thread with CSS or WAAPI, avoid per-frame React state and inherited CSS variable recalculation, bound blur cost, and use will-change only when measured. Use when an animation is janky, when picking which property to animate, or when choosing CSS vs JS motion on performance grounds. Use animate to implement motion, review-animations for critique, ui-animation for recording-based jank diagnosis, animate-expo for React Native, and vercel-react-best-practices for general React performance.

Adapted for Agent Skills–compatible agents from [Emil Kowalski’s skills](https://github.com/emilkowalski/skills),
pinned to [`2d228630ba14`](https://github.com/emilkowalski/skills/tree/2d228630ba1446365f614a108cb8252f1feda202).

## Workflow

1. List every animation in scope with its driver, animated properties, and what the page is doing while it plays.
2. Match the symptom in the guide's symptom table; name the cause before proposing any change.
3. Work the diagnosis order: properties, busy main thread, per-frame React state, inherited CSS variables, animated variables, blur, then `will-change` last.
4. Separate findings verified from source from those needing a profiler recording on a real mid-range device.
5. Report before editing unless fixes were requested.

## Output

Per finding: element and file location, cause, before and after, and verified-from-code versus needs-device-recording. Order by cost (layout before paint, busy main thread before idle).

## Use

```text
Use the animation-performance skill: this drawer drags laggily once the list grows; find why frames drop and fix it.
```

Compatible agents can also select the skill automatically when a request matches its
description.

Install the whole package by copying its directory into any
[Agent Skills](https://agentskills.io)-compatible location. `~/.agents/skills/`
is read by several agents; each host also has its own folder (see
[INSTALL.md](../../INSTALL.md)):

```bash
cp -R animation-performance ~/.agents/skills/
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
naming the skill explicitly (for example "use the animation-performance skill") identifies the desired workflow.

An audit or review is a report by default. If fixes were requested in the same
request, implement and verify them rather than imposing another permission step.

## Package contents

- [SKILL.md](SKILL.md): concise routing, workflow, and output.
- [Detailed guide](references/guide.md): the complete working guidance, loaded by relevant section.
- [Agent notes](references/agent-notes.md): scope, tools, versions, input semantics, and verification.
- [Original entrypoint](references/upstream-SKILL.md.source): exact upstream source without nested skill discovery.
- [Source manifest](references/source-manifest.json) and [provenance](references/provenance.md).

## Validation and license

From the root of the `Skills-0xcvaliente` repository, run
`python3 scripts/validate.py skills/<name>` to check the structure of this package.

Structural validation and source hashes do not establish runtime UI quality.
Verify the actual target interaction for real work. MIT, copyright 2026 Emil
Kowalski; the exact [license](LICENSE) is retained.
