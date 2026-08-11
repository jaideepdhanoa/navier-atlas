# Grok handback — `/bay-employers` microsite (Bay Area employer network)

**From:** Grok  
**Date:** 2026-08-11  
**Spec PR:** #348 (merged `74263a22`)  
**Implementation:** this handback + `/bay-employers` on `main`

## Status: Grok lane complete (P0 + P1)

Shipped a public employer sales surface at **`/bay-employers`** on the existing Atlas deploy tree (not a partner-auth path).

### What employers see (experience)
1. **Hero** — map-first CTAs: “See the network near me” / “Estimate cost for my team”
2. **Problem chips** — drive time · water speed (no knots) · foiling ride quality  
3. **Stripe proof** — ride worked; vessel class fixed (**no dock/berth dependency language**)  
4. **Two paths** — N30 shuttle now · N45 line on ~60–80 committed seats  
5. **Network map** — 6 ID-matched terminals + Lines A/B/C (water display paths); stop → seeds form + calculator  
6. **ROI calculator** — exact locked formulas; defaults **$4,500/mo · $75/rider**; line presets; copy-summary for Finance  
7. **Letter of intent** — Option A seats / Option B anchor line; non-binding; mailto handoff  

### Policy (Jaideep 2026-08-11)
- **No employer-facing framing that LOIs unlock docks, berths, or terminal access.**  
- Dock procurement is independent; LOIs sequence line + seat demand only (and may support dock talks offline, never as buyer friction).

### Resolved terminals (sealed POIs)
| Stop | `resolved_bp_id` |
|------|------------------|
| Larkspur | `bp-9ac1cd7b77` |
| SF Ferry Building | `bp-4e939f2346` |
| Mission Bay | `bp-6f4ad8afd4` |
| Oyster Point | `bp-e96f0d1393` |
| Redwood City | `bp-09dbb91b26` |
| Alameda / Jack London | `bp-98bb5bad66` |

### Gates
| Gate | Result |
|------|--------|
| Calculator defaults $4,500 / $75 | PASS |
| Copy audit (`scripts/audit_bay_employers_copy.py`) | PASS |
| Dock/berth dependency scan on copy | PASS |
| `build-site` emits `_dist/bay-employers/` | PASS |
| Middleware public path `/bay-employers` | PASS |

### Files
- `bay-employers/index.html` — page  
- `handoff/bay-employers/inputs/bay-employers-data.json` — resolved BPs + dock-clean copy  
- `scripts/build-site.mjs` — emit page + calculator/dock abort gates  
- `scripts/partner-auth-middleware.mjs` — public allowlist  
- `scripts/audit_bay_employers_copy.py` — standing copy gate  

### Live URL (after deploy)
https://navier-atlas.vercel.app/bay-employers  

### Tasklet next
1. Optional: richer form capture (CRM/Slack) beyond mailto  
2. Optional: shareable calculator querystring  
3. No further Grok geometry work — no new ROUTES; display lines only  
