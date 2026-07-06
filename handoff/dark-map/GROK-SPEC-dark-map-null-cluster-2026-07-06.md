# GROK SPEC — Dark-map: 56 routes with null cluster_id (global)

**Date:** 2026-07-06 · **Owner:** Grok (registry stamp lane) · **Data:** `handoff/dark-map/DARK-MAP-null-cluster-2026-07-06.json`

## What Tasklet found
Answering Jaideep's "does the dark-map issue apply to other markets?" — a global scan of `data-clean/ROUTES.json` (6,414 routes) found **56 routes with `cluster_id = null`**. A null cluster_id means the route renders on **no** market page — it's dark everywhere. This is the real dark-map class (NOT a Maghreb grain mismatch; Maghreb is correctly stamped).

## Affected markets (all have real clusters — pure missing stamp)
| Market | Routes | Examples |
|---|---|---|
| CalMac / Scotland | 25 | Oban↔Craignure, Kennacraig↔Islay, Uig↔Lochmaddy |
| Seoul (Hangang) | 5 | Yeouido↔Oksu, Ttukseom↔Jamsil, Magok↔Mangwon |
| Kolkata (river ferries) | 4 | Howrah↔Armenian Ghat, Fairlie Place↔Ariadaha |
| Angola | 4 | Luanda Marginal↔Mussulo, Lobito↔Benguela |
| Venezuela | 3 | La Guaira↔Los Roques, Maracaibo↔Cabimas |
| Cameroon | 3 | Douala↔Limbe, Kribi↔Douala |
| Namibia | 3 | Walvis Bay↔Pelican Point |
| Dubai (UAE) | 2 | Dubai Harbour↔Palm Jumeirah, Palm↔Atlantis |
| Norway (fjords) | 2 | Flåm↔Gudvangen, Balestrand↔Flåm |
| Ghana | 2 | Accra↔Tema, Ada Foah↔Keta |
| Congo (Brazzaville) | 2 | Pointe-Noire↔Côte Sauvage |
| Oman | 1 | Sohar Corniche↔Port of Sohar |

## Root cause
These are almost certainly the newest-minted corridors (BP-wishlist / isolated-city mints) added to `ROUTES.json` **before** the cluster_id stamp step ran — so endpoint piers exist but `cluster_id` was never assigned.

## Fix (deterministic — Grok)
For each of the 56 route_ids in the JSON: set `cluster_id` from the authoritative **endpoint `city_id` → cluster** registry. Every endpoint city already resolves to a real cluster (dubai-uae, seoul, kolkata-india, la-guaira-venezuela, calmac/scotland, luanda-angola, etc.). Keep endpoint `city_id`s unchanged.

> Tasklet could not build the city→cluster map itself: `CLUSTERS.json` `cities[]` arrays are empty in the data-clean copy (membership lives in the derived scope layer). Grok has the authoritative map.

## Standing rule
Add cluster_id stamping to the **mint step** so future BP-wishlist/isolated-city mints never ship null. This same class would keep the upcoming **Algeria (Annaba) + Senegal deepening** dark if minted without a stamp.

## Acceptance
`sum(1 for r in ROUTES if not r.properties.cluster_id) == 0`, and each of the 12 markets above lights up on its market page after deploy.
