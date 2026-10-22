# pptx-deck

A Claude Code skill that creates, fills, edits and restyles PowerPoint (`.pptx`) decks. It asks the right intake questions, plans a storyline, lets you pick one of three rendered style previews, builds the deck from a JSON spec with native shapes and charts, renders it to PNG and runs a QA check with at most two revision rounds. Output is PowerPoint only.

Four modes: new deck from scratch, fill your own template, edit an existing deck, convert or restyle an old deck.

## Install

Copy this folder to `~/.claude/skills/pptx-deck/` (all projects) or `<project>/.claude/skills/pptx-deck/` (one project).

```bash
python3 -m pip install --user -r requirements.txt
brew install --cask libreoffice   # optional, needed for rendering
brew install poppler              # optional, needed for rendering to PNG
```

On macOS with Homebrew Python, pip may report "externally-managed-environment". Either add `--break-system-packages` or use a virtual environment (`python3 -m venv .venv && . .venv/bin/activate`). Without LibreOffice and poppler everything still works except `render.py`, so the visual check is skipped.

## Quick start

Ask Claude, for example: "Make a 10 slide deck for the board about our 2026 results" or "Fill my template.pptx with this report". The skill takes over from `SKILL.md`.

The scripts can be run by hand too (set `SKILL=~/.claude/skills/pptx-deck`):

```bash
python3 $SKILL/scripts/preview_styles.py --title "Annual Review" --subtitle "Leadership team" --auto 3 -o styles
python3 $SKILL/scripts/validate_spec.py $SKILL/references/examples/annual-review.json
python3 $SKILL/scripts/build_deck.py $SKILL/references/examples/annual-review.json -o deck.pptx
python3 $SKILL/scripts/render.py deck.pptx -o render --grid
python3 $SKILL/scripts/qa_check.py deck.pptx
```

Every script supports `--help`.

## File map

| Path | Purpose |
|---|---|
| `SKILL.md` | Entry point: modes, intake, rules, delivery |
| `requirements.txt` | python-pptx, lxml, Pillow (jsonschema optional) |
| `scripts/build_deck.py` | Spec to `.pptx`, 20 layout roles, native charts |
| `scripts/validate_spec.py` | Schema and deck-rule validation |
| `scripts/preview_styles.py` | Three style preview decks |
| `scripts/render.py` | `.pptx` to PNG through LibreOffice and poppler |
| `scripts/qa_check.py` | Overflow, font size, placeholder, notes and other checks |
| `scripts/inventory.py`, `extract.py` | Read a deck: shapes, notes, content, draft spec |
| `scripts/replace_text.py`, `rearrange.py`, `ooxml.py` | Edit text, order, raw XML |
| `scripts/template_profile.py`, `fill_template.py` | Profile and fill a user template |
| `references/workflow.md` | Intake, storyline, spec writing, QA loop, delivery |
| `references/design-rules.md` | Type, grid, density, colour, images, charts |
| `references/editing.md` | Edit and convert recipes |
| `references/templates.md` | Template mode details |
| `references/themes.md`, `themes.json` | 27 themes in four families |
| `references/layout-roles.md` | The 20 layout roles and variants |
| `references/deck-spec.schema.json` | JSON schema and limits |
| `references/examples/` | Two complete example specs |
| `LICENSES/` | MIT licence texts and attribution notice |

## Credits and inspiration

This skill is an original implementation. It was shaped by ideas from four projects:

- [frontend-slides](https://github.com/zarazhangrui/frontend-slides) by Zara Zhang (MIT): new / convert / enhance modes, four intake questions, three style previews to pick from, split instead of shrink, extracting a deck to content JSON, an avoid list for generic design.
- [GordenPPTSkill](https://github.com/GordenSun/GordenPPTSkill) by GordenSun (code MIT): built-in, user-template and original modes, template profiles with slots and capacity, text-only edits without truncation, consistent chapter names, render and inspect.
- [dashi-ppt-skill](https://github.com/chuspeeism/dashi-ppt-skill) (AGPL-3.0): intake, one core message per page, a set of layout roles, themes with seeded variants, QA with pass / revise / blocked.
- [guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) (AGPL-3.0): duration to slide count, a hook-context-core-shift-takeaway arc, editorial and Swiss styles, minimum font sizes, speaker notes.

## License note

The code, schema, theme data and documentation in this folder are original. Ideas adapted from frontend-slides and GordenPPTSkill are credited with their MIT licence texts in `LICENSES/frontend-slides-MIT.txt` and `LICENSES/GordenPPTSkill-MIT.txt`; `LICENSES/NOTICE.md` summarises the attribution. The two AGPL projects were used only as conceptual inspiration: no code or text was copied from them. The PowerPoint templates that ship with GordenPPTSkill are under a separate non-commercial notice and are not included; bring your own template for template mode.
