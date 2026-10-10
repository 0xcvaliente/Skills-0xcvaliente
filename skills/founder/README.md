# Founder

**One Claude Code skill for validating, building, growing, and operating a business.** Founder (ported from Founder Codex) connects strategy, product, marketing, sales, finance, and execution through shared company context and practical playbooks. Ask for a decision or a deliverable, and it selects the guidance needed to complete the work.

The goal is consistent founder work: pricing should agree with the economics, landing-page promises should match the product, growth experiments should address the actual constraint, and fundraising claims should reflect the available evidence.

It supports bootstrapped and venture-backed companies, software and AI products, services, commerce, marketplaces, and local businesses. Start before launch, while finding your first customers, or when improving an existing business. It does not assume every founder should raise money, build SaaS, or follow the same stages.

## What you can accomplish

Turn a broad question such as “What should I focus on?” into a reasoned priority and a concrete next action. Or request a specific artifact directly: an interview guide, positioning brief, landing-page copy, product specification, pricing proposal, sales sequence, cash analysis, investor narrative, or operating procedure.

The skill contains **12 business playbooks**, with six supporting guides for company context, content, conversion and analytics, search discovery, financial inputs, and provenance. These are references within one skill. Invoke `/founder` (or let Claude pick it automatically); you do not need to install or remember twelve separate commands.

| Playbook | When to use it | Typical deliverables |
|---|---|---|
| [Diagnosis and decisions](references/diagnosis.md) | Prioritize work, investigate stalled progress, evaluate a pivot, or prepare a business review. | Decision memo, bottleneck analysis, strongest objection, prioritized next action. |
| [Validation](references/validation.md) | Test a problem, customer segment, offer, or willingness to pay. | Interview guide, evidence synthesis, demand experiment, decision criteria. |
| [Market research](references/market-research.md) | Understand alternatives, competitors, reachable customers, and market assumptions. | Sourced competitor map, customer-channel research, reachable segment, research brief. |
| [Positioning and copy](references/positioning.md) | Explain who the product serves, why it matters, and why someone should choose it. | Positioning brief, finished copy, proof map, objection handling, pitch narrative. |
| [Product and delivery](references/product.md) | Scope an MVP, define a feature, improve activation or retention, or plan delivery. | Buildable brief, acceptance criteria, rollout plan, retention investigation. |
| [Pricing and offers](references/pricing.md) | Choose pricing, packaging, monetization, or offer terms. | Pricing proposal, contribution check, packaging rationale, validation design. |
| [Growth and marketing](references/growth.md) | Plan a launch, choose channels, improve a funnel, or investigate growth performance. | Channel experiment, launch assets, funnel intervention, measurement plan. |
| [Sales and revenue operations](references/sales.md) | Find customers, improve discovery calls, qualify opportunities, or organize sales. | Outreach drafts, discovery script, proposal, qualification criteria, deal plan. |
| [Finance](references/finance.md) | Understand margins, capacity, cash, break-even, or recurring revenue. | Traceable calculations, scenario analysis, cash decision, economics review. |
| [Fundraising](references/fundraising.md) | Assess raise readiness, prepare a pitch, investigate investors, or plan a round. | Evidence-led narrative, raise model, verified investor criteria, preparation plan. |
| [Operations](references/operations.md) | Organize execution, hiring, suppliers, capacity, or recurring processes. | Runnable SOP, role scorecard, operating cadence, ownership and capacity plan. |
| [Agent workflows](references/agent-workflows.md) | Build a founder automation, AI worker, or agent product. | Implemented workflow where tools allow, outcome rubric, evaluation cases, operating handoff. |

### Marketing depth

Marketing work can draw on three focused companion guides:

