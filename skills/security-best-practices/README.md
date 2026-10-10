# Security Best Practices

`security-best-practices` provides language- and framework-specific guidance for secure coding and evidence-based security reviews. It identifies the actual stack, loads the applicable references, and uses them to assess or improve code within the requested scope.

The supported language families are Python, JavaScript/TypeScript, and Go. Bundled guides include Django, FastAPI, Flask, Express, Next.js, React, Vue, jQuery, general browser code, and Go backend code.

## When to use it

Invoke it explicitly for secure-by-default coding help, a security review, or a security report. Its trigger excludes ordinary debugging, general code review, and unrelated tasks. When both frontend and backend are in scope, the workflow examines the relevant guidance for each.

Use [Security Threat Model](../security-threat-model/README.md) when the assignment concerns assets, trust boundaries, attacker goals, and abuse paths across the system. This skill concentrates on implementation practices and concrete code findings.

## How it works

1. Identify the primary languages and frameworks from project evidence.
2. Read the applicable framework guides and relevant general-stack guide.
3. Apply secure defaults during an authorized implementation, or inspect existing code for the requested review.
4. For a report, prioritize findings by severity and include exact code locations and the impact of critical issues.
5. Handle fixes as focused changes, respecting project-specific exceptions and the normal validation workflow.

The instructions distinguish reporting from remediation: producing a report does not automatically begin fixes. Intentional exceptions in project instructions matter, and recommendations should avoid breaking real deployment assumptions, such as local development without TLS.

## Requirements and output

No executable scanner or dependency installer is bundled. The skill requires access to the in-scope code and useful context about its framework and deployment. Uncertain claims may require checking authoritative documentation.

Typical outputs are secure implementation guidance, confirmed findings, or a Markdown report. The default report filename is `security_best_practices_report.md`, unless another destination is requested. Reports include an executive summary, numbered findings grouped by severity, and code line references.

This is a guided review, not a claim that every vulnerability has been found. If the stack lacks a matching reference, the result should disclose that limit.

## Example requests

```text
/security-best-practices review this FastAPI service and React
client, then write a prioritized report with code evidence.

/security-best-practices help implement this Express endpoint
with secure defaults using the repository's conventions.
```

## Package guide

- [SKILL.md](SKILL.md): activation scope, review modes, reporting, and fixes.
- [references/](references/): ten language and framework guides.
- [LICENSE.txt](LICENSE.txt): license text.

Install it as a personal Claude Code skill by copying this directory to `~/.claude/skills/security-best-practices/` (for example `cp -R security-best-practices ~/.claude/skills/`). Invoke it with `/security-best-practices` or let Claude pick it from its description. See [Claude Code skills](https://docs.claude.com/en/docs/claude-code/skills).
