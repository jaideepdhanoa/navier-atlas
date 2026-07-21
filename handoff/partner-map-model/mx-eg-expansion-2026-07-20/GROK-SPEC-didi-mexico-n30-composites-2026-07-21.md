# Grok spec — DiDi Mexico N30 city composites (2026-07-21)

**From:** Tasklet · **To:** Grok · **Deck:** DiDi Mexico `1XwKRuJtMrou8NtBdc1oY3LL2Dk83dCs9MCLvNKgwq0c` (18 slides)

## What Tasklet sourced
Two market-specific N30 composites for the Phase-4 backup city slides. Both are `banked` in the repo,
registered in `ASSET-REGISTRY.json`, with provenance and sha256, and marked `banked` in
`deck-studio/decks/didi-mexico/image-manifest.json`.

| image_key | asset | slide | scene |
|---|---|---|---|
| `holbox_city_n30` | `didi-mexico-holbox-n30` | 15 (Isla Holbox city deep-dive) | white N30 on foils crossing the turquoise Yalahau lagoon toward car-free Holbox; low sandy island, mangroves, pastel beach shacks, wooden pier |
| `huatulco_city_n30` | `didi-mexico-huatulco-n30` | 17 (Bahías de Huatulco city deep-dive) | white N30 on foils on deep-blue Pacific; rugged green Oaxacan headlands, protected bay, golden-sand beach, Santa Cruz marina breakwater, golden hour |

- `deck-studio/assets/didi/didi-mexico-holbox-n30.png` — 1536×864, sha256 `149b6fa6530c69ffb93a089cc5fc6694b5541b8e42aef0764481a2f9ac2413dd`
- `deck-studio/assets/didi/didi-mexico-huatulco-n30.png` — 1536×864, sha256 `16f901711d89149445617402bb1362d698eba84ca6dc12368af7828e7d55a414`

## What Grok does (post-merge)
1. **Pin the stable URL.** After merge, fill `source_url` in each `ASSET-REGISTRY.json` entry with the
   commit-pinned `raw.githubusercontent.com/jaideepdhanoa/navier-atlas/<merge-sha>/<local_path>` URL
   (same pattern as `didi-city-route-map-*`). Update the manifest if you carry the URL there too.
2. **Place each composite** as the `n30_market_composite` background/hero element on its slide via the
   Slides API, as a registry-resolved element (do not re-embed a one-off binary).
   - Slide 15 ← `holbox_city_n30`
   - Slide 17 ← `huatulco_city_n30`
3. **Do NOT touch the `atlas_route_screenshot_slide_15` / `_slide_17` slots** — those remain
   human-insertion-only (Jaideep places the Atlas map). One N30 composite + one human Atlas slot per city.
4. Keep the headline/route-box text objects on top; the composite sits behind them (upper-left third of
   each plate was kept clear for the headline).
5. Return a QA receipt: deck ID, the two placed object IDs, image provenance (asset + sha256 + source_url),
   and a no-op replay confirmation.

## Guardrails
- No Atlas-generated imagery; these are market-sourced N30 composites with saved provenance.
- Vessel form/color matches `n30-reference-neutral` (lighting is a plate property; hull kept neutral).
- Main spine S1–14 untouched; this only fills imagery on backup slides 15 & 17.
