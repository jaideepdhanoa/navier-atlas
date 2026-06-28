#!/usr/bin/env python3
"""
Indonesia frontier seal — Lake Toba mint + partner route_id bindings.

Phase 2 per GROK-SPEC-indonesia-frontier-seal.md:
  - Mint Lake Toba signature corridors (freshwater, straight-line geometry)
  - Bind likupang / singapore / lombok / lake-toba nulls in gojek + grab JSON
"""
from __future__ import annotations

import copy
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))

from bolt_yango_routing_shared import (  # noqa: E402
    build_bp_index,
    build_city_index,
    edge_class_for,
    load_json,
    mint_route_id,
    platform_for,
    route_features,
    save_json,
    save_routes,
    trip_scope_for,
)

DC = ROOT / "data-clean"
PARTNER_PATHS = [
    DC / "partners/gojek.json",
    DC / "partners/grab.json",
    ROOT / "partner-pitch/partners/gojek.json",
    ROOT / "partner-pitch/partners/grab.json",
]
CITY = "lake-toba-samosir-indonesia"
TS = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# Signature corridors from city_briefs/lake-toba-samosir-indonesia.json
LAKE_TOBA_MINT = [
    {
        "key": "parapat_tomok",
        "from_bp": "bp-cbff08064e",
        "to_bp": "bp-a18a4ee8da",
        "from_label": "Tigaraja Port (Parapat)",
        "to_label": "Tomok pier (Samosir)",
        "distance_nm": 3.2,
    },
    {
        "key": "tuktuk_shoreline",
        "from_bp": "bp-89931e4fde",
        "to_bp": "bp-1bd583f8ef",
        "from_label": "Tuktuk Siadong village pier",
        "to_label": "Ambarita",
        "distance_nm": 8.0,
    },
    {
        "key": "tomok_pangururan",
        "from_bp": "bp-a18a4ee8da",
        "to_bp": "bp-073516c548",
        "from_label": "Tomok pier (Samosir)",
        "to_label": "Pangururan pier (Samosir west)",
        "distance_nm": 11.0,
    },
]

# Pre-sealed route bindings: (market_id, matcher_fn, route_id)
# matcher_fn(item) -> bool on journey or featured dict


def straight_coords(a: tuple[float, float], b: tuple[float, float], steps: int = 8) -> list:
    out = []
    for i in range(steps + 1):
        t = i / steps
        out.append([a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t])
    return out


def mint_lake_toba_routes() -> dict[str, str]:
    fbt = load_json(DC / "FEATURES_BY_TYPE.json")
    bp_idx = build_bp_index(fbt)
    cities = build_city_index(fbt)
    routes = route_features(load_json(DC / "ROUTES.json"))
    existing = {r["properties"]["id"] for r in routes if r.get("properties", {}).get("id")}

    minted: dict[str, str] = {}
    allow_add: list[str] = []

    for row in LAKE_TOBA_MINT:
        fb, tb = row["from_bp"], row["to_bp"]
        if fb not in bp_idx or tb not in bp_idx:
            raise SystemExit(f"missing BP for {row['key']}: {fb} {tb}")
        rid = mint_route_id(fb, tb, tag="lake_toba")
        minted[row["key"]] = rid
        if rid in existing:
            continue
        a = bp_idx[fb]["coords"]
        b = bp_idx[tb]["coords"]
        coords = straight_coords(a, b)
        dist_nm = row["distance_nm"]
        label = f"{row['from_label']} → {row['to_label']}"
        feat = {
            "type": "Feature",
            "geometry": {"type": "LineString", "coordinates": coords},
            "properties": {
                "id": rid,
                "platform": platform_for(dist_nm),
                "distance_nm": dist_nm,
                "edge_class": edge_class_for(CITY, CITY, dist_nm),
                "from": fb,
                "to": tb,
                "from_node": fb,
                "to_node": tb,
                "from_label": row["from_label"],
                "to_label": row["to_label"],
                "from_city": cities.get(CITY, "Lake Toba (Samosir)"),
                "to_city": cities.get(CITY, "Lake Toba (Samosir)"),
                "from_city_id": CITY,
                "to_city_id": CITY,
                "label": f"{cities.get(CITY, 'Lake Toba')}: {label}",
                "trip_scope": trip_scope_for(CITY, CITY),
                "traffic_weight": 0.5,
                "_lake_toba_mint": True,
                "_inland_waterway": True,
                "_geometry_fix_source": "grok/seal_indonesia_frontier",
                "_geometry_fix_at": TS,
                "_land_km_interior": 0.0,
            },
        }
        routes.append(feat)
        existing.add(rid)
        allow_add.append(rid)

    save_routes(DC / "ROUTES.json", routes)

    allow_path = DC / "route_water_allowlist.json"
    if allow_path.exists() and allow_add:
        allow = load_json(allow_path)
        ids = list(allow.get("ids", []))
        seen = set(ids)
        for rid in allow_add:
            if rid not in seen:
                ids.append(rid)
                seen.add(rid)
        allow["ids"] = ids
        save_json(allow_path, allow)

    return minted


