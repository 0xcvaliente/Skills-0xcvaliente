# Focused module / architecture note template

Copy only sections useful to the task. Replace placeholders with verified facts;
do not create fictional packages, data flows, decisions or test results.

```markdown
# <Module or system>

Status: <partly verified / verified for the scope below / needs review>
Scope: <repository-relative paths>
Evidence reviewed at: <commit hash; say if working tree was dirty>

## Responsibility and boundaries
<What this module owns, and what it must not do.>

## Important paths and symbols
| Path / symbol | Responsibility |
|---|---|
| <real path: symbol> | <verified role> |

## Relationships / invariants
<Only relationships actually traced through source or authoritative docs.>
<Include shared config, schema and public contracts that affect this module.>

## Validation
<Command actually run, outcome and relevant test path. Or: not run.>

## Unknowns / active risks
<Unverified behavior, omitted dependencies, or unresolved work.>
```

Use the helper's `review` command only after reviewing these claims. Its hashes
check evidence changes, not semantic correctness. Include shared configuration
as evidence and directories where additions could invalidate the note as scopes.
Keep facts in the note and machine fingerprints in the ignored `.local/` cache.
