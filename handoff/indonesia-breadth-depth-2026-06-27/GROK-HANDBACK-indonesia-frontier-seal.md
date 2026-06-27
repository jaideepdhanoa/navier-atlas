# Grok handback — Indonesia frontier seal (Phase 2)

**Branch:** `main` (direct commit)  
**At:** 2026-06-27  
**Receipt:** `INDONESIA-SEAL-RECEIPT.json`  
**Script:** `scripts/grok-indonesia/seal_indonesia_frontier.py`

---

## What Grok sealed

### Lake Toba — greenfield mint (3 corridors)

| Key | route_id | Distance |
|-----|----------|----------|
| Parapat → Tomok | `rn-db305ed7f029` | 3.2 nm |
| Tuktuk → Ambarita shoreline | `rn-89174b6f31fe` | 8.0 nm |
| Tomok → Pangururan | `rn-35e2eb8d3ca0` | 11.0 nm |

- Freshwater straight-line geometry; `_inland_waterway: true`
- Added to `route_water_allowlist.json`
- **ROUTES.json total:** 7414 (+3)

### Partner bindings (gojek + grab, data-clean + partner-pitch)

| Market | Cleared | Notes |
|--------|---------|-------|
| **lake-toba** | 9/9 nulls | All journeys + featured_routes bound |
| **likupang** | 2/3 journeys | Manado→Bunaken + Likupang→Bunaken → `ics-ab1b7a224c` |
| **singapore** | 7/7 gojek; 8/8 grab journeys | Grab Marina Bay→Sentosa → `rn-76264638fa6b` |
| **lombok** | 6/6 journeys + featured | Komodo, Gili, Mandalika corridors |

### Economics stubs

- `mint_bite2_economics_stubs.py --partner gojek --partner grab --apply`
- **+28 records** in `economics_by_route_id.json` (Lake Toba mints, frontier `ics-*`, Singapore/Lombok seals)
- Status: `estimated` / `bite2_stub_cascade` — Tasklet may replace with deck-grounded rows in Phase 3

---

## Held nulls (explicit — null beats wrong)

| Market | Partner | Item | Reason |
|--------|---------|------|--------|
| likupang | both | Manado → Lembeh Strait (18 nm) | No sealed corridor / BP pair |
| komodo-flores | both | Pink Beach / manta journeys + featured | `pending-bp-seal-pink-beach` |
| komodo-flores | both | Labuan Bajo ↔ Lombok/Mandalika featured | Cross-archipelago; held |
| sumba | both | All 7 journeys + featured (3 phases) | No Sumba corridor registry yet |
| bali-nusa-gili | gojek | 6 hub-level journeys | Cross-geo line-hauls (Komodo 237nm, Sumba 300nm, etc.) — phase-narrative hold |
| riau-singapore / cross-border | grab hub phases | Vietnam/Philippines featured | Out of Indonesia seal scope |

### Raja Ampat

- Featured routes already carry `ics-da5220fd24`, `ics-5840f85047`, `ics-71281cdfb5`, `ics-90f2ce57d8` on journeys
- Economics stubs minted for `ics-5840f85047`, `ics-71281cdfb5` (gojek/grab)
- Corridor registry registration deferred — geometry refs exist, full cascade pending Tasklet Phase 3

### Roll-up dots (karimunjawa, banda, derawan, wakatobi)

- Map footprint present; **no representative corridors minted** in this pass
- Priority B per spec — deferred to next seal lane

---

## Validation receipts

| Gate | Result |
|------|--------|
| Build (`build.mjs --profile=public`) | PASS — 7414 routes |
| Preflight (`preflight.mjs`) | PASS |
| Route linkage (strict) | PASS — 0 blocking gaps |
| Partner scope drift §3.8 | PASS — grab 46/46 live |
| Careem fidelity (P0b) | PASS_WITH_FLAGS — 0 BP errors |

### Build receipts (post-seal)

| Page | Cities | Routes |
|------|--------|--------|
| `/gojek` hub | 18 | 96+ |
| `/grab` hub | 41 | 165+ |
| `/gojek/lake-toba` | 1 | 3 |
| `/grab/lake-toba` | 1 | 3 |

---

## Files changed

```
scripts/grok-indonesia/seal_indonesia_frontier.py
data-clean/ROUTES.json
data-clean/route_water_allowlist.json
data-clean/economics_by_route_id.json
data-clean/partners/gojek.json
data-clean/partners/grab.json
partner-pitch/partners/gojek.json
partner-pitch/partners/grab.json
finance/recal/corridors-gojek.json
handoff/indonesia-breadth-depth-2026-06-27/INDONESIA-SEAL-RECEIPT.json
handoff/partner-map-model/bite2-econ-stubs-report.json
```

---

## Tasklet Phase 3 — ready to start

1. Bind any remaining featured nulls if corridor registry completes (Raja Ampat, Sumba)
2. Replace bite2 stub economics with deck-grounded cascade per market
3. Cascade → transparent sheet + master tracker + economics sidecar
4. Parity QA Gates A–F both partners
5. Decks remain untouched

---

*Grok Phase 2 complete. Hand back to Tasklet for economics cascade + sheet refresh.*