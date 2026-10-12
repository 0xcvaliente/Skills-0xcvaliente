# Provenance

Original source: [mblode/agent-skills](https://github.com/mblode/agent-skills/tree/5a781a88ed60c1033767b6b6a966887cd93dd912/skills/ui-design),
reviewed 2026-10-09 at `5a781a88ed60c1033767b6b6a966887cd93dd912`. The upstream MIT [license](../LICENSE.md)
is retained. This is a selective Codex adaptation, not a complete upstream mirror.

Preserved the installed specialist routing, local reference files, and existing
accessibility checks. Reviewed newer source guidance for product claims, repeated
content, working destinations, meaningful alternatives, reduced motion in
JavaScript, and the limits of browser accessibility checks. Integrated only the
applicable guidance, with evidence requirements and project conventions intact.

## Claude Code port

Ported from the Codex version on 2026-10-10. Raster dark-mode variants and brand-board rendering no longer depend on the Codex `imagegen` skill: they use an image-generation tool when one is available and otherwise return a text-only asset list or prompt (the default in Claude Code). Agent-instruction pointers name `CLAUDE.md` first, and the README's install and usage sections target `~/.claude/skills/ui-design/` and `/ui-design`. Rules, modes, and the audit load contract are unchanged.

## Host-neutral adaptation

Made host-neutral for the Agent Skills standard on 2026-10-12. Tool names (AskUserQuestion, the Read tool) became capability wording (ask the user, file/image reading); image-generation fallbacks no longer assume a specific host; the design-system pointer prefers `AGENTS.md` and mentions host-specific instruction files only if the project already uses one; README install and examples are host-neutral. Rules, modes, and the audit load contract are unchanged.
