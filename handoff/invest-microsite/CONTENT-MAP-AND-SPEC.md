# Series B Investor Microsite — Content Map & Build Spec

**Version:** v1.1 · 2026-08-16 · decisions locked (see §10) — cleared for contract authoring + Grok handoff
**Source of truth:** Series B Presentation Cut (`1RuRlgsD3L63T-0IfQkc35UL9_Cv6VqDWSkDU3t3QObA`, 53 slides — 36 main + 17 appendix)
**Companion files:** `CUT-SLIDE-INVENTORY.md` (verbatim slide text) · `VIDEO-INVENTORY.md` (verified video metadata)

---

## 1 · Purpose & principles

- The microsite is the **self-serve third surface**: master = reading deck, Cut = live presentation, microsite = what an investor opens between meetings and forwards internally.
- **Same locked spine, native web grammar.** Claim → Proof → Product → GTM → Money. Numbers canon-identical to the Cut. Presentation changes; content does not fork.
- **Video carries Proof.** The deck asserts "foilborne to Sea State 4"; the site *shows* it. Demo footage is the single biggest advantage over the PDF.
- **Interactivity budget: 3 moments.** Vessel ladder explorer · corridor/network map · unit-economics toggle. Everything else is restrained motion-on-scroll. SpaceX-IPO restraint; text never sits on photo/video.
- **Disclosure ≥ deck.** A URL travels further than a DocSend. Full kill-scan, plus deltas listed in §7.

---

## 2 · Site architecture

Single scrollytelling page, sticky chapter nav (six chapters), progress indicator, ~8–10 min full read. Dark field with white space discipline; gold accents per brand system.

```
HERO  →  01 CLAIM  →  02 PROOF  →  03 PRODUCT  →  04 GTM  →  05 MONEY  →  GO DEEPER (footer)
```

| Chapter | Cut slides | Weight |
|---|---|---|
| Hero | 1 | Full-bleed video, one line |
| 01 · The Claim | 2–8 | ~15% |
| 02 · The Proof | 9–10 + demo video grid | ~20% — the emotional core |
| 03 · The Product | 11–17 | ~20% |
| 04 · Go-to-Market | 18–31 | ~30% |
| 05 · The Money | 32–36 | ~10% — quiet, mostly static |
| Go deeper | footer | Vance film · data-room CTA · contact |

Appendix slides (37–53) do **not** render on the site. They stay in the data room. Two exceptions folded in below (s42 master plan optionally feeds the arc animation copy; s51 "tried before" is a strong candidate for a collapsed "History" accordion in ch. 03 — flagged as an option, default off).

---

## 3 · Slide-by-slide content map

Treatment legend: **KEEP** = content rendered as authored section · **MERGE** = combined with adjacent slide(s) · **INTERACTIVE** = feeds an interactive component · **VIDEO** = replaced/augmented by footage · **GATE** = renders only behind email gate · **OMIT** = data room only.

### Hero

| Slide | Content | Treatment |
|---|---|---|
| 1 | OWN THE EDGE | **VIDEO** — full-bleed muted loop of hero film (V1), headline "OWN THE EDGE", subline = core thesis (s2). Sound-on play button opens V1 in lightbox with narration. |

### 01 · The Claim (s2–8)

| Slide | Content | Treatment |
|---|---|---|
| 2 | Core thesis | **MERGE** into hero subline + chapter opener. |
| 3 | About Navier — American maritime company, 5× less energy | **KEEP** — chapter opener text block. |
| 4 | The Network Shift (few giant ships → thousands of fast ones; internet analogy) | **KEEP** — two-panel scroll transition: "Shipping today" dissolves into "The Navier network." The one *animated diagram* of the chapter. |
| 5 | The arc — Prove flight → … → Own the nodes | **KEEP + motion** — the six pills light sequentially on scroll; "NOW" marker on pill 3. Copy verbatim from slide. |
| 6 | Team + backers | **KEEP** — compact portrait row + backer line. No motion. |
| 7 | Three costs kept maritime stuck | **MERGE** with 8 — |
| 8 | Three levers collapse them | — single "3 costs → 3 levers" flip section; cost cards flip to lever cards on scroll. Ends on "Speed & cost — no longer a trade-off." |

