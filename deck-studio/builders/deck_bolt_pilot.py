#!/usr/bin/env python3
"""Bolt pilot: copy gold deck → populate style-preserving editplan → apply → QA."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDERS = ROOT / "builders"
sys.path.insert(0, str(BUILDERS))

from deck_edit_ops import econ_value_replace_ops, image_replace_op, text_replace_ops  # noqa: E402

GOLD_ID = "18yDAgO0Sj9PJlgf6paxtgni8Pk1xRAmNwE2TD_NCdSs"
SLIDE7_OID = "g3eec5122801_0_391"

LEAK_DENYLIST = [
    "Marina Bay",
    "Sentosa",
    "Grab",
    "Malaysia",
    "Mexico",
    "Morocco",
    "Southeast Asia",
    "Singapore",
    "Phuket",
    "Bali",
    "$211,622",
    "$151,776",
    "$59,846",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def slides_service():
    sys.path.insert(0, str(ROOT / "builders"))
    from deck_studio.cli import get_slides_service  # type: ignore

    return get_slides_service()


def drive_service():
    sys.path.insert(0, str(ROOT / "builders"))
    from deck_studio.cli import get_drive_service  # type: ignore

    return get_drive_service()


def golden_element(golden: dict, oid: str) -> dict | None:
    for slide in golden.get("slides", []):
        for el in slide.get("elements", []):
            if el.get("oid") == oid:
                return el
    return None


def element_or_fallback(golden: dict, oid: str, *, fallback_oid: str = "g3eec5122801_0_402") -> dict:
    el = golden_element(golden, oid)
    if el:
        return el
    fb = golden_element(golden, fallback_oid)
    if not fb:
        raise KeyError(f"No golden element for {oid} and fallback {fallback_oid}")
    return {
        **fb,
        "oid": oid,
        "char_budget": max(fb.get("char_budget", 12), 16),
    }


def golden_slide_oid(golden: dict, slide_index: int) -> str:
    for slide in golden.get("slides", []):
        if slide.get("index") == slide_index:
            return slide["pageObjectId"]
    raise KeyError(f"slide index {slide_index} not in golden map")


def fmt_usd(n: float) -> str:
    return f"${n:,.0f}"


def load_bolt_economics() -> dict:
    agg = load_json(ROOT.parent / "finance/recal/agg-bolt.json")
    for row in agg.get("rows", []):
        if row.get("corridor") == "Athens -> Hydra (Saronic)":
            return row["mid"]
    raise SystemExit("Athens -> Hydra mid scenario not found in agg-bolt.json")


def econ7_value_map(econ: dict) -> dict[str, str]:
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


def build_econ7_value_fix_ops() -> list[dict]:
    binding = load_json(ROOT / "decks/bolt/economics-binding.json")
    slide7 = next(s for s in binding["economics_slides"] if s["slide_index"] == 7)
    fields = slide7["fields"]
    value_map = econ7_value_map(load_bolt_economics())
    ops: list[dict] = []
    for field_key, text in value_map.items():
        oid = fields[field_key]["value_object_id"]
        ops.extend(
            econ_value_replace_ops(
                SLIDE7_OID,
                oid,
                text,
                op_prefix=f"bolt-econ7-val-fix-{field_key}",
                source_pointer="deck_edit_ops.econ_value_replace_ops (full-range style + END align)",
            )
        )
    return ops


def generate_greece_cover() -> Path:
    raise SystemExit(
        "Greece/Aegean cover generation blocked until an approved Greece source plate exists. "
        "Do not reuse mislabeled econ-uae-the-world-islands (formerly econ-cote-azur)."
    )


def register_bolt_assets() -> dict[str, str]:
    registry_path = ROOT / "assets/ASSET-REGISTRY.json"
    registry = load_json(registry_path)
    assets = registry.setdefault("assets", {})

    assets["bolt-partner-logo"] = {
        "role": "partner_logo",
        "scope": "partner",
        "partner": "bolt",
        "status": "checked_in",
        "local_path": "assets/logos/partners/bolt/bolt-logo.png",
        "drive_file_id": assets.get("bolt-partner-logo", {}).get("drive_file_id"),
        "source_url": assets.get("bolt-partner-logo", {}).get("source_url"),
        "license": "bolt-brand",
        "provenance": "official_site_asset",
        "reproducible": True,
        "notes": "Bolt wordmark (white), banked per LOGO-MANIFEST.",
        "used_by": [
            {"deck": "bolt", "slide_index": 1, "slide_object_id": "p1", "target_object_id": "p1_i5"}
        ],
        "composited": False,
        "captured_at": utc_now(),
    }

    registry.setdefault("deck_coverage", {}).setdefault("bolt", {})["roles"] = {
        "cover_hero": "pending_inventory",
        "navier_logo": "checked_in(shared)",
        "partner_logo": "checked_in",
        "value_prop_bg": "pending_inventory",
        "tam_bg": "pending_inventory",
        "partner_roles_bg": "pending_inventory",
        "econ_market_bg": "pending_inventory",
    }
    write_json(registry_path, registry)

    # Publish missing source_urls
    sys.path.insert(0, str(ROOT / "builders"))
    from deck_autonomy_sync import publish_assets_to_drive  # type: ignore

    publish_assets_to_drive(registry_path)
    registry = load_json(registry_path)
    urls = {}
    for key in ("bolt-partner-logo",):
        asset = registry["assets"][key]
        if not asset.get("source_url"):
            raise SystemExit(f"Asset {key} missing source_url after publish")
        urls[key] = asset["source_url"]
    write_json(registry_path, registry)
    return urls


def copy_gold_deck(name: str = "Bolt × Navier (gold copy pilot)") -> str:
    service = drive_service()
    body = {"name": name}
    folder = os.environ.get("DECK_ASSETS_DRIVE_FOLDER_ID")
    if folder:
        body["parents"] = [folder]
    copied = service.files().copy(fileId=GOLD_ID, body=body, fields="id,webViewLink").execute()
    return copied["id"]


def pull_manifest(presentation_id: str) -> None:
    cfg_path = ROOT / "decks/bolt/deck.config.json"
    cfg = load_json(cfg_path)
    cfg["deck_id"] = presentation_id
    cfg["live_deck_url"] = f"https://docs.google.com/presentation/d/{presentation_id}/edit"
    cfg["last_pulled_at"] = utc_now()
    cfg["notes"] = (
        "Bolt pilot deck copied from 23-slide gold template. "
        "Deprecated sandbox 1sQNF5P3… is not refreshed. "
        "Applied via deck_bolt_pilot.py style-preserving editplan."
    )
    cfg["cover_logos"]["partner_logo"]["status"] = "banked"
    write_json(cfg_path, cfg)
    subprocess.run(
        [
            sys.executable,
            "-m",
            "deck_studio",
            "pull",
            "--root",
            str(ROOT),
            "--deck",
            "bolt",
            "--mode",
            "full",
        ],
        cwd=str(ROOT / "builders"),
        check=True,
    )


def build_editplan(presentation_id: str, asset_urls: dict[str, str]) -> dict:
    golden = load_json(ROOT / "decks/grab/golden-template-map.json")
    binding = load_json(ROOT / "decks/bolt/economics-binding.json")
    content = load_json(ROOT / "decks/bolt/content-source.json")
    econ = load_bolt_economics()
    slide1 = golden_slide_oid(golden, 1)
    ops: list[dict] = []

    title_el = element_or_fallback(golden, "p1_i8")
    subtitle_el = element_or_fallback(golden, "p1_i9")
    title_text = "The water network for Europe"
    subtitle_text = "A premium, zero-emission water layer — in your app, on your wallet."
    ops.extend(
        text_replace_ops(
            slide1,
            "p1_i8",
            title_text,
            title_el,
            op_prefix="bolt-cover-title",
            source_pointer="content-source.json partner_json_extract.hero (trimmed to char_budget)",
        )
    )
    ops.extend(
        text_replace_ops(
            slide1,
            "p1_i9",
            subtitle_text,
            subtitle_el,
            op_prefix="bolt-cover-subtitle",
            source_pointer="DETERMINISTIC-DECK-EDIT-PLAN-CONTRACT hero.subtitle register",
        )
    )
    ops.append(
        image_replace_op(
            slide1,
            "p1_i5",
            asset_urls["bolt-partner-logo"],
            op_key="bolt-cover-partner-logo",
            source_pointer="ASSET-REGISTRY bolt-partner-logo",
            method="CENTER_INSIDE",
        )
    )
    cover_asset = load_json(ROOT / "assets/ASSET-REGISTRY.json")["assets"].get("bolt-cover-hero", {})
    if cover_asset.get("status") not in ("deprecated_invalid_source", "blocked") and asset_urls.get(
        "bolt-cover-hero"
    ):
        ops.append(
            image_replace_op(
                slide1,
                "p1_i2",
                asset_urls["bolt-cover-hero"],
                op_key="bolt-cover-hero",
                source_pointer="ASSET-REGISTRY bolt-cover-hero",
                method="CENTER_CROP",
            )
        )

    slide7 = next(s for s in binding["economics_slides"] if s["slide_index"] == 7)
    fields = slide7["fields"]
    cc = econ["cost_components"]
    rev = econ["revenue_per_boat_yr"]
    opex = econ["annual_opex"]
    profit = econ["ebitda_per_boat_yr"]
    margin_pct = int(round(econ["margin"] * 100))
    payback = f"{econ['payback_years']:.1f} yrs"

    text_map = {
        "header_market": "WHAT ONE BOAT EARNS · GREECE",
        "title": "Greece: profitable from year one",
        "route_line": "Athens → Hydra (Saronic)  ·  ~30 nm  ·  N30 Pioneer II (8 seats)",
        "summary_line": (
            f"{fmt_usd(rev)} revenue  −  {fmt_usd(opex)} run cost  =  "
            f"{fmt_usd(profit)} profit / boat·yr  ·  {margin_pct}% margin  ·  {payback}"
        ),
    }
    for field_key, text in text_map.items():
        spec = fields[field_key]
        oid = spec["object_id"]
        el = element_or_fallback(golden, oid, fallback_oid="g3eec5122801_0_394")
        ops.extend(
            text_replace_ops(
                SLIDE7_OID,
                oid,
                text,
                el,
                op_prefix=f"bolt-econ7-{field_key}",
                source_pointer="finance/recal/agg-bolt.json mid Athens->Hydra",
            )
        )

    value_map = econ7_value_map(econ)
    for field_key, text in value_map.items():
        spec = fields[field_key]
        oid = spec["value_object_id"]
        ops.extend(
            econ_value_replace_ops(
                SLIDE7_OID,
                oid,
                text,
                op_prefix=f"bolt-econ7-val-{field_key}",
                source_pointer="finance/recal/agg-bolt.json mid Athens->Hydra",
            )
        )

    plan = {
        "deck_key": "bolt",
        "partner_slug": "bolt",
        "presentation_id": presentation_id,
        "gold_template_id": GOLD_ID,
        "deprecated_sandbox_id": "1sQNF5P3OjhAlSh917yO6If1OPBGnwOBvrBzGXcYZh4c",
        "mode": "slides_api_batch_update",
        "status": "ready_to_apply",
        "request_summary": (
            "Bolt pilot bind: cover hero/title/subtitle + bolt logo + Greece/Aegean cover "
            "+ slide-7 Athens→Hydra mid economics from agg-bolt.json"
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
        "leak_denylist": LEAK_DENYLIST,
        "operations": ops,
        "created_at": utc_now(),
        "applied_at": None,
    }
    return plan


def drift_gate(presentation_id: str, plan: dict) -> dict:
    service = slides_service()
    pres = service.presentations().get(presentationId=presentation_id).execute()
    live_ids = set()
    for slide in pres.get("slides", []):
        live_ids.add(slide["objectId"])
        for el in slide.get("pageElements", []):
            live_ids.add(el["objectId"])
    expected = {op["target_object_id"] for op in plan["operations"]}
    missing = sorted(expected - live_ids)
    slide_count = len(pres.get("slides", []))
    return {
        "pass": not missing and slide_count == 23,
        "slide_count": slide_count,
        "missing_object_ids": missing,
        "expected_ops": len(plan["operations"]),
    }


def apply_plan(plan: dict, *, chunk_size: int = 40) -> int:
    service = slides_service()
    requests = [op["google_slides_request"] for op in plan["operations"]]
    applied = 0
    for i in range(0, len(requests), chunk_size):
        chunk = requests[i : i + chunk_size]
        service.presentations().batchUpdate(
            presentationId=plan["presentation_id"], body={"requests": chunk}
        ).execute()
        applied += len(chunk)
    return applied


def collect_slide_text(pres: dict) -> str:
    parts: list[str] = []
    for slide in pres.get("slides", []):
        for el in slide.get("pageElements", []):
            shape = el.get("shape", {})
            text = shape.get("text", {})
            for elem in text.get("textElements", []):
                if "textRun" in elem:
                    parts.append(elem["textRun"].get("content", ""))
    return "".join(parts)


def leak_scan(
    presentation_id: str,
    denylist: list[str],
    *,
    slide_indexes: list[int] | None = None,
) -> dict:
    service = slides_service()
    pres = service.presentations().get(presentationId=presentation_id).execute()
    slides = pres.get("slides", [])
    if slide_indexes:
        slides = [slides[i - 1] for i in slide_indexes if 0 < i <= len(slides)]
    blob = collect_slide_text({"slides": slides})
    hits = []
    for token in denylist:
        if token.lower() in blob.lower():
            hits.append(token)
    return {"pass": not hits, "hits": hits, "slide_indexes": slide_indexes or "all"}


def export_thumbnails(presentation_id: str, out_dir: Path, *, max_slides: int = 5) -> list[str]:
    service = slides_service()
    pres = service.presentations().get(presentationId=presentation_id).execute()
    out_dir.mkdir(parents=True, exist_ok=True)
    saved = []
    for slide in pres.get("slides", [])[:max_slides]:
        page_id = slide["objectId"]
        thumb = (
            service.presentations()
            .pages()
            .getThumbnail(
                presentationId=presentation_id,
                pageObjectId=page_id,
                thumbnailProperties_mimeType="PNG",
            )
            .execute()
        )
        url = thumb.get("contentUrl")
        if not url:
            continue
        idx = pres["slides"].index(slide) + 1
        dest = out_dir / f"slide-{idx:02d}.png"
        with urllib.request.urlopen(url) as resp:
            dest.write_bytes(resp.read())
        saved.append(str(dest))
    return saved


def run_qa(presentation_id: str, plan: dict) -> dict:
    drift = drift_gate(presentation_id, plan)
    deny = plan.get("leak_denylist", LEAK_DENYLIST)
    leak_edited = leak_scan(presentation_id, deny, slide_indexes=[1, 7])
    leak_full = leak_scan(presentation_id, deny)
    thumbs = export_thumbnails(presentation_id, ROOT / "decks/bolt/qa-receipts/thumbnails")
    pilot_pass = drift["pass"] and leak_edited["pass"] and bool(thumbs)
    status = "pass" if pilot_pass and leak_full["pass"] else ("pass_with_flags" if pilot_pass else "fail")
    checks = [
        {"name": "drift_gate", "status": "pass" if drift["pass"] else "fail", "details": json.dumps(drift)},
        {
            "name": "leak_denylist_edited_slides",
            "status": "pass" if leak_edited["pass"] else "fail",
            "details": json.dumps(leak_edited),
        },
        {
            "name": "leak_denylist_full_deck",
            "status": "warning" if not leak_full["pass"] else "pass",
            "details": json.dumps(leak_full),
        },
        {
            "name": "render_thumbnails",
            "status": "pass" if thumbs else "fail",
            "details": ", ".join(thumbs),
        },
    ]
    receipt = {
        "deck_key": "bolt",
        "presentation_id": presentation_id,
        "status": status,
        "generated_at": utc_now(),
        "checks": checks,
        "gates": {
            "drift_gate": drift,
            "leak_denylist_edited_slides": leak_edited,
            "leak_denylist_full_deck": leak_full,
            "render_thumbnails": {"pass": bool(thumbs), "files": thumbs},
        },
        "pilot_scope": "slides 1 (cover) + 7 (Greece economics); remaining 21 slides hold Grab residue until wave-2 editplan",
        "operation_count": len(plan.get("operations", [])),
        "live_deck_url": f"https://docs.google.com/presentation/d/{presentation_id}/edit",
    }
    write_json(ROOT / "decks/bolt/qa-receipts/bolt-pilot-apply-receipt.json", receipt)
    return receipt


def cmd_run_all() -> int:
    print("1/6 Register + publish bolt logo...")
    urls = register_bolt_assets()
    print(f"   published: {list(urls)}")

    print("2/6 Copy gold deck (23 slides)...")
    presentation_id = copy_gold_deck()
    print(f"   presentation_id: {presentation_id}")

    print("3/6 Pull manifest + populate editplan...")
    pull_manifest(presentation_id)
    plan = build_editplan(presentation_id, urls)
    plan_path = ROOT / "decks/bolt/deck.editplan.json"
    write_json(plan_path, plan)
    print(f"   operations: {len(plan['operations'])}")

    drift = drift_gate(presentation_id, plan)
    if not drift["pass"]:
        print(json.dumps(drift, indent=2), file=sys.stderr)
        raise SystemExit("Drift gate failed before apply")
    print("   drift gate: pass")

    print("4/6 Apply editplan...")
    applied = apply_plan(plan)
    plan["applied_at"] = utc_now()
    plan["status"] = "applied"
    write_json(plan_path, plan)
    print(f"   applied {applied} requests")

    print("5/6 QA + thumbnails...")
    receipt = run_qa(presentation_id, plan)
    print(json.dumps(receipt, indent=2))
    return 0 if receipt["status"] in ("pass", "pass_with_flags") else 1


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Bolt gold-deck pilot")
    ap.add_argument(
        "command",
        choices=[
            "run-all",
            "generate-greece",
            "register-assets",
            "copy-gold",
            "populate-editplan",
            "fix-econ7-formatting",
            "apply",
            "qa",
        ],
    )
    ap.add_argument("--presentation-id")
    args = ap.parse_args()

    if args.command == "run-all":
        return cmd_run_all()
    if args.command == "generate-greece":
        p = generate_greece_cover()
        print(p)
        return 0
    if args.command == "register-assets":
        print(json.dumps(register_bolt_assets(), indent=2))
        return 0
    if args.command == "copy-gold":
        pid = copy_gold_deck()
        pull_manifest(pid)
        print(pid)
        return 0
    if args.command == "fix-econ7-formatting":
        cfg = load_json(ROOT / "decks/bolt/deck.config.json")
        presentation_id = args.presentation_id or cfg["deck_id"]
        ops = build_econ7_value_fix_ops()
        plan = {
            "deck_key": "bolt",
            "presentation_id": presentation_id,
            "mode": "slides_api_batch_update",
            "request_summary": "Fix slide-7 economics value cells: full-range Exo-2 style + END alignment",
            "safety": {
                "no_pptx_roundtrip": True,
                "no_full_deck_replace": True,
                "preserve_object_ids": True,
                "human_review_required_for_external_send": True,
            },
            "operations": ops,
            "qa_gates": ["econ_value_format_gate"],
            "created_at": utc_now(),
        }
        fix_path = ROOT / "decks/bolt/deck.econ7-value-fix.json"
        write_json(fix_path, plan)
        n = apply_plan(plan)
        print(json.dumps({"applied": n, "operations": len(ops), "plan": str(fix_path)}, indent=2))
        return 0
    if args.command == "populate-editplan":
        if not args.presentation_id:
            cfg = load_json(ROOT / "decks/bolt/deck.config.json")
            args.presentation_id = cfg["deck_id"]
        registry = load_json(ROOT / "assets/ASSET-REGISTRY.json")
        urls = {"bolt-partner-logo": registry["assets"]["bolt-partner-logo"]["source_url"]}
        cover = registry["assets"].get("bolt-cover-hero", {})
        if cover.get("source_url") and cover.get("status") not in (
            "deprecated_invalid_source",
            "blocked",
        ):
            urls["bolt-cover-hero"] = cover["source_url"]
        plan = build_editplan(args.presentation_id, urls)
        write_json(ROOT / "decks/bolt/deck.editplan.json", plan)
        print(json.dumps({"operations": len(plan["operations"]), "presentation_id": args.presentation_id}, indent=2))
        return 0
    if args.command == "apply":
        plan = load_json(ROOT / "decks/bolt/deck.editplan.json")
        n = apply_plan(plan)
        plan["applied_at"] = utc_now()
        plan["status"] = "applied"
        write_json(ROOT / "decks/bolt/deck.editplan.json", plan)
        print(f"applied {n}")
        return 0
    if args.command == "qa":
        plan = load_json(ROOT / "decks/bolt/deck.editplan.json")
        receipt = run_qa(plan["presentation_id"], plan)
        print(json.dumps(receipt, indent=2))
        return 0 if receipt["status"] in ("pass", "pass_with_flags") else 1
    return 1


if __name__ == "__main__":
    raise SystemExit(main())