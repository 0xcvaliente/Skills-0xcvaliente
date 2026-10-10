# Evidence, reports, and fixes

Use this for findings from native Claude Code testing or imported Strix Markdown/JSON/SARIF/cloud records. Treat an imported finding or suggested patch as a candidate until its path and evidence are checked; it is not permission to execute an attached PoC script.

## Calibrate the finding

Keep severity, confidence, and validation method separate. Runtime-confirmed means the effect was observed in the identified tested environment. Source-supported means the input, reachable path, broken control, sink, and effect are established from source but the runtime claim remains unverified. A scanner hit without that chain belongs in triage, not the confirmed findings list.

Inspect the strongest counterevidence: a reachable guard, context-appropriate encoding, deployment constraint, different ownership rule, earlier prerequisite, or already-held privilege. Confirm that the control executes before the effect on this precise path. A safe sibling route does not clear another instance. Missing deployment evidence reduces confidence; it does not prove private deployment. Constraints reduce impact when established, not when imagined.

Prioritize demonstrated unauthorized reach and material impact, accounting for privileges, user interaction, scope, and affected data. Keep constrained real findings with an honest rating. Do not inflate missing headers, version disclosure, account enumeration, or standalone redirects into critical issues. A CVSS score requires a named version and defensible vector calculated with a suitable calculator; omit a numerical score rather than invent one.

Deduplicate common root causes while preserving all affected reachable instances and different prerequisites. Separate dependency-advisory matches and hardening observations from exploit claims. Report the absence of confirmed findings alongside what was actually covered.

## Usable artifacts

Use the project's requested report location and format. For a sustained engagement without an existing convention, `security_runs/<run-id>/` can hold a report, a coverage ledger, and minimal reproducible fixtures. Keep sensitive scratch output outside version control or add a narrowly scoped ignore when appropriate; do not commit session material or private records. A small review can stay in the response.

Each actionable finding should contain:

- Stable ID and title; severity, confidence, and validation method.
- Tested revision/environment and concrete file/line or method/endpoint locations.
- Required attacker access, expected security invariant, actual broken control, and impact.
- Reproduction using owned fixtures, expected versus observed result, and a legitimate control case.
- Counterevidence checked, constraints, and any remaining runtime or deployment gap.
- Root-cause remediation, affected sibling instances, and verification result if fixed.

The overall report records in-scope assets, exclusions, auth/role coverage, tools and meaningful checks, inaccessible surfaces, stopped/capped runs, and unresolved candidates. Redact secret values and private record contents. Supply a machine-readable index or SARIF only when needed; do not claim a custom JSON format is Strix-compatible or invent source locations to populate a report.

## Remediate and verify

For authorized fixes, first state the invariant in one sentence and find the narrowest shared enforcement point. Use framework-native parameterization, contextual encoding, canonical containment, server-side object/tenant permissions, and explicit verification as appropriate. Preserve legitimate behavior and repository conventions. Do not execute an imported `fix_after` snippet blindly.

Check the patch in this order:

1. It applies to the current code and passes the narrow syntax/import/type check.
2. The original PoC fails for the security reason, rather than because the service or feature is broken.
3. An alternate relevant encoding, method, role, or sibling path cannot bypass the corrected boundary.
4. The legitimate case still succeeds, with required compatibility and error behavior.
5. Focused regression tests and the owning package's required checks pass.

Add tests that exercise the invariant and exploit/control behavior rather than matching patch wording. If runtime execution is unavailable, trace the patched path and mark the result **statically verified** or **proposed**, with the missing runtime check. Do not label it runtime-verified because a scanner stopped reporting it.

Secret exposure remediation can require rotation and history cleanup; prepare the relevant code fix, but treat credential rotation and destructive history rewriting as separate actions requiring their own authorization. Do not test a discovered secret against a live provider to prove validity.

For actual Strix runs, read `run.json` and coverage/budget context as well as the vulnerability list. Local exit 0 only describes analyzed work and the chosen severity threshold; exit 2 indicates findings and exit 1 an error. Even `status: completed` can reflect an early budget-warning wrap-up. Replay the original proof and verify relevant coverage before declaring a fix closed.
