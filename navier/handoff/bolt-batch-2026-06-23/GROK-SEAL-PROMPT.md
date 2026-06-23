# Grok seal mandate — Bolt sub-proposal batch (2026-06-23)

## Why
Jaideep requested five Bolt sub-proposal changes. Tasklet authored the narrative + node-ids + scope;
Grok derives partner-view `scope_city_ids` (ID-match only), seals geometry, and runs the economics cascade.

## Changes (apply `inputs/bolt-subproposals-delta.json`; scope in `inputs/bolt-scope-map.json`)

### 1. `bolt-ksa-commercial` — RESCOPE (Jeddah + Eastern Province only)
- **Dropped giga-project anchors:** `neom-ksa`, `neom-sindalah-ksa`, `amaala-ksa`, `red-sea-global`.
- **New anchors:** `jeddah-ksa`, `dammam-khobar-ksa`, `manama-bahrain`.
- Re-derive Bolt KSA `scope_city_ids` to exactly these three. **Drop the four giga-project nodes from the
  Bolt KSA partner view.** Two clean sequential rollouts (Jeddah → Eastern Province); the Khobar–Manama
  ~18.6nm cross-Gulf leg is Pioneer II (in-range). NEOM/AMAALA/RSG appear only as *exclusion* prose — never
  bind them as Bolt KSA geometry.

### 2. `bolt-estonia` — NARRATIVE ONLY (Tallinn HQ triangle)
- Anchors unchanged (`tallinn-estonia`, `helsinki-finland`, `stockholm-sweden`). Label/summary/ask reframed
  as the Tallinn-HQ Nordic-Baltic triangle. No geometry change; reseal narrative fields only.

### 3. `bolt-thailand` — NET-NEW (Phuket / Phang Nga)
- Anchor `phuket-phang-nga-thailand` (existing Atlas node). Stand up the Bolt Thailand partner view; derive
  `scope_city_ids` from the anchor. Core Andaman cluster (Phang Nga 12nm, Yao Noi 12nm, Phi Phi 25nm,
  Krabi 30nm, Similan 50nm) = Pioneer II solid; Koh Samui 190nm + Langkawi 110nm = Quanta-LR amber-dashed.

### 4. `bolt-nigeria` — NET-NEW (Lagos Lagoon)
- Anchor `lagos-nigeria` (existing node; already POI-bound via yango-lagos). Stand up the Bolt Nigeria view.
  Core lagoon (CMS–VI 1.5nm, Ikoyi–CMS 2.5nm, CMS–Apapa 4nm, CMS–Ikorodu 13nm) = Pioneer II solid;
  Epe 30nm + Badagry 28nm = Quanta-LR amber-dashed.

### 5. `bolt-south-africa` — NET-NEW (Cape Town)
- Anchor `cape-town-south-africa` (existing node). Stand up the Bolt South Africa view. Table Bay / False Bay
  (Robben Island 7nm, Hout Bay 12nm, Simon's Town 22nm, Gordon's Bay 30nm) = Pioneer II solid; exposed-coast
  reach = Quanta-LR amber-dashed reserve.

### Dropped (do nothing)
- **Kenya (Mombasa / Lamu)** evaluated and intentionally **not** authored: no Atlas brief, Likoni crossing
  too short to foil, Lamu remote/thin. "Poor proposals are worse than none." No Kenya Bolt view.

## Acceptance gate (QA report must show)
- Bolt KSA `scope_city_ids` = exactly {jeddah-ksa, dammam-khobar-ksa, manama-bahrain}; the 4 giga-project
  nodes absent from the Bolt KSA partner view.
- New Bolt partner views (Thailand, Nigeria, South Africa) stand up from their single anchors; geometry
  renders real OR is flagged visibly aspirational (amber-dashed for all Quanta-LR legs).
- Every Pioneer II featured leg ≤ 70nm; every leg > 70nm is Quanta-LR amber-dashed (range gate intact).
- Economics cascade re-run against new gold; partner surfaces carry corrected economics (no stale provenance);
  `economics_url` + TAM-ladder rungs wired for the three new views.
- No Kenya artifacts created.
