# NYC EDC / PANYNJ Authority Deck — QA Record

Deck: `1YmUQ-dx4p4wZ_Ftd8m4xn46Q7ViXXw1eNv3-2j5F-8w` (20 slides, Authority Format v2, WETA chassis)

## QA rounds

- **R1 (edc-qa1.pdf)** — post text-relocalization. All 20 slides reviewed. Singapore leak on S12 patched (`fix1.ts`). Image gaps identified → IMAGE-SWAP-PLAN.md.
- **R2 (edc-qa2.pdf)** — post first image bind (8 slots). Findings: S9/S10 page-background fills wrong treatment (original design = solid dark navy bg + right-side photo element); S11 candidate map routes rendered too small (loose bbox).
- **R3 (edc-qa3.pdf)** — after S9/S10 background revert to sampled original navy + photo-element-only swap, and S11 rebind to v2 tight-bbox map plate (commit 2300…). **All 20 slides reviewed, all clean. Final.**

## Fix log

1. S12 Singapore string leak — patched via element-scoped text replace.
2. Rockaway route straight-line coords → real Jamaica Bay channel waypoints (`patch_nyc_ferry_waypoints_2026_07_29.py`, recorded in hand-waypoints convention).
3. Horizon insets re-rendered water-clean (today/tomorrow).
4. S9/S10: full-bleed page fill reverted to original solid dark navy (color sampled from R1 PDF, exact match); photo swapped as right-side image element only.
5. S11: candidate-links map re-rendered with tightened pad/clearance (v2 renderer) so the three authority corridors fill the frame.

## Bind state

All image slots live-verified against deck `1YmUQ-dx4p4wZ_Ftd8m4xn46Q7ViXXw1eNv3-2j5F-8w`; `used_by` written back in `image-manifest.json` (sealed).

Image hosting: raw.githubusercontent.com stable URLs, branch `authority/nyc-edc-2026-07-29`.
