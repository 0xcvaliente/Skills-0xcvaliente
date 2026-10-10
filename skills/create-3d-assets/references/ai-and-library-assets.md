# AI and library assets

Read for licensed base models, reference-to-3D generation, and organic-character shortcuts.

## Existing assets

Use a well-suited library asset when it meets the brief and creation from scratch is unnecessary. Kenney is useful for coherent stylized game kits and some rigged characters; Poly Haven is useful for realistic props, PBR textures, and HDR lighting. Record the specific asset URL and included license, and inspect actual downloads. Do not assume every marketplace item has the same rights or technical quality.

The researched [Kenney Mini Dungeon](https://kenney.nl/assets/mini-dungeon) page labels its pack CC0 and lists animation/character rigs. [Poly Haven](https://polyhaven.com/) labels its public assets CC0. A photorealistic library mesh may still need geometry/material/texture reduction for a phone or browser. A library download is adaptation, not newly authored art; describe provenance accurately.

## AI draft workflow

Favor image-to-3D when silhouette/identity matters and useful images exist. Text-to-3D is suitable for loose concept exploration. This is a workflow judgment: the research did not run a controlled quality or speed comparison. Use consistent views of the same object; unrelated generated viewpoints can contradict each other. A single front image leaves hidden geometry uncertain.

Prepare an isolated full object/character, clear silhouette, neutral lighting, and visible limbs. Use a neutral A/T pose for a humanoid that will be rigged. Avoid perspective/crop/lighting that obscures shape. Generate a raster reference only if it helps the task and an image-generation tool is available; the reference is not the mesh deliverable.

Choose a service actually available in the session. Confirm task input schema, model IDs, export formats, remesh settings, credit cost, license/privacy, and asset retention from **current** provider documentation. Do not assume a web subscription includes API credits or that a plugin includes a 3D-generation tool. Preserve existing authorization and spend limits; a research-only request does not authorize paid calls.

Submit within the agreed finite candidate budget, retain the task ID, and poll that task with bounded waits. On timeout, retrieve status before considering another creation; do not accidentally purchase duplicate candidates. Save successful outputs before links expire. Do not expose keys or signed URLs in logs/manifests.

Inspect candidates on geometry and view consistency, not only the provider thumbnail. Import the best candidate into Blender and repair disconnected/fused parts, silhouette, normals, topology, UV seams, and materials. Rebuild rather than endlessly regenerate when a particular detail can be fixed directly. Remesh/decimate for static display as appropriate; deformation-sensitive joints can require retopology and rebaking. Then export and verify in the target runtime.

## Verified provider scope and limits

[Meshy's image-to-3D API](https://docs.meshy.ai/en/api/image-to-3d) documents GLB/FBX and other exports, PBR maps, remeshing, and pose controls. Its [multi-image API](https://docs.meshy.ai/en/api/multi-image-to-3d) accepts 1–4 consistent views. These are documented capabilities, not guaranteed shape accuracy.

Its [rigging API](https://docs.meshy.ai/en/api/rigging) documents textured standard humanoids with clear limbs, and excludes non-humanoids and untextured meshes. Verify the expected facing axis and face-count constraints. Do not promise this route for quadrupeds, fused limbs, unusual anatomy, or a polished animation rig without testing. Test bends, ground contact, clipping, and clip playback after automatic rigging.

Provider parameters changed during the research period. As observed on 7 October 2026, Meshy documented retirement of `meshy-5` on 10 October and `model_type: lowpoly` on 30 October, with a newer smart-topology route. Recheck instead of hardcoding these choices into reusable code. Provider face counts are not necessarily exported triangles.

Tripo remains a candidate if the user has a connected service; the research could not read its protected homepage or fully rendered API documentation in Obscura, so it is not ranked as a verified winner. Fetch current primary documentation before using it.

## Self-hosted generation

[Microsoft TRELLIS.2](https://github.com/microsoft/TRELLIS.2) documents image-to-3D with PBR output. Its researched prerequisites were Linux, NVIDIA GPU with at least 24 GB memory, and CUDA; the displayed timing table used an H100. Do not translate those timings to a Mac or assume Apple Metal support. Consider self-hosting when compatible infrastructure and a repeated workload justify setup; otherwise an available hosted service is simpler. Recheck code, model, and dependency licenses separately.

Gaussian splats or neural representations can make effective captured-scene viewers, but do not automatically provide an editable skinned mesh, collision surface, or ordinary game asset. Use them only when the requested deliverable fits their representation; explicitly plan conversion if the user needs a mesh.
