# GROK SPEC — Corridor Restore (peak-vs-current regression)

**Date:** 2026-07-06
**Author:** Tasklet (flags only; Grok sources + mints; nobody invents a pier)
**Register:** `handoff/LOST-CORRIDORS-CLASSIFIED-2026-07-06.json`
**Scanner:** `scripts/grok-global/market_coverage_audit.py`

## What happened (root cause, evidence-backed)
- **Peak (Jun 23, commit `9c85d855`): 6,974 route features.** Current sealed build: **4,221**.
- The mid-June densification over-shot: lots of business-POI boarding points auto-generating
  permutation routes, plus out-of-range aspirational hops.
- The cleanup program (scrub w1a–w8 + UAE de-spaghetti + locale/POI cleanup + global reseal) cut
  ~2,750 raw features. **The large majority was correct** — de-duping permutation noise, junk-POI
  endpoint removal, quarantine, retiring featured/wow edges, and cutting land-crossers / out-of-range hauls.
- The reseal also **re-minted geometry → new geom-hash ids** (3,165 old ids gone, 1,983 new ids added,
  2,238 unchanged). This is why a raw id-diff looks catastrophic but is mostly churn, not deletion.
- **True distinct-OD-pair loss (canonical-member endpoints): 394 → 326 = −70 corridors.** THAT is the
  real regression, concentrated in Med/SEA/Gulf coastal markets. Buckets below.

## Restore buckets

### A — RESTORE_in_range (28) — genuine ≤60nm coastal/island OD-pairs, over-culled → RESTORE
Priority. These are real, in-range, water-clean corridors that should not have been dropped. Examples:
Naxos↔Paros, Mykonos↔Naxos, Athinios↔Ios, Paros↔Santorini (Cyclades); Limassol↔Paphos,
Larnaca↔Ayia Napa, Limassol↔Ayia Napa (Cyprus); Nice↔Monaco; Salerno↔Capri; Bonifacio↔Santa Teresa;
Doha↔Al Wakrah; Singapore(HarbourFront)↔Batam Centre; Rhodes↔Marmaris; NEOM↔Sharm El Sheikh;
Dubrovnik(Gruz)↔Kotor; Fujairah↔RAK; Dubai Harbour↔Abu Dhabi Corniche.
> **Action:** re-mint with water-following geometry; re-source any endpoint city that went dark
> (flagged `from-city-now-dark`/`to-city-now-dark` in register). No invented piers.

### B — REVIEW_midrange_qlr_candidate (23) — 60–180nm → RESTORE as Quanta-LR if water-clean
Includes the named report items: **Phuket↔Langkawi (~107nm)**, Busan↔Jeju, Busan↔Fukuoka,
Bodrum↔Mykonos, Çeşme↔Mykonos, Nice↔Bastia, Palma↔Ibiza, Lusail↔Bahrain FH, Abu Dhabi↔Doha,
Langkawi↔Penang, Singapore↔Tioman, Muscat↔Fujairah.
> **Action:** restore as Q-LR trunk where the great-circle is water-clean (no land crossing) and within
> Q-LR range; else hold null. Q-LR render policy already shipped (`route-display.mjs`).

### C — REVIEW_longhaul_out_of_range (18) — >180nm → default CONFIRM-DROP
Muscat↔Abu Dhabi (361nm), Wakatobi↔Banda (373nm), Cartagena↔Aruba (440nm), RAK↔Manama (290nm),
Raja Ampat↔Banda (279nm), etc. Most exceed N30/Q-LR range → correctly removed. **Exceptions worth a
second look** (established real ferry corridors): Bangkok↔Koh Samui (205nm), Goa↔Mumbai (213nm),
Split↔Venice (211nm). Jaideep/Grok judgment; default = stay dropped.

### D — DROP_junk (1) — correctly gone
"Hide-water-body … operational overlay" artifact endpoint. Leave dropped.

## Minting-gap (NOT regression) — separate from the above
Named report items **Bangkok↔Hua Hin** and **Pattaya↔Hua Hin** were **never** in the network:
`hua-hin-thailand` is a canonical city with **no boarding point**. These are BP-sourcing + mint gaps,
tracked in `handoff/MARKET-COVERAGE-GAP-2026-07-06.json` (bucket D isolated cities). Source a real
Hua Hin pier (e.g. Hua Hin Fishing Pier / Cha-am), then mint.

## Guardrails
- Caspian guardrail holds (no Baku↔Aktau-class open-water mints).
- Land-crossing filter + water-following waypoints required on every restore.
- Endpoint labels must resolve to real sourced piers; null beats wrong.
- After restore + reseal, re-run `market_coverage_audit.py` as the acceptance gate.
