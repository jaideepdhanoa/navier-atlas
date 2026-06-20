# Turkey beyond Istanbul — coastal node split (Yango) — 2026-06-20

Third parity handoff today (follows #46, #47). Tasklet registry/content work done; deterministic
route_id re-bind + render-check + (Chios/Samos) geometry mint is Grok's lane.

## The bug
All 27 `yango-turkey` corridors were tagged `from_node=istanbul-turkey / to_node=istanbul-turkey`, and 3 of
the 4 `anchor_cities` carried country-suffixed IDs (`bodrum-turkey`, `antalya-turkey`, `cesme-izmir-turkey`)
that **don't resolve to the atlas `city_id`** (`bodrum`, `antalya`, `cesme-izmir`). Classic Gate A ID_MISMATCH:
Bodrum/Antalya/Çeşme-İzmir rendered **nothing** despite fully-minted geometry, and coastal legs (incl. the new
Phase-3 Fethiye→Rhodes) drew **from the Bosphorus pier** — geographically ~250nm wrong.

## Geometry already exists (this is a re-tag, not a mint)
| atlas node (internal city_id) | BPs | covers |
|---|---|---|
| `istanbul-turkey` | 82 | Bosphorus, Princes' Islands |
| `bodrum` | 138 | Bodrum peninsula + Marmaris + Datça + Didim + Fethiye/Göcek |
| `cesme-izmir` | 84 | Çeşme, İzmir, Kuşadası, Foça |
| `antalya` | 89 | Antalya/Belek Riviera |
| `rhodes-dodecanese-greece` | 37 | Rhodes + Kos (cross-border to-side) |

## What Tasklet changed
**corridors.json (`yango-turkey`)** — re-tagged all 27 corridors by geography (label-classified, 0 unclassified):
`istanbul-turkey ×9, bodrum ×12, cesme-izmir ×4, antalya ×2`. Cross-border to-sides → `rhodes-dodecanese-greece`
for Kos/Rhodes legs. **Çeşme→Chios and Kuşadası→Samos have NO bound Greek node → `to_node_id: null`,
`_to_needs_minting: true`** (null beats confidently-wrong).

**partners/yango.json (`turkey` market)**:
- `anchor_cities`: `bodrum-turkey→bodrum`, `antalya-turkey→antalya`, `cesme-izmir-turkey→cesme-izmir` (Istanbul OK).
- Re-bound 3 mis-tagged featured routes to true nodes; **where the node changed, `route_id` nulled + `_link_status:
  pending`** so Grok re-binds against the corrected geometry (prior seal was against Istanbul):
  - P1 İzmir (Konak)→Karşıyaka → `cesme-izmir`
  - P2 Fethiye→Ölüdeniz → `bodrum`
  - P3 Fethiye→Rhodes → `bodrum / rhodes-dodecanese-greece`
- `label`: "Türkiye — Istanbul Bosphorus" → "Türkiye — Istanbul, Aegean & Med coast" (hero/summary already coastal-aware).

## Deterministic actions for Grok
1. **Re-bind the route_ids** for the 3 re-tagged featured routes (now null/pending) against the corrected nodes; render-check.
2. **Mint Chios + Samos** boarding-point nodes (North Aegean Greek islands) — only unbound geometry here — then bind
   Çeşme→Chios / Kuşadası→Samos to-sides. Until then they stay aspirational/one-ended.
3. Re-render the Yango map: Bodrum, Antalya, Çeşme-İzmir should now appear as distinct coastal anchors.

## Notes
- **Economics unaffected:** `yango-turkey` stays one economic market (same corridors/demand/fares); only geometry
  node-attribution was corrected. No re-cascade needed.
- Crosswalk: `TURKEY-ANCHOR-CITY-CROSSWALK.json` (this dir).
