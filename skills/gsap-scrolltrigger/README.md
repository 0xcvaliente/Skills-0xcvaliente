# GSAP ScrollTrigger

`gsap-scrolltrigger` guides GSAP animations whose activation or progress depends on scrolling. It covers discrete reveals, continuous scrubbing, pinned sections, timeline integration, callback batching, custom scrollers, and horizontal movement driven by vertical scroll.

It is useful when scroll geometry and animation ownership matter as much as the tween itself. A correct setup needs to stay aligned after layout changes and release its resources when a page or component disappears.

## When to use it

Use it for scroll reveals, parallax, a pinned story section, a scrubbed timeline, or ScrollTrigger debugging. Select [GSAP Core](../gsap-core/README.md) for tween basics and [GSAP Timeline](../gsap-timeline/README.md) when several animations share a sequence. React implementations also benefit from [GSAP React](../gsap-react/README.md).

## What it covers

- **Trigger geometry:** the element, scroll container, start and end positions, and development markers.
- **Behavior:** `toggleActions` for discrete playback or `scrub` for progress tied to scrolling.
- **Pinning:** keeping a section in place while maintaining appropriate spacing.
- **Timelines:** assigning ScrollTrigger to a top-level animation rather than competing child tweens.
- **Batching:** grouping callbacks when multiple elements enter or leave near the same time.
- **Custom scrollers:** `scrollerProxy()` and the update synchronization needed for third-party scrolling behavior.
- **Horizontal sequences:** `containerAnimation`, linear movement, and its pinning and snapping limitations.
- **Maintenance:** refreshing after relevant layout changes and reverting or killing owned triggers during teardown.

The skill calls for registering the plugin before use and removing development markers from production. It also distinguishes the pinned element from the child whose transform is animated.

## Requirements and output

The target app requires GSAP and its ScrollTrigger plugin. A browser and a scrollable route are needed to validate trigger positions, resizing, pin spacing, and teardown. The directory contains guidance, not the plugin implementation.

The result is a configured scroll interaction or a focused diagnosis and fix. Use [UI Animation](../ui-animation/README.md) when deciding whether a scroll effect serves the interface in the first place; API guidance alone does not establish that an effect belongs on a particular page.

## Example requests

```text
Use the gsap-scrolltrigger skill: build a pinned chapter with a scrubbed timeline
and verify its geometry after fonts load and the viewport changes.

Use the gsap-scrolltrigger skill: diagnose why the horizontal sequence drifts
and clean up its triggers during route navigation.
```

## Package guide

[SKILL.md](SKILL.md) contains configuration tables, implementation patterns, cleanup rules, official-documentation links, and an MIT license declaration.

Install by copying this directory into any [Agent Skills](https://agentskills.io)-compatible location, for example `cp -R gsap-scrolltrigger ~/.agents/skills/` (see [INSTALL.md](../../INSTALL.md) for each host's folder). Compatible agents select it automatically when a request matches its description, or you can name it explicitly ("use the gsap-scrolltrigger skill").
