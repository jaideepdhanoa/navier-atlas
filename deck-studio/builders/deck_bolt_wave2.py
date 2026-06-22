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
from deck_link_bindings import build_deck_link_ops  # noqa: E402
from deck_edit_ops import econ_value_replace_ops, image_replace_op, text_replace_ops  # noqa: E402
from deck_market_routes import (  # noqa: E402
    ROUTE_TARGET_OIDS,
    build_market_route_ops,
    validate_market_route_bindings,
)
from deck_slide_bindings import image_bindings_list, load_slide_bindings, validate_bindings  # noqa: E402

GOLD_ID = "18yDAgO0Sj9PJlgf6paxtgni8Pk1xRAmNwE2TD_NCdSs"

# Slide 10 TAM ladder: golden map uses shape contentAlignment MIDDLE (vertical centering in
# the box) but paragraph text must stay left-aligned — do not map MIDDLE → CENTER here.
# Unit-econ eyebrow: all slides share the same text-box geometry (Grab gold template).
# Do not derive char_budget from shorter Grab residue samples (Bali/Phuket on slides 8–9).
ECON_HEADER_MARKET_CHAR_BUDGET = 31
ECON_HEADER_MARKET_OBJECT_IDS = frozenset(
    {
        "g3eec5122801_0_392",
        "g3eec5122801_0_449",
        "g3eec5122801_0_506",
        "g3eec5122801_0_741",
        "g3eec5122801_0_798",
        "g3eec5122801_0_855",
        "g3eec5122801_0_912",
        "g3eec5122801_0_969",
    }
)

