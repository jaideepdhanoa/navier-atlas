# Addendum — canonical marquee sets (v2: city-level + hero-ranked)

## What changed from v1
1. **Granularity → city.** Sets are now keyed by `city_id`, not the country-cluster.
   Every partner operating in a city inherits the **same** set for that city
   (all UAE partners see the same **Dubai** set, the same **Abu Dhabi** set, etc.).
   A partner's featured/wow = union of the marquee sets for the cities in its clusters.
   Inter-city corridors appear in **both** endpoint cities' pools.
2. **Ranking → hero (water-beats-road), not popularity.** v1 floated trivial 2 nm
   resort hops because it scored on crowd-feature-frequency + traffic. v2 scores on:
   distance sweet-spot (peaks ~12 nm) + island endpoint + cross-city water-advantage;
   traffic_weight / crowd-features are **tiebreakers only**.
3. **Firm 3 nm floor, no exceptions.** Trivial hops (Kempinski↔Atlantis 2.0 nm,
   One&Only↔Zabeel Saray 1.9 nm, Al Marjan↔Wynn 0.4 nm) are gone by construction.
4. **Junk-endpoint filter.** Excludes jet-ski / water-sports / helipad / seaplane /
   slipway / parking / mislabeled cross-border artifacts (killed the bad-geocode
   "Dubai Marina → Old Doha Port @ 4.5 nm").

## Coverage
- **217 cities** with ≥1 marquee; **163** with ≥3.
- **978 current entries retired** (348 free-text strings, 27 no-BP-id, 603 not-in-canonical) → archive, not delete.
- WOW ≤5, FEATURED ≤8 per city.

## UAE worked example (identical for Careem / Bolt / Yango / Noon)
**Dubai:** Dubai Creek/Old Souq ↔ Atlantis The Palm (12.6) · Dubai Harbour ↔ The World Islands (8.2) · Mina Rashid ↔ Dubai Islands (4.1) · Old Souq ↔ Harbour Seafood (12.0) · Dubai Marina ↔ Al Jaddaf upper Creek (13.5).
**Abu Dhabi:** Yas Marina ↔ Zaya Nurai Island (12.6) · Yas ↔ Saadiyat Beach Club (13.0) · Emirates Palace ↔ Saadiyat (10.4) · Jebel Dhanna ↔ Sir Bani Yas (9.8) · Eastern Mangroves ↔ Yas (8.3).
**Sharjah:** Sharjah ↔ Dubai Islands (6.4) · Al Majaz ↔ Park Island (19.9) · Al Noor ↔ Al Qasba (3.4) · Vida UAQ ↔ Sharjah Waterfront (7.3).
**Ras Al Khaimah:** Al Marjan Island ↔ RAK city (15.1) · RAK ↔ Al Marjan arrival marina (16.0) · Al Marjan ↔ Jazirat Al Hamra (5.9).

## Grok's job (unchanged contract)
Curation is OD-pair level (BP node pair + city_id + cluster_id). Grok **binds/re-stamps
`route_id`** deterministically after reseal; the named waterfront pairs are canonical.
Anything genuinely ambiguous is left for Grok to confirm against resealed geometry —
**null beats wrong.** Seal gate rejects any partner featured/wow entry not in its
cities' canonical sets.

## Residual notes for the locale-cleanup lane
- A few aggregate/junk BP display labels persist (e.g. Colombia "Cartagena & The
  Rosario Islands" used as an endpoint) — flag for label scrub, not corridor drop.
- Thailand cities are sparse here (river piers < 3 nm culled by the firm floor);
  revisit Chao Phraya iconic short hops if a river exception is wanted later.
