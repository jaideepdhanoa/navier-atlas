#!/usr/bin/env python3
"""Re-apply DiDi Brazil live deck to post-#279 mid economics (Slides API only).

Implements handoff/finance/GROK-SPEC-didi-brazil-reapply-2026-07-15.md.
No PPTX, no full-replace, atlas slots untouched.
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
DECK_DIR = ROOT / "deck-studio" / "decks" / "didi-brazil"
PID = "1OixKrHjQbWu0Plkvj-57SQyTFxPL5Ii8l3K6Q9umJOk"
TOKEN_FILE = Path.home() / ".config/google-drive-mcp/tokens.json"
CLIENT_FILE = Path.home() / ".config/google-drive-mcp/gcp-oauth.keys.json"
NOW = datetime.now(timezone.utc).isoformat()

# Live object IDs verified 2026-07-16 (re-read before mutate; still present).
DELETE_IDS = [
    # Slide 5 Angra — orphan economics debris
    "didibrazil_etx1",
    "didibrazil_ebg1",
    "g3eec5122801_0_395",
    "g3eec5122801_0_397",
]

HOLD_TEXT = (
    "Route-level passenger demand and fares are under local review; "
    "economics remain blank until confirmed."
)


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


def replace_shape_text_requests(object_id: str, new_text: str) -> list[dict]:
    if new_text and not new_text.endswith("\n"):
        new_text = new_text + "\n"
    return [
        {"deleteText": {"objectId": object_id, "textRange": {"type": "ALL"}}},
        {"insertText": {"objectId": object_id, "insertionIndex": 0, "text": new_text}},
    ]


def batch_update(service, requests: list[dict], chunk: int = 30):
    for i in range(0, len(requests), chunk):
        part = requests[i : i + chunk]
        if not part:
            continue
        service.presentations().batchUpdate(
            presentationId=PID, body={"requests": part}
        ).execute()


def format_money_m(usd: float) -> str:
    return f"${usd / 1e6:.1f}M"


def rio_route_list(routes: list[dict]) -> str:
    # Canonical amber ▸ route list; distances/descs from generated-deck-economics.
    bullets = []
    for r in routes:
        ue = r.get("unit_economics") or {}
        nm = ue.get("distance_nm")
        label = r.get("label") or ""
        desc = (r.get("desc") or "").rstrip(".")
        # shorten desc for list
        short = {
            "rn-1886629dbf0c": "cross-bay commuter connection to Niterói",
            "rn-80f0d0ebe0bd": "fast crossing to the Charitas waterfront",
            "rn-369ef0eb69d9": "city-to-island link to Ilha do Governador",
            "rn-00bb6ded4be5": "longer bay crossing to car-free Paquetá Island",
        }.get(r.get("route_id"), desc)
        bullets.append(f"▸  {label}\n      ~{nm} nm · {short}")
    return "\n".join(bullets)


def format_unit_econ_body(route: dict) -> str:
    ue = route.get("unit_economics") or {}
    opex = ue.get("opex_lines") or {}
    margin_pct = round(float(ue.get("margin") or 0) * 100)
    rev = int(round(float(ue.get("revenue_per_boat_yr") or 0)))
    opex_tot = int(round(float(ue.get("total_run_cost_yr") or 0)))
    ebitda = int(round(float(ue.get("ebitda_per_boat_yr") or 0)))
    pax = int(round(float(ue.get("annual_one_way_pax_per_boat") or 0)))
    fare = float(ue.get("one_way_fare_usd") or 0)
    payback = ue.get("payback_years")
    nm = ue.get("distance_nm")
    vessel = ue.get("vessel") or "N30 Pioneer II"
    energy = int(round(float(opex.get("energy_usd_yr") or 0)))
    crew = int(round(float(opex.get("crew_usd_yr") or 0)))
    marina = int(round(float(opex.get("marina_overhead_usd_yr") or 0)))
    maint = int(round(float(opex.get("maintenance_usd_yr") or 0)))
    ins = int(round(float(opex.get("insurance_usd_yr") or 0)))
    charge = int(round(float(opex.get("charging_berth_usd_yr") or 0)))
    return "\n".join(
        [
            f"{route.get('label')}. {route.get('desc') or ''}".strip(),
            f"Vessel {vessel} · {nm} nm · one-way fare ${fare:.0f} · ~{pax:,} passengers per boat per year.",
            f"Revenue per boat ${rev:,} · run cost ${opex_tot:,} · EBITDA ${ebitda:,} · margin {margin_pct}% · payback {payback} years.",
            f"Energy ${energy:,} · Crew ${crew:,} · Marina+overhead ${marina:,} · Maintenance ${maint:,} · Insurance ${ins:,} · Charging berth ${charge:,} → total run cost ${opex_tot:,}.",
        ]
    )


def notes_object_id(notes_page: dict) -> str | None:
    """Find the speaker-notes body shape object id."""
    for el in notes_page.get("pageElements") or []:
        shape = el.get("shape") or {}
        # speaker notes body usually has substantial text or is the notes shape type
        text = extract_shape_text(shape)
        # Prefer the largest text-bearing shape that is not empty placeholder only
        if text and len(text.strip()) > 5:
            return el.get("objectId")
    # fallback: any text shape
    for el in notes_page.get("pageElements") or []:
        if el.get("shape") and el.get("objectId"):
            # skip shapes with no text capability issues
            st = (el.get("shape") or {}).get("shapeType")
            if st in (None, "TEXT_BOX", "RECTANGLE"):
                # only if it has text property
                if "text" in (el.get("shape") or {}):
                    return el.get("objectId")
    return None


def clean_notes(text: str, slide_index_1based: int) -> str:
    """Replace Grab/SEA/Singapore/Phuket/Bali leftover notes with Brazil-local notes."""
    bad = re.search(
        r"Grab|Singapore|Phuket|Bali|SEA water|grab-growth|M_today|SOM_full_network",
        text,
        re.I,
    )
    if not bad:
        return text  # keep clean notes
    replacements = {
        3: (
            "Brazil market overview (mid basis, post-PR #279): 3 coastal cities · "
            "4 sourced Rio cross-bay routes · $36.4M supported annual route revenue · "
            "113 vessels at scale. Addressable water-crossing pool $367.5M."
        ),
        4: (
            "Rio de Janeiro city deep-dive: four marquee Guanabara Bay corridors "
            "(Arariboia 2.7nm, Charitas 4.4nm, Cocotá 6.0nm, Paquetá 9.2nm) from "
            "generated-deck-economics.json. Economics on the unit-econ slide."
        ),
        5: (
            "Angra dos Reis / Ilha Grande: HELD-NULL. Crossings mapped; route-level "
            "passenger demand and fares under local review. No economics shown."
        ),
        6: (
            "Florianópolis: HELD-NULL. Island–mainland crossings mapped; demand and "
            "fares under review. No Rio corridors; no economics shown."
        ),
        7: (
            "Unit economics (mid basis): Praça XV → Arariboia. Fare $28 · ~11,757 pax/boat/yr · "
            "Revenue $329,190 · run cost $79,257 · EBITDA $249,933 · margin 76% · payback 2.4 years."
        ),
        8: (
            "Floor not ceiling (mid): SOM supported $36.4M (113 vessels, 4 routes) → "
            "SAM addressable water-crossing spend $367.5M → Rung 3 held null."
        ),
    }
    return replacements.get(slide_index_1based, "Brazil mobility review — DiDi × Navier.")


def main() -> int:
    gen = load_json(DECK_DIR / "generated-deck-economics.json")
    ep = load_json(DECK_DIR / "deck.editplan.json")
    assert ep.get("presentation_id") == PID

    routes = gen.get("economics_routes") or []
    arariboia = gen.get("economics_route") or routes[0]
    ct = (gen.get("country_total") or {}).get("values") or {}
    rev = float(ct.get("annual_revenue_usd") or 0)
    rev_m = format_money_m(rev)
    pool = float(((gen.get("tam") or {}).get("rungs") or [{}])[1].get("value_usd") or 0)
    pool_m = format_money_m(pool)

    overview_body = (ep.get("slide_text") or {}).get("slide_03_body") or ""
    # ensure body carries $36.4M
    if "$36.4M" not in overview_body and rev:
        overview_body = re.sub(r"\$\d+\.\d+M supported annual", f"{rev_m} supported annual", overview_body)

    svc = build("slides", "v1", credentials=get_creds(), cache_discovery=False)
    pres = svc.presentations().get(presentationId=PID).execute()
    slides = pres.get("slides") or []
    assert len(slides) == 12, f"expected 12 slides, got {len(slides)}"

    # Inventory live object ids for safety
    live_ids = set()
    for slide in slides:
        for el in slide.get("pageElements") or []:
            if el.get("objectId"):
                live_ids.add(el["objectId"])

    reqs: list[dict] = []
    deleted = []
    for oid in DELETE_IDS:
        if oid in live_ids:
            reqs.append({"deleteObject": {"objectId": oid}})
            deleted.append(oid)
        else:
            print(f"skip delete (not live): {oid}")

    # --- Slide 3 (index 2): market overview KPIs + body ---
    reqs += replace_shape_text_requests("g3eec5122801_0_10", rev_m)
    reqs += replace_shape_text_requests("g3eec5122801_0_20", overview_body)
    # subtitle already fine; KPI label stays

    # --- Slide 4 (index 3): Rio four marquee corridors ---
    reqs += replace_shape_text_requests("g3eec5122801_0_114", rio_route_list(routes))
    reqs += replace_shape_text_requests(
        "g3eec5122801_0_111",
        "Four sourced cross-bay corridors from Praça XV across Guanabara Bay.",
    )

    # --- Slide 5 Angra: already deleting debris; ensure hold is clear in body ---
    # body _394 already holds narrative; no econ

    # --- Slide 6 Florianópolis: remove Rio route debris ---
    reqs += replace_shape_text_requests(
        "g3eec5122801_0_209",
        f"▸  Crossings mapped\n      Demand under review\n▸  Status\n      {HOLD_TEXT}",
    )
    reqs += replace_shape_text_requests(
        "g3eec5122801_0_206",
        "Island–mainland water crossings mapped; economics held until demand and fares are confirmed.",
    )

    # --- Slide 7 unit econ Arariboia mid ---
    reqs += replace_shape_text_requests("g3eec5122801_0_300", format_unit_econ_body(arariboia))
    reqs += replace_shape_text_requests(
        "g3eec5122801_0_301",
        "Rio's flagship cross-bay commuter connection between central Rio and Niterói.",
    )
    reqs += replace_shape_text_requests(
        "g3eec5122801_0_304",
        "▸  Praça XV → Arariboia\n"
        "      Cross-bay commuter connection · 2.7 nm\n"
        "▸  Serves\n"
        "      Central Rio and Niterói\n"
        "▸  Economics\n"
        "      Mid basis on this slide",
    )

    # --- Slide 8 floor not ceiling ---
    reqs += replace_shape_text_requests("g3eec5122801_0_570", rev_m)
    tam_body = (
        f"{(gen.get('tam') or {}).get('headline') or 'The supported routes are a floor, not a ceiling'}\n\n"
        f"Supported annual route revenue today: {rev_m} — four sourced Rio cross-bay routes, "
        f"{int(ct.get('vessels_supported') or 113)} vessels at scale.\n"
        f"Addressable Brazil water-crossing spend: {pool_m} — annual passenger spend across the "
        f"bay and coastal crossings the network can compete for."
    )
    reqs += replace_shape_text_requests("g3eec5122801_0_589", tam_body)

    # --- Speaker notes scrub (slides 3–8 = indices 2–7) ---
    notes_scrubbed = []
    for i, slide in enumerate(slides):
        slide_n = i + 1
        if slide_n < 3 or slide_n > 8:
            continue
        notes_page = (slide.get("slideProperties") or {}).get("notesPage") or {}
        # find text shape with bad content
        for el in notes_page.get("pageElements") or []:
            shape = el.get("shape") or {}
            text = extract_shape_text(shape)
            if not text or not text.strip():
                continue
            cleaned = clean_notes(text, slide_n)
            if cleaned != text:
                oid = el.get("objectId")
                if oid:
                    reqs += replace_shape_text_requests(oid, cleaned)
                    notes_scrubbed.append({"slide": slide_n, "object_id": oid})

    print(f"requests: {len(reqs)} | deletes: {deleted}")
    batch_update(svc, reqs)

    # --- Read-back verification ---
    pres2 = svc.presentations().get(presentationId=PID).execute()
    slides2 = pres2.get("slides") or []
    readback = {"slides": []}
    bad_tokens = []
    for i, slide in enumerate(slides2):
        texts = []
        for el in slide.get("pageElements") or []:
            shape = el.get("shape")
            if not shape:
                continue
            t = extract_shape_text(shape).strip()
            if t:
                texts.append({"id": el.get("objectId"), "text": t[:300]})
                for tok in ("Grab", "Singapore", "Phuket", "Bali", "$23.4M", "$18 ", "8.91", "$146,448"):
                    if tok in t and "Private" not in tok:
                        # allow $18 only if not fare context - flag all for review
                        bad_tokens.append({"slide": i + 1, "token": tok, "id": el.get("objectId"), "snippet": t[:120]})
        # notes
        notes_page = (slide.get("slideProperties") or {}).get("notesPage") or {}
        note_parts = []
        for el in notes_page.get("pageElements") or []:
            shape = el.get("shape") or {}
            t = extract_shape_text(shape)
            if t.strip():
                note_parts.append(t.strip())
                for tok in ("Grab", "Singapore", "Phuket", "Bali", "SEA water", "grab-growth"):
                    if tok in t:
                        bad_tokens.append({"slide": i + 1, "token": tok, "where": "notes", "snippet": t[:120]})
        readback["slides"].append(
            {
                "index": i + 1,
                "object_id": slide.get("objectId"),
                "text_count": len(texts),
                "notes": " | ".join(note_parts)[:400],
                "key_texts": [x for x in texts if any(k in x["text"] for k in ("$36", "$28", "$329", "Arariboia", "HELD", "under review", "Charitas", "Paquet", "floor", "23.4", "18"))],
            }
        )

    # residual deletes check
    remaining_delete_targets = []
    for slide in slides2:
        for el in slide.get("pageElements") or []:
            if el.get("objectId") in DELETE_IDS:
                remaining_delete_targets.append(el.get("objectId"))

    receipt = {
        "deck_key": "didi-brazil",
        "presentation_id": PID,
        "url": f"https://docs.google.com/presentation/d/{PID}/edit",
        "applied_at": NOW,
        "slide_count": len(slides2),
        "source": {
            "generated_deck_economics": "deck-studio/decks/didi-brazil/generated-deck-economics.json",
            "editplan": "deck-studio/decks/didi-brazil/deck.editplan.json",
            "spec": "handoff/finance/GROK-SPEC-didi-brazil-reapply-2026-07-15.md",
            "mid_basis": {
                "fare": 28,
                "rev_boat": 329190,
                "margin": 0.759,
                "payback": 2.4,
                "country_rev": rev,
                "pool": pool,
                "vessels": ct.get("vessels_supported"),
            },
        },
        "deleted_object_ids": deleted,
        "remaining_delete_targets": remaining_delete_targets,
        "notes_scrubbed": notes_scrubbed,
        "request_count": len(reqs),
        "bad_token_hits": bad_tokens,
        "readback_summary": readback,
        "gates": {
            "partner_copy_lint": "run separately",
            "atlas_slots": "human_insertion_only_untouched",
        },
    }

    out = DECK_DIR / "qa-receipts" / "LIVE-REAPPLY-MID-POST279-2026-07-15.json"
    write_json(out, receipt)

    # Update editplan status
    ep["apply_status"] = "reapplied_mid_post_pr279"
    ep["reapplied_at"] = NOW
    ep["reapply_note"] = (
        "Live deck re-applied 2026-07-15 post-PR #279: slides 3/7/8 mid economics; "
        "Rio 4-corridor list; Angra/Floripa held-null debris removed; Grab notes scrubbed."
    )
    write_json(DECK_DIR / "deck.editplan.json", ep)

    print(json.dumps({
        "ok": len(remaining_delete_targets) == 0 and not any(
            b.get("token") in ("Grab", "Singapore", "Phuket", "Bali", "SEA water", "grab-growth", "$23.4M")
            for b in bad_tokens
        ),
        "slide_count": len(slides2),
        "deleted": deleted,
        "remaining_deletes": remaining_delete_targets,
        "bad_token_count": len(bad_tokens),
        "bad_tokens_sample": bad_tokens[:15],
        "receipt": str(out.relative_to(ROOT)),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