TAM_LADDER_OBJECT_IDS = frozenset(
    {
        "g3eec5122801_0_570",
        "g3eec5122801_0_571",
        "g3eec5122801_0_574",
        "g3eec5122801_0_575",
        "g3eec5122801_0_578",
        "g3eec5122801_0_579",
        "g3eec5122801_0_582",
        "g3eec5122801_0_583",
        "g3eec5122801_0_586",
        "g3eec5122801_0_587",
    }
)

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
    8: {
        "corridor": "Athens -> Hydra (Saronic)",
        "market_label": "GREECE",
        "title_market": "Greece",
        "route_line": "Athens → Hydra (Saronic)  ·  ~30 nm  ·  N30 Pioneer II (8 seats)",
        "bg_registry": "econ-greece-athens-hydra",
        "bg_oid": "navierBg_s23",
    },
    9: {
        "corridor": "Split -> Hvar",
        "market_label": "CROATIA",
        "title": "Croatia: profit from year one",
        "route_line": "Split → Hvar  ·  ~20 nm  ·  N30 Pioneer II (8 seats)",
        "bg_registry": "econ-croatia-split-hvar",
        "bg_oid": "navierBg_s24",
    },
    10: {
        "corridor": "Nice -> Monaco",
        "market_label": "RIVIERA",
        "title": "Riviera: profit from year one",
        "route_line": "Nice → Monaco  ·  ~7 nm  ·  N30 Pioneer II (8 seats)",
        "bg_registry": "econ-cote-azur-nice-monaco",
        "bg_oid": "navierBg_s25",
    },
    20: {
        "corridor": "Sorrento -> Capri",
        "market_label": "ITALY",
        "title_market": "Italy",
        "route_line": "Sorrento → Capri  ·  ~17 nm  ·  N30 Pioneer II (8 seats)",
        "bg_registry": "econ-italy-sorrento-capri",
        "bg_oid": "navierBg_s35",
    },
    21: {
        "corridor": "Dubai Harbour Marina -> Bluewaters Marina",
        "market_label": "UAE",
        "title_market": "UAE",
        "route_line": "Dubai Harbour → Bluewaters  ·  ~3 nm  ·  N30 Pioneer II (8 seats)",
        "bg_registry": "econ-uae-dubai-harbour",
        "bg_oid": "navierBg_s36",
    },
    22: {
        "corridor": "Jeddah Corniche -> Jeddah Central (PIF waterfront)",
        "market_label": "JEDDAH",
        "header_market": "WHAT ONE BOAT EARNS · JEDDAH",
        "title": "Jeddah: profitable from year one",
        "route_line": "Jeddah Corniche → Jeddah Central  ·  ~2 nm  ·  N30 Pioneer II (8 seats)",
        "bg_registry": "econ-ksa-jeddah",
        "bg_oid": "navierBg_s37",
    },
    23: {
        "corridor": "Mykonos -> Paros",
        "market_label": "GREECE",
        "title_market": "Cyclades",
        "route_line": "Mykonos → Paros  ·  ~25 nm  ·  N30 Pioneer II (8 seats)",
        "bg_registry": "econ-greece-mykonos-paros",
        "bg_oid": "navierBg_s38",
    },
    24: {
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
    # Slide 3 KPI ladder — values filled by slide3_kpi_text_map() from growth cascade
    # Slide 4 Greece example market
    ("g3eec5122801_0_106", "g3eec5122801_0_110"): "Greece — the recommended beachhead",
    ("g3eec5122801_0_106", "g3eec5122801_0_111"): "Bolt's deepest island demand and longest season — replacing slow diesel ferries.",
    # Slide 4–6 + 14–18 route lists: decks/bolt/market-route-bindings.json (4 routes, amber bullet)
    # Slide 5 Croatia
    ("g3eec5122801_0_201", "g3eec5122801_0_205"): "Croatia — the Dalmatian island chain",
    ("g3eec5122801_0_201", "g3eec5122801_0_206"): "High-volume Adriatic island hops — Split, Hvar, Brač and Korčula on one network.",
    # Slide 6 Riviera
    ("g3eec5122801_0_296", "g3eec5122801_0_300"): "Riviera — Nice to Monaco by water",
    ("g3eec5122801_0_296", "g3eec5122801_0_304"): "Premium corporate and leisure demand — skip Corniche traffic with a silent foiling run.",
    # Slide 10 TAM — ladder values filled by slide10_tam_text_map() from economics sidecar
    ("g3eec5122801_0_562", "g3eec5122801_0_565"): "A new multi-billion-dollar vertical across Europe",
    ("g3eec5122801_0_562", "g3eec5122801_0_567"): "Read it bottom-up: the fare a Navier boat collects today, the market a faster product unlocks — then the whole journey a super-app monetizes around every crossing.",
    # Slide 11 partner roles
    ("g3ea5e0fb254_4_357", "g3ea5e0fb254_4_361"): "You bring the demand. We operate the water.",
    ("g3ea5e0fb254_4_357", "g3ea5e0fb254_4_362"): "▸  Bolt — demand, the app, the wallet and the brand.\n▸  Navier — vessels, crew, maintenance, certification and the network playbook.\n▸  Together — a premium foiling water tier from the Aegean to the Gulf.",
    # Slide 12 ask
    ("g3ea5e0fb254_4_444", "g3ea5e0fb254_4_447"): "1.  Working session — walk through the presentation and Navier atlas. \n2.  Vessel demo — a live foiling run on a pilot corridor. \n3.  Pilot MOU — Greece beachhead, three corridors, 12-month launch window.",
    # Slide 13 close — body phrase "Navier × Bolt Atlas" is white hyperlinked via close_atlas_link binding
    ("g3ea5e0fb254_4_330", "g3ea5e0fb254_4_330"): "Explore the Bolt marine network",
    ("g3ea5e0fb254_4_331", "g3ea5e0fb254_4_331"): (
        "Open the Navier × Bolt Atlas, pick the first corridor, "
        "and let's discover a new foiling water tier across Europe."
    ),
    # Slide 14 Italy backup market
    ("g3eec5122801_0_677", "g3eec5122801_0_679"): "Italy — Amalfi, Capri & the lagoon",
    ("g3eec5122801_0_677", "g3eec5122801_0_680"): "Amalfi Coast day-trips, Capri crossings and Venice lagoon hops on one supply standard.",
    # Slide 15 UAE
    ("g3eec5122801_0_690", "g3eec5122801_0_692"): "UAE — Dubai & Abu Dhabi by water",
    ("g3eec5122801_0_690", "g3eec5122801_0_693"): "Premium harbour-to-harbour demand — no Sheikh Zayed Road required.",
    # Slide 16 Saudi
    ("g3eec5122801_0_703", "g3eec5122801_0_705"): "Saudi — Jeddah & the Red Sea",
    ("g3eec5122801_0_703", "g3eec5122801_0_706"): "PIF waterfront ambition meets water mobility",
    # Slide 17 Greece Cyclades
    ("g3eec5122801_0_716", "g3eec5122801_0_718"): "Greece — Cyclades island network",
    ("g3eec5122801_0_716", "g3eec5122801_0_719"): "Mykonos, Paros, Naxos and Santorini — the highest-volume Aegean hops.",
    # Slide 18 Croatia Dubrovnik
    ("g3eec5122801_0_729", "g3eec5122801_0_731"): "Croatia — Dubrovnik & the islands",
    ("g3eec5122801_0_729", "g3eec5122801_0_732"): "Elaphiti Islands, Korčula and Mljet — premium Adriatic excursions.",
}

