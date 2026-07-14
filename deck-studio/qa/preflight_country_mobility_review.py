#!/usr/bin/env python3
"""Blocking preflight for deterministic country mobility review packages."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
REQUIRED = {
    "deck.config.json", "slide-manifest.json", "content-source.json",
    "image-manifest.json", "market-scope.json", "economics-binding.json",
    "generated-deck-economics.json", "deck.editplan.json",
}


def load(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_one(deck: Path) -> dict[str, Any]:
    errors: list[str] = []
    files = {p.name for p in deck.iterdir() if p.is_file()}
    for name in sorted(REQUIRED - files):
        fail(errors, f"missing required file: {name}")
    if "country-content.json" in files:
        fail(errors, "legacy free-form country-content.json is forbidden")
    if errors:
        return {"deck_key": deck.name, "status": "FAIL", "errors": errors}

    config = load(deck / "deck.config.json")
    manifest = load(deck / "slide-manifest.json")
    content = load(deck / "content-source.json")
    images = load(deck / "image-manifest.json")
    scope = load(deck / "market-scope.json")
    binding = load(deck / "economics-binding.json")
    generated = load(deck / "generated-deck-economics.json")
    editplan = load(deck / "deck.editplan.json")

    if config.get("deck_type") != "country_mobility_review":
        fail(errors, "deck_type must be country_mobility_review")
    req = config.get("current_spec_requirements") or {}
    if req.get("reference_deck_key") != "grab":
        fail(errors, "approved Grab reference lineage is missing")
    if req.get("spine") != "market-overview -> one slide per city -> one unit-economics -> TAM":
        fail(errors, "locked country-review spine requirement is missing")
    if req.get("city_source") != "canonical CLUSTERS.json membership":
        fail(errors, "canonical city source requirement is missing")
    if req.get("shared_economics_generator") != "deck-studio/decks/gen_deck_economics.py":
        fail(errors, "shared economics generator binding is missing")
    if req.get("atlas_screenshot_automation") != "forbidden":
        fail(errors, "Atlas screenshot automation must be forbidden")

    for source in config.get("source_paths") or []:
        if not (ROOT / source).exists():
            fail(errors, f"config source path does not exist: {source}")
    for logo in (config.get("cover_logos") or {}).values():
        asset = logo.get("asset_path")
        if logo.get("status") == "banked" and (not asset or not (ROOT / asset).exists()):
            fail(errors, f"banked logo asset does not exist: {asset}")
        provenance = logo.get("provenance")
        if provenance and not (ROOT / provenance).exists():
            fail(errors, f"logo provenance does not exist: {provenance}")

    slides = manifest.get("slides") or []
    if manifest.get("slide_count") != len(slides):
        fail(errors, "slide_count does not match slide list")
    roles = [s.get("purpose") for s in slides]
    for role, name in (("market_overview", "market overview"), ("one_route_economics", "unit-economics"), ("country_prize", "TAM")):
        if roles.count(role) != 1:
            fail(errors, f"exactly one {name} slide required, found {roles.count(role)}")
    city_positions = [i for i, role in enumerate(roles) if role == "city_review"]
    if not city_positions:
        fail(errors, "at least one city slide required")
    if len(city_positions) != len(scope.get("cities") or []):
        fail(errors, "city slide count does not match canonical city roster")
    if roles.count("market_overview") == 1 and roles.count("one_route_economics") == 1 and roles.count("country_prize") == 1 and city_positions:
        mo, econ, tam = roles.index("market_overview"), roles.index("one_route_economics"), roles.index("country_prize")
        if not (mo < min(city_positions) and max(city_positions) < econ < tam):
            fail(errors, "spine order is not market-overview -> cities -> unit-economics -> TAM")

    content_ids = {s.get("slide_object_id") for s in content.get("slide_sources") or []}
    manifest_ids = {s.get("slide_object_id") for s in slides}
    if content_ids != manifest_ids:
        fail(errors, "content-source coverage does not exactly match slide manifest")

    atlas_slots = [i for i in images.get("images") or [] if i.get("role") == "atlas_route_screenshot"]
    if len(atlas_slots) != len(city_positions):
        fail(errors, "each city slide must have one Atlas screenshot slot")
    for image in images.get("images") or []:
        if image.get("provenance_required") is not True:
            fail(errors, f"image lacks provenance_required=true: {image.get('image_key')}")
        if image.get("role") == "atlas_route_screenshot":
            if image.get("status") != "human_insertion_only":
                fail(errors, f"Atlas slot status is not human_insertion_only: {image.get('image_key')}")
            if any(image.get(k) is not None for k in ("asset_ref", "asset_path", "registry_key", "target_object_id")):
                fail(errors, f"Atlas slot was populated by automation: {image.get('image_key')}")

    generated_sources = generated.get("source_files") or {}
    generated_hashes = generated.get("source_sha256") or {}
    for key in ("binding", "aggregate", "routes"):
        path = Path(generated_sources.get(key, ""))
        if not path.is_absolute():
            path = ROOT / path
        if not path.exists():
            fail(errors, f"generated source missing: {key}")
        elif sha(path) != generated_hashes.get(key):
            fail(errors, f"generated economics is stale against {key}")
    if generated.get("generator") != "deck-studio/decks/gen_deck_economics.py":
        fail(errors, "generated economics did not use the shared generator")
    if generated.get("checks", {}).get("borrowed_country_or_route_values") is not False:
        fail(errors, "borrowed route/country values are not explicitly false")

    gen_route = generated.get("economics_route") or {}
    bind_route = binding.get("economics_route") or {}
    if gen_route.get("route_id") != bind_route.get("route_id"):
        fail(errors, "economics route ID changed during generation")
    if bind_route.get("route_id") is None and gen_route.get("unit_economics") is not None:
        fail(errors, "held economics route contains non-null values")

    if editplan.get("apply_status") != "blocked_pending_reference_duplication_and_live_inventory_pull":
        fail(errors, "source edit plan must remain blocked before live inventory pull")
    if editplan.get("operations"):
        fail(errors, "source edit plan must not contain live operations")

    return {
        "deck_key": deck.name,
        "status": "PASS" if not errors else "FAIL",
        "slide_count": len(slides),
        "city_slides": len(city_positions),
        "country_total_status": generated.get("country_total", {}).get("status"),
        "errors": errors,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("deck_dirs", nargs="+")
    ap.add_argument("--json", dest="json_out", type=Path)
    args = ap.parse_args()
    results = [validate_one(Path(d).resolve()) for d in args.deck_dirs]
    report = {
        "schema_version": "country-mobility-review-preflight-v1",
        "status": "PASS" if all(r["status"] == "PASS" for r in results) else "FAIL",
        "decks": results,
        "live_apply_performed": False,
        "release_clearance": False,
    }
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
