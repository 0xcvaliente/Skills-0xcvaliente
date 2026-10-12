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
