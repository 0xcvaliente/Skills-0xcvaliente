# React and Next.js performance with correctness

Use this reference for implementation or review after confirming installed framework versions.

## Async work and streaming

- Start independent work together and await it at the latest point that still gives clear error handling.
- Model partial dependencies with ordinary promises before adding a scheduling library.
- Use Suspense boundaries when they improve meaningful streaming and the fallback reserves stable layout. Do not split content into boundaries merely to increase their count.
- Check cheap synchronous guards before starting expensive work when the skipped path is common. Do not reorder required side effects or security checks.
- Parallelization changes failure and resource behavior. Consider cancellation, connection limits, rate limits, and whether partial results are allowed.

## Next.js data and cache semantics

- Distinguish request memoization, persistent caching, revalidation, and process-local caching. They have different lifetimes and invalidation behavior.
- Identical server-render `GET` fetches may be memoized, but Route Handlers are outside the React component render tree. Confirm the installed `fetch` documentation.
- Use `React.cache` for per-render/request deduplication of non-fetch work when supported. Do not assume it is a cross-request cache.
- A process-local `Map` or LRU is shared among requests in that process, may disappear at any time, and may not be shared with other instances. Never use it as the source of truth.
- Shared cache keys must include tenant, identity/role when output differs by authority, locale, preview/draft state, and other relevant inputs. Bound memory and define invalidation.
- Do not cache secrets, authorization decisions, or personalized output unless the cache boundary is intentionally designed and tested.

## Server and client boundaries

- Keep data transformation on the server when it reduces transferred data and the client does not need the source object. Keep a transformation on the client when sending both original and derived values would duplicate serialization.
- Pass the smallest useful serializable props across the RSC boundary, without fragmenting a cohesive model into an unstable prop list.
- Avoid mutable server module state for request data. Immutable configuration and deliberately keyed caches are different cases.
- Hoist immutable static I/O only when the asset truly cannot change during the process lifetime and retaining it in memory is acceptable.
- For non-blocking post-response work, verify the installed framework's lifecycle guarantee. Critical durable work belongs in a job or queue, not a best-effort callback.

## Bundles and imports

- Prefer Server Components where interactivity is unnecessary.
- Lazy-load genuinely heavy, non-critical Client Components. In current Next.js releases, `ssr: false` is not valid in a Server Component; place that dynamic import behind a Client Component and verify the installed lazy-loading guide.
- Use statically analyzable import paths. Prefer explicit loader maps over arbitrary dynamic path construction.
- Before changing barrel imports, inspect the package exports and Next.js configuration. Some common packages are optimized automatically; deep imports can break types or unsupported export boundaries.
- Defer non-critical third-party browser code, but preserve error reporting, consent, and compliance requirements.

## Rendering and state

- Derive values during render instead of mirroring props/state through effects.
- Put effects caused by a user action in that action's handler.
- Use functional state updates when the next value depends on the previous value.
- Do not define component types inside another component when remounting would lose state or DOM identity.
- Use `useDeferredValue` or transitions for non-urgent rendering work only after correctness is established. Async transitions do not by themselves solve out-of-order responses; use request identity, cancellation, or server ordering where needed.
- Avoid manual `memo`, `useMemo`, and `useCallback` for trivial work. First check whether React Compiler is enabled and whether stable identity is semantically required.
- Use refs for transient values that should not render. Do not move visible application state into refs merely to suppress renders.

## Browser work

- Batch DOM reads and writes; prefer CSS layout over JavaScript measurement.
- Use passive touch or wheel listeners only when the handler never calls `preventDefault`.
- Use `content-visibility` or virtualization based on measured list cost, variable-height behavior, accessibility, and search/navigation requirements—not a fixed item-count threshold.
- Keep localStorage and cookies minimal. Version client-stored schemas, handle parse/storage failures, and never treat client storage as trusted authorization state.
- Bound memoization maps and invalidate them when their inputs can change externally.

## Images and scripts

- Reserve image space and provide correct `sizes`; lazy-load non-critical images.
- Read the installed `next/image` documentation before using version-sensitive props. In Next.js 16, `priority` is deprecated in favor of the current preload/loading guidance.
- Use `next/script` strategies according to dependency and execution timing. A script that must run before interactivity deserves an explicit reason.
- Add preconnect or preload only for known critical resources; unnecessary hints consume bandwidth and connection slots.

## Evidence standard

Treat the following as strong evidence: a removed round trip, fewer serialized bytes, a smaller analyzed client chunk, a prevented remount, a profiler trace, or a reproducible browser metric. Treat claims such as “faster,” “GPU accelerated,” or fixed percentage improvements as hypotheses unless measured in the target application.

## Provenance

This local skill was created after reviewing Vercel Labs' MIT-licensed React best-practices skill at commit `063bee94c3f4df8453406c830b0a7df0f2860278`. Its instructions were rewritten and narrowed for version-aware use; it does not fetch or execute upstream content.
