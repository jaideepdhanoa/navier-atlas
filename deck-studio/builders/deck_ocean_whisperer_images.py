#!/usr/bin/env python3
"""Ocean Whisperer wave-2: Tier-A deck plates (cover, slide2, Three C's, TAM, partner-roles, econ)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDERS = ROOT / "builders"
sys.path.insert(0, str(BUILDERS))

from deck_bolt_wave2_images import (  # noqa: E402
    FOIL_STATE,
    REGISTRY_PATH,
    generate_and_save_plate,
    load_json,
    write_json,
)
from deck_autonomy_sync import publish_assets_to_drive  # noqa: E402

DECK = "ocean-whisperer"
BG_DIR = ROOT / "assets/backgrounds/decks/ocean-whisperer"
MARKET_DIR = ROOT / "assets/backgrounds/markets/curacao"

# Corridor-specific landmarks for slides 8–10 (each econ slide gets its own integrated plate).
ECON_CORRIDOR_LANDMARKS: dict[str, str] = {
    "hato-baoase": (
        "Hato (Curaçao Int'l) airport waterfront on the north leeward coast opening to Baoase "
        "Luxury Resort's south-coast jetty — colourful Willemstad hills beyond, unmistakably Curaçao"
    ),
    "hato-sandals": (
        "Hato airport waterfront transitioning along open Caribbean water toward Spanish Water lagoon "
        "and Sandals Royal Curaçao's deep-water marina — tropical palms, unmistakably Curaçao"
    ),
    "willemstad-sandals": (
        "Willemstad UNESCO Sint Anna Bay colourful Dutch colonial waterfront and cruise mega-pier "
        "feeding into Spanish Water and Sandals Royal Curaçao — unmistakably Curaçao Caribbean"
    ),
}


def prompt_three_cs() -> str:
    return (
        "Using <IMAGE_0> as the white hydrofoil vessel as the exact form and colour reference, "
        "produce a single photorealistic 16:9 photograph along Curaçao's leeward resort coast at "
        "golden hour. Foreground: the white hydrofoil gliding on calm turquoise Caribbean water, "
        f"{FOIL_STATE}, rear three-quarter view. Background: colourful Willemstad waterfront and "
        "Spanish Water hills — hospitality luxury mood (Cost · Comfort · Convenience). Upper-left "
        "clear for headline copy. Exactly one vessel; hull/cabin/V-mark as reference; in-water no "
        "seam. No woman on a phone, no booking scene, no logos, no text, no other boats."
    )


def prompt_partner_roles_curacao() -> str:
    return (
        "Using <IMAGE_0> as the white hydrofoil vessel as the exact form and colour reference, "
        "produce a single photorealistic 16:9 photograph for a partner-roles slide. "
        "Full-width edge-to-edge panoramic scene of a Curaçao luxury resort jetty at Spanish Water "
        "with colourful Willemstad hills beyond — rich scenic detail across the entire frame from "
        "left to right. The white hydrofoil is moored alongside the jetty, foils down, clean "
        "reflection. Warm premium golden-hour light. Never an artificial gradient panel, never a "
        "blank chart-safe zone or empty right third. Exactly one vessel, hull/cabin/V-mark exactly "
        "as the reference, in-water no seam. Single integrated photograph. No logos, no text."
    )


def prompt_econ_corridor(corridor_key: str) -> str:
    landmark = ECON_CORRIDOR_LANDMARKS[corridor_key]
    return (
        "Using <IMAGE_0> as the white hydrofoil vessel as the exact form and colour reference, "
        "produce a single photorealistic 16:9 photograph for a unit-economics slide. "
        f"Full-width edge-to-edge panoramic scene of {landmark} — the landmark skyline, coastline, "
        "and harbour fill the entire frame from left to right with rich market-specific detail. "
        "Must be unmistakable and identifiable at thumbnail size — vibrant warm golden-hour light, "
        "never a generic empty ocean, never an artificial gradient panel or blank chart-safe zone. "
        f"A single white hydrofoil is small in the lower-center foreground on open water, {FOIL_STATE}. "
        "Hull/cabin/V-mark exactly as the reference, in-water no seam. Exactly one vessel integrated "
        "naturally in the scene — not a pasted overlay, not a collage. Cinematic aspirational premium "
        "grade. No people, no logos, no text, no map graphics."
    )


OW_PLATES: list[dict] = [
    {
        "key": "ow-cover-hero",
        "role": "cover_hero",
        "scope": "deck",
        "partner": DECK,
        "local_path": "assets/backgrounds/decks/ocean-whisperer/ow-cover-curacao-tier-a-v1.png",
        "market_slug": "curacao-curacao",
        "seed": "ow-wave2-cover-curacao",
        "prompt": (
            "Using <IMAGE_0> as the white hydrofoil vessel as the exact form and colour reference, "
            "produce a single photorealistic 16:9 photograph. Foreground: the vessel cruising on calm "
            "turquoise Caribbean water along Curaçao's leeward coast, foils deployed, hull elevated, "
            "light bow wake and clean reflection, rear three-quarter view bow angled left. Background: "
            "colourful Willemstad Dutch colonial waterfront and Spanish Water lagoon hills — unmistakably "
            "Curaçao. Warm golden-hour sunlight from the left. Vessel lower-center-left; upper-left clear "
            "for headline. Exactly one vessel; hull/cabin/V-mark as reference; in-water no seam. "
            "No people, no logos, no text, no other boats. No Grab, no Phuket, no Bali."
        ),
        "used_by": [{"deck": DECK, "slide_index": 1, "slide_object_id": "p1", "target_object_id": "p1_i2"}],
    },
    {
        "key": "ow-value-prop-bg",
        "role": "value_prop_bg",
        "scope": "deck",
        "partner": DECK,
        "local_path": "assets/backgrounds/decks/ocean-whisperer/ow-slide2-booking-curacao-tier-a-v1.png",
        "market_slug": "curacao-curacao",
        "seed": "ow-wave2-slide2-curacao",
        "prompt": (
            "Using <IMAGE_0> as the white hydrofoil vessel as the exact form and colour reference, "
            "produce a single photorealistic 16:9 photograph at a luxury resort jetty on Curaçao's "
            "Spanish Water — wooden pier, calm turquoise lagoon, tropical palms. Foreground left third: "
            "a woman on the berth looking at her phone booking a ride, candid three-quarter from behind, "
            "light resort clothing. The white hydrofoil easing to the berth, foils down, clean reflection. "
            "Warm morning light. Exactly one vessel; hull as reference; in-water no seam. "
            "No logos, no text, no other boats."
        ),
        "used_by": [{"deck": DECK, "slide_index": 2, "slide_object_id": "narr2_page", "target_object_id": "narr2_bg_img"}],
    },
    {
        "key": "ow-three-cs-bg",
        "role": "three_cs_bg",
        "scope": "deck",
        "partner": DECK,
        "local_path": "assets/backgrounds/decks/ocean-whisperer/ow-three-cs-curacao-tier-a-v1.png",
        "market_slug": "curacao-curacao",
        "seed": "ow-wave2-three-cs-curacao",
        "prompt": prompt_three_cs,
        "used_by": [
            {
                "deck": DECK,
                "slide_index": 3,
                "slide_object_id": "g3f139a0b6ec_0_0",
                "target_object_id": "g3f139a0b6ec_0_1",
            }
        ],
    },
    {
        "key": "ow-tam-bg",
        "role": "tam_bg",
        "scope": "deck",
        "partner": DECK,
        "local_path": "assets/backgrounds/decks/ocean-whisperer/ow-tam-caribbean-tier-a-v1.png",
        "market_slug": "caribbean",
        "seed": "ow-wave2-tam-caribbean",
        "prompt": (
            "Using <IMAGE_0> as the white hydrofoil vessel as the exact form and colour reference, "
            "produce a single photorealistic 16:9 photograph: wide aspirational Caribbean seascape at "
            "golden hour. Small white hydrofoil lower-center heading along Curaçao's coast; distant "
            "silhouettes suggest Bonaire and Aruba on the horizon — ABC island network scale. Expansive "
            "open sky upper two-thirds for data overlay. Foils deployed, clean wake, hull as reference, "
            "in-water no seam. Exactly one vessel. No map graphics, no people, no logos, no text."
        ),
        "used_by": [
            {
                "deck": DECK,
                "slide_index": 11,
                "slide_object_id": "g3eec5122801_0_562",
                "target_object_id": "navierBg_s26",
            }
        ],
    },
    {
        "key": "ow-partner-roles-bg",
        "role": "partner_roles_bg",
        "scope": "deck",
        "partner": DECK,
        "local_path": "assets/backgrounds/decks/ocean-whisperer/ow-partner-roles-curacao-tier-a-v1.png",
        "market_slug": "curacao-curacao",
        "seed": "ow-wave2-partner-roles-v2",
        "prompt": prompt_partner_roles_curacao,
        "used_by": [
            {
                "deck": DECK,
                "slide_index": 12,
                "slide_object_id": "g3ea5e0fb254_4_357",
                "target_object_id": "g3ea5e0fb254_4_358",
            }
        ],
    },
]

ECON_PLATES: list[dict] = [
    {
        "key": "ow-econ-hato-baoase-v1",
        "role": "econ_market_bg",
        "scope": "market",
        "partner": DECK,
        "local_path": "assets/backgrounds/markets/curacao/ow-econ-hato-baoase-tier-a-v1.png",
        "market_slug": "curacao-curacao",
        "atlas_city_id": "curacao-curacao",
        "seed": "ow-wave2-econ-hato-baoase",
        "prompt": lambda: prompt_econ_corridor("hato-baoase"),
        "used_by": [{"deck": DECK, "slide_index": 8, "target_object_id": "navierBg_s23"}],
    },
    {
        "key": "ow-econ-hato-sandals-v1",
        "role": "econ_market_bg",
        "scope": "market",
        "partner": DECK,
        "local_path": "assets/backgrounds/markets/curacao/ow-econ-hato-sandals-tier-a-v1.png",
        "market_slug": "curacao-curacao",
        "atlas_city_id": "curacao-curacao",
        "seed": "ow-wave2-econ-hato-sandals",
        "prompt": lambda: prompt_econ_corridor("hato-sandals"),
        "used_by": [{"deck": DECK, "slide_index": 9, "target_object_id": "navierBg_s24"}],
    },
    {
        "key": "ow-econ-willemstad-sandals-v1",
        "role": "econ_market_bg",
        "scope": "market",
        "partner": DECK,
        "local_path": "assets/backgrounds/markets/curacao/ow-econ-willemstad-sandals-tier-a-v1.png",
        "market_slug": "curacao-curacao",
        "atlas_city_id": "curacao-curacao",
        "seed": "ow-wave2-econ-willemstad-sandals",
        "prompt": lambda: prompt_econ_corridor("willemstad-sandals"),
        "used_by": [{"deck": DECK, "slide_index": 10, "target_object_id": "navierBg_s25"}],
    },
]


def cmd_generate_all() -> int:
    BG_DIR.mkdir(parents=True, exist_ok=True)
    MARKET_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    for spec in OW_PLATES:
        spec = dict(spec)
        spec["prompt"] = spec["prompt"] if isinstance(spec["prompt"], str) else spec["prompt"]()
        results.append(generate_and_save_plate(spec))
    for spec in ECON_PLATES:
        econ_spec = dict(spec)
        econ_spec["prompt"] = econ_spec["prompt"]()
        results.append(generate_and_save_plate(econ_spec))
    print(json.dumps({"generated": results}, indent=2))
    return 0


def cmd_generate_econ() -> int:
    MARKET_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    for spec in ECON_PLATES:
        s = dict(spec)
        s["prompt"] = s["prompt"]()
        results.append(generate_and_save_plate(s))
    print(json.dumps({"generated": results}, indent=2))
    return 0


def cmd_generate_three_cs() -> int:
    spec = next(s for s in OW_PLATES if s["key"] == "ow-three-cs-bg")
    spec = dict(spec)
    spec["prompt"] = spec["prompt"]()
    result = generate_and_save_plate(spec)
    print(json.dumps({"generated": result}, indent=2))
    return 0


def cmd_generate_partner_roles() -> int:
    spec = next(s for s in OW_PLATES if s["key"] == "ow-partner-roles-bg")
    spec = dict(spec)
    spec["prompt"] = spec["prompt"]()
    result = generate_and_save_plate(spec)
    print(json.dumps({"generated": result}, indent=2))
    return 0


def cmd_publish() -> int:
    registry = load_json(REGISTRY_PATH)
    assets = registry.setdefault("assets", {})
    for spec in OW_PLATES:
        key = spec["key"]
        asset = assets.setdefault(key, {})
        asset.update(
            {
                "role": spec["role"],
                "scope": spec["scope"],
                "partner": DECK,
                "market_slug": spec.get("market_slug"),
                "local_path": spec["local_path"],
                "status": asset.get("status", "checked_in"),
                "composited": False,
                "reproducible": True,
                "used_by": spec.get("used_by", []),
                "license": "navier-internal",
            }
        )
    for spec in ECON_PLATES:
        econ_asset = assets.setdefault(spec["key"], {})
        econ_asset.update(
            {
                "role": spec["role"],
                "scope": spec["scope"],
                "partner": DECK,
                "market_slug": spec["market_slug"],
                "atlas_city_id": spec["atlas_city_id"],
                "local_path": spec["local_path"],
                "status": econ_asset.get("status", "checked_in"),
                "composited": False,
                "reproducible": True,
                "used_by": spec["used_by"],
                "license": "navier-internal",
                "provenance": "tier_a_reference_guided_integrated_vessel",
            }
        )
    coverage = registry.setdefault("deck_coverage", {}).setdefault(DECK, {})
    coverage["roles"] = {
        "cover_hero": "checked_in",
        "partner_logo": "checked_in",
        "value_prop_bg": "checked_in",
        "three_cs_bg": "checked_in",
        "tam_bg": "checked_in",
        "partner_roles_bg": "checked_in",
        "econ_market_bg": "checked_in(3 corridors)",
    }
    coverage["status"] = "wave2_indexed"
    write_json(REGISTRY_PATH, registry)
    publish_assets_to_drive(REGISTRY_PATH)
    registry = load_json(REGISTRY_PATH)
    all_keys = [s["key"] for s in OW_PLATES] + [s["key"] for s in ECON_PLATES]
    urls = {k: registry["assets"][k]["source_url"] for k in all_keys if registry["assets"].get(k, {}).get("source_url")}
    print(json.dumps({"published": urls}, indent=2))
    return 0


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Ocean Whisperer image pipeline")
    ap.add_argument(
        "cmd",
        choices=[
            "generate-all",
            "generate-econ",
            "generate-three-cs",
            "generate-partner-roles",
            "publish",
        ],
    )
    args = ap.parse_args()
    if args.cmd == "generate-all":
        return cmd_generate_all()
    if args.cmd == "generate-econ":
        return cmd_generate_econ()
    if args.cmd == "generate-three-cs":
        return cmd_generate_three_cs()
    if args.cmd == "generate-partner-roles":
        return cmd_generate_partner_roles()
    return cmd_publish()


if __name__ == "__main__":
    raise SystemExit(main())