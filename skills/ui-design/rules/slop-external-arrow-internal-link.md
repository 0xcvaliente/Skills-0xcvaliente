---
title: Match destination cues to actual navigation
id: slop-external-arrow-internal-link
category: slop
defaultTier: backlog
detect: static
---

## Match destination cues to actual navigation

Inspect the rendered destination and the project's icon convention before
reporting a misleading external-link cue. A diagonal arrow alone is not a
universal violation: applications may use it for a new window or another
documented purpose. Buttons can also navigate, so inspect their behavior.

When an icon explicitly signals an external destination or a new window,
confirm that the link actually does so. For an ordinary in-page jump or internal
route, use the project's forward-navigation cue or omit the icon. Check redirects,
proxied routes, and dynamic URLs before deciding; retain decorative trend arrows
when they communicate data rather than navigation.
