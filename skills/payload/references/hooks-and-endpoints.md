# Payload hooks, endpoints, and side effects

Read this reference when implementing hooks, nested Local API calls, jobs, webhooks, or custom endpoints.

## Transaction context

Thread the active `req` through nested Payload operations that should participate in the current transaction and request context:

```ts
await req.payload.update({
  collection: 'posts',
  id: child.id,
  data: { status: 'published' },
  req,
})
```

Do not manufacture a partial request or transaction identifier when the real request is available. Verify adapter-specific transaction behavior against the installed version.

## Recursion and duplication

Hooks that write to the same collection can trigger themselves. Use a narrowly named `req.context` flag, document who sets it, and return early only for that explicit internal path. Do not disable all hooks merely to avoid recursion; that can skip access, invariants, or integrations unexpectedly.

Retries and concurrent requests can duplicate side effects. Use database uniqueness, idempotency keys, durable job identities, or provider idempotency support rather than an in-memory flag.

## External side effects

A database transaction cannot roll back an email, payment request, webhook, or third-party API call. Decide explicitly whether to:

- enqueue work after the database mutation;
- use an outbox or durable job record;
- perform an idempotent reconciliation; or
- accept and document a compensating action.

Do not describe a hook as atomic across systems unless the architecture actually provides that guarantee.

## Webhooks

Read the raw body when the provider signature requires it. Verify the signature before parsing or acting, reject stale or replayed events where supported, store the provider event ID with a uniqueness constraint, and make handlers idempotent. Return only after durable acceptance according to the provider's retry contract.

## Endpoint shape

For each endpoint, identify:

1. caller and authentication mechanism;
2. resource and authorization decision;
3. validated request schema;
4. bounded query and response shape;
5. mutation and transaction boundary;
6. external side effects and retry behavior; and
7. safe error and logging behavior.

Use `Response` and `APIError` patterns supported by the installed Payload version. Add CORS headers only for origins and methods intended by the application; CORS is not authentication.
