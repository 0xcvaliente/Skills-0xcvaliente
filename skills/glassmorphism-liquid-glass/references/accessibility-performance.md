# Accessibility and performance

## Contrast on a surface without a fixed background

Glass has no single background colour, so check contrast against the worst backdrop that can sit behind it, not the gradient in the mockup.

1. List every ink colour used on the glass (body text, secondary text, icons, focus ring, borders that mark control boundaries).
2. List the backdrops that can appear behind it: at minimum flat white, mid grey and flat black, plus brand colours and any full-bleed media.
3. Run the bundled script for each ink and fill:

   ```sh
   node scripts/glass-contrast.mjs --text "#111114" --tint "rgba(255,255,255,0.55)"
   node scripts/glass-contrast.mjs --text "#fff" --tint "rgba(22,20,32,0.64)" --backdrops "#fff,#808080,#000,#ff2d55"
   node scripts/glass-contrast.mjs --text "#0b0b10" --tint "rgba(255,255,255,0.4)" --target 3   # icons
   ```

   It prints the ratio over each backdrop, the worst case, and the minimum fill opacity that passes.
4. Targets (WCAG 2.x): 4.5:1 for body text, 3:1 for large text (24 px, or 18.66 px bold), icons and the visual boundary of controls.
5. Blur moderates busy backdrops, so real screens usually do better than the flat extremes. A flat area larger than the blur radius does not average out, which is why the extremes matter.

Why the usual tutorial values fail: a 10-20 % white fill with white text has nothing to stand on over a light backdrop, and the same fill with dark text fails over a dark one. Glass that must work over anything needs about half opacity for text, or an ink that adapts to the backdrop (which only native platforms do automatically).

## Type and icons on glass

- Body text at regular weight or heavier; 500+ on the web where subpixel antialiasing may be lost.
- Avoid tertiary or quaternary grey text on thin or clear glass.
- Icons: filled or 2 px strokes rather than hairlines, with labels for assistive tech.
- Do not rely on colour alone on tinted glass; the tint shifts with the backdrop.

## Settings mapping

| User need | Apple | Web | Android | Windows |
|---|---|---|---|---|
| Less transparency | Reduce Transparency; Liquid Glass look setting (slider in iOS 27) | `prefers-reduced-transparency: reduce` (Chromium only) plus an in-app setting | Platform blur can be disabled by device or power saving; check `isCrossWindowBlurEnabled` | Transparency effects off |
| More contrast | Increase Contrast | `prefers-contrast: more` | High-contrast text | Contrast themes |
| System colours only | — | `forced-colors: active` | — | Contrast themes (forced colours) |
| Less motion | Reduce Motion | `prefers-reduced-motion: reduce` | Remove animations | Animation effects off |

What each mode should do to glass:
- **Reduced transparency:** solid or near-solid fill (about 95 % opacity), no blur, no lens. Keep the shape and the shadow.
- **More contrast:** solid fill, full-strength ink, a visible border around each glass surface, no grain or gradient rim.
- **Forced colours:** no filters; `Canvas` background, `CanvasText` border and text; let the browser apply system colours.
- **Reduced motion:** no spring overshoot, no morph, no blur-in; a short crossfade still shows the change.

## Fallback ladder

Design each step; the lower ones are not afterthoughts.

1. Lens refraction + light blur + rim (Chromium web, native Liquid Glass).
2. Frosted blur + rim (other browsers, older OS).
3. Frosted-solid: near-opaque fill, no blur (reduced transparency, weak hardware, power saving).
4. Solid with border (increased contrast, forced colours).

## Focus

A focus ring on glass must work over any backdrop. Use a two-tone ring: a dark outline plus a light outer halo (or the reverse). Example in [web.md §10](web.md#10-accessibility-hooks). Keep it at 3:1 against the glass fill and visible in forced colours (`outline` survives; `box-shadow` does not).

## Performance budget

- **Web:** every glass surface re-samples and filters its backdrop when anything behind it changes. Keep a few surfaces visible at once (bars, one panel, an open menu). No glass per list row or card. Do not animate blur radius on large areas. Pre-blur static images instead of filtering them live. Measure while scrolling on a mid-range phone with the browser's performance panel, paint flashing and layer borders.
- **Apple:** put custom glass in `GlassEffectContainer` / `UIGlassContainerEffect`, limit the number of effects, profile with Instruments on the oldest supported device.
- **Android and Flutter:** blur is GPU-bound; test on low-end hardware, share backdrop sampling (`BackdropGroup` in Flutter), and fall back to a scrim when blur is disabled.
- **Windows:** use Mica for long-lived surfaces (sampled once) and Acrylic only for transient ones.
