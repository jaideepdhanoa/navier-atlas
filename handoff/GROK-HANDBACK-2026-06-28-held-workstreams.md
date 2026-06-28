# Grok handback — held workstreams (2026-06-28)

## 1 · OAuth — ACTION REQUIRED (Jaideep)

Auth server is listening on **http://localhost:3000**. Complete sign-in in the browser:

https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive.file%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive.readonly%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdocuments%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fspreadsheets%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fpresentations%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcalendar%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcalendar.events&prompt=consent&response_type=code&client_id=533129153761-fh7a0vo2gsp1qv5fcasv2rfd30jqtaec.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Foauth2callback

After auth, Grok can:
- Apply Gojek prize-ladder values to slide 11
- Create/bind AirAsia MOVE deck (PR #133 prep)

Re-run if server stopped: `GOOGLE_DRIVE_OAUTH_CREDENTIALS=~/.config/google-drive-mcp/gcp-oauth.keys.json npx -y @piotr-agier/google-drive-mcp auth`

---

## 2 · Gojek — DONE (model engine)

| Item | Status |
|------|--------|
| Sumba seal | `rn-33fe0cc24a60`, `rn-c77ad1314ae3` + bindings |
| Lake Toba | prior seal confirmed in receipt |
| Network re-cascade | `growth-gojek.json` — floor ~$22M, SAM ~$372M |
| 10-market deck pack | `handoff/gojek-indonesia/GOJEK-10-MARKET-DATA-PACK.json` |
| Economics spec | `handoff/gojek-indonesia/GROK-SPEC-economics-refresh.md` |
| Deck bindings | `deck-studio/decks/gojek/{market-scope,economics-binding}.json` |
| Deck values | `deck-studio/decks/gojek/deck-economics-values-gojek.json` |

**Held:** Slides API apply (OAuth); map QA on `/gojek/sumba` + `/gojek/lake-toba`

---

## 3 · AirAsia — DONE (model pass)

| Item | Status |
|------|--------|
| Economics cascade | `scripts/grok-airasia/run_econ_cascade.sh` |
| Demand apply | `apply_airasia_demand.py` (FLAG hub assumptions) |
| growth_case | **filled** — floor ~$18M, SAM ~$356M, TAM ~$1.42B |
| PP↔El Nido | `rn-81f865bba3ac` → `roadmap_quanta_lr` (excluded from floor) |
| SEAL hashes | `update_seal_hashes.py` run |

**Held:** AirAsia deck create/bind (OAuth + logo sourcing)

---

## Scripts added

- `scripts/grok-indonesia/build_gojek_deck_corridors.py`
- `scripts/grok-indonesia/run_gojek_deck_cascade.sh`
- `scripts/grok-airasia/apply_airasia_demand.py`
- `scripts/grok-airasia/run_econ_cascade.sh`