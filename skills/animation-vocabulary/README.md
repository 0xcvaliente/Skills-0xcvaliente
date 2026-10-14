# Animation Vocabulary

Identify the name of a motion effect from a visual or plain-language description, such as rubber-banding, stagger, morph, or origin-aware entry. Use for naming and disambiguation rather than implementing an animation.

Adapted for Agent Skills–compatible agents from [Emil Kowalski’s skills](https://github.com/emilkowalski/skills),
pinned to [`e8a175de22ae`](https://github.com/emilkowalski/skills/tree/e8a175de22ae1e49370fc144c1f3bb9aeedf988d).

## Workflow

1. Read the relevant glossary section and match the observed effect rather than isolated keywords.
2. Lead with the best term and a brief definition; distinguish one or two close alternatives when needed.
3. Label approximate matches and ask for the missing observable detail only when it would change the term.

## Output

The best matching term, a short definition, and useful disambiguation. No unsolicited implementation.

## Use

```text
Use the animation-vocabulary skill: what is the effect called when a sheet resists a drag past its boundary and snaps back?
```

Compatible agents can also select the skill automatically when a request matches its
description.

Install the whole package by copying its directory into any
[Agent Skills](https://agentskills.io)-compatible location. `~/.agents/skills/`
is read by several agents; each host also has its own folder (see
[INSTALL.md](../../INSTALL.md)):

```bash
cp -R animation-vocabulary ~/.agents/skills/
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
naming the skill explicitly (for example "use the animation-vocabulary skill") identifies the desired workflow.

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
