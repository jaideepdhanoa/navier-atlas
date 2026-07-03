# GROK SPEC — Kolkata WBTC (Hooghly Ferry Network) authority economics + verify (Phase C Batch-7, anchor-ready)

**Partner:** `kolkata-wbtc` · **Authority:** West Bengal Transport Corporation (WBTC), Govt of West Bengal — Transport Dept
**Dossier:** `handoff/partner-map-model/PTA-DOSSIER-kolkata-wbtc.json`
**Status:** **anchor-ready, geometry already SEALED.** Net-new partner authored both trees. Unlike Batch-5/6, route_ids are **bound to real `rn-<hash>` routes** already in `ROUTES.json` — NOT null. Fidelity PASS (items=9, bp_err=0, journey_bp=0, land-check clean); build exit 0.

## 1. Geometry — ALREADY SEALED (verify only, do not re-mint)
5 real corridors bound, city `kolkata-india`, all Pioneer II:
| route_id | from → to | nm |
|---|---|---|
| rn-e9a7f7e474e3 | Howrah Ferry Ghat → Millennium Park Jetty | 0.9 |
| rn-97202b12d2ce | Howrah Ferry Ghat → Fairlie Place Ferry | 0.8 |
| rn-46a91df66302 | Fairlie Place Ferry → Bagbazar Ghat | 1.7 |
| rn-b44cfaae1be2 | Dakshineswar Ferry Ghat → Belur Math Ferry Ghat | 1.3 |
| rn-174af2f4a97c | Millennium Park Jetty → Chandannagar Riverfront | 17.9 |

Real bp nodes: `bp-d5ddcaa659` (Howrah), `bp-c3d1996f22` (Fairlie Place), `bp-4767db5fe8` (Millennium Park), `bp-fa48039b00` (Bagbazar), `bp-3121aedcd3` (Dakshineswar), `bp-063ee377c3` (Belur Math), `bp-0ffc8ae32c` (Chandannagar).

**Action:** confirm the 5 bound routes render on the live map for `kolkata-india`. If the 17.9 nm Millennium Park↔Chandannagar geometry needs a hand-waypoint pass for the Hooghly channel (bridge piers, tidal bends), apply it — but the route_id stays.

## 2. Hand-waypoint hazards (if re-charting any leg)
Hooghly channel centreline; route the charted navigation spans under **Howrah Bridge (Rabindra Setu)** and **Vidyasagar Setu** clear of piers; tidal-bore/current-aware; dense country-boat + barge traffic; monsoon silt + pontoon-jetty approaches. See dossier `routing_hazards`.

## 3. Economics (Grok lane) — author authority public-value economics
No `growth_case` emitted; `_economics_status: pta_authority_regen_pending` → no economics panel renders until you author it. Apply the PTA public-value convention (fare/operating frame, congestion-relief + decarbonization value; no forbidden GMV/TAM keys). Lead on the **live electric-ferry program** ('Dheu' delivered Jan 2025 + 13 hybrid ferries under construction; World Bank IWT program) as the credibility spine. Economics not yet in `economics_by_route_id.json` for these `rn-` ids — pin when authored.

## 4. Optional mesh
Network is a spine, not a full mesh. If WBTC's full ghat list warrants, additive intra-Kolkata BPs only (Armenian Ghat, Bagbazar↔Kuthighat, Shipping etc.) — additive, ID-based, never curate away the 5 bound routes.

## 5. Acceptance
- `audit_proposal_fidelity.py --partner kolkata-wbtc` → PASS
- 5 bound routes resolve in ROUTES.json; live map shows Kolkata network
- No banned terms; build exit 0
