#!/usr/bin/env python3
"""Report which document tools are available and which workflows they unlock.

  doctor.py [--json]

Checks Python libraries, command-line tools and Node packages. Run it once before choosing
an approach so you do not plan around a tool that is not installed. Installing anything is a
separate step that needs the user's go-ahead.
"""
import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import find_soffice  # noqa: E402

PY = {
    "docx": ("python-docx", "create/edit Word files"),
    "openpyxl": ("openpyxl", "create/edit Excel files with formulas and formatting"),
    "pandas": ("pandas", "bulk tabular data in/out"),
    "pptx": ("python-pptx", "create/edit PowerPoint files"),
    "pypdf": ("pypdf", "merge/split/rotate/fill PDFs"),
    "pdfplumber": ("pdfplumber", "PDF text with layout, table extraction"),
    "reportlab": ("reportlab", "create PDFs from code"),
    "PIL": ("pillow", "images, contact sheets"),
    "lxml": ("lxml", "faster/safer XML editing"),
    "pytesseract": ("pytesseract", "OCR from Python (needs tesseract)"),
}
CLI = {
    "soffice": ("LibreOffice", "convert/render/recalculate any Office file"),
    "pandoc": ("pandoc", "Markdown/HTML <-> docx, pdf"),
    "pdftoppm": ("Poppler", "PDF -> page images"),
    "pdftotext": ("Poppler", "PDF text with -layout"),
    "qpdf": ("qpdf", "lossless PDF merge/split/encrypt/repair"),
    "tesseract": ("Tesseract", "OCR scanned pages"),
    "ocrmypdf": ("OCRmyPDF", "make scanned PDFs searchable"),
    "mutool": ("MuPDF", "PDF rendering/inspection"),
    "node": ("Node.js", "docx / pptxgenjs scripts"),
}
NODE = ["docx", "pptxgenjs"]


def node_has(pkg):
    if not shutil.which("node"):
        return False
    try:
        r = subprocess.run(["node", "-e", f"require.resolve('{pkg}')"], capture_output=True, timeout=15)
        return r.returncode == 0
    except Exception:
        return False


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    res = {"python": {}, "cli": {}, "node": {}}
    for mod, (pkg, why) in PY.items():
        res["python"][pkg] = {"available": importlib.util.find_spec(mod) is not None, "for": why}
    for exe, (name, why) in CLI.items():
        found = find_soffice() if exe == "soffice" else shutil.which(exe)
        res["cli"][name] = {"available": bool(found), "path": found, "for": why}
    for pkg in NODE:
        res["node"][pkg] = {"available": node_has(pkg)}
    py, cli = res["python"], res["cli"]
    res["workflows"] = {
        "inspect any docx/xlsx/pptx": True,
        "repack edited OOXML": True,
        "word: create/edit with library": py["python-docx"]["available"] or res["node"]["docx"]["available"],
        "excel: create/edit with formulas": py["openpyxl"]["available"],
        "excel: recalculate + error check": cli["LibreOffice"]["available"],
        "powerpoint: create/edit with library": py["python-pptx"]["available"] or res["node"]["pptxgenjs"]["available"],
        "pdf: merge/split/rotate/fill": py["pypdf"]["available"] or cli["qpdf"]["available"],
        "pdf: create from code": py["reportlab"]["available"],
        "render to PDF": cli["LibreOffice"]["available"],
        "render to page images": cli["Poppler"]["available"] or cli["MuPDF"]["available"],
        "OCR scanned pdf": cli["Tesseract"]["available"] or cli["OCRmyPDF"]["available"],
        "markdown -> docx/pdf": cli["pandoc"]["available"] or cli["LibreOffice"]["available"],
    }
    if a.json:
        print(json.dumps(res, indent=2))
        return
    print(f"python {sys.version.split()[0]}\n")
    for group in ("python", "cli", "node"):
        print(f"{group}:")
        for name, v in res[group].items():
            print(f"  [{'x' if v['available'] else ' '}] {name:<14} {v.get('for', '')}")
    print("\nworkflows:")
    for k, v in res["workflows"].items():
        print(f"  [{'x' if v else ' '}] {k}")
    missing = [n for n, v in res["python"].items() if not v["available"]]
    if missing:
        print("\nnot installed (ask before installing): " + ", ".join(missing))


if __name__ == "__main__":
    main()
