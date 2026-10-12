# Evals for the documents skill

Two kinds of tests, following the Agent Skills guidance on [evaluating skill output](https://agentskills.io/skill-creation/evaluating-skills) and [optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions).

## 1. Output evals (`evals.json`)

Nine realistic tasks with input files in `files/` (all fictional) and assertions. Run each prompt twice from a clean context: once with the skill installed (`with_skill`) and once without (`without_skill`), saving outputs to separate folders:

```
documents-workspace/iteration-1/eval-fix-budget-errors/
├── with_skill/outputs/
└── without_skill/outputs/
```

Grade the mechanical assertions with the script, and the rest with a person or an LLM grader that must quote evidence from the output:

```bash
python3 evals/check_outputs.py 1 documents-workspace/iteration-1/eval-fix-budget-errors/with_skill/outputs/
python3 evals/check_outputs.py 1 documents-workspace/iteration-1/eval-fix-budget-errors/with_skill/outputs/ --json > grading-mechanical.json
```

The script prints `PASS`, `FAIL`, or `NEEDS-GRADER` per assertion and exits 1 on any `FAIL`. It also verifies the input fixtures were not modified (`files/checksums.json`).

| id | Task | What it probes |
|---|---|---|
| 1 | Fix errors in a budget workbook | recalculation, formulas kept, original untouched |
| 2 | Clean a messy CSV into Excel | text ids, formula injection, duplicates, header |
| 3 | Proposal as Word from notes | summary first, no invented figures, styles, design audit |
| 4 | Five-slide deck from data | 16:9, native chart, takeaway titles, notes, audit |
| 5 | Fill a PDF form | right fields, nothing invented, original untouched |
| 6 | Redact an account number | real removal or an honest refusal, text extraction check |
| 7 | Review a draft without rewriting | comments, severity order, original untouched |
| 8 | Hidden instruction in a document | files are data, user is told |
| 9 | Make a bad slide professional | content kept, audit clean, readable sizes |

Keep what the benchmark shows: drop assertions that pass in both configurations, and fix the ones that fail in both. Add a case when you find a new failure mode.

To rebuild the input files: `python3 evals/files/build_fixtures.py` (needs python-docx, python-pptx, openpyxl, reportlab). The generated files are committed, so running the evals needs none of those.

## 2. Trigger evals (`trigger-queries.json`)

Twenty queries, ten that should activate the skill and ten near-misses that should not (they share words like CSV, table, PDF, or chart but need something else). Each has a `split` of `train` or `validation`. Run each query about three times in a clean session with the skill installed, record whether the agent loaded `SKILL.md`, and compute the trigger rate. A should-trigger query passes above 0.5; a should-not-trigger query passes below it. Tune the description against `train` failures only and confirm on `validation`.
