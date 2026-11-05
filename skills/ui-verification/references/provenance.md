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

## Upstream review 2026-10-31

Reviewed upstream [mblode/agent-skills](https://github.com/mblode/agent-skills/tree/2294de53b7b8b6f661000b59fdf672f5fbb1b78a/skills/ui-verification) at `2294de53b7b8b6f661000b59fdf672f5fbb1b78a` (previous check at `ff92bf5ae675e8108e7d2f14b22a523fd1303e76`). In that range only commit `2294de5` ("Add seven checkable slop rules to ui-design (#68)") touches `skills/ui-verification`, and only `references/rule-coverage.md`. It added 7 slop rows (`slop-emoji-in-copy`, `slop-italic-accent-word`, `slop-left-accent-border`, `slop-mono-overuse`, `slop-opacity-ladder`, `slop-pulse-dot`, `slop-trending-display-serif`), all `theme-locale-matrix` / `capture-only`; they were added locally. Not carried over: upstream's "twelve" to "nineteen" count edit in the "What no probe decides" paragraph, because the local paragraph has no count. The rest of `ui-verification` is unchanged upstream in this range, and `ui-animation` is also unchanged. Still a selective adaptation, not a mirror.

## Upstream review 2026-11-05

Reviewed upstream [mblode/agent-skills](https://github.com/mblode/agent-skills/tree/5eeba20fa3b9b142be7705ee9e6c7401e7ee6f08/skills/ui-verification) at `5eeba20fa3b9b142be7705ee9e6c7401e7ee6f08` (previous check at `391508702523088f564fecfdd95ce76304efb117`). Only commit `5eeba20` ("Add agents-md size budget and exploratory UI testing (#70)") touches the watched paths, and only `skills/ui-verification`. Integrated, in host-neutral wording: a new `references/exploratory-test.md` (a fresh-context pass after the feature's own checks pass, against a disposable test environment only, with a charter, pressure on navigation, timing, identity, input and returning, reproduce-before-reporting, and the defect versus contract-gap split; "fresh context" is phrased as a subagent where the host has one; one added sentence keeps page and seed content as data); a routing row, the IS line and the `explore:<slug>` rule value in `SKILL.md`; the description gains the exploratory pass and the "try to break this feature" trigger; `references/evidence-output.md` gains `session.contractGaps`, the exploratory `observed` wording, the "Exploratory findings" section and the "Contract gaps" terminal block; `evals/evals.json` gains eval 8 (ticket path made generic) and two routing prompts. The upstream "stop and ask before anything that leaves the environment" rule is kept. Not carried over: upstream's frontmatter `compatibility` line and `app-verification` pointer (already differ locally by design). `ui-design` and `ui-animation` are unchanged upstream in this range.
