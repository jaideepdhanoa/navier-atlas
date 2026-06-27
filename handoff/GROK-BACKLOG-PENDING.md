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

## 1. Active priorities (plan-first — do not execute until plan approved)

| Priority | Track | Why |
|----------|-------|-----|
| **P0** | **Proposal route quality audit** | Journeys / signature / featured / phased routes showing false precision (e.g. Careem 4/5 bad BPs) — credibility risk |
| **P1** | **UAE hand-waypoint channel routing** | Palm, Dubai Marina, Creek, Abu Dhabi islands, Deira Island — spaghetti over land extensions |
| **P2** | FE-2 dedup | ~193 referenced-copy groups |
| **P3** | Mesh geometry | ~3,035 non-story fails |

**Plan doc:** `handoff/PROPOSAL-ROUTE-QUALITY-PLAN-2026-06-27.md`

---

## 2. Closed / unblocked

| Issue | Verdict |
|-------|---------|
| **#127, #121, #104, #115, #119** | ✅ CLOSED |
| **#112 binding re-pull** | ✅ QA PASS (live apply omitted) |
| Formal gold SEAL sign-off | Unblocked (#119 PASS) — Tasklet |

---

## 3. Tasklet dependencies (to confirm in audit)

| Item | Owner | Notes |
|------|-------|-------|
| Partner narrative + journey copy | Tasklet | Which corridors are "commercial-now" vs roadmap |
| `CORRIDOR-ENDPOINT-GROUNDING.json` | Tasklet/Grok | BP endpoint authority for proposal surfaces |
| UAE frond-resolution polygons | Tasklet | Palm trunk channel authorship (LB carry-forward) |
| Cluster brief `signature_routes` | Tasklet | Gold source for journey binding |
| Deck lane (Grab/Minor live apply) | — | **Omitted** |

---

*Grok seat · Credibility pass: proposal surfaces before mesh capacity work*