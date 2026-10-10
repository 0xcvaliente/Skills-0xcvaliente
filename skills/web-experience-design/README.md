# Web Experience Design

`web-experience-design` plans, builds, and verifies coherent web experiences. It connects a product's content and primary task with a visual system, then implements a representative slice and inspects it before extending the full experience.

The skill supports substantial interfaces and narrative pages, including cinematic or 3D work when those techniques serve the brief. It uses the smallest route that answers the request rather than treating every website as an opportunity for elaborate effects.

## When to use it

Use it for a landing page, portfolio, editorial site, portal, substantial product interface, or a requested scroll-choreographed or 3D experience. For an isolated component fix, use [UI Design](../ui-design/README.md) or the relevant focused skill. Animation-only work belongs with [UI Animation](../ui-animation/README.md).

## Routes

| Route | Main concern |
|---|---|
| Product interface | Task clarity, information hierarchy, states, and accessibility. |
| Narrative page | Story, evidence, calls to action, and visual rhythm. |
| Cinematic experience | Scroll choreography, pinned chapters, camera movement, or real-time 3D central to the brief. |

All routes read design-direction guidance. Motion and 3D references are loaded only where relevant. A scoped repair does not restart the entire page design.

## How it works

Inspect the brief, repository, assets, content, framework, and existing design system. Identify the audience, primary action, constraints, and target devices, then establish a short working direction for content order, typography, color, density, imagery, and interaction.

Build the smallest representative slice: the primary workflow for a product interface, or an opening and complete story beat for a narrative page. Review it in the browser, correct the direction, and then extend the experience.

Supplied copy and claims remain authoritative unless rewriting is requested. The skill does not invent testimonials, metrics, certifications, or destinations. Optional media and renderers should enhance a usable semantic experience, with graceful behavior if they fail.

## Requirements and output

The package contains guidance rather than a starter app, asset library, renderer, or hosting service. It uses the target project's installed stack. Additional dependencies should materially improve the requested result; browser access is necessary to substantiate visual and interaction claims.

The output is an implemented experience with a coherent visual system, relevant state and device checks, and material limitations. It does not independently publish a site or configure hosting.

## Example requests

```text
/web-experience-design build this product launch page from our
approved copy and assets, inspect a representative slice first,
and verify the finished mobile and desktop experience.

/web-experience-design build a cinematic portfolio chapter with
accessible content and a fallback if the 3D scene cannot load.
```

## Package guide and provenance

- [SKILL.md](SKILL.md): routing, shared workflow, and design decisions.
- [Design direction](references/design-direction.md): content and visual system guidance.
- [Motion and 3D](references/motion-and-3d.md): enhancement choices and implementation considerations.
- [Verification](references/verification.md): checks for the chosen route.

The entrypoint records this as an original synthesis informed by UI UX Pro Max and Web Design Studio. Their code, datasets, and installers are not bundled.

Install by copying this directory to `~/.claude/skills/web-experience-design/` (for example `cp -R web-experience-design ~/.claude/skills/`). Claude Code then uses it automatically when a request matches, or you can invoke it directly with `/web-experience-design`. See the [Claude Code skills documentation](https://docs.claude.com/en/docs/claude-code/skills).

## Design collection integration — 2026-10-08

Preserves the representative-slice workflow for coherent pages and experiences. Adds scoped component, variant, motion, mobile, resilience, and library-selection support without expanding an isolated repair into a redesign.

The companion collection adapts all 14 skills from [Emil Kowalski](https://github.com/emilkowalski/skills), reviewed at `e8a175de22ae1e49370fc144c1f3bb9aeedf988d`. Each adapted package includes its original guide, supporting resources, source checksums, Claude Code notes, and MIT license. Start with [Emil Design Engineering](../emil-design-eng/README.md) or [Animate](../animate/README.md), then select the specific workflow needed.

The integration changes instructions and routing; it does not install UI libraries, launch an app, or establish device/browser verification by itself. Existing source guides, helpers, probes, fixtures, and evaluation scenarios remain available.
