"""Shared helpers for the pptx-deck skill scripts.

Everything here is import-safe (no work is done at import time except path
constants) and is used by build_deck.py, validate_spec.py, preview_styles.py
and by the editing / QA / template tools built in later slices.

Units
-----
* Slide geometry inside python-pptx is in EMU (914400 per inch, 12700 per pt).
* Layout code in this skill thinks in *design inches* on a 13.333 x 7.5 in
  canvas (16:9) or 10 x 7.5 in canvas (4:3).
* Text-fit helpers take inches and points.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import sys
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, NamedTuple, Optional, Sequence, Tuple

# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------

SCRIPTS_DIR: Path = Path(__file__).resolve().parent
SKILL_ROOT: Path = SCRIPTS_DIR.parent
REFERENCES_DIR: Path = SKILL_ROOT / "references"
SCHEMA_PATH: Path = REFERENCES_DIR / "deck-spec.schema.json"
THEMES_PATH: Path = REFERENCES_DIR / "themes.json"
EXAMPLES_DIR: Path = REFERENCES_DIR / "examples"

EMU_PER_INCH = 914400
EMU_PER_PT = 12700

# --------------------------------------------------------------------------
# Python / dependency guard
# --------------------------------------------------------------------------


def require_pptx() -> None:
    """Exit with a helpful message when python-pptx or lxml is missing."""
    try:
        import pptx  # noqa: F401
        import lxml  # noqa: F401
    except ImportError as exc:  # pragma: no cover - environment dependent
        sys.stderr.write(
            "Missing dependency (%s). Install with: pip3 install -r %s\n"
            % (exc, SKILL_ROOT / "requirements.txt")
        )
        raise SystemExit(2)


# --------------------------------------------------------------------------
# JSON / schema / themes
# --------------------------------------------------------------------------


def load_json(path: Path | str) -> Any:
    """Read a UTF-8 JSON file and return the parsed value."""
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


@lru_cache(maxsize=1)
def load_schema() -> Dict[str, Any]:
    """Return the deck-spec JSON schema (references/deck-spec.schema.json)."""
    return load_json(SCHEMA_PATH)


@lru_cache(maxsize=1)
def _themes_blob() -> Dict[str, Any]:
    return load_json(THEMES_PATH)


def load_themes() -> List[Dict[str, Any]]:
    """Return the list of theme dicts from references/themes.json (file order)."""
    return list(_themes_blob()["themes"])


def theme_ids() -> List[str]:
    """Return all theme ids in file order."""
    return [t["id"] for t in load_themes()]


def get_theme(theme_id: str) -> Dict[str, Any]:
    """Return one theme dict by id; raise KeyError listing valid ids if unknown."""
    for t in load_themes():
        if t["id"] == theme_id:
            return t
    raise KeyError("Unknown theme %r. Valid ids: %s" % (theme_id, ", ".join(theme_ids())))


def accent_text_allowed(theme: Dict[str, Any]) -> bool:
    """True when the theme's accent colour may be used for text on the paper background.

    Uses ``accentTextAllowed`` when present, otherwise treats
    ``accentUsage == "fill-only"`` as not allowed and everything else as allowed.
    """
    if "accentTextAllowed" in theme and theme["accentTextAllowed"] is not None:
        return bool(theme["accentTextAllowed"])
    return theme.get("accentUsage") != "fill-only"


def role_limits() -> Dict[str, Dict[str, Any]]:
    """Return ``x-roleLimits`` from the schema (role -> limits dict)."""
    return load_schema()["x-roleLimits"]


def typography_limits() -> Dict[str, Any]:
    """Return ``x-typography`` (minPt per kind, hero ratio) from the schema."""
    return load_schema()["x-typography"]


def density_cap(density: str, role: str) -> int:
    """Effective maximum item count for *role* at the deck's *density*.

    ``min(x-roleLimits[role].maxItems, density maxItems)`` for list-like roles,
    plain role maxItems for the others.
    """
    schema = load_schema()
    role_max = role_limits()[role]["maxItems"]
    dens = schema["x-densityLimits"]
    if role in dens["listLikeRoles"]:
        return min(role_max, dens.get(density or "speaker-led", dens["speaker-led"])["maxItems"])
    return role_max


def short_limit(full_cap: int) -> int:
    """Maximum length of a ``short`` text given the full-text cap (60 percent, floored)."""
    return int(math.floor(full_cap * 0.6))


# --------------------------------------------------------------------------
# Colour helpers
# --------------------------------------------------------------------------


def normalize_hex(value: str) -> str:
    """Return ``RRGGBB`` upper-case without ``#`` from ``#rgb``, ``#rrggbb`` or ``rrggbb``."""
    v = value.strip().lstrip("#")
    if len(v) == 3:
        v = "".join(c * 2 for c in v)
    if not re.fullmatch(r"[0-9a-fA-F]{6}", v):
        raise ValueError("Not a hex colour: %r" % value)
    return v.upper()


