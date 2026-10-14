#!/usr/bin/env python3
"""Render/check positioned diagram scenes or extract one inline SVG. No dependencies."""

import argparse
import hashlib
import html
import json
import math
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

PALETTES = {
    "light": dict(paper="#f7f4ec", surface="#ffffff", ink="#172b36",
                  muted="#50636d", rule="#7d898a", edge="#50636d",
                  accent="#be3b21", accent_surface="#fdeee6"),
    "dark": dict(paper="#13232c", surface="#1b303b", ink="#f5f1e7",
                 muted="#b5c5cb", rule="#798b95", edge="#b5c5cb",
                 accent="#ffb499", accent_surface="#512d26"),
}
# Remote font loads make exports depend on the network; system stacks need a generic fallback.
REMOTE_FONT = re.compile(
    r"fonts\.(?:googleapis|gstatic)\.com|use\.typekit\.net|fonts\.bunny\.net|"
    r"@import\s+(?:url\()?\s*['\"]?https?:|@font-face[^}]*?url\(\s*['\"]?https?:",
    re.IGNORECASE | re.DOTALL,
)
ID = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")
STATUSES = {"provided", "observed", "inferred", "proposed", "unspecified"}
EPS = 1e-6


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def luminance(color):
    values = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    values = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in values]
    return sum(v * w for v, w in zip(values, (0.2126, 0.7152, 0.0722)))


def contrast(a, b):
    low, high = sorted((luminance(a), luminance(b)))
    return (high + 0.05) / (low + 0.05)


def bounds(obj):
    return obj["x"], obj["y"], obj["x"] + obj["w"], obj["y"] + obj["h"]


def overlaps(a, b):
    return min(a[2], b[2]) > max(a[0], b[0]) + EPS and min(a[3], b[3]) > max(a[1], b[1]) + EPS


def segment_hits(a, b, rect):
    """Liang–Barsky clipping against a slightly inset rectangle; boundary contact is OK."""
    x0, y0, x1, y1 = rect
    x0, y0, x1, y1 = x0 + EPS, y0 + EPS, x1 - EPS, y1 - EPS
    low, high = 0.0, 1.0
    for start, delta, lo, hi in ((a[0], b[0] - a[0], x0, x1), (a[1], b[1] - a[1], y0, y1)):
        if abs(delta) < EPS:
            if not lo <= start <= hi:
                return False
        else:
            enter, leave = sorted(((lo - start) / delta, (hi - start) / delta))
            low, high = max(low, enter), min(high, leave)
            if low > high:
                return False
    return low <= high


def on_boundary(point, rect):
    x, y = point
    x0, y0, x1, y1 = rect
    return (x0 - EPS <= x <= x1 + EPS and y0 - EPS <= y <= y1 + EPS and
            min(abs(x - x0), abs(x - x1), abs(y - y0), abs(y - y1)) < EPS)


def text_units(text):
    return sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in text)


def wrap(text, width, font):
    """Estimate wrap by Unicode display width; browser measurements remain authoritative."""
    capacity = max(1, int(width / (font * 0.58)))
    lines, current = [], ""
    for word in str(text).split():
        if current and text_units(current + " " + word) <= capacity:
            current += " " + word
            continue
        if current:
            lines.append(current)
        current = ""
        for char in word:
            if current and text_units(current + char) > capacity:
                lines.append(current)
                current = ""
            current += char
    if current:
        lines.append(current)
    return lines or [""]


def label_box(edge):
    x, y = edge["label_at"]
    w = edge.get("label_w", 170)
    h = 12 + 18 * len(wrap(edge["label"], w - 16, 13))
    return dict(x=x, y=y, w=w, h=h)


