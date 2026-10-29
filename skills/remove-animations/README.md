# Remove Animations

Find animations an interface does not need and remove them: motion on keyboard actions, high-frequency surfaces, functional data, and decoration with no purpose, then clean up what they leave behind. Edits code only to subtract; never adds or retunes motion. Use when the app feels slow or over-animated, the user wants motion toned down, or asks which animations to remove. Use find-animation-opportunities to find places that should animate, animate to implement motion, improve-animations or review-animations for animations that stay, and animation-performance for dropped frames.

Adapted for Agent Skills–compatible agents from [Emil Kowalski’s skills](https://github.com/emilkowalski/skills),
pinned to [`a81dbca07f22`](https://github.com/emilkowalski/skills/tree/a81dbca07f2217b7103e510c0f13f8d5b017afc9).

## Workflow

1. Recon: stack, motion libraries, where motion lives, and a frequency map of animated surfaces.
2. Sweep the guide's hunt list; record candidates with `file:line` evidence.
3. Run each through the gate and record the deciding branch. Keep motion that has a stated purpose or is a rare first-time moment.
4. Check removal hazards (hidden start states, code waiting on the animation, exit timing, layout jumps, focus) before each delete or reduce.
5. Apply deletions and reductions, then remove orphaned code. Ask before dropping a dependency.
6. Verify with the type checker and tests if present, and grep for removed names.


## Output

Removed and reduced (location, was, verdict, deciding branch), kept with purpose (2 to 5, plus badly built animations for improve-animations), then cleanup and a short verdict naming what needs a real-device check.

## Use

```text
Use the remove-animations skill: the app feels over-animated; remove the motion it does not need.
```

Compatible agents can also select the skill automatically when a request matches its
description.

Install the whole package by copying its directory into any
[Agent Skills](https://agentskills.io)-compatible location. `~/.agents/skills/`
is read by several agents; each host also has its own folder (see
[INSTALL.md](../../INSTALL.md)):

```bash
cp -R remove-animations ~/.agents/skills/
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
naming the skill explicitly (for example "use the remove-animations skill") identifies the desired workflow.

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
