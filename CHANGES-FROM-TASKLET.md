# Changes from Tasklet — pitch layer + route-label + Quanta-LR curation

_Last updated 2026-05-30 (overnight session)._

---

## 2026-06-30 — PTA category replication: Qatar MOT + Singapore MPA

Rolled the Bahrain MOTC gold pattern through **Qatar MOT** and **Singapore MPA** with full depth.

**Both pages had the same contamination Bahrain did — caught and removed:**
- **Qatar:** display read "Qatar Tourism"; journeys were pasted-in UAE/RAK corridors (Yas Marina, La Mer
  Dubai, Fujairah↔Khorfakkan, Arabic RAK fishing ports); `{home}`/"inter-emirate" token leaks; full
  super-app GMV ladder; internal-jargon KPIs.
- **Singapore MPA:** journeys/KPIs were Grab/Indonesia (Bali↔Lombok↔Komodo, "Every coastal Grab market",
  MAPALLA); `_economics_authored_for: "grab"`; `{home}`/"inter-emirate" leaks; super-app ladder.

**Rewritten to the PTA pattern (sourced, domestic-first, jargon-free):**
- **Qatar** grounded in the Ministry's real Water Taxi project — Lusail/Pearl/Corniche terminals completed
  Nov 2024 with electric-charging pontoons; the published Al Wakrah→Al Khor network (8 stations, 3 lines);
  the new Qatar–Bahrain ferry (Nov 2025); 25%-by-2030 GHG target. Domestic Doha-Bay + east-coast spine;
  cross-Gulf link to Bahrain is optional Phase 3.
- **Singapore MPA** grounded in the real clean-harbour-craft mandate — all new craft electric/B100/net-zero
  from 2030, net-zero harbour craft 2050; live e-HC charging pilot at Marina South Pier; live Southern-Islands
  & Pulau Ubin ferries; Causeway ~350k crossings/day. Domestic harbour + islands spine; Batam/Bintan/Johor
  relief corridors optional Phase 3. MPA's genuine "prove first-of-class, export the standard" angle kept.
- Economics reshaped to the **PTA public-value convention** (plain rungs; super-app GMV rung dropped;
  `public_value` levers added; numbers flagged for Grok regen from the clean domestic networks).
- All `route_id`s null + `_link_status: "pending-seal"` (honest intentional-null). City IDs with no registry
  entry (`al-khor-qatar`, `batam-indonesia`, `bintan-indonesia`) kept in labels/narrative only and flagged
  for Grok to mint — not listed in `cities` arrays.

**Grok handoffs (mint + route, zero land crossings):**
`GROK-SPEC-qatar-domestic-routing-2026-06-30.md`, `GROK-SPEC-singapore-mpa-domestic-routing-2026-06-30.md`,
backed by `PTA-DOSSIER-qatar.json` and `PTA-DOSSIER-singapore-mpa.json` (anchors + hazards: Pearl/Lusail
reclamation, HIA land, Doha reef flats; Singapore TSS/anchorages, the Causeway, Sisters' Islands reefs,
Pulau Tekong live-firing areas).

**Gates:** schema 63/63 · fidelity qatar + singapore-mpa PASS (journey_bp=0) · linkage 0 gaps ·
geometry exit 0 · seal-integrity exit 0 · build exit 0.

---

## 2026-06-30 — Public Transport Authority category: Bahrain MOTC gold reference

