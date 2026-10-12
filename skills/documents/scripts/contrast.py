#!/usr/bin/env python3
"""WCAG colour contrast checker (standard library only).

  contrast.py FOREGROUND BACKGROUND [--size 11] [--bold]
  contrast.py --tokens [PRESET]            # check every contrast pair in the design tokens

Colours are 6-digit hex (with or without #). AA needs 4.5:1 for normal text and 3:1 for
large text (18 pt, or 14 pt bold) and for graphics such as chart lines and icons.
Exit code 1 when a checked pair fails AA.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _design import contrast_ratio, load_tokens, required_ratio  # noqa: E402


def check_pair(fg, bg, size=None, bold=False):
    ratio = contrast_ratio(fg, bg)
    need = required_ratio(size, bold, "AA")
    return ratio, need, ratio >= need


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("colors", nargs="*", help="FOREGROUND BACKGROUND")
    ap.add_argument("--size", type=float, help="text size in points (decides normal vs large)")
    ap.add_argument("--bold", action="store_true")
    ap.add_argument("--tokens", nargs="?", const="*", metavar="PRESET", help="check design-token pairs")
    a = ap.parse_args(argv)
    failed = False
    if a.tokens:
        presets = load_tokens()["presets"]
        names = list(presets) if a.tokens == "*" else [a.tokens]
        for n in names:
            if n not in presets:
                sys.exit(f"error: unknown preset {n!r}; choose from {', '.join(presets)}")
            p = presets[n]
            for fg, bg in p["contrast_pairs"]:
                ratio, need, ok = check_pair(p["colors"][fg], p["colors"][bg])
                failed |= not ok
                print(f"{'ok  ' if ok else 'FAIL'} {n}: {fg} on {bg} = {ratio:.2f}:1 (need {need}:1)")
            for i, col in enumerate(p["chart"], 1):
                ratio = contrast_ratio(col, p["colors"]["background"])
                ok = ratio >= 3.0
                failed |= not ok
                print(f"{'ok  ' if ok else 'FAIL'} {n}: chart series {i} {col} on background = {ratio:.2f}:1 (graphics need 3:1)")
    else:
        if len(a.colors) != 2:
            ap.error("give FOREGROUND and BACKGROUND, or use --tokens")
        try:
            ratio, need, ok = check_pair(a.colors[0], a.colors[1], a.size, a.bold)
        except ValueError as e:
            sys.exit(f"error: {e}")
        failed = not ok
        print(f"{ratio:.2f}:1  {'passes' if ok else 'FAILS'} AA (needs {need}:1)"
              + ("" if a.size else "  [size not given: normal text assumed]"))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
