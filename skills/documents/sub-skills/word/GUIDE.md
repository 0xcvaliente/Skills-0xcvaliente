# word: .docx and .dotx

A `.docx` is a ZIP of XML parts: `word/document.xml` (body), `word/styles.xml`, `word/numbering.xml` (lists), `word/comments.xml`, `word/header*.xml`, `word/footer*.xml`, `word/media/*`, plus `[Content_Types].xml` and relationship files. Legacy `.doc` is a different binary format: convert it first (`soffice --headless --convert-to docx file.doc --outdir out/`).

## Choose the approach

| Task | Approach |
|---|---|
| Read or summarise | `python3 scripts/inspect_office.py FILE --text`; or `pandoc FILE -t gfm` |
| Create a new document | `python-docx` (Python) or `docx` (npm). From Markdown: `pandoc` ([../docs/export.md](../docs/export.md)) |
| Fill a template | `python-docx`: open the template, replace text run by run, save a copy |
| Edit a few paragraphs, keep formatting | `python-docx`; edit runs, not whole paragraphs |
| Tracked changes, comments, headers with fields, anything the library lacks | Unpack, edit XML, repack (`scripts/ooxml_pack.py`) |
| Convert to PDF / check how it looks | `python3 scripts/render.py FILE` |

Run `python3 scripts/doctor.py` first. With no Word library installed, the unpack-and-edit route still works with only the standard library.

## Build with structure, not decoration

- Use **styles**: `Title`, `Heading 1-3`, `Normal`, `List Bullet`, `List Number`, `Caption`. Change a style once instead of formatting each paragraph. Headings then give a navigation pane, a table of contents, and accessibility for free.
- Never type bullets or numbers (`•`, `1.`). Use list styles or a numbering definition.
- Never use spaces or tabs to position text; never blank paragraphs for spacing. Use paragraph spacing (before/after), indents, tab stops, and page-break-before.
- One font family for body, one for headings. Set them in styles. Check the font exists on the reader's machine; if not, name a fallback.
- Tables hold data, not layout. Mark the header row to repeat across pages; set column widths; avoid merged cells in data tables.
- Images: insert at a sensible width, add alt text, put captions in the `Caption` style.

### python-docx essentials

```python
from docx import Document
from docx.shared import Inches, Pt

doc = Document()                                   # or Document("template.docx")
sec = doc.sections[0]
sec.page_width, sec.page_height = Inches(8.27), Inches(11.69)   # A4; set explicitly, do not trust the default
sec.left_margin = sec.right_margin = Inches(1)

doc.add_heading("Quarterly report", level=0)       # Title style
doc.add_heading("Summary", level=1)
p = doc.add_paragraph("Revenue grew ")
p.add_run("12%").bold = True
doc.add_paragraph("First point", style="List Bullet")

t = doc.add_table(rows=1, cols=3, style="Table Grid")
for cell, text in zip(t.rows[0].cells, ["Region", "Q2", "Q3"]):
    cell.text = text
doc.add_picture("chart.png", width=Inches(5.5))
doc.core_properties.title = "Quarterly report"
doc.core_properties.author = "Team name"           # set deliberately, see "Before sharing"
doc.save("report-v1.docx")
```

Footguns:

- The library's default template is not your house style; start from the user's template when they have one.
- A paragraph's text lives in **runs**. A phrase you can see may be split across several runs (spell-check, edits, formatting changes), so `paragraph.text.replace(...)` loses formatting and a naive run-level replace misses split phrases. Replace across runs: join the run texts, find the match, put the new text in the first run it touches, and blank the rest.
- Column widths in tables are honoured per cell: set `cell.width` on every cell in the column, not only the column.
- python-docx has no API for page-number or table-of-contents **fields**. Insert a field with XML (a `w:fldSimple` with `w:instr="PAGE"` in the footer, or a `TOC \o "1-3" \h \z \u` field). Fields show nothing useful until updated: tell the user to update fields (select all, F9) or render through LibreOffice to check.
- Units: 1 inch = 914400 EMU = 1440 twips ("dxa"); font sizes in XML are half-points (`w:sz="24"` is 12 pt). Page size in XML is in twips (US Letter 12240 x 15840, A4 11906 x 16838).
- Landscape: set orientation **and** swap width/height.
- Do not put a page break in an empty paragraph by hand when "page break before" on the next heading does the job.

