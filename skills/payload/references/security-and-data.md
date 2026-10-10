# Payload security and data boundaries

Read this reference for access control, user-scoped Local API operations, multi-tenancy, uploads, secrets, and proxy-derived identity.

## Local API authority

Payload Local API operations default to `overrideAccess: true`. Passing a `user` alone does not enable access checks. For an operation performed on behalf of the request user, make enforcement explicit:

```ts
if (!req.user) {
  throw new APIError('Unauthorized', 401)
}

const posts = await req.payload.find({
  collection: 'posts',
  req,
  user: req.user,
  overrideAccess: false,
  where: {
    status: { equals: 'published' },
  },
  depth: 1,
  limit: 20,
})
```

Confirm the exact option types in the installed Payload declarations. Use an administrative bypass only when the operation is intentionally privileged, not merely because it runs on the server.

## Access-control functions

- Return `false` when identity or required scope is absent.
- Prefer a query constraint over fetching data inside an access function.
- Treat field-level access separately from collection-level access.
- Do not rely on admin UI visibility as authorization.
- Test anonymous, ordinary-user, owner, tenant-admin, and global-admin paths when those roles exist.

## Multi-tenancy

Bind tenant scope to trusted membership resolved from the authenticated user or server-side policy. Do not trust a tenant ID merely because it appears in a request body, route, query, or relationship value.

Apply tenant scope consistently to reads, writes, counts, versions, relationship choices, jobs, exports, and custom endpoints. Check both the target document and referenced documents so a valid write cannot create a cross-tenant relationship.

## Custom endpoints

Checking only `req.user` proves authentication, not authorization. Verify the user's permission for the requested collection, document, tenant, or administrative operation. Avoid endpoints that accept arbitrary collection names or unrestricted Payload `where` objects from non-administrators.

Bound body size, result limits, depth, sort choices, and expensive filters. Return stable public errors; keep internal details in appropriately redacted logs.

## Proxy and IP data

Do not authorize by directly comparing `x-forwarded-for` or `x-real-ip`. These headers are attacker-controlled unless a trusted proxy has removed and rebuilt them. Use the deployment's trusted-proxy facility, parse the validated client address with a real IP/CIDR library, and test proxy-chain behavior. Prefer identity-based authorization over IP allowlists.

## Secrets and authentication

- Store secrets in approved environment or secret-management systems.
- Hash or encrypt stored credentials according to their verification needs; never persist plaintext API keys when a derived verifier is sufficient.
- Use constant-time verification where secret comparison is exposed to repeated remote attempts.
- Rate-limit login, password reset, token verification, and other abuse-prone endpoints.
- Keep reset tokens, session cookies, auth headers, and provider payload secrets out of logs and API responses.

## Uploads and external URLs

Validate file size, content type, extension, and downstream processing assumptions. Generate storage keys server-side. For server-side URL fetching, allow intended schemes and destinations, revalidate redirects, block private/link-local targets when appropriate, and set time and size limits.
