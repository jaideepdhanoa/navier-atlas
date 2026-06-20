#!/usr/bin/env python3
"""
Patch finance/model/corridors.json with India (Rapido/Ola) and UAE (Noon) markets
from sealed PR #58 spines + partner route seals.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORRIDORS_PATH = ROOT / "finance" / "model" / "corridors.json"
INDIA_SPINE = ROOT / "handoff" / "partner-map-model" / "india-shared-corridor-spine.json"
NOON_MANIFEST = ROOT / "handoff" / "partner-map-model" / "noon-grok-ci-seal-render-qa-2026-06-20.json"
ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"
COUNTRY_REF = ROOT / "finance" / "model" / "country-reference.json"

PIONEER_MAX_NM = 70.0

MARKET_ANCHORS = {
    "mumbai": {
        "label": "India — Mumbai harbour & Konkan",
        "fare_usd": 5.5,
        "market_pax_yr": 120000,
        "archetype": "ridehail",
        "country": "India",
    },
    "goa": {
        "label": "India — Goa rivers & coast",
        "fare_usd": 8.0,
        "market_pax_yr": 180000,
        "archetype": "ridehail",
        "country": "India",
    },
    "kerala": {
        "label": "India — Kochi & Kerala backwaters",
        "fare_usd": 3.5,
        "market_pax_yr": 350000,
        "archetype": "ridehail",
        "country": "India",
    },
    "andaman": {
        "label": "India — Andaman Islands",
        "fare_usd": 22.0,
        "market_pax_yr": 160000,
        "archetype": "tourism",
        "country": "India",
    },
}

NOON_ANCHOR = {
    "fare_usd": 48.0,
    "market_pax_yr": 420000,
    "archetype": "super_app",
    "country": "United Arab Emirates",
}


def load_routes_index() -> dict[str, dict]:
    routes = json.loads(ROUTES_PATH.read_text())
    feats = routes["features"] if isinstance(routes, dict) and "features" in routes else routes
    return {f["properties"]["id"]: f["properties"] for f in feats if f.get("properties", {}).get("id")}


def l3_block(*, fare: float, pax: int, archetype: str, source: str) -> dict:
    return {
        "comparable_fare_usd_pax": fare,
        "corridor_annual_oneway_pax": pax,
        "_fare_record": {
            "value": fare,
            "unit": "USD/pax/one-way",
            "source_tier": "T3",
            "confidence": "med-low",
            "source": source,
            "method": "PR #58 India/Noon corridor market anchor split across sealed geometry rows",
        },
        "_demand_record": {
            "value": pax,
            "unit": "pax/yr one-way (addressable)",
            "source_tier": "T3",
            "confidence": "med-low",
            "basis": "addressable",
            "source": source,
            "method": "Market-level anchor from INDIA-ECONOMICS-SIDECAR-V0 / UAE Careem ladder; split evenly across sealed corridors in market.",
        },
        "demand_confidence": "med-low",
    }


def build_india_markets(spine: dict, partner: str) -> dict[str, dict]:
    by_market: dict[str, list] = {k: [] for k in MARKET_ANCHORS}
    for c in spine.get("corridors", []):
        mk = c.get("market_key")
        if mk not in by_market:
            continue
        if c.get("current_geometry_status") != "geometry_present":
            continue
        rid = c.get("corridor_id")
        if not rid:
            continue
        by_market[mk].append(c)

    out: dict[str, dict] = {}
    for mk, corridors in by_market.items():
        if not corridors:
            continue
        anchor = MARKET_ANCHORS[mk]
        pax_each = max(5000, int(anchor["market_pax_yr"] / len(corridors)))
        rows = []
        for c in sorted(corridors, key=lambda x: x.get("corridor_id", "")):
            nm = float(c.get("route_nm") or 0)
            rows.append({
                "route_id": c["corridor_id"],
                "from": c.get("from_label") or c.get("from", ""),
                "to": c.get("to_label") or c.get("to", ""),
                "distance_nm": nm,
                "vessel": "Pioneer II" if nm <= PIONEER_MAX_NM else "Quanta-LR",
                "archetype": anchor["archetype"],
                "from_node_id": c.get("from_city_id"),
                "to_node_id": c.get("to_city_id"),
                "country": anchor["country"],
                "pool_basis": "addressable",
                "_pr58_sealed": True,
                "L3_locals": l3_block(
                    fare=anchor["fare_usd"],
                    pax=pax_each,
                    archetype=anchor["archetype"],
                    source=f"handoff/INDIA-ECONOMICS-SIDECAR-V0-2026-06-20.json ({mk})",
                ),
            })
        market_id = f"india-{mk}-{partner}"
        out[market_id] = {
            "partner": partner,
            "region": "South Asia",
            "label": anchor["label"],
            "fleet_basis": "network_sum",
            "fleet_rounding": "ceil",
            "_market_note": f"PR #58 sealed India spine — {partner} mobility platform; geometry from india-shared-corridor-spine.json",
            "corridors": rows,
        }
    return out


def build_noon_market(manifest: dict, by_id: dict[str, dict]) -> dict[str, dict]:
    rows = []
    seen: set[str] = set()
    for fr in manifest.get("featured_routes_requiring_seal", []):
        rid = fr.get("source_corridor_id") or fr.get("route_id")
        if not rid or rid in seen:
            continue
        if rid not in by_id:
            continue
        seen.add(rid)
        p = by_id[rid]
        nm = float(p.get("distance_nm") or fr.get("distance_nm") or 0)
        rows.append({
            "route_id": rid,
            "from": p.get("from_label") or fr.get("from_label", ""),
            "to": p.get("to_label") or fr.get("to_label", ""),
            "distance_nm": nm,
            "vessel": "Pioneer II" if nm <= PIONEER_MAX_NM else "Quanta-LR",
            "archetype": NOON_ANCHOR["archetype"],
            "from_node_id": p.get("from_city_id") or fr.get("from_node_id"),
            "to_node_id": p.get("to_city_id") or fr.get("to_node_id"),
            "country": NOON_ANCHOR["country"],
            "pool_basis": "addressable",
            "_pr58_sealed": True,
            "L3_locals": l3_block(
                fare=NOON_ANCHOR["fare_usd"],
                pax=max(5000, int(NOON_ANCHOR["market_pax_yr"] / 12)),
                archetype=NOON_ANCHOR["archetype"],
                source="uae-careem demand ladder + PR #58 Noon route seal (Careem-style super_app)",
            ),
        })
    return {
        "uae-noon": {
            "partner": "noon",
            "region": "MENA",
            "label": "UAE — Noon commerce & mobility",
            "fleet_basis": "network_sum",
            "fleet_rounding": "ceil",
            "_market_note": "PR #58 Noon UAE active scope — 12 sealed routes; Careem-style super_app archetype",
            "corridors": rows,
        }
    }


def ensure_india_country_ref() -> None:
    cref = json.loads(COUNTRY_REF.read_text())
    countries = cref.setdefault("countries", {})
    if "India" in countries:
        return
    countries["India"] = {
        "captain_usd_yr": {
            "value": 18000,
            "source_tier": "T4",
            "confidence": "med-low",
            "source": "Modeled India marine crew — between Indonesia $12k and Thailand $24k; PR #58 corridor pass",
        },
        "energy_usd_kwh": {
            "value": 0.1,
            "source_tier": "T3",
            "confidence": "med-low",
            "source": "India commercial tariff blended ~₹8-10/kWh",
        },
        "grid_co2_kg_kwh": {
            "value": 0.68,
            "source_tier": "T3",
            "confidence": "med-low",
            "source": "Coal-heavy India grid ~0.65-0.72",
        },
        "marina_overhead_usd_yr": {
            "value": 12000,
            "source_tier": "T5",
            "confidence": "low",
            "source": "Modeled jetty/ferry-terminal overhead India coastal",
        },
        "cost_index": {"value": 0.55, "confidence": "med-low"},
    }
    COUNTRY_REF.write_text(json.dumps(cref, indent=1, ensure_ascii=False) + "\n")
    print(f"wrote India → {COUNTRY_REF}")


def main() -> int:
    spine = json.loads(INDIA_SPINE.read_text())
    manifest = json.loads(NOON_MANIFEST.read_text())
    by_id = load_routes_index()
    corr = json.loads(CORRIDORS_PATH.read_text())

    ensure_india_country_ref()

    new_markets: dict[str, dict] = {}
    new_markets.update(build_india_markets(spine, "rapido"))
    new_markets.update(build_india_markets(spine, "ola"))
    new_markets.update(build_noon_market(manifest, by_id))

    for mid, block in new_markets.items():
        corr["markets"][mid] = block
        print(f"  {mid}: {len(block['corridors'])} corridors (partner={block['partner']})")

    meta = corr.setdefault("_meta", {})
    meta["pr58_india_noon_markets_added"] = {
        "at": "2026-06-20",
        "markets": sorted(new_markets.keys()),
        "corridor_count": sum(len(m["corridors"]) for m in new_markets.values()),
    }
    CORRIDORS_PATH.write_text(json.dumps(corr, indent=1, ensure_ascii=False) + "\n")
    print(f"patched {CORRIDORS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())