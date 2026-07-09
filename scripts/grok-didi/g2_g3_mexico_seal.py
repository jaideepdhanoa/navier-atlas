#!/usr/bin/env python3
"""DiDi ex-China #210 — G2 Mexico BP promotion + G3 route seal + Tasklet spine.

G2: reparent/bind verified Caribbean BPs; ledger Pacific holds (no invented coords).
G3: unquarantine Playa↔Cozumel; correct city_ids on marquee routes; bind DiDi featured_routes.
Does NOT invent L3 demand/fares — spine only for Tasklet T3.
"""
from __future__ import annotations

import argparse
import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
FBT = ROOT / "data-clean/FEATURES_BY_TYPE.json"
ROUTES = ROOT / "data-clean/ROUTES.json"
DIDI_PATHS = [
    ROOT / "partner-pitch/partners/didi.json",
    ROOT / "data-clean/partners/didi.json",
]
OUT_DIR = ROOT / "handoff/didi-ex-china/mexico"
RECEIPT = OUT_DIR / "G2-G3-SEAL-RECEIPT-2026-07-09.json"
SPINE = OUT_DIR / "MEXICO-ROUTE-SPINE-FOR-TASKLET-2026-07-09.json"
HANDOFF_MD = OUT_DIR / "TASKLET-T3-HANDOFF.md"

# Canonical ferry pier for PDC Muelle Fiscal (matches e__ route geometry / operator pier)
PDC_FERRY_COORDS = [-87.074971, 20.612926]
COZUMEL_FERRY_COORDS = [-86.95121, 20.512376]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load(p: Path) -> Any:
    return json.loads(p.read_text())


