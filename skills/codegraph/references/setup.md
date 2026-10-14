# Setup and troubleshooting

Reviewed with CodeGraph 1.6.2 on macOS arm64. MCP registration differs per host;
the generic JSON below is host-neutral, and the one host-specific command shown
(Claude Code's `claude mcp add`, from Claude Code 2.1.296 help) is an example.
Use the chosen scope and preserve existing configuration; a setup request does not authorize changing other
agents or indexing unrelated repositories.

## Install the instruction package

Copy the entire `codegraph/` folder into the host's skills folder (see the
repository `INSTALL.md`; `~/.agents/skills/` is the shared user-level location),
preserving an existing copy's modifications:

```sh
cp -R codegraph ~/.agents/skills/
```

Discovery may need a new agent session.

## Install the reviewed runtime

With npm available:

```sh
npm install -g --ignore-scripts --no-audit --no-fund @colbymchenry/codegraph@1.6.2
CODEGRAPH_TELEMETRY=0 CODEGRAPH_NO_DOWNLOAD=1 codegraph --version
```

The published npm package selects a platform bundle with its own Node runtime;
it differs from a source checkout's build requirements. The npm shim still
needs Node to launch. Keep optional dependencies: they contain the platform
bundle. `CODEGRAPH_NO_DOWNLOAD=1` makes a missing bundle fail with guidance
rather than downloading a replacement when a command runs.

