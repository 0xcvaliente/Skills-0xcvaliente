# Add Dark Mode

Use when the user wants to add dark mode support to an existing UI.

## Load First

- [guidelines/dark-mode.md](./guidelines/dark-mode.md) for the dark-mode design rules.
- [dark-mode-image.md](./dark-mode-image.md) for raster image work (auditing flagged images or a standalone "dark version of this image" request).

## Workflow

1. Inspect the UI and project Tailwind conventions.
2. Add dark-mode classes to the markup.
3. Audit raster images for dark-mode variants.
4. For each raster image needing a variant, follow [dark-mode-image.md](./dark-mode-image.md). It uses an image-generation tool when one is available; otherwise it returns a list of the dark variants needed and states that no image was generated.
5. Save generated dark-mode images beside the originals and wire them in. Variants that could not be generated are reported as pending; do not wire paths to files that do not exist.

## Guardrails

- Never generate, edit, or replace raster image assets without first loading [dark-mode-image.md](./dark-mode-image.md) and following its tooling check, even when the change seems simple, decorative, or incidental.

## Verify

- Check both modes for contrast, missing variants, and images still assuming a light background.
