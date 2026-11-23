---
name: mcp-cybersecurity
description: Secure and maintain Model Context Protocol (MCP) servers, clients, and configurations using the CIA triad (confidentiality, integrity, availability). Use when building, reviewing, auditing, hardening, or operating MCP servers or MCP client setups - authentication, tool poisoning, prompt injection, secrets, sandboxing, supply chain, rate limiting, and ongoing maintenance. For a language or framework security review with no MCP involved use security-best-practices; for a threat model of a whole repository use security-threat-model.
---

# MCP Cybersecurity

Keep MCP deployments secure by applying the CIA triad to every server, client, and tool.

## Threat model in one paragraph

An MCP host connects an LLM to servers that expose tools, resources, and prompts. Anything the model reads - tool descriptions, tool results, resource contents, other servers' output - is **attacker-influenceable text that can steer tool calls**. Local (stdio) servers run **arbitrary code with the user's privileges**. Remote servers hold **credentials for downstream systems**. The LLM is never a security boundary: enforce authorization, validation, and limits in code, outside the model.

## Workflow

1. **Inventory.** List every server: name, source/publisher, version, transport (stdio or Streamable HTTP), who runs it, what tools/data/credentials it touches, trust tier (first-party / vetted third-party / community).
   Run `scripts/audit_mcp_config.py <config.json>` on JSON client configs for a fast static pass, for example Claude Desktop's `claude_desktop_config.json`, a project `.mcp.json`, Cursor's `mcp.json` or VS Code's `mcp.json`. It reads server entries under `mcpServers` and `servers` keys, so a config in another format or under another key needs a manual review.
2. **Map trust boundaries.** user <-> host/client <-> LLM <-> MCP server <-> downstream APIs/data. Mark where untrusted text enters and where side effects leave.
3. **Walk the controls** below (C, then I, then A). For each gap, record a finding.
4. **Report** using the finding format at the end. Fix highest-severity first.
5. **Install the maintenance loop** (see Maintenance) so the posture does not decay.

Detailed threat -> CIA -> mitigation mapping: `references/threat-catalog.md`.

## Confidentiality - only authorized parties see data

- **Authenticate remote servers.** OAuth 2.1 with PKCE; publish protected-resource metadata (RFC 9728); clients send the `resource` parameter (RFC 8707) so tokens are audience-bound.
- **Validate token audience on every request.** Accept only tokens issued *for this server*. **Never pass a client's token through to a downstream API** (token passthrough); obtain a separate downstream token (token exchange / on-behalf-of).
- **Least privilege.** Narrow scopes, no wildcards, per-server and per-user credentials, short-lived tokens, elevate on demand.
- **Authorize in code, per request.** Check the user's rights on each data access; do not rely on the model to withhold data.
- **Confused deputy.** A proxy MCP server with a static client ID must obtain per-client user consent before forwarding to a third-party authorization server; match redirect URIs exactly; validate `state`; protect consent cookies against CSRF.
- **Secrets hygiene.** No secrets in tool args, descriptions, prompts, logs, git, or process args. Use env references or a secret manager; rotate on exposure.
- **Minimize output.** Return only needed fields; redact PII/secrets before results reach the model. Never return env vars or full configs.
- **Break the exfiltration trifecta.** Private data + untrusted content + an outbound channel in one session is exploitable. Remove one leg: isolate sensitive servers, block egress, or require human approval for outbound tools.
- **Transport.** TLS for all remote traffic. Local HTTP servers bind `127.0.0.1` only and **validate the `Origin` header** (DNS rebinding). Prefer stdio or restricted unix sockets locally.
- **SSRF.** When a client fetches URLs supplied by a server (OAuth metadata, resources), require HTTPS, block private/loopback/link-local ranges (incl. `169.254.169.254`), and re-validate after redirects.
- **Logging.** Log metadata (who, server, tool, arg hash, status), not secrets or full payloads.

## Integrity - data, tools, and behavior cannot be tampered with

