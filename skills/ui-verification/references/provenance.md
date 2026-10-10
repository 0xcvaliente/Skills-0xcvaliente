# Provenance

Original source: [mblode/agent-skills](https://github.com/mblode/agent-skills/tree/5a781a88ed60c1033767b6b6a966887cd93dd912/skills/ui-verification),
reviewed 2026-10-09 at `5a781a88ed60c1033767b6b6a966887cd93dd912`. The upstream MIT [license](../LICENSE.md)
is retained. This is a selective Codex adaptation, not a complete upstream mirror.

Preserved the installed specialist routing, local reference files, and existing
accessibility checks. Reviewed newer source guidance for product claims, repeated
content, working destinations, meaningful alternatives, reduced motion in
JavaScript, and the limits of browser accessibility checks. Integrated only the
applicable guidance, with evidence requirements and project conventions intact.

## Claude Code port

Ported from the Codex version on 2026-10-10. Driver guidance lists the browser tooling Claude Code may expose (Playwright through Bash or an MCP server, Claude in Chrome, a Chrome DevTools MCP server, the desktop app's browser pane) without assuming any of them exists, and the README's install and usage sections target `~/.claude/skills/ui-verification/` and `/ui-verification`. Probes and the evidence contract are unchanged.
