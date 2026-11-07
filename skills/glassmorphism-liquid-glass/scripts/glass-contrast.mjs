#!/usr/bin/env node
// Worst-case WCAG 2.x contrast for text sitting on a translucent (glass) surface.
//
// Glass has no single background color: what shows through depends on whatever
// scrolls or sits behind it. This script composites the glass tint over a set
// of backdrop colors (by default pure white, mid gray and pure black, the
// extremes a blur cannot average away when a large flat area sits behind the
// glass) and reports the contrast of the text color against each result.
// It also finds the smallest tint opacity that keeps every backdrop at or
// above the target ratio.
//
// Usage:
//   node glass-contrast.mjs --text "#ffffff" --tint "rgba(20,20,24,0.4)"
//   node glass-contrast.mjs --text "#111" --tint "rgb(255 255 255 / 0.3)" \
//        --backdrops "#ffffff,#000000,#ff2d55,#0a84ff" --target 4.5
//
// Compositing is done in gamma-encoded sRGB, as browsers and most design tools
// do for normal alpha blending. Blur and saturate() are ignored, so treat the
// result as a floor for flat backdrops; busy backdrops average toward mid tones.

const args = Object.fromEntries(
  process.argv.slice(2).reduce((pairs, token, i, all) => {
    if (token.startsWith("--")) pairs.push([token.slice(2), all[i + 1]]);
    return pairs;
  }, [])
);

if (!args.text || !args.tint || args.help !== undefined) {
  console.log(
    'Usage: node glass-contrast.mjs --text "#fff" --tint "rgba(0,0,0,0.4)" ' +
      '[--backdrops "#fff,#808080,#000"] [--target 4.5]'
  );
  process.exit(args.text && args.tint ? 0 : 1);
}

function parseColor(input) {
  const s = String(input).trim().toLowerCase();
  if (s.startsWith("#")) {
    let hex = s.slice(1);
    if (hex.length === 3 || hex.length === 4) hex = [...hex].map((c) => c + c).join("");
    if (hex.length !== 6 && hex.length !== 8) throw new Error(`Bad hex color: ${input}`);
    const n = (i) => parseInt(hex.slice(i, i + 2), 16);
    return { r: n(0), g: n(2), b: n(4), a: hex.length === 8 ? n(6) / 255 : 1 };
  }
  const m = s.match(/^rgba?\(([^)]+)\)$/);
  if (!m) throw new Error(`Unsupported color (use hex, rgb() or rgba()): ${input}`);
  const parts = m[1].split(/[\s,/]+/).filter(Boolean);
  if (parts.length < 3) throw new Error(`Bad rgb color: ${input}`);
  const channel = (v) => (v.endsWith("%") ? (parseFloat(v) / 100) * 255 : parseFloat(v));
  const alpha = parts[3] === undefined ? 1 : parts[3].endsWith("%") ? parseFloat(parts[3]) / 100 : parseFloat(parts[3]);
  return { r: channel(parts[0]), g: channel(parts[1]), b: channel(parts[2]), a: alpha };
}

const over = (top, bottom) => ({
  r: top.a * top.r + (1 - top.a) * bottom.r,
  g: top.a * top.g + (1 - top.a) * bottom.g,
  b: top.a * top.b + (1 - top.a) * bottom.b,
  a: 1,
});

function luminance({ r, g, b }) {
  const lin = (v) => {
    const c = v / 255;
    return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
  };
  return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b);
}

function contrast(a, b) {
  const [hi, lo] = [luminance(a), luminance(b)].sort((x, y) => y - x);
  return (hi + 0.05) / (lo + 0.05);
}

const toHex = ({ r, g, b }) =>
  "#" + [r, g, b].map((v) => Math.round(v).toString(16).padStart(2, "0")).join("");

const text = parseColor(args.text);
const tint = parseColor(args.tint);
const target = args.target ? parseFloat(args.target) : 4.5;
const backdrops = (args.backdrops ?? "#ffffff,#808080,#000000").split(",").map(parseColor);

function worstCase(tintAlpha) {
  const t = { ...tint, a: tintAlpha };
  let worst = Infinity;
  const rows = backdrops.map((bd) => {
    const surface = over(t, bd);
    const ink = text.a < 1 ? over(text, surface) : text;
    const ratio = contrast(ink, surface);
    worst = Math.min(worst, ratio);
    return { backdrop: toHex(bd), surface: toHex(surface), ratio };
  });
  return { rows, worst };
}

const { rows, worst } = worstCase(tint.a);
console.log(`text ${args.text} on tint ${args.tint} (alpha ${tint.a})`);
for (const row of rows) {
  const verdict = row.ratio >= 4.5 ? "AA text" : row.ratio >= 3 ? "large text / UI only" : "FAIL";
  console.log(
    `  backdrop ${row.backdrop} -> surface ${row.surface}  ${row.ratio.toFixed(2)}:1  ${verdict}`
  );
}
console.log(`worst case: ${worst.toFixed(2)}:1 (target ${target}:1) -> ${worst >= target ? "PASS" : "FAIL"}`);

// Smallest tint alpha that meets the target on every backdrop, if any does.
if (worstCase(1).worst < target) {
  console.log(`no tint opacity reaches ${target}:1 with this text color; change the text or tint color`);
} else {
  let lo = 0;
  let hi = 1;
  for (let i = 0; i < 30; i++) {
    const mid = (lo + hi) / 2;
    if (worstCase(mid).worst >= target) hi = mid;
    else lo = mid;
  }
  console.log(`minimum tint alpha for ${target}:1 on all backdrops: ${(Math.ceil(hi * 100) / 100).toFixed(2)}`);
}
