#!/usr/bin/env python3
"""Bolt wave-2: full 23-slide partner-ready deck (plates + editplan + apply + QA)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDERS = ROOT / "builders"
sys.path.insert(0, str(BUILDERS))

from deck_bolt_pilot import (  # noqa: E402
    LEAK_DENYLIST,
    apply_plan,
    collect_slide_text,
    drift_gate,
    export_thumbnails,
    fmt_usd,
    golden_element,
    golden_slide_oid,
    leak_scan,
    load_json,
    slides_service,
    utc_now,
    write_json,
)
from deck_edit_ops import econ_value_replace_ops, image_replace_op, text_replace_ops  # noqa: E402

GOLD_ID = "18yDAgO0Sj9PJlgf6paxtgni8Pk1xRAmNwE2TD_NCdSs"

WAVE2_LEAK_DENYLIST = LEAK_DENYLIST + [
    "Southeast Asia",
    "SEA network",
    "Koh Samui",
    "Koh Phangan",
    "Manila",
    "Boracay",
    "Langkawi",
    "Penghu",
    "Taiwan",
    "Nusa Penida",
    "Phi Phi",
    "Phang Nga",
    "Marina Bay",
    "Sentosa",
    "Benoa",
    "Gili",
    "Lombok",
    "Corregidor",
    "Caticlan",
    "Kuah",
    "Donggang",
    "$200,499",
    "$206,958",
    "$301,686",
    "$235,180",
    "$176,352",
    "$229,897",
    "$303,269",
    "$480,870",
    "$398,301",
    "$82,569",
    "Grab platform",
    "Grab marine",
    "Grab Atlas",
    "x Grab",
]

# Economics corridor bindings (mid scenario from agg-bolt.json)
ECON_BINDINGS: dict[int, dict] = {
    7: {
        "corridor": "Athens -> Hydra (Saronic)",
        "market_label": "GREECE",
        "title_market": "Greece",
        "route_line": "Athens → Hydra (Saronic)  ·  ~30 nm  ·  N30 Pioneer II (8 seats)",
        "bg_registry": "econ-greece-athens-hydra",
        "bg_oid": "navierBg_s23",
    },
    8: {
        "corridor": "Split -> Hvar",
        "market_label": "CROATIA",
        "header_market": "WHAT ONE BOAT EARNS · CRO",
        "title": "Croatia: profit from year one",
        "route_line": "Split → Hvar  ·  ~20 nm  ·  N30 Pioneer II (8 seats)",
        "bg_registry": "econ-croatia-split-hvar",
        "bg_oid": "navierBg_s24",
    },
    9: {
        "corridor": "Nice -> Monaco",
        "market_label": "RIVIERA",
        "header_market": "WHAT ONE BOAT EARNS · AZUR",
        "title": "Riviera: profit from year one",
        "route_line": "Nice → Monaco  ·  ~7 nm  ·  N30 Pioneer II (8 seats)",
        "bg_registry": "econ-cote-azur-nice-monaco",
        "bg_oid": "navierBg_s25",
    },
    19: {
        "corridor": "Sorrento -> Capri",
        "market_label": "ITALY",
        "title_market": "Italy",
        "route_line": "Sorrento → Capri  ·  ~17 nm  ·  N30 Pioneer II (8 seats)",
        "bg_registry": "econ-italy-sorrento-capri",
        "bg_oid": "navierBg_s35",
    },
    20: {
        "corridor": "Dubai Harbour Marina -> Bluewaters Marina",
        "market_label": "UAE",
        "title_market": "UAE",
        "route_line": "Dubai Harbour → Bluewaters  ·  ~3 nm  ·  N30 Pioneer II (8 seats)",
        "bg_registry": "econ-uae-dubai-harbour",
        "bg_oid": "navierBg_s36",
    },
    21: {
        "corridor": "Jeddah Corniche -> Jeddah Central (PIF waterfront)",
        "market_label": "JEDDAH",
        "header_market": "WHAT ONE BOAT EARNS · JEDDAH",
        "title": "Jeddah: profitable from year one",
        "route_line": "Jeddah Corniche → Jeddah Central  ·  ~2 nm  ·  N30 Pioneer II (8 seats)",
        "bg_registry": "econ-ksa-jeddah",
        "bg_oid": "navierBg_s37",
    },
    22: {
        "corridor": "Mykonos -> Paros",
        "market_label": "GREECE",
        "title_market": "Cyclades",
        "route_line": "Mykonos → Paros  ·  ~25 nm  ·  N30 Pioneer II (8 seats)",
        "bg_registry": "econ-greece-mykonos-paros",
        "bg_oid": "navierBg_s38",
    },
    23: {
        "corridor": "The Red Sea -> AMAALA (Triple Bay)",
        "market_label": "RED SEA",
        "title": "Red Sea: profit from year one",
        "route_line": "Red Sea → AMAALA  ·  ~45 nm  ·  N30 Pioneer II (8 seats)",
        "bg_registry": "econ-ksa-redsea-amaala",
        "bg_oid": "navierBg_s39",
    },
}

# Narrative text replacements: (slide_object_id, target_oid) -> text
NARRATIVE_TEXT: dict[tuple[str, str], str] = {
    # Slide 1 cover (refresh if still SEA residue)
    ("p1", "p1_i8"): "The water network for Europe",
    ("p1", "p1_i9"): "A premium, zero-emission water layer — in your app, on your wallet.",
    # Slide 3 region overview
    ("g3eec5122801_0_0", "g3eec5122801_0_2"): "THE REGION",
    ("g3eec5122801_0_0", "g3eec5122801_0_4"): "Europe & the Gulf: water-bound mobility markets",
    ("g3eec5122801_0_0", "g3eec5122801_0_14"): "Bolt already owns the demand from the Aegean to the Gulf; the water leg books door-to-door beside every Bolt car.",
    ("g3eec5122801_0_0", "g3eec5122801_0_6"): "6",
    ("g3eec5122801_0_0", "g3eec5122801_0_7"): "water-bound clusters in Bolt's current proposal scope",
    ("g3eec5122801_0_0", "g3eec5122801_0_10"): "$996M",
    ("g3eec5122801_0_0", "g3eec5122801_0_11"): "premium sea-transfer spend on Bolt corridors today, per year",
    ("g3eec5122801_0_0", "g3eec5122801_0_15"): "1,000+",
    ("g3eec5122801_0_0", "g3eec5122801_0_16"): "vessels at full network maturity across mapped corridors",
    ("g3eec5122801_0_0", "g3eec5122801_0_18"): "$8.8B",
    ("g3eec5122801_0_0", "g3eec5122801_0_19"): "marine-transfer TAM (induced market) · model band $4.5–15.8B, mid $8.8B",
    # Slide 4 Greece example market
    ("g3eec5122801_0_106", "g3eec5122801_0_110"): "Greece — the recommended beachhead",
    ("g3eec5122801_0_106", "g3eec5122801_0_111"): "Bolt's deepest island demand and longest season — replacing slow diesel ferries.",
    ("g3eec5122801_0_106", "g3eec5122801_0_114"): "▸  Athens → Hydra (Saronic)\n      ~30 nm · ~45-min foiling run\n▸  Piraeus → Aegina\n      ~10 nm · commuter island hop",
    # Slide 5 Croatia
    ("g3eec5122801_0_201", "g3eec5122801_0_205"): "Croatia — the Dalmatian island chain",
    ("g3eec5122801_0_201", "g3eec5122801_0_206"): "High-volume Adriatic island hops — Split, Hvar, Brač and Korčula on one network.",
    ("g3eec5122801_0_201", "g3eec5122801_0_209"): "▸  Split → Hvar\n      ~20 nm · the everyday island hop\n▸  Split → Brač (Bol)\n      ~12 nm · beach-resort crossing",
    # Slide 6 Riviera
    ("g3eec5122801_0_296", "g3eec5122801_0_300"): "Riviera — Nice to Monaco by water",
    ("g3eec5122801_0_296", "g3eec5122801_0_304"): "Premium corporate and leisure demand — skip Corniche traffic with a silent foiling run.",
    ("g3eec5122801_0_296", "g3eec5122801_0_301"): "▸  Nice → Monaco\n      ~7 nm · the Corniche bypass\n▸  Nice Airport → Monaco\n      ~7 nm · airport transfer",
    # Slide 10 TAM
    ("g3eec5122801_0_562", "g3eec5122801_0_565"): "A new multi-billion-dollar vertical across Europe",
    ("g3eec5122801_0_562", "g3eec5122801_0_567"): "Read it bottom-up: the fare a Navier boat collects today, the market a faster product unlocks — then the whole journey a super-app monetizes around every crossing.",
    ("g3eec5122801_0_562", "g3eec5122801_0_570"): "$507M",
    ("g3eec5122801_0_562", "g3eec5122801_0_571"): "SOM — Navier fare, Bolt network, today's trips, 10% capture",
    ("g3eec5122801_0_562", "g3eec5122801_0_574"): "$2.2B",
    ("g3eec5122801_0_562", "g3eec5122801_0_575"): "SAM — faster, quieter boats grow the market; 25% capture at maturity",
    ("g3eec5122801_0_562", "g3eec5122801_0_578"): "$8.8B",
    ("g3eec5122801_0_562", "g3eec5122801_0_579"): "TAM — the entire induced marine-transfer market (≈ 4× SAM; band $4.5–15.8B)",
    ("g3eec5122801_0_562", "g3eec5122801_0_582"): "$6.6B",
    ("g3eec5122801_0_562", "g3eec5122801_0_583"): "Journey GMV — add food + stays + experiences to every crossing (≈ 3× TAM)",
    ("g3eec5122801_0_562", "g3eec5122801_0_586"): "$1.2B",
    ("g3eec5122801_0_562", "g3eec5122801_0_587"): "Bolt platform revenue on Navier — 18% × Navier-corridor Journey GMV (ceiling on full network)",
    # Slide 11 partner roles
    ("g3ea5e0fb254_4_357", "g3ea5e0fb254_4_361"): "You bring the demand. We operate the water.",
    ("g3ea5e0fb254_4_357", "g3ea5e0fb254_4_362"): "▸  Bolt — demand, the app, the wallet and the brand.\n▸  Navier — vessels, crew, maintenance, certification and the network playbook.\n▸  Together — a premium foiling water tier from the Aegean to the Gulf.",
    # Slide 12 ask
    ("g3ea5e0fb254_4_444", "g3ea5e0fb254_4_447"): "1.  Working session — walk through the presentation and Navier atlas. \n2.  Vessel demo — a live foiling run on a pilot corridor. \n3.  Pilot MOU — Greece beachhead, three corridors, 12-month launch window.",
    # Slide 13 close
    ("g3ea5e0fb254_4_330", "g3ea5e0fb254_4_330"): "Explore the Bolt marine network",
    ("g3ea5e0fb254_4_331", "g3ea5e0fb254_4_331"): "Open the Navier × Bolt Atlas, pick the first corridor, and let's discover a new foiling water tier across Europe.",
    # Slide 14 Italy backup market
    ("g3eec5122801_0_677", "g3eec5122801_0_679"): "Italy — Amalfi, Capri & the lagoon",
    ("g3eec5122801_0_677", "g3eec5122801_0_680"): "Amalfi Coast day-trips, Capri crossings and Venice lagoon hops on one supply standard.",
    ("g3eec5122801_0_677", "g3eec5122801_0_683"): "▸  Sorrento → Capri\n      ~17 nm · the Amalfi day-trip\n▸  Naples → Capri\n      ~22 nm · bay crossing",
    # Slide 15 UAE
    ("g3eec5122801_0_690", "g3eec5122801_0_692"): "UAE — Dubai & Abu Dhabi by water",
    ("g3eec5122801_0_690", "g3eec5122801_0_693"): "Premium harbour-to-harbour demand — no Sheikh Zayed Road required.",
    ("g3eec5122801_0_690", "g3eec5122801_0_696"): "▸  Dubai Harbour → Bluewaters\n      ~3 nm · marina hop\n▸  Dubai Marina → Downtown Creek\n      ~2 nm · cross-city water leg",
    # Slide 16 Saudi
    ("g3eec5122801_0_703", "g3eec5122801_0_705"): "Saudi — Jeddah & the Red Sea",
    ("g3eec5122801_0_703", "g3eec5122801_0_706"): "PIF waterfront ambition meets water mobility",
    ("g3eec5122801_0_703", "g3eec5122801_0_709"): "▸  Jeddah Corniche → Jeddah Central\n      ~2 nm · waterfront hop\n▸  Red Sea → AMAALA\n      ~45 nm · resort corridor",
    # Slide 17 Greece Cyclades
    ("g3eec5122801_0_716", "g3eec5122801_0_718"): "Greece — Cyclades island network",
    ("g3eec5122801_0_716", "g3eec5122801_0_719"): "Mykonos, Paros, Naxos and Santorini — the highest-volume Aegean hops.",
    ("g3eec5122801_0_716", "g3eec5122801_0_722"): "▸  Mykonos → Paros\n      ~25 nm · inter-island hop\n▸  Mykonos → Naxos\n      ~20 nm · Cyclades crossing",
    # Slide 18 Croatia Dubrovnik
    ("g3eec5122801_0_729", "g3eec5122801_0_731"): "Croatia — Dubrovnik & the islands",
    ("g3eec5122801_0_729", "g3eec5122801_0_732"): "Elaphiti Islands, Korčula and Mljet — premium Adriatic excursions.",
    ("g3eec5122801_0_729", "g3eec5122801_0_735"): "▸  Dubrovnik → Elaphiti Islands\n      ~8 nm · island excursion\n▸  Dubrovnik → Korčula\n      ~55 nm · south Adriatic",
}

IMAGE_BINDINGS: list[dict] = [
    {"registry": "bolt-cover-hero", "slide_oid": "p1", "target_oid": "p1_i2", "method": "CENTER_CROP"},
    {"registry": "bolt-value-prop-bg", "slide_oid": "g3f139a0b6ec_0_0", "target_oid": "g3f139a0b6ec_0_1", "method": "CENTER_CROP"},
    {"registry": "bolt-tam-bg", "slide_oid": "g3eec5122801_0_562", "target_oid": "navierBg_s26", "method": "CENTER_CROP"},
    {"registry": "bolt-partner-roles-bg", "slide_oid": "g3ea5e0fb254_4_357", "target_oid": "g3ea5e0fb254_4_358", "method": "CENTER_CROP"},
    {"registry": "bolt-partner-logo", "slide_oid": "p1", "target_oid": "p1_i5", "method": "CENTER_INSIDE"},
    # Example market slide images
    {"registry": "econ-greece-athens-hydra", "slide_oid": "g3eec5122801_0_106", "target_oid": "g3eec5122801_0_107", "method": "CENTER_CROP"},
    {"registry": "econ-croatia-split-hvar", "slide_oid": "g3eec5122801_0_201", "target_oid": "g3eec5122801_0_202", "method": "CENTER_CROP"},
    {"registry": "econ-cote-azur-nice-monaco", "slide_oid": "g3eec5122801_0_296", "target_oid": "g3eec5122801_0_297", "method": "CENTER_CROP"},
    {"registry": "econ-italy-sorrento-capri", "slide_oid": "g3eec5122801_0_677", "target_oid": "g3eec5122801_0_676", "method": "CENTER_CROP"},
    {"registry": "econ-uae-dubai-harbour", "slide_oid": "g3eec5122801_0_690", "target_oid": "g3eec5122801_0_689", "method": "CENTER_CROP"},
    {"registry": "econ-ksa-jeddah", "slide_oid": "g3eec5122801_0_703", "target_oid": "g3eec5122801_0_702", "method": "CENTER_CROP"},
    {"registry": "econ-greece-mykonos-paros", "slide_oid": "g3eec5122801_0_716", "target_oid": "g3eec5122801_0_715", "method": "CENTER_CROP"},
    {"registry": "econ-croatia-dubrovnik", "slide_oid": "g3eec5122801_0_729", "target_oid": "g3eec5122801_0_728", "method": "CENTER_CROP"},
]


def element_or_fallback(golden: dict, oid: str, *, fallback_oid: str = "g3eec5122801_0_394") -> dict:
    el = golden_element(golden, oid)
    if el:
        return el
    fb = golden_element(golden, fallback_oid)
    if not fb:
        raise KeyError(f"No golden element for {oid}")
    return {**fb, "oid": oid, "char_budget": max(fb.get("char_budget", 12), 16)}


def load_agg_rows() -> list[dict]:
    agg = load_json(ROOT.parent / "finance/recal/agg-bolt.json")
    return agg.get("rows", [])


def find_corridor_mid(corridor: str) -> dict | None:
    for row in load_agg_rows():
        if row.get("corridor") == corridor:
            mid = row.get("mid", {})
            if mid.get("revenue_per_boat_yr"):
                return mid
    return None


def econ_value_map_from_mid(econ: dict) -> dict[str, str]:
    cc = econ["cost_components"]
    rev = econ["revenue_per_boat_yr"]
    opex = econ["annual_opex"]
    profit = econ["ebitda_per_boat_yr"]
    margin_pct = int(round(econ["margin"] * 100))
    payback = f"{econ['payback_years']:.1f} yrs"
    return {
        "trips_per_day": str(econ["trips_per_day"]),
        "operating_days": str(econ["assumptions"]["operating_days_yr"]),
        "revenue_legs": f"{int(econ['assumptions']['revenue_leg_pct'] * 100)}%",
        "seats_per_trip": str(econ["pax_per_trip"]),
        "paid_seats_yr": f"{int(econ['pax_per_year']):,}",
        "premium_fare": f"{fmt_usd(econ['navier_fare_usd'])} / seat",
        "revenue_per_boat": fmt_usd(rev),
        "opex_energy": fmt_usd(cc["energy_usd_yr"]),
        "opex_crew": fmt_usd(cc["crew_usd_yr"]),
        "opex_marina": fmt_usd(cc["marina_overhead_usd_yr"]),
        "opex_maintenance": fmt_usd(cc["maintenance_usd_yr"]),
        "opex_insurance": fmt_usd(cc["insurance_usd_yr"]),
        "opex_charging_berth": fmt_usd(cc["charging_berth_usd_yr"]),
        "opex_total": fmt_usd(opex),
        "result_profit": fmt_usd(profit),
        "result_margin": f"{margin_pct}%",
        "result_capex": "$600,000",
        "result_payback": payback,
        "result_co2": f"{econ['co2_saved_t_per_boat_yr']:.1f} t",
    }


HOLD_SUMMARY = "Economics pending corridor validation"
HOLD_ROUTE = "Representative corridor pending published Bolt economics"
HOLD_HEADER = "WHAT ONE BOAT EARNS · HOLD"
HOLD_TITLE = "Unit economics: pending validation"


def build_econ_slide_ops(
    golden: dict,
    binding_slide: dict,
    spec: dict,
    *,
    asset_urls: dict[str, str],
) -> list[dict]:
    slide_index = binding_slide["slide_index"]
    slide_oid = binding_slide["slide_object_id"]
    fields = binding_slide["fields"]
    ops: list[dict] = []

    econ = find_corridor_mid(spec["corridor"])
    if econ:
        rev = econ["revenue_per_boat_yr"]
        opex = econ["annual_opex"]
        profit = econ["ebitda_per_boat_yr"]
        margin_pct = int(round(econ["margin"] * 100))
        payback = f"{econ['payback_years']:.1f} yrs"
        text_map = {
            "header_market": spec.get("header_market", f"WHAT ONE BOAT EARNS · {spec['market_label']}"),
            "title": spec.get("title", f"{spec.get('title_market', spec['market_label'].title())}: profitable from year one"),
            "route_line": spec["route_line"],
            "summary_line": (
                f"{fmt_usd(rev)} revenue  −  {fmt_usd(opex)} run cost  =  "
                f"{fmt_usd(profit)} profit / boat·yr  ·  {margin_pct}% margin  ·  {payback}"
            ),
        }
        value_map = econ_value_map_from_mid(econ)
        source = f"finance/recal/agg-bolt.json mid {spec['corridor']}"
    else:
        text_map = {
            "header_market": HOLD_HEADER,
            "title": HOLD_TITLE,
            "route_line": HOLD_ROUTE,
            "summary_line": HOLD_SUMMARY,
        }
        value_map = {}
        source = "wave2 explicit hold — no mid economics in agg-bolt.json"

    for field_key, text in text_map.items():
        oid = fields[field_key]["object_id"]
        el = element_or_fallback(golden, oid)
        ops.extend(
            text_replace_ops(
                slide_oid,
                oid,
                text,
                el,
                op_prefix=f"bolt-econ{slide_index}-{field_key}",
                source_pointer=source,
            )
        )

    for field_key, text in value_map.items():
        oid = fields[field_key]["value_object_id"]
        ops.extend(
            econ_value_replace_ops(
                slide_oid,
                oid,
                text,
                op_prefix=f"bolt-econ{slide_index}-val-{field_key}",
                source_pointer=source,
            )
        )

    bg_key = spec["bg_registry"]
    if asset_urls.get(bg_key):
        ops.append(
            image_replace_op(
                slide_oid,
                spec["bg_oid"],
                asset_urls[bg_key],
                op_key=f"bolt-econ{slide_index}-bg",
                source_pointer=f"ASSET-REGISTRY {bg_key}",
                method="CENTER_CROP",
            )
        )
    return ops


def register_wave2_assets() -> dict[str, str]:
    registry_path = ROOT / "assets/ASSET-REGISTRY.json"
    registry = load_json(registry_path)
    assets = registry.setdefault("assets", {})
    now = utc_now()

    asset_defs = {
        "bolt-cover-hero": {
            "role": "cover_hero",
            "scope": "deck",
            "partner": "bolt",
            "market_slug": "athens-saronic-greece",
            "local_path": "assets/backgrounds/markets/greece/greece-aegean-v1-composited.png",
            "provenance": "n30_composite:grok_gen_greece_aegean_raw",
            "used_by": [{"deck": "bolt", "slide_index": 1, "slide_object_id": "p1", "target_object_id": "p1_i2"}],
        },
        "bolt-value-prop-bg": {
            "role": "value_prop_bg",
            "scope": "deck",
            "partner": "bolt",
            "local_path": "assets/backgrounds/decks/bolt/bolt-value-prop-v1-composited.png",
            "provenance": "n30_composite:grok_gen_bolt_value_prop_raw",
            "used_by": [{"deck": "bolt", "slide_index": 2, "slide_object_id": "g3f139a0b6ec_0_0", "target_object_id": "g3f139a0b6ec_0_1"}],
        },
        "bolt-tam-bg": {
            "role": "tam_bg",
            "scope": "deck",
            "partner": "bolt",
            "local_path": "assets/backgrounds/decks/bolt/bolt-tam-v1-composited.png",
            "provenance": "n30_composite:grok_gen_bolt_tam_raw",
            "used_by": [{"deck": "bolt", "slide_index": 10, "slide_object_id": "g3eec5122801_0_562", "target_object_id": "navierBg_s26"}],
        },
        "bolt-partner-roles-bg": {
            "role": "partner_roles_bg",
            "scope": "deck",
            "partner": "bolt",
            "local_path": "assets/backgrounds/decks/bolt/bolt-partner-roles-v1-composited.png",
            "provenance": "n30_composite:grok_gen_bolt_partner_roles_raw",
            "used_by": [{"deck": "bolt", "slide_index": 11, "slide_object_id": "g3ea5e0fb254_4_357", "target_object_id": "g3ea5e0fb254_4_358"}],
        },
        "econ-greece-athens-hydra": {
            "role": "econ_market_bg",
            "scope": "market",
            "market_slug": "athens-saronic-greece",
            "atlas_city_id": "athens-saronic-greece",
            "local_path": "assets/backgrounds/markets/greece/greece-aegean-v1-composited.png",
            "provenance": "n30_composite:grok_gen_greece_aegean_raw",
        },
        "econ-croatia-split-hvar": {
            "role": "econ_market_bg",
            "scope": "market",
            "market_slug": "split-croatia",
            "atlas_city_id": "split-croatia",
            "local_path": "assets/backgrounds/markets/croatia/croatia-dalmatian-v1-composited.png",
            "provenance": "n30_composite:grok_gen_croatia_dalmatian_raw",
        },
        "econ-cote-azur-nice-monaco": {
            "role": "econ_market_bg",
            "scope": "market",
            "market_slug": "cote-dazur-france",
            "atlas_city_id": "cote-dazur-france",
            "local_path": "assets/backgrounds/markets/cote-dazur/cote-azur-v1-composited.png",
            "provenance": "n30_composite:grok_gen_cote_azur_raw",
        },
        "econ-italy-sorrento-capri": {
            "role": "econ_market_bg",
            "scope": "market",
            "market_slug": "sorrento-italy",
            "local_path": "assets/backgrounds/markets/italy-amalfi/italy-amalfi-v1-composited.png",
            "provenance": "n30_composite:grok_gen_italy_amalfi_raw",
        },
        "econ-uae-dubai-harbour": {
            "role": "econ_market_bg",
            "scope": "market",
            "market_slug": "dubai-uae",
            "atlas_city_id": "dubai-uae",
            "local_path": "assets/backgrounds/markets/uae/uae-dubai-v1-composited.png",
            "provenance": "n30_composite:grok_gen_uae_dubai_raw",
        },
        "econ-ksa-jeddah": {
            "role": "econ_market_bg",
            "scope": "market",
            "market_slug": "jeddah-ksa",
            "local_path": "assets/backgrounds/markets/ksa/ksa-jeddah-v1-composited.png",
            "provenance": "n30_composite:grok_gen_ksa_jeddah_raw",
        },
        "econ-greece-mykonos-paros": {
            "role": "econ_market_bg",
            "scope": "market",
            "market_slug": "mykonos-greece",
            "local_path": "assets/backgrounds/markets/greece/greece-cyclades-v1-composited.png",
            "provenance": "n30_composite:grok_gen_greece_cyclades_raw",
        },
        "econ-croatia-dubrovnik": {
            "role": "econ_market_bg",
            "scope": "market",
            "market_slug": "dubrovnik-croatia",
            "local_path": "assets/backgrounds/markets/croatia/croatia-dubrovnik-v1-composited.png",
            "provenance": "n30_composite:grok_gen_croatia_dubrovnik_raw",
        },
        "econ-ksa-redsea-amaala": {
            "role": "econ_market_bg",
            "scope": "market",
            "market_slug": "red-sea-ksa",
            "local_path": "assets/backgrounds/markets/ksa/ksa-redsea-v1-composited.png",
            "provenance": "n30_composite:grok_gen_ksa_redsea_raw",
        },
    }

    for key, spec in asset_defs.items():
        prev = assets.get(key, {})
        assets[key] = {
            **spec,
            "status": "checked_in",
            "license": "navier-internal",
            "reproducible": True,
            "composited": True,
            "captured_at": now,
            "drive_file_id": prev.get("drive_file_id"),
            "source_url": prev.get("source_url"),
            "notes": spec.get("notes", f"Wave-2 N30 composite — {key}"),
        }

    # Mark legacy mislabeled assets deprecated (superseded by wave-2 keys above)
    for legacy_key in ("econ-athens-saronic-greece", "econ-uae-the-world-islands"):
        if legacy_key in assets:
            assets[legacy_key]["status"] = "deprecated_invalid_source"
            assets[legacy_key]["notes"] = (assets[legacy_key].get("notes", "") + " Superseded by wave-2 plates.").strip()

    registry.setdefault("deck_coverage", {}).setdefault("bolt", {})["roles"] = {
        "cover_hero": "checked_in",
        "navier_logo": "checked_in(shared)",
        "partner_logo": "checked_in",
        "value_prop_bg": "checked_in",
        "tam_bg": "checked_in",
        "partner_roles_bg": "checked_in",
        "econ_market_bg": "checked_in(8 corridors)",
    }
    registry["deck_coverage"]["bolt"]["status"] = "wave2_indexed"
    write_json(registry_path, registry)

    sys.path.insert(0, str(BUILDERS))
    from deck_autonomy_sync import publish_assets_to_drive  # type: ignore

    publish_assets_to_drive(registry_path)
    registry = load_json(registry_path)
    urls: dict[str, str] = {}
    for key in asset_defs:
        asset = registry["assets"][key]
        if not asset.get("source_url"):
            raise SystemExit(f"Asset {key} missing source_url after publish")
        urls[key] = asset["source_url"]
    if registry["assets"].get("bolt-partner-logo", {}).get("source_url"):
        urls["bolt-partner-logo"] = registry["assets"]["bolt-partner-logo"]["source_url"]
    write_json(registry_path, registry)
    return urls


def build_wave2_editplan(presentation_id: str, asset_urls: dict[str, str]) -> dict:
    golden = load_json(ROOT / "decks/grab/golden-template-map.json")
    binding = load_json(ROOT / "decks/bolt/economics-binding.json")
    ops: list[dict] = []

    for (slide_oid, target_oid), text in NARRATIVE_TEXT.items():
        el = element_or_fallback(golden, target_oid)
        ops.extend(
            text_replace_ops(
                slide_oid,
                target_oid,
                text,
                el,
                op_prefix=f"bolt-wave2-{target_oid}",
                source_pointer="deck_bolt_wave2.NARRATIVE_TEXT + growth-bolt.json",
            )
        )

    for bind in IMAGE_BINDINGS:
        url = asset_urls.get(bind["registry"])
        if not url:
            continue
        ops.append(
            image_replace_op(
                bind["slide_oid"],
                bind["target_oid"],
                url,
                op_key=f"bolt-wave2-img-{bind['registry']}",
                source_pointer=f"ASSET-REGISTRY {bind['registry']}",
                method=bind.get("method", "CENTER_CROP"),
            )
        )

    for slide_binding in binding["economics_slides"]:
        idx = slide_binding["slide_index"]
        spec = ECON_BINDINGS.get(idx)
        if not spec:
            continue
        ops.extend(build_econ_slide_ops(golden, slide_binding, spec, asset_urls=asset_urls))

    plan = {
        "deck_key": "bolt",
        "partner_slug": "bolt",
        "presentation_id": presentation_id,
        "gold_template_id": GOLD_ID,
        "deprecated_sandbox_id": "1sQNF5P3OjhAlSh917yO6If1OPBGnwOBvrBzGXcYZh4c",
        "mode": "slides_api_batch_update",
        "status": "ready_to_apply",
        "wave": "wave-2",
        "request_summary": (
            "Bolt wave-2: full 23-slide bind — EU/Gulf narrative + 8 corridor economics "
            "+ N30 market plates + zero Grab/SEA leak"
        ),
        "safety": {
            "no_pptx_roundtrip": True,
            "no_full_deck_replace": True,
            "preserve_object_ids": True,
            "human_review_required_for_external_send": True,
        },
        "qa_gates": [
            "drift_gate",
            "leak_denylist",
            "style_reset_scan",
            "char_budget_scan",
            "image_inheritance_scan",
            "render_thumbnails",
        ],
        "leak_denylist": WAVE2_LEAK_DENYLIST,
        "operations": ops,
        "created_at": utc_now(),
        "applied_at": None,
    }
    return plan


def run_wave2_qa(presentation_id: str, plan: dict) -> dict:
    drift = drift_gate(presentation_id, plan)
    leak_full = leak_scan(presentation_id, plan.get("leak_denylist", WAVE2_LEAK_DENYLIST))
    thumbs = export_thumbnails(
        presentation_id, ROOT / "decks/bolt/qa-receipts/thumbnails-wave2", max_slides=23
    )
    status = "pass" if drift["pass"] and leak_full["pass"] and thumbs else "fail"
    receipt = {
        "deck_key": "bolt",
        "presentation_id": presentation_id,
        "wave": "wave-2",
        "status": status,
        "generated_at": utc_now(),
        "checks": [
            {"name": "drift_gate", "status": "pass" if drift["pass"] else "fail", "details": json.dumps(drift)},
            {
                "name": "leak_denylist_full_deck",
                "status": "pass" if leak_full["pass"] else "fail",
                "details": json.dumps(leak_full),
            },
            {
                "name": "render_thumbnails",
                "status": "pass" if thumbs else "fail",
                "details": f"{len(thumbs)} thumbnails",
            },
        ],
        "gates": {"drift_gate": drift, "leak_denylist_full_deck": leak_full, "thumbnails": thumbs},
        "operation_count": len(plan.get("operations", [])),
        "live_deck_url": f"https://docs.google.com/presentation/d/{presentation_id}/edit",
        "pilot_scope": "full 23-slide wave-2 partner-ready bind",
    }
    write_json(ROOT / "decks/bolt/qa-receipts/bolt-wave2-apply-receipt.json", receipt)
    return receipt


def cmd_run_all() -> int:
    cfg = load_json(ROOT / "decks/bolt/deck.config.json")
    presentation_id = cfg["deck_id"]
    print("1/5 Register + publish wave-2 assets...")
    urls = register_wave2_assets()
    print(f"   published {len(urls)} assets")

    print("2/5 Build wave-2 editplan (all 23 slides)...")
    plan = build_wave2_editplan(presentation_id, urls)
    plan_path = ROOT / "decks/bolt/deck.editplan.json"
    write_json(plan_path, plan)
    print(f"   operations: {len(plan['operations'])}")

    drift = drift_gate(presentation_id, plan)
    if not drift["pass"]:
        print(json.dumps(drift, indent=2), file=sys.stderr)
        raise SystemExit("Drift gate failed before apply")
    print("   drift gate: pass")

    print("3/5 Apply wave-2 editplan...")
    applied = apply_plan(plan, chunk_size=35)
    plan["applied_at"] = utc_now()
    plan["status"] = "applied"
    write_json(plan_path, plan)
    print(f"   applied {applied} requests")

    print("4/5 Full-deck leak scan + thumbnails...")
    receipt = run_wave2_qa(presentation_id, plan)
    print(json.dumps(receipt, indent=2))

    cfg["notes"] = "Bolt wave-2 full deck applied via deck_bolt_wave2.py — partner-ready scope."
    cfg["last_pulled_at"] = utc_now()
    write_json(ROOT / "decks/bolt/deck.config.json", cfg)
    return 0 if receipt["status"] == "pass" else 1


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Bolt wave-2 full deck builder")
    ap.add_argument(
        "command",
        choices=["run-all", "register-assets", "build-editplan", "apply", "qa"],
    )
    ap.add_argument("--presentation-id")
    args = ap.parse_args()

    if args.command == "register-assets":
        print(json.dumps(register_wave2_assets(), indent=2))
        return 0
    if args.command == "build-editplan":
        cfg = load_json(ROOT / "decks/bolt/deck.config.json")
        pid = args.presentation_id or cfg["deck_id"]
        registry = load_json(ROOT / "assets/ASSET-REGISTRY.json")
        urls = {k: v["source_url"] for k, v in registry["assets"].items() if v.get("source_url")}
        plan = build_wave2_editplan(pid, urls)
        write_json(ROOT / "decks/bolt/deck.editplan.json", plan)
        print(json.dumps({"operations": len(plan["operations"]), "presentation_id": pid}, indent=2))
        return 0
    if args.command == "apply":
        plan = load_json(ROOT / "decks/bolt/deck.editplan.json")
        n = apply_plan(plan, chunk_size=35)
        plan["applied_at"] = utc_now()
        plan["status"] = "applied"
        write_json(ROOT / "decks/bolt/deck.editplan.json", plan)
        print(f"applied {n}")
        return 0
    if args.command == "qa":
        plan = load_json(ROOT / "decks/bolt/deck.editplan.json")
        receipt = run_wave2_qa(plan["presentation_id"], plan)
        print(json.dumps(receipt, indent=2))
        return 0 if receipt["status"] == "pass" else 1
    if args.command == "run-all":
        return cmd_run_all()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())