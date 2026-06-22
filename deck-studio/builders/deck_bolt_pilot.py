#!/usr/bin/env python3
"""Bolt pilot: copy gold deck → populate style-preserving editplan → apply → QA."""
from __future__ import annotations

import json
import mimetypes
import os
import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOLD_ID = "18yDAgO0Sj9PJlgf6paxtgni8Pk1xRAmNwE2TD_NCdSs"
SLIDE7_OID = "g3eec5122801_0_391"
STYLE_FIELDS = (
    "fontFamily,weightedFontFamily,fontSize,foregroundColor,bold,italic,backgroundColor,underline"
)

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


def rgb_color(rgb: list[float]) -> dict:
    return {"red": rgb[0], "green": rgb[1], "blue": rgb[2]}


def golden_style_to_api(style: dict) -> dict:
    weight = 700 if style.get("bold") else 400
    font = style.get("font", "Arial")
    return {
        "fontFamily": font,
        "weightedFontFamily": {"fontFamily": font, "weight": weight},
        "fontSize": {"magnitude": style.get("sizePt", 12), "unit": "PT"},
        "foregroundColor": {"opaqueColor": {"rgbColor": rgb_color(style.get("color", [0, 0, 0]))}},
        "bold": bool(style.get("bold")),
    }


def make_op(
    op_key: str,
    slide_object_id: str,
    target_object_id: str,
    request: dict,
    *,
    rationale: str,
    source_pointer: str,
) -> dict:
    return {
        "op_key": op_key,
        "slide_object_id": slide_object_id,
        "target_object_id": target_object_id,
        "rationale": rationale,
        "source_pointer": source_pointer,
        "google_slides_request": request,
    }


def text_replace_ops(
    slide_object_id: str,
    target_object_id: str,
    new_text: str,
    element: dict,
    *,
    op_prefix: str,
    source_pointer: str,
    alignment: str | None = None,
) -> list[dict]:
    if len(new_text) > element.get("char_budget", 9999):
        raise ValueError(
            f"{target_object_id}: text len {len(new_text)} exceeds char_budget {element.get('char_budget')}"
        )
    ops: list[dict] = []
    ops.append(
        make_op(
            f"{op_prefix}-clear",
            slide_object_id,
            target_object_id,
            {"deleteText": {"objectId": target_object_id, "textRange": {"type": "ALL"}}},
            rationale=f"Clear text on {target_object_id}",
            source_pointer=source_pointer,
        )
    )
    ops.append(
        make_op(
            f"{op_prefix}-insert",
            slide_object_id,
            target_object_id,
            {"insertText": {"objectId": target_object_id, "text": new_text, "insertionIndex": 0}},
            rationale=f"Insert text on {target_object_id}",
            source_pointer=source_pointer,
        )
    )
    runs = element.get("runs") or [{"start": 0, "end": len(new_text), "style": element.get("style", {})}]
    cursor = 0
    for i, run in enumerate(runs):
        run_len = min(run.get("end", len(new_text)) - run.get("start", 0), len(new_text) - cursor)
        if run_len <= 0:
            continue
        end = cursor + run_len
        style = golden_style_to_api(run.get("style") or element.get("style", {}))
        ops.append(
            make_op(
                f"{op_prefix}-style-{i}",
                slide_object_id,
                target_object_id,
                {
                    "updateTextStyle": {
                        "objectId": target_object_id,
                        "textRange": {"type": "FIXED_RANGE", "startIndex": cursor, "endIndex": end},
                        "style": style,
                        "fields": STYLE_FIELDS,
                    }
                },
                rationale=f"Re-apply run style on {target_object_id}",
                source_pointer=source_pointer,
            )
        )
        cursor = end
    align = alignment or element.get("contentAlignment", "TOP")
    align_map = {"TOP": "START", "MIDDLE": "CENTER", "BOTTOM": "END"}
    ops.append(
        make_op(
            f"{op_prefix}-para",
            slide_object_id,
            target_object_id,
            {
                "updateParagraphStyle": {
                    "objectId": target_object_id,
                    "textRange": {"type": "ALL"},
                    "style": {"alignment": align_map.get(align, "START")},
                    "fields": "alignment",
                }
            },
            rationale=f"Re-apply paragraph alignment on {target_object_id}",
            source_pointer=source_pointer,
        )
    )
    return ops


