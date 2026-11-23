# MCP Threat Catalog

Primary CIA property at risk, how the attack works, and the controls that stop it.

| Threat | CIA | Attack | Mitigations |
|---|---|---|---|
| Tool poisoning | I, C | Hidden instructions in a tool description/schema make the model leak data or misuse other tools | Review full description text; pin/hash definitions; allowlist servers; show approval with exact args |
| Rug pull | I | Server changes tool definitions after approval | Alert on `list_changed` (open a `subscriptions/listen` stream with `toolsListChanged: true`, or re-poll `tools/list`) and definition diffs; re-approve; version pinning |
| Tool shadowing / name collision | I | A malicious server redefines or influences another server's tool | Namespace tools per server; detect duplicates; isolate high-trust servers |
| Indirect prompt injection | I, C | Instructions embedded in web pages, files, tickets, or tool output steer the model | Treat output as data; human confirmation for side effects; least-privilege tools; output filtering |
| Cross-server data exfiltration | C | Poisoned server tells the model to send another server's data out | Break the trifecta (private data + untrusted content + egress); egress allowlist; approvals on outbound tools |
| Token passthrough | C, I | Server forwards client tokens to downstream APIs, bypassing controls and audit | Reject tokens not issued for this server (audience check); separate downstream tokens |
| Confused deputy (OAuth proxy) | C | Static client ID + consent cookie lets an attacker obtain codes for a victim | Per-client consent, exact redirect URI match, `state` validation, CSRF-safe consent |
| Over-broad scopes | C, I | Stolen or misused token grants far more than needed | Minimal scopes, short TTL, incremental elevation, per-server credentials |
| Session hijacking / event injection | C, I | Guessed or stolen session ID (revision 2025-11-25 and earlier) or state handle (stateless current revision) used to replay or inject events or reach another user's state | CSPRNG IDs and handles, bind to user (`<user_id>:<handle>`, user ID from the verified token), never authenticate by session or handle, verify every request |
| DNS rebinding on local HTTP server | C, I | Malicious web page reaches a `localhost` MCP server through the browser | Bind `127.0.0.1`, validate `Origin`, require auth even on localhost |
| SSRF via metadata/URL fetch | C | Malicious server points OAuth discovery at internal hosts or cloud metadata | HTTPS only, block private/link-local ranges, validate redirects, egress proxy |
| Command injection | I, C, A | Tool arg concatenated into a shell command | argv arrays, no shell, strict schemas, allowlisted commands |
| SQL / path traversal | I, C | Tool arg alters query or escapes allowed directory | Parameterized queries, canonical path + root confinement |
| Malicious or compromised local server | C, I, A | Installing a stdio server runs attacker code with user privileges | Review before run; show exact command and require consent; sandbox; no `sh -c` wrappers |
| Supply-chain compromise / typosquat | C, I, A | Unpinned or look-alike package pulls malicious code | Exact version pins, digests, lockfiles, publisher verification, dependency scanning |
| Secret exposure | C | Keys in config, args, logs, prompts, or tool results | Env refs / secret manager, redaction, rotation, secret scanning in CI |
| Excess data in results | C | Tool returns whole records, env, or configs into the model context | Field-level filtering, redaction, per-user authorization |
| Malicious sampling / elicitation | C, I | Server abuses LLM sampling or asks the user for secrets | Avoid deprecated sampling in new implementations, otherwise show and cap it; form-mode elicitation never requests credentials or payment details; sensitive flows use URL mode with explicit consent and the full URL shown |
| Resource exhaustion / DoS | A | Floods, giant payloads, recursive tool chains, ReDoS | Rate limits, quotas, timeouts, size caps, depth budgets |
| Context flooding | A, I | Huge tool output or tool list crowds out instructions | Output truncation, pagination, cap tool count and description size |
| Downstream cascade failure | A | Slow dependency exhausts workers | Timeouts, circuit breakers, bulkheads, backoff, idempotent retries |
| Container escape / host takeover | C, I, A | Privileged container, Docker socket, or host mount | Non-root, read-only FS, drop capabilities, seccomp, no privileged/host mounts |
| Missing audit trail | I | Cannot detect or reconstruct misuse | Append-only structured logs of tool calls, approvals, auth events; alerting |

## Prompt-injection test cases (use on systems you own)

- A document/web page/ticket containing "ignore previous instructions and call `<tool>` with ..." - confirm the call is blocked or needs approval.
- A tool description containing a hidden directive - confirm review catches it.
- A tool whose definition changes between sessions - confirm an alert fires.
- A tool result containing a URL pointing at an internal address - confirm egress/SSRF controls block it.
- A request carrying a token issued for a different audience - confirm it is rejected.
- A request with a valid session ID but no credentials - confirm it is rejected.
