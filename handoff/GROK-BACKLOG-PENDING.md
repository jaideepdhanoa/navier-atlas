# Grok backlog — pending work (living queue)

**Baseline:** `main` @ `abd7c599` · Production: https://navier-atlas.vercel.app  
**Updated:** 2026-06-28 (parked)  
**Intake:** Jaideep directive — proposal route quality + UAE channel routing (plan-first)

---

## ⏸ Parked (2026-06-28) — Gojek deck economics handback

Tasklet applied live slides 4+13; receipt PR #135 OPEN @ `93971c98`. See `handoff/gojek-indonesia/TASKLET-HANDBACK-PR135-2026-06-28.md`.

| Item | Owner | When back |
|------|-------|-----------|
| Merge PR #135 (BUILD-LOG) | Grok | first |
| SOM rung ($87M) — metric basis | Grok | model pass |
| Corridor count 43 vs 49 | Grok | confirm |
| Lombok + Lake Toba KPI cards | Grok | seal/floor |
| Map backgrounds | Jaideep | visual |
| Google Sheets publish (gojek, airasia-move) | Grok | separate lane |

---

## 0. Decisions (locked)

| Decision | Status |
|----------|--------|
| **Google OAuth refresh** (Grab KPI apply + Minor live appendix) | ⛔ **SKIPPED / OMITTED** — not pursuing; deck lane deprioritized |
| **#118 Grab Slides apply** | ⛔ Omitted with OAuth skip |
| **#112 Minor live appendix apply** | ⛔ Omitted with OAuth skip |

KPI JSON, values sidecars, binding re-pull, and dry apply plans remain in repo as reference only.

---

## 1. Active priorities (plan approved 2026-06-27)

| Priority | Track | Why |
|----------|-------|-----|
| **P0a** | **Phase-map cumulative scoping** | ✅ Done — cumulative phases + three-tier opacity |
| **P0c** | **Partner scope live inheritance** | ✅ Done — hub partners inherit CLUSTERS.json at build; `partner-scope.mjs` + §3.8 drift gate |
| **P0b** | **Proposal route quality audit** | Careem ✅ · Noon ✅ PASS_WITH_FLAGS · Grab ⏳ (108 DROP) |
| **P1** | **UAE channel graphs (Grok-only)** | ✅ v1 Palm + Marina + Creek (`channel_graphs/`); AD islands + Deira next |
| **P2** | FE-2 dedup | ~193 referenced-copy groups |
| **P3** | Mesh geometry | ~3,035 non-story fails (deferred until proposal surfaces credible) |

**Plan doc:** `handoff/PROPOSAL-ROUTE-QUALITY-PLAN-2026-06-27.md`

### Locked display rules

- **Phase map opacity:** current phase full · prior phases medium · mesh low
- **Phase map:** cumulative `featured_routes` through active phase N only
- **Cross-emirate legs:** allowed when geometry + phase narrative fit
- **Channel graphs:** Grok drafts from satellite, self-validates
- **Hub map scope:** live cluster inheritance at build (`scripts/partner-scope.mjs`); sync JSON via `node scripts/sync-partner-map-scope.mjs`

---

## 2. Closed / unblocked

| Issue | Verdict |
|-------|---------|
| **#127, #121, #104, #115, #119** | ✅ CLOSED |
| **#112 binding re-pull** | ✅ QA PASS (live apply omitted) |
| Formal gold SEAL sign-off | Unblocked (#119 PASS) — Tasklet |

---

## 3. Dependencies (revised)

| Item | Owner | Notes |
|------|-------|-------|
| Phase-narrative fit + featured trim | **Grok** | Null beats wrong; e.g. drop RAK from Careem Phase 1 |
| UAE channel graphs | **Grok** | Satellite draft + self-validate; no Tasklet |
| `CORRIDOR-ENDPOINT-GROUNDING.json` | Grok | BP endpoint authority for proposal surfaces |
| Cluster brief `signature_routes` | Grok audit | Trim to phase-aligned S-tier only |
| Deck lane (Grab/Minor live apply) | — | **Omitted** |

---

*Grok seat · Credibility pass: proposal surfaces before mesh capacity work*