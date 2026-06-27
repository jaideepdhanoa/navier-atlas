# Proposal fidelity — rapido

**Verdict:** REWRITE
**Checked:** 2026-06-27T15:00:01Z

## Summary

- Items audited: 79
- KEEP: 16
- DROP: 61
- DEFER: 1
- TRIM/REWRITE: 1
- BP-binding errors: 61

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Gateway of India → Mandwa (Alibaug) | `ics-45ea784fef` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Gateway of India' → 'Mandwa  |
| journey | — | South Mumbai (Nariman Point) → Navi Mumbai / new a | `ics-6a150e9b8e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'South Mumbai (Nariman Point) |
| journey | — | Panaji (Mandovi River) → North Goa beaches (Baga / | `ics-b6394de290` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Panaji (Mandovi River)' → 'N; geometry_preview: interior_land_km=4.60 (threshold 0.4) |
| journey | — | North Goa → South Goa (Palolem / Cavelossim) | `ics-30e7ae3007` | **DROP** | bp_binding: labels ≠ route endpoints: card 'North Goa' → 'South Goa (Pal; distance_honesty: card 28.0nm vs route 2.1nm (1233% delta) |
| journey | — | Kochi (Marine Drive) → Alleppey backwaters | `ics-0091e0dcc0` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Kochi (Marine Drive)' → 'All |
| journey | — | Port Blair (Phoenix Bay) → Havelock / Swaraj Dweep | `rn-15b477252a2a` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Port Blair (Phoenix Bay)' →  |
| featured | 1 | Port Blair ↔ Ross Island / North Bay | `rn-f6d2eee38e08` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Junglighat  |
| featured | 2 | Howrah ↔ Fairlie | `rn-97202b12d2ce` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Howrah Ferr |
| featured | 3 | Mumbai <-> Konkan/Goa (Quanta-LR) | `rn-ff5ccaf1831e` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Goa' → 'Mum |
| journey | market:mumbai | Gateway of India / Bhaucha Dhakka → Mandwa (Alibau | `ics-3964e5583e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Gateway of India / Bhaucha D |
| journey | market:mumbai | South Mumbai (Nariman Point) → Navi Mumbai / new a | `ics-6a150e9b8e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'South Mumbai (Nariman Point) |
| journey | market:mumbai | Gateway of India → Elephanta Caves | `ics-3964e5583e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Gateway of India' → 'Elephan |
| journey | market:mumbai | Mumbai → Goa | `rn-ff5ccaf1831e` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Mumbai' → 'Goa' vs route 'Go |
| featured | mumbai/p1 | Gateway of India / Bhaucha Dhakka ↔ Mandwa (Alibau | `ics-3964e5583e` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Mumbai Harb |
| featured | mumbai/p1 | South Mumbai (Nariman Point) ↔ Navi Mumbai / new a | `ics-6a150e9b8e` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Elephanta C |
| featured | mumbai/p1 | Gateway of India ↔ Elephanta Caves | `ics-3964e5583e` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Mumbai Harb |
| featured | mumbai/p2 | Mumbai ↔ Goa | `ics-3964e5583e` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Mumbai Harb |
| featured | mumbai/p3 | Gateway of India / Bhaucha Dhakka ↔ Mandwa (Alibau | `ics-3964e5583e` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Mumbai Harb |
| featured | mumbai/p3 | South Mumbai (Nariman Point) ↔ Navi Mumbai / new a | `ics-6a150e9b8e` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Elephanta C |
| featured | mumbai/p3 | Gateway of India ↔ Elephanta Caves | `ics-3964e5583e` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Mumbai Harb |
| journey | market:goa | Panaji (Mandovi River) → North Goa beaches (Baga / | `ics-30e7ae3007` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Panaji (Mandovi River)' → 'N |
| journey | market:goa | North Goa → South Goa (Palolem / Cavelossim) | `ics-30e7ae3007` | **DROP** | bp_binding: labels ≠ route endpoints: card 'North Goa' → 'South Goa (Pal; distance_honesty: card 30.0nm vs route 2.1nm (1329% delta) |
| journey | market:goa | Goa → Grande Island / Bat Island | `—` | **KEEP** | — |
| journey | market:goa | Goa → Mumbai | `rn-ff5ccaf1831e` | **KEEP** | — |
| featured | goa/p1 | Panaji (Mandovi River) ↔ North Goa beaches (Baga / | `ics-30e7ae3007` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Goa' → 'Old |
| featured | goa/p1 | North Goa ↔ South Goa (Palolem / Cavelossim) | `—` | **KEEP** | — |
| featured | goa/p1 | Goa ↔ Grande Island / Bat Island | `—` | **KEEP** | — |
| featured | goa/p2 | Goa ↔ Mumbai | `rn-ff5ccaf1831e` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Goa' → 'Mum |
| featured | goa/p3 | Panaji (Mandovi River) ↔ North Goa beaches (Baga / | `ics-30e7ae3007` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Goa' → 'Old |
| featured | goa/p3 | North Goa ↔ South Goa (Palolem / Cavelossim) | `—` | **KEEP** | — |
| featured | goa/p3 | Goa ↔ Grande Island / Bat Island | `—` | **KEEP** | — |
| journey | market:kerala | Kochi (Vyttila / Marine Drive) → Fort Kochi / Will | `ics-0091e0dcc0` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Kochi (Vyttila / Marine Driv |
| journey | market:kerala | Kochi → Alleppey (Alappuzha) backwaters | `ics-0091e0dcc0` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Kochi' → 'Alleppey (Alappuzh |
| journey | market:kerala | Kochi → Kumarakom / Vembanad Lake | `ics-0091e0dcc0` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Kochi' → 'Kumarakom / Vemban |
| journey | market:kerala | Kochi → Lakshadweep (Agatti / Kavaratti) | `ics-0091e0dcc0` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Kochi' → 'Lakshadweep (Agatt |
| featured | kerala/p1 | Kochi (Vyttila / Marine Drive) ↔ Fort Kochi / Will | `ics-0091e0dcc0` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Kerala Back |
| featured | kerala/p1 | Kochi ↔ Alleppey (Alappuzha) backwaters | `ics-0091e0dcc0` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Kerala Back |
| featured | kerala/p1 | Kochi ↔ Kumarakom / Vembanad Lake | `ics-0091e0dcc0` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Kerala Back |
| featured | kerala/p2 | Kochi ↔ Lakshadweep (Agatti / Kavaratti) | `ics-0091e0dcc0` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Kerala Back |
| featured | kerala/p3 | Kochi (Vyttila / Marine Drive) ↔ Fort Kochi / Will | `ics-0091e0dcc0` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Kerala Back |
| featured | kerala/p3 | Kochi ↔ Alleppey (Alappuzha) backwaters | `ics-0091e0dcc0` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Kerala Back |
| featured | kerala/p3 | Kochi ↔ Kumarakom / Vembanad Lake | `ics-0091e0dcc0` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Kerala Back |
| journey | market:andaman | Port Blair (Phoenix Bay) → Havelock / Swaraj Dweep | `rn-15b477252a2a` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Port Blair (Phoenix Bay)' →  |
| journey | market:andaman | Havelock → Neil / Shaheed Dweep | `ics-77f233e565` | **KEEP** | — |
| journey | market:andaman | Port Blair → Ross Island / North Bay | `rn-f6d2eee38e08` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Port Blair' → 'Ross Island / |
| journey | market:andaman | Port Blair → Diglipur (North Andaman) | `rn-98d8f63617ee` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Port Blair' → 'Diglipur (Nor |
| featured | andaman/p1 | Port Blair (Phoenix Bay) ↔ Havelock / Swaraj Dweep | `rn-15b477252a2a` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Andaman & N |
| featured | andaman/p1 | Havelock ↔ Neil / Shaheed Dweep | `ics-77f233e565` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Office Of A |
| featured | andaman/p1 | Port Blair ↔ Ross Island / North Bay | `rn-98d8f63617ee` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Port Blair' |
| featured | andaman/p2 | Port Blair ↔ Diglipur (North Andaman) | `rn-98d8f63617ee` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Port Blair' |
| featured | andaman/p3 | Port Blair (Phoenix Bay) ↔ Havelock / Swaraj Dweep | `rn-15b477252a2a` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Andaman & N |
| featured | andaman/p3 | Havelock ↔ Neil / Shaheed Dweep | `ics-77f233e565` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Office Of A |
| featured | andaman/p3 | Port Blair ↔ Ross Island / North Bay | `rn-98d8f63617ee` | **DROP** | bp_binding: labels ≠ route endpoints: card '' → '' vs route 'Port Blair' |
| journey | market:kolkata_hooghly_waterfront | Howrah → Shipping / Millennium Park | `rn-e9a7f7e474e3` | **KEEP** | — |
| journey | market:kolkata_hooghly_waterfront | Howrah → Fairlie | `rn-97202b12d2ce` | **KEEP** | — |
| journey | market:kolkata_hooghly_waterfront | Dakshineswar → Belur | `rn-b44cfaae1be2` | **KEEP** | — |
| journey | market:kolkata_hooghly_waterfront | Fairlie → Ariyadaha via Howrah / Baghbazar / Belur | `rn-46a91df66302` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Fairlie' → 'Ariyadaha via Ho; geometry_preview: interior_land_km=2.80 (threshold 0.4) |
| journey | market:kolkata_hooghly_waterfront | Millennium Park / Babughat / Princep Ghat → Herita | `rn-174af2f4a97c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Millennium Park / Babughat /; geometry_preview: interior_land_km=29.61 (threshold 0.4) |
| journey | market:kolkata_hooghly_waterfront | Kolkata riverfront → Chandannagar / Belur / Dakshi | `rn-b44cfaae1be2` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Kolkata riverfront' → 'Chand |
| featured | kolkata_hooghly_waterfront/p1 | Howrah → Shipping / Millennium Park | `rn-e9a7f7e474e3` | **KEEP** | — |
| featured | kolkata_hooghly_waterfront/p1 | Howrah → Fairlie | `rn-97202b12d2ce` | **KEEP** | — |
| featured | kolkata_hooghly_waterfront/p2 | Dakshineswar → Belur | `rn-b44cfaae1be2` | **KEEP** | — |
| featured | kolkata_hooghly_waterfront/p2 | Fairlie → Ariyadaha via Howrah / Baghbazar / Belur | `rn-46a91df66302` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Fairlie' → 'Ariyadaha via Ho; geometry_preview: interior_land_km=2.80 (threshold 0.4) |
| featured | kolkata_hooghly_waterfront/p2 | Millennium Park / Babughat / Princep Ghat → Herita | `rn-174af2f4a97c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Millennium Park / Babughat /; geometry_preview: interior_land_km=29.61 (threshold 0.4) |
| featured | kolkata_hooghly_waterfront/p3 | Howrah → Shipping / Millennium Park | `rn-e9a7f7e474e3` | **KEEP** | — |
| featured | kolkata_hooghly_waterfront/p3 | Howrah → Fairlie | `rn-97202b12d2ce` | **KEEP** | — |
| featured | kolkata_hooghly_waterfront/p3 | Dakshineswar → Belur | `rn-b44cfaae1be2` | **KEEP** | — |
| featured | kolkata_hooghly_waterfront/p3 | Fairlie → Ariyadaha via Howrah / Baghbazar / Belur | `rn-46a91df66302` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Fairlie' → 'Ariyadaha via Ho; geometry_preview: interior_land_km=2.80 (threshold 0.4) |
| featured | kolkata_hooghly_waterfront/p3 | Millennium Park / Babughat / Princep Ghat → Herita | `rn-174af2f4a97c` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Millennium Park / Babughat /; geometry_preview: interior_land_km=29.61 (threshold 0.4) |
| featured | kolkata_hooghly_waterfront/p3 | Kolkata riverfront → Chandannagar / Belur / Dakshi | `rn-b44cfaae1be2` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Kolkata riverfront' → 'Chand |
| journey | market:chennai_ecr_cuddalore_puducherry_coast | Napier Bridge → Kovalam via Buckingham Canal | `rn-6d907a5eae57` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Napier Bridge' → 'Kovalam vi |
| journey | market:chennai_ecr_cuddalore_puducherry_coast | Chennai Port / WQIV cruise terminal → Leisure voya | `rn-6e53a9fad2f1` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Chennai Port / WQIV cruise t |
| journey | market:chennai_ecr_cuddalore_puducherry_coast | Chennai → Cuddalore Port | `rn-659673f9bc4d` | **TRIM** | geometry_preview: interior_land_km=18.59 (threshold 0.4) |
| journey | market:chennai_ecr_cuddalore_puducherry_coast | Chennai → Puducherry / Pondicherry | `rn-63ec78cd9afb` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Chennai' → 'Puducherry / Pon; geometry_preview: interior_land_km=4.22 (threshold 0.4) |
| featured | chennai_ecr_cuddalore_puducherry_coast/p1 | Napier Bridge → Kovalam via Buckingham Canal | `rn-6d907a5eae57` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Napier Bridge' → 'Kovalam vi |
| featured | chennai_ecr_cuddalore_puducherry_coast/p1 | Chennai Port / WQIV cruise terminal → Leisure voya | `rn-6e53a9fad2f1` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Chennai Port / WQIV cruise t |
| featured | chennai_ecr_cuddalore_puducherry_coast/p2 | Chennai → Cuddalore Port | `rn-659673f9bc4d` | **DEFER** | geometry_preview: interior_land_km=18.59 (threshold 0.4) |
| featured | chennai_ecr_cuddalore_puducherry_coast/p2 | Chennai → Puducherry / Pondicherry | `rn-63ec78cd9afb` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Chennai' → 'Puducherry / Pon; geometry_preview: interior_land_km=4.22 (threshold 0.4) |
| featured | chennai_ecr_cuddalore_puducherry_coast/p3 | Napier Bridge → Kovalam via Buckingham Canal | `rn-6d907a5eae57` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Napier Bridge' → 'Kovalam vi |
