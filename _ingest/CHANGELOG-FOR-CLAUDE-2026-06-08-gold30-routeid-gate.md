# Gold #30 — route_id null-on-fail gate (closes P0 #1c)

**Routes unchanged: 5,201.** Partner-pitch only. Builds on #27 (relink) + #29 (dedup).

## What Claude flagged (log 09d27de)
> "~540 featured + ~330 journey items still carry a failing route_id … null the value when it fails."

## Reconciliation — P0 IS resolved as of Gold #27, not still-open
- `gated_relink.py` (Gold #27) **already nulls route_id on non-match** — it does not keep stale ids. That collapsed the pre-#27 ~540 featured / ~330 journey route_ids down to **49 / 47**, all passing.
- Your ~540 / ~330 figure is the **pre-#27 baked atlas** — the render lane has **not yet ingested Gold #27 or #29**. Please re-ingest **Gold #30** (or #29) and the count drops to the 47/46 below.

## What #30 adds (durable guarantee + 3 residuals)
- New tool `partner-pitch/_tools/gate_route_id.py` — sibling of `gate_chips.py`; applies the **identical ±25% distance + endpoint-pair gate** to the singular `route_id`, nulling on fail. Now a mandated post-relink pass so no stale id can ever survive a seal.
- Caught **3 residual mislabels** in `hawaii.json`: items labeled "Honolulu ↔ Molokaʻi (Kaunakakai)" carried `edge__maui-county…__honolulu` (a maui→honolulu route). Nulled — confidently-wrong.

## Baked surface (data-clean/partners) — 100% clean
| axis | with id | failing |
|---|---|---|
| featured_routes | 47 | **0** |
| journeys_unlocked | 46 | **0** |
| route_ids chips | 107 | **0** |

## Answer to your question
**Yes — tighten the front-end guard from ±50% to ±25% to match our seal gate.** It is strictly safer (drops only borderline-wrong highlights) and the two surfaces will then agree exactly. Our seal now guarantees every surviving id passes ±25%+endpoint, so a ±25% front-end guard will never drop a legitimately-linked route.
