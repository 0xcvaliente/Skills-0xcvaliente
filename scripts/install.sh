#!/usr/bin/env bash
# Install skills from this repo into one or more Agent Skills hosts.
# Usage: install.sh [--target agents,claude,gemini,copilot,opencode,project] [--dest DIR]
#                   [--copy] [--force] [--list] [skill ...]
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGETS="agents"; DEST=""; MODE="link"; FORCE=0; LIST=0; SKILLS=()

while [ $# -gt 0 ]; do
  case "$1" in
    --target) TARGETS="$2"; shift 2 ;;
    --dest)   DEST="$2"; shift 2 ;;
    --copy)   MODE="copy"; shift ;;
    --force)  FORCE=1; shift ;;
    --list)   LIST=1; shift ;;
    -h|--help) sed -n '2,5p' "$0"; exit 0 ;;
    -*) echo "unknown option: $1" >&2; exit 2 ;;
    *)  SKILLS+=("$1"); shift ;;
  esac
done

dir_for() {
  case "$1" in
    agents)   echo "$HOME/.agents/skills" ;;
    claude)   echo "$HOME/.claude/skills" ;;
    gemini)   echo "$HOME/.gemini/skills" ;;
    copilot)  echo "$HOME/.copilot/skills" ;;
    opencode) echo "$HOME/.config/opencode/skills" ;;
    project)  [ -n "$DEST" ] && echo "$DEST" || { echo "--target project needs --dest" >&2; exit 2; } ;;
    *) echo "unknown target: $1" >&2; exit 2 ;;
  esac
}

ALL=()
for d in "$REPO"/skills/*/; do ALL+=("$(basename "$d")"); done

if [ "$LIST" = 1 ]; then
  printf 'skills (%d):\n' "${#ALL[@]}"; printf '  %s\n' "${ALL[@]}"
  echo "targets: agents claude gemini copilot opencode project"
  exit 0
fi
[ ${#SKILLS[@]} -eq 0 ] && SKILLS=("${ALL[@]}")

IFS=',' read -ra TLIST <<< "$TARGETS"
for t in "${TLIST[@]}"; do
  out="$(dir_for "$t")"; mkdir -p "$out"
  done_n=0; skip_n=0
  for s in "${SKILLS[@]}"; do
    src="$REPO/skills/$s"
    [ -d "$src" ] || { echo "no such skill: $s" >&2; exit 1; }
    dst="$out/$s"
    if [ -e "$dst" ] || [ -L "$dst" ]; then
      if [ "$FORCE" = 1 ]; then rm -rf "$dst"; else skip_n=$((skip_n+1)); continue; fi
    fi
    if [ "$MODE" = copy ]; then cp -R "$src" "$dst"; else ln -s "$src" "$dst"; fi
    done_n=$((done_n+1))
  done
  echo "$t -> $out: installed $done_n, skipped $skip_n existing"
done