# Deck-level narrative plates only. Unit-econ + atlas screenshot wiring lives in
# decks/bolt/slide-image-bindings.json — never bind econ_market_bg to slides 4–6 or 14–18.
IMAGE_BINDINGS: list[dict] = [
    {"registry": "bolt-cover-hero", "slide_oid": "p1", "target_oid": "p1_i2", "method": "CENTER_CROP"},
    {"registry": "bolt-value-prop-bg", "slide_oid": "g3f139a0b6ec_0_0", "target_oid": "g3f139a0b6ec_0_1", "method": "CENTER_CROP"},
    {"registry": "bolt-tam-bg", "slide_oid": "g3eec5122801_0_562", "target_oid": "navierBg_s26", "method": "CENTER_CROP"},
    {"registry": "bolt-partner-roles-bg", "slide_oid": "g3ea5e0fb254_4_357", "target_oid": "g3ea5e0fb254_4_358", "method": "CENTER_CROP"},
    {"registry": "bolt-partner-logo", "slide_oid": "p1", "target_oid": "p1_i5", "method": "CENTER_INSIDE"},
]


def atlas_image_bindings() -> list[dict]:
    doc = load_slide_bindings("bolt")
    return image_bindings_list(doc, roles={"atlas_route_screenshot"})


def element_or_fallback(golden: dict, oid: str, *, fallback_oid: str = "g3eec5122801_0_394") -> dict:
    el = golden_element(golden, oid)
    if el:
        return el
    fb = golden_element(golden, fallback_oid)
    if not fb:
        raise KeyError(f"No golden element for {oid}")
    return {**fb, "oid": oid, "char_budget": max(fb.get("char_budget", 12), 16)}


def econ_header_market_text(spec: dict) -> str:
    return spec.get("header_market", f"WHAT ONE BOAT EARNS · {spec['market_label']}")


def econ_text_element(golden: dict, oid: str, field_key: str) -> dict:
    el = element_or_fallback(golden, oid)
    if field_key == "header_market" or oid in ECON_HEADER_MARKET_OBJECT_IDS:
        return {**el, "char_budget": max(el.get("char_budget", 12), ECON_HEADER_MARKET_CHAR_BUDGET)}
    return el


def validate_econ_header_markets() -> list[str]:
    errors: list[str] = []
    for slide_index, spec in ECON_BINDINGS.items():
        header = econ_header_market_text(spec)
        if len(header) > ECON_HEADER_MARKET_CHAR_BUDGET:
            errors.append(
                f"slide {slide_index}: header_market len {len(header)} > {ECON_HEADER_MARKET_CHAR_BUDGET}: {header!r}"
            )
        if not header.endswith(spec["market_label"]):
            errors.append(
                f"slide {slide_index}: header_market must end with market_label {spec['market_label']!r}, got {header!r}"
            )
    return errors


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

SLIDE3_OID = "g3eec5122801_0_0"
SLIDE10_OID = "g3eec5122801_0_562"
ECONOMICS_VALUES_PATH = ROOT / "decks/bolt/deck-economics-values-bolt.json"
NARRATIVE_BINDING_PATH = ROOT / "decks/bolt/narrative-binding.json"
NARRATIVE_JSON_PATH = ROOT / "decks/bolt/narrative-slide2-bolt.json"
GOLD_SLIDE2_CREATE_PATH = ROOT / "decks/grab/narrative-slide2.gold-create.editplan.json"