### 02 · The Proof (s9–10 + footage)

| Slide | Content | Treatment |
|---|---|---|
| 9 | N30 Pioneer delivered — 10,000+ hrs, 10 live, 70 NM, 90% less energy | **KEEP + counters** — four stats animate up on entry. Backdrop: still or short loop of N30 foilborne. |
| — | *(not in deck)* | **VIDEO — demo grid.** "Don't take our word for it" — 4–5 short clips as native muted loops, click for sound: V4a no-wake · V4b flat turning · V4c stabilization juxtaposition (uploaded clip) · V4d above rough seas · V4e 0-to-foiling in 18 s. Each with a one-line physics caption. |
| 10 | Traction timeline 2022→2026 + $10M rev on $33M raised | **KEEP** — horizontal scroll-driven timeline; the three stat chips (10,000+ hrs · 10 vessels · $100M contract) persist as sticky chips through the chapter. |

### 03 · The Product (s11–17)

| Slide | Content | Treatment |
|---|---|---|
| 11 | Control is the hardest tech — NavierOS anatomy | **KEEP + VIDEO** — annotated vessel diagram (hotspots on foils/OS/powertrain); CTO film (V3) embedded beside as "the 3-minute version from our CTO." |
| 12 | GMVP — skateboard/brain/mission layer | **MERGE** with 13 — GMVP intro paragraph becomes the setup text for the ladder. |
| 13 | GMVP ladder — N30 → Quanta LR → N45 → N80 → N180 | **INTERACTIVE #1 — Vessel Ladder Explorer.** Horizontal hull selector; per hull: silhouette-to-scale, class, mission, status chip (proven / sea trials / first hull target / design). Data authored, canon-identical. |
| 14 | Quanta video interstitial | **VIDEO** — chapter-break plate: "NEXT PRODUCT: QUANTA," Sampriti film (V2) as the featured embed. |
| 15 | Quanta first look — ~2,000 NMi · 35 kts dash · hybrid · trans-ocean | **KEEP** — four stat chips. ⚠ "FIRST LOOK · NOT YET PUBLIC" label — see §7 D1. |
| 16 | What Quanta unlocks — defense + every long corridor + Atlantic run | **KEEP** — two-door layout (defense / commercial), Atlantic run as a drawn route line Newfoundland→Lisbon. |
| 17 | Competitive: Saronic/Saildrone/BlackSea vs Quanta | **KEEP** — comparison table, render as authored; row-reveal on scroll. |

### 04 · Go-to-Market (s18–31)

| Slide | Content | Treatment |
|---|---|---|
| 18 | Maldives — 100 vessels · $100M signed · press | **KEEP** — signed-contract hero: big 100 / $100M, press quotes as a quiet marquee. |
| 19 | The Gulf — anonymized royal-office program, 6 buyers | **KEEP, GATE-candidate** — already anonymized in deck; see §7 D2 for whether it sits open or gated. |
| 20 | Three revenue lines | **KEEP** — three stacked cards; formula line rendered as the section's close. |
| 21 | Unit economics Maldives — N30/Targa, N45/Princess | **INTERACTIVE #3 — Unit-Econ Toggle.** Class switch (30-ft / 45-ft): three cost lines morph between electric and diesel; the 7×/13× multiple is the punchline. All figures verbatim from s21. |
| 22 | Coastal-Network Model — four roles, everyone earns | **KEEP** — four-role diagram, static. This is the business-model keystone; no gimmicks. |
| 23 | Cargo — the 14× air/ocean gap | **KEEP + motion** — the gap chart draws itself: air line, ocean line, Navier band lands between. |
| 24 | Islands pay the most | **MERGE** into 23 as supporting stat band (2× · $5,563/TEU · 29 of 50). |
| 25 | The play: dedicated foiling freighters | **KEEP** — three-chip section (network-ready / two modes / any shore). |
| 26 | Ship scale pulled forward — 180 ft sealift, sovereign discussions | **KEEP, GATE-candidate** — anonymized already; same call as s19 (§7 D2). |
| 27 | The wedge: people by day, cargo by night | **KEEP** — day/night visual flip (same vessel, lighting change). |
| 28 | Offshore service fleets | **KEEP** — single card row; CTV hero art. |
| 29 | Dual-use platform — commercial first, defense on top | **KEEP** — USMI quote as pull-quote; budget line as fine print. |
| 30 | Market — conservative floor bottoms-up ($16–31B floor, $1.1T ceiling) | **KEEP** — the six-segment table renders as horizontal bars (vessels · $ floor); ceiling stated once, floor is the story. |
| 31 | Pipeline — signed and in motion | **INTERACTIVE #2 — Network/Pipeline Map.** World map (Atlas-derived corridor/city data — 672 corridors · 385 cities · 79 countries) with the four gold stats (s31 band) and tiered pipeline list. Named rows stay exactly as deck-anonymized ("Gulf nation royal office," "Turkish mobility platform"). |

