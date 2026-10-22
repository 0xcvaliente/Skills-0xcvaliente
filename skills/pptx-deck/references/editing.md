# Editing and converting existing decks

Used by Mode C (edit) and Mode D (convert or restyle). Always work on a copy: write to a new file and keep the original untouched.

## Standard sequence

1. Inventory: see what is on each slide.
2. Choose the lightest tool: `replace_text.py` for wording, `rearrange.py` for order, raw XML only for what those cannot do.
3. Validate the package: `ooxml.py validate`.
4. Run `qa_check.py`, render with `render.py --grid`, and look at the slides you changed.

## Inventory

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/inventory.py deck.pptx -o deck-work/inventory.json
python3 ${CLAUDE_SKILL_DIR}/scripts/inventory.py deck.pptx --slides 2-5
```

The JSON lists `slideCount`, slide size, and for each slide its `index` (1-based), `layout`, `hidden`, `notes`, and every `shape` with `id`, `name`, `path`, `type`, `bounds` (inches), `outOfBounds`, paragraphs with runs (font, size, colour) and autofit. Groups are flattened; a shape inside a group has a path such as `3/2`. Use the `path`, numeric `id` or `name` as the key in replacements.

## Text replacement

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/replace_text.py deck.pptx replacements.json --dry-run
python3 ${CLAUDE_SKILL_DIR}/scripts/replace_text.py deck.pptx replacements.json -o deck-edited.pptx
```

Format of `replacements.json` (both `slides` and `find_replace` are optional):

```json
{
  "slides": {
    "2": {
      "5":        {"paragraphs": ["New first paragraph", "New second paragraph"]},
      "Subtitle": "One paragraph\nanother paragraph",
      "3/2":      "text inside the group member with path 3/2",
      "7":        {"cells": {"2,3": "new text for row 2, column 3"}},
      "7@3,1":    "same idea: cell row 3, column 1 of table shape 7",
      "9":        {"rows": [["Region", "Revenue"], [null, "13.0"]]},
      "notes":    {"paragraphs": ["New speaker notes"]}
    }
  },
  "find_replace": [
    {"find": "Q3", "replace": "Q4"},
    {"find": "Acme Corp", "replace": "Acme Inc.", "slides": [1, 4]}
  ]
}
```

Rules:

- Slide keys are 1-based slide numbers (strings). Inside a slide a key is matched first as a shape path, then a numeric shape id, then a shape name. A name that matches several shapes is an error; use the id or path.
- Paragraph replacement writes the new text into the first run of each paragraph (its formatting stays) and removes the other runs. Extra paragraphs copy the last existing paragraph. Paragraphs beyond the new list are removed. `\v` in a string becomes a line break.
- `find_replace` works across run boundaries; the first run's formatting wins. It covers groups, tables and notes. Add `slides` to limit it.
- A key or a find that matches nothing is an error: the exit code is 1 and nothing is written. Use `--dry-run` first. Exit codes: 0 ok, 1 unmatched or invalid input, 2 unreadable files.
- Never shorten text just to fit and never end with "...". If a replacement is longer than its box, say so, then pick a shorter wording yourself or move content to another slide.
- Translating a deck: build one replacements file with all text, keep numbers and names, and re-render to catch overflow because other languages are longer.

## Reordering, duplicating, deleting

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/rearrange.py deck.pptx --order "1,3,3,2" -o deck-new.pptx
python3 ${CLAUDE_SKILL_DIR}/scripts/rearrange.py deck.pptx --order "1,4-6,2" -o deck-new.pptx
```

`--order` lists the slides of the result by their 1-based position in the input. A number once keeps the slide; a repeated number duplicates it (charts, workbooks and notes are cloned under new part names); a number left out deletes that slide. Ranges like `4-6` work. Exit codes: 0 ok, 1 invalid order or output fails validation, 2 unreadable input.

Section lists, custom shows and slide-jump links are kept consistent; sections are dropped with a message if the new order no longer fits them. After duplicating a slide, change its text with `replace_text.py` on the new file (re-run `inventory.py` because slide numbers moved).

## Raw XML edits

Use when the wrapper tools cannot do the job: run-level formatting, hyperlinks, hidden slides, notes structure, theme colours, table styles.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/ooxml.py unpack deck.pptx deck-work/unpacked --pretty
# edit files under deck-work/unpacked/ppt/ with Edit
python3 ${CLAUDE_SKILL_DIR}/scripts/ooxml.py pack deck-work/unpacked deck-edited.pptx
python3 ${CLAUDE_SKILL_DIR}/scripts/ooxml.py validate deck-edited.pptx
python3 ${CLAUDE_SKILL_DIR}/scripts/ooxml.py validate deck-work/unpacked --json
```

`unpack` writes each part at its package path; `--pretty` re-indents XML for reading without changing text nodes. `pack` zips in a deterministic order ([Content_Types].xml first). `validate` accepts a `.pptx` or an unpacked directory and exits 0 clean, 1 problems, 2 unreadable.

