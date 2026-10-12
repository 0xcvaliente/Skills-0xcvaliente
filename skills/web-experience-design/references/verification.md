# Verification

Use the smallest set of checks that establishes the page's actual claims. Inspect the rendered result as well as the code. Stop adding optional checks once the material risks are resolved.

## Every substantial design build

- Run the project's build or typecheck when relevant.
- Inspect a desktop and a narrow mobile viewport with real content. Look for clipped text, overflow, collapsed hierarchy, sticky overlap, and unusable controls.
- Check keyboard order, visible focus, control names, forms and errors, and color pairings in the states used. Use an accessibility checker as a supplement to manual interaction.
- Check browser console and failed requests. Exercise the primary action, including its destination or resulting state.
- Capture or inspect the opening and at least one representative interior state. A clean console is not visual proof.

## When the experience uses significant motion

- Inspect opening, transformation midpoint, readable hold, and exit. Reverse scroll and resize during the sequence.
- Check reduced-motion behavior and a live preference change if the implementation handles it.
- Check mobile input and performance on an actual or emulated narrow device. Watch for jank, content jumping, and pointer-only interactions.

## When the page depends on media, scripts, or 3D

- Check slow/failed assets and renderer failure. Essential copy and actions need a useful fallback.
- For a public narrative page, inspect with JavaScript disabled when its static content is intended to remain available. A dynamic application may need a different failure contract; verify the one promised by the product.
- Prove the requested real-time or interactive behavior in the browser. A source import, static poster, or passing lint rule is insufficient evidence.

Report what was actually checked. Distinguish static tests, browser observations, and unverified states. Do not call a page accessible, performant, or visually successful solely because a scoring script passed.
