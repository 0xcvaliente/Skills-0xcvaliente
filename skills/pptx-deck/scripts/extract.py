#!/usr/bin/env python3
"""Extract the content of an existing .pptx for converting or restyling it.

Usage:
    extract.py IN.pptx -o OUTDIR                      # extracted.json + assets/
    extract.py IN.pptx -o OUTDIR --to-spec            # also a draft deck-spec.json
    extract.py IN.pptx -o OUTDIR --to-spec --theme research-white --density reading-first

Writes
------
OUTDIR/extracted.json   Per slide: title (title placeholder, else the largest /
                        top-most text), body text blocks in reading order with
                        paragraphs and bullet flags, tables (cell grids), chart
                        data (type, categories, series), images, speaker notes.
OUTDIR/assets/          Every picture, including pictures inside groups, saved
                        once (de-duplicated by content hash) as img-<hash>.<ext>.
OUTDIR/deck-spec.json   (--to-spec) A draft spec for references/deck-spec.schema.json
                        with media paths relative to the spec. It is meant to be
                        reviewed: roles are guesses (first slide cover, charts by
                        chart type, image-heavy slides image, lists breakdown /
                        process / risks / actions / metrics ...), text is trimmed
                        to the role limits and the full original text of anything
                        that was trimmed is stored in the slide's notes. The draft
                        is checked with validate_spec.py and must have no errors.

Build the restyled deck with:  build_deck.py OUTDIR/deck-spec.json -o restyled.pptx

Exit status: 0 ok, 1 the draft spec failed validation, 2 unreadable input.
"""

from __future__ import annotations

import argparse
import collections
import datetime as _dt
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as C  # noqa: E402

C.require_pptx()

from pptx import Presentation  # noqa: E402

from inventory import (  # noqa: E402
    A,
    abs_box,
    describe_chart,
    iter_shapes_abs,
    localname,
    shape_kind,
)

EMU = C.EMU_PER_INCH
SUPPORTED_IMAGE_EXT = {"png", "jpg", "jpeg", "gif", "bmp", "tif", "tiff"}
TITLE_PH = {"TITLE", "CENTER_TITLE", "VERTICAL_TITLE"}
SKIP_PH = {"SLIDE_NUMBER", "FOOTER", "DATE"}
CLOSING_RE = re.compile(r"\b(thank(s| you)?|questions?|q\s*&\s*a|contact|get in touch|takk|merci|danke|gracias|the end)\b", re.I)
PROCESS_RE = re.compile(r"\b(process|steps?|roadmap|timeline|phases?|plan|how (it|we|to)|workflow|journey|stages?)\b", re.I)
RISK_RE = re.compile(r"\b(risks?|challenges?|issues?|threats?|concerns?|obstacles?)\b", re.I)
ACTION_RE = re.compile(r"\b(actions?|next steps?|to-?do|recommendations?|asks?|decisions?)\b", re.I)
TEAM_RE = re.compile(r"\b(team|people|leadership|who we are|our experts)\b", re.I)
CONTEXT_RE = re.compile(r"\b(agenda|overview|background|context|situation|why)\b", re.I)
NUMBER_LEAD_RE = re.compile(r"^\s*([$€£]?\s?\d[\d.,]*\s?(?:%|[kKmMbB]\b|x\b)?)\s*(.*)$")
LIST_NUM_RE = re.compile(r"^\s*(\d+[.)]|step\s*\d+)", re.I)


# --------------------------------------------------------------------------
# Small text helpers
# --------------------------------------------------------------------------


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\v", " ")).strip()


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:32].strip("-")


def fit(text: str, cap: int, trimmed: List[str]) -> str:
    """Cut *text* to at most *cap* characters at a word boundary, adding an ellipsis; record the original."""
    text = clean(text)
    if len(text) <= cap:
        return text
    trimmed.append(text)
    cut = text[: max(cap - 1, 1)]
    sp = cut.rfind(" ")
    if sp >= cap * 0.5:
        cut = cut[:sp]
    return cut.rstrip(" ,;:-–—.") + "…"


