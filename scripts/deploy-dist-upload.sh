#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Upload _dist/ to Vercel production with batched / resumable-friendly uploads.
#
# Why this exists:
#   --archive=tgz packs the whole tree into ONE ~600MB blob. Any SSL/EPIPE mid-
#   upload fails the entire attempt and the next retry starts from 0 bytes.
#   --archive=split-tgz splits that into many smaller parts so a transient
#   network error only loses the in-flight chunk — not the whole deploy.
#
# Usage (from repo root, after _dist is built + linked):
#   VERCEL_TOKEN=… ./scripts/deploy-dist-upload.sh
#
# Env:
#   VERCEL_TOKEN            required
#   VERCEL_ARCHIVE          split-tgz (default) | tgz | none
#   VERCEL_CLI_VERSION      default 54
#   VERCEL_UPLOAD_ATTEMPTS  default 8
#   VERCEL_UPLOAD_DELAY_S   initial backoff seconds (default 4)
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST="${DIST:-$ROOT/_dist}"
LOG="${TMPDIR:-/tmp}/vercel-dist-upload.$$.log"

: "${VERCEL_TOKEN:?VERCEL_TOKEN not set}"

ARCHIVE="${VERCEL_ARCHIVE:-split-tgz}"
CLI_VER="${VERCEL_CLI_VERSION:-54}"
MAX_ATTEMPTS="${VERCEL_UPLOAD_ATTEMPTS:-8}"
DELAY="${VERCEL_UPLOAD_DELAY_S:-4}"

cleanup() { rm -f "$LOG"; }
trap cleanup EXIT

if [ ! -d "$DIST" ]; then
  echo "✗ missing $DIST — build the site first" >&2
  exit 2
fi

if [ -f "$ROOT/.vercel/project.json" ]; then
  mkdir -p "$DIST/.vercel"
  cp "$ROOT/.vercel/project.json" "$DIST/.vercel/project.json"
fi

ARCHIVE_ARGS=()
case "$ARCHIVE" in
  split-tgz|tgz)
    ARCHIVE_ARGS=(--archive="$ARCHIVE")
    echo "→ vercel upload mode: archive=$ARCHIVE (chunked parts — not one monolithic blob)"
    ;;
  none|off|files)
    ARCHIVE_ARGS=()
    echo "→ vercel upload mode: per-file (content-hash dedupe across retries)"
    ;;
  *)
    echo "✗ unknown VERCEL_ARCHIVE=$ARCHIVE (use split-tgz | tgz | none)" >&2
    exit 2
    ;;
esac

if [ -x /opt/homebrew/opt/node@22/bin/node ]; then
  export PATH="/opt/homebrew/opt/node@22/bin:$PATH"
fi
export NODE_OPTIONS="${NODE_OPTIONS:+$NODE_OPTIONS }--dns-result-order=ipv4first"

echo "→ node $(node -v) · vercel@${CLI_VER} · attempts=${MAX_ATTEMPTS}"

URL=""
attempt=1
while :; do
  echo "→ deploy attempt ${attempt}/${MAX_ATTEMPTS}…"
  set +e
  (
    cd "$DIST" && npx --yes "vercel@${CLI_VER}" deploy \
      --prod --yes \
      ${ARCHIVE_ARGS[@]+"${ARCHIVE_ARGS[@]}"} \
      --token "$VERCEL_TOKEN"
  ) >"$LOG" 2>&1
  status=$?
  set -e
  # Stream log to the operator (keep full copy for URL scrape)
  cat "$LOG" >&2

  if [ "$status" -eq 0 ]; then
    URL="$(grep -Eo 'https://[^[:space:]]+' "$LOG" | grep -E 'vercel\.app|navier' | tail -n 1 || true)"
    if [ -z "$URL" ]; then
      URL="$(grep -Eo 'https://[^[:space:]]+' "$LOG" | tail -n 1 || true)"
    fi
    if [[ "$URL" == https://* ]]; then
      break
    fi
    echo "  ⚠ vercel exited 0 but no deployment URL found in output" >&2
  fi

  if [ "$attempt" -ge "$MAX_ATTEMPTS" ]; then
    echo "✗ vercel deploy failed after ${attempt} attempts — giving up." >&2
    exit 1
  fi
  echo "  ⚠ attempt ${attempt}/${MAX_ATTEMPTS} failed — retrying in ${DELAY}s…" >&2
  echo "    split-tgz / per-file keep successful chunks; only the failed part re-uploads." >&2
  sleep "$DELAY"
  attempt=$((attempt + 1))
  DELAY=$((DELAY * 2))
  if [ "$DELAY" -gt 120 ]; then DELAY=120; fi
done

echo "✅ deployed: $URL"
printf '%s\n' "$URL" > /tmp/vercel-url.txt
# Keep URL on stdout for deploy.sh callers that capture it
printf '%s\n' "$URL"
