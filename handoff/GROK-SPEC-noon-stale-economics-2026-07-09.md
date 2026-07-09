# GROK SPEC — noon.json stale UAE economics (cascade refresh)

**Date:** 2026-07-09 · **Lane:** Grok (finance cascade + publish) · **Flagged by:** Tasklet

## Symptom
`partner-pitch/partners/noon.json` still carries pre-inheritance economics:

| field | noon (live main) | careem (live main, same UAE market) |
|---|---|---|
| `growth_case.phase_economics.horizons[2].marine_mobility_tam_yr` | **$119M** | $1,155M |
| `growth_case._model_ssot.marine_tam_mid_usd` | **$119M** | — |

## Why this is wrong
- **Finance-corridor inheritance (permanent rule):** the finance spine is identical across all partners in a market. Verified on `finance/model/corridors.json` @ main: `uae-noon`, `uae-careem`, `bolt-uae`, `yango-uae`, `uae-luxury` all carry the **same 51-corridor spine**. Only `L3_locals`, `capture_rate`, `archetype`, `fleet_basis` may differ.
- Noon's $119M predates the UAE canonical corridor consolidation + reseal. The UAE market TAM cascaded from the current 51-corridor spine is an order of magnitude higher (earlier registry estimate ≈ $471M for strict `{uae}` scope; Careem's $1,155M additionally includes its outbound Q-LR overlay edges, which noon must NOT inherit — noon is strictly `{uae}`, no Q-LR).

## Ask (Grok lane)
1. Re-run the cascade for `uae-noon` scope from the current registry spine (51 corridors, noon `L3_locals`/`capture_rate`/`archetype` unchanged).
2. Publish refreshed `growth_case` numbers into `partner-pitch/partners/noon.json` (`phase_economics`, `_model_ssot`, TAM ladder rungs). **Do not** add Q-LR edges to noon.
3. Keep Gate G clean (plain-English descriptors; SOM label = "SOM full network (~XX% capture, today, +greenfield)").

## Post-cascade (Tasklet lane)
- Re-verify Noon deck (`1jzAKR3Bi91qW3iJBcr8vffx9693faT4l8gE5F6dhR5w`) economics slides against cascaded output; deck was hand-verified against the old model, so slide values will need a refresh pass after publish.

## Guardrails (permanent, restated)
- Never invent L3 demand numbers — cascade from registry only.
- Null beats confidently-wrong.
- No `regen_pta_economics.py --all` on batch-5; no WSF growth_case rewrites.
