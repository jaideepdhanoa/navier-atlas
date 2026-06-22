# Partner Deck Grok Handoff Status — Wave 10A — 2026-06-21

## Status

Tasklet deck-prep artifacts are complete for the requested Wave 10A partners. Grok create/bind/apply/render QA remains open.

This does **not** assert live decks, image provenance, route render receipts, economics cascade completion, or proposal parity are complete.

## Partners prepared

- `qatar` — Qatar Tourism — deck-prep-complete / grok-create-or-bind-needed
  - Guardrail: Authority/tourism deck. Commercial-now content should stay on Doha Bay / Doha domestic route economics already cascaded; Gulf capital corridors are roadmap-only where economics_status=roadmap_excluded and must stay visually separated.
  - Economics status from source: `cascaded`
- `bahrain-motc` — Bahrain MOTC — deck-prep-complete / grok-create-or-bind-needed
  - Guardrail: Authority proposal, not a mobility-platform proposal. Bahrain domestic + Manama↔KSA Eastern Province are the only commercial-now candidates; Doha/Dubai/Abu Dhabi/Muscat/Ras Al Khaimah legs are roadmap-only unless separately resealed and range-gated.
  - Economics status from source: `pending_grok_route_seal_then_authority_model`
- `rakta` — RAKTA — deck-prep-complete / grok-create-or-bind-needed
  - Guardrail: Authority proposal, not a mobility-platform proposal. RAK domestic resort/city access and RAK↔Dubai/northern-emirates are proposal candidates. Musandam/Khasab remains exact-bind-required; Gulf capital links remain roadmap-only.
  - Economics status from source: `pending_grok_route_seal_then_authority_model`
- `hong-kong` — Hong Kong — deck-prep-complete / grok-create-or-bind-needed
  - Guardrail: Authority/destination-region proposal. Many ferry/PRD routes remain unlinked in source; deck must show exact-bound Victoria Harbour first and treat Macau/PRD crossings as Grok holds until IDs exist.
- `gojek` — Gojek (GoTo) — deck-prep-complete / grok-create-or-bind-needed
  - Guardrail: Commercial super-app deck. IMPORTANT: the source contains an inheritance contamination flag: phases/journeys currently include Korea/Kakao route labels despite Gojek’s Indonesia/Singapore network thesis. Grok must not present Korean route content; rebuild launch-market slide from source markets/network_footprint only after exact ID validation.
- `abu-dhabi-itc` — Abu Dhabi ITC — deck-prep-complete / grok-create-or-bind-needed
  - Guardrail: Authority deck. Focus Abu Dhabi island-core / emirates connectivity first. Gulf cross-border legs are range-gated roadmap and must not be sold as N30 commercial-now.
- `dubai-rta` — Dubai RTA — deck-prep-complete / grok-create-or-bind-needed
  - Guardrail: Authority deck. Focus Dubai Creek/Harbour/Palm/Dubai Islands and UAE emirates connectivity. Gulf cross-border legs are Quanta-LR roadmap only.
- `singapore-mpa` — Singapore MPA — deck-prep-complete / grok-create-or-bind-needed
  - Guardrail: Authority/regulator deck. Focus clean harbour-craft mandate, Singapore inner-waterfront, and exact-bound Batam/Bintan/Desaru/Riau candidates. Regional SEA examples outside Singapore must be source-labeled and not overclaimed as MPA scope.
- `red-sea-global` — Red Sea Global — deck-prep-complete / grok-create-or-bind-needed
  - Guardrail: Hospitality/sovereign developer deck included by explicit user request. Preserve prior guardrail: do not create new NEOM/Red Sea Global binds elsewhere; for this deck use only source-backed Red Sea Global assets and leave inherited Maldives/Four Seasons/Bora Bora artifacts as gaps unless validated.
- `saudi-pif` — Saudi Arabia (PIF) — deck-prep-complete / grok-create-or-bind-needed
  - Guardrail: Sovereign investment deck. Preserve prior guardrail: no new NEOM / Red Sea Global binds unless exact existing source requires them; separate PIF national/Jeddah/Eastern Province narrative from NEOM/RSG roadmap/hold items.
- `jih-global` — JIH Global — deck-prep-complete / grok-create-or-bind-needed
  - Guardrail: Sovereign/JV Maldives deck. Economics URL and sidecar exist; routes show limited exact binding. Grok should anchor to Velana/Greater Malé first and leave mid-atoll resort hops pending/null until sealed.
  - Economics status from source: `cascaded`

## Grok-owned holds

- Slides API only; no PPTX round-trip and no full-replace.
- Pull full slide/object inventory before edits for every partner.
- Use exact IDs only; null beats confidently wrong.
- N30/N35 compositing only with market-specific source-approved backgrounds; no Atlas-generated images.
- Do not change partner JSON phase topology or market topology during deck creation.
- Do not overwrite model_link, route_id, or route_ids; deck lane reads sources only.
- Return per-partner QA receipt with deck ID, slide count, image provenance, source-map coverage, render receipts, unresolved gaps, and no-op replay result.

## Tracking files

- `deck-studio/docs/PARTNER-DECK-PREP-TRACKER.json`
- `deck-studio/docs/PARTNER-DECK-PREP-TRACKER.md`
