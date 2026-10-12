# slides: .pptx, .potx

A `.pptx` is a ZIP of XML parts: `ppt/presentation.xml` (slide order and size), `ppt/slides/slideN.xml`, `ppt/slideLayouts/`, `ppt/slideMasters/`, `ppt/notesSlides/`, charts, media, and theme. Layouts and the master carry the design; slides should use them rather than redraw it.

## Choose the approach

| Task | Approach |
|---|---|
| Read a deck, list titles, extract notes | `python3 scripts/inspect_office.py FILE --text` |
| Create a new deck | `python-pptx` (Python) or `pptxgenjs` (Node) |
| Build from the user's template | `python-pptx`: open the template, add slides from its layouts, fill placeholders |
| Edit text/images in an existing deck | `python-pptx`; edit runs to keep formatting |
| Reorder, duplicate, delete slides; anything the library lacks | Unpack, edit XML, repack (`scripts/ooxml_pack.py`) |
| Look at the result | `python3 scripts/render.py FILE --montage` |

Run `python3 scripts/doctor.py` first.

## Plan the deck before touching a tool

1. **Audience, purpose, length.** Who is in the room (or reading alone), what should they decide or remember, how long do you have? Rule of thumb: one slide per minute or fewer; fewer for discussion.
2. **The story in sentences.** Write the slide titles as a sequence of full sentences that, read alone, tell the argument. If the titles do not make sense on their own, the deck will not either.
3. **One message per slide.** A slide that makes two points is two slides.
4. **Pick the shape** (adapt as needed):
   - *Decision deck:* situation, problem, options, recommendation, cost/risk, ask, next steps.
   - *Status update:* headline, progress vs plan, risks, decisions needed, next period.
   - *Pitch:* problem, solution, why now, market, product, traction, model, team, ask.
   - *Teaching:* goal, concept, example, practice, summary.
5. **Show the user the outline** for anything longer than a handful of slides, and wait for a yes before building.

## Design rules that survive any template

- **Titles state the takeaway** ("Onboarding takes 9 days; peers take 3"), not the topic ("Onboarding").
- **Text is short.** Aim for at most about six lines and a dozen words per line. Move detail to speaker notes or an appendix slide.
- **Size.** Body text at 18 pt or larger when presented; nothing under 12 pt anywhere. If text will not fit, cut words, not font size.
- **Contrast and colour.** Dark text on light, or the reverse, with strong contrast; one primary colour, one accent, neutrals. Do not use colour as the only signal.
- **Alignment and space.** Use the layout's margins; align to a grid; leave white space. Left-align body text.
- **One visual idea.** A chart, a diagram, a photo, or a big number per slide, large enough to read from the back.
- **Charts:** native charts where possible (editable, accessible), title or takeaway headline, labelled axes and units, direct labels over legends, no 3D, start bars at zero, highlight the series that matters and grey the rest.
- **Consistency:** same fonts, sizes, positions for the same kind of element on every slide.
- **Images:** real, relevant, high resolution; add alt text. Do not stretch; crop instead.
- **Speaker notes:** for each content slide, what to say, in a few lines. Notes are not on-slide text.
- **Accessibility:** a unique title on every slide, logical reading order (the order of shapes in the file), alt text on images and charts, no information only in colour.

## python-pptx essentials

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE

prs = Presentation()                              # or Presentation("template.pptx")
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)   # 16:9; the default template is 4:3

layout = prs.slide_layouts[5]                     # "Title Only" in the default template; check names in your template
s = prs.slides.add_slide(layout)
s.shapes.title.text = "Onboarding takes 9 days; peers take 3"

cd = CategoryChartData()
cd.categories = ["Us", "Peer A", "Peer B"]
cd.add_series("Days to onboard", (9, 3, 4))
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.8), Inches(1.6), Inches(11.5), Inches(5), cd)
gf.chart.has_legend = False

