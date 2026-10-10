# Finance helper schema and worked example

Use with `scripts/finance.py`. The helper reads a JSON file, prints a JSON report, and changes no files. Requires Python 3.8 or newer with no third-party packages. Unknown fields, missing fields, duplicate JSON keys, booleans as numbers, negative inputs, and nonfinite values are rejected. Values may be JSON numbers or decimal strings. Decimal outputs are strings, ratios use 0–1 scale, undefined ratios are `null`, and whole-unit break-even is an integer.

## Required top-level shape

`currency` is required. Include at least one of `unit`, `cash`, or `saas`; omitted sections are not calculated. All required values in a included section must be provided. Use an explicit zero or empty cost map only when that category is known to be zero, not when it is unknown. Put input provenance in the project evidence record alongside this document.

## Unit section

Required: `name`, `period`, `price`, `variable_costs` (named amount per unit), `fixed_costs_per_period` (named period amounts), `planned_units_per_period`. Optional: `capacity_per_period`. Every value must use the same unit, currency, and period. Price is realized revenue per unit excluding pass-through tax. Include refunds/discounts consistently. Acquisition may be a variable/fixed cost where appropriate, but do not double count it. Profit reflects only the supplied costs; it does not automatically include taxes, depreciation, or startup spend.

## Cash section

Required: `opening_cash`, `minimum_reserve`, and a nonempty chronologically ordered `periods` array. Each period requires unique `label`, `receipts`, `operating_payments`, `capital_payments`, `tax_payments`, `debt_payments`, `financing_received`.

Values are nonnegative cash totals, not signed ledger entries. Include each payment once. `debt_payments` includes the principal/interest payments allocated here; do not also put them in operating payments. Financing received is actual or explicitly modeled cash, not revenue or an unsigned commitment. Include startup spend in the period it is paid. Rows can be daily, weekly, or monthly; label the granularity.

The reserve shortfall is the extra opening cash that would keep the supplied endpoints at the reserve, holding all modeled flows unchanged. It includes the opening balance and is not a forecast beyond these periods. The report also removes listed financing as a stress view; this is not a reoptimized business scenario. It does not detect cash shortfalls between endpoints.

## SaaS section

Required: `period`, `starting_mrr`, `new_mrr`, `expansion_mrr`, `contraction_mrr`, `churned_mrr`. Normalize annual recurring subscriptions monthly; exclude one-time fees and pass-through taxes. Use a matched starting cohort for retention. Contraction/churn are losses from starting MRR, with no double counting. Expansion is retained growth from that cohort; new MRR is from new customers. Net out transient within-period swings before supplying the bridge. If the billing system's buckets use other semantics, reconcile them first or use a detailed cohort model.

Gross retention = (starting − contraction − churn) / starting. Net retention adds expansion but excludes new MRR. Ending MRR adds new MRR. Empty starting cohorts have undefined retention/growth ratios. MRR is neither collected cash nor recognized accounting revenue.

## Hypothetical example

This example demonstrates the schema, not a forecast for the user's company. Copy it to a project input file and replace the relevant sections with sourced inputs.

```json
{
  "currency": "USD",
  "unit": {
    "name": "customer-month",
    "period": "month",
    "price": "100",
    "variable_costs": {"delivery": "20", "fees": "3"},
    "fixed_costs_per_period": {"payroll": "3500", "tools": "350"},
    "planned_units_per_period": 80,
    "capacity_per_period": 120
  },
  "cash": {
    "opening_cash": "10000",
    "minimum_reserve": "2000",
    "periods": [
      {"label": "month-1", "receipts": "3000", "operating_payments": "5000", "capital_payments": "1000", "tax_payments": "0", "debt_payments": "0", "financing_received": "0"},
      {"label": "month-2", "receipts": "6000", "operating_payments": "5500", "capital_payments": "0", "tax_payments": "0", "debt_payments": "0", "financing_received": "0"}
    ]
  },
  "saas": {
    "period": "month-2",
    "starting_mrr": "4000",
    "new_mrr": "1000",
    "expansion_mrr": "400",
    "contraction_mrr": "200",
    "churned_mrr": "400"
  }
}
```

Expected checks: contribution 77; unit break-even 50 customer-months; planned operating profit 2310; cash endpoints 7000 and 7500; reserve shortfall 0; ending MRR 4800; gross retention 0.85; net retention 0.95. The sections demonstrate distinct calculations and are not intended as a fully reconciled accounting model.
