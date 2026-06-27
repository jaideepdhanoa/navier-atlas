# Grok handback — queue drain phase 2 (2026-06-27)

**Branch:** `main` (pending push)  
**Baseline:** post `44060e8a` queue drain  
**Production:** https://navier-atlas.vercel.app

---

## Phase summary

| Phase | Issue | Verdict | Notes |
|-------|-------|---------|-------|
| 1 | #127 Gojek | ✅ CLOSED | Prior commit `44060e8a` |
| 2 | #121 Maldives | ✅ CLOSED | Prior commit `44060e8a` |
| 3 | #104 Bolt Bug C | ✅ CLOSED | Prior commit `44060e8a` |
| 4 | #119 bp_on_water | 🔴 OPEN | Gate re-run with allowlist: **FAIL 1297 true mis-geocodes** (1172 pass / 215 allowlisted); scope narrowed to `bp-*` route endpoints |
| 5 | #118 Grab deck KPI | 🟡 PARTIAL | `slide3-kpis-grab-thailand.json` + `deck-economics-values-grab-thailand.json` refreshed from model; BKK marquee reconciled via footnote (river unit econ vs Quanta-LR cross-Gulf); **Slides API apply blocked** — stale object IDs (`g3eec5122801_0_15` not found) |
| 6 | #112 Deck builder | 🟡 PARTIAL | `gen_deck_economics.py` hospitality branch — Centara 7/7 appendix cards generated |
| 7 | Bite 2 hawaii | 🟡 PARTIAL | `growth_frontend_block.py` + `splice_growth_into_partner.py` forward-SAM-only path; hawaii `growth_case` spliced (roadmap held) |
| 8 | Bite 2 cote-dazur / d-marin / discovery-land | 🔴 OPEN | Still 0 `route_id`s bound |

---

## #119 SEAL gate

- **Script:** `scripts/grok-reconcile-79am/run_bp_water_gate_main.py`
- **Allowlist:** `data-clean/bp_water_allowlist.json` (promoted from `_ingest`)
- **Verdict in SEAL:** `FAIL 1297 true mis-geocodes (1172 pass / 215 allowlisted)`
- **Report:** `grok-routing-output/bp-water-adjacency-report.json`
- **Tasklet:** formal gold sign-off after true-misgeocode triage (coord snap vs allowlist expansion)

---

## #118 Grab Thailand deck

- **KPI source refresh:** `deck-studio/decks/grab-thailand/slide3-kpis-grab-thailand.json`
- **Values sidecar:** `deck-studio/decks/grab-thailand/deck-economics-values-grab-thailand.json`
- **BKK reconciliation:** Slide 9 footnote documents intentional split — river Pioneer unit econ on slide; Atlas network marquee = Bangkok ↔ Hua Hin 88 nm Quanta-LR (roadmap)
- **Blocked:** `deck_grab_thailand.py apply` — live deck OIDs drifted from `golden-template-map.json`; Tasklet should re-pull manifest or patch slide-3 / slide-10 / slide-9 footnote OIDs

---

## #112 Unified deck builder (Grok half)

- **Changed:** `deck-studio/decks/gen_deck_economics.py` — `deck_type: hospitality` reads sealed sidecar, emits `appendix_cards` (no ladder)
- **Receipt:** `gen_deck_economics.py centara-thailand` → **7/7 appendix cards filled**
- **Held:** page-fill background applier branch, Minor binding re-pull, QA gate in `deck_studio` CLI

---

## Bite 2 tail

- **hawaii:** `growth_case` bound with `_forward_sam_only: true`, 5 Quanta-LR corridors in roadmap bucket
- **cote-dazur / d-marin / discovery-land:** route_id binding still required before cascade

---

## Tasklet-unblocked

- Gojek Indonesia deck + copy cascade (#127)
- Formal SEAL sign-off after #119 triage
- Grab live Slides KPI apply after OID refresh
- Centara / Minor deck builds using hospitality gen branch