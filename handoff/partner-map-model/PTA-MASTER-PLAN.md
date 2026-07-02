# Navier PTA Program — Master Plan & Work Ledger

**Owner:** Tasklet · **Author date:** 2026-07-02 · **Status:** living document (update as PRs land)
**Decisions locked:** 2026-07-02 (see §9) — Batch-7 order confirmed, Kolkata in-scope now, Phase C per-authority PRs, Seoul dual-path, Batch-8 greenlit as Phase D.
**Gold reference partner:** `bahrain-motc` · **Convention:** `handoff/partner-map-model/PTA-ECONOMICS-CONVENTION.md`
**Grok's intake checklist (source of truth for PRs 1–7):** `handoff/partner-map-model/PTA-TASKLET-CHECKLIST-PR-PLAN.md` (committed `11b2a86e`)

> **Purpose.** This is the single planning surface for the public transport authority (PTA) program so nothing is dropped and no shortcuts are taken. It reconciles (a) Grok's 7-PR intake checklist for the 24 sealed Batch-5 authorities + 6 outside-lane authorities, and (b) the proposed Batch 7 / Batch 8 waves of new authorities. Work is organized into **phases** with explicit files, fields, acceptance gates, dependencies, and per-authority sourcing status. Check items off as they land; never mark done without the acceptance command passing.

---

## ▶ Progress log

### ✅ Phase A — Batch-5 completion — COMPLETE (2026-07-02) · PRs #150–#154 open, awaiting Jaideep merge
- **PR-1 · #150** — economics presentation scrub, all 24 authorities (48 files, −1,086 net lines). Removed `_render_chip_flag`, `_marine_tam_split_provenance` (7), `_grok_regen`, forbidden `journey_gmv`+`marine_mobility_tam` (4); relabeled revenue/phase headlines to lead with public value; de-duped 13 partners' levers from real dossier `decarb_note`; authority-specific fare systems in operating_model. Build 0, forbidden-key sweep 0.
- **PR-2 · #151** — mumbai-mmb fidelity TRIM. 9 distance syncs + 2 mis-bound routes unbound (junk endpoints) & flagged for Grok re-seal. Audit PASS.
- **PR-3 · #153** — brisbane-citycat + hamburg-hadag distance sync. Audits PASS.
- **PR-4 · #152** — nyc-ferry, sf-bay-ferry, transport-nsw, boston-mbta-ferry, stockholm-waxholm distance sync. Audits PASS.
- **PR-5 · #154** — authority hero voice pass. 5 authorities aligned to gold "Authority proposal" eyebrow + place-specific network titles. bc-ferries/hawaii deferred to Phase B full rewrites. Bahrain 21.2nm inner-harbour anomaly flagged for Grok.
- **⚠️ Grok sequencing note (from PR-1):** these presentation fields are now Tasklet-final post-regen. Do **not** blindly re-run `regen_pta_economics.py` on the 24 or it reverts operating_model/levers/headlines.
- **Next:** Phase B (Batch-6 new lane — PR-6/7).

---

## 0. How to use this document

- **Order matters.** Phases A → B → C → D. Within Phase A, follow Grok's PR order (PR-1 first — fastest win, unblocks nothing but clears the most debt).
- **Every partner edit touches two trees:** `data-clean/partners/<slug>.json` (ships) **and** `partner-pitch/partners/<slug>.json` (authoring mirror). They must stay in sync on every edit.
- **Tasklet lane = presentation + narrative + dossier + Grok spec.** Grok lane = route seals, quantified economics numbers, renderer. Never cross into sealed `route_id` geometry, `scripts/pta/regen_pta_economics.py` quantified metrics, or `index.html` renderer.
- **Acceptance is a command, not a vibe.** Each PR lists the exact audit/build command that must pass before it's called done.
- **PRs are copy-review surfaces; merges are Jaideep's call.** Open a PR only when a theme is fully complete and self-verified.

---

## 1. Governing rules (guardrails — do not shortcut)

