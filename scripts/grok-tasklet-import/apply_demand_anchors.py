#!/usr/bin/env python3
"""Apply Tasklet demand anchors → corridor_annual_oneway_pax on scoped recal views."""
from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-tasklet-import"))

from tasklet_shared import (  # noqa: E402
    CAPTURE_ABC,
    CAPEX_CARIBBEAN_COMMERCIAL,
    KLEIN_CURACAO_SEASON_DAYS_DEFAULT,
    ROUTING_OUTPUT,
    find_staging_package,
    load_json,
    partner_staging_dir,
    save_json,
    utc_now,
)

RECAL = ROOT / "finance/recal"


def distribute(weights: dict[str, float], total: int) -> dict[str, int]:
    keys = list(weights.keys())
    if not keys or total <= 0:
        return {k: 0 for k in keys}
    wsum = sum(weights.values()) or 1.0
    raw = {k: total * (weights[k] / wsum) for k in keys}
    out = {k: int(raw[k]) for k in keys}
    rem = total - sum(out.values())
    for k in sorted(keys, key=lambda x: raw[x] - out[x], reverse=True)[:rem]:
        out[k] += 1
    return out


def patch_l3(corridor: dict, pax: int, note: str, *, partner: str, season_days: int | None = None) -> None:
    l3 = corridor.setdefault("L3_locals", {})
    l3["corridor_annual_oneway_pax"] = pax
    l3["navier_capture_override"] = CAPTURE_ABC
    l3["_demand_record"] = {
        "value": pax,
        "unit": "pax/yr one-way",
        "source_tier": "T4",
        "confidence": "med",
        "source": note,
        "method": "Tasklet demand anchors → Grok distribute (grok-tasklet-import)",
        "capture_basis": CAPTURE_ABC,
    }
    l3["demand_confidence"] = "med"
    if season_days is not None:
        l3["season_days"] = season_days
    if partner == "caribbean":
        l3["capex_usd_override"] = CAPEX_CARIBBEAN_COMMERCIAL
    corridor["_demand_applied_at"] = utc_now()


def corridor_key(c: dict) -> str:
    return f"{c.get('route_id')}|{c.get('from')}|{c.get('to')}"


def apply_ocean_whisperer(corridors: list[dict], anchors: dict) -> dict:
    pool = anchors.get("island_pool") or {}
    captive = anchors.get("captive_anchors") or {}
    stay = pool.get("curacao_stayover_visitors_yr") or 700_249
    cruise = pool.get("curacao_cruise_passengers_yr") or 834_890
    min_floor = (captive.get("min_initial_exposure_pax_yr") or {}).get("value") or 3_000

    premium_pool = int(stay * 0.25 + cruise * 0.08)
    total = max(premium_pool, min_floor)

    weights = {}
    for c in corridors:
        if c.get("_economics_excluded") or c.get("tier") == "roadmap":
            continue
        rid = c.get("route_id")
        fr, to = (c.get("from") or "").lower(), (c.get("to") or "").lower()
        w = 1.0
        if "hato" in fr and "sandals" in to:
            w = 3.5
        elif "hato" in fr and "baoase" in to:
            w = 2.0
        elif "willemstad" in fr and "sandals" in to:
            w = 2.0
        elif "piscadera" in to:
            w = 1.5
        elif "baoase" in to:
            w = 1.2
        elif "klein" in to:
            w = 0.8
        if rid:
            weights[corridor_key(c)] = w

    shares = distribute(weights, total)
    patched = []
    for c in corridors:
        if c.get("_economics_excluded") or c.get("tier") == "roadmap":
            continue
        key = corridor_key(c)
        pax = shares.get(key, 0)
        season = None
        if c.get("render") == "seasonal-amber" or "klein" in (c.get("to") or "").lower():
            season = KLEIN_CURACAO_SEASON_DAYS_DEFAULT
            pax = max(int(pax * (season / 365)), int(min_floor * 0.15))
        patch_l3(
            c,
            pax,
            "ocean-whisperer-demand-anchors.json captive Curaçao premium transfer pool",
            partner="ocean-whisperer",
            season_days=season,
        )
        patched.append({"route_id": c.get("route_id"), "pax": pax, "season_days": season})
    return {"partner": "ocean-whisperer", "total_pool": total, "patched": patched}


