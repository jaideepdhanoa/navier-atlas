# GROK SPEC — Corridor render gap (dark markets) after WS-4 restamp + inheritance migration

**Owner:** Grok (geometry seal + finance cascade lane). Tasklet flags, Grok fixes, nobody invents a pier.
**Author:** Tasklet
**Date:** 2026-07-06
**Trigger:** Jaideep — Yango partner page shows NO corridor lines for Colombia, Caspian, Morocco, Tunisia (BPs render, lines don't). Confirmed global, cross-partner.
**Flag data:** `/tasklet/agent/home/yango-program/gulf-and-restamp/CORRIDOR-RENDER-GAP-2026-07-06.json`

---

## Symptom
Boarding points render (separate layer), but corridor **lines are absent** for many markets. Regression: these markets drew before the corridor-inheritance migration (partner-local `featured_routes`/`wow_corridors` retired → 926 archived; render is now `global_canonical ∩ partner.clusters` by cluster_id).

## Root cause — four compounding failure modes in `data-clean/ROUTES.json`

**A. Missing geometry.** Real market corridor networks were never sealed into ROUTES.json.
- `colombia`: **0** routes (Cartagena/Rosario network absent). BPs show, nothing to draw.

**B. Cross-country mis-stamps (WS-4 spatial-anchor fallback).** 10nm anchor + name collisions stamped **89 routes** to the wrong country's cluster. Examples:
- `morocco` ← `muscat-oman → muscat-oman`, `eastern-province-ksa → manama-bahrain` (Gulf water wearing a Morocco label)
- `amalfi-coast-italy` ← `naples-fort-myers-florida-usa` (Naples FL ↔ Naples IT collision, 11 routes)
- `cambodia` ← `phu-quoc-vietnam` (19) · `indonesia` ← `lake-geneva-switzerland` (14) · `mexico` ← `san-juan-puerto-rico`/`usvi-bvi` (20) · `mauritius` ← `sousse-monastir-tunisia`
- Full list in flag JSON `high_confidence_cross_country_misstamps`.

**C. Null cluster_id.** **326** routes still `cluster_id=None`, including REAL market corridors (Tunisia `tunis→tunis`, `hammamet→sousse`; Morocco `mdiq-tetouan`). Null can't match any partner scope → invisible. Distinguish these from the legitimately-null set (CalMac/Scotland, Geirangerfjord/Norway, Okinawa) held in WS-4.

**D. Finance⟂geometry unbound.** `finance/model/corridors.json` DEFINES the corridors but they carry **no route_id binding** to geometry. **26 markets, 0 route_ids each**, across BOTH partners:
- Yango: `yango-colombia`(6), `yango-caspian-az`(6), `yango-caspian-kz`(5), `yango-cote-divoire`(14), `yango-senegal`(7), `yango-peru`(5), `yango-pakistan`, `yango-mozambique`, `yango-namibia`, `yango-venezuela`, `yango-cameroon`, `yango-congo-brazzaville`
- Bolt: `bolt-croatia`, `bolt-italy`, `bolt-france-riviera`, `bolt-portugal`, `bolt-estonia`, `bolt-cyprus`, `bolt-ireland`, `bolt-sweden`, `bolt-spain`, `bolt-romania`, `bolt-finland`, `bolt-israel`, `bolt-lebanon`
- So finance knows the corridors; there is no route_id bridge to drawable geometry.

Plus a namespace split: finance uses partner-prefixed market keys (`yango-colombia`), geometry uses canonical cluster_ids (`colombia`/null). WS-6 renamed only dalmatia/cyprus/amalfi-coast/egypt; the rest still diverge. And a city_id split: `baku-caspian-azerbaijan` vs `baku-azerbaijan` breaks endpoint matching in Caspian.

## Blast radius
Corridors belong to geography (inheritance rule) → every partner sharing a market inherits the same holes. Not Yango-specific: Bolt Europe, Yassir Maghreb, any Italy/Mexico/SE-Asia partner affected via the same ROUTES.json.

## Fix sequence (Grok)
1. **Repair the 89 cross-country mis-stamps** — revert to correct cluster or null; tighten the WS-4 spatial-anchor fallback so it never crosses a country boundary (guard on endpoint country == cluster country; reject name-collision anchors like Naples).
2. **Seal the missing/finance-defined networks into ROUTES.json** with correct cluster_id stamps — Colombia (Cartagena/Rosario) first, then Caspian, Cote d'Ivoire, Senegal, Peru, Pakistan, Mozambique, and the Bolt-Europe set. Source real pier pairs; **nobody invents a pier** — where a pair can't be sourced, leave null and flag back.
3. **Bind route_ids finance⟂geometry** — write sealed route_ids into `corridors.json` for the 26 unbound markets; run `validate_finance_inheritance.py`.
4. **Resolve the 326 null cluster_ids** for real markets; keep the genuine true-nulls null.
5. **Reconcile namespaces** — finance `partner-{market}` ↔ geometry canonical cluster_id; fix `baku-caspian-azerbaijan` → `baku-azerbaijan` city_id.
6. Re-run `validate_partner_inheritance.py` + reseal; confirm Yango Colombia/Caspian/Morocco/Tunisia draw lines on prod.

## Guardrails
- Caspian: Baku↔Aktau (~250nm) is OUT of N30 range — never mint as a corridor (only intra-Baku, intra-Aktau, Aktau↔Kuryk are valid).
- Do not resurrect retired `featured_routes`/`wow_corridors` as the fix — correct the canonical geometry so inheritance renders it.
