#!/usr/bin/env python3
"""Build three small preview decks so a person can choose a visual style.

Each preview (style-a.pptx, style-b.pptx, style-c.pptx) has at most two slides:
the cover and one content slide, taken from the spec (or synthesised from
--title/--subtitle). The slides carry no theme names, so the choice is made on
looks alone. The mapping letter -> theme id is printed to stdout.

Themes come from --themes (explicit, comma separated; these may include
autoPick=false themes because the person named them) or from --auto N, which
picks N contrasting auto-pickable themes (different families, mixed dark and
light) by matching the spec's audience, goal and title words against each
theme's suitedFor / audience / mood. Themes with autoPick=false are never
chosen automatically.

Layout variants are fixed from the original spec so all previews show the same
layouts and differ only in style.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _common as C  # noqa: E402

CONTENT_ROLES = ["breakdown", "metrics", "context", "process", "comparison", "observation", "statement", "result", "actions"]
STOP = set("the and for with from that this your you our are will into about over under their them they have has was were been more most than then also not but can all any one two new out its who how why what when where which".split())


def _words(text: str) -> List[str]:
    return [w for w in re.findall(r"[a-z]{3,}", text.lower()) if w not in STOP]


def _stem(w: str) -> str:
    for suf in ("ing", "ers", "er", "es", "s"):
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            return w[: -len(suf)]
    return w


def score_theme(theme: Dict[str, Any], keywords: List[str]) -> float:
    """Keyword overlap between the spec text and a theme's suitedFor (weight 1), audience and mood (0.5)."""
    kw = {_stem(w) for w in keywords}
    strong = {_stem(w) for p in theme.get("suitedFor", []) for w in _words(p)}
    weak = {_stem(w) for w in _words(theme.get("audience", "") + " " + theme.get("mood", ""))}
    return len(kw & strong) + 0.5 * len(kw & weak)


def auto_pick(spec_text: str, seed: str, n: int, exclude: Optional[List[str]] = None) -> List[str]:
    """Pick *n* contrasting auto-pickable theme ids (different families, alternating dark/light)."""
    kws = _words(spec_text)
    pool = [t for t in C.load_themes() if t.get("autoPick", True) and t["id"] not in (exclude or [])]

    def tie(t: Dict[str, Any]) -> float:
        return int(hashlib.sha256((seed + ":" + t["id"]).encode()).hexdigest()[:8], 16) / 0xFFFFFFFF

    chosen: List[Dict[str, Any]] = []
    for _ in range(min(n, len(pool))):
        best, best_s = None, -1.0
        for t in pool:
            if t in chosen:
                continue
            s = score_theme(t, kws) + 0.01 * tie(t)
            if chosen:
                if all(t["family"] != c["family"] for c in chosen):
                    s += 2.0
                if all(bool(t["dark"]) != bool(c["dark"]) for c in chosen) or (len(chosen) >= 2 and any(bool(t["dark"]) != bool(c["dark"]) for c in chosen)):
                    s += 0.8
            if s > best_s:
                best, best_s = t, s
        chosen.append(best)
    return [t["id"] for t in chosen]


def make_preview_spec(spec: Dict[str, Any]) -> Dict[str, Any]:
    """Reduce a spec to a cover plus one content slide, keeping each slide's resolved layout variant."""
    out = copy.deepcopy(spec)
    slides = spec["slides"]
    cover_i = next((i for i, s in enumerate(slides) if s["role"] == "cover"), 0)
    content_i = None
    for role in CONTENT_ROLES:
        content_i = next((i for i, s in enumerate(slides) if s["role"] == role), None)
        if content_i is not None:
            break
    if content_i is None:
        content_i = next((i for i in range(len(slides)) if i != cover_i), None)
    picked = [cover_i] + ([content_i] if content_i is not None else [])
    new = []
    for i in picked:
        s = copy.deepcopy(slides[i])
        s["layoutVariant"] = C.resolve_variant(spec, i)
        new.append(s)
    out["slides"] = new
    out.pop("durationMinutes", None)
    out.pop("template", None)
    return out


def synthetic_spec(title: str, subtitle: str) -> Dict[str, Any]:
    """Minimal spec for --title/--subtitle: a cover and a three-point breakdown."""
    def t(full: str, short: Optional[str] = None) -> Dict[str, str]:
        return {"full": full, "short": short or full}

    pts = [("First point", "Where we start"), ("Second point", "What changes"), ("Third point", "What happens next")]
    return {
        "schemaVersion": 1,
        "title": title,
        "goal": subtitle or title,
        "audience": subtitle or title,
        "language": "en",
        "randomSeed": "preview-20260101-abc",
        "theme": "spectrum-report",
        "slides": [
            {"id": "cover", "role": "cover", "coreMessage": title, "title": t(title[:60]), "summary": t(subtitle[:140]) if subtitle else t(" ".join(title.split()[:3]))},
            {
                "id": "outline",
                "role": "breakdown",
                "coreMessage": "A sample content slide.",
                "title": t("How it looks with content", "Sample content"),
                "items": [{"id": "p%d" % i, "label": a, "detail": t(b)} for i, (a, b) in enumerate(pts)],
                "layoutVariant": 2,
            },
        ],
    }


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="Build style preview decks (style-a/b/c.pptx, cover + one content slide, no theme names on the slides) "
        "and print which theme each letter is. Use --themes for explicit choices or --auto N to pick N contrasting themes.",
    )
    ap.add_argument("--spec", help="deck spec JSON; the cover and one content slide are used")
    ap.add_argument("--title", help="deck title (when no --spec is given)")
    ap.add_argument("--subtitle", default="", help="subtitle / audience text (when no --spec is given)")
    ap.add_argument("--themes", help="comma separated theme ids, e.g. swiss-cobalt,onyx-gold,paper-noir (explicit choices may include autoPick=false themes)")
    ap.add_argument("--auto", type=int, metavar="N", help="pick N contrasting auto-pickable themes from the audience/goal keywords (default 3 when --themes is absent); fills up --themes to N")
    ap.add_argument("-o", "--outdir", required=True, help="output directory for style-a.pptx, style-b.pptx, ...")
    args = ap.parse_args(argv)

    if args.spec:
        spec_path = Path(args.spec).resolve()
        spec = C.load_json(spec_path)
        spec_dir = spec_path.parent
        base_spec = spec
    elif args.title:
        spec = synthetic_spec(args.title, args.subtitle)
        spec_dir = Path.cwd()
        base_spec = spec
    else:
        ap.error("give --spec or --title")

    themes: List[str] = [x.strip() for x in args.themes.split(",") if x.strip()] if args.themes else []
    for tid in themes:
        try:
            C.get_theme(tid)
        except KeyError as exc:
            ap.error(str(exc.args[0]))
    want = args.auto if args.auto else (0 if themes else 3)
    if want > len(themes):
        text = " ".join(str(base_spec.get(k, "")) for k in ("title", "goal", "audience"))
        themes += auto_pick(text, base_spec.get("randomSeed", ""), want - len(themes), exclude=themes)
    if not themes:
        ap.error("no themes selected")
    if len(themes) > 6:
        ap.error("at most 6 previews (a-f)")

    import build_deck as B

    preview = make_preview_spec(spec)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    print("Preview decks in %s:" % outdir)
    for letter, tid in zip("abcdef", themes):
        out = outdir / ("style-%s.pptx" % letter)
        B.build_deck(preview, out, spec_dir=spec_dir, theme_id=tid, validate=False)
        print("  style-%s.pptx -> %s (%s)" % (letter, tid, C.get_theme(tid)["name"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
