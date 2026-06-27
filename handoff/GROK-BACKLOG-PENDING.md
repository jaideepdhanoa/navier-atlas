# Grok backlog — pending work (living queue)

**Baseline:** `main` @ `18376e3b` · Production: https://navier-atlas.vercel.app  
**Updated:** 2026-06-27  
**Intake:** Jaideep directive — proposal route quality + UAE channel routing (plan-first)

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
| **P0a** | **Phase-map cumulative scoping** | Cumulative featured routes at full opacity; mesh/network at low opacity — was highlighting wrong/future-phase routes |
| **P0b** | **Proposal route quality audit** | Phase-narrative misfit + wrong BPs (e.g. Careem RAK in Phase 1 beachhead) — credibility risk |
| **P1** | **UAE channel graphs (Grok-only)** | Palm, Marina, Creek, AD islands, Deira — satellite draft + self-validate; no Tasklet |
| **P2** | FE-2 dedup | ~193 referenced-copy groups |
| **P3** | Mesh geometry | ~3,035 non-story fails (deferred until proposal surfaces credible) |

**Plan doc:** `handoff/PROPOSAL-ROUTE-QUALITY-PLAN-2026-06-27.md`

### Locked display rules

- **Mesh:** visible at low opacity; phased routes emphasized
- **Phase map:** cumulative `featured_routes` through active phase N only
- **Cross-emirate legs:** allowed when geometry + phase narrative fit
- **Channel graphs:** Grok drafts from satellite, self-validates

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