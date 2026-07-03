# GROK SPEC — R2 Seed-and-Seal · calmac

**Lane:** Grok geometry (mint new BPs + route + seal at 0 km land, hand-waypoints).
**Source:** https://en.wikipedia.org/wiki/Caledonian_MacBrayne (Routes table)
**Discipline:** ID-based match only; null-beats-wrong; inherit real network 1:1; never invent corridors. Approx seed coords below — geocode precisely, keep names authoritative.

## Existing BPs (reuse — do NOT re-mint)
- `bp-32d27b20cb` — Ardrossan
- `bp-de106c7bbc` — Brodick
- `bp-0f2025a2a5` — Wemyss Bay
- `bp-e1ce1ab4fb` — Rothesay
- `bp-7816c29753` — Gourock
- `bp-6b68f29ca5` — Dunoon

## New BPs to mint (41)
- **Portavadie** — seed `cm-portavadie` — ~(55.872, -5.317)
- **Tarbert (Loch Fyne)** — seed `cm-tarbert` — ~(55.865, -5.409)
- **Kilcreggan** — seed `cm-kilcreggan` — ~(55.984, -4.834)
- **Colintraive** — seed `cm-colintraive` — ~(55.92, -5.156)
- **Rhubodach (Bute)** — seed `cm-rhubodach` — ~(55.923, -5.16)
- **Largs** — seed `cm-largs` — ~(55.794, -4.87)
- **Cumbrae Slip** — seed `cm-cumbrae` — ~(55.783, -4.899)
- **Troon** — seed `cm-troon` — ~(55.548, -4.679)
- **Claonaig** — seed `cm-claonaig` — ~(55.75, -5.387)
- **Lochranza (Arran)** — seed `cm-lochranza` — ~(55.707, -5.302)
- **Tayinloan** — seed `cm-tayinloan` — ~(55.636, -5.672)
- **Ardminish (Gigha)** — seed `cm-ardminish` — ~(55.675, -5.735)
- **Kennacraig** — seed `cm-kennacraig` — ~(55.801, -5.483)
- **Port Ellen (Islay)** — seed `cm-port-ellen` — ~(55.627, -6.188)
- **Port Askaig (Islay)** — seed `cm-port-askaig` — ~(55.846, -6.106)
- **Scalasaig (Colonsay)** — seed `cm-scalasaig` — ~(56.068, -6.188)
- **Feolin (Jura)** — seed `cm-feolin` — ~(55.845, -6.115)
- **Oban** — seed `cm-oban` — ~(56.412, -5.473)
- **Craignure (Mull)** — seed `cm-craignure` — ~(56.47, -5.708)
- **Achnacroish (Lismore)** — seed `cm-lismore` — ~(56.51, -5.49)
- **Arinagour (Coll)** — seed `cm-coll` — ~(56.617, -6.517)
- **Scarinish (Tiree)** — seed `cm-tiree` — ~(56.487, -6.808)
- **Fishnish (Mull)** — seed `cm-fishnish` — ~(56.51, -5.825)
- **Lochaline** — seed `cm-lochaline` — ~(56.539, -5.777)
- **Tobermory (Mull)** — seed `cm-tobermory` — ~(56.623, -6.064)
- **Kilchoan** — seed `cm-kilchoan` — ~(56.688, -6.09)
- **Mallaig** — seed `cm-mallaig` — ~(57.006, -5.828)
- **Armadale (Skye)** — seed `cm-armadale` — ~(57.064, -5.897)
- **Sconser (Skye)** — seed `cm-sconser` — ~(57.312, -6.11)
- **Raasay** — seed `cm-raasay` — ~(57.35, -6.08)
- **Uig (Skye)** — seed `cm-uig` — ~(57.586, -6.372)
- **Lochmaddy (North Uist)** — seed `cm-lochmaddy` — ~(57.596, -7.16)
- **Tarbert (Harris)** — seed `cm-tarbert-harris` — ~(57.899, -6.797)
- **Lochboisdale (South Uist)** — seed `cm-lochboisdale` — ~(57.153, -7.308)
- **Castlebay (Barra)** — seed `cm-castlebay` — ~(56.954, -7.483)
- **Eriskay** — seed `cm-eriskay` — ~(57.072, -7.305)
- **Ardmhor (Barra)** — seed `cm-ardmhor` — ~(57.029, -7.402)
- **Leverburgh (Harris)** — seed `cm-leverburgh` — ~(57.766, -7.023)
- **Berneray** — seed `cm-berneray` — ~(57.713, -7.178)
- **Ullapool** — seed `cm-ullapool` — ~(57.895, -5.16)
- **Stornoway (Lewis)** — seed `cm-stornoway` — ~(58.209, -6.386)

## Corridors to seal (27)
- ▸ **Portavadie ↔ Tarbert (Loch Fyne)**
- ▸ **Gourock ↔ Kilcreggan**
- ▸ **Colintraive ↔ Rhubodach (Bute)**
- ▸ **Largs ↔ Cumbrae Slip**
- ▸ **Troon ↔ Brodick**
- ▸ **Claonaig ↔ Lochranza (Arran)**
- ▸ **Tayinloan ↔ Ardminish (Gigha)**
- ▸ **Kennacraig ↔ Port Ellen (Islay)**
- ▸ **Kennacraig ↔ Port Askaig (Islay)**
- ▸ **Port Askaig (Islay) ↔ Scalasaig (Colonsay)**
- ▸ **Port Askaig (Islay) ↔ Feolin (Jura)**
- ▸ **Oban ↔ Scalasaig (Colonsay)**
- ▸ **Oban ↔ Craignure (Mull)**
- ▸ **Oban ↔ Achnacroish (Lismore)**
- ▸ **Oban ↔ Arinagour (Coll)**
- ▸ **Arinagour (Coll) ↔ Scarinish (Tiree)**
- ▸ **Fishnish (Mull) ↔ Lochaline**
- ▸ **Tobermory (Mull) ↔ Kilchoan**
- ▸ **Mallaig ↔ Armadale (Skye)**
- ▸ **Sconser (Skye) ↔ Raasay**
- ▸ **Uig (Skye) ↔ Lochmaddy (North Uist)**
- ▸ **Uig (Skye) ↔ Tarbert (Harris)**
- ▸ **Oban ↔ Castlebay (Barra)**
- ▸ **Oban ↔ Lochboisdale (South Uist)**
- ▸ **Ardmhor (Barra) ↔ Eriskay**
- ▸ **Leverburgh (Harris) ↔ Berneray**
- ▸ **Ullapool ↔ Stornoway (Lewis)**

## Hand-waypoint guidance
All crossings are open-water Firth of Clyde, Sound of Bute, Kilbrannan Sound, Sound of Islay/Jura, Firth of Lorne, Sound of Mull, Sound of Sleat, Little Minch, and The Minch. Hand-waypoint any corridor whose great-circle clips a headland or island: Oban↔Craignure (route W of Kerrera, through Sound of Kerrera then Firth of Lorne); Oban↔Colonsay/Barra (S around Kerrera); Tobermory↔Kilchoan (Sound of Mull mouth); Uig↔Lochmaddy/Tarbert (Little Minch, clear of Trotternish). Never cross Kintyre/Cowal/Mull land.

## Write-back
- Bind `route_id`/`route_ids` per corridor into `data-clean/partners/calmac.json` + partner-pitch tree; `_link_status: sealed`.
- Serialization: data-clean ascii/indent2/newline; partner-pitch non-ascii/indent2/newline.
- Re-run land QA; confirm 0 crossings; append receipts to gap table.