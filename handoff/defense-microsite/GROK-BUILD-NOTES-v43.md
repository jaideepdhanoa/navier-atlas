# /defense v4.3 — Morpheus Gallery (larger-vessel imagery)

**Why:** Founder request (Sampriti, 2026-09-02) — /defense must not read as a small-boats-only provider.

**What changed (contract `deck-studio/microsite/contracts/defense.json`, version → v4.3):**
1. `def-family.morpheus_gallery` — NEW beat, placed directly after the ladder, before the PLATFORM beat.
   - 3 images: `defense-morpheus-logistics-v1.png` (golden-hour containerized logistics, 16:10 crop from the left of n180-morpheus-hero.png) · `defense-morpheus-drone-carrier-v1.png` · `defense-morpheus-escort-v1.png` (drone/escort cropped top/bottom to 16:10).
   - **CONCEPT RENDER badge mandatory on every image** — small-caps chip, top-left, site chip style.
   - Class name **"Morpheus" only** — no hull number, no length, no range/spec figures.
   - V4 crop rule applies: never crop the vessel at any viewport. Verify 390/768/1280/1440/2560.
   - Three-up single row on desktop; captions do not repeat CONCEPT RENDER (badge only). Body: "One hull, reconfigured by mission."
2. Leak scan: `N120` added (40 terms now). Word-bounded, fail-the-build, unchanged mechanics.
3. Staged alternate (unreferenced): `defense-morpheus-cargo-v1.png`.

**QA gate for this build:** ≥3 screenshots of the gallery (mobile/laptop/wide) + full leak scan + badge visibility check + vessel-not-cropped check on all 3 images.
