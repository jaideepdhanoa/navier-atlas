# Changelog for Claude — 2026-06-02 (PM) · Partner expansion + Sales Activation

## Summary
Coverage-completion + sales-activation wave. **No atlas rebuild** — POI/route blobs are unchanged
from the 18:30 build (11,214 POIs · 5,072 routes · 0 land-crossers). This wave adds **7 new partner
proposals**, syncs the **BD pipeline DB to 44 partners**, ships **10 forwardable one-pager PDFs**, and
delivers the **BD Studio pipeline app**. Re-sealed `data-clean/` reflects the 44 partners.

## Partner proposals: 37 → 44
Seven new pages authored (all leak-clean, schema-valid, final phase ≥50 vessels, `tier` set):

| partner_id | category | tier | note |
|---|---|---|---|
| `jih-global` | `investment_jv` | flagship | The live $100M / ~100-vessel Maldives deal as a proof page. Stage = **pilot**. |
| `maldives-government` | `transit_authority` | priority | Resident inter-atoll public-ferry decarbonisation angle (distinct from resort transfers). |
| `universal-enterprises` | `luxury_portfolio` | watch | Maldives asset owner / portfolio. |
| `crown-champa` | `hospitality_brand` | watch | Multi-resort operator (Lhaviyani cluster). |
| `villa-hotels` | `luxury_portfolio` | watch | High-volume owned properties near capital. |
| `sun-siyam` | `hospitality_brand` | watch | Maldivian-born collection. |
| `constance` | `hospitality_brand` | watch | Luxury Indian-Ocean operator. |

- All reference existing nodes (`male-maldives` + Maldives atoll nodes); referential-integrity gate PASS.
- Partner-page render: continue to filter **category × tier, default `flagship`**. JIH renders on its
  `investment_jv` flagship proof page.

## B5 ride-hail / super-app extensions — VERIFIED COMPLETE
Audited Grab et al.: a prior pass already brought all ride-hail/super-app partners to gold standard.
Grab carries 8 markets (incl. Vietnam, Cambodia, Borneo/Sabah-KK). No new work required; closing B5.

## BD pipeline DB (agent DB) — synced to 44
- `bd_hooks`: 37 → **44** (hooks/positioning/wow-corridor/proof authored for the 7 new partners).
- `bd_outreach`: 37 → **44** (JIH = `pilot`; maldives-government = `not_started`; owner-groups = `not_started`).
- `bd_contacts`: 64 (unchanged; outreach-hold flags intact on RTA/ITC/DMCA).
- `tier` synced into `bd_hooks` from the partner files for all 44 (13 flagship / 26 priority / 5 watch).

## Sales activation collateral
- **10 forwardable one-pager PDFs** → `partner-pitch/one-pagers/pdf/` (leak-clean, Navier-branded):
  8 archetype sheets (ridehail/super-app, transit_authority, ferry_operator, hospitality_brand,
  luxury_portfolio, marina_network, sovereign_developer, destination_region) + N35 product + Maldives proof.
  - **Spec note:** N35 range stated as **~70 nmi** (locked canon), correcting the outlines' legacy "~50 nmi".
  - Internal price (`<$2M`) and hybrid-range figures **omitted** from external PDFs per leak rules.
- **BD Studio pipeline app** → `/agent/home/apps/navier-bd-studio/` (instant app): kanban by stage,
  filter by tier × archetype (default flagship), per-partner hook/corridor/proof + researched contacts,
  inline stage editing. Reads the BD DB live.

## Leak gate
Ship surface (blobs + 134 briefs + 44 partners) and all 10 PDFs scanned: **0 hits**.
Fixed this wave: saudi-pif `investor`→`infrastructure platform`; 6 meteorological "raise" false-positives.

## Deploy
- Tasklet stayed in-lane: no `index.html`, no Vercel, no GitHub push.
- Sealed `data-clean/` (44 partners) + this changelog are in the export zip. Merge + deploy via Claude.
- Frontend: pick up the 7 new partner pages; confirm category × tier filter defaults to flagship.
