#!/usr/bin/env python3
"""Render a .pptx to one PNG per slide (and optionally a labelled contact sheet).

Pipeline: LibreOffice headless converts the deck to PDF (using a throw-away
user profile, so it works while LibreOffice is open), then the PDF is
rasterised with ``pdftoppm`` (poppler) or, when that is missing, PyMuPDF.

Usage:
    render.py IN.pptx -o OUTDIR [--dpi 110] [--grid] [--cols 4] [--timeout 180]

Outputs in OUTDIR: ``slide-01.png`` ... and, with --grid, ``grid.png`` (a
thumbnail sheet with the slide number under every thumbnail).

Exit status: 0 ok, 1 error (conversion failed, timeout, bad input),
2 a required tool is missing (the message names what to install).

Testing hooks: PPTX_DECK_NO_SOFFICE=1 and PPTX_DECK_NO_RASTER=1 make the tool
behave as if LibreOffice / every rasteriser were not installed.
"""

from __future__ import annotations

import argparse
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import List, Optional

EXIT_OK, EXIT_ERROR, EXIT_MISSING = 0, 1, 2

SOFFICE_CANDIDATES = [
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
    "/opt/homebrew/bin/soffice",
    "/usr/local/bin/soffice",
    "/usr/bin/soffice",
    "/usr/bin/libreoffice",
    "/snap/bin/libreoffice",
    "C:\\Program Files\\LibreOffice\\program\\soffice.exe",
]

INSTALL_SOFFICE = "LibreOffice (soffice) was not found. Install it with: brew install --cask libreoffice"
INSTALL_RASTER = (
    "No PDF rasteriser was found (pdftoppm or PyMuPDF). Install one with: brew install poppler   "
    "(or: pip3 install pymupdf)"
)


def check_pptx(path: Path) -> Optional[str]:
    """Return an error message when *path* is not a .pptx package, else None."""
    try:
        with zipfile.ZipFile(path) as z:
            names = set(z.namelist())
    except (zipfile.BadZipFile, OSError):
        return "%s is not a valid .pptx file (not a zip archive)" % path
    for need in ("[Content_Types].xml", "ppt/presentation.xml"):
        if need not in names:
            return "%s is not a valid .pptx file (missing %s)" % (path, need)
    return None


def find_soffice() -> Optional[str]:
    """Locate LibreOffice. PPTX_DECK_NO_SOFFICE=1 simulates a missing install (used by tests)."""
    if os.environ.get("PPTX_DECK_NO_SOFFICE"):
        return None
    for name in ("soffice", "libreoffice"):
        found = shutil.which(name)
        if found:
            return found
    for cand in SOFFICE_CANDIDATES:
        if os.path.isfile(cand) and os.access(cand, os.X_OK):
            return cand
    return None


def find_rasteriser() -> Optional[str]:
    """Return "pdftoppm", "fitz" or None."""
    if os.environ.get("PPTX_DECK_NO_RASTER"):
        return None
    if shutil.which("pdftoppm"):
        return "pdftoppm"
    try:
        import fitz  # noqa: F401

        return "fitz"
    except ImportError:
        return None


