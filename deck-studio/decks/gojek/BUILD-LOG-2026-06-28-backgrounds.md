# Gojek × Navier — Indonesia backgrounds + economics restructure (2026-06-28)

**Live deck:** `13nnvUWkTUbLNFLkxRpJPOGgbvDVRVDdXvdybRTseGBs` (Slides API, in place — no rebuild/full-replace).
**Operator:** Tasklet. **Result:** 16 → **17 slides**.

## What changed (and why)
Jaideep's asks: (1) traditional mobility partner format like Grab Thailand, (2) add Indonesia backgrounds to replace stale Thailand imagery, (3) keep only **3 markets' economics** in the main flow, (4) move the rest to **backup** slides.

### 1. Indonesia backgrounds (market-specific N30 plates)
Replaced wrong-geography Thailand imagery on every slide that wasn't an Atlas map:

| Slide | Was | Now |
|---|---|---|
| 2 narrative | Bangkok skyline | Jakarta bay dusk skyline (generated plate) |
| 3 Three C's | Thai longtail boats | Nusa Penida cliffs (generated plate) |
| 8 Bali econ | Phuket plate | Bali clifftop (master registry, public) |
| 9 Singapore econ | generic | Singapore / Marina Bay (master registry, public) |
| 10 Riau↔SG econ | **Wat Arun (Bangkok temple)** | Singapore plate (master registry, public) |
| backup Komodo | Phuket plate | Komodo dragon-spine karst (generated plate) |
| backup Likupang | Phuket plate | North Sulawesi coast (generated plate) |

- 4 new plates generated on the N30-composite system (Bali plate as vessel/grade reference), navy scrim composited for legibility, committed under `deck-studio/assets/plates/gojek/` → stable GitHub raw URLs.
- Bali + Singapore reused from the master asset registry (both confirmed public).
- **Slides 4–7 (network/market maps) still show Thailand plates** — these are Atlas renders and remain Jaideep's lane.

### 2. Economics restructure (3 marquee + backup)
- **Main flow (3 deep-dives):** Bali · Singapore · Singapore↔Riau cross-border.
- **Backup:** Komodo & Flores and Likupang & Bunaken moved to the end, behind a new **"Appendix · Backup — Additional market unit-economics"** divider slide.
- Economics values unchanged from PR #135 (SAM $372M / TAM $1.5B / GMV $4.5B / platform $201M; SOM held $87M full-network convention).

## QA
Full PDF export reviewed slide-by-slide. Narrative (Jakarta), Three C's (Nusa), the three main econ slides, the appendix divider, and both backup slides all render correctly with legible headlines/eyebrows. Wat Arun and Phuket-on-Bali defects gone.

## Receipts
- Plates: `deck-studio/assets/plates/gojek/{plate-jakarta,plate-nusa,plate-komodo,plate-likupang}.png` + `PLATE-SOURCE.json` provenance.
- `deck.config.json` synced: `slide_count: 17`, backgrounds block records each applied plate + raw URL.
- Direct-edit deck — **not handed to Grok to rebuild**; corrected state lives here in source.
