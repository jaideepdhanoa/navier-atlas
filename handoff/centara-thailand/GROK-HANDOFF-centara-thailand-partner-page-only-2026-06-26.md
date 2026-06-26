# Grok Handoff — Centara Thailand Partner Proposal Page Only

Status: **partner-page handoff only**  
Do **not** rebuild, overwrite, or own the Centara deck from this handoff. Tasklet is preparing the deck lane separately against the live Minor Hotels gold deck. This handoff gives Grok the optional partner proposal page data/narrative if we decide to publish it.

## Scope

Create or stage a Centara Thailand hospitality partner proposal page using the source-backed research package.

Partner key recommendation: `centara-thailand`  
Archetype: `hospitality` / hotel-resort operator  
Country: Thailand  
Cluster count: exactly **six**:
1. Bangkok river gateway
2. Western Gulf — Hua Hin / Cha-Am
3. Eastern Gulf — Pattaya / Jomtien / Sriracha / Koh Chang
4. Phuket / Andaman north
5. Krabi / Phi Phi
6. Samui / Gulf islands

## Mandatory narrative frame

Use normal, partner-facing language.

Core thesis:
> Centara already sits on Thailand’s best water-facing guest journeys. Navier turns those stays into a cleaner, quieter, more premium way to arrive, move, and explore — starting with six Thai clusters where the hotel footprint and destination demand overlap.

Operator framing:
- **Cost** — predictable electric run cost on short, repeatable guest-paid routes.
- **Convenience** — fewer transfer handoffs, cleaner packaging, better timing.
- **Comfort** — quieter vessel, calmer boarding, premium guest experience.

Do **not** use a SOM/SAM/TAM/GMV ladder on the hospitality page. If economics appear, use corridor examples only.

## Required property inventory input

Use the Tasklet package file:
`/tasklet/agent/home/centara-thailand-2026-06-26/centara-thailand-property-inventory.json`

If importing to repo, preserve the fields:
- `cluster_id`
- `property_name`
- `brand`
- `location`
- `status`
- `water_role`
- `fit_score`
- `source_url`
- `evidence_note`
- `hold_note`

## Required economics sidecar input

Use the Tasklet package file:
`/tasklet/agent/home/centara-thailand-2026-06-26/centara-thailand-economics-sidecar.draft.json`

Important: every route has `route_status = working distance; route_id null until sealed`. Do not convert any working distance into a sealed route claim without running the normal route-seal workflow.

## Partner page structure

Recommended sections:

1. **Hero**
   - Title: `Centara × Navier`
   - Subtitle: `A premium electric water layer for Thailand’s coastal guest journeys`
   - Body: short thesis above.

2. **Why Centara / why now**
   - Centara has a national hospitality footprint across Thailand’s best coastal and island regions.
   - Thailand tourism is scaled and returning strongly; this is a visible guest-experience opportunity, not a niche pilot.
   - The water layer is most compelling where Centara already has beach, island, river, and gateway demand.

3. **Six-cluster network**
   - Render all six clusters; do not add a seventh cluster.
   - Eastern Gulf may show both mainland and Koh Chang within the same cluster.

4. **Guest journeys unlocked**
   - Arrival: airport/pier/gateway to resort.
   - Exploration: resort-curated island or coastal excursion.
   - Resort-to-resort: only where property/demand anchors are real.
   - Event/MICE river movement in Bangkok: allowed only as hotel-curated guest movement.

5. **Operator model**
   - Cost · Convenience · Comfort.
   - Centara owns demand, packaging, guest service standards, and property coordination.
   - Navier owns vessel design, route design, operating playbook, and economics transparency.

6. **Corridor examples**
   - Use working examples only; clearly label as pending route seal.
   - Do not call them sealed corridors.

7. **Next step**
   - Select 1–2 pilot corridors.
   - Validate pier/beach/dock operations.
   - Seal route geometry and final economics.

## Route / geography rules

- `route_id`: null until sealed.
- Dock/pier rights: null until validated.
- Exact distances: pending until sealed.
- Do not invent city IDs, boarding-point IDs, or geometry.
- Do not use Yango-style additive country seeds or unrelated mobility-partner assumptions.
- Do not borrow Minor property economics except the approved hospitality deck economics convention ($1M vessel and operator frame).

## Copy rules

Plain English only. Avoid internal taxonomy and model words, including:
- SOM / SAM / TAM / GMV ladders
- captive resort mesh
- network width
- grounded
- route seal / amber-dashed / greenfield
- capture-rate language in partner-facing headings
- vessel codenames outside approved product context

Allowed product language:
- N30 if the deck/page needs the actual vessel name.
- Otherwise prefer `electric water shuttle`, `quiet electric vessel`, or `premium water arrival`.

## Assets / logo

Centara partner logo is required before any live deck or page cover uses partner branding. Use official source only. If not banked, set `partner_logo.status = needs_sourcing` and do not guess.

## Validation receipt Grok must return

Return:
- branch name
- PR link
- commit SHA
- exact files changed
- validation command/output
- explicit nulls/held items
- route IDs still null/pending
- confirmation that the deck was not rebuilt or overwritten from this partner-page handoff
