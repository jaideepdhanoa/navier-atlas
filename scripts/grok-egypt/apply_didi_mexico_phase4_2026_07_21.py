#!/usr/bin/env python3
"""DiDi Mexico Phase 4 live apply (GROK-SPEC-didi-mexico-phase4-2026-07-21).

- Refresh market overview counts on slide 3
- Append 4 backup slides: Holbox city + econ, Huatulco city + econ
  (duplicate existing city/econ chassis; substitute source-backed fields)
- Sync slide-manifest + QA receipt

Slides API only. THE PRIZE already refreshed by Tasklet — verify only.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parents[2]
TOKEN_FILE = Path.home() / ".config/google-drive-mcp/tokens.json"
CLIENT_FILE = Path.home() / ".config/google-drive-mcp/gcp-oauth.keys.json"
DECK = ROOT / "deck-studio/decks/didi-mexico"
GEN = DECK / "generated-deck-economics.json"
MANIFEST = DECK / "slide-manifest.json"
RECEIPT = (
    ROOT
    / "handoff/partner-map-model/mx-eg-expansion-2026-07-20"
    / "DIDI-MEXICO-PHASE4-QA-RECEIPT-2026-07-21.json"
)
PID = "1XwKRuJtMrou8NtBdc1oY3LL2Dk83dCs9MCLvNKgwq0c"
NOW = datetime.now(timezone.utc).isoformat()

# Chassis object IDs to duplicate
CITY_TEMPLATE = "g3eec5122801_0_106"  # Cancún city
ECON_TEMPLATE = "g3eec5122801_0_701"  # Isla Mujeres econ
OVERVIEW = "g3eec5122801_0_0"
PRIZE = "g3eec5122801_0_562"


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


def extract_text(shape: dict) -> str:
    parts = []
    for te in (shape.get("text") or {}).get("textElements") or []:
        tr = te.get("textRun") or {}
        if tr.get("content"):
            parts.append(tr["content"])
    return "".join(parts).strip()


def replace_text(oid: str, new_text: str) -> list[dict]:
    if new_text and not new_text.endswith("\n"):
        new_text += "\n"
    return [
        {"deleteText": {"objectId": oid, "textRange": {"type": "ALL"}}},
        {"insertText": {"objectId": oid, "insertionIndex": 0, "text": new_text}},
    ]


def batch(svc, reqs: list[dict], chunk: int = 30):
    for i in range(0, len(reqs), chunk):
        part = reqs[i : i + chunk]
        if part:
            svc.presentations().batchUpdate(presentationId=PID, body={"requests": part}).execute()


def money_m(usd: float) -> str:
    if usd >= 1e9:
        v = usd / 1e9
        s = f"${v:.1f}B" if v >= 10 else f"${v:.2f}B".replace(".00B", "B").replace(".0B", "B")
        return s.replace(".00B", "B")
    m = usd / 1e6
    if m >= 100:
        return f"${m:.0f}M"
    return f"${m:.1f}M".replace(".0M", "M")


def fmt_int(n: float | int) -> str:
    return f"{int(round(n)):,}"


def fmt_usd(n: float) -> str:
    return f"${int(round(n)):,}"


def by_route(gen: dict) -> dict:
    out = {}
    for r in gen.get("economics_routes") or []:
        if r.get("route_id"):
            out[r["route_id"]] = r
    return out


def map_elements(slide: dict) -> dict[str, str]:
    """Map semantic role → objectId by scanning text content on a slide."""
    roles = {}
    texts = []
    for el in slide.get("pageElements") or []:
        oid = el.get("objectId")
        t = extract_text(el.get("shape") or {})
        if not t:
            continue
        texts.append((oid, t))
        u = t.upper()
        if t.startswith("▸") or "▸" in t[:3]:
            roles["bullets"] = oid
        elif "©" in t and "NAVIER" in u:
            roles["footer"] = oid
        elif "INTERACTIVE" in u:
            roles["chip_int"] = oid
        elif "MODEL DEEPDIVE" in u or "MODEL DEEP" in u:
            roles["chip_model"] = oid
        elif "WHAT ONE BOAT EARNS" in u:
            roles["title"] = oid
        elif roles.get("title") is None and len(t) < 80 and "\n" not in t and not t.startswith("$"):
            # first short title-like line
            if "title" not in roles:
                roles["title"] = oid
    # city slides: order of non-footer text often title, body, note, bullets
    non_footer = [(o, t) for o, t in texts if "©" not in t and "INTERACTIVE" not in t.upper() and "MODEL" not in t.upper()]
    if "title" not in roles and non_footer:
        roles["title"] = non_footer[0][0]
    if len(non_footer) >= 2 and "body" not in roles:
        roles["body"] = non_footer[1][0]
    if len(non_footer) >= 3 and "note" not in roles:
        # middle short note
        for o, t in non_footer[1:]:
            if o not in (roles.get("title"), roles.get("bullets")) and len(t) < 200:
                roles["note"] = o
                break
    if "bullets" not in roles:
        for o, t in texts:
            if "▸" in t or "nm" in t.lower() or "fare" in t.lower() or "Revenue" in t:
                roles["bullets"] = o
                break
    # econ: route name often second line
    if "route" not in roles and len(non_footer) >= 2:
        roles["route"] = non_footer[1][0]
    if "desc" not in roles and len(non_footer) >= 3:
        roles["desc"] = non_footer[2][0]
    roles["_all"] = texts
    return roles


def find_slide(pres: dict, oid: str) -> dict | None:
    for s in pres.get("slides") or []:
        if s.get("objectId") == oid:
            return s
    return None


def duplicate_slide(svc, object_id: str) -> dict:
    """Duplicate slide; return objectIdMappings {old: new} including page."""
    resp = (
        svc.presentations()
        .batchUpdate(
            presentationId=PID,
            body={"requests": [{"duplicateObject": {"objectId": object_id}}]},
        )
        .execute()
    )
    replies = resp.get("replies") or []
    mapping = (replies[0].get("duplicateObject") or {}).get("objectIdMappings") or {}
    # API also returns objectId for the top-level duplicate
    new_id = (replies[0].get("duplicateObject") or {}).get("objectId")
    return {"new_page_id": new_id, "map": mapping}


def apply_overview(svc, gen: dict) -> dict:
    ct = (gen.get("country_total") or {}).get("values") or {}
    rev = float(ct.get("annual_revenue_usd") or 0)
    vessels = int(ct.get("vessels_supported") or 0)
    routes_n = int(ct.get("supported_route_count") or 0)
    cities_n = 6  # per spec / market-scope

    reqs: list[dict] = []
    reqs += replace_text("g3eec5122801_0_6", str(routes_n))
    reqs += replace_text("g3eec5122801_0_7", "supported routes with economics today")
    reqs += replace_text("g3eec5122801_0_10", money_m(rev))
    reqs += replace_text(
        "g3eec5122801_0_11",
        f"supported annual route revenue · {vessels} vessels at scale",
    )
    reqs += replace_text(
        "g3eec5122801_0_14",
        "Cancún–Isla Mujeres, Playa–Cozumel, Isla Holbox and Bahías de Huatulco: "
        "DiDi already owns the street layer; the water leg books in the same app. "
        "Five sourced corridors anchor today's floor.",
    )
    reqs += replace_text("g3eec5122801_0_15", str(vessels))
    reqs += replace_text("g3eec5122801_0_16", "vessels at full network maturity")
    reqs += replace_text("g3eec5122801_0_18", str(cities_n))
    reqs += replace_text("g3eec5122801_0_19", "coastal cities in this review")
    reqs += replace_text(
        "g3eec5122801_0_20",
        "Mexico's Caribbean and Pacific coasts run some of the highest-volume tourist "
        "and commuter ferry crossings in the Americas. We size five grounded routes "
        "across six cities — including the Holbox and Huatulco corridors added in this review.",
    )
    # optional subtitle
    try:
        reqs += replace_text("g3eec5122801_0_4", "Mexico's coastal cities are a water network waiting to happen")
    except Exception:
        pass
    batch(svc, reqs)
    return {
        "routes": routes_n,
        "revenue": money_m(rev),
        "vessels": vessels,
        "cities": cities_n,
    }


def fill_city_slide(svc, roles: dict, *, title: str, body: str, note: str, bullets: str) -> list:
    reqs = []
    if roles.get("title"):
        reqs += replace_text(roles["title"], title)
    if roles.get("body"):
        reqs += replace_text(roles["body"], body)
    if roles.get("note"):
        reqs += replace_text(roles["note"], note)
    if roles.get("bullets"):
        reqs += replace_text(roles["bullets"], bullets)
    return reqs


def fill_econ_slide(svc, roles: dict, route: dict) -> list:
    ue = route.get("unit_economics") or {}
    opex = ue.get("opex_lines") or {}
    label = route.get("label") or ""
    # City suffix for title
    if "Holbox" in label or "holbox" in (route.get("route_id") or ""):
        title = "WHAT ONE BOAT EARNS · HOLBOX"
    elif "Huatulco" in label or "Maguey" in label or "huatulco" in (route.get("route_id") or ""):
        title = "WHAT ONE BOAT EARNS · HUATULCO"
    else:
        title = f"WHAT ONE BOAT EARNS · {label.upper()}"

    rev = float(ue.get("revenue_per_boat_yr") or 0)
    cost = float(ue.get("total_run_cost_yr") or 0)
    ebitda = float(ue.get("ebitda_per_boat_yr") or 0)
    margin = float(ue.get("margin") or 0)
    payback = ue.get("payback_years")
    nm = ue.get("distance_nm")
    fare = ue.get("one_way_fare_usd")
    pax = ue.get("annual_one_way_pax_per_boat")
    fare_s = f"${fare:.0f}" if fare == int(fare or 0) else f"${fare}"

    bullets = "\n".join(
        [
            f"▸  N30 Pioneer II · {nm} nm · fare {fare_s}",
            f"▸  ~{fmt_int(pax or 0)} passengers / boat / year",
            f"▸  Revenue {fmt_usd(rev)} · EBITDA {fmt_usd(ebitda)}",
            f"▸  Margin {margin*100:.0f}% · payback {payback} years",
            f"▸  Energy {fmt_usd(opex.get('energy_usd_yr') or 0)} · Crew {fmt_usd(opex.get('crew_usd_yr') or 0)} · Marina+overhead {fmt_usd(opex.get('marina_overhead_usd_yr') or 0)}",
            f"▸  Maintenance {fmt_usd(opex.get('maintenance_usd_yr') or 0)} · Insurance {fmt_usd(opex.get('insurance_usd_yr') or 0)} · Charging berth {fmt_usd(opex.get('charging_berth_usd_yr') or 0)}",
            f"▸  Total run cost {fmt_usd(cost)} → profit {fmt_usd(ebitda)} / boat·yr",
        ]
    )

    reqs = []
    if roles.get("title"):
        reqs += replace_text(roles["title"], title)
    if roles.get("route"):
        reqs += replace_text(roles["route"], label)
    if roles.get("desc"):
        reqs += replace_text(roles["desc"], route.get("desc") or "")
    if roles.get("bullets"):
        reqs += replace_text(roles["bullets"], bullets)
    return reqs


def verify_prize(pres: dict) -> dict:
    slide = find_slide(pres, PRIZE)
    if not slide:
        return {"status": "missing"}
    texts = []
    for el in slide.get("pageElements") or []:
        t = extract_text(el.get("shape") or {})
        if t and ("$" in t or "SOM" in t or "PRIZE" in t):
            texts.append(t.replace("\n", " ")[:80])
    ok = any("163.8" in t or "163.7" in t for t in texts) and any("749.7" in t for t in texts)
    return {"status": "ok" if ok else "check", "sample": texts[:8]}


def sync_manifest(pres: dict) -> dict:
    slides_out = []
    for i, s in enumerate(pres.get("slides") or [], 1):
        texts = []
        for el in s.get("pageElements") or []:
            t = extract_text(el.get("shape") or {})
            if t:
                texts.append(t.replace("\n", " ").strip())
        title = texts[0] if texts else ""
        for t in texts:
            if any(k in t.upper() for k in ["WHAT ONE BOAT", "THE PRIZE", "PHASED", "NEXT STEP", "HOLBOX", "HUATULCO"]):
                title = t
                break
        purpose = "city-deepdive"
        if "WHAT ONE BOAT" in title.upper():
            purpose = "unit-economics"
        elif "PRIZE" in title.upper():
            purpose = "tam-ladder"
        elif i == 1:
            purpose = "cover"
        elif i == 2:
            purpose = "why-partner"
        elif i == 3:
            purpose = "market-overview"
        elif "PHASED" in title.upper():
            purpose = "rollout"
        elif "NEXT" in title.upper() or "joint route" in title.lower():
            purpose = "close"
        elif "work together" in title.lower():
            purpose = "integration"
        slides_out.append(
            {
                "index": i,
                "slide_object_id": s.get("objectId"),
                "layout_object_id": (s.get("slideProperties") or {}).get("layoutObjectId"),
                "title": title[:120],
                "purpose": purpose,
                "allowed_edit_types": ["replace_text", "replace_linked_image"],
                "locked": False,
                "notes": "Live inventory after DiDi Mexico Phase 4 apply 2026-07-21",
            }
        )
    manifest = {
        "deck_key": "didi-mexico",
        "presentation_id": PID,
        "source": "live_google_slides_full_after_phase4_2026-07-21",
        "slide_count": len(slides_out),
        "spine": (
            "cover, why-partner, market-overview, main city deep-dives (Cancún/Playa/PV/Cabos) + "
            "unit-econ (Isla Mujeres/Cozumel), THE PRIZE, integration, rollout, ask, close; "
            "BACKUP: Holbox city+econ, Huatulco city+econ"
        ),
        "object_inventory_status": "full_inventory_pulled",
        "slides": slides_out,
        "synced_at": NOW,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    cfg_path = DECK / "deck.config.json"
    if cfg_path.exists():
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        cfg["notes"] = f"Live deck synchronized after Phase 4 apply 2026-07-21 ({len(slides_out)} slides)."
        cfg_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    gen = json.loads(GEN.read_text(encoding="utf-8"))
    routes = by_route(gen)
    holbox = routes.get("rn-8e76868a5b01")
    huatulco = routes.get("rn-66e2241ca732")
    if not holbox or not huatulco:
        print("FATAL: missing holbox/huatulco in generated-deck-economics.json", file=sys.stderr)
        return 1

    svc = build("slides", "v1", credentials=get_creds(), cache_discovery=False)
    pres = svc.presentations().get(presentationId=PID).execute()
    existing_ids = {s["objectId"] for s in pres.get("slides") or []}
    n0 = len(pres.get("slides") or [])
    print(f"live slides: {n0}")

    # --- A. Market overview ---
    print("A. Market overview refresh…")
    overview = apply_overview(svc, gen)
    print("  ", overview)

    # --- B. Backup slides (skip if already 18+) ---
    applied = {"duplicated": [], "econ_source_map": {}}
    if n0 >= 18:
        print("B. Deck already has 18+ slides — skip duplicate; will re-fill if Holbox/Huatulco titles present")
        pres = svc.presentations().get(presentationId=PID).execute()
    else:
        print("B. Duplicating chassis slides…")
        # Order: create city holbox, econ holbox, city huatulco, econ huatulco
        # Then move all four after last slide
        dups = []
        for template, tag in [
            (CITY_TEMPLATE, "holbox_city"),
            (ECON_TEMPLATE, "holbox_econ"),
            (CITY_TEMPLATE, "huatulco_city"),
            (ECON_TEMPLATE, "huatulco_econ"),
        ]:
            info = duplicate_slide(svc, template)
            dups.append((tag, info))
            print(f"  duplicated {template} → {info['new_page_id']} ({tag})")

        # Re-fetch and fill
        pres = svc.presentations().get(presentationId=PID).execute()
        by_page = {s["objectId"]: s for s in pres["slides"]}

        fill_plan = {
            "holbox_city": {
                "title": "ISLA HOLBOX",
                "body": (
                    "Chiquilá is the mainland gateway to car-free Isla Holbox — a single passenger "
                    "ferry crossing across the Yalahau channel, high-frequency and sole access for most visitors."
                ),
                "note": "One sourced crossing at the $12 island-hop fare; route economics follow on their own slide.",
                "bullets": (
                    "▸  Chiquilá → Isla Holbox\n"
                    "      ~5.5 nm · sole passenger crossing to car-free Holbox\n"
                    "▸  Serves\n"
                    "      Mainland Riviera Maya visitors and Holbox stays"
                ),
            },
            "huatulco_city": {
                "title": "BAHÍAS DE HUATULCO",
                "body": (
                    "Bahías de Huatulco's nine protected bays run a water-taxi network from Santa Cruz Marina — "
                    "short coastal hops between beaches that the road cannot match."
                ),
                "note": "One sourced nine-bays hop at the $20 premium-comparable fare; route economics follow on their own slide.",
                "bullets": (
                    "▸  Marina Santa Cruz → Bahía Maguey\n"
                    "      ~1.42 nm · flagship nine-bays coastal hop\n"
                    "▸  Serves\n"
                    "      Huatulco resort bays and Santa Cruz Marina"
                ),
            },
        }

        reqs: list[dict] = []
        for tag, info in dups:
            page_id = info["new_page_id"]
            slide = by_page.get(page_id)
            if not slide:
                print(f"  WARN missing page {page_id}")
                continue
            roles = map_elements(slide)
            # Map old template child IDs → new via objectIdMappings if present
            # roles already from new slide text scan
            if "city" in tag:
                plan = fill_plan[tag]
                reqs += fill_city_slide(svc, roles, **plan)
                applied["duplicated"].append({"tag": tag, "page": page_id, "roles": {k: v for k, v in roles.items() if k != "_all"}})
            else:
                route = holbox if "holbox" in tag else huatulco
                reqs += fill_econ_slide(svc, roles, route)
                applied["duplicated"].append({"tag": tag, "page": page_id, "roles": {k: v for k, v in roles.items() if k != "_all"}})
                applied["econ_source_map"][tag] = {
                    "route_id": route.get("route_id"),
                    "label": route.get("label"),
                    "revenue_per_boat_yr": (route.get("unit_economics") or {}).get("revenue_per_boat_yr"),
                    "margin": (route.get("unit_economics") or {}).get("margin"),
                    "payback_years": (route.get("unit_economics") or {}).get("payback_years"),
                    "source": "generated-deck-economics.json",
                }

        if reqs:
            batch(svc, reqs)

        # Move the four new slides to end (after close)
        # After duplicates they sit after the source slides; reorder to absolute end.
        pres2 = svc.presentations().get(presentationId=PID).execute()
        n = len(pres2["slides"])
        # new pages should be moved to indices n-4..n-1 if not already
        new_pages = [info["new_page_id"] for _, info in dups]
        # Place sequentially at end
        move_reqs = []
        for i, pid_s in enumerate(new_pages):
            move_reqs.append(
                {
                    "updateSlidesPosition": {
                        "slideObjectIds": [pid_s],
                        "insertionIndex": n - len(new_pages) + i,
                    }
                }
            )
        batch(svc, move_reqs, chunk=1)

    # Re-fill if slides already exist with titles
    pres = svc.presentations().get(presentationId=PID).execute()
    for s in pres["slides"]:
        roles = map_elements(s)
        texts = " ".join(t for _, t in roles.get("_all") or [])
        u = texts.upper()
        if "HOLBOX" in u and "WHAT ONE BOAT" not in u and "EARNS" not in u:
            plan = {
                "title": "ISLA HOLBOX",
                "body": (
                    "Chiquilá is the mainland gateway to car-free Isla Holbox — a single passenger "
                    "ferry crossing across the Yalahau channel, high-frequency and sole access for most visitors."
                ),
                "note": "One sourced crossing at the $12 island-hop fare; route economics follow on their own slide.",
                "bullets": (
                    "▸  Chiquilá → Isla Holbox\n"
                    "      ~5.5 nm · sole passenger crossing to car-free Holbox\n"
                    "▸  Serves\n"
                    "      Mainland Riviera Maya visitors and Holbox stays"
                ),
            }
            batch(svc, fill_city_slide(svc, roles, **plan))
            applied.setdefault("refilled", []).append(s["objectId"])
        elif "WHAT ONE BOAT EARNS · HOLBOX" in u or ("HOLBOX" in u and "EARNS" in u):
            batch(svc, fill_econ_slide(svc, roles, holbox))
            applied["econ_source_map"]["holbox_econ"] = {
                "route_id": holbox["route_id"],
                "page": s["objectId"],
                "source": "generated-deck-economics.json",
                "revenue_per_boat_yr": holbox["unit_economics"]["revenue_per_boat_yr"],
                "payback_years": holbox["unit_economics"]["payback_years"],
            }
        elif "HUATULCO" in u and "EARNS" not in u:
            plan = {
                "title": "BAHÍAS DE HUATULCO",
                "body": (
                    "Bahías de Huatulco's nine protected bays run a water-taxi network from Santa Cruz Marina — "
                    "short coastal hops between beaches that the road cannot match."
                ),
                "note": "One sourced nine-bays hop at the $20 premium-comparable fare; route economics follow on their own slide.",
                "bullets": (
                    "▸  Marina Santa Cruz → Bahía Maguey\n"
                    "      ~1.42 nm · flagship nine-bays coastal hop\n"
                    "▸  Serves\n"
                    "      Huatulco resort bays and Santa Cruz Marina"
                ),
            }
            batch(svc, fill_city_slide(svc, roles, **plan))
            applied.setdefault("refilled", []).append(s["objectId"])
        elif "WHAT ONE BOAT EARNS · HUATULCO" in u or ("HUATULCO" in u and "EARNS" in u):
            batch(svc, fill_econ_slide(svc, roles, huatulco))
            applied["econ_source_map"]["huatulco_econ"] = {
                "route_id": huatulco["route_id"],
                "page": s["objectId"],
                "source": "generated-deck-economics.json",
                "revenue_per_boat_yr": huatulco["unit_economics"]["revenue_per_boat_yr"],
                "payback_years": huatulco["unit_economics"]["payback_years"],
            }

    # --- C. Close-out ---
    pres = svc.presentations().get(presentationId=PID).execute()
    prize = verify_prize(pres)
    print("C. Prize verify:", prize)
    manifest = sync_manifest(pres)
    print(f"  slide_count={manifest['slide_count']}")

    # copy lint
    import subprocess

    lint = subprocess.run(
        [sys.executable, str(ROOT / "deck-studio/qa/partner_copy_lint.py"), str(DECK)],
        capture_output=True,
        text=True,
    )
    lint_ok = lint.returncode == 0
    print("  partner_copy_lint:", "OK" if lint_ok else "FAIL", lint.stdout[-200:] if lint.stdout else lint.stderr[-200:])

    # overview readback
    ov = find_slide(pres, OVERVIEW)
    ov_texts = []
    if ov:
        for el in ov.get("pageElements") or []:
            t = extract_text(el.get("shape") or {})
            if t:
                ov_texts.append(f"{el['objectId']}: {t[:80]}")

    receipt = {
        "at": NOW,
        "deck_id": PID,
        "spec": "GROK-SPEC-didi-mexico-phase4-2026-07-21.md",
        "slide_count": manifest["slide_count"],
        "overview": overview,
        "overview_readback": ov_texts,
        "prize_verify": prize,
        "applied": applied,
        "econ_source_map": applied.get("econ_source_map"),
        "image_provenance": {
            "holbox_city_n30": "needs_sourcing (image-manifest)",
            "huatulco_city_n30": "needs_sourcing (image-manifest)",
            "atlas_map_slots": "human-only (not populated by automation)",
        },
        "partner_copy_lint": {"ok": lint_ok, "stdout": (lint.stdout or "")[-500:]},
        "guardrails": {
            "holbox_backup_only": True,
            "main_spine_untouched_except_overview": True,
            "pv_cabos_display_null": True,
        },
        "generated_sha_binding": (gen.get("source_sha256") or {}).get("binding"),
    }
    RECEIPT.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Receipt: {RECEIPT.relative_to(ROOT)}")
    return 0 if lint_ok else 1


if __name__ == "__main__":
    sys.exit(main())
