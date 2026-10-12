#!/usr/bin/env python3
"""Unpack and repack .docx/.xlsx/.pptx for direct XML editing (standard library only).

  ooxml_pack.py unpack FILE DIR [--force]
  ooxml_pack.py pack   DIR OUT [--original FILE]

unpack refuses path traversal, absolute paths and symlink entries (Office files from other
people are untrusted). pack writes [Content_Types].xml first, deflates every part, and refuses
to build a package when any .xml/.rels part is not well-formed. With --original, parts keep
the original file's order.
"""
import argparse
import os
import sys
import zipfile
from xml.etree import ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import PackageError, die, open_package, safe_extract  # noqa: E402


def cmd_unpack(a):
    z = open_package(a.file)
    dest = safe_extract(z, a.dir, force=a.force)
    print(f"unpacked {len(z.namelist())} parts to {dest}")


def collect(root):
    out = []
    for r, _, fs in os.walk(root):
        for f in fs:
            full = os.path.join(r, f)
            out.append(os.path.relpath(full, root).replace(os.sep, "/"))
    return out


def cmd_pack(a):
    root = os.path.abspath(a.dir)
    if not os.path.isdir(root):
        die(f"not a directory: {root}")
    parts = collect(root)
    if "[Content_Types].xml" not in parts:
        die("[Content_Types].xml missing: not an unpacked Office package")
    bad = []
    for p in parts:
        if p.endswith((".xml", ".rels")):
            try:
                ET.parse(os.path.join(root, p))
            except ET.ParseError as e:
                bad.append(f"{p}: {e}")
        if os.path.islink(os.path.join(root, p)):
            bad.append(f"{p}: symlink")
    if bad:
        die("refusing to pack:\n  " + "\n  ".join(bad))
    order = ["[Content_Types].xml", "_rels/.rels"]
    if a.original:
        try:
            orig = [n for n in open_package(a.original).namelist() if not n.endswith("/")]
        except PackageError as e:
            die(str(e))
        order = [n for n in orig if n in parts]
        if order[:1] != ["[Content_Types].xml"]:
            order = ["[Content_Types].xml"] + [n for n in order if n != "[Content_Types].xml"]
    ordered = [p for p in order if p in parts] + sorted(p for p in parts if p not in order)
    out = os.path.abspath(a.out)
    if os.path.exists(out) and not a.force:
        die(f"{out} exists (use --force to overwrite)")
    tmp = out + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for p in ordered:
            z.write(os.path.join(root, p), p)
    os.replace(tmp, out)
    print(f"packed {len(ordered)} parts into {out}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    u = sub.add_parser("unpack")
    u.add_argument("file")
    u.add_argument("dir")
    u.add_argument("--force", action="store_true")
    u.set_defaults(fn=cmd_unpack)
    p = sub.add_parser("pack")
    p.add_argument("dir")
    p.add_argument("out")
    p.add_argument("--original")
    p.add_argument("--force", action="store_true", help="overwrite OUT")
    p.set_defaults(fn=cmd_pack)
    a = ap.parse_args(argv)
    try:
        a.fn(a)
    except PackageError as e:
        die(str(e))


if __name__ == "__main__":
    main()
