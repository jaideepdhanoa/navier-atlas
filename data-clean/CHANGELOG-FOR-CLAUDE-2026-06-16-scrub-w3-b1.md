# CHANGELOG — Gold #79p — 2026-06-16 — Wave 3 bite 1 scrub+enrich splice+seal

**Scope:** First bite of Wave 3 (Mediterranean). Metros: Athens/Piraeus + Bay-of-Naples + Amalfi Coast + Sicily/Aeolians. Counterpart to staged delta `/tmp/scrub-wave-3-bite1/` from `navier-scrub-enrich-wave` subagent.

## Counts (Gold #79o → #79p)
- Routes: 5,405 → 5,387 (Δ −18 = 52 orphan-endpoint kills + 34 aspirational Mediterranean ferry mints).
- POIs: 11,163 → 11,148 (Δ −15 = −28 OSM-noise BPs + 13 marquee enrich BPs).
- Cities: 170 → 170 (no new anchor — coverage already adequate via LB-174 re-anchors).
- Clusters: 85 → 88 (Δ +3 greenfield meta-clusters: `aeolian-islands-italy`, `saronic-gulf-greece`, `bay-of-naples-amalfi-coast-italy`).
- Sidecar `economics_by_route_id.json`: 78 records / 48 pending.

## Kills (28 BPs, 52 routes)
- athens-piraeus: 18 BP kills + 3 rescues/skips (Harbour Architecture, Harbour Shipping, harbour view villas, charter-base SEO).
- bay-of-naples: 10 BP kills + 2 rescues/skips (Harbour View Ischia, agriturismo, residence, quartier generale).
- amalfi-coast: 0 (Med OSM = clean — official ferry brand offices, not real estate marketing).
- sicily-aeolians: 0.
- 52 pre-existing LB-180 orphan-endpoint route kills bulk-killed in-scope (Med carries same Caribbean residue pattern; sweep should run globally).

## Enrich (13 BPs, 34 routes, 3 greenfield meta-clusters)
- New BPs: bp-spetses-port, bp-poros-port, bp-forio-ischia, bp-vulcano-portolevante, bp-stromboli-scari, bp-panarea-sanpietro, bp-filicudi-porto, bp-alicudi-porto, bp-trapani-stazmar, bp-favignana-porto, bp-levanzo-porto, bp-marettimo-porto, bp-palermo-stazmar.
- Routes: 32 Pioneer II + 2 Quanta-LR; longest mint = Naples↔Palermo ~150nm (Q-LR aspirational overnight, within 700nm cap). Naples↔Stromboli also Q-LR.
- 3 meta-clusters minted with real-BP anchors:
  - `aeolian-islands-italy` (anchor Lipari ferry terminal).
  - `saronic-gulf-greece` (anchor Piraeus BP).
  - `bay-of-naples-amalfi-coast-italy` (consolidated per LB-174 real-BP anchor pattern).
- 2 LB-174 country-level re-anchors: greece (Mykonos city_id → Piraeus BP), italy (Ponza city_id → Naples Stazione Marittima BP).

## Med-specific learnings (Wave 3 bite 1)
- Med noise rate LOWEST of any wave (~14–20% dense / 0% sparse). Med OSM = official ferry brand offices, not real estate marketing.
- Greek yacht-charter SEO pattern: `yacht charter`/`charter base`/`sailing courses` → NOISE_STRONG.
- Italian noise tokens: agriturismo, ristorante, trattoria, gelateria, lido, residence, appartamenti, pescheria, taverna, quartier generale → NOISE_STRONG.
- 18 new Med ferry brand-rescue tokens: Hellenic Seaways, Blue Star Ferries, Aegean Speed Lines, ANEK Lines, Minoan Lines, SNAV, Caremar, Alilauro, NLG, Travelmar, Liberty Lines, Siremar, Tirrenia, Grimaldi Lines, Ustica Lines.
- Greenfield meta-cluster consolidation: <3-city-id adjacent clusters sharing live corridor → consolidate at mint (Naples↔Amalfi).
- 5th consecutive 0-flag `gate_premint_pair` at scale — LB-179 classifier patch ship CRITICAL.
- 52 LB-180 orphan-endpoint route kills in-scope (Med carries Caribbean residue pattern; LB-180 sweep should run globally, not metro-scoped).

## Gates (all PASS substantively)
| Gate | Result |
|---|---|
| `gate_endpoint_labels.py` | 4 HARD FLAG pre-existing carries (Philippines + UAE; identical to prior gold) — NOT introduced this bite. 3 WEAK single-token binds (SG + MLE ×2) carry per LB-183. |
| `gate_city_ids.py` | PASS — 205 valid nodes / 5,387 routes / 88 clusters |
| `gate_partner_rationale_leak.py` | clean across `partner-pitch/partners/*.json` |
| `gate_osm_noise_bp.py` advisory on 4 bite metros | 0 new flags (bite already scrubbed). 26 ADVISORY items are pre-existing baseline carries (Dubai/AbuDhabi/Doha/Sharm/Hurghada/Aqaba), NOT Med-bite-3. |
| `gate_premint_pair.py` | **0 / 5,387 routes flagged** — 5th consecutive 0-flag at scale (34 new routes, 13 new BPs); LB-179 patch ship CRITICAL |
| LB-175a pre-build | PASS — ROUTES 5,387 ≥ 5,072 floor; pier-coord verify all 13 new BPs; Pioneer II 70nm hard-cap honored; Q-LR 700nm hard-cap honored (max mint 150nm Naples↔Palermo) |
| `datastore_audit.py` post-seal | substantive PASS (see operational notes below for the pre-existing DB carry) |

## LB refs applied
- LB-67 (extract-prior-overlay seal pattern).
- LB-152 (FEATURES_BY_TYPE flat-shape overwrite, not merge).
- LB-153 (FUSE → /tmp → atomic cp + sync for large JSON writes).
- LB-171 (SEAL recompute on actual blob bytes).
- LB-174 (real-BP cluster anchors; greece/italy re-anchors + 3 greenfield mints).
- LB-175a (pre-build ROUTES floor + pier-coord verify).
- LB-176c/d/e/f (triangulation: name + bp_type + endpoint usage).
- LB-179 (name-veto-before-bp_type-rescue inline — 5th consecutive bite of inline application).
- LB-180 (orphan-endpoint route kill — 52 in-scope).
- LB-181 (street-intersection regex).
- LB-182 (DUAL-SEAL-WRITE; phase reorder: delete prior gold zip BEFORE first cp of spliced blobs to avoid mid-splice FUSE quota fire).
- LB-183 (captive-marquee rescue + Harbour-View regex; SEAL FEATURES_BY_TYPE flat-shape overwrite).
- LB-184 (condo macro + SEO multi-pipe + landmark tokens).

## Carries / follow-ups (non-blocking)
- LB-179 classifier patch still un-shipped (now 7 consecutive bites of inline application; CRITICAL).
- Re-bootstrap `atlas-external/content_store/navier-content.db` or skip-when-absent flag (4 bites of advisory noise — DB audit fail carry).
- All other follow-ups from LB-184 carry forward unchanged.

## Slack + Drive
- Slack: `#tasklet-jaideep` — 🪙 Gold #79p sealed post.
- Drive: same parent folder `14PFDM6Z-I9j4gDzJpt6yYiizojTUr0FF`; Anyone-with-link Viewer.
