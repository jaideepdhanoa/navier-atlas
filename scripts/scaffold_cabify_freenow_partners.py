#!/usr/bin/env python3
"""Scaffold cabify + freenow partner JSONs and apply 80-20 inheritance binds."""
from __future__ import annotations

import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "handoff" / "partner-map-model" / "partner-coverage-80-20-inheritance-review-2026-06-20.json"
PARTNERS = ROOT / "data-clean" / "partners"
PITCH = ROOT / "partner-pitch" / "partners"

WHY_NOW = (
    "Foiling lifts the hull clear of the water: faster, dramatically more efficient per passenger-mile, "
    "smooth and near-silent, hybrid-capable with no charging-infrastructure dependency, and autonomy-ready. "
    "A ~100-vessel network is already ramping in the Maldives (WSJ/Bloomberg, 2026), and coastal regulators "
    "are mandating clean harbour craft. The category gets claimed cluster-by-cluster."
)

WHY_NAVIER = {
    "step_change": (
        "Hydrofoiling lifts the hull clear of the water — roughly 10× more efficient than a conventional hull, "
        "faster, smoother, and quiet — with a software-defined fleet that keeps improving over time."
    ),
    "no_new_infrastructure": (
        "Navier uses the oceans and berths that already exist. Pioneer II needs only a berth pedestal; "
        "Quanta-LR hybrid needs no charging infrastructure."
    ),
    "the_moment": (
        "Coastal ride demand is dense, ferry corridors are slow and weather-exposed, and the water surface "
        "is still unowned by any mobility platform."
    ),
}


def load_rows(partner_id: str) -> list[dict]:
    review = json.loads(REVIEW.read_text())
    return [r for r in review["candidate_inherited_binds"] if r["partner_id"] == partner_id]


def market_from_country(country: str, cities: list[dict], partner_display: str) -> dict:
    slug = country.lower().replace(" ", "-")
    city_ids = [c["registry_city_id"] for c in cities]
    labels = [c["display"] for c in cities]
    top_city = city_ids[0]
    return {
        "id": slug,
        "slug": slug,
        "label": f"{country} coastal",
        "region": cities[0].get("country") or country,
        "anchor_cities": city_ids[:3],
        "summary": (
            f"Coastal and island water corridors across {country} — "
            f"{', '.join(labels[:3])}{'…' if len(labels) > 3 else ''} — "
            "where ride demand already meets ferry pain and resort flows."
        ),
        "hero": {
            "title": f"{partner_display} × Navier — {country} on the water",
            "subtitle": f"{country} coastal corridors, foiling and in-app.",
            "what_we_do_together": (
                f"We layer a foiling water tier onto the densest coastal corridors in {country} — "
                "booked in-app, premium-priced, on existing registry geometry."
            ),
        },
        "use_cases": ["island-hopping", "resort transfer", "coastal commute"],
        "phases": [
            {
                "n": 1,
                "label": f"Phase 1 — {labels[0]} beachhead",
                "boats": 6,
                "cities": [top_city],
                "route_scope": "intra",
                "featured_routes": [{"label": f"{labels[0]} coastal mesh", "route_id": None, "_link_kind": "text"}],
                "timeline": "2026 H2",
                "rationale": f"Start on the highest-geometry coastal cluster in {country}.",
                "use_cases": ["island-hopping", "resort transfer"],
            }
        ],
    }


