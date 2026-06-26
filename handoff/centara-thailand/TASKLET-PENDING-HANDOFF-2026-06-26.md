# Tasklet pending handoff — consolidated (Grok → Tasklet)

**Baseline:** `main` @ `c9db6218` · Production: https://navier-atlas.vercel.app  
**Updated:** 2026-06-26 — Grok merged all 5 open Tasklet PRs (#106–#111) to `main`.

## Division reminder

Per `DIVISION-OF-LABOR.md`, **Tasklet** owns the graph, demand model, security gates, and official SEAL. **Grok** owns mint/bind, partner-page implementation, economics cascade execution, build, and deploy. **Deck builds are explicitly Tasklet.**

---

## 1. Tasklet PRs — merged 2026-06-26 (Grok)

| PR | Title | Status |
|----|-------|--------|
| **#111** | Centara Thailand hospitality deck plan | ✅ **MERGED** — Tasklet still owns live deck appendix refresh |
| **#108** | LINE MAN Wongnai deck + proposal package | ✅ **MERGED** — Tasklet still owes live Slides build |
| **#106** | Hospitality gold: Minor realism rebase (LB-261) | ✅ **MERGED** — Tasklet still owes Minor gold deck refresh |
| **#109** | Bolt parity re-audit | ✅ **MERGED** — Grok applied surgical fixes in `6e0eb8ba` |
| **#107** | Grok-chat migration playbooks | ✅ **MERGED** — docs on `main` |

**No open Tasklet PRs remain.** PR #110 (LINE MAN Grok handoff spec) was already **CLOSED**.

---

## 2. Centara Thailand — deck lane (highest-priority Tasklet item)

Grok completed the **partner-page-only** handoff. Tasklet still owns the deck.

### Already done (Tasklet, in PR #111)
- Deck plan + fact base (`handoff/centara-thailand/CENTARA-THAILAND-DECK-PLAN-FACT-BASE-2026-06-26.md`)
- Property inventory, draft economics sidecar, builder rules
- Official logo banked (`deck-studio/assets/logos/partners/centara/`)
- **v0 live deck:** https://docs.google.com/presentation/d/1uHEWfP0IufgZShzZWPdlzbaAy2GeR-FBuD7uRMbdYeQ/edit (24 slides, Minor gold spine)

### Still pending on Tasklet

| Item | Status |
|------|--------|
| **Bind sealed geometry into deck** | Grok sealed 7 corridors; deck receipt still lists route IDs / distances pending — appendix + map slides need refresh from `handoff/centara-thailand/centara-thailand-economics-sidecar.json` |
| **Appendix economics refresh** | Replace draft working math with sealed per-corridor numbers (7 slots, $1M vessel, no SOM ladder) |
| **Visual polish** | Receipt: “v0 … can be tightened further after review” |
| **Dock/pier/beach rights** | Still **null** — ops validation |
| **Bangkok framing QA** | Hotel-curated river gateway only (not open mobility) |
| **PR #111 merge/close** | Plan on `main`; PR still **OPEN** on GitHub |
| **`deck-studio/decks/centara-thailand/`** | No deck-studio config folder yet |

### Grok already delivered (Tasklet can consume)
- Partner page live: `/centara-thailand` (+ 6 market sub-pages)
- Sealed routes including minted `rn-eb5758aeba2a` (Chalong → Karon)
- Transparent sheet published to Drive
- Partner page **not** rebuilt from deck

---

## 3. LINE MAN Wongnai — deck lane

| Item | Owner | Status |
|------|-------|--------|
| Partner proposal mirror | Grok | ✅ On `main` |
| Live Slides deck | Tasklet | ❌ PR #108 |
| Thailand economics under `line-man-wongnai` | Tasklet/Grok | Mirror files exist; cascade parity QA |
| Deck config in repo | Tasklet | Not fully in `deck-studio/decks/` |

---

## 4. Official SEAL + security gates (Tasklet-owned)

| Gate | Status | Tasklet action |
|------|--------|----------------|
| `geometry_story` | **FAIL** — 852 pass / **168 fail** | Per-corridor channel authorship; target 100% story pass |
| `bp_on_water` | **NOT_RUN** | Run `gate_bp_water_adjacency.py`; record in SEAL |
| `geometry_story_allowlisted` | PASS | Keep at 0 allowlisted story routes |
| Official re-seal | Interim | Grok refreshed hashes post-Centara; Tasklet should issue formal gold SEAL |

Mesh backlog: `handoff/MESH-BACKLOG.md` — several markets under-meshed.

---

## 5. Economics cascade + narrative (`grok-handback-2026-06-24.md`)

- **36 partners** still have no `growth_case` (aman, six-senses, four-seasons, lyft, didi, gojek, yango, transit authorities, etc.)
- **Bolt data bugs:** floor rounding ($1.54M → “2M”), stale `source_rollup`, ladder on minted corridors not census
- **Bolt East Africa narrative** — only market missing UAE-parity fields
- **~190 null `journeys_unlocked`** across 23 partners
- **India sheets QA** — Adani/Reliance on Drive; wire `economics_url` on tracker

---

## 6. Deck lane backlog

| Item | Source | Status |
|------|--------|--------|
| Grab Thailand deck KPI refresh | grok-handback #6 | Reconcile BKK marquee (Atlas BKK↔Hua Hin vs deck ICONSIAM→Wat Arun) |
| Minor hospitality gold | PR #106 | LB-261 rebase |
| Hospitality ladder cascade | Handback | aman → six-senses → four-seasons → soneva |
| Mobility ladder cascade | Handback | lyft, didi, gojek, indrive, freenow, yango |

---

## 7. Research / coverage / locale cleanup

- P0 promotion: Bolt (`crete`, `malta-gozo`), Lyft (4 Hawaii)
- Yango interim regional seed reconciliation
- P1 mobility: Grab, DiDi, Gojek, Ola, inDrive, Cabify, FREENOW, Kakao
- Locale ledgers: UAE, Bolt, Thailand, Wave2
- India normalization + Adani/Reliance missing-market scan

---

## 8. Parked geometry closure queue

`PARKED-ROUTING-GEOMETRY-QUEUE.md` — current story fail count **168** (not 205).

- Story geometry → 100% pass
- South Africa mesh (Bolt), Croatia depth, Bolt Phase 0 footprint, Phase 2 minting waves, Economics Phase 5

Grok running wave 5; **Tasklet signs SEAL** when geometry is done.

**Latest Grok geometry batch (dry-run):** `solve_story_channels.py --story` → 0 fixed / 168 held — needs per-corridor hand-waypoint authorship + `--apply`.

---

## Suggested Tasklet priority order

1. Centara deck refresh — bind 7 sealed corridors + economics; close PR #111
2. LINE MAN deck build — PR #108
3. Formal SEAL — `bp_on_water` + gold re-seal
4. Bolt East Africa + data-bug cascade — PR #109
5. Growth ladder cascade — 36 no-ladder partners
6. Grab deck KPI / marquee reconciliation
7. Geometry story closure — 168 fails (Tasklet SEAL sign-off)

---

## Not pending on Tasklet (closed by Grok)

- Centara partner page + route sealing + hospitality economics cascade
- LINE MAN partner JSON mirror (`main`, PR #110)
- Bangkok→Pattaya Pioneer II visibility
- Route linkage audit (0 gaps / 61 partners)
- Production deploy Centara partner page (`7f803dc7`)