# Grok handoff — Brazil (Floripa/Angra) + Egypt TAM, seals + deck slides (2026-07-17)

Source of truth: **PR #292** (`brazil-floripa-egypt-tam-2026-07-17`).
Do not hand-type economics — bind from the committed bindings/aggregates.

## 1. Corridor seals (before city-map render)
Three corridors are staged with provisional IDs in `finance/model/corridors.json` (market `brazil`).
Seal named `rn-` geometry into `data-clean/ROUTES.json` + `data-clean/CLUSTERS.json`, then repoint the
binding `pending_seal_route_ids` → `supported_route_ids`.

| PROV id | corridor | dist | node |
|---|---|---|---|
| `rn-angra-abraao-PROV` | Angra dos Reis Terminal ↔ Abraão Terminal (Ilha Grande) | 13.0 nm | `angra-dos-reis-ilha-grande-brazil` |
| `rn-floripa-r3-PROV` | Barreiros ↔ Miramar | 4.99 nm | `florianopolis-brazil` |
| `rn-floripa-r4-PROV` | Beira Mar ↔ Miramar | 4.87 nm | `florianopolis-brazil` |

City briefs: `partner-pitch/city_briefs/angra-dos-reis-ilha-grande-brazil.json`,
`partner-pitch/city_briefs/florianopolis-brazil.json`.

## 2. Deck slides (deterministic model→deck; Voi chassis, spine parity)
Bindings updated in PR #292 — regenerate the affected slides from the bindings/aggregates.

### DiDi Brazil (`1jHxxDgDd5Oki0eO4YoCfHHfC_aS-akGjb4UfXseIEK8`) — 12-slide spine already includes Angra + Floripa deep-dive + unit-econ slots. Refresh:
- Angra + Floripa **city deep-dive** maps (once sealed): marquee corridors, distances, descriptions.
- Per-city **unit-econ** (MID headline, `scen['mid']`):
  - Rio (Arariboia rn-1886629dbf0c): $329,190/boat-yr · 75.9% · 2.40yr · 92 boats (unchanged)
  - Angra: **$235,092/boat-yr · 65.3% · 3.91yr · 2 boats** ($30 fare, 13nm)
  - Floripa R3: **$235,136/boat-yr · 65.9% · 3.87yr · 33 boats** ($20 fare)
  - Floripa R4: **$235,136/boat-yr · 65.9% · 3.87yr · 51 boats** ($20 fare)
  - Floripa label: government pre-viability projection (EVTE, SIE SC + IDB/BID), NOT observed ridership.
- **TAM slide (5-rung):** $56.6M → SAM $1,264.6M → marine-TAM $5,058.5M → journey GMV $15,175.6M → DiDi platform 18% $682.9M.

### inDrive Brazil (see `deck-studio/decks/indrive-brazil/deck.config.json`) — same city/unit-econ slides.
- **TAM slide (4-rung, NO platform rung):** $56.6M → $1,264.6M → $5,058.5M → journey GMV $15,175.6M.

### inDrive Egypt (`1Nn3BRKUahikp87zC84JMdEVrcJYppm9ZXHgndAuzsEk`) — TAM slide only.
- **TAM slide (4-rung, NO platform rung, width template ON):** floor $8.5M pool → SAM $65.4M → marine-TAM $75.0M → journey GMV $224.9M.
- Headline: "Two boat-only routes are the floor — the Red Sea, Nile and Alexandria market runs far higher."

## 3. Discipline
- Element-scoped edits for non-unique strings (Mexico slide-9 lesson).
- Copy plain-English, pass `scripts/audit_partner_copy.py`, zero internal process vocab.
- Keep deck.config manifests + deck IDs synchronized to live state.
