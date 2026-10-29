# Sources and adaptation boundaries

Reviewed for this adaptation: **2026-10-10**.

Primary source: [usestrix/strix](https://github.com/usestrix/strix), revision [`62b496430da5df5e9e79a190e7af6f92529883a3`](https://github.com/usestrix/strix/tree/62b496430da5df5e9e79a190e7af6f92529883a3). The machine-readable [baseline](upstream.json) records that commit, its tree, and a complete file inventory for update detection. The review focused on the sources below; the inventory is not a full source audit.

| Upstream source at the reviewed revision | Adapted purpose |
|---|---|
| [`AGENTS.md`](https://github.com/usestrix/strix/blob/62b496430da5df5e9e79a190e7af6f92529883a3/AGENTS.md), `README.md` | Consumer workflow map, local/cloud differences, artifact and exit-code semantics |
| `skills/application-security-testing`, `find-security-vulnerabilities-in-code`, `web-app-penetration-testing`, `api-security-testing`, `owasp-top-10-testing` | Asset selection, source/runtime correlation, scoped testing, auth/tenant cases, category coverage |
| `skills/penetration-testing-with-strix`, `managed-pentesting-with-strix`, `ci-security-scanning-with-strix`, `fix-security-vulnerabilities-with-strix` | Optional headless/managed integration, verified upload digest, budget/completion caveats, fix and retest loop |
| `strix/agents/prompts/system_prompt.jinja`, `strix/skills/coordination/source_aware_whitebox.md` | Mapping, hypotheses, static triage feeding dynamic testing; native Codex execution replaces the source runtime |
| `strix/skills/analysis/counterevidence.md`, `fix_verification.md`, `severity_calibration.md` | Named controls, unresolved proof gaps, separate confidence/severity, security closure and preserved behavior |
| `strix/skills/README.md`, specialist pack inventory, `strix/tools/reporting/tool.py` | Conditional specialist discovery, evidence/locations and deduplication; no Strix tool API is assumed in Codex |

All upstream relative paths above resolve under the linked reviewed tree. This package consolidates nine consumer skills and adapts selected methodology; it does not bundle their full text, the specialist pack library, scanners, Docker image, sandbox, agent runtime, managed client, or credentials. Specialist source packs can be fetched selectively at a pinned revision. Actual Strix execution remains an optional separately installed integration.

The Codex entrypoint, condensed playbooks, upstream checker, tests, UI metadata, and package README were authored/adapted on 2026-10-09. They preserve the evidence-led approach while replacing Strix-specific lifecycle calls and orchestration with capabilities actually available in Codex. Fixed scanner quotas, unsupported "every finding is proven" claims, presumed authorization, automatic cloud fallback, and implicit payment/upload/account changes are not inherited.

The upstream source is Apache-2.0, with **Copyright 2025 OmniSecure Inc.** in its license. The full source license is retained in [LICENSE](../LICENSE), and [NOTICE](../NOTICE) identifies this modified adaptation. No upstream `NOTICE` file was present at the reviewed revision. The adapted package is distributed under Apache-2.0. No affiliation or endorsement by Strix, OmniSecure, OpenAI, or OWASP is claimed.

Changes after the reviewed revision are governed by [upstream maintenance](upstream-maintenance.md). Checks do not silently advance this record or rewrite installed instructions.

## Reviewed update — 2026-10-09

Reviewed all 15 changed files since `278b6a280bfb458ef02187943df25ef8731e781f`,
including MCP catalog warmup/status, stream bounds and cancellation reasons,
provider/error logging, retry classification, cost tracking, and their regression
cases. Added connection-evidence and optional-engine diagnostic guidance. The
engine implementation and retry policy remain upstream runtime behavior, not
code or unconditional retry instructions installed in Codex. Consumer workflow
APIs and license notices did not change.

## Reviewed update — 2026-10-10

Reviewed all nine changed files since `f5a900416b6e1d8023e7c2ce11885232ffa8b806`,
including root tool registration, coordinator state, budget notices, runner
configuration, lifecycle errors, and their regression cases. Strix now allows
a caller-selected root finish tool while preserving `finish_scan` as its default.
This changes the optional engine's lifecycle; it does not add a native Codex
tool or change the installed assessment workflow. Consumer skills, specialist
knowledge packs, and license files are unchanged. Advanced the complete
file-inventory baseline after this review and corrected the stale revision in
NOTICE.

## Claude Code port

Ported from the Codex version (`strix-codex`) to Claude Code on 2026-10-10. The
package was renamed `strix`; the entrypoint, README, and active references now
name Claude Code tools (Bash, the Agent tool for authorized delegation, any
available browser tool) and install at `~/.claude/skills/strix/` with `/strix`
invocation. The Codex installer, structural-validator command, and
`agents/openai.yaml` UI metadata were dropped. The assessment method, upstream
baseline (`upstream.json`), checker, tests, LICENSE, and NOTICE are unchanged.

## Host-neutral adaptation

Made host-neutral for the open Agent Skills format. The entrypoint, README, and
active references no longer name one host: Claude Code-specific wording (Bash and
Agent tool names, `~/.claude/skills/` install path, `/strix` invocation, Claude
Code settings) became capability language (shell, subagents, browser automation)
with `<skill-dir>` and `~/.agents/skills/` as the install example. The
authorization, ownership, scope, and data-handling safeguards, the assessment
method, `upstream.json`, the checker, tests, LICENSE, and NOTICE are unchanged.

## Reviewed update — 2026-10-15

Reviewed the 13 commits from `62b496430da5df5e9e79a190e7af6f92529883a3` to
`ca20626f844b64e26755b7d78ae206ba8dd3acc9`.

Adopted: `429f621` (#1366), which requires dependency and CVE reports to cite
every usage site as a code location (file, exact lines, verbatim snippet,
label) in addition to the manifest line. Rewritten host-neutrally in
`reporting-and-fixes.md`, with reachability kept separate from severity.
Re-verified the CLI flags, headless and cloud exit codes, and stream-timeout
variables in `strix-and-ci.md` against `strix/interface/cli_args.py`,
`main.py`, `cloud/http.py` and `config/settings.py`; added the deep default
scan mode, the headless-only `--fail-on`, the `--max-budget-usd` alias, and the
note that exit 2 also appears for resume-selection errors.

Declined: `87f2d78` (#1520), which removed upstream's caveat that static
dependency evidence is a prioritization signal and not proof of exploitability
or of safety. This package keeps and states that caveat, because dropping it
would weaken safety guidance.

Skipped as engine internals with no effect on the host-neutral workflow:
runtime sandbox deferral (`4bf7541`, `0f8db1f`, `956a267`), Caido proxy
logging (`c5854e7`, `d8c00a8`), TUI target boxes (`b68cdb8`, `710fe7b`,
`442b3c3`), malformed tool-call replay (`ca20626`), tests (`e21f9ce`), and the
README update note (`f7a32ae`). The file-inventory baseline in `upstream.json`
was advanced to `ca20626` after this review.

## Reviewed update — 2026-10-20

Reviewed the 8 commits from `ca20626f844b64e26755b7d78ae206ba8dd3acc9` to
`aa2036f22942eed3ecd142169289a256a2e7acb7`. No consumer skill, knowledge pack,
system prompt, AGENTS.md, README, reporting-tool semantics, CLI flag, or exit
code changed in this range; all 30 changed files are engine code, tests, and two
documentation pages.

Adopted (documentation only, in `strix-and-ci.md`): the new optional
`STRIX_RUN_RECORD_TIMINGS` setting that adds `llm_requests` and `tool_calls`
timing records to `run.json` (`f4a7413`, `aa2036f`), and the `LLM_EXTRA_BODY` /
`DEDUPE_LLM_EXTRA_BODY` settings (`972f509`, #1495) with upstream's cautions:
fields are unvalidated, must not override request-shaping fields, and a
dedicated dedupe model never inherits the main model's headers or body fields.
Also noted that an operator-paused or budget-parked run is incomplete
(`6bd1cea`, `a0f8ea2`), consistent with the existing incomplete-run guidance.
No authorization, ownership, or data-handling safeguard was changed.

Skipped as engine internals with no effect on the host-neutral workflow: the
`exec_command` 30 s yield-cap and non-TTY description text (`5e9e69a`,
`2b98deb`), the running-process marker matching (`ee22e2b`), pause and budget
policy mechanics beyond the incomplete-run note, config-file decoding of saved
dict settings, and the new tests. The file-inventory baseline in `upstream.json`
was advanced to `aa2036f` after this review.

## Reviewed update — 2026-10-21

Reviewed the range from `aa2036f22942eed3ecd142169289a256a2e7acb7` to
`a3c31236bd6305784a501a3102dab0bda83f2317` (14 files).

Adopted (guidance only, in `reporting-and-fixes.md`): upstream's reporting tool
now keeps `http_exchange_ids` with an "stored without verification" warning when
the proxy times out, and still rejects ids the proxy reports missing. The skill
records the same rule host-neutrally: keep and mark unverified captured-exchange
identifiers when the capture store is unreachable, remove ones confirmed missing,
never invent them.

Skipped: the `{{ report_tool }}` template variable in `system_prompt.jinja` and
the `counterevidence.md` wording change that drops the hardcoded
`create_vulnerability_report` name (the skill already names no Strix-only tool as
callable), the `report_tool` plumbing in `factory.py`, `prompt.py`, and
`runner.py`, the lighter id-only existence query in `proxy/tools.py`, and
CI/packaging/lockfile and test churn. No authorization, ownership, scope, or
consent safeguard was changed upstream or in the skill. The file-inventory
baseline in `upstream.json` was advanced to `a3c31236`.

## Reviewed update — 2026-10-26

Reviewed the range from `a3c31236bd6305784a501a3102dab0bda83f2317` to
`4ac5dc65e4c02afc8fdc22878716a83d481f00fb` (50 files).

Adopted (guidance only): `skills/vulnerabilities/xss.md` now covers scriptless HTML
injection, second-order rendering and Unicode normalization. The XSS row in
`testing-playbooks.md` carries the decode/normalize/sanitize/encode ordering, the
second-order render paths, the rule to keep HTML injection separate from XSS, and the
original-versus-transformed value in evidence. The root agent's rule to follow up every
open coverage row before finishing is recorded host-neutrally in `assessment.md`: work or
delegate each unresolved row, and leave one open only with its blocker stated.

Skipped: opt-in parallel tool calls (`STRIX_PARALLEL_TOOL_CALLS`), soft per-skill turn
limits for sub-agents, the switch that turns the coverage-ledger tools off and the
`coverage_tools` Jinja conditionals added to `counterevidence.md`,
`source_aware_discovery.md`, `root_agent.md` and `scan_modes/diff.md`,
`STRIX_DOCKER_SANDBOX_DEVICES` pass-through, Vercel AI Gateway and OpenRouter README and
model-id changes, dependency and lockfile bumps, and test churn. These are Strix runtime
behavior, not guidance. No authorization, ownership, scope, or consent safeguard changed
upstream or in the skill. The file-inventory baseline in `upstream.json` was advanced to
`4ac5dc65`.
