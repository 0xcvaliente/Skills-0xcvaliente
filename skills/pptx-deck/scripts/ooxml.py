#!/usr/bin/env python3
"""Low-level OOXML package tools for .pptx files: unpack, pack and validate.

Sub-commands
------------
unpack IN.pptx DIR [--pretty]
    Extract every part of the package into DIR (parts keep their package paths).
    With --pretty, XML parts are re-indented so they are easy to read and edit.
    Whitespace inside text nodes is never altered.

pack DIR OUT.pptx
    Zip DIR back into a .pptx. The order is deterministic: [Content_Types].xml
    first, then _rels/.rels, then all other parts sorted by path. Timestamps are
    fixed, so packing the same tree twice gives byte-identical files.

validate IN.pptx|DIR [--json]
    Structural checks that catch the usual causes of PowerPoint's "repair" prompt:
      * every XML part is well formed;
      * every part has a content type (Default by extension or Override) and every
        Override points at an existing part;
      * every internal relationship target exists, relationship ids are unique;
      * orphan parts (not reachable from _rels/.rels through relationships);
      * duplicate slide / master ids and slide relationship ids in presentation.xml;
      * notes slides and slides point at each other consistently.
    Exit status 0 when clean, 1 when problems were found, 2 when the input is unreadable.

The validation functions are importable (``validate_parts``, ``load_parts``) and
are used by rearrange.py to check its own output.
"""

from __future__ import annotations

import argparse
import json
import os
import posixpath
import sys
import zipfile
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import unquote

from lxml import etree

NS_CT = "http://schemas.openxmlformats.org/package/2006/content-types"
NS_REL = "http://schemas.openxmlformats.org/package/2006/relationships"
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_P = "http://schemas.openxmlformats.org/presentationml/2006/main"
RT_BASE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/"
CT_PART = "[Content_Types].xml"
FIXED_DATE = (1980, 1, 1, 0, 0, 0)

XML_EXTENSIONS = (".xml", ".rels", ".vml")


# --------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------


def load_parts(source: str | os.PathLike) -> Tuple[Dict[str, bytes], List[str]]:
    """Read a .pptx file or an unpacked directory into ``{part name: bytes}``.

    Part names have no leading slash (``ppt/slides/slide1.xml``). The second
    return value lists package-level problems found while reading (duplicate zip
    entries).
    """
    src = Path(source)
    parts: Dict[str, bytes] = {}
    problems: List[str] = []
    if src.is_dir():
        for root, _dirs, files in os.walk(src):
            for f in files:
                full = Path(root) / f
                name = full.relative_to(src).as_posix()
                parts[name] = full.read_bytes()
    else:
        with zipfile.ZipFile(src) as zf:
            for info in zf.infolist():
                if info.is_dir():
                    continue
                if info.filename in parts:
                    problems.append("duplicate zip entry: %s" % info.filename)
                parts[info.filename] = zf.read(info)
    return parts, problems


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------


def _rels_source(rels_name: str) -> Optional[str]:
    """Part name that owns a .rels part ("" for the package root), None if the name is odd."""
    if rels_name == "_rels/.rels":
        return ""
    d, f = posixpath.split(rels_name)
    if posixpath.basename(d) != "_rels" or not f.endswith(".rels"):
        return None
    return posixpath.join(posixpath.dirname(d), f[: -len(".rels")])


def _rels_name_for(part: str) -> str:
    d, f = posixpath.split(part)
    return posixpath.join(d, "_rels", f + ".rels")


def _resolve(source: str, target: str) -> str:
    """Resolve an internal relationship target against its source part name."""
    target = target.split("#")[0]
    if target.startswith("/"):
        return posixpath.normpath(target.lstrip("/"))
    base = posixpath.dirname(source)
    return posixpath.normpath(posixpath.join(base, target))


def _parse(blob: bytes):
    return etree.fromstring(blob, etree.XMLParser(resolve_entities=False, no_network=True))


class Report:
    def __init__(self) -> None:
        self.problems: List[Dict[str, str]] = []

    def add(self, code: str, part: str, message: str) -> None:
        self.problems.append({"code": code, "part": part, "message": message})