- **[Content and editorial work](references/marketing-content.md):** create useful content and campaign assets, review claims and quality, and connect production to an audience and business objective.
- **[Conversion and analytics](references/conversion-analytics.md):** investigate conversion problems, plan measurement, design experiments, and distinguish attribution from evidence of causal impact.
- **[Search discovery](references/search-discovery.md):** research search demand and discoverability, including AI visibility, with sourced claims and an actionable improvement plan.

The growth playbook connects these activities to acquisition, activation, retention, referrals, and revenue. It helps choose a relevant intervention instead of listing every possible marketing tactic.

## Install

Founder was ported from the Founder Codex skill in the [Codex Skills collection](https://github.com/0xcvaliente/codex-skills). Claude Code loads personal skills from `~/.claude/skills/<name>/`. From a directory that contains this skill folder (`founder/`), copy it into place:

```bash
mkdir -p ~/.claude/skills
cp -R founder ~/.claude/skills/
```

Run the copy command only when the destination does not already exist. If Founder is already installed, compare the files and preserve any local changes before updating. See the [Claude Code skills documentation](https://docs.claude.com/en/docs/claude-code/skills).

The skill itself does not require an API key, paid service, or third-party Python package. Research and external execution use the tools available in your Claude Code session. The separate [Founder Codex repository](https://github.com/0xcvaliente/founder-codex) also contains the original Codex package; access to that private repository requires GitHub permission.

## Quick start

Invoke the skill explicitly (or describe a founder task and let Claude pick it) and describe the outcome you want:

```text
/founder assess my business, identify the main bottleneck,
and complete the most useful next deliverable.
```

Include the relevant customer, business model, current evidence, constraints, and intended audience when available. You do not need a complete company brief for a small task. Missing information stays unknown or becomes a clearly labeled assumption when a conditional analysis is useful.

### Example requests

**Validate an idea**

```text
/founder I want to offer appointment automation to independent
dental clinics. I have two weeks and $500 to test demand. Prepare an
interview guide and a real-world experiment, with decision criteria
and a record for the results.
```

**Investigate growth**

```text
/founder review the attached funnel data. Identify whether
acquisition, activation, or retention is the main constraint, explain
the evidence, and prepare the highest-priority experiment.
```

**Create positioning and copy**

```text
/founder use our existing product-marketing context and customer
interviews to write a landing page for small accounting firms.
Include the offer, proof, objections, and primary call to action.
```

**Scope a product**

```text
/founder turn these customer problems into an MVP brief for one
engineer working for four weeks. Define the core workflow, exclusions,
acceptance criteria, and how we will observe successful use.
```

**Evaluate pricing and cash**

```text
/founder compare these three packages using our delivery costs
and capacity. Show contribution, break-even, and cash implications.
Separate known inputs from assumptions and identify what needs testing.
```

**Prepare sales materials**

```text
/founder use these discovery notes to draft a proposal and
follow-up email. Connect the offer to the buyer's stated outcome,
include clear scope and terms, and leave both ready for review.
```

**Build an agent workflow**

```text
/founder build a workflow that turns approved customer-call
transcripts into a weekly product-insight brief. Use available tools,
define useful evaluation cases, and document the operating handoff.
```

## How the skill works

1. **Understand the request.** Use the conversation and relevant project artifacts before asking for more information. A specific deliverable can proceed directly; broad or uncertain requests may need diagnosis first.
2. **Reuse company context.** Keep customer definitions, offers, metrics, constraints, and accepted decisions consistent across tasks.
3. **Load relevant guidance.** Read the primary playbook and only the companions needed for the current work.
4. **Ground the recommendation.** Separate reported information, observed evidence, assumptions, and proposals. Verify changing external claims when current sources are available.
5. **Complete the result.** Produce the requested artifact or carry out the authorized implementation using the session's capabilities. Specialist skills can handle document formats, design, or platform-specific implementation.
6. **Check the conclusion.** Reconcile calculations and claims, distinguish completed verification from proposed tests, and identify a useful next decision trigger where appropriate.

This is a flexible working approach. A copy request does not require a full business audit, and a founder can start with any playbook.

### Shared company context

The skill checks for relevant existing records such as:

```text
FOUNDER_CONTEXT.md
founder/context.md
founder/facts.md
.agents/product-marketing.md
.claude/product-marketing.md
```

It reuses the project's location and format rather than creating competing versions of the same facts. For sustained work, the [company-context guide](references/company-context.md) describes a compact brief and optional evidence, decision, and experiment records. These capture sources, dates, customer segments, metric definitions, owners, and revisit triggers when needed.

Business information stays with the project rather than being saved inside the globally installed skill. Separate businesses keep separate context. Short tasks can remain in the conversation without creating a folder of records.

## Evidence and decision quality

Founder makes distinctions that materially affect business decisions:

- **Reported information versus observed evidence:** a founder's estimate, an analytics export, and a proposed scenario have different status. Unresolved contradictions remain visible.
- **Interest versus demand:** compliments, survey intent, waitlists, commitments, payments, repeat use, and renewals answer different questions. Evidence from one buyer does not establish demand across a market.
- **Simulation versus measurement:** generated personas and review panels can suggest questions or objections. Their purchase rates cannot validate pricing, establish demand, or serve as forecasts or upper bounds on sales.
- **Attribution versus causality:** credit assigned to a channel does not by itself prove that the channel caused additional revenue.
- **Revenue versus profit versus cash:** MRR, contribution, operating profit, and collected cash use their own definitions and periods.
- **Proposed criteria versus observed results:** experiment thresholds are tied to the business economics and decision, and labeled as proposals until measured.

The skill avoids universal verdict scores, guaranteed marketing uplifts, arbitrary user-count stages, and unsupported deadlines. Changing external facts need current verification. When verification is unavailable, it identifies the uncertainty rather than inventing evidence.

Authorization follows the requested action. Drafting outreach does not send it, designing ads does not buy traffic, and discussing a recurring workflow does not schedule it. When external execution is authorized and the necessary tools are available, the skill can continue through that work.

## Offline finance helper

[`scripts/finance.py`](scripts/finance.py) provides reproducible arithmetic for financial tasks. It requires **Python 3.8 or newer**, uses only the standard library, reads a JSON file, and prints its report to stdout without modifying the input.

Include a `currency` and at least one supported section:

| Section | Inputs and purpose | What it calculates |
|---|---|---|
| `unit` | Realized unit price, named variable and fixed costs, planned volume, and optional capacity. | Contribution, margins, planned operating profit, whole-unit break-even, and capacity warnings. |
| `cash` | Opening cash, minimum reserve, and chronological receipts and payment schedules. | Period-end cash, reserve shortfalls including the opening balance, and a stress view excluding listed financing. |
| `saas` | Starting MRR, new MRR, expansion, contraction, and churn from a matched starting cohort. | Ending MRR, gross retention, net retention, and growth ratios. |

### Worked unit-economics example

Save this hypothetical input as `numbers.json` in your project:

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
  }
}
```

From this skill's directory (`~/.claude/skills/founder/` once installed), run:

```bash
python3 scripts/finance.py /path/to/numbers.json
```

These inputs produce **$77 contribution per customer-month**, **50 customer-months to break even**, and **$2,310 planned monthly operating profit** at a volume of 80. The result reflects the supplied costs; it does not automatically add omitted taxes, depreciation, or startup expenses.

The [full schema and worked example](references/finance-inputs.md) explain required fields, payment categories, cohort definitions, and calculation limits. Decimal outputs are strings, ratios use a 0–1 scale, and undefined ratios are `null`. Inputs reject unknown or missing fields, duplicate JSON keys, nonfinite or negative values, and booleans used as numbers.

Cash calculations inspect supplied endpoints, so they cannot detect a shortfall between endpoints. The helper does not forecast beyond the supplied periods or validate customer demand. Keep provenance and assumptions alongside your project model.

## Repository structure

```text
founder/
├── SKILL.md                 # Invocation metadata and task routing
├── references/              # 12 playbooks and 6 supporting guides
├── scripts/finance.py       # Offline financial calculations
├── tests/test_finance.py    # Finance regression tests
├── licenses/                # Eight retained upstream license texts
└── README.md                # Installation, usage, and project overview
```

Start with [SKILL.md](SKILL.md) to see the instructions Claude follows. Reference files supply deeper workflows; the [source map](references/sources.md) explains the synthesis and provenance.

## Validation

The Codex version passed structural validation, **11 finance tests**, and **one independent founder-request evaluation**; the finance tests also pass in this Claude Code port, while the founder-request evaluation has not been rerun with Claude. The evaluation used a hypothetical company scenario to check constraint diagnosis, conflicting metrics, rejection of simulated purchase rates as demand evidence, financial calculations, and preparation of a useful experiment.

Run the finance tests from this skill's directory:

```bash
python3 -m unittest discover -s tests -v
```

These checks establish the documented structure and tested behavior, not coverage of every business situation. After changing the finance schema or arithmetic, rerun the tests; after substantial workflow changes, evaluate a realistic founder request.

From the parent skills directory, the equivalent test command is `python3 -m unittest discover -s founder/tests -v`; the helper path is `founder/scripts/finance.py`.

## Relationship to the collection

Founder owns the business question, evidence, and consistency across decisions. Specialist skills can implement a resulting interface with [UI Design](../ui-design/README.md), shape a complete website experience with [Web Experience Design](../web-experience-design/README.md), or work on application structure with [Codebase Design](../codebase-design/README.md). A document-formatting or platform-specific task may need capabilities supplied by the active environment.

These are task-dependent handoffs rather than a requirement to install every skill. A small copy request can remain within Founder, while a product brief can become the input to an authorized implementation. See the [source collection](https://github.com/0xcvaliente/codex-skills) for the full catalog and dependency overview.

## Inspiration and attribution

Founder is an original rewritten synthesis inspired by eight repositories:

| Source | Ideas informing this skill |
|---|---|
| [emotixco/claude-skills-founder](https://github.com/emotixco/claude-skills-founder) | Shared dated facts, practical founder artifacts, validation, and MVP scoping. |
| [Varnan-Tech/opendirectory](https://github.com/Varnan-Tech/opendirectory) | Public demand signals, customer-channel discovery, comparable pricing, and launch assets. |
| [anthropics/launch-your-agent](https://github.com/anthropics/launch-your-agent) | End-to-end agent workflows, outcome rubrics, representative evaluation cases, and iteration. |
| [Jakeschincariol/founder-skill](https://github.com/Jakeschincariol/founder-skill) | Business lenses, contribution, capacity, cash reasoning, and operating dependencies. |
| [getagentseal/founder-playbook](https://github.com/getagentseal/founder-playbook) | Constraint diagnosis, customer development, pricing frameworks, channel experiments, and tradeoffs. |
| [ognjengt/founder-skills](https://github.com/ognjengt/founder-skills) | Shared founder context, executable growth work, implementation-ready briefs, CRO, and copy. |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | Product-marketing context, focused CRO, onboarding and retention, experimentation, and search discovery. |
| [ericosiu/ai-marketing-skills](https://github.com/ericosiu/ai-marketing-skills) | Experiment records, editorial review, finance-export analysis, transcript insights, and revenue readback. |

The [source map and adaptation notes](references/sources.md) retain reviewed revisions and explain deliberate changes: one entrypoint, selective loading, consistent context, explicit evidence quality, defined financial metrics, and execution based on actual tools and authorization.

Full upstream license texts and copyright notices are retained in [licenses/](licenses/): seven MIT sources and one Apache-2.0 source. No upstream executable scripts, installers, telemetry, credentials, or company data are bundled. Source authors are credited for inspiration; this project does not claim their affiliation or endorsement.
