# Provenance

- Upstream: https://github.com/supabase/agent-skills (`skills/supabase-postgres-best-practices`), MIT, Copyright (c) 2026 Supabase
- Revision: c9be0e931b7930f7d02126d04774d904c381e7d7 (c9be0e9), 2026-10-02
- Version: 1.1.1 (`metadata.version` in SKILL.md)
- 2026-11-03: imported.
  - Taken verbatim from upstream: `SKILL.md` and every file under `references/` (31 rule files plus `_sections.md`, `_template.md`, `_contributing.md`). `LICENSE` is the upstream repository root MIT license.
  - Left out, and why:
    - `CHANGELOG.md`: upstream release notes; the version is recorded here.
    - `.claude-plugin/marketplace.json`, `.mcp.json`, repository tooling, `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `README.md`: plugin manifest and maintenance material, not part of an Agent Skills package.
  - Sibling: `supabase` (same upstream) covers Supabase products, CLI, MCP and debugging; this skill covers general Postgres schema, SQL, RLS and performance.
