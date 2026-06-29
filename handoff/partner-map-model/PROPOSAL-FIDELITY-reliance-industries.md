# Proposal fidelity — reliance-industries

**Verdict:** REWRITE
**Checked:** 2026-06-29T15:10:46Z

## Summary

- Items audited: 72
- KEEP: 49
- DROP: 23
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 23

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Gateway of India / Bhaucha Dhakka → Mandwa / Aliba | `ics-45ea784fef` | **KEEP** | — |
| journey | — | Gateway of India / Bhaucha Dhakka → Mandwa / Aliba | `ics-45ea784fef` | **KEEP** | — |
| journey | — | Goa → Old Goa Ferry Terminal | `ics-b6394de290` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Goa' → 'Old Goa Ferry Termin |
| journey | — | Goa → Old Goa Ferry Terminal | `—` | **KEEP** | — |
| featured | 1 | Port Blair (Haddo Wharf / Phoenix Bay Jetty) → Ros | `rn-d3c5a1881a8e` | **KEEP** | — |
| featured | 2 | Howrah ↔ Fairlie | `—` | **KEEP** | — |
| featured | 3 | Goa → Mumbai Harbour | `rn-ff5ccaf1831e` | **KEEP** | — |
| journey | market:mumbai | Mumbai Harbour → Bhaucha Dhakka (Ferry Wharf) | `ics-3964e5583e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Mumbai Harbour' → 'Bhaucha D |
| journey | market:mumbai | Elephanta Caves → Mumbai Trans-Harbour Navi Mumbai | `ics-6a150e9b8e` | **KEEP** | — |
| journey | market:mumbai | Mumbai Harbour → Bhaucha Dhakka (Ferry Wharf) | `ics-3964e5583e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Mumbai Harbour' → 'Bhaucha D |
| journey | market:mumbai | Mumbai Harbour → Bhaucha Dhakka (Ferry Wharf) | `ics-3964e5583e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Mumbai Harbour' → 'Bhaucha D |
| featured | mumbai/p1 | Mumbai Harbour → Bhaucha Dhakka (Ferry Wharf) | `ics-3964e5583e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Mumbai Harbour' → 'Bhaucha D |
| featured | mumbai/p1 | Elephanta Caves → Mumbai Trans-Harbour Navi Mumbai | `ics-6a150e9b8e` | **KEEP** | — |
| featured | mumbai/p1 | Mumbai Harbour → Bhaucha Dhakka (Ferry Wharf) | `ics-3964e5583e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Mumbai Harbour' → 'Bhaucha D |
| featured | mumbai/p2 | Mumbai Harbour → Bhaucha Dhakka (Ferry Wharf) | `ics-3964e5583e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Mumbai Harbour' → 'Bhaucha D |
| featured | mumbai/p3 | Mumbai Harbour → Bhaucha Dhakka (Ferry Wharf) | `ics-3964e5583e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Mumbai Harbour' → 'Bhaucha D |
| featured | mumbai/p3 | Elephanta Caves → Mumbai Trans-Harbour Navi Mumbai | `ics-6a150e9b8e` | **KEEP** | — |
| featured | mumbai/p3 | Mumbai Harbour → Bhaucha Dhakka (Ferry Wharf) | `ics-3964e5583e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Mumbai Harbour' → 'Bhaucha D |
| journey | market:goa | Goa → Old Goa Ferry Terminal | `ics-30e7ae3007` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Goa' → 'Old Goa Ferry Termin |
| journey | market:goa | North Goa → South Goa / Palolem / Cavelossim | `—` | **KEEP** | — |
| journey | market:goa | Mormugao Harbour → Grande Island (Bat Island) | `rn-8e3cd84b9293` | **KEEP** | — |
| journey | market:goa | Goa → Mumbai / Konkan coast | `rn-ff5ccaf1831e` | **KEEP** | — |
| featured | goa/p1 | Goa → Old Goa Ferry Terminal | `ics-30e7ae3007` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Goa' → 'Old Goa Ferry Termin |
| featured | goa/p1 | Yacht Life Goa → Camurlim Ferry Terminal | `ics-894d34e14d` | **KEEP** | — |
| featured | goa/p1 | Mormugao Harbour → Grande Island (Bat Island) | `rn-8e3cd84b9293` | **KEEP** | — |
| featured | goa/p2 | Goa → Mumbai Harbour | `rn-ff5ccaf1831e` | **KEEP** | — |
| featured | goa/p3 | Goa → Old Goa Ferry Terminal | `ics-30e7ae3007` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Goa' → 'Old Goa Ferry Termin |
| featured | goa/p3 | Yacht Life Goa → Camurlim Ferry Terminal | `ics-894d34e14d` | **KEEP** | — |
| featured | goa/p3 | Mormugao Harbour → Grande Island (Bat Island) | `rn-8e3cd84b9293` | **KEEP** | — |
| journey | market:kerala | Kerala Backwaters & Kochi → Ernakulam Boat Jetty ( | `ics-0091e0dcc0` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Kerala Backwaters & Kochi' → |
| journey | market:kerala | Kerala Backwaters & Kochi → Ernakulam Boat Jetty ( | `ics-0091e0dcc0` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Kerala Backwaters & Kochi' → |
| journey | market:kerala | Kerala Backwaters & Kochi → Ernakulam Boat Jetty ( | `ics-0091e0dcc0` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Kerala Backwaters & Kochi' → |
| journey | market:kerala | Kerala Backwaters & Kochi → Ernakulam Boat Jetty ( | `ics-0091e0dcc0` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Kerala Backwaters & Kochi' → |
| featured | kerala/p1 | Kerala Backwaters & Kochi → Ernakulam Boat Jetty ( | `ics-0091e0dcc0` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Kerala Backwaters & Kochi' → |
| featured | kerala/p1 | Kerala Backwaters & Kochi → Ernakulam Boat Jetty ( | `ics-0091e0dcc0` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Kerala Backwaters & Kochi' → |
| featured | kerala/p1 | Kerala Backwaters & Kochi → Ernakulam Boat Jetty ( | `ics-0091e0dcc0` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Kerala Backwaters & Kochi' → |
| featured | kerala/p2 | Kerala Backwaters & Kochi → Ernakulam Boat Jetty ( | `ics-0091e0dcc0` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Kerala Backwaters & Kochi' → |
| featured | kerala/p3 | Kerala Backwaters & Kochi → Ernakulam Boat Jetty ( | `ics-0091e0dcc0` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Kerala Backwaters & Kochi' → |
| featured | kerala/p3 | Kerala Backwaters & Kochi → Ernakulam Boat Jetty ( | `ics-0091e0dcc0` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Kerala Backwaters & Kochi' → |
| featured | kerala/p3 | Kerala Backwaters & Kochi → Ernakulam Boat Jetty ( | `ics-0091e0dcc0` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Kerala Backwaters & Kochi' → |
| journey | market:andaman | Junglighat Jetty → Port Blair | `rn-f6d2eee38e08` | **KEEP** | — |
| journey | market:andaman | Bambooflat Jetty → Neil / Shaheed Dweep Jetty | `ics-5b56f03a57` | **KEEP** | — |
| journey | market:andaman | Office Of Assistant Engineer Civil, Andaman Lakshd | `ics-77f233e565` | **KEEP** | — |
| journey | market:andaman | Port Blair → BookMyBoat Andaman Ferry Booking | `rn-98d8f63617ee` | **KEEP** | — |
| featured | andaman/p1 | Andaman & Nicobar Islands — India → Office Of Assi | `rn-15b477252a2a` | **KEEP** | — |
| featured | andaman/p1 | Office Of Assistant Engineer Civil, Andaman Lakshd | `ics-77f233e565` | **KEEP** | — |
| featured | andaman/p1 | Port Blair → BookMyBoat Andaman Ferry Booking | `rn-98d8f63617ee` | **KEEP** | — |
| featured | andaman/p2 | Port Blair → BookMyBoat Andaman Ferry Booking | `rn-98d8f63617ee` | **KEEP** | — |
| featured | andaman/p3 | Andaman & Nicobar Islands — India → Office Of Assi | `rn-15b477252a2a` | **KEEP** | — |
| featured | andaman/p3 | Office Of Assistant Engineer Civil, Andaman Lakshd | `ics-77f233e565` | **KEEP** | — |
| featured | andaman/p3 | Port Blair → BookMyBoat Andaman Ferry Booking | `rn-98d8f63617ee` | **KEEP** | — |
| journey | market:kolkata_hooghly_waterfront | Howrah → Shipping / Millennium Park | `rn-e9a7f7e474e3` | **KEEP** | — |
| journey | market:kolkata_hooghly_waterfront | Howrah → Fairlie | `rn-97202b12d2ce` | **KEEP** | — |
| journey | market:kolkata_hooghly_waterfront | Dakshineswar → Belur | `rn-b44cfaae1be2` | **KEEP** | — |
| journey | market:kolkata_hooghly_waterfront | Fairlie Place Ferry → Bagbazar Ghat | `rn-46a91df66302` | **KEEP** | — |
| featured | kolkata_hooghly_waterfront/p1 | Howrah → Shipping / Millennium Park | `rn-e9a7f7e474e3` | **KEEP** | — |
| featured | kolkata_hooghly_waterfront/p1 | Howrah → Fairlie | `rn-97202b12d2ce` | **KEEP** | — |
| featured | kolkata_hooghly_waterfront/p2 | Dakshineswar → Belur | `rn-b44cfaae1be2` | **KEEP** | — |
| featured | kolkata_hooghly_waterfront/p2 | Fairlie Place Ferry → Bagbazar Ghat | `rn-46a91df66302` | **KEEP** | — |
| featured | kolkata_hooghly_waterfront/p2 | Millennium Park Jetty → Chandannagar Riverfront | `rn-174af2f4a97c` | **KEEP** | — |
| featured | kolkata_hooghly_waterfront/p3 | Howrah → Shipping / Millennium Park | `rn-e9a7f7e474e3` | **KEEP** | — |
| featured | kolkata_hooghly_waterfront/p3 | Howrah → Fairlie | `rn-97202b12d2ce` | **KEEP** | — |
| featured | kolkata_hooghly_waterfront/p3 | Dakshineswar → Belur | `rn-b44cfaae1be2` | **KEEP** | — |
| journey | market:chennai_ecr_cuddalore_puducherry_coast | Napier Bridge → Kovalam Creek | `rn-6d907a5eae57` | **KEEP** | — |
| journey | market:chennai_ecr_cuddalore_puducherry_coast | Chennai Port WQIV Cruise Terminal → Marina Beach W | `rn-6e53a9fad2f1` | **KEEP** | — |
| journey | market:chennai_ecr_cuddalore_puducherry_coast | Chennai → Cuddalore Port | `rn-659673f9bc4d` | **KEEP** | — |
| journey | market:chennai_ecr_cuddalore_puducherry_coast | Chennai Port WQIV Cruise Terminal → Puducherry Por | `rn-63ec78cd9afb` | **KEEP** | — |
| featured | chennai_ecr_cuddalore_puducherry_coast/p1 | Napier Bridge → Kovalam Creek | `rn-6d907a5eae57` | **KEEP** | — |
| featured | chennai_ecr_cuddalore_puducherry_coast/p1 | Chennai Port WQIV Cruise Terminal → Marina Beach W | `rn-6e53a9fad2f1` | **KEEP** | — |
| featured | chennai_ecr_cuddalore_puducherry_coast/p2 | Chennai → Cuddalore Port | `rn-659673f9bc4d` | **KEEP** | — |
| featured | chennai_ecr_cuddalore_puducherry_coast/p2 | Chennai Port WQIV Cruise Terminal → Puducherry Por | `rn-63ec78cd9afb` | **KEEP** | — |
| featured | chennai_ecr_cuddalore_puducherry_coast/p3 | Napier Bridge → Kovalam Creek | `rn-6d907a5eae57` | **KEEP** | — |
