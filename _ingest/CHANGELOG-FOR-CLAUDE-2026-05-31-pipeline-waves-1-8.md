# Changelog for Claude — Research Pipeline Waves 1–8 (POI conveyor sweep)

_2026-05-31 · Tasklet · source-enrichment lane (v4). **A full rebuild + reseal + scorecard rescore is required to materialize all of this on the live map.**_

## TL;DR
Ran the dense boarding-point conveyor across the entire under-developed backlog. **Source BP corpus nearly doubled: ~4.5k → 8,446 BPs across 86 files. 77/86 cities now `search_depth: deep` (was 32).** Only 2 remote dive-atolls remain below the standard floor at their honest geographic ceiling.

## What changed (source data only)

### Wave 1 — Marquee finishers
- **NEOM** (`neom-sindalah-ksa`): densified 37 → 58 BPs; `search_depth: deep`.
- **Red Sea Global** (`red-sea-global`): densified 41 → 53 BPs; **added 3 inter-corridors to `route-demand-config.json`** (red-sea market): RSG↔Jeddah (~250 nm Quanta-LR), RSG↔NEOM (~160 nm Quanta-LR), NEOM↔Jeddah (~400 nm Quanta-LR). All >70 nm → Quanta-LR (amber dashed).
- **Palm Beach** (`palm-beach-florida-usa`): added two **cross-cluster** spokes to its `.md` node table + routes — Palm Beach↔Miami (~60 nm Pioneer II) and Palm Beach↔West End/Grand Bahama (~56 nm Pioneer II). These resolve to the `miami-florida-usa` and `nassau-bahamas` clusters → true inter-corridors (was inter=0).

### Wave 2 — MENA P0/P1 deep-search closeout (all densified, all now deep)
Jeddah 43→94 · Manama 40→133 · Muscat 44→77 · Sharm 42→140 · Ras Al Khaimah 41→150 (cap) · Sharjah 31→150 (cap) · **Eastern Province 8→65** · Fujairah 7→18.

### Wave 3 — Strategic STUB rescue
- Istanbul (90) + Colombo (106) were already richly conveyed — their scorecard "0 POI" was **stale** (predated the sweeps). A rebuild attributes them correctly.
- **Jakarta** densified 57→150. NOTE: Jakarta still shows "1 node / 0 intra" — it needs a **node split** (Jakarta Bay / Thousand Islands / Ancol) at build so the intra-mesh forms. Flagging for your topology pass.

### Waves 4–8 — conveyor sweep (every genuinely-thin + never-conveyed city)
- **SEA:** Palawan 20→116 · Cebu 26→149 · Manila 26→131 · Riau/Bintan 17→131 · Boracay 13→66 · Siargao 7→20 · Brunei 5→26.
- **Turkey:** Çeşme/Izmir 33→95 · Antalya 49→106 · Bodrum 69→150.
- **Caribbean:** Cancún 7→91 · Turks & Caicos 6→36 · Cayman 5→25 · Aruba/Curaçao/Bonaire 4→70 · Antigua/Barbuda 5→75 · Cartagena 5→55 · St-Lucia/Grenadines 7→81.
- **Indonesia secondary:** Karimunjawa 4→42 · Banda 5→32 · Likupang 5→35 · Lake Toba 5→22 (freshwater — name-filter validated; real Toba ferry ports) · Derawan 5→13* · Wakatobi 4→16*.
- **East Asia:** Jeju 50→96 · Busan 57→150 · Yeosu 31→127 · Da Nang 61→117 · Phu Quoc 49→123 · Ha Long 45→125 · Penang 46→150 · Kaohsiung 40→135 · Penghu 29→150 · Koh Rong 29→78 · Hokkaido 28→79 · Sabah/KK 37→84 · Izu Peninsula 20→97 · Yaeyama 28→53 · Okinawa-main 49→109 · Setouchi 66→150 · Salalah 31→43.

\* Derawan (13) + Wakatobi (16) remain below floor — genuinely remote dive archipelagos at honest geographic ceiling; do NOT pad with junk (record registry `note`).

## What YOU (Claude) need to do
1. **Full rebuild** — reattribute all new BPs (BP_CITY_MAP unchanged/correct), regenerate the intra-cluster mesh (route counts will jump massively from the denser graphs), and emit the 3 new RSG/NEOM corridors + Palm Beach cross-cluster routes.
2. **Jakarta node split** at build (see Wave 3).
3. **Reseal** (`data-clean/`) — leak gate + brief_conformance gate; all new BP names are place-names (low leak risk) but run the gate as always.
4. **Rescore** the coverage scorecard — DONE count should jump well past 20. The current `COVERAGE-SCORECARD.md` is stale (09:57, pre-sweep).
5. Redeploy.

## Notes
- `hong-kong.json` AND `hong-kong-boarding-points.json` both exist (72 BPs each) — possible duplicate; dedupe at build if they collide.
- No leak tokens introduced; all additions are place-names + neutral nm/platform fields.

---
# ADDENDUM — Wave 9-A: Mediterranean (NET-NEW, 11 cities)

Greenlit net-new white-space scan. **11 new Mediterranean anchor cities created end-to-end** (region `Europe-Med`):
mykonos-greece · athens-saronic-greece · split-croatia · dubrovnik-croatia · amalfi-coast-italy · costa-smeralda-italy · venice-italy · mallorca-spain · ibiza-spain · cote-dazur-france · kotor-montenegro.

Each city is **fully wired across all four layers** so your rebuild renders them with no dangling joins:
1. **Boarding points** — seeded + densified via the conveyor (~893 new BPs total; e.g. Côte d'Azur 117, Athens/Saronic 113, Amalfi 95, Split 92, Venice 88, Mallorca 86, Costa Smeralda 73, Kotor 68, Dubrovnik 66, Mykonos 61, Ibiza 44). Files in `atlas-external/boarding-points/{city_id}.json`.
2. **Anchors** — added to `app/data-spine/manual-coords/city-anchors.json` (keyed by city_id = `.md` stem = BP_CITY_MAP value; all three aligned).
3. **Nodes** — created `world-map/regions/europe-med/{city_id}.md` stubs (title + posture + Region + Overview + Sub-clusters table + routes). **Verified: all 11 parse via `parse_city_files.py` with coords resolved, 4 POIs each, zero warnings.**
4. **BP_CITY_MAP** — 11 entries added to `build.py` (identity map; each resolves to its real node → dangling-join gate passes).
5. **Briefs** — 11 starter-tier briefs in `partner-pitch/city_briefs/` (and sealed on next seal). All carry the v2 analytical fields + `brief_tier:"starter"`; 0 Pioneer II cap violations; 0 leak hits; valid JSON.

**Marquee Mediterranean theses to note:**
- **Venice** (P0) — the textbook hydrofoil case: the moto-ondoso (wake) regulation is a *feature* for a foiler that lifts its hull clear; boats are the entire transport network.
- **Amalfi/Naples** (P0) — one of the world's densest premium passenger-ferry markets; road gridlock makes water decisively faster.
- **Côte d'Azur** (P0) — the original superyacht coast + a year-round HNW commute layer (Nice↔Monaco).
- **Mallorca** (P0) — the Med's largest charter/refit base.

**Studio manifest** regenerated to include all 11 (now visible in Mobility BD Studio Cities workspace + the Entities Registry markets).

**No corridors added between Med cities yet** — intra-cluster mesh will auto-form from the dense BPs on your rebuild; cross-cluster Med corridors (e.g. Kotor↔Dubrovnik ~25 nm, Sardinia↔Corsica ~15 nm) can be declared next pass if you want them as trunk lines.
