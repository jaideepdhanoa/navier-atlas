# PTA Real-World Completeness — Remediation Master Plan

**Directive (Jaideep, 2 Jul 2026):** Build every touched authority to its **real-world network** — no "held/starter" networks. Deliver **one clean handoff to Grok** for corridor routing + hand-waypoints so there are **zero land crossings**.

**Definition of done (per authority):**
1. BP mesh = the authority's real-world piers/terminals (broad-footprint-first, exact-bind-second, null-beats-wrong).
2. Corridor set = every real scheduled water link between those piers (1:1 with the real network; no invented links, no curated subset).
3. Every corridor sealed by Grok at 0 km land (hand-waypoints where needed).
4. Featured `journeys_unlocked` chips all resolve to sealed routes.

---

## Execution lanes

### Tasklet lane (sourcing + spec)
- Source real pier lists + coordinates + full corridor pairs per authority.
- Author **seed-and-seal specs** (BP seeds w/ coords + corridor list + hand-waypoint hints for known land obstructions).
- Bind partner JSONs from Grok mint receipts.

### Grok lane (geometry)
- Mint BPs from Tasklet seeds; route + seal every corridor at 0 km; hand-waypoints on all water-vs-land ambiguities.
- Re-run land QA each pass; preserve the 0-crossing record.

---

## Phases

### R1 — Seal-completion (declared corridors, endpoints already minted) — **READY NOW, no sourcing**
10 mint-heavy corridors whose BPs already exist → pure Grok seal.
| Authority | Corridors | Base sealed now |
|---|---|---|
| rotterdam-mrdh | 3 (Dordrecht, Kinderdijk, Hoek van Holland) | 0 ← empty-render fix |
| oslo-ruter | 3 (Nesoddtangen, Hovedøya, Bygdøy) | 1 |
| amsterdam-gvb | 1 (NDSM Werf) | 2 |
| copenhagen-movia | 1 (Refshaleøen) | 2 |
| gothenburg-vasttrafik | 1 (Vrångö) | 2 |
| wellington-metlink | 1 (Seatoun) | 3 |
Spec: `specs/GROK-SPEC-R1-mintheavy-seal.md`

### R2 — Marquee real-world deepening — **source + seed-seal**
Full real networks for the three flagship thin authorities:
- **CalMac** (3 → full Clyde & Hebrides lifeline network)
- **Seoul Hangang Bus** (4 → full 7-pier system)
- **Kolkata WBTC** (4 → full Hooghly ghat network)

### R3 — Remaining greenfield/anchor deepening
helsinki-hsl, hcmc-saigon-waterbus, rio-ccr-barcas, mersey-ferries, toronto-island-ferry, manila-pasig-ferry, brisbane, hamburg, kochi + mint-heavy six BP-mesh expansion beyond R1.

### R4 — Phase-B thin + Phase-A residual mint
- fullers360, hawaii (Phase B thin).
- Batch-5 aspirational chips w/o BPs (abu-dhabi, bahrain, dubai, qatar, rakta, singapore, hong-kong): mint BP or honest-null per real-world truth.

### R5 — Held honest-nulls cleanup
- CalMac Oban↔Craignure (Sound of Mull hand-waypoints).
- Manila Intramuros downstream mesh.

---

## Guardrails (permanent)
- ID-based matching only; null-beats-wrong; broad-footprint-first, exact-bind-second.
- Never invent `route_id`/corridors; inherit real network 1:1.
- No `regen_pta_economics.py --all` on batch-5; no WSF growth_case rewrites.
- Economics stays Grok's lane; Tasklet authors honest pending where net-new.
- Serialization: `data-clean` ascii/indent2/newline; `partner-pitch` non-ascii/indent2/newline.

---

## Progress log
- **[DONE] R1** — seal-completion spec authored: `specs/GROK-SPEC-R1-mintheavy-seal.md` (10 corridors, Rotterdam-first). Ready for Grok.
- **[DONE] R2** — three marquee seed-and-seal specs authored from live-sourced real networks:
  - `specs/GROK-SPEC-R2-calmac.md` — 41 new BPs / 27 corridors (Clyde + Southern/Inner/Outer Hebrides).
  - `specs/GROK-SPEC-R2-seoul-hangang-bus.md` — 4 new BPs / 7 corridors (full 8-pier all-stops line + existing express).
  - `specs/GROK-SPEC-R2-kolkata-wbtc.md` — 10 new ghats / 9 corridors (central Hooghly mesh).
  - Sourcing dossiers banked under `dossiers/R2/`.
- **[DONE] R3** — greenfield/anchor deepening spec authored from live-sourced real networks: `specs/GROK-SPEC-R3-greenfield-anchor-deepening.md`.
  - Deepen: **manila-pasig-ferry** 5→13 stations (12 linear corridors); **kochi-water-metro** seal 6 operational routes / 10-12 stations; **hamburg-hadag** 15→21 pontoons / 7 lines; **helsinki-hsl** additive island piers (Lonna/Vasikkasaari/King's Gate).
  - Validated COMPLETE (no deepening): rio-ccr-barcas (4 lines), toronto-island-ferry (3), mersey-ferries (3). NEAR-COMPLETE (optional additive): hcmc-saigon-waterbus (Line 1), brisbane-citycat (~23≈real).
  - Sourcing dossier: `dossiers/R3/SOURCED-NETWORKS.md`.
- **[DONE] R4/R5** — Phase-B seals + honest-null clearance + chip hygiene: `specs/GROK-SPEC-R4-R5-seal-and-chip-hygiene.md`.
  - **R4a fullers360** seal 3 Hauraki Gulf routes (Waiheke/Gulf Harbour/Great Barrier) — endpoints named.
  - **R4b hawaii** seal Lahaina↔Manele (LIVE) + 3 inter-island honest-aspirational.
  - **R5** land-QA seals: **wsf** 4 Puget Sound + **bc-ferries** 4 Georgia Strait (real route_ids present; bcf-d04 horizon).
  - **R4c** batch-5 aspirational-chip bind (RESOLVED): fresh ROUTES pull → conservative endpoint-token match → **18/24 chips bind to real sealed route_ids**, 6/24 kept honest-aspirational (null-beats-wrong). Bind map: `dossiers/R4/BATCH5-BIND-MAP.json`. Render-field flip (dashed→solid) = Grok renderer lane; economics_status preserved (#150 scrub intact). **Not a geometry gap** — base networks already 0-crossing.
- **PROGRAM STATUS:** Full R1–R5 Grok handoff spec set COMPLETE + batch-5 bind map resolved. Every authority touched in Phases A–D now has either (a) real-world-scale sealed geometry, (b) an authored seed-and-seal/land-QA spec for Grok, or (c) validated-complete status. Geometry sealing + hand-waypoints = Grok lane; Tasklet binds partner JSONs from mint receipts.
