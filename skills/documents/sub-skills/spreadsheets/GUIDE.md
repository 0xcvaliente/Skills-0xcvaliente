# spreadsheets: .xlsx, .xlsm, .csv, .tsv

An `.xlsx` is a ZIP of XML parts: `xl/workbook.xml`, one `xl/worksheets/sheetN.xml` per sheet, `xl/sharedStrings.xml`, `xl/styles.xml`, charts and drawings. A formula cell stores the formula **and** a cached result; libraries that write formulas usually store no result.

## Choose the approach

| Task | Approach |
|---|---|
| Look at a workbook | `python3 scripts/inspect_office.py FILE --text` (sheets, formulas, errors, cached values) |
| Create or edit with formulas, formats, charts | `openpyxl` |
| Bulk data in or out, reshaping, joins | `pandas` (`read_excel`, `to_excel`, `read_csv`); format afterwards with `openpyxl` |
| CSV/TSV cleanup | Python `csv`/`pandas`; mind encoding and types (below) |
| Check formulas, recalculate | `python3 scripts/xlsx_check.py FILE --recalc` |
| Convert (`xls` to `xlsx`, `xlsx` to `csv`/`pdf`) | `soffice --headless --convert-to xlsx FILE --outdir out/` |
| See how it looks | `python3 scripts/render.py FILE` |

Run `python3 scripts/doctor.py` first. The inspector and checker need no library.

## Requirements for anything you build

- **Formulas, not pasted results.** Write `=SUM(B2:B9)`, not the number Python computed. The sheet must update when inputs change.
- **Inputs separate from calculations.** Put assumptions (rates, dates, thresholds) in labelled cells, and have formulas point at them. No magic numbers inside formulas.
- **Follow the spec literally.** Exact sheet names, column headers, and formulas the user gave. If you see a better design, propose it; do not silently substitute.
- **Label and document.** Units in headers, a short notes area or cell comments for assumptions and sources, and a legend if someone else will fill it in.
- **Zero errors.** No `#REF!`, `#DIV/0!`, `#NAME?`, `#VALUE!`, `#N/A` in the delivered file unless they are intentional and explained.
- **Readable by default:** frozen header row, sensible column widths, number formats that match the data (currency, percent, dates), no merged cells inside data tables, print area and orientation for sheets that will be printed.
- **Editing an existing file: its conventions override these.** Find the designated input cells (often a distinct font colour or fill), write only there, leave existing formulas and formatting alone, and match its fonts and number formats.

A common modelling convention for finance work: blue font for hard-coded inputs, black for formulas, green for links to other sheets. Follow whatever the workbook already uses.

## Recalculate: the step people skip

`openpyxl` saves formulas as text with **no cached value**. Until a spreadsheet engine recalculates, readers that use cached values (pandas, many previewers, `load_workbook(data_only=True)`) see empty cells.

```bash
python3 scripts/xlsx_check.py out.xlsx                           # reports formulas with no calculated value, and error cells
python3 scripts/xlsx_check.py out.xlsx --recalc --outdir calc/   # LibreOffice recalculates a COPY and checks that
```

Deliver the recalculated copy (`out.recalculated.xlsx`) if viewers must show values without recalculating; Excel recalculates on open either way. The original is never modified. Exit code 1 means problems were found.

A clean result proves formulas evaluate, not that they are right: an off-by-one range gives a clean file with wrong numbers. After building, compute two or three results independently (in Python, or by hand) and compare them to the cells.

If the workbook links to other files (`inspect_office.py` shows `external links`), recalculating without those files can turn the linked cells into errors. Keep cached values for those cells and warn the user.

## openpyxl essentials and gotchas

```python
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

wb = Workbook()
ws = wb.active
ws.title = "Summary"
ws.append(["Item", "Qty", "Price", "Total"])
for r, (item, qty, price) in enumerate([("A", 2, 3.5), ("B", 4, 1.25)], start=2):
    ws.append([item, qty, price, f"=B{r}*C{r}"])
ws["D4"] = "=SUM(D2:D3)"
ws["D4"].number_format = '#,##0.00'
ws.freeze_panes = "A2"
ws.column_dimensions["A"].width = 18
for c in ws[1]:
    c.font = Font(bold=True)
wb.save("out.xlsx")
```

