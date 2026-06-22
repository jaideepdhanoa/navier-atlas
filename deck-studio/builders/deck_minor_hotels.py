#!/usr/bin/env python3
"""Minor Hotels operator-developer deck: copy gold → captive WIDTH editplan → apply → QA."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDERS = ROOT / "builders"
sys.path.insert(0, str(BUILDERS))

from deck_bolt_pilot import (  # noqa: E402
    apply_plan,
    copy_gold_deck,
    drift_gate,
    export_thumbnails,
    golden_element,
    golden_slide_oid,
    leak_scan,
    load_json,
    utc_now,
    write_json,
)
from deck_edit_ops import econ_value_replace_ops, image_replace_op, text_replace_ops  # noqa: E402

DECK = "minor-hotels"
GOLDEN = ROOT / "decks/grab/golden-template-map.json"
KPI_PATH = ROOT / "decks/minor-hotels/slide3-kpis-minor-hotels.json"
BINDING_PATH = ROOT / "decks/minor-hotels/economics-binding.json"
GROWTH_PATH = ROOT.parent / "finance/recal/growth-minor-hotels.json"
AGG_PATH = ROOT.parent / "finance/recal/agg-minor-hotels.json"
PARTNER_PATH = ROOT.parent / "partner-pitch/partners/minor-hotels.json"

LEAK_DENYLIST = [
    "Grab",
    "Uber",
    "Bolt",
    "Careem",
    "Singapore",
    "Sentosa",
    "super-app",
    "10% capture",
    "Koh Samui",
    "Bangkok",
    "Chao Phraya",
]

NARRATIVE_BINDING_PATH = ROOT / "decks/minor-hotels/narrative-binding.json"
NARRATIVE_JSON_PATH = ROOT / "decks/minor-hotels/narrative-slide2-minor-hotels.json"
SLIDE3_OID = "g3eec5122801_0_0"
SLIDE10_OID = "g3eec5122801_0_562"

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

ECON_SLIDES: dict[int, dict] = {
    7: {
        "slide_oid": "g3eec5122801_0_391",
        "bg_oid": "navierBg_s23",
        "bg_registry": "econ-phuket-v1",
        "corridor": "Phuket (Royal Phuket Marina) -> Phang Nga Bay / James Bond Island",
        "market_label": "PHUKET / PHANG NGA",
        "title": "Phuket: profitable from year one",
        "route_line": "Royal Phuket Marina → Phang Nga Bay  ·  ~20 nm  ·  N30 Pioneer II (8 seats)",
        "header_oid": "g3eec5122801_0_392",
        "title_oid": "g3eec5122801_0_394",
        "route_oid": "g3eec5122801_0_395",
        "summary_oid": "g3eec5122801_0_397",
    },
    8: {
        "slide_oid": "g3eec5122801_0_448",
        "bg_oid": "navierBg_s24",
        "bg_registry": "econ-bali-v1",
        "corridor": "Bali (Benoa / Sanur) -> Nusa Penida / Lembongan",
        "market_label": "BALI",
        "title": "Bali: profitable from year one",
        "route_line": "Benoa / Sanur → Nusa Penida  ·  ~14 nm  ·  N30 Pioneer II (8 seats)",
        "header_oid": "g3eec5122801_0_449",
        "title_oid": "g3eec5122801_0_451",
        "route_oid": "g3eec5122801_0_452",
        "summary_oid": "g3eec5122801_0_454",
    },
    9: {
        "slide_oid": "g3eec5122801_0_505",
        "bg_oid": "navierBg_s25",
        "bg_registry": "econ-uae-dubai-harbour",
        "corridor": "Dubai Harbour Marina -> Palm Jumeirah Marina West",
        "market_label": "PALM JUMEIRAH",
        "title": "Palm Jumeirah: profitable from year one",
        "route_line": "Dubai Harbour → Palm West Marina  ·  ~2 nm  ·  N30 Pioneer II (8 seats)",
        "header_oid": "g3eec5122801_0_506",
        "title_oid": "g3eec5122801_0_508",
        "route_oid": "g3eec5122801_0_509",
        "summary_oid": "g3eec5122801_0_511",
    },
}

MARKET_SLUGS = ("phuket-phang-nga", "bali", "palm-jumeirah")
MARKET_SLIDE_OIDS = {
    "phuket-phang-nga": {
        "slide_oid": "g3eec5122801_0_106",
        "title_oid": "g3eec5122801_0_110",
        "subtitle_oid": "g3eec5122801_0_111",
        "routes_oid": "g3eec5122801_0_114",
    },
    "bali": {
        "slide_oid": "g3eec5122801_0_201",
        "title_oid": "g3eec5122801_0_205",
        "subtitle_oid": "g3eec5122801_0_206",
        "routes_oid": "g3eec5122801_0_209",
    },
    "palm-jumeirah": {
        "slide_oid": "g3eec5122801_0_296",
        "title_oid": "g3eec5122801_0_300",
        "subtitle_oid": "g3eec5122801_0_304",
        "routes_oid": "g3eec5122801_0_301",
    },
}


def element_or_fallback(golden: dict, oid: str) -> dict:
    el = golden_element(golden, oid)
    if el:
        return el
    raise KeyError(f"missing golden element {oid}")


def fmt_usd(n: float) -> str:
    return f"${n:,.0f}"


def publish_assets() -> dict[str, str]:
    registry_path = ROOT / "assets/ASSET-REGISTRY.json"
    registry = load_json(registry_path)
    assets = registry.setdefault("assets", {})
    logo_manifest = load_json(ROOT / "assets/logos/LOGO-MANIFEST.json")
    mh = logo_manifest["decks"]["minor-hotels"]
    fid = mh.get("drive_file_id")
    assets["minor-hotels-logo"] = {
        "role": "partner_logo",
        "scope": "partner",
        "partner": "minor-hotels",
        "status": "published",
        "local_path": mh["logo_path"],
        "drive_file_id": fid,
        "source_url": (
            f"https://drive.google.com/uc?export=download&id={fid}"
            if fid
            else mh.get("source_url")
        ),
        "license": mh.get("license", "minor-hotels-brand"),
        "provenance": "official_newsroom_press_asset",
        "reproducible": True,
        "notes": "Minor Hotels masterbrand wordmark — PR #80 banked.",
        "used_by": [
            {"deck": DECK, "slide_index": 1, "slide_object_id": "p1", "target_object_id": "p1_i5"}
        ],
        "composited": False,
        "captured_at": utc_now(),
    }
    write_json(registry_path, registry)

    from deck_autonomy_sync import publish_assets_to_drive  # type: ignore

    publish_assets_to_drive(registry_path)
    registry = load_json(registry_path)
    keys = ("minor-hotels-logo", "econ-phuket-v1", "econ-bali-v1", "econ-uae-dubai-harbour")
    urls: dict[str, str] = {}
    for key in keys:
        asset = assets.get(key, registry["assets"].get(key, {}))
        url = asset.get("source_url")
        if not url and asset.get("local_path"):
            raise SystemExit(f"Asset {key} missing source_url after publish — block apply")
        if url:
            urls[key] = url
    write_json(registry_path, registry)
    return urls


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


def market_by_slug(partner: dict, slug: str) -> dict:
    for m in partner.get("markets", []):
        if m.get("slug") == slug:
            return m
    raise SystemExit(f"market slug not found: {slug}")


def route_list_text(market: dict, *, max_routes: int = 4) -> str:
    lines: list[str] = []
    for j in market.get("journeys_unlocked", [])[:max_routes]:
        frm = j["from"].split("(")[0].strip()
        to = j["to"].replace(" Resort", "").replace("Resort", "").strip()
        nm = j.get("distance_nm")
        rclass = j.get("_route_class", "?")
        tag = {"A": "gateway transfer", "B": "inter-resort hop", "C": "signature excursion"}.get(
            rclass, "captive route"
        )
        nm_s = f"~{nm:g} nm" if nm else "sealed corridor"
        lines.append(f"▸  {frm} → {to}\n      {nm_s} · {tag}")
    return "\n".join(lines)


def slide3_kpi_map() -> dict[str, str]:
    kpi = load_json(KPI_PATH)
    return dict(kpi["slide3_width_kpis"])


def slide10_tam_map() -> dict[str, str]:
    kpi = load_json(KPI_PATH)
    t = kpi["slide10_tam"]
    growth = load_json(GROWTH_PATH)
    g = growth.get("grounded", {})
    som_m = g.get("SOM_floor_navier_transport_rev_yr", 0) / 1e6
    sam_m = g.get("SAM_navier_transport_rev_yr", {}).get("mid", 0) / 1e6
    tam_m = g.get("TAM_journey_gmv_yr", {}).get("mid", 0) / 1e6
    plat_m = g.get("partner_platform_rev_yr", {}).get("mid", 0) / 1e6
    return {
        "som_value": t["som_floor_display"],
        "som_caption": f"SOM floor — captive ~90% capture, {som_m:.0f}M grounded today",
        "sam_value": t["sam_mid_display"],
        "sam_caption": f"SAM mid — WIDTH scales keys + clusters ({sam_m:.0f}M Navier rev)",
        "tam_value": t["tam_journey_gmv_mid_display"],
        "tam_caption": f"TAM — total journey GMV through Minor guest wallet ({tam_m:.0f}M)",
        "journey_gmv_value": t["tam_journey_gmv_mid_display"],
        "journey_gmv_caption": "Journey GMV routed through the Minor coastal network",
        "platform_value": t["partner_platform_rev_mid_display"],
        "platform_caption": f"Minor ancillary revenue on resort journey GMV ({plat_m:.0f}M)",
    }


def narrative_element(text: str) -> dict:
    return {
        "char_budget": max(len(text) + 24, 48),
        "style": {"font": "Exo 2", "sizePt": 11, "bold": False, "color": [1.0, 1.0, 1.0]},
    }


def build_narrative_paint_ops() -> list[dict]:
    binding = load_json(NARRATIVE_BINDING_PATH)
    narrative = load_json(NARRATIVE_JSON_PATH)
    slide_oid = binding["slide_object_id"]
    ops: list[dict] = []

    for field_key, pin in binding["fields"].items():
        if not pin.get("present"):
            continue
        text = pin["static"] if pin.get("static") else (narrative.get(field_key) or "")
        if not text:
            continue
        ops.extend(
            text_replace_ops(
                slide_oid,
                pin["object_id"],
                text,
                narrative_element(text),
                op_prefix=f"mh-narr2-{pin['object_id']}",
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
                    op_prefix=f"mh-narr2-{beat_pin[oid_key]}",
                    source_pointer=NARRATIVE_JSON_PATH.name,
                )
            )
    return ops


def build_narrative(partner: dict) -> dict[tuple[str, str], str]:
    hero = partner["hero"]
    thesis = partner["network_thesis"]
    ask = partner["the_ask"]
    close = partner["close"]
    phases = partner["phases"]

    narrative: dict[tuple[str, str], str] = {
        ("p1", "p1_i8"): hero["title"],
        ("p1", "p1_i9"): hero["subtitle"],
        (SLIDE3_OID, "g3eec5122801_0_2"): "MINOR HOTELS",
        (SLIDE3_OID, "g3eec5122801_0_4"): (
            "109 coastal properties · 13 clusters — captive transfer WIDTH"
        ),
        (
            SLIDE3_OID,
            "g3eec5122801_0_14",
        ): "Captive economics — headroom scales with keys and openings, not city mobility share.",
        (SLIDE10_OID, "g3eec5122801_0_565"): "A captive revenue layer across Minor's coastal portfolio",
        (
            SLIDE10_OID,
            "g3eec5122801_0_567",
        ): (
            "Read it bottom-up: the fare a Navier boat collects today, the WIDTH a faster product unlocks "
            "— then the whole journey Minor monetizes around every guest arrival."
        ),
        ("g3ea5e0fb254_4_357", "g3ea5e0fb254_4_361"): "You own the guests. We operate the fleet.",
        (
            "g3ea5e0fb254_4_357",
            "g3ea5e0fb254_4_362",
        ): (
            f"▸  Minor Hotels — {ask['partner_brings'].split(';')[0].strip()}.\n"
            f"▸  Navier — {ask['navier_brings'].split(',')[0].strip()}.\n"
            f"▸  Together — {ask['together']}"
        ),
        (
            "g3ea5e0fb254_4_444",
            "g3ea5e0fb254_4_447",
        ): (
            f"1.  {phases[0]['label']} — {phases[0]['rationale']}\n"
            f"2.  {phases[1]['label']} — {phases[1]['rationale']}\n"
            f"3.  {phases[2]['label']} — {phases[2]['rationale']}"
        ),
        ("g3ea5e0fb254_4_330", "g3ea5e0fb254_4_330"): "Explore the Minor Hotels marine network",
        (
            "g3ea5e0fb254_4_331",
            "g3ea5e0fb254_4_331",
        ): (
            f"{close['body']} Open the Navier × Minor Hotels Atlas, pick the first grounded cluster, "
            "and let's turn every guest arrival into a signature you own."
        ),
    }

    market_copy = {
        "phuket-phang-nga": (
            "Phuket / Phang Nga — flagship captive floor",
            "Eight Andaman properties on sealed geometry — gateway, inter-resort, and excursion.",
        ),
        "bali": (
            "Bali south coast — honest captive floor",
            "Three grounded properties — Benoa gateway and Nusa Penida day-charters.",
        ),
        "palm-jumeirah": (
            "Palm Jumeirah — premium discretionary marine",
            "Three crescent properties — BP-grounded leisure-marine at UAE premium fares.",
        ),
    }
    for slug, oids in MARKET_SLIDE_OIDS.items():
        market = market_by_slug(partner, slug)
        title, subtitle = market_copy[slug]
        narrative[(oids["slide_oid"], oids["title_oid"])] = title
        narrative[(oids["slide_oid"], oids["subtitle_oid"])] = subtitle
        narrative[(oids["slide_oid"], oids["routes_oid"])] = route_list_text(market)

    return narrative


def pull_manifest(presentation_id: str) -> None:
    cfg_path = ROOT / f"decks/{DECK}/deck.config.json"
    cfg = load_json(cfg_path)
    cfg["deck_id"] = presentation_id
    cfg["live_deck_url"] = f"https://docs.google.com/presentation/d/{presentation_id}/edit"
    cfg["last_pulled_at"] = utc_now()
    cfg["notes"] = "Minor Hotels operator-developer deck — copied from gold template, applied via deck_minor_hotels.py"
    cfg["generation_type"] = "create-from-grab-gold-template"
    cfg.setdefault("cover_logos", {}).setdefault("partner_logo", {})["status"] = "banked"
    write_json(cfg_path, cfg)
    subprocess.run(
        [sys.executable, "-m", "deck_studio", "pull", "--root", str(ROOT), "--deck", DECK, "--mode", "full"],
        cwd=str(BUILDERS),
        check=True,
    )


def build_editplan(presentation_id: str, asset_urls: dict[str, str]) -> dict:
    golden = load_json(GOLDEN)
    partner = load_json(PARTNER_PATH)
    binding = load_json(BINDING_PATH)
    grab_binding = load_json(ROOT / "decks/grab/economics-binding.json")
    narrative = build_narrative(partner)
    ops: list[dict] = []
    slide1 = golden_slide_oid(golden, 1)

    if asset_urls.get("minor-hotels-logo"):
        ops.append(
            image_replace_op(
                slide1,
                "p1_i5",
                asset_urls["minor-hotels-logo"],
                op_key="mh-cover-partner-logo",
                source_pointer="ASSET-REGISTRY minor-hotels-logo",
                method="CENTER_INSIDE",
            )
        )

    ops.extend(build_narrative_paint_ops())

    for (slide_oid, target_oid), text in narrative.items():
        el = {
            **element_or_fallback(golden, target_oid),
            "char_budget": max(element_or_fallback(golden, target_oid).get("char_budget", 12), len(text) + 4),
        }
        ops.extend(
            text_replace_ops(
                slide_oid,
                target_oid,
                text,
                el,
                op_prefix=f"mh-narr-{target_oid}",
                source_pointer=str(PARTNER_PATH.name),
            )
        )

    kpi = slide3_kpi_map()
    for oid, key in SLIDE3_KPI_FIELDS:
        text = kpi[key]
        el = {**element_or_fallback(golden, oid), "char_budget": max(len(text) + 8, 24)}
        ops.extend(
            text_replace_ops(
                SLIDE3_OID, oid, text, el, op_prefix=f"mh-slide3-{oid}", source_pointer=KPI_PATH.name
            )
        )

    tam = slide10_tam_map()
    for oid, key in SLIDE10_TAM_FIELDS:
        text = tam[key]
        el = {**element_or_fallback(golden, oid), "char_budget": max(len(text) + 8, 24)}
        ops.extend(
            text_replace_ops(
                SLIDE10_OID, oid, text, el, op_prefix=f"mh-slide10-{oid}", source_pointer=GROWTH_PATH.name
            )
        )

    for slide_idx, spec in ECON_SLIDES.items():
        url = asset_urls.get(spec["bg_registry"])
        if url:
            ops.append(
                image_replace_op(
                    spec["slide_oid"],
                    spec["bg_oid"],
                    url,
                    op_key=f"mh-bg-{spec['bg_registry']}",
                    source_pointer=f"ASSET-REGISTRY {spec['bg_registry']}",
                    method="CENTER_CROP",
                )
            )
        header = f"WHAT ONE BOAT EARNS · {spec['market_label']}"
        for oid, text in (
            (spec["header_oid"], header),
            (spec["title_oid"], spec["title"]),
            (spec["route_oid"], spec["route_line"]),
        ):
            base = element_or_fallback(golden, oid)
            el = {**base, "char_budget": max(base.get("char_budget", 12), len(text) + 4)}
            ops.extend(
                text_replace_ops(
                    spec["slide_oid"],
                    oid,
                    text,
                    el,
                    op_prefix=f"mh-econ-text-{oid}",
                    source_pointer=spec["corridor"],
                )
            )
        econ = find_corridor_mid(spec["corridor"])
        rev = econ["revenue_per_boat_yr"]
        opex = econ["annual_opex"]
        profit = econ["ebitda_per_boat_yr"]
        margin_pct = int(round(econ["margin"] * 100))
        payback = f"{econ['payback_years']:.1f} yrs" if econ.get("payback_years") else "—"
        summary = (
            f"{fmt_usd(rev)} revenue  −  {fmt_usd(opex)} run cost  =  "
            f"{fmt_usd(profit)} profit / boat·yr  ·  {margin_pct}% margin  ·  {payback}"
        )
        base = element_or_fallback(golden, spec["summary_oid"])
        el = {**base, "char_budget": max(base.get("char_budget", 12), len(summary) + 4)}
        ops.extend(
            text_replace_ops(
                spec["slide_oid"],
                spec["summary_oid"],
                summary,
                el,
                op_prefix=f"mh-econ-summary-{spec['slide_oid']}",
                source_pointer=f"agg-minor-hotels.json :: {spec['corridor']}",
            )
        )
        binding_slide = next(s for s in grab_binding["economics_slides"] if s["slide_index"] == slide_idx)
        values = econ_value_map(econ)
        source = f"finance/recal/agg-minor-hotels.json mid {spec['corridor']}"
        for field_key, text in values.items():
            field = binding_slide["fields"].get(field_key)
            if not field or not field.get("value_object_id"):
                continue
            ops.extend(
                econ_value_replace_ops(
                    spec["slide_oid"],
                    field["value_object_id"],
                    text,
                    op_prefix=f"mh-econ-val-{field_key}-{slide_idx}",
                    source_pointer=source,
                )
            )

    return {
        "deck_key": DECK,
        "presentation_id": presentation_id,
        "mode": "slides_api_batch_update",
        "archetype_variant": "operator-developer",
        "request_summary": (
            "Minor Hotels: cover logo, slide2 Three C's, slide3 WIDTH KPIs, "
            "3 cluster slides, 3 flagship econ slides, captive TAM, close"
        ),
        "safety": {
            "no_pptx_roundtrip": True,
            "no_full_deck_replace": True,
            "preserve_object_ids": True,
            "human_review_required_for_external_send": True,
        },
        "operations": ops,
        "qa": {
            "leak_denylist": binding.get("leak_denylist", LEAK_DENYLIST),
            "G1_archetype_purity": 0,
        },
        "qa_gates": ["drift_gate", "leak_scan", "render_export", "G1_archetype_purity"],
        "created_at": utc_now(),
    }


EXPECTED_SLIDE_COUNT = 24
EDITED_SLIDES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]


def minor_drift_gate(presentation_id: str, plan: dict) -> dict:
    result = drift_gate(presentation_id, plan)
    result["pass"] = not result["missing_object_ids"] and result["slide_count"] == EXPECTED_SLIDE_COUNT
    result["expected_slide_count"] = EXPECTED_SLIDE_COUNT
    return result


def run_qa(presentation_id: str, plan: dict) -> dict:
    leak_edited = leak_scan(presentation_id, LEAK_DENYLIST, slide_indexes=EDITED_SLIDES)
    leak_full = leak_scan(presentation_id, LEAK_DENYLIST)
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
        "leak_scan_full_deck_advisory": leak_full,
        "thumbnails": thumbs,
        "G1_archetype_purity": 0,
    }
    write_json(ROOT / f"decks/{DECK}/qa-receipts/live-apply-receipt.json", receipt)
    return receipt


def cmd_run_all() -> int:
    print("1/6 Publish Minor Hotels deck assets...")
    urls = publish_assets()
    print(f"   urls: {list(urls.keys())}")

    print("2/6 Copy gold Grab deck...")
    pid = copy_gold_deck("Minor Hotels × Navier")
    print(f"   deck_id: {pid}")

    print("3/6 Pull manifest + build editplan...")
    pull_manifest(pid)
    plan = build_editplan(pid, urls)
    plan_path = ROOT / f"decks/{DECK}/deck.editplan.json"
    write_json(plan_path, plan)
    print(f"   operations: {len(plan['operations'])}")

    drift = minor_drift_gate(pid, plan)
    if not drift["pass"]:
        print(json.dumps(drift, indent=2), file=sys.stderr)
        raise SystemExit("Drift gate failed")
    print("   drift gate: pass")

    print("4/6 Apply editplan...")
    applied = apply_plan(plan, chunk_size=35)
    plan["applied_at"] = utc_now()
    plan["status"] = "applied"
    write_json(plan_path, plan)
    print(f"   applied {applied} requests")

    print("5/6 QA + thumbnails...")
    receipt = run_qa(pid, plan)
    print(json.dumps(receipt, indent=2))

    cfg = load_json(ROOT / f"decks/{DECK}/deck.config.json")
    cfg["deck_id"] = pid
    cfg["live_deck_url"] = receipt["live_deck_url"]
    cfg["last_pulled_at"] = utc_now()
    write_json(ROOT / f"decks/{DECK}/deck.config.json", cfg)
    return 0 if receipt["status"] == "pass" else 1


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Minor Hotels deck builder")
    ap.add_argument(
        "command",
        choices=["run-all", "publish-assets", "copy-gold", "build-editplan", "apply", "qa", "stub"],
    )
    ap.add_argument("--presentation-id")
    args = ap.parse_args()

    if args.command == "stub":
        plan = {
            "deck_key": DECK,
            "presentation_id": "pending-grok-create-or-bind",
            "mode": "slides_api_batch_update",
            "archetype_variant": "operator-developer",
            "operations": [],
            "created_at": utc_now(),
        }
        write_json(ROOT / f"decks/{DECK}/deck.editplan.json", plan)
        print(json.dumps({"deck": DECK, "mode": "stub"}, indent=2))
        return 0
    if args.command == "publish-assets":
        print(json.dumps(publish_assets(), indent=2))
        return 0
    if args.command == "copy-gold":
        pid = copy_gold_deck("Minor Hotels × Navier")
        pull_manifest(pid)
        print(pid)
        return 0
    if args.command == "build-editplan":
        cfg = load_json(ROOT / f"decks/{DECK}/deck.config.json")
        pid = args.presentation_id or cfg["deck_id"]
        urls = publish_assets()
        plan = build_editplan(pid, urls)
        write_json(ROOT / f"decks/{DECK}/deck.editplan.json", plan)
        print(json.dumps({"operations": len(plan["operations"]), "presentation_id": pid}, indent=2))
        return 0
    if args.command == "apply":
        plan = load_json(ROOT / f"decks/{DECK}/deck.editplan.json")
        n = apply_plan(plan, chunk_size=35)
        print(f"applied {n}")
        return 0
    if args.command == "qa":
        cfg = load_json(ROOT / f"decks/{DECK}/deck.config.json")
        plan = load_json(ROOT / f"decks/{DECK}/deck.editplan.json")
        receipt = run_qa(args.presentation_id or cfg["deck_id"], plan)
        print(json.dumps(receipt, indent=2))
        return 0 if receipt["status"] == "pass" else 1
    return cmd_run_all()


if __name__ == "__main__":
    raise SystemExit(main())