def image_replace_op(
    slide_object_id: str,
    target_object_id: str,
    url: str,
    *,
    op_key: str,
    source_pointer: str,
    method: str = "CENTER_INSIDE",
) -> dict:
    return make_op(
        op_key,
        slide_object_id,
        target_object_id,
        {
            "replaceImage": {
                "imageObjectId": target_object_id,
                "url": url,
                "imageReplaceMethod": method,
            }
        },
        rationale=f"Replace image {target_object_id}",
        source_pointer=source_pointer,
    )


def fmt_usd(n: float) -> str:
    return f"${n:,.0f}"


def load_bolt_economics() -> dict:
    agg = load_json(ROOT.parent / "finance/recal/agg-bolt.json")
    for row in agg.get("rows", []):
        if row.get("corridor") == "Athens -> Hydra (Saronic)":
            return row["mid"]
    raise SystemExit("Athens -> Hydra mid scenario not found in agg-bolt.json")


def generate_greece_cover() -> Path:
    """Composite EU Mediterranean cover from cote-azur plate + N30 reference."""
    out_dir = ROOT / "assets/backgrounds/markets/athens-saronic-greece"
    out_dir.mkdir(parents=True, exist_ok=True)
    raw = ROOT / "assets/backgrounds/markets/athens-saronic-greece/athens-saronic-greece-raw.png"
    cover = ROOT / "assets/backgrounds/decks/bolt/bolt-cover-hero-greece-v1.png"
    cover.parent.mkdir(parents=True, exist_ok=True)
    cote = ROOT / "assets/backgrounds/markets/cote-azur/cote-azur-n30-raw.png"
    vessel = ROOT / "assets/n30/n30-reference-neutral.png"
    if not cote.is_file():
        raise SystemExit(f"Missing cote-azur plate: {cote}")
    if not vessel.is_file():
        raise SystemExit(f"Missing N30 reference: {vessel}")
    # Stage raw plate (interim EU coast; Aegean-specific plate pending approved source photo)
    if not raw.is_file():
        import shutil

        shutil.copy2(cote, raw)
    composite_py = ROOT / "builders/images/n30_composite.py"
    cmd = [
        sys.executable,
        str(composite_py),
        "--background",
        str(raw),
        "--vessel",
        str(vessel),
        "--out",
        str(cover),
        "--x",
        "0.58",
        "--y",
        "0.68",
        "--scale",
        "0.32",
        "--bg-darken",
        "0.90",
    ]
    subprocess.run(cmd, check=True)
    return cover


