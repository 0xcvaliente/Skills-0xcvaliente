# Provenance

- Upstream: https://github.com/supabase/agent-skills (`skills/supabase`), MIT, Copyright (c) 2026 Supabase
- Revision: c9be0e931b7930f7d02126d04774d904c381e7d7 (c9be0e9), 2026-10-02
- Version: 0.1.2 (`metadata.version` in SKILL.md; the upstream `CHANGELOG.md` at this revision lists 0.1.9, so the frontmatter value lags the release notes)
- 2026-11-03: imported.
  - Taken verbatim from upstream: `SKILL.md`, `references/skill-feedback.md`, `assets/feedback-issue-template.md`. `LICENSE` is the upstream repository root MIT license.
  - Left out, and why:
    - `CHANGELOG.md`: upstream release notes; the version is recorded here.
    - `.claude-plugin/marketplace.json`: plugin marketplace manifest for one host.
    - `.mcp.json`: example MCP server config (`https://mcp.supabase.com/mcp?features=docs`); not part of an Agent Skills package. `SKILL.md` describes the MCP setup itself.
    - Repository tooling (`.github/`, `scripts/`, `test/`, `package.json`, release-please files), `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `README.md`: upstream maintenance material.
  - Behavior to know: `references/skill-feedback.md` can file a GitHub issue on `supabase/agent-skills`, but it asks the user's permission first and the user approves the content. Keep it that way.
