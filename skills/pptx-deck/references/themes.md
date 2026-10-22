# Themes

Source of truth: `themes.json` (27 themes in four families). The renderer reads palette, fonts and `decoration` from there. Fonts list a preferred name and a safe system fallback; the builder uses the fallback when the preferred font is not installed.

| id | Name | Family | Mood | Mode | Suited for | Auto-pick |
|---|---|---|---|---|---|---|
| soft-neumorphic | Soft Clay | signature | Calm, tactile, gentle shadows | light | wellness, design studios, product tours, internal updates | yes |
| aurora-circuit | Aurora Circuit | signature | Futuristic glow, violet and green on deep night | dark | AI, SaaS, deep tech, innovation pitches | yes |
| code-canvas | Code Canvas | signature | Terminal-flavoured, crisp and utilitarian | dark | developer talks, engineering reviews, API launches, architecture | yes |
| candy-glass | Candy Glass | signature | Bright translucent pastels, playful | light | consumer brands, youth marketing, app launches, social campaigns | yes |
| spectrum-report | Spectrum Report | signature | Clean white with a wide, distinguishable colour range | light | data reports, dashboards, KPI reviews, survey results | yes |
| atlas-dark | Atlas Dark | signature | Dense dark canvas built for charts and maps | dark | strategy, market maps, operations, portfolio reviews | yes |
| research-white | Research White | signature | Cool, sober white with restrained blue accents | light | white papers, research findings, academic talks, policy briefs | yes |
| onyx-gold | Onyx Gold | signature | Black with warm gold, premium and quiet | dark | luxury, premium products, awards, high-end services | yes |
| midnight-editorial | Midnight Editorial | signature | Deep blue magazine layout with confident serif headings | dark | brand stories, annual reports, thought leadership, campaign narratives | yes |
| ledger-gold | Ledger Gold | signature | Ivory page with indexed gold rules, conservative finance | light | finance, investor relations, audit, banking | NO (explicit only) |
| growth-surge | Growth Surge | signature | High-energy orange and teal, momentum-driven | light | growth reviews, business plans, sales kickoffs, quarterly targets | yes |
| neon-wave | Neon Wave | signature | Sound-wave neon on black, loud and rhythmic | dark | events, music, entertainment, festivals, launch parties | yes |
| paper-noir | Paper Noir | editorial | Classic black-on-newsprint; serif headings, generous whitespace, thin rules | light | essays, long-form narratives, cultural briefings, annual letters | yes |
| harbour-ink | Harbour Ink | editorial | Navy ink on cool paper; serif headings, generous whitespace, thin rules | light | essays, long-form narratives, cultural briefings, annual letters | yes |
| pine-folio | Pine Folio | editorial | Forest ink on warm paper; serif headings, generous whitespace, thin rules | light | essays, long-form narratives, cultural briefings, annual letters | yes |
| walnut-press | Walnut Press | editorial | Dark walnut on parchment; serif headings, generous whitespace, thin rules | light | essays, long-form narratives, cultural briefings, annual letters | yes |
| sepia-quarto | Sepia Quarto | editorial | Soft sepia on aged cream; serif headings, generous whitespace, thin rules | light | essays, long-form narratives, cultural briefings, annual letters | yes |
| swiss-cobalt | Grid Cobalt | swiss | Flat grid, asymmetric left alignment, one hard accent | light | design talks, architecture, product systems, research summaries | yes |
| swiss-yellow | Grid Signal Yellow | swiss | Flat grid, asymmetric left alignment, one hard accent | light | design talks, architecture, product systems, research summaries | yes |
| swiss-lime | Grid Volt Lime | swiss | Flat grid, asymmetric left alignment, one hard accent | light | design talks, architecture, product systems, research summaries | yes |
| swiss-orange | Grid Vermilion | swiss | Flat grid, asymmetric left alignment, one hard accent | light | design talks, architecture, product systems, research summaries | yes |
| furnace-grotesk | Furnace Grotesk | bold | Heavy grotesk on near-black with hot orange | dark | growth, launches, keynotes | yes |
| cobalt-slab | Cobalt Slab | bold | Black field with electric blue blocks | dark | tech launches, product reveals, pitches | yes |
| dune-serif | Dune Serif | bold | Elegant serif in warm tan on near-black | dark | luxury, hospitality, brand heritage | yes |
| signal-modern | Signal Modern | bold | White page with one loud red-orange signal | light | campaigns, strategy decks, studios | yes |
| crimson-folio | Crimson Folio | bold | Warm paper, serif type, crimson emphasis | light | law, publishing, cultural institutions | yes |
| terminal-phosphor | Terminal Phosphor | bold | Phosphor green on black, monospaced | dark | security, infrastructure, hacker culture | yes |

## Families

- signature (12 themes): the original mood-led set, each tied to an audience type (developers, consumers, analysts, premium, events). Pick when the audience or industry is the main signal.
- editorial (5 themes): ink on paper, serif headings, generous whitespace, thin rules, no shadows or gradients. Pick for narrative, essay-like or reading-heavy decks, letters and cultural topics.
- swiss (4 themes): flat grid, asymmetric left alignment, square corners, bold rules, one accent. Pick for design, systems and research talks that value structure over decoration. Yellow, lime and vermilion accents are fill-only (`accentTextAllowed: false`): use them for blocks, rules and bars, never for text on the paper background. Only `swiss-cobalt` may use its accent for text.
- bold (6 themes): high-contrast presets with one strong accent and large display type. Pick for keynotes, launches and campaigns where impact matters more than density.

## Choosing a theme

1. Start from the audience, then content, then the room. Developers and AI: `code-canvas`, `aurora-circuit`, `terminal-phosphor`. Consumers and youth: `candy-glass`. Dense strategy: `atlas-dark`. Numbers-heavy: `spectrum-report`. Research and policy: `research-white`, `swiss-cobalt`. Premium: `onyx-gold`, `dune-serif`. Brand story: `midnight-editorial` or an editorial theme. Growth plans: `growth-surge`. Events: `neon-wave`.
2. Dark themes suit projected talks in dim rooms; light themes suit print, laptops and bright rooms.
3. Chart-heavy decks: `spectrum-report`, `atlas-dark`, `growth-surge`.
4. One theme per deck; never mix.

## Finance theme rule

`ledger-gold` has `autoPick: false`. Use it only when the user explicitly names it or explicitly asks for the finance theme. Automatic selection must skip every theme with `autoPick: false`; for finance topics without an explicit request choose `spectrum-report` or `research-white`.

## Decoration

Every theme has `decoration`: `shadows` (bool), `cornerRadius` (pt), `gradients` (bool), `rules` (`thin`, `bold` or `none`) and `imageTreatment` (`natural`, `grayscale` or `duotone`). Renderers must honour it; swiss themes have no shadows, radius 0 and no gradients.

## Avoid list (anti-generic design)

- Generic display fonts: Inter, Roboto or Arial as heading fonts (fine as fallbacks).
- The default indigo `#6366f1` and purple gradients on white.
- Everything centred; prefer an asymmetric, left-anchored composition.
- Identical card grids repeated slide after slide; vary structure with layout variants.
- Gratuitous glass, blur or glow effects that carry no meaning.
- Stock-photo-like illustrations; use real screenshots, data or restrained shapes.

## Seed format

`randomSeed` = `<themeId>-<YYYYMMDD>-<3 lowercase letters>`, for example `growth-surge-20261022-qzx`. The same spec and seed always produce the same layout variants.
