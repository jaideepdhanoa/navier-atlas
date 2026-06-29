# Proposal fidelity — freenow

**Verdict:** TRIM
**Checked:** 2026-06-29T14:28:18Z

## Summary

- Items audited: 19
- KEEP: 17
- DROP: 2
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 2

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Piraeus, Athens → Hydra Port | `rn-678c1b2769a9` | **KEEP** | — |
| journey | — | ACI Marina Trogir → Hvar Town Harbour | `rn-7c1e7f62f283` | **KEEP** | — |
| journey | — | Nice Port → Monaco Hercules harbour | `rn-48bac1363efe` | **KEEP** | — |
| journey | — | Dubai Marina → Downtown Creek | `—` | **KEEP** | — |
| featured | 1 | Dubai Marina Yacht Club (DMYC) → Le Méridien & Wes | `gcn-0ca7f3ffe7-bolt` | **KEEP** | — |
| featured | 1 | Port Hercule (Monaco) → Port de Villefranche-sur-M | `ics-4269303d3c` | **KEEP** | — |
| featured | 1 | Jeddah Corniche — North Public Pier → Jeddah Centr | `gcn-adcdd3d09c-bolt` | **KEEP** | — |
| featured | 2 | Marina Zeas (Piraeus) → 2nd Glyfada Marina | `rn-89552c9786ec` | **KEEP** | — |
| featured | 2 | Nice Port → Port Hercule (Monaco) | `rn-d66efc6795b3` | **KEEP** | — |
| featured | 2 | Dubai Harbour Marina → Anantara World Islands Reso | `gcn-6a2841d6db-bolt` | **KEEP** | — |
| featured | 3 | Red Sea Global (RSG + AMAALA) → Nujuma, a Ritz-Car | `rn-1a140dacd3e6` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Red Sea Global (RSG + AMAALA |
| featured | 3 | Molo Beverello (Naples) → Casamicciola | `rn-31d27d5fc623` | **KEEP** | — |
| featured | 3 | Mykonos New Port (Tourlos) → Naxos Port (Chora) | `rn-dc595b5a6ab8` | **KEEP** | — |
| featured | france/p1 | Corsica — Ajaccio, Bonifacio & Bastia → Bonifacio | `ics-6e37714d71` | **KEEP** | — |
| featured | greece/p1 | Piraeus, Athens → Hydra Port | `rn-678c1b2769a9` | **KEEP** | — |
| featured | ireland/p1 | Dublin Docklands (North Wall Quay) → Dún Laoghaire | `rn-455eede91b5a` | **KEEP** | — |
| featured | italy/p1 | Porto di Pozzuoli → Marina Grande (Capri) | `rn-2508d7811cef` | **KEEP** | — |
| featured | spain/p1 | Barcelona & the Costa Brava → Palamós | `ics-81984b66e9` | **KEEP** | — |
| featured | united-kingdom/p1 | London (River Thames) → London | `ics-5e35d5734e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'London (River Thames)' → 'Lo |
