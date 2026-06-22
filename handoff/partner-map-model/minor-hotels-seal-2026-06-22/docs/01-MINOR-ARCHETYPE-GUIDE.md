# Minor Hotels — the Hotel-Developer Archetype (read this first)

> **One line:** Minor is **not** a ride-hail or super-app partner. It is a **hotel developer/operator**, so
> its marine network is a **captive intra-portfolio graph** — routes only **from its own hotels**, **between
> its own hotels**, and **from a hotel to a signature excursion** — sized by **guest throughput**, never by a
> city's mobility pool.

This is a **new partner archetype** for Atlas. Everything sealed to date (Grab, Uber, Bolt, Yango, Careem)
is a *mobility platform* whose TAM is a **contested** share of a city's whole transport spend (~10% capture).
The Maldives/JIH and French-Polynesia cover-cases are the closest precedent because they are **captive
hospitality**, but Minor is bigger and multi-brand: ~221 properties, 109 coastal-relevant, across 6 clusters.
Treat Minor as **archetype = `hospitality_developer`** (captive), and inherit the captive-economics rules
below — do **not** run it through the ride-hail `inherit-markets` parity path.

---

## 1. The route-construction rule (the thing to get exactly right)

Build **only** these three route classes, and **only** with a Minor property on at least one endpoint:

| Class | Endpoints | Example | Capture band |
|---|---|---|---|
| **A. Gateway transfer** | airport / city seaport ↔ **Minor property** | Malé airport → Anantara Veli; Phuket Intl seaport → Avadina jetty | **captive ~0.85–0.90** (resort owns the arrival) |
| **B. Intra-portfolio hop** | **Minor property** ↔ **Minor property** | Anantara Bazaruto ↔ Anantara Medjumbe; Phuket inter-resort | **captive ~0.90** (same guest, same brand) |
| **C. Signature excursion** | **Minor property** ↔ marquee day-trip node | Bali Uluwatu → Nusa Penida; Tangalle → Mirissa whale grounds | **captive 0.60–0.85** (discretionary, resort-curated) |

**Hard exclusions — do NOT build:**
- ❌ Generic city-pair mobility (commuter, airport-for-everyone, point-to-point public transfer). That is the
  ride-hail archetype; it does not belong on a Minor proposal.
- ❌ Any route where **neither endpoint is a Minor property or a Minor-curated excursion node**.
- ❌ "Network completeness" legs that connect two non-Minor nodes just because geometry exists.
- ❌ Borrowing a contested mobility corridor from Bolt/Yango/Grab and re-skinning it as Minor.

**Endpoint identity is the gate.** A leg qualifies only if you can name the **Minor property** (by inventory
`property_name` / bound `atlas_registry_key`) on at least one end. If you cannot, the leg is **null**, not a
guess. Property-origin BPs that lack resort-jetty geometry stay **city-market / cluster-level** binds or
future-BP candidates — do not invent jetty coordinates.

---

## 2. Economics: throughput-bounded, captive-capture (inherit LB-254)

A hotel developer's TAM is **not** `city_mobility_pool × capture`. It is bounded by **how many guests the
properties actually move**:

```
annual premium marine trips  =  Σ_property [ keys × occupancy × (1/avg_LOS) × marine_transfer_attach × 2 ]
SOM floor (grounded)         =  annual marine trips × blended_fare × captive_capture
```

- **Captive capture (~0.85–0.90)** for Class A/B because the resort controls the arrival/inter-property
  transfer. Class C excursions take a lower discretionary band (0.60–0.85).
- **LB-254 applies in full.** Because the floor is built at ~90% capture, the TAM ladder MUST anchor
  `M_today` on the true `transport_spend_pool_yr` (Σ demand×fare), **never** `floor / 0.10`. Dividing a
  90%-capture floor by 0.10 inflates every rung ~9×. **At 90% capture the floor already ≈ the whole pool —
  you cannot also multiply by 10.**
- **Headroom = WIDTH, not capture-share.** Growth comes from **more keys, more properties (incl.
  under-construction pipeline), induced guest demand, and new clusters** — never from "maturing capture from
  10%→40%." The contested 0.15/0.25/0.40 ramp is **wrong-signed** for Minor.
- **The grounded floor never moves.** It is the honest number we sell. Only inflated upper rungs come down.
- **Sanity gate:** a cluster whose journey-GMV TAM exceeds its host region's whole **luxury-transfer**
  economy is the tell — re-check the capture anchor.
- **`materialize_partner_economics.py` precedent:** this is the `captive-maldives` pattern generalized — filter
  the shared corridor network to **Minor's own property set per cluster** (a brand/property filter), so a
  2-property cluster never inherits an entire archipelago's fleet. If a cluster's properties aren't bound to
  geometry yet, it materializes **nothing** (honest null) until the bind lands.
- **`country-reference.json` preflight is mandatory.** Minor spans Thailand, UAE, Indonesia, Mozambique,
  Italy, Slovenia, Croatia, Spain, Sri Lanka, Brazil, Australia, Vietnam, Kenya(held), Maldives. Any country
  missing a row silently inherits **Singapore** opex → confidently-wrong. Add honest source-tiered rows
  before any cascade. (UAE, Thailand, Indonesia rows confirmed present; verify the Med/Adriatic + Mozambique
  + Brazil + Australia rows.)
- **Vessel range-gate every leg:** ≤70nm → N30 Pioneer II (N35 Shuttle on dense Scale legs); 75–150nm →
  Quanta-LR (amber/roadmap); >150nm → Quanta-LR flagged. Most resort transfers are ≤70nm → Pioneer II.
- **CAPEX region rule:** US+EU = $900K/vessel; everywhere else = $600K, keyed by corridor country.

---

## 3. What's already grounded (don't re-derive — these are inputs)

Three flagship economics floors are drafted (grounded, captive band):

| Cluster | Grounded SOM floor (mid) | Minor props | Atlas state |
|---|---|---|---|
| **Phuket / Phang Nga (TH)** | **$4.38M / yr** | 8 | `economics_ready` |
| **Palm Jumeirah (UAE)** | **$3.75M / yr** | 3 | ⚠ Palm submarket `needs_bp_route_grounding` (parent dubai-uae routed) |
| **Bali (ID)** | **$0.63M / yr** | 3 | `economics_ready` |

These are the **floor**, not the ceiling — the multiyear ramp adds the 9 pipeline (under-construction)
assets and the seeded markets as WIDTH. Grok runs the deterministic model→deck cascade on these; Tasklet
supplies the floors + assumptions, not hand-cranked recurring numbers.
