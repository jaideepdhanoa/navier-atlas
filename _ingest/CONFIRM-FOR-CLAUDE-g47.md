# Confirmations for Claude — Gold #47

Two open confirmations from the post-#44/#46 punch-list, answered against the
Gold #47 working surface (5,260 routes; 80 econ records / 21 pending).

---

## ✅ Confirmation 1 — the "89 single-token weak matches" (#33/#44 audit)

Re-ran the #33/#44 audit tool (`geo_audit_dump.py`) + the endpoint-label
token-overlap logic across the **full partner-pitch surface** (113 unique
route-linked items, all 46 partner dossiers) on Gold #47:

| verdict | committed partners | speculative dossiers | total |
|---|---|---|---|
| OK | — | — | 60 |
| WEAK_SINGLE_TOKEN | 6 | 28 | 34 |
| HARD MISMATCH | 2 | 17 | 19 |
| DANGLING | 0 | 0 | **0** |

**Committed partners (Grab / Careem / JIH / Saudi-PIF / Red Sea) are clean.**
- The 6 committed WEAK binds are all **legitimate single distinctive anchor tokens**, not mis-binds:
  - Careem: `Dubai`, `Dubai`, `Sharjah`; Grab: `Gaya` (the Borneo Mabul→Gaya fix); Saudi-PIF: `Jeddah`, `Manama`. The label and the gold route agree on the place; the tokenizer just finds one shared distinctive token because the rest are generic ("marina","resorts","waterfront", etc.).
- The 2 committed "MISMATCH" are **JIH `Velana International Airport ↔ Greater Malé / Hulhumalé`** bound to `ics-e38bf95ac7` (Malé → North Malé Atoll) and `ics-80ea7da4a8` (Malé Jetty No.1 → Malé). Velana airport sits **on** North Malé Atoll adjacent to Malé/Hulhumalé, so the geometry is correct — it's a concept-level airport-transfer label over the right Malé boarding points, not a geo-error. (Flagged WEAK only because "velana"/"airport" don't token-match "malé".)

**The #33/#44 weak/mismatch backlog therefore survives only as a SPECULATIVE-dossier relink queue** — the original label-first fuzzy binds that the Geometry-First Principle now bans. They do not touch any live/committed deck.

### Geometry-first relink backlog (speculative dossiers — 17 hard mismatches)
Partners with label↔geometry mismatches still to relink or null:
`aman, gojek, hawaii, kakao-mobility, line, lyft, maldives, ola, rapido, uber`.
Recommend: geometry-first relink (resolve route_id from endpoints) or null per
"null beats confidently-wrong". None are shipped on a committed partner deck.

---

## ✅ Confirmation 2 — East Coast → CBD economics "drop" was intentional

Confirmed: it was **defer-until-built**, not an accident. In the Gold #46 sidecar
both Singapore marquee corridors lived in `_pending_route_pin` with
`reason: "endpoints_city_level_not_pinned"` — i.e. the corridor had no gold
route to attach economics to (0 routes), so per the exactness mandate no record
was emitted (absent record = no economics yet, never a guess).

**Now resolved in Gold #47.** I built the two corridors geometry-first (C1 East
Coast→Marina/CBD `rn-82453f6cb33e`, C2 Marina→Changi `rn-e94c308a28e3`), bound
them in `corridors.json` to those exact route_ids + endpoint nodes, and rebuilt
the sidecar: **records 78 → 80, pending 23 → 21**, Singapore pending cleared.
Grab grounded floor unchanged (128 boats / $38,966,306).

---

_Generated during the Gold #47 autonomous build pass._