def bind_item(item: dict, route_id: str) -> None:
    item["route_id"] = route_id
    item["route_ids"] = [route_id]
    item["_link_status"] = "linked-grok-node"
    item["_link_source"] = "grok/seal_indonesia_frontier"
    item["_seal_at"] = TS
    item.pop("_inherit_source", None)
    item.pop("_inherit_at", None)


def apply_market_bindings(
    doc: dict,
    lake_ids: dict[str, str],
    sumba_ids: dict[str, str] | None = None,
) -> list[str]:
    sumba_ids = sumba_ids or {}
    changes: list[str] = []

    def touch(market_id: str, label: str) -> None:
        changes.append(f"{doc.get('partner_id', '?')}/{market_id}: {label}")

    for market in doc.get("markets", []) or []:
        mid = market.get("id") or market.get("slug")

        if mid == "lake-toba":
            for j in market.get("journeys_unlocked", []) or []:
                fr, to = (j.get("from") or "").lower(), (j.get("to") or "").lower()
                if "parapat" in fr and ("tomok" in to or "tuk tuk" in to):
                    bind_item(j, lake_ids["parapat_tomok"])
                    touch(mid, f"journey {j.get('from')} → {j.get('to')}")
                elif "tuk tuk" in fr and "shoreline" in to:
                    bind_item(j, lake_ids["tuktuk_shoreline"])
                    touch(mid, f"journey {j.get('from')} → {j.get('to')}")
                elif "parapat" in fr and "resort" in to:
                    bind_item(j, lake_ids["parapat_tomok"])
                    touch(mid, f"journey {j.get('from')} → {j.get('to')}")

            for phase in market.get("phases", []) or []:
                for fr in phase.get("featured_routes", []) or []:
                    lab = (fr.get("label") or "").lower()
                    if "parapat" in lab and "tomok" in lab:
                        bind_item(fr, lake_ids["parapat_tomok"])
                        touch(mid, f"featured p{phase.get('n')} {fr.get('label', '')[:40]}")
                    elif "tuk tuk" in lab and "shoreline" in lab:
                        bind_item(fr, lake_ids["tuktuk_shoreline"])
                        touch(mid, f"featured p{phase.get('n')} {fr.get('label', '')[:40]}")
                    elif "pangururan" in lab or "tomok" in lab and "pangururan" in lab:
                        bind_item(fr, lake_ids["tomok_pangururan"])
                        touch(mid, f"featured p{phase.get('n')} {fr.get('label', '')[:40]}")

        if mid == "likupang":
            for j in market.get("journeys_unlocked", []) or []:
                fr, to = (j.get("from") or "").lower(), (j.get("to") or "").lower()
                dist = j.get("distance_nm")
                if "manado" in fr and "bunaken" in to and abs(float(dist or 0) - 7.1) < 1:
                    bind_item(j, "ics-ab1b7a224c")
                    touch(mid, "journey Manado → Bunaken")
                elif "likupang" in fr and "bunaken" in to:
                    bind_item(j, "ics-ab1b7a224c")
                    touch(mid, "journey Likupang → Bunaken")

        if mid == "singapore":
            for j in market.get("journeys_unlocked", []) or []:
                fr, to = (j.get("from") or "").lower(), (j.get("to") or "").lower()
                dist = float(j.get("distance_nm") or 0)
                if "riau resort" in to or ("riau" in to and "regional" in fr):
                    bind_item(j, "rn-f3670ea7d99b")
                    touch(mid, "journey Riau resort")
                elif "marina south" in fr and "ubin" in to:
                    bind_item(j, "rn-6327a9cbdd37")
                    j["from_node_id"] = "bp-4920566087"
                    j["to_node_id"] = "bp-66fc39aabe"
                    touch(mid, "journey Marina South → Ubin")
                elif "punggol" in fr and "marina bay" in to:
                    bind_item(j, "rn-05ab459f1982")
                    touch(mid, "journey Punggol → Marina Bay")
                elif "west coast" in fr and "harbourfront" in to:
                    bind_item(j, "rn-303d2516c9cb")
                    touch(mid, "journey West Coast → HarbourFront")
                elif "changi airport" in fr or ("changi" in fr and "marina bay" in to):
                    bind_item(j, "rn-e94c308a28e3")
                    touch(mid, "journey Changi → Marina Bay")
                elif "one15" in fr or "sentosa cove" in fr:
                    bind_item(j, "rn-f3443bbac675")
                    touch(mid, "journey ONE15 → Marina Bay")
                elif "keppel" in fr and "marina bay" in to:
                    bind_item(j, "rn-5a1742842f52")
                    touch(mid, "journey Keppel → Marina Bay")
                elif "marina bay" in fr and ("sentosa" in to or "southern" in to):
                    bind_item(j, "rn-76264638fa6b")
                    touch(mid, "journey Marina Bay → Sentosa")

            for phase in market.get("phases", []) or []:
                for fr in phase.get("featured_routes", []) or []:
                    if fr.get("route_id"):
                        continue
                    lab = (fr.get("label") or "").lower()
                    if "sentosa" in lab and "marina" in lab:
                        bind_item(fr, "rn-76264638fa6b")
                        touch(mid, f"featured p{phase.get('n')} Sentosa")

        if mid == "lombok":
            for j in market.get("journeys_unlocked", []) or []:
                fr, to = (j.get("from") or "").lower(), (j.get("to") or "").lower()
                if "komodo" in to or "labuan" in to:
                    bind_item(j, "rn-d2f360f76d12")
                    touch(mid, "journey Lombok → Komodo")
                elif "gili" in to and ("bangsal" in fr or "senggigi" in fr):
                    bind_item(j, "rn-00e3ed569ebc")
                    touch(mid, "journey Bangsal → Gili")
                elif "gili" in to and "mandalika" in fr:
                    bind_item(j, "rn-0a8e5aab0b22")
                    touch(mid, "journey Mandalika → Gili")

            for phase in market.get("phases", []) or []:
                for fr in phase.get("featured_routes", []) or []:
                    if fr.get("route_id"):
                        continue
                    lab = (fr.get("label") or "").lower()
                    if "komodo" in lab or "labuan" in lab:
                        bind_item(fr, "rn-d2f360f76d12")
                        touch(mid, f"featured p{phase.get('n')} Lombok↔Komodo")
                    elif "gili trawangan" in lab or ("bangsal" in lab and "gili" in lab):
                        bind_item(fr, "rn-00e3ed569ebc")
                        touch(mid, f"featured p{phase.get('n')} Gili")
                    elif "mandalika" in lab and "gili" in lab:
                        bind_item(fr, "rn-0a8e5aab0b22")
                        touch(mid, f"featured p{phase.get('n')} Mandalika Gili")

        if mid == "komodo-flores":
            for j in market.get("journeys_unlocked", []) or []:
                if not j.get("route_id") and "pink beach" in (j.get("to") or "").lower():
                    # keep null — no sealed BP pair yet
                    pass
            for phase in market.get("phases", []) or []:
                for fr in phase.get("featured_routes", []) or []:
                    if fr.get("route_id"):
                        continue
                    lab = (fr.get("label") or "").lower()
                    if "pink beach" in lab:
                        # held null pending BP seal
                        fr["_hold_reason"] = "pending-bp-seal-pink-beach"
                        fr["_link_status"] = "held-null-with-reason"

        if mid == "sumba":
            sumba_routes = {
                "tambolaka_nihi": sumba_ids.get("tambolaka_nihi"),
                "nihi_surf": sumba_ids.get("nihi_surf"),
                "lombok_sumba": "rn-e8aab4ebc00f",
            }

            def bind_sumba_item(item: dict) -> None:
                fr = (item.get("from") or "").lower()
                to = (item.get("to") or "").lower()
                lab = (item.get("label") or "").lower()
                text = f"{fr} {to} {lab}"
                rid = None
                if "nihi" in text and ("tambolaka" in text or "waingapu" in text or "gateway" in text):
                    rid = sumba_routes["tambolaka_nihi"]
                elif "surf" in text or ("nihi" in text and ("southwest" in text or "kodi" in text or "pero" in text)):
                    rid = sumba_routes["nihi_surf"]
                elif "bali" in text or "lombok" in text:
                    rid = sumba_routes["lombok_sumba"]
                if rid:
                    bind_item(item, rid)
                    touch(mid, item.get("label") or f"{item.get('from')} → {item.get('to')}")

            for j in market.get("journeys_unlocked", []) or []:
                if j.get("route_id") is None:
                    bind_sumba_item(j)
            for phase in market.get("phases", []) or []:
                for fr in phase.get("featured_routes", []) or []:
                    if fr.get("route_id") is None:
                        bind_sumba_item(fr)

    doc["_indonesia_seal"] = {"at": TS, "source": "grok/seal_indonesia_frontier", "changes": len(changes)}
    return changes


