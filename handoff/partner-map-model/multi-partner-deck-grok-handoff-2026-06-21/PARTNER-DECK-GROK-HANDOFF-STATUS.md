# Partner Deck Grok Handoff Status — 2026-06-21

Batch: `multi-partner-deck-grok-handoff-2026-06-21`

## Status

Tasklet deck-prep artifacts are complete for the nine requested partner deck lanes. This means the repo now has schema-valid Deck Studio configs, slide manifests, content source maps, image manifests, a batch source map, a readiness queue, and a deterministic Grok prompt.

This does **not** mean the live decks are complete. Remaining work is Grok-owned create/bind/apply/render QA plus image provenance and route appendix receipts.

## Partners

### Bolt → `bolt`

- Source partner JSON: `partner-pitch/partners/bolt.json`
- Tasklet deck status: `deck-prep-complete / grok-create-or-bind-needed`
- Source markets: 6; rollups: 0
- Growth case present in source partner JSON: `false`
- Economics URL present in source partner JSON: `false`
- Scope guard: Use current Bolt proposal baseline only; preserve constraints: no Mexico or Morocco, and Malaysia only Penang + Sabah/Kota Kinabalu if Malaysia is reintroduced. Exact city/route IDs only.

### Yango → `yango`

- Source partner JSON: `partner-pitch/partners/yango.json`
- Tasklet deck status: `deck-prep-complete / grok-create-or-bind-needed`
- Source markets: 2; rollups: 0
- Growth case present in source partner JSON: `false`
- Economics URL present in source partner JSON: `false`
- Scope guard: Use existing Yango baseline first. Country/region seeds are additive only until validated; lead with Dubai-HQ Yango framing and keep ungrounded candidates as gaps.

### Noon → `noon`

- Source partner JSON: `partner-pitch/partners/noon.json`
- Tasklet deck status: `deck-prep-complete / grok-create-or-bind-needed`
- Source markets: 0; rollups: 0
- Growth case present in source partner JSON: `false`
- Economics URL present in source partner JSON: `true`
- Scope guard: UAE-first commerce and concierge water layer. KSA/Egypt remain narrative-only unless source-backed, ID-bound, and economics-cascaded.

### Ola → `ola`

- Source partner JSON: `partner-pitch/partners/ola.json`
- Tasklet deck status: `deck-prep-complete / grok-create-or-bind-needed`
- Source markets: 6; rollups: 0
- Growth case present in source partner JSON: `true`
- Economics URL present in source partner JSON: `true`
- Scope guard: High-value India consumer markets only: Mumbai/Konkan, Goa, Kerala/Kochi/Vizhinjam/backwaters, Andaman, Kolkata/Hooghly, Chennai/ECR/Cuddalore/Puducherry. Priority B remains excluded.

### Rapido → `rapido`

- Source partner JSON: `partner-pitch/partners/rapido.json`
- Tasklet deck status: `deck-prep-complete / grok-create-or-bind-needed`
- Source markets: 6; rollups: 0
- Growth case present in source partner JSON: `true`
- Economics URL present in source partner JSON: `true`
- Scope guard: High-value India consumer markets only: Mumbai/Konkan, Goa, Kerala/Kochi/Vizhinjam/backwaters, Andaman, Kolkata/Hooghly, Chennai/ECR/Cuddalore/Puducherry. Priority B remains excluded.

### Uber India → `uber-india`

- Source partner JSON: `partner-pitch/partners/uber-india-derivative.json`
- Tasklet deck status: `deck-prep-complete / grok-create-or-bind-needed`
- Source markets: 6; rollups: 0
- Growth case present in source partner JSON: `true`
- Economics URL present in source partner JSON: `false`
- Scope guard: Use the Uber India derivative source, not global Uber. High-value India consumer markets only; Kolkata and Chennai in scope; Priority B excluded.

### Uber MENA → `uber-mena`

- Source partner JSON: `partner-pitch/partners/uber.json`
- Tasklet deck status: `deck-prep-complete / grok-create-or-bind-needed`
- Source markets: 11; rollups: 0
- Growth case present in source partner JSON: `false`
- Economics URL present in source partner JSON: `false`
- Scope guard: Deck variant over the MENA/Gulf slice of uber.json only. Do not union global Uber markets into this deck; Grok must filter source claims to MENA/Gulf.

### Andani / Adani → `adani-ports`

- Source partner JSON: `partner-pitch/partners/adani-ports.json`
- Tasklet deck status: `deck-prep-complete / grok-create-or-bind-needed`
- Source markets: 6; rollups: 5
- Growth case present in source partner JSON: `false`
- Economics URL present in source partner JSON: `false`
- Scope guard: User label “Andani” normalized to existing repo partner_id adani-ports. Treat as operator-owned India authority/infra-style proposal, not ride-hail.

### Reliance → `reliance-industries`

- Source partner JSON: `partner-pitch/partners/reliance-industries.json`
- Tasklet deck status: `deck-prep-complete / grok-create-or-bind-needed`
- Source markets: 6; rollups: 6
- Growth case present in source partner JSON: `false`
- Economics URL present in source partner JSON: `false`
- Scope guard: Use existing Reliance Industries partner source. Treat as operator/platform-backed India water mobility proposal with exact route IDs only.

## Validation

- JSON parse and schema validation passed locally for all generated deck configs, slide manifests, and image manifests.
- No live Google Slides decks were edited by Tasklet.
- Route IDs/city IDs/BPs/sheet IDs/images remain pending where source files do not provide them.

## Grok next action

Run `GROK-PARTNER-DECK-CREATION-PROMPT.md`, bind/create the nine decks, pull full object inventories, apply through Slides API only, and return per-deck QA receipts plus unresolved gaps.
