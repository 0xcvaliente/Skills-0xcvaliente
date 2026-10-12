---
name: payload
description: Build, review, or troubleshoot Payload CMS collections, fields, access control, hooks, Local API calls, custom endpoints, migrations, adapters, and Next.js integration. Use for Payload-specific TypeScript work; verify the installed Payload version and local types before changing code.
---

# Payload CMS

Work from the project's installed Payload version, generated types, and existing conventions. Static examples are secondary evidence.

## Before changing code

1. Read the repository instructions and inspect `package.json`, the installed `payload` package version, `payload.config.*`, generated Payload types, and nearby collections or globals.
2. Resolve uncertain APIs from the installed declarations under `node_modules/payload` and `node_modules/@payloadcms`. Do not assume an API from memory or from a different Payload release.
3. When the change touches Next.js, read the relevant installed Next.js guide under `node_modules/next/dist/docs/` before implementation.
4. Preserve the repository's migration, database, import-map, and code-generation workflow. Do not enable schema push or regenerate artifacts unless the task requires it.

## Security and data boundaries

Read [references/security-and-data.md](references/security-and-data.md) for authentication, Local API, tenancy, field access, secrets, uploads, and proxy/IP decisions.

The essential rule is: operations performed for a user must enforce that user's access. Payload Local API operations default to bypassing access control; use `overrideAccess: false` and thread the request or user deliberately. Reserve bypasses for explicit internal administration and make that intent visible in code.

Custom endpoints have no automatic authorization contract. Authenticate, authorize the concrete action and resource, validate input, constrain collection names and query shapes, and bound pagination or expensive work.

## Hooks, transactions, and side effects

Read [references/hooks-and-endpoints.md](references/hooks-and-endpoints.md) when adding hooks, nested Local API operations, jobs, webhooks, or endpoints.

Pass `req` through nested operations that belong to the current transaction. Guard recursive hooks with explicit context. Make external side effects idempotent and avoid claiming they are transactionally atomic with the database.

## Implementation standard

- Prefer generated collection types and Payload-exported types over `any`.
- Keep access functions fail-closed and return the narrowest boolean or `Where` constraint.
- Use `select`, bounded `depth`, limits, and indexes based on actual query paths.
- Treat relationship population as data disclosure: related documents and fields still need correct access behavior.
- Preserve existing hooks, access functions, admin configuration, and plugin arrays when extending configuration.
- Validate externally controlled slugs, IDs, sorts, filters, locales, filenames, and URLs before passing them to Payload or another service.
- Never log passwords, tokens, reset secrets, API keys, authorization headers, or full sensitive request bodies.
- For security-sensitive or version-sensitive behavior, add a focused test that exercises the real access path.

## Verification

Run the narrowest relevant typecheck and tests first, then the repository's normal validation. If generated types, import maps, or migrations are required, use the project's own scripts and review their diffs. Report any behavior that could not be verified against the installed package or a runnable environment.
