# Vercel React Best Practices

`vercel-react-best-practices` supports reviewing and improving React and Next.js applications for performance and rendering correctness. It prioritizes meaningful changes while preserving security, accessibility, failure behavior, and maintainability.

This package is a locally hardened adaptation, as its entrypoint states. It is not a live feed of upstream rules, and its advice must be checked against the target project's installed framework versions and enabled features.

## When to use it

Use it for React components, Next.js routes and layouts, data fetching, caching, hydration issues, bundle size, server/client boundaries, and performance investigations. It is useful when a plausible optimization could alter behavior or when generic framework advice conflicts with the local configuration.

## How it works

First inspect repository instructions, packages, framework configuration, and nearby code. Determine the installed React and Next.js versions and relevant features, then check installed guides and types before applying version-dependent advice.

Its optimization priorities are:

1. Remove avoidable network or server waterfalls.
2. Reduce unnecessary client JavaScript and large imports.
3. Preserve correct server/client and caching boundaries.
4. Reduce expensive renders supported by code evidence or profiling.
5. Optimize lower-level hot paths only when they are material.

The detailed reference explains how to assess performance without introducing stale state, races, unsafe shared caches, or authorization gaps. Mutations still require operation-level authorization. Hydration warnings should be investigated, and request-specific mutable state should not leak into server module scope.

## Requirements and output

The skill needs access to the application's code, installed packages, and relevant configuration. Typechecks and focused tests verify correctness; profiling, bundle analysis, and browser measurements are useful when the benefit cannot be established directly from eliminated work.

The output is an implemented improvement or prioritized review findings with exact locations and focused corrections. It distinguishes measured problems from plausible optimizations and does not install dependencies merely because a generic rule mentions them.

[UI Design](../ui-design/README.md) and [Web Design Guidelines](../web-design-guidelines/README.md) complement it for user-facing interface quality. [UI Verification](../ui-verification/README.md) supplies browser evidence.

## Example requests

```text
/vercel-react-best-practices review this Next.js route for data
waterfalls, excessive client code, and unsafe cache boundaries.

/vercel-react-best-practices investigate this hydration warning
against the installed framework version and implement the fix.
```

## Package guide

- [SKILL.md](SKILL.md): runtime checks, priorities, and correctness boundaries.
- [references/performance-and-correctness.md](references/performance-and-correctness.md): detailed decision rules.

Install by copying this directory to `~/.claude/skills/vercel-react-best-practices/` (for example `cp -R vercel-react-best-practices ~/.claude/skills/`). Claude Code then uses it automatically when a request matches, or you can invoke it directly with `/vercel-react-best-practices`. See the [Claude Code skills documentation](https://docs.claude.com/en/docs/claude-code/skills).