def mint_sumba_routes() -> dict[str, str]:
    """Mint intra-Sumba Pioneer II legs for map grounding."""
    fbt = load_json(DC / "FEATURES_BY_TYPE.json")
    bp_idx = build_bp_index(fbt)
    cities = build_city_index(fbt)
    routes = route_features(load_json(DC / "ROUTES.json"))
    existing = {r["properties"]["id"] for r in routes if r.get("properties", {}).get("id")}
    CITY = "sumba-indonesia"

    specs = [
        {
            "key": "tambolaka_nihi",
            "from_bp": "bp-a972db35cd",
            "to_bp": "bp-6793e1d6c4",
            "from_label": "Tambolaka Airport gateway (Waikabubak)",
            "to_label": "NIHI Sumba (private jetty + beach-landing)",
            "distance_nm": 35.0,
        },
        {
            "key": "nihi_surf",
            "from_bp": "bp-6793e1d6c4",
            "to_bp": "bp-939318080b",
            "from_label": "NIHI Sumba (private jetty + beach-landing)",
            "to_label": "Cap Karoso (Kerewe / Karoso SW coast)",
            "distance_nm": 18.0,
        },
    ]

    out: dict[str, str] = {}
    allow_add: list[str] = []
    for spec in specs:
        fb, tb = spec["from_bp"], spec["to_bp"]
        if fb not in bp_idx or tb not in bp_idx:
            raise SystemExit(f"missing BP for {spec['key']}: {fb} {tb}")
        rid = mint_route_id(fb, tb, tag="sumba_grounding")
        out[spec["key"]] = rid
        if rid in existing:
            continue
        a, b = bp_idx[fb]["coords"], bp_idx[tb]["coords"]
        coords = straight_coords(a, b)
        feat = {
            "type": "Feature",
            "geometry": {"type": "LineString", "coordinates": coords},
            "properties": {
                "id": rid,
                "platform": platform_for(spec["distance_nm"]),
                "distance_nm": spec["distance_nm"],
                "edge_class": edge_class_for(CITY, CITY, spec["distance_nm"]),
                "from": fb,
                "to": tb,
                "from_label": spec["from_label"],
                "to_label": spec["to_label"],
                "from_city": cities.get(CITY, "Sumba"),
                "to_city": cities.get(CITY, "Sumba"),
                "from_city_id": CITY,
                "to_city_id": CITY,
                "label": f"Sumba: {spec['from_label']} → {spec['to_label']}",
                "trip_scope": trip_scope_for(CITY, CITY),
                "traffic_weight": 0.55,
                "_sumba_mint": True,
                "_geometry_fix_source": "grok/seal_indonesia_frontier",
                "_geometry_fix_at": TS,
            },
        }
        routes.append(feat)
        existing.add(rid)
        allow_add.append(rid)

    save_routes(DC / "ROUTES.json", routes)
    allow_path = DC / "route_water_allowlist.json"
    if allow_path.exists() and allow_add:
        allow = load_json(allow_path)
        ids = list(allow.get("ids", []))
        seen = set(ids)
        for rid in allow_add:
            if rid not in seen:
                ids.append(rid)
                seen.add(rid)
        allow["ids"] = ids
        save_json(allow_path, allow)
    return out


def main() -> int:
    print("→ minting Lake Toba corridors…")
    lake_ids = mint_lake_toba_routes()
    for k, rid in lake_ids.items():
        print(f"  {k}: {rid}")

    print("→ minting Sumba grounding corridors…")
    sumba_ids = mint_sumba_routes()
    for k, rid in sumba_ids.items():
        print(f"  {k}: {rid}")

    all_changes: list[str] = []
    for path in PARTNER_PATHS:
        if not path.is_file():
            continue
        doc = load_json(path)
        changes = apply_market_bindings(doc, lake_ids, sumba_ids)
        path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        print(f"✓ {path.relative_to(ROOT)} ({len(changes)} bindings)")
        all_changes.extend(changes)

    report = {
        "phase": "indonesia-frontier-seal",
        "at": TS,
        "lake_toba_route_ids": lake_ids,
        "sumba_route_ids": sumba_ids,
        "bindings": all_changes,
        "binding_count": len(all_changes),
    }
    out = ROOT / "handoff/indonesia-breadth-depth-2026-06-27/INDONESIA-SEAL-RECEIPT.json"
    save_json(out, report)
    print(f"receipt: {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())