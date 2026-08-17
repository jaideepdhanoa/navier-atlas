# NODES & NETWORK DESIGN — Saudi Eastern Province
Internal audit file. Research date: 2026-08-16. Distances DERIVED (haversine from listed coordinates; coastal routing noted). Times at 25 kn + 3 min dwell per intermediate stop. GREENFIELD: every stop is an existing physical landing; nothing "planned" renders without a status flag.

## Locale-cleanup dependency (READ FIRST)
All EP boarding points in the sealed corridor spine are **mis-tagged `market_key: bahrain_domestic`** (see `_ref-spine-corridors-ep.json`). Every binding below is therefore conditional on **Grok locale cleanup #119** re-tagging these nodes/corridors to an `eastern-province-ksa` market key. Cite labels, bind IDs, but do NOT treat market_key as truth. The `domestic_uae_intra_city` entries in the ref file ("Jubail Mangrove", "Marsa Al Jubail", Saadiyat, Yas) are Abu Dhabi UAE false positives (Jubail-UAE ≠ Jubail-KSA) — ignored.

## Node inventory (7 active + 1 roadmap = 8; rule: 6–12 verified landings)
| # | Node | Coordinates | Evidence | Status | Spine node_id |
|---|---|---|---|---|---|
| N1 | **Dammam Corniche Boats Dock** (Ash Shati, King Abdullah Rd corniche) | 26.4717, 50.1333 | Public map listing (Waze place "Dammam Corniche - Boats Dock", plus code F4CM+M8W decoded) [DERIVED coords, PRIMARY listing] | VERIFIED existing dock | bp-9da9a24a2a |
| N2 | **King Abdulaziz Port — Cruise Saudi Terminal** | 26.4886, 50.2011 (port datum) | cruisesaudi.com KAAP port page [PRIMARY]; port coords Wikipedia [SECONDARY] | VERIFIED operating cruise berth (access = Mawani/Cruise Saudi agreement) | bp-54c27c6c13 (label "Cruise saudi Terminal") |
| N3 | **Al Khobar Corniche Marina** (Khobar Waterfront) | ~26.301, 50.221 | Amanah Khobar Waterfront has marinas on site (saudipedia [SECONDARY]); spine node exists with clean namespaced id | VERIFIED marina; exact berth TBC on binding | eastern-province-ksa__al-khobar-corniche |
| N4 | **Half Moon Bay — Half Moon Yacht Association** | ~26.167, 50.033 (bay datum, latitude.to [SECONDARY]) | Spine node + operator/community evidence of yacht club at HMB | VERIFIED landing; precise pontoon TBC | bp-1a964d0e41 |
| N5 | **Dana Bay Marina** (southern Half Moon Bay) | ~26.093, 50.029 [DERIVED approx] | danabay.sa/en — master development on HMB with operating marina & watersports [PRIMARY operator] | VERIFIED marina | bp-dd021ae2b2 |
| N6 | **Darin Port, Tarout Island** (Qatif heritage port) | ~26.545, 50.078 [DERIVED approx; island 26.571, 50.056 Wikipedia] | SPA/SDA Dareen & Tarout program: historic working port, SAR 2.64B redevelopment [PRIMARY] | VERIFIED existing harbor; **redevelopment status flag** | none — unbound |
| N7 | **Cornish Marina, Dammam** (southern Dammam corniche) | not independently located | Exists in spine (bp-ed8e1aa423, 1.9 nm from N1 via rn-8cc0ea41cfdc) | **CANDIDATE — held out of lines until location verified** (fail closed) | bp-ed8e1aa423 |
| N8 | **Uqair Heritage Port** (Al-Ahsa coast) | 25.6442, 50.2150 | en.wikipedia.org/wiki/Uqair [SECONDARY]; historic port, development program announced | **ROADMAP-ONLY** (no verified passenger landing today; render only with status flag) | none |
Excluded: King AbdulAziz Port commercial berths (bp-68da15731c) and Saudi Global Ports (bp-1a5d182430) — container/cargo berths, not passenger landings; "Marine club" HMB node (bp-0a5fd1490e) — unverifiable operator label [fail closed].

## Line design (trunk/feeder discipline; MECE; 3 lines + 1 roadmap)
Cluster check: Dammam cluster {N1,N2,N6} → ceil(3/2)=2 lines max → EP-1, EP-3 ✓. Khobar/HMB cluster {N3,N4,N5} → 2 lines max → EP-1, EP-2 ✓. **Single interchange hub: N3 Al Khobar Corniche Marina** (EP-1 × EP-2 × EP-X). N1 is a shared terminus where EP-3 feeds EP-1 (timed connection, not a second hub).

