# docs: documents written to be read, shared, and commented on

Use this for reports, proposals, memos, specs, decision records, one-pagers, meeting notes, handbooks, and similar writing. The format comes second: decide who reads it and what they must do afterwards, then pick the container.

## Decide first

Ask (or infer from the request, then confirm in one line):

1. **Reader and decision.** Who reads it, and what should they know, decide, or do afterwards?
2. **Status.** Draft for comment, final for decision, or reference? This sets how much structure and polish it needs.
3. **Where it lives.** A hosted doc the team edits together, a file they revise (`.docx`), or a fixed copy (`.pdf`)?
4. **Template or house style.** If the user has a template, headings, or prior example, use it. Read it before writing.

## Pick the container

| Situation | Write as | Then |
|---|---|---|
| Others will edit and comment in a hosted tool (Google Docs, Notion, SharePoint) | The hosted doc, if a connector or MCP server for it is available | Read existing content freely; create or change shared docs only on request and show the content first |
| Others will revise it and you cannot reach their tool | Markdown source, built to `.docx` | Use `../word/GUIDE.md` |
| Final copy to send, attach, or print | Markdown or `.docx`, exported to `.pdf` | Use `../pdf/GUIDE.md`; run `scripts/render.py` and look at the pages |
| Lives in a repository next to code | Markdown | Keep headings stable so links do not break |
| Quick answer or comparison for the chat only | Do not make a file | Answer in the conversation |

Keep one source of truth. Write the Markdown (or the hosted doc) first and export from it; do not maintain parallel versions by hand.

## Structure for a reader

Front-load. A reader should get the point in the first screen and be able to stop there.

1. **Title** that names the subject and the kind of document ("Q4 hiring plan: proposal").
2. **Header block:** owner, date, status (draft/final), audience, and the decision or feedback needed by when.
3. **Summary** (3-5 lines): the conclusion, the recommendation or ask, and the key number or risk. Written last.
4. **Context:** only what this reader lacks. Link to background instead of retelling it.
5. **Body:** headings that state the claim ("Churn rose because onboarding takes 9 days"), not the topic ("Churn"). One idea per section. Put evidence directly under the claim.
6. **Options and trade-offs** when a decision is requested: each option, its cost, its risk, and your recommendation.
7. **Next steps:** owner, action, date.
8. **Appendix:** data, long tables, methods, glossary. Nothing the reader must read to follow the argument.

Style rules that earn their keep:

- Short paragraphs; one point each. Lists for parallel items, tables for comparisons across the same attributes, prose for reasoning.
- Define a term at first use, then keep using that exact term. Do not rotate synonyms for one concept.
- Numbers carry units, dates carry year and time zone when ambiguous, and every statistic has a source or "estimate".
- Say who does what. Prefer "Priya sends the contract by 14 March" to "the contract will be sent".
- Cut: throat-clearing openings, repeated summaries, hedges that change no decision.

Templates for common types are in `templates/` (memo, proposal, spec, decision record, report, meeting notes). Copy one, delete sections that do not apply, and keep the order.

## Write it

1. Gather what exists: the request, source files, prior versions, data. Read them; do not rely on memory of them. For long inputs, take notes of facts with their source.
2. Outline the headings as claims. Show the outline to the user when the document is large or the audience is senior, and wait for a yes before filling it in.
3. Draft section by section. Mark anything you could not confirm with `[confirm: ...]` rather than guessing a figure, quote, name, or date.
4. Write the summary last, then check it against the body.
5. Read it as the reader would: first the title and summary only, then the headings alone. If the argument is unclear from the headings, rewrite them.

For a larger collaboration with the user, follow the staged process in [coauthoring.md](coauthoring.md): gather context, build sections by iteration, then test with a cold reader.

## Review and comments

When asked to review, comment on, or proof someone's document, do not rewrite it silently. Produce comments the author can act on, anchored to the text, and offer edits as suggestions. See [review-and-comments.md](review-and-comments.md) for the comment format, severity levels, and how to place real comments or tracked changes in a `.docx`.

## Export and convert

[export.md](export.md) has recipes for Markdown to `.docx`/`.pdf` (pandoc or LibreOffice), HTML to PDF, applying a reference style, and checks after export (headings kept, tables intact, links live, fonts).

## Before it leaves your hands

Run through this and report anything that fails:

- [ ] The summary matches the body; numbers agree everywhere they appear.
- [ ] Every claim that needs a source has one; every `[confirm: ...]` is resolved or listed for the user.
- [ ] Names, titles, dates, and amounts spelled and formatted consistently.
- [ ] Headings form a real outline (styles, not bold text), so navigation panes and tables of contents work.
- [ ] Links open; images have alt text; tables have a header row.
- [ ] Metadata and leftovers are intentional: author, comments, tracked changes, hidden text, revision history (`scripts/inspect_office.py FILE` for `.docx`).
- [ ] Nothing confidential was pulled in that this audience should not see.
- [ ] File named for what it is and when: `2026-03-hiring-plan-proposal-v2.docx`.

## Sharing

Sharing is the user's decision. Preparing a file, a draft email, or a post is fine; sending, uploading to a shared drive, changing sharing permissions, or inviting people is done only when explicitly asked, after showing exactly what will be sent and to whom.
