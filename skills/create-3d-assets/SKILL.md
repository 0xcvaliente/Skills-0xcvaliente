---
name: create-3d-assets
description: Create, edit, optimize, and verify real 3D meshes, props, characters, and figures for digital games or interactive web viewers. Use for Blender sources, GLB/glTF assets, procedural Three.js geometry, rigged characters, and browser model previews. Do not activate for a 2D image depicting a 3D object, ordinary UI animation, CAD engineering, or 3D printing alone.
---

# Create 3D Assets

Deliver an editable asset and a working export for the user's target. Prefer **Blender Python → GLB → target-runtime verification** for custom reusable assets. For simple shapes generated only inside a web scene, direct Three.js geometry may be faster. For complex organic forms, use a suitable licensed base mesh or an authorized image-to-3D service, then inspect and finish the mesh in Blender.

These defaults are workflow judgments, not a claim that one tool wins every quality benchmark. Preserve the user's chosen engine, visual style, references, and existing pipeline.

## Choose the route

| Need | Starting route | Read when relevant |
| --- | --- | --- |
| Custom props, low-poly figures, modular kits, repeatable variations | Blender Python; Geometry Nodes when repetition justifies them | [Blender workflow](references/blender-workflow.md) |
| Simple web-only shapes, globes, particles, parametric diagrams | Three.js geometry in the existing renderer | [Web and game delivery](references/web-and-game-delivery.md) |
| One online object with orbit/zoom and optional AR | Export GLB; use `<model-viewer>` | Web and game delivery |
| Custom interactions, multiple models, a browser game | Export GLB; use the project's Three.js/Babylon.js/game runtime | Web and game delivery |
| Complex organic character, creature, sculptural figure | Licensed base mesh, sculpt/retopology, or authorized AI draft followed by cleanup | [AI and library assets](references/ai-and-library-assets.md), then Blender workflow |
| Live changes to an open Blender scene | Discover an already-connected Blender MCP bridge; otherwise use scripts | Blender workflow |
| Comparing tools or finding visual references | Dated research and primary source links | [Research and inspiration](references/research.md) |

## Establish the asset contract

Infer what the project and request already establish. Clarify only decisions that materially change the asset: static versus animated, engine/viewer, required likeness, real dimensions, and delivery format. If unspecified, a reasonable first custom asset is a stylized static mesh, meters, a useful centered/base pivot, editable source, GLB, and a browser preview. State assumptions briefly and proceed.

Record dimensions, coordinate/pivot convention, visible silhouette and distinctive features, material palette, required animation clips, and target device. Inspect repository callers and existing rendering lifecycle before integrating. Set geometry, material, texture, download, and frame-time budgets for the actual scene; avoid universal polygon limits. Count exported triangles rather than Blender faces.

Check actual tool availability. Locate Blender and its version; discover connected tools rather than inventing Blender MCP, Meshy, Tripo, or other providers. A skill is guidance, not an installed modeling application. If a required tool is absent, still prepare useful source/specification or use an appropriate available route, while clearly distinguishing prepared files from exports actually built and viewed. Do not silently replace a mesh deliverable with a raster image.

## Build and inspect

- Begin with silhouette, proportions, negative space, and a neutral-light multi-angle preview. Add surface detail after the form reads correctly. Preserve small features that distinguish the requested subject; a pile of primitives is only a blockout when more is required.
- Keep reproducible parameters and seed in a generator or preserve editable modeling data. Keep changes scoped to the current asset/collection. Save source separately from optimized delivery copies.
- Use exportable PBR materials or deliberate unlit/vertex-color shading. Bake procedural appearance when it must travel with the model. Curves, simulations, Geometry Nodes instances, constraints, and shaders require an explicit export strategy.
- A posed figure can be static. An animated character additionally needs a suitable skeleton, bind pose, weights, deformation topology, and named clips. Do not equate a generated model or automatic rig with an animation-tested character.
- Export for the actual importer. GLB is the default for web/Godot; follow an established Unity/Unreal FBX pipeline when applicable. OBJ/STL omit capabilities needed by many textured/animated assets. GLB can still reference external resources: inspect rather than assume it is self-contained.

## Verify the delivered asset

1. Inspect the export with the bundled helper:

   ```sh
   python3 <skill-dir>/scripts/inspect_gltf.py /absolute/path/asset.glb
   ```

   This inventories structure, geometry counts, required extensions, and resource paths. It does **not** decode meshes/textures, validate the full specification, compute world bounds, or prove visual/game readiness.

2. Run Khronos glTF validation, directly or through `gltf-transform validate`, when available. Fix errors; review warnings in context. Inspect and optimize a copy with glTF Transform when transfer size, textures, or draw calls warrant it. Verify decoder support before adding Draco, Meshopt, or KTX2.
3. Reopen the exported file in a clean scene or target runtime. Inspect front, side, back, and three-quarter views under neutral light. Check missing textures, flipped normals, scale/pivot, clipping, transparency, animation clips, and comparison with the reference. Inspect actual screenshots/renders (view image files with the host's image-viewing capability; if it has none, state that visual inspection was not performed); a completed command or provider thumbnail is insufficient.
4. For game delivery, verify a real import and representative animation/collision use when the engine is available. For web delivery, check model/resource responses, console errors, loading/failure states, mobile controls, and the lifecycle described in the delivery reference, using whatever browser-automation capability the session has (a browser extension, a Playwright script or MCP server, or a built-in browser pane); do not assume one exists. If none is available, say the web checks are unverified. Report any unperformed checks precisely.

## Handoff

Provide the actual source, export, inspected preview, and concise measured facts. For reusable assets, include an `asset.json` or similarly small manifest with dimensions/pivot, generator/version/seed when applicable, export settings, geometry/material/texture counts, animation names, source/license provenance, target checks, and known limitations. Do not put secrets or signed download URLs in provenance. A simple asset can use a brief handoff instead of an extra file.

Use existing authorization for local creation and reversible edits. Paid generation needs a chosen service and authorized spend; uploading private references or publishing a viewer needs authorization when not already included in the task. Set a finite generation budget and poll an existing task rather than resubmitting after a timeout. Reading inspiration does not authorize copying proprietary assets, installing bridges, or running third-party setup scripts.
