#!/usr/bin/env python3
"""Build deterministic source packages for country mobility review decks.

The builder preserves the approved Grab mobility lineage and emits the locked
country-review spine:

    cover
    why this partner
    country market overview (one slide)
    one slide per canonical city in the country cluster
    one unit-economics slide (one representative exact-bound route)
    country TAM / path-to-scale ladder
    partner integration model
    phased rollout
    decision and ask
    close

City count follows the canonical CLUSTERS.json membership for the country, never
a route list. Each city gets its own slide with an Atlas route screenshot slot
reserved for direct human insertion. The builder does not edit Google Slides.
"""
from __future__ import annotations

import argparse
import json
from copy import deepcopy
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DECKS = ROOT / "deck-studio" / "decks"
GRAB_DECK_ID = "11WCun1Xk1flPmqvvtYrYZXsL5yRb5KQoe0xvTQSppKo"

COMMON_RULES = [
    "Slides API only for live edits; do not create or round-trip a PPTX.",
    "Duplicate or bind the approved Grab mobility reference before applying source-backed substitutions.",
    "Spine is locked: cover, why-partner, one country market overview, one slide per canonical city, one unit-economics slide, one country TAM ladder, integration, rollout, ask, close.",
    "City slides follow canonical CLUSTERS.json membership for the country, never a route list.",
    "The unit-economics slide uses one representative exact-bound route; route IDs match canonical ROUTES.json exactly; unsupported values remain null.",
    "The TAM ladder uses grounded aggregate figures (supported route revenue floor, addressable water-crossing spend); never mixed-unit bars or internal metrics.",
    "Atlas route screenshot slots are reserved for Jaideep or another human and remain unpopulated by automation.",
    "N30 composites use source-approved market imagery, stable linked URLs, documented provenance, and minimal gold.",
    "Live deck IDs and slide manifests must be read back and synchronized after apply.",
]

