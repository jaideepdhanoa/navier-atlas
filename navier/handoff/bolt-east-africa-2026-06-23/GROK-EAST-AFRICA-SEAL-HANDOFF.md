# Grok note — stand up the Bolt East Africa coastal cluster (net-new geography)

**From:** Tasklet · **Date:** 2026-06-23 · **Type:** input package (GitHub `main` stays source of truth)
**Cluster:** `bolt-east-africa` (Kenya coast + Tanzania mainland + Zanzibar/Pemba/Mafia archipelago)

This is **net-new geography** — there is no existing East-Africa geometry in Atlas (Kenya was a dropped
standalone in PR #83). Both worlds must catch up: the **render graph** (your lane) and then the
**economics** (Tasklet's cascade lane, after your seal).

## Inputs in this package
- `research/bolt-east-africa-coverage-research.json` — source-led footprint, evidence tiers, market anchors.
- `inputs/candidate-boarding-points.json` — **21 candidate BPs** with gazetteer hints; coords are null by
  design (your deterministic geocode + ID-match promotes them).
- `inputs/candidate-signature-corridors.json` — **11 candidate corridors** with range-gate + demand/fare anchors.
- `inputs/country-reference-additions-east-africa.json` — Kenya + Tanzania opex/grid/crew/marina/CAPEX rows.
- `BOLT-EAST-AFRICA-SUBPROPOSAL-NARRATIVE.md` — narrative (draft).

## What to do (deterministic only)
1. **Geocode + seal BPs:** resolve each candidate BP via gazetteer/OSM by its `gazetteer_hint`, ID-match,
   apply the **water-adjacency gate**, and seal as POIs. **0 silent drops** — every candidate ends as a
   sealed POI *or* a drop-ledger entry with a reason (failed geocode / failed water-adjacency / not a real
   maritime point). Low-confidence brief-only nodes (Bagamoyo, Tanga, Malindi, Watamu) may stay
   backlog/brief, but must be logged.
2. **Build corridor geometry:** BP↔BP routes only between sealed, water-adjacency-passing BPs; **no
   land-crossings**; every surviving BP carries a source id.
3. **Re-gate borderline legs on exact great-circle:** Dar↔Mafia and Stone Town↔Mafia (~68–70 nm) — if
   >70 nm, move to Quanta-LR. Keep Malindi↔Lamu on **Quanta-LR (amber roadmap)**. Seal the cross-border
   **Mombasa↔Pemba (KE↔TZ)** leg as a **FIRST-CLASS marquee cross-border corridor** — real geometry + render,
   same footing as **Dubai↔Doha** / **Phu Quoc↔Sihanoukville** — NOT visibly aspirational. It is in-range on
   Pioneer II (~54nm); the **KE↔TZ ICQ handshake** is the human-side gate (note it, don't down-rank the corridor).
   Author the cross-border row in BOTH city files (mombasa, pemba) with explicit Pioneer-status / Quanta-LR-status /
   human-side ICQ-gate columns per the cross-border wedge catalogue authoring discipline.
4. **Country tags:** tag Kenya + Tanzania corridors with authoritative country tags; preserve cross-partner
   overlap (this cluster is reusable for Uber/Yango).
5. **Stand up the partner view:** add a `bolt-east-africa` scope to Bolt's story `scope_city_ids` (derive by
   ID-matching the sealed markets — never hand-list), so the cluster renders on Bolt's partner page/map.
6. **Hand back** a QA report: BPs sealed/dropped (+reasons), routes built/culled, land-crossing=0 proof,
   borderline re-gate decisions, and which corridors render real vs. flagged-aspirational.

## After your seal (Tasklet's cascade lane)
Once geometry is sealed, Tasklet runs the model cascade (country-reference confirm → aggregate → growth →
frontend → splice → transparent sheet → master tracker) and builds the **economics sidecar** against the
new gold, then wires `economics_url`. **Do not** generate economics from the candidate fare anchors — those
are assumptions for Tasklet's cascade, not sealed numbers.

## Guardrails
- ID-based matching only; **null beats confidently-wrong**; broad-footprint-first, exact-bind-second.
- Do not invent coordinates, corridors, or boarding points beyond this candidate set.
- No new geography promoted from country evidence alone — only the named, sourced maritime points here.
- This cluster is **reusable** — seal it as shared network with correct country tags, not Bolt-private copies.
