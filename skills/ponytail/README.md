# Ponytail

The smallest complete change, packaged as a standalone Agent Skills package. Adapted
from [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) 5.1.0.

The agent reads the task and connected code, reuses what the project already has,
and chooses the simplest implementation that meets the requirements. It keeps
necessary validation, error handling, security, accessibility, and meaningful
verification. Reviews and audits examine correctness and expected load as well
as opportunities to remove unnecessary code.

## Workflows

| Request | Result |
|---|---|
| Coding task | Complete implementation using existing project patterns, with relevant verification. |
| `lite` | Requested implementation plus a brief smaller alternative when useful. |
| `full` | Smallest complete solution; the default level. |
| `ultra` | Also challenges unnecessary scope while honoring explicit requirements. |
| `review` | Prioritized findings for a diff, branch, PR, commit, or named files, including connected callers. |
| `audit` | Repository or package assessment with explicit coverage and workload assumptions. |
| `debt` | Counted ledger of `shortcut:`, legacy `ponytail:`, or user-selected deferral comments, including missing revisit triggers. |
| `gain` | Attributed upstream benchmark figures and limitations; no claim of measured savings for this adaptation. |
| `help` / `off` | Usage guidance, or stop applying the skill in the current chat. |

Review, audit, debt, gain, and help are one-shot reports. Reviews and audits
produce findings by default; include a request to fix them when you want edits.

## Install and use

Ported from the `ponytail-codex` skill in `0xcvaliente/codex-skills` and now
host-neutral. Copy the complete package into any
[Agent Skills](https://agentskills.io)-compatible location (see
[INSTALL.md](../../INSTALL.md) for each host's folder). `~/.agents/skills/` is
read by several agents. From a directory that contains this skill folder, check
for an existing copy, then copy the package:

```bash
mkdir -p ~/.agents/skills
cp -R ponytail ~/.agents/skills/
```

Use the project-level equivalent (for example `.agents/skills/`) for a
project-scoped install.

```text
Use the ponytail skill: fix this bug in the shared helper and update affected callers.

Use the ponytail skill in lite mode: build the requested settings form using our components.

Use the ponytail skill in ultra mode: simplify this cache design for a single-process CLI.

Use the ponytail skill to review the staged changes, including affected callers.

Use the ponytail skill to audit this API package for bugs, expected load, and needless code.

Use the ponytail skill: debt. List our shortcuts and flag missing revisit triggers.

Use the ponytail skill: gain. Explain the upstream benchmark and its limits.

Stop using the ponytail skill (normal mode).
```

Compatible agents can pick the skill automatically for coding and Ponytail requests.
Naming the skill explicitly ("use the ponytail skill") makes the intended workflow clear. Levels are preferences in the current chat
while its context is available. This instruction package does not install hooks,
write global mode settings, or guarantee activation in every turn.

## Deliberate shortcuts

Use the project's comment syntax to record an accepted limit and when to revisit it:

```python
# ponytail: one worker only; revisit when adding workers; use a shared store
```

The debt workflow searches comments and excludes prose examples and string
literals. A marker without a meaningful revisit trigger is tagged `no-trigger`.
A shortcut cannot remove a requirement or necessary safety control.

## Requirements and verification

The workflow is instruction-only. It needs the target project's source and
appropriate tools/checks; Git is useful for diffs and `rg` for source searches.
No Ponytail runtime, Node dependency, external LLM account, or plugin is required.

`SKILL.md` holds the core workflow and its frontmatter metadata.
`references/` contains review/audit, shortcut ledger, benchmark, and provenance
guidance, loaded only when relevant.

Agents read the `SKILL.md` frontmatter when they load the skill; after
installing, start a new session and confirm that `ponytail` appears among the available skills.

Structural validation does not establish behavioral quality or benchmark
performance. Neither the original Codex adaptation nor this host-neutral port
has been independently benchmarked.

## License and source

Distributed under the retained upstream [MIT license](LICENSE), copyright
2026 DietrichGebert. Reviewed source revision:
[`9cc65d03aa2da1db7121b912d03596409ee340b8`](https://github.com/DietrichGebert/ponytail/tree/9cc65d03aa2da1db7121b912d03596409ee340b8),
2026-10-09. See [provenance](references/provenance.md) for inspected sources and
adaptation choices. No affiliation or endorsement is claimed.