**PTA economics convention (hard rules):**
- ❌ No partner-facing **SOM / SAM / TAM / GMV / journey wallet / super-app / platform take** language.
- ❌ No internal finance taxonomy (`atom.py`, multipliers, derivations, `_mid (…)` strings, `water_transport_market` rung).
- ✅ **Lead with public value**; revenue is the supporting operating layer.
- ✅ Quote the **mid** figure; band + label every projected figure; never headline the optimistic ceiling.
- ✅ Fares/frequencies/cost-recovery are **"set with the authority"** — never fabricate subsidy-per-passenger numbers.

**PTA gold pattern (all batches):**
- Kill Prove/Scale/Mature phase language → **Starter service → Full network → Mature network**; geography-led phasing.
- Domestic-first arc; real sourced boarding-point pairs; ID-based matching only; **null beats confidently-wrong**.
- Honest-null `route_id` + `_link_status: "pending-seal"` / `"geometry_seal_pending"`; Grok mints routes with **explicit hand-waypoints (no land crossings)**.
- Both `data-clean/partners/` and `partner-pitch/partners/` trees mirrored.
- Must read as **super-professional and credible for a transport ministry.**

**Data discipline:**
- `archetype` chips use the canonical set; PTA uses `public_transit`. Chip renders as a visible capitalized label — keep partner-safe.
- New-geo seeds: mint `priority_city` / city feature with exact keys + register in the matching cluster; tag `_seed_node: true` for Grok. Seeds are **additive only until validated**.

---

## 2. Current-state snapshot

**Grok has shipped** (do not redo): route seals for all 24 Batch-5 authorities, `regen_pta_economics.py` for all 24, and the PTA public-value renderer (`_ptaEconomicsHtml` in `index.html`, live `a0ab6dfc`).

**Fleet in scope right now:**
- **24 Batch-5 authorities** — sealed geometry; Tasklet owes presentation scrub + fidelity TRIM + narrative.
- **6 outside-lane `public_transit` partners** — still on commercial framing; need full PTA rewrite (Batch 6).
- **Batch 7 candidates** — new authorities (electric-ferry capitals); most need new-geo sourcing.
- **Batch 8+ bench** — credible but lower electrification signal.

**Only `bahrain-motc` presentation is marked "applied."** The other 23 (+ Bahrain cleanup) still owe the scrub.

---

## 3. PHASE A — Batch 5 completion (Grok's 7-PR stack)

> Grounded 1:1 in `PTA-TASKLET-CHECKLIST-PR-PLAN.md`. Run the fidelity audit after each TRIM PR:
> ```bash
> python3 scripts/audit_proposal_fidelity.py --partner <slug>
> node scripts/audit-partner-route-linkage.mjs --partner <slug>
> ```

### PR-1 — Economics presentation scrub (all 24) ⟶ *fastest win, do first*
**Partners:** all 24 Batch-5 authorities. **Blocks:** none.

Apply to **both** trees per partner. `growth_case` edits:
- **Delete** `growth_case._render_chip_flag` (all).
- **Delete** `growth_case._marine_tam_split_provenance` — **7 carry it:** `bahrain-motc`, `nyc-ferry`, `qatar`, `singapore-mpa`, `thames-clippers`, `transport-nsw`, `wsf`.
- **Delete** `growth_case.revenue_potential.cite_rule` (if present).
- Relabel `growth_case.revenue_potential.headline` → *"Indicative operating revenue as the network matures — public value leads."*
- Relabel `growth_case.phase_economics.headline` → *"Network maturity — public value and indicative fare revenue."*
- `growth_case.modal_headline` → `"What it returns to the public"`.
- `growth_case.modal_lead` → authority-specific; no opportunity/prize/wallet/GMV/TAM.
- `growth_case.public_value.levers[]` → replace with full dossier `interpretation_for_navier` + `policy_targets.relevance` (no truncation).
- `growth_case.public_value.operating_model[]` → authority-specific fare system (per-partner table below).
- Verify **no** `water_transport_market` rung remains.
- **Do NOT delete** (Grok owns numbers): `public_value.metrics[]`, `_provenance`. From `ladder_transitions[]` keep plain `headline`/`basis`; drop `derivation`/`multipliers_cited`/`source_fields`.

