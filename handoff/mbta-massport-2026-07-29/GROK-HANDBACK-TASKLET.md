# Grok handback — PR #343 MBTA / Massport authority deck

**From:** Grok (browser-merge lane)  
**Date:** 2026-07-29  
**PR:** https://github.com/jaideepdhanoa/navier-atlas/pull/343  
**Merge commit:** `d58e216c` on `main`  
**Branch:** `authority/mbta-massport-2026-07-29`  
**Seal tip on branch (pre-merge):** `cb34691` — image-manifest `used_by` live-verified write-back  

## Status: Grok lane closed for PR #343

Squash-merged to `main`. Local `main` fast-forwarded to match `origin/main` at `d58e216c`.

## What landed

| Surface | Path / note |
|---------|-------------|
| Deck registration | `deck-studio/decks/mbta-massport/` — `deck.config.json`, `slide-manifest.json` (20 slides), `image-manifest.json`, `RESEARCH.md` |
| Image manifest | **8/8** assets with live-verified `used_by` (commit `cb34691` on PR tip) |
| Map plates (fail-closed from gold ROUTES) | `deck-studio/assets/mbta-massport/city-maps/` — candidate-links · horizon-today · horizon-tomorrow |
| Composites (5) | `deck-studio/assets/backgrounds/decks/mbta-massport/` — cover, close, mandate, network, approach |
| Map receipt | `deck-studio/assets/mbta-massport/receipts/MBTA-DECK-MAPS-RECEIPT-2026-07-29.json` |

## Live deck

- Presentation: `1pvmw9YWp4bRzzCRYTgtZT4Xpj_lKJKwrGs2ydIzGkX0`  
- Chassis: WETA gold reference (Slides-API-only edits; Authority Format v2)

## Guardrails held (as authored)

- Public-value framing only on authority surface  
- Boston↔Logan only as study candidate under public-value framing (held in partner decks)  
- Map endpoints from sealed boarding points / gold `ROUTES.json`

## Stack context (Tasklet-listed earlier — all previously merged)

| PR | Topic | State |
|----|--------|--------|
| #332 | MX/EG city expansion | Merged earlier |
| #334 | Brazil deck images | Merged earlier |
| #335 | Egypt multi-route city plates | Merged earlier |
| #339 | Blade deck images | Merged earlier |
| #340 | Hornblower NYC | Merged earlier |
| #341 | Hornblower Boston | Merged earlier |
| #342 | NYC EDC authority deck | Merged earlier (`ce59e46f`) |
| **#343** | **MBTA / Massport** | **Merged now (`d58e216c`)** |

## Open PRs remaining

**0** at time of handback (verify on `jaideepdhanoa/navier-atlas` if anything else opened mid-flight).

## Tasklet next (if any)

1. Optional atlas prod deploy if authority pages/geometry from this stack should be live on Vercel  
2. Any post-bind copy/QA residual on the live MBTA deck stays Slides-API-only (no PPTX)  
3. No Grok geometry/seal work remaining on this PR — manifest already sealed with `used_by`

## Merge method

Squash merge via GitHub API; Vercel checks green (preview) before merge.
