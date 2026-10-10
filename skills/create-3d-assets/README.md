# Create 3D Assets

`create-3d-assets` helps Claude build editable 3D meshes, props, characters, and figures for digital games or interactive web viewers. It connects the asset brief with an authoring route, export format, and checks in the actual target runtime.

The default workflow is **Blender Python → editable source and GLB → validation and optimization → target preview**. The package also covers procedural Three.js geometry, licensed starting assets, and authorized image-to-3D drafts followed by mesh cleanup. Its recommendations are practical workflow judgments, supported by dated primary-source research rather than a measured vendor-quality benchmark.

## When to use it

Use it to create or revise game props, stylized figures, modular kits, rigged characters, browser model previews, or GLB/glTF assets. It also applies when an existing model needs cleanup, optimization, export, or checks before delivery.

A static posed figure and an animated character have different requirements. Animation adds a skeleton, bind pose, weights, suitable deformation topology, and tested clips. The skill makes that distinction before choosing a route. A raster image depicting a 3D object, ordinary UI animation, CAD engineering, or 3D printing alone falls outside its scope.

## Choose a workflow

| Need | Recommended route |
|---|---|
| Custom props, low-poly figures, modular kits, repeatable variants | Scripted Blender modeling; Geometry Nodes when repetition warrants it. |
| Simple shapes generated only inside a website | Procedural Three.js geometry in the existing renderer. |
| One online figure with orbit and zoom | An optimized GLB displayed with `<model-viewer>`. |
| A browser game or custom interactive scene | Exported GLBs or procedural geometry in the project's Three.js, Babylon.js, or game runtime. |
| Complex organic characters or creatures | Suitable licensed mesh, sculpting/retopology, or authorized AI draft, followed by cleanup and deformation checks. |
| Live edits in an open Blender scene | An already-connected Blender MCP bridge, if available; scripts otherwise. |

GLB is the default for web and Godot delivery. Unity and Unreal exports follow the project's configured importer, including established FBX pipelines. Geometry, materials, textures, transfer size, and frame-time budgets depend on the actual scene and devices.

## How it works

Establish the asset's silhouette, distinctive features, dimensions, pivot, materials, animation needs, target device, and delivery format. Inspect the available tools and the project's existing rendering and import conventions.

Build the silhouette and proportions first, inspect multiple angles under neutral lighting, then add detail and exportable materials. Preserve editable source or reproducible generator parameters. Procedural shaders, curves, instances, constraints, and simulations need an explicit strategy for export or baking.

Inspect the exported asset, validate it when a full validator is available, and optimize a delivery copy when needed. Compression must match the target loader's decoder support. Reopen the export in a clean scene or the target viewer, check scale, textures, normals, clipping, transparency, and animation, then verify relevant game or web behavior. A source render or provider thumbnail does not prove that the exported file works.

## Requirements

The package supplies instructions and an inventory helper. Installing it does not install Blender, a renderer, a game engine, an AI service, or a Blender bridge.

| Capability | Requirement |
|---|---|
| Blender authoring and export | An installed Blender executable with its bundled Python API. Check the version before scripting exporters or rigs. |
| Bundled glTF inventory | Python 3.9+; standard library only. |
| Web preview | The target project's renderer, or a configured `<model-viewer>` page, served over HTTP. |
| Game delivery checks | Access to the actual engine and importer. |
| Full glTF validation and optimization | Optional Khronos glTF-Validator and/or glTF Transform. These are separate tools. |
| AI generation or live Blender control | An available, configured service or bridge. For Claude Code, an MCP server registered with `claude mcp add` (see the [Blender workflow](references/blender-workflow.md) for the community Blender bridge). Paid generation needs authorized spend; reference uploads and publication use the task's existing authorization. |

If a required tool is missing, Claude can prepare useful source or specifications and report the remaining checks. It must distinguish prepared files from exports actually built and viewed.

## Outputs

Depending on the brief, the handoff includes editable Blender source or a procedural generator, a GLB or engine-specific export, an inspected preview, and measured asset facts. Reusable assets can include a small manifest recording dimensions, pivot, generator settings, exported geometry/material/texture counts, animation names, provenance, and checks performed.

Static models do not automatically include rigs or animations. Licensing and service rights need to be checked for the specific source asset or generation service. Provenance records should exclude credentials and signed download URLs.

## Example requests

```text
/create-3d-assets create a low-poly robot for my browser game.
Use a two-meter height, a base pivot, three materials, editable
Blender source, and a GLB verified in our existing Three.js scene.

/create-3d-assets optimize this figure for an online model viewer.
Preserve its silhouette and textures, measure the exported asset,
and verify orbit, zoom, loading, and mobile interaction.

/create-3d-assets prepare this humanoid for our Godot game with
idle and walk clips. Check the skeleton, weights, deformation,
scale, and imported animations before calling it ready.
```

## Install and inspect

Copy this folder into your personal Claude Code skills directory so it lives at `~/.claude/skills/create-3d-assets/`:

```bash
cp -R create-3d-assets ~/.claude/skills/
```

Claude picks the skill automatically from its description, or you can invoke it with `/create-3d-assets`. See the [Claude Code skills documentation](https://docs.claude.com/en/docs/claude-code/skills).

To inspect an exported asset:

```bash
python3 ~/.claude/skills/create-3d-assets/scripts/inspect_gltf.py /absolute/path/model.glb
```

The helper reads `.glb` and `.gltf` files and reports JSON inventories: mesh definitions, nominal triangle and vertex counts, declared local bounds, materials, textures, animations, skins, extensions, and resource paths. Geometry counts do not include scene instancing. It checks selected container and resource problems and avoids downloading remote resources or printing embedded data and URL credentials.

Exit codes are `0` for a completed inventory without detected problems, `1` for detected resource problems, and `2` for a malformed or unreadable input. This is a focused inventory tool, not full glTF specification validation, decoded geometry analysis, world-space bounds, or visual QA.

## Package guide and provenance

- [SKILL.md](SKILL.md): selection metadata, asset contract, workflow, verification, and handoff.
- [Blender workflow](references/blender-workflow.md): scripting, editable source, materials, rigs, and export.
- [Web and game delivery](references/web-and-game-delivery.md): runtimes, import formats, optimization, and viewer behavior.
- [AI and library assets](references/ai-and-library-assets.md): licensed sources, AI task handling, cleanup, and provider limits.
- [Research and inspiration](references/research.md): tool comparison and primary sources researched with Obscura on 7 October 2026.
- [Inventory helper](scripts/inspect_gltf.py): dependency-free GLB/glTF inspection.

The workflow is an original synthesis of the linked documentation and visual references. Modeling applications, provider SDKs, third-party assets, and bridge implementations are not bundled. Recheck evolving provider APIs, costs, rights, and importer behavior before implementation.

Structural skill validation and focused helper checks passed for generated fixtures covering valid GLB data, external resources, malformed inputs, and URL redaction. No Blender, AI-generation, or game-engine integration test is claimed by this package's research.
