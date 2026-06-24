#!/usr/bin/env python3
"""Ocean Whisperer hospitality deck: copy gold → captive editplan → apply → QA."""
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
    export_thumbnails,
    golden_element,
    golden_slide_oid,
    leak_scan,
    load_json,
    utc_now,
    write_json,
)
from deck_edit_ops import econ_value_replace_ops, image_replace_op, text_replace_ops  # noqa: E402

DECK = "ocean-whisperer"
GOLDEN = ROOT / "decks/grab/golden-template-map.json"
KPI_PATH = ROOT / "decks/ocean-whisperer/slide3-kpis-ocean-whisperer.json"
VALUES_PATH = ROOT / "decks/ocean-whisperer/deck-economics-values-ocean-whisperer.json"
GROWTH_PATH = ROOT.parent / "finance/recal/growth-ocean-whisperer.json"
AGG_PATH = ROOT.parent / "finance/recal/agg-ocean-whisperer.json"
PARTNER_PATH = ROOT.parent / "partner-pitch/partners/ocean-whisperer.json"

LEAK_DENYLIST = [
    "Grab", "Uber", "Bolt", "Careem", "Singapore", "Sentosa", "Minor Hotels",
    "Phuket", "Bali", "super-app", "Koh Samui", "Bangkok",
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

ECON_SLIDE = {
    "slide_oid": "g3eec5122801_0_391",
    "bg_oid": "navierBg_s23",
    "bg_registry": "econ-curacao-v1",
    "corridor": "Hato (Curaçao Int'l) airport waterfront -> Baoase Luxury Resort (south coast, near Willemstad)",
    "market_label": "CURAÇAO",
    "header_oid": "g3eec5122801_0_392",
    "title_oid": "g3eec5122801_0_394",
    "route_oid": "g3eec5122801_0_395",
    "summary_oid": "g3eec5122801_0_397",
}

MARKET_SLIDES = {
    4: {
        "slide_oid": "g3eec5122801_0_106",
        "title_oid": "g3eec5122801_0_110",
        "subtitle_oid": "g3eec5122801_0_111",
        "routes_oid": "g3eec5122801_0_114",
        "title": "Curaçao — captive resort mesh (grounded)",
        "subtitle": "Airport, cruise-pier and inter-resort legs on sealed leeward geometry.",
    },
    5: {
        "slide_oid": "g3eec5122801_0_201",
        "title_oid": "g3eec5122801_0_205",
        "subtitle_oid": "g3eec5122801_0_206",
        "routes_oid": "g3eec5122801_0_209",
        "title": "Curaçao — premium network width",
        "subtitle": "Hato gateway + UNESCO waterfront feeds into the resort coast.",
    },
    6: {
        "slide_oid": "g3eec5122801_0_296",
        "title_oid": "g3eec5122801_0_300",
        "subtitle_oid": "g3eec5122801_0_304",
        "routes_oid": "g3eec5122801_0_301",
        "title": "ABC scale vision — island-to-island (roadmap)",
        "subtitle": "Bonaire + Aruba legs flagged amber-dashed; Quanta-LR cross-island reach.",
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

    logo = assets.get("ocean-whisperer-logo", {})
    if not logo.get("source_url"):
        raise SystemExit("ocean-whisperer-logo missing source_url in ASSET-REGISTRY")

    local_bg = "assets/backgrounds/markets/curacao/slide-bg-curacao-v1-composited.png"
    assets["econ-curacao-v1"] = {
        "role": "econ_market_bg",
        "scope": "market",
        "partner": "ocean-whisperer",
        "market_slug": "curacao",
        "atlas_city_id": "curacao-curacao",
        "local_path": f"deck-studio/{local_bg}",
        "version": "v1",
        "composited": True,
        "license": "navier-internal",
        "provenance": "grok/image_gen Spanish Water plate + n30_composite.py",
        "reproducible": True,
        "captured_at": utc_now(),
        "used_by": [{"deck": DECK, "slide_index": 7, "asset_role": "econ_market_bg"}],
        "status": "checked_in",
    }
    write_json(registry_path, registry)

    sys.path.insert(0, str(ROOT.parent / "finance"))
    from drive_upload import _drive_service  # type: ignore
    from googleapiclient.http import MediaFileUpload  # type: ignore

    svc = _drive_service()
    folder_id = os.environ.get("DECK_ASSETS_DRIVE_FOLDER_ID")
    path = ROOT / local_bg
    meta: dict = {"name": path.name}
    if folder_id:
        meta["parents"] = [folder_id]
    created = svc.files().create(
        body=meta,
        media_body=MediaFileUpload(str(path), mimetype="image/png", resumable=True),
        fields="id",
    ).execute()
    fid = created["id"]
    try:
        svc.permissions().create(fileId=fid, body={"type": "anyone", "role": "reader"}, fields="id").execute()
    except Exception:
        pass
    url = f"https://drive.google.com/uc?export=download&id={fid}"
    assets["econ-curacao-v1"]["drive_file_id"] = fid
    assets["econ-curacao-v1"]["source_url"] = url
    assets["econ-curacao-v1"]["status"] = "published"
    write_json(registry_path, registry)
    return {"ocean-whisperer-logo": logo["source_url"], "econ-curacao-v1": url}


def route_list_text(journeys: list[dict], *, max_routes: int = 4) -> str:
    lines: list[str] = []
    for j in journeys[:max_routes]:
        frm = j["from"].split("(")[0].strip()
        to = j["to"].replace(" Resort", "").strip()
        nm = j.get("distance_nm")
        render = j.get("render", "solid")
        tag = "roadmap" if "roadmap" in render else "gateway/resort"
        nm_s = f"~{nm:g} nm" if nm else "sealed corridor"
        lines.append(f"▸  {frm} → {to}\n      {nm_s} · {tag}")
    return "\n".join(lines)


def slide3_kpi_map() -> dict[str, str]:
    return dict(load_json(KPI_PATH)["slide3_width_kpis"])


def slide10_tam_map() -> dict[str, str]:
    kpi = load_json(KPI_PATH)
    t = kpi["slide10_tam"]
    growth = load_json(GROWTH_PATH)
    g = growth.get("grounded", {})
    som_m = g.get("SOM_floor_navier_transport_rev_yr", 0) / 1e6
    sam_m = g.get("SAM_navier_transport_rev_yr", {}).get("mid", 0) / 1e6
    tam_m = growth.get("marine_mobility_tam", {}).get("mid", 0) / 1e6
    jgmv_m = growth.get("journey_gmv", {}).get("mid", 0) / 1e6
    return {
        "som_value": t["som_floor_display"],
        "som_caption": f"SOM floor — captive resort mesh ({som_m:.0f}M grounded today)",
        "sam_value": t["sam_mid_display"],
        "sam_caption": f"SAM mid — induced demand + network width ({sam_m:.0f}M Navier rev)",
        "tam_value": t["tam_marine_mid_display"],
        "tam_caption": f"Marine mobility TAM — induced transfer wallet ({tam_m:.0f}M)",
        "journey_gmv_value": t["tam_journey_gmv_mid_display"],
        "journey_gmv_caption": f"Journey GMV — food + stays + experiences ({jgmv_m:.0f}M)",
        "platform_value": "",
        "platform_caption": "",
    }


def econ_fields_from_values() -> dict[str, str]:
    fields = load_json(VALUES_PATH)["economics_slides"]["7"]["fields"]
    return {k: str(v) for k, v in fields.items() if k not in ("header_market",)}


def build_narrative(partner: dict) -> dict[tuple[str, str], str]:
    hero = partner["hero"]
    ask = partner["the_ask"]
    close = partner["close"]
    phases = partner["phases"]
    journeys = partner.get("journeys_unlocked", [])
    solid = [j for j in journeys if j.get("render") == "solid"]
    roadmap = [j for j in journeys if "roadmap" in j.get("render", "")]

    narrative: dict[tuple[str, str], str] = {
        ("p1", "p1_i8"): hero["title"],
        ("p1", "p1_i9"): hero["subtitle"],
        (SLIDE3_OID, "g3eec5122801_0_2"): "OCEAN WHISPERER",
        (SLIDE3_OID, "g3eec5122801_0_4"): "Curaçao captive resort mesh — air to water",
        (
            SLIDE3_OID,
            "g3eec5122801_0_14",
        ): "Hospitality ladder — rising rungs, no platform revenue (5-rung captive frame).",
        (SLIDE10_OID, "g3eec5122801_0_565"): "A captive revenue layer for an aviation-luxury brand",
        (
            SLIDE10_OID,
            "g3eec5122801_0_567",
        ): (
            "Read it bottom-up: the fare a Navier boat collects today on Curaçao's resort coast, "
            "the WIDTH a faster product unlocks — then the whole journey wallet Ocean Whisperer monetizes."
        ),
        ("g3ea5e0fb254_4_357", "g3ea5e0fb254_4_361"): "You own the brand. We operate the fleet.",
        (
            "g3ea5e0fb254_4_357",
            "g3ea5e0fb254_4_362",
        ): (
            f"▸  Ocean Whisperer — {ask['partner_brings'].split(',')[0].strip()}.\n"
            f"▸  Navier — {ask['navier_brings'].split(',')[0].strip()}.\n"
            f"▸  Together — silent foiling tier from air gateway to resort jetty."
        ),
        (
            "g3ea5e0fb254_4_444",
            "g3ea5e0fb254_4_447",
        ): (
            f"1.  {phases[0]['label']} — {phases[0]['rationale']}\n"
            f"2.  {phases[1]['label']} — {phases[1]['rationale']}\n"
            f"3.  {phases[2]['label']} — {phases[2]['rationale']}"
        ),
        ("g3ea5e0fb254_4_330", "g3ea5e0fb254_4_330"): "Explore the Ocean Whisperer marine network",
        (
            "g3ea5e0fb254_4_331",
            "g3ea5e0fb254_4_331",
        ): (
            f"{close['body']} Open the Navier × Ocean Whisperer Atlas and pick the first grounded corridor."
        ),
    }

    narrative[(MARKET_SLIDES[4]["slide_oid"], MARKET_SLIDES[4]["title_oid"])] = MARKET_SLIDES[4]["title"]
    narrative[(MARKET_SLIDES[4]["slide_oid"], MARKET_SLIDES[4]["subtitle_oid"])] = MARKET_SLIDES[4]["subtitle"]
    narrative[(MARKET_SLIDES[4]["slide_oid"], MARKET_SLIDES[4]["routes_oid"])] = route_list_text(solid[:4])

    narrative[(MARKET_SLIDES[5]["slide_oid"], MARKET_SLIDES[5]["title_oid"])] = MARKET_SLIDES[5]["title"]
    narrative[(MARKET_SLIDES[5]["slide_oid"], MARKET_SLIDES[5]["subtitle_oid"])] = MARKET_SLIDES[5]["subtitle"]
    narrative[(MARKET_SLIDES[5]["slide_oid"], MARKET_SLIDES[5]["routes_oid"])] = route_list_text(solid[2:6] or solid)

    narrative[(MARKET_SLIDES[6]["slide_oid"], MARKET_SLIDES[6]["title_oid"])] = MARKET_SLIDES[6]["title"]
    narrative[(MARKET_SLIDES[6]["slide_oid"], MARKET_SLIDES[6]["subtitle_oid"])] = MARKET_SLIDES[6]["subtitle"]
    narrative[(MARKET_SLIDES[6]["slide_oid"], MARKET_SLIDES[6]["routes_oid"])] = route_list_text(roadmap[:4] or journeys[-2:])

    return narrative


def pull_manifest(presentation_id: str) -> None:
    cfg_path = ROOT / f"decks/{DECK}/deck.config.json"
    cfg = load_json(cfg_path)
    cfg["deck_id"] = presentation_id
    cfg["live_deck_url"] = f"https://docs.google.com/presentation/d/{presentation_id}/edit"
    cfg["economics_sheet_id"] = "109GGDSUoU_xofFU5Losb8-3OCW5ykZMBD41m4XTvOeU"
    cfg["economics_url"] = "https://docs.google.com/spreadsheets/d/109GGDSUoU_xofFU5Losb8-3OCW5ykZMBD41m4XTvOeU/edit"
    cfg["last_pulled_at"] = utc_now()
    write_json(cfg_path, cfg)
    subprocess.run(
        [sys.executable, "-m", "deck_studio", "pull", "--root", str(ROOT), "--deck", DECK, "--mode", "full"],
        cwd=str(BUILDERS),
        check=True,
    )


def build_editplan(presentation_id: str, asset_urls: dict[str, str]) -> dict:
    golden = load_json(GOLDEN)
    partner = load_json(PARTNER_PATH)
    grab_binding = load_json(ROOT / "decks/grab/economics-binding.json")
    values = load_json(VALUES_PATH)["economics_slides"]["7"]["fields"]
    econ_map = econ_fields_from_values()
    ops: list[dict] = []
    slide1 = golden_slide_oid(golden, 1)

    if asset_urls.get("ocean-whisperer-logo"):
        ops.append(
            image_replace_op(
                slide1, "p1_i5", asset_urls["ocean-whisperer-logo"],
                op_key="ow-cover-partner-logo",
                source_pointer="ASSET-REGISTRY ocean-whisperer-logo",
                method="CENTER_INSIDE",
            )
        )

    for (slide_oid, target_oid), text in build_narrative(partner).items():
        el = {**element_or_fallback(golden, target_oid), "char_budget": max(element_or_fallback(golden, target_oid).get("char_budget", 12), len(text) + 4)}
        ops.extend(text_replace_ops(slide_oid, target_oid, text, el, op_prefix=f"ow-narr-{target_oid}", source_pointer=str(PARTNER_PATH.name)))

    kpi = slide3_kpi_map()
    for oid, key in SLIDE3_KPI_FIELDS:
        text = kpi[key]
        el = {**element_or_fallback(golden, oid), "char_budget": max(len(text) + 8, 24)}
        ops.extend(text_replace_ops(SLIDE3_OID, oid, text, el, op_prefix=f"ow-slide3-{oid}", source_pointer=KPI_PATH.name))

    tam = slide10_tam_map()
    for oid, key in SLIDE10_TAM_FIELDS:
        text = tam[key]
        if not text.strip():
            continue  # hospitality: hide platform-rev rung (empty object breaks Slides API)
        el = {**element_or_fallback(golden, oid), "char_budget": max(len(text) + 8, 24)}
        ops.extend(text_replace_ops(SLIDE10_OID, oid, text, el, op_prefix=f"ow-slide10-{oid}", source_pointer=GROWTH_PATH.name))

    spec = ECON_SLIDE
    url = asset_urls.get(spec["bg_registry"])
    if url:
        ops.append(image_replace_op(spec["slide_oid"], spec["bg_oid"], url, op_key=f"ow-bg-{spec['bg_registry']}", source_pointer=f"ASSET-REGISTRY {spec['bg_registry']}", method="CENTER_CROP"))

    header = values["header_market"]
    for oid, text in (
        (spec["header_oid"], header),
        (spec["title_oid"], values["title"]),
        (spec["route_oid"], values["route_line"]),
    ):
        base = element_or_fallback(golden, oid)
        el = {**base, "char_budget": max(base.get("char_budget", 12), len(text) + 4)}
        ops.extend(text_replace_ops(spec["slide_oid"], oid, text, el, op_prefix=f"ow-econ-text-{oid}", source_pointer=VALUES_PATH.name))

    ops.extend(text_replace_ops(spec["slide_oid"], spec["summary_oid"], values["summary_line"], element_or_fallback(golden, spec["summary_oid"]), op_prefix="ow-econ-summary", source_pointer=VALUES_PATH.name))

    binding_slide = next(s for s in grab_binding["economics_slides"] if s["slide_index"] == 7)
    for field_key, text in econ_map.items():
        field = binding_slide["fields"].get(field_key)
        if not field or not field.get("value_object_id"):
            continue
        ops.extend(econ_value_replace_ops(spec["slide_oid"], field["value_object_id"], text, op_prefix=f"ow-econ-val-{field_key}", source_pointer=VALUES_PATH.name))

    return {
        "deck_key": DECK,
        "presentation_id": presentation_id,
        "mode": "slides_api_batch_update",
        "archetype_variant": "hospitality",
        "request_summary": "Ocean Whisperer: cover logo, slide3 KPIs, 3 Curaçao/ABC slides, slide7 econ, hospitality TAM",
        "safety": {"no_pptx_roundtrip": True, "no_full_deck_replace": True, "preserve_object_ids": True, "human_review_required_for_external_send": True},
        "operations": ops,
        "qa": {"leak_denylist": LEAK_DENYLIST},
        "qa_gates": ["drift_gate", "leak_scan", "render_export"],
        "created_at": utc_now(),
    }


EXPECTED_SLIDE_COUNT = 24
EDITED_SLIDES = [1, 3, 4, 5, 6, 7, 10, 11, 12, 13]


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
    }
    write_json(ROOT / f"decks/{DECK}/qa-receipts/live-apply-receipt.json", receipt)
    return receipt


def cmd_run_all() -> int:
    print("1/5 Publish Ocean Whisperer deck assets...")
    urls = publish_assets()
    print("2/5 Copy gold Grab deck...")
    pid = copy_gold_deck("Ocean Whisperer × Navier")
    print(f"   deck_id: {pid}")
    print("3/5 Pull manifest + build editplan...")
    pull_manifest(pid)
    plan = build_editplan(pid, urls)
    write_json(ROOT / f"decks/{DECK}/deck.editplan.json", plan)
    print(f"   operations: {len(plan['operations'])}")
    print("4/5 Apply editplan...")
    applied = apply_plan(plan, chunk_size=35)
    plan["applied_at"] = utc_now()
    plan["status"] = "applied"
    write_json(ROOT / f"decks/{DECK}/deck.editplan.json", plan)
    print(f"   applied {applied} requests")
    print("5/5 QA + thumbnails...")
    receipt = run_qa(pid, plan)
    print(json.dumps(receipt, indent=2))
    cfg = load_json(ROOT / f"decks/{DECK}/deck.config.json")
    cfg["deck_id"] = pid
    cfg["live_deck_url"] = receipt["live_deck_url"]
    write_json(ROOT / f"decks/{DECK}/deck.config.json", cfg)
    return 0 if receipt["status"] == "pass" else 1


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description="Ocean Whisperer deck builder")
    ap.add_argument("command", choices=["run-all", "publish-assets", "build-editplan", "apply", "qa"])
    ap.add_argument("--presentation-id")
    args = ap.parse_args()
    if args.command == "publish-assets":
        print(json.dumps(publish_assets(), indent=2))
        return 0
    if args.command == "run-all":
        return cmd_run_all()
    if args.command == "build-editplan":
        cfg = load_json(ROOT / f"decks/{DECK}/deck.config.json")
        pid = args.presentation_id or cfg.get("deck_id")
        if not pid:
            raise SystemExit("need --presentation-id or deck.config deck_id")
        plan = build_editplan(pid, publish_assets())
        write_json(ROOT / f"decks/{DECK}/deck.editplan.json", plan)
        print(json.dumps({"operations": len(plan["operations"]), "presentation_id": pid}, indent=2))
        return 0
    if args.command == "apply":
        plan = load_json(ROOT / f"decks/{DECK}/deck.editplan.json")
        print(f"applied {apply_plan(plan, chunk_size=35)}")
        return 0
    if args.command == "qa":
        cfg = load_json(ROOT / f"decks/{DECK}/deck.config.json")
        plan = load_json(ROOT / f"decks/{DECK}/deck.editplan.json")
        receipt = run_qa(args.presentation_id or cfg["deck_id"], plan)
        print(json.dumps(receipt, indent=2))
        return 0 if receipt["status"] == "pass" else 1
    return 1


if __name__ == "__main__":
    raise SystemExit(main())