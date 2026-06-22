#!/usr/bin/env python3
"""PR #65 Deck Studio content pass: text apply, slide trim, economics bind, QA receipts."""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from deck_studio.cli import (
    deck_dir,
    get_slides_service,
    load_json,
    plan_has_forbidden,
    write_json,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
DECK_ROOT = REPO_ROOT / "deck-studio"
ECON_MAP_PATH = REPO_ROOT / "finance" / "economics_url_map.json"
HANDOFF = REPO_ROOT / "handoff" / "partner-map-model"
AUDIT_SCRIPT = REPO_ROOT / "scripts" / "audit_partner_page_qa.py"

PR65_DECKS = [
    "adani-ports",
    "bolt",
    "caribbean-mobility",
    "noon",
    "ola",
    "rapido",
    "reliance-industries",
    "uber-india",
    "uber-mena",
    "yango",
    "yassir",
]

QA_PARTNER_SLUG = {
    "adani-ports": "adani-ports",
    "bolt": "bolt",
    "caribbean-mobility": "caribbean-mobility",
    "noon": "noon",
    "ola": "ola",
    "rapido": "rapido",
    "reliance-industries": "reliance-industries",
    "uber-india": "uber-india",
    "uber-mena": "uber",
    "yango": "yango",
    "yassir": "yassir",
}

ECON_PARTNER_KEY = {
    "uber-india": "uber-india",
    "uber-mena": "uber",
}

SKIP_PHRASES = ("privileged", "confidential", "distribution without consent")
MAX_TITLE = 120
MAX_BODY = 900


def _clip(text: str, limit: int) -> str:
    text = re.sub(r"\s+", " ", (text or "").strip())
    if len(text) <= limit:
        return text
    return text[: limit - 1].rsplit(" ", 1)[0] + "…"


def _shape_text(shape_el: dict) -> str:
    text = shape_el.get("shape", {}).get("text", {})
    return "".join(
        te.get("textRun", {}).get("content", "") for te in text.get("textElements", [])
    ).strip()


def _shape_area(shape_el: dict) -> float:
    size = shape_el.get("size", {})
    transform = shape_el.get("transform", {})
    w = size.get("width", {}).get("magnitude", 0) * abs(transform.get("scaleX", 1) or 1)
    h = size.get("height", {}).get("magnitude", 0) * abs(transform.get("scaleY", 1) or 1)
    return w * h


def _editable_text_shapes(slide: dict) -> list[dict]:
    shapes = []
    for el in slide.get("pageElements", []):
        content = _shape_text(el)
        if not content:
            continue
        lower = content.lower()
        if any(p in lower for p in SKIP_PHRASES):
            continue
        shapes.append(
            {
                "object_id": el["objectId"],
                "text": content,
                "area": _shape_area(el),
            }
        )
    shapes.sort(key=lambda s: s["area"], reverse=True)
    return shapes


def _fmt_journeys(journeys: list[dict], limit: int = 4) -> str:
    lines = []
    for j in journeys[:limit]:
        rid = j.get("route_id") or "held-null"
        lines.append(
            f"• {j.get('from', '?')} → {j.get('to', '?')} ({j.get('distance_nm', '?')} nm) — route_id: {rid}"
        )
    return "\n".join(lines)


def _fmt_markets(markets: list[str], limit: int = 8) -> str:
    return "\n".join(f"• {m}" for m in markets[:limit])


def _parse_dictish(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        if value.startswith("{") and value.endswith("}"):
            try:
                obj = json.loads(value.replace("'", '"'))
                return " ".join(str(v) for v in obj.values() if v)
            except json.JSONDecodeError:
                return value
        return value
    if isinstance(value, dict):
        return " ".join(str(v) for v in value.values() if v)
    return str(value)


def _slide_outline(content: dict) -> list[dict]:
    if content.get("slides") and content["slides"][0].get("slide_index") is not None:
        return [
            {
                "n": s["slide_index"],
                "slide_key": s.get("slide_key", ""),
                "title": s.get("title", ""),
            }
            for s in content["slides"]
        ]
    outline = content.get("sections", {}).get("slide_outline") or content.get("slide_outline") or []
    return outline


def _build_slide_copy(deck_key: str, content: dict, outline: list[dict], route_qa: dict | None) -> dict[int, dict]:
    sections = content.get("sections", {})
    extract = content.get("partner_json_extract", {})
    slides: dict[int, dict] = {}

    hero = sections.get("hero") or {}
    partner_ctx = sections.get("partner_context") or {}
    economics_url = (
        extract.get("economics", {}).get("economics_url")
        or content.get("partner_json_extract", {}).get("economics", {}).get("economics_url")
    )

    markets = (
        extract.get("canonical_market_scope")
        or sections.get("canonical_market_scope")
        or content.get("canonical_market_scope")
        or []
    )
    journeys = extract.get("journeys_unlocked_sample") or sections.get("journeys_unlocked_sample") or []
    phases = sections.get("phases") or extract.get("phases") or []

    for item in outline:
        n = item.get("n") or item.get("slide_index")
        if not n:
            continue
        key = item.get("slide_key", "")
        title = item.get("title", "")
        body = ""
        source = f"content-source.json slide_key={key}"

        if key == "hero" or n == 1:
            title = _clip(hero.get("title") or extract.get("hero") or title, MAX_TITLE)
            body = _clip(
                hero.get("subtitle")
                or hero.get("what_we_do_together")
                or extract.get("why_now")
                or sections.get("why_now", ""),
                MAX_BODY,
            )
        elif key in ("why-partner", "why-yassir", "regional-opportunity") or n == 2:
            title = _clip(title or "Why this partner", MAX_TITLE)
            body = _clip(
                partner_ctx.get("where_navier_fits")
                or extract.get("multimodal_fit")
                or sections.get("multimodal_fit", ""),
                MAX_BODY,
            )
        elif key in ("validated-footprint", "priority-markets") or n == 3:
            title = _clip(title or "Validated footprint", MAX_TITLE)
            body = _fmt_markets(markets if isinstance(markets, list) else [])
            if sections.get("positioning"):
                body = _clip(sections["positioning"], 200) + "\n\n" + body
        elif key in ("launch-markets", "launch-market-candidates", "use-case-map") or n == 4:
            title = _clip(title or "Launch markets", MAX_TITLE)
            body = _fmt_journeys(journeys)
            if not body and markets:
                body = _fmt_markets(markets)
        elif key in ("use-cases",) or n == 5:
            title = _clip(title or "Use cases", MAX_TITLE)
            body = _clip(extract.get("multimodal_fit") or sections.get("multimodal_fit", ""), MAX_BODY)
            if journeys:
                body = body + "\n\n" + _fmt_journeys(journeys, 3) if body else _fmt_journeys(journeys, 3)
        elif key in ("fleet-fit", "product-fit") or n == 6:
            title = _clip(title or "Fleet fit", MAX_TITLE)
            if phases:
                body = "\n".join(
                    f"Phase {p.get('n', '?')}: {p.get('label', '')}" for p in phases[:3]
                )
            elif journeys:
                body = "\n".join(
                    f"• {j.get('platform', 'N30')} — {j.get('from', '')} → {j.get('to', '')}"
                    for j in journeys[:4]
                )
        elif key == "economics" or n == 7:
            title = _clip(title or "Economics", MAX_TITLE)
            if economics_url:
                body = f"Live unit economics Sheet:\n{economics_url}"
            else:
                body = (
                    "Economics artifacts exist locally; published Sheet URL still pending "
                    "(held-null — no invented numbers)."
                )
        elif key in ("integration", "operating-model", "partner-operating-model") or n == 8:
            title = _clip(title or "Integration model", MAX_TITLE)
            body = _clip(
                _parse_dictish(extract.get("the_ask"))
                or partner_ctx.get("where_navier_fits", ""),
                MAX_BODY,
            )
        elif key in ("rollout", "launch-model", "expansion-roadmap", "city-rollout") or n == 9:
            title = _clip(title or "Rollout", MAX_TITLE)
            if phases:
                body = "\n".join(
                    f"Phase {p.get('n')}: {p.get('label', '')} — {p.get('timeline', '')}".strip(" —")
                    for p in phases[:4]
                )
            else:
                body = _clip(extract.get("close") or sections.get("close", ""), MAX_BODY)
        elif key == "grok-appendix" or n == 10:
            title = _clip(title or "Route appendix (Grok-sealed)", MAX_TITLE)
            if route_qa:
                c = route_qa.get("counts", {})
                body = (
                    f"Page QA: {route_qa.get('verdict', 'unknown')}\n"
                    f"Journeys linked: {c.get('journeys_linked', 0)}/{c.get('journeys', 0)}\n"
                    f"Featured linked: {c.get('featured_linked', 0)}/{c.get('featured_routes', 0)}\n"
                    f"Map routes in scope: {c.get('map_routes_in_scope', 0)}"
                )
                flags = route_qa.get("flags") or []
                if flags:
                    body += "\nFlags: " + "; ".join(f"{f['check']}" for f in flags[:4])
            body += "\n\n" + _fmt_journeys(journeys, 5)
        elif key == "next-steps" or n == 11:
            title = _clip(title or "Next steps", MAX_TITLE)
            body = (
                "1. Human review of live draft\n"
                "2. N30 composites when source-approved backgrounds exist\n"
                "3. Economics Sheet in-place publish where pending\n"
                "4. Route ID seal + render QA receipts"
            )

        slides[int(n)] = {
            "title": title,
            "body": _clip(body, MAX_BODY),
            "slide_key": key,
            "source_pointer": source,
        }
    return slides


def bind_economics(cfg: dict, econ_map: dict) -> bool:
    deck_key = cfg["deck_key"]
    partner_key = ECON_PARTNER_KEY.get(deck_key, cfg.get("partner_id", deck_key))
    url = econ_map.get(partner_key)
    if not url:
        return False
    cfg["economics_url"] = url
    m = re.search(r"/d/([^/]+)", url)
    if m:
        cfg["economics_sheet_id"] = m.group(1)
    return True


def image_provenance_ledger(deck_key: str, image_manifest: dict) -> dict:
    images = []
    for img in image_manifest.get("images", []):
        images.append(
            {
                "image_key": img.get("image_key"),
                "status": "held_null",
                "reason": (
                    "No source-approved market background or canonical n30.png in repo. "
                    "IMAGE-RULES forbid Atlas-generated or generic decorative imagery."
                ),
                "target_slide_object_id": img.get("target_slide_object_id"),
                "provenance_required": img.get("provenance_required", True),
            }
        )
    return {
        "deck_key": deck_key,
        "status": "held_null_pending_approved_assets",
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "images": images,
        "notes": "Composite jobs blocked until approved backgrounds and vessel assets are checked in or registered.",
    }


def run_route_qa(partner_slug: str) -> dict | None:
    if not AUDIT_SCRIPT.is_file():
        return None
    subprocess.run(
        [sys.executable, str(AUDIT_SCRIPT), "--partner", partner_slug],
        cwd=str(REPO_ROOT),
        check=False,
        capture_output=True,
    )
    ledger = HANDOFF / f"partner-page-qa-{partner_slug}.json"
    return load_json(ledger) if ledger.is_file() else None


def build_edit_plan(
    deck_key: str,
    cfg: dict,
    presentation: dict,
    slide_copy: dict[int, dict],
    trim_from_index: int = 12,
) -> dict:
    slides = presentation.get("slides", [])
    operations = []

    for idx, slide in enumerate(slides[:11], 1):
        copy = slide_copy.get(idx)
        if not copy:
            continue
        shapes = _editable_text_shapes(slide)
        if not shapes:
            continue
        sid = slide["objectId"]
        if shapes:
            operations.append(
                {
                    "op_key": f"{deck_key}-slide{idx}-title",
                    "slide_object_id": sid,
                    "target_object_id": shapes[0]["object_id"],
                    "rationale": f"Partner hero/title for slide {idx} ({copy['slide_key']})",
                    "source_pointer": copy["source_pointer"],
                    "google_slides_request": {
                        "deleteText": {
                            "objectId": shapes[0]["object_id"],
                            "textRange": {"type": "ALL"},
                        }
                    },
                }
            )
            operations.append(
                {
                    "op_key": f"{deck_key}-slide{idx}-title-insert",
                    "slide_object_id": sid,
                    "target_object_id": shapes[0]["object_id"],
                    "rationale": f"Insert partner title slide {idx}",
                    "source_pointer": copy["source_pointer"],
                    "google_slides_request": {
                        "insertText": {
                            "objectId": shapes[0]["object_id"],
                            "text": copy["title"],
                            "insertionIndex": 0,
                        }
                    },
                }
            )
        if len(shapes) > 1 and copy.get("body"):
            operations.append(
                {
                    "op_key": f"{deck_key}-slide{idx}-body-clear",
                    "slide_object_id": sid,
                    "target_object_id": shapes[1]["object_id"],
                    "rationale": f"Clear body text slide {idx}",
                    "source_pointer": copy["source_pointer"],
                    "google_slides_request": {
                        "deleteText": {
                            "objectId": shapes[1]["object_id"],
                            "textRange": {"type": "ALL"},
                        }
                    },
                }
            )
            operations.append(
                {
                    "op_key": f"{deck_key}-slide{idx}-body-insert",
                    "slide_object_id": sid,
                    "target_object_id": shapes[1]["object_id"],
                    "rationale": f"Insert partner body slide {idx}",
                    "source_pointer": copy["source_pointer"],
                    "google_slides_request": {
                        "insertText": {
                            "objectId": shapes[1]["object_id"],
                            "text": copy["body"],
                            "insertionIndex": 0,
                        }
                    },
                }
            )

    for slide in slides[trim_from_index - 1 :] if len(slides) >= trim_from_index else []:
        operations.append(
            {
                "op_key": f"{deck_key}-trim-{slide['objectId']}",
                "slide_object_id": slide["objectId"],
                "target_object_id": slide["objectId"],
                "rationale": "Trim Grab sandbox to 11-slide PR65 outline",
                "source_pointer": "PR65 slide structure trim",
                "google_slides_request": {"deleteObject": {"objectId": slide["objectId"]}},
            }
        )

    return {
        "deck_key": deck_key,
        "presentation_id": cfg["deck_id"],
        "mode": "slides_api_batch_update",
        "request_summary": f"PR65 content apply + trim to 11 slides for {deck_key}",
        "safety": {
            "no_pptx_roundtrip": True,
            "no_full_deck_replace": True,
            "preserve_object_ids": True,
            "human_review_required_for_external_send": True,
        },
        "operations": operations,
        "qa_gates": [
            "schema_validation",
            "no_full_replace",
            "object_id_check",
            "brand_lint",
            "claim_source_check",
            "render_export",
        ],
        "created_at": datetime.datetime.utcnow().isoformat() + "Z",
    }


def apply_plan(plan: dict, manifest: dict) -> int:
    bad = plan_has_forbidden(plan)
    if bad:
        raise SystemExit("Refusing unsafe plan: " + ", ".join(bad))
    known = {s["slide_object_id"] for s in manifest.get("slides", [])}
    for op in plan.get("operations", []):
        if op["slide_object_id"] not in known and "deleteObject" not in op["google_slides_request"]:
            raise SystemExit(f"Unknown slide_object_id {op['slide_object_id']}")
    if not plan.get("operations"):
        return 0
    service = get_slides_service()
    requests = [op["google_slides_request"] for op in plan["operations"]]
    service.presentations().batchUpdate(
        presentationId=plan["presentation_id"], body={"requests": requests}
    ).execute()
    return len(requests)


def update_manifest_outline(root: Path, deck_key: str, outline: list[dict], slide_copy: dict[int, dict]) -> None:
    manifest_path = deck_dir(root, deck_key) / "slide-manifest.json"
    manifest = load_json(manifest_path)
    slides = manifest.get("slides", [])[:11]
    for i, slide in enumerate(slides, 1):
        item = next((o for o in outline if (o.get("n") or o.get("slide_index")) == i), {})
        copy = slide_copy.get(i, {})
        slide["title"] = copy.get("title") or item.get("title")
        slide["purpose"] = item.get("purpose") or copy.get("slide_key")
        slide["notes"] = "PR65 content applied; trimmed from Grab sandbox."
    manifest["slides"] = slides
    manifest["slide_count"] = len(slides)
    manifest["source"] = "live_google_slides_pr65_content_applied"
    manifest["object_inventory_status"] = "full_inventory_pulled"
    manifest["qa_notes"] = [
        "PR65 content lane: partner text applied, slides 12–23 trimmed.",
        "Re-pull recommended after major structural edits.",
    ]
    write_json(manifest_path, manifest)


def process_deck(root: Path, deck_key: str, econ_map: dict, dry_run: bool = False) -> dict:
    d = deck_dir(root, deck_key)
    cfg = load_json(d / "deck.config.json")
    content = load_json(d / "content-source.json")
    image_manifest = load_json(d / "image-manifest.json")
    manifest = load_json(d / "slide-manifest.json")

    econ_bound = bind_economics(cfg, econ_map)
    if econ_bound:
        write_json(d / "deck.config.json", cfg)
        url = cfg["economics_url"]
        if content.get("partner_json_extract", {}).get("economics") is not None:
            content["partner_json_extract"].setdefault("economics", {})["economics_url"] = url
            content["partner_json_extract"]["economics"]["economics_url_present_in_partner_json"] = True
            write_json(d / "content-source.json", content)

    partner_slug = QA_PARTNER_SLUG.get(deck_key, deck_key)
    route_qa = run_route_qa(partner_slug)
    if route_qa:
        (d / "ledgers").mkdir(parents=True, exist_ok=True)
        write_json(d / "ledgers" / "route-render-qa.json", route_qa)

    prov = image_provenance_ledger(deck_key, image_manifest)
    (d / "ledgers").mkdir(parents=True, exist_ok=True)
    write_json(d / "ledgers" / "image-provenance-ledger.json", prov)

    outline = _slide_outline(content)
    slide_copy = _build_slide_copy(deck_key, content, outline, route_qa)

    service = get_slides_service()
    presentation = service.presentations().get(presentationId=cfg["deck_id"]).execute()
    plan = build_edit_plan(deck_key, cfg, presentation, slide_copy)
    plan_path = root / "out" / f"{deck_key}-pr65-content-plan.json"
    write_json(plan_path, plan)

    applied = 0
    if not dry_run:
        applied = apply_plan(plan, manifest)
        cfg["last_pulled_at"] = datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
        cfg["notes"] = (
            (cfg.get("notes", "") + " PR65 content applied; 11-slide trim.").strip()
        )
        write_json(d / "deck.config.json", cfg)
        child_env = os.environ.copy()
        child_env["PYTHONPATH"] = str(root / "builders")
        child_env.setdefault("GOOGLE_TOKEN_PATH", str(Path.home() / ".config/google-drive-mcp/tokens.json"))
        subprocess.run(
            [sys.executable, "-m", "deck_studio", "pull", "--root", str(root), "--deck", deck_key, "--mode", "full"],
            cwd=str(root),
            env=child_env,
            check=True,
            capture_output=True,
        )
        update_manifest_outline(root, deck_key, outline, slide_copy)
        subprocess.run(
            [
                sys.executable,
                "-m",
                "deck_studio",
                "qa",
                "--root",
                str(root),
                "--deck",
                deck_key,
                "--receipt",
                str(d / "qa-receipts" / "pr65-content-qa.json"),
            ],
            cwd=str(root),
            env=child_env,
            check=True,
            capture_output=True,
        )

    return {
        "deck_key": deck_key,
        "economics_bound": econ_bound,
        "economics_url": cfg.get("economics_url"),
        "route_qa_verdict": (route_qa or {}).get("verdict"),
        "operations": len(plan.get("operations", [])),
        "applied_requests": applied,
        "image_status": prov["status"],
        "plan_path": str(plan_path),
        "dry_run": dry_run,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=str(DECK_ROOT))
    ap.add_argument("--deck", action="append")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    root = Path(args.root)
    decks = args.deck or PR65_DECKS
    econ_map = load_json(ECON_MAP_PATH).get("economics_url", {})

    results = []
    for deck in decks:
        print(f"=== {deck} ===", flush=True)
        results.append(process_deck(root, deck, econ_map, dry_run=args.dry_run))

    report = {
        "lane": "pr65-deck-content",
        "completed_at": datetime.datetime.utcnow().isoformat() + "Z",
        "decks": results,
    }
    write_json(root / "out" / "pr65-content-lane-report.json", report)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())