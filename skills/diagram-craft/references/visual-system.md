# Visual system and rendered checks

## Style from context

Use supplied guidance or project tokens first. For a website the user asked to match, inspect actual computed fonts/colors when possible and label approximations. Favor available readable fonts. Exports should not silently depend on web-font requests: end every font stack in a generic family (`sans-serif`, `serif`, `monospace`, `system-ui`) so the diagram still renders offline, and treat a brand web font as an opt-in the user asked for. `diagram.py check file.html` (or `.svg`) flags remote font requests and stacks without a generic fallback.

Scope tokens to the artifact: background, surface, text, secondary text, border, connector, accent, and accent surface. Coordinate dark colors deliberately rather than mathematically inverting them. The helper supplies warm-paper light and slate dark palettes with scene overrides.

## Hierarchy and density

Choose a clear entry point and reading direction. A title names the question/subject; a caption states the insight. Differentiate group, node, edge, and source labels with size/weight. Use mono for exact technical strings when helpful, not every label.

Favor readable text over fitting everything onto one page. Starting points are 16–20 CSS px for node labels and 12–14 px for secondary labels; adapt to the medium. ViewBox units change size when scaled. Wrap long labels, expand nodes, or use details. Don't shrink text until overflow disappears.

Groups express containment/scope. Keep related objects close and separate clusters. Status and category need textual or shape/line encodings in addition to color. An “assumed” badge remains useful in grayscale. Emphasize what answers the reader's question.

## Geometry

Position nodes from topology, route edges, then place labels. Give arrowheads space and keep labels off junctions. Distinguish crossings from joins. Shared connectors must intentionally mean the same thing before a split. Reserve gutters/corridors for feedback routes.

Use masks matching the surface under a label. On mixed surfaces move labels or use an explicit chip. Draw connectors before opaque nodes and labels last. Group boxes must not hide content or imply communication by touching.

Custom SVG can opt into the browser helper's annotations:

```xml
<g data-node="payments" data-x="80" data-y="90" data-w="240" data-h="120">…</g>
<text data-node-text="payments">Payments</text>
<g data-label="e1" data-x="340" data-y="120" data-w="130" data-h="32">…</g>
<polyline data-edge="e1" points="320,140 480,140" …/>
```

Bounds describe actual geometry in the annotated element’s local coordinate frame. The helper maps supported element/group translations, text bounds, and polyline points into the selected root SVG’s viewBox frame before comparing them. Scaling, rotation, skew, and unavailable transforms produce explicit warnings and skip affected geometry measurements; nested SVG content is excluded. It checks the first meaningful root SVG and warns if more diagrams need review. Untagged elements and curved connector paths require visual review; the helper cannot reliably infer their intention.

## Accessibility and responsiveness

Each meaningful SVG needs `role="img"`, unique `<title>`/`<desc>`, and resolving `aria-labelledby`. Describe the principal relationship; for substantial work add a text summary or relationship table. Hide decoration from assistive technology; do not make every SVG text separately focusable.

Contrast contract: text needs 4.5:1 against the surface it sits on; marks that carry meaning (node borders that define a shape, connectors, arrowheads, focus rings) need 3:1. A white node on warm paper is not a visible boundary by itself, so its border counts as an essential mark. Measure translucent tints after compositing them over the actual background, and check both themes. Purely decorative rules may be fainter. Color alone must not convey state or edge type.

The scene validator enforces these pairs for both built-in palettes and any token overrides: ink/muted text on paper, surface and accent surface; rule (node and region borders) on paper and surface; edge on paper; accent on paper and accent surface.

Use a responsive wrapper with a fixed readable canvas when shrinking would make labels illegible. Local horizontal scrolling is acceptable; whole-page overflow is not. Text alternatives should remain available on narrow screens. Check print scaling separately.

## Interaction and motion

Use interaction to expose sources, optional layers, versions, or events. Controls should be native, labeled, keyboard operable, visibly focused, and announce the current step where relevant. Preserve a complete static/no-JS view.

Animate when requested or when temporal change materially benefits. Provide pause/step for ongoing playback and honor reduced motion. Export a complete static state. Avoid decorative loops in a technical handoff.

## Rendered review

Wait for fonts. Inspect intended size and narrow view, including captions/tables. Check clipping, label overflow, arrowheads, masks, intersections, page overflow, and controls. Inspect actual PNG/PDF exports when delivered.

The helper detects annotated text containment, SVG bounds, simple orthogonal route obstruction, duplicate IDs, accessible naming, selected computed contrast, and page overflow. It does not validate meaning, every arbitrary path, occlusion, full WCAG compliance, export font portability, or every paint interaction. A clean report establishes only its declared checks.
