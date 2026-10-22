# Layout roles

Authoritative numeric limits live in `deck-spec.schema.json` under `x-roleLimits`; this file explains intent and variant geometry. Canvas for variant descriptions: 16:9, 13.333 x 7.5 in, 0.6 in outer margin. Text fields are `{full, short}`; `short` is used when `full` does not fit and must be at most 60% of the full limit. `variant` is 1-based: `layoutVariant` if given, else `(hash(randomSeed + ':' + slideIndex) mod variants) + 1`.

## Summary table

| Role | Max items | Title | Summary | Label | Detail | Variants | Chart | Media | Required |
|---|---|---|---|---|---|---|---|---|---|
| cover | 0 | 60 | 140 | 30 | 80 | 3 | no | yes | title, coreMessage |
| statement | 0 | 80 | 200 | 30 | 80 | 2 | no | no | title, coreMessage |
| breakdown | 6 | 60 | 140 | 30 | 80 | 3 | no | no | title, coreMessage, items |
| transition | 0 | 50 | 100 | 30 | 60 | 2 | no | no | title, coreMessage |
| context | 4 | 60 | 200 | 30 | 120 | 3 | no | no | title, coreMessage |
| metrics | 6 | 60 | 140 | 24 | 60 | 3 | yes | no | title, coreMessage, items |
| trend | 7 | 60 | 140 | 24 | 80 | 3 | yes | no | title, coreMessage |
| comparison | 6 | 60 | 140 | 24 | 100 | 3 | yes | no | title, coreMessage |
| distribution | 6 | 60 | 140 | 24 | 80 | 3 | yes | no | title, coreMessage |
| relationship | 6 | 60 | 140 | 24 | 80 | 2 | no | no | title, coreMessage, items |
| case | 4 | 60 | 200 | 30 | 140 | 3 | no | yes | title, coreMessage |
| image | 3 | 60 | 140 | 24 | 80 | 3 | no | yes | title, coreMessage, media |
| process | 6 | 60 | 140 | 24 | 100 | 3 | no | no | title, coreMessage, items |
| risks | 5 | 60 | 140 | 30 | 120 | 2 | no | no | title, coreMessage, items |
| observation | 5 | 60 | 200 | 30 | 140 | 3 | yes | no | title, coreMessage |
| ambient | 0 | 50 | 100 | 30 | 60 | 2 | no | yes | title, coreMessage |
| actions | 6 | 60 | 140 | 30 | 100 | 3 | no | no | title, coreMessage, items |
| result | 4 | 60 | 160 | 30 | 100 | 3 | yes | no | title, coreMessage |
| team | 8 | 50 | 140 | 30 | 80 | 2 | no | yes | title, coreMessage, items |
| closing | 3 | 50 | 140 | 30 | 80 | 2 | no | yes | title, coreMessage |

Character columns are maxChars for the full text. `title` and `coreMessage` are always required; `coreMessage` has no length cap but belongs in notes or the summary, not as extra text on the slide.

## cover

- Purpose: Opening slide that names the deck and sets the frame.
- Use when: Always as slide 1; exactly one per deck.
- Required: title, coreMessage
- Optional: summary, items, notes, media
- Max items: 0
- Variants (3):
  1. Left-aligned title block over a full-height accent band on the right.
  2. Centered title on the background with a thin accent rule; media (if any) as a faint full-bleed backdrop.
  3. Split: title left half, media (cover fit) right half; without media the right half is a primary-colour block.

## statement

- Purpose: One bold claim or thesis stated in large type.
- Use when: To anchor an argument or open a chapter with a single sentence.
- Required: title, coreMessage
- Optional: summary, items, notes
- Max items: 0
- Variants (2):
  1. Giant centered title, summary beneath in muted text.
  2. Left-aligned title with oversized opening quote mark in accent colour and a vertical rule.

## breakdown

