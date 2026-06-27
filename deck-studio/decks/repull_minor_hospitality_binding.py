#!/usr/bin/env python3
"""Re-pull Minor Hotels hospitality economics-binding from cached manifest (#112)."""
from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
DECK = "minor-hotels"
GOLD_DECK_ID = "1p5NtoaORRWyBpcsbfqnSB9PLg9yyTpvuzJAyBMjen4o"
RAW = "https://raw.githubusercontent.com/jaideepdhanoa/navier-atlas/main"

MANIFEST = ROOT / f"decks/{DECK}/slide-manifest.json"
BINDING = ROOT / f"decks/{DECK}/economics-binding.json"
GOLD_ECON = REPO / "finance/model/minor-hotels-econ-gold-2026-06-25.json"
ASSET_SRC = REPO / "decks/minor-hotels-v2/assets"
ASSET_DST = ROOT / "assets/minor-hotels/econ"
REGISTRY = ROOT / "assets/ASSET-REGISTRY.json"

# Slides 18–19 use compact layout; 20–24 use expanded 3-column grid (manifest pull).
APPENDIX_OID_MAP = {
    18: {"eyebrow": "g3eec5122801_0_723", "title": "g3eec5122801_0_718", "distance": "g3eec5122801_0_719", "equation": "g3eec5122801_0_720", "columns": "g3eec5122801_0_722"},
    19: {"eyebrow": "g3eec5122801_0_736", "title": "g3eec5122801_0_731", "distance": "g3eec5122801_0_732", "equation": "g3eec5122801_0_733", "columns": "g3eec5122801_0_735"},
    20: {"eyebrow": "g3eec5122801_0_793", "title": "g3eec5122801_0_743", "distance": "g3eec5122801_0_744", "equation": "g3eec5122801_0_791", "columns": "g3eec5122801_0_745"},
    21: {"eyebrow": "g3eec5122801_0_850", "title": "g3eec5122801_0_800", "distance": "g3eec5122801_0_801", "equation": "g3eec5122801_0_848", "columns": "g3eec5122801_0_802"},
    22: {"eyebrow": "g3eec5122801_0_907", "title": "g3eec5122801_0_857", "distance": "g3eec5122801_0_858", "equation": "g3eec5122801_0_905", "columns": "g3eec5122801_0_859"},
    23: {"eyebrow": "g3eec5122801_0_964", "title": "g3eec5122801_0_914", "distance": "g3eec5122801_0_915", "equation": "g3eec5122801_0_962", "columns": "g3eec5122801_0_916"},
    24: {"eyebrow": "g3eec5122801_0_1021", "title": "g3eec5122801_0_971", "distance": "g3eec5122801_0_972", "equation": "g3eec5122801_0_1019", "columns": "g3eec5122801_0_973"},
}

CORRIDOR_SLIDES = [
    ("uae-anantara-palm-bluewaters", 18, "palm", "APPENDIX · UAE"),
    ("uae-sirbaniyas-jebeldhanna", 19, "palm", "APPENDIX · UAE"),
    ("uae-minaalarab-palm", 20, "palm", "APPENDIX · UAE"),
    ("uae-palm-yasmarina", 21, "palm", "APPENDIX · UAE"),
    ("maldives-dharavandhoo-kihavah", 22, "maldives", "APPENDIX · MALDIVES"),
    ("thailand-aopo-layan", 23, "phuket", "APPENDIX · PHUKET"),
    ("bali-seminyak-uluwatu", 24, "bali", "APPENDIX · BALI"),
]

