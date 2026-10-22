# Workflow details

Companion to `SKILL.md`. Covers intake, storyline, writing the spec, the QA loop and delivery.

## 1. Intake

Send the questions together in one message and wait. Offer a default for each so the user can answer "defaults are fine".

| # | Question | Default if the user delegates |
|---|---|---|
| 1 | What is the deck for, and what should the audience know, decide or do afterwards? | Infer from the brief; state it as the deck goal |
| 2 | Who is the audience (role, seniority, prior knowledge)? | Informed non-specialists |
| 3 | How long is the talk, or how many slides? | 8 to 12 slides, about 15 minutes |
| 4 | What material exists (text, numbers, images) and how final is it? | Use what was given; mark gaps instead of inventing |
| 5 | Delivered live or read alone? | Live: `speaker-led` |
| 6 | Images or media to include? | None; use shapes, numbers and charts |
| 7 | Theme preference or mood? | Show three previews |
| 8 | Hard constraints (brand colours, fonts, language, mandatory sections, template)? | None |

Pacing: slide count is about duration in minutes divided by 1.5. A 15 minute talk is about 10 slides; 30 minutes is about 20. The validator warns when the count is more than 30 percent away from `durationMinutes / 1.5`. Set `durationMinutes` in the spec so this check works.

Density: `speaker-led` means the speaker carries the detail, slides hold at most 3 items; `reading-first` is for decks that are sent ahead and may hold up to 8 items per slide. Set `density` in the spec to match.

Language: write all slide text and notes in the user's language. Set `language` to its BCP 47 tag (`en`, `nb`, `de`, ...). Theme fonts must support the script; if unsure, check the render.

When the user delegates everything: pick the values from the defaults column, tell them in one short paragraph what you assumed, and continue. Do not stall. Still show style previews unless the user clearly said not to.

## 2. Storyline

Decide the arc before writing slides. Five stages, each can take one or more slides:

1. hook: why the audience should care now (the cover and an opening claim or number).
2. context: the situation, the problem or what happened.
3. core: the main evidence or the solution, one idea per slide.
4. shift: what changes because of it (a decision, risk, comparison with alternatives).
5. takeaway: what to do next and the one thing to remember (actions, result, closing).

Set `arcStage` on each slide. Then draft the outline as a list of one-sentence core messages, one per slide, in order. Check the list:

- Read only the sentences aloud: do they tell the whole story?
- First slide `cover`, last `closing`, one of each.
- For 8 or more slides, add a `breakdown` agenda after the cover and `transition` dividers between parts. Use the same chapter names in the agenda, the dividers and the titles.
- Alternate dense and light slides; put an `observation` after a data slide to say what it means.
- Pick a role per slide from `layout-roles.md`: numbers go to `metrics` or `result`, change over time to `trend`, a choice to `comparison`, a method to `process`, commitments to `actions`.
- Every claim has support in the material. Where there is none, cut the slide or flag it.

Show the outline to the user for decks over about 6 slides or when the goal is unclear; otherwise continue.

## 3. Choosing the theme

Run `preview_styles.py` with `--auto 3` (contrasting auto-pickable themes) or `--themes a,b,c` for explicit picks. It writes `style-a.pptx`, `style-b.pptx`, `style-c.pptx` (cover plus one content slide, no theme names on the slides) and prints which theme each letter is. Render each to PNG with `render.py`, look at the images, and show the user the three options by letter and theme name. Record the choice in `theme` and make `randomSeed` start with that theme id: `<themeId>-<YYYYMMDD>-<three lowercase letters>`, for example `growth-surge-20261022-qzx`. Family guidance is in `themes.md`.

## 4. Writing the deck spec

The spec is a JSON file validated by `deck-spec.schema.json`. Keys at the top: `schemaVersion` (1), `title`, `goal`, `audience`, `language`, `randomSeed`, `theme`, `slides`; optional `owner`, `aspect` (`16:9` default or `4:3`), `density`, `durationMinutes`, `mode`, `template`.

Per slide: `id` (lowercase letters, digits, hyphens), `role`, `coreMessage`, `title`; optional `summary`, `items`, `chart`, `media`, `notes`, `layoutVariant`, `arcStage`.

Text fields (`title`, `summary`, item `detail`) are objects `{ "full": "...", "short": "..." }`. The builder uses `full` when it fits at the minimum font size and `short` otherwise. `short` must be at most 60 percent of the role's character limit for that field, so write it as a genuinely tighter version, not a cut-off. Limits per role are in `layout-roles.md` (and `x-roleLimits` in the schema). Item `label` is a plain string.

Rules that save a revision round:

- Titles state the takeaway: "Revenue grew every quarter", not "Revenue".
- `coreMessage` is the one sentence you want remembered; it also becomes the notes if notes are missing, so still write real notes.
- Notes: two to five sentences, what to say, which number to stress, how to hand over to the next slide.
- Numbers: put the number in `value`, the text shown in `displayValue`, a unit in `unit`. A `priority` of 1 marks the hero item.
- Count items against the role maximum and the density cap before validating.
- Leave `layoutVariant` out to get seeded variety; set it when two neighbours look alike.
- Image paths are relative to the spec file and must exist; every image `alt` text is required.
- Chart: `type` (`bar`, `column`, `line`, `pie`, `doughnut`, `stacked_bar`), `categories`, `series[{name, values}]` with as many values as categories, and an `insight` sentence that the data supports.

