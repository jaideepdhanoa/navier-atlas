# GROK SPEC — Sovereign Suppression + Redundancy Dedupe + Norway Leftover (2026-07-06)

Three curation tasks off the current live set (`18f6e0e9`, 6,883 routes / 6,448 live).

---
## 1. Sovereign-corridor suppression for COMMERCIAL partners (Jaideep approved)
Now that `ksa-commercial` is merged into `saudi-arabia`, commercial partners (Bolt, Yango) scoped to `saudi-arabia` would inherit sovereign PIF giga-project corridors. Suppress **pure intra-giga-project corridors** from commercial partner render.

- **Sovereign asset city_ids:** `neom-sindalah-ksa`, `red-sea-global-ksa`, `the-red-sea-archipelago-ksa`, `amaala-triple-bay-ksa`, `thuwal-private-retreat-ksa`.
- **Suppress** (do NOT render on commercial partner pages `/bolt*`, `/yango*`): any corridor where **BOTH** endpoints are sovereign-asset cities (pure resort island-hops, e.g. Ummahat AlShaykh↔Shura, RSG↔Umluj internal). ~131 corridors.
- **Keep** (render): corridors with **exactly one** sovereign endpoint = aspirational trunk bridges (Jeddah→NEOM, Red Sea Global→Umluj-to-commercial). ~13 corridors. Treat as overlay/aspirational tier.
- **Mechanism:** partner-scope/archetype tag, NOT cluster split — cluster stays unified (one Saudi Arabia). Sovereign assets keep full render on their OWN sovereign proposals (RSG deck, PTA).
- **Gate:** `/bolt` KSA page shows Jeddah/Yanbu/Dammam + Jeddah→NEOM trunk; shows NO internal resort island shuttle.

---
## 2. Redundancy dedupe (mint-time hygiene, no coverage loss)
Post-restore audit of live routes finds **481 true duplicate edges** across **295 berth-pairs** — same two berths (identical `from_label`+`to_label`, same city pair) connected by >1 route. These are pure redundancy from overlapping restore sources.
- **Action:** collapse each duplicated berth-pair to **one canonical edge** (keep the `rn-` sealed id / richest geometry; drop the rest). Worst: Malé↔North Malé Atoll 9x, Ishigaki↔Yaeyama 9x, RSG↔Shura 6x.
- **Do NOT touch** distinct berth-pairs — Singapore's 194 / Krabi's 169 distinct intra-metro pairs are real coverage, NOT redundancy. Only collapse EXACT berth-pair repeats.
- Self-berth (from_label==to_label): only 3 live — drop.
- **Gate:** 0 exact-duplicate berth-pairs remain; per-city distinct-OD counts unchanged.

---
## 3. Norway leftover cleanup (market exited)
**91 Norway routes still live** (cluster_id=`norway`) despite Yango exiting Norway Oct-2025 and Norway having no other partner. Some are quarantined, 91 are not.
- **Action:** quarantine/hide all `cluster_id=norway` routes (`_quarantine=true` + `relevance=hide`) unless a non-Yango partner claims Norway. Confirm none render on any live partner/aggregate page.

---
## Acceptance
- `/bolt` KSA: commercial cities + Jeddah→NEOM trunk render; no intra-sovereign island shuttles.
- 0 exact-duplicate berth-pairs; distinct-OD per-city counts preserved.
- 0 live Norway routes on any surface.
- Report: suppressed count, deduped count, Norway hidden count.
