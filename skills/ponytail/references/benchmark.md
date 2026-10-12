# Published benchmark context

Use only for `gain` or a question about Ponytail's measured impact. This skill
has no benchmark of its own and does not measure savings in the user's project.

The [pinned upstream report](https://github.com/DietrichGebert/ponytail/blob/9b58c1ffb790c075ca32e70a89cf1d80588f4abf/benchmarks/results/2026-10-07-agentic.md)
reports these Ponytail 5 results against the same agent without the skill:

| Metric | Publisher-reported change |
|---|---|
| Delivered lines of code | 53% fewer |
| Output tokens | 45% fewer |
| Cost | 26% lower |
| Time | 41% lower |

Attribute those figures explicitly to the upstream author's 2026-10-07 study:
39 tasks, five runs per task and arm, headless Claude Code with the report's
named Opus 5.5 model. The figures summarize geometric means of per-task median
ratios. They have not been independently reproduced for this adaptation.

A completeness check was added to the report on 2026-10-10: a blind model
judge (Opus 5.5) scored whether each run on the size-only tasks still delivered
the whole job. The author reports every judged run as complete in both arms
(100/100 without the skill, 105/105 with Ponytail 5), with runs killed at the
timeout excluded and one judge miss corrected by hand. Read this as "the shorter
output did not skip required work on those tasks", not as proof of quality; the
judge saw diffs rather than whole repositories and is itself a model.

The report disabled shell execution during generation. Only 18 of its 39 tasks
had hidden correctness/safety checks; the other tasks do not establish overall
quality. The report says the hidden-check results were similar across arms.
Do not present the headline savings as results for this adaptation (the study
ran on Claude Code but measured the upstream package, not this port), a quality
guarantee, or a prediction of the user's bill.

If asked for current figures, inspect the current upstream report and state
its date and environment. If it cannot be read, retain the pinned label. For
project-specific evidence, offer a counted shortcut ledger or a scoped audit.
An observed diff can show changed lines; code that was never written supplies
no measurable counterfactual savings.
