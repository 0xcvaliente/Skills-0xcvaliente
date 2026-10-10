# Provenance

Diagram Craft is original Codex skill content and code by 0xcvaliente, inspired by the problem addressed by [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design).

Inspected on 2026-10-07 at revision [`d1376371965f513d99cc9ec388835d255c5c88d5`](https://github.com/cathrynlavery/diagram-design/tree/d1376371965f513d99cc9ec388835d255c5c88d5). The reference's MIT license names Cathryn Lavery, copyright 2025.

The reference demonstrates the value of editorial layout, HTML/SVG output, semantic notation, and rendered checks. This package does not copy its instruction text, scripts, templates, fonts, artwork, or gallery. The schema, renderer, inspector, tests, scenes, and documentation were authored for this package.

Our emphasis is a concise Codex entrypoint, entity/edge evidence status, flexible styling, optional tooling, and explicit verification limits. We do not claim universal superiority or the reference's full gallery/import coverage. Automatic discovery is enabled; routine work has no first-use brand gate.

The package MIT license covers its original files only, not neighboring skills or user materials.

## Inspiration review — 2026-10-09

Reviewed upstream export/import guidance changes through
[`f4547ee95f88e5b28a52517feff6b6c11cc657f9`](https://github.com/cathrynlavery/diagram-design/tree/f4547ee95f88e5b28a52517feff6b6c11cc657f9).
Added independent SVG/XML, ID/reference, font-dependency, and state-import
verification guidance. No upstream scripts, fonts, chart families, or parser
capabilities were copied or claimed for this original renderer.

## Inspiration review — 2026-10-10

Reviewed the 12 changed upstream files through
[`75f47bbae5db21d2269a0c5134b22ce342686db4`](https://github.com/cathrynlavery/diagram-design/tree/75f47bbae5db21d2269a0c5134b22ce342686db4).
The geometry and motion checks now account for translated elements and exempt
decorative SVG icons from diagram naming requirements. Independently upgraded
this package's browser helper to select the first meaningful root SVG for
checks and PNG capture, normalize supported translations into one canvas frame,
and warn about unsupported transforms. Added browser regressions for valid
translated diagrams, route obstruction, off-canvas nodes, decorative-only pages,
unsupported transforms, and PNG target selection. No upstream scripts or
instruction text were copied.

## Claude Code port

Ported from the Codex version on 2026-10-10. Install and invocation docs now
target `~/.claude/skills/` and `/diagram-craft`; Codex desktop preview steps
became Read-tool viewing and optional browser tooling; the Codex-only
`agents/openai.yaml` metadata and collection installer/validator commands were
dropped. The schema, renderer, inspector, tests, and examples are unchanged.

## 2026-10-10 upstream review (cathrynlavery/diagram-design 2.6.71–2.6.73)

Reviewed upstream commits since `75f47bb` (head `246d6d7`) for ideas, without
copying files. Upstream raised its default palette to WCAG AA, wrote a contrast
contract for text and essential marks, and added a system-font export mode.
Applied independently here: the light `rule` token moved from `#9aa5a6`
(2.30:1 on paper) to `#7d898a` (3.28:1) because it draws node borders; the
validator now also checks muted/paper, rule/paper, rule/surface and
accent/paper; `diagram.py check` accepts an HTML/SVG export and reports remote
font requests and font stacks without a generic fallback. The shipped examples
were re-rendered (only the border color changed). Upstream's gallery numbering
and doc type-count guard concern its 44-type catalog, which this package does
not ship, so they were not adopted.
