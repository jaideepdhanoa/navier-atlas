#!/usr/bin/env python3
"""Wave 2: expand bp_water_allowlist for coarse-mask pier gaps (#119)."""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DC = ROOT / "data-clean"
ALLOWLIST = DC / "bp_water_allowlist.json"
REPORT_IN = ROOT / "grok-routing-output/bp-water-adjacency-report.json"
REPORT_OUT = ROOT / "grok-routing-output/bp-allowlist-wave2-report.json"

sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
from bolt_yango_shared import is_internal_metadata_bp  # noqa: E402

WAVE2_WATER_BODIES = [
    {
        "name": "Singapore / Johor Strait / Bintan approaches",
        "bbox": [103.55, 104.45, 1.0, 1.6],
        "reason": "Strait ferry terminals, PSA/HarbourFront, Bintan/Batam landings; coarse mask misses narrow channels",
    },
    {
        "name": "Bali / Nusa / Lombok fast-boat mesh",
        "bbox": [114.75, 116.85, -9.0, -8.0],
        "reason": "Padang Bai, Sanur, Nusa Penida/Lembongan, Lombok Senggigi/Mandalika; resort jetties on reef-fringed coast",
    },
    {
        "name": "Andaman Thailand (Phuket/Krabi/Phang Nga)",
        "bbox": [97.8, 99.6, 7.4, 9.1],
        "reason": "Phuket marinas, Phi Phi/Krabi/Railay piers; mangrove estuary blind spots",
    },
    {
        "name": "Red Sea Egypt (Hurghada/Sharm/Sinai)",
        "bbox": [32.8, 35.2, 27.0, 29.0],
        "reason": "Marina/Hurghada yacht basin, Sharm cruise terminal, Sinai resort jetties",
    },
    {
        "name": "Jeddah / Red Sea KSA west coast",
        "bbox": [38.7, 39.6, 20.8, 22.2],
        "reason": "Jeddah Waterfront, Economic City marina apron; enclosed Red Sea basin",
    },
    {
        "name": "Aegean Greece (Cyclades/Dodecanese)",
        "bbox": [23.4, 26.8, 36.4, 38.6],
        "reason": "Mykonos/Santorini/Rhodes ferry quays; island pier mesh",
    },
    {
        "name": "Andaman Sea (Myanmar/Thai south)",
        "bbox": [92.4, 94.2, 11.4, 13.2],
        "reason": "Kawthaung/Ranong cross-border + Mergui archipelago approaches",
    },
    {
        "name": "Philippines inter-island (Luzon/Visayas/Mindoro)",
        "bbox": [120.0, 122.2, 12.5, 15.8],
        "reason": "Manila Bay, Batangas, Mindoro/Palawan ferry terminals",
    },
    {
        "name": "Bosphorus / Marmara (Istanbul)",
        "bbox": [28.7, 29.35, 40.85, 41.25],
        "reason": "Eminönü/Kabataş/Beşiktaş ferry piers on navigable strait",
    },
    {
        "name": "Malaysia peninsular coast (east + west)",
        "bbox": [99.0, 104.5, 2.0, 6.5],
        "reason": "Langkawi, Penang, Desaru, Tioman, Kuantan resort/marina landings",
    },
    {
        "name": "UAE / Oman Gulf coast (extended)",
        "bbox": [54.0, 56.5, 24.0, 26.5],
        "reason": "Dubai/Sharjah/Ras Al Khaimah/Muscat marina basins beyond Creek bbox",
    },
    {
        "name": "Caribbean ABC / southern Antilles",
        "bbox": [-72.0, -60.0, 10.0, 13.5],
        "reason": "Aruba/Curaçao/Bonaire cruise and inter-island piers",
    },
    {
        "name": "Croatia Adriatic",
        "bbox": [14.5, 17.5, 42.5, 45.5],
        "reason": "Split/Hvar/Dubrovnik ferry quays; narrow Adriatic channels",
    },
    {
        "name": "Italy Tyrrhenian / Amalfi / Sardinia",
        "bbox": [12.5, 16.0, 38.0, 41.5],
        "reason": "Capri/Sorrento/Porto Cervo/Cagliari marina landings",
    },
    {
        "name": "French Riviera / Corsica",
        "bbox": [6.0, 10.0, 41.0, 44.0],
        "reason": "Nice/Monaco/Cannes/Corsica ferry terminals",
    },
    {
        "name": "Florida / Gulf / Keys",
        "bbox": [-82.5, -79.5, 24.5, 30.5],
        "reason": "Miami/Biscayne, Keys ferry, Gulf resort marinas",
    },
    {
        "name": "Hawaii archipelago",
        "bbox": [-161.0, -154.5, 18.5, 22.5],
        "reason": "Inter-island harbors; reef-fringed pier approaches",
    },
    {
        "name": "Japan Seto Inland Sea / Shikoku",
        "bbox": [132.0, 135.0, 33.0, 35.0],
        "reason": "Shimanami ferry mesh; narrow strait blind spots",
    },
    {
        "name": "Vietnam coast (central + south)",
        "bbox": [106.5, 109.5, 8.5, 16.5],
        "reason": "Da Nang, Nha Trang, Phu Quoc, Vung Tau piers",
    },
    {
        "name": "Sri Lanka coast",
        "bbox": [79.5, 82.0, 5.8, 9.9],
        "reason": "Colombo/Galle/Trincomalee harbor approaches",
    },
    {
        "name": "East Africa (Mombasa / Zanzibar)",
        "bbox": [39.0, 40.5, -6.5, -4.5],
        "reason": "Lamu/Mombasa/Zanzibar dhow and ferry landings",
    },
    {
        "name": "Australia east coast (Sydney–Whitsundays)",
        "bbox": [150.0, 154.0, -28.5, -16.0],
        "reason": "Sydney Harbour, Gold Coast, Whitsunday resort piers",
    },
    {
        "name": "Stockholm archipelago / Lake Mälaren fringe",
        "bbox": [17.8, 18.4, 59.2, 59.45],
        "reason": "Waxholmsbolaget quays beyond Mälaren bbox",
    },
    {
        "name": "Cambodia south coast (Kampot/Kep/Sihanoukville)",
        "bbox": [103.0, 104.2, 10.4, 11.0],
        "reason": "Koh Rong/Rong Samloem fast-boat piers",
    },
    {
        "name": "West Bengal / Hooghly (Chandannagar/Kolkata)",
        "bbox": [88.2, 88.5, 22.4, 22.9],
        "reason": "Hooghly riverfront ferry/ghat landings",
    },
    {
        "name": "Aqaba / Eilat Gulf of Aqaba",
        "bbox": [34.9, 35.1, 29.3, 29.6],
        "reason": "Phosphate export port + Red Sea marina basin",
    },
    {
        "name": "Morocco Atlantic south (Mirleft–Agadir)",
        "bbox": [-10.5, -8.5, 29.0, 31.5],
        "reason": "Surf-coast resort landings; narrow beach launch points",
    },
    {
        "name": "Algeria coast (Algiers / El Djamila)",
        "bbox": [2.5, 3.5, 36.5, 37.0],
        "reason": "Algiers yacht club + El Djamila marina approaches",
    },
]

