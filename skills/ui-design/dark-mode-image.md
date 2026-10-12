# Dark Mode Image

Use when adapting a standalone source image into a dark-mode-suitable version.

> **Tooling:** Not every host has image generation. If the host has an image-generation or image-editing tool (built in or from an MCP server), use it for the generation steps below. Otherwise take the default path: identify the images needing dark variants, list them with target background colors, and ask the user to generate them or source dark versions manually; say plainly that no image was generated. Never substitute CSS filter workarounds.

## Load First

- Before any image generation or editing, check whether an image-generation or image-editing tool is actually available. If none is, follow the default (no-generator) path.

## Workflow

Default (no image-generation tool):

1. Inspect the source image (use the host's file/image reading so the image is visible) and the dark-mode UI context.
2. For each image, record the source path, its exact dimensions, the target path with a `-dark` suffix, the chosen dark background color, and the preservation notes from Rules below (contrast, softness, fades, palette, vibe).
3. Write a concise generation or edit prompt per image that the user can run in their own image tool.
4. Return that list to the caller and state that no dark-mode image was generated. Do not wire a `-dark` path into the UI until the file actually exists.

With an image-generation tool:

1. Inspect the source image and the dark-mode UI context.
2. Generate or edit a dark-mode version at the original's dimensions.
3. Save it with a `-dark` suffix alongside the original.
4. Return the saved project path for the caller to wire in.

## Rules

- Check for and use a real image-generation or editing tool before any image generation or editing. Do not fake a variant with an ad hoc workaround (scripted inversion, brightness or contrast tweaks, filters); without a tool, use the default path
- If the source is a local file, view it first (host file/image reading) so the image is visible in the conversation context, and pass it to the tool as the edit input when the tool supports that
- Save project-bound generated outputs into the workspace beside the original; never leave a project-referenced dark-mode asset only in a tool's temporary or output directory
- Never claim a dark-mode image was created unless the file exists at the returned path
- Choose a background color that feels like an appropriate inversion of the original background: black or dark gray for white, dark gray for off-white, or the specific dark color the user provides; if the original background matched the site background, match the dark-mode site background instead
- Preserve the original contrast characteristics: light sections become darker while relative separation and readability stay intact
- Preserve blurs and softness; never sharpen anything that was blurry in the original
- Preserve foreground palette hues, adjusting saturation and lightness only as needed so the image presents correctly on a dark background
- Preserve the original vibe: bright and intense stays bright and intense, subtle and muted stays subtle and muted
- Preserve fades: watch areas that fade out and keep those fades in the dark-mode version
- The dark-mode image must be exactly the same dimensions as the original
- Save dark-mode images with a `-dark` suffix, e.g. `bg.jpg` and `bg-dark.jpg`

## Verify

- Generated image dimensions match the original exactly.
- The dark-mode image preserves the original composition, softness, fades, and foreground palette.
- Without a generator: every flagged image appears in the returned list with its target path, dimensions, and background color, and the response says no image was generated.
