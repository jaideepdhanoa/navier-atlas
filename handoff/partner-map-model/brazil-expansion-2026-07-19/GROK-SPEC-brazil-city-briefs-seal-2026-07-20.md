# Grok seal QA — Brazil expansion city briefs + cluster brief (2026-07-20)

## Why
The Brazil expansion geometry (nodes, boarding points, routes) was sealed in PR #296, but the
**side-panel city briefs never reached the front end** for the new markets — Jaideep reported he is
"not seeing city briefs for any of these new cities," and the Brazil cluster brief still described the
original 3-city (Rio / Costa Verde / Floripa) scope.

This PR closes that two-worlds gap by sealing the already-authored, gold-validated briefs from
`partner-pitch/city_briefs/` into `data-clean/city_briefs/` and rewriting the cluster brief to the
expanded 8-city network.

## What changed (all in `data-clean/`, staged and mergeable)
- **9 city briefs sealed** (straight copy from `partner-pitch/city_briefs/`, byte-identical seal path
  confirmed against Rio):
  - New T1 (full economics): `salvador-brazil`, `sao-sebastiao-ilhabela-brazil`, `santos-guaruja-brazil`,
    `vitoria-vila-velha-brazil`, `ilha-do-mel-brazil`
  - Display / brief markets (null econ): `paraty-brazil`, `buzios-cabo-frio-arraial-brazil`,
    `porto-alegre-guaiba-brazil`, `recife-brazil`
- **`_index.json`** — 9 new anchor entries added (sorted), `briefs` 266→275, `total_anchors` 269→278.
- **`cluster_briefs/brazil.json`** — rewritten to the 8-city seaboard network (Salvador bay, Costa
  Verde, São Sebastião–Ilhabela, Santos–Guarujá, Vitória, Floripa, Ilha do Mel). Every demand figure
  is carried from the sourced city briefs. Signature routes expanded 3→8, and the **stale headline
  route `ics-6536c49acf` (now absent from `ROUTES.json`) was replaced** with the live Costa Verde
  flagship `rn-7ec802385553` (Angra dos Reis ↔ Ilha Grande). All 8 signature `route_id`s verified live
  in `ROUTES.json`.

## Held out on purpose (do NOT seal)
- `belem-brazil`, `manaus-brazil` — Amazon lane is geometry-only, parked until explicitly opened.
- `sao-luis-alcantara-brazil` — economics on hold pending an annual pax series.

## Grok QA acceptance
- Side panel renders a brief for each of the 9 newly-sealed city nodes.
- Brazil cluster brief renders the 8-city network; all 8 signature-route deep-links resolve to live routes.
- No dead route_id anywhere in the Brazil cluster/city briefs (the `ics-6536c49acf` regression is gone).
- `partner_copy` lint clean (verified locally: 0 leaks across the 10 files).
