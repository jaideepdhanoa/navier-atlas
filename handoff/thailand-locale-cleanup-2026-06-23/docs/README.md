# Thailand locale + POI cleanup — seal handoff (2026-06-23)

Mirror of the UAE cleanup (PR #82). Tasklet supplies the spec/ledger; Grok applies it deterministically,
runs the residual gate, and reseals to the next gold tag. GitHub `main` stays source of truth.

## Contents
| Path | What |
|---|---|
| `docs/GROK-SEAL-PROMPT.md` | The mandate (apply order, guardrail, acceptance gate) |
| `inputs/THAILAND-CLEANUP-LEDGER.json` | Exact ids: dedup / retag / junk / locale keep+drop |

## Confirmed directives
- **Rather not have them than have them wrong** (Jaideep 2026-06-23).
- Wrong-city POIs are **retagged** to the correct in-scope city (the pier is real, only the parent was wrong);
  combined / corridor / foreign locales are **dropped**; exact-duplicate copies are **collapsed**.
- Sequence: **Thailand first → all Bolt markets → the rest.** This package is Thailand only.

## Tally
- **POIs (363):** 74 exact-dedup drops · 53 identity retags · 19 junk/annotation drops · 217 kept in place.
- **Locales (11):** 3 keep (Phang Nga Bay, Phuket east coast, Phuket west-coast belt) · 8 drop
  (2× Malaysia, 2× cross-Gulf Koh Samui, combined Krabi+Phi Phi, Bang Saray/Sattahip, Koh Chang/Trat-via, Pattaya/Ocean Marina).

## Dependency
Retag targets include **hua-hin / cha-am / koh-samet** (new cities in PR #88) — seal those first so the
retags land on existing cities.
