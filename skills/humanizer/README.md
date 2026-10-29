# humanizer

Rewrites AI-sounding prose so it reads like the writer, without changing what it says. Use it when editing or reviewing text for AI tells: not-X-but-Y contrasts, one-line closers, staged openers, forced triads, overused dashes, inflated claims, sales language, stock AI words, bold labels and filler. Based on Wikipedia's "Signs of AI writing."

This is humanizer v3.1.0 by Siqi Chen (blader), MIT, vendored from upstream at revision 0ef9fe5.

## Layout

- `SKILL.md`: the workflow and numbered pattern list (verbatim upstream).
- `LICENSE`: upstream MIT license (verbatim).
- `references/upstream-README.md.source`: the upstream README, kept verbatim for reference only. It contains host-specific install instructions.
- `references/provenance.md`: the import log, with the pin and the files left out.

`SKILL.md` and `LICENSE` are verbatim upstream. Only this README and `provenance.md` are local.

## Use

Works in any agent that loads Agent Skills (Claude Code, Codex, Gemini CLI, GitHub Copilot, Cursor, OpenCode and others), and reads fine as plain Markdown in a chat without skills support. Give it a draft, or ask it to review one; it needs no scripts, network access or extra tools.
