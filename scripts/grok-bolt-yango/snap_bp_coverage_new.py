#!/usr/bin/env python3
"""
Snap Tasklet web-research BPs to navigable water + extend lagoon/river allowlist.
Targets BP-COVERAGE-NEW-2026-06-20.json entries that failed water_adjacency_fail.
"""
from __future__ import annotations

import argparse
import json
import math
from copy import deepcopy
from pathlib import Path

from bolt_yango_shared import (
    is_water,
    load_json,
    load_land_mask,
    save_json,
    water_distance_km,
)

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INGEST = ROOT / "_ingest/bp-seal-2026-06-20"
DEFAULT_COVERAGE = DEFAULT_INGEST / "inputs/BP-COVERAGE-NEW-2026-06-20.json"

# Navigable inland water invisible to coarse ocean mask
EXTRA_WATER_BODIES = [
    {
        "name": "Ébrié Lagoon (Abidjan)",
        "bbox": [-4.45, -3.68, 5.12, 5.42],
        "reason": "Lagoon ferry network; SOTRA/CITRANS/STL lagoon stations",
    },
    {
        "name": "Nile River (Greater Cairo)",
        "bbox": [31.15, 31.38, 29.94, 30.12],
        "reason": "Nile commuter/cruise piers; Maadi, Zamalek, Maspero",
    },
    {
        "name": "Gulf of Finland (Helsinki archipelago)",
        "bbox": [24.65, 25.25, 59.92, 60.28],
        "reason": "HSL island ferries; Suomenlinna, Vallisaari, Pihlajasaari",
    },
    {
        "name": "Tallinn Bay / Gulf of Finland (Estonia)",
        "bbox": [24.42, 25.12, 59.35, 59.72],
        "reason": "Tallinn island ferries; Aegna, Naissaar, Prangli",
    },
    {
        "name": "Porvoo River estuary",
        "bbox": [25.62, 25.72, 60.36, 60.42],
        "reason": "Porvoo Old Town quay; Helsinki day-trip corridor",
    },
    {
        "name": "Ria Formosa / Algarve coast",
        "bbox": [-8.95, -7.35, 36.82, 37.18],
        "reason": "Faro, Olhão, Lagos, Benagil, VRSA island/coast landings",
    },
    {
        "name": "Tagus estuary (Lisbon)",
        "bbox": [-9.45, -8.95, 38.62, 38.78],
        "reason": "Cais do Sodré, Belém, Cacilhas, Cascais coastal corridor",
    },
    {
        "name": "Douro River (Porto/Gaia)",
        "bbox": [-8.72, -8.55, 41.12, 41.18],
        "reason": "Ribeira–Gaia river crossing",
    },
    {
        "name": "Red Sea Egypt (Hurghada–Sharm corridor)",
        "bbox": [33.75, 34.55, 27.15, 28.55],
        "reason": "Giftun, Ras Mohammed, Dahab dive/island piers",
    },
    {
        "name": "Bouregreg estuary (Rabat–Salé)",
        "bbox": [-7.75, -6.65, 33.55, 34.12],
        "reason": "Salé–Rabat river crossing; Casablanca/Mohammedia marina cluster",
    },
    {
        "name": "Al Hoceima Bay",
        "bbox": [-4.12, -3.78, 35.10, 35.32],
        "reason": "Cal Iris / Al Hoceima marina landings",
    },
    {
        "name": "Guadalquivir / Ayamonte–VRSA",
        "bbox": [-7.45, -7.35, 37.17, 37.22],
        "reason": "Cross-border Spain–Portugal river mouth",
    },
    {
        "name": "Venice Lagoon (Laguna Veneta)",
        "bbox": [12.20, 12.50, 45.38, 45.50],
        "reason": "ACTV vaporetto network; San Zaccaria, Murano, Burano, Lido S.M.E.",
    },
    {
        "name": "Lagos Lagoon (Five Cowries Creek)",
        "bbox": [3.00, 3.70, 6.30, 6.55],
        "reason": "Yango Lagos: Osborne Foreshore jetty; lagoon water-taxi approaches",
    },
    {
        "name": "Lake Mälaren (Stockholm)",
        "bbox": [17.50, 18.30, 59.20, 59.45],
        "reason": "Bolt Sweden: Drottningholm slottsbrygga; palace ferry pier",
    },
]

R_EARTH_KM = 6371.0088


