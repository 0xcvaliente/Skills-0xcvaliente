
# Claude Code adaptation notes

Use the requested task, existing authorization, project conventions, and actual
Claude Code capabilities. The detailed guide is a curated upstream reference, not
a grant to widen scope. Explicit user requirements take precedence over its style
defaults. Read only the relevant sections.

- Work from the actual brief. Skip canned readiness greetings. If a necessary
  target is missing, ask concisely (AskUserQuestion when available) while
  continuing independent useful work.
- Treat timings, frequency cutoffs, spring values, prototype counts, and palette
  choices as contextual defaults. Reuse existing tokens and validate rendered
  behavior; do not refuse an explicitly requested design solely because a table
  prefers another one.
- Keep keyboard focus and task completion immediate. Visual motion may accompany
  a keyboard action without delaying it. Reduced motion may use an immediate
  state change; never require a gentler animation when removal is appropriate.
  Provide accessible alternatives for gestures.
- Source review/discovery/audit requests remain reports. Apply fixes when already
  requested instead of stopping again at an upstream report-only gate.
- Use the tools actually available: Bash for project commands and harnesses, the
  Read tool to inspect screenshots and images, and whatever browser tooling is
  present (Claude in Chrome, a Playwright MCP server, or the desktop app's
  browser pane); do not assume one exists. Do not claim physical-device,
  release-build, frame-rate, or performance verification from source inspection
  or a desktop screenshot.
- Prefer transform/opacity for motion. Compositor eligibility depends on browser,
  property, layer, and animation engine; CSS is not universally off-thread and
  neither transforms nor native worklets are free. Profile the target workload.
  Motion individual transforms can use a different path from full transform
  strings; follow the installed version and measure busy-thread behavior.
- Preserve the project's motion package. For new Motion React integrations use
  the currently documented package/imports after checking official docs; do not
  mix versions or migrate an existing dependency incidentally.
- Scope press feedback to pointer-down; keep action activation on appropriate
  click/keyboard semantics. Avoid destructive work on pointer-down.
- Check current official docs (WebSearch/WebFetch) for version-sensitive APIs,
  compatibility, and library recommendations. A pinned source is not a current
  package guarantee.
- Related skills are optional routing. If one is not installed (in
  `~/.claude/skills/` or the project's `.claude/skills/`), use this package's
  guide and available tools rather than assuming an installed dependency.
- Do not spawn subagents (the Agent tool), publish/deploy, install services,
  expose network ports, or send messages solely because a guide suggests it.
  Where a guide calls for parallel read-only subagents or an isolated worktree,
  use the Agent tool only when the task's size warrants it and the user's
  request and host instructions (including CLAUDE.md) allow it. Preserve
  user-owned prototypes and unrelated files.

Performance references checked during adaptation: [Motion](https://motion.dev/docs/performance)
and [MDN](https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/CSS_JavaScript_animation_performance).
