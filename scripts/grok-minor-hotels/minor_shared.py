#!/usr/bin/env python3
"""Shared constants and loaders for Minor Hotels seal/cascade lane."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HANDOFF = ROOT / "handoff/partner-map-model/minor-hotels-seal-2026-06-22"
INPUTS = HANDOFF / "inputs"
BINDS = INPUTS / "binds"
SEEDS = INPUTS / "seeds"
ECON = INPUTS / "economics"

PARTNER_ID = "minor-hotels"
PARTNER_SRC = ROOT / "partner-pitch/partners/minor-hotels.json"
PARTNER_DST = ROOT / "data-clean/partners/minor-hotels.json"
CORR_OUT = ROOT / "finance/recal/corridors-minor-hotels.json"
CROSSWALK_OUT = ROOT / "grok-routing-output/MINOR-ANCHOR-CITY-CROSSWALK.json"
SEAL_REPORT = ROOT / "grok-routing-output/minor-hotels-seal-report.json"
FBT_PATH = ROOT / "data-clean/FEATURES_BY_TYPE.json"
ROUTES_PATH = ROOT / "data-clean/ROUTES.json"
COUNTRY_REF = ROOT / "finance/model/country-reference.json"

# Gate A: bind registry_key → atlas render city_id (country-suffixed canonical)
ANCHOR_CROSSWALK: dict[str, str] = {
    "dubai-uae": "dubai-uae",
    "dubai-uae__palm-jumeirah-crescent-inner": "dubai-uae__palm-jumeirah-crescent-inner",
    "dubai-uae__world-islands-heart-of-europe": "dubai-uae__world-islands-heart-of-europe",
    "phuket-phang-nga-thailand": "phuket-phang-nga-thailand",
    "bali-indonesia": "bali-indonesia",
    "bangkok-thailand": "bangkok-thailand",
    "koh-samui-thailand": "koh-samui-thailand",
    "male-maldives": "male-maldives",
    "abu-dhabi-uae": "abu-dhabi-uae",
    "ras-al-khaimah-uae": "ras-al-khaimah-uae",
    "gold-coast-australia": "gold-coast-australia",
    "algarve": "algarve",
    "porto": "porto",
    "gulf-of-thailand-upper-thailand": "gulf-of-thailand-upper-thailand",
}

HELD_PROPERTIES = {
    "Anantara Villa Padierna Marbella",
    "Elewana AfroChic Diani Beach",
}

TIER1_CLUSTERS = {
    "phuket-phang-nga": {
        "market_key": "phuket",
        "anchor_city": "phuket-phang-nga-thailand",
        "economics_file": "minor-hotels-phuket-flagship-economics-DRAFT.json",
        "status": "economics_ready",
    },
    "bali": {
        "market_key": "bali",
        "anchor_city": "bali-indonesia",
        "economics_file": "minor-hotels-bali-flagship-economics-DRAFT.json",
        "status": "economics_ready",
    },
    "palm-jumeirah": {
        "market_key": "palm-jumeirah",
        "anchor_city": "dubai-uae__palm-jumeirah-crescent-inner",
        "economics_file": "minor-hotels-palm-jumeirah-flagship-economics-DRAFT.json",
        "status": "economics_ready",
    },
}

# Representative captive corridors per Tier-1 cluster (route_id from parent markets)
TIER1_CORRIDOR_ROUTES: dict[str, list[str]] = {
    "phuket": [
        "rn-830bd4d377ca",  # Rassada → Koh Yao Yai (A)
        "rn-b28ac4ca3d14",  # Ao Po → Layan (A)
        "rn-b1313beb0eaa",  # Koh Yao → Khao Lak (B)
        "gcn-cbc11a6947-shared",  # Phang Nga excursion (C)
        "gcn-9ae16d4c34-shared",  # Phi Phi excursion (C)
        "gcn-e927fe8958-shared",  # Krabi corridor (C)
    ],
    "bali": [
        "rn-c256a044c8be",  # Benoa → Uluwatu (A)
        "rn-488fcf2617fe",  # Sanur → Seminyak coast (A)
        "gcn-3d7809869d-shared",  # Nusa Penida (C)
    ],
    "palm-jumeirah": [
        "rn-b0d5e6498ee4",  # Dubai Harbour → Anantara (A)
        "rn-42aa1791bb60",  # Dubai Harbour → Palm Marina West (C)
        "rn-b49c885ed913",  # Palm Marina West → Atlantis (C)
    ],
}

COUNTRY_PREFLIGHT = {
    "Australia": {"cost_index": 0.85, "captain_usd_yr": 42000, "energy_usd_kwh": 0.18},
    "Brazil": {"cost_index": 0.38, "captain_usd_yr": 14000, "energy_usd_kwh": 0.09},
    "Sri Lanka": {"cost_index": 0.32, "captain_usd_yr": 10000, "energy_usd_kwh": 0.08},
    "Slovenia": {"cost_index": 0.55, "captain_usd_yr": 28000, "energy_usd_kwh": 0.14},
}


def slug(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (s or "").lower()).strip("-")
    return s[:80] or "unknown"


def load_json(path: Path) -> dict | list:
    return json.loads(path.read_text())


def load_binds() -> list[dict]:
    rows: list[dict] = []
    for path in sorted(BINDS.glob("minor-hotels-*-bind.json")):
        doc = load_json(path)
        for key in ("bound", "attach", "pipeline"):
            for row in doc.get(key) or []:
                row = dict(row)
                row["_bind_source"] = path.name
                row["_bind_bucket"] = key
                rows.append(row)
    return rows


def load_seeds() -> list[dict]:
    out: list[dict] = []
    for path in sorted(SEEDS.glob("*.json")):
        doc = load_json(path)
        if isinstance(doc, dict) and doc.get("registry_key"):
            out.append({**doc, "_seed_file": path.name})
        elif isinstance(doc, dict) and doc.get("markets"):
            for m in doc["markets"]:
                out.append({**m, "_seed_file": path.name})
        elif isinstance(doc, dict) and doc.get("seeds"):
            for s in doc["seeds"]:
                out.append({**s, "_seed_file": path.name})
    return out


def load_economics_floor(cluster_key: str) -> dict:
    spec = TIER1_CLUSTERS[cluster_key]
    return load_json(ECON / spec["economics_file"])


def property_poi_id(name: str) -> str:
    return f"minor-hotels__{slug(name)}"