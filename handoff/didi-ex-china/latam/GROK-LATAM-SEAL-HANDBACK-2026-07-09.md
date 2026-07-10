# DiDi Latin America — Grok seal handback

**UTC:** 2026-07-10T03:04:41Z  
**Status:** `latam_geometry_seal_complete / finance_cascade_not_run`  
**Git commit:** `1671a0f96657`  
**Upstream PR:** #212 (`c4a4af20`)  
**Handoff:** `handoff/didi-ex-china/latam/DIDI-LATAM-GROK-SEAL-HANDOFF-2026-07-09.md`

## Route inventory (before → after)

| Cluster | Before S/A/E | After S/A/E | Delta |
|---|---:|---:|---|
| `brazil` | 59/59/0 | 59/59/0 | no inventory change |
| `colombia` | 15/14/1 | 15/14/1 | no inventory change |
| `costa-rica` | 67/65/2 | 67/65/2 | no inventory change |
| `panama` | 47/47/0 | 47/47/0 | no inventory change |
| `dominican-republic` | 32/29/3 | 32/29/3 | no inventory change |
| `galapagos-ecuador` | 3/0/3 | 3/0/3 | no inventory change |
| `peru` | 12/12/0 | 12/12/0 | no inventory change |
| **Total** | 235/226/9 | **235/226/9** | pinned reproduced |

## Wave outcomes

### A1 Brazil + Colombia
- BP: sealed=9 held=6 dropped=2 (researched=17)
- Featured (active only): Brazil ['rn-1886629dbf0c', 'rn-80f0d0ebe0bd', 'rn-00bb6ded4be5', 'rn-369ef0eb69d9']; Colombia ['rn-aa790551baa7']
- `rn-3d69b89a7af6` remains quarantine/hide
- No finance; annual pax null

### A2 Costa Rica + Panama + DR
- BP: sealed=19 held=91 dropped=14 (researched=124)
- Featured active spines only; **not featured:** `rn-60740d4c3114` (quarantine/hide)
- Cartí–Colón `route_id` remains null

### B Ecuador + Peru
- BP: sealed=0 held=9 dropped=3
- Galápagos: **3 stamped / 0 active / 3 excluded** — quarantine retained; **not rendered**
- Foreign stamps remain absent; `rn-f0a756c7f278` stamped `peru` (hygiene ≠ seal claim)
- No DiDi galapagos/peru market blocks → partner bind deferred

### C Chile + Argentina
- **No mint.** Registry approval required before canonical IDs.
- BP dispositions: held=20 dropped=2 (all candidates)
- All 10 corridor `route_id`s remain null

## BP totals

- Researched: **175**
- Sealed (confirm existing): **28**
- Held: **126**
- Dropped: **21**
- Silent drops: **0**

## Finance

- **Cascade not run**
- Annual one-way pax: all null (expected 49)

## Gates

- **gate_g:** PASS (exit 0)
- **inheritance_strict:** PASS (exit 0)
- **finance_inheritance:** PASS (exit 0)
- **fidelity:** PASS (exit 0)
- **route_linkage:** PASS (exit 0)

## Deploy

- **Alias:** https://navier-atlas.vercel.app
- **Production:** https://navier-atlas-6rxsvlm2v-jaideepdhanoas-projects.vercel.app
- **DiDi:** https://navier-atlas.vercel.app/didi
- Pre-flight: PASSED

## Render QA

- Live deck not edited
- Only active routes eligible for render
- Galápagos not rendered
- Post-deploy: verify partner pages for Rio, Cartagena, Nicoya, San Blas, Samaná, Lima anchors

## Artifacts

- Machine: `handoff/didi-ex-china/latam/GROK-LATAM-SEAL-HANDBACK-2026-07-09.json`
- BP detail: `handoff/didi-ex-china/latam/GROK-LATAM-BP-DISPOSITIONS-2026-07-09.json`
- This file: `handoff/didi-ex-china/latam/GROK-LATAM-SEAL-HANDBACK-2026-07-09.md`

