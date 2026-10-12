# Export and convert recipes

Check what is available first: `python3 scripts/doctor.py`. Always write to a new filename, then look at the result with `python3 scripts/render.py OUT`.

## Markdown to .docx

With pandoc:

```bash
pandoc report.md -o report.docx
pandoc report.md --reference-doc=house-style.docx -o report.docx   # use a styled template
pandoc report.md --toc --toc-depth=3 -o report.docx                # table of contents
```

`--reference-doc` takes fonts, heading styles, margins, headers and footers from a `.docx` whose styles you set up once; pandoc fills in the content. Generate the starting reference with `pandoc -o custom-reference.docx --print-default-data-file reference.docx`, edit its styles in a word processor, and reuse it.

Without pandoc, convert through HTML with LibreOffice:

```bash
soffice --headless --convert-to docx:"MS Word 2007 XML" report.html --outdir out/
```

The fidelity is lower (list nesting and table widths may need touching up). If the document needs precise layout, build the `.docx` with a library instead: `../word/GUIDE.md`.

## Anything to .pdf

```bash
python3 scripts/render.py report.docx --outdir out/     # LibreOffice; also writes page images when Poppler/MuPDF exist
pandoc report.md -o report.pdf                          # needs a LaTeX or other PDF engine installed
soffice --headless --convert-to pdf report.html --outdir out/
```

Fonts missing on the machine are substituted, which can change line breaks and page counts. For a final PDF whose layout matters, say which fonts were used or embed the ones you have.

## HTML

```bash
pandoc report.md -s --metadata title="Report" -o report.html
```

Add `--css style.css` for styling. Self-contained single file: `--embed-resources --standalone` (pandoc 2.19+; older versions use `--self-contained`).

## .docx or .pdf to Markdown

```bash
pandoc report.docx -t gfm --wrap=none -o report.md --extract-media=media
python3 scripts/pdf_tool.py text report.pdf          # PDF text; tables and columns may need ../pdf/GUIDE.md
```

Conversion loses comments, tracked changes, and some layout. Say so.

## After exporting, check

- Headings are real headings (open the outline or run `python3 scripts/inspect_office.py out.docx`).
- Tables kept their header row and did not overflow the page width.
- Links are live; images are present and have alt text.
- Lists are real lists, not lines starting with typed bullets.
- Page breaks and the table of contents are sensible after rendering.
- Metadata: set a title and author you intend; remove stray ones.
