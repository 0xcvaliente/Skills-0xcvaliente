# GSAP React

`gsap-react` focuses on integrating GSAP into React and React-based frameworks. Its main concern is lifecycle ownership: animations should be scoped to the intended component and cleaned up when that component unmounts or its dependencies change.

The package complements the animation API skills. It supplies the React setup patterns that keep a working tween from becoming a leak, a stale callback, or a selector that affects another component instance.

## When to use it

Use it when animating a React or Next.js component with GSAP, introducing `useGSAP()`, managing refs and scoped selectors, or diagnosing duplicated animations and missing cleanup. It also covers a manual `gsap.context()` approach when using React effect hooks.

Use [GSAP Core](../gsap-core/README.md) for tween details, [GSAP Timeline](../gsap-timeline/README.md) for sequencing, and [GSAP ScrollTrigger](../gsap-scrolltrigger/README.md) for scrolling behavior. The referenced `gsap-frameworks` package for other frameworks is not included here.

## How it works

The preferred setup uses `@gsap/react` and its `useGSAP()` hook. A component ref scopes selectors, and the hook manages reverting the GSAP work it owns. The guidance explains dependencies, `revertOnUpdate`, and `contextSafe` for animation work created by later callbacks.

When the hook is unavailable, the skill shows how to create a GSAP context inside an effect and return cleanup that calls `revert()`. Server rendering needs care because DOM-dependent work runs in the browser. Next.js examples must fit the application's client component boundary.

The workflow emphasizes avoiding global selectors, preserving cleanup on unmount, and ensuring dependency-driven updates have deliberate lifecycle behavior. The exact integration should follow the installed React, framework, and GSAP packages.

## Requirements and output

The target application needs React and GSAP; the preferred hook also needs `@gsap/react`. This directory does not install those packages. Access to the component and a runnable app helps verify repeated mounting, navigation, and dependency changes.

The output is a component integration or focused correction, with lifecycle and selector ownership made explicit. It does not replace the component's underlying accessibility or application state logic.

## Example requests

```text
/gsap-react migrate this animation setup to useGSAP with a scoped
ref and correct cleanup when the component unmounts.

/gsap-react check why this animation duplicates after navigation
and verify the dependency update behavior.
```

## Package guide

[SKILL.md](SKILL.md) contains hook examples, context and effect patterns, and an MIT license declaration. No runtime library or executable helper is bundled.

Install by copying this directory to `~/.claude/skills/gsap-react/` (for example `cp -R gsap-react ~/.claude/skills/`). Claude Code then uses it automatically when a request matches, or you can invoke it directly with `/gsap-react`. See the [Claude Code skills documentation](https://docs.claude.com/en/docs/claude-code/skills).
