#!/usr/bin/env python3
"""Measure visual-design problems in a .docx, .xlsx, .pptx or .pdf.

  design_audit.py FILE [--json] [--min-severity info|warn|error]

Reports what can be measured from the file itself (font sizes and families, margins,
explicit colour contrast, alt text, off-slide or overlapping shapes, text density, clipped
spreadsheet text, PDF font embedding). It cannot judge taste: always also look at a render
(scripts/render.py). Sizes and colours that are inherited from a theme or template are only
checked where the file states them, so a clean report is not proof of a good design.

Severities: error = fix before delivering; warn = fix unless there is a reason; info = look.
Exit code 1 when any error is found. Rules and thresholds: sub-skills/design/GUIDE.md.
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import PackageError, die, local, open_package, read_xml  # noqa: E402
from _design import contrast_ratio, required_ratio  # noqa: E402
from inspect_office import (A, P, R, S, W, col_to_num, rels, shared_strings,  # noqa: E402
                            slide_order)

SEV = {"info": 0, "warn": 1, "error": 2}
EMU_IN = 914400


class Report:
    def __init__(self):
        self.items = []

    def add(self, severity, rule, where, message):
        self.items.append({"severity": severity, "rule": rule, "where": where, "message": message})


def hexcolor(val):
    return "#" + val.upper() if val and re.fullmatch(r"[0-9a-fA-F]{6}", val) else None


# ------------------------------------------------------------------ docx
def style_table(styles):
    """styleId -> {'sz','font','color','bold','based'} and docDefaults."""
    out, defaults = {}, {}
    if styles is None:
        return out, defaults

    def props(rpr):
        d = {}
        if rpr is None:
            return d
        sz = rpr.find(f"{W}sz")
        if sz is not None:
            d["sz"] = int(sz.get(f"{W}val")) / 2
        rf = rpr.find(f"{W}rFonts")
        if rf is not None:
            d["font"] = rf.get(f"{W}ascii") or rf.get(f"{W}hAnsi")
        c = rpr.find(f"{W}color")
        if c is not None:
            d["color"] = hexcolor(c.get(f"{W}val"))
        b = rpr.find(f"{W}b")
        if b is not None:
            d["bold"] = b.get(f"{W}val") not in ("0", "false")
        return d

    dd = styles.find(f"{W}docDefaults/{W}rPrDefault/{W}rPr")
    defaults = props(dd)
    for st in styles.iter(f"{W}style"):
        sid = st.get(f"{W}styleId")
        d = props(st.find(f"{W}rPr"))
        b = st.find(f"{W}basedOn")
        d["based"] = b.get(f"{W}val") if b is not None else None
        out[sid] = d
    return out, defaults


def resolve(styles, defaults, style_id, key):
    seen = set()
    while style_id and style_id not in seen:
        seen.add(style_id)
        st = styles.get(style_id)
        if not st:
            break
        if key in st and st[key] is not None:
            return st[key]
        style_id = st.get("based")
    return defaults.get(key)


def audit_docx(z, rep):
    doc = read_xml(z, "word/document.xml")
    styles, defaults = style_table(read_xml(z, "word/styles.xml"))
    body = doc.find(f"{W}body")
    sizes, fonts, empty_run, max_empty, heads, paras = {}, {}, 0, 0, 0, 0
    contrast_seen = set()
    parent = {c: par for par in body.iter() for c in par}

    def cell_fill(el):
        while el is not None:
            if local(el.tag) == "tc":
                shd = el.find(f"{W}tcPr/{W}shd")
                return hexcolor(shd.get(f"{W}fill")) if shd is not None else None
            el = parent.get(el)
        return None

    for p in body.iter(f"{W}p"):
        paras += 1
        ps = p.find(f"{W}pPr/{W}pStyle")
        pstyle = ps.get(f"{W}val") if ps is not None else None
        if pstyle and re.match(r"(?i)heading|title", pstyle):
            heads += 1
        text = "".join(t.text or "" for t in p.iter(f"{W}t"))
        if not text.strip() and p.find(f".//{W}drawing") is None and p.find(f".//{W}br") is None:
            empty_run += 1
            max_empty = max(max_empty, empty_run)
        else:
            empty_run = 0
        shd = p.find(f"{W}pPr/{W}shd")
        bg = (hexcolor(shd.get(f"{W}fill")) if shd is not None else None) or cell_fill(p)
        for r in p.findall(f".//{W}r"):
            t = "".join(x.text or "" for x in r.findall(f"{W}t"))
            if not t.strip():
                continue
            rpr = r.find(f"{W}rPr")
            rs = rpr.find(f"{W}rStyle").get(f"{W}val") if rpr is not None and rpr.find(f"{W}rStyle") is not None else None
            def get(key):
                v = None
                if rpr is not None:
                    el = {"sz": rpr.find(f"{W}sz"), "color": rpr.find(f"{W}color")}.get(key)
                    if el is not None:
                        v = int(el.get(f"{W}val")) / 2 if key == "sz" else hexcolor(el.get(f"{W}val"))
                    if key == "font" and rpr.find(f"{W}rFonts") is not None:
                        v = rpr.find(f"{W}rFonts").get(f"{W}ascii")
                if v is None and rs:
                    v = resolve(styles, defaults, rs, key)
                if v is None:
                    v = resolve(styles, defaults, pstyle or "Normal", key)
                return v
            sz, font, color = get("sz"), get("font"), get("color")
            if sz:
                sizes[sz] = sizes.get(sz, 0) + len(t)
            if font:
                fonts[font] = fonts.get(font, 0) + len(t)
            if color and (color, bg, sz) not in contrast_seen:
                contrast_seen.add((color, bg, sz))
                bgc = bg or "#FFFFFF"
                ratio = contrast_ratio(color, bgc)
                need = required_ratio(sz, False)
                if ratio < need:
                    rep.add("error", "D-CONTRAST", f"text {t[:30]!r}",
                            f"{color} on {bgc} is {ratio:.2f}:1 at {sz or 'default'} pt; needs {need}:1")
    if sizes:
        small = {s: n for s, n in sizes.items() if s < 9}
        if small:
            rep.add("warn", "D-FONT-SIZE", "runs", f"text below 9 pt ({', '.join(f'{s:g} pt' for s in sorted(small))}): hard to read in print and on screen")
        body_size = max(sizes, key=sizes.get)
        if body_size < 10:
            rep.add("warn", "D-BODY-SIZE", "body", f"most text is {body_size:g} pt; aim for 10.5-12 pt")
    if len(fonts) > 3:
        rep.add("warn", "D-FONT-FAMILIES", "document", f"{len(fonts)} font families in use ({', '.join(sorted(fonts))}); use one or two")
    sect = body.find(f".//{W}sectPr/{W}pgMar")
    if sect is not None:
        for side in ("left", "right", "top", "bottom"):
            v = sect.get(f"{W}{side}")
            if v is not None:
                inches = int(v) / 1440
                if inches < 0.5:
                    rep.add("error", "D-MARGINS", f"{side} margin", f"{inches:.2f} in is under the printable minimum of 0.5 in")
                elif inches < 0.75:
                    rep.add("warn", "D-MARGINS", f"{side} margin", f"{inches:.2f} in is tight; 0.8-1.2 in reads better")
    if paras > 30 and heads == 0:
        rep.add("warn", "D-HEADINGS", "document", "long document with no Title/Heading styles (no navigation, TOC or accessibility structure)")
    if max_empty >= 3:
        rep.add("warn", "D-EMPTY-PARAS", "document", f"{max_empty} empty paragraphs in a row used as spacing; use paragraph spacing or page-break-before")
    for tbl in body.iter(f"{W}tbl"):
        first = tbl.find(f"{W}tr")
        if first is not None and first.find(f"{W}trPr/{W}tblHeader") is None and len(tbl.findall(f"{W}tr")) > 3:
            rep.add("warn", "D-TABLE-HEADER", "table", "first row is not marked as a repeating header row")
    for dp in doc.iter("{http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing}docPr"):
        if not (dp.get("descr") or "").strip() and dp.get("hidden") != "1":
            rep.add("warn", "D-ALT-TEXT", f"image {dp.get('name', '')}", "no alt text")
    lang = styles_has_lang(read_xml(z, "word/styles.xml"))
    if not lang:
        rep.add("info", "D-LANGUAGE", "styles", "no document language set (affects spell-check and screen readers)")


def styles_has_lang(styles):
    if styles is None:
        return False
    return styles.find(f".//{W}lang") is not None


# ------------------------------------------------------------------ pptx
def audit_pptx(z, rep):
    pres, order = slide_order(z)
    sz = pres.find(f"{P}sldSz")
    sw, sh = int(sz.get("cx")), int(sz.get("cy"))
    families = {}
    for n, part in enumerate(order, 1):
        root = read_xml(z, part)
        where = f"slide {n}"
        bg_el = root.find(f"{P}cSld/{P}bg//{A}srgbClr")
        slide_bg = hexcolor(bg_el.get("val")) if bg_el is not None else None
        has_title, words = False, 0
        boxes = []
        for sp in root.iter(f"{P}sp"):
            ph = sp.find(f"{P}nvSpPr/{P}nvPr/{P}ph")
            paras = list(sp.iter(f"{A}p"))
            text = " ".join("".join(t.text or "" for t in p.iter(f"{A}t")) for p in paras).strip()
            if ph is not None and ph.get("type") in ("title", "ctrTitle") and text:
                has_title = True
            if ph is not None and not text and ph.get("type") not in ("sldNum", "dt", "ftr"):
                rep.add("warn", "P-EMPTY-PLACEHOLDER", where, "empty placeholder ('Click to add...' shows in edit view)")
            if ph is None or ph.get("type") not in ("sldNum", "dt", "ftr"):
                words += len(text.split())
            off, ext = sp.find(f"{P}spPr/{A}xfrm/{A}off"), sp.find(f"{P}spPr/{A}xfrm/{A}ext")
            if off is not None and ext is not None:
                x, y, cx, cy = int(off.get("x")), int(off.get("y")), int(ext.get("cx")), int(ext.get("cy"))
                if x < 0 or y < 0 or x + cx > sw * 1.001 or y + cy > sh * 1.001:
                    rep.add("error", "P-OFF-SLIDE", where, f"shape {sp.find(f'{P}nvSpPr/{P}cNvPr').get('name')!r} extends beyond the slide")
                if text:
                    boxes.append((x, y, cx, cy, sp.find(f"{P}nvSpPr/{P}cNvPr").get("name")))
            for r in sp.iter(f"{A}r"):
                rpr = r.find(f"{A}rPr")
                t = (r.find(f"{A}t").text or "") if r.find(f"{A}t") is not None else ""
                if rpr is None or not t.strip():
                    continue
                size = int(rpr.get("sz")) / 100 if rpr.get("sz") else None
                if size is not None:
                    if size < 12:
                        rep.add("error", "P-FONT-SIZE", where, f"{size:g} pt text {t[:25]!r}: nothing on a slide should be under 12 pt")
                    elif size < 16:
                        rep.add("info", "P-FONT-SIZE", where, f"{size:g} pt text {t[:25]!r}: small for presenting (ok for footnotes)")
                lat = rpr.find(f"{A}latin")
                if lat is not None and lat.get("typeface") and not lat.get("typeface").startswith("+"):
                    families[lat.get("typeface")] = families.get(lat.get("typeface"), 0) + 1
                fill = rpr.find(f"{A}solidFill/{A}srgbClr")
                if fill is not None:
                    fg, bgc = hexcolor(fill.get("val")), slide_bg or "#FFFFFF"
                    if fg:
                        need = required_ratio(size, rpr.get("b") == "1")
                        ratio = contrast_ratio(fg, bgc)
                        if ratio < need:
                            rep.add("error", "P-CONTRAST", where, f"{fg} on {bgc} is {ratio:.2f}:1 for {t[:25]!r}; needs {need}:1")
            for ppr in sp.iter(f"{A}pPr"):
                if int(ppr.get("lvl", "0")) >= 2:
                    rep.add("warn", "P-BULLET-DEPTH", where, "bullets nested 3+ levels deep; restructure into separate slides or a table")
                    break
        for pic in root.iter(f"{P}pic"):
            c = pic.find(f"{P}nvPicPr/{P}cNvPr")
            if not (c.get("descr") or "").strip():
                rep.add("warn", "P-ALT-TEXT", where, f"picture {c.get('name')!r} has no alt text")
        if not has_title:
            rep.add("warn", "P-TITLE", where, "no title placeholder text (hurts navigation and accessibility)")
        if words > 90:
            rep.add("error", "P-TEXT-DENSITY", where, f"{words} words: a wall of text; split it or move detail to notes")
        elif words > 60:
            rep.add("warn", "P-TEXT-DENSITY", where, f"{words} words; aim for under ~50")
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                a, b = boxes[i], boxes[j]
                ox = min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0])
                oy = min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1])
                if ox > 0 and oy > 0:
                    smaller = min(a[2] * a[3], b[2] * b[3]) or 1
                    if ox * oy / smaller > 0.15:
                        rep.add("warn", "P-OVERLAP", where, f"text boxes {a[4]!r} and {b[4]!r} overlap")
    if len(families) > 3:
        rep.add("warn", "P-FONT-FAMILIES", "deck", f"{len(families)} font families set explicitly ({', '.join(sorted(families))}); use the theme fonts")


# ------------------------------------------------------------------ xlsx
def audit_xlsx(z, rep):
    wb = read_xml(z, "xl/workbook.xml")
    wrels = rels(z, "xl/workbook.xml")
    sst = shared_strings(z)
    styles = read_xml(z, "xl/styles.xml")
    fonts, xfs, numfmts = [], [], {}
    if styles is not None:
        for f in styles.iter(f"{S}font"):
            fonts.append({"b": f.find(f"{S}b") is not None, "name": (f.find(f"{S}name").get("val") if f.find(f"{S}name") is not None else None)})
        xf_parent = styles.find(f"{S}cellXfs")
        if xf_parent is not None:
            xfs = [{"font": int(x.get("fontId", 0)), "fmt": int(x.get("numFmtId", 0))} for x in xf_parent.findall(f"{S}xf")]
    used = {f["name"] for f in fonts if f["name"]}
    if len(used) > 3:
        rep.add("warn", "X-FONT-FAMILIES", "workbook", f"{len(used)} font families defined ({', '.join(sorted(used))})")
    for sh in wb.iter(f"{S}sheet"):
        path = wrels.get(sh.get(f"{R}id"), ("",))[0]
        root = read_xml(z, path) if path else None
        if root is None:
            continue
        name = sh.get("name")
        widths = {}
        for c in root.iter(f"{S}col"):
            for i in range(int(c.get("min")), int(c.get("max")) + 1):
                widths[i] = float(c.get("width", 8.43))
        rows = list(root.iter(f"{S}row"))
        if not rows:
            continue
        first_cells = rows[0].findall(f"{S}c")
        texty = [c for c in first_cells if c.get("t") in ("s", "inlineStr")]
        if len(rows) > 3 and texty:
            bold = sum(1 for c in texty if xfs and fonts and int(c.get("s", 0)) < len(xfs)
                       and xfs[int(c.get("s", 0))]["font"] < len(fonts) and fonts[xfs[int(c.get("s", 0))]["font"]]["b"])
            if bold == 0:
                rep.add("warn", "X-HEADER-STYLE", name, "header row is not bold/styled; headers should be visibly distinct")
        has_pane = root.find(f".//{S}pane") is not None
        if len(rows) > 20 and not has_pane:
            rep.add("info", "X-FREEZE", name, f"{len(rows)} rows and no frozen header row")
        clipped = 0
        for row in rows:
            cells = row.findall(f"{S}c")
            by_col = {col_to_num(c.get("r")): c for c in cells}
            for ci, c in by_col.items():
                if c.get("t") not in ("s", "inlineStr"):
                    continue
                v = c.find(f"{S}v")
                if c.get("t") == "s" and v is not None and v.text is not None and int(v.text) < len(sst):
                    txt = sst[int(v.text)]
                elif c.get("t") == "inlineStr":
                    txt = "".join(x.text or "" for x in c.iter(f"{S}t"))
                else:
                    continue
                width = widths.get(ci, 8.43)
                nxt = by_col.get(ci + 1)
                nxt_has = nxt is not None and (nxt.find(f"{S}v") is not None or nxt.find(f"{S}is") is not None)
                if nxt_has and len(txt) > width * 1.15:
                    clipped += 1
        if clipped:
            rep.add("warn", "X-CLIPPED-TEXT", name, f"{clipped} text cell(s) longer than their column and next to a filled cell, so the text is cut off; widen the column or wrap")
        raw_numbers = 0
        for c in root.iter(f"{S}c"):
            if c.get("t") in (None, "n") and c.find(f"{S}v") is not None and c.find(f"{S}f") is None:
                try:
                    val = float(c.find(f"{S}v").text)
                except (TypeError, ValueError):
                    continue
                sidx = int(c.get("s", 0))
                fmt = xfs[sidx]["fmt"] if sidx < len(xfs) else 0
                if fmt == 0 and (abs(val) >= 10000 or (val != int(val) and len(repr(val)) > 6)):
                    raw_numbers += 1
        if raw_numbers > 3:
            rep.add("warn", "X-NUMBER-FORMAT", name, f"{raw_numbers} large or long-decimal numbers use the General format; set thousands separators, fixed decimals, or percent/currency")
        merges = len(list(root.iter(f"{S}mergeCell")))
        if merges > 5:
            rep.add("info", "X-MERGED", name, f"{merges} merged ranges; merges break sorting, filtering, and screen readers in data tables")


# ------------------------------------------------------------------- pdf
def audit_pdf(path, rep):
    try:
        from pypdf import PdfReader
    except ImportError:
        die("pypdf is required for PDF audits: pip install pypdf")
    r = PdfReader(path)
    if r.is_encrypted:
        die("PDF is encrypted; decrypt first")
    sizes = set()
    unembedded = set()
    small = {}
    for i, page in enumerate(r.pages, 1):
        box = page.mediabox
        sizes.add((round(float(box.width)), round(float(box.height))))
        res = page.get("/Resources")
        fonts = (res.get_object().get("/Font") if res is not None else None)
        if fonts is not None:
            for key, ref in fonts.get_object().items():
                f = ref.get_object()
                desc = f.get("/FontDescriptor")
                base = str(f.get("/BaseFont", key))
                if f.get("/Subtype") == "/Type0":
                    desc = None
                    kids = f.get("/DescendantFonts")
                    if kids:
                        desc = kids.get_object()[0].get_object().get("/FontDescriptor")
                std14 = base.lstrip("/").split("+")[-1] in (
                    "Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Helvetica-BoldOblique", "Times-Roman",
                    "Times-Bold", "Times-Italic", "Times-BoldItalic", "Courier", "Courier-Bold", "Courier-Oblique",
                    "Courier-BoldOblique", "Symbol", "ZapfDingbats")
                if desc is not None:
                    d = desc.get_object()
                    if not any(k in d for k in ("/FontFile", "/FontFile2", "/FontFile3")):
                        unembedded.add(base)
                elif not std14:
                    unembedded.add(base)

        def visitor(text, cm, tm, font_dict, font_size, _small=small, _i=i):
            if text.strip() and font_size:
                eff = abs(font_size * (tm[3] if tm[3] else 1))
                if 0 < eff < 7:
                    _small[_i] = min(_small.get(_i, 99), round(eff, 1))
        try:
            page.extract_text(visitor_text=visitor)
        except Exception:
            pass
    if len(sizes) > 1:
        rep.add("info", "F-PAGE-SIZE", "document", f"mixed page sizes: {sorted(sizes)} points")
    if unembedded:
        rep.add("warn", "F-FONTS-NOT-EMBEDDED", "document", f"fonts not embedded: {', '.join(sorted(unembedded))}; they may be substituted on other machines")
    if small:
        pages = ", ".join(str(p) for p in sorted(small)[:10])
        rep.add("warn", "F-FONT-SIZE", f"pages {pages}", f"text below 7 pt (smallest {min(small.values())} pt)")
    root = r.trailer["/Root"]
    mark = root.get("/MarkInfo")
    if not (mark and mark.get_object().get("/Marked")):
        rep.add("info", "F-TAGGED", "document", "not a tagged PDF (screen readers get no structure); export from a source with real headings if accessibility matters")
    if "/Lang" not in root:
        rep.add("info", "F-LANGUAGE", "document", "no document language set")
    meta = r.metadata
    if not (meta and meta.title):
        rep.add("info", "F-TITLE", "document", "no title in document properties")
    if not any((p.extract_text() or "").strip() for p in r.pages[:3]):
        rep.add("info", "F-NO-TEXT", "document", "no extractable text in the first pages (scanned image?); OCR if it must be searchable or accessible")


# ------------------------------------------------------------------ main
def audit(path):
    ext = os.path.splitext(path)[1].lower()
    rep = Report()
    if ext == ".pdf":
        audit_pdf(path, rep)
        return rep
    z = open_package(path)
    if ext in (".docx", ".dotx", ".docm"):
        audit_docx(z, rep)
    elif ext in (".pptx", ".potx", ".pptm"):
        audit_pptx(z, rep)
    elif ext in (".xlsx", ".xltx", ".xlsm"):
        audit_xlsx(z, rep)
    else:
        raise PackageError(f"unsupported extension {ext!r}: expected .docx, .xlsx, .pptx or .pdf")
    return rep


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--min-severity", choices=list(SEV), default="info")
    a = ap.parse_args(argv)
    try:
        rep = audit(a.file)
    except PackageError as e:
        die(str(e))
    items = [i for i in rep.items if SEV[i["severity"]] >= SEV[a.min_severity]]
    items.sort(key=lambda i: (-SEV[i["severity"]], i["rule"], i["where"]))
    errors = sum(1 for i in items if i["severity"] == "error")
    if a.json:
        print(json.dumps({"file": a.file, "errors": errors, "findings": items}, indent=2))
    else:
        for i in items:
            print(f"{i['severity'].upper():5} {i['rule']:<22} {i['where']}: {i['message']}")
        warns = sum(1 for i in items if i["severity"] == "warn")
        print(f"{errors} error(s), {warns} warning(s), {len(items) - errors - warns} note(s). "
              "Measured from the file only: also look at a render.")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
