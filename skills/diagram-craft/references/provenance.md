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

## Host-neutral adaptation

Made host-neutral Agent Skills content on 2026-10-12. Install and invocation
docs now target the shared `~/.agents/skills/` location (see the repository
INSTALL.md) and name the skill in the prompt instead of a slash command;
Read-tool and named-browser wording became generic image-viewing and
browser-automation capability statements with an explicit "unverified" fallback;
one error message in the browser helper no longer mentions a host-bundled
`NODE_PATH`. The schema, renderer, inspector checks, tests, and examples are
otherwise unchanged.

## 2026-10-15 upstream review (cathrynlavery/diagram-design, reviewed through `d97c5c7`)

Reviewed the 66 upstream commits from `75f47bb` to `d97c5c7` for ideas only.
No upstream text, code, schemas, or data contracts were copied; the guidance and
the new helper checks were written independently here.

Adopted as ideas: a service blueprint diagram type (`9dcaff8`) and architecture
containment scopes separating administrative from traffic scopes (`a3af885`),
now guidance in `semantics-and-layout.md` with no new renderer. Export
robustness (`778bd8b` alpha with presentation opacity, `c959f97` CDATA,
`e794452` CSS selector scoping, `efcdcaf` live references versus commented
definitions, `489dbd5` nested icon SVGs and double-hyphen comments) and the
self-check for content painted outside the viewBox (`1a6a6fc`) became the
`export_findings` checks behind `diagram.py check` on an HTML/SVG export, with
tests, plus an "Export robustness" section in `delivery-and-import.md`. Mermaid
and Excalidraw input edge cases (BOM `3a856cd`, outer Markdown fences `e86841c`,
bare states `d2efbfb`, sequence fragments across highlight blocks `1a2d5c0`,
nesting guard `dd5ac3f`) are documented as import guidance only, because this
package ships no importer. The onboarding source-trust and output-verification
idea (`d8d7e3b`) became a confirm-before-fetching rule and a verify-inferred-style
note in `SKILL.md`, without any brand-profile gate.

Skipped: the gallery and navigation (`0482b93`), the type-count guard
(`3b7c186`, `14f95e2`), chart and geometry verifiers (`be2e736`, `d54f331`,
`76e7e26`, treemap, heatmap, dumbbell), example re-renders, release and manifest
bumps, the `--out` error handling (`56940eb`), the multi-PR landing commits
(`09c1428`, `3560ace`, `4afc31b`) beyond the fixes named above, and the headless
Chromium doctor (`13b2da4`), since this package has no doctor command.

## Inspiration review — 2026-10-20

Reviewed the upstream commits from `d97c5c7` through
[`f2f4d49ea8d632f17cf196ba26599277a93f767b`](https://github.com/cathrynlavery/diagram-design/tree/f2f4d49ea8d632f17cf196ba26599277a93f767b)
(v2.6.115) for ideas only, including the changes to its SVG export, PNG export,
draw.io and Mermaid extraction scripts and its loop reference. No upstream text,
code, tests, or data were copied; the guidance and the fix below were written
independently here.

Adopted as ideas:

- Conditional CSS in exports (`1553bf1`, media conditions kept; related
  `02b0ff9` comment-looking text in CSS strings, `da999a1` CSS-escaped local
  references). Our package has no CSS-carrying exporter, so these are
  verification notes in `delivery-and-import.md`. One of our own checks had the
  matching weakness: the scoped-selector test in `diagram.py check` ignored every
  rule nested inside `@media`/`@supports`/`@layer`/`@container` and could strip
  comment-looking text inside quoted selectors. It now reads grouped rules with
  a small string-aware scanner (`css_selectors`), with regression tests.
- Mermaid and draw.io import edge cases (`c633741` statements after the
  flowchart header semicolon, `64203b7` whitespace before a pipe label,
  `3f73d31` invisible links, `880b383` single-line state notes, `15d44ae`
  hidden draw.io cells): import guidance only, since this package ships no
  importer.
- PNG export (`5695d3d`): a verification note (pixel size equals viewBox times
  scale, no clipped edge, fallback-typography disclosure). Our browser helper
  already waits for fonts and widens the page wrapper; it does not yet release
  arbitrary clipping ancestors of a user-supplied page, which is recorded as a
  limit rather than changed, because Playwright was not available in this
  environment to run `tests/test_browser.cjs`.
- System-font mode also dropping carried `@font-face` (from the `--system-fonts`
  doc change): added to the export notes.

Skipped: plugin-manifest version bumps, Qoder/Factory/Codex host packaging,
maintainer-policy and merge-gate changes, upstream's packaged PNG renderer
refactor and its test suites, `@scope`/animation-name refusal logic (no exporter
here), the architecture containment important-priority fix (`4ebfd0c`, no such
verifier here), documentation anchor fixes, and the loop station-0 wording
(`05a858c`): this package ships no loop diagram type, so there is no station
placement formula to correct.

## Inspiration review — 2026-10-26

Checked cathrynlavery/diagram-design `b8f3617` (previously reviewed through `f2f4d49ea8d632f17cf196ba26599277a93f767b`, plugin 2.6.115 to 2.6.129). Changes are fixes to the upstream Mermaid importer (edge IDs in flowcharts, kept sequence `autonumber` directives, counted config directives, `else`/`and`/`option` regions in the digest), the self-check (rejects a document that stopped early), the service-blueprint verifier (Japanese two-line labels), heatmap markup parsing, export commands, and CI pins. This package has no Mermaid importer or upstream-style verifiers, so nothing was adopted; the "document stopped early" check is noted as an idea for a future completeness check in the inspector. No upstream text or code was copied.

## Inspiration review — 2026-10-29

Reviewed cathrynlavery/diagram-design from `b8f3617` through `0cf73c3` (14 commits, plugin 2.6.130 to 2.6.136) for ideas only. No upstream text or code was copied; the guidance, the fix, and the tests were written independently here.

Adopted as ideas: draw.io plain-versus-HTML label handling that keeps literal angle brackets (`17686b9`) and the Excalidraw outer-group chain (`84886eb`), both as import guidance in `delivery-and-import.md` because this package ships no importer; and the CSS-transform blind spot in geometry verification (`0b5b3bc`, plus the quoting-robustness idea from `d39a365`). Our `viewbox_findings` skipped only a `transform` attribute, so a shape moved by an inline `style` transform was judged at its written coordinates; it now treats that as unmeasurable, with regression cases. Our check parses XML, so single-quoted attributes were already read.

Skipped: the box-plot variant and its verifier, and the expanded scatter reference (`7bf9445`), because quantitative plots belong to a chart workflow per this skill's scope; the dp-integration arrowhead example tweak (`1677a5c`), since this package ships no such type; docs-sync test and release manifest bumps (`fbdbd83` and the version commits).
