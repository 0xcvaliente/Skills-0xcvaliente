# Write Swift

Write, review, or migrate Swift with value modeling, optionals/errors, ownership, protocols, generics, concurrency, performance, and Swift Testing. Use for Swift implementation and diagnostics; inspect toolchain and build flags before applying newer language features.

Adapted for Agent Skills–compatible agents (via an earlier Codex adaptation) from [Emil Kowalski’s skills](https://github.com/emilkowalski/skills),
pinned to [`e8a175de22ae`](https://github.com/emilkowalski/skills/tree/e8a175de22ae1e49370fc144c1f3bb9aeedf988d).

## Workflow

1. Inspect Swift/Xcode version, deployment target, language mode, actor-isolation settings, and package/app boundaries.
2. Read only the relevant guide sections for the model, diagnostic, concurrency, ARC, performance, or testing issue.
3. Use value types and explicit ownership where appropriate. Keep UI isolation correct and expensive work off the UI actor when required.
4. Treat Swift 6.2 concurrency behavior as dependent on actual compiler features/settings; do not rewrite a general-purpose library to main-actor-by-default.
5. Use project builds/tests and targeted diagnostics. Change compiler settings or adopt new features only when compatible and necessary.

## Output

Version-appropriate Swift code or findings, relevant build/test evidence, and unresolved runtime limitations.

## Use

```text
Use the write-swift skill: fix this Swift concurrency error while preserving the package’s public API and compiler settings.
```

Or describe a Swift task and let a compatible agent pick the skill automatically.

Install the whole package by copying it into any
[Agent Skills](https://agentskills.io)-compatible location (ported from
`write-swift` in `0xcvaliente/codex-skills`). `~/.agents/skills/` is read by
several agents; each host also has its own folder (see
[INSTALL.md](../../INSTALL.md)):

```bash
mkdir -p ~/.agents/skills
cp -R write-swift ~/.agents/skills/
```

Preserve local edits before replacing an existing copy.

## Agent behavior and requirements

The skill uses existing project tools and whatever browser, simulator, or
terminal tooling the agent session actually has. It does not install a runtime by being loaded. Read-only requests
produce findings; requested fixes proceed within their scope. Dependencies and
version-sensitive APIs must match the actual project. Physical-device, release
build, and performance claims require corresponding evidence. Normal automatic
selection is enabled with a scoped description; explicit invocation identifies
the desired workflow.

## Package contents

- [SKILL.md](SKILL.md): concise routing, workflow, and output.
- [Detailed guide](references/guide.md): the complete working guidance, loaded by relevant section.
- [Agent notes](references/agent-notes.md): scope, tools, versions, input semantics, and verification.
- [Original entrypoint](references/upstream-SKILL.md.source): exact upstream source without nested skill discovery.
- [Source manifest](references/source-manifest.json) and [provenance](references/provenance.md).

## Validation and license

Agents read the `SKILL.md` frontmatter when they load the skill; after
installing, start a new session and confirm that `write-swift` appears among the available skills.

Structural validation and source hashes do not establish runtime UI quality.
Verify the actual target interaction for real work. MIT, copyright 2026 Emil
Kowalski; the exact [license](LICENSE) is retained.
