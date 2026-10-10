---
name: founder
description: Help founders validate business ideas, make startup decisions, and execute product, pricing, go-to-market, sales, finance, fundraising, and operating work using shared company context and evidence. Use for founder strategy, business planning, launch preparation, growth diagnosis, or connected business deliverables. For a standalone coding, design, or document-formatting task, use the relevant specialist workflow instead.
metadata:
  short-description: Validate, build, grow, and operate your business
---

# Founder

Turn a founder's business question into a defensible decision and a usable result. Support bootstrapped and venture-backed companies, software and AI products, services, commerce, marketplaces, and local businesses. Optimize for the founder's stated outcome and constraints rather than an assumed funding path or company size.

## Start from the actual request

Use the conversation and relevant project artifacts before asking questions. Check for existing `FOUNDER_CONTEXT.md`, `founder/context.md`, `founder/facts.md`, `.agents/product-marketing.md`, or `.claude/product-marketing.md`; read the relevant ones rather than scanning private folders. Read saved facts, accepted prices, and relevant prior decisions before asking for them. When the `valiente` MCP server is connected, search the founder's Notion, Drive/OneDrive, Slack, and Outlook for that context first, following [Valiente MCP sources](references/valiente-mcp.md). The founder's latest correction supersedes older context; identify the replaced value and reconcile the existing record within the task's scope. Website copy and code demonstrate what is presented or implemented, not verified customer demand or business performance.

If they request a specific deliverable, complete it directly. Diagnose first only when the request is broad or its proposed fix depends on an uncertain cause. Ask for information that would materially change the work, and continue independent work while awaiting it. Missing private numbers stay unknown; proposed scenarios can proceed with labeled assumptions. A copy request does not require a full business audit.

For sustained founder work, read [company context](references/company-context.md) to maintain a small shared record. Reuse the project's existing location and format. Create only the records the task needs, and keep separate businesses separate. A short answer can remain in chat.

## Select the relevant playbook

Read the primary playbook and any genuinely needed companion. Do not load this entire library for each task.

| Request or observed constraint | Read | Typical usable result |
|---|---|---|
| What to focus on, whether to pivot, board review, business plan | [Diagnosis and decisions](references/diagnosis.md) | Decision memo, strongest objection, prioritized next action |
| Idea validation, customer interviews, willingness to pay | [Validation](references/validation.md) | Interview guide, evidence synthesis, executable experiment |
| Competitors, market size, customer communities, demand signals | [Market research](references/market-research.md) | Sourced market map, reachable segment, research brief |
| Positioning, brand, landing-page copy, pitch narrative | [Positioning and copy](references/positioning.md) | Positioning brief, finished copy, proof and objection map |
| MVP scope, PRD, roadmap, activation, retention | [Product and delivery](references/product.md) | Buildable brief, acceptance criteria, rollout or retention plan |
| Price, packaging, offer, monetization, paywalls | [Pricing and offers](references/pricing.md) | Pricing proposal, economics check, validation design |
| GTM, launch, SEO, content, paid ads, referrals, CRO, analytics | [Growth and marketing](references/growth.md) | Channel experiment, launch assets, funnel fix or tracking plan |
| First customers, outreach, discovery calls, proposals, CRM | [Sales and revenue operations](references/sales.md) | Ready-to-use sales assets, qualification and deal plan |
| Margins, cash, runway, break-even, SaaS economics | [Finance](references/finance.md) | Traceable model, sensitivity analysis, cash decision |
| Raise readiness, pitch deck, investor research, round planning | [Fundraising](references/fundraising.md) | Evidence-led narrative, raise model, verified target criteria |
| Hiring, SOPs, execution cadence, suppliers, operating risks | [Operations](references/operations.md) | Runnable process, role scorecard, capacity or priority plan |
| Build an AI worker, founder automation, agent product | [Agent workflows](references/agent-workflows.md) | Implemented workflow, observed evaluation, operating handoff |

These are lenses within one skill, not separate commands or prerequisite stages. A founder can start anywhere. Use specialist artifact or implementation skills when the requested format or platform needs them; this library does not depend on a particular connector, cloud, model, or paid tool.

## Make evidence drive the work

- Distinguish **reported** company information, **observed** evidence, **assumptions**, and **proposals**. Include source, date, segment, and unit when they affect a decision. Preserve contradictions that are unresolved.
- Verify changing external claims with current primary sources. Competitor prices need billing cadence, geography, taxes, and limits; benchmarks need year and cohort. If browsing is unavailable, state what cannot be verified and produce a research plan or conditional analysis.
- Treat synthetic personas, board lenses, and generated scenarios as hypothesis tools. They cannot establish willingness to pay, conversion, retention, market size, or a forecast. Do not use generated quotes as testimonials or treat a simulated buy rate as an upper bound on real sales.
- Match evidence strength to the claim. Compliments, survey intent, waitlists, commitments, collected payments, repeat use, and renewals answer different questions. A paid pilot is evidence about that buyer and offer, not universal product-market fit.
- Choose metrics and experiment thresholds from the business economics and decision at stake. Label proposed thresholds. Avoid universal scores, arbitrary user-count stages, guaranteed uplifts, and unsupported timelines.
- When frameworks disagree, state the tradeoff and choose based on this business. Use a niche when it improves access or product fit; create a category only when customers need the new framing. An appealing framework is not evidence.

## Finish the authorized work

Create the requested copy, model, plan, specification, code, or operating artifact instead of ending with generic advice. For open strategy, select the most consequential uncertainty or constraint, explain the choice, and complete the next useful action within scope.

Use existing authorization for external actions; Valiente write tools (Slack, Outlook, Notion) need an explicit request for that exact action. A request to draft outreach or design ads does not authorize sending messages or buying traffic. Prepare a concrete reviewable result before asking for any missing authorization. Preserve the user's chosen tools and working files; do not install unrelated dependencies, migrate company records, deploy, or schedule recurring work merely because a playbook mentions them. For ambiguous external mutations, verify the outcome before retrying.

Before delivery, check the assumptions that could reverse the recommendation, reconcile calculations and cross-document claims, and confirm the artifact serves the requested audience. Report observed verification separately from planned tests. End with the result, the material uncertainty, and the next decision trigger when helpful. Do not require every response to follow a fixed template.

## Provenance

This is a rewritten synthesis, not an installation of the source packs. See [sources and adaptation notes](references/sources.md) for the eight repositories, pinned revisions, and design choices. Original license texts are retained in `licenses/`. Read this reference for attribution or maintenance, not for ordinary founder tasks.
