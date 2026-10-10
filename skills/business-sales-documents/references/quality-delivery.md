# Quality and delivery

Scale verification to the task. Tiny edits need meaning, local layout, and file checks; new brochures need source, reader, design, and export checks. Report completed checks rather than assigning a score to your own work.

## Content and commercial fit

Check requested coverage/changes, clear category, audience relevance, and practical action. Retain necessary detail even when dense technical comparison is appropriate. A requested one-pager must fit one page without becoming unreadable.

Verify units, values, names, identifiers, dates, prices, terms, and examples. Separate customer outcomes, company statements, and illustrations. Omit unsupported optional claims; identify facts essential to finalization. Current authority takes priority over historical profiles.

## Visual and file checks

Render with the matching file skill (`docx`, `pptx`, `pdf`, if available) or installed tools and inspect page/slide images with the Read tool. Check clipping, collisions, missing glyphs, distorted logos, unintended fonts, tight cells, awkward breaks, and empty overflow pages. Inspect real-size readability in the intended print/digital use.

Check hierarchy across page roles, numbering, captions, cross-references, headers/footers, contrast, and color-independent meaning. Reopen the final file; verify requested format/editability, pages, appropriate metadata, and absence of accidental comments, draft tokens, or confidential working notes.

Verify QR codes by decoding them and confirming their destination. Printed contact blocks need readable destinations, not just clickable labels. For native Google files, read back authorized changes and confirm structure/content. Text presence or `/MarkInfo` alone cannot certify reading order or accessibility.

## PDF structural preflight

Use a `python3` that has `pypdf` installed, and absolute paths. Replace the runtime and file paths in this argument example with discovered values:

```text
<python3> <skill-directory>/scripts/pdf_preflight.py <final.pdf> --pages 6 --size-mm 210 297 --text-policy required --required-text "Credo" --out <working-directory>/preflight.json
```

- `--size-mm W H`: effective displayed CropBox dimensions after rotation and UserUnit; tolerance is configurable.
- `--trim-mm W H`: final TrimBox dimensions. Bleed-inclusive media need not equal trim.
- `--bleed-mm N`: geometric margin of BleedBox around TrimBox; it does not inspect the artwork extending into bleed.
- `--text-policy required`: missing nonblank extracted page text is an error. Use `warn` for legitimate image-only pages and inspect those; default is `warn`.
- `--required-text`: checks expected phrases in whitespace-normalized document text. This is coverage, not truth or layout verification.
- Known draft tokens and `--forbid-text` matches are errors. Use `--allow-draft` only for deliberately unfinished work.
- Review token findings in context: an explanatory document can intentionally discuss a token. For such a document, permit these literal matches only after inspection and use specific forbidden-text checks for its actual unfinished fields.
- `--max-mb`: file-size warning; there is no universal email cap for all channels.
- URI annotations are reported without visiting destinations. Verify working links/contact destinations separately when relevant.

Exit 0 means no structural errors; 1 means defects or an unreadable PDF; 2 means invalid options or a missing dependency. Warnings and limitations still apply at exit 0. The JSON is a working record, not normally a customer deliverable.

The helper cannot establish claim accuracy, visual quality, full accessibility, embedded fonts, image DPI, color/output conformance, working links, or final printer acceptance. Use visual inspection and the appropriate authoring/production tools for those requirements.

## Release judgment

Fix material defects before final delivery. For a requested draft, retain only needed, visible unresolved fields and identify missing inputs. Complete authorized final exports without routine confirmation. Sending, sharing, publishing, or connected-service edits follow actual user authorization and tool permissions.

Deliver requested formats with concise consequential changes and concrete remaining limits. Keep intermediate renders, test fixtures, build code, and internal evidence records out of the handoff unless requested.
