# UI Verification

`ui-verification` runs scoped browser probes to determine what an interface actually does. It measures focus, hit targets, overflow, failure states, themes, request errors, layout shift, and performance attribution, then connects that evidence to interface findings.

Its value is confirming or rejecting source-level predictions. A small visible control may have a larger effective hit area, and a retry button may render correctly while failing to perform its action. Those questions require exercising the page.

## When to use it

Use it to reproduce an audit finding, verify a fix, inspect a route in a running app, check documented design-token values, or capture a viewport and theme matrix. When handed rule identifiers from [UI Design](../ui-design/README.md), it selects only the probes that cover those questions.

This skill owns the browser session and measurements. UI Design owns source audits, severity assignments, and the overall readiness verdict. UI Verification does not independently claim that a product is ready to ship.

## Probe catalog

| Probe | What it checks |
|---|---|
| [Accessibility scan](probes/axe-scan.md) | axe-core violations, accessible names, landmarks, and computed contrast. |
| [Target size](probes/target-size.md) | Element bounds and effective hit areas. |
| [Focus walk](probes/focus-walk.md) | Keyboard traversal, visible focus, dialog trapping, and restoration. |
| [Layout shift](probes/layout-shift.md) | Attributed shifts while controlling a data response. |
| [Viewport stress](probes/viewport-stress.md) | Narrow layouts, overflow, clipping, and expanded strings. |
| [Failure injection](probes/failure-injection.md) | Server errors, empty or malformed responses, and unresolved loading. |
| [Theme and locale matrix](probes/theme-locale-matrix.md) | Captures across width, theme, pseudo-locale, and direction. |
| [Console and network](probes/console-network.md) | Runtime errors, failed requests, and hydration warnings. |
| [Web vitals](probes/web-vitals.md) | Lab measurements and attribution for LCP, CLS, and scripted interaction timing. |

## How it works

First establish the driver, build mode, base URL, authentication, data, and reachable routes. Playwright is the preferred driver when supported; the references also describe a DevTools route. Some probes require interception capabilities and cannot run under every driver.

Capture artifacts before interpreting them. Each finding receives `reproduced`, `not-reproduced`, or `unknown`, with conditions and evidence. After a fix, repeat the identical probe and preserve the before and after artifacts. A skipped probe is recorded as a coverage gap.

Performance and layout-shift probes use a production build so development compilation does not dominate the numbers. A theme check must drive and verify the app's actual theme mechanism.

## Requirements and output

The app must be reachable, with a usable browser driver and any necessary authenticated session or seeded data. The bundled JavaScript recipes use the Playwright page API; they are documentation to apply, not an installed test runner.

Outputs include session metadata, measurements keyed to rule IDs, screenshots or JSON artifacts, clearing re-runs, and explicit skipped checks. Lab measurements do not establish field performance; that requires RUM or CrUX data.

## Example request

```text
Use the ui-verification skill: reproduce the focus and hit-target findings on
this route, then rerun the same probes after the fixes.
```

## Package guide

- [SKILL.md](SKILL.md): probe selection, session workflow, and evidence rules.
- [probes/](probes/): nine probe recipes.
- [references/](references/): session setup, rule coverage, and evidence output.
- [evals/evals.json](evals/evals.json): maintenance scenarios.

Install by copying this directory into any [Agent Skills](https://agentskills.io)-compatible location, for example `cp -R ui-verification ~/.agents/skills/` (see [INSTALL.md](../../INSTALL.md) for each host's folder). Compatible agents select it automatically when a request matches its description, or you can name it explicitly ("use the ui-verification skill").

## Design collection integration — 2026-10-08

Preserves every browser probe and the reproduced / not-reproduced / unknown evidence contract. `break-ui` can supply realistic fixtures and `mobile-native` can identify device scenarios. Browser emulation is reported separately from physical-device verification. Runtime requirements now live in the body rather than an unsupported frontmatter field.

The companion collection adapts all 15 skills from [Emil Kowalski](https://github.com/emilkowalski/skills), 14 of them reviewed at `e8a175de22ae1e49370fc144c1f3bb9aeedf988d`, plus `animation-performance` at `2d228630ba1446365f614a108cb8252f1feda202`. Each adapted package includes its original guide, supporting resources, source checksums, Agent notes, and MIT license. Start with [Emil Design Engineering](../emil-design-eng/README.md) or [Animate](../animate/README.md), then select the specific workflow needed.

The integration changes instructions and routing; it does not install UI libraries, launch an app, or establish device/browser verification by itself. Existing source guides, helpers, probes, fixtures, and evaluation scenarios remain available.