### 05 · The Money (s32–36)

| Slide | Content | Treatment |
|---|---|---|
| 32 | Operating plan conservative — $512M · 567 vessels FY30E | **KEEP** — quiet stat band. No animation. |
| 33 | Next 12–18 months roadmap | **KEEP** — four-column roadmap, static. "Every milestone is funded by this round." |
| 34 | One platform · five markets · thesis restated | **KEEP** — five status rows; closing line verbatim. |
| 35 | Final plate — every coastline a network | **MERGE** into site finale (below s36). |
| 36 | THE ROUND — $10M B-1 first close of $100–150M+ | **GATE (recommended)** — renders after email gate; see §6/§7 D3. Followed by data-room CTA + contact. |

### Appendix (s37–53)

**OMIT** from site (data room only): 37–53 — including operating upside (39), premium-market N30 P&L (43), night-cargo economics (44), hydrofoil field (45), $1.1T breakdown (46), production (47–48), TRL (49), defense validation (50), prior attempts (51), full unit-econ (52). *Option (default off):* s51 as collapsed "It's been tried before" accordion in ch. 03.

---

## 4 · Video plan

All 8 YouTube videos verified **public + embeddable** (see `VIDEO-INVENTORY.md`). Placement:

| ID | Video | Placement | Method |
|---|---|---|---|
| V1 | `aavaIZPkDyk` — hero/narrator film | Hero | Muted background loop (self-hosted excerpt) + sound-on lightbox (YouTube) |
| V2 | `QhiaYVgXMf0` — Sampriti: Quanta + US resilience | Ch. 03, Quanta interstitial (s14 slot) | YouTube embed (nocookie), click-to-play with poster frame |
| V3 | `S7WB91FvSFI` — CTO: hydrofoiling + software-defined vessels | Ch. 03, technology section (s11) | Same |
| V4a | `Hlp9oynUQNE` — no wake vs regular boat | Ch. 02 demo grid | Native muted mp4 loop (needs source file) |
| V4b | `93MCRJYsD_8` — smooth turning | Ch. 02 demo grid | Same |
| V4c | Uploaded clip (18.6 s, 720p) — stabilization vs chase boat | Ch. 02 demo grid | Self-hosted mp4 — already in hand; 720p acceptable for a loop card, not hero |
| V4d | `7HETK4rsByc` — above rough seas | Ch. 02 demo grid | Native loop (needs source file) |
| V4e | `htUWE3AJUbc` — 0→foiling in 18 s (Four Seasons) | Ch. 02 demo grid *or* ch. 04 Maldives section | Native loop (needs source file) |
| V5 | `ZNgh39DM_Jg` — Ashlee Vance long-form | Footer "Go deeper" | YouTube embed with duration label |

