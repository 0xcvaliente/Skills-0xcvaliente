---
name: pptx-deck
description: Create, build, design, edit, restyle, convert or fill PowerPoint (.pptx) decks, slides, presentations, pitch decks and templates. Use when the user wants a new deck from a brief or outline, wants to fill their own .pptx template with content, edit or reorder slides of an existing deck, replace text, convert or restyle an old deck into a new theme, or check a deck for overflow, small fonts and leftovers. Handles intake questions, storyline, 27 themes with three style previews, native charts, speaker notes, rendering to PNG and a QA loop. PowerPoint output only.
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/*) Bash(mkdir *) Bash(ls *) Bash(cp *) Read Write Edit
---

# pptx-deck

Build and edit PowerPoint decks with scripts that write native shapes, text boxes and charts (no screenshots of slides). The deliverable is always a `.pptx` file.

## When to use

Use this skill for any request to make, change, restyle, convert or check a `.pptx` deck. Do not use it for Word, Excel, PDF or web slides.

## Prerequisites

- Required: `python3` with python-pptx, lxml and Pillow. Install with `python3 -m pip install --user -r ${CLAUDE_SKILL_DIR}/requirements.txt`. Homebrew Python on macOS may refuse with "externally-managed-environment": add `--break-system-packages`, or create a venv (`python3 -m venv .venv && . .venv/bin/activate`) and install there.
- Optional, for rendering and visual QA: LibreOffice (`brew install --cask libreoffice`) and poppler (`brew install poppler`). Without them `render.py` exits 2 and names the missing tool; say so and fall back to `qa_check.py` alone.
- Run all commands with `python3 ${CLAUDE_SKILL_DIR}/scripts/<name>.py`. Add `--help` to any script for its flags.

## Pick a mode

| The user has | Mode |
|---|---|
| A topic, brief, notes or documents and no deck | A. New deck |
| Their own template `.pptx` and content to put in it | B. Fill a template |
| An existing deck to fix, reorder, update or translate | C. Edit a deck |
| An existing deck to look different or be rebuilt cleanly | D. Convert / restyle |

If the request is ambiguous, ask one question to choose the mode. Work in a scratch folder such as `deck-work/`, and give the final deck a clear name next to the user's files.

## Intake (all modes except small edits)

Ask the questions in one concise message, then wait for the answers. Do not ask them one at a time.

1. Purpose and goal: what should the audience know, decide or do afterwards?
2. Audience: who, how senior, how familiar with the topic?
3. Length: talk duration in minutes or slide count (about 1 slide per 1.5 minutes; default 8 to 12 slides).
4. Source material: do they have text, data, images, or only a topic? Is it final or rough?
5. Density: speaker-led (sparse, 3 items per slide) or reading-first (denser, up to 8 items).
6. Images and media: files to use, or none.
7. Theme preference: a named theme, a mood, or "show me options".
8. Hard constraints: brand colours, fonts, language, template, mandatory sections, deadline.

If the user delegates everything ("just do it"), choose sensible values, then state the assumptions in your first progress note and again at delivery. The deck language follows the user's language unless they ask otherwise. Full question wording and defaults are in `${CLAUDE_SKILL_DIR}/references/workflow.md`.

## Mode A. New deck from scratch

1. Intake (above). Gather source facts; never invent numbers, quotes or names. Ask for missing data or mark the gap openly in your summary.
2. Storyline: write a one-line core message per slide following the arc hook, context, core, shift, takeaway. First slide `cover`, last `closing`. Show the outline to the user when the deck is more than about 6 slides or the goal is unclear. See `${CLAUDE_SKILL_DIR}/references/workflow.md`.
3. Style pick: render three contrasting previews, then let the user choose (never choose silently unless they delegated).

```bash
mkdir -p deck-work
python3 ${CLAUDE_SKILL_DIR}/scripts/preview_styles.py --title "Deck title" --subtitle "Audience or tagline" --auto 3 -o deck-work/styles
for s in a b c; do python3 ${CLAUDE_SKILL_DIR}/scripts/render.py deck-work/styles/style-$s.pptx -o deck-work/styles/$s; done
```

   The script prints which theme each letter is. Look at the PNGs (Read tool) and show them or describe them, then ask which one. To compare specific themes use `--themes id1,id2,id3`. Theme guidance is in `${CLAUDE_SKILL_DIR}/references/themes.md`.
4. Write the spec `deck-spec.json` (format in `${CLAUDE_SKILL_DIR}/references/deck-spec.schema.json`, roles in `${CLAUDE_SKILL_DIR}/references/layout-roles.md`, examples in `${CLAUDE_SKILL_DIR}/references/examples/`). Every slide has `id`, `role`, `coreMessage`, `title`, usually `summary` or `items`, and `notes`. Texts are `{full, short}` pairs.
5. Validate, build, render and check:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/validate_spec.py deck-spec.json
python3 ${CLAUDE_SKILL_DIR}/scripts/build_deck.py deck-spec.json -o deck.pptx
python3 ${CLAUDE_SKILL_DIR}/scripts/render.py deck.pptx -o deck-work/render --grid
python3 ${CLAUDE_SKILL_DIR}/scripts/qa_check.py deck.pptx --spec deck-spec.json
```

6. Inspect `deck-work/render/grid.png` first, then any slide that looks wrong at full size (`slide-01.png`, ...). Combine what you see with the `qa_check` issues.
7. Revise at most 2 rounds: fix the spec (split slides, shorten text, change variants), rebuild, re-render, re-check. If errors remain after round 2, deliver anyway and list what is left.
8. Deliver (see Delivery).

Exit codes: `validate_spec.py` 0 ok, 1 errors, 2 unreadable file. `build_deck.py` 0 built, 1 spec errors (nothing built), 2 bad input. `qa_check.py` 0 pass, 1 revise, 2 blocked.

## Mode B. Fill the user's template

Use when the deck must look exactly like the user's own file. Only text and pictures change; layout, fonts and colours stay. Details: `${CLAUDE_SKILL_DIR}/references/templates.md`.

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/template_profile.py template.pptx -o deck-work/profile.json
python3 ${CLAUDE_SKILL_DIR}/scripts/render.py template.pptx -o deck-work/template-render --grid
# write deck-work/edits.json (slide choice per role + slot text)
python3 ${CLAUDE_SKILL_DIR}/scripts/fill_template.py template.pptx deck-work/edits.json --profile deck-work/profile.json -o deck.pptx
python3 ${CLAUDE_SKILL_DIR}/scripts/ooxml.py validate deck.pptx
python3 ${CLAUDE_SKILL_DIR}/scripts/qa_check.py deck.pptx --template template.pptx
python3 ${CLAUDE_SKILL_DIR}/scripts/render.py deck.pptx -o deck-work/render --grid
```

1. Profile the template and render it so you can see every layout.
2. Run intake and storyline as in Mode A, then pick one template slide per planned slide by page role (cover, agenda, section, content types, closing). A source slide may repeat; unused ones are dropped.
3. Write `edits.json` with slot ids from the profile. Keep chapter names identical across agenda, dividers and titles. Never shorten text to fit and never add "..."; if a slot warns about capacity, rewrite shorter yourself or choose a roomier slide.
4. `fill_template.py` exit codes: 0 ok, 1 invalid edits or output fails validation (or any warning with `--strict`), 2 unreadable input. Revise at most 2 rounds after QA and render.

## Mode C. Edit an existing deck

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/inventory.py deck.pptx -o deck-work/inventory.json
python3 ${CLAUDE_SKILL_DIR}/scripts/replace_text.py deck.pptx deck-work/replacements.json --dry-run
python3 ${CLAUDE_SKILL_DIR}/scripts/replace_text.py deck.pptx deck-work/replacements.json -o deck-edited.pptx
python3 ${CLAUDE_SKILL_DIR}/scripts/rearrange.py deck-edited.pptx --order "1,3,3,2" -o deck-final.pptx
python3 ${CLAUDE_SKILL_DIR}/scripts/ooxml.py validate deck-final.pptx
```

- Text changes: `replace_text.py` (keeps formatting). Slide order, duplicates and deletes: `rearrange.py`. Anything else (run formatting, notes structure, hidden slides): unpack with `ooxml.py unpack`, edit the XML, `ooxml.py pack`, then validate.
- Never overwrite the user's original; write a new file. Always run `ooxml.py validate`, `qa_check.py` and `render.py` after editing, and compare against the original render if the change was visual.
- Recipes, JSON format and pitfalls: `${CLAUDE_SKILL_DIR}/references/editing.md`.

## Mode D. Convert or restyle

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/extract.py old.pptx -o deck-work/extracted --to-spec --theme research-white
```

1. `extract.py` writes `extracted.json`, `assets/` and (with `--to-spec`) a draft `deck-spec.json`. Exit codes: 0 ok, 1 draft spec has validation errors, 2 unreadable input.
2. Review the draft: fix roles, write real `coreMessage` and `notes`, trim wording, split overfull slides, check that images in `assets/` are used once.
3. Offer style previews as in Mode A step 3, set `theme` and a matching `randomSeed`, then `validate_spec.py`, `build_deck.py` (add `--template template.pptx` only to reuse a template's masters), `render.py`, `qa_check.py`.

## Core rules

- One message per slide. The title states the takeaway (a sentence, not a topic label); `coreMessage` records it.
- Split, never shrink. Minimums: body 18 pt, caption 12 pt, title 28 pt, hero numbers at least 2.5 times body. If text does not fit, split the slide or use the `short` text.
- Density caps: speaker-led 3 items on list-like roles, reading-first 8, always bounded by the role's own maximum.
- No page numbers, dates or footers unless the user asks (then pass `--allow-footers` to `qa_check.py`).
- Speaker notes on every slide: what to say, the evidence, the transition.
- Vary layouts: no more than 2 consecutive slides with the same role and variant; add `transition` or `ambient` breathers in long decks.
- One theme per deck. Never auto-pick `ledger-gold` (finance); use it only when the user names it. Themes with `accentTextAllowed: false` use the accent for fills and rules only.
- Charts: the `insight` sentence must be true of the numbers shown. Each image is used once, with `alt` text.
- Template work is text-only. Never truncate with "..."; never invent facts.
- Avoid generic design: indigo-purple gradients, everything centred, identical card grids, decorative glow. See `${CLAUDE_SKILL_DIR}/references/design-rules.md`.

## Reference map

- `${CLAUDE_SKILL_DIR}/references/workflow.md`: intake wording, defaults, storyline, spec writing with a worked example, QA loop, delivery checklist.
- `${CLAUDE_SKILL_DIR}/references/design-rules.md`: type scale, grid, density, colour, images, charts, avoid list.
- `${CLAUDE_SKILL_DIR}/references/editing.md`: Mode C and D recipes.
- `${CLAUDE_SKILL_DIR}/references/templates.md`: Mode B details.
- `${CLAUDE_SKILL_DIR}/references/themes.md` and `${CLAUDE_SKILL_DIR}/references/themes.json`: the 27 themes.
- `${CLAUDE_SKILL_DIR}/references/layout-roles.md`: the 20 roles and their variants.

## Delivery

End with a short message containing: the output path of the `.pptx` (and the render folder if kept), a 3-line summary (slide count, theme, storyline), the QA status (pass, revise or blocked, with remaining warnings in plain words), and the assumptions you made. Do not paste logs. If rendering was unavailable, say the visual check was skipped.
