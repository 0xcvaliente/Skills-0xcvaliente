#!/usr/bin/env python3
"""Reorder, duplicate and delete slides of an existing .pptx.

Usage:
    rearrange.py IN.pptx -o OUT.pptx --order "1,3,3,2"

``--order`` lists the slides of the result by their 1-based position in the
input, e.g. ``"1,3,3,2"``. Ranges work too (``"1,4-6,2"``).

* A number that appears once keeps the original slide.
* A number that appears again creates a copy: the slide XML and its
  relationships are deep-copied. Charts are cloned together with their embedded
  workbook (and chart style/colour parts), notes slides are cloned and point at
  the new slide, all with new part names. Pictures, layouts, masters and themes
  are shared rather than copied, as PowerPoint itself does.
* A number that is left out deletes that slide: its slide id and relationship
  are removed so the part (and anything only it used) is not written.

Section lists (PowerPoint sections), custom shows and slide-jump hyperlinks
are kept consistent; sections are dropped, with a message, if the new order
no longer fits them. The result is checked with ooxml.py's validator.

Exit status: 0 ok, 1 invalid order or the output fails validation, 2 unreadable input.
"""

from __future__ import annotations

import argparse
import copy
import io
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as C  # noqa: E402

C.require_pptx()

from lxml import etree  # noqa: E402
from pptx import Presentation  # noqa: E402
from pptx.opc.constants import RELATIONSHIP_TARGET_MODE as RTM  # noqa: E402
from pptx.opc.package import _Relationship  # noqa: E402
from pptx.opc.packuri import PackURI  # noqa: E402

import ooxml  # noqa: E402

NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS_A = "http://schemas.openxmlformats.org/drawingml/2006/main"
NS_P14 = "http://schemas.microsoft.com/office/powerpoint/2010/main"
NSMAP = {"p": NS_P, "r": NS_R, "a": NS_A, "p14": NS_P14}

#: Relationship types whose targets are shared between the original and the copy.
SHARED_RELTYPES = (
    "slideLayout",
    "slideMaster",
    "notesMaster",
    "handoutMaster",
    "theme",
    "image",
    "video",
    "audio",
    "media",
    "slide",
)


def _xp(el: Any, expr: str) -> List[Any]:
    """XPath with the p/r/a/p14 prefixes (python-pptx's own xpath() lacks p14)."""
    return etree._Element.xpath(el, expr, namespaces=NSMAP)


def parse_order(text: str, count: int) -> List[int]:
    """Parse "1,3-4,2" into a list of 1-based slide numbers, validated against *count*."""
    out: List[int] = []
    for part in text.split(","):
        part = part.strip()
        if not part:
            continue
        m = re.fullmatch(r"(\d+)(?:\s*-\s*(\d+))?", part)
        if not m:
            raise ValueError("cannot read %r in --order (use numbers like 1,3,3,2 or ranges like 2-4)" % part)
        lo = int(m.group(1))
        hi = int(m.group(2)) if m.group(2) else lo
        step = 1 if hi >= lo else -1
        for i in range(lo, hi + step, step):
            out.append(i)
    if not out:
        raise ValueError("--order is empty; a deck needs at least one slide")
    bad = [i for i in out if not 1 <= i <= count]
    if bad:
        raise ValueError("slide number(s) %s out of range 1..%d" % (sorted(set(bad)), count))
    return out


# --------------------------------------------------------------------------
# Part cloning
# --------------------------------------------------------------------------