def apply_caribbean(corridors: list[dict], anchors: dict) -> dict:
    islands = anchors.get("islands") or {}
    aruba = islands.get("aruba") or {}
    curacao = islands.get("curacao") or {}
    bonaire = islands.get("bonaire") or {}

    specs: dict[str, tuple[int, str]] = {}
    for c in corridors:
        if c.get("_economics_excluded") or c.get("tier") == "roadmap":
            continue
        key = corridor_key(c)
        fr, to = (c.get("from") or "").lower(), (c.get("to") or "").lower()
        rid = c.get("route_id")

        if "bonaire" in to and "spanish" in fr:
            pax = int(19 * 8 * 365)
            note = "inter_island_air_substitution_pool Curaçao↔Bonaire high-frequency turboprop"
        elif "palm beach" in to and "cruise" in fr:
            pax = int((aruba.get("cruise_passengers_yr") or 850_000) * 0.12)
            note = "aruba cruise → resort strip"
        elif "palm beach" in to and "airport" in fr:
            pax = int((aruba.get("stopover_visitors_yr") or 1_200_000) * 0.18)
            note = "aruba airport → resort"
        elif "jan thiel" in to or "spanish water" in to:
            if "hato" in fr:
                pax = int((curacao.get("stayover_visitors_yr") or 700_249) * 0.12)
                note = "curacao airport → south-coast resorts"
            else:
                pax = int((curacao.get("cruise_passengers_yr") or 834_890) * 0.10)
                note = "curacao cruise → resort cluster"
        elif "klein bonaire" in to:
            pax = int((bonaire.get("stayover_visitors_yr") or 182_181) * (bonaire.get("dive_share_of_stayover") or 0.43) * 0.35)
            note = "bonaire dive transfer pool"
        elif "harbour village" in to:
            pax = int((bonaire.get("cruise_passengers_yr") or 359_000) * 0.15)
            note = "bonaire cruise → dive-resort cluster"
        elif "klein" in to and "curacao" in fr:
            base = int((curacao.get("stayover_visitors_yr") or 700_249) * 0.05)
            season = KLEIN_CURACAO_SEASON_DAYS_DEFAULT
            pax = max(int(base * (season / 365)), 2_500)
            specs[key] = (pax, "curacao Klein Curaçao seasonal excursion")
            c.setdefault("L3_locals", {})["season_days"] = season
            patch_l3(c, pax, "curacao Klein Curaçao seasonal excursion", partner="caribbean", season_days=season)
            continue
        else:
            pax = 5_000
            note = "ABC broad-footprint default slice"
        specs[key] = (pax, note)
        patch_l3(c, pax, note, partner="caribbean")

    patched = [{"route_id": c.get("route_id"), "pax": (c.get("L3_locals") or {}).get("corridor_annual_oneway_pax")}
               for c in corridors if not c.get("_economics_excluded") and c.get("tier") != "roadmap"]
    return {"partner": "caribbean", "patched": patched}


def apply_partner(partner: str, package: Path, corr_path: Path) -> dict:
    staging_dir = partner_staging_dir(package, partner)
    anchor_name = f"{partner}-demand-anchors.json"
    anchors = load_json(staging_dir / anchor_name)
    scoped = load_json(corr_path)
    mk = scoped["markets"][partner]
    corridors = mk.get("corridors") or []

    if partner == "ocean-whisperer":
        result = apply_ocean_whisperer(corridors, anchors)
    elif partner == "caribbean":
        result = apply_caribbean(corridors, anchors)
    else:
        raise ValueError(f"No demand apply recipe for partner {partner}")

    scoped["_demand_applied_at"] = utc_now()
    save_json(corr_path, scoped)
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--partner", required=True)
    ap.add_argument("--package", help="seal-staging package dir")
    ap.add_argument("--corridors", help="scoped corridors JSON (default: finance/recal/corridors-<partner>.json)")
    args = ap.parse_args()

    package = find_staging_package(args.package)
    corr_path = Path(args.corridors) if args.corridors else RECAL / f"corridors-{args.partner}.json"
    if not corr_path.exists():
        print(f"✗ missing {corr_path} — run build_scoped_corridors.py first", file=sys.stderr)
        return 1

    result = apply_partner(args.partner, package, corr_path)
    report_path = ROUTING_OUTPUT / f"{args.partner}-demand-apply-report.json"
    save_json(report_path, {"at": utc_now(), **result})
    print(json.dumps({"corridors": str(corr_path), "patched": len(result.get("patched", []))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())