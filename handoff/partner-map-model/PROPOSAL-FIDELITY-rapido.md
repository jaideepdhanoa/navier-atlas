# Proposal fidelity — rapido

**Verdict:** PASS_WITH_FLAGS
**Checked:** 2026-06-29T11:29:21Z

## Summary

- Items audited: 32
- KEEP: 30
- DROP: 0
- DEFER: 1
- TRIM/REWRITE: 1
- BP-binding errors: 0

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | market:mumbai | Coastal corridor → Seal pending | `—` | **KEEP** | — |
| featured | mumbai/p1 | Corridor seal pending — roadmap | `—` | **KEEP** | — |
| featured | mumbai/p2 | Corridor seal pending — roadmap | `—` | **KEEP** | — |
| featured | mumbai/p3 | Corridor seal pending — roadmap | `—` | **KEEP** | — |
| journey | market:goa | Goa → Grande Island / Bat Island | `—` | **KEEP** | — |
| journey | market:goa | Goa → Mumbai | `rn-ff5ccaf1831e` | **KEEP** | — |
| featured | goa/p1 | North Goa ↔ South Goa (Palolem / Cavelossim) | `—` | **KEEP** | — |
| featured | goa/p1 | Goa ↔ Grande Island / Bat Island | `—` | **KEEP** | — |
| featured | goa/p2 | Corridor seal pending — roadmap | `—` | **KEEP** | — |
| featured | goa/p3 | North Goa ↔ South Goa (Palolem / Cavelossim) | `—` | **KEEP** | — |
| featured | goa/p3 | Goa ↔ Grande Island / Bat Island | `—` | **KEEP** | — |
| journey | market:kerala | Coastal corridor → Seal pending | `—` | **KEEP** | — |
| featured | kerala/p1 | Corridor seal pending — roadmap | `—` | **KEEP** | — |
| featured | kerala/p2 | Corridor seal pending — roadmap | `—` | **KEEP** | — |
| featured | kerala/p3 | Corridor seal pending — roadmap | `—` | **KEEP** | — |
| journey | market:andaman | Havelock → Neil / Shaheed Dweep | `ics-77f233e565` | **KEEP** | — |
| featured | andaman/p1 | Corridor seal pending — roadmap | `—` | **KEEP** | — |
| featured | andaman/p2 | Corridor seal pending — roadmap | `—` | **KEEP** | — |
| featured | andaman/p3 | Corridor seal pending — roadmap | `—` | **KEEP** | — |
| journey | market:kolkata_hooghly_waterfront | Howrah → Shipping / Millennium Park | `rn-e9a7f7e474e3` | **KEEP** | — |
| journey | market:kolkata_hooghly_waterfront | Howrah → Fairlie | `rn-97202b12d2ce` | **KEEP** | — |
| journey | market:kolkata_hooghly_waterfront | Dakshineswar → Belur | `rn-b44cfaae1be2` | **KEEP** | — |
| featured | kolkata_hooghly_waterfront/p1 | Howrah → Shipping / Millennium Park | `rn-e9a7f7e474e3` | **KEEP** | — |
| featured | kolkata_hooghly_waterfront/p1 | Howrah → Fairlie | `rn-97202b12d2ce` | **KEEP** | — |
| featured | kolkata_hooghly_waterfront/p2 | Dakshineswar → Belur | `rn-b44cfaae1be2` | **KEEP** | — |
| featured | kolkata_hooghly_waterfront/p3 | Howrah → Shipping / Millennium Park | `rn-e9a7f7e474e3` | **KEEP** | — |
| featured | kolkata_hooghly_waterfront/p3 | Howrah → Fairlie | `rn-97202b12d2ce` | **KEEP** | — |
| featured | kolkata_hooghly_waterfront/p3 | Dakshineswar → Belur | `rn-b44cfaae1be2` | **KEEP** | — |
| journey | market:chennai_ecr_cuddalore_puducherry_coast | Chennai → Cuddalore Port | `rn-659673f9bc4d` | **TRIM** | geometry_preview: interior_land_km=18.59 (threshold 0.4) |
| featured | chennai_ecr_cuddalore_puducherry_coast/p1 | Corridor seal pending — roadmap | `—` | **KEEP** | — |
| featured | chennai_ecr_cuddalore_puducherry_coast/p2 | Chennai → Cuddalore Port | `rn-659673f9bc4d` | **DEFER** | geometry_preview: interior_land_km=18.59 (threshold 0.4) |
| featured | chennai_ecr_cuddalore_puducherry_coast/p3 | Corridor seal pending — roadmap | `—` | **KEEP** | — |