Common places in the XML:

| Spot | File | What it is |
|---|---|---|
| `<a:t>` | `ppt/slides/slideN.xml` | The visible text of a run. Edit text here |
| `<a:r>`, `<a:rPr>` | same | A run and its properties: `sz` (hundredths of a point, 1800 = 18 pt), `b`, `i`, `lang`, fill colour |
| `<a:p>`, `<a:pPr>` | same | A paragraph and its alignment, bullets, spacing |
| `<p:sp>`, `<p:pic>`, `<p:graphicFrame>` | same | A shape, a picture, a chart or table frame; `<a:off>` and `<a:ext>` give position and size in EMU (914400 per inch) |
| `<p:sldIdLst>` | `ppt/presentation.xml` | The slide order; each `<p:sldId>` has an `id` and an `r:id` that points into `ppt/_rels/presentation.xml.rels` |
| `show="0"` on `<p:sld>` | slide XML | A hidden slide |
| notes | `ppt/notesSlides/notesSlideN.xml` | Speaker notes text in the body placeholder's `<a:t>` |
| theme colours and fonts | `ppt/theme/theme1.xml` | `<a:clrScheme>`, `<a:fontScheme>` |
| relationships | `ppt/slides/_rels/slideN.xml.rels` | Links from a slide to its layout, images, charts, notes |

Pitfalls:

- Split runs: a visible word is often several `<a:r>` elements ("Rev", "enue"). Search for fragments, or use `replace_text.py` find/replace, which merges runs for you. When you edit XML by hand, put the full text in the first run and delete the rest.
- Text with `&`, `<` or `>` must be escaped (`&amp;`, `&lt;`, `&gt;`). A leading or trailing space needs `xml:space="preserve"` on the text element where the format uses it.
- Orphan parts: deleting a `<p:sldId>` leaves `slideN.xml` and its relationship in place. Remove the slide's relationship from `ppt/_rels/presentation.xml.rels` and its `Override` from `[Content_Types].xml`, and delete the notes slide and any chart parts that only it used. `rearrange.py` does all this for you; prefer it for deleting slides.
- Content types: every new part needs a `Default` (by extension) or an `Override` in `[Content_Types].xml`, or PowerPoint will ask to repair the file.
- Unique ids: `<p:sldId id>` values must be unique (at least 256); shape ids unique per slide; relationship ids unique per rels file.
- Do not hand-write new slides when the builder can make them. If you must add one, copy an existing slide with `rearrange.py` first and change its text.
- Do not touch `docProps` unless the user asks.

## Convert or restyle (Mode D)

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/extract.py old.pptx -o deck-work/extracted
python3 ${CLAUDE_SKILL_DIR}/scripts/extract.py old.pptx -o deck-work/extracted --to-spec --theme swiss-cobalt --density reading-first
```

`extract.py` writes `deck-work/extracted/extracted.json` (titles, text blocks, bullets, tables, chart data, images, notes) and saves images in `assets/`. With `--to-spec` it also writes `deck-spec.json`, validated; `--theme` sets the theme (default an auto-pick theme), `--density` is `speaker-led` (default) or `reading-first`. Exit codes: 0 ok, 1 the draft spec has validation errors, 2 unreadable input.

The draft is a starting point, not a result:

1. Read `extracted.json` and the draft spec. Roles are guesses; change them to fit the content (`metrics`, `comparison`, `process`, ...).
2. Rewrite titles as takeaways, add a real `coreMessage` per slide, add notes (the source notes are kept when present).
3. Trim: one message per slide, split slides that exceed the item caps, remove duplicated or decorative text.
4. Check image paths in `assets/`, add `alt` text, and drop images that were backgrounds or logos from the old design.
5. Offer style previews (`preview_styles.py --spec deck-work/extracted/deck-spec.json --auto 3 -o deck-work/styles`), set the chosen `theme` and a `randomSeed` that starts with it.
6. `validate_spec.py`, `build_deck.py -o deck-restyled.pptx`, `render.py`, `qa_check.py --spec`. Compare against a render of the old deck and confirm nothing was lost: slide count, numbers, names, chart data.

To keep a company's masters and layouts while rebuilding the content, pass `--template company.pptx` to `build_deck.py`. This reuses the template's masters, theme fonts and colours and builds new slides on its blank layout; it does not fill the template's existing slides (see `templates.md`).

## After every edit

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/ooxml.py validate deck-edited.pptx
python3 ${CLAUDE_SKILL_DIR}/scripts/qa_check.py deck-edited.pptx
python3 ${CLAUDE_SKILL_DIR}/scripts/render.py deck-edited.pptx -o deck-work/render --grid
```

Read the QA issues, then look at the changed slides in the render. A deck that validates can still look wrong, and a deck that looks right can still fail validation. Report both results.
