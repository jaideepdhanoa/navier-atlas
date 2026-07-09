# GROK SPEC — Korea TAM/corridor deepening (kakao-mobility · swing · naver)

**Date:** 2026-07-09 · **Lane:** Grok (finance spine rebuild + corridor minting + cascade) · **Tasklet:** L3 sourcing done (this package)

## Problem (Jaideep directive)
Korea TAM is ~$50M — far too thin for a rich economy. Root cause found:

- **Map layer is fine-ish:** 39 canonical `rn-` corridors in `data-clean/ROUTES.json` (cluster `korea`; cities: seoul-incheon, busan-geoje, jeju, yeosu-tongyeong, + seoul-hangang-bus PTA nodes).
- **Finance layer is broken:** `finance/recal/corridors-{kakao-mobility,swing,naver}.json` carries only **11 corridors on synthetic `ics-` route_ids** (not the canonical `rn-` spine) with sidecar-inherited T3 placeholder demand of ~21–29K pax/yr per corridor. That placeholder floor is the entire reason the TAM is small.
- **Reality (sourced this pass):** 10.4M one-way pax/yr found across 13 sourced rows (T1/T2), fares $2.14–$67.86. Verified single flows include Udo gateway ~3.19M, Tongyeong district 1.75M, Incheon Coastal Terminal 1.08M, Oedo cruises ~1–2M boardings, Mokpo↔Jeju 678K, Wando↔Jeju 633K, Busan↔Tsushima 540K.

## Inputs (this package, `handoff/korea-deepening/`)
| File | Contents |
|---|---|
| `KOREA-L3-SOURCING-2026-07-09.json` | 47 corridor rows (13 with sourced demand, 34 honest nulls), 16 market totals. Every number has source URL + tier (T1/T2/T3) + confidence + **level** (`route` / `port_pair` / `port_total` / `market_total`). KRW→USD @1,400. |
| `KOREA-BP-WISHLIST-2026-07-09.json` | 26 verified-traffic piers/terminals missing from the canonical set. `approx_latlon` is flagged — verify exact coords before binding; **nobody invents a pier**. |
| `korea-corridors-canonical.json` | The 39 canonical `rn-` corridors with ODs + distances. |

## Work order

### W1 — Rebuild the Korea finance spine on canonical route_ids
Replace the 11 synthetic `ics-` corridors with the canonical spine: `finance_spine(korea) = 39 rn- corridors ∩ partner.clusters`, **identical across kakao-mobility, swing, naver** (finance-corridor inheritance). Only `L3_locals`, `capture_rate`, `archetype`, `fleet_basis` may differ per partner. Gate: `validate_finance_inheritance.py`.

### W2 — Attach sourced L3 (level discipline)
- `level: route` rows → may bind 1:1 to a matching route_id.
- `level: port_pair` → bind to the OD pair's corridors, allocate transparently if >1.
- `level: port_total` / `market_total` → **allocation pools only. Never bind a port_total to a single route_id** (e.g., the Tongyeong 1,745,223 row currently sits adjacent to rn-eab1a8d9b140 — it is district-level, not that route).
- Do not double count: route rows that are inside a port_total (Udo ⊂ Jeju totals, island routes ⊂ Tongyeong district) must not be summed together.
- 34 null rows stay null at route level — these are proposed water-taxi ODs with no incumbent service. Use the greenfield convention (`greenfield_corridor_factor`, as in Yango) with gateway-throughput proxies noted in the row notes — do not invent route-level demand.

### W3 — Mint missing corridors (priority queue by verified pax)
1. **Udo gateway** — Seongsan/Jongdal↔Udo, ~3.19M one-way (jeju)
2. **Unjin Port (Moseulpo)↔Gapado / Marado** — ~1.07M combined (jeju)
3. **Sammok Wharf↔Sindo/Jangbongdo** — 817,730 pax 2025 (seoul/incheon; bridge-risk flagged)
4. **Oedo cruise piers** — Jangseungpo/Gujora/Dojangpo↔Oedo/Haegeumgang, ~1M customers/yr (south-coast)
5. **Mokpo↔Jeju** (678K) and **Wando↔Jeju** (633K) — mainland trunks; ~90/~55nm → Q-LR lane (within 700nm ceiling)
6. **Busan↔Tsushima** — 540K, cross-border Q-LR (render policy: shows when one endpoint in scope)
7. **Singi↔Geumodo** (243K), **Gaochi↔Saryangdo**, **Samdeok↔Yokjido** — the real Tongyeong-area ODs (payload ODs like Busan↔Yokjido don't exist as services)
8. **Wolmido↔Gueup**, Hallim↔Biyangdo route binding, Chuja link
Verify pier coordinates first (BP hygiene: Tasklet flags, Grok applies, nobody invents a pier). Reseal → `validate_partner_inheritance.py` green → corridors flow to all three partners 1:1.

### W4 — Cleanups found during sourcing
- Duplicate OD: `rn-eab1a8d9b140` vs `rn-f4f4e680146e` — dedupe.
- Suspended/lapsed services stay honest-null with latent anchors recorded: Busan↔Jeju (suspended Dec 2022, hist. ~158K), Busan↔Geoje (killed by Geoga Bridge 2010, pre-bridge ~1M — latent-demand anchor only), Muuido (bridge 2019, terminal demolished), Queen Beetle exit Aug 2024 (use 2024 Fukuoka baseline 255,750 with note).

### W5 — Cascade
Model → sheets → partner JSONs (kakao-mobility, swing, naver) → decks. Deck TAM/SOM slides for all three partners currently reflect the thin model; Tasklet will re-verify deck S-numbers after cascade lands (do not rebuild the decks — they are live-edited; corrected data flows through JSON/source files only).

## Guardrails (permanent, restated)
- Never invent route_ids or L3 numbers — null beats wrong.
- <3nm is a marquee curation gate only, never corridor existence (Hangang hops are 1.1–1.7nm and stay).
- Q-LR ceiling ~700nm. Cross-border render policy applies to Tsushima/Fukuoka.
- Finance spine identity across the 3 Korea partners; overlay-only divergence.

## Expected outcome
With 10M+ sourced annual pax and real fares replacing 11×~25K placeholders, honest Korea TAM lands in the **hundreds of $M** across the three partner ladders — consistent with Grab-Thailand-scale methodology, no inflation needed.
