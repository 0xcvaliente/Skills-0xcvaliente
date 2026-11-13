# design-taste-frontend

Anti-slop art direction for company and product websites: landing pages, marketing sites, shops, cafes, hotels, studios, SaaS, AI, developer-tool and game sites, as static HTML/CSS or inside an existing React, Next.js, Vue, Svelte, Astro or Tailwind project. This is tasteskill 2.5.1 by Leonxlnx (MIT), vendored from upstream at revision f6b7657.

What 2.5 does: it deals the page plan, palette, type pairing, hero layout, backgrounds, effects and "moments" from local libraries (so pages differ and nothing is picked by taste), writes plain copy, places real or licensed stand-in photographs and real product UI, and enforces nine house rules with browser checkers and a finish gate that counts fix rounds. Version 2.1's app-screen and dashboard coverage is gone; use `ui-design` for app screens.

## Layout

- `SKILL.md`: the workflow (verbatim upstream).
- `references/`: system, layout, sections, copy (voice, registers, moves, tells), photos, backgrounds, cards, icons, diagrams, effects, moments, motion, scenes, performance and the finish gate (verbatim upstream). `upstream-README.md.source` is the v2.1.5 upstream README kept for reference (upstream no longer ships one in the skill folder); `provenance.md` is the import log.
- `library/`: palette and type data the scripts read.
- `scripts/`: `start`, `gate`, `consistency`, `copy-lint`, `photos`, `icons`, `effects`, `moments`, `perf` and `shoot` (`.mjs`).
- `assets/`: the starter page, `system.css`/`system.js`, and libraries of components, layouts, backgrounds, effects, moments, scenes, objects, UI, icons and photographs (about 37 MB). Photographs and icons carry their own licences (Unsplash License, CC0, CC BY and CC BY-SA photographs; CC0, ISC and MIT icon sets), recorded per file in `assets/photos/photos.json`, the `credits.json` files and `icons-credits.json`. A page that shows them prints the credits.

`SKILL.md` and every supporting file are verbatim upstream. Only this README and `references/provenance.md` are local.

## Requirements

- Node 22 or newer.
- A local Chrome, Edge or Chromium for the checkers and the gate (each run uses its own throwaway profile).
- `ffmpeg` is optional (WebP and phone crops of film frames).
- Network access only for live photograph searches and downloads (`photos.mjs`, Wikimedia Commons and Unsplash), icon sets read from a pinned CDN commit (`icons.mjs`), and the Google Fonts link a generated page uses.
- History files live in the project's `.taste-skill/` folder; nothing is written outside the project unless `TASTE_SKILL_RECENT` is set.

## The finish gate hook

In hosts that honour hooks in skill frontmatter (Claude Code), invoking the skill adds a Stop hook that runs the bundled `scripts/gate.mjs`. It holds back the end of the session only while a page build is armed in the project (`.taste-skill/build.json`) and the checker still finds fixable FAILs. It is capped: after the set rounds plus a few blocks, or 30 blocks in six hours, every finish is allowed, and `gate.mjs --done "<the user's words>"` closes a build. It opens only local pages. Other hosts can wire the same gate by hand; see `references/gate.md`.
