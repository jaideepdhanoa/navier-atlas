#!/usr/bin/env python3
"""
PR #65 — Yassir + Caribbean-mobility deterministic Grok lane.

  - Algeria full mint (cities/BPs/routes)
  - Yassir Morocco/Tunisia/Algeria route seal + partner bind
  - Caribbean country-reference promotion + corridor wire + cascade
  - data-clean sync + execution report
"""
from __future__ import annotations

import copy
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
HANDOFF65 = ROOT / "handoff" / "partner-map-model" / "caribbean-yassir-gold-2026-06-21"
HANDOFF = ROOT / "handoff" / "partner-map-model"
PARTNERS = ROOT / "partner-pitch" / "partners"
DC_PARTNERS = ROOT / "data-clean" / "partners"
FINANCE = ROOT / "finance"
MODEL = FINANCE / "model"
RECAL = FINANCE / "recal"

# Curated exact binds: (market_key, from_norm, to_norm) -> route_id
YASSIR_EXACT_BINDS: dict[tuple[str, str, str], str] = {
    ("yassir-tunisia", "la goulette", "sidi bou said"): "rn-74a61d330456",
    ("yassir-morocco", "casablanca", "mohammedia"): "rn-967b688b5591",
    ("yassir-morocco", "casablanca", "rabat"): "rn-a30214f88daf",
    ("yassir-morocco", "agadir marina", "taghazout"): "e__agadir-essaouira-morocco__agadir__agadir-essaouira-morocco__taghazout",
    ("yassir-morocco", "al hoceima marina", "cala iris"): "rn-c2a689f7600d",
    ("yassir-morocco", "tanger med", "ceuta"): "rn-24c3aa4c2acf",
    ("yassir-morocco", "tangier marina bay", "tanger med"): "rn-c92594b54b8f",
}

