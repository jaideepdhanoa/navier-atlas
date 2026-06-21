# India Adani / Reliance expanded proposal package — 2026-06-21

Status: **Grok-ready narrative and scope package; exact geography/economics still gated.**

## What changed

- Expands **Adani Ports & SEZ** from a shell / asset queue into an India operator proposal across all Atlas display-ready India markets.
- Adds **Reliance Industries** as a new India owner/operator proposal file.
- Uses the existing Atlas India display layer only:
  - `mumbai-india`
  - `goa-india`
  - `kerala-backwaters-india`
  - `andaman-india`
- Keeps all port/campus/industrial assets in exact-bind backlog until Grok can match or mint deterministic IDs.

## Guardrails

- Broad narrative is allowed: both partners can own/run Navier India.
- Executable geography is strict: `route_id: null` unless Grok exact-binds/mints.
- No new finance corridors or economics were created.
- No fuzzy promotion for Ulwe, Dighi, Hazira, Mundra, Jamnagar, Nariman Point, Ghansoli/RCP, Dahej, Raigad, or east/south ports.
- `adani-ports` existing partner shell is reused; not recreated.

## Files

- `partner-pitch/partners/adani-ports.json` — expanded operator proposal.
- `partner-pitch/partners/reliance-industries.json` — new operator proposal.
- `handoff/partner-map-model/india-adani-reliance-expanded-proposal-control-2026-06-21.json` — Grok control/acceptance gates.
- This status file.

## Grok next action

1. Validate anchor-city IDs against sealed Atlas city IDs.
2. Bind or mint exact boarding points and routes only where source-supported.
3. Leave all unbound asset corridors null and emit a drop/hold ledger.
4. Do not run economics until route-level demand and fare evidence exists.
5. Range-gate all long routes: Pioneer II/N30 for ≤70nm; Quanta-LR for long legs.
