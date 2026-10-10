# GSAP Timeline

`gsap-timeline` explains how to coordinate multiple GSAP animations on one controllable timeline. It replaces fragile chains of independent delays with a sequence whose order, overlap, labels, and playback can be understood and adjusted together.

The core idea is the position parameter. A tween can start at an absolute time, at a label, relative to the timeline's end, or relative to the most recently added animation. This makes choreography explicit without recalculating every delay when one step changes.

## When to use it

Use it for a multi-part entrance, an animated explanation, a reversible component sequence, or any group of tweens that needs shared playback. It is also useful when reviewing timing code that has become difficult to maintain.

[GSAP Core](../gsap-core/README.md) covers individual tween methods and easing. [GSAP ScrollTrigger](../gsap-scrolltrigger/README.md) covers timelines driven by scroll, and [GSAP React](../gsap-react/README.md) covers component ownership and cleanup.

## What it covers

The skill shows how to create a timeline, append tweens, overlap them, and place them relative to labels. Shared `defaults` keep repeated duration and ease settings in one place. Constructor options cover paused state, repeating, yoyo, and timeline-level callbacks.

Labels support readable sequencing and targeted playback. Nested timelines let separate animation sections compose into a master sequence. Playback controls include play, pause, reverse, restart, seeking by time or progress, and teardown.

The entrypoint distinguishes a timeline's duration from a tween's duration: the sequence length comes from its contents. It also warns against placing ScrollTrigger on child animations inside a parent timeline; a scroll-driven sequence needs deliberate top-level ownership.

## Requirements and output

The target environment needs GSAP. The package has no scripts or bundled runtime. Provide the elements or component to animate, the desired order, and any overlap or reversal constraints. Browser review is useful when pacing and interruption are part of the outcome.

The deliverable is a coordinated timeline or a focused explanation of sequence behavior. For animation purpose, timing craft, and reduced-motion decisions beyond timeline mechanics, consult [Animate](../animate/README.md) or [UI Animation](../ui-animation/README.md).

## Example requests

```text
/gsap-timeline coordinate the heading, image, and call to action
with labels so we can adjust the overlap without independent delays.

/gsap-timeline refactor this modal's tweens into one reversible
timeline with shared defaults.
```

## Package guide

[SKILL.md](SKILL.md) is the complete package: methods, position syntax, labels, nesting, controls, and an MIT license declaration.

Install by copying this directory to `~/.claude/skills/gsap-timeline/` (for example `cp -R gsap-timeline ~/.claude/skills/`). Claude Code then uses it automatically when a request matches, or you can invoke it directly with `/gsap-timeline`. See the [Claude Code skills documentation](https://docs.claude.com/en/docs/claude-code/skills).