class Cloner:
    """Deep-copies parts (and the parts only they use) into the same package."""

    def __init__(self, package: Any) -> None:
        self.package = package
        self.used: Set[str] = {str(p.partname) for p in package.iter_parts()}
        self.cloned: List[Tuple[str, str]] = []

    def new_name(self, old: str) -> PackURI:
        m = re.fullmatch(r"(.*?)(\d*)(\.[^./]+)", old)
        if m:
            prefix, _digits, ext = m.groups()
        else:
            prefix, ext = old, ""
        n = 1
        while "%s%d%s" % (prefix, n, ext) in self.used:
            n += 1
        name = "%s%d%s" % (prefix, n, ext)
        self.used.add(name)
        return PackURI(name)

    @staticmethod
    def is_shared(reltype: str) -> bool:
        return reltype.rsplit("/", 1)[-1] in SHARED_RELTYPES

    def clone(self, part: Any, memo: Dict[Any, Any]) -> Any:
        if part in memo:
            return memo[part]
        new = type(part).load(self.new_name(str(part.partname)), part.content_type, self.package, part.blob)
        memo[part] = new
        self.cloned.append((str(part.partname), str(new.partname)))
        base = new.partname.baseURI
        for rid, rel in list(part.rels.items()):
            if rel.is_external:
                new.rels._rels[rid] = _Relationship(base, rid, rel.reltype, RTM.EXTERNAL, rel.target_ref)
                continue
            target = rel.target_part
            if target in memo:
                new_target = memo[target]
            elif self.is_shared(rel.reltype):
                new_target = target
            else:
                new_target = self.clone(target, memo)
            new.rels._rels[rid] = _Relationship(base, rid, rel.reltype, RTM.INTERNAL, new_target)
        return new


# --------------------------------------------------------------------------
# Presentation-level bookkeeping
# --------------------------------------------------------------------------


def _strip_jump_links(slide_part: Any, rid: str) -> None:
    for el in _xp(slide_part._element, '//*[@r:id="%s"]' % rid):
        if etree.QName(el).localname in ("hlinkClick", "hlinkHover"):
            el.getparent().remove(el)


def _update_sections(pres_el: Any, sections_plan: Dict[int, List[int]], new_ids: List[int], notes: List[str]) -> None:
    """Rewrite p14:sectionLst so it matches the new slide id sequence.

    *sections_plan* maps final-slide position -> source slide id; *new_ids* are the final slide ids.
    """
    lst = _xp(pres_el, "p:extLst/p:ext/p14:sectionLst")
    if not lst:
        return
    section_lst = lst[0]
    sections = _xp(section_lst, "p14:section")
    section_of: Dict[int, int] = {}
    for si, sec in enumerate(sections):
        for el in _xp(sec, "p14:sldIdLst/p14:sldId"):
            section_of[int(el.get("id"))] = si
    final_sections: List[Optional[int]] = []
    for pos, new_id in enumerate(new_ids):
        src = sections_plan[pos][0]
        final_sections.append(section_of.get(src))
    known = [s for s in final_sections if s is not None]
    if any(b < a for a, b in zip(known, known[1:])) or len(known) != len(final_sections):
        ext = section_lst.getparent()
        ext.getparent().remove(ext)
        notes.append("sections were removed because the new order no longer fits them")
        return
    for sec in sections:
        holder = sec.find("{%s}sldIdLst" % NS_P14)
        for el in list(holder):
            holder.remove(el)
    for pos, new_id in enumerate(new_ids):
        holder = sections[final_sections[pos]].find("{%s}sldIdLst" % NS_P14)
        el = etree.SubElement(holder, "{%s}sldId" % NS_P14)
        el.set("id", str(new_id))


