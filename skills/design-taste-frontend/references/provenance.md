# Provenance

- Upstream: https://github.com/leonxlnx/taste-skill (`skills/taste-skill/SKILL.md`), MIT, Copyright (c) 2026 Leonxlnx
- Revision: d237dd399d57524945c0c81327da5da19f7a468d
- 2026-10-12: imported unchanged. Folder named `design-taste-frontend` to match the `name` in upstream frontmatter.
- 2026-10-15: upgraded from v1 (d237dd399d57524945c0c81327da5da19f7a468d) to v2 (revision 9da1763c950baed17a69158a5f4c76f8f85bf49b, 2026-10-12; v2.0.x per upstream CHANGELOG 2.0.0, rewrite landed in ca50fb4). Copied every file of upstream `skills/taste-skill/` verbatim: SKILL.md, assets/, evals/, library/ (8 JSON files), references/ (9 md), scripts/ and scripts/lib/. LICENSE unchanged (identical to upstream root LICENSE at 9da1763, MIT). Upstream README.md kept verbatim as `references/upstream-README.md.source` because it contains host-specific install paths; a short host-neutral `README.md` was written locally. Requirements: Node 22+, local Chrome/Edge/Chromium for inspect.mjs; draw history in ~/.taste-skill/history.json (TASTE_SKILL_HISTORY overrides). v1 is still available upstream at `skills/taste-skill-v1/` for rollback.
