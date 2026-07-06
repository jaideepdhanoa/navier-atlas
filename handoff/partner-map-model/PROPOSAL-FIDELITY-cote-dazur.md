# Proposal fidelity — cote-dazur

**Verdict:** REWRITE
**Checked:** 2026-07-06T05:04:09Z

## Summary

- Items audited: 5
- KEEP: 3
- DROP: 2
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 2

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Nice (Port) → Monaco (Port Hercule) | `e__cote-dazur-france__port-de-nice__monaco-monaco__port-hercule` | **DROP** | route_missing: e__cote-dazur-france__port-de-nice__monaco-monaco__port-herc; bp_binding: route_id e__cote-dazur-france__port-de-nice__monaco-monaco__ |
| journey | — | Cannes → Îles de Lérins (Sainte-Marguerite) | `ics-529325c5eb` | **DROP** | route_missing: ics-529325c5eb not in gold; bp_binding: route_id ics-529325c5eb missing from ROUTES.json |
| featured | 1 | Nice (Port) ↔ Monaco (Port Hercule) | `—` | **KEEP** | — |
| featured | 2 | Cannes ↔ Îles de Lérins (Sainte-Marguerite) | `—` | **KEEP** | — |
| featured | 3 | costa-smeralda-italy ↔ cote-dazur-france | `—` | **KEEP** | — |