BG_FILES = {
    "palm": "econ-bg-uae-palm-n30.jpg",
    "maldives": "econ-bg-maldives-n30.jpg",
    "phuket": "econ-bg-thailand-andaman-n30.jpg",
    "bali": "econ-bg-bali-n30.jpg",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fmt_usd(n: int) -> str:
    return f"${n:,}"


def slide_page_oid(manifest: dict, idx: int) -> str:
    for s in manifest["slides"]:
        if s["index"] == idx:
            return s["slide_object_id"]
    raise KeyError(idx)


def ensure_assets() -> dict[str, str]:
    ASSET_DST.mkdir(parents=True, exist_ok=True)
    refs: dict[str, str] = {}
    registry = json.loads(REGISTRY.read_text())
    assets = registry.setdefault("assets", {})
    for slug, fname in BG_FILES.items():
        src = ASSET_SRC / fname
        dst = ASSET_DST / fname
        if src.is_file() and not dst.is_file():
            shutil.copy2(src, dst)
        rel = f"deck-studio/assets/minor-hotels/econ/{fname}"
        key = f"minor-econ-{slug}"
        url = f"{RAW}/{rel}"
        refs[slug] = url
        assets[key] = {
            "asset_key": key,
            "role": "econ_market_bg",
            "partner": DECK,
            "local_path": rel,
            "source_url": url,
            "status": "banked",
            "notes": "Minor hospitality appendix page-fill (wave-4 repull)",
        }
    registry.setdefault("deck_coverage", {}).setdefault(DECK, {})["econ_market_bg"] = "banked(4 markets)"
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n")
    return refs


def main() -> int:
    manifest = json.loads(MANIFEST.read_text())
    gold = json.loads(GOLD_ECON.read_text())
    by_id = {c["corridor_id"]: c for c in gold["corridors"]}
    urls = ensure_assets()

    appendix_cards = []
    appendix_backgrounds = []
    for corridor_id, slide_idx, market, eyebrow in CORRIDOR_SLIDES:
        row = by_id[corridor_id]
        oids = APPENDIX_OID_MAP[slide_idx]
        rev = row["revenue_per_vessel_yr"]
        opex = row["opex"]["total"]
        kept = row["ebitda_per_vessel_yr"]
        appendix_cards.append(
            {
                "slide_index": slide_idx,
                "page_object_id": slide_page_oid(manifest, slide_idx),
                "cluster_id": corridor_id,
                "market_slug": market,
                "object_ids": oids,
                "eyebrow": eyebrow,
                "title": row["label"],
                "distance_line": f"~{row['distance_nm']} nm",
                "equation_line": f"{fmt_usd(rev)} revenue   −   {fmt_usd(opex)} to run   =   ",
                "value_source": f"finance/model/minor-hotels-econ-gold-2026-06-25.json#{corridor_id}",
                "result_line_emphasis": "gold; kept figure gold @15pt",
                "co2_field": "co2_avoided_tonnes_year",
                "background_asset_ref": f"minor-econ-{market}",
            }
        )
        appendix_backgrounds.append(
            {
                "slide_index": slide_idx,
                "page_object_id": slide_page_oid(manifest, slide_idx),
                "asset_ref": f"minor-econ-{market}",
                "market_slug": market,
                "apply": "updatePageProperties.pageBackgroundFill.stretchedPictureFill.contentUrl",
                "binding": "PAGE-FILL (NOT navierBg_* element). LB-262.",
                "source_url": urls[market],
            }
        )

    binding = {
        "deck_key": DECK,
        "partner_id": DECK,
        "archetype": "operator-developer",
        "deck_type": "hospitality",
        "generated_at": utc_now(),
        "gold_deck_id": GOLD_DECK_ID,
        "_source_of_truth": (
            "Live gold deck 1p5Ntoa… was directly edited. Bindings repulled from cached slide-manifest "
            "+ minor-hotels-econ-gold-2026-06-25.json. DO NOT rebuild live deck from scratch."
        ),
        "sidecar_source": "handoff/minor-hotels/minor-hotels-economics-sidecar.json",
        "economics_frame": {
            "vessel_investment_usd": 1_000_000,
            "operator_framing": "Cost · Convenience · Comfort",
            "ladder": "NONE — hospitality decks DO NOT use a SOM/SAM/TAM/GMV ladder.",
            "slide2": "KPI-FREE, own distinct image",
        },
        "opex_six_line_order": [
            "energy_usd",
            "captain_crew_usd",
            "marina_overhead_usd",
            "maintenance_usd",
            "insurance_usd",
            "shore_power_berth_usd",
        ],
        "appendix_cards": appendix_cards,
        "appendix_backgrounds": appendix_backgrounds,
        "appendix_backgrounds_policy": {
            "binding": "PAGE-FILL via updatePageProperties.pageBackgroundFill",
            "status": "repulled_wave4",
            "manifest_source": str(MANIFEST.relative_to(REPO)),
            "auth_note": "Fresh Slides pull blocked (OAuth expired); OIDs from 2026-06-22 cached manifest.",
        },
        "qa_gates": {
            "deck_type": "hospitality",
            "no_ladder": True,
            "appendix_cards": len(appendix_cards),
            "appendix_page_fills": len(appendix_backgrounds),
        },
    }
    BINDING.write_text(json.dumps(binding, indent=2) + "\n")

    cfg_path = ROOT / f"decks/{DECK}/deck.config.json"
    cfg = json.loads(cfg_path.read_text())
    cfg["deck_id"] = GOLD_DECK_ID
    cfg["live_deck_url"] = f"https://docs.google.com/presentation/d/{GOLD_DECK_ID}/edit"
    cfg["deck_type"] = "hospitality"
    cfg["last_binding_repull_at"] = utc_now()
    cfg_path.write_text(json.dumps(cfg, indent=2) + "\n")

    print(f"repull: appendix_cards={len(appendix_cards)} backgrounds={len(appendix_backgrounds)}")
    print(f"wrote: {BINDING}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())