# GROK SPEC — Brazil expansion seal (2026-07-19)

## Mandate
Seal the Brazil priority-market expansion onto the Atlas front end: **12 new markets + Angra densification**, growing Brazil from 3 → 14 rendered cities. Inputs are in this folder (`boarding-points/`, `route-inventories/`, `demand-records/`) plus 9 new city briefs in `partner-pitch/city_briefs/`. GitHub `main` is source of truth; push the resealed gold to `main` with a QA report.

## Inputs
- `boarding-points/*.json` — 13 files, 162 BPs (149 verified coords, 13 null-coord entries that must go to the drop-ledger with reason `coords_unverified_survey_needed`, NOT silently dropped, NOT guessed).
- `route-inventories/*.json` — 185 candidate routes with haversine distances + stated coastal-wrap margins; `basis: grounded|aspirational`; `signature: true` flags (41). Distances are candidates — recompute against water-routed geometry.
- `demand-records/*.json` — provenance for tagging; economics are NOT part of this seal (cascade follows separately).

## Deterministic tasks
1. **Promote BPs → POIs** by ID-match; every on-disk BP either sealed or in the drop-ledger with a reason. **0 silent drops.**
2. **Mint city nodes** for the 12 new markets (country tag `brazil`, cluster inheritance per the corridor-inheritance rules; new cities join the existing Brazil cluster scope).
3. **Build route geometry** for all water-navigable candidate pairs; extend the water/land-crossing allowlist for: Baía de Todos os Santos, Canal de São Sebastião, Santos/Bertioga channels, Baía de Vitória, Baía de São Marcos, Baía de Paranaguá, Lago Guaíba + Delta do Jacuí, Recife Capibaribe basin, Baía do Guajará (Belém), Rio Negro/Amazonas (Manaus). 0 land crossings post-allowlist.
4. **Angra densification:** market currently renders 2 routes; target 12+ using `route-inventories/angra-dos-reis-ilha-grande-brazil.json` (21 BPs, existing `bp-` ID mappings noted in the BP file). Existing sealed corridor `Angra–Abraão` (economics-bearing) must be preserved byte-identical.
5. **Signature flags:** carry `signature: true` onto the rendered route features (min 1/city, no max — 41 total).
6. **Aspirational flagging:** routes with `basis: aspirational` and the display-lane markets (paraty, buzios-cabo-frio-arraial, recife, belem, manaus) must render visibly aspirational — never silently mixed with grounded corridors.
7. **Label repair:** rename stale "CCR Barcas - Mangaratiba" label (`bp-f032d26f15`) → "Barcas Rio – Mangaratiba".
8. **Cross-market links** (dedupe, one owner): Paraty↔Abraão + Paraty↔Angra (owner: paraty), Ilhabela↔Paraty 52 nm, Rio↔Búzios 78.9 nm (Quanta-LR), Santos↔Ilhabela. Route inventories reference each other's BP ids — reconcile by ID.
9. **Partner scope:** extend `didi-brazil` and `indrive-brazil` story `scope_city_ids` by ID-matching the new markets (shared corridor network, scoped views — per corridor-inheritance rules). Economics fields stay as-is until the cascade lands.

## Route-density acceptance targets (rendered, non-quarantined)
| City | Target |
|---|---|
| salvador-brazil | 15+ (27 candidates) |
| santos-guaruja-brazil | 15+ (21) |
| sao-sebastiao-ilhabela-brazil | 15+ (18) |
| vitoria-vila-velha-brazil | 8+ (13) |
| sao-luis-alcantara-brazil | 8+ (12) |
| porto-alegre-guaiba-brazil | 8+ (14) |
| buzios-cabo-frio-arraial-brazil | 8+ (12) |
| ilha-do-mel-brazil | 6+ (10) |
| paraty-brazil | 6+ (10) |
| recife-brazil | 6+ (9) |
| belem-brazil | 6+ (10) |
| manaus-brazil | 6+ (10) |
| angra-dos-reis-ilha-grande-brazil | **12+ (currently 2)** |

## QA report must show
- BP coverage reconciliation: sealed / dropped(+reason) counts per market; 0 silent drops.
- 0 land crossings post-allowlist; 0 orphan routes.
- Per-city rendered-route counts **before → after** vs the table above.
- Signature-route flags present per city (min 1).
- Aspirational markets/routes visibly flagged.
- Existing Brazil economics surfaces (Rio/Angra/Floripa corridors, didi-brazil/indrive-brazil partner JSON) unchanged.
- No shrinkage of any existing Brazil coverage (no-shrink baseline = current main).
