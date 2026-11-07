# Glassmorphism and Liquid Glass

Design, build and review glass interfaces: classic glassmorphism (frosted backdrop-blur panels) and Apple's Liquid Glass (iOS, iPadOS, macOS, watchOS and tvOS 26+, revised in 27). The skill decides where glass belongs (the floating navigation layer, not content), which variant and tint to use, how opaque the fill must be for text to stay readable over any backdrop, and how to fall back for accessibility settings and weaker hardware.

Original work in this repository, researched in November 2026 from Apple's Human Interface Guidelines and developer documentation, the WWDC25 "Meet Liquid Glass" session, Nielsen Norman Group's glassmorphism article, and WWDC 2026 coverage. See [references/sources.md](references/sources.md).

## Workflow

1. Establish platform, design system and target OS or browser versions.
2. Mark each surface as content or functional; only floating functional surfaces get glass.
3. Choose regular or clear glass and tint only the primary action.
4. Build with the platform recipe (web, SwiftUI/UIKit/AppKit, Expo, Compose, Flutter, Windows).
5. Check every ink and fill with the contrast script over white, grey, black and brand backdrops.
6. Check reduced transparency, increased contrast, reduced motion, forced colours, light and dark.
7. Add materialize, press and morph motion with a reduced-motion variant.
8. Keep the number of live glass surfaces small and measure scrolling.
9. Render over worst-case backdrops in each setting and state what was not verified.

## Output

For builds: code, the list of surfaces that got glass and why, contrast results, settings checked, and what remains unverified. For reviews: findings by severity with location, failing condition, evidence and fix.

## Example requests

```text
Use the glassmorphism-liquid-glass skill to give this app's tab bar and toolbar a Liquid Glass look on the web, with fallbacks.
Audit the glass cards on our pricing page for legibility and accessibility.
Adopt Liquid Glass in this SwiftUI app without custom backgrounds fighting the system.
```

## Package contents

- [SKILL.md](SKILL.md): when to use glass, workflow, rules, routing.
- [references/principles.md](references/principles.md): anatomy, Apple's rules, placement, motion, iOS 27 changes, criticism.
- [references/web.md](references/web.md): CSS and SVG recipes, support table, gotchas, performance.
- [references/apple-platforms.md](references/apple-platforms.md): SwiftUI, UIKit and AppKit APIs, opt-out changes, testing.
- [references/other-platforms.md](references/other-platforms.md): Expo, Android/Compose, Flutter, Windows, visionOS.
- [references/accessibility-performance.md](references/accessibility-performance.md): contrast method, settings mapping, fallback ladder, budget.
- [references/audit.md](references/audit.md): review checklist, anti-patterns, report format.
- [references/sources.md](references/sources.md): sources and what was verified locally.
- [scripts/glass-contrast.mjs](scripts/glass-contrast.mjs): worst-case contrast and minimum fill opacity (Node 18+).
- [assets/glass-demo.html](assets/glass-demo.html): runnable reference page, no dependencies.

## Requirements

Instructions only, except the optional contrast script (Node 18+) and the demo page (any current browser; lens refraction renders in Chromium). Browser automation, when available, is used to screenshot states; without it the skill says which states were not rendered.

## Install

Copy this directory into your host's skills folder (see the repository [INSTALL.md](../../INSTALL.md)), for example `cp -R glassmorphism-liquid-glass ~/.agents/skills/`, or run the repository installer. Name the skill in your prompt or let the host select it from its description.

## Validation

From the repository root: `python3 scripts/validate.py skills/glassmorphism-liquid-glass`. Structural validation does not establish visual quality; render the real screens.