def shorten(text: str, short_cap: int) -> str:
    """A version of *text* of at most *short_cap* characters (first clause, else word cut)."""
    text = clean(text)
    if len(text) <= short_cap:
        return text
    for sep in (". ", ": ", " – ", " — ", " - ", "; ", ", "):
        head = text.split(sep, 1)[0]
        if 6 <= len(head) <= short_cap:
            return head
    cut = text[: max(short_cap - 1, 1)]
    sp = cut.rfind(" ")
    if sp >= short_cap * 0.5:
        cut = cut[:sp]
    return cut.rstrip(" ,;:-–—.") + "…"


def text_obj(text: str, cap: int, trimmed: List[str]) -> Dict[str, str]:
    full = fit(text, cap, trimmed)
    return {"full": full, "short": shorten(full, C.short_limit(cap))}


def words(text: str) -> int:
    return len(text.split())


# --------------------------------------------------------------------------
# Reading a slide
# --------------------------------------------------------------------------


def paragraph_records(shape: Any, is_placeholder_body: bool) -> List[Dict[str, Any]]:
    paras = []
    for p in shape.text_frame.paragraphs:
        text = clean(p.text)
        if not text:
            continue
        ppr = p._p.find(A + "pPr")
        explicit: Optional[bool] = None
        numbered = False
        if ppr is not None:
            if ppr.find(A + "buAutoNum") is not None:
                explicit, numbered = True, True
            elif ppr.find(A + "buChar") is not None:
                explicit = True
            elif ppr.find(A + "buNone") is not None:
                explicit = False
        sizes = [r.font.size.pt for r in p.runs if r.font.size is not None]
        paras.append({"text": text, "level": p.level, "bullet": explicit, "numbered": numbered, "size": max(sizes) if sizes else None})
    multi = len(paras) >= 2
    for rec in paras:
        if rec["bullet"] is None:
            rec["bullet"] = bool(rec["level"] > 0 or multi or (is_placeholder_body and multi))
    return paras


class SlideData:
    def __init__(self, index: int) -> None:
        self.index = index
        self.layout = ""
        self.hidden = False
        self.notes = ""
        self.title: Optional[Dict[str, Any]] = None
        self.blocks: List[Dict[str, Any]] = []
        self.tables: List[Dict[str, Any]] = []
        self.charts: List[Dict[str, Any]] = []
        self.images: List[Dict[str, Any]] = []
        self.footers: List[str] = []


def read_slide(prs: Any, slide: Any, index: int, assets: Path, saved: Dict[str, str]) -> SlideData:
    sw, sh = prs.slide_width, prs.slide_height
    sd = SlideData(index)
    sd.layout = slide.slide_layout.name
    sd.hidden = slide._element.get("show") == "0"
    if slide.has_notes_slide:
        try:
            sd.notes = slide.notes_slide.notes_text_frame.text.strip()
        except Exception:
            sd.notes = ""
    for shp, path, _depth, tf in iter_shapes_abs(slide.shapes):
        kind = shape_kind(shp)
        box = abs_box(shp, tf)
        bounds = None
        if box:
            bounds = {
                "left": round(box[0] / EMU, 3),
                "top": round(box[1] / EMU, 3),
                "width": round((box[2] - box[0]) / EMU, 3),
                "height": round((box[3] - box[1]) / EMU, 3),
            }
        ph_type = None
        if shp.is_placeholder:
            try:
                ph_type = shp.placeholder_format.type.name
            except Exception:
                ph_type = None
        if ph_type in SKIP_PH:
            if getattr(shp, "has_text_frame", False) and shp.has_text_frame and shp.text_frame.text.strip():
                sd.footers.append(clean(shp.text_frame.text))
            continue
        if kind == "table":
            grid = [[clean(c.text) for c in row.cells] for row in shp.table.rows]
            sd.tables.append({"id": shp.shape_id, "path": path, "name": shp.name, "rows": grid, "bounds": bounds})
            continue
        if kind == "chart":
            ch = describe_chart(shp.chart)
            ch.update({"id": shp.shape_id, "path": path, "bounds": bounds})
            sd.charts.append(ch)
            continue
        if localname(shp._element) == "pic":
            try:
                img = shp.image
            except Exception:
                continue
            digest = img.sha1
            ext = img.ext.lower()
            name = saved.get(digest)
            if name is None:
                name = "img-%s.%s" % (digest[:10], ext)
                assets.mkdir(parents=True, exist_ok=True)
                (assets / name).write_bytes(img.blob)
                saved[digest] = name
            cnv = shp._element.find(".//{http://schemas.openxmlformats.org/presentationml/2006/main}cNvPr")
            alt = (cnv.get("descr") if cnv is not None else "") or ""
            frac = 0.0
            small_side = 99.0
            if bounds:
                frac = bounds["width"] * bounds["height"] / ((sw / EMU) * (sh / EMU))
                small_side = min(bounds["width"], bounds["height"])
            sd.images.append(
                {
                    "path": "assets/" + name,
                    "sha1": digest,
                    "ext": ext,
                    "alt": clean(alt),
                    "bounds": bounds,
                    "areaFraction": round(frac, 4),
                    "decorative": bool(frac < 0.015 or small_side < 0.3),
                    "supported": ext in SUPPORTED_IMAGE_EXT,
                }
            )
            continue
        if getattr(shp, "has_text_frame", False) and shp.has_text_frame and shp.text_frame.text.strip():
            paras = paragraph_records(shp, ph_type in ("BODY", "OBJECT"))
            if not paras:
                continue
            sizes = [p["size"] for p in paras if p["size"]]
            default = 44.0 if ph_type in TITLE_PH else 18.0
            sd.blocks.append(
                {
                    "id": shp.shape_id,
                    "path": path,
                    "name": shp.name,
                    "placeholder": ph_type,
                    "isTitle": ph_type in TITLE_PH,
                    "fontPt": max(sizes) if sizes else default,
                    "bounds": bounds,
                    "paragraphs": paras,
                    "text": "\n".join(p["text"] for p in paras),
                }
            )
    pick_title(sd, sh / EMU)
    return sd


