# Web interface guidelines

Use the sections relevant to the requested surface. These are decision prompts, not a reason to generate noisy findings.

## Semantics and accessibility

- Prefer native `button`, `a`, `label`, table, list, and heading elements before adding ARIA.
- Use links for navigation and buttons for actions. A custom interactive widget must implement its required keyboard behavior; native controls already provide theirs.
- Give every form control an associated visible label when possible. Name icon-only controls with an accessible name and hide purely decorative icons from assistive technology.
- Provide useful alternative text for meaningful images and empty alternative text for decorative images.
- Keep heading order meaningful and provide a skip link on substantial pages with repeated navigation.
- Announce important asynchronous status changes without moving focus unnecessarily.
- Do not rely on color alone for state or meaning. Verify text, control, focus, and disabled-state contrast against the project's accessibility target.
- Preserve browser zoom. Meaningful audio/video needs appropriate captions, transcripts, descriptions, and keyboard-operable controls.

## Keyboard and focus

- All flows must work without a pointer.
- Every focusable element needs a visible, unobscured `:focus-visible` treatment. Never remove an outline without an equivalent replacement.
- Modals and popovers follow an appropriate focus-entry, containment, Escape, and focus-return pattern.
- Sticky UI and overlays must not cover the focused element.
- Drag, swipe, pinch, and path gestures need a tap/click and keyboard alternative unless the gesture is essential.

## Forms

- Use meaningful `name`, `autocomplete`, `type`, and `inputMode` values. Do not blanket-disable autocomplete; choose tokens according to the field's purpose.
- Never block paste into credentials, one-time codes, or other inputs.
- Make labels and their controls one generous hit target. Keep mobile control targets comfortably sized.
- Allow submission to reveal validation unless the action would be harmful. Once a request starts, prevent duplicate submission while retaining a stable label and progress indication.
- Put errors beside their fields, connect them programmatically, and focus or summarize the first error after a failed submit.
- Preserve user input after validation, network failure, and hydration.
- Warn before abandoning meaningful unsaved work.
- Server mutations still validate input, authorize the action, and use idempotency where retries could duplicate effects.

## Interaction and state

- Every screen has a useful loading, empty, error, sparse, and dense state where applicable.
- Keep shareable/navigation-relevant state in the URL. Do not force transient presentation state into the URL without a user benefit.
- Destructive actions require a proportionate confirmation or a reliable undo window.
- Optimistic updates need rollback or reconciliation on failure.
- Preserve browser Back/Forward behavior and expected scroll restoration.
- Scope overscroll suppression to the actual modal or scroll region. Suppressing page overscroll can also remove pull-to-refresh, scroll chaining, and native swipe navigation. If explicitly required for desktop, test hybrid touch devices; `pointer: fine` describes the primary input, not the absence of touch.
- Avoid autofocus on mobile; use it on desktop only when one obvious primary input benefits.
- Tooltips supplement rather than replace essential labels or instructions.

## Layout and responsive behavior

- Prefer intrinsic sizing, flex, and grid over JavaScript measurement.
- Test narrow mobile, common laptop/desktop, zoomed layouts, and wide screens.
- Handle safe-area insets for fixed or full-bleed controls.
- Prevent accidental horizontal scrolling by fixing the overflowing content instead of globally hiding evidence of it.
- Give truncating flex/grid children the necessary shrink behavior, and provide access to the full value when truncation hides important content.
- Layouts must survive empty strings, translations, large text, and unusually long user-generated content.

## Content and typography

- Use concise, specific labels and error messages that explain the next action.
- Keep product terminology consistent. Follow the existing product voice; title case, sentence case, ampersands, and second-person language are style choices, not universal accessibility rules.
- Use locale-aware date, time, number, and currency formatting.
- Protect code identifiers and brand terms from unwanted translation when appropriate.
- Use tabular numerals for columns or rapidly changing values where alignment matters.
- Use the ellipsis character for omitted continuation or an action that opens a follow-up, according to product style.

## Motion

- Honor `prefers-reduced-motion` and provide an equivalent usable state.
- Motion should explain causality, orientation, or deliberate emphasis. Avoid decorative autoplay that competes with tasks.
- Prefer CSS or platform animation primitives and compositor-friendly properties when they achieve the intended result.
- List transitioned properties explicitly; avoid `transition: all`.
- Keep animations interruptible and choose transform origins that match the visual source of motion.
- Motion lasting more than a few seconds alongside other content needs a way to pause, stop, or hide when accessibility requirements apply.

## Images and media

- Reserve image dimensions or aspect ratio to avoid layout shift.
- Use responsive sizes and formats appropriate to the framework and browser matrix.
- Lazy-load non-critical below-fold media. Preload or elevate priority only for known critical media, using the installed framework's current API.
- Prefer efficient video to animated GIF when it is materially smaller, while providing reduced-motion and still-image behavior as needed.

## Theme and browser integration

- Define supported color schemes so native controls and browser UI render appropriately.
- Keep theme color, page background, form controls, and native selects legible in each theme and on Windows high-contrast/dark configurations.
- Respect forced-colors and user font-size settings where the product supports them.
- Interaction states should become clearer, not lower contrast.

## Performance

- Measure before adding virtualization, memoization, resource hints, or workers.
- Avoid layout reads during render and interleaved DOM reads/writes.
- Keep controlled input work cheap enough for each keystroke.
- Virtualize or use `content-visibility` when measured list cost warrants it and the choice preserves keyboard, search, and accessibility behavior.
- Preconnect or preload only critical origins/resources; unused hints compete for bandwidth and connections.
- Subset and preload fonts only when doing so improves real loading behavior without causing duplicate downloads.

## Hydration and framework behavior

- Controlled inputs need an update path; otherwise use an appropriate uncontrolled default.
- Make server and first client render agree. Resolve locale/timezone and client-storage differences deliberately.
- Use `suppressHydrationWarning` only for a known, contained mismatch that cannot reasonably be rendered consistently.
- Read the installed framework documentation before recommending version-sensitive image, script, font, caching, or dynamic-import APIs.

## Review output

For a concise file audit, use:

```text
path/to/file.tsx:42 - icon-only button has no accessible name; add a contextual aria-label
path/to/file.tsx:71 - focus enters the modal but is not returned to the trigger on close
```

Explain non-obvious corrections, interactions among findings, and any result that needs rendered verification. Avoid mechanical style findings that do not affect the requested product.

## Provenance

This checklist is a hardened local adaptation of Vercel Labs' MIT-licensed Web Interface Guidelines, reviewed at commit `434b7f91364665f2f733b310ec54809bf8f37937`. It intentionally removes runtime remote fetching and narrows several brand-specific or overly absolute rules.

Reviewed 2026-10-09 against [vercel-labs/web-interface-guidelines](https://github.com/vercel-labs/web-interface-guidelines/tree/434b7f91364665f2f733b310ec54809bf8f37937). The upstream desktop overscroll addition is applied conditionally to preserve native navigation and touch behavior.
