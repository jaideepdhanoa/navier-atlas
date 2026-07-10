# Grok — Wave1 P0 + DiDi HK seal

**UTC:** 2026-07-10T22:03:56Z  
**Status:** `p0_complete / wave1_new_mints_held_null_coords / finance_untouched`  
**Upstream:** PR #219 + #220

## P0 repairs
| Fix | Result |
|-----|--------|
| Lake Geneva 14 IDs | indonesia → **switzerland** (IDs preserved) |
| UK decompose | London 33 · Mersey 3 · Clyde 10 · Hebrides 18 |
| Dott UK inherit | **Clyde only** (no London/Liverpool) |
| Voi UK inherit | **London + Clyde** (no Liverpool) |
| Ibiza | reuse **10** existing routes; no mint |
| HK/Macau split | HK 37 · Macau 16; DiDi **HK only** |

## Partner counts (visible ∩ sealed clusters)
| Partner | Routes |
|---------|--------|
| DiDi | **804** (was 767 pre-split + 37 HK) |
| Dott | **1,164** |
| Voi | **401** |

## Wave1 new geography (Belgium, Solent, Le Havre, Poland, AT/HU, …)
**HELD** — all research ledger BP `coordinates: null`. Null beats inventing coords. Ledgers remain for Tasklet coordinate seal.

## Gates
Inheritance strict didi/dott/voi **PASS** · Linkage **0 gaps** · Gate G **PASS** · Fidelity all **PASS** · Economics **untouched**

Machine: `GROK-WAVE1-P0-DIDI-HK-SEAL-RECEIPT-2026-07-10.json`
