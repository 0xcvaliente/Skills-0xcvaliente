# Hatch Pet

`hatch-pet` creates, repairs, validates, and packages animated pets for the Codex v2 spritesheet format. It accepts a character concept, existing art, reference images, or brand cues and carries that identity through generation, deterministic assembly, visual review, and packaging.

This is a substantial production workflow rather than a single image prompt. Generated strips supply the artwork; local scripts provide exact cell geometry, extraction, registration, transparency cleanup, atlas assembly, and review artifacts.

## When to use it

Use it to make a new Codex pet, create a mascot in a non-pixel style, adapt approved art, upgrade an older atlas, or repair an existing v2 pet. Styles can include pixel art, plush, clay, sticker, flat vector, toy-like 3D, or painterly treatments when the character remains readable at pet size.

For a bare company or product name, the workflow first researches visual and personality cues. Concrete mascot descriptions and supplied references normally bypass that discovery stage.

## Format and behavior

The final atlas has **8 columns and 11 rows**, with **192 × 208 pixel cells**, for a total image size of **1536 × 2288 pixels**. Packaging declares `spriteVersionNumber: 2`.

Rows 0–8 contain the standard states: `idle`, `running-right`, `running-left`, `waving`, `jumping`, `failed`, `waiting`, `running`, and `review`. Here `running` represents active task work; directional running rows represent left or right movement.

Rows 9–10 contain sixteen clockwise look directions at 22.5-degree intervals. `000` means up; neutral/front is a separate reference. The intermediate 8 × 9 atlas is used during assembly and is not the final package for a new pet.

## How it works

1. Establish the identity, style, inputs, and working folder; research brand cues only when needed.
2. Generate a canonical base with an available image-generation tool or MCP server, or start from art the user supplies.
3. Generate grounded standard-state row strips and perform incremental checks. An approved right-running row can be mirrored with the dedicated helper when that is safe for the character.
4. Write the look-mechanics plan and establish four cardinal anchors.
5. Generate coherent eight-pose look rows, register them deterministically, and validate their geometry, labeled directions, and continuity.
6. Assemble the extended atlas, perform its defined chroma-cleanup pass, and run deterministic validation.
7. Complete labeled and blind direction review, motion previews, and final visual QA before packaging.

Repair targets the smallest failed row while preserving approved material. The instructions distinguish semantic artwork failures from extraction or geometry failures so deterministic problems do not cause unnecessary regeneration.

## Requirements and output

This skill targets the Codex app's pet format (8x11 atlas, `spriteVersionNumber: 2`); it can be run from any compatible agent host. The workflow needs an image-generation tool or MCP server that accepts reference images, or user-supplied art for each visual job; image generation is not assumed to be built into the host. Without either, the agent prepares the prompts, layout guides, and job manifest, then stops and lists the images to provide; it never draws sprites in code or claims an image was generated. The scripts need Python 3 with Pillow (use an interpreter already installed on the machine or in a virtualenv) and the parent steps use `jq`. The full workflow also uses lightweight subagents for generation and review when the host provides them (otherwise the same jobs run sequentially); brand-only discovery needs web search.

Typical outputs include `pet.json`, the transparent extended spritesheet, validation reports, contact sheets, animation previews, direction-semantics results, blind-review records, continuity results, and a final run summary. Generation and review can take substantial time; the instructions' time target is a planning aid rather than a QA shortcut.

Deterministic checks establish geometry and cleanup. They do not replace semantic and motion review, including readable directions, stable identity, real loop variation, and absence of accidental transparent holes.

## Example requests

```text
Use the hatch-pet skill: create a plush fox pet from this reference, preserve
its scarf, and package all standard states and look directions.

Use the hatch-pet skill: repair the look-direction rows in this v2 atlas while
preserving its approved standard animation rows.
```

## Package guide

- [SKILL.md](SKILL.md): complete production workflow, worker contracts, repair rules, and acceptance criteria.
- [Animation rows](references/animation-rows.md): state and frame contract.
- [Codex pet contract](references/codex-pet-contract.md): packaging expectations.
- [QA rubric](references/qa-rubric.md): visual acceptance guidance.
- [scripts/](scripts/): preparation, extraction, registration, composition, cleanup, validation, and preview tools.
- [tests/](tests/): regression coverage for assembly, chroma processing, and directional QA policies.
- [LICENSE.txt](LICENSE.txt): license text.

## Install and use

Copy this folder into a shared skills directory so it lives at `~/.agents/skills/hatch-pet/`:

```bash
mkdir -p ~/.agents/skills
cp -R hatch-pet ~/.agents/skills/
```

Your agent selects the skill automatically from its description, or name it in the prompt ("use the hatch-pet skill"). Finished pets are written to the Codex app's pets folder (`${CODEX_HOME:-$HOME/.codex}/pets/<pet-name>/`), since the output is the Codex app pet format. See [INSTALL.md](../../INSTALL.md) for host-specific skill folders.
