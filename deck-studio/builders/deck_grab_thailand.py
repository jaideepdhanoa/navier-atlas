#!/usr/bin/env python3
"""Grab Thailand WS6 deck: copy gold Grab deck → Thailand editplan → apply → QA."""
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
    GOLD_ID,
    apply_plan,
    collect_slide_text,
    copy_gold_deck,
    drift_gate,
    export_thumbnails,
    golden_element,
    golden_slide_oid,
    leak_scan,
    load_json,
    slides_service,
    utc_now,
    write_json,
)
from deck_edit_ops import econ_value_replace_ops, image_replace_op, text_replace_ops  # noqa: E402

DECK = "grab-thailand"
GOLDEN = ROOT / "decks/grab/golden-template-map.json"
KPI_PATH = ROOT / "decks/grab-thailand/slide3-kpis-grab-thailand.json"
GROWTH_PATH = ROOT.parent / "finance/recal/growth-grab-thailand.json"
AGG_PATH = ROOT.parent / "finance/recal/agg-grab-thailand.json"

LEAK_DENYLIST = [
    "Marina Bay",
    "Sentosa",
    "Southeast Asia",
    "Europe",
    "Malaysia",
    "Mexico",
    "Morocco",
    "Bali",
    "Singapore",
    "Langkawi",
    "Manila",
    "Boracay",
    "Penang",
    "$480,870",
    "Bolt",
    "Uber",
]

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
        "bg_registry": "econ-koh-samui-v2",
        "corridor": "Samui Pralarn Pier (Mae Nam) -> Koh Phangan (Thong Sala) — pier-exact",
        "market_label": "KOH SAMUI",
        "title": "Samui: profitable from year one",
        "route_line": "Mae Nam → Thong Sala  ·  ~8 nm  ·  N30 Pioneer II (8 seats)",
        "header_oid": "g3eec5122801_0_392",
        "title_oid": "g3eec5122801_0_394",
        "route_oid": "g3eec5122801_0_395",
        "summary_oid": "g3eec5122801_0_397",
        "footnote_oid": "g3eec5122801_0_441",
    },
    8: {
        "slide_oid": "g3eec5122801_0_448",
        "bg_oid": "navierBg_s24",
        "bg_registry": "econ-phuket-v1",
        "corridor": "Phuket (Royal Phuket Marina) -> Phang Nga Bay / James Bond Island",
        "market_label": "PHUKET",
        "title": "Phuket: profitable from year one",
        "route_line": "Royal Phuket Marina → Phang Nga (James Bond Island)  ·  ~20 nm  ·  N30 Pioneer II (8 seats)",
        "header_oid": "g3eec5122801_0_449",
        "title_oid": "g3eec5122801_0_451",
        "route_oid": "g3eec5122801_0_452",
        "summary_oid": "g3eec5122801_0_454",
        "footnote_oid": "g3eec5122801_0_498",
    },
    9: {
        "slide_oid": "g3eec5122801_0_505",
        "bg_oid": "navierBg_s25",
        "bg_registry": "econ-bangkok-v1",
        "corridor": "ICONSIAM Pier (Chao Phraya) -> ICONSIAM Pier (Chao Phraya)",
        "market_label": "BANGKOK",
        "title": "Bangkok: profitable from year one",
        "route_line": "Icon Siam → Wat Arun  ·  ~5 nm  ·  N30 Pioneer II (8 seats)",
        "header_oid": "g3eec5122801_0_506",
        "title_oid": "g3eec5122801_0_508",
        "route_oid": "g3eec5122801_0_509",
        "summary_oid": "g3eec5122801_0_511",
        "footnote_oid": "g3eec5122801_0_555",
    },
}

