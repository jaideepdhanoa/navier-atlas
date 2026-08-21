# /defense Microsite — Plan (v1, for Jaideep review before any build)

2026-08-21. No build until this plan is blessed. Route: `/defense` on navier-atlas, extending the /invest architecture (same renderer, same contracts pattern, new `defense.json`).

---

## 1. Who this is for, and what it is not

**Audience:** DoD program offices and PMs, DIU, SOCOM, service labs, primes, and defense-adjacent evaluators. People who think in missions, requirements, and readiness — not returns.

**Posture: capability brief, not a pitch.** This is the single biggest difference from /invest. Everything that frames Navier as an investment is *out*: the raise, financials, revenue plans, TAM dollar figures, pipeline ratios, capture scenarios, partnership/equity structures, "why now" market framing. A DoD reader who sees fundraising language discounts the capability claims. What replaces it: mission fit, demonstrated performance, program alignment, and the industrial-base argument.

**One-line proposition (already audited, gtm.json):** *"A standardized foiling platform changes how navies move."*

**The coherent story in one paragraph:** Navies need speed, range, sea-keeping, and low signature in the same hull — and have never been able to have all four. The physics of hydrofoils was proven by the U.S. Navy itself (USS Plainview, 1969); what was missing for fifty years was control. Navier built the control system, proved it on a commercial fleet with 10,000+ hours, and now fields Quanta-D: foilborne-stable in Sea State 4, electric-quiet, with the range to matter — manned or unmanned. Behind it sits a commercial production line, which means defense buys at commercial cost and commercial rate. That's the dual-use argument, and it's the same one Tesla/SpaceX made land: the commercial engine funds the defense capability, not the other way around.

## 2. Disclosure boundary — the kill list (fail closed)

Everything below is excluded, enforced by the jargon/leak scan at QA:

| # | Excluded | Why |
|---|---|---|
| 1 | LC-180 — name, specs, costs, counterparty, existence | Permanent firewall |
| 2 | Gulf counterparties, royal office, H.H./LOI material | Anonymization rule; "Gulf naval evaluation Q3 2026" (already-audited phrase) is the ceiling |
| 3 | Effector/payload partner name — copy, captions, alt text | Standing rule from defense panel |
| 4 | Raise, valuations, round terms, use of funds | Not investor material; standing memo rule anyway |
| 5 | Revenue/EBITDA/fleet plan, defense $ share, capture scenario bands | Internal planning; investor-surface only |
| 6 | TAM dollar figures ($8B+, $22–38B, vessel floors) | Investor framing; DoD readers know their own budgets |
| 7 | ASPs / pricing of any vessel | Never public |
| 8 | Pipeline tiers (T1–T4), signed-demand ratios, named commercial counterparties beyond audited copy | Internal |
| 9 | FOCI/clearance timeline | Internal planning lane |
| 10 | Commercial Quanta "in sea trials, unannounced" framing applies to the commercial variant — site leads with **Quanta-D**, which is public (SAS 2026 + SOF Week 2026) | Framing rule |
| 11 | Navier-voiced rank claims — "officers" only; the Defence Blog quote may say "admirals" because it is third-party, attributed, linked | Caption rule |
| 12 | Blanket "built in America" — identity is "an American maritime company"; photo-specific "Made in America" captions only where already approved | Manufacturing claim rule |
| 13 | Sergey Brin | Standing rule |
| 14 | Employer networks, partner programs, commercial GTM detail | Off-topic for this audience |

**Copy-sourcing rule for the whole site:** every sentence traces to an already-audited external surface — the gtm.json defense panel (round-7), P4 chapters 01–04, Cut s13–s16 (Quanta chapter + proof), or the /invest About/Thesis block. Zero net-new claims. Where a section needs connective tissue, it's written in plain English and runs through `audit_partner_copy.py` plus the standing jargon kill-scan.

## 3. Site spine (9 sections)

