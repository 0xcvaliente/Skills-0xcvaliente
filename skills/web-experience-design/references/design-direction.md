# Design direction

Use this reference to turn a brief into a coherent design before filling pages with components. Treat its questions as decision aids, not a form to reproduce in the final output.

## Form the direction

Capture only what changes the design:

| Decision | Evidence to inspect | Output |
| --- | --- | --- |
| Page job | User goal, product task, call to action | One sentence stating what the page must help someone do |
| Audience and context | Device, environment, familiarity, accessibility needs | Reading and interaction priorities |
| Content hierarchy | Supplied copy, data, proof, legal or trust needs | Order of sections or task steps |
| Visual character | Brand assets, design files, product positioning | Two or three compatible attributes, plus one thing to avoid |
| Constraints | Stack, existing components, performance, media | Implementation boundaries |

Use references and searchable catalogs to widen options when the direction is unclear. Search one concern at a time, such as typography for dense data or patterns for an editorial reveal. Confirm the result fits the product and platform. If a suggestion conflicts with the user's content, existing system, readability, or task flow, reject it.

## Route-specific composition

**Product interface:** Start with the user's next action, key information, and consequences. Design navigation, hierarchy, data density, forms, feedback, empty/loading/error states, and responsive reflow together. Decorative style must preserve clear boundaries and control affordances. A marketing hero or testimonial sequence is rarely a useful default for a signed-in workflow.

**Narrative page:** Establish a promise, show the subject, provide specific evidence, then make the next action easy to find. Section order should follow the actual argument, not a stock template. Give important copy a stable readable moment. Social proof requires real supplied evidence.

**Cinematic experience:** Define a subject and transformation before choosing effects. The opening, transition, readable hold, and exit should communicate something distinct. Use [motion and 3D](motion-and-3d.md) for the implementation contract.

## Define a small visual system

- **Type:** Assign display, heading, body, label, and numeric roles only where needed. Choose typefaces for content, language support, legibility, and brand fit. Test long labels and real data.
- **Color:** Define background/surface, foreground, primary action, secondary action, border, focus, and status roles. Check each used pairing and state; a palette that looks good in a swatch may fail on a button or chart.
- **Space and density:** Use a consistent scale, then tune it for the work. Dashboards can be dense without crowding; stories can be spacious without losing continuity.
- **Imagery and materials:** Prefer supplied or licensed assets. Decide what images prove or explain. Effects such as glass, soft relief, grain, and blur are optional material choices, not product categories.
- **Components:** Reuse existing components and tokens. Add variants for genuine hierarchy or behavior. Specify hover, focus, pressed, disabled, loading, error, and selected states where applicable.

Implement one representative slice and inspect it with actual copy and data before spreading the system across the page.
