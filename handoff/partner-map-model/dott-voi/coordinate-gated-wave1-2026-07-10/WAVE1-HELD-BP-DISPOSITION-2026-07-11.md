# Wave1 held BP disposition — 2026-07-11

**At:** 2026-07-11T16:58:07Z
**Status:** `disposition_complete_no_mints`
**Held BPs:** 21 (permanent 6, research-gated 15, sealed this pass 0)

Autonomous pass reviewed all 21 held BPs. None had newly available exact T1/T2 named-landing coordinates that meet the coordinate-gated seal gate. All remain held with explicit dispositions. Hand-geometry routes for sealed BPs completed separately.

## Permanent holds

- **Portus Ganda** — `permanent_hold_identity_ambiguity`: Multiple exact features; selecting one would invent identity.
- **Estación Marítima de Formentera (Port of Ibiza)** — `permanent_hold_dedupe_canonical`: Must reuse existing route endpoints; no new BP mint.
- **La Savina passenger terminal** — `permanent_hold_dedupe_canonical`: Must reuse existing route endpoints; no new BP mint.
- **Egholmfærgen ferry landing, Aalborg (Egholm Færgevej 23)** — `permanent_hold_identity_ambiguity`: Multiple exact features; selecting one would invent identity.
- **Broomielaw Pontoon** — `permanent_hold_closed`: Source reports closed until further notice; null beats wrong.
- **Govan Pontoon** — `permanent_hold_closed`: Source reports closed until further notice; null beats wrong.

## Research-gated holds (still blocked)

- **Sint Anna** — `hold_pending_t1_t2_coordinate`: Only a T3 commercial map pin was found. The OSM search surfaced a nearby public-transport stop named Sint-Anna Veerdienst, not an exact ferr
- **Muttenz Waldhaus** — `hold_pending_t1_t2_coordinate`: Federal geodata search returned a bus stop and Restaurant Waldhaus, but no exact boat landing. No exact named OSM ferry/landing object was f
- **Bootshafen Hörnlibuck** — `hold_pending_t1_t2_coordinate`: The exact named marina did not resolve in the federal or OSM searches. Available evidence was a T3 commercial map pin or a nearby bus stop, 
- **Hafen Hard** — `hold_pending_transfer_suitability`: specific official municipal marina; passenger-transfer suitability not yet proven
- **Klosterneuburg ferry landing** — `hold_pending_exact_feature`: Held for exact feature identity: the plausible opposite-bank OSM terminal is unnamed, so it does not meet the exact-named T2 threshold. A te
- **Margitsziget stop** — `hold_pending_t1_t2_coordinate`: Held for exact feature identity: multiple island landings exist and no exact named Sportuszoda T1/T2 coordinate was found. A current operato
- **Viikinsaari Island landing** — `hold_pending_name_validation`: Operator names the destination as Viikinsaari Island, not a formal pier name; Grok must confirm terminal naming before bank.
- **Egholm ferry landing** — `hold_pending_name_validation`: Municipal page describes the Egholm ferry landing functionally; Grok must verify canonical local label and exact point.
- **Nordermole Travemünde landing** — `hold_pending_t1_t2_coordinate`: The official source identifies the Priwall VI passenger ferry at Nordermole, but exact-feature searches found only the Nordermole lighthouse
- **Priwall ferry landing** — `hold_pending_exact_feature`: Nearby named OSM 'Priwallfähre' terminals are for the separate vehicle ferry farther upriver; they cannot be substituted for the Priwall VI 
- **Flensburg Fördebrücke** — `hold_pending_t1_t2_coordinate`: Exact-feature searches found bus stops named Fördebrücke but no exact named ferry pier/landing object that can be tied to the MS Viking oper
- **Glücksburg Seebrücke** — `hold_pending_t1_t2_coordinate`: Only a T3 map-listing coordinate was found for the exact name; no T1/T2 coordinate/geolocation source was verified, so the point remains hel
- **KD Bonn-Bad Godesberg landing stage** — `hold_pending_exact_feature`: Exact local landing-stage label should be confirmed before banking.; source status: hold_name_validation
- **Port-Deauville–Les Marinas** — `hold_pending_exact_feature`: Only general marina/harbour coordinates were found. No T1/T2 object could be reconciled to the exact Deauville/Trouville passenger landing; 
- **Westerplatte water-tram stop** — `hold_pending_exact_feature`: Exact passenger landing could not be isolated. General Westerplatte or quay coordinates would be speculative.

