# Sources and adaptation notes

Reviewed: 2026-10-07. Revisions below pin the material actually inspected; source repositories can change. This skill is an original rewritten synthesis of operational ideas, not a verbatim aggregation, an endorsement by the source authors, or a substitute for the books cited in some repositories. No upstream executable scripts, telemetry, installers, API credentials, or proprietary data are bundled.

## Source map

| Repository and representative source | Revision | License | Ideas adapted |
|---|---|---|---|
| [emotixco/claude-skills-founder](https://github.com/emotixco/claude-skills-founder) · [reviewed source](https://github.com/emotixco/claude-skills-founder/blob/0602cad0520e4d8cb165bb1c779d7010cfbc5b45/skills/validate-idea/SKILL.md) | `0602cad0520e4d8cb165bb1c779d7010cfbc5b45` | [MIT](../licenses/emotixco--claude-skills-founder.txt) | Shared dated facts, practical founder artifacts, validation and MVP scoping. |
| [Varnan-Tech/opendirectory](https://github.com/Varnan-Tech/opendirectory) · [reviewed source](https://github.com/Varnan-Tech/opendirectory/blob/62e437ab13408171805a87d16f5cb0151f96ea3c/skills/where-your-customer-lives/SKILL.md) | `62e437ab13408171805a87d16f5cb0151f96ea3c` | [MIT](../licenses/Varnan-Tech--opendirectory.txt) | Traceable public demand signals, customer-channel discovery, comparable competitor pricing and launch assets. |
| [anthropics/launch-your-agent](https://github.com/anthropics/launch-your-agent) · [reviewed source](https://github.com/anthropics/launch-your-agent/blob/d5d0ffbca3abe857478165a7c48f4cfc39a50920/.claude/skills/launch-your-agent/SKILL.md) | `d5d0ffbca3abe857478165a7c48f4cfc39a50920` | [Apache-2.0](../licenses/anthropics--launch-your-agent.txt) | End-to-end first version, outcome rubrics, representative cases, iteration, and honest connector boundaries. |
| [Jakeschincariol/founder-skill](https://github.com/Jakeschincariol/founder-skill) · [reviewed source](https://github.com/Jakeschincariol/founder-skill/blob/fd9385b0cfe1b96bebce3898fbd506d73eff5a9d/skills/founder-cfo/SKILL.md) | `fd9385b0cfe1b96bebce3898fbd506d73eff5a9d` | [MIT](../licenses/Jakeschincariol--founder-skill.txt) | Distinct business lenses, contribution/capacity/cash reasoning, offer and operating dependencies. |
| [getagentseal/founder-playbook](https://github.com/getagentseal/founder-playbook) · [reviewed source](https://github.com/getagentseal/founder-playbook/blob/e811e63be42c9b64a208707220b145451ad4b6c8/skills/diagnose/SKILL.md) | `e811e63be42c9b64a208707220b145451ad4b6c8` | [MIT](../licenses/getagentseal--founder-playbook.txt) | Constraint diagnosis, customer-development and pricing frameworks, channel experiments, explicit limits and framework tradeoffs. |
| [ognjengt/founder-skills](https://github.com/ognjengt/founder-skills) · [reviewed source](https://github.com/ognjengt/founder-skills/blob/a45931cad934dc6243a68f905485467935a4ad9a/FOUNDER_CONTEXT.md) | `a45931cad934dc6243a68f905485467935a4ad9a` | [MIT](../licenses/ognjengt--founder-skills.txt) | Shared founder context, executable growth moves, implementation-ready product briefs, CRO and copy deliverables. |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) · [reviewed source](https://github.com/coreyhaines31/marketingskills/blob/1efedbc5148b54b2f0f6c6c9fe0be62e151c7fff/skills/product-marketing/SKILL.md) | `1efedbc5148b54b2f0f6c6c9fe0be62e151c7fff` | [MIT](../licenses/coreyhaines31--marketingskills.txt) | Product marketing context, focused CRO, behavioral onboarding/retention, rigorous A/B testing, search discovery, and revenue handoffs. |
| [ericosiu/ai-marketing-skills](https://github.com/ericosiu/ai-marketing-skills) · [reviewed source](https://github.com/ericosiu/ai-marketing-skills/blob/8088e1a167804d5615f6e982f62e5b4b6ff8f2f1/revenue-intelligence/SKILL.md) | `8088e1a167804d5615f6e982f62e5b4b6ff8f2f1` | [MIT](../licenses/ericosiu--ai-marketing-skills.txt) | Experiment/result records, editorial quality review, finance-export analysis, transcript insights, revenue readback, and measured playbook updates. |

## Deliberate changes

- One Codex entrypoint with twelve business playbooks and conditional marketing references. Source-pack commands and mandatory stage sequences were replaced by task-driven routing.
- Existing founder and marketing context can be reused without moving files or duplicating facts. Reported, observed, assumed, and proposed information remain distinguishable.
- Simulated panels and model scores are retained only as qualitative hypothesis/review tools. Generated purchase rates are excluded from demand estimates, price validation, and forecasts; they are not treated as real-world upper bounds.
- Arbitrary business verdict totals, universal stage thresholds, promised marketing uplifts, guaranteed launch rankings, and mandatory 90-point editorial scores were replaced by business-specific evidence and decision criteria.
- Cash, recurring revenue, contribution, capacity, acquisition, and attribution have explicit meanings. The original offline helper in `scripts/finance.py` validates inputs and computes only supported arithmetic.
- Attribution credit is separated from causal impact. Fixed-horizon experiments use precommitted stopping rules; patterns are promoted only with observed results and context.
- Provider-specific launch mechanics were rewritten into a platform-neutral implementation and outcome-evaluation workflow. Actual tools, capabilities, credentials, authorization, and current official APIs control execution.
- No source-sponsored tool, telemetry call, scraper, or broad permission assumption is inherited. Draft/build/research authorization does not silently become send/publish/spend/schedule authorization.

## Attribution and licensing

Copyright notices and full upstream license texts are retained in `../licenses/`. The Anthropic source identifies Copyright 2026 Anthropic PBC and Apache-2.0; its adapted workflow is rewritten and generalized in `agent-workflows.md`. All adaptation files were authored for Founder Codex on 2026-10-07. Nothing here claims affiliation with the source authors or the business-book authors. The framework discussions are short original applications, not reproduced book text.

## Maintenance

Refresh only the source or platform details needed for a demonstrated improvement. Keep the pinned revision and adaptation rationale current when changing source-derived guidance. Prefer changes supported by actual usage to copying growing upstream catalogs. Verify finance behavior after arithmetic/schema changes, and evaluate a realistic request after substantial workflow changes.

## Reviewed update — 2026-10-09

Rechecked all eight source repository heads. Six retained their reviewed revision.
Reviewed the Founder source's conventions/changelog and new saved-fact/pricing
regression cases at `0602cad0520e4d8cb165bb1c779d7010cfbc5b45`; retained context
reuse and explicit correction history. Its model-specific evaluation scores are
not claimed for Codex.

Reviewed Marketing Skills at `1efedbc5148b54b2f0f6c6c9fe0be62e151c7fff`, focusing
on A/B testing and sample-size interpretation, analytics, attribution, AI SEO,
content refresh, and sales enablement. Adopted statistical and event-contract
corrections, outcome/credit separation, saved-price continuity, and scoped search
refresh/visibility guidance. This is a selective adaptation review; new paid-ad,
outbound, affiliate, and lead-magnet catalogs were not installed wholesale.
Source licenses remain unchanged.

## Claude Code port

Ported from the Codex version (`founder-codex`) to a Claude Code skill named
`founder` on 2026-10-10. The skill name, invocation (`/founder`), install path
(`~/.claude/skills/founder/`), and README usage were updated; recurring-workflow
guidance now names Claude Code's `/schedule`, `/loop`, and subagents. The Codex
interface metadata (`agents/openai.yaml`) was dropped. Playbook substance, source
revisions, and licenses are unchanged; the history above describes the Codex
adaptation, and no evaluation results are claimed for Claude.