def validate_parts(parts: Dict[str, bytes], pre_problems: Optional[List[str]] = None) -> Report:
    """Run all structural checks on ``{part name: bytes}``; return a :class:`Report`."""
    rep = Report()
    for msg in pre_problems or []:
        rep.add("zip", "", msg)

    # ---- well-formedness ------------------------------------------------
    trees: Dict[str, etree._Element] = {}
    for name, blob in sorted(parts.items()):
        if name.lower().endswith(XML_EXTENSIONS):
            try:
                trees[name] = _parse(blob)
            except etree.XMLSyntaxError as exc:
                rep.add("xml-malformed", name, "not well-formed XML: %s" % exc)

    # ---- content types --------------------------------------------------
    defaults: Dict[str, str] = {}
    overrides: Dict[str, str] = {}
    if CT_PART not in parts:
        rep.add("content-types-missing", CT_PART, "[Content_Types].xml is missing")
    elif CT_PART in trees:
        for el in trees[CT_PART]:
            tag = etree.QName(el).localname if isinstance(el.tag, str) else ""
            if tag == "Default":
                defaults[el.get("Extension", "").lower()] = el.get("ContentType", "")
            elif tag == "Override":
                overrides[(el.get("PartName") or "").lstrip("/")] = el.get("ContentType", "")
        for name in sorted(parts):
            if name == CT_PART:
                continue
            base = posixpath.basename(name)
            ext = base.rpartition(".")[2].lower() if "." in base else ""
            if name not in overrides and ext not in defaults:
                rep.add("content-type-missing", name, "no Default (by extension) or Override content type")
        for pn in sorted(overrides):
            if pn not in parts:
                rep.add("override-dangling", pn, "Override in [Content_Types].xml points at a part that does not exist")

    # ---- relationships --------------------------------------------------
    graph: Dict[str, List[str]] = defaultdict(list)  # source part -> internal target parts
    rel_info: Dict[str, List[Tuple[str, str, str]]] = {}  # source -> [(rId, type, target part)]
    for name in sorted(parts):
        if not name.endswith(".rels"):
            continue
        src = _rels_source(name)
        if src is None:
            rep.add("rels-name", name, "unexpected relationships part name")
            continue
        if src != "" and src not in parts:
            rep.add("rels-orphan", name, "relationships part belongs to missing part %s" % src)
            continue
        tree = trees.get(name)
        if tree is None:
            continue
        seen_ids = set()
        items = []
        for rel in tree:
            if not isinstance(rel.tag, str) or etree.QName(rel).localname != "Relationship":
                continue
            rid = rel.get("Id", "")
            if rid in seen_ids:
                rep.add("rel-id-dup", name, "duplicate relationship id %s" % rid)
            seen_ids.add(rid)
            if rel.get("TargetMode") == "External":
                continue
            target = rel.get("Target", "")
            resolved = _resolve(src, target)
            if resolved not in parts and unquote(resolved) in parts:
                resolved = unquote(resolved)
            if resolved not in parts:
                rep.add("rel-dangling", name, "%s (%s) targets missing part %s" % (rid, (rel.get("Type") or "").rsplit("/", 1)[-1], resolved))
                continue
            graph[src].append(resolved)
            items.append((rid, rel.get("Type", ""), resolved))
        rel_info[src] = items

    # ---- orphan parts ---------------------------------------------------
    reachable = set()
    stack = [""]
    while stack:
        cur = stack.pop()
        for tgt in graph.get(cur, []):
            if tgt not in reachable:
                reachable.add(tgt)
                stack.append(tgt)
    for name in sorted(parts):
        if name == CT_PART or name.endswith(".rels"):
            continue
        if name not in reachable:
            rep.add("orphan-part", name, "part is not reachable from _rels/.rels")

    # ---- presentation.xml ids ------------------------------------------
    pres_name = None
    for _rid, rtype, tgt in rel_info.get("", []):
        if rtype.endswith("/officeDocument"):
            pres_name = tgt
    if pres_name and pres_name in trees:
        _check_presentation(rep, pres_name, trees[pres_name], rel_info.get(pres_name, []))

    # master and layout ids share one number space
    ids: Dict[str, str] = {}
    for name in sorted(trees):
        root = trees[name]
        if not (name.startswith("ppt/slideMasters/") and name.endswith(".xml")):
            continue
        for el in root.xpath("//p:sldLayoutId", namespaces={"p": NS_P}):
            num = el.get("id", "")
            if num in ids:
                rep.add("layout-id-dup", name, "slide layout id %s also used in %s" % (num, ids[num]))
            ids[num] = name
    if pres_name and pres_name in trees:
        for el in trees[pres_name].xpath("p:sldMasterIdLst/p:sldMasterId", namespaces={"p": NS_P}):
            num = el.get("id", "")
            if num in ids:
                rep.add("master-id-dup", pres_name, "slide master id %s also used by a layout in %s" % (num, ids[num]))

    # ---- notes <-> slide back-references -------------------------------
    _check_notes(rep, parts, rel_info)
    return rep


