#!/usr/bin/env python3
"""Inspect a .docx, .xlsx or .pptx without any third-party library.

Reports structure, text, comments, tracked changes, errors, notes and metadata
so you can plan an edit or check a result. Read-only: never modifies the file.

Usage:
  inspect_office.py FILE [--text] [--json] [--max-rows N]
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import PackageError, die, local, open_package, read_xml  # noqa: E402

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
PR = "{http://schemas.openxmlformats.org/package/2006/relationships}"


# ---------------------------------------------------------------- shared
def core_props(z):
    root = read_xml(z, "docProps/core.xml")
    out = {}
    if root is not None:
        for el in root:
            if el.text and local(el.tag) in (
                "title", "subject", "creator", "lastModifiedBy", "created", "modified", "keywords", "description",
            ):
                out[local(el.tag)] = el.text
    return out


def rels(z, part):
    """Return {rId: (target_path, type_suffix, external)} for a part."""
    d, f = os.path.split(part)
    root = read_xml(z, f"{d}/_rels/{f}.rels" if d else f"_rels/{f}.rels")
    out = {}
    if root is None:
        return out
    for r in root.iter(f"{PR}Relationship"):
        tgt = r.get("Target", "")
        ext = r.get("TargetMode") == "External"
        if not ext:
            tgt = os.path.normpath(os.path.join(d, tgt)).replace("\\", "/") if not tgt.startswith("/") else tgt[1:]
        out[r.get("Id")] = (tgt, r.get("Type", "").rsplit("/", 1)[-1], ext)
    return out


def paragraph_text(p, wns):
    parts = []
    for el in p.iter():
        t = local(el.tag)
        if t in ("t", "delText") and el.text:
            parts.append(el.text)
        elif t == "tab":
            parts.append("\t")
        elif t in ("br", "cr"):
            parts.append("\n")
    return "".join(parts)


def names(z):
    return z.namelist()


# ------------------------------------------------------------------ docx
def inspect_docx(z, want_text):
    doc = read_xml(z, "word/document.xml")
    if doc is None:
        raise PackageError("word/document.xml missing: not a Word document")
    body = doc.find(f"{W}body")
    info = {"type": "docx", "metadata": core_props(z)}
    paragraphs, outline, text_lines = 0, [], []
    for p in body.iter(f"{W}p"):
        paragraphs += 1
        style_el = p.find(f"{W}pPr/{W}pStyle")
        style = style_el.get(f"{W}val") if style_el is not None else ""
        txt = paragraph_text(p, W)
        if re.match(r"(?i)^(heading\s*\d|title|subtitle)", style) and txt.strip():
            m = re.search(r"(\d)$", style)
            outline.append({"level": int(m.group(1)) if m else 0, "text": txt.strip()})
        if want_text and txt.strip():
            text_lines.append(txt)
    info.update(
        paragraphs=paragraphs,
        tables=len(list(body.iter(f"{W}tbl"))),
        images=len([n for n in names(z) if n.startswith("word/media/")]),
        outline=outline,
    )
    sect = body.find(f".//{W}sectPr/{W}pgSz")
    if sect is not None:
        w, h = int(sect.get(f"{W}w", 0)), int(sect.get(f"{W}h", 0))
        info["page"] = {
            "width_in": round(w / 1440, 2), "height_in": round(h / 1440, 2),
            "orientation": sect.get(f"{W}orient", "portrait"),
        }
    comments = []
    croot = read_xml(z, "word/comments.xml")
    if croot is not None:
        for c in croot.iter(f"{W}comment"):
            comments.append({
                "id": c.get(f"{W}id"), "author": c.get(f"{W}author"), "date": c.get(f"{W}date"),
                "text": " ".join(paragraph_text(p, W) for p in c.iter(f"{W}p")).strip(),
            })
    info["comments"] = comments
    tracked = {"insertions": 0, "deletions": 0, "authors": set()}
    for el in doc.iter():
        t = local(el.tag)
        if t in ("ins", "del") and el.get(f"{W}author"):
            tracked["insertions" if t == "ins" else "deletions"] += 1
            tracked["authors"].add(el.get(f"{W}author"))
    tracked["authors"] = sorted(tracked["authors"])
    info["tracked_changes"] = tracked
    instr = " ".join((el.text or "") for el in doc.iter(f"{W}instrText"))
    instr += " ".join(el.get(f"{W}instr", "") for el in doc.iter(f"{W}fldSimple"))
    info["fields"] = sorted({m.group(1) for m in re.finditer(r"\b(TOC|PAGE|NUMPAGES|REF|HYPERLINK|DATE)\b", instr)})
    info["hyperlinks_external"] = sum(1 for r in rels(z, "word/document.xml").values() if r[1] == "hyperlink" and r[2])
    info["has_macros"] = "word/vbaProject.bin" in names(z)
    info["footnotes"] = "word/footnotes.xml" in names(z)
    if want_text:
        info["text"] = "\n".join(text_lines)
    return info


# ------------------------------------------------------------------ xlsx
def shared_strings(z):
    root = read_xml(z, "xl/sharedStrings.xml")
    out = []
    if root is not None:
        for si in root.iter(f"{S}si"):
            out.append("".join(t.text or "" for t in si.iter(f"{S}t")))
    return out


def col_to_num(ref):
    letters = re.match(r"[A-Z]+", ref).group(0)
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n


def inspect_xlsx(z, want_text, max_rows=50):
    wb = read_xml(z, "xl/workbook.xml")
    if wb is None:
        raise PackageError("xl/workbook.xml missing: not an Excel workbook")
    wrels = rels(z, "xl/workbook.xml")
    sst = shared_strings(z)
    info = {"type": "xlsx", "metadata": core_props(z), "sheets": []}
    for sh in wb.iter(f"{S}sheet"):
        rid = sh.get(f"{R}id")
        path = wrels.get(rid, ("",))[0]
        sheet = {"name": sh.get("name"), "state": sh.get("state", "visible"), "part": path}
        root = read_xml(z, path) if path else None
        if root is None:
            sheet["error"] = "sheet part missing"
            info["sheets"].append(sheet)
            continue
        dim = root.find(f"{S}dimension")
        sheet["dimension"] = dim.get("ref") if dim is not None else None
        cells = formulas = uncached = 0
        errors, rows_out = [], []
        for row in root.iter(f"{S}row"):
            line = {}
            for c in row.findall(f"{S}c"):
                cells += 1
                ref, t = c.get("r"), c.get("t")
                f, v = c.find(f"{S}f"), c.find(f"{S}v")
                if f is not None:
                    formulas += 1
                    if v is None or v.text in (None, ""):
                        uncached += 1
                val = v.text if v is not None else None
                if t == "s" and val is not None:
                    val = sst[int(val)] if int(val) < len(sst) else val
                elif t == "inlineStr":
                    val = "".join(x.text or "" for x in c.iter(f"{S}t"))
                if t == "e":
                    errors.append({"cell": ref, "value": val, "formula": f.text if f is not None else None})
                if want_text and val not in (None, "") and len(rows_out) < max_rows:
                    line[col_to_num(ref)] = ("=" + f.text + " -> " if f is not None and f.text else "") + str(val)
            if want_text and line and len(rows_out) < max_rows:
                width = max(line)
                rows_out.append((row.get("r"), [line.get(i, "") for i in range(1, width + 1)]))
        sheet.update(cells=cells, formulas=formulas, formulas_without_cached_value=uncached,
                     errors=errors[:25], error_count=len(errors),
                     merged_ranges=len(list(root.iter(f"{S}mergeCell"))))
        if want_text:
            sheet["rows"] = [{"row": r, "values": vals} for r, vals in rows_out]
        info["sheets"].append(sheet)
    info["defined_names"] = [d.get("name") for d in wb.iter(f"{S}definedName")]
    info["charts"] = len([n for n in names(z) if n.startswith("xl/charts/chart")])
    info["external_links"] = len([n for n in names(z) if n.startswith("xl/externalLinks/externalLink")])
    info["has_macros"] = "xl/vbaProject.bin" in names(z)
    return info


# ------------------------------------------------------------------ pptx
def slide_order(z):
    pres = read_xml(z, "ppt/presentation.xml")
    if pres is None:
        raise PackageError("ppt/presentation.xml missing: not a PowerPoint file")
    prels = rels(z, "ppt/presentation.xml")
    order = []
    for sid in pres.iter(f"{P}sldId"):
        tgt = prels.get(sid.get(f"{R}id"))
        if tgt:
            order.append(tgt[0])
    return pres, order


def inspect_pptx(z, want_text):
    pres, order = slide_order(z)
    info = {"type": "pptx", "metadata": core_props(z), "slides": []}
    sz = pres.find(f"{P}sldSz")
    if sz is not None:
        cx, cy = int(sz.get("cx")), int(sz.get("cy"))
        info["size_in"] = {"width": round(cx / 914400, 2), "height": round(cy / 914400, 2)}
    for i, part in enumerate(order, 1):
        root = read_xml(z, part)
        srels = rels(z, part)
        title, lines = None, []
        for sp in root.iter(f"{P}sp"):
            ph = sp.find(f"{P}nvSpPr/{P}nvPr/{P}ph")
            paras = ["".join(t.text or "" for t in p.iter(f"{A}t")) for p in sp.iter(f"{A}p")]
            paras = [x for x in paras if x.strip()]
            if ph is not None and ph.get("type") in ("title", "ctrTitle") and paras:
                title = " ".join(paras)
            lines.extend(paras)
        pics = list(root.iter(f"{P}pic"))
        missing_alt = sum(1 for p in pics if not (p.find(f"{P}nvPicPr/{P}cNvPr").get("descr") or "").strip())
        notes = ""
        for tgt, typ, ext in srels.values():
            if typ == "notesSlide":
                nroot = read_xml(z, tgt)
                if nroot is not None:
                    notes = " ".join(
                        "".join(t.text or "" for t in p.iter(f"{A}t"))
                        for sp in nroot.iter(f"{P}sp")
                        if (sp.find(f"{P}nvSpPr/{P}nvPr/{P}ph") is not None
                            and sp.find(f"{P}nvSpPr/{P}nvPr/{P}ph").get("type") == "body")
                        for p in sp.iter(f"{A}p")
                    ).strip()
        layout = ""
        for tgt, typ, ext in srels.values():
            if typ == "slideLayout":
                lroot = read_xml(z, tgt)
                cs = lroot.find(f"{P}cSld") if lroot is not None else None
                layout = cs.get("name", "") if cs is not None else ""
        slide = {
            "n": i, "part": part, "title": title, "layout": layout,
            "text_lines": len(lines), "pictures": len(pics), "pictures_missing_alt": missing_alt,
            "tables": len(list(root.iter(f"{A}tbl"))),
            "charts": sum(1 for r in srels.values() if r[1] == "chart"),
            "has_notes": bool(notes), "hidden": root.get("show") == "0",
        }
        if want_text:
            slide["text"] = lines
            slide["notes"] = notes
        info["slides"].append(slide)
    info["slide_count"] = len(order)
    info["has_macros"] = "ppt/vbaProject.bin" in names(z)
    return info


# ---------------------------------------------------------------- output
def inspect(path, want_text=False, max_rows=50):
    ext = os.path.splitext(path)[1].lower()
    z = open_package(path)
    if ext in (".docx", ".dotx", ".docm"):
        return inspect_docx(z, want_text)
    if ext in (".xlsx", ".xltx", ".xlsm"):
        return inspect_xlsx(z, want_text, max_rows)
    if ext in (".pptx", ".potx", ".pptm"):
        return inspect_pptx(z, want_text)
    raise PackageError(f"unsupported extension {ext!r}: expected .docx, .xlsx or .pptx")


def render_text(info):
    out = [f"type: {info['type']}"]
    md = info.get("metadata") or {}
    if md:
        out.append("metadata: " + ", ".join(f"{k}={v}" for k, v in md.items()))
    if info["type"] == "docx":
        out.append(f"paragraphs: {info['paragraphs']}  tables: {info['tables']}  images: {info['images']}")
        if "page" in info:
            p = info["page"]
            out.append(f"page: {p['width_in']}x{p['height_in']} in ({p['orientation']})")
        out.append("outline:")
        out += [f"  {'  ' * max(h['level'] - 1, 0)}- {h['text']}" for h in info["outline"]] or ["  (no heading styles)"]
        tc = info["tracked_changes"]
        out.append(f"tracked changes: {tc['insertions']} insertions, {tc['deletions']} deletions {tc['authors']}")
        out.append(f"comments: {len(info['comments'])}")
        out += [f"  [{c['id']}] {c['author']}: {c['text'][:100]}" for c in info["comments"]]
        out.append(f"fields: {info['fields']}  external links: {info['hyperlinks_external']}  macros: {info['has_macros']}")
    elif info["type"] == "xlsx":
        for s in info["sheets"]:
            out.append(
                f"sheet {s['name']!r} [{s['state']}] dim={s.get('dimension')} cells={s.get('cells')} "
                f"formulas={s.get('formulas')} uncached={s.get('formulas_without_cached_value')} "
                f"errors={s.get('error_count')} merged={s.get('merged_ranges')}"
            )
            for e in s.get("errors", [])[:5]:
                out.append(f"    {e['cell']}: {e['value']}  {e['formula'] or ''}")
            for r in s.get("rows", []):
                out.append(f"    {r['row']}: " + " | ".join(r["values"]))
        out.append(f"charts: {info['charts']}  defined names: {info['defined_names']}  "
                   f"external links: {info['external_links']}  macros: {info['has_macros']}")
    else:
        out.append(f"slides: {info['slide_count']}  size: {info.get('size_in')}")
        for s in info["slides"]:
            flags = []
            if not s["title"]:
                flags.append("no title")
            if s["pictures_missing_alt"]:
                flags.append(f"{s['pictures_missing_alt']} picture(s) without alt text")
            if s["hidden"]:
                flags.append("hidden")
            out.append(f"  {s['n']:>2}. {s['title'] or '(untitled)'}  [{s['layout']}] "
                       f"lines={s['text_lines']} pics={s['pictures']} charts={s['charts']} "
                       f"tables={s['tables']} notes={'yes' if s['has_notes'] else 'no'}"
                       + (f"  <{'; '.join(flags)}>" if flags else ""))
            for line in s.get("text", []):
                out.append(f"        {line}")
            if s.get("notes"):
                out.append(f"        notes: {s['notes']}")
        out.append(f"macros: {info['has_macros']}")
    if "text" in info:
        out += ["", "--- text ---", info["text"]]
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--text", action="store_true", help="include document text / cell values / slide text")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--max-rows", type=int, default=50, help="rows per sheet with --text (default 50)")
    a = ap.parse_args(argv)
    try:
        info = inspect(a.file, a.text, a.max_rows)
    except PackageError as e:
        die(str(e))
    print(json.dumps(info, indent=2, ensure_ascii=False) if a.json else render_text(info))


if __name__ == "__main__":
    main()
