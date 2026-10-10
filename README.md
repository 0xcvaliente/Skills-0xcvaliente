# claude-skills-0xcvaliente

A curated library of 44 [Claude Code](https://claude.com/claude-code) skills maintained by 0xcvaliente. They cover UI design and motion, Figma-to-code, React/Next.js, Swift, engineering workflow, security review, and founder/business work.

A **skill** is a folder with a `SKILL.md` file. The file's frontmatter (`name`, `description`) tells Claude what the skill does and when to use it. The body holds the instructions, plus optional `references/`, `scripts/`, and `assets/` that Claude reads only when it needs them. Installing a skill adds no runtime code to your projects. It only changes how Claude approaches a matching task.

## Contents

- [Quick start](#quick-start)
- [How to use the skills](#how-to-use-the-skills)
- [Skill catalog](#skill-catalog)
- [Requirements by skill](#requirements-by-skill)
- [Anatomy of a skill](#anatomy-of-a-skill)
- [Updating, adding, and removing skills](#updating-adding-and-removing-skills)
- [Troubleshooting](#troubleshooting)
- [Valiente MCP integration](#valiente-mcp-integration)
- [Licensing](#licensing)

## Quick start

1. Clone the repository:

   ```sh
   git clone https://github.com/0xcvaliente/claude-skills-0xcvaliente.git ~/Documents/Github-Projects/claude-skills-0xcvaliente
   ```

2. Install the skills you want into `~/.claude/skills/` (available in every project). **Symlinking** is recommended: a later `git pull` then updates the installed skills too.

   ```sh
   REPO=~/Documents/Github-Projects/claude-skills-0xcvaliente
   mkdir -p ~/.claude/skills

   # One skill
   ln -s "$REPO/skills/ui-design" ~/.claude/skills/ui-design

   # Every skill (skips names that already exist in ~/.claude/skills)
   for s in "$REPO"/skills/*/; do
     n=$(basename "$s")
     [ -e ~/.claude/skills/"$n" ] || ln -s "${s%/}" ~/.claude/skills/"$n"
   done
   ```

   To use a frozen copy instead, run `cp -R "$REPO/skills/<name>" ~/.claude/skills/`.

3. Start a new Claude Code session. Skills load at session start.

To scope a skill to a single project, put it in that project's `.claude/skills/<name>/`. You can commit it there so collaborators get it too.

## How to use the skills

There are two ways to use a skill.

**Automatically.** Describe the task normally. Claude matches your request against each installed skill's `description` and loads the skill that fits. Examples:

| You say | Skill that loads |
|---|---|
| "The settings sheet feels janky when I drag it on iPhone" | `mobile-native`, `animate` |
| "Build this Figma frame: https://figma.com/design/…" | `figma-implement-design` |
| "Is this PR doing more than it needs to?" | `ponytail` |
| "Threat model the API in `services/api`" | `security-threat-model` |
| "Help me price the Pro tier" | `founder` |
| "What's that effect where the list items come in one after another?" | `animation-vocabulary` |

**Explicitly.** Type `/<skill-name>` followed by your request, or name the skill in the prompt:

```text
/ui-design audit src/components/Checkout.tsx
/break-ui stress-test the ProjectCard component
/ponytail ultra review this diff
Use the diagram-craft skill to draw the request flow in docs/architecture.md
```

Use the explicit form when several skills overlap (for example `animate` vs. `review-animations` vs. `improve-animations`) and you want a specific one.

### Tips

- **Pick the narrowest skill.** Many skills are deliberately paired as *build* vs. *review* vs. *plan*. Each description says which sibling to use instead. For example, `animate` implements motion, `review-animations` critiques a diff, `improve-animations` produces a roadmap, and `find-animation-opportunities` only identifies where motion should go.
- **Skills don't grant permissions.** A skill can tell Claude to run a script or open a browser, but your normal Claude Code permission settings still apply.
- **Review-only skills don't edit unless asked.** `break-ui`, `review-animations`, `find-animation-opportunities`, `security-*`, and `ui-verification` report findings. Ask for fixes explicitly.
- **Fewer installed skills means sharper matching.** If unrelated skills keep triggering, install only the categories you use.

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

### Creative assets

| Skill | Use it to | Example prompt |
|---|---|---|
| [`create-3d-assets`](skills/create-3d-assets) | Create, optimize, and verify real 3D meshes/GLB for games or web viewers. | "Make a low-poly lamp GLB for the Three.js scene" |
| [`hatch-pet`](skills/hatch-pet) | Create and validate Codex app animated pets (8×11 spritesheet, v2). | "Hatch a pet from this mascot art" |

## Requirements by skill

Most skills are instructions only and need nothing extra. These ones depend on tools:

| Skill | Needs |
|---|---|
| `figma`, `figma-implement-design`, `figma-create-design-system-rules` | Figma MCP server connected to Claude Code (setup in `skills/figma/references/figma-mcp-config.md`) |
| `ui-verification`, `strix`, `outlook-email-automation`, `diagram-craft` | A browser automation tool (Playwright, a browser MCP server, or the desktop app's browser pane) |
| `ui-animation` | Python 3, `ffmpeg` (`brew install ffmpeg`), `pip install opencv-python numpy scipy` |
| `create-3d-assets` | Blender for mesh work; Python 3 for `scripts/inspect_gltf.py` |
| `hatch-pet` | Python 3 and an image generation/editing tool |
| `codegraph` | The CodeGraph CLI and an indexed repository (see `skills/codegraph/references/setup.md`) |
| `repo-context`, `pstack`, `founder`, `business-sales-documents`, `diagram-craft` | Python 3.9+ for their bundled helper scripts |

## Anatomy of a skill

```text
skills/<name>/
├── SKILL.md            # Required. Frontmatter (name, description) + instructions
├── README.md           # Human-facing overview (optional)
├── references/         # Detailed guides Claude reads on demand
├── scripts/            # Helper scripts Claude can run (Python, shell, Node)
├── assets/             # Templates, presets, images
├── tests/              # Tests for the scripts
└── LICENSE / NOTICE    # Upstream license, kept with the skill
```

Only the frontmatter `description` is always in Claude's context. The rest loads when the skill is used, so large reference folders cost nothing until then. Several skills are adapted from upstream sources. Their `references/provenance.md` (and `source-manifest.json` / `upstream-SKILL.md.source`) record where they came from and what changed.

## Updating, adding, and removing skills

**Update.** If you symlinked, run:

```sh
git -C ~/Documents/Github-Projects/claude-skills-0xcvaliente pull
```

Copied installs must be re-copied. Then start a new Claude Code session.

**Add a skill.**

1. Create `skills/<name>/SKILL.md`:

   ```markdown
   ---
   name: <name>
   description: What it does and when to use it. Name the situations that should trigger it, and the sibling skill to use instead when it shouldn't.
   ---

   # <Title>

   Instructions...
   ```

2. Keep `name` identical to the folder name.
3. Put long material in `references/`.
4. Add a row to the catalog above.
5. Symlink the skill into `~/.claude/skills/`.

**Remove a skill.** Run `rm ~/.claude/skills/<name>`. For a symlink, this removes only the link and leaves the repository copy.

## Troubleshooting

- **A skill never triggers.** Check that `~/.claude/skills/<name>/SKILL.md` exists. Then restart the session and invoke it explicitly with `/<name>`. If explicit use works but automatic doesn't, make the `description` more specific about when to use it.
- **The wrong skill triggers.** Invoke the one you want explicitly, or uninstall overlapping skills you don't use.
- **A script fails.** Check the [requirements](#requirements-by-skill). Script skills expect `python3` on `PATH`.
- **Broken symlinks after moving the repo.** Re-run the install loop with the new path.

## Valiente MCP integration

`founder`, `outlook-email-automation`, and `business-sales-documents` include a `references/valiente-mcp.md`. It describes how to use the private `valiente` MCP server (Slack, Notion, Google Drive, Outlook, OneDrive) when that server is connected. The skills treat retrieved content as untrusted data, and write actions (sending mail or messages, editing pages) require an explicit request. Without the server, these skills work from what you provide in the conversation.

## Licensing

This repository has no single license. Each skill keeps the license and notices it shipped with: see the `LICENSE`, `LICENSE.txt`, `NOTICE`, or `licenses/` files inside each skill directory. Check them before redistributing.

## Not included

- Company- and project-specific skills, kept in a separate private repository.
- The account-synced document skills (`docs`, `docx`, `pdf`, `pptx`, `xlsx`), which come with your Claude account.
