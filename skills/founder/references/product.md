# Product, MVP, and delivery

Use for product briefs, scope, PRDs, roadmaps, activation, retention, or connecting business intent to implementation.

## Scope around the job

Define the primary user, trigger, existing workflow, desired outcome, and smallest end-to-end experience that delivers it. A concierge workflow can test value; a functional prototype can test usability; a production release has different reliability requirements. Match the artifact to the uncertainty.

Separate the core outcome from optional features. Include capabilities needed to make the promised outcome real, even if inconvenient to build. Do not arbitrarily cut a fixed percentage of the feature list or defer essential data protection, permissions, or failure recovery as “post-MVP.”

For each deferred capability, record why it can wait and the evidence or operating trigger for reconsideration. Avoid a roadmap based only on calendar dates or impressive feature counts.

## A buildable brief

Scale detail to the implementation. A useful brief includes:

- Customer job, business objective, and success metric with definition.
- Main flow and critical empty, loading, error, permission, cancellation, and recovery states.
- Functional requirements with observable acceptance criteria and priority rationale.
- Domain concepts, data relationships, lifecycle, access rules, and integration contracts.
- Performance/reliability constraints warranted by the actual use case.
- Existing stack, relevant repository evidence, implementation slices, validation, and rollout.
- Dependencies, unknowns, and deferred features with revisit triggers.

Choose architecture from the existing code and problem. Do not impose a new stack because a source skill recommends it. Distinguish observed implementation facts from proposed design. Estimates should be ranges with dependencies and team capacity, not unsupported deadlines.

If authorized to build, implement a coherent vertical slice, verify the important user journey, and report what works. A PRD alone does not complete a build request. Use the appropriate coding, UI, artifact, or hosting workflow for the requested output.

## Activation and retention

Identify the first value event and natural recurrence interval. A daily retention metric is unsuitable for an annual task. Define activation using a customer outcome, not merely signup or tutorial completion. Investigate whether a behavior predicts repeat value across cohorts; correlation alone does not make it causal.

Segment by acquisition source, user need, and start period. Observe users doing the core job, examine dropoffs and support, and distinguish poor fit from product friction. Fix the earliest consequential failure rather than adding more nudges to a broken value proposition.

For onboarding, specify first-run data/demo state, shortest useful path, help at actual obstacles, event instrumentation, and stalled-user interventions. Avoid requesting account setup or imports before the user understands the value unless the job requires them.

For churn, distinguish voluntary reasons, failed payments, missing delivery, and seasonal use. A save offer should address the reason without hiding cancellation. Measure retained usage, paid renewals, refunds, and support burden after intervention. Read [conversion and measurement](conversion-analytics.md) for a test or analytics implementation.

For marketplaces, assess liquidity by relevant geography/category/time and both sides' participation. For services or commerce, include delivery capacity, fulfillment, repeat purchases, and quality outcomes rather than defaulting to SaaS metrics.
