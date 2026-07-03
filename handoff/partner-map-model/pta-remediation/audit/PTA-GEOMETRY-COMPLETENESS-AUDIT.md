# PTA Program — Geometry Completeness Audit (Phases A–D)

**Scope:** all 44 public-transport-authority proposals touched across Phases A–D.
**Data sources (main@1687754d):** `ROUTES.json` (7,971 route features), `qa_land_crossing_report.json` (authoritative land QA), `PTA-PAIR-GAP-TABLE.json`, and each partner JSON's `journeys_unlocked`. Routes bound to an authority via the `_pta_{authority}` tag **and** by bound `route_id` (anchor-bind). Land measured on the current sealed geometry (`_geometry_land_km`, post-hand-waypoint fix).

---

## 0. Headline

- **421 corridors are sealed across the 44 authorities — and every one is geometrically clean.** Zero land crossings > 50 m, zero quarantined routes, in every phase.
- **The "lots of land crossings" worry does not apply to the PTA authorities.** The 4,984 land-flagged edges in the global QA report are on *other* partner layers (cross-border ride-hail, aspirational non-PTA edges), not our authority networks. Grok's gold pattern only seals at 0 km, and it held.
- **The real completeness gap is not land — it's thinness.** Two distinct issues:
  1. **25 already-declared corridors are pending-seal** (they're scoped, not yet minted into clean geometry) across 13 authorities.
  2. **16 authorities are "thin"** (< 5 sealed corridors) — their live map network is far smaller than the real-world ferry system they represent.
- **One authority renders effectively empty: `rotterdam-mrdh` has 0 sealed corridors** (all 4 pending). That's the single most visible gap.

---

## 1. Phase-by-phase rollup

| Phase | Authorities | Sealed corridors | Land crossings | Thin (<5 sealed) | Declared-but-pending |
|---|---|---|---|---|---|
| **A** — Batch-5 mature | 24 | 352 | **0** | 0 | 11 (small residuals) |
| **B** — outside-lane | 5 | 25 | **0** | 2 | ~4 |
| **C** — anchors + mint-heavy | 8 | 18 | **0** | 8 | 14 |
| **D** — Batch-8 | 7 | 26 | **0** | 6 | 0 (complete as-scoped) |
| **All** | **44** | **421** | **0** | **16** | **~25 hard** |

**Phase A is essentially done and correct** — sealed count = planned network for most (Transport NSW 30/30, Istanbul 27/27, NYC 24/24, Venice 24/24…). The pending "journeys" that show in Phase A are *featured display chips* (marquee aspirational cards), not missing geometry.

---

## 2. Where the real gaps are

### Bucket 1 — `rotterdam-mrdh` renders empty (P0)
0 of 4 corridors sealed. Needs immediate Grok seal of the 4 declared pending corridors.

### Bucket 2 — Mint-heavy six: finish the seal (P1)
Seed cities minted with tiny sealed networks; 14 declared corridors still pending:

| Authority | Sealed / planned | Pending |
|---|---|---|
| rotterdam-mrdh | 0 / 4 | 4 |
| oslo-ruter | 1 / 4 | 3 |
| amsterdam-gvb | 2 / 4 | 2 |
| copenhagen-movia | 2 / 4 | 2 |
| gothenburg-vasttrafik | 2 / 4 | 2 |
| wellington-metlink | 3 / 4 | 1 |

These are honest-pending by design — Grok seal only.

### Bucket 3 — Batch-5 residuals (P1, small)
Seven mature authorities are 1–3 corridors short of their own planned mesh: `singapore-mpa` (8/11), `abu-dhabi-itc` (10/12), `bahrain-motc` (10/12), `dubai-rta` (11/12), `qatar` (11/12), `rakta` (7/8), `wsf` (13/14). **11 corridors total.** Grok seal (some are the WSF/UAE land-QA-pending ones already on the backlog).

### Bucket 4 — Thin greenfield & anchor networks vs real world (P2, scope decision)
Sealed at planned scope, but planned scope is minimal vs the actual system:

| Authority | Sealed now | Real-world network (approx) |
|---|---|---|
| calmac | 3 | ~25–30 Clyde + Hebrides routes |
| kolkata-wbtc | 4 | 20+ Hooghly ghats |
| seoul-hangang-bus | 4 | 7 piers / 6+ links (3 piers minted, under-linked) |
| helsinki-hsl | 4 | Suomenlinna + archipelago |
| amsterdam / copenhagen / rotterdam | 2–4 | multi-line harbour networks |
| hcmc / rio / mersey / toronto | 3–5 | correct as-scoped; modest real networks |

This is a **scope call**, not a defect: do we deepen these to real-world scale, or hold them as credible starter networks?

### Bucket 5 — Documented held honest-nulls (P3)
- `calmac` Oban↔Craignure — Sound of Mull crossing (needs hand waypoints).
- `manila-pasig-ferry` Intramuros downstream — BP not meshed.

---

## 3. Remediation plan — Tasklet lane vs Grok lane

### Grok lane (geometry — seal & mint)
1. **P0 Rotterdam:** seal 4 pending corridors → authority stops rendering empty.
2. **P1 Mint-heavy:** seal remaining 10 corridors (oslo/amsterdam/copenhagen/gothenburg/wellington).
3. **P1 Batch-5 residuals:** seal 11 corridors (respecting the standing guardrails — no `regen_pta_economics.py --all` on batch-5, no WSF growth_case rewrites).
4. **P2:** mint + seal any new BPs/corridors Tasklet sources for network deepening.
5. **P3:** hand-waypoint Oban↔Craignure; mesh Manila Intramuros.
6. **Every pass:** re-run land QA; preserve the 0-crossing record.

### Tasklet lane (sourcing — dossiers & specs)
1. **Author Grok seal specs** for Buckets 1–3 (already-declared pending corridors) — no new sourcing needed, just the seal handoff. I can produce these now.
2. **For Bucket 4 (deepening):** source real-world pier/terminal lists + corridor pairs per authority (broad-footprint-first, exact-bind-second, null-beats-wrong), author BP-mesh expansion specs with seed coordinates for Grok to mint. Priority marquee set: **CalMac, Seoul Hangang, Kolkata**.
3. **Intra-city BP mesh policy** (existing backlog) folds in here.

---

## 4. Recommended sequencing

- **Now (no scope decision needed):** I write Grok seal specs for Rotterdam + mint-heavy (14) + batch-5 residual (11) = **25 corridors**. Pure completion of already-declared network. This clears the empty-render and brings every authority to its own planned scope.
- **Next (needs your call):** pick the marquee authorities to deepen to real-world scale (my recommendation: CalMac, Seoul, Kolkata first). I source + spec; Grok mints + seals.
- **Cleanup:** Oban↔Craignure + Manila Intramuros hand-waypoints.

**Bottom line:** the program is geometrically *honest and clean* — nothing sealed is wrong, and there are no hidden land crossings. What remains is (a) a fast seal-completion pass on 25 already-declared corridors, and (b) a scope decision on how deep to build the thin greenfield networks.