- **Two loads to read a model.** `load_workbook(p)` gives formula text; `load_workbook(p, data_only=True)` gives cached values. One load cannot give both.
- **Never save a workbook opened with `data_only=True`.** It replaces every formula with its cached value, permanently.
- **`data_only=True` on a file openpyxl just wrote returns `None`**: there are no cached values until a recalculation.
- **Formula syntax:** English function names, comma argument separators, A1 references. Sheet names with spaces need quotes: `='Q3 Data'!B2`.
- **Function compatibility.** Prefer long-established functions: `SUMIFS`, `COUNTIFS`, `INDEX`/`MATCH`, `IFERROR`, `SUMPRODUCT`. Functions added to Excel after 2007 must be written with the `_xlfn.` prefix when a library writes the XML (for example `_xlfn.CONCAT`, `_xlfn.TEXTJOIN`, `_xlfn.IFS`, `_xlfn.MAXIFS`), or they show `#NAME?`. Avoid dynamic-array functions (`FILTER`, `SORT`, `UNIQUE`, `SEQUENCE`, `XLOOKUP`) in files you generate: libraries do not write the spill metadata they need and other engines may not evaluate them. Sort, filter, and de-duplicate in Python and write the results.
- **Merged cells:** write to the top-left cell only; the others are read-only placeholders.
- **Dates:** write real `datetime`/`date` objects and set a number format; text that looks like a date is not one. Percentages: store `0.15` and format `0.0%`.
- **Large data:** `Workbook(write_only=True)` streams rows; `load_workbook(read_only=True)` reads without loading everything.
- **Preserving what you did not touch:** openpyxl drops things it does not model (some charts, images, pivot tables, slicers, form controls). Before saving over an existing workbook, run `inspect_office.py` on the original and again on the result and compare the charts/defined names/external links lines. If something would be lost, edit the XML instead (`scripts/ooxml_pack.py`).
- **Macro-enabled files:** `load_workbook(p, keep_vba=True)` keeps the macros; save as `.xlsm`. Never run them.
- **Charts:** `openpyxl.chart` makes native charts (`BarChart`, `LineChart`, `PieChart`, `ScatterChart`) from cell ranges. Give them a title, axis titles, and a legend only when there are several series.
- **Validation and conditional formats:** `DataValidation` for dropdowns; `ws.conditional_formatting.add(...)` with rules. Keep colours meaningful and add a legend.
- **Protection:** sheet protection stops accidents, not attackers. Do not describe it as security.

## CSV and TSV

- **Encoding:** read as UTF-8 first. Excel opens UTF-8 CSV correctly only with a byte-order mark: write `encoding="utf-8-sig"` for files meant for Excel.
- **Delimiter:** in some locales Excel uses `;`. Detect with `csv.Sniffer` or ask; do not assume commas.
- **Types:** keep identifiers as text. Leading zeros (`00123`), long numbers (account or order ids), and codes like `1E5` are silently changed if parsed as numbers. With pandas, pass `dtype=str` for those columns.
- **Dates:** ambiguous day/month order is a real bug source. Parse with an explicit format and say which.
- **Formula injection:** a text cell that begins with `=`, `+`, `-`, or `@` runs as a formula when the file is opened in a spreadsheet. When you export untrusted or user-provided text, prefix such cells with a single quote or tab, or write them as text cells in `.xlsx`.
- **Messy inputs:** report what you found (blank rows, repeated headers, mixed types, duplicate keys, trailing totals) and what you did about each, instead of cleaning silently.

## Analysis work

When the task is understanding data rather than building a model: state the question, read the data and profile it (row counts, nulls, ranges, duplicates), do the calculation in a language with tests or a formula the user can audit, and show the numbers behind any statement. Say which rows you excluded and why. Do not round intermediate results.

## Verify

1. `python3 scripts/xlsx_check.py OUT.xlsx --recalc`: zero errors, zero uncalculated formulas.
2. `python3 scripts/inspect_office.py OUT.xlsx --text`: sheets, dimensions, defined names, and a sample of values are as intended; hidden sheets are known.
3. Two or three results recomputed independently match.
4. `python3 scripts/render.py OUT.xlsx`: columns not truncated (`####`), print layout acceptable.
5. State what you did not check: Excel-only features, macros, pivot refresh, external links.

## Before sharing

Hidden sheets, hidden rows/columns, comments with names, document properties (author), external links to other files or paths on your machine, and cached values from before an edit. Report them; remove them only with the user's agreement.
