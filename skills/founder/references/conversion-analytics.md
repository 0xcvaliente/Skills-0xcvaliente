# Conversion, experimentation, analytics, and attribution

Use for page/funnel audits, signup, onboarding, paywalls, analytics, A/B tests, or interpreting growth results. Match measurement to the decision rather than producing a large dashboard by default.

## Conversion diagnosis

Inspect the actual page or flow if available. Identify traffic intent, segment, device, primary action, current counts/period, and post-conversion quality. Check comprehension, promise/offer consistency, proof, objections, CTA hierarchy, friction, forms, errors, accessibility, and mobile use. Trace findings to observed page elements or journey steps.

Prioritize concrete defects and the hypotheses behind optimization ideas separately. Write replacement copy or implement the requested changes within scope. Label predicted lifts as unvalidated; do not assign invented revenue to every UI suggestion.

For signup, ask whether each field is needed at that moment. For a paywall, clarify the value already delivered, entitlement limits, price/cadence, billing, and recoverable payment errors. For cancellation, provide a straightforward exit and relevant optional help; hiding the exit is not retention.

## Define trustworthy events

Specify event, business meaning, trigger, identity/anonymous-to-known handling, properties, owner/source, and validation. Use stable naming and deduplication keys. Reconcile client events, server success, billing, refunds, and CRM outcomes where needed. A CTA click does not equal a successful purchase.

Track only what answers decisions. Include metric numerator/denominator, time window, cohort, source, and what action follows a change. Do not place sensitive user content in URLs or event properties. Consent, data access, and retention choices must fit the actual system and jurisdiction; verify current requirements when material.

Validate the actual event flow with a test journey and readback. Planned instrumentation is not working instrumentation. Make missing and duplicate events visible before trusting dashboard conclusions.

## Design a decision-worthy experiment

State the causal hypothesis, eligible population, randomization unit, control and intervention, exposure, one primary outcome, guardrails, baseline, practical effect worth detecting, and analysis plan. User/account assignment should be stable and prevent contamination. Account for shared accounts, repeat exposures, multiple variants, and delayed outcomes.

Choose sample size and duration from baseline, minimum detectable effect, error tolerance, power, and available traffic. Use a verified statistical method or tool; do not invent confidence intervals. If the experiment would take too long, propose a larger meaningful contrast, a different measurable decision, or qualitative learning, and state the weaker inference.

Precommit the stopping rule. A fixed-horizon test should not stop early merely because today's result is significant. Sequential methods require an appropriate preplanned procedure. Stop for defined harm when necessary and retain the record. Check assignment balance, data quality, novelty/seasonality, uncertainty intervals, practical importance, guardrails, and downstream quality. Report inconclusive honestly.

## Attribution and readback

First-touch, last-touch, linear, and time-decay models allocate observed credit; they do not prove incrementality. State identity matching, tracking loss, lookback window, model, excluded traffic, cost allocation, and distinction between pipeline, booked revenue, and collected cash. Use randomized or defensible quasi-experimental evidence for causal lift claims.

After an intervention, read back the same metric/cohort/window and exact artifact version. Separate campaign, list, spend, and product changes. Record keep, revise, rollback, or unproven with the observation supporting it. Do not automatically generalize a result or schedule a monitor without the user's request.

## Interpret the analysis correctly

For a planned fixed-horizon test, a p-value measures how incompatible the data
are with the null model under its assumptions. It is not the probability the
result is random or the null hypothesis is true. A confidence interval describes
a repeated-sampling procedure, not a posterior probability for this one interval.
Report effect size, uncertainty, guardrails, and practical value together. After
an inconclusive finished test, do not keep collecting until significance appears;
interpret the effect interval and plan a new test if needed. Treat unplanned
segments as exploratory.

Keep real conversions in one deduplicated outcome ledger; report platform credit
and attribution windows separately. A large direct/branded share may include
repeat customers, genuine direct visits, and tracking loss. Verify its composition
before claiming either a broken measurement system or successful acquisition.

Provider-defined automatic/recommended event names must retain their required
names and payloads. Map internal business names explicitly; a renamed custom
event does not become automatically collected merely because its meaning matches.
