# CHANGELOG FOR CLAUDE — 2026-06-06 — Partner-proposal deepening + ops learning system

## What changed in this export (content lane only — no geometry, no path-set changes)

Path-set is a **superset of prior gold** (`navier-export-20260605T231547Z.zip`): same
files + this changelog. No routes/POIs/nodes added or removed. 5,150 routes / 11,351 POIs
/ 166 briefs / 46 partners unchanged. Postflight PASS (0 crossers, 0 leak hits). Audit
PASS (0 fail / 0 warn).

### 4 partner proposals deepened (data-clean/partners/*.json)
- **kakao-mobility** — 6 `journeys_unlocked` linked to real `route_ids`, 4 `proof_points`,
  Seoul "pending" copy removed, Hangang Bus corrected to "launched Sept 2025" (not relaunch).
- **line** — 23 `route_ids`, 0 unresolved, null-geo caveat cleared, LY Corporation framing.
- **goto-gojek** — Jakarta de-conflated (Thousand Islands corridor; cross-border attributed
  to Riau, not Jakarta); `the_ask` + `close` added.
- **grab** — foodpanda 2026 Taiwan acquisition added as lead `proof_points[0]`
  (citation caveat: exact press-release URL pending Jaideep confirm).

All four conform to the locked schema (`journeys_unlocked`, `proof_points`, `objections`,
`end_state`, `the_ask`, `close`).

### Renderer-relevant notes
- No schema change needed for `featured_routes` — confirmed object-form `{label, route_id}`
  renders clickable. The remaining **113 bare-string `featured_routes` are a Tasklet data
  task** (string -> object), tracked on our side; they light up automatically once converted.
- `route_ids[]` array form confirmed supported everywhere — no action.
- `seoul-incheon-korea` node present; Kakao market builds at 0 skipped pages.

## Process change (no data impact)
- Added `OPS-LOOP-LEDGER.md` + canonical `content_lane_finish.sh` to kill "long loops on a
  small delta." Read-first gate now: BUILD-ROUTER.md -> OPS-LOOP-LEDGER.md.
