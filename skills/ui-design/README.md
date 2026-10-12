# UI Design

`ui-design` chooses visual direction, implements interfaces, records existing design systems, and audits built React, Next.js, and Tailwind surfaces for user-facing defects. It combines practical construction guidance with a separate rule-based audit process.

The skill resolves the kind of work before acting. Building a new page, inspecting an existing page, and adding dark mode require different references and produce different results. This separation helps preserve an established interface during a focused repair or review.

## When to use it

Use it to create a landing page or dashboard, extract tokens and component conventions, add dark mode, improve responsive layout, componentize a page, or investigate interface defects. It also handles requests to simplify generic decoration or unsupported visual proof.

## Operating modes

| Mode | Purpose | Typical result |
|---|---|---|
| Direction | Choose a visual system for the requested surface. | Thesis, palette, type scale, spacing, shape, and layout decisions. |
| Extract | Record design decisions already present in a codebase. | Evidence-based `design-system.md` with tokens, components, conventions, and exceptions. |
| Build | Implement a new surface. | Working UI using existing project patterns. |
| Audit | Investigate defects in an existing surface. | Confirmed findings, scoped fixes when requested, and a readiness verdict. |
| Options | Build meaningfully different variants for comparison. | Working alternatives that differ on a named design axis. |
| Scaffold | Derive semantic markup from a visual source. | Unstyled structure. |
| Retrofit | Add a specific dimension such as responsive layout or dark mode. | Focused changes to existing UI. |
| Componentize | Extract components or clean up Tailwind classes. | Reusable components and simpler styling structure. |

## How it works

The workflow reads the project's existing brand or design documentation and checks it against implemented tokens. Direction distinguishes product interfaces from marketing surfaces. Build loads applicable construction guidance and uses the current framework, assets, and components.

Audit instead loads feature playbooks and individual rules. Findings need exact source evidence; rules that depend on rendered behavior require a browser measurement. A verdict question produces a report, while an explicit request to fix or simplify permits scoped edits. Fixes outside the audited files are proposed rather than silently applied.

The audit has documented severity and output schemas, including a stable `ui-audit-ignore:` suppression convention. Its refinement hierarchy prefers deleting unsupported decoration, reducing complexity, and reconciling token drift before restyling.

## Requirements and output

The package has no application runtime or component library. Implementation uses the target project's React, Next.js, or Tailwind environment. Browser access is needed for rendered claims, state exercises, and visual captures.

[UI Verification](../ui-verification/README.md) owns measurement and evidence collection. [UI Animation](../ui-animation/README.md) owns timing and gestures. References to `product-design`, `tidy`, `ax-audit`, `typography-audit`, `ghostwriter`, and `seo` concern external skills that are not bundled here. Raster dark-mode variants and brand boards use an image-generation tool when one is available; if the host has none, they produce a text-only list of the needed assets or the board prompt, and no image is generated.

## Example requests

```text
Use the ui-design skill: extract our existing tokens and components into a
design-system.md, checking representative values in the browser.

Use the ui-design skill: audit and fix this settings page within the named files;
verify its form errors, mobile layout, focus, and theme behavior.
```

## Package guide

- [SKILL.md](SKILL.md): mode selection, quality bar, audit boundaries, and verification.
- [direction/](direction/): product and marketing direction, layout planning, and conversion guidance.
- [design-guidelines.md](design-guidelines.md) and [guidelines/](guidelines/): build guidance by UI topic.
- [rules/](rules/): individual source and rendered audit checks.
- [references/](references/): extraction, feature playbooks, severity, states, evidence adapters, and readiness.
- Root-level guides such as [add-dark-mode.md](add-dark-mode.md), [make-responsive.md](make-responsive.md), and [componentize.md](componentize.md): focused transformation workflows.
- [evals/](evals/) and [evaluations/](evaluations/): maintenance scenarios and fixtures.

Install by copying this directory into any [Agent Skills](https://agentskills.io)-compatible location, for example `cp -R ui-design ~/.agents/skills/` (see [INSTALL.md](../../INSTALL.md) for each host's folder). Compatible agents select it automatically when a request matches its description, or you can name it explicitly ("use the ui-design skill").

## Design collection integration — 2026-10-08

Preserves Direction, Extract, Build, Audit, Options, Scaffold, Retrofit, and Componentize modes. The Audit load contract and local rule corpus remain in place. Focused companion workflows cover component craft, working variant pickers, platform behavior, edge-case fixtures, and library decisions.

The companion collection adapts all 14 skills from [Emil Kowalski](https://github.com/emilkowalski/skills), reviewed at `e8a175de22ae1e49370fc144c1f3bb9aeedf988d`. Each adapted package includes its original guide, supporting resources, source checksums, Agent notes, and MIT license. Start with [Emil Design Engineering](../emil-design-eng/README.md) or [Animate](../animate/README.md), then select the specific workflow needed.

The integration changes instructions and routing; it does not install UI libraries, launch an app, or establish device/browser verification by itself. Existing source guides, helpers, probes, fixtures, and evaluation scenarios remain available.