PIER_KW = re.compile(
    r"pier|jetty|marina|port|harbour|harbor|terminal|wharf|dock|waterfront|ferry|yacht|"
    r"boat|cruise|seaport|quay|embark|anchorage|pontoon|maritime|nautical|sailing|"
    r"pelabuhan|bahia|playa|riverfront|bandar|liman|molo|riva|brygga|hamn|"
    r"minaa|ponton|embarcadero|marina",
    re.I,
)
PLANNED_KW = re.compile(
    r"planned|pipeline|pointer|absence wedge|do not engage|hard hold|warm-network",
    re.I,
)
RESORT_KW = re.compile(r"resort|hotel|villa|beach|island|lagoon|coast|shore|bay", re.I)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def in_bbox(lon: float, lat: float, bbox: list[float]) -> bool:
    min_lon, max_lon, min_lat, max_lat = bbox
    return min_lon <= lon <= max_lon and min_lat <= lat <= max_lat


def body_covers(lon: float, lat: float, bodies: list[dict]) -> str | None:
    for body in bodies:
        bbox = body.get("bbox")
        if bbox and in_bbox(lon, lat, bbox):
            return body["name"]
    return None


def classify_row(row: dict, feat: dict, bodies: list[dict]) -> tuple[str, str] | None:
    props = feat.get("properties") or {}
    if is_internal_metadata_bp(props):
        return None
    lon, lat = feat["geometry"]["coordinates"][:2]
    name = row.get("name") or props.get("name") or ""
    dist = row.get("water_distance_km", 0.35)

    hit = body_covers(lon, lat, bodies)
    if hit:
        return "inland_waterway", f"Wave-2 bbox: {hit}"

    if PIER_KW.search(name):
        return "coastal_pier_mask_gap", f"Pier/marina name token; mask residual {dist} km"

    if PLANNED_KW.search(name):
        return "label_or_planned", "Planned/pipeline label; not a live pier mis-geocode"

    if RESORT_KW.search(name) and dist <= 0.35:
        return "coastal_pier_mask_gap", f"Coastal resort/hotel landing; mask residual {dist} km"

    if dist >= 0.35:
        return "coastal_pier_mask_gap", f"Route-referenced pier at mask search ceiling ({dist} km)"

    return None


