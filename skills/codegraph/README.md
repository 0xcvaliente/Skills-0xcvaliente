# CodeGraph for Claude Code

Trace code paths and change impact with CodeGraph's local source index. This
package adds a focused Claude Code workflow around the existing CLI and MCP server;
it does not fork or bundle the runtime.

## Fit

Use it for cross-file callers, dependencies, unfamiliar implementation paths,
and refactors. For a small edit with complete context, inspect the supplied
files directly. Relationships can be heuristic or incomplete; source and the
project's compiler/tests establish correctness.

`repo-context` owns maintained project notes and evidence records. CodeGraph
supplies derived structural relationships. Either skill works on its own.

## Install and connect

Install the instruction package as a personal Claude Code skill at
`~/.claude/skills/codegraph/` (for example from a clone of the source collection
`0xcvaliente/codex-skills`):

```sh
cp -R codegraph ~/.claude/skills/
```

See [Claude Code skills](https://docs.claude.com/en/docs/claude-code/skills).

For a new runtime/server installation with npm:

```sh
npm install -g --ignore-scripts --no-audit --no-fund @colbymchenry/codegraph@1.6.2
claude mcp add --scope user codegraph -e CODEGRAPH_TELEMETRY=0 \
  -e CODEGRAPH_NO_DOWNLOAD=1 -- codegraph serve --mcp
```

Check an existing registration (`claude mcp get codegraph`) before changing it.
Restart Claude Code (or run `/mcp` to check); GUI launchers may need an
absolute executable path. In each project you choose
to index, run `CODEGRAPH_TELEMETRY=0 codegraph init /absolute/project`.
The [setup guide](references/setup.md) explains separate skill/runtime/server
requirements, disabled-watcher Git-hook behavior, CLI fallback, and removal.

The default 1.6.2 MCP menu contains `codegraph_explore` only (shown in Claude
Code as `mcp__codegraph__codegraph_explore`). Its `projectPath`
argument chooses the intended indexed repository. A CLI example:

```sh
CODEGRAPH_TELEMETRY=0 codegraph explore --path /absolute/project --max-files 4 'submitOrder calculateTotal'
```

## Examples

```text
/codegraph trace how submitOrder reaches calculateTotal in this indexed repo,
show callers that could break, and identify relevant tests.

/codegraph configure CodeGraph for Claude Code and index this project.

/codegraph diagnose stale results in this monorepo; use source tools for
services that have no index.
```

## Verification and maintenance

The optional compatibility test requires Python 3.9+ and an installed runtime:

```sh
python3 codegraph/scripts/smoke_test.py --codegraph /absolute/path/to/codegraph
```

It checks actual CLI/MCP behavior with isolated fixtures, including edits and
an unindexed server root. See the [assessment](references/assessment.md) for
research, observed checks, and limitations. This is not a token/cost benchmark
or a proof of complete language coverage.

- [SKILL.md](SKILL.md): agent workflow and scope.
- [references/setup.md](references/setup.md): installation and diagnosis.
- [references/assessment.md](references/assessment.md): fit and tradeoffs.
- [references/provenance.json](references/provenance.json): pinned source hashes.
- [scripts/smoke_test.py](scripts/smoke_test.py): runtime compatibility check.
- [LICENSE](LICENSE) and [NOTICE](NOTICE): terms and attribution.

Before upgrading, inspect release changes and installed help/tool schemas,
rerun the smoke test, and update setup, assessment, and provenance together.
The skill does not fetch upstream instructions at invocation or automatically
upgrade the runtime. Invoke it with `/codegraph` or let Claude pick it from
its description.