**Per-partner operating-model / fare system to insert:**

| slug | fare system to name | TAM-split drop? |
|---|---|---|
| abu-dhabi-itc | water-taxi / island-ferry ticketing | |
| auckland-ferries | AT HOP | |
| bahrain-motc | Masar app; Vision 2030 / net-zero 2060 | **drop** |
| bangkok-chao-phraya | BTS Sathorn interchange; MINE Smart Ferry precedent | |
| boston-mbta-ferry | CharlieCard / MBTA | |
| brisbane-citycat | go card / TransLink | |
| dubai-rta | Nol / RTA multimodal | |
| hamburg-hadag | HVV / HADAG tariff | |
| hong-kong | Octopus / existing ferry operators | |
| istanbul-sehir-hatlari | Istanbulkart | |
| kochi-water-metro | Kochi One card | |
| lisbon-transtejo | Navegante | |
| mumbai-mmb | BEST / water-transport tariff (set with MMB) | |
| nyc-ferry | NYC Ferry flat fare / OMNY | **drop** |
| qatar | Sila integration; 2030 emissions target | **drop** |
| rakta | RAK public transport (set with authority) | |
| sf-bay-ferry | Clipper Card | |
| singapore-mpa | existing harbourcraft / MPA licensing | **drop** |
| stockholm-waxholm | SL / Waxholmsbolaget | |
| thames-clippers | Uber Boat ticketing / TfL interchange | **drop** |
| transport-nsw | Opal / Sydney Ferries | **drop** |
| vancouver-seabus | TransLink Compass | |
| venice-actv | ACTV / Venezia Unica | |
| wsf | WSF fare classes / ORCA | **drop** |

**Acceptance:**
```bash
rg '_render_chip_flag|_marine_tam_split_provenance|cite_rule|water_transport_market' data-clean/partners/*.json   # → 0 hits across the 24
BUILD_PROFILE=public node scripts/build.mjs --profile=public
BUILD_PROFILE=public node scripts/build-site.mjs --profile=public   # spot-check intro step 2 on 2–3 authorities
```

### PR-2 — Fidelity TRIM: `mumbai-mmb`  (verdict TRIM: 9 TRIM + 2 DROP)
Receipt: `PROPOSAL-FIDELITY-mumbai-mmb.md`.
- Sync `distance_nm` to sealed geometry on journeys + featured for: `rn-c9bcc9219b04`, `rn-af6a20ee2a0a`, `rn-a685bc50d3c2`, `rn-0c05727c37fa`, `rn-c70751e14751` (cards show 2.1–2.5 nm vs routes 6–13 nm).
- **DROP** `ics-ed747a4789` (Belapur↔Nerul labels ≠ endpoints) and `ics-3964e5583e` (Gateway↔Rewas labels ≠ endpoints).
- **Acceptance:** `python3 scripts/audit_proposal_fidelity.py --partner mumbai-mmb` → PASS, journey_bp=0, trim=0.

### PR-3 — Fidelity TRIM: `brisbane-citycat` (10) + `hamburg-hadag` (7)
- **brisbane-citycat** distance_nm fixes: `rn-771a3b2ef251` (2.6→1.6), `rn-e3914af94b36` (1.0→0.6), `rn-19fbaad122e8` (6.5→3.7), `rn-5a374ade1b89` (3.2→2.2), `rn-35192771d472` (2.4→1.2), `rn-41e5061725f4` (4.4→2.5).
- **hamburg-hadag** distance_nm fixes: `rn-24451443bb54` (3.0→1.5), `rn-3aec7fb1f836` (2.0→0.8), `rn-a5add4c4928b` (1.0→1.5), `rn-9771964f7bdc` (1.0→0.6).
- **Acceptance:** both → PASS, trim=0.

### PR-4 — Fidelity TRIM: remaining PASS_WITH_FLAGS (5)
Pattern: sync `journeys_unlocked[].distance_nm` + matching `phases[].featured_routes[].distance_nm` to sealed length; **do not** change `route_id` bindings.

