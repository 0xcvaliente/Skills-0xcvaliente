# External workflow analysis and coverage

Reviewed 29 September 2026. This analysis covers the eight published skill entrypoints previously discussed, not a benchmark of their complete packages or resulting artifacts. The installed workflow is newly written; it does not bundle their instructions, scripts, fonts, or templates. Source links provide attribution and allow later comparison.

## 1 Better Documents

[Source — Anil Dash](https://github.com/anildash/better-documents/blob/main/SKILL.md)

**Strength:** Combines generation and review with clear attention to audience, argument order, restrained formatting, navigation, and naming. Its narrow-review modes are useful for routine business editing.

**Fit limitation:** Some visual rules are categorical, such as strict color counts and a neutral default. Those can conflict with a supplied expressive brochure brand. The entrypoint does not supply a document production or rendering pipeline.

**Our treatment:** Keep reader-first structure and scoped reviews, make visual decisions conditional on brand/genre, and connect content review to actual editable-file production and render checks.

## 2 Sales Enablement

[Source — Corey Haines](https://github.com/coreyhaines31/marketingskills/blob/main/skills/sales-enablement/SKILL.md)

**Strength:** Offers broad coverage of sales decks, one-pagers, objections, proposals, personas, demos, and playbooks, with attention to persona and buying stage.

**Fit limitation:** Outputs are often copy/outline plus layout guidance. Fixed slide/page frameworks and examples of quantified benefits do not fit every product maturity or evidence base. Some detailed workflows depend on other references and skills.

**Our treatment:** Cover the same relevant commercial asset families, adapt length to the assignment, produce the requested file through available artifact tools, and require evidence before benefits become quantified promises.

## 3 Industrial Product Brochure

[Source — sauewi](https://github.com/sauewi/industrial-product-brochure/blob/main/SKILL.md)

**Strength:** The closest brochure-specific workflow. It protects product/photo/specification identity, assigns page roles, reviews printed image scale, and distinguishes preview, master, and printer delivery.

**Fit limitation:** Machinery, bilingual catalogs, A4 pages, and raster master delivery shape many defaults. It requires page approval before creating a master even when a user may already have authorized a final export.

**Our treatment:** Generalize page roles and asset manifests to service and software brochures as well as catalogs. Prefer real text and vectors where suitable, preserve current authorization, and use explicit printer requirements instead of a universal A4/raster recipe.

## 4 Copy Editing

[Source — Corey Haines](https://github.com/coreyhaines31/marketingskills/blob/main/skills/copy-editing/SKILL.md)

**Strength:** Separates meaning, voice, customer benefit, proof, specificity, emotional relevance, and action friction into focused editing passes. It also distinguishes refresh from new writing.

**Fit limitation:** Mandatory repeated sweeps can be excessive for a small correction. Simulated expert scores are not independent verification. Specificity and risk-reduction examples require careful handling to avoid invented outcomes or guarantees.

**Our treatment:** Use only the relevant passes, preserve factual qualifications, require authorized offer conditions, and judge defects by their location and effect on the reader rather than a fictional expert panel's score.

## 5 Copywriting

[Source — Corey Haines](https://github.com/coreyhaines31/marketingskills/blob/main/skills/copywriting/SKILL.md)

**Strength:** Connects audience, offer, customer language, benefits, headline, and action in a practical conversion-writing workflow.

**Fit limitation:** Its primary medium is the website, with hero/button structures that can feel misplaced in print. Some broad conversion figures appear without substantiation in the entrypoint; some headline formulas can imply absolute promises.

**Our treatment:** Adapt persuasion to documents, make printed contact actions usable, preserve uncertainty, and support commercial assertions with task-specific evidence. Do not inherit generic performance figures as proof.

## 6 Theme Factory

[Source — Anthropic](https://github.com/anthropics/skills/blob/main/skills/theme-factory/SKILL.md)

**Strength:** Treats colors and typography as a coherent theme and supports predefined or custom directions.

**Fit limitation:** Its workflow depends on a bundled showcase and theme files and pauses for explicit theme selection. A routine pause is unnecessary when the user has supplied a brand or delegated design judgment.

**Our treatment:** Supply five original optional token presets, derive a custom system from the actual brand when supplied, and use role-based colors and documented font fallbacks without requiring theme selection on every task.

## 7 Canvas Design

[Source — Anthropic](https://github.com/anthropics/skills/blob/main/skills/canvas-design/SKILL.md)

**Strength:** Encourages deliberate composition, distinctive typography, restraint, and refinement of static PDF/PNG visuals.

**Fit limitation:** It prioritizes artwork with minimal text and abstract aesthetic exploration. That does not provide the information density, editable content, or decision support needed for many business documents.

**Our treatment:** Keep intentional composition and local refinement for covers and visual pages, while tying design choices to the commercial reader and preserving required text, facts, and editable layers. Unrelated fine-art creation remains outside this skill's scope.

## 8 Pro Report Builder

[Source — Rebecca Rae Barton](https://github.com/thatrebeccarae/claude-marketing/blob/main/skills/pro-report-builder/SKILL.md)

**Strength:** Provides reusable document modules, style tokens, explicit page budgeting, overflow checks, and an HTML-to-PDF production path.

**Fit limitation:** Mandatory cover/summary/recommendation pages, Letter sizing, warm content backgrounds, and fixed type rules can override the brief. Dense table defaults can reduce readability. Browser export does not fulfill DOCX or PPTX requests.

**Our treatment:** Keep reusable modules and page budgeting, make composition and format conditional, favor readability over compressed page counts, and route editable formats to the proper native authoring workflow.

## What the installed skill adds

| Need | Installed component |
|---|---|
| Generation, editing, redesign, review, repurposing | Scope-sensitive modes in `SKILL.md` |
| Proposals, brochures, catalogs, decks, reports, sales aids | `artifact-structures.md` |
| Copy and commercial evidence | `sales-writing.md` with a compact claim register |
| Brand styling and covers | `design-production.md` plus five original token presets |
| Digital, editable, and print output | Format routing and production checks |
| Structural PDF checks | `scripts/pdf_preflight.py` |
| Credo continuity | Dated source locator and brand snapshot, with current-fact refresh rules |

The measurable additions are broader integrated task coverage, an executable structural check, conditional use of the available native artifact workflows, and explicit preservation of evidence and editing scope. This is designed to improve suitability for Credo's business/sales work; it does not establish universal superiority over the external skills or better conversion outcomes.

## Validation completed

- The standard Skill Creator validator passed, and UI metadata allows automatic selection for matching tasks.
- All local reference links resolve. The five preset text palettes exceed 4.5:1 against their specified paper colors; other placements still need artifact-specific checks.
- The PDF helper passed 15 tests covering valid/invalid geometry, page count, rotated pages, UserUnit, bleed boxes, draft and required text, image-only policy, encrypted/corrupt inputs, URI annotations, CLI error behavior, and read-only input handling.
- A read-only structural check of the existing six-page Credo brochure passed page count, A4 displayed size, text presence, required brand text, and draft-token checks.

This validation does not benchmark authoring quality against the external skills. Native Word, PowerPoint, and Google authoring workflows were not exercised in this creation task, and the PDF structural pass does not establish visual quality, accurate commercial claims, full accessibility, or press acceptance.

## Claude Code port

Ported from the Codex version on 2026-10-10. The validation above was recorded for that version, whose UI metadata file is not part of this port; Claude Code selects the skill from its `SKILL.md` description. Format routing now names the `docx`, `pptx`, `pdf`, and `xlsx` skills where available, installed runtimes replace the Codex bundled-runtime loader, image generation is conditional on an available tool with a text-only fallback, and the PDF helper's missing-dependency message no longer refers to bundled Python. Its checks are otherwise unchanged.
