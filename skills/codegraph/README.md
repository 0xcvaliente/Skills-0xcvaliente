# CodeGraph

Trace code paths and change impact with CodeGraph's local source index. This
package adds a focused, host-neutral agent workflow around the existing CLI and MCP server;
it does not fork or bundle the runtime.

## Fit

Use it for cross-file callers, dependencies, unfamiliar implementation paths,
and refactors. For a small edit with complete context, inspect the supplied
files directly. Relationships can be heuristic or incomplete; source and the
project's compiler/tests establish correctness.

`repo-context` owns maintained project notes and evidence records. CodeGraph
supplies derived structural relationships. Either skill works on its own.

## Install and connect

Install the instruction package like any Agent Skill: copy the whole
`codegraph/` folder into your host's skills folder (see the repository's
`INSTALL.md`; `~/.agents/skills/` is the shared user-level location).

```sh
cp -R codegraph ~/.agents/skills/
```

For a new runtime/server installation with npm:

```sh
npm install -g --ignore-scripts --no-audit --no-fund @colbymchenry/codegraph@1.6.2
```

Then register the stdio MCP server in your host. Every host adds MCP servers its
own way (a config file or a CLI command; see your host's MCP documentation). The
generic server definition is:

```json
{
  "mcpServers": {
    "codegraph": {
      "command": "codegraph",
      "args": ["serve", "--mcp"],
      "env": {"CODEGRAPH_TELEMETRY": "0", "CODEGRAPH_NO_DOWNLOAD": "1"}
    }
  }
}
```

Check for an existing registration before changing it. Restart or reload the
host's MCP connections after changing configuration; GUI launchers may need an
absolute executable path. In each project you choose
to index, run `CODEGRAPH_TELEMETRY=0 codegraph init /absolute/project`.
The [setup guide](references/setup.md) explains separate skill/runtime/server
requirements, disabled-watcher Git-hook behavior, CLI fallback, and removal.

The default 1.6.2 MCP menu contains `codegraph_explore` only (hosts may prefix
the name with the server name). Its `projectPath`
argument chooses the intended indexed repository. A CLI example:

```sh
CODEGRAPH_TELEMETRY=0 codegraph explore --path /absolute/project --max-files 4 'submitOrder calculateTotal'
```

## Examples

```text
Use the codegraph skill to trace how submitOrder reaches calculateTotal in this
indexed repo, show callers that could break, and identify relevant tests.

Use the codegraph skill to configure CodeGraph for this host and index this project.

Use the codegraph skill to diagnose stale results in this monorepo; use source
tools for services that have no index.
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
upgrade the runtime. Name the skill in your prompt or let the host pick it from
its description.
