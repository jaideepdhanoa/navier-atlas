# Grab Thailand — Ko Lanta Andaman addition (2026-06-23)

Adds **Ko Lanta (`koh-lanta-thailand`)** as a connected city in the existing **Andaman cluster**
(`phuket_andaman` market), south of Phi Phi/Krabi on the same dense ferry web.

## Contents
| Path | What |
|---|---|
| `GROK-SEAL-PROMPT-kolanta.md` | Seal mandate + acceptance gate |
| `GRAB-THAILAND-KOLANTA-BINDSET.json` | Authoritative city/BP/route seal list (route_id null) |
| `GRAB-THAILAND-KOLANTA-DEMAND-ANCHORS.json` | Source-tiered demand for the post-seal economics cascade |
| `boarding-points/koh-lanta-thailand.json` | 2 BP curated seeds (Saladan P0, Old Town P1) |
| `seal-manifest-kolanta.json` | Seal-manifest increment |

## Durable source (committed alongside)
- `partner-pitch/partners/grab-thailand.json` — +Ko Lanta in `phuket_andaman.connected_cities`, +1 journey,
  +3 `connected_city_mesh` routes (route_id null, `pending-seal-thailand-kolanta`).
- `data-clean/city_briefs/koh-lanta-thailand.json` — connected_city_v2 brief.

## Routes (all Pioneer II, ≤40 nm)
- Ko Lanta ↔ Phi Phi (~17 nm, tier A) · Ko Lanta ↔ Krabi (~24 nm, tier B) · Phuket ↔ Ko Lanta (~40 nm, tier B)

## Not touched
`data-clean/partners/grab-thailand.json` — Grok reseals it after route_ids bind, so the live front end
never renders a geometry-less market. No new markets; no Samui/lower-Gulf corridor.
