---
name: glassmorphism-liquid-glass
description: "Design, build and review glass interfaces: classic glassmorphism (frosted backdrop-blur panels) and Apple's Liquid Glass (iOS, iPadOS, macOS, watchOS and tvOS 26+, revised in 27). Covers where glass belongs (the floating navigation layer, not content), regular vs clear variants, tinting, worst-case text contrast, accessibility settings, motion and performance, with recipes for CSS backdrop-filter and SVG refraction, SwiftUI/UIKit/AppKit glass APIs, Expo, Compose, Flutter and Windows Acrylic/Mica. Use when the user mentions glassmorphism, liquid glass, frosted or translucent UI, glass cards, bars or toolbars, backdrop-filter, Acrylic or Mica, wants an iOS 26 look, or asks to audit a glass UI. Use apple-design for springs and gestures, animate for general web motion, animation-performance for dropped frames, ui-verification for browser probes, and write-swift for Swift language questions."
---

# Glassmorphism and Liquid Glass

Glass is a layer in the hierarchy, not a surface style. It earns its place when a control floats over content that should stay visible. Everywhere else it costs legibility and frame time.

## Pick the material first

| | Glassmorphism | Liquid Glass |
|---|---|---|
| Optics | Blur scatters the backdrop (frosted) | Lensing bends light at the edges; the centre stays clearer |
| Behaviour | Static | Adapts to what is behind it, reacts to touch, morphs, materializes |
| Where | Overlays, panels, menus; often overused on content cards | Only the functional layer: bars, toolbars, tab bars, sidebars, menus, sheets, floating controls |
| Origin | 2020-21 trend (macOS Big Sur, Windows 11 Acrylic/Mica) | Apple, WWDC 9 June 2025; revised at WWDC 8 June 2026 |
| Web | Fully achievable with `backdrop-filter` | Approximation: rim light everywhere, refraction in Chromium only |

When someone asks for "liquid glass" on the web, say up front what browsers can and cannot reproduce ([web.md §5](references/web.md#5-liquid-glass-approximation)).

## Workflow

1. **Context.** Establish platform, existing design system, target OS or browser versions, and brand. On Apple platforms the system components already are Liquid Glass; start from them, not from custom effects.
2. **Map layers.** List every surface and mark it *content* or *functional*. Only functional surfaces that float over content get glass. Content gets solid fills or standard materials.
3. **Variant and tint.** Regular by default. Clear only over photos or video, with a dimming layer and bold foreground. Tint only the primary action.
4. **Build** with the platform recipe: [web](references/web.md), [Apple](references/apple-platforms.md), [other platforms](references/other-platforms.md).
5. **Legibility pass.** Run `scripts/glass-contrast.mjs` for each text and icon colour on each glass fill against white, mid grey, black and any brand colour that can sit underneath. Raise the fill opacity or change ink until text reaches 4.5:1 and icons 3:1.
6. **Settings pass.** Reduced transparency, increased contrast, reduced motion, forced colours, light and dark, and on Apple platforms the user's Liquid Glass look setting.
7. **Motion pass.** Materialize (not plain fade), press response, morph from the source control, plus a reduced-motion variant.
8. **Performance pass.** Count glass surfaces visible at once, group them, keep blur out of long lists, profile on a mid-range device.
9. **Verify** by rendering over worst-case backdrops (flat white, flat black, busy photo, text, stripes) in every setting. With browser automation, screenshot each state. Say what could not be rendered: some automated WebKit builds do not paint `backdrop-filter` at all, so Safari visuals need a real Safari.

## Rules

1. Glass only in the floating functional layer. The one exception: transient controls such as a slider knob or toggle may turn to glass while being touched.
2. No glass on glass. Elements on top of glass use fills, vibrancy or plain text.
3. Never mix regular and clear glass in one group of controls.
4. Tint one thing: the primary action. Bring colour in through content.
5. Contrast must hold over the worst backdrop, not the mockup's gradient: 4.5:1 for text, 3:1 for icons and control boundaries.
6. Every glass surface has a solid fallback used for reduced transparency, increased contrast, forced colours and missing `backdrop-filter`.
7. Glass needs something behind it. Over flat white it reads as grey plastic; give the page imagery or colour, or use a solid surface.
8. Where content scrolls under a bar, use a scroll edge effect (fading blur) instead of a divider line.
9. Use it sparingly: a few glass surfaces per screen, never a grid of glass cards.
10. On the web, no ancestor of a glass element may have `opacity` below 1, `filter`, `mask`, `clip-path`, `mix-blend-mode`, `backdrop-filter` or a `will-change` naming one of them. Any of those cuts the backdrop and the blur shows nothing ([web.md §12](references/web.md#12-gotchas)).

## References

- [principles.md](references/principles.md): anatomy of a glass surface, Apple's Liquid Glass rules, where glass belongs, what changed in iOS 27, the criticism to design against.
- [web.md](references/web.md): support table, tokens, frosted recipe, Liquid Glass approximation with an SVG lens, scroll edge effect, toolbars, menus, motion, fallbacks, Tailwind, gotchas.
- [apple-platforms.md](references/apple-platforms.md): adoption order and SwiftUI, UIKit and AppKit APIs with code, the iOS 27 SDK opt-out change.
- [other-platforms.md](references/other-platforms.md): React Native/Expo, Android/Compose, Flutter, Windows Fluent, visionOS.
- [accessibility-performance.md](references/accessibility-performance.md): contrast maths, settings mapping, focus rings, motion, performance budget.
- [audit.md](references/audit.md): review checklist, glass anti-patterns, report format.
- [sources.md](references/sources.md): sources with dates and what was verified.

## Bundled files

- `scripts/glass-contrast.mjs` (Node 18+): worst-case WCAG contrast of text on a translucent fill, plus the minimum fill opacity that passes. `node scripts/glass-contrast.mjs --text "#fff" --tint "rgba(20,20,24,.4)"`.
- `assets/glass-demo.html`: runnable reference with frosted glass, a Liquid Glass toolbar with SVG lens refraction, scroll edge header, materializing menu and all accessibility fallbacks. Serve it over HTTP or open it directly in a browser.

## Output

- **Build:** the code, which surfaces got glass and why, contrast results per fill, the settings that were checked, and what stays unverified (for example Safari rendering or physical-device performance).
- **Review:** findings ordered by severity, each with location, failing condition and fix, using [audit.md](references/audit.md).
