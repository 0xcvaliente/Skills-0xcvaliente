# Research: effective agent workflows for game and web 3D

Researched **7 October 2026**, browsing primary documentation and inspiration with **Obscura**. Rankings below are practical judgments about control, editability, automation, portability, and iteration cost. They are not measured vendor-quality benchmarks. No paid generation, Blender installation, bridge installation, or production publishing was performed.

## Recommendation

For original reusable assets, make **Blender Python → editable `.blend` + GLB → validation/optimization → actual runtime preview** the default. Blender exposes scene/mesh/material data through Python and can run scripts in background processes. GLB carries meshes, PBR materials, skinning, and animation into supporting runtimes. This makes the work reproducible and gives the agent precise ways to revise proportions and exports. [Blender API](https://docs.blender.org/api/current/info_quickstart.html), [CLI](https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html), [glTF exporter](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html).

The efficient route changes with the task: direct procedural Three.js for simple web shapes; an existing suitable licensed mesh for rapid game prototypes; AI generation plus cleanup for complex first drafts. Animated organic characters add topology, skeleton, weights, and deformation testing whichever route supplies the initial shape.

## Most useful tools and methods

| Priority | Tool / method | Best use | Strength for an agent | Practical limit |
| --- | --- | --- | --- | --- |
| 1 | **Blender + Python** | Custom props, figures, kits, cleanup, rigs | Precise code-based editing, editable source, repeatable export/render | Needs installed Blender; realistic anatomy/deformation requires modeling work |
| 2 | **Three.js** | Parametric web objects, custom viewers, browser games | Direct geometry/interaction in JavaScript; loads GLB | Rendering/runtime toolkit, not advanced mesh authoring |
| 3 | **`<model-viewer>`** | A single online figure or product | Simple orbit/zoom integration, poster, optional AR | Creates a viewer; the asset still needs an authoring route |
| 4 | **Kenney / Poly Haven** | Prototypes, coherent kits, realistic materials/props | Often removes unnecessary modeling; inspectable licensing | Existing art can miss a custom brief or exceed mobile budgets |
| 5 | **Meshy image-to-3D + Blender cleanup** | Organic or complex draft shapes | Documented async API, multiple views, PBR and GLB exports | Credits/rights, uncertain hidden geometry, topology/rigging cleanup |
| 6 | **Community MCP for Blender** | Iterating in an open Blender scene | Documented Claude Code integration and scene/visual inspection | Requires setup; community bridge, not a separate modeling engine |
| 7 | **glTF Transform + Khronos validation** | Reliable portable delivery | Inspects, validates, simplifies, compresses exports | Not an authoring tool; compression must match loader support |

Sources for rows 2–7: [Three.js GLTFLoader](https://threejs.org/docs/#GLTFLoader), [`<model-viewer>`](https://modelviewer.dev/), [Kenney Mini Dungeon](https://kenney.nl/assets/mini-dungeon), [Poly Haven](https://polyhaven.com/), [Meshy](https://docs.meshy.ai/en/api/image-to-3d), [MCP for Blender](https://github.com/ahujasid/mcp-for-blender), [glTF Transform](https://gltf-transform.dev/cli), [Khronos glTF-Validator](https://github.com/KhronosGroup/glTF-Validator).

## Workflow by deliverable

- **Stylized game prop or figure:** scripted Blender blockout → proportion/detail pass → exportable materials → GLB or established engine format → actual game import.
- **Animated humanoid:** suitable base/reference → topology cleanup → skeleton/weights → motion/deformation tests → named clips → engine import. Meshy auto-rigging documents a narrower textured-humanoid scope; it is not universal creature rigging. [Rigging limits](https://docs.meshy.ai/en/api/rigging).
- **One online figure:** optimized GLB + poster → `<model-viewer>` → real touch/keyboard/mobile/loading checks.
- **Interactive browser scene/game:** procedural shapes or imported GLBs → existing Three.js/Babylon runtime → interaction/collision/animation integration → measured frame time/loading.
- **Many related assets:** parameterized Blender generator / Geometry Nodes → reusable exported pieces → runtime instancing where appropriate.
- **Complex organic draft:** consistent reference image(s) → authorized AI candidate → Blender cleanup/retopology → export and inspect. Meshy's multi-image endpoint documents 1–4 views of the same object. [Multi-image API](https://docs.meshy.ai/en/api/multi-image-to-3d).

## Format and delivery findings

GLB/glTF is a strong web and Godot default. Godot explicitly recommends glTF 2.0; direct `.blend` import invokes Blender behind the scenes and requires it installed. Unity/Unreal delivery should follow the configured importer, often FBX for established mesh/rig pipelines. OBJ/STL are poor defaults for a textured animated web figure because they do not preserve the same capabilities. [Godot formats](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html), [Blender glTF](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html), [Unreal FBX](https://dev.epicgames.com/documentation/en-us/unreal-engine/fbx-content-pipeline).

Exporter materials/extensions need verification: arbitrary Blender shader nodes are not portable shader programs, and quads become triangles. glTF Transform recommends inspection before choosing optimizations. Khronos validates schema, resource, accessor, animation, and image details, but visual correctness still needs the target viewer. [Exporter](https://docs.blender.org/manual/en/4.5/addons/import_export/scene_gltf2.html), [Optimization guidance](https://gltf-transform.dev/cli), [Validator scope](https://github.com/KhronosGroup/glTF-Validator).

## Inspiration

- **Readable stylized silhouettes:** [Kenney Mini Dungeon](https://kenney.nl/assets/mini-dungeon). The Obscura viewport showed a coherent miniature kit with chunky architecture, restrained palettes, props, and small characters. Useful direction for game assets that must read at small screen sizes. The page labels the pack CC0 and lists animation/character-rig updates.
- **Realistic surfaces and neutral lighting:** [Poly Haven](https://polyhaven.com/). HDRI/PBR/prop categories offer references for materials and lighting. Public assets are labeled CC0. Reduce resolution/complexity for the target rather than blindly taking the largest download.
- **Object-first online presentation:** [`<model-viewer>` examples](https://modelviewer.dev/). The GLB/poster/camera-controls pattern is a useful starting point for inspectable figures; AR is a separate optional feature.
- **Editable AI-assisted scene construction:** [MCP for Blender](https://github.com/ahujasid/mcp-for-blender). Useful inspiration for a model–inspect–revise loop with deterministic source and runtime checks.

## Advanced option and research limits

[TRELLIS.2](https://github.com/microsoft/TRELLIS.2) is a documented self-hosted image-to-3D option. Its readme specifies tested Linux support, NVIDIA GPU with at least 24 GB, and CUDA; speed examples use an H100. It is not a default local route on macOS; verify compatible infrastructure before choosing it.

Obscura could not complete Tripo's protected homepage/API application, so no current Tripo API or comparative quality claim is made. Three.js uses iframe documentation; actual GLTFLoader iframe content was read, including decoder/extension requirements. Epic's navigation timed out but returned readable FBX pipeline text with document-tree errors; importer-version details should be rechecked before implementation. Blender's `latest` exporter URL returned 404, so the working 4.5 LTS exporter manual was used alongside current Python/CLI documentation.

No generation quality/speed benchmark was run. Blender was unavailable in the research environment, so no Blender export was executed. Recheck tool availability in the environment where the skill is used. The skill's standalone inventory helper is tested separately; this research does not claim Blender/AI/engine integration tests passed.
