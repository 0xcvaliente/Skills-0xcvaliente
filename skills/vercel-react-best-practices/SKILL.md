---
name: vercel-react-best-practices
description: Review or improve React and Next.js code for performance, rendering correctness, bundle size, and server/client boundaries. Use for React components, Next.js routes and layouts, data fetching, caching, hydration, or performance work; verify behavior against the project's installed versions before applying advice.
---

# Vercel React Best Practices

Apply performance guidance without weakening correctness, security, accessibility, or maintainability. This is a locally hardened adaptation, not a live upstream feed.

## Establish the runtime first

1. Read repository instructions, `package.json`, framework configuration, and nearby code.
2. Determine the installed React and Next.js versions and whether React Compiler, Cache Components, or other relevant features are enabled.
3. Before writing Next.js code, read the relevant guide in `node_modules/next/dist/docs/`. Installed documentation and types override this skill.
4. When a claim depends on another package, inspect that installed package's types or primary documentation. Do not add SWR, an LRU library, or another dependency solely because a generic rule mentions it.

## Priorities

Optimize in this order:

1. remove network or server waterfalls;
2. avoid unnecessary client JavaScript and large imports;
3. preserve correct server/client and cache boundaries;
4. reduce expensive renders proven by code shape or profiling;
5. address low-level JavaScript or DOM hot paths only when they are material.

Read [references/performance-and-correctness.md](references/performance-and-correctness.md) for the detailed decision rules.

## Non-negotiable boundaries

- Authenticate and authorize every Server Action and mutation endpoint at the operation itself.
- Never keep request-, user-, or tenant-specific mutable state in server module scope.
- Key shared caches by every value that changes authorization or output, bound their growth, and define invalidation. Prefer framework-supported cache primitives when they fit.
- Do not use `useTransition`, memoization, module caches, or deferred work to hide races, stale authorization, or incorrect state ownership.
- Treat hydration warnings as bugs until a deliberate server/client difference is proven. `suppressHydrationWarning` is a narrow escape hatch.
- `next/dynamic({ ssr: false })` belongs in a Client Component. Confirm current lazy-loading rules in the installed Next.js docs.
- Preserve failure semantics when parallelizing. Use `Promise.all` only when fail-fast behavior and shared cancellation are acceptable; otherwise design partial failure explicitly.

## Review and verification

For reviews, report high-impact findings first with exact locations, observed consequence, and a focused correction. Distinguish measured problems from plausible optimizations.

For implementation, run relevant typechecks and tests. Use bundle analysis, profiling, or browser measurements when the optimization's value is not evident from eliminated I/O, serialization, or work. Avoid broad refactors justified only by microbenchmarks or generic rules.
