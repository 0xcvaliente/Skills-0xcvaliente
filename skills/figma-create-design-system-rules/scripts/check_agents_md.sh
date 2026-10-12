#!/usr/bin/env bash
# Draft helper: report which common agent instruction files exist at repo root.
# AGENTS.md is the cross-tool default; the others are read by specific hosts.
set -euo pipefail

for f in AGENTS.md CLAUDE.md GEMINI.md .github/copilot-instructions.md; do
  if [[ -f "$f" ]]; then
    echo "$f found"
  else
    echo "$f not found"
  fi
done