def validate(scene):
    errors = []
    if not isinstance(scene, dict):
        return ["scene must be an object"]
    for key in ("title", "description"):
        if not isinstance(scene.get(key), str) or not scene[key].strip():
            errors.append(f"{key} must be a nonempty string")
    for key in ("width", "height"):
        if not number(scene.get(key)) or scene[key] <= 0:
            errors.append(f"{key} must be a finite positive number")
    theme = scene.get("theme", "light")
    if theme not in PALETTES:
        errors.append("theme must be light or dark")
    tokens = scene.get("tokens", {})
    if not isinstance(tokens, dict) or any(k not in PALETTES["light"] or not isinstance(v, str) or
                                         not re.fullmatch(r"#[0-9a-fA-F]{6}", v) for k, v in tokens.items()):
        errors.append("tokens must map known palette roles to six-digit hex colors")
    if not isinstance(scene.get("notes", []), list) or any(not isinstance(x, str) for x in scene.get("notes", [])):
        errors.append("notes must be a list of strings")
    seen = set()
    for kind in ("nodes", "edges", "regions"):
        items = scene.get(kind, [] if kind == "regions" else None)
        if not isinstance(items, list):
            errors.append(f"{kind} must be a list")
            continue
        for item in items:
            if not isinstance(item, dict):
                errors.append(f"{kind} entries must be objects")
                continue
            name = item.get("id")
            if not isinstance(name, str) or not ID.fullmatch(name):
                errors.append(f"invalid {kind} ID: {name!r}")
            elif name in seen:
                errors.append(f"duplicate ID: {name}")
            else:
                seen.add(name)
            for key in (("label",) if kind != "edges" else ("from", "to")):
                if not isinstance(item.get(key), str) or not item[key].strip():
                    errors.append(f"{name}: {key} must be a nonempty string")
            if kind != "edges":
                for key in ("x", "y", "w", "h"):
                    if not number(item.get(key)) or (key in ("w", "h") and item[key] <= 0):
                        errors.append(f"{name}: invalid {key}")
            else:
                pts = item.get("points")
                if not isinstance(pts, list) or len(pts) < 2 or any(
                        not isinstance(p, list) or len(p) != 2 or not all(number(v) for v in p) for p in pts):
                    errors.append(f"{name}: points must contain at least two numeric pairs")
                if item.get("style", "solid") not in ("solid", "dashed"):
                    errors.append(f"{name}: invalid edge style")
                if "label" in item and (not isinstance(item["label"], str) or not item["label"].strip()):
                    errors.append(f"{name}: label must be nonempty text")
                if item.get("label"):
                    at = item.get("label_at")
                    if not isinstance(at, list) or len(at) != 2 or not all(number(v) for v in at):
                        errors.append(f"{name}: labeled edges need numeric label_at")
                    if not number(item.get("label_w", 170)) or item.get("label_w", 170) < 32:
                        errors.append(f"{name}: label_w must be at least 32")
            if kind == "nodes":
                if item.get("shape", "box") not in ("box", "store", "decision"):
                    errors.append(f"{name}: invalid node shape")
                if "detail" in item and not isinstance(item["detail"], str):
                    errors.append(f"{name}: detail must be text")
                if "emphasis" in item and not isinstance(item["emphasis"], bool):
                    errors.append(f"{name}: emphasis must be boolean")
            if kind != "regions":
                if item.get("status", "unspecified") not in STATUSES:
                    errors.append(f"{name}: invalid evidence status")
                sources = item.get("sources", [])
                if not isinstance(sources, list) or any(not isinstance(s, str) for s in sources):
                    errors.append(f"{name}: sources must be strings")
    if errors:
        return errors
    nodes = {n["id"]: n for n in scene["nodes"]}
    width, height = scene["width"], scene["height"]
    for item in scene["nodes"] + scene.get("regions", []):
        x0, y0, x1, y1 = bounds(item)
        if x0 < 0 or y0 < 0 or x1 > width or y1 > height:
            errors.append(f'{item["id"]}: rectangle outside canvas')
    for i, a in enumerate(scene["nodes"]):
        for b in scene["nodes"][i + 1:]:
            if overlaps(bounds(a), bounds(b)):
                errors.append(f'{a["id"]}/{b["id"]}: nodes overlap')
    for edge in scene["edges"]:
        eid = edge["id"]
        for key in ("from", "to"):
            if edge[key] not in nodes:
                errors.append(f"{eid}: unknown {key} endpoint {edge[key]}")
        if any(not (0 <= p[0] <= width and 0 <= p[1] <= height) for p in edge["points"]):
            errors.append(f"{eid}: route outside canvas")
        for key, point in (("from", edge["points"][0]), ("to", edge["points"][-1])):
            if edge[key] in nodes and not on_boundary(point, bounds(nodes[edge[key]])):
                errors.append(f"{eid}: {key} point must lie on its node boundary")
        for node in scene["nodes"]:
            if any(segment_hits(a, b, bounds(node)) for a, b in zip(edge["points"], edge["points"][1:])):
                errors.append(f'{eid}: route passes through node {node["id"]}')
        if edge.get("label"):
            rect = bounds(label_box(edge))
            if rect[0] < 0 or rect[1] < 0 or rect[2] > width or rect[3] > height:
                errors.append(f"{eid}: label outside canvas")
            for node in scene["nodes"]:
                if overlaps(rect, bounds(node)):
                    errors.append(f'{eid}: label overlaps node {node["id"]}')
    colors = {**PALETTES[theme], **tokens}
    # Text needs 4.5:1; marks that carry meaning (node borders, connectors, focus rings) need 3:1.
    for a, b, minimum in (("ink", "surface", 4.5), ("muted", "surface", 4.5),
                          ("ink", "accent_surface", 4.5), ("ink", "paper", 4.5),
                          ("muted", "paper", 4.5), ("edge", "paper", 3),
                          ("rule", "paper", 3), ("rule", "surface", 3),
                          ("accent", "paper", 3), ("accent", "accent_surface", 3)):
        ratio = contrast(colors[a], colors[b])
        if ratio < minimum:
            errors.append(f"contrast {a}/{b}: {ratio:.2f}:1 is below {minimum}:1")
    return errors


