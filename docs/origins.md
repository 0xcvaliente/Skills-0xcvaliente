# Origins

Each skill keeps its upstream attribution and license. Where a package records its source (`references/provenance.md`, `source-manifest.json`, `upstream-SKILL.md.source`), this table repeats it. The adaptation history for most skills is: upstream source → Codex version in [`codex-skills-deprecated`](https://github.com/0xcvaliente/codex-skills-deprecated) → Claude Code version in [`claude-skills-0xcvaliente`](https://github.com/0xcvaliente/claude-skills-0xcvaliente) → this host-neutral version.

| Skills | Upstream | Notes |
|---|---|---|
| `animate`, `animate-expo`, `animation-vocabulary`, `apple-design`, `ask-sonner`, `break-ui`, `emil-design-eng`, `find-animation-opportunities`, `improve-animations`, `mobile-native`, `pick-ui-library`, `prototype`, `review-animations`, `write-swift` | [emilkowalski/skills](https://github.com/emilkowalski/skills) (pinned revision in each `source-manifest.json`) | MIT. Upstream entrypoint kept as `references/upstream-SKILL.md.source`. Host notes in `references/agent-notes.md`. |
| `codebase-design`, `domain-modeling` | [mattpocock/skills](https://github.com/mattpocock/skills) | Pinned revision in each `provenance.md`. |
| `ui-design`, `ui-verification`, `ui-animation` | [mblode/agent-skills](https://github.com/mblode/agent-skills) | Pinned revision in each `provenance.md`. |
| `gsap-core`, `gsap-react`, `gsap-scrolltrigger`, `gsap-timeline` | [greensock/gsap-skills](https://github.com/greensock/gsap-skills) | GreenSock's official GSAP skills; `SKILL.md` content unchanged. |
| `pstack` | [cursor/plugins](https://github.com/cursor/plugins) (`pstack`) | Poteto's pstack; original bytes preserved under `upstream/`. |
| `strix` | [usestrix/strix](https://github.com/usestrix/strix) | Authorization and ownership safeguards retained. |
| `ponytail` | [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) | |
| `diagram-craft` | [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) | |
| `frontend-design`, `figma`, `figma-implement-design`, `figma-create-design-system-rules`, `security-best-practices`, `security-threat-model`, `hatch-pet`, `codegraph` | Ship with their own `LICENSE`/`NOTICE` files | No upstream URL is recorded in the package; check the license file for the rights holder. |
| `founder`, `repo-context`, `business-sales-documents`, `outlook-email-automation`, `create-3d-assets`, `payload`, `vercel-react-best-practices`, `web-design-guidelines`, `web-experience-design` | Authored or curated in the 0xcvaliente collections | No external upstream recorded in the package. |

When you update a skill from its upstream, refresh the pinned revision and checksum in its `source-manifest.json` and add a dated line to `provenance.md`.
