#!/usr/bin/env python3
"""DiDi G4 — materialize Tasklet T1–T12 evidence return (PR #218).

Materializes only four usable passenger-volume candidates:
  rn-7e59f984abec  Paquera→Puntarenas     642,133 (2024 one-way)
  rn-eb4ca32edbef  Playa Naranjo→Puntarenas 317,859 (2024 one-way)
  rn-f451444da7fe  Rosario→Sabino Corsi   38,900 (2025–26 season)
  rn-04b92d6952d2  BA↔Colonia           2,177,670 (2024 both-dir movements)

Holds: Colombia C, Panama permission, DR/PE/TW/Egypt nulls, Galápagos/HK
benchmark-only, Chile featured empty, Tigre zone-only, El Gouna no inheritance.

Country-ref opex for CR/AR/UY is absent → demand+fare grounded; full opex P&L
remains pending country-reference (null beats wrong on opex).
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "finance" / "model"))

import importlib.util

_spec = importlib.util.spec_from_file_location("atom", ROOT / "finance/model/atom.py")
_atom = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_atom)

AGG = ROOT / "finance/recal/agg-didi.json"
GROWTH = ROOT / "finance/didi-growth-case.json"
SIDECAR = ROOT / "data-clean/economics_by_route_id.json"
ROUTES = ROOT / "data-clean/ROUTES.json"
CORR = ROOT / "finance/model/corridors.json"
DC = ROOT / "data-clean/partners/didi.json"
PITCH = ROOT / "partner-pitch/partners/didi.json"
SHEET_IDS = ROOT / "finance/PARTNER-SHEET-IDS.json"
OUT = ROOT / "handoff/didi-ex-china/waves/tasklet-proof"
RECEIPT = OUT / "GROK-G4-T2-T7-EVIDENCE-MATERIALIZE-2026-07-10.json"
RECEIPT_MD = OUT / "GROK-G4-T2-T7-EVIDENCE-MATERIALIZE-2026-07-10.md"

# FX / fares from prior Tasklet T3 bank (ARESEP + BCCR venta 453.77 CRC/USD on 2026-07-09)
CRC_PER_USD = 453.77
CR_FARES = {
    "rn-7e59f984abec": {"crc": 810, "usd": round(810 / CRC_PER_USD, 4)},  # Paquera adult
    "rn-eb4ca32edbef": {"crc": 1000, "usd": round(1000 / CRC_PER_USD, 4)},  # Naranjo adult
}

CANDIDATES = [
    {
        "route_id": "rn-7e59f984abec",
        "market": "costa-rica",
        "country": "Costa Rica",
        "pax": 642133,
        "period": "2024 calendar year",
        "unit": "one-way passenger journeys (named Paquera→Puntarenas direction)",
        "fare_usd": CR_FARES["rn-7e59f984abec"]["usd"],
        "fare_note": "ARESEP RE-0074-IT-2026 adult CRC 810 / BCCR venta 453.77 — benchmark not yield",
        "source": "MOPT 2024 statistical yearbook Cuadro 6.2",
        "ask": "T2",
        "pool_basis": "directional_one_way",
        "seasonal": False,
    },
    {
        "route_id": "rn-eb4ca32edbef",
        "market": "costa-rica",
        "country": "Costa Rica",
        "pax": 317859,
        "period": "2024 calendar year",
        "unit": "one-way passenger journeys (named Playa Naranjo→Puntarenas direction)",
        "fare_usd": CR_FARES["rn-eb4ca32edbef"]["usd"],
        "fare_note": "ARESEP adult CRC 1000 / BCCR venta 453.77 — benchmark not yield",
        "source": "MOPT 2024 statistical yearbook Cuadro 6.2",
        "ask": "T2",
        "pool_basis": "directional_one_way",
        "seasonal": False,
    },
    {
        "route_id": "rn-f451444da7fe",
        "market": "argentina",
        "country": "Argentina",
        "pax": 38900,
        "period": "2025-2026 summer operating season",
        "unit": "operator/port-authority passengers transported; aggregate directions",
        "fare_usd": None,  # no published fare in evidence return
        "fare_note": "fare null — no primary published tariff in Tasklet return",
        "source": "ENAPRO 2025-2026 season report",
        "ask": "T7",
        "pool_basis": "season_total_not_calendar_year",
        "seasonal": True,
    },
    {
        "route_id": "rn-04b92d6952d2",
        "market": "argentina",
        "country": "Argentina",
        "pax": 2177670,
        "period": "2024",
        "unit": "annual passenger movements both directions aggregated",
        "fare_usd": None,
        "fare_note": "fare null — international; no single operator tariff sealed",
        "source": "Uruguay national port-pair statistics 2024",
        "ask": "T7",
        "pool_basis": "both_directions_movements",
        "seasonal": False,
        "international": True,
    },
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load(p: Path) -> Any:
    return json.loads(p.read_text())


def save(p: Path, obj: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def economics_url() -> str:
    ids = load(SHEET_IDS) if SHEET_IDS.exists() else {}
    sid = (ids.get("didi") if isinstance(ids, dict) else None) or "1LY0Vp7FskgDDnEixkrEUCH0m-A_pYd2YCNuq3LF8ESM"
    return f"https://docs.google.com/spreadsheets/d/{sid}/edit"


def route_props(routes: list, rid: str) -> dict:
    for f in routes:
        p = f.get("properties") or {}
        if p.get("id") == rid:
            return p
    return {}


def num(x: Any) -> Any:
    return None if x is None else round(float(x), 2)


def build_corridor_def(c: dict, props: dict) -> dict:
    fare = c["fare_usd"]
    L3: dict[str, Any] = {
        "corridor_annual_oneway_pax": c["pax"],
        "pool_basis": c["pool_basis"],
        "_demand_record": {
            "value": c["pax"],
            "unit": c["unit"],
            "period": c["period"],
            "source_tier": "T1",
            "confidence": "high" if not c.get("seasonal") else "med",
            "source": c["source"],
            "ask": c["ask"],
            "method": "Tasklet PR #218 usable_for_base_case — exact published value, no doubling/halving/annualization",
        },
    }
    if fare is not None:
        L3["comparable_fare_usd_pax"] = fare
        L3["_fare_record"] = {
            "value": fare,
            "unit": "USD/pax/one-way comparable published tariff",
            "source_tier": "T1/T2",
            "confidence": "med",
            "note": c["fare_note"],
        }
    return {
        "from": props.get("from_label") or props.get("from"),
        "to": props.get("to_label") or props.get("to"),
        "distance_nm": props.get("distance_nm"),
        "vessel": "Pioneer II",
        "route_id": c["route_id"],
        "country": c["country"],
        "from_node_id": props.get("from_city_id"),
        "to_node_id": props.get("to_city_id"),
        "endpoint_boarding_points": {"from": props.get("from"), "to": props.get("to")},
        "archetype": "ridehail",
        "service_status": "current_scheduled" if not c.get("seasonal") else "seasonal",
        "in_phase1_shuttle": c["route_id"].startswith("rn-7e") or c["route_id"].startswith("rn-eb"),
        "_in_grounded_floor": fare is not None and not c.get("international"),
        "_source": "didi-t2-t7-evidence-2026-07-10",
        "_permission_status": "Incumbent regulated service; DiDi/Navier entry permission not transferred",
        "_international": bool(c.get("international")),
        "L3_locals": L3,
    }


def atom_mid(corr: dict) -> dict:
    """Run atom; attach demand pool sizing for vessels_supported when opex incomplete."""
    r = _atom.compute_atom(corr)
    pax = (corr.get("L3_locals") or {}).get("corridor_annual_oneway_pax")
    fare = r.get("navier_fare_usd") or r.get("comparable_fare_usd")
    # Transport spend pool = published pax × published comparable fare (when fare known)
    if pax and fare:
        pool = float(pax) * float(fare)
        r["pool_yr"] = round(pool, 2)
        # 10% capture sizing when vessel pax/year known
        ppy = r.get("pax_per_year") or 0
        if ppy:
            r["vessels_supported_10pct"] = int(math.floor((pax * 0.10) / ppy)) if ppy else None
            if r.get("revenue_per_boat_yr") and r["vessels_supported_10pct"] is not None:
                r["market_revenue_yr"] = round(r["revenue_per_boat_yr"] * r["vessels_supported_10pct"], 0)
    else:
        r["pool_yr"] = None
    r["demand_confidence"] = "high" if pax and not corr.get("_international") else "med"
    r["route_id"] = corr.get("route_id")
    r["corridor"] = f"{corr.get('from')} -> {corr.get('to')}"
    r["distance_nm"] = corr.get("distance_nm")
    return r


def scenario_band(mid: dict, factor: float) -> dict:
    out = copy.deepcopy(mid)
    for k in ("revenue_per_boat_yr", "ebitda_per_boat_yr", "market_revenue_yr", "pax_per_year"):
        if out.get(k) is not None:
            out[k] = round(float(out[k]) * factor, 2 if k != "pax_per_year" else 0)
    if out.get("vessels_supported_10pct") is not None:
        out["vessels_supported_10pct"] = max(1, int(round(out["vessels_supported_10pct"] * factor)))
    return out


def agg_row(c: dict, corr: dict, mid: dict) -> dict:
    fare = c["fare_usd"]
    # Prefer published comparable (pre-refare) for pool when available
    pub_fare = fare
    pool = round(c["pax"] * pub_fare, 2) if pub_fare else None
    status = "grounded" if (pub_fare is not None and mid.get("annual_opex") is not None) else "demand_grounded"
    if mid.get("annual_opex") is None and pub_fare is not None:
        status = "demand_grounded"  # fare+demand yes, opex country-ref pending
    return {
        "market": c["market"],
        "country": c["country"],
        "pool_yr": pool if pool is not None else mid.get("pool_yr"),
        "corridor": mid.get("corridor"),
        "nm": corr.get("distance_nm"),
        "fare": pub_fare if pub_fare is not None else mid.get("comparable_fare_usd"),
        "is_dup": False,
        "_subset_of": None,
        "_forward_sam": False,
        "_tier": None,
        "_in_grounded_floor": bool(corr.get("_in_grounded_floor")) and status == "grounded",
        "route_id": c["route_id"],
        "_ceiling_ratio": 1.0,
        "thin": scenario_band(mid, 0.7),
        "mid": mid,
        "full": scenario_band(mid, 1.3),
        "demand_conf": "high" if not c.get("seasonal") else "med",
        "status": status,
        "est_basis": None,
        "_demand_period": c["period"],
        "_demand_unit": c["unit"],
        "_source": "tasklet/pr-218 + grok-g4-2026-07-10",
        "_opex_status": "pending_country_reference" if mid.get("annual_opex") is None else "modeled",
    }


def economics_record(row: dict) -> dict:
    mid = row.get("mid") or {}
    thin = row.get("thin") or {}
    full = row.get("full") or {}
    status = row.get("status")
    return {
        "corridor": row.get("corridor"),
        "market": (row.get("market") or "").replace("-", " ").title(),
        "country": row.get("country"),
        "distance_nm": row.get("nm"),
        "status": status,
        "demand_confidence": row.get("demand_conf"),
        "fare_today_usd": mid.get("comparable_fare_usd") or row.get("fare"),
        "navier_fare_usd": mid.get("navier_fare_usd"),
        "vessel": mid.get("vessel"),
        "mid": {
            "rev_per_boat_yr": num(mid.get("revenue_per_boat_yr")),
            "margin": num(mid.get("margin")),
            "payback_years": num(mid.get("payback_years")),
            "co2_saved_t_per_boat_yr": num(mid.get("co2_saved_t_per_boat_yr")),
            "vessels_10pct": mid.get("vessels_supported_10pct"),
            "market_rev_yr": num(mid.get("market_revenue_yr")),
        },
        "band": {
            "payback_years": [
                num(thin.get("payback_years")),
                num(mid.get("payback_years")),
                num(full.get("payback_years")),
            ],
            "vessels_10pct": [
                thin.get("vessels_supported_10pct"),
                mid.get("vessels_supported_10pct"),
                full.get("vessels_supported_10pct"),
            ],
        },
        "provenance": {
            "fare": row.get("_opex_status") and (
                "published comparable adult benchmark — not operator realized yield"
                if row.get("fare") is not None
                else "null_until_sourced"
            ),
            "demand": "sourced corridor demand — Tasklet PR #218 usable_for_base_case",
            "permission": "required_not_transferred",
            "opex": row.get("_opex_status"),
            "source": "finance/recal/agg-didi.json",
            "lane": "didi-g4-t2-t7-2026-07-10",
            "demand_period": row.get("_demand_period"),
            "demand_unit": row.get("_demand_unit"),
            "sealed_at": utc_now(),
        },
        "annual_one_way_pax": (row.get("mid") or {}).get("_demand_pax") or None,
    }


def stamp_partner(didi: dict, rows: list[dict], routes_by_id: dict) -> dict:
    """Update featured/journeys economics; Tigre zone; Chile empty; Colombia hold; Egypt caveats."""
    by_rid = {r["route_id"]: r for r in rows}

    def feat_entry(rid: str) -> dict:
        p = routes_by_id.get(rid) or {}
        return {
            "route_id": rid,
            "from_label": p.get("from_label"),
            "to_label": p.get("to_label"),
            "cluster_id": p.get("cluster_id"),
        }

    for m in didi.get("markets") or []:
        mid = m.get("id") or m.get("slug")
        if mid == "costa-rica":
            feats = [
                feat_entry("rn-7e59f984abec"),
                feat_entry("rn-eb4ca32edbef"),
            ]
            # keep existing papagayo if present
            existing = {x.get("route_id") for x in (m.get("featured_routes") or [])}
            for f in feats:
                if f["route_id"] not in existing:
                    m.setdefault("featured_routes", []).insert(0, f)
            # ensure primary two at front
            m["featured_routes"] = feats + [
                x for x in (m.get("featured_routes") or []) if x.get("route_id") not in {f["route_id"] for f in feats}
            ]
            journeys = []
            for rid in ("rn-7e59f984abec", "rn-eb4ca32edbef"):
                p = routes_by_id.get(rid) or {}
                row = by_rid.get(rid) or {}
                journeys.append(
                    {
                        "from": p.get("from_label"),
                        "to": p.get("to_label"),
                        "from_label": p.get("from_label"),
                        "to_label": p.get("to_label"),
                        "label": f"{p.get('from_label')} → {p.get('to_label')}",
                        "route_id": rid,
                        "distance_nm": p.get("distance_nm"),
                        "_link_status": "linked-t2-evidence",
                        "_link_source": "tasklet/pr-218",
                        "economics_status": row.get("status") or "demand_grounded",
                        "annual_one_way_pax": next(c["pax"] for c in CANDIDATES if c["route_id"] == rid),
                        "comparable_fare_usd": row.get("fare"),
                        "today": "Car/passenger ferry with published demand.",
                        "with_navier": "A clean high-frequency hop once entry permission is secured.",
                        "platform": "Pioneer II",
                        "archetype": "commuter",
                    }
                )
            m["journeys_unlocked"] = journeys
            for ph in m.get("phases") or []:
                ph["featured_routes"] = list(m["featured_routes"][:2])

        if mid == "argentina":
            # Rosario featured (already may exist); do NOT feature international BA–Colonia
            ros = feat_entry("rn-f451444da7fe")
            fr = m.get("featured_routes") or []
            fr = [x for x in fr if x.get("route_id") != "rn-04b92d6952d2"]
            if not any(x.get("route_id") == "rn-f451444da7fe" for x in fr):
                fr.insert(0, ros)
            m["featured_routes"] = fr
            # Tigre zone note
            caveats = m.get("_operation_caveats") or []
            note = "Tigre: official DiDi zone proof only — no ferry-ramp/supply claim"
            if note not in caveats:
                caveats.append(note)
            caveats = [c for c in caveats if "Tigre polygon unproven" not in c]
            caveats.append("BA–Colonia demand banked as international movements — not domestic-featured")
            caveats.append("Rosario–Sabino Corsi: 38,900 is 2025–26 season total, not calendar year")
            m["_operation_caveats"] = list(dict.fromkeys(caveats))
            # journeys
            p = routes_by_id.get("rn-f451444da7fe") or {}
            m["journeys_unlocked"] = [
                {
                    "from": p.get("from_label"),
                    "to": p.get("to_label"),
                    "from_label": p.get("from_label"),
                    "to_label": p.get("to_label"),
                    "label": f"{p.get('from_label')} → {p.get('to_label')}",
                    "route_id": "rn-f451444da7fe",
                    "distance_nm": p.get("distance_nm"),
                    "_link_status": "linked-t7-evidence",
                    "_link_source": "tasklet/pr-218",
                    "economics_status": "demand_grounded_seasonal",
                    "annual_one_way_pax": 38900,
                    "comparable_fare_usd": None,
                    "today": "Seasonal island ferry service.",
                    "with_navier": "A clean seasonal hop once fare and entry terms are sealed.",
                    "platform": "Pioneer II",
                    "archetype": "tourism",
                }
            ]

        if mid == "chile":
            m["featured_routes"] = []
            for ph in m.get("phases") or []:
                ph["featured_routes"] = []
            caveats = m.get("_operation_caveats") or []
            caveats.append("Featured empty — ferry towns not in official DiDi CL directory")
            m["_operation_caveats"] = list(dict.fromkeys(caveats))

        if mid == "colombia":
            caveats = m.get("_operation_caveats") or []
            caveats.append("Finance decision C hold — no exact OD demand/fare for rn-aa790551baa7")
            m["_operation_caveats"] = list(dict.fromkeys(caveats))

        if mid == "egypt":
            caveats = m.get("_operation_caveats") or []
            for n in (
                "Do not extend Hurghada proof to El Gouna",
                "NEOM is Saudi Arabia only — not Egypt domestic",
                "Egypt berth coordinates remain null for candidate BPs",
            ):
                if n not in caveats:
                    caveats.append(n)
            m["_operation_caveats"] = caveats

    # map_scope held updates
    ms = didi.setdefault("_map_scope", {})
    held = ms.setdefault("_held", {})
    held["tigre-argentina"] = (
        "official DiDi zone/service-area proof (T8) — city-level only; "
        "no ferry-ramp pickup or supply claim"
    )
    # remove older "Tigre polygon unproven" if present as opposite
    held["el-gouna-component"] = "no inheritance from Hurghada; combined city ID is leakage risk"
    held["neom-sindalah-ksa"] = "Saudi Arabia only — not Egypt geography"

    didi["economics_url"] = economics_url()
    didi["_economics_status"] = "brazil_mexico_cr_ar_partial"
    didi["_didi_g4_t2_t7"] = {
        "at": utc_now(),
        "materialized_route_ids": [c["route_id"] for c in CANDIDATES],
        "colombia": "C_hold",
        "chile_featured": [],
        "source": "tasklet/pr-218",
    }
    return didi


def recompute_rollup(agg: dict) -> None:
    rows = agg.get("rows") or []
    grounded = [r for r in rows if r.get("status") == "grounded" and r.get("_in_grounded_floor")]
    demand_g = [r for r in rows if r.get("status") == "demand_grounded"]
    est = [r for r in rows if r.get("status") == "estimated"]

    def sum_field(rs, path):
        t = 0.0
        for r in rs:
            mid = r.get("mid") or {}
            v = mid.get(path)
            if v is not None:
                t += float(v)
        return round(t, 2)

    fleet = sum((r.get("mid") or {}).get("vessels_supported_10pct") or 0 for r in grounded)
    pool = sum(float(r["pool_yr"]) for r in grounded + demand_g if r.get("pool_yr"))
    mrev = sum_field(grounded, "market_revenue_yr")
    co2 = sum_field(grounded, "market_co2_saved_t_yr")
    rollup = agg.get("rollup") or {}
    rollup.update(
        {
            "partner": "didi",
            "n_corridors_total": len(rows),
            "n_grounded": len(grounded),
            "n_demand_grounded_opex_pending": len(demand_g),
            "n_estimated": len(est),
            "grounded_floor": {
                "fleet": fleet,
                "market_rev_yr": mrev,
                "co2_saved_t_yr": co2,
                "transport_spend_pool_yr": round(pool, 2),
                "effective_capture": round(mrev / pool, 4) if pool else None,
            },
            "_t2_t7_note": "CR/AR demand_grounded rows contribute to pool but not vessel opex floor until country-reference opex lands",
        }
    )
    agg["rollup"] = rollup


def main() -> int:
    routes = load(ROUTES)
    routes_by_id = {}
    for f in routes:
        p = f.get("properties") or {}
        if p.get("id"):
            routes_by_id[p["id"]] = p

    corr_doc = load(CORR)
    markets = corr_doc.setdefault("markets", {})

    # Ensure market shells
    for mid, country, label in (
        ("costa-rica", "Costa Rica", "Costa Rica — Nicoya"),
        ("argentina", "Argentina", "Argentina"),
    ):
        markets.setdefault(
            mid,
            {
                "display_name": label,
                "partner": "didi",
                "country": country,
                "country_slug": mid,
                "currency": "USD",
                "scope": "ex-china-latam",
                "archetype": "ridehail",
                "_tier": "t2_t7_evidence",
                "corridors": [],
            },
        )

    new_rows = []
    corridor_defs = []
    for c in CANDIDATES:
        props = route_props(routes, c["route_id"])
        if not props:
            print("MISSING ROUTE", c["route_id"], file=sys.stderr)
            continue
        cdef = build_corridor_def(c, props)
        corridor_defs.append(cdef)
        mid = atom_mid(cdef)
        mid["_demand_pax"] = c["pax"]
        row = agg_row(c, cdef, mid)
        # store pax on row for receipts
        row["mid"]["_demand_pax"] = c["pax"]
        new_rows.append(row)

        # upsert into corridors.json market
        m = markets[c["market"]]
        cors = m.setdefault("corridors", [])
        cors = [x for x in cors if x.get("route_id") != c["route_id"]]
        cors.append(cdef)
        m["corridors"] = cors

    corr_doc["_didi_t2_t7_evidence"] = {
        "at": utc_now(),
        "route_ids": [c["route_id"] for c in CANDIDATES],
        "source": "tasklet/pr-218",
        "opex_note": "Costa Rica / Argentina / Uruguay absent from country-reference — opex null until sourced",
    }
    save(CORR, corr_doc)

    # agg-didi upsert
    agg = load(AGG) if AGG.exists() else {"rows": [], "rollup": {}}
    rows = [r for r in (agg.get("rows") or []) if r.get("route_id") not in {c["route_id"] for c in CANDIDATES}]
    rows.extend(new_rows)
    agg["rows"] = rows
    recompute_rollup(agg)
    save(AGG, agg)

    # economics sidecar
    side = load(SIDECAR) if SIDECAR.exists() else {"_meta": {}, "records": {}}
    recs = side.get("records")
    if not isinstance(recs, dict):
        recs = {}
        side["records"] = recs
    for row in new_rows:
        rid = row["route_id"]
        rec = economics_record(row)
        rec["annual_one_way_pax"] = row["mid"].get("_demand_pax")
        recs[rid] = rec
    side.setdefault("_meta", {})
    side["_meta"]["didi_t2_t7_g4"] = {
        "at": utc_now(),
        "routes": [c["route_id"] for c in CANDIDATES],
        "added": len(new_rows),
    }
    side["_meta"]["generated"] = utc_now()
    # write compact-ish
    SIDECAR.write_text(json.dumps(side, indent=1, ensure_ascii=False) + "\n")

    # partner stamp
    didi = load(DC)
    didi = stamp_partner(didi, new_rows, routes_by_id)
    save(DC, didi)
    if PITCH.exists():
        shutil.copyfile(DC, PITCH)

    # growth case light touch
    if GROWTH.exists():
        g = load(GROWTH)
        g["_t2_t7_materialize"] = {
            "at": utc_now(),
            "routes": [c["route_id"] for c in CANDIDATES],
            "note": "Demand banked; opex pending country-reference for CR/AR",
        }
        save(GROWTH, g)

    # gates
    gates = {}
    for name, cmd in [
        ("gate_g", [sys.executable, str(ROOT / "scripts/audit_partner_copy.py")]),
        ("fidelity_didi", [sys.executable, str(ROOT / "scripts/audit_proposal_fidelity.py"), "--partner", "didi"]),
    ]:
        try:
            r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=180)
            gates[name] = {"exit": r.returncode, "pass": r.returncode == 0, "tail": (r.stdout or r.stderr or "")[-500:]}
        except Exception as e:
            gates[name] = {"pass": False, "error": str(e)}

    # inheritance dott/voi/didi strict if possible
    try:
        r = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/validate_partner_inheritance.py"),
                "--partner",
                "didi",
                "dott",
                "voi",
                "--strict",
                "--json",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=180,
        )
        gates["inheritance_strict"] = {
            "exit": r.returncode,
            "pass": r.returncode == 0,
            "tail": (r.stdout or r.stderr or "")[-800:],
        }
    except Exception as e:
        gates["inheritance_strict"] = {"pass": None, "error": str(e)}

    receipt = {
        "at": utc_now(),
        "lane": "DiDi G4 T2/T7 evidence materialize after PR #218",
        "status": "demand_materialized / opex_pending_country_ref / finance_partial",
        "upstream_prs": [217, 218],
        "materialized": [
            {
                "route_id": c["route_id"],
                "pax": c["pax"],
                "period": c["period"],
                "fare_usd": c["fare_usd"],
                "status": next((r["status"] for r in new_rows if r["route_id"] == c["route_id"]), None),
                "pool_yr": next((r.get("pool_yr") for r in new_rows if r["route_id"] == c["route_id"]), None),
            }
            for c in CANDIDATES
        ],
        "holds": {
            "colombia": "C_hold",
            "panama": "permission_required",
            "dominican_republic": "null",
            "galapagos": "benchmark_only_no_annualization",
            "peru": "null",
            "hong_kong": "historical_benchmark_only",
            "taiwan": "hard_hold",
            "egypt_bps": "berth_coords_null",
            "chile_featured": [],
            "tigre": "zone_proof_only",
            "el_gouna": "no_hurghada_inheritance",
            "neom": "saudi_only",
        },
        "gates": gates,
        "do_not": [
            "No Galápagos annualization",
            "No HK 2017 refresh",
            "No Colombia finance",
            "No opex invent for CR/AR without country-reference",
            "Published fares are benchmarks not yield",
        ],
    }
    save(RECEIPT, receipt)
    md = [
        "# Grok — DiDi T2/T7 evidence materialize",
        "",
        f"**UTC:** {receipt['at']}",
        f"**Status:** `{receipt['status']}`",
        "",
        "## Materialized demand",
    ]
    for m in receipt["materialized"]:
        md.append(
            f"- `{m['route_id']}` — pax **{m['pax']:,}** ({m['period']}) — "
            f"fare {m['fare_usd']} — status `{m['status']}` — pool ${m['pool_yr']}"
        )
    md += [
        "",
        "## Holds retained",
        "- Colombia C · Panama permission · DR/PE/TW/Egypt passenger nulls",
        "- Galápagos/HK benchmark-only · Chile featured empty · Tigre zone-only",
        "- El Gouna no Hurghada inheritance · NEOM Saudi only",
        "",
        "## Gates",
    ]
    for k, v in gates.items():
        md.append(f"- **{k}:** {'PASS' if v.get('pass') else 'FAIL/NA'}")
    md.append("")
    md.append(f"Machine: `{RECEIPT.relative_to(ROOT)}`")
    RECEIPT_MD.write_text("\n".join(md) + "\n")

    print(json.dumps({
        "materialized": receipt["materialized"],
        "gates": {k: v.get("pass") for k, v in gates.items()},
    }, indent=2))
    return 0 if gates.get("gate_g", {}).get("pass") and gates.get("fidelity_didi", {}).get("pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())
