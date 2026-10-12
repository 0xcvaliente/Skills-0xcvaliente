# Animate Expo

Build or fix React Native and Expo animations, gestures, sheets, screen transitions, and haptics. Use the project’s compatible Reanimated, Gesture Handler, and navigation APIs; use animate for web motion.

Adapted for Agent Skills–compatible agents from [Emil Kowalski’s skills](https://github.com/emilkowalski/skills),
pinned to [`e8a175de22ae`](https://github.com/emilkowalski/skills/tree/e8a175de22ae1e49370fc144c1f3bb9aeedf988d).

## Workflow

1. Inspect Expo SDK, React Native, architecture, Reanimated/Worklets, gesture, and navigation versions before choosing APIs.
2. Name purpose and frequency, then choose compatible native primitives and a UI-runtime motion path for continuous gestures.
3. Read the matching guide/RECIPES.md section; preserve velocity and interruption, reduce motion, and accessible alternatives.
4. Keep per-frame updates out of React state. Add dependencies only when needed and compatible with the existing SDK.
5. Build and check the target platform; distinguish simulator/emulator results from release-build physical-device evidence.

## Output

Native code, relevant build/probe results, and explicit device-only validation gaps.

## Use

```text
Use the animate-expo skill: add a gesture-driven sheet in this Expo app using its installed SDK and motion stack.
```

Compatible agents can also select the skill automatically when a request matches its
description.

Install the whole package by copying its directory into any
[Agent Skills](https://agentskills.io)-compatible location. `~/.agents/skills/`
is read by several agents; each host also has its own folder (see
[INSTALL.md](../../INSTALL.md)):

```bash
cp -R animate-expo ~/.agents/skills/
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
naming the skill explicitly (for example "use the animate-expo skill") identifies the desired workflow.

## Package contents

- [SKILL.md](SKILL.md): concise routing, workflow, and output.
- [Detailed guide](references/guide.md): the complete working guidance, loaded by relevant section.
- [Agent notes](references/agent-notes.md): scope, tools, versions, input semantics, and verification.
- [Original entrypoint](references/upstream-SKILL.md.source): exact upstream source without nested skill discovery.
- [Source manifest](references/source-manifest.json) and [provenance](references/provenance.md).
- [RECIPES.md](RECIPES.md).

## Validation and license

From the root of the `agent-skills-0xcvaliente` repository, run
`python3 scripts/validate.py skills/<name>` to check the structure of this package.

Structural validation and source hashes do not establish runtime UI quality.
Verify the actual target interaction for real work. MIT, copyright 2026 Emil
Kowalski; the exact [license](LICENSE) is retained.
