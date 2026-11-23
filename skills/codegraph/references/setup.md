# Setup and troubleshooting

Reviewed with CodeGraph 1.6.2 on macOS arm64. MCP registration differs per host;
the generic JSON below is host-neutral, and the one host-specific command shown
(Claude Code's `claude mcp add`, from Claude Code 2.1.296 help) is an example.
Use the chosen scope and preserve existing configuration; a setup request does not authorize changing other
agents or indexing unrelated repositories. Release 1.6.3 (2026-11-17) was
reviewed in source on 2026-11-20 without running it; statements marked 1.6.3
below come from that review, and [What 1.6.3 changes](#what-163-changes)
explains why the pin has not moved. Release 1.6.4 (2026-11-20) was reviewed the
same way on 2026-11-23; [What 1.6.4 changes](#what-164-changes) lists what
differs from 1.6.3.

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
request. 1.6.3 adds nine more targets (IBM Bob, Factory Droid, Windsurf, Qwen
Code, DeepSeek Harness, Grok Build, Kimi Code, Qoder CLI, Pi), several of which
also get an instruction-file section, and the auto-allow permission list is
now written for the Qwen Code target too (`--no-permissions` skips it), so
`--target=auto` can touch more hosts than before.

## Initialize a selected project

Once indexing the particular repository is requested:

```sh
CODEGRAPH_TELEMETRY=0 codegraph init /absolute/project
CODEGRAPH_TELEMETRY=0 codegraph status /absolute/project
CODEGRAPH_TELEMETRY=0 codegraph explore --path /absolute/project --max-files 4 'knownSymbol'
```

`init` creates the database and indexes immediately; it does not connect any host to the MCP server.
Respect ignored paths and keep `.codegraph/` out of commits. Do not index a home
directory or filesystem root or override that refusal for orientation. From
1.6.3, `init --local-only` makes `.codegraph/` ignore itself so nothing of it
shows in `git status` (it also converts an initialized project), and system or
credential folders (`/etc`, `~/.ssh`, `~/.aws`, `~/.config` and anything inside
them) are refused as a project or as an MCP session's default project, however
the path is spelled or linked.

Use interactive initialization when watching is disabled and hooks have not
been requested: **1.6.2 `init --yes` installs fallback Git hooks in a Git
repository when live watching is disabled** (unchanged in the 1.6.3 source).
Choose manual syncing in the
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
- **Unexpected tool menu:** 1.6.2 through 1.6.4 default to explore only. Additional tools need
  `CODEGRAPH_MCP_TOOLS`; use the CLI for a one-off caller/status query rather
  than widening every session's menu.
- **After a runtime upgrade:** resolver fixes only reach an existing index after
  a full re-index of each project, which needs the user's authorization like any
  index write. Until then, treat old edges as the previous version's answer.
  From 1.6.3, `codegraph status` and the first MCP answer for a project say
  when its index was built by an older version; the rebuild is
  `codegraph index /absolute/project`. `codegraph sync` on such an index
  applies current edits and warns that untouched files still need the rebuild.

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

Review 2026-11-20: v1.6.3 (`ef4bd05`, released 2026-11-17) contains every fix
commit named above (33c1436, a9781b0, 16344af, e30a2c1, c0f45c7, fc0da38,
16bc05a, 3de5bef). Its changelog also covers the patterns that had no commit
here: package-imported React/Vue tags and generic TSX tags, C++ bare and
`this->` calls and range-`for` variables, and `unittests/`, `*_unittest/` and
`*_unittest.*` test detection (a folder named just `unittest/` still counts as
production code). This is a source and changelog review; nothing was run. The
gaps therefore still apply to a 1.6.2 runtime and to any index a 1.6.2 runtime
built, until that project is fully re-indexed with 1.6.3.

## What 1.6.3 changes

The pin stays at 1.6.2: this package moves it only after its smoke test passes
against the new runtime (see the [assessment](assessment.md#maintenance)), and
that run has not happened. 1.6.3 does carry security fixes (the sensitive-folder
refusal can no longer be bypassed through a link, junction or path spelling,
and the bundled Node.js moves to 24.22.1 for a Brotli decoder CVE), so for a
new install prefer running the smoke test against 1.6.3 and using it if it
passes, over installing 1.6.2 unexamined. Everything this guide says about
1.6.2 was checked against the 1.6.3 source and still holds unless noted here.

- **Unchanged:** `codegraph_explore` is still the only tool listed by default
  (`CODEGRAPH_MCP_TOOLS` widens the menu), `projectPath` selects the project,
  `CODEGRAPH_TELEMETRY=0` and `CODEGRAPH_NO_DOWNLOAD=1` work as before, and the
  `init`, `sync`, `index`, `status`, `explore`, `callers`, `impact` and
  `affected` commands keep their options.
- **`maxFiles`:** accepts 1 to 20. When omitted, the default now depends on
  project size (4 files below 150 indexed files, 5 below 500, 8 otherwise; it
  was 12). Output is also capped by characters, so a higher value spreads the
  same budget over more files.
- **`projectPath`** may name a file inside a project; the answer comes from
  that project.
- **Explore answers** leave out files ranked as tests or examples, first list
  query names the index has never seen, and can show part of a long function
  with a note on the lines cut. Read the source for what was cut or left out.
- **`impact`** stops at a safety limit on a heavily referenced symbol and
  reports the truncation; a truncated answer is not the full blast radius.
- **`callers`** lists each caller at every calling line and marks a function
  that calls itself. A qualified name such as `Format.Price` matches only the
  symbol whose scope is spelled that way.
- **`affected --filter`** matches the glob against the whole name: no slash
  means the file name at any depth, a slash means that folder at any depth, and
  a leading `/` anchors at the project root.
- **New commands:** `codegraph implementations <symbol>` (types that implement
  or extend a type; `--depth`, `--json`), `codegraph cycles [path]` (circular
  imports between files; `--json`; exit code 1 when any exist), and
  `codegraph files --format package`, `--tests`, `--no-tests`.
- **`codegraph status --strict`** exits non-zero when the index is missing,
  unfinished, out of date, or a language yielded no symbols.
- **`serve --mcp --no-telemetry`** disables telemetry for that server entry
  and the background server it starts, like `CODEGRAPH_TELEMETRY=0`. A
  background server already running without the flag keeps its own setting.
  The environment variable works on both versions, so the examples keep it.
- **Read commands during a rebuild** (`status`, `query`, `explore`, `callers`)
  no longer make a running `codegraph index` fail with "database is locked".
- **Coverage added:** Razor/Blazor views, Tauri frontend-to-Rust links,
  CodeIgniter 3, Drupal services and plugins, Next.js middleware/proxy links
  and MediatR handlers. The absence-of-edge cautions in the skill still apply.

## What 1.6.4 changes

Release 1.6.4 (`461a5d8`) was reviewed in source and changelog on 2026-11-23;
nothing was run. The pinned, tested version is still 1.6.2, for the reason
given under [What 1.6.3 changes](#what-163-changes). The points below apply
only from 1.6.4 and add to the 1.6.3 list.

- **Unchanged:** `codegraph_explore` is still the only tool listed by default,
  `CODEGRAPH_MCP_TOOLS` widens the menu, and `projectPath` selects the project.
- **Re-index after upgrading:** 1.6.4 reads code that indexes built by 1.6.3
  or earlier lack, so `codegraph status` and the first answer in each agent
  session flag those indexes as out of date. The rebuild is
  `codegraph index /absolute/project`, an index write that needs the user's
  authorization; `sync` leaves untouched files as the older version read them.
- **One-symbol questions:** an explore query that names a single symbol
  ("who calls `toValidURL`?", "what is `MAX_RETRIES`?") returns that symbol's
  source and every line that uses it, each with its enclosing function, tests
  listed apart. Ask about one name this way rather than with a broad query.
- **`affected` stops at process boundaries:** tests on the far side of an HTTP
  call, a queue or an event are no longer selected, because they usually mock
  that boundary. `--cross-tier` includes them, which fits end-to-end tests that
  make the real call. A shorter list does not show the other side is unaffected.
- **Changed-on-disk warning:** `callers`, `callees` and `impact` warn when a
  file in the answer changed after it was indexed, so its line numbers may be
  off. With `--json` the warning goes to stderr and the files are listed under
  `changedOnDisk`; read them, or sync, before relying on those lines.
- **`init`** on a project whose last index run was killed or failed now says the
  index is incomplete and to run `codegraph index`, instead of "Already
  initialized".
- **`status`** also reports edits, new files and deletions in gitignored source
  that `codegraph.json` `include` brings into the index.
- **PHP web-root includes:** `require $_SERVER['DOCUMENT_ROOT'] . '/inc/x.php'`
  links to its file when the includes settle which folder the server serves;
  otherwise it links to nothing rather than a guess. `"webRoot": "public"` (or
  `"."` for the project root) in `codegraph.json` names the folder, and the next
  sync applies it. Includes built from `__DIR__` need neither.
- **Git and the background server:** a sync no longer holds git's index lock,
  so a commit during one no longer fails with "index.lock: File exists". On a
  shared computer each session checks that the background server runs as the
  same user before sending it anything, and a server whose project folder was
  deleted exits within about half a minute.
- **Coverage and resolution:** Elysia (Bun) routes, Dart 3.13 primary
  constructors, newer Kotlin, Swift and Dart grammars, ASP.NET Core route names,
  and many call-resolution fixes (most in JavaScript/TypeScript, Python, Rust,
  C#, PHP and Java). They reach an existing index only after the full re-index.
- **Documented in this range, not new:** `serve --mcp --no-watch` (present in
  1.6.2) turns off the file watcher for slow filesystems, leaving the index to
  manual `codegraph sync`. `--force` on `init` or `index` only overrides the
  home-folder or filesystem-root refusal; a plain `codegraph index` already
  rebuilds from scratch, so routine rebuilds never need it. `--no-telemetry` is
  covered in the 1.6.3 list.

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