| partner | trim | route IDs |
|---|---|---|
| nyc-ferry | 4 | `rn-b2490e3f6350`, `rn-711092a81931` |
| sf-bay-ferry | 4 | `rn-cabe543d04e9`, `rn-a82989283656`, `rn-1ffa4b3d5058` |
| transport-nsw | 3 | `rn-0d609ac0ab33`, `rn-2b603df666b7` |
| boston-mbta-ferry | 2 | `rn-a0edcc795e58`, `rn-0183727f495b` |
| stockholm-waxholm | 1 | `rn-72110604025d` (Utö corridor) |

### PR-5 — P2 narrative copy pass (8 + Bahrain stub) — polish only, no structural edits
Partners: `qatar`, `hong-kong`, `transport-nsw`, `thames-clippers`, `nyc-ferry`, `bc-ferries`, `wsf`, `hawaii`, + `bahrain-motc` phase-1 stub. `bc-ferries`/`hawaii`/`wsf` overlap the Batch-6 rewrite (see Phase B).
Per-partner narrative checklist:
- [ ] `partner_context.their_ambition` cites the authority's **published** network/policy target.
- [ ] `partner_context.their_pressure` = congestion/emissions/access (not commercial TAM).
- [ ] `hero.title`/`hero.subtitle` authority-facing, not marketplace.
- [ ] `why_now` ties to decarbonization mandate + existing water service.
- [ ] `phases[].label`/`scope` geography-led (Starter → Full network → Mature).
- [ ] `objections[]` answer subsidy / fare integration credibly.
- [ ] No SOM/SAM/TAM/GMV/journey-wallet anywhere.

### PR-6 / PR-7 — Batch 6 new PTA lane → **detailed in Phase B**

**Phase A checkbox ledger:**
- [ ] PR-1 economics scrub (24)
- [ ] PR-2 mumbai-mmb TRIM
- [ ] PR-3 brisbane + hamburg TRIM
- [ ] PR-4 nyc/sf/tfnsw/boston/stockholm TRIM
- [ ] PR-5 P2 narrative (8 + Bahrain stub)

---

## 4. PHASE B — Batch 6 new PTA lane (6 outside-lane authorities)

> These carry `archetype: public_transit` but have **no** dossier, seal receipt, or PTA economics — still on commercial `growth_case`. Grok's Wave-9 repair already **sealed their journey/featured geometry** (bc-ferries 22/22, wsf 31/31, hawaii 3/3, nyc-ferry 21/21, norway-fjords 4/4), so this is a **copy/economics rewrite**, not a fresh geometry seal — a meaningful head start.

