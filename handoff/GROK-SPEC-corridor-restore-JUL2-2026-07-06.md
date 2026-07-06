# GROK SPEC — Corridor Restore (JULY-2 pre-cull baseline) — SUPERSEDES peak-vs-current

**Date:** 2026-07-06
**Author:** Tasklet (flags only; Grok sources + mints; nobody invents a pier)
**Reference build:** main @ `1687754d` (July 2 22:32 UTC) — the most recent build **before** the July 5–6 cull
**Register:** `handoff/LOST-CORRIDORS-JUL2-CLASSIFIED.json`
**Scanner/acceptance:** `scripts/grok-global/market_coverage_audit.py`

> This supersedes the Jun-23-peak spec (`GROK-SPEC-corridor-restore-2026-07-06.md`). Jun-23 was
> mid-densification; July-2 is the correct "just-before-culling" reference Jaideep asked for.

## Contrast (July 2 vs current)
- Raw features: **7,971 → 4,221** (−3,750).  Most of the raw drop is correct: permutation-noise
  de-dupe, business-POI endpoint removal, retired featured/wow, quarantine, land-crossers, out-of-range.
- **Distinct city-to-city corridors: 455 → 342 = −113.**
- Of 116 distinct lost OD-pairs:
  - **58 GENUINE RESTORE** — 37 in-range (3–60nm) + 21 Q-LR (60–180nm)
  - **58 CORRECT DROPS** — 35 trivial self-referential / <3nm hygiene + 21 long-haul (180–400nm) + 2 >400nm

## CORRECTION vs prior spec
Prior spec said Bangkok↔Hua Hin / Pattaya↔Hua Hin were "never minted (Hua Hin has no BP)". **Wrong
against July 2.** All three named report items existed on July 2 and were culled:
- `krabi-thailand ↔ langkawi-malaysia` (~104nm, labeled "Phuket → Langkawi") — B_restore_qlr
- `bangkok-thailand ↔ hua-hin-thailand` (~76nm) — B_restore_qlr
- `hua-hin-thailand ↔ pattaya-thailand` (~56nm) + `hua-hin-thailand ↔ cha-am-thailand` (~13nm) — A_restore_in_range
The **`hua-hin-thailand` boarding point was removed during the locale/POI cleanup** and must be
re-sourced (real pier: Hua Hin Fishing Pier / Cha-am), then the corridors re-minted.

## RESTORE LIST — A (37 in-range, 3–60nm) — genuine coastal/island over-culls → re-mint water-clean
Highlights (full list in register):
- **Thailand (10):** Bangkok↔Pattaya (53), Hua Hin↔Pattaya (56), Hua Hin↔Cha-am (13),
  Koh Lanta↔Krabi (27), Phuket/Phang-Nga↔Koh Lanta (42), Koh Lanta↔Koh Phi Phi (17), Pattaya↔Koh Larn (5)
- **UAE (6):** Dubai↔RAK (51), Dubai↔Abu Dhabi (47), Dubai↔Sharjah (20), RAK↔Fujairah (45)
- **Greece (5):** Mykonos↔Santorini (19), Mykonos↔Naxos (22), Naxos↔Santorini (44)
- **Cyprus (5):** Limassol↔Larnaca (33), Limassol↔Paphos (32), Larnaca↔Ayia Napa (18), Limassol↔Ayia Napa (51)
- **France/Riviera (4+2):** Nice↔Monaco (7), Cannes↔St-Tropez (23), Nice↔St-Tropez (38), Bonifacio↔Santa Teresa (9)
- **Turkey-Aegean (4):** Bodrum↔Rhodes (11), Çeşme↔Chios (9)
- **Korea (3):** Yeosu-Tongyeong↔Busan-Geoje (4)
- **Indonesia (3):** Riau↔Singapore (10), Riau↔Desaru (19)
- **Italy (2):** Amalfi↔Naples-Capri (13); **Spain (2):** Mallorca↔Menorca (53)
- **Qatar (2):** Doha↔Al Khor (4); **Bahrain:** Manama↔Doha (19); **Croatia:** Dubrovnik↔Kotor (5)

## RESTORE LIST — B (21 Q-LR, 60–180nm) — restore as Quanta-LR if water-clean
Phuket↔Langkawi (104), Bangkok↔Hua Hin (76), Langkawi↔Penang (66), Busan↔Jeju (157),
Busan↔Fukuoka (110), Bodrum↔Mykonos (103), Çeşme↔Mykonos (69), Nice↔Corsica (157),
Mallorca↔Ibiza (68), Naples↔Aeolian (131), Athens↔Mykonos (82), Rhodes↔Antalya (117),
Larnaca↔Beirut (113), Komodo↔Sumba (83), Sabah↔Brunei (64), Singapore↔Tioman (92),
Kaohsiung↔Penghu (69), Al Wakrah↔Doha (73), Abu Dhabi↔RAK (108), Fujairah↔Muscat (148),
Abu Dhabi↔Al Wakrah/Qatar (173).

## CONFIRM-DROP (58) — leave dropped
- **35 hygiene:** same-city self-referential + sub-3nm marina hops (Palm Jumeirah inner, Larnaca marina↔airport, etc.) — correctly removed by de-spaghetti/marquee floor rules.
- **23 out-of-range (>180nm):** Muscat↔Abu Dhabi (361), Cartagena↔Aruba (440), Raja Ampat↔Banda, etc. — beyond N30/Q-LR. Second-look exceptions (real ferry lanes, Jaideep judgment): Bangkok↔Koh Samui, Goa↔Mumbai, Split↔Venice — default stay-dropped.

## Guardrails
- Nobody invents a pier. Re-source removed endpoints (Hua Hin first) from real infrastructure.
- Water-following geometry, land-crossing filter, Caspian guardrail all hold.
- After restore + reseal, `market_coverage_audit.py` is the acceptance gate.
- Redeploy of `2b51b357` still relights every corridor that *survived* the cull but is dark on stale prod.
