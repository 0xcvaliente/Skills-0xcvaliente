"""Colour maths and token loading shared by the design scripts (standard library only)."""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
TOKENS_PATH = os.path.join(os.path.dirname(HERE), "assets", "design-tokens.json")

_HEX = re.compile(r"^#?([0-9a-fA-F]{6})$")


def parse_hex(value):
    """'#1F4E79' or '1F4E79' -> (r, g, b) ints. Raises ValueError otherwise."""
    m = _HEX.match((value or "").strip())
    if not m:
        raise ValueError(f"not a 6-digit hex colour: {value!r}")
    h = m.group(1)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def luminance(rgb):
    """WCAG relative luminance."""
    def chan(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (chan(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(fg, bg):
    """WCAG contrast ratio (1.0 to 21.0) between two hex colours."""
    a, b = luminance(parse_hex(fg)), luminance(parse_hex(bg))
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def is_large_text(size_pt, bold=False):
    """WCAG 'large text': at least 18 pt, or 14 pt and bold."""
    return size_pt is not None and (size_pt >= 18 or (bold and size_pt >= 14))


def required_ratio(size_pt=None, bold=False, level="AA"):
    large = is_large_text(size_pt, bold)
    if level == "AAA":
        return 4.5 if large else 7.0
    return 3.0 if large else 4.5


def load_tokens(path=None):
    with open(path or TOKENS_PATH, encoding="utf-8") as f:
        return json.load(f)


def resolve_color(preset, name):
    """Token colour name ('primary') or a literal hex -> hex string with '#'."""
    colors = preset["colors"]
    if name in colors:
        return colors[name]
    parse_hex(name)
    return "#" + name.lstrip("#").upper()
