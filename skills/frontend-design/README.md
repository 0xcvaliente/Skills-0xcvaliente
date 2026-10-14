# Frontend Design

`frontend-design` guides distinctive visual design for new interfaces and substantial redesigns. It starts with the product's subject, audience, and primary job, then makes deliberate choices about typography, palette, layout, content, imagery, and motion.

The emphasis is on a recognizable point of view grounded in the brief. Familiar design treatments can be appropriate, but they should express this product rather than appear automatically in every generated page.

## When to use it

Use it when creating a page's aesthetic direction, giving a product a stronger visual identity in its interface, or reshaping a design that feels generic. It is useful for marketing pages, editorial work, and product interfaces when visual direction is part of the assignment.

For mode-specific React and Tailwind implementation or an evidence-based interface audit, use [UI Design](../ui-design/README.md). For a complete multi-section experience with implementation and verification, use [Web Experience Design](../web-experience-design/README.md).

## How it works

The skill first grounds the design in real content and context. It then develops a compact plan: named palette values, typography roles, a layout concept, alignment, and the principles that make the result fit the brief. ASCII wireframes can help compare structures.

Before building, it critiques that plan for generic choices and revises weak decisions. Implementation follows the revised direction, with further visual review as the work develops. It recommends concentrating expressive design in a small number of meaningful places and removing decoration that does not help the page.

Copy is part of the design. Actions use clear verbs, wording stays consistent through a flow, and empty or failure states explain what to do next. Structural devices such as labels, rules, or numbering should convey information rather than act as filler.

## Requirements and output

The package is a self-contained Markdown workflow. It has no bundled scripts, font assets, component library, or runtime dependencies. Useful inputs are the brief, existing brand guidance, actual content, assets, and the application's current framework.

The result may include a visual direction, a compact token system, and implemented UI. Responsive behavior, keyboard focus, readable contrast, and reduced motion are part of the expected quality floor. Screenshots and browser review strengthen claims about the finished design.

## Example requests

```text
Use the frontend-design skill: design and build a distinctive archive page for
this photography studio using the supplied work and brand guide.

Use the frontend-design skill: revise this landing page's visual direction;
keep its content and give the typography a clearer hierarchy.
```

## Package guide

- [SKILL.md](SKILL.md): design principles, planning process, critique, and interface-writing guidance.
- [LICENSE.txt](LICENSE.txt): license text.

Install by copying this directory into any [Agent Skills](https://agentskills.io)-compatible location, for example `cp -R frontend-design ~/.agents/skills/` (see [INSTALL.md](../../INSTALL.md) for each host's folder). Compatible agents select it automatically when a request matches its description, or you can name it explicitly ("use the frontend-design skill").

## Design collection integration — 2026-10-08

Preserves brief-led visual direction and adds focused component, prototype, motion, mobile, and resilience companions without substituting their example aesthetics for the user's brief.

The companion collection adapts all 15 skills from [Emil Kowalski](https://github.com/emilkowalski/skills), 14 of them reviewed at `e8a175de22ae1e49370fc144c1f3bb9aeedf988d`, plus `animation-performance` at `2d228630ba1446365f614a108cb8252f1feda202`. Each adapted package includes its original guide, supporting resources, source checksums, Agent notes, and MIT license. Start with [Emil Design Engineering](../emil-design-eng/README.md) or [Animate](../animate/README.md), then select the specific workflow needed.

The integration changes instructions and routing; it does not install UI libraries, launch an app, or establish device/browser verification by itself. Existing source guides, helpers, probes, fixtures, and evaluation scenarios remain available.
