# Figma Create Design System Rules

`figma-create-design-system-rules` turns a project's existing UI conventions into reusable instructions for future Figma-to-code work. It captures knowledge that would otherwise need to be repeated in prompts: component locations, naming, token usage, styling conventions, imports, assets, and application architecture.

The result is tailored to the repository. A React project using Tailwind and a Vue project using CSS Modules should receive different instructions based on the patterns actually present.

## When to use it

Use it when onboarding an agent to a UI codebase, establishing a consistent Figma implementation workflow, or refining rules after the project's design system changes. It is especially useful before implementing many related frames or components.

The destination is the project's instruction file: `AGENTS.md` by default (the cross-tool convention), or the host-specific file the project already uses (`CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`, or `.cursor/rules/figma-design-system.mdc` for Cursor). Existing instructions should be preserved when adding the relevant rules.

## How it works

1. Ask the Figma MCP `create_design_system_rules` tool for its foundational guidance, identifying the project's languages and framework.
2. Inspect component organization, styling sources, design tokens, composition patterns, state management, routing, and imports.
3. Write rules based on observed conventions, including component reuse, design-context retrieval, screenshot validation, and asset handling.
4. Save the rules in the project's existing instruction file, or `AGENTS.md` if there is none (plus host-specific files only when the project uses them). Cursor rules include frontmatter and repository-specific globs.
5. Try the rules on a representative component and refine them where observed behavior differs from the intended conventions.

The skill includes examples and a rule template. These are starting points; project-specific values and paths must come from the repository.

## Requirements and output

It requires access to the project code and a connected Figma MCP server with the rules tool. Familiarity with team conventions is useful, but the workflow can discover many of them from source.

The deliverable is a maintained instruction file for an agent, rather than a new Figma library or a completed screen. It can guide [Figma Implement Design](../figma-implement-design/README.md) on later tasks.

## Example requests

```text
Use the figma-create-design-system-rules skill to inspect this React repository
and add Figma implementation conventions to its instruction file.

Use the figma-create-design-system-rules skill to update our existing rules to
use the current token source and component import aliases.
```

## Package guide

- [SKILL.md](SKILL.md): workflow, supported destinations, and examples.
- [references/rule-template.md](references/rule-template.md): reusable rule structure.
- [scripts/check_agents_md.sh](scripts/check_agents_md.sh): draft helper that reports which common instruction files (AGENTS.md, CLAUDE.md, GEMINI.md, .github/copilot-instructions.md) exist in the current directory; it does not validate their content.
- [assets/](assets/) and [LICENSE.TXT](LICENSE.TXT): icons and licensing.

Install by copying this directory into your host's skills folder (see the repository `INSTALL.md`; for example `cp -R figma-create-design-system-rules ~/.agents/skills/`). The host can select it when a request matches, or you can name the skill in your prompt.
