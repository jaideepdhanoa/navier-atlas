---
name: grok-seal-handoff
description: How Tasklet hands new geography (boarding points, cities, corridors, country tags) and corrected economics to Grok to seal onto the Atlas front end. Use when new BPs/markets/routes or economics change and the live map/partner pages must catch up.
---

# Grok seal handoff (front-end)

The single source of truth for "we made new geography / fixed economics — how does it reach the live
front end." This is a **separate world** from the economics cascade (see `partner-model-cascade`).

## ⚑ The two-worlds rule (the #1 thing people forget)
There are **two independent data worlds**. Updating one does NOT update the other:

| World | Owner | Holds | Surface |
|---|---|---|---|
| **Finance / economics** | Tasklet | countries, *economic* corridors, fares, unit economics | `finance/model/corridors.json` → Sheets + master tracker |
| **Atlas / render graph** | **Grok** | cities, clusters, *geometric* routes, boarding points, partner views | `atlas-external/boarding-points/*.json` → sealed `atlas-repo/data-clean/` |

Publishing economics (refreshing Sheets + tracker) leaves the **atlas front end stale**. Proof to look
for: `data-clean/partners/<p>.json` still showing old `census`/`*-aggregate` provenance, and new markets
absent from `ROUTES.json`. Fixing economics is necessary but **not sufficient** — you must also seal the
graph. After any cascade that adds/changes geography, ask "is the front end still stale?" and run this.

## Division of labor
- **Tasklet owns:** research, financial model, growth-story **narrative** content, corrected economics,
  and **assembling this handoff package**.
- **Grok owns (deterministic only):** ID-match / gazetteer promotion of BPs, BP↔BP route graph,
  water + land-crossing gates, cascade / dedupe / density-cap, reseal to the next gold tag, push to
  GitHub `main`, QA report. GitHub `main` is source of truth; the zip hand-back model is retired —
  this zip is an **input** package only.

## The handoff package (proven format: markdown prompt + input zip)
Build it in `/tmp` (shared FUSE FS is slow; stage there, copy the final zip to `/tasklet/...`). A complete
package — see the 2026-06-19 Bolt/Yango build at `navier/bolt-yango-seal-2026-06-19.zip` for a worked example:

| Path | What | Grok does with it |
|---|---|---|
| `docs/GROK-PROMPT.md` | The instruction (mandate, gates, acceptance) | Executes it |
| `boarding-points/*.json` | **ALL** BP files (full set, not a delta) | ID-match → seal POIs |
| `inputs/BP-COVERAGE-GAP-*.json` | The coverage audit (see below) | Reconcile to **0 silent drops** |
| `inputs/bp_water_allowlist.json` | LB-242 water/land-crossing allowlist | Fold into routing/mask gate |
| `inputs/seal-manifest.json` | Per-partner markets/countries/corridor counts from `corridors.json` | Inherit country tags + cross-partner overlap |
| `inputs/corridors.json` | Finance economic corridors (authoritative country tags) | Reference for tagging/overlap |
| `inputs/economics_url_map.json` | The `economics_url` render-contract field per partner | Bind to view + TAM-ladder rungs |
| `inputs/build_economics_sidecar.py` | Route-keyed econ sidecar builder | Run **against the NEW gold** |
| `partners/<p>.json` + `partners/<p>-scope.json` | Partner surface + market scope spec | Reseal economics; derive `scope_city_ids` |
| `README.md` | Contents map + the confirmed directives | Orientation |

Post the prompt + zip link to `#tasklet-jaideep`. Keep external outreach as drafts; this internal post is fine.

## Coverage audit — "include ALL boarding points" (0 silent drops)
Hours of research die quietly if BPs aren't sealed. **Always reconcile before handoff.** Recipe
(do it in `/tmp` for speed; full script pattern in `navier/atlas-external/BP-COVERAGE-GAP-2026-06-19.json`):

1. On-disk BPs: every `boarding-points/<city>.json`, count `boarding_points[]` per city.
2. Sealed markers: `data-clean/FEATURES_BY_TYPE.json` → `poi[]`, keyed by `properties.parent_city_id`.
3. Sealed routes: `data-clean/ROUTES.json`, endpoints are `{city_id}__{bp_id}` (5k+ features).
4. **City-id naming gotcha:** BP files use **bare slugs** (`abu-dhabi`); routes/POIs use **country-suffixed**
   slugs (`abu-dhabi-uae`). Match by prefix or you'll report false gaps.
5. Classify gaps:
   - **Zero-POI cities** — researched but completely unsealed (fold in fully).
   - **Ghost endpoints** — `routed=true` but **0 POI markers** (routes exist with nothing behind them).
   - **Partial cities** — fewer POIs than on disk (some are legit junk-POI / water-adjacency drops; some are lost research).
6. **Acceptance:** every on-disk BP is either **sealed as a POI** or in a **drop-ledger with a reason**
   (junk-POI repoint / failed water-adjacency / unresolved coords). Silent drops are not allowed; make
   "0 silent drops" a hard gate in the prompt.

## economics_url — clicking the TAM ladder → live economics (confirmed Jaideep 2026-06-19)
- **Field name: `economics_url`** (per partner). Source = published Sheet URL from `PARTNER-SHEET-IDS.json`
  (`https://docs.google.com/spreadsheets/d/<id>/edit`).
- **Bind targets:** the partner view **and** the growth story's **TAM-ladder rungs** — clicking a rung
  deep-links to the live economics Sheet. It also lights the Unit-economics chip/panel.
- It's a **seam/render-contract change → mutual PR**: Tasklet ships the field (in the partner JSON +
  `economics_url_map.json`); Grok wires the chip + rung links.
- The **route-keyed sidecar** `economics_by_route_id.json` (rung-level corridor cards) joins onto **gold
  route_ids**, so it is built **after** the seal, against the new gold — by `build_economics_sidecar.py`.
  Don't try to build it pre-seal; ship the builder + the source aggs and let it run against new gold.

## Partner views are derived, never hand-listed
A partner's map scope comes from its **story `scope_city_ids`**, which Grok derives by ID-matching the
markets in the scope spec — never a hand-typed city list. Two actions:
- **Existing partner (e.g. Bolt):** extend story scope to new markets + reseal partner JSON with corrected economics.
- **Net-new partner (e.g. Yango):** Tasklet authors the story narrative; add a `PARTNER_VIEWS['<p>']`
  entry + seal the partner JSON. The scope spec supplies markets/countries so Grok can stand up the view skeleton.

## Acceptance gate (Grok's QA report must show)
- BP coverage: **0 silent drops**; zero-POI and ghost-endpoint cities resolved.
- 0 land-crossings (post-allowlist); 0 orphan routes; every surviving BP carries a source id.
- New markets render real geometry OR are flagged visibly aspirational.
- Shared corridor network: correct country tags + cross-partner overlap.
- Partner surfaces carry corrected economics (no stale census provenance).
- `economics_url` wired; TAM-ladder rungs deep-link to the economics Sheet.
- Counts: BPs sealed / dropped (+reason), routes built / culled, before→after POI total, land-crossing=0 proof.
