# Tasklet residual ask — Grok-autonomous deck lane

_Updated: 2026-06-22 · After PR #66–#73 on `main`_

Grok now owns the deterministic deck build loop per `AUTONOMOUS-DECK-BUILD-CONTRACT.md`. Tasklet is **out of the hand-build path** except for the items below.

## What Grok is doing ourselves (no Tasklet dependency)

| Work | Inputs we already have |
|---|---|
| Build `deck.editplan.json` per deck | `golden-template-map.json`, `economics-binding.json`, `ASSET-REGISTRY.json`, `content-source.json`, partner pitch JSON |
| Emit per-deck `economics-binding.json` | Copy Grab binding pattern; object IDs from gold-deck copy pull; values from transparent sheet / `economics_by_route_id.json` |
| Wire `image-manifest.json` object IDs | `golden-template-map.json` + `ASSET-REGISTRY.used_by[].target_object_id` |
| Annotate golden map (role, char_budget, runs) | `deck_studio pull --mode full` + existing PR #68 style capture |
| Publish checked-in assets → stable `source_url` | Drive upload + registry update |
| Generate market backgrounds on miss | `n30-reference-neutral.png`, `builders/images/n30_composite.py`, sealed `atlas_city_id` from partner proposals |
| Build multi-run KPI / OPEX styled text ops | Style templates from golden map; values from sheet; leak denylist from binding |
| Fix schema / CLI drift | `deck-config`, `image-manifest`, `apply` validation against golden map |
| Reconcile stale docs | `AUTONOMOUS-DECK-BUILD-CONTRACT` §3, queue markdown, `BRANCH-MAP.md` |
| Fresh partner deck from gold copy | Drive copy of Grab gold deck; drift gate; new `deck_id` in `deck.config.json` |

## Still needed from Tasklet (narrow list)

### 1. Exact-bind evidence when ambiguous (not bulk deck work)

Provide **only when Grok flags `exact_bind_blocked`** on a specific deck/market:

- Sealed Atlas `city_id` ↔ live Slides `object_id` for a market background slot where registry has no exact match
- Confirmation when a partner's **display market** in the proposal does not map 1:1 to a sealed city ID (e.g. "Aegean archipelago" spanning multiple clusters)

Format: one JSON snippet per bind, not a full deck handoff.

### 2. Scope / entity guardrails (judgment, not generation)

Reply only when Grok opens a scoped question:

- **Bolt:** confirm Europe/Gulf beachhead ordering if proposal JSON and `deck.config.json` diverge
- **Territory decks:** confirm Navier-only cover (Caribbean, FP, Hong Kong) — already locked; no re-litigation unless partner entity changes
- **New partner entity decisions** before logo bind (e.g. if a government deck needs a specific ministry mark vs tourism board)

### 3. Transparent sheet layout drift check (one-time per sheet)

If Grok reports `economics_field_missing` when pulling Bolt (or any refresh deck):

- Confirm the 6-line OPEX row labels / cell addresses in the transparent sheet still match the field names Grok expects
- Or publish a one-row `sheet_field_map.json` sidecar: `{ "opex_energy": "B42", ... }` for that sheet ID

We do **not** need Tasklet to re-author economics — only to confirm sheet structure if it changed since the last recal.

### 4. Gold template change review (rare)

If someone edits the live Grab gold deck (`18yDAgO0Sj9PJlgf6paxtgni8Pk1xRAmNwE2TD_NCdSs`):

- Review the regenerated `golden-template-map.json` diff before Grok propagates to partner decks

## Explicitly NOT needed from Tasklet

- Full `deck.editplan.json` authoring
- Per-deck narrative copy (sourced from `partner-pitch/partners/*.json` + `content-source.json`)
- Logo sourcing for banked partners (`LOGO-MANIFEST.json` is canonical)
- Market image generation / N30 compositing
- Drive publish / `source_url` registration
- Live Slides apply (Grok + human thumbnail review)
- Rebuilding the 25-deck queue markdown (Grok reconciles from `LOGO-MANIFEST` + `CONSOLIDATED-DECK-GENERATION-QUEUE.json`)

## Response format (keep Tasklet replies small)

When Grok tags a Tasklet ask, prefer:

```json
{
  "deck_key": "bolt",
  "blocker": "exact_bind_blocked | sheet_field_missing | scope_question | gold_template_changed",
  "market_or_field": "...",
  "question": "one sentence",
  "grok_proposal": "null | hold | <proposed bind>"
}
```

Tasklet replies with `approved`, `corrected`, or `held_null` — no deck rebuilds.