# Assessment: CodeGraph as an agent skill

Research date: 2026-10-09. Decision: **adopt as an optional structural-retrieval
companion**, with a separate runtime and project index. The research below was
done for the Codex version of this skill; it was ported to Claude Code on
2026-10-10 (setup rewritten for `claude mcp`, runtime findings unchanged).

## Reviewed artifacts

- [CodeGraph](https://github.com/colbymchenry/codegraph), main revision
  `b635dd467f0578926a9c01a37b9d28d2b26689f1`.
- Stable [v1.6.2](https://github.com/colbymchenry/codegraph/releases/tag/v1.6.2),
  source revision `6560052a6f856855d3f71eee838fd66ccfa4285d`, published
  2026-10-03; npm's latest tag was also 1.6.2 at review time.
- Released npm packages `@colbymchenry/codegraph@1.6.2` and the macOS arm64
  platform bundle, plus local `codex-cli 0.162.1` help/configuration behavior.
- The collection's `repo-context` workflow and packaging conventions.

Main and a release are distinct artifacts. Examples target the release;
[provenance.json](provenance.json) records hashes from the release tag.

## Why it fits

CodeGraph parses symbols and resolves edges into a SQLite index, then supplies
CLI/MCP retrieval. That supports discovery about connected code without
replacing human architecture prose. The source has dedicated agent integrations
(including Claude Code), so a skill can teach query scope, freshness and
interpretation without adding a parser or graph engine to this collection.

This integrates a tool rather than converting an upstream skill. The runtime
stays separately distributed and pinned; the package contains original integration
guidance and a small behavioral compatibility helper.

| Need | Owner |
|---|---|
| Project map, architecture notes, evidence records | `repo-context` |
| Parsed callers, dependencies, candidate change impact | `codegraph` |
| Runtime correctness and required validation | Project source, compiler, tests |

An index is derived data; a note records interpretation. Neither makes the
other automatically correct. Cross-links permit combined use without requiring
either package or rewriting existing architecture records.

## Tradeoffs

- **Coverage:** name resolution and synthesized framework edges can be
  ambiguous. Missing edges do not prove isolation or dead code. See the
  [release server guidance](https://github.com/colbymchenry/codegraph/blob/v1.6.2/src/mcp/server-instructions.ts)
  and [resolution code](https://github.com/colbymchenry/codegraph/tree/v1.6.2/src/resolution).
- **Freshness:** watching may lag or be disabled; secondary `projectPath`
  indexes can be unwatched. Inspect response notices, read affected source and
  sync when needed.
- **Context:** upstream reports discovery savings in its own benchmarks, while
  [its residual-context analysis](https://github.com/colbymchenry/codegraph/blob/b635dd467f0578926a9c01a37b9d28d2b26689f1/docs/benchmarks/residual-context-occupancy.md)
  reports larger retained retrieval context. This adaptation claims no
  savings percentage. Keep queries focused and measure representative tasks.
- **Setup side effects:** the [Claude Code installer target](https://github.com/colbymchenry/codegraph/blob/v1.6.2/src/installer/targets/claude.ts)
  can also write auto-allow permissions, an opt-in prompt hook, and a
  `CLAUDE.md` instruction block (observed in the installed 1.6.2 bundle).
  Native MCP registration (`claude mcp add`) avoids that. Disabled-watch
  `init --yes` can install Git hooks; see
  [offerWatchFallback](https://github.com/colbymchenry/codegraph/blob/v1.6.2/src/installer/index.ts).
- **Networking:** local source storage and [usage telemetry](https://github.com/colbymchenry/codegraph/blob/v1.6.2/TELEMETRY.md)
  are separate. Setup disables telemetry and the npm launcher's missing-bundle
  download fallback during queries.
- **Host loading:** an enabled user-level Claude Code entry may need a restart
  (check with `/mcp`) and does not alter another harness's live MCP catalog.
  CLI retrieval remains usable.

The adaptation reuses adequate current results while permitting source
verification proportional to the actual task. It does not inherit upstream's
unconditional preference against file reading.

## Verification

The smoke test uses the released runtime without an LLM or paid service:

- TypeScript/Python symbol retrieval and cross-file caller resolution.
- Explore containing named entrypoint/callee source.
- Impact and transitive affected-test discovery on a changed dependency.
- Edited source after explicit incremental sync.
- MCP initialization and default explore-only discovery from an unindexed
  server root, then querying an indexed project via `projectPath`.
- Unindexed-project guidance and successful subsequent indexed queries.
- Disabled telemetry, downloads, watching and daemon detachment in fixtures.

Actual commands, versions, and outcomes are recorded in
[verification.json](verification.json). These checks establish compatibility
on the reviewed platform, not all languages, operating systems, project sizes,
automatic-watcher behavior, or comparative token use. Registration and tool
loading in Claude Code have not been separately verified.

## Maintenance

Review future CLI flags, MCP schema/default allowlist, freshness policy,
installer side effects, npm launcher and telemetry controls. Rerun the helper
before changing the pinned version and manifest. Do not advance the reviewed
revision merely because a release exists. The retained MIT notice attributes
CodeGraph; its runtime remains separately distributed by the author.