SLIDE3_KPI_FIELDS: list[tuple[str, str]] = [
    ("g3eec5122801_0_6", "card1_value"),
    ("g3eec5122801_0_7", "card1_caption"),
    ("g3eec5122801_0_10", "card2_value"),
    ("g3eec5122801_0_11", "card2_caption"),
    ("g3eec5122801_0_15", "card3_value"),
    ("g3eec5122801_0_16", "card3_caption"),
    ("g3eec5122801_0_18", "card4_value"),
    ("g3eec5122801_0_19", "card4_caption"),
]

SLIDE10_TAM_FIELDS: list[tuple[str, str]] = [
    ("g3eec5122801_0_570", "som_value"),
    ("g3eec5122801_0_571", "som_caption"),
    ("g3eec5122801_0_574", "sam_value"),
    ("g3eec5122801_0_575", "sam_caption"),
    ("g3eec5122801_0_578", "tam_value"),
    ("g3eec5122801_0_579", "tam_caption"),
    ("g3eec5122801_0_582", "journey_gmv_value"),
    ("g3eec5122801_0_583", "journey_gmv_caption"),
    ("g3eec5122801_0_586", "platform_value"),
    ("g3eec5122801_0_587", "platform_caption"),
]

SLIDE10_TAM_CAPTIONS = {
    "som_caption": "SOM — Navier fare, Bolt network, today's trips, 10% capture",
    "sam_caption": "SAM — faster, quieter boats grow the market; 25% capture at maturity",
    "tam_caption": "TAM — the entire induced marine-transfer market (≈ 4× SAM; band $4.5–15.8B)",
    "journey_gmv_caption": "Journey GMV — add food + stays + experiences to every crossing (≈ 3× TAM)",
    "platform_caption": "Bolt platform revenue on Navier — 18% × Navier-corridor Journey GMV (ceiling on full network)",
}


def load_economics_values() -> dict:
    return load_json(ECONOMICS_VALUES_PATH)


def slide3_kpi_text_map() -> dict[str, str]:
    """Market-overview KPI ladder from deck-economics-values sidecar."""
    sidecar = load_economics_values()
    cards = sidecar["slide3_kpi"]["network_cards"]
    if len(cards) != 4:
        raise ValueError(f"expected 4 network_cards, got {len(cards)}")
    return {
        "card1_value": cards[0]["value"],
        "card1_caption": cards[0]["meaning"],
        "card2_value": cards[1]["value"],
        "card2_caption": cards[1]["meaning"],
        "card3_value": cards[2]["value"],
        "card3_caption": cards[2]["meaning"],
        "card4_value": cards[3]["value"],
        "card4_caption": cards[3]["meaning"],
    }


def slide10_tam_text_map() -> dict[str, str]:
    """TAM ladder values from deck-economics-values sidecar + fixed Bolt captions."""
    sidecar = load_economics_values()
    rungs = sidecar["slide10_tam"]["rungs"]
    if len(rungs) != 5:
        raise ValueError(f"expected 5 TAM rungs, got {len(rungs)}")
    keys = ("som", "sam", "tam", "journey_gmv", "platform")
    out: dict[str, str] = {}
    for key, rung in zip(keys, rungs):
        out[f"{key}_value"] = rung["value"]
        out[f"{key}_caption"] = SLIDE10_TAM_CAPTIONS[f"{key}_caption"]
    return out


def kpi_element(golden: dict, oid: str, text: str) -> dict:
    el = element_or_fallback(golden, oid)
    return {**el, "char_budget": max(el.get("char_budget", 12), len(text) + 4)}


def build_slide3_kpi_ops(golden: dict) -> list[dict]:
    kpi = slide3_kpi_text_map()
    ops: list[dict] = []
    source = "decks/bolt/deck-economics-values-bolt.json slide3_kpi.network_cards"
    for oid, key in SLIDE3_KPI_FIELDS:
        text = kpi[key]
        el = kpi_element(golden, oid, text)
        ops.extend(
            text_replace_ops(
                SLIDE3_OID,
                oid,
                text,
                el,
                op_prefix=f"bolt-slide3-kpi-{oid}",
                source_pointer=source,
            )
        )
    return ops


