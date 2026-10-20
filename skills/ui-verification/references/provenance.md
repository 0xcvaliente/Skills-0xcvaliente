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

## Host-neutral adaptation

Made host-neutral for the Agent Skills standard on 2026-10-12. Browser-driver wording (Bash, Claude in Chrome, the desktop app's browser pane) became capability wording; the instruction-file reference lists `AGENTS.md` first; README install and example are host-neutral. Probes and evidence rules are unchanged.

## Upstream review: 81d0af2 (2026-10-20)

Reviewed upstream [mblode/agent-skills](https://github.com/mblode/agent-skills/tree/81d0af2f6d4b32d791fb26caa82b17603ef4d807/skills/ui-verification) at `81d0af2f6d4b32d791fb26caa82b17603ef4d807` (new revision since `5a781a88ed60c1033767b6b6a966887cd93dd912`; upstream commit "Strengthen visual and flow verification evidence (#65)"). Still a selective adaptation, not a mirror. Integrated: a new `references/visual-review.md` (matched before/after capture conditions, inspecting the actual images, masks recorded as untested, duplicate-frame investigation with state preconditions), reworded in host-neutral capability vocabulary; routing rows and a pointer in `SKILL.md`; the sharper "screenshot is evidence, not a verdict" rule; the IS NOT line narrowed from pixel-diff regression to persistent pixel-baseline approval workflows; description gains the "review before and after screenshots" trigger; evals 5-7, two routing prompts, and the `evals/files/onboarding.html` and `billing.html` fixtures. Not carried over: upstream's frontmatter `compatibility` line and `app-verification` pointer (already differ locally by design) and its note naming a user-supplied bundle as the guidance source. `ui-design` and `ui-animation` upstream paths have no changes between `5a781a8` and `81d0af2`, so nothing was appended there. Probes and the evidence contract are unchanged.
