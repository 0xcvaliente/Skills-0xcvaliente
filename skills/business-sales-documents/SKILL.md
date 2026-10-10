---
name: business-sales-documents
description: Create, edit, review, and design business documents and sales brochures, including proposals, company profiles, product catalogs, sales one-pagers, reports, and pitch decks. Use when audience, sales messaging, brand consistency, page layout, or print preparation matters. use other skills for unrelated web UI or standalone artwork.
metadata:
  version: 1.0.0
---

# Business & Sales Documents

Deliver the requested business artifact with a clear commercial purpose, supportable claims, appropriate design, and a usable final file. Load only the references needed for the task.

## Choose the mode and scope

| Request | Working approach |
|---|---|
| Create or draft | Produce the artifact in the requested format. |
| Edit or proofread | Make the requested changes; preserve sound copy, facts, voice, structure, and styling. |
| Redesign | Improve hierarchy and layout within the user's content and brand constraints. |
| Review | Identify specific defects and proposed repairs; do not rewrite unless requested. |
| Repurpose | Adapt audience, sales stage, density, and format while retaining factual scope. |
| Prepare for printing | Apply the supplied printer specification and check the exported file. |

For a narrow correction, read the file and make the correction directly. Do not turn a typo fix into a strategy exercise, brand reset, new document family, or full review.

## Establish the brief from existing context

Identify the artifact, reader, desired action or decision, use channel, format, content boundaries, and brand/template authority. For sales collateral, also identify the buying stage and recipient's role. Inspect supplied materials before asking questions.

Ask only when a missing answer would materially change the result, such as conflicting source values, an unknown recipient that changes the argument, or a printer's fold specification needed for final production. Otherwise state a reasonable assumption and proceed. Design direction and page count may be chosen from the brief; they do not require routine confirmation.

For company-specific brand or context material, use the brand source the user supplies; do not assume one.

## Select relevant references

- For proposals, reports, one-pagers, catalogs, brochures, or decks: read the relevant section of [artifact structures](references/artifact-structures.md).
- For sales messaging, evidence, copy editing, or objections: read [sales writing and evidence](references/sales-writing.md).
- For creation or substantial visual changes: read [design and production](references/design-production.md).
- When the `valiente` MCP server is connected and the brief needs existing files, notes, or correspondence: read [Valiente MCP](references/valiente-mcp.md).
- Before delivery or a substantive review: use applicable checks in [quality and delivery](references/quality-delivery.md).
- For provenance, coverage, and design rationale: [external workflow analysis](references/external-workflow-analysis.md). Do not load this during ordinary authoring.

## Build the argument and design together

Start with what this reader must understand or do. In a proposal, connect work to scope and terms. In a brochure, make category, relevance, demonstrated mechanism, and next action easy to find. In a report, make conclusions traceable to evidence. Give each section or page a purpose.

Map significant claims to supplied or verified sources. Preserve conditions, units, dates, and limitations. Use current authoritative material for changing facts. Metrics, certifications, prices, guarantees, affiliations, and testimonials need appropriate evidence. A product example demonstrates a mechanism; it does not prove customer outcomes.

Keep sources, open questions, and production notes outside customer-facing copy unless citations or limitations belong in the artifact. For a large or claim-heavy deliverable, use the compact working claim register in the writing reference. Small edits do not need a separate register.

Use a supplied template or brand as the design authority. Preserve logo artwork and product screenshots. Without a visual reference, choose a coherent direction suited to the industry and channel. Record type, color, spacing, and page roles; avoid forcing all artifacts into one palette, card system, cover, or page size.

## Produce the requested format

Use available file-format skills for file mechanics and required verification, applying this skill's brief and commercial decisions. In Claude Code these are typically the `docx`, `pptx`, `pdf`, and `xlsx` skills, if available:

- **Word / DOCX:** the `docx` skill; preserve styles, tables, links, and requested tracked changes. Explicit user/template choices take priority over generic visual defaults.
- **PowerPoint / PPTX:** the `pptx` skill; distinguish slides for a speaker from a deck that must stand alone.
- **Google Docs / Slides:** a connected Google Drive integration (MCP server or connector) and a matching authoring skill, if available; preserve native templates and requested native deliverables.
- **PDF:** the `pdf` skill; keep important text searchable where possible. Retain an editable working source, but deliver additional formats only if requested or necessary for an explicit editable-output requirement.
- **HTML:** use when requested or appropriate as a PDF working source. It does not fulfill a request for editable Word or PowerPoint.
- **Images:** if an image-generation tool or MCP server is available, use it for imagery that benefits from it; otherwise supply the image prompts, specifications, and a list of the assets needed, and say plainly that no image was generated. Never claim an image was made. Retain exact text, logos, data, and specifications in deterministic layout layers.

Use the runtimes and tools already installed on the machine or in the project (for example `python3` with `pypdf`, LibreOffice, or a headless browser) for artifact work; check before relying on one. Follow the matching skill's authoring markers and render gates. Do not assume a particular install path, browser binary, commercial font, API key, or uninstalled service.

If a required tool or source is unavailable, complete independent work and explain the concrete limitation. Do not silently substitute output types or claim verification that did not run.

## Verify and finish

Check content and edit scope, factual consistency, reader comprehension, brand fidelity, actual-size layout, and output integrity. Fix material defects and inspect again. Render pages or slides to images with the matching file skill or installed tools and inspect them with the Read tool; text extraction alone cannot verify layout.

For PDFs, `scripts/pdf_preflight.py` checks page counts, dimensions, box containment, draft tokens, basic text presence, and URI annotations. Run it with a `python3` that has `pypdf` installed and explicit expectations. It is a structural aid, not a claim verifier or certificate of accessibility, print readiness, working links, or visual quality.

Use authorization already in the conversation. Do not invent a confirmation gate before an authorized final export. Sharing, sending, publishing, and connected-document changes remain within the actual request and tool permissions.

Return the requested deliverable with a short note about consequential changes, completed checks, and remaining limits. For review-only work, give location, defect, reader impact, and a concrete repair. Do not attach private QA or evidence records unless requested.