def build_slide10_tam_ops(golden: dict) -> list[dict]:
    tam = slide10_tam_text_map()
    ops: list[dict] = []
    source = "decks/bolt/deck-economics-values-bolt.json slide10_tam.rungs"
    for oid, key in SLIDE10_TAM_FIELDS:
        text = tam[key]
        el = kpi_element(golden, oid, text)
        ops.extend(
            text_replace_ops(
                SLIDE10_OID,
                oid,
                text,
                el,
                op_prefix=f"bolt-slide10-tam-{oid}",
                source_pointer=source,
                alignment="START" if oid in TAM_LADDER_OBJECT_IDS else None,
            )
        )
    return ops


def narrative_element(text: str) -> dict:
    return {"char_budget": max(len(text) + 24, 48), "style": {"font": "Exo 2", "sizePt": 11, "bold": False, "color": [1.0, 1.0, 1.0]}}


def apply_slides_requests(presentation_id: str, requests: list[dict], *, chunk_size: int = 35) -> int:
    service = slides_service()
    applied = 0
    for i in range(0, len(requests), chunk_size):
        chunk = requests[i : i + chunk_size]
        service.presentations().batchUpdate(
            presentationId=presentation_id, body={"requests": chunk}
        ).execute()
        applied += len(chunk)
    return applied


def slide2_exists(presentation_id: str) -> bool:
    service = slides_service()
    pres = service.presentations().get(presentationId=presentation_id).execute()
    return any(slide.get("objectId") == "narr2_page" for slide in pres.get("slides", []))


def cmd_insert_slide2() -> int:
    cfg = load_json(ROOT / "decks/bolt/deck.config.json")
    presentation_id = cfg["deck_id"]
    if slide2_exists(presentation_id):
        print(json.dumps({"status": "already_present", "slide_object_id": "narr2_page"}, indent=2))
        return 0
    gold_create = load_json(GOLD_SLIDE2_CREATE_PATH)
    requests = gold_create["requests"]
    applied = apply_slides_requests(presentation_id, requests, chunk_size=12)
    print(json.dumps({"applied_requests": applied, "slide_object_id": "narr2_page"}, indent=2))
    return 0


def build_narrative_paint_ops() -> list[dict]:
    binding = load_json(NARRATIVE_BINDING_PATH)
    narrative = load_json(NARRATIVE_JSON_PATH)
    slide_oid = binding["slide_object_id"]
    ops: list[dict] = []

    for field_key, pin in binding["fields"].items():
        if not pin.get("present"):
            continue
        if pin.get("static"):
            text = pin["static"]
        else:
            text = narrative.get(field_key) or ""
        if not text:
            continue
        ops.extend(
            text_replace_ops(
                slide_oid,
                pin["object_id"],
                text,
                narrative_element(text),
                op_prefix=f"bolt-narr2-{pin['object_id']}",
                source_pointer=NARRATIVE_JSON_PATH.name,
            )
        )

    for i, beat_pin in enumerate(binding["your_world"]):
        if not beat_pin.get("present"):
            continue
        beat = narrative["your_world"][i]
        for part, oid_key in (("label", "head_object_id"), ("text", "body_object_id")):
            text = beat[part]
            ops.extend(
                text_replace_ops(
                    slide_oid,
                    beat_pin[oid_key],
                    text,
                    narrative_element(text),
                    op_prefix=f"bolt-narr2-{beat_pin[oid_key]}",
                    source_pointer=NARRATIVE_JSON_PATH.name,
                )
            )
    return ops