New proposal category for **public transport authorities** (distinct from mobility partners:
public-good framing, the authority's own mandate/precedents, domestic-first). Bahrain MOTC is the
**gold reference**; pattern then replicates to Qatar MOTC, Singapore MPA, and beyond.

**Tasklet lane (this PR — partner-facing content + presentation only):**
- Rewrote `bahrain-motc.json` (both trees): new authority narrative arc (network & gap → new public
  mode → **home-water network first** → optional regional links → mandate delivery → plain ask).
- **Killed Prove/Scale/Mature** scaffolding and all internal jargon (Grok/Tasklet/seal-lane/N30 ladder/
  super-app/journey-wallet/SOM-SAM-TAM/`{home}`/"inter-emirate"). 0 rendered-text jargon hits.
- **Fixed wrong data:** removed the Ras-Al-Khaimah/Dubai journeys that had been copy-pasted into Bahrain.
- **Domestic-first, grounded in real precedent:** the live Masar **water taxi** (Apr 2025, 6 stations),
  the **Bahrain–Qatar ferry** (Nov 2025), King Fahd Causeway (~33M crossings/yr), net-zero 2060 / −30% 2035.
- **Economics → PTA public-value + operating convention** (presentation): rungs/horizons relabeled plain,
  super-app rung dropped, ladder bridges de-jargoned, `public_value` block added. **Model numbers untouched.**
- All routes `route_id: null` + `_link_status: "pending-seal"` (intentional-null). **All 4 strict gates pass;
  build clean.** Fidelity `bahrain-motc` = PASS, journey_bp=0.

**New evidence/handoff files:**
- `PTA-DOSSIER-bahrain-motc.json` — sourced mandate/targets/precedent + the domestic boarding-point network
  (15 BPs w/ anchor coords, 8 domestic pairs, 2 regional links) + routing hazards. Dossier schema = PTA template.
- `GROK-SPEC-bahrain-motc-domestic-routing-2026-06-30.md` — **routing handoff**: mint/bind BPs, route every
  pair with **hand-curated waypoints, ZERO land crossings** (causeway/reef/shallow rules), land/water QA gate,
  then rebind `route_id`s + regenerate economics under the convention.
- `PTA-ECONOMICS-CONVENTION.md` — the public-value + fares/operating frame (replaces the mobility ladder).

**Grok lane (next):** seal the domestic routes with hand waypoints (no land crossings), rebind route_ids,
regenerate quantified public-value + operating-model numbers, add a `public_value` render slot.

---

## 2026-06-29 — Fidelity debt burn-down COMPLETE (A · B · C) → Grok may tighten gates

Closes `docs/NOTES-FOR-TASKLET.md § 2026-06-29 — Fidelity debt burn-down` and
`handoff/partner-map-model/TASKLET-FIDELITY-DEBT-MANIFEST.json`. **All three workstreams done; all
four gates green.** Grok is clear to restore the full §3.7 gate (block all hub partners on
`journey_bp` / REWRITE), drop the tiered reference-only workaround, and run `RELEASE=1 ./scripts/deploy.sh`.

### Gate receipt (run on this branch)

| Gate | Command | Result |
|------|---------|--------|
| Fidelity | `audit_proposal_fidelity.py --all-partners --strict-deploy-gate` | **exit 0** · journey_bp=0 across **all 62** partners |
| Geometry | `audit-route-geometry.py --strict-severe` | **exit 0** · story **0 fail / 0 allowlisted** |
| Linkage | `audit-partner-route-linkage.mjs --strict --global` | **exit 0** · 0 gaps · 62 story-ready · 0 allowlist |
| Seal | `validate-seal-integrity.py --strict` | **exit 0** |
| Build | `build.mjs && build-site.mjs` | **exit 0** · 268 partner/market + 1043 share pages |

Final verdict spread: **PASS 54 · TRIM 7 · REWRITE 1**. `journey_bp = 0 everywhere.`

### Workstream A — hub `journey_bp` + REWRITE

Pipeline run per partner in documented order: `relink_partner_journeys.py --apply` →
`reground_proposal_surfaces.py --apply` → `fix_partner_distance_honesty.py --apply` → re-audit.

- **All 18 manifest hubs** now `journey_bp=0`. 16/18 PASS; **uber** and **line** are TRIM/`journey_bp=0`
  (residuals are *featured* chips bound to non-gold routes — `e__uae__1b860507c38f` Dubai↔Abu Dhabi,
  `ics-2df0a1d37f` Florianópolis — that `reground` deliberately skips; not journey debt).
- Also cleaned 11 non-hub partners that were REWRITE/`journey_bp>0` (dubai-rta, hong-kong,
  indian-ocean-luxury, norway-fjords, nyc-ferry, qatar, singapore-mpa, wsf, d-marin, abu-dhabi-itc, yango).
- **Only remaining REWRITE: `transport-nsw`** (non-hub, `journey_bp=0`). Its 3 featured chips
  (`Circular Quay ↔ Manly / Watsons Bay / Parramatta`) bind to `ics-*` Sydney-ferry routes whose
  stored endpoint labels are coarse ("Sydney Harbour"). Left at HEAD on purpose — forcing a label
  sync would degrade the partner-facing copy; proper fix is precise endpoint labels on those `ics-*`
  routes (geometry/label lane), not a journey reground. **Not a hub, does not block the hub gate.**
- Note: `relink` is *not* idempotent if re-run after `reground` — it re-promotes clickable routes
  and can reintroduce label mismatches. Run the sequence **once, in order, per partner**. (uber/line/
  thames-clippers/transport-nsw were reset to HEAD and re-run cleanly after an out-of-order double pass.)

### Workstream B — story routes on allowlist → 0

- `scrub_story_allowlist.py --apply` removed **86** story `route_id`s from
  `data-clean/route_water_allowlist.json` (5386 → 5300 ids).
- Re-audit: **story 696 pass / 0 fail / 0 allowlisted**. Every scrubbed route passes land QA on its
  raw geometry (`interior_land_km = 0`) — **no `mint_story_channels` authorship was required** for the
  live set; the allowlist entries were pure grandfathering. (The mint lane needs `shapely`, which isn't
  in this env; it wasn't needed.)
- `GEOMETRY-STORY-HOLD.json` (809 broader pending) untouched — still Grok's channel-authorship lane.

### Workstream C — linkage after TRIM DROP (no permanent aspirational chips)

- Linkage gate global strict: **0 gaps, 62 story-ready, 0 allowlist.**
- Re-grounded the `grok/mark_unlinked_aspirational` filler chips on **cabify, centara-thailand,
  freenow, soneva** → real `route_id`s; all 4 stay PASS. `mark_unlinked_aspirational` count on those = 0.
- **saudi-pif** left at HEAD: re-grounding regressed it to TRIM/`journey_bp=1` (scoped route had a
  non-gold label), so kept PASS with its existing chips — acceptable for a non-hub. One residual
  `mark_unlinked_aspirational` holder; flag for the precise-label lane if product wants it real.

### Files in this PR

- `data-clean/partners/*.json` (33) + `partner-pitch/partners/*.json` (33 mirrors) — relinked/regrounded.
- `data-clean/route_water_allowlist.json` — story scrub.
- Aggregate evidence: `PROPOSAL-FIDELITY-AUDIT.json`, `GEOMETRY-TRIAGE.json`, `PARTNER-ROUTE-LINKAGE-AUDIT.json`.
- Per-partner `PROPOSAL-FIDELITY-<slug>.{json,md}` receipts regenerate deterministically from the data
  via `audit_proposal_fidelity.py` — not all re-committed here to keep the diff reviewable; re-run the
  audit after merge (Grok does this as part of gate tightening) for a byte-fresh set.

### Open follow-ups (small, non-blocking)

- `transport-nsw` + uber/line/thames-clippers featured chips on coarse `ics-*` labels — precise endpoint
  label pass (geometry lane) to take them PASS.
- `saudi-pif` one aspirational chip — re-ground once a gold route with matching labels exists.

---

_Last updated 2026-05-30 (overnight session)._

## This push (dev-mode build, route cache warm)

### Route labels — every tooltip now reads City → City (no slugs, no hashes)
- `route_labels.py` resolves BP endpoints in all forms: node id, raw BP id, **rendered
  `bp-<hash>` pin id**, and `city__suffix`.
- **Fixed a latent bug affecting ~906 local-mesh capillary routes**: bp-hash endpoints
  previously prettified to "Bp <hash>". Now they resolve to the real BP name AND real
  parent city. Verify: 0 routes contain a raw "Bp <hash>" label.
- Verbose BP names trimmed for tooltips (e.g. "Nuweiba Port (historic … ferry terminal)"
  → "Nuweiba Port"). Intra-city capillaries read "City: A → B".
- **Front-end ask still open**: tooltip should use `properties.label` (clean) — one-line change.

### Quanta-LR curation (A+B+C+D applied)
- **A** — any route ≤70 nm is now Pioneer II (all-electric range), even if the spine/config
  marked it Quanta-LR. Enforced in both `route_network._emit` and build.py edge gate.
  Result: Quanta-LR count 94 → 46; **0 Quanta-LR routes ≤70 nm**.
- **B** — illustrative placeholder endpoint (`rsg-marawi-east-island`) suppressed
  (`relevance:"hide"`); its 6 spur routes are gone.
- **C** — fixed the one raw unresolved endpoint (now "Nuweiba Port").
- **D** — genuine long-haul hospitality spurs kept, framed City → Region.
- Clean QLR hero backbone: Jeddah→NEOM (472nm), Wakatobi→Banda (370), Manama→Dubai (291),
  Lombok→Komodo (237), Bangkok→Koh Samui (205), Doha→Dubai (196)…
- Full curation log: `docs/QUANTA-LR-CURATION-REVIEW.md`.

### Partner pitch content layer (expanded — for Claude's render)
- **19 city briefs** (`partner-pitch/city_briefs/*.json`) — partner-neutral pitch synthesis
  (demand, use-cases by archetype, routes, POIs, PT angle, vessel fit) with per-partner overlays:
  MENA — dubai, abu-dhabi, doha, manama, muscat, jeddah, red-sea-global, neom, sharm-el-sheikh;
  SEA — singapore, bali, lombok, komodo, phuket, bangkok, hong-kong, maldives, jakarta-batam, colombo.
- **6 partner proposals** (`partner-pitch/partners/*.json`) — phased narrative arcs (hero,
  why-now, ordered phases w/ city subsets + routes + camera + KPIs):
  grab, dubai-rta, careem, abu-dhabi-itc, singapore-mpa, red-sea-global.
- **Now live in the page**: build injects `window.CITY_BRIEFS` and `window.PARTNERS` globals
  (guaranteed, idempotent) so the front-end can read them immediately. If/when the template
  adds `__CITY_BRIEFS__` / `__PARTNERS__` placeholders, the build uses those instead.
- **Claude action**: read `window.CITY_BRIEFS[cityId]` for the rich city panel; read
  `window.PARTNERS[slug]` (phases[]) for the phase carousel + `?partner=<slug>` scoping.
- Render specs: `docs/BRIEF-FOR-CLAUDE-pitch-panels.md`, test brief `docs/BRIEF-FOR-COWORK-pitch-flow.md`.

### Build architecture v4 — fast dev path vs weekly release gate
- `BUILD-ARCHITECTURE-v4.md`: `dev.sh` (seconds, default) vs `release.sh` (weekly full gate + seal + sweep).
- Two recurring traps fixed permanently in code: vessel_specs fallback (never empty),
  route-cache key now hashes supplemental inputs (no manual cache deletes).

## data-clean blobs (this build)
- FEATURES_BY_TYPE (4), ROUTES (1501), STORIES (7), VESSEL_SPECS (2).
- NOTE: dev-mode push — `SEAL.json` will be re-derived at next weekly `release.sh`.
