# design: visual principles for every document type

Applies to Word pages, PDFs, slides, spreadsheets, and shareable docs. Read this before building anything the reader will *look at*, and again for the Visual QA pass. Numbers below are defaults to measure against, not laws: a user's brand, template, or explicit request overrides them.

## The method

1. **Start from the reader and medium.** Printed A4/Letter, read on a laptop, projected in a room, or skimmed on a phone? That sets sizes, density, and colour.
2. **Pick a preset or adopt theirs.** `assets/design-tokens.json` has four presets (`report-classic`, `business-modern`, `minimal`, `deck-dark`) with fonts, colours, type scales, spacing, margins, table style, and a chart palette. If the user gave a brand guide or template, take fonts, colours, and margins from it and keep these tokens only for what it leaves open.
3. **Set the system once, then fill it in.** Define styles (Word), the theme and layouts (slides), cell styles (sheets), or a style sheet (PDF code). Never format element by element.
4. **Build, render, look.** `python3 scripts/render.py OUT --montage`, then `python3 scripts/design_audit.py OUT`. Fix, repeat.

Run `python3 scripts/contrast.py --tokens` to see every preset's colour pairs pass WCAG AA.

## Hierarchy: what the eye reads first

- One focal point per page or slide. Make the most important thing the biggest, boldest, or highest-contrast, and make everything else visibly less.
- Use at most **three visible levels** of emphasis on a page (title, heading, body, with captions and footers as quiet extras). More levels read as noise.
- Signal level with *size and weight first*, colour second, position third. Colour alone is not a hierarchy (greyscale test, below).
- Group by **proximity**: space between groups larger than space inside them (at least 2x). Rules and boxes are a last resort; whitespace does the job.

## Typography

| Property | Default | Why |
|---|---|---|
| Families | One family, or one serif plus one sans. Never more than two, plus mono for code | Fewer faces look deliberate |
| Scale | Pick sizes from the preset (`type.document`, `type.slide`, `type.sheet`); steps of roughly 1.2-1.33x | A scale makes hierarchy obvious |
| Body, print/screen document | 10.5-12 pt | Below 10 pt is hard to read in long text |
| Body, slides | 24 pt, never below 18 pt for content, never below 12 pt for anything | Back-row readability |
| Line length | 45-75 characters per line (about 6-12 words); in two-column layouts 35-50 | Longer lines lose the reader on the return sweep |
| Line height | 1.4-1.6 for body, 1.1-1.25 for headings and slide text | Tight headings, airy body |
| Alignment | Left-aligned, ragged right. Justify only with hyphenation on and wide columns | Justified text without hyphenation makes rivers |
| Weight | Regular and bold. Use italics for titles and terms, not for emphasis blocks | Light weights fail on projectors and low-resolution screens |
| Case | Sentence case for headings; ALL CAPS only for short labels (under ~25 characters) with extra letter-spacing | Capitals slow reading |
| Numbers | In tables use right alignment and, where available, tabular (fixed-width) figures | Digits line up |

Font practicalities: the reader needs the font. Prefer the preset's widely installed faces, name a fallback, and say so when a custom font is used. In PDFs, embed fonts. After rendering on a machine without the font, the layout may shift: check.

## Space and layout

- **Spacing scale** from the preset (`space.scale`, multiples of 4): use only those values for gaps, padding, and paragraph spacing. Consistent gaps are what make a layout look designed.
- **Margins:** print 20-30 mm (0.8-1.2 in); never under 12 mm. Slides: keep content inside a safe area of at least 0.5 in from every edge.
- **Grid:** pick a column grid (12 columns for slides and dashboards, 1-2 for documents) and snap every block to it. Left edges align; so do baselines of neighbouring text.
- **Whitespace is content.** If a page is more than about 60% filled, cut or split. Do not shrink type to make things fit.
- **Alignment:** one dominant alignment per page. Mixed centre/left/right text is the commonest tell of amateur layout.
- **Repetition:** the same element sits in the same place on every page or slide (title, page number, logo).
- **Orphans and widows:** headings stay with the next paragraph (keep-with-next); no single line stranded at a page top or bottom; no table row split across pages unless unavoidable.

## Colour

