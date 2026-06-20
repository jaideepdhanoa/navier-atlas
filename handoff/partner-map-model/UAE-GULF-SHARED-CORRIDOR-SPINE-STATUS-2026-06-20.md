# UAE / Gulf Shared Corridor Spine — Execution Slice 1

Source branch: `partner-proposal-schema-conformance-pr57` (`4611a7f`).

## Scope rules applied

- Noon mirrors Careem: domestic UAE plus cross-border from UAE, modeled like Careem/full-journey GMV.
- RAKTA focuses on RAK only, then RAK to other UAE emirates, then Musandam/Muscat/Doha/Bahrain.
- Bahrain MOTC focuses on Bahrain, KSA Eastern Province, Doha, Dubai, and Abu Dhabi.
- All RAK/Bahrain/Gulf cross-border routes are Quanta-LR roadmap except Manama ↔ KSA Eastern Province as commercial-now candidate.

## Extracted route counts

- **bahrain_domestic**: 92 routes; 87 geometry-present; 5 quarantined/hidden; 86 commercial-now candidates; 0 Quanta-LR roadmap.
- **bahrain_gulf_cross_border_roadmap**: 7 routes; 6 geometry-present; 1 quarantined/hidden; 0 commercial-now candidates; 7 Quanta-LR roadmap.
- **bahrain_ksa_eastern_province**: 3 routes; 2 geometry-present; 1 quarantined/hidden; 2 commercial-now candidates; 0 Quanta-LR roadmap.
- **domestic_uae_intra_city**: 706 routes; 452 geometry-present; 254 quarantined/hidden; 446 commercial-now candidates; 0 Quanta-LR roadmap.
- **inter_emirate_uae**: 26 routes; 18 geometry-present; 8 quarantined/hidden; 18 commercial-now candidates; 0 Quanta-LR roadmap.
- **rak_cross_border_roadmap**: 3 routes; 3 geometry-present; 0 quarantined/hidden; 0 commercial-now candidates; 3 Quanta-LR roadmap.
- **rak_musandam_candidate**: 5 routes; 4 geometry-present; 1 quarantined/hidden; 0 commercial-now candidates; 0 Quanta-LR roadmap.
- **uae_gulf_cross_border**: 23 routes; 14 geometry-present; 9 quarantined/hidden; 0 commercial-now candidates; 23 Quanta-LR roadmap.

## Immediate posture

- **Noon:** fastest GCC proposal because it can clone Careem geography/GMV logic, with Noon-specific consumer-platform narrative.
- **RAKTA:** route spine exists for RAK domestic and Gulf roadmap; RAK ↔ Musandam is represented indirectly through Khasab-labelled RAK routes and needs exact registry treatment before proposal-ready map display.
- **Bahrain MOTC:** Manama ↔ Eastern Province is the only commercial-now cross-border candidate under current instruction; Doha/Dubai/Abu Dhabi stay Quanta-LR roadmap.