### Worked mini example

A 5-minute lightning talk, 3 slides. The shape of a valid spec:

```json
{
  "schemaVersion": 1,
  "title": "Support Response Times",
  "goal": "Get approval to add one weekend support shift",
  "audience": "Operations leadership",
  "language": "en",
  "randomSeed": "research-white-20261022-abc",
  "theme": "research-white",
  "density": "speaker-led",
  "durationMinutes": 5,
  "slides": [
    {
      "id": "cover", "role": "cover", "arcStage": "hook",
      "coreMessage": "Weekend delays cost us customers, and one shift fixes it.",
      "title": {"full": "Faster answers on weekends", "short": "Faster weekends"},
      "summary": {"full": "A proposal for one extra support shift", "short": "One extra shift"},
      "notes": "State the ask in the first sentence: one extra weekend shift."
    },
    {
      "id": "gap", "role": "metrics", "arcStage": "core",
      "coreMessage": "Weekend replies take four times longer than weekday replies.",
      "title": {"full": "Weekend replies take 4x longer", "short": "Weekends 4x slower"},
      "items": [
        {"id": "wd", "label": "Weekday", "value": 3, "displayValue": "3 h", "priority": 2,
         "detail": {"full": "Median first reply", "short": "Median"}},
        {"id": "we", "label": "Weekend", "value": 12, "displayValue": "12 h", "priority": 1,
         "detail": {"full": "Median first reply", "short": "Median"}}
      ],
      "notes": "Stress the 12 hours. Source: helpdesk export, last quarter."
    },
    {
      "id": "close", "role": "closing", "arcStage": "takeaway",
      "coreMessage": "Approve one shift to cut weekend replies to 4 hours.",
      "title": {"full": "Approve one weekend shift", "short": "Approve one shift"},
      "summary": {"full": "Decision needed this month", "short": "Decide this month"},
      "notes": "Ask for the decision. Offer to share the staffing plan."
    }
  ]
}
```

A full-size example is `examples/annual-review.json` and `examples/product-launch.json` in this folder. Copy their structure rather than writing from nothing.

## 5. The QA loop

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/validate_spec.py deck-spec.json
python3 ${CLAUDE_SKILL_DIR}/scripts/build_deck.py deck-spec.json -o deck.pptx
python3 ${CLAUDE_SKILL_DIR}/scripts/render.py deck.pptx -o deck-work/render --grid --dpi 110
python3 ${CLAUDE_SKILL_DIR}/scripts/qa_check.py deck.pptx --spec deck-spec.json
```

Status meanings (`qa_check.py` prints `{status, issues}`; exit 0, 1, 2):

- pass (exit 0): no error-level issues; warnings may remain and should be mentioned.
- revise (exit 1): at least one error. Fix and run another round.
- blocked (exit 2): the package is invalid or unreadable. Rebuild from the spec; for an edited file, run `ooxml.py validate` and fix the structure.

Issue codes and the usual fix:

| Code | Meaning | Fix |
|---|---|---|
| off-slide | A shape sticks out of the slide | Split the slide or change the variant |
| text-overflow | Text needs more height than its box | Use the `short` text, cut words, or split the slide |
| font-too-small | Below 18 pt body, 12 pt caption, 28 pt title | Split the slide; never lower the size |
| leftover-placeholder | Empty placeholder, "Click to add", lorem, TODO, bracketed prompts | Fill or delete the shape |
| slide-number-field, date-field, footer-placeholder | Page number, date or footer present | Remove, unless the user asked (`--allow-footers`) |
| too-many-fonts | More than 3 font families | Use one theme font set |
| font-missing | A font is not installed here | Informational; the fallback is used |
| image-reused | The same image appears on several slides | Use each image once, or use a different one |
| no-notes | A slide has no speaker notes | Add notes |
| low-contrast | Text colour against its background is under 4.5:1 (3:1 for large text) | Change theme or the element |
| layout-repeat | Same layout on more than 2 consecutive slides | Change `layoutVariant` or the role |
| slide-count | With `--spec`: the slide count differs from the spec | Rebuild; check for a failed build |
| title-missing | With `--spec`: a slide title was not found | Check the spec title and the render |

Reading the renders: open `grid.png` to judge rhythm, balance and repetition across the deck; then open single slides (`slide-01.png`, ...) that look crowded, empty or off. Look for clipped or overlapping text, text touching edges, unbalanced halves, a missing image, low-contrast text, and slides that look the same as their neighbours. LibreOffice may substitute fonts, so judge spacing roughly, not by pixel.

Revision rounds: at most 2. Each round list the problems (from `qa_check` and from the PNGs), change the spec in one pass, rebuild, re-render and re-check. After round 2, stop and deliver with the remaining items stated honestly.

## 6. Delivery checklist

- [ ] Deck file exists and opens: `ooxml.py validate deck.pptx` exits 0.
- [ ] `qa_check.py` status is pass, or the remaining issues are listed.
- [ ] Slide count matches the plan (about duration / 1.5).
- [ ] Every slide has a takeaway title and speaker notes.
- [ ] No page numbers, placeholders, "..." truncations or invented facts.
- [ ] Chart insights match the numbers; each image appears once.
- [ ] Theme was chosen by the user or, if delegated, stated as an assumption.
- [ ] Final message gives the output path, a short summary, QA status and assumptions.