### docx (npm) essentials

If Node is the available tool: `docx` builds documents from `Document`, `Paragraph`, `TextRun`, `Table`, `ImageRun`. Set the page size explicitly (it defaults to A4), give tables both a total width and per-column widths in DXA, use a `numbering` config for lists, never `\n` inside a `TextRun` (use separate paragraphs), and give `ImageRun` a `type`. It writes new files only; it cannot open an existing one.

## Edit an existing document safely

1. `python3 scripts/inspect_office.py FILE`: note headings, tables, comments, tracked changes, fields, macros.
2. Work on a copy. Make the smallest change that does the job; leave unrelated text, styles, and section settings untouched.
3. Match what is there: the document's own styles, fonts, list formats, and numbering, even where you would do it differently.
4. If the document has tracked changes on, or the user wants to see what you changed, make **tracked changes**, not silent edits (below).
5. Re-run `inspect_office.py` and `render.py`; compare against the original.

### Unpack, edit, repack

```bash
python3 scripts/ooxml_pack.py unpack input.docx work/
# edit work/word/document.xml etc. Do not reformat or pretty-print the XML
python3 scripts/ooxml_pack.py pack work/ output.docx --original input.docx
python3 scripts/inspect_office.py output.docx
python3 scripts/render.py output.docx
```

`unpack` refuses unsafe paths and symlinks; `pack` refuses malformed XML and puts `[Content_Types].xml` first. Keep the XML declaration and namespace prefixes as they are. Preserve `xml:space="preserve"` on `<w:t>` elements with leading or trailing spaces.

### Tracked changes

Insertion and deletion wrap runs, each with a unique `w:id`, an author, and a date:

```xml
<w:ins w:id="101" w:author="Reviewer" w:date="2026-03-01T09:00:00Z">
  <w:r><w:t>new words</w:t></w:r>
</w:ins>
<w:del w:id="102" w:author="Reviewer" w:date="2026-03-01T09:00:00Z">
  <w:r><w:delText>old words</w:delText></w:r>
</w:del>
```

Inside `<w:del>` the text element is `<w:delText>`, never `<w:t>`. Ids must be unique across all tracked changes and comments in the part. To delete a whole paragraph as a tracked change, delete every run and also mark the paragraph mark deleted, or an empty paragraph remains once changes are accepted. Use the name the user gives you as author. Do not "accept all" or "reject all" unless asked; to produce a clean copy, have the user (or a word processor you can drive) accept the changes, then check that no deleted text or empty bullet remains.

### Comments

Comments need `word/comments.xml`, range markers in `document.xml`, a content-type override, and a relationship. The step-by-step is in [../docs/review-and-comments.md](../docs/review-and-comments.md).

### Template filling

Keep placeholders unambiguous (`{{client_name}}`) so they are easy to find even when split across runs. After replacing, search the output for `{{` to catch misses, and render it. Do not invent values for fields the user did not supply: leave them visibly marked or ask.

## Special content

- **Headers/footers:** per section; "different first page" and odd/even settings change which part is used. Check each section.
- **Table of contents:** needs real heading styles. Insert the field; say it needs updating.
- **Footnotes/endnotes:** library support is limited; use XML or pandoc.
- **Equations, SmartArt, embedded objects:** preserve when editing; do not attempt to rebuild with a library.
- **Forms (content controls, legacy form fields):** inspect the XML before changing; protected documents may refuse edits.
- **Macros (`.docm`):** never run or enable. If preserving them, say the file still contains macros.
- **Right-to-left or complex scripts:** set the language and paragraph direction; test the render.

## Verify

1. `python3 scripts/inspect_office.py OUT.docx`: outline is as intended, no unexpected tracked changes, comment count right, no stray placeholders in `--text`.
2. `python3 scripts/render.py OUT.docx --montage`: look at every page. Check page breaks, orphaned headings, table overflow, clipped images, fonts.
3. For documents others will open in Word, say plainly that you checked in a LibreOffice render, not in Word.

## Before sharing

Check and report: author and last-modified-by names in metadata, comments, tracked changes, hidden text, and file name. Remove or confirm each one with the user before the file leaves their hands. Accessibility basics: real headings, alt text on images, a header row on tables, document language set, meaningful link text.