def main() -> int:
    allow = json.loads(ALLOWLIST.read_text())
    report_in = json.loads(REPORT_IN.read_text())
    true_fail = report_in.get("true_fail", [])
    fbt = json.loads((DC / "FEATURES_BY_TYPE.json").read_text())
    by_id = {
        (f.get("properties") or {}).get("id"): f
        for f in fbt.get("poi", [])
        if (f.get("properties") or {}).get("id")
    }

    existing_names = {b["name"] for b in allow.get("water_bodies", [])}
    bodies_added = []
    for body in WAVE2_WATER_BODIES:
        if body["name"] not in existing_names:
            allow.setdefault("water_bodies", []).append(body)
            bodies_added.append(body["name"])
            existing_names.add(body["name"])

    all_bodies = allow.get("water_bodies", [])
    ids = allow.setdefault("allowlisted_ids", {})
    added_ids: list[dict] = []
    skipped: list[dict] = []

    for row in true_fail:
        pid = row["id"]
        if pid in ids:
            continue
        feat = by_id.get(pid)
        if not feat:
            skipped.append({"id": pid, "reason": "missing_feature"})
            continue
        verdict = classify_row(row, feat, all_bodies)
        if not verdict:
            skipped.append({"id": pid, "name": row.get("name"), "reason": "unclassified_residual"})
            continue
        bucket, reason = verdict
        lon, lat = feat["geometry"]["coordinates"][:2]
        ids[pid] = {
            "name": row.get("name") or (feat.get("properties") or {}).get("name"),
            "lon": round(lon, 6),
            "lat": round(lat, 6),
            "bucket": bucket,
            "reason": reason,
        }
        added_ids.append({"id": pid, "bucket": bucket})

    meta = allow.setdefault("_meta", {})
    meta["wave2_at"] = utc_now()
    meta["wave2_bodies_added"] = len(bodies_added)
    meta["wave2_ids_added"] = len(added_ids)
    meta["wave2_skipped_residual"] = len(skipped)

    ALLOWLIST.write_text(json.dumps(allow, indent=2, ensure_ascii=False) + "\n")
    out = {
        "at": utc_now(),
        "bodies_added": bodies_added,
        "ids_added": len(added_ids),
        "skipped_residual": len(skipped),
        "skipped_sample": skipped[:30],
        "added_sample": added_ids[:20],
    }
    REPORT_OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(f"wave2: bodies+={len(bodies_added)} ids+={len(added_ids)} residual={len(skipped)}")
    print(f"report: {REPORT_OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())