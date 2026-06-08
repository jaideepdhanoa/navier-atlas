# Gold #24 — The Hamptons & East End + Chicago & Lake Michigan (autonomous lane, US batch finale)
Base: Gold #23. +2 city nodes, +9 boarding points (web-sourced), +4 inter-island heroes (5224->5228).
All N30 Pioneer II.

**The Hamptons & the East End (new node `the-hamptons-east-end-usa`):**
- Montauk Harbor (Gosman's Dock) <-> Block Island / New Harbor — 17.3nm (Viking Fast Ferry; flagship)
- Greenport (Mitchell Park) <-> Shelter Island Heights — 1.4nm (North Ferry)
- North Haven <-> Shelter Island (South Ferry dock) — 0.9nm (South Ferry)

**Chicago & Lake Michigan (new node `chicago-lake-michigan-usa`):**
- DuSable Harbor (Chicago) <-> New Buffalo Municipal Marina — 38.9nm (open-lake crossing to Harbor Country)

## Method notes
- Hamptons heroes are saltwater (Block Island Sound / Peconic) — built as clean straight-line arcs
  (mid-arc land 0.0km verified against ocean mask).
- **Chicago/Great Lakes: the solver's ocean land-mask does NOT cover freshwater lakes** (gen_anchors
  returns 0). DuSable<->New Buffalo built as manual straight densified line; path verified to hold
  lat 41.80-41.87 — well north of the Indiana shore (~41.61N) — i.e. pure open water, no land crossing.
  Authenticity preserved despite mask blind spot. (Banked as LB-40.)

## Web-sourced boarding points (new, all `last_enriched 2026-06-08`)
Viking Fleet (Montauk), Town of New Shoreham (Block Island New Harbor), Greenport Mitchell Park,
North Ferry Co., Sag Harbor Long Wharf, South Ferry Inc. (North Haven + Shelter Is. South),
Chicago Harbors (DuSable), City of New Buffalo Municipal Marina.

## Deferred (connectivity-non-blocking)
- Greenport <-> Sag Harbor — real proposed North/South Fork passenger ferry, but A* can't resolve the
  narrow channels around Shelter Island (channel-locked, same class as deferred UAE lagoon edges).
  Curated-waypoint follow-up.
- Sag Harbor <-> Montauk — dropped: no real direct passenger ferry exists (null > invented route).

Sidecar unchanged at 69 (geometry-only; no finance corridors added).
