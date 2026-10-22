# Design rules

The numbers here mirror the `x-typography`, `x-densityLimits` and `x-roleLimits` blocks of `deck-spec.schema.json`. If they ever differ, the schema wins.

## Type scale and minimums

| Element | Minimum | Notes |
|---|---|---|
| Title | 28 pt | A sentence stating the takeaway, at most 2 lines |
| Body | 18 pt | Paragraphs and list text |
| Caption | 12 pt | Source lines, chart labels, small labels only |
| Hero number | at least 2.5 times body (45 pt at body 18) | KPI values, the result number |

- Never shrink text below these sizes to make it fit. Use the `short` text, cut words, or split the slide.
- Text over 90 characters is treated as body text by the QA check, so a long sentence at 14 pt is an error.
- Use at most 3 font families. Themes define heading, body and mono fonts; do not add others.
- Left-align paragraphs. Keep lines under about 60 characters on wide boxes by splitting into columns.

## Margins and grid

- Canvas 13.333 x 7.5 in for 16:9 (4:3 is narrower). Keep a 0.6 in outer margin; nothing text-bearing leaves it.
- Align everything to the same left edge and a column grid; use one gap size inside a slide.
- White space is a layout element. A slide that is 60 percent filled usually reads better than one that is 95 percent filled.
- Do not stack more than three levels of hierarchy (title, heading, body).

## Density modes

| Mode | Use when | Items per list-like slide |
|---|---|---|
| speaker-led | A person presents and talks over the slide | at most 3 |
| reading-first | The deck is sent ahead or read alone | at most 8 |

The effective cap is the smaller of the density cap and the role's `maxItems` (for example `risks` is 5, `context` is 4, `case` is 4). It applies to these roles: breakdown, context, metrics, trend, comparison, distribution, relationship, case, process, risks, observation, actions, team. If a slide exceeds the cap, split it into two slides; do not shrink. Validation fails with an error otherwise.

One message per slide: if a slide needs "and" in its title, it is probably two slides.

## Colour

- One palette per deck, taken from the theme. Use the `primary` for structure, the `accent` for the single thing to look at, `mutedText` for secondary text.
- Accent on at most one or two elements per slide.
- Themes with `accentTextAllowed: false` (swiss-yellow, swiss-lime, swiss-orange) use the accent only as fill: blocks, bars, rules, large shapes. Text on the paper background uses the theme text colour.
- Keep contrast at 4.5:1 for text (3:1 for large text). The QA check warns below that.
- Use chart series colours from the theme in order; do not colour every bar differently when one category is the point (highlight one, mute the rest).
- Dark themes suit dim rooms and projectors; light themes suit print and laptops.

## Images

- Use real photos, screenshots or data visuals. Avoid generic stock imagery.
- Aspect ratios: full-bleed 16:9 (1920 x 1080 or larger); half-slide about 4:5 or 1:1; avatars 1:1. `fit: "cover"` crops to fill; `fit: "contain"` shows the whole image.
- Resolution: at least 150 dpi at the size shown (about 1600 px wide for a half slide, 2000 px for full bleed). Smaller images look soft in a projected deck.
- Each image is used once in the deck; the QA check flags reuse. Logos and small marks may repeat.
- Always write meaningful `alt` text (it is required).
- Respect the theme's `imageTreatment` (natural, grayscale or duotone).
- No text baked into images; keep the text live so it can be edited.

## Charts

- Prefer a native chart (`bar`, `column`, `line`, `pie`, `doughnut`, `stacked_bar`) over a picture, so it stays editable.
- One chart, one point. The `insight` sentence is the title of the chart in words: "Revenue grew every quarter". Any number quoted in it must match the series values; the validator checks.
- Use line for change over time, bars for comparing categories, pie or doughnut only for 2 to 5 parts of a whole.
- `series[i].values` must have as many entries as `categories`.
- Do not clutter: no 3D, no more than 6 series, direct labels where possible.
- Put the source in notes or a caption of at least 12 pt.

## Layout variety

- Do not use the same role with the same layout variant on more than 2 consecutive slides (validator warning, x-sameRoleRun). Change the variant or the role to break a run.
- Alternate dense slides (comparison, process, risks) with light ones (statement, result, ambient, image).
- Use `transition` between parts of an 8+ slide deck, `ambient` as a breather.
- Leave `layoutVariant` unset for seeded variety, or set it explicitly where two slides still feel alike.
- The look is consistent through the theme: same fonts, same palette, same title position; the layout varies, the style does not.

## Avoid list (anti-generic design)

- Heading fonts like Inter, Roboto or Arial used as the signature; default indigo `#6366f1` and purple-on-white gradients.
- Everything centred; prefer a left-anchored, asymmetric composition.
- The same card grid on every slide; icons in circles above every heading.
- Glow, glass, blur or drop shadows that carry no meaning.
- Stock illustrations of people at laptops; emoji used as icons.
- Titles that are labels ("Overview", "Results") instead of statements.
- Bullets that are full sentences copied from a document.
- A closing slide that only says "Thank you" with nothing to do next.
- Footers, page numbers and logos on every slide unless asked.

## Choosing a theme family

Details and the full table are in `themes.md`; the data is in `themes.json`.

| Family | Pick when |
|---|---|
| signature (12) | The audience or industry is the main signal: developers, consumers, analysts, premium, events |
| editorial (5) | Narrative, reading-heavy decks, essays, letters; serif headings, thin rules, no shadows |
| swiss (4) | Design, systems and research talks; flat grid, one hard accent (fill-only for yellow, lime, orange) |
| bold (6) | Keynotes, launches and campaigns where impact matters more than density |

Rules: one theme per deck; chart-heavy decks use `spectrum-report`, `atlas-dark` or `growth-surge`; never auto-pick `ledger-gold` (explicit request only); for finance topics without that request use `spectrum-report` or `research-white`.
