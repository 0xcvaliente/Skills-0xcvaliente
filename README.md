# Skills-0xcvaliente

A curated library of 58 [Agent Skills](https://agentskills.io) maintained by 0xcvaliente. Most are **host-neutral**; 11 are Claude Code flavored (see [Claude Code flavored skills](#claude-code-flavored-skills)). They work in any agent that loads the open `SKILL.md` format (Claude Code, Codex, Gemini CLI, GitHub Copilot, Cursor, OpenCode and dozens more), and read fine as plain Markdown in a chat that has no skills support. They cover UI design and motion, Figma-to-code, React/Next.js, Swift, engineering workflow, security review, and founder/business work.

This repository consolidates the earlier Claude-specific, Codex-specific and host-neutral skill repositories (since retired; see [docs/origins.md](docs/origins.md)) into one host-neutral library; the Git history of the Claude-specific and host-neutral repositories is preserved here. Wording that tied a skill to one product (tool names, install paths, slash commands) is replaced by the capability vocabulary in [docs/capability-map.md](docs/capability-map.md). Upstream sources, licenses and provenance records are kept as published; see [docs/origins.md](docs/origins.md).

A **skill** is a folder with a `SKILL.md`. Its frontmatter (`name`, `description`) tells the agent what the skill does and when to use it. The body holds instructions, plus optional `references/`, `scripts/` and `assets/` the agent reads only when needed. Installing a skill adds no runtime code to your projects.

## Contents

- [Quick start](#quick-start)
- [How to use the skills](#how-to-use-the-skills)
- [Skill catalog](#skill-catalog)
- [Requirements by skill](#requirements-by-skill)
- [Anatomy of a skill](#anatomy-of-a-skill)
- [Updating, adding and removing skills](#updating-adding-and-removing-skills)
- [Troubleshooting](#troubleshooting)
- [Contributing and validation](#contributing-and-validation)
- [Licensing](#licensing)

## Quick start

```sh
git clone https://github.com/0xcvaliente/Skills-0xcvaliente.git
cd Skills-0xcvaliente
scripts/install.sh --target agents          # ~/.agents/skills: Codex, Gemini CLI, Copilot, OpenCode, ...
scripts/install.sh --target claude          # ~/.claude/skills: Claude Code
```

The installer symlinks each skill into `~/.claude/skills` (`--target claude`) and `~/.agents/skills` (`--target agents`), so `git pull` updates them. Existing copies are skipped unless you pass `--force`, which replaces them. Start a new agent session afterwards. Per-host folders, project-level installs and the no-skills fallback are in [INSTALL.md](INSTALL.md).

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
| [`design-taste-frontend`](skills/design-taste-frontend) | Anti-slop art direction (taste-skill v2.1) for public web pages and app screens (dashboards, admin views, settings): draws researched directions from a library, lints and browser-inspects the page, finds open-licence images, and runs a look-and-fix loop. | "Redesign this landing page so it doesn't look AI-generated" |
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
| [`diagram-craft`](skills/diagram-craft) | Produce polished, editable SVG/HTML diagrams (architecture, flows, sequences, states, service blueprints) from code or notes. | "Draw a sequence diagram of the checkout flow from this code" |

### Motion and animation

| Skill | Use it to | Example prompt |
|---|---|---|
| [`animate`](skills/animate) | Implement web UI motion with purposeful timing, interruption, exits, and reduced motion. | "Animate the modal open and close" |
| [`animate-expo`](skills/animate-expo) | Build React Native/Expo animations, gestures, sheets, and haptics with Reanimated. | "Add a swipe-to-dismiss card in Expo" |
| [`animation-performance`](skills/animation-performance) | Find why a web animation drops frames and fix it: composite-only properties, main-thread load, per-frame state. | "This drawer drag gets laggy as the list grows" |
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

### Claude Code flavored skills

These were imported from earlier Claude Code collections and keep Claude Code wording (tool names, `~/.claude` paths, hooks). They still read as plain Markdown elsewhere, but expect to adapt them on other hosts. Nine are adapted from [mattpocock/skills](https://github.com/mattpocock/skills) (see each `UPSTREAM.md`); `reverse-engineer-anything` is imported verbatim from [morluto/rea](https://github.com/morluto/rea).

| Skill | Use it to | Example prompt |
|---|---|---|
| [`diagnosing-bugs`](skills/diagnosing-bugs) | Run a diagnosis loop on hard bugs and performance regressions. | "Diagnose why the export job is slow" |
| [`tdd`](skills/tdd) | Build features or fix bugs test-first (red-green-refactor). | "Do this with red-green-refactor" |
| [`grilling`](skills/grilling) / [`grill-me`](skills/grill-me) | Get grilled on a plan, decision or idea until the gaps show (`grill-me` is the short interview form). | "Grill me on this migration plan" |
| [`handoff`](skills/handoff) | Compact the conversation into a handoff document for another agent. | "Hand this off to a fresh session" |
| [`to-questionnaire`](skills/to-questionnaire) | Turn a decision you can't fully answer into a questionnaire for someone else to fill in. | "Turn this open question into a questionnaire for the client" |
| [`wait-what`](skills/wait-what) | Re-pitch a message that didn't land, more clearly. | "Wait, what? Say that again" |
| [`writing-for-agents`](skills/writing-for-agents) | Write skills, `AGENTS.md` and `CLAUDE.md` that agents follow. | "Tighten this CLAUDE.md" |
| [`git-guardrails-claude-code`](skills/git-guardrails-claude-code) | Install Claude Code hooks that block dangerous git commands. | "Block git push and reset --hard" |
| [`update-mattpocock-skills`](skills/update-mattpocock-skills) | Check mattpocock/skills for upstream changes and merge them. | "Refresh the Matt Pocock skills" |
| [`reverse-engineer-anything`](skills/reverse-engineer-anything) | Reverse engineer native, Electron, packaged and browser targets with REA. | "How does this app's updater work?" |

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
| [`documents`](skills/documents) | One skill with six bundled sub-skills: **docs** (reports, proposals, memos, specs to read, share, review), **word** (`.docx`), **spreadsheets** (`.xlsx`/`.csv`), **slides** (`.pptx`), **pdf**, and **design** (typography, layout, colour, contrast, tables and charts, with four presets and starter builds). Includes dependency-free inspect, pack/unpack, render, formula-check, design-audit and PDF scripts, plus evals. | "Turn this brief into a proposal as Word and PDF", "Make this deck look professional", "Fix the formula errors in this workbook", "Fill this PDF form" |

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
| `design-taste-frontend` | Node 18+ for `draw`, `lint` and `assets` scripts; Node 22+ and a local Chrome, Edge or Chromium for `inspect.mjs`; network access for `assets.mjs` (open-licence image sources) |
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

## Updating, adding and removing skills

**Update.** Symlinked installs follow the repository: run `git pull` in your clone. Copied installs (`--copy` or a manual `cp -R`) must be re-copied, or re-run the installer with `--force` to replace them. Start a new agent session afterwards.

**Add.** Create `skills/<name>/SKILL.md` with `name` and `description` frontmatter, keep `name` identical to the folder, put long material in `references/`, add a catalog row, run `python3 scripts/validate.py`, then re-run the installer.

**Remove.** Delete the installed entry, for example `rm ~/.agents/skills/<name>` or `rm ~/.claude/skills/<name>`. For a symlink this removes only the link and leaves the repository copy.

## Troubleshooting

- **A skill never triggers.** Check that `<skills dir>/<name>/SKILL.md` exists in the folder your host reads (see [INSTALL.md](INSTALL.md)), restart the session, then invoke the skill by name. If explicit use works but automatic matching does not, make its `description` more specific about when to use it.
- **The wrong skill triggers.** Name the skill you want, or uninstall overlapping skills you do not use.
- **A script fails.** Check [Requirements by skill](#requirements-by-skill). Script-based skills expect `python3` on `PATH`.
- **Broken symlinks after moving the repository.** Re-run the installer with `--force` from the new location.
- **Installer skipped a skill.** The destination already exists; pass `--force` to replace it.

## Contributing and validation

```sh
python3 scripts/validate.py                  # all skills
python3 scripts/validate.py skills/animate   # one skill
```

The validator checks frontmatter, that `name` matches the folder, local links, and that active files carry no single-host wording (provenance, upstream sources and licenses are exempt; the Claude Code flavored skills only warn). For the official format check, `pip install skills-ref` and run `agentskills validate skills/<name>`. To add a skill: create `skills/<name>/SKILL.md`, keep `name` identical to the folder, write the `description` so any agent can tell when to use it and which sibling to use instead, put long material in `references/`, add a catalog row here, and run the validator.

## Licensing

This repository has no single license. Each skill keeps the license and notices it shipped with: see the `LICENSE`, `LICENSE.txt`, `NOTICE` or `licenses/` files inside each skill directory. Check them before redistributing.

## Not included

- Company- and project-specific skills, kept in a private companion repository.
- Host-supplied document skills (some hosts ship their own `docx`, `pdf`, `pptx`, `xlsx`). The `documents` skill here is an independent, original implementation and does not use or copy them.
