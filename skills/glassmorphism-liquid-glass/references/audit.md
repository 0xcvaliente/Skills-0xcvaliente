# Auditing a glass UI

Use this for reviews. Read the code and, when possible, render the screens over worst-case backdrops in each setting. Report only what you checked, and say which states you could not render.

## Checklist

**Placement and hierarchy**
- [ ] Every glass surface is in the floating functional layer (bars, toolbars, sidebars, menus, sheets, floating controls, media controls).
- [ ] No glass on content: cards, list rows, tables, form bodies, page backgrounds.
- [ ] No glass on glass, including menus or popovers nested inside a glass parent.
- [ ] A handful of glass surfaces per screen at most.
- [ ] Something meaningful sits behind every glass surface in every state (including empty and loading states).

**Variant and colour**
- [ ] Regular by default; clear only over media, with dimming where the media is bright and with bold foreground.
- [ ] Regular and clear are not mixed in one control group.
- [ ] Only the primary action is tinted; tints are translucent, not solid fills.
- [ ] Brand colour lives in content, not spread across chrome.

**Legibility**
- [ ] Each ink/fill pair passes the contrast script over white, mid grey, black and the relevant brand colours (4.5:1 text, 3:1 icons and control boundaries).
- [ ] Body text weight is regular or heavier; no hairline icons; no low-contrast tertiary text on thin glass.
- [ ] Scroll edge effect (fading blur or dimming) where content passes under bars, instead of hard divider lines.
- [ ] Focus ring visible over light, dark and busy backdrops.

**Settings**
- [ ] Reduced transparency gives a near-solid surface (OS setting and, on the web, an in-app setting).
- [ ] Increased contrast gives a solid surface with a border and full-strength ink.
- [ ] Forced colours removes filters and uses system colours (web).
- [ ] Reduced motion removes spring, morph and blur-in.
- [ ] Light and dark themes both pass.
- [ ] On Apple platforms, the full range of the user's Liquid Glass look setting.

**Interaction and motion**
- [ ] Press feedback is fast and settles; materialize instead of a plain fade; menus grow from their trigger.
- [ ] Menus and popovers take focus, close on Escape, return focus, and are hidden from focus when closed.

**Implementation**
- [ ] Native: system components and glass button styles before custom glass; custom glass in a container; no custom backgrounds on system bars.
- [ ] Web: no backdrop-root ancestor (`opacity < 1`, `filter`, `mask`, `clip-path`, `mix-blend-mode`, `backdrop-filter`, or `will-change` on those) above a glass element.
- [ ] Web: `-webkit-backdrop-filter` present if Safari 17 or older is supported; `@supports not` fallback to a solid fill.
- [ ] Web: SVG lens refraction gated on the engine, not on `@supports`, and turned off in the accessibility modes.

**Performance**
- [ ] No glass inside long or virtualized lists.
- [ ] Blur radius is not animated on large surfaces.
- [ ] Scrolling and transitions measured on a mid-range device.

## Anti-patterns ("glass slop")

- Purple-blue gradient blobs with a grid of 10 % white cards and 1 px white borders: glass used as decoration on content.
- White text on light glass over a light photo; "it looks fine on my wallpaper".
- Every button tinted a different colour.
- Glass toolbar with a glass search field with glass chips inside it.
- A menu inside a glass toolbar that blurs nothing because the toolbar is its backdrop root.
- An entrance animation on a wrapper's opacity that turns every glass child flat for its duration.
- Clear glass over bright media without dimming.
- A fake "liquid" wobble from `feTurbulence` across the whole surface; real lensing is strongest at the edge and calm in the centre.
- No reduced-transparency or high-contrast state at all.

## Report format

For each finding:

```text
[severity] location (file:line or screen > element)
Problem: what fails and under which condition (backdrop, setting, device).
Evidence: contrast ratio from the script, screenshot name, or the code line.
Fix: the concrete change (fill opacity to X, move menu out of the toolbar, add the prefers-contrast rule, ...).
```

Severity: **blocker** (text or controls unreadable or unreachable in some supported state), **major** (fails a stated rule in common use), **minor** (polish or consistency). Finish with what was not verified.