**Asset request (critical path):** source mp4s for V1 (or a 10–20 s hero excerpt) and V4a/b/d/e from Sampriti/Kenneth. YouTube embeds cannot autoplay-loop cleanly in a grid; native muted loops are the difference between "website with videos" and "immersive." Fallback if sources unavailable: click-to-play YouTube lightboxes with strong poster frames (site still works, loses ~30% of the effect).

**Prarit CGI** (world-scale network hero, pending): reserved slot = site finale behind "Every coastline a network — OWN THE EDGE." Ship without it; upgrade when it lands.

---

## 5 · Interactive moments (hard cap: 3)

1. **Vessel Ladder Explorer** (ch. 03) — hull selector, canon specs only. Data file: `ladder.json`.
2. **Network/Pipeline Map** (ch. 04) — world map from Atlas corridor/city data + pipeline tiers. Real geometry, no invented dots. Data file: `pipeline-map.json`.
3. **Unit-Econ Toggle** (ch. 04) — 30-ft/45-ft class switch on the s21 table. Data file: `unitecon.json`.

Everything else: scroll-triggered reveals, counters, and one drawing chart (cargo gap). No parallax excess, no cursor effects, no autoplaying sound ever.

---

## 6 · Access, analytics, deployment

**Recommended access model — two-layer:**
- **Layer 1 (Acts Hero–04):** unlisted URL, `noindex,nofollow`, no gate. Zero friction for a partner forwarding to their Monday meeting.
- **Layer 2 (Act 05 Money + data-room CTA):** lightweight email gate (name + firm + email, no verification loop). Gating the *ask* rather than the *story* keeps virality where we want it and gives us a signal exactly at the moment of intent.
- No password unless Jim/Joseline require it; if they do, gate moves to the whole site.

**Analytics (decide before build, not after):**
- Per-chapter scroll depth, section dwell, video play/complete events, ladder/map/toggle interactions, gate conversions — funnel: land → reach Proof → play a demo → reach Money → gate → data-room click.
- Tool: PostHog (self-serve, EU/US hosting, session replays off by default) or Plausible (lighter, no per-user). Recommend **PostHog with anonymized IPs**; per-viewer identity only post-gate.
- This is *better* intelligence than DocSend page-time.

**Deployment:**
- Build lives in `navier-atlas` repo (same stack/discipline as archetype microsites) **but must not sit behind the repo's production Basic Auth**. Options: separate Vercel project from the same repo (recommended), or auth-exempt route. Domain: `invest.navierboat.com` or similar — Jaideep to pick; must be a Navier-controlled domain, not a vercel.app URL, for investor trust.
- OG/social card: dark plate, "Navier — Series B" only. No numbers in the OG image (it renders in chat apps regardless of gate).

---

## 7 · Disclosure — deltas vs the deck (kill-scan additions)

Standard kill-scan applies (no valuations, no lead, no LC-180 name/counterparty/specs beyond the anonymized s26 content, no royal-office identity, no Sergey Brin, Quanta ~2,000 NMi canon, no internal vocabulary). URL-specific deltas needing decisions:

- **D1 — "NOT YET PUBLIC" tension (s15).** The deck labels Quanta "first look · not yet public," but V2 (Sampriti on Quanta) and press coverage are public YouTube. Recommend the site drops the "not yet public" chip and keeps "in sea trials — unmanned ocean crossing targeted late 2026." Keeping a "not yet public" label on a website is self-contradicting. **Jaideep call.**
- **D2 — Gulf sections (s19, s26) open vs gated.** Both are already anonymized. Options: (a) render open as-is; (b) move behind the Layer-2 gate with Money. Recommend **(b)** — cheap insurance, and the Gulf story lands better after Maldives-signed anyway. **Jaideep call (+ Jim/Joseline view).**
- **D3 — The Round (s36) on-site vs data-room-only.** Recommend on-site behind gate: the $10M B-1 / $100–150M structure is already our standard written disclosure. **Jaideep call.**
- **D4 — Stripe mention (s10 timeline).** "Stripe commuter pilot" is named in the deck timeline; case-study permission is an open item. Site renders the timeline **without the Stripe name** ("Bay Area commuter pilot") until permission confirmed. Default applied unless overridden.
- **D5 — Named backers/customers (s6 backers, USMI/Leidos s29).** All already in the deck and publicly attributable; keep. Leidos wording stays exactly as deck.

