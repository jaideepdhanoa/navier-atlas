# Gold #33 — label-vs-route geographic audit (8 hero highlights nulled)

Partner-pitch-only reseal. Routes (5,201) + economics sidecar (69) unchanged.

This closes the loop on the error class discovered in #32: **label-vs-route geographic
mismatch** — items whose route_id + distance_nm + from/to node_ids are all self-consistent,
but all three disagree with the human label. The distance gate (LB-47) and endpoint gate are
structurally blind to it. With Places API disabled, I audited all **210** linked items by
geographic reasoning and found 2 genuinely confidently-wrong cases (both flagship hero routes):

## Nulled
1. **six-senses "Dubai / Ras Al Khaimah ↔ Six Senses Zighy Bay" (×3)** — pointed at
   `rn-1ba484ccccc6` = Bandar Al Khairan → Ras Al Hadd, a **Muscat / SE-Oman** route
   (~300 km from Zighy Bay, which is in Musandam). Item is mis-homed on the `muscat-oman` node.
2. **aman "Tivat / Porto Montenegro ↔ Aman Sveti Stefan" + "Montenegro coast ↔ Porto
   Montenegro / Portonovi" (×5)** — pointed at `ics-1ec3383b58` = Zaton → Mlini, a
   **Dubrovnik-area Croatian** route (~45 km from the Montenegro Aman sites). The
   `kotor-montenegro` node carries Croatian boarding points.

## Upstream root causes (your domain) — see `FLAG-FOR-CLAUDE-upstream-geo-mistags.md`
- Need a **Musandam (Dibba/Khasab) node** + a real Dubai/RAK ↔ Zighy Bay corridor.
- Need real **Montenegro boarding points** (Tivat, Porto Montenegro, Budva, Sveti Stefan,
  Kotor) so Boka-Bay / Budva-coast corridors stop resolving to Croatian harbors.

## Verify
Baked surface: the 8 wrong highlights are gone; gates idempotent (0 nulled). 210 → 202
linked items, all geographically consistent. Routes/sidecar unchanged.

## Recommendation
Until geocoding is available, keep this label↔geography pass as a recurring manual audit
step on every partner re-externalize (it's not automatable with distance math alone).
