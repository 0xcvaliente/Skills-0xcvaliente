---
name: web-experience-design
description: Plan, build, and verify coherent web experiences that combine visual direction with implementation. Use for substantial landing pages, product interfaces, editorial sites, or cinematic and 3D web projects; skip isolated component fixes and animation-only tasks.
---

# Web experience design

Create a visual system that fits the product, then build and inspect the actual experience. Use the smallest route that answers the brief. The user's content, brand, design files, and existing product conventions take precedence over examples and style catalogs.

## Route the work

1. **Product interface:** dashboards, portals, tools, forms, or ongoing workflows. Prioritize task clarity, information hierarchy, states, and accessibility. Read [design direction](references/design-direction.md).
2. **Narrative page:** launch, landing, portfolio, editorial, or campaign. Prioritize the story, evidence, calls to action, and visual rhythm. Read [design direction](references/design-direction.md); read [motion and 3D](references/motion-and-3d.md) only if motion carries part of the story.
3. **Cinematic experience:** scroll choreography, pinned chapters, camera moves, or real-time 3D requested by the user or central to the subject. Read [design direction](references/design-direction.md) and [motion and 3D](references/motion-and-3d.md).

For a scoped repair inside an existing experience, inspect the affected code and use only the relevant reference. Do not restart the page design.

## Shared workflow

- Inspect the repository, brief, content, assets, framework, design system, and current page before choosing a direction. Identify the audience, primary task or action, constraints, and target devices. Ask only when a missing answer changes a hard-to-reverse decision; otherwise state a reasonable assumption and proceed.
- Write a short working direction: page job, content order, visual character, typography roles, color roles, density, imagery, and interaction character. For an existing brand, adapt its tokens and components. Choose styles for their fit; never map an industry or keyword to a predetermined aesthetic.
- Build the smallest representative slice first: the main task flow for an interface, or the opening plus one complete story beat for a narrative page. Inspect it in the browser, correct the direction, then extend the rest.
- Preserve supplied copy and claims unless the user asks to rewrite them. Do not invent testimonials, metrics, certifications, prices, logos, or destinations. Keep semantic content and primary actions available before enhancement.
- Implement within the existing framework and installed stack. Introduce a library, asset, script, or 3D renderer only when it materially improves the requested result. Keep project rules and user choices authoritative.
- Read [verification](references/verification.md) when the result is ready to check. Verify the states and devices that matter for this route; report what was tested and any material limit.

## Decision rules

- Start from content and behavior, then define tokens. A generated palette, font pairing, layout pattern, or visual reference is a candidate to judge against the product; it is not an instruction to apply unchanged.
- Keep a single recognizable visual language across pages and states. Use variation to establish hierarchy or convey a real change, not to accumulate effects.
- Motion needs a job: orient, explain, show cause and effect, or reward an action. Keep reading and control possible while it moves. If motion has no clear job, use a static state.
- Accessibility and resilience are part of the design: keyboard operation, visible focus, readable text and contrast, reflow, reduced motion, loading/error/empty states, and useful content if optional media or a renderer fails.
- Match verification to claims. Static checks can catch code and token defects; they cannot establish visual quality, mobile usability, or that a 3D scene actually works.

This skill is an original synthesis informed by the MIT-licensed [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) and [Web Design Studio](https://github.com/MustBeSimo/web-design-studio). It does not bundle their code, datasets, or installers.

## Focused design companions

Use these optional packages at a specific step without restarting the overall experience:

- `prototype` compares working variants when the user requests them; otherwise build the representative slice directly.
- `emil-design-eng` polishes a component within the established visual system.
- `animate` constructs purposeful web motion; `review-animations` critiques it; `ui-animation` measures reference recordings or diagnoses jank.
- `mobile-native` checks platform behavior; `break-ui` prepares realistic edge-case fixtures; `ui-verification` observes the rendered outcome.
- `apple-design` supports a requested tactile or Apple-inspired control, rather than imposing that aesthetic on an unrelated brand.
- `pick-ui-library` resolves a genuine dependency choice; reuse the existing stack when it already supports the interaction.

The Emil-derived companions are pinned, locally bundled instructions. Read only the relevant guide and retain the user's scope, content, and runtime constraints.
