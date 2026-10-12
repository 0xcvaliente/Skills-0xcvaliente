# Payload

`payload` supports building, reviewing, and troubleshooting Payload CMS applications. It covers collections, fields, access control, hooks, Local API calls, endpoints, migrations, adapters, generated types, and Next.js integration.

The workflow is grounded in the project's installed version. Local declarations, generated types, configuration, and nearby code take precedence over examples remembered from another release.

## When to use it

Use it for Payload-specific TypeScript changes: introducing a collection, correcting access behavior, adding a hook or endpoint, investigating relationship population, or extending an existing configuration. It is also useful when Payload operations participate in a transaction or produce external side effects.

## How it works

1. Inspect repository instructions, package versions, `payload.config.*`, generated types, and existing collection patterns.
2. Resolve uncertain APIs from installed `payload` and `@payloadcms` declarations. Check relevant installed Next.js guidance when the integration touches Next.js.
3. Preserve the project's migration, database, import-map, and type-generation workflow.
4. Enforce the acting user's access deliberately. Local API operations can bypass access control by default, so user-facing operations need an explicit access path.
5. Thread `req` through nested operations that belong to a transaction, guard recursive hooks, and make external side effects idempotent.
6. Run focused checks before the project's normal validation and review generated-artifact changes when they are required.

The guidance pays particular attention to custom endpoints, which need their own authentication, authorization, input validation, and work limits. It also treats populated relationships as possible data disclosure and favors generated types over `any`.

## Requirements and output

The target project needs a Payload installation and its normal development environment. The skill does not provide a CMS instance, database, application starter, or migration runner. A runnable environment is important for confirming access and transaction behavior.

The result is a version-appropriate configuration or implementation, a focused diagnosis, or review findings supported by code. Security-sensitive and version-sensitive behavior should be verified through the real access path, with limitations reported when that environment is unavailable.

## Example requests

```text
Use the payload skill: add a collection using this project's generated types
and enforce tenant access on both queries and mutations.

Use the payload skill: review this hook's nested Local API operation for request
propagation, recursion, and duplicate external side effects.
```

## Package guide

- [SKILL.md](SKILL.md): version checks, core boundaries, and verification.
- [Security and data](references/security-and-data.md): access, tenancy, secrets, uploads, and related concerns.
- [Hooks and endpoints](references/hooks-and-endpoints.md): transactions, recursion, jobs, and external effects.

Install by copying this directory into any [Agent Skills](https://agentskills.io)-compatible location, for example `cp -R payload ~/.agents/skills/` (see [INSTALL.md](../../INSTALL.md) for each host's folder). Compatible agents select it automatically when a request matches its description, or you can name it explicitly ("use the payload skill").
