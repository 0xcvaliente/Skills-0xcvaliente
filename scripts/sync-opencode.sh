#!/usr/bin/env bash
# Merge the public and private skills libraries into OpenCode's global skills folder.
#
# OpenCode reads global skills from ~/.config/opencode/skills (highest precedence),
# and also ~/.claude/skills and ~/.agents/skills for compatibility. This script keeps
# the OpenCode folder current from both repos:
#
#   1. fast-forward pulls the public and private repos (skipped when a repo has
#      uncommitted tracked changes, is off BRANCH, or cannot fast-forward);
#   2. symlinks (default) or copies every skill from both repos' skills/ into DEST;
#   3. installs the private repo's local-variants/, which OVERRIDE the public skill
#      of the same name;
#   4. with --prune, removes links in DEST that point into a repo but are now dangling
#      (a skill that was renamed or deleted), so renames never leave a stale entry.
#
# Usage:
#   sync-opencode.sh [--pull|--no-pull] [--link|--copy] [--force] [--prune]
#                    [--dry-run] [--validate] [--list] [skill ...]
#
# Env overrides: PUBLIC, PRIVATE, DEST, BRANCH
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PUBLIC="${PUBLIC:-$(cd "$SCRIPT_DIR/.." && pwd)}"
PRIVATE="${PRIVATE:-$(cd "$PUBLIC/.." && pwd)/Private-skills-0xcvaliente}"
DEST="${DEST:-$HOME/.config/opencode/skills}"
BRANCH="${BRANCH:-main}"

PULL=1; MODE="link"; FORCE=0; PRUNE=0; DRY=0; VALIDATE=0; LIST=0; WANT=()

while [ $# -gt 0 ]; do
  case "$1" in
    --pull)    PULL=1; shift ;;
    --no-pull) PULL=0; shift ;;
    --link)    MODE="link"; shift ;;
    --copy)    MODE="copy"; shift ;;
    --force)   FORCE=1; shift ;;
    --prune)   PRUNE=1; shift ;;
    --dry-run) DRY=1; shift ;;
    --validate) VALIDATE=1; shift ;;
    --list)    LIST=1; shift ;;
    -h|--help) sed -n '2,19p' "$0"; exit 0 ;;
    -*) echo "unknown option: $1" >&2; exit 2 ;;
    *)  WANT+=("$1"); shift ;;
  esac
done

[ -d "$PUBLIC" ] || { echo "public repo not found: $PUBLIC" >&2; exit 1; }
HAVE_PRIVATE=0
[ -d "$PRIVATE" ] && HAVE_PRIVATE=1

