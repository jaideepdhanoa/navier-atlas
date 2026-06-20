# Noon / Reliance / Adani next slice — 2026-06-20

This is the next execution slice for PR #58 after the India partner normalization and Grok handoff. It keeps the same posture: exactness over coverage, display only from existing Atlas/accepted geometry, and overlay-only where the partner evidence is asset/platform-level rather than a current marine operating footprint.

## 1) Noon — proceed UAE-first

**Decision:** build **Noon UAE-first** from the UAE/Gulf spine, using Careem-style mechanics but with platform/commerce framing rather than ride-hail framing.

**Why this is safe:** the Noon app listing presents Noon as a shopping / grocery / food / delivery platform in **UAE, Saudi Arabia, and Egypt**, with fast-delivery products such as **noon Minutes**, **NowNow**, **noon Food**, **noon Send**, and OUT. The developer footprint is Dubai-based. That supports a UAE-first platform proposal without inventing local marine operations.

**Atlas inheritance from current UAE/Gulf spine:**

- `usable_by_noon = true` and geometry-present routes: **484**
- Domestic UAE intra-city: **452**
- Inter-emirate UAE: **18**
- UAE/Gulf cross-border: **14**

**Noon scope rule:**

- Start with domestic UAE + selected inter-emirate routes.
- Keep cross-border as amber/roadmap unless regulatory and vessel gates pass.
- KSA and Egypt stay as `coverage_note` / future scope until exact Atlas overlap and local use cases are validated.
- Do **not** present Noon as a marine operator; present it as a commerce/logistics super-app that can activate waterfront quick-commerce, concierge, resort, event, and premium-transfer use cases.

**Proposal phases:**

1. **Prove:** Dubai / Abu Dhabi / RAK waterfront delivery and concierge-transfer pilots from sealed domestic UAE geometry.
2. **Scale:** inter-emirate waterfront corridors and high-density resort/event nodes where N30 routes are commercial-now.
3. **Mature:** platform TAM from selected marine mobility + premium logistics / experience GMV; KSA/Egypt only after grounding.

## 2) Reliance — keep overlay-only

**Decision:** Reliance is not a rideshare-style or consumer marine mobility footprint for this pass. Keep it as an overlay/gap queue until exact business-owner + corridor binds are clean.

**Source-backed facts:** Reliance’s official site supports:

- Jamnagar as the world’s largest integrated single-location refining complex.
- Reliance Retail as India’s largest retailer with omni-channel presence.
- Jio as a national-scale digital services platform.

**Allowed exact-bind candidates:**

- **Gujarat / Jamnagar-Sikka:** industrial/coastal logistics overlay; candidate for asset-supported exact-bind work.
- **Mumbai:** possible corporate / consumer platform narrative on existing Atlas baseline, but brief-only until exact marine use case is validated.

**Do not do:**

- Do not infer nationwide marine mobility from Jio/Retail national footprint.
- Do not add Reliance to Goa, Kerala, Andaman, or Mumbai as if it were Rapido/Ola/Uber.
- Do not materialize economics until the exact corridors and buyer/use-case owner are chosen.

## 3) Adani — overlay-only, but strong exact-bind backlog

**Decision:** Adani Ports has strong official asset evidence, but it is still an **asset/port overlay**, not a consumer operating footprint. Bind exact assets where they overlap accepted India lanes; otherwise keep in backlog.

**Official source:** Adani Ports’ ports-and-terminals page states APSEZ operates **19 ports and terminals**, including **15 in India**, and lists the relevant Indian locations.

**Exact-bind lanes:**

| Lane | Official Adani assets | Status |
|---|---|---|
| Gujarat | Mundra, Tuna, Dahej, Hazira | Active exact-bind lane; do not fabricate BP/corridor geometry |
| Goa | Mormugao | Overlay on Goa marquee expansion; not consumer mobility footprint |
| Kerala | Vizhinjam | Can overlay existing Kerala baseline after exact geometry/use-case review |
| Tamil Nadu / Chennai | Ennore, Kattupalli, Karaikal | Active exact-bind lane |
| Andhra / Vizag | Gangavaram, Krishnapatnam | Active exact-bind lane; map to Vizag/Andhra only after exact hierarchy match |
| West Bengal / Kolkata-Haldia | Haldia | Active exact-bind lane |
| Odisha | Dhamra, Gopalpur | Source-supported but outside current named India additions; backlog unless green-lit |

## 4) Grok deterministic tasks

- Create Noon proposal skeleton from UAE-first scope; derive `scope_city_ids` from UAE/Gulf spine, not hand-listed city arrays.
- Reconcile `usable_by_noon` candidates: domestic UAE and inter-emirate first; cross-border only amber/roadmap unless regulatory gate passes.
- Add Reliance / Adani overlay ledgers as exact-bind/backlog inputs, not display partner map footprints.
- For Adani assets overlapping active India lanes, produce ID/alias/provenance crosswalk: `OK`, `ID_MISMATCH`, `MISSING_GEOMETRY`, or `HELD`.
- Run vessel re-gating and 0-land-crossing checks after any route promotion.
- Run economics cascade only after accepted scope and route IDs are final; build economics sidecar into the gold export.

## Source notes

- Noon app listing: `https://play.google.com/store/apps/details?id=com.noon.buyerapp&hl=en_US`
- Reliance official site: `https://www.ril.com/`
- Adani Ports official locations: `https://www.adaniports.com/ports-and-terminals`

Structured companion artifact: `noon-reliance-adani-next-slice-2026-06-20.json`.
