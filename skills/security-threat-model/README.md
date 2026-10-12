# Security Threat Model

`security-threat-model` produces an actionable threat model grounded in a repository or a defined project path. It connects actual components and entry points to assets, trust boundaries, realistic attacker capabilities, abuse paths, and specific mitigations.

Its emphasis is on credible scenarios. Threat priority depends on exposure, existing controls, likelihood, impact, and deployment assumptions rather than on a generic vulnerability checklist.

## When to use it

Invoke it explicitly to threat model a codebase, enumerate abuse paths, or perform application-security modeling. It does not activate for a general architecture overview or ordinary code review.

[Security Best Practices](../security-best-practices/README.md) complements it when the next task is inspecting language-specific implementation patterns or correcting a concrete weakness.

## How it works

1. Define the repository or directory scope and extract the system model from code and relevant architecture documents.
2. Separate runtime components from build, CI, development tools, and examples.
3. Identify assets, entry points, and concrete edges where trust changes.
4. Describe attacker capabilities and meaningful limits on those capabilities.
5. Enumerate a small set of high-quality abuse paths and prioritize them with explicit likelihood and impact reasoning.
6. Validate assumptions that materially affect scope or ranking with the user before writing the final report.
7. Tie mitigations to specific components, boundaries, or entry points and distinguish existing controls from proposals.
8. Check coverage and save the report using the reference output contract.

The assumption-validation stage is part of this skill's workflow. Deployment, authentication, internet exposure, sensitive data, and tenancy can change the assessment substantially. Remaining uncertainty is recorded rather than silently filled in.

## Requirements and output

The package needs access to the target code and relevant deployment context. It does not bundle a scanner, exploitation tool, or runtime dependency.

The result is a concise Markdown artifact named `<repo-or-dir-name>-threat-model.md`. It includes evidence-backed system claims, explicit assumptions, threats and priorities, and actionable mitigations. The exact report structure is defined in the prompt-template reference.

## Example requests

```text
Use the security-threat-model skill: model this multi-tenant upload service,
including external storage, job workers, and administrator actions.

Use the security-threat-model skill: enumerate abuse paths for this CLI's
plugin-loading directory and distinguish runtime from CI risks.
```

## Package guide

- [SKILL.md](SKILL.md): scope, modeling steps, calibration, and quality checks.
- [references/prompt-template.md](references/prompt-template.md): repository-summary prompts and report contract.
- [references/security-controls-and-assets.md](references/security-controls-and-assets.md): optional control and asset guidance.
- [LICENSE.txt](LICENSE.txt): license text.

Install by copying this directory into any [Agent Skills](https://agentskills.io)-compatible location, for example `cp -R security-threat-model ~/.agents/skills/` (see [INSTALL.md](../../INSTALL.md) for each host's folder). Compatible agents select it automatically when a request matches its description, or you can name it explicitly ("use the security-threat-model skill").