# ---------------------------------------------------------------------------
# Deck definitions. City rosters follow canonical CLUSTERS.json membership.
#   cities[]        : one slide per canonical city (supported / held).
#   economics_route : single representative exact-bound route for the one
#                     unit-economics slide (values bound from the aggregate).
#   tam             : path-to-scale ladder rungs bound to aggregate fields.
# ---------------------------------------------------------------------------
DEFINITIONS: dict[str, dict[str, Any]] = {
    "didi-brazil": {
        "partner_id": "didi",
        "partner_label": "DiDi",
        "country": "Brazil",
        "deck_id": "1OixKrHjQbWu0Plkvj-57SQyTFxPL5Ii8l3K6Q9umJOk",
        "logo": "deck-studio/assets/logos/partners/didi/didi-logo-official.png",
        "aggregate": "finance/recal/agg-didi.json",
        "aggregate_market_key": "brazil",
        "scope_market_keys": ["brazil"],
        "country_total": {
            "expected_annual_revenue_usd": 23404822.0,
            "expected_vessels_supported": 113,
            "supported_route_ids": ["rn-1886629dbf0c", "rn-80f0d0ebe0bd", "rn-369ef0eb69d9", "rn-00bb6ded4be5"],
        },
        "market_overview": {
            "thesis": (
                "Brazil's coastal cities move enormous numbers of people across water every day, "
                "but on slow, aging diesel ferries. Rio de Janeiro alone runs one of the world's "
                "busiest urban ferry networks across Guanabara Bay, while Angra dos Reis and "
                "Florianópolis add dense island and strait crossings driven by both daily commuting "
                "and heavy tourism. Navier's electric hydrofoils cut these crossings to a fraction of "
                "the time with zero local emissions, and a ride-hail partner brings the demand, "
                "booking, and payment layer that turns scattered ferry trips into an on-demand water network."
            ),
            "kpis": [
                {"label": "Coastal cities in scope", "value": "3"},
                {"label": "Supported cross-bay routes", "value": "4"},
                {"label": "Supported annual route revenue", "value": "$23.4M"},
                {"label": "Vessels supported at scale", "value": "113"},
            ],
        },
        "cities": [
            {
                "key": "rio", "label": "Rio de Janeiro", "supported": True, "hold_reason": None,
                "thesis": (
                    "Guanabara Bay is the heart of the opportunity. From the Praça XV terminal in central "
                    "Rio, daily commuters cross to Niterói (Arariboia and the fast Charitas catamaran), to "
                    "Ilha do Governador (Cocotá), and out to Paquetá island. These are established, "
                    "high-frequency commuter flows — exactly where an electric hydrofoil beats road "
                    "congestion and slow diesel ferries. All four of the deck's supported routes sit here."
                ),
            },
            {
                "key": "angra", "label": "Angra dos Reis and Ilha Grande", "supported": False,
                "hold_reason": "Route-level passenger demand and fares are under local review; economics remain blank until confirmed.",
                "thesis": (
                    "Angra dos Reis is the gateway to Ilha Grande and the Green Coast's hundreds of islands, "
                    "with a mix of year-round island residents and heavy seasonal tourism moving by boat. The "
                    "water crossings are mapped, but route-level passenger counts and fares are still being "
                    "confirmed with local operators, so this city's economics are shown as under review rather "
                    "than estimated."
                ),
            },
            {
                "key": "floripa", "label": "Florianópolis", "supported": False,
                "hold_reason": "Route-level passenger demand and fares are under local review; economics remain blank until confirmed.",
                "thesis": (
                    "Florianópolis sits on an island linked to the mainland across a narrow strait, combining "
                    "daily island commuting with strong tourism. Marina and mainland crossings map naturally to "
                    "short hydrofoil hops. As with Angra dos Reis, the water crossings are mapped but passenger "
                    "demand and fares are still under review, so economics are held rather than estimated."
                ),
            },
        ],
        "economics_route": {
            "label": "Praça XV → Arariboia",
            "route_id": "rn-1886629dbf0c",
            "desc": "Rio's flagship cross-bay commuter connection between central Rio and Niterói.",
        },
        "tam": {
            "headline": "The supported routes are a floor, not a ceiling",
            "rungs": [
                {"label": "Supported annual route revenue today", "aggregate_field": "rollup.grounded_floor_by_market.brazil.market_rev_yr",
                 "value_usd": 23404822.0, "note": "Four sourced Rio cross-bay routes, 113 vessels at scale."},
                {"label": "Addressable Brazil water-crossing spend", "aggregate_field": "rollup.grounded_floor_by_market.brazil.transport_spend_pool_yr",
                 "value_usd": 236225070.0, "note": "Annual passenger spend across the bay and coastal crossings the network can compete for."},
            ],
        },
    },
    "indrive-brazil": {
        "partner_id": "indrive",
        "partner_label": "inDrive",
        "country": "Brazil",
        "deck_id": "1QImIe6KAee0Eajsokgh9NmH0I29lir4l2LV63e-9OxE",
        "logo": "deck-studio/assets/logos/partners/indrive/indrive-logo-white-cover.png",
        "aggregate": "finance/recal/agg-indrive.json",
        "aggregate_market_key": "indrive-brazil",
        "scope_market_keys": ["indrive-brazil"],
        "shared_basis_with": "didi-brazil",
        "country_total": {
            "expected_annual_revenue_usd": 23404822.0,
            "expected_vessels_supported": 113,
            "supported_route_ids": ["rn-1886629dbf0c", "rn-80f0d0ebe0bd", "rn-369ef0eb69d9", "rn-00bb6ded4be5"],
        },
        "market_overview": {
            "thesis": (
                "Brazil's coastal cities move enormous numbers of people across water every day, "
                "but on slow, aging diesel ferries. Rio de Janeiro alone runs one of the world's "
                "busiest urban ferry networks across Guanabara Bay, while Angra dos Reis and "
                "Florianópolis add dense island and strait crossings driven by both daily commuting "
                "and heavy tourism. Navier's electric hydrofoils cut these crossings to a fraction of "
                "the time with zero local emissions, and a ride-hail partner brings the demand, "
                "booking, and payment layer that turns scattered ferry trips into an on-demand water network."
            ),
            "kpis": [
                {"label": "Coastal cities in scope", "value": "3"},
                {"label": "Supported cross-bay routes", "value": "4"},
                {"label": "Supported annual route revenue", "value": "$23.4M"},
                {"label": "Vessels supported at scale", "value": "113"},
            ],
        },
        "cities": [
            {
                "key": "rio", "label": "Rio de Janeiro", "supported": True, "hold_reason": None,
                "thesis": (
                    "Guanabara Bay is the heart of the opportunity. From the Praça XV terminal in central "
                    "Rio, daily commuters cross to Niterói (Arariboia and the fast Charitas catamaran), to "
                    "Ilha do Governador (Cocotá), and out to Paquetá island. These are established, "
                    "high-frequency commuter flows — exactly where an electric hydrofoil beats road "
                    "congestion and slow diesel ferries. All four of the deck's supported routes sit here."
                ),
            },
            {
                "key": "angra", "label": "Angra dos Reis and Ilha Grande", "supported": False,
                "hold_reason": "Route-level passenger demand and fares are under local review; economics remain blank until confirmed.",
                "thesis": (
                    "Angra dos Reis is the gateway to Ilha Grande and the Green Coast's hundreds of islands, "
                    "with a mix of year-round island residents and heavy seasonal tourism moving by boat. The "
                    "water crossings are mapped, but route-level passenger counts and fares are still being "
                    "confirmed with local operators, so this city's economics are shown as under review rather "
                    "than estimated."
                ),
            },
            {
                "key": "floripa", "label": "Florianópolis", "supported": False,
                "hold_reason": "Route-level passenger demand and fares are under local review; economics remain blank until confirmed.",
                "thesis": (
                    "Florianópolis sits on an island linked to the mainland across a narrow strait, combining "
                    "daily island commuting with strong tourism. Marina and mainland crossings map naturally to "
                    "short hydrofoil hops. As with Angra dos Reis, the water crossings are mapped but passenger "
                    "demand and fares are still under review, so economics are held rather than estimated."
                ),
            },
        ],
        "economics_route": {
            "label": "Praça XV → Arariboia",
            "route_id": "rn-1886629dbf0c",
            "desc": "Rio's flagship cross-bay commuter connection between central Rio and Niterói.",
        },
        "tam": {
            "headline": "The supported routes are a floor, not a ceiling",
            "rungs": [
                {"label": "Supported annual route revenue today", "aggregate_field": "rollup.grounded_floor_by_market.indrive-brazil.market_rev_yr",
                 "value_usd": 23404822.0, "note": "Four sourced Rio cross-bay routes, 113 vessels at scale."},
                {"label": "Addressable Brazil water-crossing spend", "aggregate_field": "rollup.grounded_floor_by_market.indrive-brazil.transport_spend_pool_yr",
                 "value_usd": 236225070.0, "note": "Annual passenger spend across the bay and coastal crossings the network can compete for."},
            ],
        },
    },
    "didi-mexico": {
        "partner_id": "didi",
        "partner_label": "DiDi",
        "country": "Mexico",
        "deck_id": "1XwKRuJtMrou8NtBdc1oY3LL2Dk83dCs9MCLvNKgwq0c",
        "logo": "deck-studio/assets/logos/partners/didi/didi-logo-official.png",
        "aggregate": "finance/recal/agg-didi.json",
        "aggregate_market_key": "mexico-caribbean",
        "scope_market_keys": ["mexico-caribbean", "mexico-pacific"],
        "country_total": {
            "expected_annual_revenue_usd": 14759160.0,
            "expected_vessels_supported": 88,
            "supported_route_ids": ["ics-413f51cd44", "ics-dd1d814699", "ics-aa6ff40d2d"],
        },
        "market_overview": {
            "thesis": (
                "Mexico's Caribbean and Pacific coasts run some of the highest-volume tourist and commuter "
                "ferry crossings in the Americas — Cancún to Isla Mujeres, Playa del Carmen to Cozumel, and "
                "the Pacific resort coast around Puerto Vallarta and Los Cabos. These are short, dense, "
                "high-frequency water crossings that suit electric hydrofoils, and a ride-hail partner supplies "
                "the on-demand booking and payment layer today's ferry operators lack."
            ),
            "kpis": [
                {"label": "Coastal cities in scope", "value": "4"},
                {"label": "Supported routes", "value": "3"},
                {"label": "Supported annual route revenue", "value": "$14.8M"},
                {"label": "Vessels supported at scale", "value": "88"},
            ],
        },
        "cities": [
            {
                "key": "cancun-isla", "label": "Cancún and Isla Mujeres", "supported": True, "hold_reason": None,
                "thesis": (
                    "The Puerto Juárez–Isla Mujeres crossing is one of Mexico's busiest island connections, "
                    "moving a constant flow of tourists and island workers off the Cancún waterfront. High "
                    "frequency and short distance make it a natural first electric route."
                ),
            },
            {
                "key": "playa-cozumel", "label": "Playa del Carmen and Cozumel", "supported": True, "hold_reason": None,
                "thesis": (
                    "The Playa del Carmen–Cozumel crossing is the main artery to Mexico's largest Caribbean "
                    "island, with heavy daily tourist and resident traffic. It carries supported economics in "
                    "the deck alongside the Cancún crossing."
                ),
            },
            {
                "key": "vallarta", "label": "Puerto Vallarta", "supported": False,
                "hold_reason": "Route-level fare and financial inputs are incomplete; economics remain blank until confirmed.",
                "thesis": (
                    "Puerto Vallarta anchors the Pacific resort coast, with coastal access south toward Yelapa "
                    "and the surrounding bays. The water crossings are mapped, but route-level fares and "
                    "financial inputs are still incomplete, so this city's economics are shown as under review."
                ),
            },
            {
                "key": "cabos", "label": "Los Cabos", "supported": False,
                "hold_reason": "Route-level fare and financial inputs are incomplete; economics remain blank until confirmed.",
                "thesis": (
                    "Los Cabos combines marina transfers with resort and excursion demand at the tip of Baja. "
                    "Local marina connections map to short hydrofoil hops, but route-level fares and financial "
                    "inputs are still incomplete, so economics are held rather than estimated."
                ),
            },
        ],
        "economics_route": {
            "label": "Puerto Juárez → Isla Mujeres",
            "route_id": "ics-413f51cd44",
            "desc": "Cancún's highest-frequency island crossing.",
        },
        "tam": {
            "headline": "The supported routes are a floor, not a ceiling",
            "rungs": [
                {"label": "Supported annual route revenue today", "aggregate_field": "rollup.grounded_floor_by_market.mexico-caribbean.market_rev_yr",
                 "value_usd": 14759160.0, "note": "Three sourced Caribbean crossings, 88 vessels at scale."},
                {"label": "Addressable Mexico water-crossing spend", "aggregate_field": "rollup.grounded_floor_by_market.mexico-caribbean.transport_spend_pool_yr",
                 "value_usd": 149933425.0, "note": "Annual passenger spend across the coastal crossings the network can compete for."},
            ],
        },
    },
    "indrive-egypt": {
        "partner_id": "indrive",
        "partner_label": "inDrive",
        "country": "Egypt",
        "deck_id": "1Nn3BRKUahikp87zC84JMdEVrcJYppm9ZXHgndAuzsEk",
        "logo": "deck-studio/assets/logos/partners/indrive/indrive-logo-white-cover.png",
        "aggregate": "finance/recal/agg-indrive.json",
        "aggregate_market_key": "indrive-egypt",
        "scope_market_keys": ["indrive-egypt"],
        "country_total": {
            "expected_annual_revenue_usd": 7420110.0,
            "expected_vessels_supported": 20,
            "supported_route_ids": [
                "rn-b06f6971ed47",
                "rn-c16a1627130f",
            ],
        },
        "market_overview": {
            "thesis": (
                "Egypt's Red Sea Riviera — Hurghada and Sharm El Sheikh — runs constant boat traffic to "
                "Giftun Island and Ras Mohammed. Two luxury-belt routes are grounded on labeled destination-pool "
                "demand and premium day-trip fares under captive capture; three further Red Sea routes stay held. "
                "Cairo is out of scope (Nile); Alexandria remains candidate/null until a scheduled network is proven."
            ),
            "kpis": [
                {"label": "Coastal cities in scope", "value": "2"},
                {"label": "Supported routes", "value": "2"},
                {"label": "Supported annual route revenue", "value": "$7.4M"},
                {"label": "Vessels supported", "value": "20"},
            ],
        },
        "cities": [
            {
                "key": "hurghada", "label": "Hurghada", "supported": True,
                "hold_reason": None,
                "thesis": (
                    "Giftun Island is Hurghada's flagship excursion — white-sand islands and the Orange Bay and "
                    "Mahmya reefs, reached by boat and drawing roughly 187,000 visitors a year."
                ),
            },
            {
                "key": "sharm", "label": "Sharm El Sheikh", "supported": True,
                "hold_reason": None,
                "thesis": (
                    "Ras Mohammed's reefs rank among the Red Sea's finest dive and snorkel sites, reached by boat "
                    "from Sharm and drawing about 50,000 visitors a year."
                ),
            },
        ],
        "economics_route": {
            "label": "Hurghada Marina → Giftun Island (Orange Bay / Mahmya)",
            "route_id": "rn-b06f6971ed47",
            "desc": "Flagship Red Sea luxury-belt excursion; provisional unit-economics anchor pending Jaideep's choice between Giftun and Ras Mohammed.",
        },
        "tam": {
            "headline": "Two promoted luxury-belt routes are a grounded floor, not a ceiling",
            "rungs": [
                {
                    "label": "Supported annual route revenue today",
                    "aggregate_field": "rollup.grounded_floor_by_market.indrive-egypt.market_rev_yr",
                    "value_usd": 7420110.0,
                    "note": "Giftun + Ras Mohammed only, mid-band grounded floor at ~90% captive capture. Three further Red Sea routes remain held.",
                },
                {
                    "label": "Addressable Egypt luxury-belt water-crossing spend",
                    "aggregate_field": "rollup.grounded_floor_by_market.indrive-egypt.transport_spend_pool_yr",
                    "value_usd": 8500384.0,
                    "note": "Labeled destination-pool × fare for the two promoted routes (not observed boardings). Captive floor is ~90% of this pool.",
                },
            ],
        },
    },
}