def _check_presentation(rep: Report, pres_name: str, root, rels: List[Tuple[str, str, str]]) -> None:
    by_id = {rid: (rtype, tgt) for rid, rtype, tgt in rels}
    ns = {"p": NS_P, "r": NS_R}
    sld_ids = root.xpath("p:sldIdLst/p:sldId", namespaces=ns)
    seen_num: Dict[str, int] = {}
    seen_rid: Dict[str, int] = {}
    for i, el in enumerate(sld_ids, start=1):
        num = el.get("id", "")
        rid = el.get("{%s}id" % NS_R, "")
        if num in seen_num:
            rep.add("slide-id-dup", pres_name, "slide id %s is used by slides %d and %d" % (num, seen_num[num], i))
        seen_num.setdefault(num, i)
        if rid in seen_rid:
            rep.add("slide-rid-dup", pres_name, "relationship %s is listed by slides %d and %d" % (rid, seen_rid[rid], i))
        seen_rid.setdefault(rid, i)
        if rid not in by_id:
            rep.add("slide-rel-missing", pres_name, "slide %d references unknown relationship %s" % (i, rid))
        elif not by_id[rid][0].endswith("/slide"):
            rep.add("slide-rel-type", pres_name, "slide %d relationship %s is not a slide relationship" % (i, rid))
        try:
            if not (256 <= int(num) < 2147483648):
                rep.add("slide-id-range", pres_name, "slide id %s is outside 256..2147483647" % num)
        except ValueError:
            rep.add("slide-id-range", pres_name, "slide id %r is not an integer" % num)
    listed = {by_id[r][1] for r in seen_rid if r in by_id}
    for rid, rtype, tgt in rels:
        if rtype.endswith("/slide") and tgt not in listed:
            rep.add("slide-unlisted", pres_name, "slide part %s (%s) is related but not in sldIdLst" % (tgt, rid))
    master_ids = root.xpath("p:sldMasterIdLst/p:sldMasterId", namespaces=ns)
    seen_m: Dict[str, int] = {}
    for el in master_ids:
        num = el.get("id", "")
        if num in seen_m:
            rep.add("master-id-dup", pres_name, "slide master id %s is duplicated" % num)
        seen_m[num] = 1
        rid = el.get("{%s}id" % NS_R, "")
        if rid not in by_id:
            rep.add("master-rel-missing", pres_name, "slide master references unknown relationship %s" % rid)


def _check_notes(rep: Report, parts: Dict[str, bytes], rel_info: Dict[str, List[Tuple[str, str, str]]]) -> None:
    notes_parts = {n for n in parts if n.startswith("ppt/notesSlides/") and n.endswith(".xml")}
    slide_to_notes: Dict[str, List[str]] = {}
    for src, items in rel_info.items():
        if not (src.startswith("ppt/slides/") and src.endswith(".xml")):
            continue
        for rid, rtype, tgt in items:
            if rtype.endswith("/notesSlide"):
                slide_to_notes.setdefault(src, []).append(tgt)
    notes_users: Dict[str, List[str]] = defaultdict(list)
    for slide, notes in slide_to_notes.items():
        if len(notes) > 1:
            rep.add("notes-multiple", slide, "slide has %d notesSlide relationships" % len(notes))
        for n in notes:
            notes_users[n].append(slide)
            back = [t for _r, ty, t in rel_info.get(n, []) if ty.endswith("/slide")]
            if back != [slide]:
                rep.add(
                    "notes-backref",
                    n,
                    "notes slide used by %s points back to %s" % (slide, ", ".join(back) if back else "no slide"),
                )
    for n in sorted(notes_parts):
        users = notes_users.get(n, [])
        if len(users) > 1:
            rep.add("notes-shared", n, "notes slide is shared by slides %s" % ", ".join(sorted(users)))
        back = [t for _r, ty, t in rel_info.get(n, []) if ty.endswith("/slide")]
        for b in back:
            if n not in slide_to_notes.get(b, []):
                rep.add("notes-forward", n, "points at %s, which does not reference it back" % b)


