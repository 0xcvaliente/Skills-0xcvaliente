# Tables and charts

Read with [GUIDE.md](GUIDE.md). Applies to Word, PDF, slides, spreadsheets, and docs.

## Choose the display

| You want to show | Use | Avoid |
|---|---|---|
| Exact values to look up or compare | Table | A chart that hides the numbers |
| Change over time | Line (many points), column (few periods) | Pie, area stacks with many series |
| Comparison between categories | Horizontal bars sorted by value; vertical columns for few, short labels | 3D, radar, unsorted bars |
| Part of a whole | Stacked bar or a single 100% bar; pie/donut only for 2-4 parts that add to 100% | Pies with more than five slices |
| Relationship between two measures | Scatter (add a trend line only if you can defend it) | Dual-axis lines that imply a link |
| Distribution | Histogram or box plot | Averages alone |
| One key number | A big number with a label and context (vs target, vs last period) | A chart with one bar |
| Process or structure | Diagram (see the diagram-craft skill if installed) | A chart |

If the reader can only keep one thing, give them the number or the takeaway as text next to the display.

## Tables

- **Header row** styled differently from the body and set to repeat across pages. Left-align text columns and headers over text; right-align numbers and their headers.
- **Numbers:** same decimals down a column; thousands separators; units and currency in the header (`Revenue (EUR k)`), not in every cell; negative numbers consistently marked; percent and currency formatted as such.
- **Rules:** thin horizontal lines or light zebra bands, not a full grid. Use a heavier line only above totals.
- **Width:** no more than about seven columns in portrait. If it does not fit, rotate the page, split the table, or move it to an appendix. Do not shrink text below the minimum.
- **Density:** row height at least 1.4x text size. Pad cells (about 4-8 pt).
- **Emphasis:** bold the row or cell that matters, not everything. Highlight with one colour and explain it.
- **Order:** sort by what the reader looks for (largest first, alphabetical for lookup, chronological for time). Keep an obvious order.
- **Totals and notes:** totals set apart; sources, dates, and definitions in a note beneath.
- **Long tables:** repeat the header on each page; avoid splitting a row across pages; add "continued" if useful.

## Charts

1. **Title = the conclusion** ("Support tickets fell 31% after the redesign"), subtitle = what and when, with units.
2. **Axes:** label them with units. Bars and areas start at zero. A line chart may crop the axis if it is marked. Use the same scale across charts that are compared.
3. **Labels:** put values or series names directly on the marks where there is room; delete the legend when direct labels work. Gridlines faint or absent.
4. **Colour:** the preset's chart palette; grey for context series, one strong colour for the series that matters; the same colour for the same thing everywhere. At most five series; beyond that, group or split into small multiples.
5. **Ink:** no 3D, shadows, gradients, background images, or decorative icons inside plots. Minimise borders.
6. **Annotate:** mark the event or threshold that explains the shape (launch date, target line).
7. **Source line:** data source and date, small, under the chart.
8. **Native and editable:** build charts in the format's own chart object (`openpyxl.chart`, `python-pptx` chart data, Word via an embedded or pasted image if the library lacks charts). If you must use an image (Word, PDF), render at 200+ ppi, match the document's fonts and palette, and keep the data in an adjacent table or appendix.
9. **Accessibility:** alt text that states the takeaway and the main numbers; do not rely on colour alone (direct labels, markers, or line styles).

## Matching sizes to medium

| Medium | Chart text | Line weight | Notes |
|---|---|---|---|
| Slide | 14 pt and up (axis), 18 pt and up (labels you want read) | 2.25-3 pt lines, thick bars | One chart per slide, fills the content area |
| Document / PDF | 8-10 pt in the plot, caption 9 pt | 1-1.5 pt | Fits column width; caption below |
| Spreadsheet | Default sizes ok | Default | Place beside or below the data, not on top of it |

## Checks before you ship

- Do the numbers in the chart, the table, and the text agree?
- Is every unit, period, and source stated?
- Would it still read in greyscale and for someone who cannot tell red from green?
- Is anything on it purely decorative? Remove it.