def to_pdf(soffice: str, src: Path, workdir: Path, timeout: int) -> Path:
    """Convert *src* to PDF inside *workdir*; return the PDF path. Raises RuntimeError."""
    profile = workdir / "lo-profile"
    outdir = workdir / "pdf"
    outdir.mkdir(parents=True, exist_ok=True)
    # work on a copy with a plain name so odd characters in the file name cannot upset soffice
    local = workdir / "deck.pptx"
    shutil.copyfile(src, local)
    cmd = [
        soffice,
        "-env:UserInstallation=file://" + str(profile),
        "--headless",
        "--norestore",
        "--nolockcheck",
        "--convert-to",
        "pdf",
        "--outdir",
        str(outdir),
        str(local),
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        raise RuntimeError(
            "LibreOffice did not finish within %d s (try a larger --timeout, or close stuck soffice processes)" % timeout
        )
    pdf = outdir / "deck.pdf"
    if proc.returncode != 0 or not pdf.is_file():
        detail = (proc.stderr or proc.stdout or "").strip().splitlines()
        raise RuntimeError("LibreOffice conversion failed (exit %d)%s" % (proc.returncode, ": " + detail[-1] if detail else ""))
    return pdf


def rasterise(method: str, pdf: Path, outdir: Path, dpi: int, timeout: int) -> List[Path]:
    """Write slide-NN.png files for every page of *pdf*; return them in order."""
    tmp = outdir / ".raster-tmp"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    pages: List[Path] = []
    try:
        if method == "pdftoppm":
            try:
                proc = subprocess.run(
                    ["pdftoppm", "-png", "-r", str(dpi), str(pdf), str(tmp / "p")],
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                )
            except subprocess.TimeoutExpired:
                raise RuntimeError("pdftoppm did not finish within %d s" % timeout)
            if proc.returncode != 0:
                raise RuntimeError("pdftoppm failed: " + (proc.stderr or "").strip()[:200])
            pages = sorted(
                (Path(p) for p in glob.glob(str(tmp / "p-*.png"))),
                key=lambda p: int(re.search(r"-(\d+)\.png$", p.name).group(1)),
            )
        else:
            import fitz

            doc = fitz.open(str(pdf))
            zoom = dpi / 72.0
            for i, page in enumerate(doc, start=1):
                pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
                target = tmp / ("p-%d.png" % i)
                pix.save(str(target))
                pages.append(target)
            doc.close()
        width = max(2, len(str(len(pages))))
        out: List[Path] = []
        for i, p in enumerate(pages, start=1):
            dest = outdir / ("slide-%0*d.png" % (width, i))
            if dest.exists():
                dest.unlink()
            shutil.move(str(p), str(dest))
            out.append(dest)
        return out
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def make_grid(images: List[Path], dest: Path, cols: int, thumb_w: int = 480) -> None:
    """Contact sheet: thumbnails on a light grey background, slide number under each."""
    from PIL import Image, ImageDraw, ImageFont

    thumbs = []
    for p in images:
        with Image.open(p) as im:
            im = im.convert("RGB")
            h = max(1, round(im.height * thumb_w / im.width))
            thumbs.append(im.resize((thumb_w, h), Image.LANCZOS))
    th = max(t.height for t in thumbs)
    pad, label_h = 16, 28
    cols = max(1, min(cols, len(thumbs)))
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (thumb_w + pad) + pad, rows * (th + label_h + pad) + pad), (236, 236, 236))
    draw = ImageDraw.Draw(sheet)
    font = None
    for cand in ("/System/Library/Fonts/Helvetica.ttc", "/System/Library/Fonts/Supplemental/Arial.ttf", "DejaVuSans.ttf"):
        try:
            font = ImageFont.truetype(cand, 18)
            break
        except OSError:
            continue
    if font is None:
        font = ImageFont.load_default()
    for i, t in enumerate(thumbs):
        r, c = divmod(i, cols)
        x = pad + c * (thumb_w + pad)
        y = pad + r * (th + label_h + pad)
        draw.rectangle([x - 1, y - 1, x + t.width, y + t.height], outline=(190, 190, 190))
        sheet.paste(t, (x, y))
        draw.text((x, y + t.height + 4), "Slide %d" % (i + 1), fill=(60, 60, 60), font=font)
    sheet.save(dest)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="Render a .pptx to slide-01.png ... with LibreOffice (headless) and pdftoppm or PyMuPDF. "
        "Exit 2 when a required tool is missing.",
    )
    ap.add_argument("input", help="input .pptx")
    ap.add_argument("-o", "--output", required=True, help="output directory for the PNG files")
    ap.add_argument("--dpi", type=int, default=110, help="raster resolution (default 110)")
    ap.add_argument("--grid", action="store_true", help="also write grid.png, a labelled thumbnail contact sheet")
    ap.add_argument("--cols", type=int, default=4, help="columns in grid.png (default 4)")
    ap.add_argument("--timeout", type=int, default=180, help="seconds allowed for each external tool (default 180)")
    args = ap.parse_args(argv)

    src = Path(args.input)
    if not src.is_file():
        print("error: input not found: %s" % src, file=sys.stderr)
        return EXIT_ERROR
    bad = check_pptx(src)
    if bad:
        print("error: " + bad, file=sys.stderr)
        return EXIT_ERROR
    if args.dpi < 10 or args.dpi > 600:
        print("error: --dpi must be between 10 and 600", file=sys.stderr)
        return EXIT_ERROR

    soffice = find_soffice()
    if not soffice:
        print(INSTALL_SOFFICE, file=sys.stderr)
        return EXIT_MISSING
    method = find_rasteriser()
    if not method:
        print(INSTALL_RASTER, file=sys.stderr)
        return EXIT_MISSING

    outdir = Path(args.output)
    outdir.mkdir(parents=True, exist_ok=True)
    for old in list(outdir.glob("slide-*.png")) + [outdir / "grid.png"]:
        if old.exists():
            old.unlink()

    with tempfile.TemporaryDirectory(prefix="pptx-render-") as td:
        work = Path(td)
        try:
            pdf = to_pdf(soffice, src, work, args.timeout)
            images = rasterise(method, pdf, outdir, args.dpi, args.timeout)
        except RuntimeError as exc:
            print("error: %s" % exc, file=sys.stderr)
            return EXIT_ERROR
    if not images:
        print("error: the PDF has no pages", file=sys.stderr)
        return EXIT_ERROR
    print("rendered %d slide(s) to %s (%s, %d dpi)" % (len(images), outdir, method, args.dpi))
    for p in images:
        print("  " + str(p))
    if args.grid:
        try:
            grid = outdir / "grid.png"
            make_grid(images, grid, args.cols)
            print("  " + str(grid))
        except Exception as exc:  # Pillow missing or image problem
            print("error: could not build grid.png: %s" % exc, file=sys.stderr)
            return EXIT_ERROR
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
