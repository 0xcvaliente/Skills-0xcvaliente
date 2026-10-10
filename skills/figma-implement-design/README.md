# Figma Implement Design

`figma-implement-design` is a structured workflow for converting a specific Figma design into application code with close visual fidelity. It combines design retrieval, screenshot comparison, real assets, component reuse, token mapping, and final interaction checks.

Its aim is a design that belongs in the existing application. Figma's generated code is adapted to the project's conventions rather than copied wholesale into a competing styling or component system.

## When to use it

Use it to implement a Figma component, screen, dashboard, or page from a frame link or node identifier. With the desktop MCP server, the workflow can use a selected node in the open Figma file; remote workflows require a link identifying the target frame or layer.

[Figma](../figma/README.md) covers the shared integration and troubleshooting rules. [Figma Create Design System Rules](../figma-create-design-system-rules/README.md) records repository conventions for repeated implementation work.

## How it works

1. Identify the design node from its link or supported desktop selection.
2. Fetch structured context for layout, typography, color, variants, and spacing. For a large result, use metadata to narrow the request to specific nodes.
3. Capture a screenshot of the same target as the visual reference.
4. Use assets returned by the server rather than unrelated replacements.
5. Reuse project components and map the design into the existing framework and token system.
6. Refine spacing and sizing while respecting accessibility and application conventions.
7. Compare layout, typography, colors, states, responsive behavior, and asset rendering against the source design.

The workflow calls for documenting necessary deviations. When an existing component already fulfills the role, extending its variant is preferable to creating a near-duplicate.

## Requirements and output

The skill requires access to a Figma MCP server, the target design, and the application repository. A runnable app and browser inspection are needed to substantiate claims about rendered fidelity and interaction behavior.

The output is integrated UI code, any necessary component documentation, and a report of validation or material deviations. The package contains no generator script or application starter; implementation happens in the target project.

## Example requests

```text
/figma-implement-design implement the frame at this Figma link
using our existing tokens and components, then compare it visually.

/figma-implement-design add this button variant to our shared
component and preserve its keyboard and disabled behavior.
```

## Package guide

- [SKILL.md](SKILL.md): full retrieval, implementation, and validation process.
- [assets/](assets/): skill icons.
- [LICENSE.txt](LICENSE.txt): license text.

Install by copying this directory to `~/.claude/skills/figma-implement-design/` (for example `cp -R figma-implement-design ~/.claude/skills/`). Claude Code then uses it automatically when a request matches, or you can invoke it directly with `/figma-implement-design`. See the [Claude Code skills documentation](https://docs.claude.com/en/docs/claude-code/skills).
