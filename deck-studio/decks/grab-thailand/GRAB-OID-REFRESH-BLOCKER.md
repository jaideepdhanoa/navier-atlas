# Grab Thailand — Slides OID refresh blocker (#118)

**Live deck:** `11WCun1Xk1flPmqvvtYrYZXsL5yRb5KQoe0xvTQSppKo`  
**Status:** KPI JSON refreshed; **Slides apply blocked** (OAuth + stale OIDs)

## Failure observed (phase 2)

```
g3eec5122801_0_15 not found on live presentation
```

Cached `slide-manifest.json` still lists `g3eec5122801_0_15` on slide 3, but the live deck was edited in-place and object IDs may have shifted.

## Values ready (no apply needed to regenerate)

| Artifact | Path |
|----------|------|
| Slide 3 KPIs | `deck-studio/decks/grab-thailand/slide3-kpis-grab-thailand.json` |
| Values sidecar | `deck-studio/decks/grab-thailand/deck-economics-values-grab-thailand.json` |

## Unblock steps (Tasklet or Grok after OAuth refresh)

1. Re-auth Google Slides (`deck_studio` OAuth token).
2. `python3 -m deck_studio pull --root deck-studio --deck grab-thailand --mode full`
3. Re-map slide-3 KPI object IDs in `economics-binding.json` from refreshed manifest.
4. `python3 deck-studio/builders/deck_grab_thailand.py apply` (or targeted KPI text ops only).

## Phase 4 note

Grok attempted `pull_manifest` for Minor gold deck — same `invalid_grant` OAuth failure. Grab refresh shares this blocker.