#!/usr/bin/env python3
"""Build deterministic source packages for country mobility review decks.

The builder preserves the approved Grab mobility lineage, emits alternating
city/route and one-route economics chapters, and reserves every Atlas route
screenshot slot for direct human insertion. It does not edit Google Slides.
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
    "Every city chapter is immediately followed by one representative route economics chapter.",
    "Route IDs match canonical ROUTES.json exactly; unsupported values remain null.",
    "Atlas route screenshot slots are reserved for Jaideep or another human and remain unpopulated by automation.",
    "N30 composites use source-approved market imagery, stable linked URLs, documented provenance, and minimal gold.",
    "Live deck IDs and slide manifests must be read back and synchronized after apply.",
]

DEFINITIONS: dict[str, dict[str, Any]] = {
    "didi-brazil": {
        "partner_id": "didi",
        "partner_label": "DiDi",
        "country": "Brazil",
        "deck_id": "1oJ-Z5fI80E3VxTVZ1V35Mn7rEr26mOU3Dqq7zwtSkEg",
        "logo": "deck-studio/assets/logos/partners/didi/didi-logo-official.png",
        "aggregate": "finance/recal/agg-didi.json",
        "scope_market_keys": ["brazil"],
        "country_total": {"expected_annual_revenue_usd": 23404822.0, "expected_vessels_supported": 113,
            "supported_route_ids": ["rn-1886629dbf0c", "rn-80f0d0ebe0bd", "rn-369ef0eb69d9", "rn-00bb6ded4be5"]},
        "pairs": [
            ("rio-niteroi", "Rio de Janeiro", "Praça XV → Arariboia", "rn-1886629dbf0c", "Cross-bay commuter connection between central Rio and Niterói."),
            ("rio-charitas", "Rio de Janeiro", "Praça XV → Charitas", "rn-80f0d0ebe0bd", "Fast cross-bay connection to Charitas."),
            ("rio-cocota", "Rio de Janeiro", "Praça XV → Cocotá", "rn-369ef0eb69d9", "City-to-island connection serving Ilha do Governador."),
            ("rio-paqueta", "Rio de Janeiro", "Praça XV → Paquetá", "rn-00bb6ded4be5", "Longer city-to-island passenger connection."),
        ],
    },
    "indrive-brazil": {
        "partner_id": "indrive",
        "partner_label": "inDrive",
        "country": "Brazil",
        "deck_id": "1QTk8OnW60KuYSMwm2YSko9t1fDIqhEMM71lMk64D2A4",
        "logo": "deck-studio/assets/logos/partners/indrive/indrive-logo-white-cover.png",
        "aggregate": "finance/recal/agg-indrive.json",
        "scope_market_keys": ["indrive-brazil"],
        "country_total": {"expected_annual_revenue_usd": 23404822.0, "expected_vessels_supported": 113,
            "supported_route_ids": ["rn-1886629dbf0c", "rn-80f0d0ebe0bd", "rn-369ef0eb69d9", "rn-00bb6ded4be5"]},
        "pairs": [
            ("rio-niteroi", "Rio de Janeiro", "Praça XV → Arariboia", "rn-1886629dbf0c", "Cross-bay commuter connection between central Rio and Niterói."),
            ("rio-charitas", "Rio de Janeiro", "Praça XV → Charitas", "rn-80f0d0ebe0bd", "Fast cross-bay connection to Charitas."),
            ("rio-cocota", "Rio de Janeiro", "Praça XV → Cocotá", "rn-369ef0eb69d9", "City-to-island connection serving Ilha do Governador."),
            ("rio-paqueta", "Rio de Janeiro", "Praça XV → Paquetá", "rn-00bb6ded4be5", "Longer city-to-island passenger connection."),
        ],
    },
    "didi-mexico": {
        "partner_id": "didi",
        "partner_label": "DiDi",
        "country": "Mexico",
        "deck_id": "1llJbJgVOejzupIreUzsrvEkIL0Y8pgaW5WPO8OUh6R8",
        "logo": "deck-studio/assets/logos/partners/didi/didi-logo-official.png",
        "aggregate": "finance/recal/agg-didi.json",
        "scope_market_keys": ["mexico-caribbean", "mexico-pacific"],
        "country_total": {"expected_annual_revenue_usd": 14759160.0, "expected_vessels_supported": 88,
            "supported_route_ids": ["ics-413f51cd44", "ics-dd1d814699", "ics-aa6ff40d2d"]},
        "pairs": [
            ("cancun-isla-mujeres", "Cancún and Isla Mujeres", "Puerto Juárez → Isla Mujeres", "ics-413f51cd44", "High-frequency island access from the Cancún waterfront."),
            ("playa-cozumel", "Playa del Carmen and Cozumel", "Playa del Carmen → Cozumel", "ics-dd1d814699", "Mainland-to-island passenger connection."),
            ("vallarta-yelapa", "Puerto Vallarta", "Puerto Vallarta → Yelapa", "ics-89a8844858", "Coastal access south of Puerto Vallarta."),
            ("cabos", "Los Cabos", "Cabo San Lucas Marina → Los Cabos", "ics-db0930d9d1", "Local marina connection in the Los Cabos area."),
        ],
        "pair_holds": {
            "vallarta-yelapa": "Annual revenue and fleet support remain blank because the route finance row is incomplete.",
            "cabos": "Annual revenue and fleet support remain blank because route-level fare and financial inputs are incomplete.",
        },
    },
    "indrive-egypt": {
        "partner_id": "indrive",
        "partner_label": "inDrive",
        "country": "Egypt",
        "deck_id": "1hNyCMz8UTmfzTghYX5xwU9aZv0x3U975JJMkDVhUVCg",
        "logo": "deck-studio/assets/logos/partners/indrive/indrive-logo-white-cover.png",
        "aggregate": "finance/recal/agg-indrive.json",
        "scope_market_keys": [],
        "country_total": {"expected_annual_revenue_usd": None, "expected_vessels_supported": None,
            "supported_route_ids": [],
            "hold_reason": "Country financial values remain blank pending named-terminal validation and route-level passenger demand and fare evidence."},
        "pairs": [
            ("hurghada", "Hurghada", "Hurghada Marina → Giftun Island", None, "Island-access route under local terminal and operating review."),
            ("sharm", "Sharm El Sheikh", "Sharm Marina → Ras Mohammed", None, "Reef-access route under local terminal and operating review."),
        ],
        "pair_holds": {
            "hurghada": "Route ID and financial values remain blank pending authoritative terminal coordinates, annual passenger demand, and fare evidence.",
            "sharm": "Route ID and financial values remain blank pending authoritative terminal coordinates, annual passenger demand, and fare evidence.",
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
    pairs = []
    pair_holds = definition.get("pair_holds") or {}
    for key, city, route_label, route_id, city_thesis in definition["pairs"]:
        pairs.append({
            "pair_key": key,
            "city_key": key,
            "city_label": city,
            "route_label": route_label,
            "route_id": route_id,
            "city_thesis": city_thesis,
            "hold_reason": pair_holds.get(key),
            "selection_rule": "highest supported annual route revenue within the city chapter; source order breaks ties" if route_id else "no exact supported route available; values remain null",
        })

    scope = {
        "schema_version": "country-market-scope-v2",
        "deck_key": slug,
        "partner_id": partner,
        "country": country,
        "geography_rule": "global_canonical intersection partner clusters",
        "source_paths": [
            f"partner-pitch/partners/{partner}.json",
            f"data-clean/partners/{partner}.json",
            "data-clean/CLUSTERS.json",
            "data-clean/ROUTES.json",
        ],
        "finance_market_keys": definition["scope_market_keys"],
        "city_route_pairs": [{k: p[k] for k in ("pair_key", "city_key", "city_label", "route_label", "route_id", "city_thesis")} for p in pairs],
        "unsupported_values_policy": "null",
    }
    binding = {
        "schema_version": "country-economics-binding-v2",
        "deck_key": slug,
        "partner_id": partner,
        "country": country,
        "generator": "deck-studio/decks/gen_deck_economics.py",
        "aggregate_source": definition["aggregate"],
        "canonical_routes_source": "data-clean/ROUTES.json",
        "city_route_pairs": pairs,
        "country_total": deepcopy(definition["country_total"]),
        "rules": {
            "id_matching": "exact",
            "unsupported_values": "null",
            "country_substitution": "forbidden",
            "published_brazil_basis": "shared unchanged across DiDi Brazil and inDrive Brazil" if country == "Brazil" else None,
        },
    }

    slides = []
    rendered_text: dict[str, str] = {}
    idx = 1
    opening = [
        ("cover", f"{definition['partner_label']} × Navier | {country}"),
        ("partner_country_thesis", f"Why water mobility matters in {country}"),
        ("country_scope", f"The {country} opportunity"),
    ]
    for role, title in opening:
        slides.append(slide(slug, idx, role, title)); rendered_text[f"slide_{idx:02d}_title"] = title; idx += 1
    for p in pairs:
        city_title = f"{p['city_label']}: {p['route_label']}"
        econ_title = f"Route economics: {p['route_label']}"
        slides.append(slide(slug, idx, "city_route_review", city_title))
        rendered_text[f"slide_{idx:02d}_title"] = city_title
        rendered_text[f"slide_{idx:02d}_body"] = p["city_thesis"]
        idx += 1
        slides.append(slide(slug, idx, "one_route_economics", econ_title))
        rendered_text[f"slide_{idx:02d}_title"] = econ_title
        rendered_text[f"slide_{idx:02d}_body"] = (
            p["hold_reason"] if p.get("hold_reason") else
            "Annual passenger demand, one-way fare, annual revenue, and fleet support are populated by the shared route economics generator."
        )
        idx += 1
    closing = [
        ("country_prize", f"A focused path to scale in {country}"),
        ("integration_model", f"How {definition['partner_label']} and Navier work together"),
        ("phased_rollout", "Prove the route, then expand"),
        ("decision_and_ask", "A joint route review is the next step"),
        ("close", f"Build the complete journey in {country}"),
    ]
    for role, title in closing:
        slides.append(slide(slug, idx, role, title)); rendered_text[f"slide_{idx:02d}_title"] = title; idx += 1

    slide_manifest = {
        "deck_key": slug,
        "presentation_id": definition["deck_id"],
        "source": "deterministic country-review plan based on approved Grab mobility lineage",
        "slide_count": len(slides),
        "object_inventory_status": "stale_requires_pull",
        "slides": slides,
        "pull_command": f"Google Slides API summary/full pull for {definition['deck_id']} after approved template duplication and before apply",
        "qa_notes": [
            "Current live inventory belongs to the rejected country_proposal build and is not reused as the source chassis.",
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
    for s in slides:
        if s["purpose"] == "city_route_review":
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
        "schema": "deck-image-manifest-v2",
        "deck_key": slug,
        "policy": "N30 market compositing with documented provenance; Atlas screenshot slots remain human-only",
        "asset_registry": "deck-studio/assets/ASSET-REGISTRY.json",
        "role_contract": "deck-studio/docs/ASSET-ROLE-CONTRACT.md",
        "images": images,
    }

    content_source = {
        "schema_version": "country-content-source-v2",
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
                    "generated-deck-economics.json" if s["purpose"] in {"country_scope", "one_route_economics", "country_prize"} else f"partner-pitch/partners/{partner}.json",
                ],
            }
            for s in slides
        ],
    }

    config = {
        "deck_key": slug,
        "deck_id": definition["deck_id"],
        "display_name": f"{definition['partner_label']} × Navier — {country} mobility review",
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
            "city_economics_pairing": True,
            "shared_economics_generator": "deck-studio/decks/gen_deck_economics.py",
            "atlas_screenshot_automation": "forbidden",
        },
        "asset_policy": {"n30_compositing": "market-specific", "gold": "minimal", "stable_linked_urls": True},
        "generation_type": "deterministic_source_package",
        "notes": "Source package only until preflight passes and an approved Slides API apply/readback is completed.",
    }

    editplan = {
        "schema_version": "country-review-source-editplan-v1",
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
        print(slug)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