- **Palette:** neutrals for 90% (text, surface, rules), one primary, one accent. Semantic colours (success, warning, danger) only when they carry meaning.
- **Contrast (WCAG AA):** text 4.5:1 against its background; large text (18 pt, or 14 pt bold) and meaningful graphics (chart lines, icons, borders that carry meaning) 3:1. Check with `python3 scripts/contrast.py FG BG --size 11`. Text on images needs a scrim or solid panel behind it.
- **Never colour alone.** Add a label, pattern, icon, or position. Test in greyscale: if distinctions vanish, they depend on colour.
- **Colour-blind safety:** avoid red/green as the only pair; use the preset's chart palette, which varies in lightness as well as hue.
- **Dark backgrounds:** off-white text rather than pure white, slightly larger sizes, avoid pure black grounds. Not for print.
- **Print:** screens are brighter than paper. Pale tints under 8% may vanish; check a greyscale render. Large dark fills use a lot of toner and bleed.

## Tables and charts

Full rules and recipes: [data-display.md](data-display.md). The short version:

- Table: header row styled and repeated, numbers right-aligned with consistent decimals and units in the header, light horizontal rules instead of full grids, no more than about seven columns, totals set apart by a top rule.
- Chart: the title says the conclusion; bars start at zero; label directly instead of using a legend when you can; at most five series; same colour for the same thing across all charts; no 3D, no decorative gradients; native, editable charts beat pictures.

## Imagery and graphics

- Resolution: at least 150 ppi at final print size (300 ppi for print-ready), at least 1920 px wide for a full-bleed slide image.
- **Crop, never stretch.** Keep aspect ratio. Keep a consistent style (all photos or all illustrations, one icon set).
- Every informative image has alt text; decorative images are marked decorative.
- Logos: use the supplied file, with clear space around it of at least the logo's cap height; never recolour or distort.
- Prefer one strong image to several weak ones. Remove clip art, drop shadows, bevels, and WordArt-style effects.

## Applying it by format

| Format | Do this |
|---|---|
| **Word / docs** | Define Title, Heading 1-3, Normal, Caption, List styles from the preset; page size and margins in section settings; header/footer with page numbers; heading keep-with-next on; tables styled once. See [../word/GUIDE.md](../word/GUIDE.md) |
| **PDF** | Choose page size deliberately; embed fonts; leave 12 mm minimum margins (3 mm bleed and crop marks only if a printer asks); tagged PDF from a properly styled source. See [../pdf/GUIDE.md](../pdf/GUIDE.md) |
| **Slides** | 16:9, layouts and theme carry fonts/colours, title in the same place on every slide, one idea per slide, body 24 pt, safe area 0.5 in, native charts. See [../slides/GUIDE.md](../slides/GUIDE.md) |
| **Spreadsheets** | Title row, styled header, frozen panes, column widths fitted to content, one number format per column, gridlines off on presentation sheets, fills only for inputs and headers, print area and orientation set. See [../spreadsheets/GUIDE.md](../spreadsheets/GUIDE.md) |
| **Shareable docs** | Strong first screen (title, status, summary); headings as claims; short paragraphs; tables over dense prose for comparisons. See [../docs/GUIDE.md](../docs/GUIDE.md) |

## Visual QA

Run after every render. Each check is also something you can report.

1. **Squint test:** blur your eyes (or view the thumbnail from `render.py --montage`). Is the hierarchy still clear? Is there one focal point per page?
2. **Greyscale test:** does meaning survive without colour?
3. **100% zoom test:** read body text at the size a reader will see. Any line over about 80 characters? Any text under the minimum size?
4. **Edge test:** anything touching a margin, clipped, overflowing its box, or overlapping something else?
5. **Consistency test:** flip through; do titles, numbers, logos, and spacing stay put?
6. **Data test:** do numbers in text, tables, and charts agree? Are units and sources present?
7. **Measure:** `python3 scripts/design_audit.py OUT` reports small fonts, too many font families, missing alt text, narrow margins, contrast failures, off-slide or overlapping shapes, text-heavy slides, clipped spreadsheet text, missing PDF fonts.

State plainly what you checked, and that previews come from LibreOffice, not the end user's application.

## Common failures to avoid

Default theme left in place; five fonts; centred paragraphs; text over a busy photo; rainbow charts; pie with eight slices; gridlines on every cell; bold used for everything; all caps headings; tiny footnote-sized body text to "fit it in"; inconsistent bullet styles; decorative clip art; low-contrast grey on white; one slide that is a wall of text; mixing units or decimal places in a column.