def dump(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def slide(slug: str, index: int, role: str, title: str) -> dict[str, Any]:
    return {
        "index": index,
        "slide_object_id": f"planned_{slug.replace('-', '_')}_{index:02d}",
        "layout_object_id": None,
        "title": title,
        "purpose": role,
        "allowed_edit_types": ["replace_text", "replace_linked_image"],
        "locked": False,
        "notes": "Planned source-package record. Replace with the live object ID after reference duplication/apply/readback.",
    }


def build(slug: str, definition: dict[str, Any]) -> None:
    out = DECKS / slug
    partner = definition["partner_id"]
    country = definition["country"]
    label = definition["partner_label"]

    cities = deepcopy(definition["cities"])
    econ_route = deepcopy(definition["economics_route"])
    tam = deepcopy(definition["tam"])
    market_overview = deepcopy(definition["market_overview"])

    scope = {
        "schema_version": "country-market-scope-v3",
        "deck_key": slug,
        "partner_id": partner,
        "country": country,
        "geography_rule": "global_canonical intersection partner clusters",
        "city_source": "data-clean/CLUSTERS.json canonical member cities for the country cluster",
        "source_paths": [
            f"partner-pitch/partners/{partner}.json",
            f"data-clean/partners/{partner}.json",
            "data-clean/CLUSTERS.json",
            "data-clean/ROUTES.json",
        ],
        "finance_market_keys": definition["scope_market_keys"],
        "cities": [{k: c[k] for k in ("key", "label", "supported", "hold_reason")} for c in cities],
        "economics_route": econ_route,
        "unsupported_values_policy": "null",
    }

    binding = {
        "schema_version": "country-economics-binding-v3",
        "deck_key": slug,
        "partner_id": partner,
        "country": country,
        "generator": "deck-studio/decks/gen_deck_economics.py",
        "aggregate_source": definition["aggregate"],
        "aggregate_market_key": definition.get("aggregate_market_key"),
        "canonical_routes_source": "data-clean/ROUTES.json",
        "economics_route": econ_route,
        "tam": tam,
        "country_total": deepcopy(definition["country_total"]),
        "rules": {
            "id_matching": "exact",
            "unsupported_values": "null",
            "country_substitution": "forbidden",
            "unit_economics_route": "single representative exact-bound route; all values bound from the aggregate, never hand-typed",
            "tam_source": "aggregate grounded_floor_by_market (supported revenue floor + addressable spend pool); no mixed-unit bars",
            "published_brazil_basis": "shared unchanged across DiDi Brazil and inDrive Brazil" if country == "Brazil" else None,
        },
    }

    # ---- locked spine ----
    slides: list[dict[str, Any]] = []
    rendered_text: dict[str, str] = {}
    idx = 1

    def add(role: str, title: str, body: str | None = None) -> dict[str, Any]:
        nonlocal idx
        s = slide(slug, idx, role, title)
        slides.append(s)
        rendered_text[f"slide_{idx:02d}_title"] = title
        if body is not None:
            rendered_text[f"slide_{idx:02d}_body"] = body
        idx += 1
        return s

    add("cover", f"{label} × Navier | {country}")
    add("partner_country_thesis", f"Why water mobility matters in {country}")

    mo_body = market_overview["thesis"] + "\n\n" + "  ·  ".join(
        f"{k['value']} {k['label'].lower()}" for k in market_overview["kpis"]
    )
    mo = add("market_overview", f"{country}: the water-mobility opportunity", mo_body)
    rendered_text["slide_%02d_kpis" % mo["index"]] = json.dumps(market_overview["kpis"], ensure_ascii=False)

    city_slides: list[dict[str, Any]] = []
    for c in cities:
        cs = add("city_review", c["label"], c["thesis"])
        if c.get("hold_reason"):
            rendered_text[f"slide_{cs['index']:02d}_hold"] = c["hold_reason"]
        city_slides.append(cs)

    econ_body = (
        f"Representative route: {econ_route['label']}. {econ_route['desc']} "
        "Annual passenger demand, one-way fare, annual revenue, fleet support, and payback are shown "
        "for this route from the sourced route model."
    ) if econ_route.get("route_id") else (
        f"Representative route: {econ_route['label']}. {econ_route['desc']} "
        "Route details and economics are left blank until local terminal, demand, and fare evidence is confirmed."
    )
    add("one_route_economics", f"Route economics: {econ_route['label']}", econ_body)

    tam_body = tam.get("headline", f"A focused path to scale in {country}")
    if tam.get("rungs"):
        tam_body += "\n\n" + "\n".join(f"{r['label']}: {r['note']}" for r in tam["rungs"])
    elif tam.get("hold_reason"):
        tam_body += "\n\n" + tam["hold_reason"]
    add("country_prize", tam.get("headline", f"A focused path to scale in {country}"), tam_body)

    add("integration_model", f"How {label} and Navier work together")
    add("phased_rollout", "Prove the route, then expand")
    add("decision_and_ask", "A joint route review is the next step")
    add("close", f"Build the complete journey in {country}")

    slide_manifest = {
        "deck_key": slug,
        "presentation_id": definition["deck_id"],
        "source": "deterministic country-review plan based on approved Grab mobility lineage",
        "spine": "cover, why-partner, market-overview, one slide per city, unit-economics, TAM, integration, rollout, ask, close",
        "slide_count": len(slides),
        "city_count": len(city_slides),
        "object_inventory_status": "stale_requires_pull",
        "slides": slides,
        "pull_command": f"Google Slides API summary/full pull for {definition['deck_id']} before apply",
        "qa_notes": [
            "City slides follow canonical CLUSTERS.json membership, not a route list.",
            "Exactly one unit-economics slide (one representative exact-bound route) follows the city slides.",
            "Synchronize slide IDs and object inventory to the live deck only after source-package preflight passes.",
        ],
    }

    images = [
        {
            "image_key": "cover_hero",
            "role": "n30_market_composite",
            "asset_ref": None,
            "registry_key": None,
            "asset_path": None,
            "target_slide_index": 1,
            "target_slide_object_id": slides[0]["slide_object_id"],
            "target_object_id": None,
            "status": "needs_sourcing",
            "provenance_required": True,
            "notes": "Market-specific source-approved N30 composite; no Atlas-generated imagery.",
        }
    ]
    for s in city_slides:
        images.append({
            "image_key": f"atlas_route_screenshot_slide_{s['index']:02d}",
            "role": "atlas_route_screenshot",
            "asset_ref": None,
            "registry_key": None,
            "asset_path": None,
            "target_slide_index": s["index"],
            "target_slide_object_id": s["slide_object_id"],
            "target_object_id": None,
            "status": "human_insertion_only",
            "provenance_required": True,
            "notes": "Reserved for Jaideep or another human. Automation must not populate this slot.",
        })
    image_manifest = {
        "schema": "deck-image-manifest-v3",
        "deck_key": slug,
        "policy": "N30 market compositing with documented provenance; Atlas screenshot slots remain human-only, one per city slide",
        "asset_registry": "deck-studio/assets/ASSET-REGISTRY.json",
        "role_contract": "deck-studio/docs/ASSET-ROLE-CONTRACT.md",
        "images": images,
    }

    content_source = {
        "schema_version": "country-content-source-v3",
        "deck_key": slug,
        "reference_lineage": {
            "deck_key": "grab",
            "deck_id": GRAB_DECK_ID,
            "instruction": "Duplicate or bind the approved reference; preserve layouts and substitute source-backed fields only.",
        },
        "slide_sources": [
            {
                "slide_index": s["index"],
                "slide_object_id": s["slide_object_id"],
                "role": s["purpose"],
                "title": s["title"],
                "sources": [
                    "market-scope.json",
                    "economics-binding.json",
                    "generated-deck-economics.json" if s["purpose"] in {"market_overview", "one_route_economics", "country_prize"} else f"partner-pitch/partners/{partner}.json",
                ],
            }
            for s in slides
        ],
    }

    config = {
        "deck_key": slug,
        "deck_id": definition["deck_id"],
        "display_name": f"{label} × Navier — {country} mobility review",
        "deck_type": "country_mobility_review",
        "editing_mode": "slides_api_only",
        "live_deck_url": f"https://docs.google.com/presentation/d/{definition['deck_id']}/edit",
        "partner_id": partner,
        "slide_manifest": f"deck-studio/decks/{slug}/slide-manifest.json",
        "content_source": f"deck-studio/decks/{slug}/content-source.json",
        "image_manifest": f"deck-studio/decks/{slug}/image-manifest.json",
        "source_paths": [
            f"partner-pitch/partners/{partner}.json",
            f"data-clean/partners/{partner}.json",
            definition["aggregate"],
            "data-clean/ROUTES.json",
            f"deck-studio/decks/{slug}/market-scope.json",
            f"deck-studio/decks/{slug}/economics-binding.json",
            f"deck-studio/decks/{slug}/generated-deck-economics.json",
        ],
        "canonical_market_scope": definition["scope_market_keys"] or ["Egypt routes held pending exact support"],
        "cover_logos": {
            "navier_logo": {"status": "banked", "asset_path": "deck-studio/assets/logos/navier/navier-wordmark-white.png"},
            "partner_logo": {"status": "banked", "asset_path": definition["logo"], "provenance": f"deck-studio/assets/logos/partners/{partner}/LOGO-SOURCE.json"},
        },
        "rules": COMMON_RULES,
        "current_spec_requirements": {
            "reference_deck_key": "grab",
            "reference_deck_id": GRAB_DECK_ID,
            "spine": "market-overview -> one slide per city -> one unit-economics -> TAM",
            "city_source": "canonical CLUSTERS.json membership",
            "shared_economics_generator": "deck-studio/decks/gen_deck_economics.py",
            "atlas_screenshot_automation": "forbidden",
        },
        "asset_policy": {"n30_compositing": "market-specific", "gold": "minimal", "stable_linked_urls": True},
        "generation_type": "deterministic_source_package",
        "notes": "Source package only until preflight passes and an approved Slides API apply/readback is completed.",
    }

    editplan = {
        "schema_version": "country-review-source-editplan-v2",
        "deck_key": slug,
        "presentation_id": definition["deck_id"],
        "apply_status": "blocked_pending_reference_duplication_and_live_inventory_pull",
        "operations": [],
        "slide_text": rendered_text,
        "economics_source": "generated-deck-economics.json",
        "atlas_route_screenshot_policy": "human_insertion_only",
    }

    dump(out / "market-scope.json", scope)
    dump(out / "economics-binding.json", binding)
    dump(out / "slide-manifest.json", slide_manifest)
    dump(out / "content-source.json", content_source)
    dump(out / "image-manifest.json", image_manifest)
    dump(out / "deck.config.json", config)
    dump(out / "deck.editplan.json", editplan)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--deck", action="append", choices=sorted(DEFINITIONS))
    args = ap.parse_args()
    for slug in args.deck or sorted(DEFINITIONS):
        build(slug, DEFINITIONS[slug])
    print(f"Built source packages for: {', '.join(args.deck or sorted(DEFINITIONS))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