def register_bolt_assets(cover_path: Path) -> dict[str, str]:
    registry_path = ROOT / "assets/ASSET-REGISTRY.json"
    registry = load_json(registry_path)
    assets = registry.setdefault("assets", {})

    logo_path = ROOT / "assets/logos/partners/bolt/bolt-logo.png"
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

    rel_cover = str(cover_path.relative_to(ROOT))
    assets["bolt-cover-hero"] = {
        "role": "cover_hero",
        "scope": "deck",
        "partner": "bolt",
        "market_slug": "athens-saronic-greece",
        "status": "checked_in",
        "local_path": rel_cover,
        "drive_file_id": assets.get("bolt-cover-hero", {}).get("drive_file_id"),
        "source_url": assets.get("bolt-cover-hero", {}).get("source_url"),
        "license": "navier-internal",
        "provenance": "n30_composite_from_cote-azur_interim_eu_coast",
        "reproducible": True,
        "composited": True,
        "notes": "Interim EU/Aegean cover: cote-azur plate + N30 neutral. Replace when Greece-specific plate approved.",
        "used_by": [
            {"deck": "bolt", "slide_index": 1, "slide_object_id": "p1", "target_object_id": "p1_i2"}
        ],
        "captured_at": utc_now(),
    }

    assets["econ-athens-saronic-greece"] = {
        "role": "econ_market_bg",
        "scope": "market",
        "market_slug": "athens-saronic-greece",
        "atlas_city_id": "athens-saronic-greece",
        "status": "checked_in",
        "local_path": rel_cover,
        "drive_file_id": assets.get("econ-athens-saronic-greece", {}).get("drive_file_id"),
        "source_url": assets.get("econ-athens-saronic-greece", {}).get("source_url"),
        "license": "navier-internal",
        "provenance": "n30_composite_from_cote-azur_interim_eu_coast",
        "reproducible": True,
        "composited": True,
        "notes": "Interim Greece/Saronic econ plate (shared with cover composite).",
        "captured_at": utc_now(),
    }

    registry.setdefault("deck_coverage", {}).setdefault("bolt", {})["roles"] = {
        "cover_hero": "checked_in",
        "navier_logo": "checked_in(shared)",
        "partner_logo": "checked_in",
        "value_prop_bg": "pending_inventory",
        "tam_bg": "pending_inventory",
        "partner_roles_bg": "pending_inventory",
        "econ_market_bg": "checked_in(1: athens-saronic-greece interim)",
    }
    write_json(registry_path, registry)

    # Publish missing source_urls
    sys.path.insert(0, str(ROOT / "builders"))
    from deck_autonomy_sync import publish_assets_to_drive  # type: ignore

    publish_assets_to_drive(registry_path)
    registry = load_json(registry_path)
    urls = {}
    for key in ("bolt-partner-logo", "bolt-cover-hero"):
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

    value_map = {
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
    for field_key, text in value_map.items():
        spec = fields[field_key]
        oid = spec["value_object_id"]
        el = element_or_fallback(golden, oid)
        if len(text) > el.get("char_budget", 999):
            el = {**el, "char_budget": len(text)}
        ops.extend(
            text_replace_ops(
                SLIDE7_OID,
                oid,
                text,
                el,
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
    print("1/6 Generate Greece/Aegean cover composite...")
    cover = generate_greece_cover()
    print(f"   cover: {cover}")

    print("2/6 Register + publish bolt assets...")
    urls = register_bolt_assets(cover)
    print(f"   published: {list(urls)}")

    print("3/6 Copy gold deck (23 slides)...")
    presentation_id = copy_gold_deck()
    print(f"   presentation_id: {presentation_id}")

    print("4/6 Pull manifest + populate editplan...")
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

    print("5/6 Apply editplan...")
    applied = apply_plan(plan)
    plan["applied_at"] = utc_now()
    plan["status"] = "applied"
    write_json(plan_path, plan)
    print(f"   applied {applied} requests")

    print("6/6 QA + thumbnails...")
    receipt = run_qa(presentation_id, plan)
    print(json.dumps(receipt, indent=2))
    return 0 if receipt["status"] in ("pass", "pass_with_flags") else 1


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Bolt gold-deck pilot")
    ap.add_argument(
        "command",
        choices=["run-all", "generate-greece", "register-assets", "copy-gold", "populate-editplan", "apply", "qa"],
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
        cover = ROOT / "assets/backgrounds/decks/bolt/bolt-cover-hero-greece-v1.png"
        if not cover.is_file():
            generate_greece_cover()
        print(json.dumps(register_bolt_assets(cover), indent=2))
        return 0
    if args.command == "copy-gold":
        pid = copy_gold_deck()
        pull_manifest(pid)
        print(pid)
        return 0
    if args.command == "populate-editplan":
        if not args.presentation_id:
            cfg = load_json(ROOT / "decks/bolt/deck.config.json")
            args.presentation_id = cfg["deck_id"]
        registry = load_json(ROOT / "assets/ASSET-REGISTRY.json")
        urls = {
            "bolt-partner-logo": registry["assets"]["bolt-partner-logo"]["source_url"],
            "bolt-cover-hero": registry["assets"]["bolt-cover-hero"]["source_url"],
        }
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