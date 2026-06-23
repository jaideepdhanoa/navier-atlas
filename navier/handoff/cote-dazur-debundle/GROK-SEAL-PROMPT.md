# Grok seal mandate — Côte d'Azur de-bundle (2026-06-23)

## Mandate
Côte d'Azur was modeled as a single cluster "city." Per Jaideep, de-bundle it into operationally
distinct **city nodes**, fold **Monaco** into the cluster family, and re-key the existing sealed
geometry onto the new nodes. This is a **deterministic re-key + reseal** — no net-new invented geometry.

Authoritative node definitions: `briefs/*.md`. Deterministic mapping: `node-map.json`.

## What to do (deterministic only)
1. **Mint four nodes** (region `europe-med`, parent cluster `cote-dazur-france`):
   `nice-france`, `cannes-france`, `antibes-france`, `saint-tropez-france`.
2. **Keep `monaco-monaco`** as its own node but **tag it a member of the `cote-dazur-france` cluster
   family** for network + partner-scope purposes.
3. **Re-key existing POIs/BPs**: every point currently sealed under `parent_city_id = cote-dazur-france`
   → reassign to exactly one node per `node-map.json → poi_rekey_rule.label_to_node`. Points not in a
   minted node (Menton, Villefranche, Sanremo IT, Portofino IT) **stay under the `cote-dazur-france`
   cluster catch-all**.
4. **Rebuild the route graph**: re-point the Riviera route endpoints (`{city_id}__{bp_id}`) to the
   re-keyed node ids. Water-allowlist unchanged.
5. **Reseal** to the next gold tag; update `data-clean/` POIs + `ROUTES.json` + `FEATURES_BY_TYPE.json`.
6. **Bolt partner view**: derive `scope_city_ids` by ID-matching the updated `anchor_cities`
   (`node-map.json → partner_view`), and reseal the Bolt partner JSON from
   `bolt-france-riviera.subproposal.json` so the cluster + five nodes render in the Bolt view.

## Acceptance gates (your QA report must show)
- **0 silent drops**: every previously-sealed Côte d'Azur POI is re-keyed to exactly one node OR the
  cluster catch-all OR is in a drop-ledger with a reason. Report before→after POI counts per node.
- **No invented geometry**: nodes are populated only from re-keyed existing points. Any node with 0
  existing POIs is flagged **visibly aspirational**, not faked.
- **Routes**: 0 orphan routes, 0 land-crossings (post-allowlist), every surviving BP carries a source id.
- **Cluster integrity**: `monaco-monaco` renders as its own node AND is tagged in the `cote-dazur-france`
  cluster family. The four new nodes each carry `parent_cluster = cote-dazur-france`.
- **Bolt view**: `scope_city_ids` includes `cote-dazur-france`, `nice-france`, `monaco-monaco`,
  `antibes-france`, `cannes-france`, `saint-tropez-france`; partner JSON carries no stale census provenance.
- **Counts**: nodes minted = 4; POIs re-keyed / dropped (+reason); routes re-pointed / culled.

## Economics (separate world — flag, don't block)
Adding St-Tropez and splitting nodes changes scope. The economic cascade (corridors.json → aggregate →
growth → sheet → master tracker → partner JSON phases) is **Grok-owned deterministic model work** and
should re-run for `bolt-france-riviera` after the seal, so floor/TAM reflect the de-bundled scope.
Tasklet has updated the sub-proposal **narrative + phases + node-ids** only (see subproposal JSON);
boat counts / capture (0.18) are unchanged pending the cascade.
