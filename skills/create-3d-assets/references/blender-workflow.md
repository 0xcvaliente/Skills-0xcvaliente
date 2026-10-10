# Blender workflow

Read for custom modeling, cleanup, rigs, procedural kits, and exporting Blender sources.

## Scripted modeling

Use Blender's bundled Python (`bpy`), not an assumption that system Python can import it. Check `blender --version` and the installed exporter/operator properties. Match API documentation to that version; `current` documentation can describe a newer build.

A reproducible build usually runs in a separate background process:

```sh
blender --background --factory-startup --python-exit-code 1 --python /absolute/path/build_asset.py -- --output-dir /absolute/path/output
```

The generator parses only arguments after `--`. Put parameters, materials, random seed, and output paths together. Argument order matters. `--factory-startup` belongs to this isolated process; never use it to replace an open user scene.

Prefer `bpy.data` and explicit object references for operations that should work without a selected UI area. `bpy.ops` is useful for primitives/export but is context-sensitive: set mode, selection, active object, and view layer deliberately. Do not hide operator poll failures with broad exception handlers. Scope reruns to a named generated collection or start a clean background process; avoid deleting the user's whole scene.

Create meaningful named parts. Use primitives, mesh construction, curves converted to meshes, bevels, and controlled modifiers for props. Repeated architecture/vegetation can benefit from Geometry Nodes, with a documented way to realize/export instances. Use instances at runtime for repeated assets when supported; do not bake thousands of duplicates unnecessarily.

For believable characters, work from a suitable base mesh or adequate modeling references. Primitive assembly works for deliberately stylized rigid figures, not automatically for deforming anatomy. Correct joint loops, detached parts, hair/clothing, face features, and symmetry according to the brief. Decimation reduces geometry but does not create good deformation topology.

## Materials and scale

Use Principled BSDF connections the glTF exporter recognizes. Keep base color/emission in the appropriate color space and normal/roughness/metallic data as non-color. glTF uses a metal/rough workflow; channel-packed occlusion/roughness/metallic convention is R/G/B. Inspect the actual baked maps and normal-map convention in the target.

Arbitrary Blender procedural nodes and viewport effects do not become portable shader programs. Bake them to appropriately sized textures when necessary. Keep a richer source material and a delivery material if that helps editing. Avoid baked lighting in base color when the target relights the object.

Specify physical dimensions and pivot in source. Blender is commonly Z-up; glTF is Y-up and the exporter performs conversion. Do not add a second compensating rotation blindly. Verify the exported transform in the importer. Apply transforms deliberately; applying transforms to a bound rig can damage its relationship to the mesh. Use a separate export copy when needed.

## Rigging and animation

Choose rig complexity from required motions. A rigid robot can use parented parts; a soft character needs skinned deformation. Build or import a suitable armature, confirm bind pose, weight the mesh, and test elbows, shoulders, knees, hips, and feet before detailed animation. Name bones and clips consistently with the target game's conventions.

Exporter action/NLA settings and animation data APIs vary by Blender version. Inspect available properties instead of pasting an old operator signature. Bake constraints/IK to supported bone/object transforms when required; Blender control rigs do not run inside a GLB. Keep deformation bones, morph targets, root motion, and clip ranges intentional. Verify exported clips independently; automatic rigging is a starting point.

## Export and visual loop

Save `.blend` before destructive export preparation. Export only the asset hierarchy, excluding turntable cameras, backdrop, lights, and helpers unless requested. Convert unsupported geometry or evaluate modifiers deliberately. Check whether instance/material extensions are supported by the recipient. Retain a simple uncompressed GLB baseline before optimization.

Basic calls, with additional settings chosen for the installed exporter:

```python
bpy.ops.wm.save_as_mainfile(filepath=str(source_path))
bpy.ops.export_scene.gltf(filepath=str(export_path), export_format="GLB", use_selection=True)
```

These calls assume correct asset selection has already been set. For animated assets, inspect exporter options and verify clips rather than relying on defaults.

Render front/side/back/three-quarter evidence at a readable size. Reimport GLB in a clean process for a comparison render, or inspect it in the target viewer. A beautiful source render can conceal an export failure.

## Optional live bridge

An already-connected Blender MCP bridge can inspect scene objects, run Python, and provide viewport/render evidence. Discover its actual tools and verify the intended scene before edits. Save/checkpoint before structural changes. Preserve reproducible source alongside conversational commands.

[MCP for Blender](https://github.com/ahujasid/mcp-for-blender) is a **community** project, formerly `blender-mcp`; its maintainer documents Claude Code support. It is not a Blender Foundation tool. The research did not install or execute it. Read its current setup, telemetry, and execution behavior when bridge installation is actually requested; prefer a scoped inspected setup over a downloaded shell script that configures multiple applications.

As documented in its README (checked 2026-10-10), it needs `uv`, Blender 3.0+, and its Blender add-on (`uvx mcp-for-blender install-addon`, then enable "MCP for Blender" in Blender's add-on preferences and start its server from the viewport sidebar). Register the server with Claude Code only when the user asks for the bridge:

```sh
claude mcp add --scope user blender -- uvx mcp-for-blender
```

Omit `--scope user` to register it for the current project only (Claude Code's default local scope). The bridge sends a minimal anonymous usage record by default; to disable telemetry, register it as `claude mcp add --scope user --env DISABLE_TELEMETRY=true blender -- uvx mcp-for-blender` instead. Run only one MCP client against the Blender add-on at a time. Restart Claude Code (or run `/mcp`) to confirm the server's tools are connected before relying on them.

Primary references: [Blender Python quickstart](https://docs.blender.org/api/current/info_quickstart.html), [command-line arguments](https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html), [Blender 4.5 LTS glTF export](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html). The last link is a verified versioned exporter reference; confirm differences for the installed version.
