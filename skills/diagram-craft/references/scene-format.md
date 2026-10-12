# Positioned scene format

`diagram.py` uses Python 3.9+ standard library. Positions are explicit, not auto-layout. Use native notation for sequences, UML, and ER.

```json
{
  "title": "Request path", "description": "The client calls the API.",
  "width": 760, "height": 300,
  "nodes": [
    {"id": "client", "label": "Client", "x": 40, "y": 90, "w": 220, "h": 120},
    {"id": "api", "label": "API", "x": 500, "y": 90, "w": 220, "h": 120}
  ],
  "edges": [
    {"id": "call", "from": "client", "to": "api", "label": "HTTPS request",
     "points": [[260,150],[500,150]], "label_at": [320,118]}
  ]
}
```

Coordinates are viewBox units; rectangles use upper-left `x/y` and positive `w/h`. `label_at` is a chip's upper-left. Points run from source boundary to target boundary. Reserve label space before rendering.

| Object | Required | Optional |
|---|---|---|
| Scene | `title`, `description`, `width`, `height`, `nodes`, `edges` | `theme` (`light`/`dark`), `tokens`, `regions`, `notes` (string list) |
| Node | `id`, `label`, `x`, `y`, `w`, `h` | `detail`, `shape` (`box`/`store`/`decision`), `emphasis` (boolean), `status`, `sources` (string list) |
| Edge | `id`, `from`, `to`, `points` | `label`, `label_at`, `label_w` (170 default), `style` (`solid`/`dashed`), `status`, `sources` |
| Region | `id`, `label`, `x`, `y`, `w`, `h` | none |

Status: `provided`, `observed`, `inferred`, `proposed`, or `unspecified` (default). Evidence tables expose status; inferred/proposed nodes carry a badge. Sources are escaped literal evidence descriptions/file references/URLs. The renderer does not fetch sources or verify truth. Use `observed` only for observations actually performed. `provided` suits user briefs and synthetic examples.

Overrides accept six-digit hex colors for `paper`, `surface`, `ink`, `muted`, `rule`, `edge`, `accent`, `accent_surface`. Use readable combinations.

```bash
python3 scripts/diagram.py render assets/architecture.scene.json --output request.html
python3 scripts/diagram.py check assets/architecture.scene.json
python3 scripts/diagram.py check request.html   # offline-font check for an export
python3 scripts/diagram.py extract request.html --output request.svg
```

Validation catches malformed schema, duplicate IDs, missing endpoints, nonfinite coordinates, invalid tokens, off-canvas geometry, node overlaps, rectangular edge obstruction, label/node overlap, off-boundary endpoints, and selected contrast failures. It refuses to render on failure. Touching nodes are allowed; diagonal routes are checked against rectangles. Region/node overlap is intentional containment.

Text wrapping is estimated; the browser checks actual bounds. Diamonds use rectangular bounds for text/route checks, so inspect corners manually. Checks do not prove all route quality, label/label separation, semantics, or source accuracy. Ports are points on bounding rectangles, not arbitrary shape paths.

IDs start with a letter and contain letters, digits, underscores, or hyphens; all IDs are unique across nodes/edges/regions. Text is HTML/XML escaped. Output files require `--force` to overwrite. Generated artifacts contain no JavaScript, remote fonts, or network dependencies.

Asset scenes are synthetic examples, not verified production systems. Regenerate their HTML/SVG after source changes.