- **Treat all tool arguments as hostile.** Strict JSON Schema (types, enums, lengths, `additionalProperties: false`). No shell string interpolation (use argv arrays); parameterized queries; canonicalize paths and confine to allowlisted roots; allowlist URLs/hosts.
- **Tool poisoning.** Read the *full* tool description and schema text (not the UI summary) for hidden instructions before approving a server.
- **Rug pulls.** Pin or hash approved tool definitions; alert on `notifications/tools/list_changed` (delivered only on a `subscriptions/listen` stream opened with `toolsListChanged: true`, so open that stream or re-poll `tools/list`) and on any diff; re-approve changes.
- **Shadowing / name collisions.** Namespace tools by server; flag duplicates; one server's description must not alter how another server's tools are used.
- **Indirect prompt injection.** Tool results and resources are data, not instructions. Require human confirmation for destructive, state-changing, financial, or outbound actions, and show the *exact* arguments being approved.
- **Supply chain.** Pin exact versions (and digests for images); no `npx -y pkg@latest`; use lockfiles; verify publisher and spelling (typosquats); scan dependencies; prefer signed releases. Review a local server's code or sandbox it before first run - installing it is running arbitrary code.
- **Sessions and state handles.** MCP is now stateless with no protocol-level sessions; servers that keep state mint a handle instead (session IDs apply to revision 2025-11-25 and earlier). Secure, non-deterministic IDs and handles (CSPRNG). **Never use a session or handle as authentication** - verify credentials on every request. Bind them to the user (`<user_id>:<handle>`, user ID taken from the verified token).
- **Sampling and elicitation.** Sampling is deprecated, so new implementations should not adopt it; where it is still used, show users sampling prompts and results and cap sampling. Form-mode elicitation must never request passwords, API keys, access tokens or payment credentials; a sensitive flow uses URL mode with explicit consent and the full URL shown.
- **Roots.** Expose only the directories a task needs; roots are informational and deprecated, so enforce confinement in the server or its sandbox.
- **Audit trail.** Append-only, tamper-evident log of every tool call and approval.

## Availability - the service stays usable and fails safely

- **Limits everywhere.** Per-user/client/tool rate limits, concurrency caps, per-call timeouts, request and response size caps, pagination, output truncation (prevents context flooding).
- **Budget expensive work.** Bound recursion, fan-out, regex complexity (ReDoS), query cost, and tool chaining depth.
- **Contain the blast radius.** Run servers in containers/sandboxes: non-root, read-only FS, dropped capabilities, seccomp, cgroup CPU/memory limits, egress allowlist. Never `--privileged`, host networking, host root mounts, or the Docker socket.
- **Resilience.** Circuit breakers and backoff to downstream APIs, idempotent tools so retries are safe, health checks, graceful degradation.
- **Cap tool surface.** Limit tool count and description size per server (tool bloat degrades model behavior and cost).
- **Operability.** Alerts on auth failures, rate-limit hits, schema violations, and latency; a **kill switch** to disable a server fast; documented credential-rotation and incident runbooks; backups for stateful servers.
- **Dependency availability.** Pin and mirror critical packages and images.

## Maintenance loop

| When | Do |
|---|---|
| Every change | Diff tool definitions and scopes; re-run the config audit; re-approve changed tools |
| Weekly | Review auth-failure, anomaly, and rate-limit logs; check dependency advisories (CVE) for each server |
| Monthly | Patch/update pinned versions deliberately; rotate long-lived secrets; remove unused servers and scopes |
| Quarterly | Re-inventory servers and trust tiers; run injection/poisoning test cases; rehearse the kill switch and incident runbook; re-read the current MCP spec security pages for changes |

Treat any unexplained tool-definition change, unexpected outbound call, or token used outside its audience as an incident: disable the server, rotate credentials, preserve logs, then investigate.

## Finding format

```
[SEVERITY] <title>            (C | I | A)
Where:    <server / file / endpoint>
Evidence: <what was observed - redact secret values>
Impact:   <what an attacker gains>
Fix:      <specific change>
```

Severity: **Critical** (remote exploit or credential exposure), **High** (exploit needs one precondition), **Medium** (weakens defense in depth), **Low** (hygiene).

## Guardrails

- Defensive use only: assess systems the user owns or is authorized to test. Do not probe third-party servers.
- Never print secret values in reports; show the key name and location only.
- Never "fix" a finding by disabling authentication, confirmations, or logging.
- Verify against the current MCP specification (Authorization and Security Best Practices pages) when a recommendation depends on spec wording; the protocol evolves.
- The protocol claims here were last checked against MCP specification revision 2026-07-28.
