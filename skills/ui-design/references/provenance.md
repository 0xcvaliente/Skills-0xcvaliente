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

## Upstream review 2026-10-26

Checked mblode/agent-skills `193fa28cba62506457a815141f37b41396b0ad91` (previously reviewed at `81d0af2f6d4b32d791fb26caa82b17603ef4d807`). `ui-verification` and `ui-animation` have no upstream changes in that range. `ui-design` changed in two commits (`8d78f92`, `dc3f816`). Integrated: the rule that a design spec started from a client's assets records only what the client supplied and marks each gap "Not supplied" instead of filling it with defaults, added to the design-system paragraph in `SKILL.md`. Not carried over: the `npx` to `pnpm dlx` and `npm audit` to `pnpm audit` command swaps in `canonicalize-tailwind.md`, `componentize.md`, `defer-to-other-tools.md` and `output-adapters.md`, since this skill stays package-manager neutral.

## Upstream review 2026-10-31

Checked mblode/agent-skills `2294de53b7b8b6f661000b59fdf672f5fbb1b78a` (previously reviewed at `ff92bf5ae675e8108e7d2f14b22a523fd1303e76`). `ui-design` changed in two commits (`4d15fab`, `2294de5`). Integrated: the seven new `slop` rules (`slop-emoji-in-copy`, `slop-italic-accent-word`, `slop-left-accent-border`, `slop-mono-overuse`, `slop-opacity-ladder`, `slop-pulse-dot`, `slop-trending-display-serif`); in `rules/_sections.md`, the slop rule count (9 to 16), the total (55 to 62), and the sentence added to the slop description; in `direction/aesthetic-direction.md`, the Instrument Serif clause on the fashionable-font bullet, the repeated-section-shape sentence on the card-grids bullet, and the new bullets from "Uppercase, letter-spaced subtitles" through "Headings far larger than the content they head" plus "More text than the reader needs". Adapted: `related:` frontmatter trimmed to rule ids that exist locally, dropping `slop-slogan-headings` from `slop-emoji-in-copy` and `slop-italic-accent-word`, and `slop-eyebrow-overuse` from `slop-mono-overuse`. Not carried over: the upstream edit to the `01`, `02`, `03` bullet in `aesthetic-direction.md`, since this skill has no such bullet.
