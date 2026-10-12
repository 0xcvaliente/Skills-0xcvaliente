# Design and production

## Design authority and themes

Use the supplied template or approved brand guide first; honor explicit departures. Competitor references may inform layout, not authorize borrowed text, proof, logos, or imagery. Preserve accepted layers when repairing a defect.

Without a reference, choose an industry- and audience-appropriate direction. Restraint often suits a proposal; a brochure may need more expressive composition. The original optional [design presets](../assets/design-presets.json) provide five role-based starting systems. Adapt them rather than forcing a preset. Record palette roles, type hierarchy, spacing, grid, image treatment, and page roles. A fixed theme catalog need not interrupt every job.

Define colors by role: paper, main/secondary text, accent, and real data states. Use available, permitted fonts and record fallback substitutions. Do not assume a commercial font or that online fonts load before export. A body family and optional display family are often enough; the user's brand governs.

## Layout decisions

- Choose size/orientation from the brief. A4 is a reasonable stated working assumption for European handouts; preserve specified Letter or custom sizes.
- Give pages distinct jobs within a coherent system. Opening, mechanism, comparison, evidence, and contact pages need not repeat one composition.
- Budget captions, notes, and footers before fitting content. Inspect real-size readability, not universal word or component counts.
- For A4, body around 10.5–12 pt and notes around 9–10 pt are starting values. Repaginate or simplify before shrinking essential text.
- Keep headings with their content, captions with images, and table headers with rows. Let rows expand instead of clipping fixed heights.
- Use tables for comparable attributes; preserve units and clarify empty values. Do not put narrative paragraphs into decorative grids.
- Use product examples/diagrams to explain real relationships. Unrelated stock images and icons often consume useful space.
- Use only modules the artifact needs: narrative, image/caption, specification table, comparison, workflow, quote, and contact.

## Identity and accessibility

Preserve logo proportions, artwork, and authorized colors. Crop photos without hiding decisive features. Keep catalog asset/model mapping explicit. Do not let generation redraw logos, model labels, technical parts, data, or UI evidence.

Keep essential copy in real text layers when the medium permits. Rasterize artwork rather than whole documents. Effective image DPI equals pixels divided by placed inches; a file labeled 300 DPI can still contain a low-resolution image.

Pair meaning conveyed by color with labels. Aim for 4.5:1 contrast for normal digital text and 3:1 for large text. Preserve original logos and choose legible surroundings. Use supported heading structure, table semantics, reading order, alternative text, and document language. Visual checks alone do not certify accessibility.

## File formats

**DOCX:** Use semantic styles and stable paragraph/table layout; preserve requested breaks, numbering, headers, links, comments, and tracked changes. Use the `docx` skill, if available, for mechanics and rendering.

**PPTX:** Keep text/elements editable; preserve requested ratio, notes, masters, and theme. Forwarded decks must explain themselves. Use the `pptx` skill, if available, for mechanics/rendering.

**HTML to PDF:** Keep maintainable local source, semantic text, and style tokens. Set print size/margins, wait for fonts/images, use break rules, avoid clipped fixed-height containers, and inspect the exported PDF. HTML is not an editable Word/PowerPoint substitute.

**PDF:** Preserve searchable text, links, page order, and appropriate metadata. Make page boxes intentional. Some edits are better made in the original source and re-exported; preserve the supplied PDF if rebuilding.

**Native Google document:** Use a connected Google Drive integration when one is available and preserve native template features. A remote reference is not an authorized edit target merely because it was supplied.

## Print and folded brochures

Inspect the printer's specification when supplied. Establish trim, orientation, bleed, safe area, fold/binding, panel order, color profile, and PDF standard to the extent needed.

For folded brochures, determine outside/inside panel order and fold direction. Some folds need unequal widths. Prefer the printer's dieline. A labeled draft can proceed without final geometry, but do not promise press readiness. Do not silently compress a long brochure into three panels.

Use 3 mm bleed only as a stated working assumption when relevant. Extend backgrounds to bleed and keep essential content safely inside trim/folds; the production spec governs distances. TrimBox describes finished size; BleedBox includes bleed and fits in MediaBox. Add crop marks when requested, not automatically.

Tie RGB/CMYK to the delivery specification. Browser RGB output is not automatically PDF/X or accepted by every press. Use suitable conversion/preflight tools when the required standard calls for them, and verify the conversion. Disclose unsupported requirements specifically. Geometry checks do not certify artwork bleed, separations, fonts, or printer acceptance.

## Revision repair

Identify the failing layer: facts/identity, reader message, copy, hierarchy, typography/spacing, or export. Repair the smallest effective layer. Inspect affected pages and neighboring pagination; follow the artifact skill's full render gate where required. Retain originals and clear revision names; old drafts are not current approvals.
