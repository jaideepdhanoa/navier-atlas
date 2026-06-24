#!/usr/bin/env python3
"""Ocean Whisperer hospitality deck — Bolt wave-2 contract (images + slide2 + links + QA)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDERS = ROOT / "builders"
sys.path.insert(0, str(BUILDERS))

from deck_bolt_pilot import (  # noqa: E402
    apply_plan,
    copy_gold_deck,
    export_thumbnails,
    golden_element,
    golden_slide_oid,
    leak_scan,
    load_json,
    slides_service,
    utc_now,
    write_json,
)
from deck_bolt_wave2 import apply_slides_requests  # noqa: E402
from deck_edit_ops import econ_value_replace_ops, image_replace_op, text_replace_ops  # noqa: E402
from deck_link_bindings import build_deck_link_ops  # noqa: E402
from deck_market_routes import (  # noqa: E402
    ROUTE_TARGET_OIDS,
    build_market_route_ops,
    validate_market_route_bindings,
)
from deck_narrative_slide2 import build_narrative_paint_ops as build_narr2_paint_ops  # noqa: E402
from deck_slide_bindings import image_bindings_list, load_slide_bindings, validate_bindings  # noqa: E402

DECK = "ocean-whisperer"
GOLDEN = ROOT / "decks/grab/golden-template-map.json"
KPI_PATH = ROOT / "decks/ocean-whisperer/slide3-kpis-ocean-whisperer.json"
VALUES_PATH = ROOT / "decks/ocean-whisperer/deck-economics-values-ocean-whisperer.json"
GROWTH_PATH = ROOT.parent / "finance/recal/growth-ocean-whisperer.json"
AGG_PATH = ROOT.parent / "finance/recal/agg-ocean-whisperer.json"
PARTNER_PATH = ROOT.parent / "partner-pitch/partners/ocean-whisperer.json"
NARRATIVE_BINDING_PATH = ROOT / "decks/ocean-whisperer/narrative-binding.json"
NARRATIVE_JSON_PATH = ROOT / "decks/ocean-whisperer/narrative-slide2-ocean-whisperer.json"
SLIDE_LINK_BINDINGS_PATH = ROOT / "decks/ocean-whisperer/slide-link-bindings.json"
GOLD_SLIDE2_CREATE_PATH = ROOT / "decks/grab/narrative-slide2.gold-create.editplan.json"

THREE_CS_SLIDE_OID = "g3f139a0b6ec_0_0"
THREE_CS_BG_OID = "g3f139a0b6ec_0_1"

SLIDE3_KPI_CAPTION_OIDS = frozenset(
    {
        "g3eec5122801_0_7",
        "g3eec5122801_0_11",
        "g3eec5122801_0_16",
        "g3eec5122801_0_19",
    }
)

LEAK_DENYLIST = [
    "Grab", "Uber", "Bolt", "Careem", "Singapore", "Sentosa", "Minor Hotels",
    "Phuket", "Bali", "super-app", "Koh Samui", "Bangkok", "Benoa", "Nusa Penida",
]

SLIDE3_OID = "g3eec5122801_0_0"
SLIDE10_OID = "g3eec5122801_0_562"
ECON_HEADER_CHAR_BUDGET = 31

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

IMAGE_BINDINGS: list[dict] = [
    {"registry": "ow-cover-hero", "slide_oid": "p1", "target_oid": "p1_i2", "method": "CENTER_CROP"},
    {
        "registry": "ow-three-cs-bg",
        "slide_oid": THREE_CS_SLIDE_OID,
        "target_oid": THREE_CS_BG_OID,
        "method": "CENTER_CROP",
    },
    {"registry": "ow-tam-bg", "slide_oid": SLIDE10_OID, "target_oid": "navierBg_s26", "method": "CENTER_CROP"},
    {
        "registry": "ow-partner-roles-bg",
        "slide_oid": "g3ea5e0fb254_4_357",
        "target_oid": "g3ea5e0fb254_4_358",
        "method": "CENTER_CROP",
    },
    {"registry": "ocean-whisperer-logo", "slide_oid": "p1", "target_oid": "p1_i5", "method": "CENTER_INSIDE"},
]

ECON_SLIDES: dict[int, dict] = {
    7: {
        "slide_oid": "g3eec5122801_0_391",
        "bg_oid": "navierBg_s23",
        "bg_registry": "ow-econ-hato-baoase-v1",
        "corridor": "Hato air arrival → leeward embarkation (Piscadera Bay) -> Baoase Luxury Resort (south coast, near Willemstad)",
        "market_label": "CURAÇAO",
        "title": "Curaçao: profitable from year one",
        "header_oid": "g3eec5122801_0_392",
        "title_oid": "g3eec5122801_0_394",
        "route_oid": "g3eec5122801_0_395",
        "summary_oid": "g3eec5122801_0_397",
    },
    8: {
        "slide_oid": "g3eec5122801_0_448",
        "bg_oid": "navierBg_s24",
        "bg_registry": "ow-econ-hato-sandals-v1",
        "corridor": "Hato air arrival → leeward embarkation (Piscadera Bay) -> Sandals Royal Curaçao (Spanish Water / Santa Barbara)",
        "market_label": "CURAÇAO",
        "title": "Curaçao: Sandals gateway corridor",
        "header_oid": "g3eec5122801_0_449",
        "title_oid": "g3eec5122801_0_451",
        "route_oid": "g3eec5122801_0_452",
        "summary_oid": "g3eec5122801_0_454",
    },
    9: {
        "slide_oid": "g3eec5122801_0_505",
        "bg_oid": "navierBg_s25",
        "bg_registry": "ow-econ-willemstad-sandals-v1",
        "corridor": "Willemstad / Sint Anna Bay (cruise mega-pier + Queen Emma waterfront) -> Sandals Royal Curaçao (Spanish Water / Santa Barbara)",
        "market_label": "CURAÇAO",
        "title": "Curaçao: cruise-pier feed",
        "header_oid": "g3eec5122801_0_506",
        "title_oid": "g3eec5122801_0_508",
        "route_oid": "g3eec5122801_0_509",
        "summary_oid": "g3eec5122801_0_511",
    },
}

MARKET_SLIDES = {
    5: {
        "slide_oid": "g3eec5122801_0_106",
        "title_oid": "g3eec5122801_0_110",
        "subtitle_oid": "g3eec5122801_0_111",
        "title": "Curaçao — captive resort mesh (grounded)",
        "subtitle": "Airport, cruise-pier and inter-resort legs on sealed leeward geometry.",
    },
    6: {
        "slide_oid": "g3eec5122801_0_201",
        "title_oid": "g3eec5122801_0_205",
        "subtitle_oid": "g3eec5122801_0_206",
        "title": "Curaçao — premium network width",
        "subtitle": "Hato gateway + UNESCO waterfront feeds into the resort coast.",
    },
    7: {
        "slide_oid": "g3eec5122801_0_296",
        "title_oid": "g3eec5122801_0_300",
        "subtitle_oid": "g3eec5122801_0_304",
        "title": "ABC scale vision — island-to-island (roadmap)",
        "subtitle": "Bonaire + Aruba legs flagged amber-dashed; Quanta-LR cross-island reach.",
    },
}

EXPECTED_SLIDE_COUNT = 25
EDITED_SLIDES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]


def element_or_fallback(golden: dict, oid: str) -> dict:
    el = golden_element(golden, oid)
    if el:
        return el
    raise KeyError(f"missing golden element {oid}")


def fmt_usd(n: float) -> str:
    return f"${n:,.0f}"


def slide2_exists(presentation_id: str) -> bool:
    pres = slides_service().presentations().get(presentationId=presentation_id).execute()
    return any(slide.get("objectId") == "narr2_page" for slide in pres.get("slides", []))


def build_narrative_paint_ops() -> list[dict]:
    binding = load_json(NARRATIVE_BINDING_PATH)
    narrative = load_json(NARRATIVE_JSON_PATH)
    return build_narr2_paint_ops(
        binding, narrative, deck_key=DECK, source_name=NARRATIVE_JSON_PATH.name
    )


def find_corridor_mid(corridor: str) -> dict:
    agg = load_json(AGG_PATH)
    for row in agg.get("rows", []):
        if row.get("corridor") == corridor:
            mid = row.get("mid", {})
            if mid.get("revenue_per_boat_yr"):
                return mid
    raise SystemExit(f"corridor not found in agg: {corridor}")


def econ_value_map(econ: dict) -> dict[str, str]:
    cc = econ["cost_components"]
    rev = econ["revenue_per_boat_yr"]
    opex = econ["annual_opex"]
    profit = econ["ebitda_per_boat_yr"]
    margin_pct = int(round(econ["margin"] * 100))
    payback = f"{econ['payback_years']:.1f} yrs" if econ.get("payback_years") else "—"
    return {
        "trips_per_day": str(econ["trips_per_day"]),
        "operating_days": str(econ["assumptions"]["operating_days_yr"]),
        "revenue_legs": f"{int(econ['assumptions']['revenue_leg_pct'] * 100)}%",
        "seats_per_trip": str(round(econ["pax_per_trip"], 1)),
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
        "result_capex": "$1,000,000",
        "result_payback": payback,
        "result_co2": f"{econ['co2_saved_t_per_boat_yr']:.1f} t",
    }


def route_line(corridor: str, econ: dict) -> str:
    parts = corridor.split(" -> ", 1)
    left = parts[0].strip()
    right = parts[1].strip() if len(parts) > 1 else ""
    nm = econ.get("nm") or econ.get("distance_nm")
    nm_s = f"~{nm:g} nm" if nm else "sealed corridor"
    return f"{left} → {right}  ·  {nm_s}  ·  N30 Pioneer II (8 seats)"


def publish_assets() -> dict[str, str]:
    from deck_autonomy_sync import publish_assets_to_drive  # type: ignore

    registry_path = ROOT / "assets/ASSET-REGISTRY.json"
    registry = load_json(registry_path)
    assets = registry.setdefault("assets", {})
    econ_specs = [
        ("ow-econ-hato-baoase-v1", "assets/backgrounds/markets/curacao/ow-econ-hato-baoase-tier-a-v1.png", 8, "navierBg_s23"),
        ("ow-econ-hato-sandals-v1", "assets/backgrounds/markets/curacao/ow-econ-hato-sandals-tier-a-v1.png", 9, "navierBg_s24"),
        ("ow-econ-willemstad-sandals-v1", "assets/backgrounds/markets/curacao/ow-econ-willemstad-sandals-tier-a-v1.png", 10, "navierBg_s25"),
    ]
    for key, local_bg, slide_idx, target_oid in econ_specs:
        assets[key] = {
            **assets.get(key, {}),
            "role": "econ_market_bg",
            "scope": "market",
            "partner": DECK,
            "market_slug": "curacao-curacao",
            "atlas_city_id": "curacao-curacao",
            "local_path": f"deck-studio/{local_bg}",
            "status": assets.get(key, {}).get("status", "checked_in"),
            "composited": False,
            "license": "navier-internal",
            "used_by": [{"deck": DECK, "slide_index": slide_idx, "target_object_id": target_oid}],
        }
    write_json(registry_path, registry)
    publish_assets_to_drive(registry_path)
    registry = load_json(registry_path)
    keys = (
        "ocean-whisperer-logo",
        "ow-econ-hato-baoase-v1",
        "ow-econ-hato-sandals-v1",
        "ow-econ-willemstad-sandals-v1",
        "ow-cover-hero",
        "ow-three-cs-bg",
        "ow-value-prop-bg",
        "ow-tam-bg",
        "ow-partner-roles-bg",
    )
    urls: dict[str, str] = {}
    for key in keys:
        url = registry["assets"].get(key, {}).get("source_url")
        if url:
            urls[key] = url
    atlas_doc = load_slide_bindings(DECK)
    for bind in image_bindings_list(atlas_doc, roles={"atlas_route_screenshot"}):
        url = registry["assets"].get(bind["registry"], {}).get("source_url")
        if url:
            urls[bind["registry"]] = url
    return urls


def build_narrative(partner: dict) -> dict[tuple[str, str], str]:
    hero = partner["hero"]
    phases = partner["phases"]
    link_doc = load_json(SLIDE_LINK_BINDINGS_PATH)
    close_link = link_doc.get("close_atlas_link", {})
    narrative: dict[tuple[str, str], str] = {
        ("p1", "p1_i8"): hero["title"],
        ("p1", "p1_i9"): hero["subtitle"],
        (SLIDE3_OID, "g3eec5122801_0_2"): "OCEAN WHISPERER",
        (SLIDE3_OID, "g3eec5122801_0_4"): "Curaçao captive resort mesh — air to water",
        (SLIDE3_OID, "g3eec5122801_0_14"): "Hospitality ladder — rising rungs, no platform revenue (5-rung captive frame).",
        (SLIDE10_OID, "g3eec5122801_0_565"): "A captive revenue layer for an aviation-luxury brand",
        (SLIDE10_OID, "g3eec5122801_0_567"): (
            "Read it bottom-up: the fare a Navier boat collects today on Curaçao's resort coast, "
            "the WIDTH a faster product unlocks — then the whole journey wallet Ocean Whisperer monetizes."
        ),
        ("g3ea5e0fb254_4_357", "g3ea5e0fb254_4_361"): "You own the brand. We operate the fleet.",
        ("g3ea5e0fb254_4_444", "g3ea5e0fb254_4_447"): (
            f"1.  {phases[0]['label']} — {phases[0]['rationale']}\n"
            f"2.  {phases[1]['label']} — {phases[1]['rationale']}\n"
            f"3.  {phases[2]['label']} — {phases[2]['rationale']}"
        ),
        ("g3ea5e0fb254_4_330", "g3ea5e0fb254_4_330"): "Explore the Ocean Whisperer marine network",
        ("g3ea5e0fb254_4_331", "g3ea5e0fb254_4_331"): close_link.get(
            "body_text",
            "Open the Navier × Ocean Whisperer Atlas and pick the first grounded corridor.",
        ),
    }
    for spec in MARKET_SLIDES.values():
        narrative[(spec["slide_oid"], spec["title_oid"])] = spec["title"]
        narrative[(spec["slide_oid"], spec["subtitle_oid"])] = spec["subtitle"]
    return narrative


def slide3_kpi_map() -> dict[str, str]:
    return dict(load_json(KPI_PATH)["slide3_width_kpis"])


def slide10_tam_map() -> dict[str, str]:
    kpi = load_json(KPI_PATH)
    t = kpi["slide10_tam"]
    growth = load_json(GROWTH_PATH)
    g = growth.get("grounded", {})
    som_m = g.get("SOM_floor_navier_transport_rev_yr", 0) / 1e6
    sam_m = g.get("SAM_navier_transport_rev_yr", {}).get("mid", 0) / 1e6
    tam_m = (g.get("marine_mobility_tam_yr") or {}).get("mid", 0) / 1e6
    jgmv_m = (g.get("TAM_journey_gmv_yr") or {}).get("mid", 0) / 1e6
    return {
        "som_value": t["som_floor_display"],
        "som_caption": f"SOM floor — captive resort mesh ({som_m:.0f}M grounded today)",
        "sam_value": t["sam_mid_display"],
        "sam_caption": f"SAM mid — induced demand + network width ({sam_m:.0f}M Navier rev)",
        "tam_value": t["tam_marine_mid_display"],
        "tam_caption": f"Marine mobility TAM — induced transfer wallet ({tam_m:.0f}M)",
        "journey_gmv_value": t["tam_journey_gmv_mid_display"],
        "journey_gmv_caption": f"Journey GMV — food + stays + experiences ({jgmv_m:.0f}M)",
        "platform_value": "—",
        "platform_caption": "Captive hospitality — platform revenue rung not applicable",
    }


def build_editplan(presentation_id: str, asset_urls: dict[str, str]) -> dict:
    golden = load_json(GOLDEN)
    partner = load_json(PARTNER_PATH)
    grab_binding = load_json(ROOT / "decks/grab/economics-binding.json")
    ops: list[dict] = []

    for bind in IMAGE_BINDINGS:
        url = asset_urls.get(bind["registry"])
        if url:
            ops.append(
                image_replace_op(
                    bind["slide_oid"], bind["target_oid"], url,
                    op_key=f"ow-img-{bind['registry']}",
                    source_pointer=f"ASSET-REGISTRY {bind['registry']}",
                    method=bind.get("method", "CENTER_CROP"),
                )
            )

    if slide2_exists(presentation_id):
        ops.extend(build_narrative_paint_ops())
        url = asset_urls.get("ow-value-prop-bg")
        if url:
            ops.append(
                image_replace_op(
                    "narr2_page", "narr2_bg_img", url,
                    op_key="ow-img-ow-value-prop-bg",
                    source_pointer="ASSET-REGISTRY ow-value-prop-bg",
                    method="CENTER_CROP",
                )
            )

    for (slide_oid, target_oid), text in build_narrative(partner).items():
        if target_oid in ROUTE_TARGET_OIDS:
            continue
        el = {**element_or_fallback(golden, target_oid), "char_budget": max(element_or_fallback(golden, target_oid).get("char_budget", 12), len(text) + 4)}
        ops.extend(text_replace_ops(slide_oid, target_oid, text, el, op_prefix=f"ow-narr-{target_oid}", source_pointer=PARTNER_PATH.name))

    errs = validate_market_route_bindings(DECK, partner_json_path=ROOT.parent / "data-clean/partners/ocean-whisperer.json", golden=golden)
    if not errs:
        ops.extend(
            build_market_route_ops(
                golden, DECK,
                partner_json_path=ROOT.parent / "data-clean/partners/ocean-whisperer.json",
                element_lookup=element_or_fallback,
            )
        )
    else:
        raise SystemExit("market-route-bindings invalid:\n" + "\n".join(errs))

    kpi = slide3_kpi_map()
    for oid, key in SLIDE3_KPI_FIELDS:
        text = kpi[key]
        el = {**element_or_fallback(golden, oid), "char_budget": max(len(text) + 8, 24)}
        align = "CENTER" if oid in SLIDE3_KPI_CAPTION_OIDS else None
        ops.extend(
            text_replace_ops(
                SLIDE3_OID, oid, text, el,
                op_prefix=f"ow-slide3-{oid}", source_pointer=KPI_PATH.name,
                alignment=align,
            )
        )

    tam = slide10_tam_map()
    for oid, key in SLIDE10_TAM_FIELDS:
        text = tam[key]
        el = {**element_or_fallback(golden, oid), "char_budget": max(len(text) + 8, 24)}
        ops.extend(text_replace_ops(SLIDE10_OID, oid, text, el, op_prefix=f"ow-slide10-{oid}", source_pointer=GROWTH_PATH.name))

    binding_doc = load_slide_bindings(DECK)
    bind_errs = validate_bindings(binding_doc)
    if bind_errs:
        raise SystemExit("slide-image-bindings invalid:\n" + "\n".join(bind_errs))
    for bind in image_bindings_list(binding_doc):
        url = asset_urls.get(bind["registry"])
        if url:
            ops.append(
                image_replace_op(
                    bind["slide_oid"], bind["target_oid"], url,
                    op_key=f"ow-img-{bind['registry']}",
                    source_pointer=f"ASSET-REGISTRY {bind['registry']}",
                    method=bind.get("method", "CENTER_CROP"),
                )
            )

    for slide_idx, spec in ECON_SLIDES.items():
        url = asset_urls.get(spec["bg_registry"])
        if url:
            ops.append(
                image_replace_op(
                    spec["slide_oid"], spec["bg_oid"], url,
                    op_key=f"ow-bg-{spec['bg_registry']}-s{slide_idx}",
                    source_pointer=f"ASSET-REGISTRY {spec['bg_registry']}",
                    method="CENTER_CROP",
                )
            )
        econ = find_corridor_mid(spec["corridor"])
        header = f"WHAT ONE BOAT EARNS · {spec['market_label']}"
        route = route_line(spec["corridor"], econ)
        for oid, text in (
            (spec["header_oid"], header),
            (spec["title_oid"], spec["title"]),
            (spec["route_oid"], route),
        ):
            base = element_or_fallback(golden, oid)
            el = {**base, "char_budget": max(ECON_HEADER_CHAR_BUDGET, len(text) + 4)}
            ops.extend(text_replace_ops(spec["slide_oid"], oid, text, el, op_prefix=f"ow-econ-text-{oid}", source_pointer=AGG_PATH.name))
        rev, opex, profit = econ["revenue_per_boat_yr"], econ["annual_opex"], econ["ebitda_per_boat_yr"]
        margin_pct = int(round(econ["margin"] * 100))
        payback = f"{econ['payback_years']:.1f} yrs"
        summary = f"{fmt_usd(rev)} revenue  −  {fmt_usd(opex)} run cost  =  {fmt_usd(profit)} profit / boat·yr  ·  {margin_pct}% margin  ·  {payback}"
        ops.extend(text_replace_ops(spec["slide_oid"], spec["summary_oid"], summary, element_or_fallback(golden, spec["summary_oid"]), op_prefix=f"ow-econ-summary-{slide_idx}", source_pointer=AGG_PATH.name))
        binding_slide = next(s for s in grab_binding["economics_slides"] if s["slide_index"] == slide_idx)
        values = econ_value_map(econ)
        for field_key, text in values.items():
            field = binding_slide["fields"].get(field_key)
            if field and field.get("value_object_id"):
                ops.extend(econ_value_replace_ops(spec["slide_oid"], field["value_object_id"], text, op_prefix=f"ow-econ-val-{field_key}-{slide_idx}", source_pointer=AGG_PATH.name))

    ops.extend(build_deck_link_ops(DECK, op_prefix="ow-deck-link"))

    return {
        "deck_key": DECK,
        "presentation_id": presentation_id,
        "mode": "slides_api_batch_update",
        "archetype_variant": "hospitality",
        "wave": "wave-2",
        "request_summary": "Ocean Whisperer wave-2: cover+slide2+images, 3 econ, TAM/partner-roles plates, links",
        "safety": {"no_pptx_roundtrip": True, "no_full_deck_replace": True, "preserve_object_ids": True, "human_review_required_for_external_send": True},
        "operations": ops,
        "qa": {"leak_denylist": LEAK_DENYLIST},
        "qa_gates": ["drift_gate", "leak_scan", "render_export"],
        "created_at": utc_now(),
    }


def run_qa(presentation_id: str, plan: dict) -> dict:
    leak_edited = leak_scan(presentation_id, LEAK_DENYLIST, slide_indexes=EDITED_SLIDES)
    thumb_dir = ROOT / f"decks/{DECK}/qa-receipts/thumbnails"
    thumbs = export_thumbnails(presentation_id, thumb_dir, max_slides=EXPECTED_SLIDE_COUNT)
    status = "pass" if leak_edited["pass"] else "fail"
    receipt = {
        "deck_key": DECK,
        "presentation_id": presentation_id,
        "live_deck_url": f"https://docs.google.com/presentation/d/{presentation_id}/edit",
        "status": status,
        "generated_at": utc_now(),
        "operations": len(plan.get("operations", [])),
        "leak_scan_edited_scope": leak_edited,
        "thumbnails": thumbs,
        "wave": "wave-2",
    }
    write_json(ROOT / f"decks/{DECK}/qa-receipts/live-apply-receipt.json", receipt)
    return receipt


def cmd_insert_slide2(presentation_id: str) -> int:
    if slide2_exists(presentation_id):
        print(json.dumps({"status": "already_present"}, indent=2))
        return 0
    gold_create = load_json(GOLD_SLIDE2_CREATE_PATH)
    applied = apply_slides_requests(presentation_id, gold_create["requests"], chunk_size=12)
    print(json.dumps({"applied_requests": applied}, indent=2))
    return 0


def cmd_run_wave2(presentation_id: str) -> int:
    print("1/6 Insert slide 2 (if missing)...")
    cmd_insert_slide2(presentation_id)
    print("2/6 Publish assets...")
    urls = publish_assets()
    missing = [
        k
        for k in (
            "ow-cover-hero",
            "ow-three-cs-bg",
            "ow-value-prop-bg",
            "ow-tam-bg",
            "ow-partner-roles-bg",
            "ow-econ-hato-baoase-v1",
        "ow-econ-hato-sandals-v1",
        "ow-econ-willemstad-sandals-v1",
            "ocean-whisperer-logo",
        )
        if k not in urls
    ]
    if missing:
        raise SystemExit(f"Missing source_url for: {missing} — run deck_ocean_whisperer_images.py generate-all && publish")
    print(f"   resolved: {list(urls.keys())}")
    print("3/6 Build editplan...")
    plan = build_editplan(presentation_id, urls)
    write_json(ROOT / f"decks/{DECK}/deck.editplan.json", plan)
    print(f"   operations: {len(plan['operations'])}")
    print("4/6 Apply...")
    applied = apply_plan(plan, chunk_size=35)
    plan["applied_at"] = utc_now()
    plan["status"] = "applied"
    write_json(ROOT / f"decks/{DECK}/deck.editplan.json", plan)
    print(f"   applied {applied} requests")
    print("5/6 QA...")
    receipt = run_qa(presentation_id, plan)
    print(json.dumps(receipt, indent=2))
    cfg = load_json(ROOT / f"decks/{DECK}/deck.config.json")
    cfg["deck_id"] = presentation_id
    cfg["live_deck_url"] = receipt["live_deck_url"]
    cfg["wave"] = "wave-2"
    write_json(ROOT / f"decks/{DECK}/deck.config.json", cfg)
    return 0 if receipt["status"] == "pass" else 1


def cmd_run_all() -> int:
    pid = copy_gold_deck("Ocean Whisperer × Navier")
    return cmd_run_wave2(pid)


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Ocean Whisperer deck builder (wave-2)")
    ap.add_argument("command", choices=["run-all", "run-wave2", "insert-slide2", "publish-assets", "build-editplan", "apply", "qa"])
    ap.add_argument("--presentation-id")
    args = ap.parse_args()
    cfg = load_json(ROOT / f"decks/{DECK}/deck.config.json")
    pid = args.presentation_id or cfg.get("deck_id")
    if args.command == "publish-assets":
        print(json.dumps(publish_assets(), indent=2))
        return 0
    if args.command == "insert-slide2":
        if not pid:
            raise SystemExit("need --presentation-id")
        return cmd_insert_slide2(pid)
    if args.command == "run-all":
        return cmd_run_all()
    if args.command == "run-wave2":
        if not pid:
            raise SystemExit("need --presentation-id")
        return cmd_run_wave2(pid)
    if args.command == "build-editplan":
        if not pid:
            raise SystemExit("need --presentation-id")
        plan = build_editplan(pid, publish_assets())
        write_json(ROOT / f"decks/{DECK}/deck.editplan.json", plan)
        print(json.dumps({"operations": len(plan["operations"])}, indent=2))
        return 0
    if args.command == "apply":
        plan = load_json(ROOT / f"decks/{DECK}/deck.editplan.json")
        print(f"applied {apply_plan(plan, chunk_size=35)}")
        return 0
    if args.command == "qa":
        plan = load_json(ROOT / f"decks/{DECK}/deck.editplan.json")
        receipt = run_qa(pid, plan)
        print(json.dumps(receipt, indent=2))
        return 0 if receipt["status"] == "pass" else 1
    return 1


if __name__ == "__main__":
    raise SystemExit(main())