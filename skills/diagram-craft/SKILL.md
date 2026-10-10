---
name: diagram-craft
description: Create, redraw, or refine explanatory diagrams from source material or code, including architecture, flows, sequences, states, and data relationships. Use for polished editable SVG/HTML diagrams and diagram reviews; use a chart workflow for quantitative plots and an image workflow for illustrations.
license: MIT
metadata:
  version: "1.1.0"
---

# Diagram Craft

Make the relationship clear, preserve the evidence, and deliver a diagram the user can edit. Visual polish must not change what the model says.

## Decide the representation

Respect the requested type, brand, format, and detail level. For an unspecified format, use inline Mermaid for a small static engineering explanation that fits comfortably in chat. Use standalone SVG with an HTML companion for a polished, shareable, or visually controlled deliverable. Use interaction when filtering, stepping through events, or comparing scenarios materially helps. Do not turn a diagram request into an application build or require brand onboarding.

Identify the reader's question and choose the layout that answers it. Read the relevant section of [semantics-and-layout.md](references/semantics-and-layout.md) when modeling architecture, behavior, data relationships, or structural changes. Do not load every reference for a small task.

## Establish the model before drawing

- Use supplied material first. For repository diagrams, inspect the relevant current code/configuration and cite concrete file locations. Ask for missing material only when it determines correctness; continue independent work meanwhile.
- Name entities with stable IDs and relationships with explicit direction and meaning. Distinguish observed implementation, user-provided claims, inferences, and proposals. Never invent retries, owners, cardinalities, quantities, or trust boundaries.
- Preserve synchronous versus queued work, success versus failure, possible versus guaranteed, and logical ownership versus runtime placement. Two different relationships need two arrows or explicit notation.
- For substantial diagrams, keep an evidence ledger: entity/relationship ID, statement, source, and status. Store it in editable source or adjacent notes. Do not expose secrets or private source text in shared outputs.
- Split overview/detail based on readability at the intended size, not a universal node cap. Keep necessary branches in a detail panel or companion view rather than deleting them to fit a template.

For multi-part work, give a brief update naming the question, representation, and material assumptions, then proceed. Default palettes and routine layout choices do not require a confirmation pause.

## Design the reading path

Read [visual-system.md](references/visual-system.md) when authoring or substantially restyling SVG/HTML. Reuse project tokens or supplied brand guidance; otherwise select an intentional neutral palette and name it in the handoff. Keep styling local to the artifact. Do not modify globally installed skills or save brand profiles unless requested.

Use spacing, typography, grouping, and line weight before adding color. Comparable objects need comparable treatment; important distinctions must remain legible in grayscale. Separate focal emphasis from labeled status/category encodings. Shapes, shadows, corners, diagonal connectors, and fonts are design choices, not universal prohibitions.

Route edges deliberately. Put labels in clear space; use a background mask where a line would interfere. Avoid non-endpoint nodes, ambiguous junctions, hidden arrowheads, and overlapping labels. Use distinct attachment points where several edges meet. Curves and diagonals are useful when they explain the structure clearly.

## Author an editable artifact

The bundled [scene format](references/scene-format.md) and standard-library helper suit positioned node-and-edge diagrams. They provide deterministic rendering, evidence tables, text wrapping, geometry checks, and standalone SVG extraction:

```bash
python3 <skill-dir>/scripts/diagram.py render scene.json --output diagram.html
python3 <skill-dir>/scripts/diagram.py check scene.json
python3 <skill-dir>/scripts/diagram.py check diagram.html   # export needs no web fonts
python3 <skill-dir>/scripts/diagram.py extract diagram.html --output diagram.svg
```

Start from the architecture or decision-flow scene in `assets/` when it fits. The helper does not auto-layout or implement sequence, ER, or UML notation. Author those with native SVG/HTML, Mermaid, or the requested editor format and apply the semantic guidance. The [sequence example](assets/sequence/order-sequence.html) demonstrates alternatives, asynchronous messages, and an evidence ledger. Copy example sources into the target workspace before adapting them. Do not force specialized notation into generic boxes.

Read [delivery-and-import.md](references/delivery-and-import.md) for imports, exports, interaction, or embedding. Preserve original imports and account for changed or unsupported semantics. This package supplies guidance, not a universal import converter.

## Verify the actual result

Compare relationships, branch conditions, ordering, and assumptions against the model and evidence. Inspect the rendered artifact at its intended size and a narrow viewport. Render and inspect an exported/shared visual in its delivered format too.

When Playwright and a browser are available, the optional helper measures actual SVG text/shape bounds, checks accessible naming and selected contrast pairs, and captures previews:

```bash
node <skill-dir>/scripts/inspect_diagram.cjs diagram.html --out-dir checks
# Add --png diagram.png or --pdf diagram.pdf for requested exports.
```

View the captured screenshots and exports with the Read tool. Without Playwright, use whatever browser tooling the session has (Claude in Chrome, a Playwright MCP server, or the desktop app's browser pane) for a visual check; do not assume one exists. The helpers report a useful subset of defects, not a complete visual/semantic verdict. Review crossings, chronology, line masks, custom contrast, and source accuracy yourself. Fix observed defects and repeat affected checks. If rendering is unavailable, perform structural checks and report the missing visual verification instead of claiming a pass.

## Deliver

Return requested output and editable source, a short description, and material assumptions/omissions. For substantial work include a compact receipt stating checks actually performed and their limits. Give absolute file paths; when browser tooling is available, open a useful file/browser preview. A preview is not a deployment. Publish or update another application only within the user's requested scope.
