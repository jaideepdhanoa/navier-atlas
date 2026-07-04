# Finance-registry drift audit — Yango roster correction (2026-07-03)

**Question (Jaideep):** the Norway→Peru / roster correction updated the live Yango surface — does the **finance economics pipeline** need refreshing, and are **other partners** affected too?

**Short answer:** The finance pipeline (`finance/model/corridors.json` → `aggregate.py` → `agg-<p>.json` → sheet) is **independent** of the sealed partner surface and did **not** auto-update. It needed a Tasklet bite, now landed. The roster change is **isolated to Yango** — no other partner's confirmed market list changed, so only Yango's economics actually move. A full-partner sheet republish is optional (consistency only).

---

## 1. What this PR changed (Tasklet lane per `finance/README.md`)

### `finance/model/corridors.json`
**Dropped 6 stale Yango markets** (not on Jaideep's authoritative 27-market list):

| Key | Reason |
|---|---|
| `yango-turkey` | Turkey is NOT a Yango ridehail market (directive) |
| `yango-ksa-commercial` | KSA is NOT a Yango ridehail market (directive) |
| `yango-lagos` | Nigeria removed from Yango surface (#178) |
| `yango-caspian-az` | Azerbaijan/Baku removed from Yango surface (#178) |
| `yango-israel` | Israel not on authoritative Yango list |
| `yango-tunisia` | Tunisia not confirmed a Yango market (null-beats-wrong) |

**Added 2 net-new markets** with grounded L3 (fare + demand sourced, not invented):
- `yango-peru` — 5 corridors (Lima Bay run, La Punta↔San Lorenzo, Callao↔Palominos, Paracas↔Ballestas, Lima↔Paracas Quanta-LR). Fares from 2026 operator prices; demand from MINCETUR/tourism visitor pools (Ballestas ~150k/yr).
- `yango-colombia` — 6 corridors (Baru/Playa Blanca, Bocagrande, Islas del Rosario ×2, Tierrabomba, Barranquilla↔Puerto Colombia). Fares from 2026 operator prices (Rosario COP 90k ≈ $22 each way); demand from Cartagena tourism pools (~855k intl + 500k cruise).

**Retained 9 Yango markets** — `yango-uae · yango-qatar · yango-egypt · yango-cote-divoire · yango-senegal · yango-caspian-kz (Kazakhstan) · yango-morocco · yango-mozambique · yango-pakistan`.
⚠️ **Morocco / Mozambique / Pakistan are KEPT** — they ARE on the authoritative Yango list (Morocco demoted to a roll-up but still a Yango market). Grok's earlier note lumping "Morocco" as stale was incorrect.

### `finance/model/country-reference.json`
Added **Peru** and **Colombia** opex rows (modeled T3/T4, hydro-heavy grid CO2), following the existing Egypt/Kenya "modeled vs SG anchor" convention. Both were missing — the cascade would have fallen back to global-median estimates without them.

---

## 2. Cross-partner sweep — is anyone else affected?

Registry now **78 markets · 1,015 corridors · 70% route-bound**. Per-partner:

| Partner | Mkts | Corridors | Bound | Null | Bind% |
|---|---|---|---|---|---|
| bolt | 18 | 223 | 60 | 163 | 27% |
| yango | 11 | 119 | 48 | 71 | 40% |
| rapido | 7 | 115 | 115 | 0 | 100% |
| ola | 7 | 113 | 113 | 0 | 100% |
| careem | 2 | 79 | 79 | 0 | 100% |
| rakta | 1 | 46 | 46 | 0 | 100% |
| jih-global (Maldives) | 1 | 43 | 43 | 0 | 100% |
| uber-india | 3 | 21 | 21 | 0 | 100% |
| yassir | 3 | 20 | 14 | 6 | 70% |
| singapore | 1 | 18 | 6 | 12 | 33% |
| french-polynesia | 1 | 23 | 12 | 11 | 52% |
| philippines | 1 | 10 | 2 | 8 | 20% |
| cambodia | 1 | 5 | 0 | 5 | 0% |
| _(others 100% bound)_ | | | | | |

**Finding:** finance markets are keyed `{partner}-{geography}`, so partners never share rows. The geographies removed from Yango (Bahrain, Oman, Baku, Colombo, Lagos, Eastern-Province KSA) do **not** appear under any other partner's key — so **the Yango correction is economically isolated to Yango.** No other partner's confirmed market list changed.

**Separate (pre-existing, NOT caused by this change):** several partners carry unbound corridors (`route_id: null`) — bolt 27%, cambodia 0%, philippines 20%, singapore 33%, taiwan 33%, french-polynesia 52%. That's a **route-binding backlog** (Grok seal lane), not roster drift. Flagged here for awareness; the cascade already floor-fills unbound corridors, so sheets still build — they'd just gain precision as binds land. Not a blocker for this refresh.

---

## 3. Refresh scope

- **Required:** re-cascade **`yango`** (rows changed) → republish the Yango transparent sheet.
- **Optional (consistency only):** full-partner republish. Country-reference gained Peru/Colombia but those only feed Yango, so no other partner's numbers move.
- **Follow-on (not in this PR):** Cameroon (Douala), Congo (Pointe-Noire), Namibia (Walvis Bay), Venezuela (La Guaira/Maracaibo) are now in the Yango footprint but remain **finance-pending** (roll-up markets, not sub-pages). Their corridor dossiers exist (#178) — Tasklet can source L3 for them in a follow-on bite if you want them lifting the Yango TAM.
