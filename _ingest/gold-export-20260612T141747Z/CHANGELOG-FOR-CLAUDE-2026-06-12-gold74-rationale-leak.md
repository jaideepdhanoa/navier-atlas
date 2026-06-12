# Gold #74 — rationale leak-gate fix (2026-06-12)

## Trigger
Jaideep flagged "geometry pending — speculative bind" as internal jargon surfaced in partner-facing rationale fields.

## What changed
- `data-clean/partners/grab.json`: 4 rationale strings rewritten to partner-safe copy
  - 3× "Aspirational — geometry pending — speculative bind" → "Aspirational route — opportunity flagged for future build-out"
  - 1× "Quanta-LR queue (~50nm coastal line); geometry pending — speculative bind" → "Quanta-LR queue (~50nm coastal line); aspirational route for future build-out"
- `SEAL.json` resealed: meta.gold #73 → #74, partner-blob SHA refreshed, `sealed_at` bumped

## What did NOT change
- ROUTES / FEATURES / sidecar — identical to Gold #73
- All other partners — none had the offending strings

## Rule banked (LB-137)
Partner JSON `rationale` fields render in deck/atlas → partner-facing. Internal hygiene terms (sidecar, speculative bind, bind-stats, gate, leak) are banned from these fields. Pre-flight leak gate must scan `partners/*.json` `rationale` recursively, not just narrative blocks.