wanted() { # $1 = name; true when no names were given or it is listed
  [ ${#WANT[@]} -eq 0 ] && return 0
  local w; for w in "${WANT[@]}"; do [ "$w" = "$1" ] && return 0; done
  return 1
}

list_repo() { # $1 = repo
  local d
  for d in "$1"/skills/*/; do [ -d "$d" ] && basename "$d"; done
}

if [ "$LIST" = 1 ]; then
  printf 'public (%s):\n' "$PUBLIC"; list_repo "$PUBLIC" | sed 's/^/  /'
  if [ "$HAVE_PRIVATE" = 1 ]; then
    printf 'private (%s):\n' "$PRIVATE"; list_repo "$PRIVATE" | sed 's/^/  /'
    local_v="$PRIVATE"/local-variants/*/
    if [ -d "${local_v%/}" ] 2>/dev/null; then
      printf 'local-variants (override public):\n'
      for d in "$local_v"; do [ -d "$d" ] && basename "$d" | sed 's/^/  /'; done
    fi
  fi
  printf 'dest: %s\n' "$DEST"
  exit 0
fi

linked=0; over=0; skipped=0; pruned=0; pulled=""

pull_repo() { # $1 = repo
  local r="$1" name; name="$(basename "$r")"
  if [ ! -d "$r/.git" ]; then printf '  %s: not a git repo, pull skipped\n' "$name"; return 0; fi
  if [ "$(git -C "$r" branch --show-current 2>/dev/null)" != "$BRANCH" ]; then
    printf '  %s: not on %s, pull skipped\n' "$name" "$BRANCH"; return 0; fi
  if [ -n "$(git -C "$r" status --porcelain --untracked-files=no)" ]; then
    printf '  %s: uncommitted changes, pull skipped\n' "$name"; return 0; fi
  if [ "$DRY" = 1 ]; then printf '  %s: (dry-run) would git pull --ff-only\n' "$name"; return 0; fi
  if git -C "$r" pull --ff-only --quiet; then
    printf '  %s: up to date\n' "$name"; pulled="$pulled $name"
  else
    printf '  %s: pull failed (not fast-forward or offline)\n' "$name"
  fi
}

install_skill() { # $1 = repo, $2 = name, $3 = src, $4 = variant(0/1)
  local name="$2" src="$3" variant="$4" dst="$DEST/$name"
  wanted "$name" || return 0
  if [ -e "$dst" ] || [ -L "$dst" ]; then
    if { [ "$variant" = 1 ] && [ -L "$dst" ]; } || [ "$FORCE" = 1 ]; then
      [ "$variant" = 1 ] && [ -L "$dst" ] && over=$((over+1))
      if [ "$DRY" = 1 ]; then printf '  (dry-run) replace %s\n' "$name"
      else if [ -L "$dst" ]; then rm "$dst"; else rm -rf "$dst"; fi; fi
    else
      skipped=$((skipped+1)); printf '  skip    %s (exists)\n' "$name"; return 0
    fi
  fi
  if [ "$DRY" = 1 ]; then
    printf '  %s %s -> %s\n' "$MODE" "$name" "$src"
  else
    if [ "$MODE" = copy ]; then cp -R "$src" "$dst"; else ln -s "$src" "$dst"; fi
    printf '  %s %s\n' "$MODE" "$name"
  fi
  linked=$((linked+1))
}

install_repo() { # $1 = repo, $2 = install local-variants too (0/1)
  local repo="$1" d name
  for d in "$repo"/skills/*/; do
    [ -d "$d" ] || continue
    name="$(basename "$d")"
    install_skill "$repo" "$name" "${d%/}" 0
  done
  [ "$2" = 1 ] || return 0
  for d in "$repo"/local-variants/*/; do
    [ -d "$d" ] || continue
    name="$(basename "$d")"
    install_skill "$repo" "$name" "${d%/}" 1
  done
}

prune_dangling() {
  [ -d "$DEST" ] || return 0
  local entry target
  for entry in "$DEST"/*; do
    [ -L "$entry" ] || continue
    target="$(readlink "$entry")"
    case "$target" in
      "$PUBLIC"/*|"$PRIVATE"/*) ;;
      *) continue ;;
    esac
    if [ ! -e "$target" ]; then
      pruned=$((pruned+1))
      if [ "$DRY" = 1 ]; then printf '  (dry-run) prune %s (dangling)\n' "$(basename "$entry")"
      else rm "$entry"; printf '  prune   %s (dangling)\n' "$(basename "$entry")"; fi
    fi
  done
}

printf 'OpenCode skills sync\n'
printf '  public  : %s\n' "$PUBLIC"
if [ "$HAVE_PRIVATE" = 1 ]; then printf '  private : %s\n' "$PRIVATE"
else printf '  private : not found (%s), continuing with public only\n' "$PRIVATE"; fi
printf '  dest    : %s\n' "$DEST"

if [ "$PULL" = 1 ]; then
  printf '\nPull:\n'; pull_repo "$PUBLIC"; [ "$HAVE_PRIVATE" = 1 ] && pull_repo "$PRIVATE"
fi

[ "$DRY" = 1 ] || mkdir -p "$DEST"

printf '\nInstall:\n'
install_repo "$PUBLIC" 0
[ "$HAVE_PRIVATE" = 1 ] && install_repo "$PRIVATE" 1

if [ "$PRUNE" = 1 ]; then printf '\nPrune:\n'; prune_dangling; fi

if [ "$VALIDATE" = 1 ]; then
  printf '\nValidate:\n'
  python3 "$PUBLIC/scripts/validate.py" || printf '  %s reported problems\n' "$(basename "$PUBLIC")"
  if [ "$HAVE_PRIVATE" = 1 ] && [ -f "$PRIVATE/scripts/validate.py" ]; then
    python3 "$PRIVATE/scripts/validate.py" || printf '  %s reported problems\n' "$(basename "$PRIVATE")"
  fi
fi

printf '\nDone: %d linked, %d overrode, %d skipped, %d pruned.\n' "$linked" "$over" "$skipped" "$pruned"
[ -n "$pulled" ] && printf 'Pulled:%s\n' "$pulled"
printf 'OpenCode reloads skills on change; run /reload if a skill does not appear.\n'
