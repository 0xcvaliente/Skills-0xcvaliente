#!/usr/bin/env python3
"""Check a workbook for formula errors and formulas that were never calculated.

  xlsx_check.py FILE.xlsx [--recalc] [--outdir DIR] [--json]

Libraries such as openpyxl write formulas without cached results, so anything that reads
cached values (pandas, previews, many viewers) sees empty cells until a spreadsheet engine
recalculates. With --recalc this script has LibreOffice recalculate a COPY (the original is
never modified) and checks that copy. Exit code 1 means errors or uncalculated formulas were
found. A clean result proves formulas evaluate, not that they are correct: check a few
values by hand.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import PackageError, clean_err, die, find_soffice, open_package  # noqa: E402
from inspect_office import inspect_xlsx  # noqa: E402


def recalc_copy(src, outdir):
    soffice = find_soffice()
    if not soffice:
        die("LibreOffice not found; cannot recalculate. Re-run without --recalc to check cached values only.")
    os.makedirs(outdir, exist_ok=True)
    stage = tempfile.mkdtemp(prefix="xlsx-recalc-")
    profile = tempfile.mkdtemp(prefix="lo-profile-")
    try:
        r = subprocess.run(
            [soffice, f"-env:UserInstallation={Path(profile).as_uri()}", "--headless", "--norestore",
             "--convert-to", "xlsx:Calc MS Excel 2007 XML", "--outdir", stage, src],
            capture_output=True, text=True, timeout=180)
        produced = os.path.join(stage, Path(src).stem + ".xlsx")
        if r.returncode != 0 or not os.path.exists(produced):
            die(f"recalculation failed: {clean_err(r)}")
        dest = os.path.join(outdir, Path(src).stem + ".recalculated.xlsx")
        shutil.move(produced, dest)
        return dest
    except subprocess.TimeoutExpired:
        die("LibreOffice timed out (close other LibreOffice windows and retry)")
    finally:
        shutil.rmtree(stage, ignore_errors=True)
        shutil.rmtree(profile, ignore_errors=True)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    ap.add_argument("--recalc", action="store_true", help="recalculate a copy with LibreOffice first")
    ap.add_argument("--outdir", default=".", help="where the recalculated copy goes (default: current directory)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    target = a.file
    if a.recalc:
        target = recalc_copy(os.path.abspath(a.file), os.path.abspath(a.outdir))
    try:
        info = inspect_xlsx(open_package(target), want_text=False)
    except PackageError as e:
        die(str(e))
    total_err = sum(s.get("error_count", 0) for s in info["sheets"])
    total_unc = sum(s.get("formulas_without_cached_value", 0) for s in info["sheets"])
    total_f = sum(s.get("formulas", 0) for s in info["sheets"])
    result = {
        "checked": target, "recalculated_copy": bool(a.recalc), "formulas": total_f,
        "errors": total_err, "formulas_without_cached_value": total_unc,
        "external_links": info["external_links"],
        "status": "ok" if not total_err and not total_unc else "problems",
        "error_cells": [dict(sheet=s["name"], **e) for s in info["sheets"] for e in s.get("errors", [])],
    }
    if a.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"{result['status'].upper()}: {total_f} formulas, {total_err} error cells, "
              f"{total_unc} formulas with no calculated value  ({target})")
        for e in result["error_cells"][:20]:
            print(f"  {e['sheet']}!{e['cell']}: {e['value']}  {e['formula'] or ''}")
        if total_unc and not a.recalc:
            print("  hint: run again with --recalc to calculate a copy with LibreOffice")
        if info["external_links"]:
            print("  note: workbook links to other files; recalculation can turn those links into errors")
    sys.exit(0 if result["status"] == "ok" else 1)


if __name__ == "__main__":
    main()