def rearrange(prs: Any, order: List[int]) -> Dict[str, Any]:
    """Apply *order* to *prs* in place. Returns a summary dict."""
    pres_part = prs.part
    pres_el = pres_part._element
    sld_lst = pres_el.sldIdLst
    old_els = list(sld_lst)
    old_rids = [e.rId for e in old_els]
    old_parts = [pres_part.related_part(r) for r in old_rids]
    old_ids = [int(e.id) for e in old_els]
    cloner = Cloner(pres_part.package)
    notes: List[str] = []

    final: List[Any] = []  # sldId elements in final order
    plan: Dict[int, List[int]] = {}  # position -> [source slide id]
    seen: Set[int] = set()
    copies = 0
    for pos, num in enumerate(order):
        i = num - 1
        if num not in seen:
            seen.add(num)
            final.append(old_els[i])
        else:
            memo: Dict[Any, Any] = {}
            new_part = cloner.clone(old_parts[i], memo)
            rid = pres_part.relate_to(new_part, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide")
            final.append(sld_lst.add_sldId(rid))
            copies += 1
        plan[pos] = [old_ids[i]]

    # detach everything, then re-append in the requested order
    for el in list(sld_lst):
        sld_lst.remove(el)
    for el in final:
        sld_lst.append(el)

    deleted_rids = [r for k, r in enumerate(old_rids, start=1) if k not in seen]
    # custom shows may list slides by relationship id
    for rid in deleted_rids:
        for el in _xp(pres_el, 'p:custShowLst//p:sldId[@r:id="%s"]' % rid):
            el.getparent().remove(el)
    for rid in deleted_rids:
        pres_part.drop_rel(rid)

    kept_parts = {pres_part.related_part(e.rId) for e in final}
    # slide-jump links that point at deleted slides
    for sp in list(kept_parts):
        for rid, rel in list(sp.rels.items()):
            if not rel.is_external and rel.reltype.endswith("/slide") and rel.target_part not in kept_parts:
                _strip_jump_links(sp, rid)
                sp.rels.pop(rid)

    pres_part.rename_slide_parts([e.rId for e in final])
    new_ids = [int(e.id) for e in final]
    _update_sections(pres_el, plan, new_ids, notes)

    # docProps/app.xml slide count
    for part in pres_part.package.iter_parts():
        if str(part.partname) == "/docProps/app.xml" and hasattr(part, "_blob"):
            try:
                blob = part.blob.decode("utf-8")
                blob = re.sub(r"<Slides>\d+</Slides>", "<Slides>%d</Slides>" % len(final), blob)
                part._blob = blob.encode("utf-8")
            except Exception:
                pass
    return {
        "kept": len(seen),
        "copied": copies,
        "deleted": len(old_els) - len(seen),
        "cloned_parts": cloner.cloned,
        "notes": notes,
        "total": len(final),
    }


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="Reorder, duplicate (repeat a number) and delete (omit a number) slides of a .pptx. "
        "Copies include charts with their workbooks and notes slides, under new part names.",
    )
    ap.add_argument("input", help="input .pptx")
    ap.add_argument("-o", "--output", required=True, help="output .pptx")
    ap.add_argument("--order", required=True, help='slides of the result by 1-based input position, e.g. "1,3,3,2" or "1,4-6"')
    args = ap.parse_args(argv)
    try:
        before = ooxml.validate(args.input)
        prs = Presentation(args.input)
    except Exception as exc:
        print("error: cannot open %s: %s" % (args.input, exc), file=sys.stderr)
        return 2
    try:
        order = parse_order(args.order, len(prs.slides))
    except ValueError as exc:
        print("error: %s" % exc, file=sys.stderr)
        return 1
    summary = rearrange(prs, order)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    prs.save(args.output)
    print(
        "wrote %s: %d slide(s) (%d kept, %d copied, %d deleted)"
        % (args.output, summary["total"], summary["kept"], summary["copied"], summary["deleted"])
    )
    for old, new in summary["cloned_parts"]:
        print("  cloned %s -> %s" % (old, new))
    for n in summary["notes"]:
        print("  note: " + n)
    after = ooxml.validate(args.output)
    if after.problems:
        known = {(p["code"], p["part"], p["message"]) for p in before.problems}
        fresh = [p for p in after.problems if (p["code"], p["part"], p["message"]) not in known]
        for p in after.problems:
            print("  PROBLEM [%s] %s: %s" % (p["code"], p["part"], p["message"]), file=sys.stderr)
        if fresh:
            print("output failed validation", file=sys.stderr)
            return 1
    else:
        print("validation: OK (no orphan parts, dangling relationships or content-type gaps)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
