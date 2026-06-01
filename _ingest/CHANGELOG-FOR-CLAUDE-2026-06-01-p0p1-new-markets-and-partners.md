# CHANGELOG FOR CLAUDE — 2026-06-01 — P0+P1 new-market scans + 10 new partners

## TL;DR
Sealed a fresh bundle. **126 cities · 12,318 POIs · 3,233 routes (0 land-crossers) · 130 city briefs · 29 partner proposals · 18 externalized stories.** All gates PASS. Bake the website from `atlas-repo/data-clean/` (NOT `partner-pitch/`).

## What changed since the 0626 seal

### New / upgraded city nodes (10 with boarding-point files)
- **Vietnam (Grab priority market):** `ha-long-bay-vietnam`, `phu-quoc-vietnam`, `da-nang-hoi-an-vietnam` (upgraded to full dossiers + BPs), `ho-chi-minh-city-vietnam` (**NEW** — Saigon River urban transit + Vung Tau line-haul + Can Gio/Mekong gateway).
- **Lagos, Nigeria** (`lagos-nigeria`) — NEW. Africa's largest commuter-ferry opportunity (Lagos Lagoon).
- **London / Thames** (`london-thames-uk`) — NEW. Thames Clippers/Uber Boat + TfL.
- **Tokyo Bay** (`tokyo-bay-japan`) — NEW. Tokyo–Yokohama commuter + Izu pointer.
- **Setouchi** (`setouchi-japan`) — upgraded from stub to full dossier (Naoshima/Teshima art-island inland sea) + BPs.
- **Hurghada / El Gouna, Egypt** (`hurghada-el-gouna-egypt`) — NEW. Red Sea Riviera (intra-Egypt only; NO Eilat edges).
- **Angra dos Reis / Ilha Grande, Brazil** (`angra-dos-reis-ilha-grande-brazil`) — NEW. Costa Verde near Rio.

### BP_CITY_MAP (build.py)
Added 6 Wave-14 entries so new-city POIs ingest: `ho-chi-minh-city-vietnam`, `tokyo-bay-japan`, `lagos-nigeria`, `london-thames-uk`, `hurghada-el-gouna-egypt`, `angra-dos-reis-ilha-grande-brazil`. (Vietnam Ha Long/Phú Quốc/Da Nang + Setouchi were already mapped.)

### New partner proposals (19 → 29)
- **Luxury hospitality hubs (hub/spoke):** `soneva`, `four-seasons`, `aman`, `six-senses` — brand → island properties; each market full-depth (partner_context + why_navier_now + 7-key end_state + ≥4 journeys incl. Quanta-LR + ≥4 proof + 3–4 objections + 3–4 phases).
- **Public-transport ferries (flat):** `washington-state-ferries`, `nyc-ferry`.
- **Demand platforms:** `yango` (hub — MENA + Africa whitespace), `shun-tak-turbojet` (flat — Pearl River Delta, distinct from `hong-kong` city page).
- **P1:** `thames-clippers-tfl` (flat, London), `bc-ferries` (flat, Vancouver).

### Grab hub
Added **Vietnam as 6th market** (full hub-depth schema; `why_now` string; HCMC + Ha Long + Phú Quốc + Da Nang journeys).

### Integrity
Registered 2 new known gaps (out-of-corpus inland pointers): `ha-long-bay-vietnam__…red-river-corridor` (Hanoi) and `vietnam__hcmc-mekong-delta…` (My Tho/Can Tho). Both are aspirational Quanta-LR river corridors to unmodeled inland nodes; land-scrubber drops the segments. 0 ERROR-level integrity checks.

## Gate verdicts (SEAL.json)
- externalization: PASS — internal/deck_only stripped
- land_crossing: PASS — 0/3233
- referential_integrity: PASS — 0 new dangling joins
- brief_conformance: PASS — 130 briefs carry required + v2 analytical fields
- leak gate: CLEAN — 0 hits across briefs + partners

## Build notes for Claude
- Hub/spoke routing now needs index/market pages for the new hubs: `/soneva`, `/four-seasons`, `/aman`, `/six-senses`, `/yango` (+ existing `/uber`, `/grab`, `/bolt`).
- Stories generator is markets-aware; walks `markets[].phases`.
- Bake from `data-clean/`. `data-clean/{city_briefs,partners}/` are the public-stripped surface.
