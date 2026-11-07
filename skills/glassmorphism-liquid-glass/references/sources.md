# Sources

Researched November 2026. Apple documentation was read in its Markdown form on developer.apple.com. Press coverage of WWDC 2026 is marked as such; prefer Apple's own pages when they disagree.

## Apple (primary)

- Human Interface Guidelines, *Materials*: <https://developer.apple.com/design/human-interface-guidelines/materials>. Liquid Glass guidance added 9 June 2025, updated 9 September 2025. Source of the layer rule, regular vs clear, the 35 % dimming layer, vibrancy levels and platform notes.
- *Adopting Liquid Glass*: <https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass>. Adoption checklist, API lists, `UIDesignRequiresCompatibility`.
- *Applying Liquid Glass to custom views* (SwiftUI): <https://developer.apple.com/documentation/swiftui/applying-liquid-glass-to-custom-views>. `glassEffect`, `GlassEffectContainer`, `glassEffectUnion`, `glassEffectID`, transitions, performance note.
- API reference pages: `UIGlassEffect`, `UIGlassContainerEffect`, `NSGlassEffectView`.
- WWDC25 session 219, *Meet Liquid Glass*: <https://developer.apple.com/videos/play/wwdc2025/219/>. Lensing, materialization, adaptivity, the three conditions for clear glass, tinting, glass on glass, scroll edge effects, accessibility behaviour.
- Apple Developer Forums thread 832543, *Clarification on the planned removal of UIDesignRequiresCompatibility*: <https://developer.apple.com/forums/thread/832543>.

## WWDC 2026 and iOS 27 (press)

- TapSmart, *WWDC 2026 recap*: <https://www.tapsmart.com/news/wwdc26-recap/> (8 June 2026). Clear-to-tinted slider, toolbars returning, fewer bezels and less rounding, selective icon highlights.
- Wikipedia, *Liquid Glass*: <https://en.wikipedia.org/wiki/Liquid_Glass>. Timeline, iOS 26 beta opacity changes, iOS 26.1 controls, reception, reduced default transparency in the 27 releases.
- Tom's Guide and Tech Times WWDC 2026 coverage (Tech Times was written before the keynote and reports expected changes).

## Glassmorphism and accessibility

- Nielsen Norman Group, Megan Brown, *Glassmorphism: Definition and Best Practices* (7 June 2024): <https://www.nngroup.com/articles/glassmorphism/>.
- WCAG 2.2 contrast criteria 1.4.3 (text) and 1.4.11 (non-text).

## Web

- kube.io, *Liquid Glass in the Browser: Refraction with CSS and SVG*: <https://kube.io/blog/liquid-glass-css-svg>. Displacement maps from a surface profile, Chromium-only `backdrop-filter: url()`.
- Web Platform features explorer, `backdrop-filter` (Baseline since 16 September 2024) and `prefers-reduced-transparency` (limited availability).
- Filter Effects Module Level 2, backdrop root definition.

## Other platforms

- Expo SDK reference, *GlassEffect*: <https://docs.expo.dev/versions/latest/sdk/glass-effect/>.
- Haze: <https://chrisbanes.github.io/haze/>.
- Flutter 3.29 release notes (`BackdropGroup`, `BackdropFilter.grouped`).
- Microsoft Fluent 2 material guidance (Mica, Acrylic).

## Verified locally for this skill

- `scripts/glass-contrast.mjs`: outputs checked by hand for black and white fills (54 % and 46 % minimums match the WCAG formula).
- `assets/glass-demo.html` in headless Chromium 156: lens filters build and apply, menu focus handling, reduced transparency and contrast modes switch off blur and lens, forced colours, dark mode, no horizontal scroll at 390 px, no console errors.
- Backdrop-root behaviour (opacity, filter, `will-change`, transform, nested glass, masked blur layer) in Chromium 156.
- WebKit (Safari 27.2 engine, automated build): `CSS.supports` returns true for `url()` backdrop filters; `prefers-reduced-transparency` is not recognised. That build did not paint `backdrop-filter` at all, so Safari visuals were **not** verified.
- Firefox was not tested.
