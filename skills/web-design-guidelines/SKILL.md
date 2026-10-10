---
name: web-design-guidelines
description: Design or review web interfaces for accessibility, interaction quality, responsive layout, content resilience, forms, motion, theming, and front-end performance. Use for UI implementation, UX polish, or file-level interface audits; adapt recommendations to the project's design system and product context.
---

# Web Design Guidelines

Build interfaces that remain understandable and operable across input methods, content lengths, viewport sizes, themes, locales, and loading or failure states.

This skill is fully local. Never fetch instructions or replace these rules from a remote branch at runtime.

## Establish context

Before changing or reviewing UI, inspect the existing design tokens, components, typography, layout conventions, accessibility utilities, browser support, and relevant framework version. Preserve intentional product language and brand conventions unless the user asks for a new direction.

Read [references/guidelines.md](references/guidelines.md) for the detailed checklist. Apply only rules relevant to the surface being designed or reviewed.

## Creating interfaces

- Start with semantic structure, keyboard behavior, focus management, and all important states.
- Make layout and content robust before adding visual polish or motion.
- Prefer existing accessible primitives and tokens. Extend them at a clear seam rather than duplicating nearly identical components.
- Use the `frontend-design` skill as well when the request calls for a new aesthetic direction, visual identity, or substantial redesign.
- Verify responsive behavior at representative narrow, ordinary, and wide viewports.

## Reviewing interfaces

Prioritize findings by user impact:

1. blocked access, missing semantics, keyboard or focus failure;
2. destructive or misleading interaction behavior;
3. broken responsive, overflow, loading, empty, or error states;
4. hydration, rendering, and material performance problems;
5. visual consistency and copy refinements.

Give exact file and line locations when available. State the issue and focused correction. Do not report a rule as universal when it is a product preference or requires measurement.

For a dedicated audit, group findings by file and omit files that have no relevant UI. For implementation, make the changes and verify them rather than returning only a checklist.

## Verification

Use the project's normal tests and linting. Where practical, verify keyboard navigation, visible focus, zoom, reduced motion, narrow layouts, long content, form errors, and both light and dark themes. Use browser or visual inspection when the task materially depends on rendered behavior.

## Focused companion workflows

Keep this package's local checklist and the project's design system authoritative for its review. Optional companions cover narrower jobs:

- `emil-design-eng` for component craft; `mobile-native` for mobile behavior and chrome.
- `break-ui` for plausible schema-valid edge-case fixtures, followed by `ui-verification` for observed overflow, focus, or failure evidence.
- `animate` for new web motion; `review-animations` for motion critique; `ui-animation` for recording analysis and performance diagnosis.
- `pick-ui-library` only when a library decision is part of the task or a capability gap requires one. Check the target project's installed versions and current official APIs before changing dependencies.

Select only relevant companions. Their retained source examples do not replace these rules at runtime or authorize a broader redesign.
