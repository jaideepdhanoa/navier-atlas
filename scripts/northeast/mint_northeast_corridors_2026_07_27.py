#!/usr/bin/env python3
"""Northeast USA expansion — mint 5 corridors + 1 boarding point (2026-07-27).

Fills the geometry gaps identified in the approved fare-anchor table
(northeast program, Jaideep approval 2026-07-27):
  R1 E 34th St (Manhattan) -> LGA Marine Air Terminal        [new BP: LGA MAT]
  R2 Wall St / Pier 11    -> Sag Harbor (Long Wharf)
  R3 Wall St / Pier 11    -> Montauk (Viking Fleet Dock)
  R4 Long Wharf (Boston)  -> Hingham Shipyard
  R5 Seastreak New Bedford -> Oak Bluffs (SSA Terminal)

Also fills the empty `bos-long-wharf|bos-hingham` key flagged in PR #251
(waypoints exported to data-clean/northeast_expansion_hand_waypoints.json).

Validation: the global land mask is too coarse for tight urban channels
(it reports Rikers Island as water), so geometry acceptance is hand
waypoints + high-zoom visual QA (Singapore standard). The mask check is
retained as a coarse backstop only.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[0]
# repo root passed as argv[1], default /tmp/na
REPO = Path(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else Path("/tmp/na")
sys.path.insert(0, str(REPO / "scripts/grok-bolt-yango"))

from bolt_yango_routing_shared import (  # noqa: E402
    LAND_THRESH_KM,
    interior_land_km,
    load_json,
    load_land_mask,
    make_route_feature,
    path_length_km,
    route_features,
    save_json,
    save_routes,
)

DC = REPO / "data-clean"
SEAL_LANE = "northeast-expansion-2026-07-27"
NOW = datetime.now(timezone.utc).isoformat()

LGA_BP = {
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [-73.8858, 40.7736]},
    "properties": {
        "id": "bp-lga-marine-air",
        "bp_type": "ferry-terminal",
        "confidence": "high",
        "coords_resolved": True,
        "display_type": "ferry-terminal",
        "fullName": "LGA Marine Air Terminal (Bowery Bay)",
        "name": "LGA Marine Air Terminal (Bowery Bay)",
        "shortName": "LGA Marine Air",
        "parent_city_id": "new-york-harbor-usa",
        "source_url": "https://en.wikipedia.org/wiki/Marine_Air_Terminal",
        "status": "proposed",
        "type": "poi",
        "_seal_lane": SEAL_LANE,
        "last_enriched": NOW,
    },
}

BP = {
    "e34": ("bp-5f0981ff77", "East 34th Street (Manhattan)", [-73.971, 40.743], "new-york-harbor-usa"),
    "lga": ("bp-lga-marine-air", "LGA Marine Air Terminal (Bowery Bay)", [-73.8858, 40.7736], "new-york-harbor-usa"),
    "pier11": ("bp-58a56df431", "Wall Street / Pier 11 (Manhattan)", [-74.0085, 40.703], "new-york-harbor-usa"),
    "sag": ("bp-505629a487", "Long Wharf (Sag Harbor Village Dock)", [-72.2919, 41.003], "the-hamptons-east-end-usa"),
    "mtk": ("bp-55f162ae8f", "Viking Fleet Dock — Montauk Harbor", [-71.9415796, 41.0715971], "the-hamptons-east-end-usa"),
    "bos_lw": ("bp-98fe0af19b", "Long Wharf", [-71.05, 42.36], "boston-new-england-usa"),
    "hingham": ("bp-cb7113ff22", "Hingham Shipyard", [-70.9192, 42.254], "boston-new-england-usa"),
    "nb": ("bp-41b26f2bfc", "Seastreak Ferry Terminal at New Bedford", [-70.919879, 41.635409], "boston-new-england-usa"),
    "ob": ("bp-83a62832de", "Steamship Authority Oak Bluffs Terminal", [-70.5559054, 41.4579385], "cape-cod-islands-usa"),
}

# East River spine shared by R2/R3: Pier 11 -> Hell Gate via the west
# (Manhattan-side) channel around Roosevelt Island.
EAST_RIVER_UP = [
    [-74.0020, 40.7065],
    [-73.9930, 40.7105],
    [-73.9790, 40.7130],
    [-73.9700, 40.7185],
    [-73.9660, 40.7280],
    [-73.9680, 40.7380],
    [-73.9640, 40.7470],
    [-73.9585, 40.7555],
    [-73.9520, 40.7625],
    [-73.9465, 40.7700],
    [-73.9415, 40.7745],
    [-73.9360, 40.7790],  # Hell Gate
]
# Hell Gate -> NE mid-channel (Astoria shore S, Port Morris/Bronx N), south of
# South Brother Island, then the Rikers Island Channel entrance.
RIKERS_CHANNEL_E = [
    [-73.9310, 40.7865],
    [-73.9200, 40.7905],
    [-73.9080, 40.7910],
    [-73.8985, 40.7895],
    [-73.8940, 40.7875],
]
# Rikers channel -> east past Rikers, Whitestone, around Throgs Neck tip -> LI Sound -> Plum Gut
SOUND_TO_PLUM_GUT = [
    [-73.8880, 40.7865],
    [-73.8790, 40.7870],
    [-73.8680, 40.7900],
    [-73.8560, 40.7950],
    [-73.8400, 40.8000],
    [-73.8330, 40.8015],  # Whitestone Bridge
    [-73.8150, 40.8020],
    [-73.7970, 40.8000],
    [-73.7880, 40.8020],  # SE of Throgs Neck tip (Fort Schuyler)
    [-73.7760, 40.8170],
    [-73.7620, 40.8360],  # NW of Kings Point (Great Neck) tip
    [-73.7450, 40.8550],
    [-73.7260, 40.8740],  # between Execution Rocks and Sands Point
    [-73.6900, 40.9000],
    [-73.6200, 40.9250],
    [-73.5400, 40.9600],
    [-73.4400, 40.9950],
    [-73.3200, 41.0300],
    [-73.1800, 41.0650],
    [-73.0400, 41.0900],
    [-72.9000, 41.1050],
    [-72.7600, 41.1200],
    [-72.6200, 41.1350],
    [-72.4800, 41.1500],
    [-72.3600, 41.1600],
    [-72.2700, 41.1650],
    [-72.2150, 41.1680],  # Plum Gut
]

ROUTES = [
    {
        "key": "r1-e34-lga",
        "from": "e34",
        "to": "lga",
        "coords": (
            [BP["e34"][2]]
            + [
                [-73.9668, 40.7480],
                [-73.9630, 40.7520],
                [-73.9585, 40.7555],
                [-73.9520, 40.7625],
                [-73.9465, 40.7700],
                [-73.9415, 40.7745],
                [-73.9360, 40.7790],  # Hell Gate
            ]
            + RIKERS_CHANNEL_E
            + [
                [-73.8905, 40.7850],
                [-73.8885, 40.7820],
                [-73.8870, 40.7785],
                [-73.8862, 40.7755],
            ]
            + [BP["lga"][2]]
        ),
    },
    {
        "key": "r2-pier11-sag-harbor",
        "from": "pier11",
        "to": "sag",
        "coords": (
            [BP["pier11"][2]]
            + EAST_RIVER_UP
            + RIKERS_CHANNEL_E
            + SOUND_TO_PLUM_GUT
            + [
                [-72.2250, 41.1350],  # south through Plum Gut into Gardiners Bay
                [-72.2400, 41.0950],
                [-72.2450, 41.0560],  # east of Mashomack (Shelter Island)
                [-72.2620, 41.0480],
                [-72.2755, 41.0430],  # Mashomack Pt / Cedar Pt gap
                [-72.2830, 41.0300],  # Sag Harbor Bay
                [-72.2870, 41.0180],
                [-72.2890, 41.0080],
            ]
            + [BP["sag"][2]]
        ),
    },
    {
        "key": "r3-pier11-montauk",
        "from": "pier11",
        "to": "mtk",
        "coords": (
            [BP["pier11"][2]]
            + EAST_RIVER_UP
            + RIKERS_CHANNEL_E
            + SOUND_TO_PLUM_GUT
            + [
                [-72.1600, 41.1550],  # across Block Island Sound, north of Gardiners Island
                [-72.0800, 41.1350],
                [-72.0000, 41.1100],
                [-71.9500, 41.0900],
                [-71.9352, 41.0800],  # Montauk Harbor inlet (jetties)
                [-71.9356, 41.0765],
                [-71.9366, 41.0735],
                [-71.9378, 41.0718],
                [-71.9400, 41.0714],
            ]
            + [BP["mtk"][2]]
        ),
    },
    {
        "key": "r4-longwharf-hingham",
        "from": "bos_lw",
        "to": "hingham",
        "coords": [
            BP["bos_lw"][2],
            [-71.0454, 42.3579],
            [-71.0362, 42.3536],
            [-71.0270, 42.3493],
            [-71.0178, 42.3450],
            [-71.0085, 42.3407],
            [-70.9993, 42.3364],
            [-70.9901, 42.3321],
            [-70.9809, 42.3279],
            [-70.9717, 42.3236],
            [-70.9625, 42.3193],
            [-70.9533, 42.3150],
            [-70.9440, 42.3107],  # Hull Gut (proven MBTA Hull line terminus)
            [-70.9410, 42.3040],
            [-70.9390, 42.2950],
            [-70.9345, 42.2840],
            [-70.9330, 42.2750],  # west of Bumkin Island
            [-70.9290, 42.2640],
            [-70.9250, 42.2590],
            [-70.9200, 42.2555],
            BP["hingham"][2],
        ],
    },
    {
        "key": "r5-newbedford-oakbluffs",
        "from": "nb",
        "to": "ob",
        "coords": [
            BP["nb"][2],
            [-70.9155, 41.6280],  # New Bedford harbor channel
            [-70.9120, 41.6180],
            [-70.9095, 41.6080],
            [-70.9075, 41.5950],  # hurricane barrier opening
            [-70.9020, 41.5800],
            [-70.8900, 41.5450],  # Buzzards Bay
            [-70.8750, 41.5000],
            [-70.8580, 41.4520],  # Quicks Hole north entrance
            [-70.8545, 41.4450],
            [-70.8510, 41.4380],  # Quicks Hole south exit
            [-70.8200, 41.4250],
            [-70.7500, 41.4400],  # Vineyard Sound centerline
            [-70.6800, 41.4600],
            [-70.6300, 41.4750],
            [-70.5960, 41.4870],  # round West Chop
            [-70.5750, 41.4790],
            [-70.5620, 41.4720],  # round East Chop
            [-70.5560, 41.4640],
            BP["ob"][2],
        ],
    },
]


def main() -> int:
    apply = "--apply" in sys.argv
    mask = load_land_mask()
    cities: dict[str, str] = {}

    fbt = load_json(DC / "FEATURES_BY_TYPE.json")
    for c in fbt["city"]:
        p = c.get("properties", {})
        if p.get("id"):
            cities[p["id"]] = p.get("name") or p.get("fullName") or p["id"]

    feats_obj = load_json(DC / "ROUTES.json")
    feats = route_features(feats_obj)
    existing_ids = {f["properties"].get("id") for f in feats}

    minted, waypoints_out, failures = [], {}, []
    for spec in ROUTES:
        fk, tk = spec["from"], spec["to"]
        fid, fname, _, fcity = BP[fk]
        tid, tname, _, tcity = BP[tk]
        coords = spec["coords"]
        land_km = interior_land_km(coords, mask)
        nm = path_length_km(coords) * 0.539957
        status = "OK" if land_km <= LAND_THRESH_KM else "LAND-CLIP"
        print(f"{spec['key']}: {nm:.1f} nm, interior_land={land_km:.3f} km -> {status}")
        if status != "OK":
            failures.append((spec["key"], land_km))
            continue
        feat = make_route_feature(
            fid, tid, fname, tname, fcity, tcity, coords, cities,
            source="northeast_expansion_2026_07_27", land_km=land_km,
        )
        feat["properties"]["_seal_lane"] = SEAL_LANE
        rid = feat["properties"]["id"]
        if rid in existing_ids:
            print(f"  already exists: {rid}")
            continue
        minted.append(feat)
        waypoints_out[f"{fid}|{tid}"] = coords
        print(f"  minted {rid} ({feat['properties']['edge_class']})")

    if failures:
        print(f"FAIL-CLOSED: {len(failures)} route(s) clip land; aborting mint.")
        return 2

    if not apply:
        print("(dry run — pass --apply to write)")
        return 0

    poi_ids = {p.get("properties", {}).get("id") for p in fbt["poi"]}
    if LGA_BP["properties"]["id"] not in poi_ids:
        fbt["poi"].append(LGA_BP)
        save_json(DC / "FEATURES_BY_TYPE.json", fbt)
        print("BP inserted: bp-lga-marine-air")

    feats.extend(minted)
    save_routes(DC / "ROUTES.json", feats_obj if isinstance(feats_obj, dict) else feats)
    print(f"ROUTES.json: +{len(minted)} routes")

    hw = {
        "partner": "northeast-expansion",
        "generated_at": NOW,
        "lane": SEAL_LANE,
        "policy": "hand-waypointed; high-zoom visual QA (land mask too coarse for urban channels)",
        "waypoints": waypoints_out,
        "aliases": {"bos-long-wharf|bos-hingham": "bp-98fe0af19b|bp-cb7113ff22"},
    }
    save_json(DC / "northeast_expansion_hand_waypoints.json", hw)
    print("hand waypoints written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
