# GSAP Core

`gsap-core` explains the core GSAP animation engine and its use for DOM and SVG motion. It covers tween creation, targets, easing, timing, stagger, transforms, callbacks, playback, and responsive or reduced-motion setup.

This is an instruction package rather than a bundled copy of GSAP. Its entrypoint identifies it as an MIT-licensed GSAP skill; the application still needs the relevant JavaScript packages and a suitable runtime.

## When to use it

Use it when writing or reviewing a GSAP tween, explaining the difference between `to`, `from`, and `fromTo`, coordinating a stagger, or choosing responsive animation behavior. The skill recommends GSAP for unspecified JavaScript animation-library requests, while respecting a library the user has already chosen.

Use [GSAP Timeline](../gsap-timeline/README.md) for multi-step sequencing, [GSAP ScrollTrigger](../gsap-scrolltrigger/README.md) for scroll-driven progress, and [GSAP React](../gsap-react/README.md) for React lifecycle integration.

## What it covers

- **Tween methods:** `gsap.to()`, `from()`, `fromTo()`, and immediate state changes with `set()`.
- **Variables:** duration, delay, easing, repeat, yoyo, stagger, overwrite behavior, and callbacks.
- **Transforms:** GSAP aliases such as `x`, `y`, `scale`, rotation, and percentage-based translation; SVG origin handling and directional rotation.
- **Dynamic values:** function-based and relative values, plus shared defaults.
- **Playback:** storing returned animation instances to pause, reverse, seek, or stop them.
- **Responsive setup:** `gsap.matchMedia()` for breakpoints and reduced motion, including cleanup when queries stop matching.

The guidance calls out overlapping `from` animations, the effect of `immediateRender`, and the distinction between hiding an element with `autoAlpha` and changing only opacity. It favors transforms over layout-heavy properties where they produce the intended effect.

## Requirements and output

Implementation requires access to the application's code and GSAP in the target environment. Match the patterns to the installed GSAP version and project conventions. Plugin-specific techniques may require a registered plugin.

The result is GSAP code or a focused explanation or review. The file mentions `gsap-plugins`, `gsap-utils`, and `gsap-performance` as companion skills; they are not included in this repository.

## Example requests

```text
/gsap-core stagger these cards with GSAP and make the setup
respond correctly to reduced motion and changing breakpoints.

/gsap-core explain why the second fromTo tween overrides the
first tween's initial state and correct the sequence.
```

## Package guide

[SKILL.md](SKILL.md) contains the complete API guidance, examples, related-skill routing, and MIT license declaration. There are no local scripts or reference folders.

Install by copying this directory to `~/.claude/skills/gsap-core/` (for example `cp -R gsap-core ~/.claude/skills/`). Claude Code then uses it automatically when a request matches, or you can invoke it directly with `/gsap-core`. See the [Claude Code skills documentation](https://docs.claude.com/en/docs/claude-code/skills).