def build_cabify(rows: list[dict]) -> dict:
    by_country: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_country[r["country"]].append(r)

    spain = by_country["Spain"]
    colombia = by_country.get("Colombia", [])
    phase1 = [r["registry_city_id"] for r in spain if r["registry_city_id"] == "ibiza-spain"] or [
        spain[0]["registry_city_id"]
    ]
    phase2 = [r["registry_city_id"] for r in spain if r["registry_city_id"] != phase1[0]]
    phase3 = [r["registry_city_id"] for r in colombia]

    markets = [market_from_country("Spain", spain, "Cabify")]
    if colombia:
        markets.append(market_from_country("Colombia", colombia, "Cabify"))

    return {
        "partner_id": "cabify",
        "display": "Cabify",
        "archetype": "ridehail",
        "category": "ridehail",
        "region": "Europe + LatAm",
        "layout": "hub",
        "partner_context": {
            "their_ambition": (
                "You are Spain and Latin America's premium ride-hail platform — present in six countries "
                "and 40+ cities, with a business and consumer mobility stack built for regulated, urban markets."
            ),
            "their_pressure": (
                "Land ride-hail is contested in every core city. Your next differentiated growth surface is "
                "coastal resort corridors and island hops where ferries are slow, seasonal, and cash-heavy."
            ),
            "where_navier_fits": (
                "Navier adds the water-mobility tier Cabify does not have: a software-defined foiling fleet "
                "booked in-app across Spain's Balearics and Colombia's Caribbean coast."
            ),
        },
        "hero": {
            "title": "Cabify × Navier — Spain and LatAm's premium ride-hail, on the water",
            "subtitle": "Balearic island hops and Caribbean resort corridors — the surface no ride-hail platform owns yet.",
            "what_we_do_together": (
                "We launch a Cabify-branded foiling water tier across Spain's coastal islands and Colombia's "
                "Cartagena archipelago — booked in-app, premium-priced, on registry geometry that already exists."
            ),
        },
        "why_now": WHY_NOW,
        "why_navier_now": {
            **WHY_NAVIER,
            "wow_corridors": [
                "Ibiza ↔ Formentera",
                "Palma ↔ Dragonera",
                "Cartagena ↔ Rosario Islands",
            ],
        },
        "multimodal_fit": (
            "Cabify already owns the first/last mile by car. A foiling pier becomes the water node: "
            "Cabify to the marina, a silent foil across the strait or bay, Cabify on arrival — one booking flow."
        ),
        "differentiation": {
            "why_navier": (
                "Software-defined foiling fleet, Maldives-scale proof, and zero new infrastructure — "
                "a premium tier Cabify can own before global platforms move on island leisure."
            )
        },
        "network_thesis": {
            "headline": "The water layer of Spain and LatAm's premium ride-hail network.",
            "body": (
                "Cabify operates across Spain and Latin America with dense coastal and island demand. "
                "Each market below is a real, ready water network on existing Atlas geometry — "
                "island hops, resort runs, and ferry-corridor alternatives inside the app riders already use."
            ),
            "stats": [
                {"label": "Inherited cities", "value": str(len(rows))},
                {"label": "Anchor regions", "value": "Spain · Colombia"},
                {"label": "Platforms", "value": "Pioneer II + Quanta-LR"},
            ],
            "how_to_read": "Each card is a coastal market with registry geometry. Start in the Balearics or Cartagena.",
            "coverage_note": (
                "Cabify is present across Spain and six Latin American countries; these five inherited "
                "registry cities are the first exact-bound coastal footprint from the 80-20 inheritance pass."
            ),
        },
        "phases": [
            {
                "n": 1,
                "label": "Phase 1 — Ibiza beachhead",
                "boats": 6,
                "cities": phase1,
                "route_scope": "intra",
                "featured_routes": [{"label": "Ibiza ↔ Formentera", "route_id": None, "_link_kind": "text"}],
                "timeline": "2026 H2",
                "rationale": "Start on Spain's highest-velocity island leisure corridor with marquee economics-ready geometry.",
                "use_cases": ["island-hopping", "nightlife coast"],
            },
            {
                "n": 2,
                "label": "Phase 2 — Balearics mesh",
                "boats": 24,
                "cities": phase2,
                "route_scope": "regional",
                "featured_routes": [{"label": "Palma ↔ Menorca", "route_id": None, "_link_kind": "text"}],
                "timeline": "2027",
                "rationale": "Expand across Mallorca, Menorca, and Costa Brava resort coasts.",
                "use_cases": ["resort transfer", "coastal commute"],
            },
            {
                "n": 3,
                "label": "Phase 3 — Colombia Caribbean",
                "boats": 12,
                "cities": phase3 or ["cartagena-colombia"],
                "route_scope": "intra",
                "featured_routes": [{"label": "Cartagena ↔ Rosario Islands", "route_id": None, "_link_kind": "text"}],
                "timeline": "2027 H2",
                "rationale": "Carry the water tier to Cabify's LatAm resort coast.",
                "use_cases": ["reef run", "resort transfer"],
            },
        ],
        "markets": markets,
        "network_footprint": [],
        "_footprint_model": {
            "contract": "PARTNER-MAP-MODEL-SPEC.md",
            "source_of_truth": "finance/model/corridors.json",
            "binding": "network_footprint[].registry_key references shared registry market; inherits on registry growth",
            "roster_status": "80-20 inheritance scaffold — footprint populated by apply_partner_8020_inheritance_bindings.py",
        },
    }