Without npm, inspect the appropriate pinned asset and checksum from the
[v1.6.2 release](https://github.com/colbymchenry/codegraph/releases/tag/v1.6.2).
Do not silently substitute an unreviewed rolling installer.

## Connect an MCP-capable host

Each host adds MCP servers its own way (a config file, a settings UI, or a CLI
command). Follow your host's MCP documentation, check for an existing
`codegraph` entry before changing anything, and preserve other servers. The
server is a local stdio process: `codegraph serve --mcp`, with
`CODEGRAPH_TELEMETRY=0` and `CODEGRAPH_NO_DOWNLOAD=1` in its environment.

Generic definition (many hosts accept this `mcpServers` shape in their MCP
config file; key names such as `type` vary by host):

```json
{
  "mcpServers": {
    "codegraph": {
      "command": "/absolute/path/to/codegraph",
      "args": ["serve", "--mcp"],
      "env": {"CODEGRAPH_TELEMETRY": "0", "CODEGRAPH_NO_DOWNLOAD": "1"}
    }
  }
}
```

Hosts launched from a GUI may need an absolute executable path when their PATH
differs from a terminal's. A direct platform-bundle `bin/codegraph` launcher on
macOS/Linux uses bundled Node and avoids the npm shim's dependency on Node being
on the GUI's PATH.

Edit an existing entry rather than adding a duplicate. Many hosts ask the user
to approve project-level MCP servers before connecting them; do not change
approval or trust settings to activate CodeGraph. For a server tied to one
repository, add `--path`, `/absolute/project` to its args. Otherwise pass an
explicit `projectPath` in queries.

Example (Claude Code only; other hosts use their own command or file):

```sh
claude mcp add --scope user codegraph \
  -e CODEGRAPH_TELEMETRY=0 -e CODEGRAPH_NO_DOWNLOAD=1 \
  -- codegraph serve --mcp
```

Restart or reload the host's MCP connections after changing configuration. An
enabled entry establishes registration, not that a running session has loaded
the tool. Each harness maintains its own MCP catalog; use CLI retrieval until
the host exposes `codegraph_explore` (hosts may prefix the name with the server
name).

The upstream alternative, `codegraph install --target=<agent> --location=global`,
writes host-specific configuration. In 1.6.2 the Claude Code target also writes
`mcp__codegraph__` auto-allow permissions to `~/.claude/settings.json`, can add a
`UserPromptSubmit` hook running `codegraph prompt-hook`, and writes a CodeGraph
section to `~/.claude/CLAUDE.md`; other targets write their own host files. Use
it only when those settings and instruction edits are wanted. `--yes` defaults to
`--target=auto`; do not configure all agents to satisfy a single-host setup
request.

## Initialize a selected project

Once indexing the particular repository is requested:

```sh
CODEGRAPH_TELEMETRY=0 codegraph init /absolute/project
CODEGRAPH_TELEMETRY=0 codegraph status /absolute/project
CODEGRAPH_TELEMETRY=0 codegraph explore --path /absolute/project --max-files 4 'knownSymbol'
```

`init` creates the database and indexes immediately; it does not connect any host to the MCP server.
Respect ignored paths and keep `.codegraph/` out of commits. Do not index a home
directory or filesystem root or override that refusal for orientation.

Use interactive initialization when watching is disabled and hooks have not
been requested: **1.6.2 `init --yes` installs fallback Git hooks in a Git
repository when live watching is disabled.** Choose manual syncing in the
prompt if hooks are outside scope. Non-Git temporary fixtures, as used by this
package's smoke test, have no such hook side effect.

An MCP session normally watches its primary project. Watching can lag edits;
additional `projectPath` indexes may be unwatched. Refresh an existing index:

```sh
CODEGRAPH_TELEMETRY=0 codegraph sync /absolute/project
```

Use `codegraph index /absolute/project` for a full rebuild when required by
schema/configuration changes or failed incremental recovery. Do not delete a
database or force an unlock to address an ordinary stale result; inspect the
reported lock owner and running writer first.

## Diagnose a failure

- **No tool:** check registration and reconnect; use the CLI if available.
  Installing a skill alone never exposes an MCP tool.
- **No index / wrong project:** verify the selected root and index location.
  Continue with source tools when indexing was not requested. Do not silently
  initialize every service in a monorepo.
- **Empty or ambiguous result:** check actual names, language and ignore rules,
  then inspect relevant source. A missing edge is not an absence proof.
- **Stale result:** read affected source, sync the authorized index, and retry.
  Disabled/recovering watching affects the whole index; per-file notices affect
  listed files.
- **Missing platform bundle:** check optional dependencies and registry access,
  then reinstall the pinned runtime. The offline flag deliberately blocks the
  shim's automatic GitHub download fallback.
- **Unexpected tool menu:** 1.6.2 defaults to explore only. Additional tools need
  `CODEGRAPH_MCP_TOOLS`; use the CLI for a one-off caller/status query rather
  than widening every session's menu.
- **After a runtime upgrade:** resolver fixes only reach an existing index after
  a full re-index of each project, which needs the user's authorization like any
  index write. Until then, treat old edges as the previous version's answer.

## Known 1.6.2 resolution gaps

Upstream `main` (reviewed 2026-10-10, unreleased after v1.6.2) fixes several
edge-resolution mistakes. With 1.6.2, confirm these patterns in source before
relying on callers, impact or call paths:

- **JS/TS default imports** can link to the first exported function (often a
  React Router `loader`/`action`) instead of the `export default` declaration.
  Fixed on upstream main in 33c1436, unreleased as of 2026-10-15; re-check
  after the next release.
- **React/Vue tags imported from a package** (`<Button>` from antd, MUI
  `<Typography>`, `<Link>`) can link to an unrelated local component with the
  same name; generic TSX tags such as `<List<Item> …/>` may not link at all.
- **React Router `lazy` routes** can point at the module's default export rather
  than the page the loader returns. Fixed on upstream main in a9781b0 (the page
  the loader picks), with barrel re-export follow-ups 16344af and e30a2c1,
  unreleased as of 2026-10-15; re-check after the next release.
- **C++** calls through `std::unique_ptr`/`shared_ptr`/`optional` `->`, bare or
  `this->` method calls, and range-`for` loop variables can resolve by name to
  the wrong class. Smart-pointer/`optional` `->` calls and calls on declared
  pointers, values and references are fixed on upstream main in c0f45c7 and
  fc0da38, unreleased as of 2026-10-15; bare or `this->` method calls and
  range-`for` loop variables were not individually verified. Re-check after
  the next release.
- **Go** calls through a variable bound from a type assertion can link to a
  same-named method elsewhere. Fixed on upstream main in 16bc05a (locals bound
  from a type assertion) and 3de5bef (calls made directly through an
  assertion), unreleased as of 2026-10-15; re-check after the next release.
- **Test detection**: files under `unittests/` or `*_unittest/` folders are
  ranked as production code.

Review 2026-10-15: upstream HEAD d0bb9be still has no release after v1.6.2, so
the pin is unchanged. The annotations above are an upstream-main review only,
not verified against the pinned runtime. `src/mcp/tools.ts` changed on main
since v1.6.2, but the default tool exposure did not (still `explore` only,
`CODEGRAPH_MCP_TOOLS` to widen), so the "defaults to explore only" note holds.

When a release after 1.6.2 ships these fixes, upgrade the pinned version above
and re-index affected projects.

Telemetry is disabled in these examples. Upstream documents usage statistics
separately from local source storage in
[TELEMETRY.md](https://github.com/colbymchenry/codegraph/blob/v1.6.2/TELEMETRY.md).
Use `CODEGRAPH_TELEMETRY=0` for CLI runs too; an MCP setting applies only to that
server process.

## Verify or remove

With Python 3.9+ and an installed runtime, run from the directory that contains
the package (for example `~/.agents/skills`):

```sh
python3 codegraph/scripts/smoke_test.py --codegraph /absolute/path/to/codegraph
```

The helper indexes only temporary non-Git TypeScript/Python fixtures, exercises
CLI retrieval and edit/sync behavior, then checks MCP from an unindexed root
with explicit `projectPath`. It disables telemetry, downloads, watching, and
daemon detachment, and terminates its server. It does not call an LLM, install
packages, change any agent's config, or measure savings.

Remove the `codegraph` entry from the host's MCP configuration to unregister it
(Claude Code example: `claude mcp remove codegraph --scope user`). Remove an
installed skill/runtime only when requested, after checking its path and
ownership.
`codegraph uninit /absolute/project` removes that index and may remove CodeGraph
sync hooks; it is not a routine troubleshooting step.
