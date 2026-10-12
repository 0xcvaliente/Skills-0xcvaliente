#!/usr/bin/env python3
"""Read-only structural PDF checks. Does not certify visual or press quality."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit


MM_PER_POINT = 25.4 / 72.0
DRAFT_RE = re.compile(
    r"\b(?:TODO|TBD|FIXME|lorem\s+ipsum)\b"
    r"|\[(?:insert\b|placeholder\b|to\s+be\s+(?:confirmed|provided)\b)[^\]]*\]"
    r"|\{\{[^{}]+\}\}",
    re.IGNORECASE,
)
LIMITS = [
    "No visual, claim, full accessibility, font, image-resolution, or color-standard verification.",
    "URI destinations are listed but not visited or verified.",
    "Bleed checks concern page boxes, not whether artwork extends to bleed.",
]


def normalized(text):
    return re.sub(r"\s+", " ", text).strip().casefold()


def rectangle(box):
    result = tuple(float(value) for value in box)
    if len(result) != 4 or not all(math.isfinite(value) for value in result):
        raise ValueError("Nonfinite or malformed page rectangle")
    if result[2] <= result[0] or result[3] <= result[1]:
        raise ValueError("Page rectangle has no positive area")
    return result


def contains(outer, inner, tolerance):
    return (
        inner[0] >= outer[0] - tolerance
        and inner[1] >= outer[1] - tolerance
        and inner[2] <= outer[2] + tolerance
        and inner[3] <= outer[3] + tolerance
    )


def dimensions(box, unit, rotation):
    width = (box[2] - box[0]) * unit * MM_PER_POINT
    height = (box[3] - box[1]) * unit * MM_PER_POINT
    return (height, width) if rotation in (90, 270) else (width, height)


def audit_pdf(path, *, pages=None, size_mm=None, trim_mm=None, bleed_mm=None,
              tolerance_mm=0.6, text_policy="warn", required_text=(),
              forbid_text=(), allow_draft=False, max_mb=None):
    from pypdf import PdfReader

    path = Path(path)
    result = {
        "file": str(path.resolve()), "status": "fail", "page_count": 0,
        "errors": [], "warnings": [], "pages": [], "uris": [], "limits": LIMITS,
    }
    errors, warnings = result["errors"], result["warnings"]
    try:
        size_bytes = path.stat().st_size
        result["size_bytes"] = size_bytes
        if max_mb is not None and size_bytes > max_mb * 1024 * 1024:
            warnings.append(f"File exceeds the requested {max_mb:g} MiB budget")
        reader = PdfReader(path)
        if reader.is_encrypted:
            errors.append("Encrypted PDF: audit an authorized unencrypted working copy")
            return result
        result["page_count"] = count = len(reader.pages)
        if count == 0:
            errors.append("PDF has no pages")
        if pages is not None and count != pages:
            errors.append(f"Expected {pages} pages; found {count}")
        all_text = []
        for number, page in enumerate(reader.pages, 1):
            info = {"number": number}
            result["pages"].append(info)
            try:
                unit = float(page.get("/UserUnit", 1))
                if not math.isfinite(unit) or unit <= 0:
                    raise ValueError("Invalid UserUnit")
                raw_rotation = float(page.get("/Rotate", 0))
                if not math.isfinite(raw_rotation) or raw_rotation % 90 != 0:
                    raise ValueError("Rotation must be a multiple of 90 degrees")
                rotation = int(raw_rotation) % 360
                boxes = {
                    "media": rectangle(page.mediabox),
                    "crop": rectangle(page.cropbox),
                    "trim": rectangle(page.trimbox),
                    "bleed": rectangle(page.bleedbox),
                }
                point_tolerance = tolerance_mm / (unit * MM_PER_POINT)
                info.update({"rotation": rotation, "user_unit": unit})
                for kind, box in boxes.items():
                    width, height = dimensions(box, unit, rotation)
                    info[kind + "_mm"] = [round(width, 3), round(height, 3)]
                    if kind != "media" and not contains(boxes["media"], box, point_tolerance):
                        errors.append(f"Page {number}: {kind} box extends outside media box")
                for kind, expected in (("crop", size_mm), ("trim", trim_mm)):
                    if expected is None:
                        continue
                    actual = dimensions(boxes[kind], unit, rotation)
                    if any(abs(actual[i] - expected[i]) > tolerance_mm for i in (0, 1)):
                        errors.append(
                            f"Page {number}: {kind} size {actual[0]:.2f} x {actual[1]:.2f} mm; "
                            f"expected {expected[0]:g} x {expected[1]:g} mm"
                        )
                if bleed_mm is not None:
                    if "/TrimBox" not in page or "/BleedBox" not in page:
                        errors.append(f"Page {number}: bleed check needs explicit TrimBox and BleedBox")
                    trim, bleed = boxes["trim"], boxes["bleed"]
                    margins = [
                        trim[0] - bleed[0], trim[1] - bleed[1],
                        bleed[2] - trim[2], bleed[3] - trim[3],
                    ]
                    margins = [value * unit * MM_PER_POINT for value in margins]
                    info["bleed_margins_mm"] = [round(value, 3) for value in margins]
                    if any(value < bleed_mm - tolerance_mm for value in margins):
                        errors.append(f"Page {number}: bleed margin is below {bleed_mm:g} mm on one or more sides")
                    if not contains(bleed, trim, point_tolerance):
                        errors.append(f"Page {number}: trim box extends outside bleed box")
            except (ValueError, TypeError, KeyError, OverflowError) as exc:
                errors.append(f"Page {number}: invalid geometry ({exc})")

            try:
                text = page.extract_text() or ""
            except Exception as exc:
                text = ""
                warnings.append(f"Page {number}: text extraction failed ({type(exc).__name__})")
            info["text_characters"] = len(text.strip())
            all_text.append(text)
            if not text.strip() and text_policy != "ignore":
                target = errors if text_policy == "required" else warnings
                target.append(f"Page {number}: no nonblank extractable text")
            matches = sorted(set(DRAFT_RE.findall(text)))
            if matches:
                target = warnings if allow_draft else errors
                target.append(f"Page {number}: draft tokens {matches}")

            try:
                annotations = page.get("/Annots", []) or []
                if hasattr(annotations, "get_object"):
                    annotations = annotations.get_object()
                for annotation in annotations:
                    annotation = annotation.get_object()
                    action = annotation.get("/A")
                    if not action:
                        continue
                    action = action.get_object()
                    if "/URI" not in action:
                        continue
                    uri = str(action["/URI"]).strip()
                    result["uris"].append({"page": number, "uri": uri})
                    try:
                        scheme = urlsplit(uri).scheme.lower()
                    except ValueError:
                        scheme = ""
                    if scheme not in ("http", "https", "mailto", "tel"):
                        warnings.append(f"Page {number}: inspect URI with unusual or missing scheme")
            except Exception as exc:
                warnings.append(f"Page {number}: annotation inspection failed ({type(exc).__name__})")

        document_text = normalized("\n".join(all_text))
        for phrase in required_text:
            if normalized(phrase) not in document_text:
                errors.append(f"Required text not found: {phrase}")
        for phrase in forbid_text:
            if normalized(phrase) in document_text:
                errors.append(f"Forbidden text found: {phrase}")
        result["status"] = "fail" if errors else ("pass_with_warnings" if warnings else "pass")
    except Exception as exc:
        errors.append(f"Cannot audit PDF ({type(exc).__name__}: {exc})")
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--pages", type=int)
    parser.add_argument("--size-mm", type=float, nargs=2, metavar=("WIDTH", "HEIGHT"))
    parser.add_argument("--trim-mm", type=float, nargs=2, metavar=("WIDTH", "HEIGHT"))
    parser.add_argument("--bleed-mm", type=float)
    parser.add_argument("--tolerance-mm", type=float, default=0.6)
    parser.add_argument("--text-policy", choices=("required", "warn", "ignore"), default="warn")
    parser.add_argument("--required-text", action="append", default=[])
    parser.add_argument("--forbid-text", action="append", default=[])
    parser.add_argument("--allow-draft", action="store_true")
    parser.add_argument("--max-mb", type=float)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    if args.pages is not None and args.pages < 1:
        parser.error("--pages must be positive")
    for label, values in (("--size-mm", args.size_mm), ("--trim-mm", args.trim_mm)):
        if values and any(not math.isfinite(v) or v <= 0 for v in values):
            parser.error(label + " dimensions must be finite and positive")
    for label, value in (("--bleed-mm", args.bleed_mm), ("--tolerance-mm", args.tolerance_mm)):
        if value is not None and (not math.isfinite(value) or value < 0):
            parser.error(label + " must be finite and nonnegative")
    if args.max_mb is not None and (not math.isfinite(args.max_mb) or args.max_mb <= 0):
        parser.error("--max-mb must be finite and positive")
    if any(not normalized(v) for v in args.required_text + args.forbid_text):
        parser.error("Text checks must not be empty")
    if args.out and args.out.resolve() == args.pdf.resolve():
        parser.error("--out must not overwrite the input PDF")
    try:
        report = audit_pdf(
            args.pdf, pages=args.pages, size_mm=args.size_mm, trim_mm=args.trim_mm,
            bleed_mm=args.bleed_mm, tolerance_mm=args.tolerance_mm,
            text_policy=args.text_policy, required_text=args.required_text,
            forbid_text=args.forbid_text, allow_draft=args.allow_draft, max_mb=args.max_mb,
        )
    except ModuleNotFoundError as exc:
        print(json.dumps({"status": "error", "errors": [f"Missing dependency: {exc.name}; use a Python with pypdf installed"]}))
        return 2
    output = json.dumps(report, indent=2, ensure_ascii=False)
    if args.out:
        try:
            args.out.write_text(output + "\n", encoding="utf-8")
        except OSError as exc:
            report["status"] = "fail"
            report["errors"].append(f"Cannot write report ({type(exc).__name__}: {exc})")
            output = json.dumps(report, indent=2, ensure_ascii=False)
    print(output)
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