### EP-1 · Corniche Spine (THE trunk) — Dammam Corniche ↔ Cruise Terminal ↔ Khobar Corniche
- N1 → N2: **3.8 nm**, 9 min · N2 → N3: **11.3 nm**, 27 min (offshore of KAAP fairway; +3 min crossing pad per SPEED-RULES)
- End-to-end: 15.1 nm ≈ **9 + 3 (dwell) + 27 + 3 (pad) ≈ 42 min**; direct N1→N3 skip-stop ≈ 11.3 nm greatcircle but must round the KAAP fairway → assume ~13–15 nm, **~35 min** [DERIVED routing]
- vs road: 21.9 km, 15 min off-peak (rome2rio [SECONDARY]) — **the water route is LONGER than the road off-peak**. Honest positioning: EP-1 wins only at peak congestion, for the cruise-terminal connection, and as the premium corniche-to-corniche experience. It is the network spine because it links the two anchor waterfronts and the cruise gateway, not because it beats an empty highway.
- Purpose: "the two corniches and the cruise gateway on one line."

### EP-2 · Half Moon Bay Leisure Line — Khobar Corniche ↔ Half Moon Bay ↔ Dana Bay
- N3 → N4: **~12.9 nm** greatcircle, assume ~14 nm coastal [DERIVED], **~34 min** · N4 → N5: **5.6 nm** (spine figure, rn-bee07be06790), **13 min**
- End-to-end ≈ 34 + 3 + 13 ≈ **50 min** vs 40–50 km road (30–40+ min [SECONDARY])
- Purpose: "the weekend line — Khobar waterfront to the resort bay." Water is time-competitive here AND replaces the most congested weekend drive. Tourism-weighted per addendum.

### EP-3 · Tarout Heritage Feeder — Dammam Corniche ↔ Darin Port (Tarout)
- N1 → N6: **~5.3 nm**, **~13 min** + shallow-bay speed regime (Tarout Bay shallows; displacement-mode segments likely — see SPEED-RULES) → plan **~20 min** [DERIVED]
- Purpose: "the heritage line — 5,000 years of Tarout Bay by water." Feeds EP-1 at N1 (timed). Aligns 1:1 with the SAR 2.64B SDA Dareen program [PRIMARY].

### EP-X · Khobar ↔ Bahrain (ROADMAP-ONLY — no economics, no schedule)
- N3 ↔ Bahrain Financial Harbour Marina: **18.6 nm** (spine corridor, clean id) — ~45 min at 25 kn EXCLUDING causeway-passage routing and border formalities [DERIVED]
- Constraints: causeway passage per Bahrain Marine Notice 3/2020 [PRIMARY register]; Saudi-side restricted zones UNSOURCED; cross-border immigration infrastructure does not exist at either marina today.
- Render: roadmap-amber-dashed, text-only economics. **Bahrain's PTA page mirrors this line from the Manama side** — keep corridor identity shared (corridor-inheritance skill), one corridor, two pages.
- Roadmap extension (not a line): Half Moon Bay/Dana Bay ↔ Uqair heritage port, 28.8–32.9 nm — pairs with Uqair development program; N45 range-comfortable; render only with Uqair status flag.

## Corridor bindings (spine ↔ lines)
| Line leg | Spine corridor_id | Binding |
|---|---|---|
| EP-1 N1↔N2 | — (spine has KAAP↔Cruise rn-1874ce7ec9ce = intra-port 0.8 nm, different geometry) | **UNBOUND — new corridor needed** |
| EP-1 N2↔N3 / N1↔N3 | — | **UNBOUND — new corridor needed** |
| EP-2 N3↔N4 | — | **UNBOUND — new corridor needed** |
| EP-2 N4↔N5 | rn-bee07be06790 (Dana Bay Marina ↔ Half Moon Yacht Association, 5.6 nm) | **BOUND** (conditional on #119 re-tag) |
| EP-3 N1↔N6 | — | **UNBOUND — new corridor needed** |
| EP-X N3↔BFH | e__eastern-province-ksa__al-khobar-corniche__manama-bahrain__bahrain-financial-harbour-marina (18.6 nm, market bahrain_ksa_eastern_province) | **BOUND** (id already clean) |
| (held) N1↔N7 | rn-8cc0ea41cfdc (Cornish Marina ↔ Boats Dock, 1.9 nm) | HELD with N7 |
| (roadmap refs) | rn-38c057452ce6 (Manama↔KAAP 27.3 nm) · rn-aec00e3ad974 (Manama↔HMYA 36.9 nm) | NOT USED — cross-border variants, roadmap notes only |
Never-invent rule respected: no new IDs fabricated; unbound legs go to Grok seal (grok-seal-handoff) as new-geometry requests, with the #119 locale-cleanup note that EP spine nodes/corridors are mis-tagged bahrain_domestic.

## Mis-geocode findings for the research record (feed #119, do NOT touch Atlas here)
1. All 8 `bahrain_domestic` corridors among Dammam/Khobar/HMB labels are EP-KSA locale.
2. `rn-38c057452ce6` / `rn-aec00e3ad974` are cross-border (Manama↔EP) but tagged `intra_city`.
3. `domestic_uae_intra_city` "Jubail" corridors conflate Jubail (KSA) with Al Jubail Island (Abu Dhabi) — they are Abu Dhabi geometry, already flagged in the international addendum.