def save(p: Path, obj: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def g2_promote_bps(fbt: dict) -> dict:
    ledger: list[dict] = []
    by_id: dict[str, dict] = {}
    for feat in fbt.get("poi") or []:
        props = feat.get("properties") or {}
        pid = props.get("id")
        if pid:
            by_id[pid] = feat

    promotions = [
        {
            "id": "bp-062decef2f",
            "parent_city_id": "cancun-riviera-maya-mexico",
            "name": "Terminal Marítima Puerto Juárez",
            "action": "confirm_existing",
            "market": "mexico-caribbean",
        },
        {
            "id": "bp-d08462d3d9",
            "parent_city_id": "cancun-riviera-maya-mexico",
            "name": "Terminal Marítima de Isla Mujeres",
            "action": "confirm_existing",
            "market": "mexico-caribbean",
        },
        {
            "id": "bp-1f95439031",
            "parent_city_id": "cozumel-mexico",
            "name": "Passenger Ferry Ultramar Cozumel (San Miguel)",
            "action": "reparent_to_cozumel",
            "market": "mexico-caribbean",
            "coords": COZUMEL_FERRY_COORDS,
        },
        {
            "id": "bp-pdc-muelle-fiscal",
            "parent_city_id": "playa-del-carmen-mexico",
            "name": "Muelle Fiscal Playa del Carmen (Ferry Terminal)",
            "action": "reparent_and_snap_ferry_pier",
            "market": "mexico-caribbean",
            "coords": PDC_FERRY_COORDS,
        },
        {
            "id": "bp-608e348da1",
            "parent_city_id": "cancun-riviera-maya-mexico",
            "name": "Marina El Cid Puerto Morelos",
            "action": "confirm_poi_only_not_route_demand",
            "market": "mexico-caribbean",
        },
    ]

    accepted = []
    for row in promotions:
        feat = by_id.get(row["id"])
        if not feat:
            ledger.append({"id": row["id"], "action": "drop_missing", "reason": "not_in_FEATURES"})
            continue
        props = feat.setdefault("properties", {})
        before = {
            "parent_city_id": props.get("parent_city_id"),
            "coords": (feat.get("geometry") or {}).get("coordinates"),
        }
        props["parent_city_id"] = row["parent_city_id"]
        props["status"] = props.get("status") or "operational"
        props["bp_type"] = props.get("bp_type") or "ferry_terminal"
        props["name"] = row.get("name") or props.get("name")
        props["fullName"] = props.get("name")
        if row.get("coords"):
            feat["geometry"] = {"type": "Point", "coordinates": list(row["coords"])}
            props["coords_resolved"] = True
            props["coords_source"] = "didi_g2_mexico_operator_pier_2026-07-09"
        props["_didi_g2"] = {
            "at": utc_now(),
            "action": row["action"],
            "market": row["market"],
            "before": before,
        }
        if row["action"] == "confirm_poi_only_not_route_demand":
            props["_not_route_demand_proof"] = True
        accepted.append({"id": row["id"], "action": row["action"], "parent_city_id": row["parent_city_id"]})
        ledger.append({"id": row["id"], "action": row["action"], "status": "accepted"})

    # Explicit drops from research (zero silent)
    for drop in [
        {"id": None, "name": "Puerto de Lerma", "reason": "non_bp_poi_for_passenger_lane"},
        {"id": None, "name": "San Pedro Belize Express terminal", "reason": "foreign_city_unbound_backlog"},
        {"id": None, "name": "Chetumal Muelle Fiscal", "reason": "no_atlas_city_backlog"},
        {"id": "bp-0ac46ffe2e", "name": "Los Cabos generic place label", "reason": "reject_drop_research"},
    ]:
        ledger.append({**drop, "action": "explicit_drop"})

    return {"accepted": accepted, "ledger": ledger, "accepted_n": len(accepted)}


def g3_seal_routes(routes: list) -> dict:
    by_id = {}
    for i, f in enumerate(routes):
        rid = (f.get("properties") or {}).get("id")
        if rid:
            by_id[rid] = i

    changes = []

    def patch(rid: str, **kwargs) -> None:
        i = by_id.get(rid)
        if i is None:
            changes.append({"route_id": rid, "action": "missing"})
            return
        props = routes[i].setdefault("properties", {})
        before = {k: props.get(k) for k in kwargs}
        for k, v in kwargs.items():
            if k == "_clear_quarantine" and v:
                props["_quarantine"] = False
                props.pop("_quarantine_reason", None)
                props.pop("quarantine_reason", None)
                if props.get("relevance") == "hide":
                    props["relevance"] = "show"
                continue
            props[k] = v
        props["_didi_g3_seal"] = {"at": utc_now(), "before": before}
        changes.append({"route_id": rid, "action": "patched", "fields": list(kwargs.keys())})

    # Unquarantine canonical Playa↔Cozumel geometry route — bind real BPs
    patch(
        "e__playa-del-carmen-mexico__playa-del-carmen-ferry__cozumel-mexico__cozumel-ferry-san-miguel",
        from_city_id="playa-del-carmen-mexico",
        to_city_id="cozumel-mexico",
        from_label="Muelle Fiscal Playa del Carmen",
        to_label="Passenger Ferry Ultramar Cozumel (San Miguel)",
        **{
            "from": "bp-pdc-muelle-fiscal",
            "to": "bp-1f95439031",
            "cluster_id": "mexico",
            "_clear_quarantine": True,
            "label": "Playa del Carmen ↔ Cozumel (San Miguel ferry)",
        },
    )

    # Fix ics marquee city parenting
    patch(
        "ics-dd1d814699",
        from_city_id="playa-del-carmen-mexico",
        to_city_id="cozumel-mexico",
        from_label="Muelle Fiscal Playa del Carmen",
        to_label="Passenger Ferry Ultramar Cozumel",
        **{"from": "bp-pdc-muelle-fiscal", "to": "bp-1f95439031", "cluster_id": "mexico"},
    )
    patch(
        "ics-9d3a6b961f",
        from_city_id="playa-del-carmen-mexico",
        to_city_id="cozumel-mexico",
        from_label="Muelle Fiscal Playa del Carmen",
        to_label="Cozumel Ferry Terminal",
        **{"from": "bp-pdc-muelle-fiscal", "to": "bp-1f95439031", "cluster_id": "mexico"},
    )
    # Juárez ↔ Isla Mujeres — already clean; tag seal
    patch(
        "ics-413f51cd44",
        from_city_id="cancun-riviera-maya-mexico",
        to_city_id="cancun-riviera-maya-mexico",
        **{"from": "bp-062decef2f", "to": "bp-d08462d3d9", "cluster_id": "mexico"},
    )
    patch(
        "ics-03e3853317",
        from_city_id="cancun-riviera-maya-mexico",
        to_city_id="cancun-riviera-maya-mexico",
        **{"to": "bp-d08462d3d9", "cluster_id": "mexico"},
    )
    # Pacific marquees — tag seal only (already mexico cluster)
    for rid in ("ics-89a8844858", "ics-db0930d9d1", "ics-b5861451fb", "ics-de6758216f"):
        patch(rid, cluster_id="mexico")

    # Snap e__ geometry endpoints to BP coords if present
    e_rid = "e__playa-del-carmen-mexico__playa-del-carmen-ferry__cozumel-mexico__cozumel-ferry-san-miguel"
    if e_rid in by_id:
        f = routes[by_id[e_rid]]
        coords = (f.get("geometry") or {}).get("coordinates") or []
        if len(coords) >= 2:
            coords[0] = list(PDC_FERRY_COORDS)
            coords[-1] = list(COZUMEL_FERRY_COORDS)
            f["geometry"]["coordinates"] = coords

    return {"changes": changes, "n": len([c for c in changes if c.get("action") == "patched"])}


# Marquee spine for Tasklet L3 bind (current-service first)
CARIBBEAN_SPINE = [
    {
        "route_id": "ics-413f51cd44",
        "od": "Puerto Juárez ↔ Isla Mujeres",
        "from_bp": "bp-062decef2f",
        "to_bp": "bp-d08462d3d9",
        "from_city_id": "cancun-riviera-maya-mexico",
        "to_city_id": "cancun-riviera-maya-mexico",
        "distance_nm": 5.27,
        "service_status": "current_scheduled",
        "demand_hint": {
            "geography": "Puerto Juárez–Isla Mujeres",
            "passenger_movements_2025_approx": 5_460_000,
            "note": "APIQ/operator series — Tasklet must set directional one-way + fare mix before model use",
            "model_use": "blocked_until_direction_and_fare_mix",
        },
        "sub_proposal": "mexico-caribbean",
        "priority": 1,
    },
    {
        "route_id": "ics-dd1d814699",
        "od": "Playa del Carmen ↔ Cozumel (Ultramar/Winjet)",
        "from_bp": "bp-pdc-muelle-fiscal",
        "to_bp": "bp-1f95439031",
        "from_city_id": "playa-del-carmen-mexico",
        "to_city_id": "cozumel-mexico",
        "distance_nm": 9.53,
        "service_status": "current_scheduled",
        "demand_hint": {
            "geography": "Playa del Carmen–Cozumel",
            "passenger_movements_2025_approx": 3_850_000,
            "departures_2025": 27920,
            "fare_mxn_one_way_observed": {"ultramar_premium_plus": 320, "winjet_from_playa": 335},
            "note": "No FX conversion or yield mix in Grok lane — Tasklet owns USD fare + direction split",
            "model_use": "blocked_until_fare_yield_and_direction",
        },
        "sub_proposal": "mexico-caribbean",
        "priority": 1,
        "alias_route_ids": [
            "e__playa-del-carmen-mexico__playa-del-carmen-ferry__cozumel-mexico__cozumel-ferry-san-miguel",
            "ics-9d3a6b961f",
        ],
    },
    {
        "route_id": "ics-03e3853317",
        "od": "Cancún Ultramar ↔ Isla Mujeres",
        "from_city_id": "cancun-riviera-maya-mexico",
        "to_city_id": "cancun-riviera-maya-mexico",
        "distance_nm": 5.49,
        "service_status": "current_scheduled",
        "sub_proposal": "mexico-caribbean",
        "priority": 2,
    },
    {
        "route_id": "ics-aa6ff40d2d",
        "od": "Punta Sam ↔ Isla Mujeres (car ferry)",
        "from_city_id": "cancun-riviera-maya-mexico",
        "to_city_id": "cancun-riviera-maya-mexico",
        "distance_nm": 3.35,
        "service_status": "current_scheduled",
        "sub_proposal": "mexico-caribbean",
        "priority": 2,
    },
]

PACIFIC_SPINE = [
    {
        "route_id": "ics-89a8844858",
        "od": "Puerto Vallarta / Los Muertos → Yelapa",
        "from_city_id": "puerto-vallarta-mexico",
        "to_city_id": "puerto-vallarta-mexico",
        "distance_nm": 14.5,
        "service_status": "current_water_taxi_evidence",
        "demand_hint": {
            "fare_mxn_one_way_observed": 350,
            "note": "No audited annual ridership — Tasklet sources or leaves null",
            "model_use": "blocked_until_ridership",
        },
        "sub_proposal": "mexico-pacific",
        "priority": 1,
    },
    {
        "route_id": "ics-de6758216f",
        "od": "Puerto Vallarta → Punta de Mita",
        "from_city_id": "puerto-vallarta-mexico",
        "to_city_id": "puerto-vallarta-mexico",
        "distance_nm": 9.9,
        "service_status": "future_opportunity",
        "sub_proposal": "mexico-pacific",
        "priority": 2,
    },
    {
        "route_id": "ics-db0930d9d1",
        "od": "Cabo San Lucas Marina → Puerto Los Cabos / SJC",
        "from_city_id": "los-cabos-mexico",
        "to_city_id": "los-cabos-mexico",
        "distance_nm": 17.0,
        "service_status": "future_opportunity",
        "sub_proposal": "mexico-pacific",
        "priority": 2,
    },
    {
        "route_id": "ics-b5861451fb",
        "od": "Palmilla → San José del Cabo Marina",
        "from_city_id": "los-cabos-mexico",
        "to_city_id": "los-cabos-mexico",
        "distance_nm": 3.4,
        "service_status": "future_opportunity",
        "sub_proposal": "mexico-pacific",
        "priority": 3,
    },
]


def bind_didi_markets(doc: dict) -> dict:
    car_ids = [r["route_id"] for r in CARIBBEAN_SPINE]
    pac_ids = [r["route_id"] for r in PACIFIC_SPINE]
    bound = []

    def fr_objs(ids: list[str]) -> list[dict]:
        return [{"route_id": rid} for rid in ids]

    for m in doc.get("markets") or []:
        if not isinstance(m, dict):
            continue
        mid = m.get("id") or ""
        if mid == "mexico-caribbean":
            m["featured_routes"] = fr_objs(car_ids)
            m["wow_corridors"] = fr_objs(car_ids[:2])
            for i, ph in enumerate(m.get("phases") or []):
                if not isinstance(ph, dict):
                    continue
                # phase 0 prove: top 2; later: all
                ph["featured_routes"] = fr_objs(car_ids[:2] if i == 0 else car_ids)
            bound.append({"market": mid, "n": len(car_ids)})
        elif mid == "mexico-pacific":
            m["featured_routes"] = fr_objs(pac_ids)
            m["wow_corridors"] = fr_objs(pac_ids[:1])
            for i, ph in enumerate(m.get("phases") or []):
                if not isinstance(ph, dict):
                    continue
                ph["featured_routes"] = fr_objs(pac_ids[:1] if i == 0 else pac_ids)
            bound.append({"market": mid, "n": len(pac_ids)})
    doc["_didi_g3_mexico"] = {"at": utc_now(), "bound": bound}
    return {"bound": bound}


def write_handoff_md(spine: dict) -> None:
    lines = [
        "# Tasklet T3 handoff — DiDi Mexico economics",
        "",
        f"**From:** Grok · G2/G3 seal · `{utc_now()}`  ",
        "**Status after Grok:** `seal-complete / cascade-needed`  ",
        "**Do not:** invent L3, use Grab census, or cascade on catch-all `didi` market key.",
        "",
        "## What Grok sealed",
        "",
        "### G2 boarding points (accepted)",
        "| bp_id | city | note |",
        "|-------|------|------|",
        "| `bp-062decef2f` | cancun-riviera-maya-mexico | Puerto Juárez ferry terminal |",
        "| `bp-d08462d3d9` | cancun-riviera-maya-mexico | Isla Mujeres ferry terminal |",
        "| `bp-pdc-muelle-fiscal` | **playa-del-carmen-mexico** (reparented) | coords snapped to ferry pier |",
        "| `bp-1f95439031` | **cozumel-mexico** (reparented) | Ultramar Cozumel |",
        "| `bp-608e348da1` | cancun-riviera-maya-mexico | POI only — not demand proof |",
        "",
        "### Explicit drops / backlog (not silent)",
        "- Chetumal, San Pedro (Belize), Puerto de Lerma — backlog or reject",
        "- Pacific candidate BPs without confirmed coordinates — **not minted**",
        "",
        "### G3 routes",
        "- Unquarantined `e__playa-del-carmen…cozumel…` and rebound to real BP ids",
        "- Corrected `from_city_id` / `to_city_id` on Playa↔Cozumel `ics-*` routes",
        "- Marquee spine bound into DiDi `mexico-caribbean` + `mexico-pacific` featured_routes + phases",
        "",
        "## Route-ID spine for L3 bind",
        "",
        "Machine-readable: `MEXICO-ROUTE-SPINE-FOR-TASKLET-2026-07-09.json`",
        "",
        "### mexico-caribbean (priority)",
    ]
    for r in CARIBBEAN_SPINE:
        lines.append(
            f"- **`{r['route_id']}`** — {r['od']} · {r['distance_nm']} nm · {r['service_status']}"
        )
        dh = r.get("demand_hint") or {}
        if dh:
            lines.append(f"  - demand hint: {json.dumps(dh, ensure_ascii=False)[:200]}")
    lines += ["", "### mexico-pacific (priority)"]
    for r in PACIFIC_SPINE:
        lines.append(
            f"- **`{r['route_id']}`** — {r['od']} · {r['distance_nm']} nm · {r['service_status']}"
        )
    lines += [
        "",
        "## Tasklet T3 checklist",
        "",
        "1. **Source** `corridor_annual_oneway_pax` + `comparable_fare_usd_pax` per spine `route_id` "
        "(directional one-way; never put port_total on a single route 1:1 without allocation note).",
        "2. **Country-reference** Mexico opex row if missing (no Singapore silent fallback).",
        "3. Build finance markets as **geography keys**, not catch-all `didi`:",
        "   - `mexico-caribbean` (partner=`didi`)",
        "   - `mexico-pacific` (partner=`didi`)",
        "   - Spine route_ids must match this handoff exactly (finance-corridor inheritance).",
        "4. Run aggregate → growth → frontend splice → partner JSON.",
        "5. Update live Sheet; confirm model ↔ Sheet agree.",
        "6. Hand back to Grok for **G4** economics sidecar + partner reseal + Gate G.",
        "",
        "## Blockers still open (honest)",
        "",
        "- Directional split + fare yield mix for Isla Mujeres (~5.46M movements) and Cozumel (~3.85M / 27,920 deps).",
        "- Pacific water-taxi annual ridership (Yelapa etc.) unpublished — null beats guess.",
        "- La Paz / Mazatlán / Acapulco candidates need registry cities + BPs (not in this seal).",
        "- Chile / Argentina still registry-gap (Wave C).",
        "",
        "## Files",
        "",
        "- `G2-G3-SEAL-RECEIPT-2026-07-09.json`",
        "- `MEXICO-ROUTE-SPINE-FOR-TASKLET-2026-07-09.json`",
        "- Research inputs under same directory (L3 sourcing, BP briefs).",
        "",
    ]
    HANDOFF_MD.write_text("\n".join(lines) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    fbt = load(FBT)
    raw_routes = load(ROUTES)
    routes = raw_routes if isinstance(raw_routes, list) else raw_routes.get("features") or []

    g2 = g2_promote_bps(fbt)
    g3 = g3_seal_routes(routes)

    didi_bind = []
    for path in DIDI_PATHS:
        doc = load(path)
        didi_bind.append({"path": str(path.relative_to(ROOT)), **bind_didi_markets(doc)})
        if args.apply:
            save(path, doc)

    spine = {
        "at": utc_now(),
        "partner": "didi",
        "status": "seal-complete / cascade-needed",
        "finance_market_keys": ["mexico-caribbean", "mexico-pacific"],
        "cluster_id": "mexico",
        "caribbean": CARIBBEAN_SPINE,
        "pacific": PACIFIC_SPINE,
        "all_route_ids": [r["route_id"] for r in CARIBBEAN_SPINE + PACIFIC_SPINE],
        "rules": [
            "Null beats wrong — do not invent pax or USD fares",
            "No grab-greenfield-census",
            "No catch-all didi market key for economics",
            "Finance spine route_ids must equal this list in shared mexico markets",
            "port_total / passenger_movements are allocation pools until direction+fare resolved",
        ],
    }

    receipt = {
        "at": utc_now(),
        "pr": 210,
        "g2": g2,
        "g3": g3,
        "didi_bind": didi_bind,
        "spine_path": str(SPINE.relative_to(ROOT)),
        "handoff_md": str(HANDOFF_MD.relative_to(ROOT)),
    }

    if not args.apply:
        print(json.dumps(receipt, indent=2, default=str)[:4000])
        return 0

    save(FBT, fbt)
    if isinstance(raw_routes, list):
        save(ROUTES, routes)
    else:
        raw_routes["features"] = routes
        save(ROUTES, raw_routes)
    save(RECEIPT, receipt)
    save(SPINE, spine)
    write_handoff_md(spine)
    print(json.dumps({"g2_accepted": g2["accepted_n"], "g3_patched": g3["n"], "spine_ids": spine["all_route_ids"]}, indent=2))
    print(f"wrote {RECEIPT}")
    print(f"wrote {SPINE}")
    print(f"wrote {HANDOFF_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
