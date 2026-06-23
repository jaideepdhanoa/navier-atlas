# Bolt-markets locale + POI cleanup — seal handoff (2026-06-23)

Wave 1b of the cleanup program (UAE = PR #82, Thailand = PR #89, **this = Bolt markets**, then the rest).
Tasklet supplies the country-agnostic spec/ledger; Grok applies + runs the residual gate + reseals.
`main` stays source of truth.

## Method (no guessing)
Country-agnostic, **gazetteer-free**: exact-dedup + universal junk/artifact + wrong-city retag only where a
POI name carries a *different in-scope city's own sealed name*, geometry-corroborated. Anything not
high-confidence is left for Grok's geometric residual gate — exactness over coverage, null beats
confidently-wrong.

## Scope
Bolt footprint excl. UAE (done) + Thailand (PR #89): 20 countries, 68 cities.
**Sovereign Saudi-PIF cities (NEOM / Red Sea Global / AMAALA / Sindalah) EXCLUDED** (bespoke/held builds).

## Tally
- **POIs (2258):** 16 exact-dedup · 38 identity retags · 19 junk/artifact drops · 2134 kept ·
  **51 review** (name carries another city, geometry uncertain → Grok residual gate).
- **Locales (11):** 6 keep · 5 drop (combined/inland corridor artifacts).

## Highlights
- Whole **Côte d'Azur** (Nice/Cannes/Antibes ports) was mis-parented under **Monaco** → retagged.
- **Mykonos** cluster mis-parented under **Paros** → retagged.
- **Doha ↔ Manama** cross-tagging both directions; **Hurghada ↔ Sharm**; **Dar es Salaam** under **Zanzibar**.
- **Cross-border corridor pointers** ("Dubai Marina … endpoint" under Doha, etc.) dropped as artifacts.