def pick_title(sd: SlideData, slide_h: float) -> None:
    blocks = sd.blocks
    if not blocks:
        return
    explicit = [b for b in blocks if b["isTitle"]]
    if explicit:
        title = explicit[0]
    else:
        cands = [b for b in blocks if words(b["text"]) <= 22 and len(b["paragraphs"]) <= 2] or blocks

        def top(b: Dict[str, Any]) -> float:
            return b["bounds"]["top"] if b["bounds"] else 0.0

        upper = [b for b in cands if top(b) < slide_h * 0.45] or cands
        title = sorted(upper, key=lambda b: (-round(b["fontPt"]), top(b)))[0]
    sd.title = title


def reading_order(blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    def key(b: Dict[str, Any]) -> Tuple[int, float]:
        bd = b["bounds"] or {"top": 0.0, "left": 0.0}
        return int(bd["top"] / 0.35), bd["left"]

    return sorted(blocks, key=key)


def body_blocks(sd: SlideData) -> List[Dict[str, Any]]:
    return reading_order([b for b in sd.blocks if b is not sd.title])


# --------------------------------------------------------------------------
# Draft spec
# --------------------------------------------------------------------------


def detect_language(prs_path: str) -> str:
    import zipfile

    counts: collections.Counter = collections.Counter()
    try:
        with zipfile.ZipFile(prs_path) as zf:
            for name in zf.namelist():
                if name.startswith("ppt/slides/slide") and name.endswith(".xml"):
                    counts.update(re.findall(rb'\blang="([A-Za-z]{2,3}(?:-[A-Za-z0-9]+)*)"', zf.read(name)))
    except Exception:
        return "en"
    for lang, _n in counts.most_common():
        text = lang.decode("ascii")
        if re.fullmatch(r"[a-z]{2,3}(-[A-Za-z0-9]+)*", text):
            return text
    return "en"


def chart_type_for_spec(ch: Dict[str, Any]) -> str:
    t = str(ch.get("chartType", "")).upper()
    if "DOUGHNUT" in t:
        return "doughnut"
    if "PIE" in t:
        return "pie"
    if any(k in t for k in ("LINE", "AREA", "XY", "SCATTER", "RADAR", "BUBBLE")):
        return "line"
    if "BAR" in t:
        return "stacked_bar" if "STACKED" in t else "bar"
    if "COLUMN" in t:
        return "stacked_bar" if "STACKED" in t else "column"
    return "column"


def spec_chart(ch: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    series = [s for s in ch.get("series", []) if s.get("values")]
    if not series:
        return None
    cats = [clean(str(c)) or "-" for c in ch.get("categories", [])]
    n = max(len(cats), max(len(s["values"]) for s in series))
    if len(cats) < n:
        cats += [str(i) for i in range(len(cats) + 1, n + 1)]
    out_series = []
    for s in series:
        vals = [float(v) if isinstance(v, (int, float)) else 0.0 for v in s["values"]][:n]
        vals += [0.0] * (n - len(vals))
        out_series.append({"name": clean(str(s.get("name") or "Series")) or "Series", "values": [round(v, 6) for v in vals]})
    ctype = chart_type_for_spec(ch)
    first = out_series[0]
    top = max(range(n), key=lambda i: first["values"][i])
    if ctype in ("pie", "doughnut"):
        insight = "%s is the largest share at %s." % (cats[top], ("%g" % first["values"][top]))
    else:
        insight = "%s peaks at %s in %s." % (first["name"], "%g" % first["values"][top], cats[top])
    return {"type": ctype, "categories": cats, "series": out_series, "insight": insight}


def split_label_detail(src: str, label_cap: int) -> Tuple[str, str]:
    """Split one sentence into a short label and the remaining detail."""
    src = clean(src)
    if len(src) <= label_cap:
        return src, ""
    for sep in (": ", " – ", " — ", " - ", " | "):
        if sep in src:
            head, tail = src.split(sep, 1)
            if 2 <= len(head) <= label_cap and tail.strip():
                return head.strip(), tail.strip()
    cut = src[:label_cap]
    sp = cut.rfind(" ")
    if sp >= label_cap * 0.4:
        cut = cut[:sp]
    return cut.rstrip(" ,;:-–—."), src


def make_item(n: int, label_src: str, detail_src: str, caps: Dict[str, int], trimmed: List[str]) -> Dict[str, Any]:
    label, extra = split_label_detail(label_src, caps["label"])
    detail_src = clean(" ".join(x for x in (detail_src, extra if extra and extra != detail_src else "") if x)) or extra
    item: Dict[str, Any] = {"id": "item-%d" % n, "label": fit(label, caps["label"], trimmed) or "Item"}
    if detail_src and clean(detail_src) != item["label"]:
        item["detail"] = text_obj(detail_src, caps["detail"], trimmed)
    return item


def metric_item(n: int, text: str, caps: Dict[str, int], trimmed: List[str]) -> Optional[Dict[str, Any]]:
    m = NUMBER_LEAD_RE.match(text)
    if not m:
        return None
    token, rest = m.group(1).strip(), m.group(2).strip()
    digits = re.sub(r"[^\d.,]", "", token).replace(",", "")
    try:
        value = float(digits)
    except ValueError:
        return None
    item: Dict[str, Any] = {"id": "item-%d" % n, "label": fit(rest or token, caps["label"], trimmed) or "Value", "value": value}
    if len(token) <= 10:
        item["displayValue"] = token
    if rest and len(rest) > caps["label"]:
        item["detail"] = text_obj(rest, caps["detail"], trimmed)
    return item


def collect_items(sd: SlideData, blocks: List[Dict[str, Any]]) -> Tuple[List[Tuple[str, str]], List[Dict[str, Any]], bool, bool]:
    """Return (raw items as (label, detail), leftover blocks, numbered?, numeric-lead?)."""
    raw: List[Tuple[str, str]] = []
    used: List[Dict[str, Any]] = []
    numbered = False
    bullet_paras: List[Tuple[Dict[str, Any], Dict[str, Any]]] = []
    for b in blocks:
        listy = len(b["paragraphs"]) >= 2 or any(p["bullet"] for p in b["paragraphs"])
        if listy:
            for p in b["paragraphs"]:
                bullet_paras.append((b, p))
    top_level = [(b, p) for b, p in bullet_paras if p["level"] == 0]
    if len(top_level) >= 2:
        for b, p in bullet_paras:
            if p["numbered"] or LIST_NUM_RE.match(p["text"]):
                numbered = True
            if p["level"] == 0:
                raw.append((p["text"], ""))
            elif raw:
                prev = raw[-1]
                raw[-1] = (prev[0], clean(prev[1] + " " + p["text"]))
        used = [b for b in blocks if len(b["paragraphs"]) >= 2 or any(p["bullet"] for p in b["paragraphs"])]
    else:
        loose = [b for b in blocks if len(b["paragraphs"]) == 1 and words(b["text"]) <= 16]
        if len(loose) >= 3:
            i = 0
            while i < len(loose):
                a = loose[i]
                nxt = loose[i + 1] if i + 1 < len(loose) else None
                if nxt and words(a["text"]) <= 6 and words(nxt["text"]) > 6 and _overlaps(a, nxt):
                    raw.append((a["text"], nxt["text"]))
                    used += [a, nxt]
                    i += 2
                else:
                    raw.append((a["text"], ""))
                    used.append(a)
                    i += 1
    left = [b for b in blocks if b not in used]
    numeric = bool(raw) and sum(1 for lab, _d in raw if NUMBER_LEAD_RE.match(lab)) >= max(2, int(0.6 * len(raw) + 0.5))
    if raw and not numbered:
        numbered = sum(1 for lab, _d in raw if LIST_NUM_RE.match(lab)) >= max(2, int(0.6 * len(raw) + 0.5))
    return raw, left, numbered, numeric


def _overlaps(a: Dict[str, Any], b: Dict[str, Any]) -> bool:
    ba, bb = a["bounds"], b["bounds"]
    if not ba or not bb:
        return True
    ca = ba["left"] + ba["width"] / 2
    cb = bb["left"] + bb["width"] / 2
    return abs(ca - cb) <= max(ba["width"], bb["width"]) * 0.75 and bb["top"] >= ba["top"] - 0.1


def choose_role(sd: SlideData, title_text: str, items: List[Tuple[str, str]], numbered: bool, numeric: bool, leftover_words: int, big_images: List[Dict[str, Any]]) -> str:
    if sd.charts:
        ch = sd.charts[0]
        t = chart_type_for_spec(ch)
        if t == "line":
            return "trend"
        if t in ("pie", "doughnut"):
            return "distribution"
        nseries = len([s for s in ch.get("series", []) if s.get("values")])
        return "comparison" if nseries >= 2 else "metrics"
    if sd.tables:
        return "comparison"
    n = len(items)
    if big_images:
        if n == 0 and leftover_words <= 45:
            return "image"
        if n <= 4:
            return "case"
    if n >= 2:
        if numeric:
            return "metrics"
        if numbered or PROCESS_RE.search(title_text):
            return "process"
        if RISK_RE.search(title_text):
            return "risks"
        if ACTION_RE.search(title_text):
            return "actions"
        if TEAM_RE.search(title_text):
            return "team"
        if CONTEXT_RE.search(title_text) and n <= 4:
            return "context"
        return "breakdown" if n >= 3 else "context"
    if leftover_words == 0:
        return "transition" if words(title_text) <= 6 else "statement"
    return "context" if leftover_words >= 40 else "statement"


def build_slide(sd: SlideData, pos: int, total: int, role_hint: Optional[str], density: str, used_media: set, prs_w_h: Tuple[float, float]) -> Tuple[Dict[str, Any], Optional[Dict[str, Any]]]:
    """Return (slide dict, extra closing slide or None) for source slide *sd*."""
    limits = C.role_limits()
    trimmed: List[str] = []
    title_text = clean(sd.title["text"]) if sd.title else "Slide %d" % sd.index
    blocks = body_blocks(sd)
    big_images = [i for i in sd.images if i["supported"] and not i["decorative"] and i["areaFraction"] >= 0.1]
    all_images = [i for i in sd.images if i["supported"] and not i["decorative"]]
    raw_items, leftover, numbered, numeric = collect_items(sd, blocks)
    leftover_text = clean(" ".join(clean(b["text"]) for b in leftover))
    lw = words(leftover_text)

    if role_hint:
        role = role_hint
    else:
        role = choose_role(sd, title_text, raw_items, numbered, numeric, lw if raw_items else words(clean(" ".join(b["text"] for b in blocks))), big_images)
        if not raw_items and role in ("statement", "context") and blocks:
            leftover, leftover_text = blocks, clean(" ".join(clean(b["text"]) for b in blocks))

    lim = limits[role]
    caps = lim["maxChars"]
    notes_extra: List[str] = []

    slide: Dict[str, Any] = {"id": "", "role": role}
    slide["title"] = text_obj(title_text, caps["title"], trimmed)

    # summary
    summary_src = leftover_text
    if role == "cover":
        summary_src = clean(" · ".join(clean(b["text"]) for b in blocks[:2]))
    if summary_src:
        slide["summary"] = text_obj(summary_src, caps["summary"], trimmed)

    # chart
    chart = None
    if lim["allowsChart"] and sd.charts:
        chart = spec_chart(sd.charts[0])
        if chart:
            slide["chart"] = chart
        if len(sd.charts) > 1:
            notes_extra.append("Source slide also had %d more chart(s) that are not in this draft." % (len(sd.charts) - 1))
    elif sd.charts:
        notes_extra.append("Source slide had a chart that this role cannot show.")

    # table rows become items for the comparison role
    items: List[Dict[str, Any]] = []
    cap_items = C.density_cap(density, role) if lim["maxItems"] > 0 else 0
    dropped: List[str] = []
    if lim["maxItems"] > 0:
        if sd.tables and role == "comparison" and not chart:
            grid = [r for r in sd.tables[0]["rows"] if any(r)]
            header = grid[0] if len(grid) > 1 else []
            for r in grid[1:] if header else grid:
                label = r[0] or "Row"
                rest = [c for c in r[1:] if c]
                if header:
                    detail = "; ".join("%s: %s" % (h, c) for h, c in zip(header[1:], r[1:]) if c and h) or " | ".join(rest)
                else:
                    detail = " | ".join(rest)
                raw_items.append((label, detail))
        if role == "metrics" and chart and not raw_items:
            first = chart["series"][0]
            for cat, val in list(zip(chart["categories"], first["values"]))[:cap_items]:
                items.append({"id": "item-%d" % (len(items) + 1), "label": fit(cat, caps["label"], trimmed), "value": val})
        else:
            for label, detail in raw_items:
                n = len(items) + 1
                it = metric_item(n, label, caps, trimmed) if role == "metrics" else None
                items.append(it or make_item(n, label, detail, caps, trimmed))
        if len(items) > cap_items:
            dropped = [items[i]["label"] + ((": " + items[i]["detail"]["full"]) if "detail" in items[i] else "") for i in range(cap_items, len(items))]
            items = items[:cap_items]
    if dropped:
        notes_extra.append("Points left out of this slide because of the item limit: " + "; ".join(dropped))
    if items:
        slide["items"] = items

    if "items" in lim["requiredFields"] and not slide.get("items"):
        return build_slide(sd, pos, total, "context" if role != "context" else "statement", density, used_media, prs_w_h)

    # media
    media: List[Dict[str, Any]] = []
    if lim["allowsMedia"]:
        pool = sorted(all_images, key=lambda i: -i["areaFraction"])
        for img in pool:
            if len(media) >= 3 or (role == "cover" and media):
                break
            if img["path"] in used_media:
                continue
            used_media.add(img["path"])
            media.append({"path": img["path"], "kind": "image", "alt": img["alt"] or ("Image from the slide: %s" % title_text)[:120], "fit": "cover" if img["areaFraction"] > 0.3 else "contain"})
    elif all_images:
        notes_extra.append("Images on the source slide (not placed by this role): " + ", ".join(i["path"] for i in all_images))
    if media:
        slide["media"] = media

    if "media" in lim["requiredFields"] and not slide.get("media"):
        return build_slide(sd, pos, total, "context", density, used_media, prs_w_h)

    # core message and notes
    if slide.get("summary"):
        core = slide["summary"]["full"]
    elif chart:
        core = chart["insight"]
    else:
        core = slide["title"]["full"]
    slide["coreMessage"] = core
    notes_parts = []
    if sd.notes:
        notes_parts.append(sd.notes)
    else:
        notes_parts.append("Talking point: %s" % core)
    notes_parts.extend(notes_extra)
    if trimmed:
        notes_parts.append("Original text that was shortened for this slide: " + " | ".join(dict.fromkeys(trimmed)))
    slide["notes"] = "\n\n".join(notes_parts)
    slide["arcStage"] = "hook" if role == "cover" else ("takeaway" if role == "closing" else ("context" if pos == 1 else "core"))
    return slide, None


def closing_slide_from(sd: Optional[SlideData], used_media: set, density: str) -> Dict[str, Any]:
    caps = C.role_limits()["closing"]["maxChars"]
    trimmed: List[str] = []
    if sd is not None:
        title_src = clean(sd.title["text"]) if sd.title else "Thank you"
        rest = clean(" ".join(clean(b["text"]) for b in body_blocks(sd)))
    else:
        title_src, rest = "Thank you", "Questions and discussion"
    slide: Dict[str, Any] = {"id": "closing", "role": "closing", "title": text_obj(title_src, caps["title"], trimmed)}
    if rest:
        slide["summary"] = text_obj(rest, caps["summary"], trimmed)
    slide["coreMessage"] = slide.get("summary", slide["title"])["full"]
    note = sd.notes if sd is not None and sd.notes else "Close by thanking the audience and opening for questions."
    if trimmed:
        note += "\n\nOriginal text that was shortened for this slide: " + " | ".join(dict.fromkeys(trimmed))
    slide["notes"] = note
    slide["arcStage"] = "takeaway"
    return slide


def looks_like_closing(sd: SlideData, n: int) -> bool:
    text = " ".join(b["text"] for b in sd.blocks)
    if sd.charts or sd.tables:
        return False
    if CLOSING_RE.search(text):
        return True
    return n >= 3 and words(text) <= 14 and not sd.images


def default_theme() -> str:
    for pref in ("research-white", "swiss-cobalt", "paper-noir"):
        try:
            t = C.get_theme(pref)
        except KeyError:
            continue
        if t.get("autoPick") is not False:
            return pref
    for t in C.load_themes():
        if t.get("autoPick") is not False:
            return t["id"]
    return C.theme_ids()[0]


def make_seed(theme: str, source: Path) -> str:
    digest = hashlib.sha1(source.read_bytes()).hexdigest()
    letters = "".join(chr(ord("a") + int(digest[i : i + 2], 16) % 26) for i in (0, 2, 4))
    return "%s-%s-%s" % (theme, _dt.date.today().strftime("%Y%m%d"), letters)


def build_spec(slides: List[SlideData], src: Path, theme: Optional[str], density: str, aspect: str) -> Dict[str, Any]:
    n = len(slides)
    theme_id = theme or default_theme()
    used_media: set = set()
    out: List[Dict[str, Any]] = []
    extra_note: List[str] = []
    for i, sd in enumerate(slides):
        if i == 0:
            s, _ = build_slide(sd, 1, n, "cover", density, used_media, (0, 0))
            s["id"] = "cover"
        elif i == n - 1 and looks_like_closing(sd, n):
            s = closing_slide_from(sd, used_media, density)
            # keep the largest image as backdrop if one is available
        else:
            s, _ = build_slide(sd, i + 1, n, None, density, used_media, (0, 0))
        out.append(s)
    if out[-1]["role"] != "closing":
        out.append(closing_slide_from(None, used_media, density))
        extra_note.append("A closing slide was added because the last source slide did not look like one.")
    seen: collections.Counter = collections.Counter()
    for i, s in enumerate(out):
        if s["id"] in ("cover", "closing"):
            seen[s["id"]] += 1
            continue
        base = slug(s["title"]["full"]) or "slide-%d" % (i + 1)
        if base in ("cover", "closing"):
            base += "-slide"
        seen[base] += 1
        s["id"] = base if seen[base] == 1 else "%s-%d" % (base, seen[base])
    # a final dedupe pass for ids that collide after suffixing
    ids: set = set()
    for i, s in enumerate(out):
        while s["id"] in ids:
            s["id"] += "-x"
        ids.add(s["id"])
    first_title = out[0]["title"]["full"]
    spec: Dict[str, Any] = {
        "schemaVersion": 1,
        "title": first_title,
        "goal": "Restyled version of the deck %r with its content preserved" % src.stem,
        "audience": "The audience of the original deck",
        "language": "en",
        "randomSeed": make_seed(theme_id, src),
        "theme": theme_id,
        "aspect": aspect,
        "density": density,
        "mode": "restyle",
        "slides": out,
    }
    try:
        if C.get_theme(theme_id).get("autoPick") is False:
            spec["themeChosenBy"] = "user"
    except KeyError:
        pass
    if extra_note:
        out[-1]["notes"] += "\n\n" + " ".join(extra_note)
    return spec


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------


def extracted_json(slides: List[SlideData], src: Path, prs: Any) -> Dict[str, Any]:
    out_slides = []
    for sd in slides:
        bullets = []
        for b in body_blocks(sd):
            for p in b["paragraphs"]:
                if p["bullet"]:
                    bullets.append(p["text"])
        out_slides.append(
            {
                "index": sd.index,
                "layout": sd.layout,
                "hidden": sd.hidden,
                "title": clean(sd.title["text"]) if sd.title else None,
                "titleShapeId": sd.title["id"] if sd.title else None,
                "textBlocks": [{k: v for k, v in b.items() if k != "text"} for b in body_blocks(sd)],
                "bullets": bullets,
                "tables": sd.tables,
                "charts": sd.charts,
                "images": sd.images,
                "footers": sd.footers,
                "notes": sd.notes,
            }
        )
    return {
        "source": str(src),
        "slideWidthIn": round(prs.slide_width / EMU, 3),
        "slideHeightIn": round(prs.slide_height / EMU, 3),
        "slideCount": len(slides),
        "slides": out_slides,
    }


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="Extract titles, text blocks, bullets, tables, chart data, images and notes from a .pptx "
        "into OUTDIR (extracted.json, assets/); with --to-spec also write a draft deck-spec.json for restyling.",
    )
    ap.add_argument("input", help="input .pptx")
    ap.add_argument("-o", "--outdir", required=True, help="output directory (created if needed)")
    ap.add_argument("--to-spec", action="store_true", help="also write OUTDIR/deck-spec.json (draft, validated)")
    ap.add_argument("--theme", help="theme id for the draft spec (default: an auto-pick theme)")
    ap.add_argument("--density", choices=("speaker-led", "reading-first"), default="speaker-led", help="density written to the draft spec (default speaker-led)")
    args = ap.parse_args(argv)

    src = Path(args.input)
    out = Path(args.outdir)
    try:
        prs = Presentation(str(src))
    except Exception as exc:
        print("error: cannot open %s: %s" % (src, exc), file=sys.stderr)
        return 2
    if args.theme:
        try:
            C.get_theme(args.theme)
        except KeyError as exc:
            print("error: %s" % exc.args[0], file=sys.stderr)
            return 2
    out.mkdir(parents=True, exist_ok=True)
    assets = out / "assets"
    saved: Dict[str, str] = {}
    slides = [read_slide(prs, s, i, assets, saved) for i, s in enumerate(prs.slides, start=1)]
    data = extracted_json(slides, src, prs)
    (out / "extracted.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote %s (%d slide(s), %d image(s) saved)" % (out / "extracted.json", len(slides), len(saved)))
    if not args.to_spec:
        return 0
    if not slides:
        print("error: the deck has no slides", file=sys.stderr)
        return 2
    aspect = "4:3" if abs(prs.slide_width / prs.slide_height - 4 / 3) < 0.05 else "16:9"
    spec = build_spec(slides, src, args.theme, args.density, aspect)
    spec["language"] = detect_language(str(src))
    spec_path = out / "deck-spec.json"
    spec_path.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    import validate_spec as V

    _spec, errors, warnings = V.validate_file(spec_path)
    for e in errors:
        print(str(e), file=sys.stderr)
    roles = ", ".join(s["role"] for s in spec["slides"])
    print("wrote %s (%d slides: %s)" % (spec_path, len(spec["slides"]), roles))
    print("validate_spec: %d error(s), %d warning(s)" % (len(errors), len(warnings)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
