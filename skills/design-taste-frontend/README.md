# design-taste-frontend

Anti-slop art direction for public-facing web pages (landing pages, marketing sites, portfolios, one-pagers, redesigns) and, since v2.1, app screens (dashboards, admin and analytics views, settings, inboxes). This is taste-skill v2.1.4 by Leonxlnx (MIT), vendored from upstream at revision 6010f91.

What v2 does: it deals researched design directions from a local library (`scripts/draw.mjs`), enforces a house style with a static linter (`scripts/lint.mjs`) and a real-browser inspector (`scripts/inspect.mjs`), finds open-licence pictures (`scripts/assets.mjs`), and runs a look-and-fix loop on screenshots.

## Layout

- `SKILL.md`: the workflow (verbatim upstream v2).
- `references/`: type, colour, layout, copy, imagery, motion, critique, tells, research, app screens, scenes (verbatim upstream); `upstream-README.md.source` is the upstream README kept verbatim for reference only (it contains host-specific install paths); `provenance.md` is the import log.
- `library/`: JSON data the draw script reads. Use the script; do not read it whole.
- `scripts/`: `draw`, `lint`, `inspect`, `assets`, `scenes` (`.mjs`) and `lib/`.
- `assets/`: optional neutral `base.css` and `base.js`, plus `app.css`, `charts.js` and `scenes/` for app screens and scroll scenes.
- `evals/evals.json`: upstream evaluation prompts.

`SKILL.md` and every supporting file are verbatim upstream v2. Only this README and `provenance.md` are local.

## Requirements

- Node 22 or newer for `inspect.mjs` only; Node 18 or newer for `draw.mjs`, `lint.mjs` and `assets.mjs`.
- A local Chrome, Edge or Chromium for `inspect.mjs` (browser measurements).
- Network access only for `assets.mjs` searches and downloads.
- `draw.mjs` keeps its draw history in `~/.taste-skill/history.json`; set `TASTE_SKILL_HISTORY` to move it.

Previous version: v1 remains upstream at `skills/taste-skill-v1/` (see `references/provenance.md`).
