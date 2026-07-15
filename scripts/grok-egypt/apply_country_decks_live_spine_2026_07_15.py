#!/usr/bin/env python3
"""Deterministic live apply: restructure 4 country decks to locked spine (Slides API only).

Implements GROK-SPEC-country-deck-live-apply-2026-07-15.md.
No PPTX round-trip. No wholesale presentation replace. Atlas slots left blank.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parents[2]
DECKS_ROOT = ROOT / "deck-studio" / "decks"
TOKEN_FILE = Path.home() / ".config/google-drive-mcp/tokens.json"
CLIENT_FILE = Path.home() / ".config/google-drive-mcp/gcp-oauth.keys.json"
NOW = datetime.now(timezone.utc).isoformat()

# After delete, remaining slides are rewritten by NEW order index (1-based).
# delete_indices are 1-based positions in the CURRENT (old) live deck, deleted high→low.
RESTRUCTURE = {
    "didi-brazil": {
        "target_count": 12,
        # Keep: 1,2,3,4(Rio city),5(econ),6(city→Angra),8(city→Floripa),12-16
        "delete_indices": [11, 10, 9, 7],
    },
    "indrive-brazil": {
        "target_count": 12,
        "delete_indices": [11, 10, 9, 7],
    },
    "didi-mexico": {
        "target_count": 13,
        # Keep: 1-6,8,10,12-16  delete alternating econ 7,9,11
        "delete_indices": [11, 9, 7],
    },
    "indrive-egypt": {
        "target_count": 12,
        "delete_indices": [],  # already 12; rewrite in place
    },
}

DECK_IDS = {
    "didi-brazil": "1OixKrHjQbWu0Plkvj-57SQyTFxPL5Ii8l3K6Q9umJOk",
    "didi-mexico": "1XwKRuJtMrou8NtBdc1oY3LL2Dk83dCs9MCLvNKgwq0c",
    "indrive-brazil": "1QImIe6KAee0Eajsokgh9NmH0I29lir4l2LV63e-9OxE",
    "indrive-egypt": "1Nn3BRKUahikp87zC84JMdEVrcJYppm9ZXHgndAuzsEk",
}


def get_creds() -> Credentials:
    tok = json.loads(TOKEN_FILE.read_text())
    acct = tok["accounts"].get("jaideep") or tok["accounts"][tok.get("defaultAccount", "default")]
    client = json.loads(CLIENT_FILE.read_text())
    installed = client.get("installed") or client.get("web") or {}
    creds = Credentials(
        token=acct.get("accessToken") or acct.get("access_token"),
        refresh_token=acct.get("refreshToken") or acct.get("refresh_token"),
        token_uri=installed.get("token_uri", "https://oauth2.googleapis.com/token"),
        client_id=installed.get("client_id"),
        client_secret=installed.get("client_secret"),
        scopes=(acct.get("scope") or "").split() or None,
    )
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        acct["accessToken"] = creds.token
        if creds.expiry:
            acct["expiryDate"] = int(creds.expiry.timestamp() * 1000)
        TOKEN_FILE.write_text(json.dumps(tok, indent=2))
    return creds


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def extract_shape_text(shape: dict) -> str:
    parts = []
    for te in (shape.get("text") or {}).get("textElements") or []:
        tr = te.get("textRun") or {}
        if tr.get("content"):
            parts.append(tr["content"])
    return "".join(parts)


def collect_text_shapes(slide: dict) -> list[dict]:
    """Return text-bearing shapes with approximate vertical position."""
    out = []
    for el in slide.get("pageElements") or []:
        shape = el.get("shape")
        if not shape:
            continue
        text = extract_shape_text(shape)
        if not text or not text.strip():
            continue
        # skip pure whitespace / single control chars
        if not re.sub(r"\s+", "", text):
            continue
        transform = el.get("transform") or {}
        ty = float(transform.get("translateY") or 0)
        tx = float(transform.get("translateX") or 0)
        size = el.get("size") or {}
        h = float((size.get("height") or {}).get("magnitude") or 0)
        w = float((size.get("width") or {}).get("magnitude") or 0)
        out.append(
            {
                "object_id": el.get("objectId"),
                "text": text,
                "ty": ty,
                "tx": tx,
                "h": h,
                "w": w,
                "area": h * w,
                "len": len(text.strip()),
            }
        )
    # top-to-bottom then left-to-right
    out.sort(key=lambda s: (s["ty"], s["tx"]))
    return out


def replace_shape_text_requests(object_id: str, new_text: str) -> list[dict]:
    # Ensure trailing newline for paragraph shapes (Slides often expects it)
    if new_text and not new_text.endswith("\n"):
        new_text = new_text + "\n"
    return [
        {"deleteText": {"objectId": object_id, "textRange": {"type": "ALL"}}},
        {"insertText": {"objectId": object_id, "insertionIndex": 0, "text": new_text}},
    ]


def format_econ_body(route: dict) -> str:
    ue = route.get("unit_economics") or {}
    if route.get("status") != "supported" or not ue:
        return (
            f"{route.get('label')}. "
            "Route details and economics remain blank until local terminal, demand, and fare evidence is confirmed."
        )
    opex = ue.get("opex_lines") or {}
    margin_pct = round(float(ue.get("margin") or 0) * 100)
    rev = int(round(float(ue.get("revenue_per_boat_yr") or 0)))
    opex_tot = int(round(float(ue.get("total_run_cost_yr") or 0)))
    ebitda = int(round(float(ue.get("ebitda_per_boat_yr") or 0)))
    pax = int(round(float(ue.get("annual_one_way_pax_per_boat") or 0)))
    fare = ue.get("one_way_fare_usd")
    payback = ue.get("payback_years")
    nm = ue.get("distance_nm")
    vessel = ue.get("vessel") or "N30 Pioneer II"
    lines = [
        f"{route.get('label')}. {route.get('desc') or ''}".strip(),
        f"Vessel {vessel} · {nm} nm · one-way fare ${fare:.0f} · ~{pax:,} passengers per boat per year.",
        f"Revenue per boat ${rev:,} · run cost ${opex_tot:,} · EBITDA ${ebitda:,} · margin {margin_pct}% · payback {payback} years.",
        "Energy, crew, marina, maintenance, insurance, and charging-berth costs are included in the run cost.",
    ]
    return "\n".join(lines)


def format_tam_body(gen: dict, editplan_body: str | None) -> str:
    # Prefer editplan body (already plain English); append numeric rungs when available.
    rungs = (gen.get("tam") or {}).get("rungs") or []
    if not rungs:
        return editplan_body or (gen.get("tam") or {}).get("headline") or ""
    parts = [(gen.get("tam") or {}).get("headline") or ""]
    for r in rungs:
        label = r.get("label") or ""
        val = r.get("value_usd")
        note = r.get("note") or ""
        low = r.get("value_usd_low")
        high = r.get("value_usd_high")
        if val is None and low is None and high is None:
            parts.append(f"{label}: {note}".strip(": "))
        elif low is not None and high is not None:
            parts.append(
                f"{label}: ${int(low)/1e6:.1f}M–${int(high)/1e6:.1f}M. {note}".strip()
            )
        else:
            parts.append(f"{label}: ${float(val):,.0f}. {note}".strip())
    # Prefer editplan if present and longer (has full prose)
    if editplan_body and len(editplan_body) > 80:
        return editplan_body
    return "\n\n".join(p for p in parts if p)


def format_overview_body(ep: dict, gen: dict) -> str:
    st = ep.get("slide_text") or {}
    body = st.get("slide_03_body")
    if body:
        return body
    ct = (gen.get("country_total") or {}).get("values") or {}
    rev = ct.get("annual_revenue_usd")
    ves = ct.get("vessels_supported")
    n = ct.get("supported_route_count")
    return f"Supported routes: {n}. Supported annual route revenue: ${rev:,.0f}. Vessels supported: {ves}."


def batch_update(service, presentation_id: str, requests: list[dict], chunk: int = 40):
    for i in range(0, len(requests), chunk):
        part = requests[i : i + chunk]
        if not part:
            continue
        service.presentations().batchUpdate(
            presentationId=presentation_id, body={"requests": part}
        ).execute()


def apply_deck(service, deck_key: str) -> dict:
    deck_dir = DECKS_ROOT / deck_key
    cfg = load_json(deck_dir / "deck.config.json")
    ep = load_json(deck_dir / "deck.editplan.json")
    gen = load_json(deck_dir / "generated-deck-economics.json")
    content = load_json(deck_dir / "content-source.json")
    pid = DECK_IDS[deck_key]
    assert cfg.get("deck_id") == pid

    plan = RESTRUCTURE[deck_key]
    pres = service.presentations().get(presentationId=pid).execute()
    slides = pres.get("slides") or []
    before_count = len(slides)

    # 1) Delete abolished slides (high index first)
    del_reqs = []
    for idx in sorted(plan["delete_indices"], reverse=True):
        if 1 <= idx <= len(slides):
            del_reqs.append({"deleteObject": {"objectId": slides[idx - 1]["objectId"]}})
    if del_reqs:
        batch_update(service, pid, del_reqs)
        pres = service.presentations().get(presentationId=pid).execute()
        slides = pres.get("slides") or []

    after_delete = len(slides)
    if after_delete != plan["target_count"]:
        # Egypt already 12; Brazil/Mexico should match after deletes
        if deck_key != "indrive-egypt" or after_delete != 12:
            print(
                f"WARNING {deck_key}: slide count after delete {after_delete} "
                f"(target {plan['target_count']}, before {before_count})"
            )

    # 2) Build per-slide content from editplan + economics
    st = ep.get("slide_text") or {}
    slide_specs = content.get("slide_sources") or []
    # map by index
    by_index = {s.get("slide_index"): s for s in slide_specs}

    econ_routes = gen.get("economics_routes") or (
        [gen["economics_route"]] if gen.get("economics_route") else []
    )
    econ_i = 0

    text_reqs: list[dict] = []
    applied_text: list[dict] = []

    for i, slide in enumerate(slides, 1):
        shapes = collect_text_shapes(slide)
        if not shapes:
            continue
        title_key = f"slide_{i:02d}_title"
        body_key = f"slide_{i:02d}_body"
        title = st.get(title_key)
        body = st.get(body_key)

        # Purpose-aware enrichment
        purpose = (by_index.get(i) or {}).get("role") or ""
        if not purpose and i <= len(slide_specs):
            purpose = slide_specs[i - 1].get("role") or ""

        # Fallbacks from content-source titles
        if not title and by_index.get(i):
            title = by_index[i].get("title")

        if purpose in ("market_overview", "country_scope") or i == 3:
            body = format_overview_body(ep, gen)
            if not title:
                title = st.get("slide_03_title")
        if purpose == "one_route_economics" or (
            title and title.lower().startswith("route economics")
        ):
            if econ_i < len(econ_routes):
                er = econ_routes[econ_i]
                title = f"Route economics: {er.get('label')}"
                body = format_econ_body(er)
                econ_i += 1
        if purpose in ("country_prize",) or (title and "floor" in (title or "").lower()):
            body = format_tam_body(gen, st.get(body_key) or st.get("slide_08_body") or st.get("slide_07_body"))

        # Heuristic: largest top shape = title-ish, largest mid = body
        # Prefer shapes that look like titles (short, upper area)
        title_candidates = [s for s in shapes if s["len"] < 120 and s["ty"] < 2.0e6]
        body_candidates = [s for s in shapes if s["len"] >= 40 or s["area"] > 1.0e10]
        if not title_candidates:
            title_candidates = shapes[:1]
        if not body_candidates:
            body_candidates = shapes[1:2] if len(shapes) > 1 else []

        # Pick title shape: highest non-tiny text near top
        title_shape = sorted(title_candidates, key=lambda s: (s["ty"], -s["area"]))[0]
        # Body: largest area shape that is not title shape
        body_shape = None
        for s in sorted(body_candidates, key=lambda s: -s["area"]):
            if s["object_id"] != title_shape["object_id"]:
                body_shape = s
                break

        if title:
            # Keep partner-facing titles clean; avoid ALL-CAPS forced styling
            text_reqs.extend(replace_shape_text_requests(title_shape["object_id"], title))
            applied_text.append({"slide": i, "role": "title", "object_id": title_shape["object_id"], "text": title[:80]})
        if body and body_shape:
            text_reqs.extend(replace_shape_text_requests(body_shape["object_id"], body))
            applied_text.append({"slide": i, "role": "body", "object_id": body_shape["object_id"], "text": body[:80]})

        # Also try to clear obvious placeholder jargon in other short shapes
        for s in shapes:
            if s["object_id"] in {title_shape["object_id"], (body_shape or {}).get("object_id")}:
                continue
            raw = s["text"].strip()
            if any(tok in raw for tok in ("CITY ROUTE REVIEW", "ROUTE ECONOMICS ·", "pending", "HELD NULL", "captive capture")):
                # blank or soften secondary eyebrow if it still shows abolished structure
                if "CITY ROUTE REVIEW" in raw:
                    text_reqs.extend(replace_shape_text_requests(s["object_id"], "CITY REVIEW\n"))
                elif "ROUTE ECONOMICS" in raw:
                    text_reqs.extend(replace_shape_text_requests(s["object_id"], "ROUTE ECONOMICS\n"))

    if text_reqs:
        batch_update(service, pid, text_reqs)

    # 3) Readback pull
    pres2 = service.presentations().get(presentationId=pid).execute()
    slides2 = pres2.get("slides") or []
    manifest_slides = []
    for i, slide in enumerate(slides2, 1):
        shapes = collect_text_shapes(slide)
        title_guess = shapes[0]["text"].strip().split("\n")[0] if shapes else None
        manifest_slides.append(
            {
                "index": i,
                "slide_object_id": slide.get("objectId"),
                "layout_object_id": (slide.get("slideProperties") or {}).get("layoutObjectId"),
                "title": title_guess,
                "purpose": (by_index.get(i) or {}).get("role") or "live_readback",
                "allowed_edit_types": ["replace_text", "replace_linked_image"],
                "locked": False,
                "notes": "Live inventory read back after spine apply 2026-07-15",
            }
        )

    manifest = {
        "deck_key": deck_key,
        "presentation_id": pid,
        "source": "live_google_slides_full_after_spine_apply_2026-07-15",
        "slide_count": len(manifest_slides),
        "spine": "cover, why-partner, market-overview, one slide per city, unit-economics (1+), TAM, integration, rollout, ask, close",
        "object_inventory_status": "full_inventory_pulled",
        "slides": manifest_slides,
        "pull_command": f"apply_country_decks_live_spine_2026_07_15.py --deck {deck_key}",
        "qa_notes": [
            "Restructured from abolished alternating city/econ spine",
            "Atlas screenshot slots intentionally unpopulated",
            f"before_count={before_count} after_delete={after_delete} final={len(slides2)}",
        ],
    }
    write_json(deck_dir / "slide-manifest.json", manifest)

    ep["apply_status"] = "applied_and_live_inventory_read_back"
    ep["applied_at"] = NOW
    ep["presentation_id"] = pid
    write_json(deck_dir / "deck.editplan.json", ep)

    receipt = {
        "deck_key": deck_key,
        "presentation_id": pid,
        "live_url": f"https://docs.google.com/presentation/d/{pid}/edit",
        "status": "applied",
        "generated_at": NOW,
        "before_slide_count": before_count,
        "after_slide_count": len(slides2),
        "target_slide_count": plan["target_count"],
        "deleted_indices": plan["delete_indices"],
        "text_ops_applied": len(applied_text),
        "applied_text_sample": applied_text[:20],
        "economics_routes": [
            {
                "route_id": r.get("route_id"),
                "status": r.get("status"),
                "payback_years": (r.get("unit_economics") or {}).get("payback_years"),
                "margin": (r.get("unit_economics") or {}).get("margin"),
            }
            for r in econ_routes
        ],
        "country_total": gen.get("country_total"),
        "atlas_screenshots": "human_insertion_only_unpopulated",
        "pptx_roundtrip": False,
        "wholesale_replace": False,
        "unresolved_gaps": [
            g
            for g in [
                "Atlas route screenshot slots empty by policy",
                None
                if len(slides2) == plan["target_count"]
                else f"slide_count_mismatch final={len(slides2)} target={plan['target_count']}",
            ]
            if g
        ],
        "no_op_replay": "re-run this script; deletes are idempotent only when already at target structure — prefer text-only second pass",
    }
    out_dir = deck_dir / "qa-receipts"
    write_json(out_dir / f"LIVE-SPINE-APPLY-RECEIPT-2026-07-15.json", receipt)
    write_json(out_dir / "latest-live-spine-apply.json", receipt)
    print(json.dumps({"deck": deck_key, "final_slides": len(slides2), "text_ops": len(applied_text)}, indent=2))
    return receipt


def main() -> int:
    service = build("slides", "v1", credentials=get_creds(), cache_discovery=False)
    summary = {"generated_at": NOW, "decks": {}}
    for deck in ("didi-brazil", "didi-mexico", "indrive-brazil", "indrive-egypt"):
        print(f"\n===== APPLY {deck} =====")
        try:
            summary["decks"][deck] = apply_deck(service, deck)
        except Exception as e:
            summary["decks"][deck] = {"status": "failed", "error": str(e)}
            print("FAILED", deck, e)
            raise
    out = (
        ROOT
        / "handoff/partner-map-model/indrive-scope-expansion-2026-07-13"
        / "COUNTRY-DECK-LIVE-SPINE-APPLY-RECEIPT-2026-07-15.json"
    )
    write_json(out, summary)
    print("\nWrote", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
