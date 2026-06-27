# Grok seal spec — AirAsia MOVE Malaysia corridor mint + bind

**Partner:** `airasia-move` · **Archetype:** `super_app` (gold convention — do NOT normalize) · **Status in:** `research-complete / seal-needed`

This is the deterministic seal handoff for the **AirAsia MOVE** proposal. Tasklet has authored the full partner JSON (hub + 15 sub-pages) into both render trees. Thailand and Indonesia corridors are **inherited 1:1** from the sealed `grab-thailand` and `gojek` networks — **do not re-mint or re-touch them.** The only new geometry is **Malaysia**.

## Mandate (deterministic only)
Mint + bind the **13 Malaysia corridors** across the 4 core markets, then bind their `route_id`s back into `data-clean/partners/airasia-move.json` (and mirror to `partner-pitch/`). Run render QA. Hand back per the contract below.

## Mint scope — Malaysia (13 corridors, 4 markets)
All node endpoints use **verified atlas city_ids** (see scope spec). `route_id` is currently `null` with `_link_status: "unlinked-needs-mint"`.

| Market (city_id) | Corridors to mint | Notes |
|---|---|---|
| `sabah-kota-kinabalu-malaysia` | Jesselton Pt ↔ Gaya Island Resort (3nm); ↔ Manukan/Sapi (3nm); ↔ Mamutik/Sulug (4nm); Semporna ↔ Mabul/Kapalai/Sipadan (20nm) | All intra-Sabah, Pioneer II. Semporna is a separate node cluster on Sabah's east coast. |
| `langkawi-malaysia` | Kuah/Telaga ↔ Datai Bay/Kilim geoparks (12nm intra); ↔ **Koh Lipe/Tarutao (30nm, cross-border MY→TH)**; ↔ Penang (60nm); ↔ **Phuket (140nm, cross-border, Quanta-LR)** | Koh Lipe city_id not in Atlas — **mint the cross-border endpoint** or flag aspirational. Phuket endpoint = `phuket-phang-nga-thailand` (verified). |
| `penang-malaysia` | George Town ↔ Butterworth/Penang Sentral (2nm); ↔ Batu Ferringhi (8nm); ↔ Langkawi (60nm) | Channel + coastal, Pioneer II. Langkawi endpoint verified. |
| `desaru-coast-malaysia` | **Singapore (Tanah Merah) ↔ Desaru (28nm, cross-border)**; Desaru intra-coast (6nm) | Singapore endpoint = `singapore` (verified). Cross-border. |

**Cross-border legs flagged** (`_cross_border: true`): Langkawi↔Koh Lipe, Langkawi↔Phuket, Singapore↔Desaru. Apply the LB-242 water/land-crossing allowlist; these are open-water and must pass the water gate.

## Inherited — DO NOT re-mint
- **Thailand (5 markets, 57 corridors):** inherited 1:1 from `grab-thailand.json`; all `route_id` bound. Leave geometry untouched; only the partner view + copy differ.
- **Indonesia (5 markets, 39 corridors):** inherited 1:1 from `gojek.json`. 26 bound, **13 inherit Gojek's own `null`/unlinked state** (intra-city legs Gojek had not bound). These are **NOT** AirAsia mint scope — they bind when the shared corridor (same registry) binds in Gojek. Do not divergently mint them under AirAsia.
- **Tioman:** `singapore ↔ tioman-island` already bound (`ics-1a53f8237d`) — leave as-is.

## Range-gating note (inherited anomalies)
Five inherited **Indonesia** legs carry a long-range hull on a short leg (e.g. 45nm on Quanta-LR) — this reflects the **source Gojek network's** gating and is preserved 1:1 for cross-partner registry consistency. **Do not re-gate them only under AirAsia** (would desync the shared route_id from Gojek). If a re-gate is desired, fix at source (Gojek) and cascade to all partners. Malaysia-authored legs are correctly range-gated (≤70nm Pioneer II; 140nm Langkawi↔Phuket = Quanta-LR).

## Partner view
Net-new partner: add `PARTNER_VIEWS['airasia-move']`; derive `scope_city_ids` by ID-matching `airasia-move-scope.json` anchor city_ids (never hand-list). Held roll-ups (`raja-ampat`, `likupang`, `lake-toba`) are **not** in scope here — they belong to the Indonesia frontier seal (PR #130).

## Economics
`growth_case` is `model-pass-pending` by design — **no fabricated numbers.** TAM is anchored on **arriving-seat distribution-capture** (Jaideep 2026-06-27); demand anchors are in `AIRASIA-DEMAND-ANCHORS.json`; the capture band is handed to the **model pass**, not this seal. After the model pass + sheet build, `economics_url` and the route-keyed sidecar bind against new gold. Do not invent economics during the seal.

## Acceptance gate (handback must show)
- 13 Malaysia corridors minted + bound; `route_id`s written into BOTH `data-clean/partners/airasia-move.json` and `partner-pitch/partners/airasia-move.json`.
- 0 land-crossings post-allowlist on the 3 cross-border legs; 0 orphan routes.
- All 15 markets render real geometry OR are visibly flagged aspirational (Koh Lipe endpoint if unminted).
- Thailand + Indonesia geometry untouched (diff shows only Malaysia route_ids + partner view).
- **Handback contract:** branch name · PR link · commit SHA · exact files changed · validation/render receipt · explicit nulls/held items (Indonesia 13 inherited-null, frontier roll-ups, Koh Lipe). No self-certified completion, no line-range audits.
