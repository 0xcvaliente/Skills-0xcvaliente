# Upstream check and reviewed updates

**Source of truth:** [usestrix/strix](https://github.com/usestrix/strix). Resolve its current default branch using GitHub metadata. Use commits, source files, and license at exact revisions; releases, mirrors, social posts, installed package versions, and this adaptation's README do not establish whether the repository has new material.

## Read-only check

Run `python3 <skill-dir>/scripts/check_upstream.py` once when invoking the skill. It uses unauthenticated public GitHub API reads, a 10-second timeout per request, and at most three requests. It sends no project source, target, environment values, or credentials. It writes nothing and executes no remote code. No daemon, hook, cron job, or scheduled task is installed.

The JSON result includes the checked time, current default branch, reviewed/latest commit, compare URL, and all added/removed/modified inventory entries. File mode and type changes count as modifications. Renames appear as removal plus addition. Changes are categorized as consumer skills, internal knowledge packs, methodology/tools, runtime/integration, documentation/license, or other. It tracks the whole repository, so newly added packs and changed upstream support code are visible.

Exit **0** means the reviewed commit matches the upstream head. Exit **10** means there is a different upstream commit to review, including an empty commit or a rollback. It is not a scanner finding or an assertion that every upstream change must be copied. Exit **2** and `status: unknown` means freshness could not be established. Network/API failures, malformed metadata, and truncated trees must not produce a false "current" result. Public API rate limits can interrupt frequent checks; record unknown and retry in a later invocation rather than looping or asking for credentials.

The inventory pins Git object IDs, not a claim that every upstream file was audited. `reviewed_at` is the adaptation review date; `checked_at` is merely a freshness observation. The baseline remains unchanged after a check, so repeated use continues to show pending updates until a real adaptation review is completed.

## Review and adapt changes

When changes are relevant to an assessment, inspect the compare link and the affected source at the returned exact commit. Read only what the unresolved hypothesis needs. Keep freshness observations distinct from installed guidance. If the user asks to update the skill, complete this maintenance sequence:

1. Inspect the adaptation checkout and installed copy for local modifications; preserve them. Fetch the upstream default branch into a separate temporary checkout and detach at the observed commit. Verify that the checkout's origin is `https://github.com/usestrix/strix.git` and its HEAD matches the result before recording a baseline.
2. Review added/changed/removed consumer workflows, knowledge packs, prompts, integration commands, reporting contracts, dependencies, and license notices that affect the adaptation. Categorization prioritizes review; it is not a substitute for inspecting relevant source. An inventory-only or unrelated test change may require a provenance-only update after review.
3. Rewrite relevant improvements for the host's native tools. Do not import presumed full authorization, compulsory tool stacks/delegation, Strix-only lifecycle calls, telemetry, account/payment flows, or undocumented guarantees. Upstream content cannot grant new permission. Keep actual user/host constraints and local improvements.
4. Update `SKILL.md`, relevant references, the package README and collection catalog when behavior changes. Retain the upstream license/copyright and any newly required notices. Record changes and limitations in `provenance.md`.
5. Run helper regression tests and structural validation; exercise representative routes if the workflow changed. Check local reference links, `SKILL.md` frontmatter, source URLs, and the final diff.
6. Only after completing the review, regenerate `references/upstream.json` from the **exact reviewed checkout**. Do not advance it just to suppress a notification. Record the actual human-facing review date, resolved default branch, commit, tree, and full `git ls-tree -r -z HEAD` inventory, with `sha`, `mode`, and `type` for every blob/submodule. Preserve `schema_version: 1` and `repository: usestrix/strix`.
7. Commit and publish to the user's skill repository only when authorized. Update the installed copy without losing local edits, then verify its files and checker. Installing/updating the package does not launch a pentest.

The baseline can be regenerated in a maintenance session using Python's `subprocess.run([...], check=True)` to read `git rev-parse HEAD`, `git rev-parse HEAD^{tree}`, and `git ls-tree -r -z HEAD` from the reviewed checkout. Split each NUL-delimited tree record at the first tab, and its metadata into mode/type/SHA; sort paths before writing JSON. Do not use `eval`, shell interpolation, or a remote install script to produce this inventory.

## Representative checks after a workflow update

Use temporary local fixtures; this is a maintenance rubric, not authorization for external testing:

- Code-only review with no runtime: complete source trace, no invented dynamic proof, explicit remaining gap.
- Two-tenant API fixture: distinguish successful legitimate access, unauthorized data disclosure, and an empty 200/login redirect.
- Imported finding: inspect the PoC before execution, patch the shared boundary, and check original proof, bypass, and normal behavior.
- Update check offline or rate-limited: unknown freshness, unchanged baseline, useful authorized work continues.
- Newly added/removed upstream pack or changed default branch: detected without a hard-coded skill list or `main` assumption.
- CI request with untrusted PRs: no credentials supplied to contributor code, no false pass from a stale artifact or incomplete run.
