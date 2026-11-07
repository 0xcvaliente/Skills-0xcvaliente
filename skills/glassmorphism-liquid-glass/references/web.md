# Glass on the web

All code here is taken from [`assets/glass-demo.html`](../assets/glass-demo.html), which was rendered and checked in headless Chromium 156 (November 2026). Copy from the demo when in doubt; it is the tested version.

## Contents

1. [Support](#1-support)
2. [Tokens](#2-tokens)
3. [Frosted surface](#3-frosted-surface)
4. [Edge light and grain](#4-edge-light-and-grain)
5. [Liquid Glass approximation](#5-liquid-glass-approximation)
6. [Scroll edge effect](#6-scroll-edge-effect)
7. [Floating toolbars and tab bars](#7-floating-toolbars-and-tab-bars)
8. [Menus and popovers](#8-menus-and-popovers)
9. [Press and materialize motion](#9-press-and-materialize-motion)
10. [Accessibility hooks](#10-accessibility-hooks)
11. [Tailwind](#11-tailwind)
12. [Gotchas](#12-gotchas)
13. [Performance](#13-performance)

## 1. Support

| Feature | Status (November 2026) |
|---|---|
| `backdrop-filter` | Baseline (newly available) since 16 September 2024: Chrome 76, Edge 79, Firefox 103, Safari 18. Keep `-webkit-backdrop-filter` first for Safari 17 and older. |
| `backdrop-filter: url(#svg-filter)` | Renders in Chromium only. WebKit returns `true` from `CSS.supports('backdrop-filter', 'url(#a)')` but does not render it, so `@supports` cannot detect it: gate on the engine instead. Firefox not verified. |
| `prefers-reduced-transparency` | Chromium 118+. Not recognised by WebKit (checked in a Safari 27.2 engine build); behind a flag in Firefox. Provide an in-app setting as well. |
| `prefers-contrast`, `forced-colors`, `prefers-reduced-motion`, `prefers-color-scheme` | Supported across current engines. |
| `color-mix()`, individual `scale`/`translate` | Supported across current engines. |

## 2. Tokens

Fill opacities are not taste: they are the minimum that keeps the ink legible over a flat white or flat black backdrop. Recompute them with `scripts/glass-contrast.mjs` whenever ink or fill colours change.

```css
:root {
  color-scheme: light dark;
  --ink: #111114;
  --ink-2: #3a3a42;
  --page: #f3f1ff;

  /* Frosted glass */
  --glass-fill: rgb(255 255 255 / 0.55);   /* >= 0.49 keeps --ink text at 4.5:1 over any backdrop */
  --glass-optics: blur(18px) saturate(180%);
  --glass-edge: rgb(255 255 255 / 0.55);
  --glass-rim: rgb(255 255 255 / 0.9);
  --glass-solid: rgb(250 250 252 / 0.97);   /* reduced-transparency fill */
  --glass-shadow: 0 10px 30px rgb(20 10 60 / 0.18), 0 1px 2px rgb(20 10 60 / 0.10);

  /* Liquid Glass approximation */
  --lg-fill: rgb(255 255 255 / 0.40);       /* >= 0.37 keeps icons at 3:1 over any backdrop */
  --lg-optics: blur(3px) saturate(180%) brightness(1.06);
  --lg-ink: #0b0b10;

  --radius-lg: 28px;
  --radius-md: 18px;
  --spring: cubic-bezier(.34, 1.56, .64, 1);
}
@media (prefers-color-scheme: dark) {
  :root {
    --ink: #f4f4f7;
    --ink-2: #c9c9d3;
    --page: #0d0b16;
    --glass-fill: rgb(22 20 32 / 0.64);     /* >= 0.62 for --ink at 4.5:1 */
    --glass-edge: rgb(255 255 255 / 0.14);
    --glass-rim: rgb(255 255 255 / 0.35);
    --glass-solid: rgb(24 22 32 / 0.97);
    --glass-shadow: 0 10px 30px rgb(0 0 0 / 0.45), 0 1px 2px rgb(0 0 0 / 0.3);
    --lg-fill: rgb(30 30 40 / 0.50);        /* >= 0.48 keeps white icons at 3:1 */
    --lg-ink: #ffffff;
  }
}
```

Rules of thumb from the contrast script (flat backdrop, sRGB blending):
- Black text needs a white fill of at least 46 % opacity; `#111114` needs 49 %.
- White text needs a black fill of at least 54 %; a near-black `rgb(22 20 32)` needs 62 %.
- Icons (3:1) get away with less: about 37 % white behind black icons, 48 % dark behind white icons.
- A 10-20 % fill, the usual glassmorphism tutorial value, fails over one of the two extremes every time.

## 3. Frosted surface

```css
.glass {
  position: relative;
  background: var(--glass-fill);
  -webkit-backdrop-filter: var(--glass-optics);   /* Safari < 18 */
  backdrop-filter: var(--glass-optics);
  border: 1px solid var(--glass-edge);
  border-radius: var(--radius-lg);
  box-shadow: var(--glass-shadow), inset 0 1px 0 var(--glass-rim);
  color: var(--ink);
}
/* No backdrop-filter at all: use the solid fill so text stays legible */
@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {
  .glass, .lg { background: var(--glass-solid); }
}
```

If you support Safari 17 or older, test the prefixed declaration with `var()` values on a real device; write literal values there if it does not apply.

Blur radius: 12-20 px for panels, up to 30 px over photos and video. Bigger surfaces read as thicker, so give them more blur and a deeper shadow than small chips.

## 4. Edge light and grain

```css
/* Grain: 3 % noise reads as material and hides gradient banding */
.glass::after {
  content: ""; position: absolute; inset: 0; border-radius: inherit; pointer-events: none;
  opacity: .035; mix-blend-mode: overlay;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}

/* Rim light: a gradient border, brighter where the light hits */
.lg::before {
  content: ""; position: absolute; inset: 0; border-radius: inherit; padding: 1px; pointer-events: none;
  background: linear-gradient(140deg, rgb(255 255 255 / .9), rgb(255 255 255 / 0) 35%,
                              rgb(255 255 255 / 0) 65%, rgb(255 255 255 / .45));
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
}
```

Masks, blend modes and filters on **pseudo-elements and children** are safe. On an **ancestor** of a glass element they break it (§12).

## 5. Liquid Glass approximation

What browsers can do:

| Liquid Glass trait | Web equivalent | Reach |
|---|---|---|
| Rim highlight, specular edge | Inset shadows + gradient rim | All engines |
| Light blur, saturation lift | `backdrop-filter: blur() saturate() brightness()` | All engines |
| Lensing at the edge | SVG `feDisplacementMap` in `backdrop-filter: url()` | Chromium only |
| Adaptive light/dark ink for small elements | Needs the backdrop's luminance; CSS cannot read it | Only when the app knows what is behind (for example a known dark video) |
| Refraction of content outside the shape | Not possible: `backdrop-filter` only sees inside the element's box | None |
| Morphing and merging shapes | View Transitions or FLIP animations of separate elements | All engines, approximate |

Because the ink cannot adapt, the web version needs a heavier fill than Apple's (about 40 % instead of near-clear) to keep icons at 3:1. Say so when presenting it.

### Surface

```css
.lg {
  position: relative;
  background: var(--lg-fill);
  -webkit-backdrop-filter: var(--lg-optics);
  backdrop-filter: var(--lens,) var(--lg-optics);   /* --lens = url(#lens-N), set by JS in Chromium */
  border-radius: 999px;
  color: var(--lg-ink);
  box-shadow:
    0 8px 24px rgb(0 0 0 / 0.18),             /* lift */
    inset 0 1px 1px rgb(255 255 255 / 0.75),  /* top specular */
    inset 0 -1px 1px rgb(255 255 255 / 0.25), /* bottom bounce light */
    inset 0 0 0 1px rgb(255 255 255 / 0.18);  /* rim */
}
```

`var(--lens,)` has an empty fallback, so the declaration stays valid where no lens is set.

### Lens refraction (Chromium)

A per-element displacement map: neutral (128, 128) in the flat centre, pushing samples inward across a bezel near the rounded edge. The backdrop then bends at the rim like the edge of a thick lens. Red drives x, green drives y; `feDisplacementMap` moves each pixel by `scale × (channel − 0.5)`.

```js
function lensMap(w, h, radius, bezel) {
  const c = document.createElement("canvas");
  c.width = w; c.height = h;
  const ctx = c.getContext("2d");
  const img = ctx.createImageData(w, h);
  const d = img.data;
  const r = Math.min(radius, w / 2, h / 2);
  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
      const px = x + 0.5 - w / 2, py = y + 0.5 - h / 2;
      const qx = Math.abs(px) - (w / 2 - r), qy = Math.abs(py) - (h / 2 - r);
      // signed distance to the rounded rect (negative inside)
      const dist = Math.hypot(Math.max(qx, 0), Math.max(qy, 0)) + Math.min(Math.max(qx, qy), 0) - r;
      const inset = -dist;
      let nx = 0, ny = 0, m = 0;
      if (inset > 0 && inset < bezel) {
        if (qx > 0 && qy > 0) { const l = Math.hypot(qx, qy); nx = qx / l; ny = qy / l; }
        else if (qx > qy) nx = 1; else ny = 1;
        nx *= Math.sign(px) || 1; ny *= Math.sign(py) || 1;
        const t = 1 - inset / bezel;  // 1 at the edge, 0 where the flat centre starts
        m = t * t;                     // steeper toward the rim
      }
      const i = (y * w + x) * 4;
      d[i] = 128 - nx * m * 127;       // R drives x: sample inward
      d[i + 1] = 128 - ny * m * 127;   // G drives y
      d[i + 2] = 128; d[i + 3] = 255;
    }
  }
  ctx.putImageData(img, 0, 0);
  return c.toDataURL();
}
```

Wiring (abridged; the demo has the full version with settings listeners):

```js
const isChromium = !!navigator.userAgentData?.brands?.some(b => /Chromium/i.test(b.brand));
// lensAllowed() = isChromium && not reduced transparency && not more contrast && not forced colours

function applyLens(el, { bezel = 14, scale = 24 } = {}) {
  // on resize: build <filter id="lens-N" color-interpolation-filters="sRGB">
  //   <feImage href={lensMap(w, h, borderRadius, bezel)} x="0" y="0" width={w} height={h} result="map"/>
  //   <feDisplacementMap in="SourceGraphic" in2="map" scale={scale} xChannelSelector="R" yChannelSelector="G"/>
  // </filter>
  // then el.style.setProperty("--lens", "url(#lens-N)")
}
```

Tuning:
- `bezel` is how far in from the edge the bending reaches. Keep it under about half the element's height, or the whole pill warps and looks like water instead of glass.
- `scale` is the maximum shift in px (`scale / 2` each way). 20-30 suits a 60 px toolbar.
- The map must match the element's size, so rebuild it in a `ResizeObserver`. Animating `scale` is cheap; changing size or shape regenerates the map.
- Set `color-interpolation-filters="sRGB"` or the map values are read through a colour conversion and the displacement drifts.
- Use `navigator.userAgentData` or another engine check, not `CSS.supports`, to gate the lens (§1).

Libraries exist (React components and WebGL renderers that snapshot the page). Check how each handles scrolling, video, dynamic content and accessibility settings before adopting one, and keep the CSS fallback either way.

## 6. Scroll edge effect

Put the blur on its own layer and mask that layer, so the blur fades out while the title stays sharp.

```css
.app-header { position: sticky; top: 0; z-index: 10; }
.app-header::before {
  content: ""; position: absolute; inset: 0 0 -28px 0; z-index: -1; pointer-events: none;
  -webkit-backdrop-filter: blur(12px) saturate(160%);
  backdrop-filter: blur(12px) saturate(160%);
  background: linear-gradient(to bottom, color-mix(in srgb, var(--page) 70%, transparent), transparent);
  -webkit-mask-image: linear-gradient(to bottom, #000 55%, transparent);
  mask-image: linear-gradient(to bottom, #000 55%, transparent);
}
```

A mask on the element that *has* the backdrop filter fades the blur correctly (checked in Chromium). For a "hard" edge (a toolbar plus pinned column headers), drop the mask and extend the layer over both.

## 7. Floating toolbars and tab bars

```css
.dock {
  position: fixed; left: 50%; bottom: max(16px, env(safe-area-inset-bottom));
  transform: translateX(-50%);          /* transform on an ancestor is safe */
  display: flex; gap: 10px; align-items: center; z-index: 20;
}
.toolbar { display: flex; gap: 2px; padding: 6px; }
.lg-btn {
  appearance: none; border: 0; background: transparent; color: inherit; cursor: pointer;
  width: 48px; height: 48px; border-radius: 999px; display: grid; place-items: center;
  transition: transform 420ms var(--spring), background-color 200ms ease;
}
/* The one tinted element */
.lg.primary { width: 60px; height: 60px; display: grid; place-items: center;
              background: rgb(10 132 255 / .78); color: #fff; }
```

- Concentric shapes: inner radius = outer radius − padding. Capsules (`999px`) inside capsules are concentric automatically.
- Group related actions on one shared background; give a separate action its own capsule.
- Hit targets of at least 44-48 px. Pad the page bottom so the last content can scroll clear of the dock.
- Label every icon button (`aria-label`).

## 8. Menus and popovers

```css
.menu {
  position: fixed; left: 50%; bottom: calc(max(16px, env(safe-area-inset-bottom)) + 76px);
  translate: -50% 0; z-index: 21;
  border-radius: var(--radius-md); padding: 6px; min-width: 220px;
  transform-origin: 70% 100%;           /* grow from the button that opened it */
  transition: opacity 220ms ease, scale 360ms var(--spring), filter 260ms ease, visibility 0s;
}
/* Stay rendered so it can animate out, but hidden from focus and screen readers */
.menu[hidden] {
  display: block; visibility: hidden; opacity: 0; scale: .6; filter: blur(10px); pointer-events: none;
  transition: opacity 160ms ease, scale 200ms ease, filter 160ms ease, visibility 0s 200ms;
}
```

- Make the menu a **sibling** of the toolbar, never a child. Inside a backdrop-filtered parent it would blur only the parent (§12).
- Elements in the top layer (`popover`, `<dialog>` opened modally) see the whole page as their backdrop, which also avoids the problem.
- Move focus into the menu on open, close on Escape and outside click, and return focus to the trigger. The `visibility` transition keeps the closed menu out of the tab order.

## 9. Press and materialize motion

```css
.lg-btn:hover  { background: rgb(255 255 255 / .16); }
.lg-btn:active { transform: scale(1.12); background: rgb(255 255 255 / .28); transition-duration: 120ms; }

@media (prefers-reduced-motion: reduce) {
  .lg-btn, .menu { transition: opacity 150ms ease; }
  .lg-btn:active { transform: none; }
  .menu[hidden] { scale: 1; filter: none; }
}
```

- Press: grow slightly and brighten fast, settle with a small overshoot.
- Materialize: scale + blur + opacity together, from the trigger's position.
- Morph between related controls with View Transitions (`view-transition-name` on the source and target) where supported; otherwise a FLIP animation.
- Animate `transform`, `opacity` and the element's own `filter`. Avoid animating `backdrop-filter` radius on large surfaces; crossfade two layers instead.

## 10. Accessibility hooks

Every effect switches off through tokens, from the OS setting or an in-app setting (needed because WebKit and Firefox do not expose reduced transparency).

```css
/* Reduced transparency: OS setting OR in-app toggle */
@media (prefers-reduced-transparency: reduce) {
  :root:not([data-transparency="full"]) {
    --glass-fill: var(--glass-solid); --glass-optics: none;
    --lg-fill: var(--glass-solid);    --lg-optics: none;
  }
}
:root[data-transparency="reduced"] {
  --glass-fill: var(--glass-solid); --glass-optics: none;
  --lg-fill: var(--glass-solid);    --lg-optics: none;
}

/* Increased contrast: solid surface, hard border, full-strength ink */
@media (prefers-contrast: more) {
  :root:not([data-contrast="normal"]) {
    --glass-fill: var(--glass-solid); --glass-optics: none;
    --lg-fill: var(--glass-solid);    --lg-optics: none;
    --glass-edge: var(--ink); --ink-2: var(--ink);
  }
  :root:not([data-contrast="normal"]) .lg { box-shadow: none; outline: 1.5px solid var(--ink); }
}

/* Forced colours: system colours, no filters */
@media (forced-colors: active) {
  .glass, .lg, .app-header::before { -webkit-backdrop-filter: none; backdrop-filter: none; background: Canvas; }
  .glass, .lg { border: 1px solid CanvasText; }
}

/* Focus ring that survives any backdrop: dark ring + light halo */
.lg-btn:focus-visible { outline: 2px solid #000; outline-offset: 2px; box-shadow: 0 0 0 5px #fff; }
```

The JS lens must also turn off in these modes; the demo's `lensAllowed()` checks all of them and listens for changes. Persist the in-app setting with the app's own preference storage.

## 11. Tailwind

Tailwind v4 has `backdrop-blur-*`, `backdrop-saturate-*`, `contrast-more:`, `motion-reduce:` and `dark:`. Add a variant for reduced transparency that covers both the OS setting and the in-app attribute (v4 `@custom-variant` block syntax; not compiled as part of this skill's checks, so build once to confirm):

```css
@custom-variant reduce-transparency {
  @media (prefers-reduced-transparency: reduce) { @slot; }
  &:where([data-transparency="reduced"] *) { @slot; }
}
```

```html
<nav class="rounded-full border border-white/50 bg-white/55 shadow-lg backdrop-blur-xl backdrop-saturate-150
            reduce-transparency:bg-white/95 reduce-transparency:backdrop-blur-none
            contrast-more:bg-white contrast-more:backdrop-blur-none contrast-more:border-black
            dark:bg-zinc-900/65 dark:border-white/15">
```

Keep the fill opacity from §2 (`bg-white/55`, not `bg-white/10`). Keep the plain-CSS `@supports not (...)` fallback from §3 for engines without `backdrop-filter`. Put repeated stacks in a component or `@utility` rather than copying class strings.

## 12. Gotchas

**Backdrop root.** A `backdrop-filter` can only see content inside its nearest ancestor that isolates rendering. Checked in Chromium 156:

| Ancestor of the glass element has | Blur still works? |
|---|---|
| nothing special | yes |
| `opacity: .99` | **no**, glass shows only its own fill |
| `filter: brightness(1)` (even a no-op filter) | **no** |
| `will-change: opacity` | **no** |
| `transform: translateZ(0)` | yes |
| `backdrop-filter` (glass inside glass) | **no**, the inner pane only sees the outer pane |
| `mask-image` on the blur layer itself | yes, the blur fades with the mask |

Per the Filter Effects Level 2 spec, `mask`, `clip-path`, `mix-blend-mode` and the root element also start a new backdrop root. Common traps: animation libraries that fade a wrapper's opacity on enter, `will-change` added "for performance", and a menu placed inside a glass toolbar.

**Other traps**
- Over flat white, glass is just grey. Check that something meaningful sits behind every glass surface in every state, including empty states.
- `backdrop-filter` only samples inside the element's border box; refraction cannot pull in content from outside it.
- `@supports` reports `url()` backdrop filters as supported in WebKit even though they do not render.
- Some automated WebKit builds do not paint `backdrop-filter`, so their screenshots are not evidence of how Safari looks.
- Text on a composited layer may lose subpixel antialiasing; use weight 500+ for body text on glass.
- `position: fixed` glass over a long scrolling page re-blurs on every scroll frame (§13).

## 13. Performance

- Each glass surface re-samples and filters its backdrop whenever anything behind it changes. Cost grows with blur radius × area × number of surfaces.
- Budget: a few glass surfaces visible at once (bars, one floating panel, an open menu). Never one per list row or card.
- Keep blur radius moderate on large or fixed surfaces; prefer more fill over more blur for legibility.
- For static backgrounds (a hero image), pre-blur the image region and skip `backdrop-filter` entirely.
- Do not animate blur radius on large areas; animate opacity or transform of a pre-filtered layer.
- The SVG lens adds a displacement pass and a data-URL image per element; keep it to the main toolbar.
- Measure: browser performance panel, paint flashing and layer borders while scrolling, on a mid-range phone, not only on a desktop.
- For dropped frames beyond this, use the animation-performance skill.
