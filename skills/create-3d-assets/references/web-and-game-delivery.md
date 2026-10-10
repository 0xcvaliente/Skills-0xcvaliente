# Web and game delivery

Read for online model viewers, browser games, optimization, and native-engine handoff.

## Choose a viewer

Use `<model-viewer>` for a single model with standard orbit/zoom controls, posters, hotspots, and optional AR. Bundle/pin the component using the project's build system. Size the element explicitly and provide a real poster and useful `alt` text. A minimal element is:

```html
<model-viewer src="/models/asset.glb" poster="/images/asset-poster.webp"
  alt="Description of the displayed figure" camera-controls touch-action="pan-y">
</model-viewer>
```

Import the component before use; the element alone does not install it. Configure loading and error behavior. Enable rotation or animation only when it helps and respects motion preferences. AR needs its own device/format testing; do not infer AR support from successful desktop rendering.

Use the project's Three.js/Babylon.js runtime for custom interactions, multiple objects, shaders, or a browser game. Keep React Three Fiber only when it fits an existing React architecture. Do not add React solely to display a GLB. For procedural web-only shapes, use the runtime's geometry directly; preserve a generator and export with a supported exporter if the user also needs a portable mesh. Shader appearance may need baking or documented runtime recreation.

Three.js GLB loading starts with an explicit addon import:

```js
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
const gltf = await new GLTFLoader().loadAsync('/models/asset.glb');
scene.add(gltf.scene);
```

This is a loading fragment, not a complete viewer. Fit camera/controls to loaded world-space bounds; choose near/far planes from object scale. Use neutral lighting/environment and deliberate color-management/tone-mapping settings from the installed runtime. For animation, select actual clip names and update the mixer using elapsed time.

## Export compatibility

| Target | Delivery choice | Check |
| --- | --- | --- |
| Web viewer / Three.js / Babylon.js | GLB/glTF 2.0 | Materials, required extensions, decoders, external resources, animation |
| Godot | GLB/glTF 2.0 recommended | Actual import, materials, skeleton/clips, scale, collision |
| Unity / Unreal | Project's established importer, commonly FBX for meshes/rigs | Installed engine/importer version, axes/units, rig mapping, material conversion |
| Static mesh exchange only | OBJ can be appropriate if requested | Textures/MTL and format limits; no assumption of skeletal animation |

Retain `.blend`/generator as editable source. Do not choose STL for a textured animated online figure. Import formats do not encode the whole game setup: attach collision shapes, sockets, gameplay state, and rig mapping separately as needed. Prefer simple collision geometry for dynamic bodies; a render mesh is not automatically a good collider.

## Optimize from measurements

Record file/transfer size, exported triangles, mesh primitives/materials, texture dimensions, runtime draw calls, and frame time. Primitive count is only a clue about draw calls; instancing, shadow passes, and batching change the result. Derive budgets from simultaneous visible assets, devices, quality goals, and existing project measurements. Texture memory and expensive transparency/shadows can dominate even when triangles are low.

Use `gltf-transform inspect` first. Its `validate` command checks the specification. Deduplicate/prune, reduce textures, and use simplification/LODs where appearance survives. Do not flatten/join a hierarchy needed for animation/gameplay, or remove small identifying features. Keep input/output separate and compare rendered exports.

Choose compression according to the target loader: Draco requires a DRACOLoader, Meshopt requires a compatible decoder, and KTX2 textures require a KTX2Loader with device support detection in Three.js. Pin versions and make decoder/transcoder files reachable under the deployed base path/CSP. A smaller download can increase startup cost; measure the full load. Validate and visually check optimized output as well as the baseline.

## Browser verification

Serve previews over HTTP using the existing development server when possible. Verify actual model/image/decoder responses; do not rely on `file://` paths. Provide bounded loading feedback, useful failure text/retry, and a static poster fallback for unavailable graphics. Preserve readable surrounding content.

For a showcase, render on demand while static; run a bounded loop for interaction/animation and pause off-screen or hidden. Fit pixel ratio and shadows to the target device. Handle resize and graphics-context failures; release owned geometry, materials, textures, controls, observers, mixers, and renderer resources on disposal. Shared resources need ownership checks, and image bitmaps need explicit handling. Avoid duplicate canvases/listeners after remount.

Check mouse, keyboard, touch, vertical page scrolling, focus, narrow screens, reduced motion, and save-data behavior where applicable. Do not require motion to understand the asset. Gameplay can need a continuous loop; showcase lifecycle rules should not break game simulation. Use browser evidence from the target engine. Obscura can read sources/inspiration, but its independent engine does not establish Chromium/WebKit performance or compatibility.

Primary references: [`<model-viewer>`](https://modelviewer.dev/), [Three.js GLTFLoader](https://threejs.org/docs/#GLTFLoader), [glTF Transform CLI](https://gltf-transform.dev/cli), [Khronos validator](https://github.com/KhronosGroup/glTF-Validator), [Godot formats](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html), [Unreal FBX pipeline](https://dev.epicgames.com/documentation/en-us/unreal-engine/fbx-content-pipeline).
