# Caribbean consolidation — correction for Grok

**Date:** 2026-06-24 · **From:** Tasklet · **Supersedes** the "retire caribbean-mobility / new caribbean"
instruction in the PR #93 seal package.

## What went wrong
PR #93 created a **new, thin `caribbean` partner** (ABC-only, 0 markets, no model) and Grok **retired the
rich `caribbean-mobility` record** (11 markets, live economics model, growth case) as "superseded." That
is backwards — it downgraded the canonical Caribbean network to a stub.

## The correction (this PR)
- **`caribbean-mobility` → `caribbean`** (renamed, **un-retired**). This rich 11-market regional record is
  the canonical generic **Caribbean × Navier** network. Markets, `economics_url`, and `growth_case`
  preserved untouched.
- **Aggregator branding shed** — "Caribbean Mobility Partner / one app / ride-hail aggregator" reframed to
  a generic Navier network ("not an aggregator-led pitch"); `category: destination_region` so it groups
  with the destination regions, not ride-hail platforms.
- **Thin standalone `caribbean` deleted** (it only ever held the ABC slice already covered by the
  `abc-islands` market).
- Economics model **kept as network GMV — NOT** hospitality $1M (Caribbean is a shared/generic network,
  not a dedicated hospitality partner).
- Cross-ref fixed: `lyft.json _economics_authored_for` → `caribbean`. Stale
  `caribbean-mobility.json.bak-*` removed.

## What Grok needs to reconcile
1. **Geometry binding (REQUIRED):** the ABC routes you sealed in PR #93 under partner **`caribbean`**
   must be bound to the **`abc-islands` market** — *not* at the partner level and *not* spread across the
   other 10 markets. The partner id is unchanged, so the routes still resolve; the action is to attach
   every ABC `route_id` to the `abc-islands` market entry. Drop any duplicate ABC corridors created under
   the short-lived standalone `caribbean`. Net: ABC geometry lives in exactly one place — `abc-islands`.
2. **Ocean Whisperer** stays its own partner (Curaçao captive scoped view) — unchanged.
3. After binding, hand back to **Tasklet** to reconcile the `abc-islands` economics into the existing
   growth_case; then reseal the `/caribbean` page/map.

## End state
One Caribbean partner: **`/caribbean`** = Caribbean × Navier, generic 11-market network, below the
hurricane belt. No `caribbean-mobility`, no duplicate.
