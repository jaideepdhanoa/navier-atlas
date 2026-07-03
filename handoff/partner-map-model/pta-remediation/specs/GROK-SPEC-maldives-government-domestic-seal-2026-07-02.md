# GROK SPEC — Maldives National Ferry Network (RTL) domestic seal + economics (Phase B Batch-6)

**Partner:** `maldives-government` · **Authority:** Government of the Maldives (Ministry of Transport) / MTCC — Raajje Transport Link (RTL)
**Dossier:** `handoff/partner-map-model/PTA-DOSSIER-maldives-government.json`
**Tasklet state:** resort→public **correction landed**. Prior draft led with resort-transfer jetties (Soneva Fushi, Six Senses, Baros) and used "resort transfers" as the proof spine — both **removed**. Proposal now leads with the PUBLIC RTL network: Greater Malé resident corridors + national atoll reach. Hero eyebrow set; phases rebuilt to public-network domestic-first arc; route_ids null + `_link_status: geometry_seal_pending` + `_seed_node`. Commercial `growth_case` removed → `_pta_economics_status: grok_authority_regen_pending`. Fidelity PASS; build exit 0.

## 1. Mint seed boarding points (Greater Malé — high confidence)
Register the 8 public terminals from `domestic_network.boarding_points` (approx anchor `[lng,lat]`). Node ids canonical:
`male-ferry-terminal`, `hulhumale-ferry`, `villimale-ferry`, `thilafushi-jetty`, `maafushi-jetty`, `gulhi-jetty`, `guraidhoo-jetty`, `thulusdhoo-jetty`. City: `male-maldives`.
**Do NOT reuse the old resort-jetty nodes** (soneva-fushi/six-senses/baros); those are out of scope for the public authority.

## 2. Seal the 7 domestic pairs (ID-based, 1:1) — PUBLIC network only
| pair | from → to | approx nm | vessel |
|---|---|---|---|
| mal-d01 | male-ferry-terminal → hulhumale-ferry | 5 | Pioneer II |
| mal-d02 | male-ferry-terminal → villimale-ferry | 1.5 | Pioneer II |
| mal-d06 | male-ferry-terminal → thilafushi-jetty | 4 | Pioneer II |
| mal-d03 | male-ferry-terminal → maafushi-jetty | 14 | Pioneer II |
| mal-d04 | male-ferry-terminal → gulhi-jetty | 11 | Pioneer II |
| mal-d05 | male-ferry-terminal → guraidhoo-jetty | 16 | Quanta-LR |
| mal-d07 | hulhumale-ferry → thulusdhoo-jetty | 14 | Pioneer II |

## 3. National RTL reach — qualitative, DO NOT mint speculative distant-atoll corridors
The northern (Ha/Hdh/Sh), Lh, and southern (Ga/Gdh) RTL zones are described in the narrative as the authority's reach. **Do not mint precise inter-island corridors in distant atolls** — exact berth pairs are unverified and "null beats confidently-wrong." If/when Grok has sourced atoll-capital coordinates, propose them as a separate additive seed for Tasklet validation.

## 4. Hand waypoints — lagoon/channel water only, NO reef or island crossings (mandatory)
- Every inhabited island sits inside a reef ring — route to charted channel entrances (Maafushi, Gulhi, Guraidhoo, Thulusdhoo), never straight-line to shore.
- Depart Malé via the charted public-ferry channel, clear of the congested commercial anchorage.
- Longer legs (Guraidhoo, Thulusdhoo) cross open current-swept inter-atoll channels — weather/current-aware waypoints.
- Observe protected reefs / marine areas. See `routing_hazards`.

## 5. No cross-border link
`regional_links` intentionally empty. Do not mint a Colombo↔Malé corridor (not a public RTL route).

## 6. Economics (Grok lane) — full re-author
**growth_case removed.** Partner is `grok_authority_regen_pending`, no economics panel renders until you re-author. Source finance data retained at `finance/recal/growth-maldives-government.json` (if present). Re-author `growth_case` → `public_value` + authority operating-model (RTL public fares) + headlines, set `_economics_status: pta_regenerated`. Apply the Phase-A convention (no forbidden GMV/TAM keys, plain-English fares). **Frame the economics on the PUBLIC network, not resort transfers.**

## 7. Acceptance
- `audit_proposal_fidelity.py --partner maldives-government` → PASS
- No resort-transfer framing in partner-facing copy (one contextual "beyond the resorts" contrast is intentional)
- build exit 0
