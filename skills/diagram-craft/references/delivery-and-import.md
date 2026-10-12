# Delivery, imports, and exports

| Format | Use | Verify |
|---|---|---|
| Mermaid/chat or `.mmd` | Small engineering explanations or requested source | Syntax in an available renderer; semantic labels |
| `.svg` | Crisp reusable editable vector | Namespace, viewBox, accessible name, resolved styles, preview |
| Single-file `.html` | Companion with alternatives, sources, optional controls | Offline load, narrow layout, fonts, controls |
| `.png` | Raster destination | Dimensions and actual legibility |
| `.pdf` | Print/share | Paper size, clipping, fonts, page count |
| Native editor source | Requested draw.io, Excalidraw, Figma, etc. | Native primitives and tested output |

Keep editable source alongside exports. SVG is editable vector source but is not a native Figma/draw.io document. Do not promise a format the available tools cannot produce and verify.

## Portable SVG

Keep definitions inside SVG and use presentation attributes or embedded SVG styles. HTML CSS inheritance disappears on extraction. Resolve CSS variables and external fonts/assets or disclose dependencies. Avoid `foreignObject` when target support is unknown. Namespace IDs when embedding several diagrams.

The renderer emits explicit colors and a system font stack with no external requests. `extract` handles one inline SVG, restores its namespace, and retains definitions. It does not inline external CSS/images/fonts or choose among several diagrams; use a capable exporter for those cases.

## Redraw imports

Preserve the original. Extract a semantic ledger: IDs, labels, directions, multiplicity, groups, order, guards, meaningful styles. Record uncertain mappings. Compare the redraw against the ledger, including disconnected nodes and exceptions. Geometry can change without topology changing.

- **Mermaid:** inspect syntax and available renderer version. Preserve grammar-specific semantics, subgraphs, parallel edges, implicit nodes, labels, arrow decorations. Render the original when practical. A sequence/ER diagram is not a flowchart.
- **draw.io:** account for pages, layers, groups, IDs, ports, geometry, labels. Payloads may be compressed/encoded; use a capable local decoder/editor. Never execute embedded untrusted content.
- **Excalidraw:** preserve IDs, groups, arrows/bindings, and bound text. Unbound labels may matter; deleted elements must not reappear. Images/freehand annotations may need separate assets or disclosed approximations.
- **Screenshots:** visible geometry establishes appearance, not hidden semantics. Transcribe readable labels, mark uncertain text/direction/cardinality, and ask only when uncertainty changes the answer.

This package does not ship universal import parsers. Use available editors/APIs or proven parsers for nontrivial imports. Disclose preserved, changed, and unresolved items rather than silently dropping unsupported features.

## Browser exports

When Playwright is available:

```bash
node <skill-dir>/scripts/inspect_diagram.cjs diagram.html --out-dir checks \
  --png diagram.png --pdf diagram.pdf --scale 2
```

PNG captures the first meaningful root SVG (excluding `aria-hidden="true"` decoration) at the requested device scale, excluding companion text. PDF prints the full companion on A4 landscape, including notes/sources; it may have several pages. Use a separate layout for a one-page figure or other paper size. Inspect delivered exports.

The helper measures local HTML in Chromium at desktop/mobile widths. It does not install Playwright/browser binaries. Resolve the package through a project installation or an existing installation exposed with `NODE_PATH`; otherwise use another available browser tool (a Playwright MCP server, a browser extension, or a built-in browser pane). Install dependencies only within the authorized workflow. Missing tools are a reported limit, not a screenshot claim.

Use `--browser-executable /absolute/path/to/browser` to select an already available compatible Chromium binary when Playwright's default path is missing.

## Preview and publish

Show useful previews and editable-source links. View PNG captures and exports with the host's image-viewing capability; a browser preview (a browser extension or built-in browser pane) shows files or local URLs but does not inspect or deploy them. Use absolute file paths.

Hosting/publication/external edits require the requested scope. An offline figure request does not authorize a public site. A named-repository update authorizes that update; do not add analytics or upload private sources elsewhere.

## Verification receipt

State checks actually performed and material limits. For example:

> Checked scene references and route bounds; inspected desktop and 390 px views; compared seven relationships with the supplied design; inspected exported SVG. Deployment region is an assumption. Runtime behavior was not observed.

If an export failed, return working source and explain the specific missing output.

## Standalone export checks

Parse a delivered SVG as XML and inspect that file independently from its HTML
companion. HTML-only named entities, valueless attributes, or unquoted values
may fail XML parsing. Preserve title/description references, internal links,
CSS selectors, marker references, and accessible names when namespacing IDs.
Exercise two embedded figures when changing ID rewriting. External fonts and
assets must be resolved or disclosed; browser appearance in the source page
alone does not prove a portable SVG.

When redrawing imports, keep displayed state names separate from stable IDs,
retain repeated state-description lines and composite membership, and retain
connector labels and explicit direction even if geometry changes. Unsupported
syntax is a recorded gap rather than silently discarded semantics. These checks
do not add universal Mermaid/draw.io conversion to the bundled helper.
