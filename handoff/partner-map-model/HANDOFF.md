# Partner Map Model — Existing-Registry Coastal Footprint Reconciliation

This amends the universal partner-map rollout with a stricter rule from Jaideep:

- Include **every coastal / waterfront-relevant market already grounded in the shared registry** when a partner's written footprint references that market or region.
- Do **not** research or create new boarding points/routes in this pass.
- If a market is not already registry-grounded, leave it as `registry_key:null` / aspirational backlog.

## What changed vs the first PR #55 pass

The first pass created the universal binding framework but was conservative for broad market IDs (`mena`, `mediterranean`, `thailand`, etc.). This pass adds explicit aliases from those broad written markets to already-grounded registry keys only.

### Bolt / Yango

No change needed from the first universal pass:

- **Bolt:** 18/18 bound, 0 null. Regions covered: Europe + MENA, with Israel/Lebanon sovereign-held off-map.
- **Yango:** 15/15 bound, 0 null. Regions covered: MENA, Africa, Central Asia/Caucasus, Turkey, with Israel sovereign-held off-map.

Important caveat: this is complete against the **current registry-grounded coastal footprint**, not a newly researched official global operating-country roster.

### Uber

Upgraded from 9 aspirational/null stories to **20 footprint entries**:

- **15 bound** via existing registry markets:
  - MENA/Gulf: `uae-careem`, `uae-luxury`, `qatar`, `saudi-redsea`, `saudi-redsea-resort`, `bolt-egypt`, `yango-egypt`, `yango-morocco`, `yango-tunisia`
  - Mediterranean: `bolt-greece`, `bolt-croatia`, `bolt-italy`, `bolt-france-riviera`, `bolt-cyprus`, `yango-turkey`
- **5 remain null/aspirational:** `bay-area`, `brazil-latam`, `hawaii`, `miami`, `sydney-nsw`

### Other partner upgrades

- **Lyft:** `athens-cyclades` now binds to `bolt-greece`; US coastal markets remain null.
- **Line:** Thailand now binds only to already-grounded Thailand keys (`bangkok`, `phuket`, `koh-samui`); Taiwan already bound; Japan remains null.
- **inDrive:** Egypt/Morocco/Sub-Saharan Africa stories now bind to existing Yango/Bolt Africa/MENA keys; India remains null.
- **Aman / Soneva / Four Seasons / Six Senses / Gojek:** broad Indonesia/Maldives/Thailand/Riau-Singapore stories bind to existing SEA/Indian-Ocean registry keys where available.

## Remaining honest gaps

Backlog is now **63 entries**:

- LATAM remains ungrounded in this registry version: Didi's Brazil/Mexico/Colombia/Panama/Costa Rica/Dominican Republic and Uber `brazil-latam` still stay null.
- US/Australia/Korea/India/Japan/Seychelles/Venice and some resort-specific coastal stories also remain null.
- No fake geometry was introduced.

## Implementation rule for Grok

`network_footprint[].registry_key` is the only source for inherited cities/routes/economics. `registry_key:null` remains visibly aspirational. `map_scope` includes only `map_promote:true` entries with sealed cluster cities.

Null beats confidently-wrong. Geometry first.
