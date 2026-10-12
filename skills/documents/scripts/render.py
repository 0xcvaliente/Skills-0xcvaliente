#!/usr/bin/env python3
"""Render a document to PDF and page images so you can look at the result.

  render.py FILE [--outdir DIR] [--dpi 80] [--pages 1-3] [--montage]

Uses LibreOffice (headless, throwaway profile) for .docx/.xlsx/.pptx/.odt/.html/etc., then
`pdftoppm` (Poppler) or `mutool` for page images. Prints every file it wrote. Rendering is an
approximation of Word/Excel/PowerPoint: fonts missing on this machine are substituted, so
pagination can differ from the real application.
"""
import argparse
import glob
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import clean_err, die, find_soffice  # noqa: E402


def to_pdf(src, outdir, timeout=180):
    soffice = find_soffice()
    if not soffice:
        die("LibreOffice not found. Install it (or set SOFFICE=/path/to/soffice), or open the file in the real application.")
    profile = tempfile.mkdtemp(prefix="lo-profile-")
    try:
        cmd = [soffice, f"-env:UserInstallation={Path(profile).as_uri()}", "--headless", "--norestore",
               "--convert-to", "pdf", "--outdir", outdir, src]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        die(f"LibreOffice timed out after {timeout}s (huge file, or a stuck instance: close other LibreOffice windows)")
    finally:
        shutil.rmtree(profile, ignore_errors=True)
    pdf = os.path.join(outdir, Path(src).stem + ".pdf")
    if r.returncode != 0 or not os.path.exists(pdf):
        die(f"conversion failed: {clean_err(r)}")
    return pdf


def rasterize(pdf, outdir, dpi, first, last):
    prefix = os.path.join(outdir, Path(pdf).stem + "-page")
    if shutil.which("pdftoppm"):
        cmd = ["pdftoppm", "-r", str(dpi), "-png"]
        if first:
            cmd += ["-f", str(first)]
        if last:
            cmd += ["-l", str(last)]
        subprocess.run(cmd + [pdf, prefix], check=True)
    elif shutil.which("mutool"):
        rng = f"{first or 1}-{last}" if last else (f"{first}-N" if first else "1-N")
        subprocess.run(["mutool", "draw", "-r", str(dpi), "-o", prefix + "-%d.png", pdf, rng], check=True)
    else:
        return []
    return sorted(glob.glob(prefix + "-*.png"))


def montage(images, out, cols=3, width=480):
    try:
        from PIL import Image
    except ImportError:
        return None
    thumbs = []
    for p in images:
        im = Image.open(p).convert("RGB")
        im.thumbnail((width, width * 2))
        thumbs.append(im)
    if not thumbs:
        return None
    w = max(t.width for t in thumbs)
    h = max(t.height for t in thumbs)
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (w + 10) + 10, rows * (h + 10) + 10), "white")
    for i, t in enumerate(thumbs):
        sheet.paste(t, (10 + (i % cols) * (w + 10), 10 + (i // cols) * (h + 10)))
    sheet.save(out)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--outdir", help="default: ./render-<name>/ next to the current directory")
    ap.add_argument("--dpi", type=int, default=80)
    ap.add_argument("--pages", help="e.g. 1-3 or 2 (page images only)")
    ap.add_argument("--montage", action="store_true", help="also write one contact sheet (needs Pillow)")
    a = ap.parse_args(argv)
    src = os.path.abspath(a.file)
    if not os.path.isfile(src):
        die(f"not a file: {src}")
    outdir = os.path.abspath(a.outdir or f"render-{Path(src).stem}")
    os.makedirs(outdir, exist_ok=True)
    pdf = src if src.lower().endswith(".pdf") else to_pdf(src, outdir)
    print(f"pdf: {pdf}")
    first = last = None
    if a.pages:
        s, _, e = a.pages.partition("-")
        first, last = int(s), int(e or s)
    imgs = rasterize(pdf, outdir, a.dpi, first, last)
    if not imgs:
        print("no page images: install Poppler (pdftoppm) or MuPDF (mutool) to rasterize the PDF; "
              "the PDF above can still be opened and checked by hand.")
    for p in imgs:
        print(f"page: {p}")
    if a.montage and imgs:
        m = montage(imgs, os.path.join(outdir, Path(src).stem + "-montage.png"))
        print(f"montage: {m}" if m else "montage skipped: Pillow not installed")


if __name__ == "__main__":
    main()
