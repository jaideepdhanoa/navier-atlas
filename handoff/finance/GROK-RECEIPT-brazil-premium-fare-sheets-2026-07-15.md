# GROK-RECEIPT — Brazil $28 premium fare Sheet rebuild

**Date:** 2026-07-15  
**Upstream:** PR #279 merged (`d0b31901`); follow-up PR #280 merged (corridors-didi cascade + xlsx artifacts)

## Drive (in-place, IDs preserved)
| Partner | Sheet ID | URL |
|---------|----------|-----|
| DiDi | `1LY0Vp7FskgDDnEixkrEUCH0m-A_pYd2YCNuq3LF8ESM` | https://docs.google.com/spreadsheets/d/1LY0Vp7FskgDDnEixkrEUCH0m-A_pYd2YCNuq3LF8ESM/edit |
| inDrive | `1xo2a-XalddB6kRiLKzB7RIrV-u29LJmt3N2zc7ik3_k` | https://docs.google.com/spreadsheets/d/1xo2a-XalddB6kRiLKzB7RIrV-u29LJmt3N2zc7ik3_k/edit |

## Verified mid basis (both partners identical on Brazil)
| Corridor | fare | rev/boat/yr | payback |
|----------|------|-------------|---------|
| Arariboia 2.7nm | $28 | $329,190 | 2.40 yr |
| Charitas 4.4nm | $28 | $329,190 | 2.41 yr |
| Cocotá 6.0nm | $28 | $329,190 | 2.41 yr |
| Paquetá 9.2nm | $28 | $263,278 | 3.29 yr |

Country floor: **113 vessels**, **$36,407,526/yr**; pool **$367,461,220**.

Egypt (inDrive sheet only): Giftun **$32**, Ras Mohammed **$50** — unchanged.

## Notes
- First DiDi upload used stale `corridors-didi.json` (fare 18). Patched + re-uploaded; #280 lands the scoped file.
- `drive_upload.py` OAuth multi-account tokens incompatible with legacy loader; used MCP `uploadFile` in-place.
- Route-level parity mismatches: 0 for DiDi and inDrive. DiDi floor_delta ≈ Costa Rica ($1.57M) is pre-existing sim vs rollup inclusion, not Brazil.

## Next (Tasklet / Jaideep)
Rebuild DiDi Brazil deck on Voi-duplicate machine; bring proof before cascading Mexico / inDrive Brazil / inDrive Egypt.