- Purpose: Agenda or structure of the deck or topic.
- Use when: Right after the cover, or to map a framework into parts.
- Required: title, coreMessage, items
- Optional: summary, items, notes
- Max items: 6
- Variants (3):
  1. Numbered vertical list, one row per item with large index numbers.
  2. Grid of cards (2 or 3 columns) with index badge, label and detail.
  3. Horizontal band of segments, one column per item, label on top, detail below.

## transition

- Purpose: Section divider between parts of the deck.
- Use when: Between major sections of 8+ slide decks.
- Required: title, coreMessage
- Optional: summary, items, notes
- Max items: 0
- Variants (2):
  1. Full-bleed primary background, big section title left, section number right.
  2. Background colour with centered title and a short accent underline.

## context

- Purpose: Background, situation or problem framing.
- Use when: Early in the deck to explain why the topic matters.
- Required: title, coreMessage
- Optional: summary, items, notes
- Max items: 4
- Variants (3):
  1. Summary paragraph on the left 55%, stacked items as short fact rows on the right.
  2. Top summary band, below it a row of item cards.
  3. Two-column: heading and summary left, large pull-fact (first item) right with remaining items beneath.

## metrics

- Purpose: Key figures shown as KPI tiles, optionally with a supporting chart.
- Use when: To present 2 to 6 headline numbers.
- Required: title, coreMessage, items
- Optional: summary, items, notes, chart
- Max items: 6
- Variants (3):
  1. Row of equal KPI tiles (value large, label below, detail small).
  2. One hero tile on the left (priority 1) and a grid of smaller tiles on the right.
  3. Tiles on the left half, chart on the right half when chart is present; tiles only otherwise.

## trend

- Purpose: Change over time: timeline or time-series chart.
- Use when: To show history, milestones or growth trajectories.
- Required: title, coreMessage
- Optional: summary, items, notes, chart
- Max items: 7
- Variants (3):
  1. Horizontal timeline with markers, label above and detail below alternating.
  2. Large line or column chart with insight callout under the chart.
  3. Vertical timeline on the left, small chart on the right.

## comparison

- Purpose: Side-by-side comparison of options, periods or segments.
- Use when: When the audience must choose or see a contrast.
- Required: title, coreMessage
- Optional: summary, items, notes, chart
- Max items: 6
- Variants (3):
  1. Two columns with header chips, items listed per column (items alternate A/B by index parity).
  2. Table-like grid: one row per item with label, value and detail aligned.
  3. Chart on the left with an insight callout, key differences as items on the right.

## distribution

- Purpose: Shares of a whole, or a funnel of stages.
- Use when: For market share, budget split, conversion funnel.
- Required: title, coreMessage
- Optional: summary, items, notes, chart
- Max items: 6
- Variants (3):
  1. Doughnut or pie chart with legend list of items on the right.
  2. Funnel: stacked bars narrowing top to bottom, one per item.
  3. Horizontal stacked bar across the slide with item legend below.

## relationship

- Purpose: How parts connect: hub and spokes, ecosystem or dependencies.
- Use when: To explain structures, partnerships or system architecture.
- Required: title, coreMessage, items
- Optional: summary, items, notes
- Max items: 6
- Variants (2):
  1. Hub: first item as central circle, other items around it connected by lines.
  2. Left-to-right chain of boxes with arrow connectors.

## case

- Purpose: A single example, customer story or project with outcome.
- Use when: To make an abstract claim concrete.
- Required: title, coreMessage
- Optional: summary, items, notes, media
- Max items: 4
- Variants (3):
  1. Media on the left 40% (if any), challenge/approach/result items stacked on the right.
  2. Quote-style header with summary, items as three columns beneath.
  3. Full-width summary on top, items as horizontal timeline of steps, media as small thumbnail.

## image