def hex_to_rgb(value: str):
    """Convert a hex colour string to a ``pptx.dml.color.RGBColor``."""
    from pptx.dml.color import RGBColor

    return RGBColor.from_string(normalize_hex(value))


def hex_to_tuple(value: str) -> Tuple[int, int, int]:
    """Convert a hex colour string to an ``(r, g, b)`` tuple of ints."""
    v = normalize_hex(value)
    return int(v[0:2], 16), int(v[2:4], 16), int(v[4:6], 16)


def tuple_to_hex(rgb: Sequence[float]) -> str:
    """Convert an ``(r, g, b)`` tuple to ``RRGGBB`` upper-case hex."""
    return "%02X%02X%02X" % tuple(max(0, min(255, int(round(c)))) for c in rgb)


def mix_hex(a: str, b: str, t: float) -> str:
    """Linear blend: ``t`` = 0 returns *a*, ``t`` = 1 returns *b*."""
    ra, rb = hex_to_tuple(a), hex_to_tuple(b)
    return tuple_to_hex([ra[i] + (rb[i] - ra[i]) * t for i in range(3)])


def relative_luminance(value: str) -> float:
    """WCAG relative luminance (0 black .. 1 white) of a hex colour."""

    def chan(c: int) -> float:
        s = c / 255.0
        return s / 12.92 if s <= 0.03928 else ((s + 0.055) / 1.055) ** 2.4

    r, g, b = hex_to_tuple(value)
    return 0.2126 * chan(r) + 0.7152 * chan(g) + 0.0722 * chan(b)


def contrast_ratio(a: str, b: str) -> float:
    """WCAG contrast ratio between two hex colours (1 .. 21)."""
    la, lb = relative_luminance(a), relative_luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


# --------------------------------------------------------------------------
# Unit helpers
# --------------------------------------------------------------------------


def inches_to_emu(inches: float) -> int:
    """Inches to integer EMU."""
    return int(round(inches * EMU_PER_INCH))


def emu_to_inches(emu: float) -> float:
    """EMU to inches."""
    return emu / EMU_PER_INCH


def pt_to_emu(pt: float) -> int:
    """Points to integer EMU."""
    return int(round(pt * EMU_PER_PT))


def emu_to_pt(emu: float) -> float:
    """EMU to points."""
    return emu / EMU_PER_PT


def slide_size(aspect: str = "16:9") -> Tuple[float, float]:
    """Slide ``(width_in, height_in)`` for an aspect: 16:9 -> 13.333 x 7.5, 4:3 -> 10 x 7.5."""
    if aspect == "4:3":
        return 10.0, 7.5
    if aspect in (None, "16:9"):
        return 40.0 / 3.0, 7.5
    raise ValueError("Unsupported aspect %r (use '16:9' or '4:3')" % aspect)


def slide_size_emu(aspect: str = "16:9") -> Tuple[int, int]:
    """Slide ``(width, height)`` in EMU for an aspect (16:9 = 12192000 x 6858000)."""
    w, h = slide_size(aspect)
    return int(round(w * EMU_PER_INCH)), int(round(h * EMU_PER_INCH))


# --------------------------------------------------------------------------
# Shape geometry
# --------------------------------------------------------------------------


def iter_shapes(shapes: Iterable[Any]) -> Iterator[Any]:
    """Yield every shape in *shapes*, descending into group shapes."""
    for shp in shapes:
        yield shp
        if shp.__class__.__name__ == "GroupShape":
            yield from iter_shapes(shp.shapes)


def shape_bounds(shape: Any) -> Optional[Tuple[int, int, int, int]]:
    """Return ``(left, top, right, bottom)`` in EMU, or None when the shape inherits its position."""
    try:
        l, t, w, h = shape.left, shape.top, shape.width, shape.height
    except Exception:
        return None
    if l is None or t is None or w is None or h is None:
        return None
    return int(l), int(t), int(l) + int(w), int(t) + int(h)