def validate(source: str | os.PathLike) -> Report:
    parts, pre = load_parts(source)
    return validate_parts(parts, pre)


# --------------------------------------------------------------------------
# Unpack / pack
# --------------------------------------------------------------------------


def _pretty(blob: bytes) -> bytes:
    """Re-indent an XML document without touching text content.

    lxml only indents where an element has no text or tail, so ``<a:t> </a:t>``
    and mixed content are left alone.
    """
    try:
        root = etree.fromstring(blob, etree.XMLParser(resolve_entities=False, no_network=True))
    except etree.XMLSyntaxError:
        return blob
    return etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8", standalone=True)


def unpack(src: str, dest: str, pretty: bool = False) -> int:
    with zipfile.ZipFile(src) as zf:
        names = [i.filename for i in zf.infolist() if not i.is_dir()]
        out = Path(dest)
        out.mkdir(parents=True, exist_ok=True)
        for name in names:
            target = (out / name).resolve()
            if out.resolve() not in target.parents:
                raise SystemExit("refusing to write outside the target directory: %s" % name)
            target.parent.mkdir(parents=True, exist_ok=True)
            data = zf.read(name)
            if pretty and name.lower().endswith(XML_EXTENSIONS):
                data = _pretty(data)
            target.write_bytes(data)
    return len(names)


def pack(src: str, dest: str) -> int:
    parts, _ = load_parts(src)
    if CT_PART not in parts:
        raise SystemExit("%s/[Content_Types].xml not found; is this an unpacked .pptx?" % src)
    names = [n for n in parts if n not in (CT_PART, "_rels/.rels")]
    names.sort()
    ordered = [CT_PART] + (["_rels/.rels"] if "_rels/.rels" in parts else []) + names
    Path(dest).parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in ordered:
            info = zipfile.ZipInfo(name, FIXED_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, parts[name])
    return len(ordered)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="Unpack, pack and structurally validate .pptx packages (see module docstring).",
    )
    sub = ap.add_subparsers(dest="cmd", required=True)
    up = sub.add_parser("unpack", help="extract a .pptx into a directory")
    up.add_argument("input", help="input .pptx")
    up.add_argument("dir", help="output directory (created if needed)")
    up.add_argument("--pretty", action="store_true", help="re-indent XML parts")
    pk = sub.add_parser("pack", help="zip a directory into a .pptx (deterministic order)")
    pk.add_argument("dir", help="unpacked directory")
    pk.add_argument("output", help="output .pptx")
    va = sub.add_parser("validate", help="check package structure; exit 1 on problems")
    va.add_argument("input", help=".pptx file or unpacked directory")
    va.add_argument("--json", action="store_true", help="machine-readable report")
    args = ap.parse_args(argv)

    try:
        if args.cmd == "unpack":
            n = unpack(args.input, args.dir, args.pretty)
            print("unpacked %d part(s) to %s" % (n, args.dir))
            return 0
        if args.cmd == "pack":
            n = pack(args.dir, args.output)
            print("packed %d part(s) into %s" % (n, args.output))
            return 0
        rep = validate(args.input)
    except (OSError, zipfile.BadZipFile) as exc:
        print("error: cannot read %s: %s" % (getattr(args, "input", args.dir if hasattr(args, "dir") else ""), exc), file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps({"ok": not rep.problems, "problemCount": len(rep.problems), "problems": rep.problems}, indent=2))
    else:
        for p in rep.problems:
            print("PROBLEM [%s] %s: %s" % (p["code"], p["part"], p["message"]))
        print("%s: %d problem(s)" % ("FAIL" if rep.problems else "OK", len(rep.problems)))
    return 1 if rep.problems else 0


if __name__ == "__main__":
    sys.exit(main())
