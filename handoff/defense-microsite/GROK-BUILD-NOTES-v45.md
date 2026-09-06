# /defense v4.5 + /invest v10.5 — Canon Sync Build Notes (2026-09-05)

Contract files are the source of truth; this note explains what changed and what to verify. Both contracts ship in one PR because the numbers must agree across routes on the same deploy.

## Why
The Defense Edition deck (`140eO2QPItJy78wtiODHT6wYhkd8YEXU5BCoGey2y2fU`) went through a primary-source verification pass and a founder review. Several figures it corrected were still live on /defense, /invest and the Series B re-spine deck. Jaideep approved the cascade (decisions D1–D7) on 2026-09-05.

## /defense — `deck-studio/microsite/contracts/defense.json` v4.4 → v4.5
| Section | Change | Verify in build |
|---|---|---|
| `def-hero` | headline **OWN THE LITTORAL** (was OWN THE EDGE) — bookends `def-close` | Hero and close carry the same mark |
| `def-navier` | Beat 2 body no longer opens with "We do not build defense-specific vessels." Beats 3–5 **moved** to `def-amc` | Only two beats render beside the film |
| `def-plainview` | **220 ft** · 310 tons · 40 kn (NHHC DANFS). "268 foilborne hours" dropped. New `source_line` | Source line renders under the blocks |
| `def-autonomy` | Body: "each one demonstrated on the water." Rung 4: "on-water N30 trials — **Q4 2026, first milestone filmed by December**"; "every trial adds to the autonomy record." | No "September 2026", no "before the loop is closed" |
| `def-quanta-stats` | **2,400 NMI** | — |
| `def-quanta-unlocks` | Atlantic band: "Unmanned crossing — **on the autonomy roadmap** · Newfoundland → Lisbon." Map plate unchanged | No date on the band |
| `def-dual-use` | deployment line: "**Leidos — a Navier customer**" (Sampriti-cleared wording; never the project or contract value) | — |
| `def-field` | Quanta 2,400 NMi / **2,200 lbs**; Corsair **35+ kts (top)**; GARC range **Not published**, **Up to 40 kts**. New `sources_line` | Table renders 10 rows, no clipping at 1280 |
| **`def-amc` (NEW)** | Gap → Answer finale between `def-team` and `def-close`. See render notes in the contract. | See below |
| `def-team` | No longer the closing beat | — |

### `def-amc` render spec (type `gap-answer`)
- Two panels, hairline vertical divider. **LEFT — THE GAP:** "1,700+ / CHINA" over a **native DOM or SVG pictogram grid of 340 gold squares (10 rows, each square = 5 vessels)**; "< 5 / UNITED STATES" over **one hollow white square**. Captions one line each. Source line. **No PNG chart.**
- **RIGHT — THE ANSWER:** gold kicker → headline *Out-innovate, don't outnumber.* (18–20px bold) → subhead → numbered gold rail **01–04**, caps head + one body line (≤2 lines at 1280). No card boxes.
- Reference render: Defense Edition slide 27 (Jaideep-approved 2026-09-05). Text never on photo; dark field; Playfair title; gold kickers.

### Gates (unchanged, must pass)
- 14-term leak scan on rendered text = 0 hits. Term list untouched.
- FILMED / SIMULATION badges intact on all four autonomy loops.
- Screenshot pass 1280 / 1440 / 2560; no clipping, no ellipsis.
- **Still open from v4.4:** `/defense` assets are reachable without a gate code — fix in this build if not already done.

## /invest — `handoff/invest-microsite/contracts/*.json` v10.4 → v10.5
| File | Change |
|---|---|
| `gtm.json` | TAM defense row: "**$6.5B+ named U.S. program plans: 83 MUSVs ($3.1B, FY27–31) · ~$3.5B boat MAC**" (was $8B+ · 2,799-boat MAC · $4.4B FYDP). Landing-craft closing line: "Sovereign demand for the 45–180 ft classes has already arrived." Deployment line: Leidos — a Navier customer |
| `ladder.json` | Quanta chip **2,400 NMi**; "unmanned Atlantic run — on the autonomy roadmap" |
| `product.json` | 2,400 NMi stat + label; Atlantic band undated; competitive table (2,400 / 2,200 lbs / Corsair 35+ kts top / GARC not published · up to 40 kts); autonomy Q4 2026 wording |
| `money.json` | Roadmap: H2 2026 "Autonomy on-water trials (N30) — toward the unmanned Atlantic run"; H2 2027 "U.S. shipyard sited — stand-up begins"; **2028 "U.S. shipyard online → ramp toward 100 Quanta/yr"** added. **The Round → OKR v4:** headline "$10M Series B-1 → Series B-2 in Q1 2027"; B-1 card $10M · closing September 2026 with the five B-1 objectives; B-2 card "Q1 2027 · sized in December" with the five B-2 objectives — **no B-2 dollar total**, only the ~$45M gross shipyard line. Closing line "$10M first close funds the first phase of the network." Quanta status 2,400 NMi |
| `site.json` | version v10.5 + notes |

- **OWN THE EDGE stays** as the /invest hero and closing mark (investor mark; only /defense bookends on LITTORAL).
- `/teaser` inherits all of the above; energy remains held from /teaser (unchanged).
- The `invest.js` heading regex (`$NM SERIES B-1`) still matches the new B-1 title; B-2 title intentionally has no dollar figure.

## Not in this PR (deliberate)
Programs & Fit table · MENA theater line items · anything LC · seven-act deck tags · MASC (no other surface names it) · Replicator windows (both sourced, both labelled).