NARRATIVE: dict[tuple[str, str], str] = {
    ("p1", "p1_i8"): "Water layer for Gulf, Andaman, river",
    ("p1", "p1_i9"): "Grab already owns Thailand's in-app demand. Water is the only surface no one owns yet.",
    (SLIDE3_OID, "g3eec5122801_0_2"): "THAILAND",
    (SLIDE3_OID, "g3eec5122801_0_4"): "Two coasts and a river megacity — one foiling network",
    (SLIDE3_OID, "g3eec5122801_0_14"): "Grab Thailand owns the demand; Navier brings the foiling fleet proven in the Maldives.",
    ("g3eec5122801_0_106", "g3eec5122801_0_110"): "Koh Samui & the Gulf — flagship beachhead",
    ("g3eec5122801_0_106", "g3eec5122801_0_111"): "Samui ↔ Phangan ↔ Tao triangle on sealed Bucket-C geometry.",
    (
        "g3eec5122801_0_106",
        "g3eec5122801_0_114",
    ): (
        "▸  Mae Nam → Thong Sala (Phangan)\n"
        "      ~8 nm · flagship cascade corridor\n"
        "▸  Samui → Koh Tao\n"
        "      ~35 nm · dive-school triangle leg\n"
        "▸  Lipa Noi → Donsak (mainland)\n"
        "      ~15 nm · airport-to-island gateway\n"
        "▸  Nathon → Ang Thong marine park\n"
        "      ~12 nm · day-trip premium hop"
    ),
    ("g3eec5122801_0_201", "g3eec5122801_0_205"): "Phuket & the Andaman",
    ("g3eec5122801_0_201", "g3eec5122801_0_206"): "Resort flows, Phi Phi hops, and Krabi mesh on pier-exact routes.",
    (
        "g3eec5122801_0_201",
        "g3eec5122801_0_209",
    ): (
        "▸  Phuket → Phi Phi (Tonsai)\n"
        "      ~25 nm · marquee Andaman hop\n"
        "▸  Royal Phuket Marina → Phang Nga\n"
        "      ~20 nm · limestone-bay run\n"
        "▸  Phuket → Krabi (Ao Nang)\n"
        "      ~40 nm · resort mesh leg\n"
        "▸  Phuket → Railay\n"
        "      ~25 nm · cliff-beach premium run"
    ),
    ("g3eec5122801_0_296", "g3eec5122801_0_300"): "Bangkok — Chao Phraya & gulf gateway",
    ("g3eec5122801_0_296", "g3eec5122801_0_304"): "River spine sealed; Pattaya, Hua Hin, Koh Larn and Koh Chang connected cities live.",
    (
        "g3eec5122801_0_296",
        "g3eec5122801_0_301",
    ): (
        "▸  Sathorn → Phra Arthit\n"
        "      ~3 nm · Chao Phraya river spine\n"
        "▸  Icon Siam → Wat Arun\n"
        "      ~2 nm · tourist river loop\n"
        "▸  Bangkok → Pattaya\n"
        "      ~60 nm · gulf gateway city\n"
        "▸  Bangkok ↔ Hua Hin\n"
        "      ~88 nm · cross-Gulf Quanta-LR ring"
    ),
    (SLIDE10_OID, "g3eec5122801_0_565"): "A new multi-billion-dollar vertical across Thailand",
    (SLIDE10_OID, "g3eec5122801_0_567"): "Read it bottom-up: the fare a Navier boat collects today, the market a faster product unlocks — then the whole journey Grab monetizes around every crossing.",
    ("g3ea5e0fb254_4_357", "g3ea5e0fb254_4_361"): "You bring the demand. We operate the water.",
    ("g3ea5e0fb254_4_357", "g3ea5e0fb254_4_362"): "▸  Grab — demand, the app, the wallet and the brand.\n▸  Navier — vessels, crew, maintenance, certification and the network playbook.\n▸  Together — a premium foiling water tier across the Gulf, Andaman and Chao Phraya.",
    ("g3ea5e0fb254_4_444", "g3ea5e0fb254_4_447"): "1.  Working session — walk the Thailand atlas and economics.\n2.  Vessel demo — a live foiling run on a pilot corridor.\n3.  Pilot MOU — Samui triangle beachhead, three corridors, 12-month launch window.",
    ("g3ea5e0fb254_4_330", "g3ea5e0fb254_4_330"): "Explore the Grab Thailand marine network",
    ("g3ea5e0fb254_4_331", "g3ea5e0fb254_4_331"): (
        "Open the Navier × Grab Thailand Atlas, pick the first corridor, "
        "and let's discover a new foiling water tier across two coasts and a river."
    ),
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
    from deck_autonomy_sync import publish_assets_to_drive  # type: ignore

    publish_assets_to_drive(registry_path)
    registry = load_json(registry_path)
    keys = ("grab-partner-logo", "econ-koh-samui-v2", "econ-phuket-v1", "econ-bangkok-v1")
    urls = {}
    for key in keys:
        asset = registry["assets"].get(key, {})
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


def slide3_kpi_map() -> dict[str, str]:
    kpi = load_json(KPI_PATH)
    width = kpi.get("slide3_width_kpis") or {}
    if width:
        return {k: str(v) for k, v in width.items()}
    g = kpi["network_headline"]["grounded"]
    n = kpi["network_headline"].get("routes_mapped_total", kpi["network_headline"].get("sealed_anchor_corridors"))
    cards = [
        (str(n), "premium water corridors mapped — 5 Thailand clusters"),
        (f"${g['addressable_transport_spend_usd_m']:.0f}M", "addressable transport spend on sourced corridors today"),
        (kpi["slide10_tam"]["som_floor_display"], "SOM floor — Navier fare, ~11% capture, today's demand"),
        (f"${g['SAM_navier_rev_mid_usd_m']:.0f}M", "SAM mid — full network Navier transport revenue"),
    ]
    return {
        "card1_value": cards[0][0],
        "card1_caption": cards[0][1],
        "card2_value": cards[1][0],
        "card2_caption": cards[1][1],
        "card3_value": cards[2][0],
        "card3_caption": cards[2][1],
        "card4_value": cards[3][0],
        "card4_caption": cards[3][1],
    }


def slide10_tam_map() -> dict[str, str]:
    growth = load_json(GROWTH_PATH)
    kpi = load_json(KPI_PATH)
    t = kpi["slide10_tam"]
    rungs = {r["id"]: r for r in growth.get("revenue_potential", {}).get("rungs", [])}
    som = rungs.get("som_floor", {})
    sam = rungs.get("sam_full_network", {})
    tam = rungs.get("tam_journey_gmv", {})
    jgmv = rungs.get("journey_gmv_through_network", {})
    plat = rungs.get("partner_platform_rev", {})
    return {
        "som_value": som.get("display", {}).get("mid") or t["som_floor_display"],
        "som_caption": "SOM — Navier fare, Grab Thailand network, today's trips, 10% capture",
        "sam_value": sam.get("display", {}).get("mid") or f"${sam.get('mid', 0)/1e6:.0f}M",
        "sam_caption": "SAM — faster boats grow the market; contested capture at maturity",
        "tam_value": tam.get("display", {}).get("mid") or t.get("marine_mobility_tam_mid_display", t["journey_gmv_mid_display"]),
        "tam_caption": "Marine mobility TAM — induced transfer market, mid of model band",
        "journey_gmv_value": jgmv.get("display", {}).get("mid") or t["journey_gmv_mid_display"],
        "journey_gmv_caption": "Journey GMV routed through the Navier network",
        "platform_value": plat.get("display", {}).get("mid") or t["partner_platform_rev_mid_display"],
        "platform_caption": "Grab platform revenue on Navier-corridor journey GMV",
    }


def pull_manifest(presentation_id: str) -> None:
    cfg_path = ROOT / f"decks/{DECK}/deck.config.json"
    cfg = load_json(cfg_path)
    cfg["deck_id"] = presentation_id
    cfg["live_deck_url"] = f"https://docs.google.com/presentation/d/{presentation_id}/edit"
    cfg["last_pulled_at"] = utc_now()
    cfg["notes"] = "Grab Thailand WS6 deck — copied from gold template, applied via deck_grab_thailand.py"
    cfg.setdefault("cover_logos", {}).setdefault("partner_logo", {})["status"] = "banked"
    write_json(cfg_path, cfg)
    subprocess.run(
        [sys.executable, "-m", "deck_studio", "pull", "--root", str(ROOT), "--deck", DECK, "--mode", "full"],
        cwd=str(BUILDERS),
        check=True,
    )


def build_editplan(presentation_id: str, asset_urls: dict[str, str]) -> dict:
    golden = load_json(GOLDEN)
    ops: list[dict] = []
    slide1 = golden_slide_oid(golden, 1)

    if asset_urls.get("grab-partner-logo"):
        ops.append(
            image_replace_op(
                slide1, "p1_i5", asset_urls["grab-partner-logo"],
                op_key="gt-cover-partner-logo",
                source_pointer="ASSET-REGISTRY grab-partner-logo",
                method="CENTER_INSIDE",
            )
        )

    for (slide_oid, target_oid), text in NARRATIVE.items():
        el = {**element_or_fallback(golden, target_oid), "char_budget": max(element_or_fallback(golden, target_oid).get("char_budget", 12), len(text) + 4)}
        ops.extend(
            text_replace_ops(
                slide_oid, target_oid, text, el,
                op_prefix=f"gt-narr-{target_oid}",
                source_pointer="partner-pitch/partners/grab-thailand.json",
            )
        )

    kpi = slide3_kpi_map()
    for oid, key in SLIDE3_KPI_FIELDS:
        text = kpi[key]
        el = {**element_or_fallback(golden, oid), "char_budget": max(len(text) + 8, 24)}
        ops.extend(
            text_replace_ops(SLIDE3_OID, oid, text, el, op_prefix=f"gt-slide3-{oid}", source_pointer=str(KPI_PATH.name))
        )

    tam = slide10_tam_map()
    for oid, key in SLIDE10_TAM_FIELDS:
        text = tam[key]
        el = {**element_or_fallback(golden, oid), "char_budget": max(len(text) + 8, 24)}
        ops.extend(
            text_replace_ops(SLIDE10_OID, oid, text, el, op_prefix=f"gt-slide10-{oid}", source_pointer=str(GROWTH_PATH.name))
        )

    grab_binding = load_json(ROOT / "decks/grab/economics-binding.json")
    for slide_idx, spec in ECON_SLIDES.items():
        url = asset_urls.get(spec["bg_registry"])
        if url:
            ops.append(
                image_replace_op(
                    spec["slide_oid"], spec["bg_oid"], url,
                    op_key=f"gt-bg-{spec['bg_registry']}",
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
                    spec["slide_oid"], oid, text, el,
                    op_prefix=f"gt-econ-text-{oid}",
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
                spec["slide_oid"], spec["summary_oid"], summary, el,
                op_prefix=f"gt-econ-summary-{spec['slide_oid']}",
                source_pointer=f"agg-grab-thailand.json :: {spec['corridor']}",
            )
        )
        # Footnote tagline: builder-owned so a rebuild reproduces the live deck.
        # Payback is derived from the model (mid scenario), never hand-typed.
        footnote_oid = spec.get("footnote_oid")
        if footnote_oid:
            if econ.get("payback_years"):
                footnote = (
                    "Profitable from year one — every line item ties on this slide; "
                    f"the vessel pays itself back in {econ['payback_years']:.1f} yrs."
                )
            else:
                footnote = "Profitable from year one — every line item ties on this slide."
            base = element_or_fallback(golden, footnote_oid)
            el = {**base, "char_budget": max(base.get("char_budget", 12), len(footnote) + 4)}
            ops.extend(
                text_replace_ops(
                    spec["slide_oid"], footnote_oid, footnote, el,
                    op_prefix=f"gt-econ-footnote-{spec['slide_oid']}",
                    source_pointer=f"agg-grab-thailand.json :: {spec['corridor']} (payback)",
                )
            )
        binding_slide = next(s for s in grab_binding["economics_slides"] if s["slide_index"] == slide_idx)
        values = econ_value_map(econ)
        source = f"finance/recal/agg-grab-thailand.json mid {spec['corridor']}"
        for field_key, text in values.items():
            field = binding_slide["fields"].get(field_key)
            if not field or not field.get("value_object_id"):
                continue
            ops.extend(
                econ_value_replace_ops(
                    spec["slide_oid"],
                    field["value_object_id"],
                    text,
                    op_prefix=f"gt-econ-val-{field_key}-{slide_idx}",
                    source_pointer=source,
                )
            )

    return {
        "deck_key": DECK,
        "presentation_id": presentation_id,
        "mode": "slides_api_batch_update",
        "request_summary": "Grab Thailand WS6: cover, slide3 KPIs, 3 market slides, 3 econ slides, TAM, close",
        "safety": {
            "no_pptx_roundtrip": True,
            "no_full_deck_replace": True,
            "preserve_object_ids": True,
            "human_review_required_for_external_send": True,
        },
        "operations": ops,
        "qa": {"leak_denylist": LEAK_DENYLIST},
        "qa_gates": ["drift_gate", "leak_scan", "render_export"],
        "created_at": utc_now(),
    }


EXPECTED_SLIDE_COUNT = 24
WS6_EDITED_SLIDES = [1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]


def thailand_drift_gate(presentation_id: str, plan: dict) -> dict:
    result = drift_gate(presentation_id, plan)
    result["pass"] = not result["missing_object_ids"] and result["slide_count"] == EXPECTED_SLIDE_COUNT
    result["expected_slide_count"] = EXPECTED_SLIDE_COUNT
    return result


def run_qa(presentation_id: str, plan: dict) -> dict:
    leak_edited = leak_scan(presentation_id, LEAK_DENYLIST, slide_indexes=WS6_EDITED_SLIDES)
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
    }
    write_json(ROOT / f"decks/{DECK}/qa-receipts/ws6-apply-receipt.json", receipt)
    return receipt


def cmd_run_all() -> int:
    print("1/6 Publish Thailand deck assets...")
    urls = publish_assets()
    print(f"   urls: {list(urls.keys())}")

    print("2/6 Copy gold Grab deck...")
    pid = copy_gold_deck("Grab Thailand × Navier (WS6)")
    print(f"   deck_id: {pid}")

    print("3/6 Pull manifest + build editplan...")
    pull_manifest(pid)
    plan = build_editplan(pid, urls)
    plan_path = ROOT / f"decks/{DECK}/deck.editplan.json"
    write_json(plan_path, plan)
    print(f"   operations: {len(plan['operations'])}")

    drift = thailand_drift_gate(pid, plan)
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

    ap = argparse.ArgumentParser(description="Grab Thailand deck builder")
    ap.add_argument("command", choices=["run-all", "publish-assets", "copy-gold", "build-editplan", "apply", "qa"])
    ap.add_argument("--presentation-id")
    args = ap.parse_args()

    if args.command == "publish-assets":
        print(json.dumps(publish_assets(), indent=2))
        return 0
    if args.command == "copy-gold":
        pid = copy_gold_deck("Grab Thailand × Navier (WS6)")
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