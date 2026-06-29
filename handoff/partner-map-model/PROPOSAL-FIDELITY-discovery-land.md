# Proposal fidelity — discovery-land

**Verdict:** TRIM
**Checked:** 2026-06-29T12:38:42Z

## Summary

- Items audited: 40
- KEEP: 38
- DROP: 2
- DEFER: 0
- TRIM/REWRITE: 0
- BP-binding errors: 2

## Trim list

| Surface | Phase | Corridor | Route | Rec | Flags |
|---------|-------|----------|-------|-----|-------|
| journey | — | Nassau & The Bahamas → Nassau & The Bahamas | `ics-3e84761396` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Nassau & The Bahamas' → 'Nas |
| journey | — | Miami → Nassau | `edge__miami-florida-usa__nassau-bahamas` | **KEEP** | — |
| featured | 1 | Nassau & The Bahamas → Nassau & The Bahamas | `ics-3e84761396` | **DROP** | bp_binding: labels ≠ route endpoints: card 'Nassau & The Bahamas' → 'Nas |
| featured | 2 | Miami → Nassau & The Bahamas | `edge__miami-florida-usa__nassau-bahamas` | **KEEP** | — |
| featured | 3 | Governor's Harbour Airport → Governor's Harbour Fe | `ics-582bb891bc` | **KEEP** | — |
| journey | market:nassau-bahamas | Marsh Harbour → Baker's Bay (Great Guana Cay) | `—` | **KEEP** | — |
| journey | market:nassau-bahamas | Treasure Cay → Baker's Bay | `—` | **KEEP** | — |
| journey | market:nassau-bahamas | Baker's Bay → Hope Town / Elbow Cay | `—` | **KEEP** | — |
| journey | market:nassau-bahamas | Marsh Harbour Airport jetty → Baker's Bay villas | `—` | **KEEP** | — |
| featured | nassau-bahamas/p1 | Marsh Harbour ↔ Baker's Bay (Great Guana Cay) | `—` | **KEEP** | — |
| featured | nassau-bahamas/p1 | Treasure Cay ↔ Baker's Bay | `—` | **KEEP** | — |
| featured | nassau-bahamas/p1 | Baker's Bay ↔ Hope Town / Elbow Cay | `—` | **KEEP** | — |
| featured | nassau-bahamas/p2 | Marsh Harbour Airport jetty ↔ Baker's Bay villas | `—` | **KEEP** | — |
| featured | nassau-bahamas/p3 | Marsh Harbour ↔ Baker's Bay (Great Guana Cay) | `—` | **KEEP** | — |
| featured | nassau-bahamas/p3 | Treasure Cay ↔ Baker's Bay | `—` | **KEEP** | — |
| featured | nassau-bahamas/p3 | Baker's Bay ↔ Hope Town / Elbow Cay | `—` | **KEEP** | — |
| journey | market:los-cabos-mexico | San José del Cabo → Costa Palmas Marina | `—` | **KEEP** | — |
| journey | market:los-cabos-mexico | Cabo San Lucas → Costa Palmas | `—` | **KEEP** | — |
| journey | market:los-cabos-mexico | Costa Palmas Marina → East Cape dive & beach clubs | `—` | **KEEP** | — |
| featured | los-cabos-mexico/p1 | San José del Cabo ↔ Costa Palmas Marina | `—` | **KEEP** | — |
| featured | los-cabos-mexico/p1 | Cabo San Lucas ↔ Costa Palmas | `—` | **KEEP** | — |
| featured | los-cabos-mexico/p1 | Costa Palmas Marina ↔ East Cape dive & beach clubs | `—` | **KEEP** | — |
| featured | los-cabos-mexico/p2 | San José del Cabo ↔ Costa Palmas Marina | `—` | **KEEP** | — |
| featured | los-cabos-mexico/p2 | Cabo San Lucas ↔ Costa Palmas | `—` | **KEEP** | — |
| featured | los-cabos-mexico/p2 | Costa Palmas Marina ↔ East Cape dive & beach clubs | `—` | **KEEP** | — |
| featured | los-cabos-mexico/p3 | San José del Cabo ↔ Costa Palmas Marina | `—` | **KEEP** | — |
| featured | los-cabos-mexico/p3 | Cabo San Lucas ↔ Costa Palmas | `—` | **KEEP** | — |
| featured | los-cabos-mexico/p3 | Costa Palmas Marina ↔ East Cape dive & beach clubs | `—` | **KEEP** | — |
| journey | market:antigua-barbuda | Antigua (St. John's) → Barbuda Ocean Club | `—` | **KEEP** | — |
| journey | market:antigua-barbuda | Codrington → Barbuda Ocean Club | `—` | **KEEP** | — |
| journey | market:antigua-barbuda | Barbuda Ocean Club → Frigate Bird Sanctuary | `—` | **KEEP** | — |
| featured | antigua-barbuda/p1 | Antigua (St. John's) ↔ Barbuda Ocean Club | `—` | **KEEP** | — |
| featured | antigua-barbuda/p1 | Codrington ↔ Barbuda Ocean Club | `—` | **KEEP** | — |
| featured | antigua-barbuda/p1 | Barbuda Ocean Club ↔ Frigate Bird Sanctuary | `—` | **KEEP** | — |
| featured | antigua-barbuda/p2 | Antigua (St. John's) ↔ Barbuda Ocean Club | `—` | **KEEP** | — |
| featured | antigua-barbuda/p2 | Codrington ↔ Barbuda Ocean Club | `—` | **KEEP** | — |
| featured | antigua-barbuda/p2 | Barbuda Ocean Club ↔ Frigate Bird Sanctuary | `—` | **KEEP** | — |
| featured | antigua-barbuda/p3 | Antigua (St. John's) ↔ Barbuda Ocean Club | `—` | **KEEP** | — |
| featured | antigua-barbuda/p3 | Codrington ↔ Barbuda Ocean Club | `—` | **KEEP** | — |
| featured | antigua-barbuda/p3 | Barbuda Ocean Club ↔ Frigate Bird Sanctuary | `—` | **KEEP** | — |
