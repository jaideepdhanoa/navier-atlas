# GROK SPEC — R1 Mint-Heavy Seal-Completion

**Lane:** Grok geometry seal only. Endpoints already minted by Tasklet; no new BP mint required.
**Task:** Route + seal each corridor below at **0 km land** (hand-waypoints where a straight line clips land). Bind `route_id` back per corridor. Re-run land QA; preserve 0-crossing record.
**Order:** rotterdam-mrdh FIRST (currently renders empty: 0 sealed).

**Serialization on write-back:** data-clean ascii/indent2/newline; partner-pitch non-ascii/indent2/newline.

## rotterdam-mrdh  (base sealed now: 0 → +3)
- **Rotterdam (Erasmusbrug) ↔ Dordrecht**  ~9.5 nm
  - from_node_id: `rtd-erasmusbrug` (Erasmusbrug (Willemsplein) Waterbus)
  - to_node_id: `rtd-dordrecht` (Dordrecht Merwekade Waterbus)
- **Rotterdam (Erasmusbrug) ↔ Kinderdijk**  ~6.0 nm
  - from_node_id: `rtd-erasmusbrug` (Erasmusbrug (Willemsplein) Waterbus)
  - to_node_id: `rtd-kinderdijk` (Kinderdijk Waterbus Stop)
- **Rotterdam (Erasmusbrug) ↔ Hoek van Holland**  ~13.4 nm
  - from_node_id: `rtd-erasmusbrug` (Erasmusbrug (Willemsplein) Waterbus)
  - to_node_id: `rtd-hoek-van-holland` (Hoek van Holland Haven)

## oslo-ruter  (base sealed now: 1 → +3)
- **Aker Brygge ↔ Nesoddtangen**  ~3.4 nm
  - from_node_id: `oslo-aker-brygge` (Aker Brygge Ferry Terminal)
  - to_node_id: `oslo-nesoddtangen` (Nesoddtangen Ferry Terminal)
- **Aker Brygge ↔ Hovedøya**  ~1.4 nm
  - from_node_id: `oslo-aker-brygge` (Aker Brygge Ferry Terminal)
  - to_node_id: `oslo-hovedoya` (Hovedøya Island Pier)
- **Aker Brygge ↔ Bygdøy**  ~1.4 nm
  - from_node_id: `oslo-aker-brygge` (Aker Brygge Ferry Terminal)
  - to_node_id: `oslo-bygdoy` (Bygdøy Ferry Pier)

## amsterdam-gvb  (base sealed now: 2 → +1)
- **Centraal Station ↔ NDSM Werf**  ~1.3 nm
  - from_node_id: `ams-centraal-ij` (Centraal Station IJ Pontoon)
  - to_node_id: `ams-ndsm` (NDSM Ferry Pontoon)

## copenhagen-movia  (base sealed now: 2 → +1)
- **Nyhavn ↔ Refshaleøen**  ~1.0 nm
  - from_node_id: `cph-nyhavn` (Nyhavn Harbour Bus Stop)
  - to_node_id: `cph-refshaleoen` (Refshaleøen Ferry Stop)

## gothenburg-vasttrafik  (base sealed now: 2 → +1)
- **Saltholmen ↔ Vrångö**  ~5.3 nm
  - from_node_id: `got-saltholmen` (Saltholmen Ferry Terminal)
  - to_node_id: `got-vrango` (Vrångö Pier)

## wellington-metlink  (base sealed now: 3 → +1)
- **Queens Wharf ↔ Seatoun**  ~3.2 nm
  - from_node_id: `wlg-queens-wharf` (Queens Wharf Ferry Terminal)
  - to_node_id: `wlg-seatoun` (Seatoun Wharf)

**Total corridors to seal: 10**

### Hand-waypoint watch (known land obstructions to route around)
- **Rotterdam ↔ Hoek van Holland**: follow Nieuwe Waterweg channel; do not cut across Maasvlakte/port land.
- **Rotterdam ↔ Kinderdijk / Dordrecht**: follow Nieuwe Maas → Noord/Beneden Merwede channels; keep off Alblasserwaard polder.
- **Oslo ↔ Nesoddtangen / Hovedøya / Bygdøy**: open Oslofjord — route clear of Hovedøya/Bleikøya islets.
- **Gothenburg Saltholmen ↔ Vrångö**: southern archipelago — thread between Styrsö/Donsö/Vrångö, no island clipping.
- **Wellington Queens Wharf ↔ Seatoun**: follow harbour, round Point Halswell; keep off Miramar Peninsula.
- **Amsterdam Centraal ↔ NDSM**: straight up the IJ, clear of Java-eiland.
- **Copenhagen Nyhavn ↔ Refshaleøen**: inner harbour channel, clear of Holmen.