# Optional Strix integration and CI

Use this only when the user requests the actual Strix engine/platform or security CI. Native assessment by the agent needs neither Docker nor a separate LLM account. The commands below were checked against the pinned source; review upstream changes and the installed CLI's help before execution. No CLI, API, or sandbox implementation is bundled.

## Self-hosted engine

Check `strix --version`, relevant `--help`, and Docker availability. Strix requires its own supported LLM configuration or supported sign-in. Do not infer that the active agent's subscription/configuration is shared with another executable. Keep credentials in the existing environment or protected local input, never command-line literals or reports.

If installation is needed and authorized, consult the current official repository/docs and use a reviewed pinned package or installer. Do not pipe an uninspected remote installer into a shell. A request to create/install this skill does not request installation of Strix's runtime.

A headless local-code scan takes this shape (substitute the actual authorized paths and user-approved budget):

```bash
strix -n -t /path/to/disposable-checkout --scan-mode quick --max-budget <approved-usd>
```

Add an authorized running service as a second `-t` when runtime evidence is needed. Docker Desktop typically reaches a host service through `host.docker.internal`; verify networking for the installed environment. OpenAPI/Swagger and Postman JSON/YAML exports can be targets alongside the API base URL. A protobuf file is supporting input via `--workspace-file`, not a spec target. Use a protected `--instruction-file` for lengthy scope/context or synthetic test credentials; account for any persistence in run artifacts.

Important runtime properties:

- A local code target is writable in Strix's sandbox. Use a disposable checkout and inspect its diff afterward; a clean working tree alone does not isolate important files.
- The CLI's default scan mode is `deep` (`--scan-mode` accepts `quick`, `standard`, `deep`), so pass the mode explicitly in CI. `--fail-on <severity>` is headless-only and sets the exit-2 threshold. `--max-budget` also accepts the alias `--max-budget-usd`; `--max-turns` limits turns per agent. Verified in `strix/interface/cli_args.py` (`-n` line 185, `--instruction-file` 164, `--workspace-file` 172, `--fail-on` 195, `--scan-mode` 211, `--scope-mode`/`--diff-base` 225/238, `--max-budget` 277) at upstream `ca20626`.
- Use `-n` to avoid the interactive TUI and explicit `--max-budget` for authorized spend. Scan depth and caps affect coverage. Launch long work using the host's process/session facilities (for example a background shell command) and report progress without rapid polling.
- Explicit diff scoping uses `--scope-mode diff --diff-base <real-base>`. Verify the base and nonempty intended changes rather than guessing `HEAD~1` or a branch's own upstream.
- Local headless exit codes: **0** no findings at the configured threshold in analyzed work; **1** error (for example interrupt, model connection or scan preparation failure: `strix/interface/cli.py:157`, `main.py:371,409,416`); **2** findings at or above `--fail-on`, or any finding when it is unset (`main.py:272-293,549-551`). Exit 2 is also used for resume-selection errors (`main.py:385,394`), so read the output before treating 2 as findings. Keep lower-severity findings even when `--fail-on high` allows the gate to pass.
- Inspect the selected run's `run.json`, `penetration_test_report.md`, `vulnerabilities/*.md`, structured findings, and `findings.sarif`. A stopped run or exhausted cap is incomplete. Even completed status can represent budget-warning wrap-up; read coverage and usage.

Replay imported PoCs only after checking their code and scope. They are not trusted executables merely because Strix generated them.

## Managed platform

Use cloud only when the task authorizes that service, its spend, and any source transfer. Missing local tooling is not permission to upload the project or change an account. Consult current `strix cloud <resource> help` and [managed API docs](https://docs.app.strix.ai) for exact resources, scopes, and plan requirements; do not freeze billing prices or API schemas into this skill.

Use existing sign-in and least-privilege scopes. If sign-in requires human browser action, present the concrete sign-in step. Do not log tokens or request them in chat. For an authorized source upload, inspect the exact dry-run selection:

```bash
strix cloud scans start --source /path/to/checkout --dry-run --show-files --json
```

Review excluded secrets and the files leaving the machine; capture `source.archive_sha256`. After the required upload/spend authorization exists, launch with the **same selection flags** and `--approve-sha256 <reviewed-digest> --wait`. Do not replace a digest-bound handoff with an unconditional `--yes`.

Cloud commands have different exit codes: **0** success, **1** error, **2** usage, **4** auth/plan limit, **5** payment required in the reviewed version (`strix/interface/cloud/http.py:30-34`, rechecked at `ca20626`). Credit purchases, invitations, schedules, integrations, DNS changes, and status updates require their own task authorization. On an ambiguous launch/upload failure, inspect existing scans/upload IDs before retrying to avoid duplicates and repeated spend.

## Security CI

Create CI only when requested. Fit the repository's existing CI platform, package/version policy, and target environment. Keep third-party action revisions and Strix versions pinned according to current project policy and verify the chosen references. Do not add an unsolicited paid scanner or scheduled assessment.

For GitHub Actions, author the gate around these observable conditions:

1. Trusted event/context and isolated disposable target. Do not expose secrets to untrusted PR code or use `pull_request_target` to run a contributor's code with credentials.
2. Full-enough Git history and an explicit verified PR base supplied safely through an environment variable. Avoid interpolating untrusted PR metadata into shell code.
3. Explicit headless mode, scan depth, scope, budget, and severity threshold. Capture the scanner exit code without turning errors or incomplete runs into success.
4. Associate output with **this invocation** in a fresh artifact directory or by its recorded run ID. Do not select an unrelated older `run.json` with `ls -t`.
5. Preserve artifacts even on failure, redacting sensitive values. Distinguish scanner error, findings, unavailable coverage, and an actual completed gate result.
6. Enforce completion and relevant coverage separately from the vulnerability threshold. Budget warnings can still yield completed status; do not imply a status check proves exhaustive analysis.
7. Upload SARIF only where supported with least-privilege permissions; mark the job as a required check only if repository-setting changes are authorized.

For managed PR reviews, use an already authorized integration or scoped token and poll the specific review to its terminal state. Trigger success alone does not establish scan success. Validate YAML, event behavior, artifact association, and the error/incomplete paths locally or with a safe fixture before publishing the configuration.

## Engine timeout and connection diagnostics

For the actual Strix engine, the reviewed revision distinguishes first-event,
idle-between-events, and total-stream timeouts. Check the installed version before
using `LLM_STREAM_FIRST_EVENT_TIMEOUT`, `LLM_STREAM_IDLE_TIMEOUT`, or
`LLM_STREAM_TOTAL_TIMEOUT`; zero disables the corresponding bound in this version.
A timeout or unavailable MCP catalog limits coverage. Inspect the run's status and
sanitized error/provider details before retrying or changing limits; do not turn
an incomplete attempt into a clean security result. These are Strix settings,
not the agent host's settings, and this instruction package does not change either runtime.