- Purpose: Image-led slide with a caption and optional callouts.
- Use when: When a picture or screenshot carries the point.
- Required: title, coreMessage, media
- Optional: summary, items, notes, media
- Max items: 3
- Variants (3):
  1. Full-bleed media with a translucent caption bar at the bottom.
  2. Media on the right 60%, title, summary and items on the left.
  3. Centered framed media (contain fit) with caption beneath and items as side labels.

## process

- Purpose: Ordered steps of a method or workflow.
- Use when: To explain how something is done or how work flows.
- Required: title, coreMessage, items
- Optional: summary, items, notes
- Max items: 6
- Variants (3):
  1. Horizontal chevron row, number badge on each step.
  2. Vertical numbered steps with connecting line, detail on the right of each.
  3. Snaking 2-row path of cards (3 per row) with arrows.

## risks

- Purpose: Risks, issues or constraints with mitigations.
- Use when: Before asking for a decision or commitment.
- Required: title, coreMessage, items
- Optional: summary, items, notes
- Max items: 5
- Variants (2):
  1. Table rows: label, detail (risk and mitigation), priority chip (1 high to 3 low).
  2. Cards sorted by priority, left accent bar coloured by priority.

## observation

- Purpose: Insights, outlook or conclusions drawn from the material.
- Use when: After data slides, to say what it means.
- Required: title, coreMessage
- Optional: summary, items, notes, chart
- Max items: 5
- Variants (3):
  1. Large summary text left, numbered observations right.
  2. Three-column cards, each with label and detail; optional chart strip above.
  3. Single wide callout with the coreMessage and items as bullet list beneath.

## ambient

- Purpose: Visual mood page with minimal text.
- Use when: As a breather between dense slides or to set tone.
- Required: title, coreMessage
- Optional: summary, items, notes, media
- Max items: 0
- Variants (2):
  1. Full-bleed media or gradient with a short title low-left.
  2. Background colour with oversized outline word (title) and small summary line.

## actions

- Purpose: Roadmap or next steps with owners and timing.
- Use when: Near the end, to convert the story into commitments.
- Required: title, coreMessage, items
- Optional: summary, items, notes
- Max items: 6
- Variants (3):
  1. Horizontal roadmap with phases (value/displayValue = date or quarter).
  2. Checklist rows with priority chip and owner in detail.
  3. Three swimlane columns (now, next, later) assigned by priority 1,2,3.

## result

- Purpose: Headline number and takeaways.
- Use when: To land the single most important outcome.
- Required: title, coreMessage
- Optional: summary, items, notes, chart
- Max items: 4
- Variants (3):
  1. One giant number (first item value) with label, takeaways in a column beside it.
  2. Number centered over a band, remaining items in a row beneath.
  3. Number left, chart (if any) right, takeaways under both.

## team

- Purpose: People, roles or partners.
- Use when: To introduce who does the work; label = name, detail = role.
- Required: title, coreMessage, items
- Optional: summary, items, notes, media
- Max items: 8
- Variants (2):
  1. Grid of circular avatars (media by index if provided, else initials) with name and role.
  2. Rows list with name left, role and short bio right.

## closing

- Purpose: Final slide: thanks, contact, call to action.
- Use when: Always as the last slide; exactly one per deck.
- Required: title, coreMessage
- Optional: summary, items, notes, media
- Max items: 3
- Variants (2):
  1. Centered title and contact items on the primary background.
  2. Left title with call-to-action, contact items stacked right.

## Media example

An `image` slide references a file path relative to the spec; the file must exist at build time (the example specs omit media for that reason):

```json
"media": [{"path": "assets/photo.jpg", "kind": "image", "alt": "Team at the product demo", "fit": "cover"}]
```

## Deck-level rules

- First slide is `cover`, last is `closing`, one of each.
- Avoid more than 2 consecutive slides with the same role and layout variant (validator warning, `x-sameRoleRun`); alternate dense and light roles (use `transition` or `ambient` as breathers).
- Chart `insight` must be a statement the data supports; the validator compares quoted numbers to series values.
