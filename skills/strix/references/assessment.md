# Assessment workflow

Read this for application, code, web, API, and PR assessments. Apply the parts the target and requested depth need.

## Build a small target map

Connect the source subtree to its running environment and data owners. Identify public/authenticated entrypoints, privileged operations, tenant/object ownership, external fetches, uploaded files, persistence, background jobs, and sensitive output. Follow real callers and configuration; a helper's name is not proof that it enforces authorization.

For a local project, inspect its setup and use existing disposable test infrastructure. Preserve uncommitted work. Record the tested revision and dirty state. Inspect scripts before running unfamiliar project code; respect project rules about migrations, seeds, mail, payments, and hosted services. Prefer an isolated checkout or fixture when starting the app could affect shared data.

For a deployed target, keep exact scheme/host/port/path scope and exclusions. Credentials should come from an existing secret channel or local protected fixture, not prompts, command-line literals, reports, or shell tracing. Missing authenticated access limits coverage rather than inviting credential guessing.

For APIs, locate the OpenAPI/Swagger, GraphQL, Postman, or protobuf contract and the actual implementation. A contract helps enumerate operations; it is not proof of authorization. Track method, route, auth, resource ownership, writable properties, returned fields, and side effects. Include documented-but-unreachable and reachable-but-undocumented routes as coverage gaps or findings as appropriate.

## Prioritize hypotheses

Write a specific expected invariant and a possible violating path. Examples: a tenant query omits the caller's tenant predicate; a webhook trusts a client-supplied signature result; a canonicalized upload path can leave its destination; an agent uses a tool result as authorization to perform a privileged action.

Prioritize reachable auth, cross-tenant access, executable sinks, file/network boundaries, data integrity, and high-value workflow transitions. Consider dependencies, configuration, and secrets without assuming every outdated version is exploitable. Use the relevant [testing playbooks](testing-playbooks.md) rather than spraying every payload class at every endpoint.

Optional installed tooling:

| Tool family | Useful evidence | Limit |
|---|---|---|
| Semgrep, ast-grep, Tree-sitter | Candidate sinks, callers, routes, structural patterns | Findings require path and control review; incomplete parsing limits coverage |
| Gitleaks, TruffleHog | Secret-shaped material and history exposure | Redact results; never validate a credential against a third-party account without authorization |
| Trivy, native package audits, OSV tooling | Resolved vulnerable versions, configuration issues | Check actual package, advisory, runtime reachability, and relevant fix version |
| Browser and bounded HTTP requests | Auth, response content, state transitions, browser execution | Respect scope, stateful side effects, request limits, and test identities |

Use existing tools first. No fixed scanner stack is mandatory, and missing tooling does not prevent source review. An AST pass is useful when textual search cannot distinguish structural callers or guards. Keep scanner and route inventories scoped and bounded; suppress raw secret output.

## Prove or close each candidate

Trace attacker-controlled input → parsing/transformation → guard → sink → impact, including aliases and alternate callers. Identify conditions that would break the proposed path. For dynamic proof, establish a benign control first, execute the smallest violating case, and compare the actual effect. A 200 response is not proof of unauthorized data access; a 403 is not proof that every method and sibling path is protected.

For access control, use two owned seeded identities and objects; show same-owner success and cross-owner denial or demonstrated unauthorized access. Include low/high privilege when function-level permissions matter. Never substitute private customer records for fixtures.

For suspected unsafe output or command execution, show the effect in an isolated target using inert markers. Avoid persistence, destructive commands, external exfiltration, or resource exhaustion. For race conditions, bounded deterministic fixture tests are stronger and safer than production load.

Keep a compact ledger:

| Surface / candidate | Expected boundary | Evidence and counterevidence | Disposition / proof gap |
|---|---|---|---|
| Method + route or file + symbol | Required control | Test result or complete source trace | Runtime-confirmed, source-supported, ruled out, unresolved, not tested, or not applicable |

Name the actual control before ruling something out and verify its order and coverage on the reachable path. Distinguish "no issue found in the tested case" from a universal clearance. Record build failures, unavailable accounts, environment mismatch, and cap-related truncation explicitly. Move to other useful surfaces when repeated setup attempts add no evidence. Before finishing, go back over every row still marked unresolved or not tested: work it, or hand it to a worker when delegation is authorized, until it reaches a real disposition. A row stays unresolved only when it is genuinely blocked, and the blocker is stated in its evidence.

## PR and diff reviews

Resolve the intended merge base from the PR or repository's real default branch. Verify that it exists and that the diff contains the intended changes. Check staged, unstaged, and relevant untracked source if the request covers the working tree. Comparing a branch to its own upstream often yields an empty diff and can omit the entire feature.

Review changed code with its callers, authorization middleware, shared storage queries, serializers, tests, and configuration. Diff scope sets the entrypoints for reasoning; it does not imply guards outside the diff are correct. State the baseline and any excluded files in the report.

Finish using [evidence, reports, and fixes](reporting-and-fixes.md). Test depth and runtime availability control the confidence claim, not whether the write-up sounds complete.

## Connection evidence

When an available authorized connector can establish deployment configuration,
schema, access policies, or prior findings, use its authoritative read capability
for the relevant hypothesis. A configured connection is not proof that its tool
catalog loaded. Distinguish loading, ready, unavailable, and an actually empty
catalog; unknown counts must not become zero. Continue source review when a
connection fails and record the resulting proof gap. Use actual
agent capabilities
(such as configured MCP servers) rather than assuming Strix-specific MCP discovery tools exist.
