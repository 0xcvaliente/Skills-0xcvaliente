# Strix

An evidence-led application security skill for Claude Code, adapted from [usestrix/strix](https://github.com/usestrix/strix). Claude maps the target, tests concrete hypotheses, validates findings, reports coverage, and verifies requested fixes using the tools available in the session.

The package consolidates Strix's nine consumer workflow areas into one Claude Code entrypoint. It includes optional instructions for the actual Strix CLI, managed platform, and security CI. It does **not** include or replace Strix's executable agent engine, Docker sandbox, scanners, specialist knowledge library, or cloud service. Native assessment works without installing Strix or configuring another LLM account.

## Scope and outputs

| Request | Result |
|---|---|
| Application or source-code assessment | Prioritized, deduplicated findings with source/endpoint locations and a coverage ledger |
| PR or working-tree security review | Verified diff scope plus analysis of callers and shared controls |
| Web/API testing | Scoped proof using test identities, real authorization boundaries, and legitimate control cases |
| OWASP assessment | An edition-labeled category report with explicit partial and untested coverage |
| Vulnerability remediation | Root-cause patch, original proof replay, bypass/normal-case checks, and relevant project tests |
| Existing Strix findings | Evidence review and fixes from Markdown, JSON, SARIF, or authorized managed records |
| Strix or security CI setup | Concrete optional integration with budgets, artifact association, and incomplete-run handling |
| Upstream maintenance | Read-only freshness result and, when requested, reviewed adaptation changes |

Runtime-confirmed findings, source-supported findings without runtime proof, ruled-out candidates, and unresolved proof gaps remain distinct. A clean scanner exit or empty findings list does not establish complete coverage or compliance certification.

## Upstream source of truth

**[usestrix/strix](https://github.com/usestrix/strix) is the authoritative source for upstream changes.** The skill instructs Claude to run its update checker once at the start of every invocation:

```bash
python3 ~/.claude/skills/strix/scripts/check_upstream.py
```

The checker resolves the repository's current default branch and compares it with the reviewed commit/file inventory in `references/upstream.json`. It detects added, removed, and modified files across the whole repository, including new consumer skills and internal specialist packs. It returns JSON with the reviewed/current revisions, compare link, changed paths/categories, and check time.

| Exit | Status | Meaning |
|---|---|---|
| `0` | `current` | The upstream head equals the reviewed baseline. |
| `10` | `updates_available` | A different upstream commit needs review; changed files are listed. |
| `2` | `unknown` | Network, rate limit, metadata, or baseline failure prevented verification. |

The checker uses Python's standard library and unauthenticated public GitHub API reads. It sends no project data or credentials, installs nothing, runs no fetched code, and leaves the baseline untouched. It makes at most three requests with a 10-second timeout each. Unknown freshness does not block useful authorized assessment work. In an offline or network-restricted environment, record unknown rather than claiming the baseline is current.

Checks happen **when the skill is used**, not continuously in the background. No scheduler, daemon, or automatic instruction replacement is installed. A detected change remains pending until a maintenance session reviews it, adapts relevant guidance, validates the package, and advances the baseline. See [maintenance](references/upstream-maintenance.md).

## Install

Install it as a personal Claude Code skill at `~/.claude/skills/strix/`. First check for an existing copy and preserve its local changes, then copy the complete `strix/` directory (for example from a clone of the source collection `0xcvaliente/codex-skills`):

```bash
cp -R strix ~/.claude/skills/
```

Start a new Claude Code session if the skill does not appear. See [Claude Code skills](https://docs.claude.com/en/docs/claude-code/skills) for skill locations and discovery.

Installation does not start a scan, install the Strix runtime, upload source, or change project CI. Claude can pick the skill automatically from its description; explicit invocation is `/strix`.

## Example requests

```text
/strix review this repository for reachable authorization and injection
issues. Use disposable local fixtures and report runtime proof gaps.

/strix review this PR against its actual base, including the shared
authorization helper and its callers.

/strix test our local two-tenant API using the seeded test accounts.
Keep billing and outbound email out of scope.

/strix fix the findings in security_runs/latest/report.md, then verify
the original proofs, an alternate bypass, and normal behavior.

/strix check usestrix/strix for updates and refresh this adaptation in
my skills repository, preserving local improvements and updating its README.
```

The user/host's actual scope and authorization control actions. A source review does not authorize probing discovered third-party URLs, uploading private source, or changing production data. Existing session authorization is reused rather than repeatedly requested.

## Requirements and package layout

- Python **3.9+** for the checker and offline regression tests; no third-party Python dependency.
- Network access to the public GitHub API for freshness verification. The public API may rate-limit frequent invocations.
- Project source and its own supported runtime/tests for native source review and local proofs; a capable browser/HTTP client when needed.
- Optional installed scanners/AST tools. Missing tools limit coverage; no fixed scanner stack is required.
- For actual Strix execution: separately installed Strix, Docker for self-hosted scans, its own supported auth/configuration, and authorized spend. Managed use needs its own account/scopes, authorized data transfer, and current service availability.

`SKILL.md` is the agent entrypoint; its frontmatter supplies the name, description, and short description. `references/` holds assessment, targeted testing, evidence/fix, integration/CI, maintenance, provenance, and baseline inventory material. `scripts/check_upstream.py` implements the read-only check; `tests/test_check_upstream.py` exercises it without network access. `LICENSE` and `NOTICE` retain Apache-2.0 attribution.

## Verify and maintain

From the directory that contains the package (for example `~/.claude/skills`):

```bash
python3 -m unittest discover -s strix/tests -v
python3 strix/scripts/check_upstream.py
```

Helper tests cover freshness behavior, not the security of any application. Exit 10 from the live checker is a successful detection of pending upstream changes. Installed copies do not update when the collection clone changes; preserve local modifications when synchronizing them.

Reviewed source revision: `62b496430da5df5e9e79a190e7af6f92529883a3`, **2026-10-10**. See [provenance](references/provenance.md) for inspected sources and deliberate adaptation choices. Upstream copyright is **2025 OmniSecure Inc.**; this modified package is distributed under [Apache-2.0](LICENSE). No upstream affiliation or endorsement is claimed.
