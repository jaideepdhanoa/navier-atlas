# R22 — Legibility + plain-English arc + chrome normalization
Trigger: Sampriti (via Jaideep, 2026-08-05 23:03): (a) text over heavy graphic backgrounds is hard to read — want white space / fewer photos / consistent colors, SpaceX roadshow deck as legibility reference; (b) ladder slide unclear — "Node" jargon; wants plain segment sequence: recreational → validate tech, mobility → build network, hybrid → extend range, then cargo, then defense; (c) claim + vision slides don't land; (d) new slides drifted off deck chrome (title style, trackers, footer, logo).

## Design rule (SpaceX-informed, applied to Navier dark system)
Text ALWAYS on solid dark field, never on photos. Photos confined to dedicated plates (right zone or cards). Every content slide carries standard chrome:
- Title: Exo 2 w600 17pt white, x=0.633" y=0.499", sentence case
- Tracker: right-aligned x=5.6" y=0.458" w=4.167" — number gold #C59D5F bold 8pt + " · CHAPTER" gray #9EA3AD
- Footer: "© 2026 -  Navier - Private & Confidential" Exo 2 5pt, x=0.216" y=5.392"
- AV logo: x=9.479" y=5.226" w=0.384" h=0.242"
- Background: exact bg image reused from slide 16 (g3f645480738_0_197), sent to back

## Slide work
| # | id | action |
|---|---|---|
| 2 | st_r19_claim | REWRITE+REBUILD split layout. Kill packet-switching/node/N-of-1 jargon. Plain claim: water = last transport network left to build. Photo → right plate. |
| 3 | st_r19_vision | REBUILD split. Plain vision copy. Photo → right plate. +footer/logo |
| 4 | st_r19_ladder | FULL REBUILD as 5 segment cards (slide-16 card pattern): 1 Recreational—validate tech (N30 Pioneer, in service) · 2 Mobility—build network (Maldives $100M) · 3 Long Range—hybrid Quanta ~2,000 NMi (sea trials) · 4 Cargo—night shift (2027) · 5 Defense—strategic missions (core, long-term). Kick: every stage funds the next; first two earning. No "node/full layer/monolith". |
| 5 | sb_c3_grave | RESKIN clean: standard bg, two fact panels + gold inversion panel. Chrome. |
| 24 | sb_c1_gap | RESKIN: standard bg, keep AIR/GAP content panels. Tracker: THE SECOND ACT — CARGO. |
| 25 | g3f6623c186e_4_78 | REBUILD split: title/copy left on solid, day-night photo right plate ("Concept render" tag). |
| 26 | sb_c5_prize | RESKIN: standard bg, 3 stat cards + kick. No photo. |
| 30 | r21_wiw | Chrome + title restyle to standard (collage stays). Tracker 05. |
| 31 | st_r19_ask | Chrome (tracker 05, footer, logo). |
| 33–40 | appendix | Trackers → "APPENDIX" (add 34/35/39/40, replace stale 36), logos on 29/30/33/37/38, footers on 34/40. |

## Assets (push to deck-studio/assets/seriesb/r22/, SHA-pinned raw URLs)
- s2-plate.jpg — crop of s2-missing-layer-v1.png (right, ~square)
- s3-plate.jpg — crop of vision-hero-v1.png
- c2-plate.jpg — daynight-v1.png plate
Bg image + AV logo: fetch fresh contentUrls from slide 16 at runtime and re-insert.

## Verify
Full PDF export → per-slide zoom on 2,3,4,5,24,25,26,30,31,34,40 + contact sheet. Then push scripts/log/slide-map, update SLIDE-MAP-R21 → R22 notes.