CARIBBEAN_EXACT_BINDS: dict[str, str] = {
    "carib-bahamas-nassau-paradise-island-water-layer": "ics-05ae8c432d",
    "carib-usvi-red-hook-cruz-bay-short-hop": "ics-c24cfec613",
    "carib-barbados-bridgetown-port-waterfront-extension": "rn-3a37afb0fb5c",
    # San Juan–Cataño: held until dedicated mint; do not bind to Safe Harbor proxy
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def norm(s: str | None) -> str:
    if not s:
        return ""
    s = s.strip().lower()
    s = re.sub(r"\([^)]*\)", "", s)
    s = re.sub(r"[/|]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def route_index() -> dict[str, dict]:
    routes = load_json(ROOT / "data-clean" / "ROUTES.json")
    feats = routes if isinstance(routes, list) else routes.get("features", [])
    idx: dict[str, dict] = {}
    for r in feats:
        p = r.get("properties", r)
        rid = p.get("id")
        if rid:
            idx[rid] = p
    return idx


def match_route_by_cities_and_distance(
    ridx: dict[str, dict],
    from_city: str | None,
    to_city: str | None,
    target_nm: float | None,
    *,
    tol: float = 3.0,
) -> str | None:
    best_id = None
    best_delta = 999.0
    for rid, p in ridx.items():
        if p.get("_quarantine"):
            continue
        fc, tc = p.get("from_city_id"), p.get("to_city_id")
        if from_city and fc != from_city:
            continue
        if to_city and tc != to_city:
            continue
        d = p.get("distance_nm")
        if target_nm is None or d is None:
            return rid
        delta = abs(float(d) - float(target_nm))
        if delta < best_delta:
            best_delta = delta
            best_id = rid
    if best_id and best_delta <= tol:
        return best_id
    return None


def promote_country_references(stats: dict) -> None:
    cref_path = MODEL / "country-reference.json"
    cref = load_json(cref_path)
    countries = cref.setdefault("countries", {})

    algeria_draft = load_json(HANDOFF65 / "algeria-country-reference-draft.json")
    row = algeria_draft.get("proposed_country_reference_row", {}).get("Algeria")
    if row:
        countries["Algeria"] = row
        stats["country_ref_promoted"].append("Algeria")

    carib_draft = load_json(HANDOFF65 / "caribbean-country-reference-draft-batch-1.json")
    for country, row in (carib_draft.get("countries") or {}).items():
        flat = {
            "captain_usd_yr": row.get("captain_usd_yr"),
            "energy_usd_kwh": row.get("energy_usd_kwh"),
            "grid_co2_kg_kwh": row.get("grid_co2_kg_kwh"),
            "marina_overhead_usd_yr": row.get("marina_overhead_usd_yr"),
            "cost_index": row.get("cost_index"),
        }
        countries[country] = flat
        stats["country_ref_promoted"].append(country)

    save_json(cref_path, cref)


def wire_yassir_corridors(ridx: dict[str, dict], stats: dict) -> None:
    corridors = load_json(MODEL / "corridors.json")
    markets = corridors["markets"]

    algeria_mint = load_json(HANDOFF / "algeria-yassir-mint-report.json")

    for mk in ("yassir-tunisia", "yassir-morocco"):
        if mk not in markets:
            continue
        for cor in markets[mk].get("corridors", []):
            key = (mk, norm(cor.get("from")), norm(cor.get("to")))
            rid = YASSIR_EXACT_BINDS.get(key)
            if not rid:
                rid = match_route_by_cities_and_distance(
                    ridx,
                    cor.get("from_node_id"),
                    cor.get("to_node_id"),
                    cor.get("distance_nm"),
                )
            if rid and rid in ridx:
                cor["route_id"] = rid
                cor["_route_id_status"] = "sealed_grok_pr65"
                cor["_grok_seal_at"] = utc_now()
                stats["yassir_corridors_sealed"] += 1
            else:
                cor["_route_id_status"] = "held_null"
                stats["yassir_corridors_held"] += 1

    # Algeria market
    algeria_corridors = []
    for m in algeria_mint.get("minted", []):
        if m.get("economics_status") == "roadmap_excluded":
            econ = "roadmap_excluded"
        else:
            econ = "commercial_now"
        algeria_corridors.append({
            "route_id": m["route_id"],
            "from": m["from_label"],
            "to": m["to_label"],
            "distance_nm": m["distance_nm"],
            "vessel": "Pioneer II" if m["distance_nm"] <= 70 else "Quanta-LR",
            "archetype": "urban_coastal",
            "from_node_id": m["from_bp"],
            "to_node_id": m["to_bp"],
            "from_city_id": m["from_city_id"],
            "to_city_id": m["to_city_id"],
            "country": "Algeria",
            "partner": "yassir",
            "_candidate_id": m["candidate_id"],
            "_vessel_gate": m["vessel_gate"],
            "_economics_status": econ,
        })
        stats["algeria_corridors_added"] += 1

    # Tasklet demand/fare from completion packet
    completion = load_json(HANDOFF65 / "yassir-algeria-tasklet-research-completion-2026-06-21.json")
    demand_by_cand = {d["candidate_id"]: d for d in completion.get("route_demand_fare_assumptions", [])}
    for cor in algeria_corridors:
        cand = demand_by_cand.get(cor["_candidate_id"], {})
        fare = cand.get("fare_assumption", {})
        demand = cand.get("demand_assumption", {})
        if fare.get("model_fare_usd_selected"):
            cor.setdefault("L3_locals", {})["comparable_fare_usd_pax"] = fare["model_fare_usd_selected"]
        if demand.get("selected_annual_one_way_passengers"):
            cor.setdefault("L3_locals", {})["corridor_annual_oneway_pax"] = demand["selected_annual_one_way_passengers"]

    markets["yassir-algeria"] = {
        "partner": "yassir",
        "region": "Maghreb",
        "label": "Yassir Algeria — batch-1 sealed corridors",
        "fleet_basis": "aspirational",
        "capture_rate": 0.15,
        "_scope_isolated": True,
        "_tier": "B",
        "corridors": algeria_corridors,
    }

    save_json(MODEL / "corridors.json", corridors)


def wire_caribbean_corridors(ridx: dict[str, dict], stats: dict) -> None:
    corridors = load_json(MODEL / "corridors.json")
    markets = corridors["markets"]
    inputs = load_json(HANDOFF65 / "caribbean-route-economics-inputs-batch-1.json")

    carib_corridors = []
    for row in inputs.get("routes", []):
        cand = row["candidate_id"]
        rid = CARIBBEAN_EXACT_BINDS.get(cand)
        if not rid and cand != "carib-puerto-rico-san-juan-catano-metro-water-layer":
            cities = row.get("atlas_city_ids") or []
            city = cities[0] if cities else None
            est = (row.get("distance_nm_estimate") or {}).get("value")
            rid = match_route_by_cities_and_distance(ridx, city, city, est, tol=2.5)

        cor = {
            "route_id": rid,
            "from": row.get("from"),
            "to": row.get("to"),
            "distance_nm": (row.get("distance_nm_estimate") or {}).get("value"),
            "vessel": row.get("vessel", "Pioneer II"),
            "archetype": "tourism",
            "country": row.get("market"),
            "partner": "caribbean-mobility",
            "_candidate_id": cand,
            "_route_id_status": "sealed_grok_pr65" if rid else "held_null",
        }
        if rid and rid in ridx:
            cor["distance_nm"] = ridx[rid].get("distance_nm", cor["distance_nm"])
            cor["from_node_id"] = ridx[rid].get("from")
            cor["to_node_id"] = ridx[rid].get("to")
            cor["from_city_id"] = ridx[rid].get("from_city_id")
            cor["to_city_id"] = ridx[rid].get("to_city_id")
            stats["caribbean_corridors_sealed"] += 1
        else:
            stats["caribbean_corridors_held"] += 1

        fare = row.get("fare") or {}
        demand = row.get("demand") or {}
        l3: dict[str, Any] = {}
        if fare.get("navier_draft_fare_usd_pax_one_way"):
            l3["comparable_fare_usd_pax"] = fare["navier_draft_fare_usd_pax_one_way"]
        if demand.get("corridor_annual_oneway_pax_draft"):
            l3["corridor_annual_oneway_pax"] = demand["corridor_annual_oneway_pax_draft"]
        if l3:
            cor["L3_locals"] = l3

        carib_corridors.append(cor)

    markets["caribbean-mobility"] = {
        "partner": "caribbean-mobility",
        "region": "Caribbean",
        "label": "Caribbean Mobility Partner — batch-1 prove markets",
        "fleet_basis": "aspirational",
        "capture_rate": 0.12,
        "_scope_isolated": True,
        "corridors": carib_corridors,
    }
    save_json(MODEL / "corridors.json", corridors)


def bind_route_cards(obj: dict, bind_map: dict[str, str], ridx: dict[str, dict], stats: dict, *, prefix: str) -> None:
    containers: list[list] = []
    for ph in obj.get("phases", []) or []:
        containers.append(ph.get("featured_routes", []) or [])
    for m in obj.get("markets", []) or []:
        for ph in m.get("phases", []) or []:
            containers.append(ph.get("featured_routes", []) or [])
        containers.append(m.get("featured_routes", []) or [])

    for routes in containers:
        for card in routes:
            if not isinstance(card, dict):
                continue
            label = norm(card.get("label") or f"{card.get('from', '')} {card.get('to', '')}")
            rid = None
            for k, v in bind_map.items():
                if k in label or label in k:
                    rid = v
                    break
            if not rid:
                rid = card.get("route_id")
            if rid and rid in ridx:
                p = ridx[rid]
                card["route_id"] = rid
                card["route_ids"] = [rid]
                card["distance_nm"] = p.get("distance_nm")
                card["from_node_id"] = p.get("from")
                card["to_node_id"] = p.get("to")
                card["_bind_status"] = "sealed_grok_pr65"
                stats[f"{prefix}_cards_sealed"] += 1
            elif card.get("route_id") is None:
                stats[f"{prefix}_cards_held"] += 1


def build_yassir_bind_map(ridx: dict[str, dict]) -> dict[str, str]:
    m: dict[str, str] = {}
    corridors = load_json(MODEL / "corridors.json")["markets"]
    for mk in ("yassir-tunisia", "yassir-morocco", "yassir-algeria"):
        for cor in corridors.get(mk, {}).get("corridors", []):
            rid = cor.get("route_id")
            if rid:
                m[norm(f"{cor.get('from')} {cor.get('to')}")] = rid
                m[norm(cor.get("from", ""))] = rid
    return m


def build_caribbean_bind_map() -> dict[str, str]:
    corridors = load_json(MODEL / "corridors.json")["markets"]
    m: dict[str, str] = {}
    for cor in corridors.get("caribbean-mobility", {}).get("corridors", []):
        rid = cor.get("route_id")
        if rid:
            m[norm(f"{cor.get('from')} {cor.get('to')}")] = rid
    return m


def update_yassir_algeria_display(yassir: dict, ridx: dict[str, dict], stats: dict) -> None:
    """Add Algeria market block after seal."""
    algeria_market = {
        "id": "yassir-algeria",
        "market_id": "yassir-algeria",
        "label": "Algeria — Yassir home market unlock",
        "display": "Algeria — Yassir home market unlock",
        "country": "Algeria",
        "anchor_cities": ["algiers-algeria", "bejaia-algeria", "oran-algeria", "mostaganem-algeria"],
        "evidence_tier": "country_supported",
        "economics_status": "model_cascaded_after_grok_seal",
        "phases": [],
        "featured_routes": [],
    }
    corridors = load_json(MODEL / "corridors.json")["markets"].get("yassir-algeria", {}).get("corridors", [])
    for cor in corridors:
        rid = cor.get("route_id")
        if not rid:
            continue
        algeria_market["featured_routes"].append({
            "label": f"{cor.get('from')} ↔ {cor.get('to')}",
            "from": cor.get("from"),
            "to": cor.get("to"),
            "route_id": rid,
            "distance_nm": cor.get("distance_nm"),
            "vessel_gate": cor.get("_vessel_gate"),
            "economics_status": cor.get("_economics_status"),
            "_bind_status": "sealed_grok_pr65",
        })
        stats["algeria_display_routes"] += 1

    markets = yassir.setdefault("markets", [])
    replaced = False
    for i, m in enumerate(markets):
        if m.get("market_id") == "yassir-algeria" or m.get("id") == "yassir-algeria":
            markets[i] = {**m, **algeria_market}
            replaced = True
            break
    if not replaced:
        markets.append(algeria_market)

    yassir.setdefault("network_footprint", [])
    if "Algeria" not in yassir["network_footprint"]:
        yassir["network_footprint"].append("Algeria")

    hero = yassir.get("hero", {})
    hero["subtitle"] = (
        "Morocco, Tunisia, and Algeria batch-1 corridors are now geometry-sealed where Tasklet evidence "
        "and Grok mint/bind succeeded; held-null rows remain explicit."
    )
    yassir["hero"] = hero


def run_finance_cascade(partner: str, stats: dict) -> None:
    agg_out = RECAL / f"agg-{partner}.json"
    growth_out = RECAL / f"growth-{partner}.json"
    frontend_out = RECAL / f"growth-frontend-{partner}.json"
    subprocess.run(
        [sys.executable, str(MODEL / "aggregate.py"), "--partner", partner, "--json", str(agg_out)],
        check=True,
        cwd=str(ROOT),
    )
    subprocess.run(
        [sys.executable, str(MODEL / "growth.py"), "--partner", partner, "--agg", str(agg_out), "--json", str(growth_out)],
        check=True,
        cwd=str(ROOT),
    )
    subprocess.run(
        [
            sys.executable,
            str(MODEL / "growth_frontend_block.py"),
            "--partner",
            partner,
            "--growth",
            str(growth_out),
            "--rollup",
            str(agg_out),
            "--out",
            str(frontend_out),
        ],
        check=True,
        cwd=str(ROOT),
    )
    partner_json = PARTNERS / f"{partner}.json"
    subprocess.run(
        [
            sys.executable,
            str(FINANCE / "splice_growth_into_partner.py"),
            "--partner",
            partner,
            "--growth",
            str(growth_out),
            "--frontend",
            str(frontend_out),
            "--partner-json",
            str(partner_json),
        ],
        check=True,
        cwd=str(ROOT),
    )
    stats["finance_cascaded"].append(partner)


def sync_data_clean(partners: list[str]) -> None:
    DC_PARTNERS.mkdir(parents=True, exist_ok=True)
    for p in partners:
        src = PARTNERS / f"{p}.json"
        if src.exists():
            save_json(DC_PARTNERS / f"{p}.json", load_json(src))


def main() -> int:
    stats: dict[str, Any] = {
        "at": utc_now(),
        "lane": "grok/execute_pr65_yassir_caribbean",
        "country_ref_promoted": [],
        "yassir_corridors_sealed": 0,
        "yassir_corridors_held": 0,
        "algeria_corridors_added": 0,
        "algeria_display_routes": 0,
        "caribbean_corridors_sealed": 0,
        "caribbean_corridors_held": 0,
        "yassir_cards_sealed": 0,
        "yassir_cards_held": 0,
        "caribbean_cards_sealed": 0,
        "caribbean_cards_held": 0,
        "finance_cascaded": [],
    }

    print("→ mint Algeria geometry")
    subprocess.run([sys.executable, str(ROOT / "scripts/grok-econ-reseal/mint_algeria_yassir_geometry.py")], check=True)

    print("→ promote country-reference drafts")
    promote_country_references(stats)

    ridx = route_index()

    print("→ wire Yassir + Caribbean corridors")
    wire_yassir_corridors(ridx, stats)
    wire_caribbean_corridors(ridx, stats)

    print("→ bind partner JSON")
    yassir = load_json(PARTNERS / "yassir.json")
    caribbean = load_json(PARTNERS / "caribbean-mobility.json")

    ybind = build_yassir_bind_map(ridx)
    cbind = build_caribbean_bind_map()
    bind_route_cards(yassir, ybind, ridx, stats, prefix="yassir")
    bind_route_cards(caribbean, cbind, ridx, stats, prefix="caribbean")
    update_yassir_algeria_display(yassir, ridx, stats)

    # Update economics status badges
    yassir.setdefault("network_thesis", {})["stats"] = [
        {"label": "evidence tier", "value": "country_supported"},
        {"label": "economics status", "value": "model_cascaded_maghreb_plus_caribbean_batch1"},
    ]
    caribbean.setdefault("network_thesis", {})["stats"] = [
        {"label": "evidence tier", "value": "atlas_geometry_supported_partner_generic"},
        {"label": "economics status", "value": "batch1_cascaded_after_country_ref_promotion"},
    ]

    save_json(PARTNERS / "yassir.json", yassir)
    save_json(PARTNERS / "caribbean-mobility.json", caribbean)

    print("→ finance cascade")
    run_finance_cascade("yassir", stats)
    run_finance_cascade("caribbean-mobility", stats)

    print("→ sync data-clean")
    sync_data_clean(["yassir", "caribbean-mobility"])

    print("→ validate proposals")
    subprocess.run([sys.executable, str(ROOT / "scripts/validate_partner_proposals.py")], check=True, cwd=str(ROOT))

    report_path = HANDOFF / "PR65-GROK-EXECUTION-REPORT-2026-06-21.md"
    report_path.write_text(
        f"""# PR #65 Grok Execution Report — 2026-06-21

- Lane: `grok/execute_pr65_yassir_caribbean`
- Partners: yassir, caribbean-mobility

## Summary

| Gate | Count |
|------|------:|
| Country refs promoted | {len(stats['country_ref_promoted'])} |
| Yassir corridors sealed | {stats['yassir_corridors_sealed']} |
| Yassir corridors held | {stats['yassir_corridors_held']} |
| Algeria corridors added | {stats['algeria_corridors_added']} |
| Algeria display routes | {stats['algeria_display_routes']} |
| Caribbean corridors sealed | {stats['caribbean_corridors_sealed']} |
| Caribbean corridors held | {stats['caribbean_corridors_held']} |
| Yassir cards sealed | {stats['yassir_cards_sealed']} |
| Caribbean cards sealed | {stats['caribbean_cards_sealed']} |
| Finance cascaded | {', '.join(stats['finance_cascaded'])} |

## Country references promoted

{chr(10).join('- ' + c for c in stats['country_ref_promoted'])}

## Artifacts

- `handoff/partner-map-model/algeria-yassir-mint-report.json`
- `partner-pitch/partners/yassir.json`
- `partner-pitch/partners/caribbean-mobility.json`
- `data-clean/partners/yassir.json`
- `data-clean/partners/caribbean-mobility.json`
- `finance/recal/agg-yassir.json`, `finance/recal/agg-caribbean-mobility.json`
- `finance/growth-yassir.json`, `finance/growth-caribbean-mobility.json`
"""
    )
    save_json(HANDOFF / "pr65-grok-execution-stats.json", stats)
    print(json.dumps(stats, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())