def is_out_of_bounds(shape: Any, slide_w: int, slide_h: int, tolerance: float = 0.02) -> bool:
    """True when the shape's box extends beyond the slide.

    ``slide_w`` and ``slide_h`` are in EMU; ``tolerance`` is the allowed overshoot
    in inches (default 0.02 in absorbs EMU rounding on full-bleed shapes).
    Shapes without explicit geometry (inherited placeholders) are never flagged.
    """
    b = shape_bounds(shape)
    if b is None:
        return False
    tol = int(tolerance * EMU_PER_INCH)
    l, t, r, btm = b
    return l < -tol or t < -tol or r > slide_w + tol or btm > slide_h + tol


def list_out_of_bounds(prs: Any, tolerance: float = 0.02) -> List[Tuple[int, str, Tuple[int, int, int, int]]]:
    """Return ``(slide_number, shape_name, bounds)`` for every shape outside its slide (1-based numbers)."""
    out = []
    for i, slide in enumerate(prs.slides, start=1):
        for shp in iter_shapes(slide.shapes):
            if is_out_of_bounds(shp, prs.slide_width, prs.slide_height, tolerance):
                out.append((i, shp.name, shape_bounds(shp)))
    return out


# --------------------------------------------------------------------------
# Text-size estimation (heuristic, no font metrics)
# --------------------------------------------------------------------------

LATIN_CHAR_EM = 0.5  # average Latin glyph advance, in em (0.5 * point size)
CJK_CHAR_EM = 1.0  # CJK glyph advance, in em
DEFAULT_LINE_SPACING = 1.2


class TextCapacity(NamedTuple):
    """Result of :func:`estimate_text_capacity`."""

    chars_per_line: int
    max_lines: int
    max_chars: int


def _is_wide(ch: str) -> bool:
    return unicodedata.east_asian_width(ch) in ("W", "F")


def char_advance_em(ch: str, latin_em: float = LATIN_CHAR_EM) -> float:
    """Advance width of one character in em: ``latin_em`` for Latin, 1.0 for CJK, ``latin_em`` otherwise."""
    return CJK_CHAR_EM if _is_wide(ch) else latin_em