def build_freenow(rows: list[dict]) -> dict:
    by_country: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_country[r["country"]].append(r)

    greece = by_country["Greece"]
    italy = by_country["Italy"]
    france = by_country["France"]
    spain = by_country["Spain"]
    uk = by_country.get("United Kingdom", [])
    ireland = by_country.get("Ireland", [])

    def top_ids(bucket: list[dict], n: int = 3) -> list[str]:
        ranked = sorted(bucket, key=lambda x: -(x.get("route_count_active") or 0))
        return [r["registry_city_id"] for r in ranked[:n]]

    markets = []
    for country, bucket in sorted(by_country.items()):
        if bucket:
            markets.append(market_from_country(country, bucket, "FREENOW"))

    return {
        "partner_id": "freenow",
        "display": "FREENOW",
        "archetype": "ridehail",
        "category": "ridehail",
        "region": "Europe",
        "layout": "hub",
        "partner_context": {
            "their_ambition": (
                "You are Europe's leading taxi and mobility platform — 180+ cities across nine countries — "
                "now part of Lyft's European expansion while retaining a distinct multi-country taxi network."
            ),
            "their_pressure": (
                "European urban taxi demand is mature; growth needs premium tiers and multimodal surfaces "
                "that bypass road congestion — especially on coasts, islands, and harbour cities."
            ),
            "where_navier_fits": (
                "Navier is the foiling water supply layer for FREENOW's coastal and island corridors: "
                "Greece, Italy, France, Spain, the UK and Ireland — booked in-app on existing registry geometry."
            ),
        },
        "hero": {
            "title": "FREENOW × Navier — Europe's taxi platform, on the water",
            "subtitle": "Mediterranean islands, Riviera coasts, and Thames harbour runs — the surface no taxi app owns yet.",
            "what_we_do_together": (
                "We add a foiling water tier across FREENOW's densest European coastal corridors — "
                "Greek islands, Italian archipelagos, the Côte d'Azur, Balearics, and the Thames — "
                "on registry geometry that is already display-ready."
            ),
        },
        "why_now": WHY_NOW,
        "why_navier_now": {
            **WHY_NAVIER,
            "wow_corridors": [
                "Mykonos ↔ Delos",
                "Amalfi ↔ Capri",
                "Nice ↔ Monaco",
                "London Thames ↔ Greenwich",
            ],
        },
        "multimodal_fit": (
            "FREENOW already dispatches taxis and multimodal trips across Europe. A foiling pier is the "
            "water leg in the same trip graph — taxi to the marina, foil across the bay, taxi on arrival."
        ),
        "differentiation": {
            "why_navier": (
                "A uniform software-defined foiling fleet across nine countries — the premium water tier "
                "Lyft's European platform can light up market by market without new infrastructure."
            )
        },
        "network_thesis": {
            "headline": "The water layer of Europe's leading taxi platform.",
            "body": (
                "FREENOW operates in 180+ European cities; thirty inherited registry cities already have "
                "Atlas coastal geometry. Each is a ready foiling corridor — island hops, Riviera runs, "
                "and harbour commutes inside the app riders already use."
            ),
            "stats": [
                {"label": "Inherited cities", "value": str(len(rows))},
                {"label": "Countries", "value": str(len(by_country))},
                {"label": "Platforms", "value": "Pioneer II + Quanta-LR"},
            ],
            "how_to_read": "Each card is a country coastal cluster. Start in Greece or the Côte d'Azur.",
            "coverage_note": (
                "FREENOW spans nine European countries; these thirty inherited registry cities are the "
                "first exact-bound coastal footprint from the 80-20 inheritance pass."
            ),
        },
        "phases": [
            {
                "n": 1,
                "label": "Phase 1 — Greece Cyclades flagship",
                "boats": 12,
                "cities": top_ids(greece, 4),
                "route_scope": "regional",
                "featured_routes": [{"label": "Mykonos ↔ Paros", "route_id": None, "_link_kind": "text"}],
                "timeline": "2026 H2",
                "rationale": "Lead with Greece's densest island geometry and marquee resort flows.",
                "use_cases": ["island-hopping", "resort transfer"],
            },
            {
                "n": 2,
                "label": "Phase 2 — Italy + France Riviera",
                "boats": 36,
                "cities": top_ids(italy, 3) + top_ids(france, 2),
                "route_scope": "regional",
                "featured_routes": [{"label": "Amalfi ↔ Capri", "route_id": None, "_link_kind": "text"}],
                "timeline": "2027",
                "rationale": "Expand across Amalfi, Naples islands, and the Côte d'Azur.",
                "use_cases": ["Riviera commute", "island leisure"],
            },
            {
                "n": 3,
                "label": "Phase 3 — UK, Ireland, Spain + full mesh",
                "boats": 48,
                "cities": top_ids(uk, 1) + top_ids(ireland, 1) + top_ids(spain, 2),
                "route_scope": "network",
                "featured_routes": [{"label": "Thames ↔ Greenwich", "route_id": None, "_link_kind": "text"}],
                "timeline": "2027 H2",
                "rationale": "Complete the nine-country coastal mesh.",
                "use_cases": ["harbour commute", "island-hopping"],
            },
        ],
        "markets": markets,
        "network_footprint": [],
        "_footprint_model": {
            "contract": "PARTNER-MAP-MODEL-SPEC.md",
            "source_of_truth": "finance/model/corridors.json",
            "binding": "network_footprint[].registry_key references shared registry market; inherits on registry growth",
            "roster_status": "80-20 inheritance scaffold — footprint populated by apply_partner_8020_inheritance_bindings.py",
        },
    }


def main() -> int:
    cabify_rows = load_rows("cabify")
    freenow_rows = load_rows("freenow")
    if not cabify_rows or not freenow_rows:
        print("✗ missing cabify/freenow rows in 80-20 review artifact", file=sys.stderr)
        return 1

    cabify = build_cabify(cabify_rows)
    freenow = build_freenow(freenow_rows)

    for doc in (cabify, freenow):
        for phase in doc.get("phases") or []:
            for fr in phase.get("featured_routes") or []:
                if "route_id" not in fr:
                    fr["route_id"] = None

    for pid, doc in (("cabify", cabify), ("freenow", freenow)):
        path = PARTNERS / f"{pid}.json"
        path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        if PITCH.parent.exists():
            (PITCH / f"{pid}.json").write_text(path.read_text())
        print(f"  ✓ scaffolded {path}")

    print("→ applying 80-20 inheritance binds")
    rc = subprocess.call([sys.executable, str(ROOT / "scripts" / "apply_partner_8020_inheritance_bindings.py")])
    return rc


if __name__ == "__main__":
    raise SystemExit(main())