| § | Section | Content | Source (audited) | Media |
|---|---|---|---|---|
| 1 | **Hero** | Full-bleed `defense-sofweek-loop.mp4` (effector-equipped Quanta-D, foilborne). Title: *"A standardized foiling platform changes how navies move."* Kicker: NAVIER · DEFENSE | gtm.json thesis_line | defense-sofweek-loop.mp4 |
| 2 | **Navier in 60 seconds** | "An American maritime company." Approved thesis opening, compressed. Fleet of N30s in commercial service, 10,000+ hours; one control platform across hulls | /invest About/Thesis + P4 s3, s17 | traction-hangar-wide.jpg or n30-pioneer-at-sea.png |
| 3 | **The problem navies have** | Speed / range / sea-keeping / signature — pick-two-until-now framing. Plainview: *"the physics was proven in 1969 — what was missing was control"* | P4 s8–s10 + Plainview slide (P4 s20) | plainview archival + control-wireframe-clean.png |
| 4 | **The platform** | Control system anatomy — bow-left schematic, seven callouts (reuse /invest component). Foilborne Sea State 4 · electric-quiet · software-defined. NavierOS one line (UMAA-compliant phrasing only if already externally used — verify, else drop) | Cut s10/control section, Quanta four-pillar frame | control schematic + stabilization-juxtaposition.mp4 |
| 5 | **Quanta-D — ready now** | Unmanned: patrol · ISR · interceptor. Manned: combatant craft · special-ops · medevac. Publicly exhibited SAS 2026 + SOF Week 2026. Spec row TBD (see open Q4) | gtm.json blocks + P4 Quanta ch. | defense-sofweek-armed.jpg, quanta-defense-camo, cockpit + approach videos (click-to-play) |
| 6 | **Proof** | USMI pull-quote (first DoD work) · deployment line: *"Deployed with the US Navy · running in Leidos operations · Gulf naval evaluation Q3 2026"* · Defence Blog quote, attributed + linked · SAS officers photo | gtm.json panel verbatim + P4 s14/s15 | defense-sas-officers-looking.jpg, defense-sas-camo-foilborne.png |
| 7 | **The family — contested logistics** | Vessel ladder, defense lens: Quanta-D (ready now) → N45 (crew/patrol class) → N80 Valkyrie · N180 Morpheus (contested logistics, any-shore resupply, more completed missions per vessel-day). Wireframes, no pricing | gtm.json large-hulls block + P4 s12 | fleet-wireframe family, navy-foiler-night.png, n180-morpheus-hero.png |
| 8 | **The industrial base** | Dual-use argument: commercial volume → cost and rate for defense. *"Commercial infrastructure first. Defense on top."* Budget fine-print line (Replicator ≈$1B · Australia A$176M · US Navy FY26 $203M USV R&D — sourced Aug 2026, already audited) | gtm.json panel + P4 ch05 industrial-base framing | foundry-interior-flag.png |
| 9 | **Team & engagement** | Sampriti + CTO one-liners; **advisors LeClair + Cederholm with bio links** (strongest possible close for this audience). CTA: contact line, no calendly/no form | team contract (already carries advisors + bio_urls from PR #389) | headshots (already in repo) |

Deliberately **no** money chapter, no market chapter, no roadmap/milestones chapter (roadmap invites requirement conversations we should have in the room, not on a website).

## 4. Reuse economics

- **Renderer/components:** hero video, section kickers (`NAVIER · DEFENSE` taxonomy), photo-pair panel, pull-quote, capability rail chips, vessel-ladder tabs, team grid, password gate — all exist on /invest. Grok reuses; near-zero new component work.
- **Contracts:** one new `defense.json` + reuse of `claim.json` team section and `assets.json` entries. All defense media already committed to the repo.
- **Copy:** ~90% verbatim from audited surfaces; ~10% connective tissue → through the audit script.
- **Render rules that carry over:** no text on photos · no large wakes (foilborne = faint ripple) · bright imagery standard · clip/no-ellipsis scans at 1280/1440/2560 · US flag visibility (foundry-interior-flag.png satisfies naturally) · no reflow · all-caps kickers only.

## 5. Access model (recommendation + open question)

Recommend: **unlisted + noindex + password**, same pattern as /teaser. Suggested password: `plainview`. Rationale: everything on the site is publicly exhibited or third-party published, but gating (a) keeps it out of search and competitor monitoring, (b) signals seriousness, (c) lets us log who we've given it to. Alternative: fully open as a recruiting/credibility surface — Jaideep's call.

One extra: a one-line footer — *"Distribution limited. Not an offer of securities."* plus recommending **counsel glance at export-control posture** before wide circulation (imagery is all publicly exhibited, so expected answer is "fine," but effector-equipped vessel imagery deserves the 10-minute check).

## 6. Build path

1. Jaideep blesses plan + resolves open questions below.
2. Agent authors `contracts/defense.json` (all copy traced, kill-scan clean) + section map.
3. Grok handoff PR: route `/defense`, reuse components, ≥10 named screenshots, standard scan gates + defense-specific leak scan (LC-180, payload partner, Gulf names, $ figures).
4. Agent live-QA on deployed route; Jaideep merges.

## 7. Open questions — RESOLVED (Jaideep 2026-08-21)

1. Gate: password = **quanta** · noindex/unlisted. 2. Contact: **sampriti@navierboat.com**. 3. Field-for-contrast panel: **include, softened** (title drops "Quanta Doesn't"; table + "pick two, until now" closer; public sources Aug 2026). 4. Quanta-D specs: **full spec row** (verbatim from P4 p4_sas). 5. Plainview: **yes** — sourced `assets/deck/plainview-foilborne-1969.jpg` (U.S. Navy, public domain, foilborne shot, 2819×2231, Wikimedia Commons). 6. UMAA: **verification FAILED** — appears on no external surface → dropped; NavierOS retained (external on /invest product.json). 7. Atlantic run: **include** — `assets/deck/atlantic-run-map.png`.

## 8. Status

- 2026-08-21 (later): UMAA re-verified across Cut (55 slides) + master (53) + teaser (17) + P4 + all contracts — zero hits anywhere; never displayed externally → stays dropped. Launch film bound to def-about: self-hosted `assets/navier-launch-film-540p.mp4` (960×540, 1:34, audio intact), click-to-play WITH SOUND; YouTube embed (aavaIZPkDyk) remains /invest-hero-lightbox-only, never on /defense. Flag: source is 540p — swap if a true 1080p export surfaces.
- 2026-08-21: `contracts/defense.json` v1 authored — 12 sections, all copy traced to P4 (audited external) / gtm.json round-7 panel / invest About. Self-QA: leak scan (word-bounded, rendered text) CLEAN · jargon scan CLEAN · all 18 asset paths verified present. Awaiting Jaideep copy review → then Grok handoff PR.

## (superseded) Original open questions

1. **Gate:** password (`plainview`?) vs fully open?
2. **Contact:** sampriti@navierboat.com, or stand up defense@navierboat.com?
3. **Competitor trade-off content:** P4 s16 has the Saronic/Saildrone/GARC trade-off. Include a softened "field, for contrast" panel, or keep the site competitor-silent? (Lean: silent — let the room conversation do it.)
4. **Quanta-D spec disclosure:** which specs are releasable on a website — speed/sea-state/quiet, or full spec row? (Range is sensitive: ~2,000 NMi canon is tied to the *commercial* unannounced variant. Lean: qualitative pillars only, no numbers table.)
5. **Plainview archival image:** public-domain Navy photo exists; OK to source and add? (Only net-new asset needed.)
6. **NavierOS/UMAA line:** include only if that phrasing already appears on an external surface — verify or drop?
7. **Atlantic-run material:** P4 uses it for defense missions framing — include the map plate or hold?
