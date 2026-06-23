# Partner proposal route linkage playbook

Required for the Atlas **story / backbone / mesh** density system (`scripts/route-display.mjs`).

## Why this matters

Dense markets (UAE, Singapore, India metros, multi-market hubs) ship hundreds of geometry-valid routes. The map defaults to **Story mode**, which only draws routes explicitly linked in the proposal JSON. Unlinked phases render as empty or generic city blobs — a failed pitch.

## Mandatory fields per phase

Every `phases[]` entry (partner-level and `markets[].phases[]`) must include:

```json
{
  "n": 1,
  "label": "Phase 1 — …",
  "cities": ["dubai-uae"],
  "featured_routes": [
    {
      "label": "Dubai Marina ↔ Palm Jumeirah",
      "from_node_id": "bp-…",
      "to_node_id": "bp-…",
      "distance_nm": 2.1,
      "platform": "Pioneer II",
      "route_id": "rn-…",
      "route_ids": ["rn-…"]
    }
  ]
}
```

Rules:

1. **`route_id` / `route_ids[]`** must resolve to a route in `data-clean/ROUTES.json` (run `node scripts/audit-partner-route-linkage.mjs` after edits).
2. **`distance_nm`** must be within ±25% of the linked route's `distance_nm` (render linkage guard).
3. **`from_node_id` / `to_node_id`** must match the corridor endpoints (place-name guard).
4. String-only featured routes (`"Palm east crescent jetties"`) do **not** work — convert to objects with `route_id`.

## Hub markets (`layout: "hub"`)

Each `markets[]` sub-proposal needs its own:

- `phases[]` with linked `featured_routes`
- `journeys_unlocked[]` with `route_id` on every journey card
- `anchor_cities[]` scoped to the market (no cluster inflation)

## Journeys unlocked

Top-level or market-level `journeys_unlocked[]` entries must carry `route_id` (or `route_ids[]` for multi-leg):

```json
{
  "title": "Marina ↔ Palm express",
  "route_id": "rn-42aa1791bb60",
  "from_node_id": "bp-…",
  "to_node_id": "bp-…",
  "distance_nm": 2.1
}
```

## Signature routes (city / cluster briefs)

Locale and cluster briefs power map clicks and story tags:

- `city_briefs/<city_id>.json` → `signature_routes[]` with `route_id`
- `cluster_briefs/<cluster_id>.json` → `signature_routes[]` with `route_id`

## Validation workflow

```bash
# Full lane (bind + audit + build spot-check)
./scripts/run-route-linkage-lane.sh --partner <slug> --apply

# Or step-by-step:
python3 scripts/validate_partner_proposals.py --strict-linkage
node scripts/audit-partner-route-linkage.mjs --strict --partner <slug>
BUILD_PROFILE=public node scripts/build-site.mjs --profile=public | grep '<partner-slug>'
```

**Publish gates:** `deploy.sh` runs `--strict` audit (allowlist grandfathering). `RELEASE=1` requires zero gaps globally. Remove partner from `ROUTE-LINKAGE-ALLOWLIST.json` once gap-free.

Acceptance: `story:N` in build log should be ≥ number of phases × 1 (ideally ≥ featured routes count). Gaps in `handoff/partner-map-model/PARTNER-ROUTE-LINKAGE-AUDIT.json` should trend to zero for active proposals.

## map_display (optional overrides)

```json
"map_display": {
  "density_tier": "high",
  "default_layer": "story",
  "expand_network": false
}
```

- `density_tier: "high"` — force story default below 81 routes
- `expand_network: true` — flat partners only; re-enable cluster expansion for end-state maps

## Seal / Grok binding scripts

When sealing a new partner lane:

1. Bind phase featured routes: `scripts/grok-*/bind_*_journeys*.py`
2. Wire `journeys_unlocked.route_id` from seal report
3. Re-run econ cascade if economics change
4. Run audit + build-site before deploy

See `partner-pitch/proposals/<partner>/GROK-SEAL-PROMPT-*.md` for lane-specific bind commands.