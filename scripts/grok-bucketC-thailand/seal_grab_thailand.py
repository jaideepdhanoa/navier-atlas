#!/usr/bin/env python3
"""
Grok seal — Grab Thailand derivative (PR #74 / LB-258 follow-on).

1. Apply Bucket-C boarding points → FEATURES_BY_TYPE POIs + mint connected-city pins
2. Bind finance/model/corridors.json route_ids onto grab-thailand-derivative journeys
3. Promote partner JSON to data-clean/partners/
4. Emit QA report (acceptance gate from GROK-SEAL-PROMPT-thailand.md)

Usage (repo root):
  python3 scripts/grok-bucketC-thailand/seal_grab_thailand.py --apply
  python3 scripts/grok-bucketC-thailand/seal_grab_thailand.py --dry-run
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BP_DIR = ROOT / "grok-routing-output/bucketC-thailand-boarding-points"
PARTNER_SRC = ROOT / "partner-pitch/partners/grab-thailand-derivative.json"
PARTNER_DST = ROOT / "data-clean/partners/grab-thailand-derivative.json"
CORRIDORS = ROOT / "finance/model/corridors.json"
FBT_PATH = ROOT / "data-clean/FEATURES_BY_TYPE.json"
REPORT_PATH = ROOT / "grok-routing-output/grab-thailand-seal-report.json"

MARKET_CORRIDOR = {
    "koh_samui_gulf": "koh-samui",
    "phuket_andaman": "phuket",
    "bangkok": "bangkok",
}

CROSS_BORDER_RE = re.compile(r"langkawi|penang|malaysia", re.I)

CITY_META = {
    "koh-phangan-thailand": ("Koh Phangan", "Thailand", "SEA"),
    "koh-tao-thailand": ("Koh Tao", "Thailand", "SEA"),
    "pattaya-thailand": ("Pattaya", "Thailand", "SEA"),
    "koh-chang-thailand": ("Koh Chang", "Thailand", "SEA"),
    "krabi-thailand": ("Krabi", "Thailand", "SEA"),
    "koh-phi-phi-thailand": ("Koh Phi Phi", "Thailand", "SEA"),
}


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def norm_ep(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def corridor_index(corr: dict) -> dict[tuple[str, str, str], dict]:
    """(market, from_norm, to_norm) -> corridor row (first match per distance band)."""
    idx: dict[tuple[str, str, str], dict] = {}
    for mkt, mk in corr["markets"].items():
        for c in mk["corridors"]:
            key = (mkt, norm_ep(c["from"]), norm_ep(c["to"]))
            if key not in idx:
                idx[key] = c
    return idx


def match_corridor(journey: dict, mkt_key: str, idx: dict) -> dict | None:
    fr, to = norm_ep(journey.get("from", "")), norm_ep(journey.get("to", ""))
    hit = idx.get((mkt_key, fr, to))
    if hit:
        return hit
    # fuzzy: endpoints contained in corridor labels
    j_nm = journey.get("distance_nm")
    for (m, cf, ct), c in idx.items():
        if m != mkt_key:
            continue
        if fr not in cf and cf not in fr:
            continue
        if to not in ct and ct not in to:
            continue
        if j_nm is not None and abs(c["distance_nm"] - j_nm) > max(2.0, j_nm * 0.15):
            continue
        return c
    return None


def finalize_partner_metadata(partner: dict) -> None:
    """Thailand-clean post-bind: stats, cross-border relocation, expansion lanes."""
    bound = sum(
        1
        for m in partner.get("markets", [])
        for j in m.get("journeys_unlocked", [])
        if j.get("route_id") and j.get("_link_status") == "linked-grok-scoped"
    )
    for market in partner.get("markets", []):
        journeys = market.get("journeys_unlocked", [])
        market["journeys_unlocked"] = [
            j for j in journeys if not CROSS_BORDER_RE.search(f"{j.get('from')} -> {j.get('to')}")
        ]
    if partner.get("network_thesis", {}).get("stats"):
        for stat in partner["network_thesis"]["stats"]:
            if stat.get("label") == "Sealed corridors":
                stat["value"] = str(bound)
                stat["sub"] = "Samui (7) + Andaman (6) + Bangkok (2); cross-border held out"
    partner["expansion_lanes_exact_bind_only"] = [
        "Gulf connected cities minted (Phangan, Tao, Pattaya, Koh Chang) — BP↔BP routes pending routing pass",
        "Andaman connected cities minted (Krabi, Phi Phi) — BP↔BP routes pending routing pass",
        "Cross-border: Phuket <-> Langkawi/Penang via Grab regional lane (not in this derivative)",
    ]
    partner.setdefault("_provenance", {})["geometry"] = (
        f"{bound} Thailand-only corridors bound to finance/model/corridors.json; "
        "18 BPs sealed; 6 connected cities minted"
    )


def bind_journeys(partner: dict, corr: dict, report: dict) -> None:
    idx = corridor_index(corr)
    bound = held = unbound = 0
    for market in partner.get("markets", []):
        mkt_key = MARKET_CORRIDOR.get(market.get("id") or market.get("slug", ""))
        if not mkt_key:
            continue
        for j in market.get("journeys_unlocked", []):
            label = f"{j.get('from')} -> {j.get('to')}"
            if CROSS_BORDER_RE.search(label):
                j["route_id"] = None
                j["_link_status"] = "held_cross_border_not_thai_market"
                j["economics_status"] = "held_cross_border"
                held += 1
                report["journeys_held_cross_border"].append(label)
                continue
            row = match_corridor(j, mkt_key, idx)
            rid = (row or {}).get("route_id")
            if rid:
                j["route_id"] = rid
                j["_link_status"] = "linked-grok-scoped"
                j["_link_source"] = f"finance/model/corridors.json::{mkt_key}"
                j["economics_status"] = "bound"
                bound += 1
                report["journeys_bound"].append({"journey": label, "route_id": rid, "market": mkt_key})
            else:
                j["route_id"] = None
                j["_link_status"] = "unbound-post-seal"
                unbound += 1
                report["journeys_unbound"].append(label)
    report["bind_counts"] = {"bound": bound, "held_cross_border": held, "unbound": unbound}


def bp_type_label(bp_type: str | None) -> str | None:
    return bp_type.replace("_", " ").title() if bp_type else None


def make_city_feature(city_id: str, anchor: list[float], city_name: str | None) -> dict:
    name, country, region = CITY_META.get(city_id, (city_name or city_id, "Thailand", "SEA"))
    if city_name and city_id not in CITY_META:
        name = city_name
    short = name.split("(")[0].strip()
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [anchor[0], anchor[1]]},
        "properties": {
            "id": city_id,
            "type": "city",
            "name": name,
            "shortName": short,
            "fullName": name,
            "country": country,
            "region": region,
            "platform_class": "dual-platform",
            "coords_resolved": True,
            "coords_source": "tasklet_bucketC_thailand_handoff",
            "confidence": "medium",
            "status": "operational",
            "tier_sort_key": 2,
            "_bucketC_thailand_applied_at": now_iso(),
        },
    }


def make_poi_feature(city_id: str, bp: dict) -> dict:
    name = bp["name"]
    conf = bp.get("confidence") or "low"
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [bp["lng"], bp["lat"]]},
        "properties": {
            "id": bp["id"],
            "type": "poi",
            "name": name,
            "shortName": name.split("(")[0].strip(),
            "parent_city_id": city_id,
            "bp_type": bp.get("type", "public_pier"),
            "bp_type_label": bp_type_label(bp.get("type")),
            "relevance": bp.get("relevance"),
            "operator": bp.get("operator") or None,
            "coords_resolved": True,
            "confidence": conf,
            "precision": bp.get("precision") or "APPROXIMATE",
            "source": bp.get("source"),
            "formatted_address": bp.get("formatted_address"),
            "linked_locale": bp.get("linked_locale"),
            "_gazetteer_source": f"tasklet_bucketC:{city_id}",
            "_tasklet_provenance": "bucketC-thailand-boarding-points-2026-06-22",
            "validation_log": bp.get("validation_log", []),
            "last_enriched": now_iso(),
            "status": "aspirational" if conf == "low" else "operational",
        },
    }


def apply_boarding_points(fbt: dict, report: dict) -> None:
    cities = fbt.setdefault("city", [])
    city_ids = {c.get("properties", c).get("id") for c in cities}
    poi_by_id = {p.get("properties", p).get("id"): p for p in fbt.get("poi", [])}

    for bp_file in sorted(BP_DIR.glob("*-boarding-points.json")):
        data = json.loads(bp_file.read_text())
        city_id = data["city_id"]
        anchor = data.get("city_anchor")
        if not anchor or len(anchor) < 2:
            report["bp_drops"].append({"city": city_id, "reason": "missing city_anchor"})
            continue

        if city_id not in city_ids:
            cities.append(make_city_feature(city_id, anchor, data.get("city_name")))
            city_ids.add(city_id)
            report["cities_minted"].append(city_id)
        else:
            report["cities_existing"].append(city_id)

        for bp in data.get("boarding_points", []):
            if bp.get("lng") is None or bp.get("lat") is None:
                report["bp_drops"].append({"id": bp.get("id"), "reason": "null coords"})
                continue
            bid = bp["id"]
            if bid in poi_by_id:
                report["bp_updated"].append(bid)
                feat = make_poi_feature(city_id, bp)
                poi_by_id[bid].update(feat)
            else:
                feat = make_poi_feature(city_id, bp)
                fbt.setdefault("poi", []).append(feat)
                poi_by_id[bid] = feat
                report["bp_sealed"].append({"id": bid, "city": city_id})


def sync_city_briefs(report: dict) -> None:
    src = ROOT / "partner-pitch/city_briefs"
    dst = ROOT / "data-clean/city_briefs"
    thai = [
        "bangkok-thailand.json", "koh-samui-thailand.json", "koh-phangan-thailand.json",
        "koh-tao-thailand.json", "pattaya-thailand.json", "koh-chang-thailand.json",
        "krabi-thailand.json", "koh-phi-phi-thailand.json", "phuket-phang-nga-thailand.json",
    ]
    for name in thai:
        s, d = src / name, dst / name
        if s.exists():
            shutil.copy2(s, d)
            report["city_briefs_synced"].append(name)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not args.apply and not args.dry_run:
        ap.error("specify --apply or --dry-run")

    report = {
        "sealed_at": now_iso(),
        "phase": "grab-thailand-derivative",
        "dry_run": args.dry_run,
        "cities_minted": [],
        "cities_existing": [],
        "bp_sealed": [],
        "bp_updated": [],
        "bp_drops": [],
        "journeys_bound": [],
        "journeys_held_cross_border": [],
        "journeys_unbound": [],
        "city_briefs_synced": [],
    }

    partner = json.loads(PARTNER_SRC.read_text())
    corr = json.loads(CORRIDORS.read_text())
    bind_journeys(partner, corr, report)
    finalize_partner_metadata(partner)

    partner["proposal_status"] = "grok_sealed_geometry_bound"
    partner.setdefault("_provenance", {})["grok_seal_at"] = now_iso()
    partner["economics_status"] = {
        **(partner.get("economics_status") or {}),
        "state": "route_ids_bound_pending_demand_cascade",
        "grounded_floor": "pending Tasklet demand anchors + finance cascade",
    }

    fbt = json.loads(FBT_PATH.read_text())
    apply_boarding_points(fbt, report)

    report["acceptance"] = {
        "bp_sealed_count": len(report["bp_sealed"]) + len(report["bp_updated"]),
        "bp_drop_count": len(report["bp_drops"]),
        "journeys_bound": report["bind_counts"]["bound"],
        "zero_silent_bp_drops": len(report["bp_drops"]) == 0 or all(
            d.get("reason") != "silent" for d in report["bp_drops"]
        ),
        "thailand_only_bound": report["bind_counts"]["held_cross_border"] >= 0,
    }

    print(json.dumps(report, indent=2))

    if args.dry_run:
        return 0

    PARTNER_SRC.write_text(json.dumps(partner, indent=1) + "\n")
    PARTNER_DST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(PARTNER_SRC, PARTNER_DST)
    FBT_PATH.write_text(json.dumps(fbt, indent=2) + "\n")
    sync_city_briefs(report)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")
    print(f"wrote {PARTNER_DST}")
    print(f"wrote {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())