def snap_to_water(lon: float, lat: float, mask, max_km: float = 0.5) -> tuple[float, float, float]:
    """Return (lon, lat, residual_km) snapped to nearest water within max_km."""
    if is_water(lon, lat, mask):
        return lon, lat, 0.0
    best = (lon, lat, water_distance_km(lon, lat, mask, max_km=max_km))
    if best[2] <= 0.15:
        return best

    step = 0.025  # ~2.5 km at equator, finer below
    for ring in range(1, int(max_km / step) + 1):
        r_km = ring * step
        for deg in range(0, 360, 15):
            br = math.radians(deg)
            dlat = (r_km / R_EARTH_KM) * math.cos(br) * (180 / math.pi)
            dlon = (r_km / R_EARTH_KM) * math.sin(br) / max(math.cos(math.radians(lat)), 1e-6) * (180 / math.pi)
            nlng, nlat = lon + dlon, lat + dlat
            if is_water(nlng, nlat, mask):
                dist = water_distance_km(lon, lat, mask, max_km=r_km)
                if dist <= 0.15:
                    return nlng, nlat, 0.0
                if dist < best[2]:
                    best = (nlng, nlat, dist)
    return best


def fix_city_anchor(data: dict) -> bool:
    anchor = data.get("city_anchor")
    if isinstance(anchor, list) and len(anchor) >= 2:
        return False
    bps = data.get("boarding_points") or []
    if not bps:
        return False
    lng = sum(float(b["lng"]) for b in bps if b.get("lng") is not None) / len(bps)
    lat = sum(float(b["lat"]) for b in bps if b.get("lat") is not None) / len(bps)
    data["city_anchor"] = [round(lng, 6), round(lat, 6)]
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ingest", default=str(DEFAULT_INGEST))
    ap.add_argument("--coverage", default=str(DEFAULT_COVERAGE))
    ap.add_argument("--max-snap-km", type=float, default=0.5)
    args = ap.parse_args()

    ingest = Path(args.ingest)
    coverage = load_json(Path(args.coverage))
    target_ids = {row["id"] for row in coverage.get("new_bps", [])}
    mask = load_land_mask()

    allow_path = ingest / "inputs/bp_water_allowlist.json"
    if not allow_path.exists():
        src = ROOT / "_ingest/bolt-yango-seal-2026-06-19/bolt-yango-seal-2026-06-19/inputs/bp_water_allowlist.json"
        allow = load_json(src)
    else:
        allow = load_json(allow_path)

    existing = {b["name"] for b in allow.get("water_bodies", [])}
    added_bodies = []
    for body in EXTRA_WATER_BODIES:
        if body["name"] not in existing:
            allow.setdefault("water_bodies", []).append(body)
            added_bodies.append(body["name"])
    allow.setdefault("_meta", {})["bp_seal_snap_at"] = "2026-06-20"
    save_json(allow_path, allow)

    bp_dir = ingest / "boarding-points"
    by_file: dict[str, list[str]] = {}
    for row in coverage.get("new_bps", []):
        by_file.setdefault(row["file"], []).append(row["id"])

    report = {"snapped": [], "anchor_fixed": [], "unchanged": [], "still_inland": []}

    for fname, ids in sorted(by_file.items()):
        path = bp_dir / fname
        if not path.exists():
            continue
        data = load_json(path)
        if fix_city_anchor(data):
            report["anchor_fixed"].append(fname)

        id_set = set(ids)
        for bp in data.get("boarding_points") or []:
            if bp.get("id") not in id_set:
                continue
            lng, lat = float(bp["lng"]), float(bp["lat"])
            slng, slat, residual = snap_to_water(lng, lat, mask, max_km=args.max_snap_km)
            if slng != lng or slat != lat:
                bp["lng"] = round(slng, 6)
                bp["lat"] = round(slat, 6)
                bp.setdefault("validation_log", []).append(
                    {
                        "stage": "grok_snap",
                        "result": "snapped",
                        "note": f"Snapped from ({lng},{lat}) residual_km={residual}",
                    }
                )
                report["snapped"].append({"id": bp["id"], "file": fname, "residual_km": residual})
            elif residual <= 0.15:
                report["unchanged"].append(bp["id"])
            else:
                report["still_inland"].append({"id": bp["id"], "residual_km": residual, "file": fname})

        save_json(path, data)

    out = ROOT / "grok-routing-output/bp-coverage-snap-report.json"
    report["allowlist_bodies_added"] = added_bodies
    save_json(out, report)
    print(
        f"snap: snapped={len(report['snapped'])} anchors_fixed={len(report['anchor_fixed'])} "
        f"allowlist+={len(added_bodies)} still_inland={len(report['still_inland'])}"
    )
    print(f"report: {out}")


if __name__ == "__main__":
    main()