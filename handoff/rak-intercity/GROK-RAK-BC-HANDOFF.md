# Grok handoff — RAK Workstreams B + C (RAKTA alignment + gateway network)

Builds on the PR #402 geometry repair (merge that first). Everything below is deterministic render + one mint.

## 1 · What changed (data, already in this PR)
- `employer-hub/hubs/ras-al-khaimah/hub.json`
  - **3 new Phase-2 stops:** `rams`, `al-ghalilah`, `shaam` — approximate town-waterfront pins snapped to water; every `tag` carries the berth-TBC flag (Al Ghalilah = "modular pontoon — site TBC with authority"). Render tags verbatim.
  - **New line `NTH-1` "Northern Arc"** (phase 2): qawasim-1 → rams → al-ghalilah → shaam. Hand waterways, land-QA clean, detour gate ≤1.35 passed (no exceptions needed).
  - **`network.phase_labels`** now mirror the authority's strategy: Phase 1 (2025) / Phase 2 (2026) / Phase 3 (2027).
  - **`corridor_table`** — NEW, the single source of truth for every corridor figure on any RAK surface. Rows with `render_on_map: false` (HER-1, GTW-*, GLF-*) must NOT draw on the hub map. Camera stays emirate-framed; Phase 4/5 render as copy sections only.
- `employer-hub/hubs/ras-al-khaimah/public-partners.json`
  - New section **`strategy_alignment`** (after `gap`): headline + body + 3 cards. Contract v3 fields only.
  - New section **`intercity`** (before `flywheel`): headline + body + 2 cards (Phase 4 UAE Gateway Line, Phase 5 Gulf Gateway). Footnotes fn9 (RAKTA strategy citation) and fn10 (distance basis / roadmap qualifier) render in the single Notes section as usual.
  - `section_order` + `nav_anchors` updated — wire both.
- `employer-hub/hubs/ras-al-khaimah/fleet-investors.json` — internal corridor provenance now derives from `corridor_table`; rendered copy unchanged except previously-synced spine times. No new sections.

## 2 · The one mint (global network — corridor-inheritance contract)
**KSA Eastern Province ↔ Ras Al Khaimah** is absent from the shared spine. Author it ONCE, globally:
- Mirror the `edge-0774` record shape in `handoff/partner-map-model/uae-gulf-shared-corridor-spine.json`; `market_key: rak_cross_border_roadmap`; open-Gulf geometry; `vessel_gate: "Quanta-LR review >150nm"`; amber-dashed roadmap tier.
- Acceptance: 0 land crossings, route_nm recorded (≈310 nm research estimate — re-measure), sealed into `ROUTES.json` at the next gold tag.
- Then update `corridor_table` row `GLF-4`: set `route_id`, `status: "roadmap"`, correct `path_nm`.
- While there: `GLF-1` Khasab ref `rn-4231b9e22408` is `quarantined_or_hidden` — re-verify or replace at seal.

## 3 · QA gates (fail the build)
1. `python3 scripts/validate_hub_page_consistency.py employer-hub/hubs/ras-al-khaimah` — corridor drift gate (already passing).
2. Detour sweep: all NTH-1 segments carry `routing.detour` receipts; max ratio 1.238.
3. Map plates **text-free**; northern stops show pins + station callouts only.
4. Screenshots at 1280 / 1440 / 2560: hub map (phase 2 visible), strategy_alignment, intercity, footnotes.
5. Leak scan on both rendered pages: no long-range program names (N-series + "long-range hybrid class" only), no launch dates in Phase 4/5, no counterparty names beyond published Wynn figures, no fundraising terms.
6. Phase labels render exactly as in `network.phase_labels` — no invented dates elsewhere.
