# Noon skeleton + Adani exact-bind crosswalk — 2026-06-20

This file converts the prior next-slice memo into deterministic inputs for Grok. It is **not** a live partner JSON replacement.

## Noon draft scope spec

**Partner:** `noon`  
**Archetype:** commerce / logistics super-app  
**Lead country:** UAE  
**Evidence tier:** country-supported + platform-model-supported  
**Primary source:** `https://play.google.com/store/apps/details?id=com.noon.buyerapp&hl=en_US`

### Scope derivation rule

Derive Noon `scope_city_ids` from:

`handoff/partner-map-model/uae-gulf-shared-corridor-spine.json`

Filter:

- `usable_by_noon = true`
- `current_geometry_status = geometry_present`

Do **not** hand-list city IDs.

### First-pass route pools

| Market key | Count | Include? | Treatment |
|---|---:|---|---|
| `domestic_uae_intra_city` | 452 | yes | commercial-now review pool |
| `inter_emirate_uae` | 18 | yes, selected | commercial-now review pool |
| `uae_gulf_cross_border` | 14 | amber only | roadmap / regulatory gated |

### Draft page framing

- **Hero:** Waterfront quick-commerce, concierge transfer, and experience logistics for the UAE’s densest marina, resort, and event districts.
- **Why now:** UAE waterfront districts concentrate high-value residents, visitors, restaurants, hotels, and events, while Noon already aggregates commerce, food, grocery, send, and fast-delivery demand in one app surface.
- **Multimodal fit:** Navier operates as the marine leg inside Noon’s same-day / minutes / send / experience layer, not as a standalone consumer ferry brand.

### Phase scaffold

1. **Prove:** Dubai / Abu Dhabi / RAK domestic waterfront routes from sealed geometry. Featured routes use `from_node_id` / `to_node_id`; `route_id = null` until seal.
2. **Scale:** selected inter-emirate waterfront resort/event links. N30 only unless re-gated.
3. **Mature:** platform GMV across marine mobility + premium delivery / experience use cases. Economics after route IDs are final.

## Adani exact-bind crosswalk

Current finding: none of the official Adani asset labels below produced an exact label hit in the current **97-route India spine**. Therefore, every active lane remains exact-bind work, not current display footprint.

| Lane | Asset | Current spine label hit | Binding verdict | Proposal status |
|---|---|---|---|---|
| Gujarat | Mundra | none_found_in_current_97_route_india_spine | MISSING_GEOMETRY_OR_UNVERIFIED_ALIAS | active_exact_bind_lane |
| Gujarat | Tuna | none_found_in_current_97_route_india_spine | MISSING_GEOMETRY_OR_UNVERIFIED_ALIAS | active_exact_bind_lane |
| Gujarat | Dahej | none_found_in_current_97_route_india_spine | MISSING_GEOMETRY_OR_UNVERIFIED_ALIAS | active_exact_bind_lane |
| Gujarat | Hazira | none_found_in_current_97_route_india_spine | MISSING_GEOMETRY_OR_UNVERIFIED_ALIAS | active_exact_bind_lane |
| Goa | Mormugao | none_found_in_current_97_route_india_spine | MISSING_GEOMETRY_OR_UNVERIFIED_ALIAS | overlay_on_goa_marquee_expansion |
| Kerala | Vizhinjam | none_found_in_current_97_route_india_spine | MISSING_GEOMETRY_OR_UNVERIFIED_ALIAS | overlay_on_existing_kerala_baseline_after_review |
| Tamil Nadu / Chennai | Ennore | none_found_in_current_97_route_india_spine | MISSING_GEOMETRY_OR_UNVERIFIED_ALIAS | active_exact_bind_lane |
| Tamil Nadu / Chennai | Kattupalli | none_found_in_current_97_route_india_spine | MISSING_GEOMETRY_OR_UNVERIFIED_ALIAS | active_exact_bind_lane |
| Tamil Nadu / Chennai | Karaikal | none_found_in_current_97_route_india_spine | MISSING_GEOMETRY_OR_UNVERIFIED_ALIAS | active_exact_bind_lane |
| Andhra / Vizag | Gangavaram | none_found_in_current_97_route_india_spine | MISSING_GEOMETRY_OR_UNVERIFIED_ALIAS | active_exact_bind_lane |
| Andhra / Vizag | Krishnapatnam | none_found_in_current_97_route_india_spine | MISSING_GEOMETRY_OR_UNVERIFIED_ALIAS | active_exact_bind_lane |
| West Bengal / Kolkata-Haldia | Haldia | none_found_in_current_97_route_india_spine | MISSING_GEOMETRY_OR_UNVERIFIED_ALIAS | active_exact_bind_lane |
| Odisha | Dhamra | none_found_in_current_97_route_india_spine | MISSING_GEOMETRY_OR_UNVERIFIED_ALIAS | backlog_outside_current_named_india_additions |
| Odisha | Gopalpur | none_found_in_current_97_route_india_spine | MISSING_GEOMETRY_OR_UNVERIFIED_ALIAS | backlog_outside_current_named_india_additions |

## Reliance overlay gate

Reliance remains held as overlay-only. There are no exact Reliance route/asset label hits in the current 97-route India spine. Jamnagar/Sikka and Mumbai remain candidate narrative lanes until exact binds and owner/use-case are validated.

## Acceptance gates

- Noon `scope_city_ids` derived from actual UAE/Gulf route endpoints only.
- Adani assets cannot render as partner footprint until crosswalk verdict is `OK` or `ID_MISMATCH` is resolved.
- Reliance cannot render or cascade economics until exact buyer/use-case plus route geometry are accepted.
- All `route_id` fields remain null until Grok seal binds real route IDs.

Structured companion artifact: `noon-skeleton-adani-crosswalk-2026-06-20.json`.
