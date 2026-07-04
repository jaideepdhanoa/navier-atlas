# Cross-partner coverage reconciliation — new-economics geographies (2026-07-04)

**Jaideep's question:** we've added grounded corridor economics for several markets — track them against the full partner list to see whether **other partners** operating in those same markets need corridors added too (so their TAM isn't under-counted).

**Method:** the corridor is a physical waterway with a partner-agnostic demand pool (e.g. Cartagena tourism). If two partners both operate in a market, the *same* corridor economics apply to both — only the capture rate differs. So for each geography where we now hold grounded L3, I scanned every mobility partner's **sealed proposal** (structured coverage/market/corridor arrays, not prose) for real presence.

Geographies with new economics: **Peru, Colombia** (PR #180) + **Cameroon, Congo, Namibia, Venezuela** (this follow-on).

---

## Result

| Geography | Corridor economics now held | Other partners with **structured** coverage | Verdict |
|---|---|---|---|
| **Colombia (Cartagena & Rosario)** | `yango-colombia` (6 corridors, grounded) | **DiDi**, **Cabify** (built corridors) · **Uber**, **inDrive** (coverage node only) | ⚠️ **Real overlap — action below** |
| **Peru (Lima · Callao · Paracas)** | `yango-peru` (5 corridors, grounded) | none | Yango-exclusive |
| **Cameroon (Douala)** | `yango-cameroon` (3) | none | Yango-exclusive |
| **Congo (Pointe-Noire)** | `yango-congo-brazzaville` (2) | none | Yango-exclusive |
| **Namibia (Walvis Bay)** | `yango-namibia` (3) | none | Yango-exclusive |
| **Venezuela (La Guaira · Maracaibo)** | `yango-venezuela` (3) | none | Yango-exclusive |

*(The one apparent Peru hit under inDrive was `derawan-berau-...-indonesia` — a false positive, not Peru.)*

## The one real overlap: **Colombia / Cartagena**

Cartagena & the Rosario Islands is a **shared corridor geography**. Five partners reference the identical `cartagena-colombia` node and the same waterways (Cartagena↔Rosario ~18 nm, ↔Barú ~12 nm), but depth varies:

| Partner | Cartagena in proposal | Built corridor set? | Finance block today | Economics state |
|---|---|---|---|---|
| **Yango** | yes | yes (6) | ✅ `yango-colombia` (grounded, this PR) | sealed L3, route_id null |
| **DiDi** | yes — deepest (3 phases, journeys) | **yes** — Rosario 18.3 nm, Barú 12.2 nm, Santa Marta 92.7 nm + cross-Caribbean | ❌ **none** | `economics_pending`, route_id null |
| **Cabify** | yes | partial (Cartagena↔Rosario stub) | ❌ none | pending |
| **Uber** | yes — coverage node | no built corridors | ❌ none | aspirational node only |
| **inDrive** | yes — coverage node | no built corridors | ❌ none | aspirational node only |

**Key structural finding:** DiDi, Uber, Cabify, inDrive (and Lyft) have **zero finance-registry blocks at all** — none of them are in `corridors.json` yet. So this isn't a one-corridor gap; their whole economics layer is pending. My Colombia L3 additions didn't *create* this gap — they *surfaced* it, exactly as you suspected.

### Recommendation (tiered, honest)
1. **DiDi — seed now (highest value).** DiDi has the full Cartagena corridor set built; economics just pending. The grounded `yango-colombia` L3 (same waterways, same Cartagena tourism demand pool: ~855k intl + ~500k cruise pax) is **directly reusable** — copy the fare + demand records into a new `didi-colombia` block, apply DiDi's own capture rate. I've staged the reusable L3; **instantiating the block + setting capture is a Grok cascade call** (per lane split), and whether DiDi enters the transparent-sheet universe is your scope call.
2. **Cabify — seed light.** One built corridor; same treatment, smaller.
3. **Uber / inDrive — hold (null beats wrong).** Cartagena is an aspirational coverage node with no built corridor set. Seeding economics would be confidently-wrong. Add when/if their corridors are built.

**No other geography needs cross-partner action** — Peru and the four African/LatAm roll-ups are Yango-exclusive.

## What I did *not* do (and why)
I did **not** unilaterally instantiate `didi-colombia` / `cabify-colombia` finance blocks. These four partners have no finance presence at all, and capture-rate + sheet-inclusion are modeling/scope decisions in Grok's cascade lane — inventing them would violate null-beats-wrong. The grounded L3 (the hard, sourcing-heavy part) is done and staged; Grok can instantiate on your go.