def estimate_text_capacity(
    width_in: float,
    height_in: float,
    font_pt: float,
    line_spacing: float = DEFAULT_LINE_SPACING,
    char_em: float = LATIN_CHAR_EM,
) -> TextCapacity:
    """Estimate how much Latin text a box holds.

    Average character width is ``char_em * font_pt`` points (0.5 by default for
    Latin; CJK text needs 1.0 and is handled by :func:`measure_text`). Returns
    characters per line, number of lines and their product.
    """
    if width_in <= 0 or height_in <= 0 or font_pt <= 0:
        return TextCapacity(0, 0, 0)
    cpl = int((width_in * 72.0) // (char_em * font_pt))
    lines = int((height_in * 72.0) // (font_pt * line_spacing))
    return TextCapacity(cpl, lines, cpl * lines)


def count_lines(text: str, width_in: float, font_pt: float, char_em: float = LATIN_CHAR_EM) -> int:
    """Simulate word wrap and return the number of lines *text* occupies.

    Explicit newlines start new lines. Words longer than the line are broken.
    Latin advance is ``char_em`` em, CJK 1.0 em.
    """
    width_pt = width_in * 72.0
    if width_pt <= 0 or font_pt <= 0:
        return max(1, text.count("\n") + 1)
    space_w = char_em * font_pt
    total = 0
    for para in text.split("\n"):
        lines = 1
        cur = 0.0
        for word in para.split(" "):
            if word == "":
                cur += space_w
                continue
            w = sum(char_advance_em(c, char_em) for c in word) * font_pt
            if cur == 0.0:
                cur = w
            elif cur + space_w + w <= width_pt:
                cur += space_w + w
            else:
                lines += 1
                cur = w
            if cur > width_pt:  # word wider than a line: hard break
                extra = int(cur // width_pt)
                lines += extra
                cur = cur - extra * width_pt
        total += lines
    return total


def measure_text(
    text: str,
    width_in: float,
    font_pt: float,
    line_spacing: float = DEFAULT_LINE_SPACING,
    char_em: float = LATIN_CHAR_EM,
) -> Tuple[int, float]:
    """Return ``(lines, height_in)`` needed for *text* at *font_pt* in a box *width_in* wide."""
    n = count_lines(text, width_in, font_pt, char_em)
    return n, n * font_pt * line_spacing / 72.0


def text_fits(
    text: str,
    width_in: float,
    height_in: float,
    font_pt: float,
    line_spacing: float = DEFAULT_LINE_SPACING,
    char_em: float = LATIN_CHAR_EM,
) -> bool:
    """Heuristic: does *text* fit a ``width_in x height_in`` box at *font_pt*?

    The box dimensions are the usable text area (insets already subtracted).
    """
    _, needed = measure_text(text, width_in, font_pt, line_spacing, char_em)
    return needed <= height_in + 1e-6


def paragraphs_height(
    paragraphs: Sequence[Tuple[str, float, float]],
    width_in: float,
    line_spacing: float = DEFAULT_LINE_SPACING,
    char_em: float = LATIN_CHAR_EM,
) -> float:
    """Height in inches for ``(text, font_pt, space_before_pt)`` paragraphs stacked in one box."""
    total = 0.0
    for text, pt, before in paragraphs:
        _, h = measure_text(text, width_in, pt, line_spacing, char_em)
        total += h + before / 72.0
    return total


def _frame_insets_in(text_frame: Any) -> Tuple[float, float, float, float]:
    """(left, top, right, bottom) text insets in inches from a text frame (python-pptx defaults if unset)."""
    try:
        bp = text_frame._txBody.bodyPr
    except Exception:
        return 0.1, 0.05, 0.1, 0.05

    def val(name: str, default: int) -> float:
        raw = bp.get(name)
        return (int(raw) if raw is not None else default) / EMU_PER_INCH

    return val("lIns", 91440), val("tIns", 45720), val("rIns", 91440), val("bIns", 45720)


def text_frame_demand(shape: Any, line_spacing: float = DEFAULT_LINE_SPACING) -> Optional[Tuple[float, float]]:
    """Return ``(needed_in, available_in)`` text height for a shape's text frame, or None without text.

    Uses each run's explicit font size (18 pt when unset), the shape's width minus
    insets, and the heuristic average glyph width. Only paragraphs with text count.
    """
    if not getattr(shape, "has_text_frame", False) or not shape.has_text_frame:
        return None
    tf = shape.text_frame
    if not tf.text.strip():
        return None
    b = shape_bounds(shape)
    if b is None:
        return None
    li, ti, ri, bi = _frame_insets_in(tf)
    width_in = (b[2] - b[0]) / EMU_PER_INCH - li - ri
    avail = (b[3] - b[1]) / EMU_PER_INCH - ti - bi
    needed = 0.0
    for p in tf.paragraphs:
        text = "".join(r.text for r in p.runs)
        sizes = [r.font.size.pt for r in p.runs if r.font.size is not None]
        pt = max(sizes) if sizes else 18.0
        if not text:
            needed += pt * line_spacing / 72.0
            continue
        _, h = measure_text(text, width_in, pt, line_spacing)
        needed += h
        if p.space_before is not None:
            needed += p.space_before.pt / 72.0
        if p.space_after is not None:
            needed += p.space_after.pt / 72.0
    return needed, avail


def list_text_overflows(prs: Any, tolerance_in: float = 0.05) -> List[Tuple[int, str, float, float]]:
    """Return ``(slide_number, shape_name, needed_in, available_in)`` for text frames estimated to overflow."""
    out = []
    for i, slide in enumerate(prs.slides, start=1):
        for shp in iter_shapes(slide.shapes):
            d = text_frame_demand(shp)
            if d and d[0] > d[1] + tolerance_in:
                out.append((i, shp.name, round(d[0], 2), round(d[1], 2)))
    return out


# --------------------------------------------------------------------------
# Variants
# --------------------------------------------------------------------------

#: For each role, the layout variants that can show a chart (1-based).
CHART_VARIANTS: Dict[str, Tuple[int, ...]] = {
    "metrics": (1, 3),
    "trend": (2, 3),
    "comparison": (3,),
    "distribution": (1, 2, 3),
    "observation": (2,),
    "result": (3,),
}

#: Variants that cannot render without a chart.
CHART_REQUIRED_VARIANTS: Dict[str, Tuple[int, ...]] = {
    "trend": (2,),
    "comparison": (3,),
}


def stable_variant(seed: str, index: int, n: int) -> int:
    """Stable 1-based variant number: ``(sha256(seed + ':' + index) mod n) + 1``.

    ``index`` is the 0-based position of the slide in ``spec["slides"]``.
    Never uses Python's randomised ``hash()``; same inputs give the same answer on every machine.
    """
    if n <= 1:
        return 1
    digest = hashlib.sha256(("%s:%d" % (seed, index)).encode("utf-8")).hexdigest()
    return int(digest, 16) % n + 1


def resolve_variant(spec: Dict[str, Any], index: int) -> int:
    """Layout variant (1-based) for ``spec["slides"][index]``.

    ``layoutVariant`` wins. Otherwise ``stable_variant(randomSeed, index, variants)``;
    when the slide has a chart (or none) and the hashed variant cannot show it
    (or requires one), the choice is made among the compatible variants instead,
    using the same hash, so charts are never silently dropped.
    """
    slide = spec["slides"][index]
    role = slide["role"]
    n = role_limits()[role]["variants"]
    if slide.get("layoutVariant"):
        return int(slide["layoutVariant"])
    seed = spec.get("randomSeed", "")
    v = stable_variant(seed, index, n)
    has_chart = bool(slide.get("chart"))
    capable = CHART_VARIANTS.get(role)
    required = CHART_REQUIRED_VARIANTS.get(role, ())
    if has_chart and capable and v not in capable:
        return capable[(v - 1) % len(capable)]
    if not has_chart and v in required:
        others = [x for x in range(1, n + 1) if x not in required]
        return others[(v - 1) % len(others)]
    return v


# --------------------------------------------------------------------------
# Fonts
# --------------------------------------------------------------------------

_FONT_DIRS = [
    "~/Library/Fonts",
    "/Library/Fonts",
    "/System/Library/Fonts",
    "/System/Library/Fonts/Supplemental",
    "/Applications/Microsoft PowerPoint.app/Contents/Resources/DFonts",
    "/Applications/Microsoft Word.app/Contents/Resources/DFonts",
    "/usr/share/fonts",
    "/usr/local/share/fonts",
    "~/.fonts",
    "~/.local/share/fonts",
    "C:\\Windows\\Fonts",
]

#: Fonts every Office install ships; treated as available even when no file is found.
_ASSUMED_FONTS = {"calibri", "arial", "times new roman", "courier new", "georgia", "cambria", "consolas", "segoe ui", "trebuchet ms", "verdana", "tahoma", "impact"}


def _norm_font(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


@lru_cache(maxsize=1)
def _installed_font_keys() -> Tuple[str, ...]:
    keys = set()
    for d in _FONT_DIRS:
        root = Path(os.path.expanduser(d))
        if not root.is_dir():
            continue
        try:
            for dirpath, _dirs, files in os.walk(root):
                for f in files:
                    if f.lower().endswith((".ttf", ".otf", ".ttc", ".otc", ".fon", ".dfont")):
                        keys.add(_norm_font(Path(f).stem))
        except OSError:
            continue
    return tuple(sorted(keys))


def font_available(name: str, assume_office: bool = False) -> bool:
    """Best-effort check whether a font family is installed on this machine.

    Scans common macOS / Linux / Windows font directories and matches the
    normalised family name against file names (``Segoe UI`` matches ``segoeui.ttf``).
    With ``assume_office=True`` the classic Office fonts (Calibri, Arial, Georgia,
    ...) count as present even if no file is found. Returns False for empty names.
    """
    if not name:
        return False
    key = _norm_font(name)
    if assume_office and name.lower() in _ASSUMED_FONTS:
        return True
    keys = _installed_font_keys()
    return any(k == key or k.startswith(key) for k in keys)


def resolve_font(fontspec: Any) -> str:
    """Return the family name to write into a deck for a theme font spec.

    *fontspec* is ``{"name": ..., "fallback": ...}`` (or a plain string). The
    preferred name is used when installed here, otherwise the fallback.
    """
    if isinstance(fontspec, str):
        return fontspec
    name = fontspec.get("name", "")
    fallback = fontspec.get("fallback") or name
    if font_available(name):
        return name
    return fallback


# --------------------------------------------------------------------------
# Spec text helpers
# --------------------------------------------------------------------------


def spec_date(spec: Dict[str, Any]) -> Tuple[int, int, int]:
    """Date ``(year, month, day)`` encoded in randomSeed (``<theme>-YYYYMMDD-abc``); 2000-01-01 if absent."""
    m = re.search(r"-(\d{4})(\d{2})(\d{2})-[a-z]{3}$", spec.get("randomSeed", ""))
    if m:
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if 1 <= mo <= 12 and 1 <= d <= 28 + 3:
            return y, mo, min(d, 28)
    return 2000, 1, 1


def seed_theme_prefix(seed: str) -> Optional[str]:
    """Theme id encoded in a randomSeed, or None if the seed does not match the format."""
    m = re.fullmatch(r"(.+)-\d{8}-[a-z]{3}", seed or "")
    return m.group(1) if m else None


def format_item_value(item: Dict[str, Any]) -> str:
    """Display string for an item's number: ``displayValue`` if set, else ``value`` plus ``unit``; "" if neither."""
    if item.get("displayValue"):
        return str(item["displayValue"])
    if "value" in item and item["value"] is not None:
        v = item["value"]
        s = ("%d" % v) if float(v).is_integer() else ("%g" % v)
        return s + (item.get("unit") or "")
    return ""
