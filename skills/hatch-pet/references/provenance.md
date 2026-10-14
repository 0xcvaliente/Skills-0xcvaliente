# Provenance

- Upstream: https://github.com/openai/skills (`skills/.curated/hatch-pet`)
- Derived from revision: c25113bf4c64c8dba6bfe61acf06051d79aa43f6 (2026-05-12, "Replace hatch-pet curated skill workflow (#399)")
- Upstream HEAD checked: 49f948faa9258a0c61caceaf225e179651397431; no upstream commits to this path after c25113b.
- 2026-10-15: reviewed, no upstream changes since c25113b.
- Local status: a substantially extended fork, not a copy. It targets the 8x11 v2 atlas, adds scripts (`assemble_extended_atlas.py`, direction QA and blind-verdict tools, `despill_chroma_edges.py`, cardinal anchor tools, `render_animation_previews.py`) and a `tests/` directory, and changes `SKILL.md`, three reference files, and several upstream scripts. Do not overwrite from upstream; port upstream changes by hand and review each against the local scripts.
- `LICENSE.txt` is retained unchanged and is not edited here.
