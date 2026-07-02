# GROK SPEC — Helsinki HSL (Region Ferry Network) authority economics + verify (Phase C Batch-7, anchor-ready)

**Partner:** `helsinki-hsl` · **Authority:** Helsinki Region Transport (HSL / Helsingin seudun liikenne)
**Dossier:** `handoff/partner-map-model/PTA-DOSSIER-helsinki-hsl.json`
**Status:** **anchor-ready, geometry already SEALED.** Net-new partner, both trees. route_ids **bound to real `rn-` routes** in `ROUTES.json` (not null). Fidelity PASS (items=11, bp_err=0, journey_bp=0, land-check clean); build exit 0; no banned terms.

## 1. Geometry — ALREADY SEALED (verify only). 7 bound corridors, city `helsinki-finland`, Pioneer II
| route_id | from → to | nm |
|---|---|---|
| rn-ca17345bf0e8 | Market Square (Kauppatori) → Suomenlinna Main Pier | 1.7 |
| rn-4ab75813e3cc | Market Square → Kruunuvuorenranta (Laajasalo) | 2.3 |
| rn-8523ec0a5309 | Market Square → Vallisaari | 1.8 |
| rn-312e87d88d71 | Market Square → Lonna | 1.5 |
| rn-2025e138f6c3 | Market Square → Korkeasaari (Zoo) | 1.3 |
| rn-c470fde6e58f | Market Square → Pihlajasaari | 1.9 |
| rn-a02134ddb302 | Market Square → Porvoo River Quay | 30.0 |

bp nodes: `bp-fe03528b18` (Market Sq), `bp-1104e2096f` (Suomenlinna), `bp-kruunuvuorenranta`, `bp-vallisaari`, `bp-lonna`, `bp-korkeasaari`, `bp-pihlajasaari`, `bp-porvoo`.

## 2. DOMESTIC SCOPE — cross-border excluded (deliberate)
The atlas has real cross-border corridors from Helsinki that are **OUTSIDE HSL's domestic mandate** and are **excluded** from this authority arc:
- `rn-27744d73b24b` Helsinki (Viking Line) ↔ **Tallinn** ~203.8 nm (Quanta-LR) — real, but international
- `rn-bbb07ba01911` Viking Line ↔ **DFDS Kapellskär** (Sweden) 38.4 nm — international
- `rn-78a59bb55915` "Viking Line → **Stockholm** 2.2 nm" — **JUNK / mis-scaled** (Stockholm is ~200 nm); recommend cleanup.

Do **not** fold these into `helsinki-hsl`. If Navier wants a Baltic cross-border proposal, that's a separate lane.

## 3. Hand-waypoint hazards (if re-charting)
Charted archipelago fairways; **Baltic winter sea-ice** routing (Suomenlinna runs year-round today); low-wake around **protected Vallisaari/Pihlajasaari** nature areas; shallow **Kruunuvuorenselkä** approach for Laajasalo; the 30 nm **Porvoo** line-haul ends in a shallow river-quay approach — explicit hand waypoints. See dossier `routing_hazards`.

## 4. Economics (Grok lane)
No `growth_case`; `pta_authority_regen_pending` → no economics panel until you author it. Apply the PTA public-value convention; lead on HSL's published **emission-free-by-2035 / zero-emission-ops-by-2030** commitment + single-ticket integration. Economics not yet in `economics_by_route_id.json` for these `rn-` ids — pin when authored.

## 5. Acceptance
- `audit_proposal_fidelity.py --partner helsinki-hsl` → PASS
- 7 bound routes resolve; live map shows Helsinki archipelago network; cross-border legs absent from this partner
- No banned terms; build exit 0
