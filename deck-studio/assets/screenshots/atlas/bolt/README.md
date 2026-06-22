# Bolt deck — Atlas route screenshots

Human or automated captures from Navier Atlas for market side-panel slides **4–6** and **14–18**.
No Tier-A generation — register and apply via `python builders/deck_bolt_wave2_images.py apply-atlas-screenshots`.

## Automated capture (Playwright)

From `deck-studio/`:

```bash
# Local _dist (no password) — preferred for batch capture
python builders/deck_bolt_wave2_images.py capture-atlas-screenshots --serve-dist

# Prod Vercel (requires PARTNER_AUTH_BOLT or --password)
python builders/deck_bolt_wave2_images.py capture-atlas-screenshots --base-url https://navier-atlas.vercel.app
```

Then apply: `python builders/deck_bolt_wave2_images.py apply-atlas-screenshots`

## Required files

| Slide | Filename | Market / corridor |
|------:|----------|-------------------|
| 4 | `slide-04-athens-saronic-greece.png` | Athens → Saronic (Greece) |
| 5 | `slide-05-split-croatia.png` | Split (Croatia) |
| 6 | `slide-06-cote-dazur-france.png` | Côte d'Azur (France) |
| 14 | `slide-14-sorrento-italy.png` | Sorrento / Amalfi (Italy) |
| 15 | `slide-15-dubai-uae.png` | Dubai (UAE) |
| 16 | `slide-16-jeddah-ksa.png` | Jeddah (KSA) |
| 17 | `slide-17-mykonos-greece.png` | Mykonos / Cyclades (Greece) |
| 18 | `slide-18-dubrovnik-croatia.png` | Dubrovnik (Croatia) |

## Capture notes

- Frame the Atlas route/map UI clearly; include corridor labels and distance if visible.
- PNG, 16:9 preferred; minimum 1920×1080.
- Authoritative wiring: `decks/bolt/slide-image-bindings.json` (`atlas_filename` per slide).