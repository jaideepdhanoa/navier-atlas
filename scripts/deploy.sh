#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Navier Atlas — production deploy  (DIVISION-OF-LABOR.md §3 / §4)
# Runs the mandatory pre-flight, then publishes index.html to Vercel prod.
# Claude Code owns this path; Tasklet seals the data. ABORTS if pre-flight fails.
#
#   VERCEL_TOKEN=… ./scripts/deploy.sh
#
# Required env:
#   VERCEL_TOKEN                  Vercel access token (NEVER commit; provided via env secret)
# Optional env (if the project isn't linked via .vercel/):
#   VERCEL_ORG_ID, VERCEL_PROJECT_ID   target the existing navier-atlas project non-interactively
#
# Partner auth (set in Vercel project env — not in git):
#   AUTH_SECRET                        session-cookie signing key
#   PARTNERS_HUB_PASSWORD              password for /partners internal directory
#   PARTNER_AUTH_GRAB, PARTNER_AUTH_UBER, …   per-slug passwords (hyphens → underscores)
#   PARTNER_AUTH_JSON                  optional {"grab":"…","__hub__":"…"} bulk map
#   /cluster/* and /city/* stay public; /partners + /<partner>/* gated by _dist/middleware.js
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

: "${VERCEL_TOKEN:?VERCEL_TOKEN not set — provision it as an environment secret, never in git}"

# 1 · pre-flight deps (gitignored node_modules; install on first run)
if [ ! -d scripts/preflight/node_modules ]; then
  echo "→ installing pre-flight deps…"
  ( cd scripts/preflight && npm install --silent --no-audit --no-fund )
fi

# 2 · build the full deploy tree _dist/ from data-clean/ (Claude owns render+build; Tasklet delivers DATA).
#     build.mjs writes the root atlas-data.js the pre-flight gates; build-site.mjs assembles the tree:
#       _dist/index.html + atlas-data.js          aggregate (all partners; internal)
#       _dist/<slug>/index.html + atlas-data.js   per-partner: data SCOPED to that partner + render lock
#     Each per-partner build runs an exclusion-token grep + cross-partner sweep (aborts on any hit).
echo "→ building deploy tree (_dist/) from data-clean/…  (profile: ${BUILD_PROFILE:-public})"
BUILD_PROFILE="${BUILD_PROFILE:-public}" node scripts/build.mjs --profile="${BUILD_PROFILE:-public}"
BUILD_PROFILE="${BUILD_PROFILE:-public}" node scripts/build-site.mjs --profile="${BUILD_PROFILE:-public}"

# 2b · route linkage audit (advisory unless RELEASE=1 or partner-scoped strict).
echo "→ route linkage audit…"
LINKAGE_ARGS=(--strict)
if [ -n "${RELEASE:-}" ]; then LINKAGE_ARGS+=(--global); fi
node scripts/audit-partner-route-linkage.mjs "${LINKAGE_ARGS[@]}" || {
  if [ -n "${RELEASE:-}" ]; then
    echo "✗ RELEASE=1 deploy blocked — fix route linkage: ./scripts/run-route-linkage-lane.sh --apply" >&2
    exit 1
  fi
  echo "  ⚠ route linkage gaps (allowlisted partners OK) — set RELEASE=1 only when allowlist is empty"
}

echo "→ partner footprint→market keep inheritance gate…"
python3 scripts/audit_partner_route_inheritance_health.py --fail-on-a || {
  if [ -n "${RELEASE:-}" ]; then
    echo "✗ RELEASE=1 deploy blocked — covered footprint cities lack markets[] keep (Dott/Doha-class gap)" >&2
    echo "  See handoff/partner-map-model/RULE-COVERED-FOOTPRINT-MARKET-KEEP.md" >&2
    exit 1
  fi
  echo "  ⚠ A_footprint_without_market findings — fix markets[] or demote footprint; RELEASE=1 will block"
}

echo "→ route geometry audit…"
python3 scripts/audit-route-geometry.py || true
python3 scripts/audit-route-geometry.py --strict-severe 2>/dev/null || {
  echo "  ⚠ story route severe geometry gaps (>1km) — see GEOMETRY-STORY-HOLD.json; channel solver backlog"
}

# 3 · §3 pre-flight on the gated surface (seal hash · exclusion grep · MapLibre smoke · pitch-render).
#     Set RELEASE=1 for a prod cut to ENFORCE the seal (§3.1); non-zero ⇒ abort the deploy.
echo "→ running deploy pre-flight…"
node scripts/preflight/preflight.mjs "$ROOT" ${RELEASE:+--release}

# 4 · publish the _dist/ tree to Vercel prod (aggregate at /, each partner at /<slug>).
#     Carry the project link INTO _dist (build-site wiped it) so the deploy targets the existing
#     navier-atlas project — else Vercel would create a new one. (VERCEL_ORG_ID/VERCEL_PROJECT_ID
#     env vars also work and take precedence if the .vercel/ link file isn't present.)
if [ -f "$ROOT/.vercel/project.json" ]; then
  mkdir -p "$ROOT/_dist/.vercel"
  cp "$ROOT/.vercel/project.json" "$ROOT/_dist/.vercel/project.json"
fi
echo "→ pre-flight clean; deploying _dist/ to Vercel prod…"
# vercel.json must NOT use legacy `builds` — that bypasses Edge middleware on /<partner>/ paths.
# Vercel auto-builds api/og.js as a serverless function; middleware.js runs on the edge.
# The upload can hit transient Vercel API errors on large trees — e.g. a non-JSON 5xx
# ("upstream connect error …" → "FetchError: invalid json response body"). The build and
# pre-flight already passed, so retry just the upload with exponential backoff (2s,4s,8s,16s)
# before giving up. Re-uploads are cheap: Vercel dedupes already-sent files by content hash.
URL=""
attempt=1; max_attempts=5; delay=2
while :; do
  if URL="$(cd "$ROOT/_dist" && npx --yes vercel@54 deploy --prod --yes --archive=tgz --token "$VERCEL_TOKEN")"; then
    break
  fi
  if [ "$attempt" -ge "$max_attempts" ]; then
    echo "✗ vercel deploy failed after ${attempt} attempts — giving up." >&2
    exit 1
  fi
  echo "  ⚠ deploy attempt ${attempt}/${max_attempts} failed (likely transient Vercel API error) — retrying in ${delay}s…" >&2
  sleep "$delay"
  attempt=$((attempt + 1)); delay=$((delay * 2))
done
echo "✅ deployed: $URL"
echo "   (post to #tasklet-jaideep:  ✅ deployed $(git rev-parse --short HEAD) · routes rendering · pre-flight clean)"
