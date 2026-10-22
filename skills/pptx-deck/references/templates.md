# Working with a user's template (Mode B)

Use this when the finished deck must look exactly like the user's own `.pptx`. The idea: select, order and duplicate the template's existing slides, then change text and pictures only. Layout, fonts, colours and shapes stay as the template designer made them. No template is bundled with this skill.

## Steps

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/template_profile.py template.pptx -o deck-work/profile.json
python3 ${CLAUDE_SKILL_DIR}/scripts/render.py template.pptx -o deck-work/template-render --grid
# write deck-work/edits.json
python3 ${CLAUDE_SKILL_DIR}/scripts/fill_template.py template.pptx deck-work/edits.json --profile deck-work/profile.json -o deck.pptx --dry-run
python3 ${CLAUDE_SKILL_DIR}/scripts/fill_template.py template.pptx deck-work/edits.json --profile deck-work/profile.json -o deck.pptx
python3 ${CLAUDE_SKILL_DIR}/scripts/qa_check.py deck.pptx --template template.pptx
python3 ${CLAUDE_SKILL_DIR}/scripts/render.py deck.pptx -o deck-work/render --grid
```

## What the profile contains

`template_profile.py` prints JSON (or writes it with `-o`). Top level: `file`, `slideWidthIn`, `slideHeightIn`, `slideCount`, `summary`, `slides`. Slide numbers are 1-based.

`summary`:

- `typeScale`: the font sizes used for title, subtitle, figure, body and label, with `bodyMedian`.
- `palette`: theme colours (`dark1`, `light1`, `dark2`, `light2`, `accents`, `hyperlink`).
- `fonts`: `major`, `minor` and the fonts `used`.
- `rolesToSlides`: slide numbers recommended for each page role: `cover`, `agenda`, `section`, `content`, `closing`.
- `contentTypes`: content slides grouped by type (for example `columns`, `chart`).

Each entry of `slides`:

- `index`, `layout`, `hidden`, `notes`, `hasChart`, `hasTable`.
- `role`: cover, agenda, section, content or closing (a heuristic guess; `roleReason` says why).
- `contentType`: refines content slides: text, columns, grid, big-numbers, image-text, chart, table, process, quote.
- `title`: the guessed slide title.
- `slots`: every text-bearing shape (groups and table cells included). Each slot has:
  - `id`: `s<slide>:<shape id path>`, for example `s4:6`, `s6:18/2` for a group member, `s7:12@2,3` for table row 2, column 3.
  - `name`, `placeholder`, `sample` (the current text), `paragraphs`, `bounds` (inches), `fontPt`, `fontSizes`, `font`, `role` (such as title or running-label).
  - `capacity`: `charsPerLine`, `lines`, `chars` (estimate at the current font size) and `softChars` (about 20 percent headroom, never below the sample text).
  - `editable` (and `editableReason` when false): page numbers, dates, tiny text and locked shapes are not editable.
  - `persistent`: a running header or footer label that repeats on most slides and is kept when unfilled.
- `pictures`: picture slots with an `id`, `bounds`, pixel size, `role` (photo, logo, icon, background) and `replaceable`. Logos and full-bleed backgrounds are not replaceable.

Render the template too (`render.py --grid`) and look at it: the profile tells you the structure, the picture tells you whether a slide suits your content.

## Choosing slides per role

1. Plan the storyline first (see `workflow.md`): one core message per slide.
2. For each planned slide choose a template slide whose `role` and `contentType` fit: cover for the first, agenda for the outline, section for dividers, a content slide matching the content (big-numbers for KPIs, chart for a chart, columns for comparisons, image-text for a picture, process for steps, quote for a statement), closing for the last.
3. Match the amount of text to `capacity`. Three bullet points do not belong in a slot that holds 40 characters. Prefer a slide with more room over cramming.
4. A source slide may appear more than once; it is duplicated. Template slides you do not list are dropped.
5. Vary the content slides: do not use the same source slide for more than two consecutive slides.
6. If nothing in the template fits, say so and either choose the nearest slide or offer Mode A with `build_deck.py --template` instead (see below).

## Consistent chapter names

Chapter names appear in several places: the agenda items, the section divider titles and often the content slide headers. Use exactly the same wording and order everywhere. Decide the list of chapter names once, then copy the strings into every slot that needs them. Check at the end by searching `inventory.py` output for each name.

## The edits.json format

```json
{
  "slides": [
    {"source": 1, "slots": {"s1:2": "Quarterly review", "s1:3": ["Line one", "Line two"]}},
    {"source": 5, "slots": {"s5:6": "Heading", "s5:7/2": "text in a group member",
                            "s5:9@2,3": "text in table cell row 2, column 3"},
                   "images": {"s5:4": "photos/team.jpg"},
                   "notes": "Speaker notes for this slide"},
    {"source": 5, "slots": {"s5:6": "A second copy of template slide 5"}}
  ]
}
```

- `slides` is the output deck in order. `source` is the 1-based template slide number.
- `slots` maps slot ids from the profile to new text. A value is a string (`\n` separates paragraphs) or a list of paragraph strings. A bare path such as `6` or `7/2` is accepted too. Only slots with `editable: true` can be filled.
- `images` maps a picture slot id to an image file path. The picture replaces the old one and keeps the frame; it is cropped, never stretched. Pictures shared with other slides are not modified.
- `notes` sets the speaker notes of that slide. Write notes for every slide.
- Position, size, colour, font and paragraph formatting stay. The first run's formatting is used for every paragraph.

## Capacity, warnings and what is never done

- The tool never shortens text and never adds "...". A slot whose new text is above its `softChars` gets a warning; the text stays in full. Fix it by rewriting shorter yourself or choosing another slide.
- Editable slots you do not fill have their sample text cleared (an unfilled placeholder shape is removed), with a warning. Fill every slot you use, or choose a slide with fewer slots.
- Persistent running labels are kept. Static page numbers that match their template position are renumbered to the new position; pass `--no-renumber` to keep them as they were. If the user does not want page numbers, say that they come from the template and are outside this tool's text-only scope, or remove them with a raw XML edit (see `editing.md`).
- Options: `--profile` reuses a saved profile (otherwise it is computed on the fly), `--dry-run` does everything except write the file, `--strict` turns warnings into exit status 1. Exit codes: 0 ok, 1 invalid edits or the output fails validation (or warnings with `--strict`), 2 unreadable input.
- The output is checked with the `ooxml.py` validator automatically.

## Image slots

Use the template's picture slots for photos: supply a file with enough pixels for the frame (see the slot's pixel size), prefer the same aspect ratio to limit cropping, and use each image once. Logos and background pictures are not replaceable through this tool. After filling, check in the render that faces and subjects are not cropped.

## QA for template decks

`qa_check.py deck.pptx --template template.pptx` also treats sentences copied verbatim from the template as leftover sample text. Typical fixes: fill the missing slot, delete a leftover shape through raw XML, or change the source slide. Slide numbers and footers inherited from the template are errors unless `--allow-footers` is passed; if the user wants them, pass the flag. Render and look at every slide: placeholder-like text, long strings that overflow, and pictures with the wrong crop are the usual problems. Maximum 2 revision rounds, then deliver and list what is left.

## `build_deck.py --template` versus `fill_template.py`

| Need | Tool |
|---|---|
| The deck must reuse specific, finished template slides (cover art, designed content pages) and swap the words | `fill_template.py` |
| The user wants the company's fonts, colours and masters, but the slides can be built fresh from a spec | `build_deck.py deck-spec.json --template company.pptx -o deck.pptx` |

`build_deck.py --template` keeps the template's masters, layouts, theme fonts and colours, removes the template's slides and builds new slides from the spec on its blank layout (pass `--theme` only if you want a skill theme to override the template's look). It does not fill the template's existing slides. `fill_template.py` does exactly that and nothing else.
