# Principles

## Contents

1. [Vocabulary](#1-vocabulary)
2. [Anatomy of a glass surface](#2-anatomy-of-a-glass-surface)
3. [Glassmorphism and Liquid Glass compared](#3-glassmorphism-and-liquid-glass-compared)
4. [Apple's Liquid Glass rules](#4-apples-liquid-glass-rules)
5. [Where glass belongs](#5-where-glass-belongs)
6. [Hierarchy, colour and type](#6-hierarchy-colour-and-type)
7. [Motion](#7-motion)
8. [What changed in iOS 27](#8-what-changed-in-ios-27)
9. [The criticism to design against](#9-the-criticism-to-design-against)

## 1. Vocabulary

- **Glassmorphism.** A visual style named in late 2020 for interfaces built from frosted, translucent panes. It went mainstream with macOS Big Sur (2020) and Windows 11's Acrylic and Mica materials (2021). Nielsen Norman Group (Megan Brown, June 2024) defines it as using "different levels of translucency to create depth and contrast between foreground and background elements."
- **Liquid Glass.** Apple's dynamic material, announced 9 June 2025 for iOS, iPadOS, macOS Tahoe, watchOS, tvOS and visionOS 26. Apple describes it as combining "the optical properties of glass with a sense of fluidity." Revised for the 27 releases at WWDC on 8 June 2026.
- **Backdrop.** Whatever is painted behind the glass at this moment. It changes as content scrolls, so a glass surface has no fixed background colour.
- **Tint / fill.** The translucent colour laid over the processed backdrop. It carries most of the legibility.
- **Vibrancy.** Apple's term for foreground colours that pull light and colour from the material so labels stay legible on it.
- **Lensing.** Bending and concentrating light, strongest at the edge of the shape, instead of scattering it with blur.
- **Material thickness.** How opaque and how blurred a material is. Thicker means more contrast for text; thinner keeps more of the context visible.
- **Content layer vs functional layer.** Content is what the user came for (photos, lists, documents). The functional layer holds navigation and controls and floats above it. Liquid Glass belongs only to the functional layer.
- **Scroll edge effect.** A blur or dimming that fades content as it scrolls under a bar, replacing hard divider lines.
- **Dimming layer.** A dark translucent layer between bright media and clear glass that restores contrast.
- **Backdrop root (web).** The nearest ancestor whose rendering isolates what a `backdrop-filter` can see. See [web.md §12](web.md#12-gotchas).

## 2. Anatomy of a glass surface

Bottom to top:

1. **Backdrop sample.** The content behind the element.
2. **Optics.** Blur (glassmorphism) and/or lensing (Liquid Glass). More blur over busy backdrops; NN/g's guidance is that more background blur is better over photos and video.
3. **Colour and luminance correction.** A saturation boost (140-180 %) keeps colour alive through the blur; a brightness shift pulls luminance toward a band that the ink can read on.
4. **Fill.** The translucent tint. Its opacity is what guarantees contrast when the backdrop is flat white or flat black, because blur cannot average a large flat area away.
5. **Grain (optional).** 2-4 % noise. It hides gradient banding and makes the pane read as a material. Fluent's Acrylic uses noise for the same reason.
6. **Edge.** A 1 px border or gradient rim, brighter on the side facing the light. Liquid Glass adds a specular highlight that follows the shape.
7. **Shadow.** Separation from content. Apple's glass raises shadow opacity over text and lowers it over plain light backgrounds.
8. **Foreground.** Text and symbols in high-contrast or vibrant colours, at a heavier weight than on solid surfaces.

## 3. Glassmorphism and Liquid Glass compared

| Aspect | Glassmorphism | Liquid Glass |
|---|---|---|
| Light | Scatters (frosted blur) | Bends and concentrates (lensing), plus specular highlights that move with interaction and sometimes device motion |
| Appearance | Fixed tint per theme | Continuously adapts to the backdrop: small elements flip light/dark, shadows strengthen over text |
| Size | Same treatment at every size | Larger elements read thicker: deeper shadow, stronger lensing, softer scattering; large elements do not flip light/dark |
| Shape | Rounded rectangles, often arbitrary radii | Capsules and concentric radii that nest into window and device corners |
| Interaction | Usually none | Flexes and glows on touch, morphs between controls, materializes in and out |
| Placement | Often content cards | Navigation and controls only |
| Accessibility | Up to the implementer | System-managed: Reduce Transparency, Increase Contrast, Reduce Motion, plus a user look setting |

## 4. Apple's Liquid Glass rules

From the HIG Materials page and the WWDC25 session "Meet Liquid Glass". Quotes are Apple's.

**Layering**
- "Don't use Liquid Glass in the content layer." Use standard materials there. Exception: transient controls such as sliders and toggles take on glass while being used.
- "Use Liquid Glass effects sparingly." Limit custom glass to the most important functional elements.
- "Always avoid glass on glass." For elements on top of glass, use fills, transparency and vibrancy so they feel like a thin overlay that is part of the material.
- Avoid letting content intersect glass in steady states (for example at launch); reposition or scale the content instead.

**Variants**
- **Regular** is the default and most versatile: it blurs and adjusts luminosity, works at any size over any content, and suits components with a lot of text (alerts, sidebars, popovers).
- **Clear** is permanently more transparent and has no adaptive behaviour. Use it only when all three hold: the element sits over media-rich content, a dimming layer will not hurt that content, and the content on the glass is bold and bright.
- Over bright content, put a dark dimming layer of about 35 % opacity behind clear glass. Over dark content, or with system media controls that dim already, skip it. For small elements, local dimming keeps more of the media's vibrancy.
- "They should never be mixed."

**Tint**
- Tinting maps a colour to a range of tones that follow the brightness of the content underneath, like coloured glass.
- "Tinting should only be used to bring emphasis to primary elements and actions." When every element is tinted, nothing stands out.
- Do not replace the tint with a solid fill; an opaque fill breaks the material.

**Optics and behaviour**
- Lensing defines the material: it "bends, shapes, and concentrates light" rather than scattering it.
- Objects **materialize** by modulating the lensing, not by fading opacity.
- The material is gel-like: it flexes with interaction, lights from within on touch, and the glow spreads to nearby glass.
- Controls can lift into glass only while being touched, so the resting state stays quiet.
- When a Mac or iPad window loses focus, the glass recedes.

**Legibility**
- Scroll edge effects dissolve content under bars; over dark content they switch to a subtle dimming. A **hard** style applies uniformly under a toolbar plus pinned accessory (for example column headers) when more separation is needed.
- Symbols on regular glass flip light/dark with the glass.

**System settings** (applied automatically to system glass)
- Reduce Transparency makes glass frostier and hides more of the backdrop.
- Increase Contrast makes elements mostly black or white with a contrasting border.
- Reduce Motion lowers the intensity of some effects and disables the elastic behaviour.
- A user setting chooses the Liquid Glass look (iOS 26.1 added transparency controls; iOS 27 turned them into a slider, see §8).

## 5. Where glass belongs

Good fits:
- Navigation bars, tab bars, toolbars, sidebars and inspectors that float over content.
- Floating action clusters and media controls over photos or video.
- Menus, popovers, context menus, toasts and HUDs.
- Half-height sheets (Apple makes a sheet more opaque when it expands to full height, to focus the task).
- Overlays in spatial and AR interfaces, where opacity would block the surroundings.
- Hero overlays: one frosted panel over a photo or illustration.

Poor fits:
- Content cards in grids and feeds, tables, lists and long text.
- Forms and dense data (dashboards, charts).
- Anything stacked on other glass.
- Pages with nothing interesting behind the glass.

Test: if the element would be meaningless without content scrolling or sitting behind it, glass can fit. If the element *is* the content, use a solid surface or a standard material.

## 6. Hierarchy, colour and type

- Glass recedes; content leads. Put brand colour in content, keep chrome neutral, tint only the primary action.
- Thickness encodes hierarchy: thicker for surfaces that hold text, thinner where context matters more than reading.
- Type on glass: regular weight or heavier (500+ on the web), no hairline weights, no low-contrast grey secondary text on thin or clear glass. Apple advises against quaternary label colours on thin and ultra-thin materials.
- Icons in toolbars: use standard symbols, group related actions on one shared background, do not mix text and icons in one group, and give every icon an accessible label.
- Shapes: capsules for controls, concentric radii for nested shapes (inner radius = outer radius - padding).

## 7. Motion

- **Materialize.** Enter by growing in scale while blur or lensing resolves; exit by the reverse. A plain opacity fade looks like a picture, not a material.
- **Press.** A short, slightly springy response: the glass grows a little and brightens from within, then settles.
- **Morph.** Buttons turn into the menu or popover they open, from the point that was tapped. Nearby glass shapes merge when they come within a threshold distance (`GlassEffectContainer` spacing on Apple platforms).
- **Reduced motion.** Drop the elastic overshoot and the morph; keep a short crossfade so the state change is still visible.
- For springs, gestures and momentum, use the apple-design and animate skills.

## 8. What changed in iOS 27

Announced at WWDC on 8 June 2026 for iOS 27, iPadOS 27 and macOS 27. Sources are press coverage; check Apple's current HIG before relying on details.

- Lower default transparency and a changed glass effect, in response to legibility complaints.
- The binary Liquid Glass look setting (added in iOS 26.1) became a slider from fully clear to fully tinted and frosted.
- Some system apps brought toolbars back, so floating buttons feel less detached.
- iPadOS and macOS sidebars lost unnecessary bezels; overly round corners were reduced.
- App icons: only some elements catch the light; a layered effect gives depth.
- For developers: the `UIDesignRequiresCompatibility` opt-out is ignored for apps linked against the iOS 27 SDK (see [apple-platforms.md](apple-platforms.md#ios-27-and-the-opt-out)).

Design consequence: users can now set any transparency between clear and frosted. Custom surfaces built from the system glass APIs follow that setting; hand-built blur views do not, and must still be legible at the clearest setting.

## 9. The criticism to design against

Liquid Glass launched to mixed reviews. Recurring complaints: text hard to read over busy or bright content (for example in sunlight), effects pulling attention from content, departures from established conventions, and extra complexity for small teams. Apple raised opacity during the iOS 26 betas (July 2025), added user controls in iOS 26.1, and lowered default transparency in iOS 27.

NN/g's earlier critique of glassmorphism points the same way: translucency can leave text too light or too dark, busy backdrops distract, and low-vision users need options to reduce transparency or raise contrast.

Lesson: ship legible by default, treat transparency as garnish, and make the solid fallback a first-class design rather than an afterthought.
