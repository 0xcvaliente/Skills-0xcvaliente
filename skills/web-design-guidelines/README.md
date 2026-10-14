# Web Design Guidelines

`web-design-guidelines` provides a local checklist and workflow for interfaces that remain understandable and usable across input methods, viewport sizes, content lengths, themes, locales, and loading or failure states.

It covers accessibility and interaction quality as part of design and implementation. The guidance adapts to the product's existing tokens, components, language, and browser requirements instead of automatically imposing a new aesthetic.

## When to use it

Use it when building UI, polishing a flow, or conducting a file-level interface audit. Typical questions include whether forms provide usable errors, navigation works by keyboard, text survives long content, mobile layouts remain operable, or motion respects user preferences.

For new visual identity or substantial aesthetic direction, the entrypoint calls for [Frontend Design](../frontend-design/README.md) as well. [UI Design](../ui-design/README.md) offers a larger mode-based construction and audit system.

## How it works

Inspect the existing design system, typography, component conventions, accessibility utilities, browser support, and framework version. Load the detailed checklist and apply the relevant parts to the surface in scope.

For construction, establish semantic structure, keyboard behavior, focus, important states, and robust layout before visual polish. Reuse existing accessible primitives where possible and verify representative narrow, ordinary, and wide viewports.

For review, prioritize blocked access and focus failures, destructive or misleading interactions, broken responsive and asynchronous states, rendering or performance problems, and then visual and copy refinements. Findings use exact file and line locations where available, with a focused correction.

The skill is fully local: it does not fetch replacement rules from a remote branch during use. Product preferences and measurement-dependent recommendations should be presented with their actual context.

## Requirements and output

There are no bundled scanners or executable helpers. The workflow needs access to the target code and uses the project's existing tests and linting. A browser helps verify rendered behavior, keyboard navigation, zoom, reduced motion, narrow layouts, long content, form errors, and themes.

Implementation requests produce changed UI and validation. Dedicated audits produce findings grouped by relevant file. A static check alone does not establish that every rendered state is usable; [UI Verification](../ui-verification/README.md) can supply runtime evidence.

## Example requests

```text
Use the web-design-guidelines skill: audit this form for keyboard access,
error recovery, mobile layout, and long translated labels.

Use the web-design-guidelines skill: implement this navigation using our
existing primitives and verify focus and responsive behavior.
```

## Package guide

- [SKILL.md](SKILL.md): context, construction, review priorities, and verification.
- [references/guidelines.md](references/guidelines.md): detailed local checklist.
- [references/LICENSE.txt](references/LICENSE.txt): reference licensing.

Install by copying this directory into any [Agent Skills](https://agentskills.io)-compatible location, for example `cp -R web-design-guidelines ~/.agents/skills/` (see [INSTALL.md](../../INSTALL.md) for each host's folder). Compatible agents select it automatically when a request matches its description, or you can name it explicitly ("use the web-design-guidelines skill").

## Design collection integration — 2026-10-08

Preserves the fully local checklist and adds focused component, mobile, fixture, motion, and dependency-selection companions. No remote rules are fetched or substituted during a review.

The companion collection adapts all 15 skills from [Emil Kowalski](https://github.com/emilkowalski/skills), 14 of them reviewed at `e8a175de22ae1e49370fc144c1f3bb9aeedf988d`, plus `animation-performance` at `2d228630ba1446365f614a108cb8252f1feda202`. Each adapted package includes its original guide, supporting resources, source checksums, Agent notes, and MIT license. Start with [Emil Design Engineering](../emil-design-eng/README.md) or [Animate](../animate/README.md), then select the specific workflow needed.

The integration changes instructions and routing; it does not install UI libraries, launch an app, or establish device/browser verification by itself. Existing source guides, helpers, probes, fixtures, and evaluation scenarios remain available.
