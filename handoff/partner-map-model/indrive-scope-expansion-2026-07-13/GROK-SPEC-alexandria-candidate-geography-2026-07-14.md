# GROK SPEC — Alexandria candidate marine geography (2026-07-14)

Clean handoff for Grok to mint **candidate** Alexandria geography into the canonical graph. Requested by
Jaideep 2026-07-14. Alexandria stays **candidate / economics-null** until the gates below are met — this spec
mints geography only, never demand, fares, or economics.

## Standing status
Broad-footprint-first, exact-bind-later. Alexandria has a real Mediterranean waterfront with named facilities,
but research found **no scheduled marine transit network with published route-level boardings** — only private
Eastern-Harbour excursion boats (over the sunken monuments near Qaitbay), ~$5 Montaza harbour rides, and
cruise-ship shore excursions. So: mint candidate boarding points + candidate corridors; hold all economics null.

## Mint as candidate boarding points (require authoritative coordinates before binding)
Mirror the DiDi Egypt berth-coordinate discipline (T11/T12): mint as candidate keyed to the named facility;
the geometry solver must validate authoritative named-facility coordinates before the BP leaves candidate state.
Do **not** invent pier coordinates.

1. **Eastern Harbour — Qaitbay Citadel side** (Pharos Island, mouth of the Eastern Harbour). Departure area for
   existing private excursion boats.
2. **Corniche / Bibliotheca Alexandrina waterfront** (Eastern Harbour south shore).
3. **Montaza Palace marina** (east Alexandria; existing ~$5 harbour boat rides depart here).
4. *(optional)* **Stanley** (Stanley Bay/Bridge) — lower confidence; only if a facility coordinate is found.

## Candidate corridors (mint geometry; Grok assigns route IDs — none exist yet)
- Eastern-Harbour heritage loop: Qaitbay ↔ Bibliotheca/Corniche.
- Coastal Corniche hop: Eastern Harbour ↔ Montaza.
All `candidate`, `demand: null`, `fare: null`, `_economics_hold_reason` set. No `rn-*` IDs are asserted here;
Grok mints them on binding.

## Explicit exclusions (do not fold into Alexandria)
- **Marina El Alamein / Porto Marina / Marassi** sit ~100 km west on the North Coast — a **separate market**, not
  Alexandria proper. Do not attach these BPs/corridors to the Alexandria market.
- No Nile/river product (that is Cairo, excluded).

## Hard gates before ANY Alexandria economics (all three required)
1. Authoritative named-facility coordinates validated for each boarding point.
2. A scheduled marine service with **published route-level annual boardings** (not excursion-operator marketing).
3. A locally comparable per-seat fare for that scheduled service.

Until all three hold: Alexandria remains candidate/null — not in the grounded floor, not in any market total, and
**no numbers on partner-facing slides**. Reserve Atlas screenshot slots for Jaideep's insertion only.

## Evidence (accessed 2026-07-14)
- Private Eastern-Harbour boat trips over sunken monuments, Qaitbay (cairoprivatetours.com; getyourguide.com
  Alexandria cruises list is dominated by multi-day Nile packages, not local marine transit).
- ~$5 Montaza boat ride (travel coverage; youtube.com/-Sey4jBzSQU).
- Alexandria Port coordinates 31°12′16″N 29°52′48″E (en.wikipedia.org/wiki/Alexandria_Port) — cruise/commercial
  port, not a passenger marine-transit network.
- No published scheduled-service annual boarding volumes located.
