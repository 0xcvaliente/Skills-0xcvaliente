# agent-skills-0xcvaliente

A curated library of 45 **host-neutral** [Agent Skills](https://agentskills.io) maintained by 0xcvaliente. They work in any agent that loads the open `SKILL.md` format (Claude Code, Codex, Gemini CLI, GitHub Copilot, Cursor, OpenCode and dozens more), and read fine as plain Markdown in a chat that has no skills support. They cover UI design and motion, Figma-to-code, React/Next.js, Swift, engineering workflow, security review, and founder/business work.

This repository is the model-agnostic successor to [`claude-skills-0xcvaliente`](https://github.com/0xcvaliente/claude-skills-0xcvaliente) and [`codex-skills-deprecated`](https://github.com/0xcvaliente/codex-skills-deprecated). Wording that tied a skill to one product (tool names, install paths, slash commands) is replaced by the capability vocabulary in [docs/capability-map.md](docs/capability-map.md). Upstream sources, licenses and provenance records are kept as published; see [docs/origins.md](docs/origins.md).

A **skill** is a folder with a `SKILL.md`. Its frontmatter (`name`, `description`) tells the agent what the skill does and when to use it. The body holds instructions, plus optional `references/`, `scripts/` and `assets/` the agent reads only when needed. Installing a skill adds no runtime code to your projects.

## Contents

- [Quick start](#quick-start)
- [How to use the skills](#how-to-use-the-skills)
- [Skill catalog](#skill-catalog)
- [Requirements by skill](#requirements-by-skill)
- [Anatomy of a skill](#anatomy-of-a-skill)
- [Contributing and validation](#contributing-and-validation)
- [Licensing](#licensing)

## Quick start

```sh
git clone https://github.com/0xcvaliente/agent-skills-0xcvaliente.git
cd agent-skills-0xcvaliente
scripts/install.sh --target agents          # ~/.agents/skills: Codex, Gemini CLI, Copilot, OpenCode, ...
scripts/install.sh --target claude          # ~/.claude/skills: Claude Code
```

Skills are symlinked, so `git pull` updates them. Start a new agent session afterwards. Per-host folders, project-level installs and the no-skills fallback are in [INSTALL.md](INSTALL.md).

## How to use the skills

**Automatically.** Describe the task normally. The agent matches your request against each installed skill's `description` and loads the one that fits.

| You say | Skill that loads |
|---|---|
| "The settings sheet feels janky when I drag it on iPhone" | `mobile-native`, `animate` |
| "Build this Figma frame: https://figma.com/design/…" | `figma-implement-design` |
| "Is this PR doing more than it needs to?" | `ponytail` |
| "Threat model the API in `services/api`" | `security-threat-model` |
| "Help me price the Pro tier" | `founder` |
| "What's that effect where the list items come in one after another?" | `animation-vocabulary` |

**Explicitly.** Name the skill in the prompt: "use the `ui-design` skill to audit `src/components/Checkout.tsx`". Most hosts also offer shorthand (`/ui-design` in Claude Code and Cursor, `$ui-design` in Codex).

### Tips

- **Pick the narrowest skill.** Many skills come in *build* / *review* / *plan* sets. Each description names its sibling: `animate` implements motion, `review-animations` critiques a diff, `improve-animations` produces a roadmap, `find-animation-opportunities` only locates where motion belongs.
- **Skills don't grant permissions.** A skill may tell the agent to run a script or open a browser; your host's permission settings still apply.
- **Review-only skills don't edit unless asked.** `break-ui`, `review-animations`, `find-animation-opportunities`, `security-*` and `ui-verification` report findings; ask for fixes explicitly.
- **Fewer installed skills means sharper matching.** Install only the categories you use.
- **Missing capability?** If your host has no subagents, browser, or image tool, the skill says what to do instead and what stays unverified. See [docs/capability-map.md](docs/capability-map.md).

## Skill catalog

### Design and UI

| Skill | Use it to | Example prompt |
|---|---|---|
| [`frontend-design`](skills/frontend-design) | Choose a distinctive visual direction (type, color, layout) instead of a templated default. | "Design a landing page for a coffee roastery that doesn't look like a SaaS template" |
| [`ui-design`](skills/ui-design) | Build React/Next/Tailwind UI and audit visual and interaction defects: design systems, dark mode, responsiveness, "UI slop". | "Extract our design system and add dark mode" |
| [`web-experience-design`](skills/web-experience-design) | Plan and build a whole coherent site or product experience, including cinematic and 3D web. | "Plan and build the new portfolio homepage" |
| [`web-design-guidelines`](skills/web-design-guidelines) | Review or implement against accessibility, forms, responsive layout, theming, and front-end performance rules. | "Check the signup form against web interface guidelines" |
| [`emil-design-eng`](skills/emil-design-eng) | Polish details in Emil Kowalski's style: feedback, spacing, typography, shadows, motion continuity. | "Polish this dropdown so it feels crafted" |
| [`apple-design`](skills/apple-design) | Apply Apple-style fluid motion: gestures, sheets, momentum, translucent materials. | "Make this bottom sheet feel like iOS" |
| [`pick-ui-library`](skills/pick-ui-library) | Choose a library for a UI capability from a curated shortlist, respecting existing dependencies. | "Which library should I use for a command palette?" |
| [`prototype`](skills/prototype) | Build several genuinely different variants of a UI behind a working picker. | "Give me three variants of the pricing table to compare" |
| [`break-ui`](skills/break-ui) | Stress-test a component with worst-case data, locales, and missing media; reports what breaks. | "Break the ProjectCard with long titles and empty images" |
| [`ui-verification`](skills/ui-verification) | Run browser probes for focus, hit targets, overflow, themes, failed requests, and performance. | "Verify the nav fix in the browser" |
| [`mobile-native`](skills/mobile-native) | Fix mobile web/PWA issues: sticky hover, `100vh`, input zoom, safe areas, keyboard layout. | "Inputs zoom in on iOS and the footer jumps under the keyboard" |
| [`diagram-craft`](skills/diagram-craft) | Produce polished, editable SVG/HTML diagrams (architecture, flows, sequences, states) from code or notes. | "Draw a sequence diagram of the checkout flow from this code" |

### Motion and animation

| Skill | Use it to | Example prompt |
|---|---|---|
| [`animate`](skills/animate) | Implement web UI motion with purposeful timing, interruption, exits, and reduced motion. | "Animate the modal open and close" |
| [`animate-expo`](skills/animate-expo) | Build React Native/Expo animations, gestures, sheets, and haptics with Reanimated. | "Add a swipe-to-dismiss card in Expo" |
| [`animation-vocabulary`](skills/animation-vocabulary) | Name a motion effect from a description. | "What's it called when a button squishes on press?" |
| [`find-animation-opportunities`](skills/find-animation-opportunities) | List the state changes that deserve motion and the ones that should stay instant. Read-only. | "Where should this dashboard animate?" |
| [`review-animations`](skills/review-animations) | Critique an animation diff or component and return a verdict. | "Review the motion in this PR" |
| [`improve-animations`](skills/improve-animations) | Audit motion across a codebase and produce prioritized improvement plans. | "Give me a motion roadmap for the app" |
| [`ui-animation`](skills/ui-animation) | Reverse-engineer motion from recordings, fit easing and springs, diagnose jank, add sparse UI sound. | "Match the easing in this screen recording" |
| [`gsap-core`](skills/gsap-core) | Work with GSAP tweens, easing, staggers, and responsive or reduced motion. | "Stagger the hero letters with GSAP" |
| [`gsap-react`](skills/gsap-react) | Use GSAP in React/Next.js with `useGSAP`, scoping, and cleanup. | "My GSAP animation runs twice in Next.js dev" |
| [`gsap-scrolltrigger`](skills/gsap-scrolltrigger) | Build scroll-driven scrubbing, pinning, and refresh handling. | "Pin the section and scrub the image on scroll" |
| [`gsap-timeline`](skills/gsap-timeline) | Sequence with timelines, labels, nesting, and playback controls. | "Build an intro timeline with pause and replay" |

### Figma

These skills require the Figma MCP server.

| Skill | Use it to | Example prompt |
|---|---|---|
| [`figma`](skills/figma) | Fetch design context, screenshots, variables, and assets; set up the Figma MCP. | "Pull the variables from this Figma file" |
| [`figma-implement-design`](skills/figma-implement-design) | Turn a Figma node into production code with 1:1 fidelity. | "Implement this frame: <figma URL>" |
| [`figma-create-design-system-rules`](skills/figma-create-design-system-rules) | Generate project-specific rules for future Figma-to-code work. | "Create design system rules for this repo" |

### Frameworks and languages

| Skill | Use it to | Example prompt |
|---|---|---|
| [`vercel-react-best-practices`](skills/vercel-react-best-practices) | Review React/Next.js for performance, rendering correctness, bundle size, and server/client boundaries. | "Why is this page shipping so much JS?" |
| [`payload`](skills/payload) | Work with Payload CMS collections, access control, hooks, Local API, migrations, and Next.js integration. | "Add a localized `projects` collection with drafts" |
| [`ask-sonner`](skills/ask-sonner) | Set up and style Sonner toasts, promise toasts, stacking, and themes. | "Show a loading toast that resolves when the save finishes" |
| [`write-swift`](skills/write-swift) | Write, review, or migrate Swift: concurrency, ownership, generics, Swift Testing. | "Migrate this class to Swift 6 strict concurrency" |

### Engineering workflow and architecture

| Skill | Use it to | Example prompt |
|---|---|---|
| [`ponytail`](skills/ponytail) | Make the smallest complete change; review for over-engineering (lite/full/ultra modes). | "/ponytail simplest fix for this bug" |
| [`pstack`](skills/pstack) | Run a full investigate → design → implement → adversarial review → verify → PR workflow. | "Use pstack to fix the flaky upload" |
| [`repo-context`](skills/repo-context) | Orient in an unfamiliar repo with compact architecture notes checked against source. | "Get oriented in this repo before we change auth" |
| [`codegraph`](skills/codegraph) | Trace cross-file calls and change impact with a local CodeGraph index, or set it up. | "What breaks if I change `getSession`?" |
| [`codebase-design`](skills/codebase-design) | Design deep modules: interfaces, seams, testability. | "Where should the seam go between billing and orders?" |
| [`domain-modeling`](skills/domain-modeling) | Sharpen domain terms and maintain `GLOSSARY.md`, `CONTEXT.md`, and ADRs. | "Record an ADR for switching to Postgres" |

### Security

| Skill | Use it to | Example prompt |
|---|---|---|
| [`security-best-practices`](skills/security-best-practices) | Review Python, JavaScript/TypeScript, or Go for language- and framework-specific security practice. | "Security review the Express routes" |
| [`security-threat-model`](skills/security-threat-model) | Write a repo-grounded threat model: trust boundaries, assets, abuse paths, mitigations. | "Threat model this repo" |
| [`strix`](skills/strix) | Run evidence-led app security assessments (web/API, OWASP), triage Strix reports, set up security CI. | "Pentest the staging API (I own it)" |

Run security assessments only against systems you own or are authorized to test.

### Business and founder work

| Skill | Use it to | Example prompt |
|---|---|---|
| [`founder`](skills/founder) | Validate ideas and make product, pricing, go-to-market, sales, finance, and fundraising decisions from evidence. | "Is this idea worth building? Here's the pitch…" |
| [`business-sales-documents`](skills/business-sales-documents) | Write and design proposals, company profiles, catalogs, one-pagers, reports, and pitch decks, ready for print. | "Make a 2-page sales brochure for our service" |
| [`outlook-email-automation`](skills/outlook-email-automation) | Set up and browser-test Outlook sending and follow-up automation with Power Automate. | "Automate a follow-up email 3 days after no reply" |

### Documents and files

| Skill | Use it to | Example prompt |
|---|---|---|
| [`documents`](skills/documents) | One skill with five bundled sub-skills: **docs** (reports, proposals, memos, specs to read, share, review), **word** (`.docx`), **spreadsheets** (`.xlsx`/`.csv`), **slides** (`.pptx`), **pdf**. Includes dependency-free inspect, pack/unpack, render, formula-check and PDF scripts. | "Turn this brief into a proposal as Word and PDF", "Fix the formula errors in this workbook", "Fill this PDF form" |

### Creative assets

| Skill | Use it to | Example prompt |
|---|---|---|
| [`create-3d-assets`](skills/create-3d-assets) | Create, optimize, and verify real 3D meshes/GLB for games or web viewers. | "Make a low-poly lamp GLB for the Three.js scene" |
| [`hatch-pet`](skills/hatch-pet) | Create and validate Codex-app animated pets (8×11 spritesheet, v2). The output format is specific to the Codex app; the workflow is host-neutral. | "Hatch a pet from this mascot art" |

## Requirements by skill

Most skills are instructions only and need nothing extra. These ones depend on tools:

| Skill | Needs |
|---|---|
| `figma`, `figma-implement-design`, `figma-create-design-system-rules` | Figma MCP server connected to your agent (setup in `skills/figma/references/figma-mcp-config.md`) |
| `ui-verification`, `strix`, `outlook-email-automation`, `diagram-craft` | A browser automation tool (Playwright, a browser MCP server, or the desktop app's browser pane) |
| `ui-animation` | Python 3, `ffmpeg` (`brew install ffmpeg`), `pip install opencv-python numpy scipy` |
| `create-3d-assets` | Blender for mesh work; Python 3 for `scripts/inspect_gltf.py` |
| `hatch-pet` | Python 3 and an image generation/editing tool |
| `codegraph` | The CodeGraph CLI and an indexed repository (see `skills/codegraph/references/setup.md`) |
| `repo-context`, `pstack`, `founder`, `business-sales-documents`, `diagram-craft` | Python 3.9+ for their bundled helper scripts |
| `documents` | Python 3.9+ for the bundled scripts (standard library only). Optional, by task: `python-docx`, `openpyxl`, `python-pptx`, `pypdf`, `reportlab`, LibreOffice, Poppler, pandoc. `scripts/doctor.py` reports what is installed |

## Anatomy of a skill

```text
skills/<name>/
├── SKILL.md            # Required. Frontmatter (name, description) + instructions
├── README.md           # Human-facing overview (optional)
├── references/         # Detailed guides the agent reads on demand
├── scripts/            # Helper scripts (Python, shell, Node)
├── assets/             # Templates, presets, images
├── tests/              # Tests for the scripts
└── LICENSE / NOTICE    # Upstream license, kept with the skill
```

Only the frontmatter is always in context; the rest loads when the skill is used. Skills adapted from upstream sources keep `references/provenance.md` (and `source-manifest.json` / `upstream-SKILL.md.source`) recording where they came from and what changed. `references/agent-notes.md` (formerly `claude-notes.md`) holds the host-neutral runtime notes for the Emil Kowalski–derived set.

## Contributing and validation

```sh
python3 scripts/validate.py                  # all skills
python3 scripts/validate.py skills/animate   # one skill
```

The validator checks frontmatter, that `name` matches the folder, local links, and that active files carry no single-host wording (provenance, upstream sources and licenses are exempt). To add a skill: create `skills/<name>/SKILL.md`, keep `name` identical to the folder, write the `description` so any agent can tell when to use it and which sibling to use instead, put long material in `references/`, add a catalog row here, and run the validator.

## Licensing

This repository has no single license. Each skill keeps the license and notices it shipped with: see the `LICENSE`, `LICENSE.txt`, `NOTICE` or `licenses/` files inside each skill directory. Check them before redistributing.

## Not included

- Company- and project-specific skills, kept in a private companion repository.
- Host-supplied document skills (some hosts ship their own `docx`, `pdf`, `pptx`, `xlsx`). The `documents` skill here is an independent, original implementation and does not use or copy them.
