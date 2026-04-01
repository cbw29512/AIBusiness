#!/usr/bin/env bash
# deploy_after_cycle.sh
# Drop-in replacement for autonomous_loop.sh that also regenerates and
# deploys the site after every cycle that produces new or updated products.
#
# Usage:
#   ./scripts/deploy_after_cycle.sh [interval_minutes]
#
# Default interval: 45 minutes (same as autonomous_loop.sh)

set -u
trap 'echo "[ERROR] deploy_after_cycle.sh failed at line $LINENO" >&2' ERR

ROOT_DIR="${HOME}/Desktop/makethatmoney"
INTERVAL_MINUTES="${1:-45}"
LOG_DIR="${ROOT_DIR}/logs"
HEARTBEAT_LOG="${LOG_DIR}/autonomous_loop.log"
DEPLOY_LOG="${LOG_DIR}/deploy_site.log"

mkdir -p "${LOG_DIR}"
export OPENCODE_ENABLE_EXA=1

log() {
  echo "${1}"
  printf '%s %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "${1}" >> "${HEARTBEAT_LOG}"
}

deploy_log() {
  printf '%s %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "${1}" >> "${DEPLOY_LOG}"
}

cd "${ROOT_DIR}" || exit 1

log "[START] Autonomous loop with site deploy — interval: ${INTERVAL_MINUTES} min"

# Snapshot product state before cycle so we can detect changes
snapshot_products() {
  find products -name "gumroad_listing.json" -exec md5 {} \; 2>/dev/null | sort | md5
}

while true; do
  log "[CYCLE] Starting autonomous cycle"

  BEFORE="$(snapshot_products)"

  # --- Run the main research cycle ---
  python3 ./scripts/autonomous_cycle.py

  # --- Run goal tracker ---
  python3 ./scripts/goal_status.py 2>/dev/null || true

  # --- Check if products changed ---
  AFTER="$(snapshot_products)"

  if [ "${BEFORE}" != "${AFTER}" ] || [ ! -f index.html ]; then
    log "[DEPLOY] Product changes detected — regenerating site"
    deploy_log "[DEPLOY] Products changed — regenerating"

    python3 scripts/generate_site.py >> "${DEPLOY_LOG}" 2>&1

    # Push to GitHub if git is set up
    if [ -d ".git" ]; then
      git add index.html products/ state/offers.json 2>/dev/null || true

      if ! git diff --cached --quiet 2>/dev/null; then
        git commit -m "chore: update site $(date '+%Y-%m-%d %H:%M')" >> "${DEPLOY_LOG}" 2>&1
        git push origin main >> "${DEPLOY_LOG}" 2>&1
        log "[DEPLOY] ✅ Site pushed to GitHub Pages"
        deploy_log "[DEPLOY] ✅ Pushed to GitHub"
      else
        log "[DEPLOY] No git changes after regen — skipping push"
      fi
    else
      log "[DEPLOY] ⚠️  No git repo — site regenerated locally only"
      log "[DEPLOY]    Run GITHUB_SETUP steps to enable auto-push"
    fi
  else
    log "[DEPLOY] No product changes — skipping site regen"
  fi

  log "[SLEEP] Next cycle in ${INTERVAL_MINUTES} minutes"
  sleep "$((INTERVAL_MINUTES * 60))"
done
