# Isolated-City & Empty-Market Audit — July-3 vs current (a9b5d47e)

**Question:** did these gaps exist before the cull, or did the cull create them?
**Method:** `market_coverage_audit.py` on July-3 build vs current, same CLUSTERS.

## Definitions
- **Empty market** = canonical cluster with 0 routes attaching by endpoint-city membership.
- **Isolated city** = a canonical city on the map (has a boarding point) that **no corridor touches** — a lone dot with no routes.
- **Registry-gap route** = a route whose endpoints resolve to no canonical cluster (CalMac/Norway); honest-null until backing city features exist.

## Result

| Bucket | July-3 | Current | Verdict |
|---|---|---|---|
| Empty markets | 7 | 7 | 6 pre-existing; Peru **fixed**; Taiwan newly-empty (the out-of-range Jakarta↔Penghu drop) |
| Sparse markets | 13 | 13 | flat |
| Isolated cities | 25 | 35 | +24 new / −14 recovered |
| Registry-gap routes | 78 | 66 | improved (−12) |

## Isolated cities — the honest breakdown of the 24 "new"
Touch-count analysis (July-3 partners):
- **~19 cities had ONLY self-referential intra-city micro-hops** on July-3 (Casablanca 116 self-hops, Corfu 40, Crete 32, Costa Brava 30, Likupang 30, Milos 28, Kochi 28, Kerala 24…). The de-spaghetti pass **correctly** removed these as <3nm / self-referential junk. These cities were never genuinely connected — they were map-dots padded with noise. "Isolated" here is **more honest, not worse**. → real BP-pair sourcing targets (my wishlist lane).
- **5 cities lost GENUINE inter-city corridors** → **restore** (Batch 2b): Koh Lanta↔Phi Phi/Krabi/Phuket (Andaman), Cannes↔St-Tropez, Nice↔St-Tropez (Riviera). All have proven water geometry @ July-3. Added to restore register.

## What we need to do
1. **Restore the 5 real corridors** (Batch 2b) — copy-proven-features, done in register.
2. **BP-pair sourcing** for the ~19 self-hop-only cities + 6 pre-existing empty markets — Tasklet flags real piers, Grok mints. Nobody invents a pier.
3. **66 registry-gap** (CalMac/Norway) = honest-null until backing city features exist.
4. **Taiwan** stays empty (Jakarta↔Penghu is out of range; Kaohsiung↔Penghu is intra-Taiwan only) — defer unless Jaideep wants a Taiwan sourcing pass.