def esc(value):
    return html.escape(str(value), quote=True)


def svg_text(lines, x, y, size, color, owner, weight=400, anchor="start"):
    attrs = f' data-node-text="{esc(owner)}"' if owner else ""
    spans = "".join(f'<tspan x="{x}" dy="{0 if i == 0 else size + 5}">{esc(line)}</tspan>'
                    for i, line in enumerate(lines))
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}"{attrs}>{spans}</text>'


def render_svg(scene):
    errors = validate(scene)
    if errors:
        raise ValueError("\n".join(errors))
    c = {**PALETTES[scene.get("theme", "light")], **scene.get("tokens", {})}
    prefix = "dc-" + hashlib.sha256(json.dumps(scene, sort_keys=True).encode()).hexdigest()[:10]
    width, height = scene["width"], scene["height"]
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-labelledby="{prefix}-title {prefix}-desc" font-family="system-ui, -apple-system, Segoe UI, sans-serif">',
             f'<title id="{prefix}-title">{esc(scene["title"])}</title>',
             f'<desc id="{prefix}-desc">{esc(scene["description"])}</desc>',
             f'<defs><marker id="{prefix}-arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto" markerUnits="userSpaceOnUse"><path d="M0 0 L10 4 L0 8 Z" fill="{c["edge"]}"/></marker></defs>',
             f'<rect width="{width}" height="{height}" fill="{c["paper"]}" aria-hidden="true"/>']
    for region in scene.get("regions", []):
        x, y, w, h = (region[k] for k in ("x", "y", "w", "h"))
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="none" stroke="{c["rule"]}" stroke-dasharray="4 4"/>')
        parts.append(svg_text([region["label"]], x + 16, y + 24, 13, c["muted"], None, 600))
    for edge in scene["edges"]:
        pts = " ".join(f"{x},{y}" for x, y in edge["points"])
        dash = ' stroke-dasharray="6 5"' if edge.get("style") == "dashed" else ""
        parts.append(f'<polyline data-edge="{edge["id"]}" points="{pts}" fill="none" stroke="{c["edge"]}" stroke-width="2" stroke-linejoin="round" marker-end="url(#{prefix}-arrow)"{dash}/>')
    for node in scene["nodes"]:
        x, y, w, h = (node[k] for k in ("x", "y", "w", "h"))
        focal = node.get("emphasis", False)
        fill, stroke = c["accent_surface"] if focal else c["surface"], c["accent"] if focal else c["rule"]
        parts.append(f'<g id="{prefix}-node-{node["id"]}" data-node="{node["id"]}" data-x="{x}" data-y="{y}" data-w="{w}" data-h="{h}">')
        shape = node.get("shape", "box")
        if shape == "decision":
            points = f'{x + w/2},{y} {x + w},{y+h/2} {x+w/2},{y+h} {x},{y+h/2}'
            parts.append(f'<polygon points="{points}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        else:
            parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="{2 if focal else 1.5}"/>')
            if shape == "store":
                parts.append(f'<path d="M{x+10} {y+9} H{x+w-10} M{x+10} {y+h-9} H{x+w-10}" stroke="{stroke}" fill="none"/>')
        inner = w * 0.48 if shape == "decision" else w - 36
        name_lines = wrap(node["label"], inner, 18)
        detail_lines = wrap(node.get("detail", ""), inner, 13) if node.get("detail") else []
        badge = node.get("status") if node.get("status") in ("inferred", "proposed") else None
        block_h = len(name_lines)*23 + len(detail_lines)*18 + (22 if badge else 0)
        first_y = y + (h - block_h)/2 + 18
        text_x, anchor = (x+w/2, "middle") if shape == "decision" else (x+18, "start")
        parts.append(svg_text(name_lines, text_x, first_y, 18, c["ink"], node["id"], 650, anchor))
        if detail_lines:
            parts.append(svg_text(detail_lines, text_x, first_y + len(name_lines)*23 + 3, 13, c["muted"], node["id"], anchor=anchor))
        if badge:
            parts.append(svg_text([badge.upper()], text_x, y+h-15, 11, c["ink"], node["id"], 700, anchor))
        parts.append("</g>")
    for edge in scene["edges"]:
        if edge.get("label"):
            box = label_box(edge)
            x, y, w, h = (box[k] for k in ("x", "y", "w", "h"))
            parts.append(f'<g data-label="{edge["id"]}" data-x="{x}" data-y="{y}" data-w="{w}" data-h="{h}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{c["paper"]}"/>')
            parts.append(svg_text(wrap(edge["label"], w-16, 13), x+8, y+19, 13, c["ink"], None))
            parts.append("</g>")
    return "\n".join(parts + ["</svg>"])


def render_html(scene):
    svg = render_svg(scene)
    c = {**PALETTES[scene.get("theme", "light")], **scene.get("tokens", {})}
    node_rows = "".join(f'<tr><th scope="row">{esc(n["id"])}</th><td>{esc(n["label"])}</td><td>{esc(n.get("status", "unspecified"))}</td><td>{esc("; ".join(n.get("sources", [])) or "Not recorded")}</td></tr>' for n in scene["nodes"])
    edge_rows = "".join(f'<tr><th scope="row">{esc(e["id"])}</th><td>{esc(e["from"])} → {esc(e["to"])}</td><td>{esc(e.get("label", "Unlabeled relationship"))}</td><td>{esc(e.get("status", "unspecified"))}</td><td>{esc("; ".join(e.get("sources", [])) or "Not recorded")}</td></tr>' for e in scene["edges"])
    notes = "".join(f"<li>{esc(n)}</li>" for n in scene.get("notes", []))
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(scene["title"])}</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:{c['paper']};color:{c['ink']};font:16px/1.5 system-ui,-apple-system,Segoe UI,sans-serif}}
main{{max-width:1280px;margin:auto;padding:36px 24px}}header{{max-width:760px;margin-bottom:24px}}h1{{font-size:clamp(26px,4vw,42px);line-height:1.12;letter-spacing:-.035em;margin:8px 0 16px}}h2{{font-size:20px;margin:28px 0 12px}}p{{margin:0 0 12px}}.eyebrow{{color:{c['muted']};font-size:12px;font-weight:700;letter-spacing:.14em;text-transform:uppercase}}
.canvas,.table-wrap{{max-width:100%;overflow-x:auto}}.canvas{{border:1px solid {c['rule']};border-radius:8px}}.canvas svg{{display:block;width:100%;min-width:{scene['width']}px;height:auto}}.canvas:focus-visible,.table-wrap:focus-visible{{outline:3px solid {c['accent']};outline-offset:3px}}.hint{{color:{c['muted']};font-size:13px;margin-top:10px}}
table{{border-collapse:collapse;width:100%;min-width:680px;font-size:13px;text-align:left}}th,td{{padding:10px 12px;border-bottom:1px solid {c['rule']};vertical-align:top}}td:last-child{{overflow-wrap:anywhere}}thead{{background:{c['surface']}}}th{{font-weight:650;white-space:nowrap}}li{{margin-bottom:6px}}
@media(max-width:600px){{main{{padding:24px 16px}}}}@media print{{body{{font-size:12px}}main{{max-width:none;padding:0}}header{{max-width:none;margin-bottom:12px}}h1{{font-size:26px;margin:4px 0 10px}}h2{{font-size:16px;break-after:avoid}}.canvas svg{{min-width:0;width:auto;max-width:100%;height:auto;max-height:135mm;margin:auto}}.canvas{{overflow:visible;break-inside:avoid}}.hint{{display:none}}table{{min-width:0;font-size:10px}}th,td{{padding:6px}}tr{{break-inside:avoid}}}}
</style></head><body><main><header><p class="eyebrow">Diagram Craft · editable system view</p><h1>{esc(scene['title'])}</h1><p>{esc(scene['description'])}</p></header>
<div class="canvas" tabindex="0" role="region" aria-label="Scrollable diagram">{svg}</div>
<p class="hint">On narrow screens, scroll the diagram horizontally. The relationships and evidence are also listed below.</p>
{('<h2>Notes and assumptions</h2><ul>' + notes + '</ul>') if notes else ''}
<h2>Entities and evidence</h2><div class="table-wrap" tabindex="0" role="region" aria-label="Entity evidence table"><table><thead><tr><th scope="col">ID</th><th scope="col">Entity</th><th scope="col">Status</th><th scope="col">Source</th></tr></thead><tbody>{node_rows}</tbody></table></div>
<h2>Relationships and evidence</h2><div class="table-wrap" tabindex="0" role="region" aria-label="Relationship evidence table"><table><thead><tr><th scope="col">ID</th><th scope="col">Direction</th><th scope="col">Meaning</th><th scope="col">Status</th><th scope="col">Source</th></tr></thead><tbody>{edge_rows}</tbody></table></div>
</main></body></html>'''


class SVGParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.depth, self.parts, self.svgs, self.tags = 0, [], [], []

    def handle_starttag(self, tag, attrs):
        if tag == "svg" or self.depth:
            if self.depth == 0:
                self.parts = []
            self.depth += 1
            self.tags.append(re.match(r"<([^\s/>]+)", self.get_starttag_text()).group(1))
            self.parts.append(self.get_starttag_text())

    def handle_startendtag(self, tag, attrs):
        if self.depth:
            self.parts.append(self.get_starttag_text())

    def handle_endtag(self, tag):
        if self.depth:
            original = self.tags.pop()
            if original.lower() != tag:
                raise ValueError("mismatched SVG element tags")
            self.parts.append(f"</{original}>")
            self.depth -= 1
            if self.depth == 0:
                self.svgs.append("".join(self.parts))

    def handle_data(self, data):
        if self.depth:
            self.parts.append(data)

    def handle_entityref(self, name):
        if self.depth:
            self.parts.append(f"&{name};")

    def handle_charref(self, name):
        if self.depth:
            self.parts.append(f"&#{name};")

    def handle_comment(self, data):
        if self.depth:
            self.parts.append(f"<!--{data}-->")


def extract_svg(content):
    parser = SVGParser()
    parser.feed(content)
    if parser.depth or len(parser.svgs) != 1:
        raise ValueError("extraction requires exactly one well-formed inline SVG")
    svg = normalize_svg(parser.svgs[0])
    ET.fromstring(svg)
    return svg


def normalize_svg(svg):
    if not re.search(r'<svg\b[^>]*\bxmlns\s*=', svg):
        svg = svg.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
    # HTML entities are not all valid XML entities; normalize them to Unicode.
    svg = re.sub(r"&([A-Za-z][A-Za-z0-9]+);", lambda m: m.group(0) if m.group(1) in
                 ("amp", "lt", "gt", "quot", "apos") else html.unescape(m.group(0)), svg)
    return svg


def inline_svgs(content):
    """Every top-level inline SVG in a document, normalized for XML parsing."""
    parser = SVGParser()
    parser.feed(content)
    if parser.depth:
        raise ValueError("unclosed inline SVG")
    return [normalize_svg(svg) for svg in parser.svgs]


def offline_font_findings(content):
    """Report web-font requests and font stacks without a generic family fallback."""
    findings = [f"remote font request: {m.group(0)[:60]}" for m in REMOTE_FONT.finditer(content)]
    generic = re.compile(r"\b(?:sans-serif|serif|monospace|system-ui|ui-sans-serif|ui-serif|ui-monospace|cursive|fantasy)\s*$", re.IGNORECASE)
    for stack in re.findall(r"font-family\s*[:=]\s*[\"']?([^;\"'}>]+)", content, re.IGNORECASE):
        stack = stack.strip()
        if stack and not stack.lower().startswith(("inherit", "var(")) and not generic.search(stack):
            findings.append(f"font stack without generic fallback: {stack[:60]}")
    return findings


SVG_NS = "{http://www.w3.org/2000/svg}"
# Parts of an SVG that are never painted directly, or whose geometry needs real rendering to judge.
NOT_PAINTED = {"defs", "clipPath", "mask", "marker", "symbol", "pattern", "metadata", "title", "desc", "style", "script"}
ALPHA_PAINT = re.compile(r"^\s*(?:rgba|hsla)\(|^\s*#(?:[0-9a-fA-F]{4}|[0-9a-fA-F]{8})\s*$", re.IGNORECASE)


def _num(value):
    """Plain user-unit number (optional px), or None for percentages, other units, or missing values."""
    match = re.fullmatch(r"\s*([-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?)(?:px)?\s*", value or "")
    return float(match.group(1)) if match else None


def _shape_box(el):
    """Axis-aligned box (x0, y0, x1, y1) for simple shapes; None when not measurable or not rendered."""
    tag = el.tag.replace(SVG_NS, "")
    a = lambda k, d=None: _num(el.get(k, d))
    if tag == "rect":
        x, y, w, h = a("x", "0"), a("y", "0"), a("width"), a("height")
        return None if None in (x, y, w, h) or w <= 0 or h <= 0 else (x, y, x + w, y + h)
    if tag == "circle":
        x, y, r = a("cx", "0"), a("cy", "0"), a("r")
        return None if None in (x, y, r) or r <= 0 else (x - r, y - r, x + r, y + r)
    if tag == "ellipse":
        x, y, rx, ry = a("cx", "0"), a("cy", "0"), a("rx"), a("ry")
        return None if None in (x, y, rx, ry) or rx <= 0 or ry <= 0 else (x - rx, y - ry, x + rx, y + ry)
    if tag == "line":
        v = [a("x1", "0"), a("y1", "0"), a("x2", "0"), a("y2", "0")]
        return None if None in v else (min(v[0], v[2]), min(v[1], v[3]), max(v[0], v[2]), max(v[1], v[3]))
    if tag in ("polyline", "polygon"):
        nums = re.findall(r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?", el.get("points", ""))
        if len(nums) < 2:
            return None
        xs, ys = [float(n) for n in nums[0::2]], [float(n) for n in nums[1::2]]
        return min(xs), min(ys), max(xs), max(ys)
    if tag == "text":
        x, y = a("x", "0"), a("y", "0")
        return None if None in (x, y) else (x, y, x, y)
    return None


def _hidden(el):
    style = el.get("style", "")
    return (el.get("display") == "none" or el.get("visibility") == "hidden" or el.get("clip-path") or el.get("mask")
            or re.search(r"display\s*:\s*none|visibility\s*:\s*hidden", style) is not None)


def viewbox_findings(root, label="svg"):
    """Report simple shapes painted outside the viewBox, which exporters and viewers clip silently.

    Only untransformed, directly measurable shapes are judged; paths, transforms, clipped or hidden
    content are skipped, so a clean result is not proof that nothing is cut off."""
    vb = root.get("viewBox")
    if vb:
        parts = [_num(p) for p in re.split(r"[\s,]+", vb.strip())]
        if len(parts) != 4 or None in parts or parts[2] <= 0 or parts[3] <= 0:
            return [f"{label}: viewBox is not four numbers with positive size"]
        x0, y0 = parts[0], parts[1]
        x1, y1 = x0 + parts[2], y0 + parts[3]
    else:
        w, h = _num(root.get("width")), _num(root.get("height"))
        if not w or not h:
            return [f"{label}: no viewBox or numeric width/height; size cannot be checked"]
        x0, y0, x1, y1 = 0, 0, w, h
    findings = []

    def walk(el):
        tag = el.tag.replace(SVG_NS, "")
        if tag in NOT_PAINTED or _hidden(el) or el.get("transform"):
            return
        box = _shape_box(el)
        if box and (box[0] < x0 - 0.01 or box[1] < y0 - 0.01 or box[2] > x1 + 0.01 or box[3] > y1 + 0.01):
            ident = el.get("id") or el.get("data-node") or el.get("data-edge") or ""
            findings.append(f"{label}: <{tag}{' ' + ident if ident else ''}> extends outside the viewBox")
        for child in el:
            walk(child)

    for child in root:
        walk(child)
    return findings


def export_findings(content, html_document=None):
    """Portability problems in an HTML or SVG export: alpha paint, CDATA, unscoped styles, bad refs, clipping."""
    try:
        svgs = inline_svgs(content)
    except ValueError as exc:
        return [f"inline SVG cannot be read: {exc}"]
    if not svgs:
        return ["no inline SVG found"]
    findings, seen = [], {}
    for index, source in enumerate(svgs, 1):
        label = f"svg {index}"
        try:
            root = ET.fromstring(source)
        except ET.ParseError as exc:
            findings.append(f"{label}: not well-formed XML ({exc})")
            continue
        findings.extend(viewbox_findings(root, label))
        ids = {el.get("id") for el in root.iter() if el.get("id")}
        for name in ids:
            if name in seen:
                findings.append(f"{label}: id {name!r} also used by svg {seen[name]}; namespace IDs when embedding")
            seen.setdefault(name, index)
        for el in root.iter():
            declared = dict((k.strip().lower(), v.strip()) for k, _, v in
                            (d.partition(":") for d in el.get("style", "").split(";")) if k.strip())
            for attr in ("fill", "stroke", "stop-color", "flood-color"):
                for value in (el.get(attr), declared.get(attr)):
                    if value and ALPHA_PAINT.search(value.replace("!important", "").strip()):
                        findings.append(f"{label}: {attr}={value[:32]!r} carries alpha in a paint value; "
                                        f"use an opaque color with {attr.replace('-color', '')}-opacity")
            refs = re.findall(r"url\(\s*['\"]?#([^)'\"\s]+)", " ".join(el.attrib.values()))
            refs += [v[1:] for k, v in el.attrib.items() if k.split("}")[-1] == "href" and v.startswith("#")]
            for ref in refs:
                if ref not in ids:
                    findings.append(f"{label}: reference to missing id {ref!r}")
        for style in root.iter(SVG_NS + "style"):
            text = style.text or ""
            if len(svgs) > 1:
                for selector in re.findall(r"(?:^|\})\s*([^{}@]+)\{", re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)):
                    if not all(part.strip().startswith(("#", "svg#")) for part in selector.split(",") if part.strip()):
                        findings.append(f"{label}: style selector {selector.strip()[:40]!r} is not scoped to an ID and can restyle sibling diagrams")
                        break
        if html_document and re.search(r"<!\[CDATA\[", source):
            findings.append(f"{label}: CDATA section in an HTML-embedded SVG is parsed as a comment; use plain escaped text")
    return findings


def write_file(path, content, force=False):
    with Path(path).open("w" if force else "x", encoding="utf-8") as stream:
        stream.write(content + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("render", "check", "extract"),
                        help="check takes a scene JSON, or an HTML/SVG export to verify it needs no web fonts")
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--force", action="store_true", help="replace an existing output file")
    args = parser.parse_args()
    try:
        content = args.input.read_text(encoding="utf-8")
        if args.command == "check" and args.input.suffix.lower() in {".html", ".htm", ".svg"}:
            findings = offline_font_findings(content)
            export = export_findings(content, args.input.suffix.lower() != ".svg")
            print(json.dumps({"ok": not findings and not export, "offline_fonts": findings, "export": export}))
            return 1 if findings or export else 0
        if args.command == "extract":
            if not args.output:
                parser.error("extract needs --output")
            result = extract_svg(content)
        else:
            scene = json.loads(content)
            errors = validate(scene)
            if errors:
                raise ValueError("\n".join(errors))
            if args.command == "check":
                print(json.dumps({"ok": True, "nodes": len(scene["nodes"]), "edges": len(scene["edges"])}))
                return 0
            if not args.output:
                parser.error("render needs --output")
            result = render_html(scene)
        write_file(args.output, result, args.force)
        print(str(args.output))
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
