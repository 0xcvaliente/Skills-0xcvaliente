#!/usr/bin/env bash
# Draft helper: report whether CLAUDE.md (primary) and AGENTS.md exist at repo root.
set -euo pipefail

for f in CLAUDE.md AGENTS.md; do
  if [[ -f "$f" ]]; then
    echo "$f found"
  else
    echo "$f not found"
  fi
done
