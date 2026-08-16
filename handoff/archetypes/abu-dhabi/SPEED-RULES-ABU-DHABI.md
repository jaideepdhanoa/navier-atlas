# SPEED-RULES-ABU-DHABI (internal audit file — never renders)

**As of:** 2026-08-16 · All sources accessed 2026-08-16.
**Primary basis: STRONG (better than Dubai).** Abu Dhabi Maritime publishes bilingual waterway **safety maps with zoned, numeric speed limits** and a codified set of General Speed Limit Rules. Base schedule math in REVENUE-STACK-ABU-DHABI.md respects these posted limits.

## 1 · Who sets and enforces

- **Rules:** DMT's *Regulatory Bylaw for Maritime Safety in the Waterways of the Emirate of Abu Dhabi* (announced 11 Jul 2025; Administrative Decision No. (69) of 2025 per Abu Dhabi Maritime tariff schedule §2.2.10) — licensing, conduct, environmental obligations, penalties for "non-compliance with navigation rules." Source: https://admobility.gov.ae/en/news/comprehensive-maritime-safety-regulations-to-safeguard-waterways-and-support-sustainable-growth
- **Implementation/enforcement:** Abu Dhabi Maritime with the Integrated Transport Centre (same source). Safety maps state the zoned limits "must be adhered to." Source: https://www.admaritime.ae/safety-maps/

## 2 · General Speed Limit Rules (PRIMARY — quoted from the published safety map document)

Source PDF: https://www.admaritime.ae/wp-content/uploads/2025/12/abu-dhabi-maritime-safety-maps-general-updated.pdf — "Where the speed is not otherwise restricted, following General Speed Limits Rules shall apply:"

| # | Rule | Limit |
|---|---|---|
| 1 | **No-wake zones** — within 50 m of shore, piers, pontoons, slipways, marinas, any marine facility | **Max 5 kn** |
| 2 | Passing under a bridge arch | **Max 8 kn** |
| 3 | **In channels** | **Max 20 kn** (unless authorized by marine event permit) |
| 4 | **Open waters** | **Max 50 kn** (unless authorized by marine event permit) |
| 5 | **At night (sunset to sunrise), all waters** | **Max 20 kn** |
| 6 | Within 50 m of any other vessel | Max 15 kn |
| 7 | Passing a diving operation | ≥100 m distance, 5 kn |

Plus a codified due-care rule: unlawful to operate "at any rate of speed greater than the legally permitted or… greater than that which will permit… the vessel to come to a stop within the assured clear distance ahead."

**Zoned limits on the maps:** the safety maps mark discrete speed-limit zones at **5 / 8 / 12 / 15 / 40 kn** across specific water areas, and **Marine Protected Area core zones: innocent passage at max 10 kn**.

## 3 · What this means on our corridors

| Segment type | Basis used in schedule math | Note |
|---|---|---|
| Marina basins & first/last 50 m at every landing | 5 kn | Rule 1, primary |
| Bridge arches (e.g., approaches around Maqta/inter-island bridges if routed) | 8 kn | Rule 2, primary |
| Marked channels (Zayed Port approach, inter-island channels) | 20 kn | Rule 3, primary |
| Open water (Saadiyat/Yas outer runs) | **25 kn N45 service speed** (canon) — well inside the 50 kn open-water limit | vessel-capability bound, not rule bound |
| **Evening service after sunset** | **20 kn cap on all waters** | Rule 5 — matters for a 16-hr day; evening legs re-timed at 20 kn (≈+2–4 min on the spine; see stack §2) |
| MPA core zones | 10 kn innocent passage; avoid scheduling through core zones | map legend, primary |

## 4 · Mangrove waters (Eastern Mangroves / Jubail)

- The mangrove channels sit inside the Mangrove National Park, managed by **EAD**; kayak/eco-tour operations dominate access. Source: https://www.ead.gov.ae/en/Experience-Green-Abu-Dhabi/Places-To-Go/Mangrove-National-Park
- **Numeric mangrove-channel zone tier: NOT READ at print resolution** — the city-inset zone colors (5/8/12/15 kn tiers) could not be geographically bound to the Eastern Mangroves channel from the downloaded map this run. **Conservative planning basis: 8 kn in mangrove channels, 5 kn within 50 m of any facility/shore** (the no-wake rule applies by its own terms along fringing shorelines). Flag for re-verification against the high-resolution map sheet.
- Purpose of the rules (stated): the bylaw "places a special emphasis on marine environmental protection… preventing pollution and preserving Abu Dhabi's rich natural heritage" (DMT announcement, §1 source).

## 5 · What relief unlocks (framing only — never a schedule assumption)

The stated purpose of mangrove and no-wake restrictions is wake damage, noise and wildlife protection. A foiling vessel at speed produces near-zero wake and near-silent electric operation — i.e., it serves the rule's own purpose better than displacement craft at the same speed. Where EAD/Abu Dhabi Maritime were ever to grant purpose-based relief in protected or no-wake waters, mangrove and inner-corniche legs would compress materially. **All base math uses posted limits; relief appears only as this labeled sensitivity.**

## 6 · Confidence register

| Item | Status |
|---|---|
| General limits (5/8/20/50/20-night/15/dive) | PRIMARY — published safety-map document, quoted verbatim |
| Zone tiers 5/8/12/15/40 kn + MPA 10 kn | PRIMARY — map legend |
| Eastern Mangroves channel specific tier | NOT VERIFIED numerically — conservative 8 kn basis used, flagged |
| Enforcement authority | PRIMARY — DMT announcement (bylaw), Abu Dhabi Maritime + ITC implementing |