s.notes_slide.notes_text_frame.text = "Walk through the gap; ask about causes."
prs.save("deck-v1.pptx")
```

Footguns:

- **Layouts are by index and differ per template.** List `[l.name for l in prs.slide_layouts]` and pick by name. Use placeholders (`slide.placeholders`) so the template's formatting applies.
- **Changing slide size after building does not rescale content.** Set it before adding slides, or rebuild.
- **Text does not auto-shrink in the file.** The library cannot measure text; overflow only shows when rendered. Set explicit sizes, keep text short, and check the render.
- **Edit runs, not text frames.** `text_frame.text = ...` resets formatting. Change `run.text` to keep fonts and colours.
- **Replacing text across runs:** a phrase may span runs; join, replace in the first, blank the others (same issue as in Word).
- **Deleting or reordering slides** has no public API. Reorder by moving `<p:sldId>` elements inside `<p:sldIdLst>` in `ppt/presentation.xml`. To delete, remove the `sldId` and drop the relationship, then repack: orphaned slide parts increase file size and can raise repair prompts in PowerPoint.
- **Cloning a slide** copies shapes but not images or chart parts' relationships automatically. Prefer building new slides from layouts.
- **Tables:** `shapes.add_table(rows, cols, x, y, cx, cy)`; set column widths, font sizes per cell, and keep to a few columns.
- **Images:** `shapes.add_picture(path, x, y, width=...)`; give only the width or only the height to keep the aspect ratio. Alt text needs the XML `descr` attribute on `<p:cNvPr>`.
- **Fonts:** only fonts on the viewer's machine render; use the template's theme fonts.

### pptxgenjs essentials

If Node is the available tool: set the layout (`pres.layout = "LAYOUT_WIDE"` for 13.33 x 7.5 in; the default 16:9 canvas is 10 x 5.625 in), and remember positions beyond the canvas are written but invisible. Colours are six-digit hex without `#`. Do not share one options object across several `add*` calls (it is modified in place). Use `bullet: true` for lists rather than typed bullets, `addNotes()` for speaker notes, and `addChart()` for native charts. One `pptxgen` instance per output file.

## Editing an existing deck

1. `python3 scripts/inspect_office.py FILE --text`: slide titles, layouts, notes, pictures missing alt text, hidden slides.
2. Work on a copy; keep the template's layouts, theme, and master untouched.
3. Make the requested changes only. If text grows, check for overflow and resize or trim; do not shrink fonts below the template's sizes.
4. `python3 scripts/render.py OUT.pptx --montage`, then look at each slide.

## Design and visual QA

Read [../design/GUIDE.md](../design/GUIDE.md) and [../design/data-display.md](../design/data-display.md). `python3 assets/starters/pptx_starter.py out.pptx --preset business-modern` builds a 16:9 deck from a preset (title at a fixed position, 24 pt body, safe margins, notes, native chart with alt text): copy `new_deck`, `add_title`, `add_bullets`, `add_chart_slide`, `set_alt`. The `deck-dark` preset is for screens only. Slide-specific checks:

- Title in the same place on every slide; one idea per slide; body 24 pt, nothing under 12 pt, content inside a 0.5 in safe area.
- At most about 50 words per slide; the audit warns above 60 and errors above 90.
- No bullets nested three levels deep; split the slide or use a table.
- Chart title states the takeaway; native chart with alt text; palette from the preset.
- Text on images sits on a solid panel or scrim; every picture has alt text.
- Measure: `python3 scripts/design_audit.py OUT.pptx` (font sizes, off-slide and overlapping shapes, density, contrast where colours are explicit, missing titles and alt text), then `scripts/render.py OUT.pptx --montage` and look at every slide.

## Verify

1. Render every slide and look for: text running off the slide or out of its box, overlapping shapes, tiny text, cropped or stretched images, low contrast, empty placeholders ("Click to add title" shows in the editor even when hidden in the show).
2. `inspect_office.py`: every slide has a title, notes exist where promised, no unexpected hidden slides, pictures have alt text.
3. Numbers on slides agree with the source data and with each other.
4. Say that the preview is LibreOffice, not PowerPoint: fonts, spacing and some effects can differ; animations and transitions are not previewed.

## Before sharing

Speaker notes, comments, hidden slides, author and company in properties, embedded workbooks behind charts (they hold the full data), and file size. Report each; remove only with the user's agreement. For external distribution a PDF export (`../pdf/GUIDE.md`) drops notes and embedded data.
