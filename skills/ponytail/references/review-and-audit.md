# Change reviews and repository audits

Review as the developer who will maintain the result. Prioritize correctness,
security and data integrity, expected load, meaningful tests, performance,
then unnecessary complexity. Review requests produce findings; edit code
when the user also requests fixes.

## Establish the scope

For a change review, use the user-selected uncommitted changes, index, branch,
PR, commit, or files. When no target is given, review uncommitted changes,
including relevant untracked files; if there are none, review the last commit.
Use a branch or PR's actual base and compare the relevant diff. Do not assume
the previous commit represents an entire branch. Read changed code together
with its callers, dependencies, tests, and documented behavior. Trace changed
contracts through all consumers.

For an audit, map the named repository, package, or folder first. Read its
README, build/deployment configuration, dependencies, entry points, and tests.
Trace important flows end to end, especially authentication, untrusted input,
money, writes, background work, and state shared across processes. In a large
repository, go deep where failures matter most and state the coverage limits.

Infer the expected workload from project evidence and identify any assumption
that affects a finding. Do not recommend distributed infrastructure for a
single-user script merely because it could someday have more users.

## Look for concrete failures and justified simplification

- Wrong results, crashes, boundary cases, broken callers, and rules applied
  inconsistently across paths.
- Reachable injection, missing authorization or validation, exposed secrets,
  swallowed write errors, partial updates, and data-loss risks.
- Races, process-local state that must be shared, unbounded growth, repeated
  queries, and algorithms that fail at the expected workload.
- Risky behavior without a test that would detect the failure. Do not report
  missing tests solely because a changed function contains a branch.
- Material slowdowns and repeated hot-path work, grounded in the actual flow.
- Dead or speculative code, needless dependencies, duplicated rules that
  change together, pass-through wrappers, and functions mixing unrelated jobs.
  Reuse an existing project helper when it truly fits; name its path. Split
  by responsibility when useful, rather than by a line-count threshold.

Before reporting, re-read the exact code and establish a concrete trigger,
mechanism, and consequence. Check dynamic references, exports, configuration,
tests, and fixtures before calling code unused. A documented `shortcut:`
(or legacy `ponytail:`) ceiling is a conscious decision unless current requirements or load exceed
it. Reject style-only preferences and hypothetical scaling worries.

## Report

Briefly explain the change or repository and any consequential load assumption.
Number actionable findings in priority order. Use the host's required review
format when one exists; otherwise group into **Must fix**, **Should fix**, and
**Nice to have**, omitting empty groups.

Each finding names a precise source location and explains what the code does,
the situation that goes wrong, the smallest adequate fix, and the consequence
of leaving it. Distinguish a reproduced failure from source-supported reasoning
that was not run. Keep optional simplification separate from blocking defects.
Avoid arbitrary finding quotas; prioritize important findings in a broad audit
and state any deliberate reporting or coverage limit.

End with a verdict supported by the findings and what was checked or remains
unchecked. A clear review means no confirmed issue in the examined scope,
not a guarantee about unread paths. Quantify removable code or dependencies
only from an inspected, explicit change; do not invent a hypothetical baseline.