def cmd_apply_narrative() -> int:
    cfg = load_json(ROOT / "decks/bolt/deck.config.json")
    presentation_id = cfg["deck_id"]
    if not slide2_exists(presentation_id):
        raise SystemExit("narr2_page missing — run insert-slide2 first")
    ops = build_narrative_paint_ops()
    plan = {"deck_key": "bolt", "presentation_id": presentation_id, "operations": ops}
    applied = apply_plan(plan, chunk_size=40)
    print(json.dumps({"applied_ops": applied, "fields": len(ops) // 3}, indent=2))
    return 0


def cmd_apply_slide2_image() -> int:
    cfg = load_json(ROOT / "decks/bolt/deck.config.json")
    presentation_id = cfg["deck_id"]
    if not slide2_exists(presentation_id):
        raise SystemExit("narr2_page missing — run insert-slide2 first")
    registry = load_json(ROOT / "assets/ASSET-REGISTRY.json")
    asset = registry["assets"]["bolt-value-prop-bg"]
    url = asset.get("source_url")
    if not url:
        raise SystemExit("bolt-value-prop-bg missing source_url")
    emu_w, emu_h = 9144000, 5143500
    requests = [
        {
            "createImage": {
                "objectId": "narr2_bg_img",
                "url": url,
                "elementProperties": {
                    "pageObjectId": "narr2_page",
                    "size": {
                        "width": {"magnitude": emu_w, "unit": "EMU"},
                        "height": {"magnitude": emu_h, "unit": "EMU"},
                    },
                    "transform": {
                        "scaleX": 1,
                        "scaleY": 1,
                        "translateX": 0,
                        "translateY": 0,
                        "unit": "EMU",
                    },
                },
            }
        },
        {
            "updatePageElementsZOrder": {
                "pageElementObjectIds": ["narr2_bg_img"],
                "operation": "SEND_TO_BACK",
            }
        },
    ]
    applied = apply_slides_requests(presentation_id, requests, chunk_size=2)
    print(json.dumps({"applied_requests": applied, "image_url": url, "target": "narr2_bg_img"}, indent=2))
    return 0


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
            "header_market": econ_header_market_text(spec),
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
        el = econ_text_element(golden, oid, field_key)
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
            "used_by": [{"deck": "bolt", "slide_index": 3, "slide_object_id": "g3f139a0b6ec_0_0", "target_object_id": "g3f139a0b6ec_0_1"}],
        },
        "bolt-tam-bg": {
            "role": "tam_bg",
            "scope": "deck",
            "partner": "bolt",
            "local_path": "assets/backgrounds/decks/bolt/bolt-tam-v1-composited.png",
            "provenance": "n30_composite:grok_gen_bolt_tam_raw",
            "used_by": [{"deck": "bolt", "slide_index": 11, "slide_object_id": "g3eec5122801_0_562", "target_object_id": "navierBg_s26"}],
        },
        "bolt-partner-roles-bg": {
            "role": "partner_roles_bg",
            "scope": "deck",
            "partner": "bolt",
            "local_path": "assets/backgrounds/decks/bolt/bolt-partner-roles-v1-composited.png",
            "provenance": "n30_composite:grok_gen_bolt_partner_roles_raw",
            "used_by": [{"deck": "bolt", "slide_index": 12, "slide_object_id": "g3ea5e0fb254_4_357", "target_object_id": "g3ea5e0fb254_4_358"}],
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


def partner_json_path() -> Path:
    return ROOT.parent / "data-clean/partners/bolt.json"


def build_market_route_slide_ops(golden: dict) -> list[dict]:
    errs = validate_market_route_bindings(
        "bolt", partner_json_path=partner_json_path(), golden=golden
    )
    if errs:
        raise SystemExit("market-route-bindings.json invalid:\n" + "\n".join(errs))
    return build_market_route_ops(
        golden,
        "bolt",
        partner_json_path=partner_json_path(),
        element_lookup=element_or_fallback,
    )


def build_wave2_editplan(presentation_id: str, asset_urls: dict[str, str]) -> dict:
    header_errs = validate_econ_header_markets()
    if header_errs:
        raise SystemExit("ECON_BINDINGS header_market invalid:\n" + "\n".join(header_errs))
    golden = load_json(ROOT / "decks/grab/golden-template-map.json")
    binding = load_json(ROOT / "decks/bolt/economics-binding.json")
    ops: list[dict] = []

    ops.extend(build_slide3_kpi_ops(golden))
    ops.extend(build_slide10_tam_ops(golden))
    ops.extend(build_market_route_slide_ops(golden))

    for (slide_oid, target_oid), text in NARRATIVE_TEXT.items():
        if target_oid in ROUTE_TARGET_OIDS:
            continue
        el = element_or_fallback(golden, target_oid)
        para_align = "START" if target_oid in TAM_LADDER_OBJECT_IDS else None
        ops.extend(
            text_replace_ops(
                slide_oid,
                target_oid,
                text,
                el,
                op_prefix=f"bolt-wave2-{target_oid}",
                source_pointer="deck_bolt_wave2.NARRATIVE_TEXT + deck-economics-values-bolt.json",
                alignment=para_align,
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

    binding_doc = load_slide_bindings("bolt")
    bind_errs = validate_bindings(binding_doc)
    if bind_errs:
        raise SystemExit("slide-image-bindings.json invalid:\n" + "\n".join(bind_errs))
    for bind in atlas_image_bindings():
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

    ops.extend(build_deck_link_ops("bolt", op_prefix="bolt-wave2-deck-link"))

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


def build_econ_header_ops(golden: dict, *, slide_indices: list[int] | None = None) -> list[dict]:
    binding = load_json(ROOT / "decks/bolt/economics-binding.json")
    ops: list[dict] = []
    for slide_binding in binding["economics_slides"]:
        idx = slide_binding["slide_index"]
        if slide_indices is not None and idx not in slide_indices:
            continue
        spec = ECON_BINDINGS.get(idx)
        if not spec:
            continue
        slide_oid = slide_binding["slide_object_id"]
        oid = slide_binding["fields"]["header_market"]["object_id"]
        text = econ_header_market_text(spec)
        el = econ_text_element(golden, oid, "header_market")
        ops.extend(
            text_replace_ops(
                slide_oid,
                oid,
                text,
                el,
                op_prefix=f"bolt-econ{idx}-header_market",
                source_pointer=f"deck_bolt_wave2.ECON_BINDINGS slide {idx}",
            )
        )
    return ops


def cmd_apply_econ_headers(slide_indices: list[int] | None = None) -> int:
    header_errs = validate_econ_header_markets()
    if header_errs:
        raise SystemExit("ECON_BINDINGS header_market invalid:\n" + "\n".join(header_errs))
    cfg = load_json(ROOT / "decks/bolt/deck.config.json")
    golden = load_json(ROOT / "decks/grab/golden-template-map.json")
    ops = build_econ_header_ops(golden, slide_indices=slide_indices)
    plan = {"deck_key": "bolt", "presentation_id": cfg["deck_id"], "operations": ops}
    applied = apply_plan(plan, chunk_size=40)
    headers = {
        idx: econ_header_market_text(ECON_BINDINGS[idx])
        for idx in (slide_indices or sorted(ECON_BINDINGS))
        if idx in ECON_BINDINGS
    }
    print(json.dumps({"applied_ops": applied, "header_market": headers}, indent=2))
    return 0


def cmd_apply_market_routes() -> int:
    cfg = load_json(ROOT / "decks/bolt/deck.config.json")
    presentation_id = cfg["deck_id"]
    golden = load_json(ROOT / "decks/grab/golden-template-map.json")
    ops = build_market_route_slide_ops(golden)
    plan = {
        "deck_key": "bolt",
        "presentation_id": presentation_id,
        "operations": ops,
    }
    applied = apply_plan(plan, chunk_size=40)
    print(json.dumps({"applied_ops": applied, "market_route_slides": [5, 6, 7, 15, 16, 17, 18, 19]}, indent=2))
    return 0


def cmd_apply_slide3_kpis() -> int:
    cfg = load_json(ROOT / "decks/bolt/deck.config.json")
    presentation_id = cfg["deck_id"]
    golden = load_json(ROOT / "decks/grab/golden-template-map.json")
    ops = build_slide3_kpi_ops(golden)
    plan = {
        "deck_key": "bolt",
        "presentation_id": presentation_id,
        "operations": ops,
    }
    applied = apply_plan(plan, chunk_size=40)
    kpi = slide3_kpi_text_map()
    binding = load_json(ROOT / "decks/bolt/economics-binding.json")
    slide3 = binding.setdefault("slide3_kpi", {})
    slide3["applied_at"] = utc_now()
    slide3["source"] = "decks/bolt/deck-economics-values-bolt.json"
    for item in slide3.get("kpis", []):
        field_map = {
            "g3eec5122801_0_6": ("sample_value", "card1_value"),
            "g3eec5122801_0_7": ("sample_caption", "card1_caption"),
            "g3eec5122801_0_10": ("sample_value", "card2_value"),
            "g3eec5122801_0_11": ("sample_caption", "card2_caption"),
            "g3eec5122801_0_15": ("sample_value", "card3_value"),
            "g3eec5122801_0_16": ("sample_caption", "card3_caption"),
            "g3eec5122801_0_18": ("sample_value", "card4_value"),
            "g3eec5122801_0_19": ("sample_caption", "card4_caption"),
        }
        vid = item.get("value_object_id")
        cid = item.get("caption_object_id")
        if vid in field_map:
            attr, k = field_map[vid]
            item[attr] = kpi[k]
        if cid in field_map:
            attr, k = field_map[cid]
            item[attr] = kpi[k]
    write_json(ROOT / "decks/bolt/economics-binding.json", binding)
    print(json.dumps({"applied_ops": applied, "slide3_kpi": kpi}, indent=2))
    return 0


def cmd_apply_slide10_tam() -> int:
    cfg = load_json(ROOT / "decks/bolt/deck.config.json")
    presentation_id = cfg["deck_id"]
    golden = load_json(ROOT / "decks/grab/golden-template-map.json")
    ops = build_slide10_tam_ops(golden)
    plan = {
        "deck_key": "bolt",
        "presentation_id": presentation_id,
        "operations": ops,
    }
    applied = apply_plan(plan, chunk_size=40)
    tam = slide10_tam_text_map()
    binding = load_json(ROOT / "decks/bolt/economics-binding.json")
    slide10 = binding.setdefault("slide10_tam", {})
    slide10["applied_at"] = utc_now()
    slide10["source"] = "decks/bolt/deck-economics-values-bolt.json"
    value_keys = ("som_value", "sam_value", "tam_value", "journey_gmv_value", "platform_value")
    caption_keys = ("som_caption", "sam_caption", "tam_caption", "journey_gmv_caption", "platform_caption")
    for item, vkey, ckey in zip(slide10.get("rungs", []), value_keys, caption_keys):
        item["sample_value"] = tam[vkey]
        item["sample_caption"] = tam[ckey]
    write_json(ROOT / "decks/bolt/economics-binding.json", binding)
    print(json.dumps({"applied_ops": applied, "slide10_tam": tam}, indent=2))
    return 0


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
        choices=[
            "run-all",
            "register-assets",
            "build-editplan",
            "apply",
            "qa",
            "apply-slide3-kpis",
            "apply-slide10-tam",
            "insert-slide2",
            "apply-narrative",
            "apply-slide2-image",
            "apply-market-routes",
            "validate-market-routes",
            "validate-econ-headers",
            "apply-econ-headers",
            "apply-atlas-links",
            "validate-atlas-links",
        ],
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
    if args.command == "apply-slide3-kpis":
        return cmd_apply_slide3_kpis()
    if args.command == "apply-slide10-tam":
        return cmd_apply_slide10_tam()
    if args.command == "insert-slide2":
        return cmd_insert_slide2()
    if args.command == "apply-narrative":
        return cmd_apply_narrative()
    if args.command == "apply-slide2-image":
        return cmd_apply_slide2_image()
    if args.command == "apply-market-routes":
        return cmd_apply_market_routes()
    if args.command == "validate-econ-headers":
        errs = validate_econ_header_markets()
        if errs:
            print("\n".join(errs), file=sys.stderr)
            return 1
        headers = {idx: econ_header_market_text(spec) for idx, spec in ECON_BINDINGS.items()}
        print(json.dumps({"status": "pass", "header_market": headers}, indent=2))
        return 0
    if args.command == "apply-econ-headers":
        return cmd_apply_econ_headers()
    if args.command == "validate-market-routes":
        golden = load_json(ROOT / "decks/grab/golden-template-map.json")
        errs = validate_market_route_bindings(
            "bolt", partner_json_path=partner_json_path(), golden=golden
        )
        if errs:
            print("\n".join(errs), file=sys.stderr)
            return 1
        print(json.dumps({"status": "pass", "slides": [5, 6, 7, 15, 16, 17, 18, 19]}, indent=2))
        return 0
    if args.command == "apply-atlas-links":
        from deck_link_bindings import cmd_apply

        return cmd_apply("bolt", presentation_id=args.presentation_id)
    if args.command == "validate-atlas-links":
        from deck_link_bindings import cmd_validate

        return cmd_validate("bolt")
    if args.command == "run-all":
        return cmd_run_all()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())