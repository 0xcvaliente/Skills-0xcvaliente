# Origins

Each skill keeps its upstream attribution and license. Where a package records its source (`references/provenance.md`, `source-manifest.json`, `upstream-SKILL.md.source`), this table repeats it. The adaptation history for most skills is: upstream source → Codex version (`codex-skills-deprecated`) → Claude Code version (`claude-skills-0xcvaliente`) → this host-neutral version. This repository is consolidated from `claude-skills-0xcvaliente`, `agent-skills-0xcvaliente` and `codex-skills-deprecated`, which have been retired.

| Skills | Upstream | Notes |
|---|---|---|
| `animate`, `animate-expo`, `animation-vocabulary`, `apple-design`, `ask-sonner`, `break-ui`, `emil-design-eng`, `find-animation-opportunities`, `improve-animations`, `mobile-native`, `pick-ui-library`, `prototype`, `review-animations`, `write-swift` | [emilkowalski/skills](https://github.com/emilkowalski/skills) (pinned revision in each `source-manifest.json`) | MIT. Upstream entrypoint kept as `references/upstream-SKILL.md.source`. Host notes in `references/agent-notes.md`. |
| `codebase-design`, `domain-modeling` | [mattpocock/skills](https://github.com/mattpocock/skills) | Pinned revision in each `provenance.md`. |
| `ui-design`, `ui-verification`, `ui-animation` | [mblode/agent-skills](https://github.com/mblode/agent-skills) | Pinned revision in each `provenance.md`. |
| `gsap-core`, `gsap-react`, `gsap-scrolltrigger`, `gsap-timeline` | [greensock/gsap-skills](https://github.com/greensock/gsap-skills) | GreenSock's official GSAP skills; `SKILL.md` content unchanged. |
| `pstack` | [cursor/plugins](https://github.com/cursor/plugins) (`pstack`) | Poteto's pstack; original bytes preserved under `upstream/`. |
| `strix` | [usestrix/strix](https://github.com/usestrix/strix) | Authorization and ownership safeguards retained. |
| `ponytail` | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | |
| `design-taste-frontend` | [leonxlnx/taste-skill](https://github.com/leonxlnx/taste-skill) | MIT. `SKILL.md` unchanged; pinned revision in `references/provenance.md`. Other skills in that pack are not included. |
| `diagram-craft` | [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) | |
| `frontend-design`, `figma`, `figma-implement-design`, `figma-create-design-system-rules`, `security-best-practices`, `security-threat-model`, `hatch-pet`, `codegraph` | Ship with their own `LICENSE`/`NOTICE` files | No upstream URL is recorded in the package; check the license file for the rights holder. |
| `documents` | Original work in this repository | Studied the *approach* of Anthropic's published `docx`/`pdf`/`pptx`/`xlsx` and `doc-coauthoring` skills ([anthropics/skills](https://github.com/anthropics/skills)): route by file type, work on structure not appearance, verify by rendering. Those skills are proprietary (all rights reserved) and **no text or code was copied**; every guide and script here is newly written. Format facts come from the public OOXML and PDF specifications and the libraries' own documentation. |
| `founder`, `repo-context`, `business-sales-documents`, `outlook-email-automation`, `create-3d-assets`, `payload`, `vercel-react-best-practices`, `web-design-guidelines`, `web-experience-design` | Authored or curated in the 0xcvaliente collections | No external upstream recorded in the package. |

When you update a skill from its upstream, refresh the pinned revision and checksum in its `source-manifest.json` and add a dated line to `provenance.md`.
