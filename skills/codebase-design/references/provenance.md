# Provenance

Original source: [mattpocock/skills](https://github.com/mattpocock/skills/tree/b0618bc436ad893b3c5e84e55fba86586d34a404/skills/engineering/codebase-design),
reviewed 2026-10-09 at `b0618bc436ad893b3c5e84e55fba86586d34a404`.
The upstream MIT [license](../LICENSE) is retained. The original codebase-design entrypoint is unchanged.

## Claude Code port

Ported from the Codex version on 2026-10-10. The README's install and usage sections target `~/.claude/skills/codebase-design/` and `/codebase-design`, the reference to the removed Codex `agents/openai.yaml` metadata was dropped, and DESIGN-IT-TWICE.md names the Agent tool for the parallel sub-agents. The entrypoint is still unchanged.

## Host-neutral adaptation

Made host-neutral for the Agent Skills standard on 2026-10-12. DESIGN-IT-TWICE.md now asks for the host's subagent facility (sequential work if none) instead of naming the Agent tool; README install and examples are host-neutral.
