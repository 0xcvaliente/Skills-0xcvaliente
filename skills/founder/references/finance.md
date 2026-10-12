# Finance, unit economics, and cash

Use for contribution, break-even, profitability, runway, business models, forecasts, expense review, or SaaS economics. Define the entity, currency, time period, tax treatment, business model, and decision first.

## Establish the inputs

Prefer actual billing/accounting exports, bank records, supplier quotes, contracts, payroll, and usage/cost data. Record source, period, and whether each input is reported, observed, or assumed. Reconcile totals and sign conventions before interpreting ratios. Do not infer development cost from lines of code or claim an AI productivity saving without a comparable baseline.

Separate revenue, bookings, collected cash, pass-through taxes, deferred obligations, variable delivery costs, acquisition costs, fixed operating costs, capital expenditure, debt service, and financing. Founder time and compensation belong in the relevant scenario; omission should be explicit. Marketplace GMV is not platform revenue. Inventory purchases and deposits can precede cost recognition or revenue collection.

For costs hidden in AI/service products, include heavy users, retries, refunds, support, human review, failed jobs, payment fees, and delivery capacity. Preserve actual currency rather than silently converting; use a dated sourced exchange rate if conversion is needed.

## Deterministic calculations

Use `scripts/finance.py` relative to this skill directory for supported unit, cash, and MRR calculations. It is offline, Python standard-library only, rejects malformed/unknown inputs, and returns JSON to stdout. The schema and hypothetical worked example are in [finance inputs](finance-inputs.md). Resolve the actual installed skill path before invoking (for example `$HOME/.agents/skills/founder/`, or the skill directory your host reports when it loads the skill); do not assume the current project is its directory.

Save business inputs in the project's chosen working location, not inside the skill. Execute:

```bash
python3 /absolute/path/to/founder/scripts/finance.py /absolute/path/to/numbers.json
```

For spreadsheets, multi-product cohorts, accounting statements, irregular intra-period cash, or complex financing, use a model appropriate to the requested artifact. This helper checks arithmetic; it does not certify completeness or validate demand.

## Interpret the model

- Contribution per unit = realized price minus stated variable costs. Break-even depends on positive contribution and feasible capacity. Classify acquisition consistently and avoid counting it in both variable cost and a separate CAC allowance.
- Operating profit is not cash flow. Schedule receipts and payments by when they happen. An endpoint cash schedule can miss a payroll shortfall earlier in the month.
- Constant-burn runway is only a rough ratio when burn is positive and stable. Use a dated cash forecast when seasonality, collections, hiring, or financing change it. Never treat an unsigned raise as cash in the bank.
- Gross retention excludes expansion and new sales. Net retention includes expansion but excludes new sales. Starting denominators and matched cohorts matter.
- CAC requires attributable acquisition spend and acquired customers from a matching window/cohort. Include labor and onboarding when relevant. A spend/new-customer ratio is not necessarily a mature cohort CAC.
- CAC payback uses gross contribution from the acquired cohort. LTV from inverse churn is a simplified stationary approximation that can be misleading with sparse or changing cohorts. Prefer observed cumulative cohort contribution and show uncertainty; avoid undefined ratios when denominators are zero.

## Scenarios and decision

Build base, downside, and upside only when useful. Vary coherent drivers such as price, acquisition, retention, cost, ramp, collections, and capacity. Recalculate each; label forecasts as conditional. Do not feed synthetic persona purchase rates into revenue assumptions.

Identify the assumption that could reverse the recommendation, minimum cash/reserve gap, capacity constraints, and a concrete operating response. A loss can be a deliberate investment; evaluate it against the founder's objective and funding constraints rather than issuing a universal failure verdict.

If tax, payroll, securities, or legal structure becomes material, verify the current jurisdiction-specific rules and identify the unresolved item. Do not insert a generic professional-advice disclaimer into every routine calculation.