---

## 8 · Build plan & QA gates

1. **Content contract first.** Authored JSON per chapter (`hero.json`, `claim.json`, `proof.json`, `product.json`, `gtm.json`, `money.json` + 3 interactive data files). Every renderable string authored here, canon-derived from the Cut. Renderer renders authored data only — no generated copy. `_internal` provenance fields per archetype-v3 pattern.
2. **Grok handoff.** Spec + contract + asset manifest → Grok builds the route in `navier-atlas` (separate Vercel project). Same PR discipline as archetype microsites.
3. **QA gates (all mandatory before any investor sees it):**
   - Side-by-side vs the Cut, slide-by-slide — every number identical.
   - Kill-scan (§7) on rendered HTML, not just source.
   - Banned-terms scan (boats/fleets → vessels/platforms; N120; 2,400 NMi; $600B headline; etc.).
   - Legibility pass — no text on photo/video, contrast, mobile at 375 px.
   - Video weight budget — hero loop ≤ 8 MB, grid loops ≤ 4 MB each, lazy-loaded; Lighthouse perf ≥ 85 mobile.
   - Gate + analytics event test end-to-end.
4. **Freshness rule.** The Cut remains canonical; any Cut edit triggers a microsite content-contract diff (same cascade discipline as partner decks).

---

## 9 · Open decisions for Jaideep

| # | Decision | Recommendation |
|---|---|---|
| 1 | Access model | Two-layer: story open (unlisted+noindex), Money + Gulf behind light email gate |
| 2 | D1 — Quanta "not yet public" chip | Drop chip on site; keep "in sea trials" |
| 3 | D2 — Gulf sections open or gated | Gated (Layer 2) |
| 4 | D3 — The Round on-site | Yes, behind gate |
| 5 | Domain | `invest.navierboat.com` (or Jaideep's pick) — needs DNS |
| 6 | Analytics tool | PostHog, anonymized pre-gate |
| 7 | Source mp4s | Request from Sampriti/Kenneth: hero excerpt + 4 demo clips |
| 8 | s51 "tried before" accordion in ch. 03 | Default off — data room |
| 9 | Stripe name in timeline | Removed pending permission (default applied) |

---

## 10 · Decisions locked (Jaideep, 2026-08-16 22:44 PT)

1. **Access:** unlisted + noindex approved. With Gulf (D2) and the Round (D3) both ruled **open**, the Layer-2 email gate has no content — **v1 ships with no gate**. Gate can be reintroduced later without redesign.
2. **D1:** Quanta "NOT YET PUBLIC" chip dropped on site; "in sea trials — unmanned ocean crossing targeted late 2026" stays.
3. **D2:** Gulf sections (s19, s26) render **open**, exactly as deck-anonymized.
4. **D3:** The Round (s36) renders **open** on-site.
5. **Deployment:** `navier-atlas` repo, route **`/invest`**, existing Vercel demo (`navier-atlas.vercel.app/invest`). Custom domain deferred. NOTE: production has had HTTP Basic Auth — Jaideep to confirm `/invest` is reachable or auth-exempted before sharing.
6. **Analytics:** none in v1 (PostHog skipped). Design must not preclude adding events later.
7. **Video:** YouTube embeds (nocookie, click-to-play, poster frames) for all 8 in v1; native mp4 loops swap in when Jaideep supplies source files. Uploaded stabilization clip (V4c) self-hosted from day 1 — the one native loop in v1.
8. **Appendix:** everything after slide 36 excluded entirely, including the s51 accordion option. Site = main slides 1–36 only.
9. **Stripe:** named on the timeline — publicly announced (Bloomberg, TechCrunch).
