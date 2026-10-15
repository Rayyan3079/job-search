#!/usr/bin/env bash
# Prepares a fresh cloud container for a job-search run.
# Usage: source scripts/setup.sh   (from the job-search repo root)
set -e
JS_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CO_ROOT="${CO_ROOT:-$(dirname "$JS_ROOT")/career-ops}"
if [ ! -d "$CO_ROOT/.git" ]; then
  GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/career-ops-hq/career-ops "$CO_ROOT"
fi
(cd "$CO_ROOT" && (npm ci --no-audit --no-fund >/dev/null 2>&1 || npm install --no-audit --no-fund >/dev/null 2>&1))

# Point Playwright at whichever pre-installed headless shell exists, whatever revision it expects.
WANT=$(python3 -c "import json,sys;b=json.load(open(sys.argv[1]))[\"browsers\"];print([x[\"revision\"] for x in b if x[\"name\"]==\"chromium-headless-shell\"][0])" "$CO_ROOT/node_modules/playwright-core/browsers.json" 2>/dev/null)
HAVE=$(ls -d /opt/pw-browsers/chromium_headless_shell-* 2>/dev/null | grep -v "\-${WANT}$" | head -1)
if [ -n "$WANT" ] && [ ! -e "/opt/pw-browsers/chromium_headless_shell-$WANT" ] && [ -n "$HAVE" ]; then
  mkdir -p "/opt/pw-browsers/chromium_headless_shell-$WANT"
  ln -sfn "$HAVE/chrome-linux" "/opt/pw-browsers/chromium_headless_shell-$WANT/chrome-headless-shell-linux64"
  ln -sf headless_shell "$HAVE/chrome-linux/chrome-headless-shell"
  touch "/opt/pw-browsers/chromium_headless_shell-$WANT/INSTALLATION_COMPLETE"
fi

export CAREER_OPS_DATA_DIR="$JS_ROOT"
export CAREER_OPS_TRUST_PROXY_EGRESS=1   # cloud egress proxy; scan.mjs providers need it
export CO_ROOT JS_ROOT
echo "career-ops: $CO_ROOT  data: $CAREER_OPS_DATA_DIR"