**PR-6:** `bc-ferries`, `hawaii` · **PR-7:** `wsf`, `fullers360`, `maldives-government`, `norway-fjords`, `shun-tak`
*(Note: `wsf` sits in Batch-5's 24 for the scrub/narrative but has no PTA dossier/pair-table entry yet — treat its dossier+rewrite here.)*

**Per-partner deliverables (Bahrain gold template) — one PR per partner group:**
1. **Dossier** `handoff/partner-map-model/PTA-DOSSIER-<slug>.json` (schema from `PTA-DOSSIER-bahrain-motc.json`): `authority`, `policy_targets` (+`relevance`), full `interpretation_for_navier`, `domestic_network.boarding_points[]` `[lng,lat]`+labels, `domestic_network.domestic_pairs[]`, optional `regional_links[]` (amber roadmap), `routing_hazards[]`.
2. **Partner rewrite** `data-clean/partners/<slug>.json` + mirror: `archetype:"public_transit"`, `_public_transit_authority` block, `partner_context`, authority `hero`, domestic-first `phases[]` with `route_id:null` + `_link_status:"pending-seal"`, matching `journeys_unlocked[]`, PTA-convention `growth_case` with qualitative `public_value` (no commercial rungs), `modal_headline:"What it returns to the public"`.
3. **Grok routing spec** `handoff/partner-map-model/GROK-SPEC-<slug>-domestic-routing-YYYY-MM-DD.md` (structure from `GROK-SPEC-bahrain-motc-domestic-routing-2026-06-30.md`): §1 what Tasklet did · §2 what Grok owns (mint BPs, hand-waypoint, land QA, bind route_ids) · §3 hazard table · §4 acceptance gate · §5 economics regen pointer.
4. **Gap table row** append to `PTA-PAIR-GAP-TABLE.json` + regenerate `.md`.
5. **Handoff receipt** in PR description (dossier / partner / spec / seal targets / fidelity pre-seal PASS).

**Per-partner notes:**
- `bc-ferries` — Island Class electrification; Gulf Islands + Tsawwassen–Swartz Bay pressure. Existing `partner_context` is a good seed; replace commercial `growth_case` entirely.
- `hawaii` — inter-island vs harbour-commute framing; **Quanta-LR on roadmap legs only** (`render: amber-dashed`); see GROK-HANDBACK §P3 Hawaii growth_case.
- `norway-fjords` — after rewrite, Grok runs **repair + promote only, no full relink** (do-not-touch). Norway fjord anchors already exist (`stavanger-norway`, `bergen-norway` + rich BPs).
- `shun-tak` — cross-harbour + airport ferries (HK/Macau); clarify public-authority vs commercial-operator relationship in narrative.
- `fullers360` — Auckland commuter ferry; align with `auckland-ferries` AT HOP context; watch for overlap/collision.
- `maldives-government` — National Ferry Network; keep distinct from hospitality Maldives partners; RTL/atoll equity framing.

**Phase B checkbox ledger:**
- [ ] PR-6 dossier+rewrite+spec: bc-ferries, hawaii
- [ ] PR-7 dossier+rewrite+spec: wsf, fullers360, maldives-government, norway-fjords, shun-tak
- [ ] Grok seal PRs follow each (post-merge)

---

## 5. PHASE C — Batch 7 new authorities ("Electric-ferry capitals")

> Wedge: authorities that have **already publicly committed to electric/zero-emission ferries** — Navier is the upgrade to a mode they've already funded. Each new authority = full Batch-6-style deliverable set (dossier → rewrite → Grok spec → seal handoff) **plus** new-geo sourcing where no anchor exists.

**Anchor status verified against `data-clean/FEATURES_BY_TYPE.json` (2026-07-02):**

| Authority | Water body | Electrification signal | Anchor status | Sourcing effort |
|---|---|---|---|---|
| **Kolkata — WBTC / Hooghly** | Hooghly River | in-scope India continuity | ✅ **City node `kolkata-india` + Hooghly BPs exist** (Howrah, Fairlie Place, Millennium Park, Dakshineswar, Belur Math) | **Low** — anchor ready; source WBTC pairs |
| **Helsinki — HSL / Suomenlinna** | Gulf of Finland archipelago | UNESCO island access + archipelago equity | ✅ **City node `helsinki-finland` + rich BP set** (Suomenlinna, Vallisaari, Pihlajasaari, Korkeasaari, Lonna, Kruunuvuorenranta) | **Low** — anchor ready; source HSL pairs |
| **Oslo — Ruter city ferries** | Oslofjord | all-electric Nesodden + island boats live | ⚠️ **No real anchor** — only junk POI "Oslo Road Boat Ramp" (mis-geocode) | **High** — mint Oslo city node + source BPs (Aker Brygge, Nesoddtangen, Hovedøya, etc.) |
| **Copenhagen — Movia harbour buses** | Copenhagen harbour | fully electric 991/992/993 since 2020 | ❌ **Nothing** | **High** — full new-geo mint |
| **Gothenburg — Västtrafik / Styrsöbolaget** | Göta älv + archipelago | ElectriCity electric Älvsnabben | ❌ **Nothing** | **High** — full new-geo mint |
| **Amsterdam — GVB IJ ferries** | River IJ | free public ferries, electrifying | ⚠️ **No real anchor** — only junk POI "Fort Amsterdam" (Caribbean mis-geocode) | **High** — mint Amsterdam city node + IJ BPs |
| **Rotterdam — RET / Waterbus** | Nieuwe Maas / Rhine-Meuse | Rotterdam–Dordrecht public waterbus | ❌ **Nothing** | **High** — full new-geo mint (incl. Dordrecht) |
| **Wellington — Metlink / East by West** | Wellington Harbour | NZ's first electric ferry *Ika Rere* | ⚠️ **No real anchor** — only junk POIs (Wellington Point AU, US yacht club) | **High** — mint Wellington NZ city node + BPs (Queens Wharf, Days Bay, Seatoun, Matiu/Somes) |

**Sequencing within Phase C (lowest-effort / highest-continuity first):**
1. **Kolkata (WBTC)** — anchor ready, India in-scope thread continues after Kochi + Mumbai. *(Confirm scope: Priority-B India is out unless reintroduced; Kolkata is explicitly in scope.)*
2. **Helsinki (HSL)** — anchor + rich BPs ready; strong electrification story.
3. **Oslo, Amsterdam, Wellington** — junk-POI cleanup + real city-node mint, then dossier.
4. **Copenhagen, Gothenburg, Rotterdam** — full new-geo mints (most sourcing).

**New-geo mint checklist (per authority needing an anchor):**
- [ ] Purge/quarantine junk mis-geocoded POIs for the city name (don't bind them).
- [ ] Mint `city` (or `priority_city`) feature with exact id/label + `[lng,lat]`, `_seed_node:true`.
- [ ] Register in the matching cluster in `CLUSTERS.json`.
- [ ] Source real boarding points `[lng,lat]` + labels into the dossier (published terminal locations).
- [ ] Then run the Batch-6 deliverable set (dossier → rewrite → Grok spec → seal handoff).

**Phase C checkbox ledger:**
- [ ] Kolkata WBTC (dossier+rewrite+spec)
- [ ] Helsinki HSL (dossier+rewrite+spec)
- [ ] Oslo Ruter (mint + deliverables)
- [ ] Amsterdam GVB (mint + deliverables)
- [ ] Wellington Metlink (mint + deliverables)
- [ ] Copenhagen Movia (mint + deliverables)
- [ ] Gothenburg Västtrafik (mint + deliverables)
- [ ] Rotterdam RET/Waterbus (mint + deliverables)

---

## 6. PHASE D — Batch 8+ bench (credible, lower electrification signal)

Hold until Jaideep greenlights; capture now so they're not lost:
- **Scotland — CalMac / Transport Scotland** (Hebrides lifeline; big but diesel-legacy).
- **Liverpool — Mersey Ferries (Merseytravel).**
- **Ho Chi Minh City — Saigon Waterbus.**
- **Manila — Pasig River Ferry.**
- **Rio de Janeiro — CCR Barcas.**
- **Toronto Island Ferry.**
- **Seoul — Hangang Bus** ⚠️ **COLLISION RISK:** repo already has `kakao-mobility` Seoul / Han River entries (`kakao_hand_waypoints_seoul.json`, Han River routes + economics). **Reconcile IDs before adding** — do not mint a colliding Seoul node. Resolve as an authority vs. commercial-operator distinction first.

---

## 7. Cross-phase sequencing & dependencies

```
Phase A (Batch-5 completion) ──► can run fully in parallel with Phase B authoring
   PR-1 (scrub, 24) ─ fastest, do first
   PR-2/3/4 (TRIM) ─ independent, any order
   PR-5 (narrative) ─ PR-1 helpful first (shared partners)

Phase B (Batch-6 rewrite) ──► each partner PR ──► Grok seal PR ──► Grok economics regen
   (geometry already sealed by Wave 9 → copy/econ rewrite only)

Phase C (Batch-7 new authorities)
   new-geo mint (where needed) ──► dossier ──► rewrite ──► Grok spec ──► Grok seal ──► regen
   Kolkata + Helsinki first (anchors ready)

Phase D (Batch-8) — GREENLIT (Jaideep 2026-07-02), runs as its own wave after Batch 7.
   CalMac · Mersey · Saigon Waterbus · Pasig · CCR Barcas · Toronto Island · Seoul/Hangang
   Seoul/Hangang: reconcile IDs vs existing kakao-mobility node (hygiene, not a blocker);
   authority + commercial paths run in parallel.
```

**Grok is idle / watching:** will regen economics after Batch-6 dossiers + seals land; will rebuild+deploy after Tasklet PRs merge to `main`. **Do NOT** re-run full `relink_hub_market_featured.py` on `norway-fjords`.

---

## 8. Definition of done (per PR)

- Both `data-clean/` + `partner-pitch/` trees edited and in sync.
- Convention hard-rules pass (rg scrub → 0 hits; no SOM/SAM/TAM/GMV/jargon).
- Fidelity audit PASS with trim=0 (for TRIM PRs); build exits 0.
- For new authorities: dossier + Grok spec present; pre-seal fidelity PASS (pending-seal nulls OK); handoff receipt in PR description.
- PR opened only when the theme is fully complete + self-verified; merge is Jaideep's call.

---

## 9. Resolved decisions (Jaideep, 2026-07-02) — LOCKED

1. **Batch-7 go-list & order** ✅ **Confirmed.** Proceed **Kolkata + Helsinki first** (anchors ready), then the mint-heavy five (Oslo, Amsterdam, Wellington → cleanup+mint; Copenhagen, Gothenburg, Rotterdam → full mint). **No authority dropped, none added.** Full Batch-7 set of 8 stands.
2. **Kolkata scope** ✅ **Confirmed in scope, proceed now** (not batched later). WBTC / Hooghly River authority runs in the anchor-ready first slice alongside Helsinki.
3. **PR granularity** ✅ **Approved to split Phase C per-authority** (and/or per anchor-ready vs mint-heavy). Batch-5/6 keep Grok's 7-PR stack; Batch-7 splits finer so each authority is its own reviewable copy surface.
4. **Seoul/Hangang** ✅ **Pursue the authority angle in parallel** with the `kakao-mobility` commercial-operator path. These are **independent parallel proposals** — we don't know which converts, so propose to both. ID reconciliation is a data-hygiene step (avoid node collision), **not** a reason to hold either path. Seoul stays in Phase D / Batch 8.
5. **Batch 8 bench** ✅ **Greenlit as Phase D — not on hold.** Scotland (CalMac), Liverpool (Mersey Ferries), HCMC (Saigon Waterbus), Manila (Pasig River Ferry), Rio (CCR Barcas), Toronto (Island Ferry), + Seoul/Hangang all remain in Batch 8 and are **active Phase D**, sequenced after Batch 7. No promotions into a nearer wave; Phase D executes as its own wave once Batch 7 clears.

---

## 10. Reference index

| Resource | Path |
|---|---|
| Grok intake checklist (PRs 1–7) | `handoff/partner-map-model/PTA-TASKLET-CHECKLIST-PR-PLAN.md` |
| PTA economics convention | `handoff/partner-map-model/PTA-ECONOMICS-CONVENTION.md` |
| Grok→Tasklet coverage handoff (P0–P4) | `handoff/partner-map-model/GROK-TASKLET-PARTNER-COVERAGE-HANDOFF.md` |
| Gold dossier schema | `handoff/partner-map-model/PTA-DOSSIER-bahrain-motc.json` |
| Gold Grok routing spec | `handoff/partner-map-model/GROK-SPEC-bahrain-motc-domestic-routing-2026-06-30.md` |
| Fidelity receipts | `handoff/partner-map-model/PROPOSAL-FIDELITY-<slug>.md` |
| PTA authority proposal skill | `/tasklet/workspace/home/pta-authority-proposal/SKILL.md` |
| Ships JSON / authoring mirror | `data-clean/partners/<slug>.json` / `partner-pitch/partners/<slug>.json` |
| Anchor/feature source | `data-clean/FEATURES_BY_TYPE.json`, `data-clean/CLUSTERS.json` |

*Living doc — update the checkboxes and status as each PR opens/merges. Do not delete completed items; strike or mark ✅ so the audit trail stays intact.*
