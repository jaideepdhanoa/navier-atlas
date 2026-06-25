# GROK HANDOFF — LINE MAN Wongnai Thailand mirror from live Grab Thailand

Date: 2026-06-25  
Owner split: Tasklet = source-of-truth deck edit + exact spec + QA. Grok = deterministic partner-page/economics build + repo PR + validation receipts.

## Status / source of truth

Tasklet edited the live duplicate deck directly via Google Slides API. Do **not** rebuild or overwrite this live deck from stale JSON/PDF/PPTX exports.

- Edited live deck: `https://docs.google.com/presentation/d/1wT1_t2HkYX0DTO1_5Ip6jywlI0I1_cs-iVQnn7IOO-Q/edit`
- Source deck that was duplicated by Jaideep: `https://docs.google.com/presentation/d/11WCun1Xk1flPmqvvtYrYZXsL5yRb5KQoe0xvTQSppKo/edit`
- Deck title: `LINE MAN Wongnai × Navier`
- Slide count verified: **14**
- Scope verified: **Thailand-only**
- Cover logo inserted from official source: `https://lmwn.com/wp-content/uploads/2025/06/logo-lmwn.png`
- Local logo asset/provenance: `/tasklet/agent/home/line-man-wongnai/deck-package/assets/logos/line-man-wongnai/logo-lmwn.png` and `LOGO-SOURCE.json`

The previous 24-slide/stale LINE MAN attempt is superseded for deck purposes. Use the live 14-slide edited duplicate as the deck receipt.

## Non-negotiable rules

1. Thailand-only. No Japan, Taiwan, Korea, Philippines, Malaysia, Indonesia, Maldives, etc.
2. Do **not** use `partner-pitch/partners/line.json` as the base; it is a broader LINE/LY Corporation file and is not the LINE MAN Wongnai Thailand mirror.
3. Use `partner-pitch/partners/grab-thailand.json` as the structural/economics source.
4. Create a new partner key/file: `line-man-wongnai`.
5. Keep route IDs, geometry, clusters, markets, phases, and economics from Grab Thailand unless a deterministic validation failure requires a null/hold.
6. Partner-facing copy must be plain English; no internal taxonomy leakage. Recognized labels SOM/SAM/TAM/GMV may remain only as labels with plain-English descriptors.
7. Null beats confidently-wrong. Do not invent LINE MAN-specific market data where Grab Thailand data is being mirrored.
8. Do not ask Tasklet/user to trust a self-report. Hand back PR link, branch, commit SHA, files changed, and validation receipts.

## Required build outputs

### A. Partner proposal JSON

Create `partner-pitch/partners/line-man-wongnai.json` by deterministic transform from `partner-pitch/partners/grab-thailand.json`.

Required transform:

- `partner_id`: `line-man-wongnai`
- `display`: `LINE MAN Wongnai`
- Partner category/archetype: same consumer/super-app framing as Grab Thailand.
- Geography: preserve Grab Thailand's Thailand-only network exactly.
- Markets/sub-pages: preserve the same Thailand markets, anchors, routes, phases, proof structure, and economics bindings.
- Economics/growth_case: mirror Grab Thailand magnitudes unless the finance engine recomputes identical values under the new partner key.
- Partner copy: adapt only partner-facing language from Grab to LINE MAN Wongnai.

Deck-aligned copy targets:

- Lockup: `LINE MAN Wongnai × Navier`
- Positioning: `Thailand’s local-life network, on the water`
- Thesis: `Thailand’s local-life platform already owns daily demand. Water is the only transport surface no one owns yet.`
- Deal summary: `We launch a LINE MAN Wongnai-branded foiling water tier across Thailand’s strongest water flows — the Gulf islands, the Andaman, the Chao Phraya, and the upper-Gulf ring — booked in-app, premium-priced and category-defining.`
- Partner context: `You are Thailand’s local-life platform — food, groceries, payments, maps and everyday mobility.`
- Cover/narrative line: `LINE MAN Wongnai already owns Thailand’s daily local demand. Water is the only surface no one owns yet.`
- Market headline line: `LINE MAN Wongnai brings daily Thai demand; Navier brings the foiling fleet proven in the Maldives.`
- Ways-of-working line: `LINE MAN Wongnai — local demand, the app, payments and the brand.`

### B. Data-clean sync

After creating the partner-pitch JSON, sync/produce the data-clean partner file using the repo's existing pipeline.

Expected output:

- `data-clean/partners/line-man-wongnai.json`

### C. Anchor-city crosswalk

Produce a grounded crosswalk for the new partner using the render join key from `data-clean/FEATURES_BY_TYPE.json`.

Expected output:

- `partner-pitch/LINE-MAN-WONGNAI-ANCHOR-CITY-CROSSWALK.json`

Expected result: all Thailand anchor city IDs inherited from Grab Thailand resolve. If any do not, hold/null them; do not rename by guess.

### D. Economics sheet + sidecar

Do **not** overwrite the Grab Thailand sheet.

Create/register a new transparent economics sheet for `line-man-wongnai` by mirroring/rebuilding Grab Thailand under the new partner key.

Expected repo updates:

- `finance/_refresh_line-man-wongnai.xlsx`
- `finance/PARTNER-SHEET-IDS.json` adds `line-man-wongnai` with the new Google Sheet ID
- `finance/economics_url_map.json` adds `line-man-wongnai` with the new sheet URL
- Any partner JSON `economics_url` fields point to the new LINE MAN Wongnai sheet, not the Grab Thailand sheet
- Economics sidecar generated for the LINE MAN package/export

Model requirements:

- Use the same Thailand corridor economics as Grab Thailand.
- Sheet/model/partner JSON must agree.
- Preserve existing CAPEX/opex country rules; Thailand country reference must be explicit, not inherited silently.

### E. Validation / QA receipts

Run the repo's existing validators/build receipts and include output in PR body.

Minimum validation:

- JSON parse for `line-man-wongnai.json`
- Anchor-city crosswalk against `FEATURES_BY_TYPE.json`
- Partner proposal strict narrative validation, if available
- Partner copy lint for `line-man-wongnai`
- Finance build/sheet generation receipt
- Data-clean sync receipt
- Render/Atlas local receipt if available

## PR requirements

Open one clean PR. Required handback:

1. Branch name
2. PR URL
3. Commit SHA
4. Exact files changed
5. Validation commands and results
6. Any held/null items explicitly listed

Suggested branch: `grok/line-man-wongnai-thailand-mirror-2026-06-25`

Suggested PR title: `Add LINE MAN Wongnai Thailand mirror from Grab Thailand`

## Do not do

- Do not rebuild the live edited deck.
- Do not use the stale 24-slide package as deck source.
- Do not use or extend `partner-pitch/partners/line.json` for this job.
- Do not introduce non-Thai slides, markets, or economics.
- Do not send external outreach.
- Do not mark complete without PR + validation receipts.

## Tasklet deck edit receipt

Tasklet live-edit summary on `1wT1_t2HkYX0DTO1_5Ip6jywlI0I1_cs-iVQnn7IOO-Q`:

- Replaced remaining Grab/Grab Thailand references with LINE MAN Wongnai copy.
- Replaced the cover partner logo with official LINE MAN Wongnai wordmark.
- Verified edited key slides show no remaining `Grab` text.
- Verified deck remains 14 slides and Thailand-only.

Grok should align source JSON/economics to this corrected state, not overwrite the deck.
