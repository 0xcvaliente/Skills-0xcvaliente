# Figma

`figma` is the collection's foundation for working with design information through a Figma MCP server. It explains how to retrieve structured design context, capture a visual reference, obtain assets, and translate the design into the target project's conventions.

The skill treats generated design code as a representation of the design. The implementation must still respect the application's framework, routing, state handling, reusable components, and design tokens.

## When to use it

Use it for requests involving Figma frame or layer URLs, node identifiers, design-to-code work, or Figma MCP setup and troubleshooting. A link should identify the exact frame or variant to implement; a broad file URL may not identify enough context.

For a more detailed end-to-end implementation process, use [Figma Implement Design](../figma-implement-design/README.md). For reusable project instructions that standardize later implementations, use [Figma Create Design System Rules](../figma-create-design-system-rules/README.md).

## How it works

1. Retrieve structured context for the exact nodes.
2. If the result is too large, retrieve metadata and request the necessary child nodes individually.
3. Obtain a screenshot of the same design variant.
4. Use returned image and SVG assets, following the server's asset handling rules.
5. Adapt the output to existing components, typography, spacing, and color tokens.
6. Compare the rendered implementation with the screenshot before completing the task.

Context and screenshots come before asset downloads and implementation. The asset rules discourage replacing supplied assets with placeholders or adding an unrelated icon library. Local asset URLs returned by the server should be used as supplied.

## Requirements and output

The workflow requires an accessible Figma MCP connection and access to the relevant design. Implementation also requires the application repository. The package itself contains guidance and metadata; it does not bundle a Figma server or configure access automatically.

Depending on the request, the result can be retrieved design information, a setup diagnosis, or production code integrated into the project's existing system. Visual parity requires inspecting the rendered result, not only reading generated markup.

## Example requests

```text
/figma inspect this frame link, retrieve its design context and
screenshot, and identify components we can reuse in the app.

/figma troubleshoot my MCP connection and explain which setup
checks establish that the server can read the selected frame.
```

## Package guide

- [SKILL.md](SKILL.md): retrieval sequence and implementation rules.
- [MCP configuration guide](references/figma-mcp-config.md): setup and troubleshooting.
- [Tools and prompts](references/figma-tools-and-prompts.md): tool selection and prompting patterns.
- [assets/](assets/) and [LICENSE.txt](LICENSE.txt): icons and license text.

Install by copying this directory to `~/.claude/skills/figma/` (for example `cp -R figma ~/.claude/skills/`). Claude Code then uses it automatically when a request matches, or you can invoke it directly with `/figma`. See the [Claude Code skills documentation](https://docs.claude.com/en/docs/claude-code/skills).
