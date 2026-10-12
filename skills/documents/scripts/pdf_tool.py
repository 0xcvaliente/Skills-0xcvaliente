#!/usr/bin/env python3
"""Everyday PDF operations on top of pypdf (pip install pypdf).

  pdf_tool.py info    IN
  pdf_tool.py text    IN [--pages 1-3]
  pdf_tool.py merge   OUT IN1 IN2 [...]
  pdf_tool.py split   IN OUTDIR
  pdf_tool.py extract IN OUT --pages 1-3,7
  pdf_tool.py rotate  IN OUT --degrees 90 [--pages 2,4]
  pdf_tool.py fields  IN                         # list AcroForm fields
  pdf_tool.py fill    IN OUT --values values.json # {"field name": "value"}

Never overwrites IN. Does not redact: drawing over text does not remove it (see sub-skills/pdf).
Page numbers are 1-based. Encrypted PDFs: pass --password.
"""
import argparse
import json
import os
import sys

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:  # pragma: no cover
    print("error: pypdf is required: pip install pypdf", file=sys.stderr)
    sys.exit(2)


def parse_pages(spec, total):
    if not spec:
        return list(range(total))
    out = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            s, e = part.split("-", 1)
            lo, hi = int(s), int(e or total)
        else:
            lo = hi = int(part)
        if lo < 1 or hi > total or lo > hi:
            raise SystemExit(f"error: page range {part!r} outside 1-{total}")
        out.extend(range(lo - 1, hi))
    return out


def open_reader(path, password=None):
    r = PdfReader(path)
    if r.is_encrypted:
        if not password or not r.decrypt(password):
            raise SystemExit("error: PDF is encrypted; pass the correct --password")
    return r


def write(writer, out, force):
    if os.path.exists(out) and not force:
        raise SystemExit(f"error: {out} exists (use --force)")
    with open(out, "wb") as f:
        writer.write(f)
    print(f"wrote {out}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--password")
    ap.add_argument("--force", action="store_true", help="overwrite output files")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("info"); s.add_argument("input")
    s = sub.add_parser("text"); s.add_argument("input"); s.add_argument("--pages")
    s = sub.add_parser("merge"); s.add_argument("output"); s.add_argument("inputs", nargs="+")
    s = sub.add_parser("split"); s.add_argument("input"); s.add_argument("outdir")
    s = sub.add_parser("extract"); s.add_argument("input"); s.add_argument("output"); s.add_argument("--pages", required=True)
    s = sub.add_parser("rotate"); s.add_argument("input"); s.add_argument("output")
    s.add_argument("--degrees", type=int, required=True, choices=[90, 180, 270]); s.add_argument("--pages")
    s = sub.add_parser("fields"); s.add_argument("input")
    s = sub.add_parser("fill"); s.add_argument("input"); s.add_argument("output"); s.add_argument("--values", required=True)
    a = ap.parse_args(argv)

    if a.cmd == "merge":
        w = PdfWriter()
        for p in a.inputs:
            for page in open_reader(p, a.password).pages:
                w.add_page(page)
        return write(w, a.output, a.force)

    r = open_reader(a.input, a.password)
    n = len(r.pages)
    if a.cmd == "info":
        m = r.metadata or {}
        box = r.pages[0].mediabox if n else None
        print(json.dumps({
            "pages": n, "encrypted": r.is_encrypted,
            "page_size_pt": [float(box.width), float(box.height)] if box else None,
            "title": getattr(m, "title", None), "author": getattr(m, "author", None),
            "creator": getattr(m, "creator", None), "producer": getattr(m, "producer", None),
            "has_form_fields": bool(r.get_fields()),
            "text_extractable": any((p.extract_text() or "").strip() for p in r.pages[: min(n, 3)]),
        }, indent=2))
    elif a.cmd == "text":
        for i in parse_pages(a.pages, n):
            print(f"--- page {i + 1} ---")
            print(r.pages[i].extract_text() or "")
    elif a.cmd == "split":
        os.makedirs(a.outdir, exist_ok=True)
        width = len(str(n))
        for i in range(n):
            w = PdfWriter()
            w.add_page(r.pages[i])
            write(w, os.path.join(a.outdir, f"page-{str(i + 1).zfill(width)}.pdf"), a.force)
    elif a.cmd == "extract":
        w = PdfWriter()
        for i in parse_pages(a.pages, n):
            w.add_page(r.pages[i])
        write(w, a.output, a.force)
    elif a.cmd == "rotate":
        targets = set(parse_pages(a.pages, n))
        w = PdfWriter()
        for i, page in enumerate(r.pages):
            if i in targets:
                page.rotate(a.degrees)
            w.add_page(page)
        write(w, a.output, a.force)
    elif a.cmd == "fields":
        fields = r.get_fields() or {}
        if not fields:
            print("no AcroForm fields (scanned or flat form: overlay text instead, see sub-skills/pdf)")
        for name, f in fields.items():
            print(f"{name}\ttype={f.get('/FT')}\tvalue={f.get('/V')!r}\toptions={f.get('/_States_', '')}")
    elif a.cmd == "fill":
        fields = r.get_fields() or {}
        if not fields:
            raise SystemExit("error: no fillable AcroForm fields in this PDF; overlay text instead (see sub-skills/pdf)")
        with open(a.values, encoding="utf-8") as f:
            values = json.load(f)
        unknown = sorted(set(values) - set(fields))
        if unknown:
            raise SystemExit("error: unknown field name(s): " + ", ".join(unknown) + "  (run `fields` to list them)")
        w = PdfWriter(clone_from=r)
        for page in w.pages:
            w.update_page_form_field_values(page, values, auto_regenerate=False)
        w.set_need_appearances_writer(True)
        write(w, a.output, a.force)
        print("filled; open the result and check each field visually before sending")


if __name__ == "__main__":
    main()
