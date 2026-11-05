#!/usr/bin/env bash
# Scheduled upstream check for the skills library (meant to run every 4th day).
#
# Default run (read-only for skill content):
#   1. fast-forward pulls the public and private skills repos (skipped when a repo has
#      uncommitted tracked changes, is off its main branch or cannot fast-forward);
#   2. runs `check_upstreams.py status` and logs the table;
#   3. shows a macOS notification when the set of moved upstreams CHANGED since the last
#      notification (an upstream you deliberately skipped does not nag every 4 days).
#
# --apply: when something moved, also start a headless Claude Code session that follows
#   the update-skills skill (review, adopt, validate, record, commit, push). This commits
#   and pushes to GitHub without asking, so it is opt-in. Not used by the schedule unless
#   you install with `--install --apply`.
#
# Usage:
#   auto-update.sh [--apply] [--dry-run]     run once now
#   auto-update.sh --install [--apply]       schedule with launchd, every 4 days
#   auto-update.sh --uninstall               remove the schedule
#   auto-update.sh --status                  show the schedule and the last log lines
#
# Env: PRIVATE_REPO (default: sibling Private-skills-0xcvaliente), MODEL (default: opus),
#      INTERVAL_DAYS (default: 4, used by --install).
set -euo pipefail

export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

SCRIPT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/$(basename "${BASH_SOURCE[0]}")"
PUBLIC_REPO="$(cd "$(dirname "$SCRIPT")/.." && pwd)"
PRIVATE_REPO="${PRIVATE_REPO:-$(cd "$PUBLIC_REPO/.." && pwd)/Private-skills-0xcvaliente}"
MODEL="${MODEL:-opus}"
INTERVAL_DAYS="${INTERVAL_DAYS:-4}"
LABEL="com.0xcvaliente.skills-update"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
LOG="$HOME/Library/Logs/skills-update.log"
STATE_DIR="$HOME/.local/state/skills-update"
STATE="$STATE_DIR/last-moved"
CHECKER="$PUBLIC_REPO/skills/update-skills/scripts/check_upstreams.py"

APPLY=0; DRY=0; ACTION=run
while [ $# -gt 0 ]; do
  case "$1" in
    --apply) APPLY=1; shift ;;
    --dry-run) DRY=1; shift ;;
    --install) ACTION=install; shift ;;
    --uninstall) ACTION=uninstall; shift ;;
    --status) ACTION=status; shift ;;
    -h|--help) sed -n '2,22p' "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done

log() { printf '%s %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*"; }
notify() {
  [ "$DRY" = 1 ] && { log "(dry-run) notify: $1"; return 0; }
  osascript -e "display notification \"$1\" with title \"Skills update\"" >/dev/null 2>&1 || true
}

install_schedule() {
  local secs=$((INTERVAL_DAYS * 86400)) args="<string>$SCRIPT</string>"
  [ "$APPLY" = 1 ] && args="$args<string>--apply</string>"
  mkdir -p "$(dirname "$PLIST")" "$(dirname "$LOG")"
  cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>$LABEL</string>
  <key>ProgramArguments</key><array><string>/bin/bash</string>$args</array>
  <key>StartInterval</key><integer>$secs</integer>
  <key>RunAtLoad</key><false/>
  <key>StandardOutPath</key><string>$LOG</string>
  <key>StandardErrorPath</key><string>$LOG</string>
</dict></plist>
EOF
  launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
  launchctl bootstrap "gui/$(id -u)" "$PLIST"
  echo "Installed: runs every $INTERVAL_DAYS days ($([ "$APPLY" = 1 ] && echo apply || echo check-only) mode). Log: $LOG"
}

case "$ACTION" in
  install) install_schedule; exit 0 ;;
  uninstall)
    launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
    rm -f "$PLIST"; echo "Schedule removed."; exit 0 ;;
  status)
    if launchctl print "gui/$(id -u)/$LABEL" >/dev/null 2>&1; then echo "Schedule: loaded ($PLIST)"; else echo "Schedule: not loaded"; fi
    [ -f "$LOG" ] && tail -n 15 "$LOG" || echo "No log yet."
    exit 0 ;;
esac

# --- run once -----------------------------------------------------------------
mkdir -p "$STATE_DIR" "$(dirname "$LOG")"
log "== skills update run (apply=$APPLY dry=$DRY) =="

pull_repo() {
  local r="$1" name; name="$(basename "$r")"
  [ -d "$r/.git" ] || { log "$name: not found, skipped"; return 0; }
  [ "$(git -C "$r" branch --show-current)" = main ] || { log "$name: not on main, skipped"; return 0; }
  if [ -n "$(git -C "$r" status --porcelain --untracked-files=no)" ]; then
    log "$name: uncommitted tracked changes, pull skipped"; return 0
  fi
  [ "$DRY" = 1 ] && { log "$name: (dry-run) would git pull --ff-only"; return 0; }
  git -C "$r" pull --ff-only --quiet && log "$name: up to date with origin" || log "$name: pull failed (not fast-forward or offline)"
}
pull_repo "$PUBLIC_REPO"
pull_repo "$PRIVATE_REPO"

if ! OUT="$(python3 "$CHECKER" --repo "$PUBLIC_REPO" status 2>&1)"; then
  log "status check failed:"; printf '%s\n' "$OUT"
  notify "Upstream check failed, see $LOG"; exit 1
fi
printf '%s\n' "$OUT"

MOVED="$(printf '%s\n' "$OUT" | awk '$0 ~ / MOVED / {print $1 "@" $4}' | sort | tr '\n' ' ')"
ERRORS="$(printf '%s\n' "$OUT" | awk '$0 ~ / ERROR / {print $1}' | tr '\n' ' ')"
[ -n "$ERRORS" ] && log "upstream errors: $ERRORS"

if [ -z "$MOVED" ]; then
  log "nothing moved upstream"; : > "$STATE"; exit 0
fi
log "moved: $MOVED"

if [ "$MOVED" != "$(cat "$STATE" 2>/dev/null || true)" ]; then
  notify "Upstreams moved: $MOVED. Run the update-skills skill to review."
  [ "$DRY" = 1 ] || printf '%s' "$MOVED" > "$STATE"
else
  log "same moved set as last time, no new notification"
fi

if [ "$APPLY" = 1 ]; then
  if [ "$DRY" = 1 ]; then log "(dry-run) would start headless claude ($MODEL) to run update-skills"; exit 0; fi
  command -v claude >/dev/null || { log "claude CLI not found, cannot apply"; exit 1; }
  log "starting headless review and upgrade with $MODEL"
  cd "$PUBLIC_REPO"
  claude -p --model "$MODEL" --permission-mode acceptEdits \
    --allowedTools "Bash(git:*) Bash(python3:*) Bash(diff:*) Bash(ls:*) Bash(cat:*) Read Grep Glob Edit Write WebFetch WebSearch" \
    "Follow skills/update-skills/SKILL.md for $PUBLIC_REPO. Upstreams that moved: $MOVED. Review each, adopt only ADOPT or ADOPT-ADAPTED changes, and SKIP anything that is a large rewrite, removes coverage or adds more than a few MB: list those in your final report instead of applying them. Obey AGENTS.md (no attribution lines, never edit protected records). Run python3 scripts/validate.py; if it fails, do not commit. Otherwise record each reviewed upstream, commit, and git push origin main. Then pull and check $PRIVATE_REPO the same way if it has upstream sources. End with a short report." \
    2>&1 || log "headless run exited with an error"
  log "apply run finished"
fi
