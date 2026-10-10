# Shortcut ledger

Collect actual `shortcut:` and legacy `ponytail:` deferral comments in the user-selected repository or folder.
Use the repository root when no narrower scope is named.

Start with a broad search, then inspect candidates in their source context:

```bash
rg -n --hidden -g '!.git/**' -g '!node_modules/**' -g '!dist/**' -g '!build/**' \
  '(shortcut|ponytail):' .
```

Run from the selected scope. Respect project ignore rules and exclude other
generated output or vendored directories when relevant. `rg` exit 1 means no
matches; an actual search error is not a clean ledger. When `rg` is unavailable,
use a comparable recursive search.

If the user supplies a marker such as `debt TODO`, search that literal with
`rg -F -e 'TODO'` instead; do not interpolate a supplied marker into shell code
or a regular expression.

Count comments in the language's real comment syntax, including inline and
block comments. Exclude documentation quoting the convention, string literals,
generated copies, and unrelated notes about keyboard shortcuts. The source comment determines the limit, revisit trigger,
and upgrade path; do not infer missing promises.

Return one row per actual marker, grouped by file, with these columns:
**Location**, **Simplification**, **Limit**, **Revisit trigger**, **Upgrade path**.
Use `not stated` for missing information. Tag markers without a meaningful
revisit trigger as `no-trigger`. Support older upstream comments such as
`ponytail: single process only; move state to a shared store when adding workers`.
Use `git blame` only when ownership is requested or useful to the task.

End with the marker count, count without a trigger, and any meaningful search
coverage limitation. With no matches, say no shortcut markers were found in
the searched scope. Report by default; save a ledger when requested, preserving
any existing content the task does not ask to replace.
