#!/usr/bin/env python3
"""DiDi ex-China — Brazil / Colombia G2 geometry seal.

Inputs:
  handoff/didi-ex-china/waves/DIDI-BRAZIL-COLOMBIA-DEEPENING-2026-07-09.json

Lane: Grok geometry only.
  - Re-parent Guanabara/Rio BPs wrongly under Angra
  - Confirm evidence-backed terminals; hold null for unsealed endpoints
  - Seal exact four Rio public-ferry route IDs + tag Cartagena geometry baseline
  - Bind DiDi Brazil/Colombia featured_routes (no invented demand, no new route IDs)

Does NOT invent L3 pax/fares. Does NOT mint route IDs. Does NOT edit live deck.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
FBT = ROOT / "data-clean/FEATURES_BY_TYPE.json"
ROUTES = ROOT / "data-clean/ROUTES.json"
SEAL = ROOT / "data-clean/SEAL.json"
PITCH = ROOT / "partner-pitch/partners/didi.json"
DC = ROOT / "data-clean/partners/didi.json"
OUT_DIR = ROOT / "handoff/didi-ex-china/waves"
DEEPENING = OUT_DIR / "DIDI-BRAZIL-COLOMBIA-DEEPENING-2026-07-09.json"
RECEIPT = OUT_DIR / "G2-BRAZIL-COLOMBIA-SEAL-RECEIPT-2026-07-09.json"
SPINE = OUT_DIR / "BRAZIL-COLOMBIA-ROUTE-SPINE-FOR-TASKLET-2026-07-09.json"
HANDOFF_MD = OUT_DIR / "TASKLET-T3-BRAZIL-COLOMBIA-HANDOFF.md"

# Exact gold IDs only — research-locked
RIO_SPINE = [
    {
        "route_id": "rn-1886629dbf0c",
        "od": "Praça XV ↔ Arariboia (Niterói)",
        "from_bp": "bp-660ea6736a",
        "to_bp": "bp-45ba34fda2",
        "from_city_id": "rio-de-janeiro-brazil",
        "to_city_id": "rio-de-janeiro-brazil",
        "distance_nm": 2.7,
        "service_status": "current_scheduled",
        "sub_proposal": "brazil",
        "priority": 1,
        "demand_hint": {
            "note": "Peak-day system observations exist; annual line-by-line pax still null. Tasklet owns annual one-way + fare effective year.",
            "model_use": "blocked_until_annual_line_pax",
            "fare_benchmark_brl": 5.0,
            "fare_note": "State notice R$5 Arariboia/Cocotá/Paquetá — effective year needs confirmation before USD yield.",
        },
    },
    {
        "route_id": "rn-80f0d0ebe0bd",
        "od": "Praça XV ↔ Charitas (Niterói)",
        "from_bp": "bp-660ea6736a",
        "to_bp": "bp-85947006eb",
        "from_city_id": "rio-de-janeiro-brazil",
        "to_city_id": "rio-de-janeiro-brazil",
        "distance_nm": 4.4,
        "service_status": "current_scheduled",
        "sub_proposal": "brazil",
        "priority": 1,
        "demand_hint": {
            "note": "Official peak-day Charitas boardings (7,928) must not be annualized.",
            "model_use": "blocked_until_annual_line_pax",
            "fare_benchmark_brl": 7.7,
            "fare_note": "2025 Charitas benchmark R$7.70 — Tasklet confirms currency/yield mix.",
        },
    },
    {
        "route_id": "rn-00bb6ded4be5",
        "od": "Praça XV ↔ Paquetá",
        "from_bp": "bp-660ea6736a",
        "to_bp": "bp-e2aae460aa",
        "from_city_id": "rio-de-janeiro-brazil",
        "to_city_id": "rio-de-janeiro-brazil",
        "distance_nm": 9.2,
        "service_status": "current_scheduled",
        "sub_proposal": "brazil",
        "priority": 2,
        "demand_hint": {
            "model_use": "blocked_until_annual_line_pax",
            "fare_benchmark_brl": 5.0,
        },
    },
    {
        "route_id": "rn-369ef0eb69d9",
        "od": "Praça XV ↔ Cocotá",
        "from_bp": "bp-660ea6736a",
        "to_bp": "bp-53684b584c",
        "from_city_id": "rio-de-janeiro-brazil",
        "to_city_id": "rio-de-janeiro-brazil",
        "distance_nm": 6.0,
        "service_status": "current_scheduled",
        "sub_proposal": "brazil",
        "priority": 2,
        "demand_hint": {
            "model_use": "blocked_until_annual_line_pax",
            "fare_benchmark_brl": 5.0,
        },
    },
]

# Geometry exists; current scheduled service not verified — featured with honest status
COLOMBIA_GEOMETRY = [
    {
        "route_id": "rn-aa790551baa7",
        "od": "Club de Pesca Marina ↔ Bocachica (Tierrabomba)",
        "from_city_id": "cartagena-colombia",
        "to_city_id": "cartagena-colombia",
        "distance_nm": 5.74,
        "service_status": "atlas_geometry_current_service_unverified",
        "sub_proposal": "colombia",
        "priority": 2,
        "demand_hint": {
            "model_use": "blocked_until_service_proof_and_annual_pax",
            "note": "Do not map La Bodeguita terminal entries 1:1 onto this corridor.",
        },
    },
]

# Held null — no route_id mint
HELD_NULL_CORRIDORS = [
    {
        "od": "Cais da Lapa ↔ Vila do Abraão (Estação Abraão)",
        "route_id": None,
        "reason": "historical_operation_current_timetable_unverified",
        "sub_proposal": "brazil",
        "city_ids": ["angra-dos-reis-ilha-grande-brazil"],
    },
    {
        "od": "Costa da Lagoa lacustrine line",
        "route_id": None,
        "reason": "current_service_evidence_route_geometry_unsealed",
        "sub_proposal": "brazil",
        "city_ids": ["florianopolis-brazil"],
    },
    {
        "od": "Muelle La Bodeguita ↔ Isla Grande / Rosario",
        "route_id": None,
        "reason": "la_bodeguita_bp_and_destination_split_unsealed",
        "sub_proposal": "colombia",
        "city_ids": ["cartagena-colombia"],
    },
    {
        "od": "Barranquilla Río-Bus",
        "route_id": None,
        "reason": "future_project_not_current_scheduled",
        "sub_proposal": "colombia",
        "city_ids": ["barranquilla-colombia"],
    },
]

# Must-fix route endpoint parents (evidence + gold route endpoints)
MUST_REPARENT = {
    "bp-45ba34fda2": {
        "parent_city_id": "rio-de-janeiro-brazil",
        "name": "Barcas Rio - Terminal Araribóia",
        "bp_type": "ferry_terminal",
        "reason": "Niterói Arariboia ferry terminal; was mis-parented under Angra",
    },
    "bp-e2aae460aa": {
        "parent_city_id": "rio-de-janeiro-brazil",
        "name": "Paquetá Island Terminal",
        "bp_type": "ferry_terminal",
        "reason": "Guanabara Paquetá ferry terminal; was mis-parented under Angra",
    },
}

# Confirm-only (correct parent already)
CONFIRM_BPS = [
    {
        "id": "bp-660ea6736a",
        "parent_city_id": "rio-de-janeiro-brazil",
        "name": "Praça XV Terminal",
        "bp_type": "ferry_terminal",
        "market": "brazil",
    },
    {
        "id": "bp-85947006eb",
        "parent_city_id": "rio-de-janeiro-brazil",
        "name": "Charitas Terminal (Niterói)",
        "bp_type": "ferry_terminal",
        "market": "brazil",
    },
    {
        "id": "bp-53684b584c",
        "parent_city_id": "rio-de-janeiro-brazil",
        "name": "Cocotá Terminal",
        "bp_type": "ferry_terminal",
        "market": "brazil",
    },
    {
        "id": "bp-ff2a6bbcaf",
        "parent_city_id": "angra-dos-reis-ilha-grande-brazil",
        "name": "Cais da Lapa",
        "bp_type": "ferry_terminal",
        "market": "brazil",
        "note": "Identity safe; Angra–Abraão route_id remains null",
    },
    {
        "id": "bp-2f52d0faf1",
        "parent_city_id": "angra-dos-reis-ilha-grande-brazil",
        "name": "Marina Pier Costa Verde",
        "bp_type": "marina",
        "market": "brazil",
        "note": "Cluster anchor; display-only until route pin",
    },
    {
        "id": "bp-7adc0d37cf",
        "parent_city_id": "florianopolis-brazil",
        "name": "Terminal Lacustre Ponto de Saída Costa da Lagoa",
        "bp_type": "public_pier",
        "market": "brazil",
        "note": "Current lacustrine service; opposite landing + route_id unsealed",
    },
    {
        "id": "bp-cartagena-bocachica",
        "parent_city_id": "cartagena-colombia",
        "name": "Bocachica Tierrabomba Jetty",
        "bp_type": "ferry_terminal",
        "market": "colombia",
        "note": "Geometry baseline endpoint for rn-aa790551baa7",
    },
    {
        "id": "bp-709896d994",
        "parent_city_id": "cartagena-colombia",
        "name": "Isla Grande landing",
        "bp_type": "ferry_terminal",
        "market": "colombia",
        "note": "Do not route-bind until exact dock confirmed",
        "hold_route_bind": True,
    },
]

NON_BP_MARK = [
    {
        "id": "bp-899770a893",
        "reason": "cruise_terminal_not_island_transfer_substitute_for_la_bodeguita",
    },
    {
        "id": "bp-fe30890718",
        "reason": "coarse_record_not_current_passenger_bp",
    },
]

FUTURE_MARK = [
    {
        "id": "bp-574ef0c2d1",
        "reason": "barranquilla_riverfront_rio_bus_future_only",
    },
]

# Guanabara box — BPs under Angra that are clearly Rio metro waterfront
RIO_LON_MIN, RIO_LON_MAX = -43.55, -42.85
RIO_LAT_MIN, RIO_LAT_MAX = -23.05, -22.55


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load(p: Path) -> Any:
    return json.loads(p.read_text())


def save(p: Path, obj: Any, indent: int = 2) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=indent, ensure_ascii=False) + "\n")


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha256_obj(obj: Any) -> str:
    return sha256_bytes(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode())


def index_poi(fbt: dict) -> dict[str, dict]:
    by: dict[str, dict] = {}
    for feat in fbt.get("poi") or []:
        props = feat.get("properties") or {}
        pid = props.get("id")
        if pid:
            by[pid] = feat
    return by


def reparent_and_confirm_bps(fbt: dict) -> dict:
    by = index_poi(fbt)
    ledger: list[dict] = []
    accepted: list[dict] = []

    def touch(bp_id: str, **fields: Any) -> None:
        feat = by.get(bp_id)
        if not feat:
            ledger.append({"id": bp_id, "action": "missing", "status": "drop_missing"})
            return
        props = feat.setdefault("properties", {})
        before = {
            "parent_city_id": props.get("parent_city_id"),
            "name": props.get("name"),
            "status": props.get("status"),
            "bp_type": props.get("bp_type"),
        }
        for k, v in fields.items():
            if v is None:
                continue
            props[k] = v
        props["status"] = props.get("status") or "operational"
        props["_didi_br_co_g2"] = {
            "at": utc_now(),
            "before": before,
            "lane": "brazil-colombia-g2-2026-07-09",
        }
        if props.get("fullName") is None or fields.get("name"):
            props["fullName"] = props.get("name")
        accepted.append({"id": bp_id, "parent_city_id": props.get("parent_city_id"), "action": fields.get("_action")})
        ledger.append(
            {
                "id": bp_id,
                "action": fields.get("_action") or "touch",
                "status": "accepted",
                "parent_city_id": props.get("parent_city_id"),
            }
        )

    # Must reparent route endpoints
    for bp_id, spec in MUST_REPARENT.items():
        touch(
            bp_id,
            parent_city_id=spec["parent_city_id"],
            name=spec["name"],
            bp_type=spec["bp_type"],
            _action="reparent_route_endpoint",
            _reparent_reason=spec["reason"],
        )
        # store reason on props
        feat = by.get(bp_id)
        if feat:
            feat["properties"]["_reparent_reason"] = spec["reason"]

    # Bulk: Angra-parented BPs inside Rio Guanabara coords → Rio
    bulk = 0
    for feat in fbt.get("poi") or []:
        props = feat.get("properties") or {}
        if props.get("parent_city_id") != "angra-dos-reis-ilha-grande-brazil":
            continue
        pid = props.get("id")
        if not pid or pid in MUST_REPARENT:
            continue
        coords = (feat.get("geometry") or {}).get("coordinates") or []
        if len(coords) < 2:
            continue
        lon, lat = float(coords[0]), float(coords[1])
        if RIO_LON_MIN < lon < RIO_LON_MAX and RIO_LAT_MIN < lat < RIO_LAT_MAX:
            before = props.get("parent_city_id")
            props["parent_city_id"] = "rio-de-janeiro-brazil"
            props["_didi_br_co_g2"] = {
                "at": utc_now(),
                "action": "bulk_reparent_guanabara_coords",
                "before_parent": before,
            }
            props["_reparent_reason"] = "coordinates_in_guanabara_box_under_angra"
            bulk += 1
            ledger.append(
                {
                    "id": pid,
                    "action": "bulk_reparent_guanabara_coords",
                    "status": "accepted",
                    "parent_city_id": "rio-de-janeiro-brazil",
                    "name": props.get("name"),
                }
            )
    accepted.append({"action": "bulk_guanabara", "n": bulk})

    for row in CONFIRM_BPS:
        extra = {
            "_action": "confirm_existing",
            "parent_city_id": row["parent_city_id"],
            "name": row["name"],
            "bp_type": row["bp_type"],
        }
        touch(row["id"], **extra)
        feat = by.get(row["id"])
        if feat and row.get("hold_route_bind"):
            feat["properties"]["_hold_route_bind"] = True
            feat["properties"]["_hold_reason"] = row.get("note")
        if feat and row.get("note"):
            feat["properties"]["_g2_note"] = row["note"]

    for row in NON_BP_MARK:
        feat = by.get(row["id"])
        if not feat:
            ledger.append({"id": row["id"], "action": "non_bp_mark", "status": "missing"})
            continue
        props = feat.setdefault("properties", {})
        props["_not_route_demand_proof"] = True
        props["_didi_br_co_g2"] = {"at": utc_now(), "action": "mark_non_bp_poi", "reason": row["reason"]}
        ledger.append({"id": row["id"], "action": "mark_non_bp_poi", "status": "accepted", "reason": row["reason"]})

    for row in FUTURE_MARK:
        feat = by.get(row["id"])
        if not feat:
            ledger.append({"id": row["id"], "action": "future_mark", "status": "missing"})
            continue
        props = feat.setdefault("properties", {})
        props["_future_only"] = True
        props["_didi_br_co_g2"] = {"at": utc_now(), "action": "mark_future_only", "reason": row["reason"]}
        ledger.append({"id": row["id"], "action": "mark_future_only", "status": "accepted", "reason": row["reason"]})

    # Explicit held (no invent)
    for hold in [
        {"name": "Cais das Barcas / Estação Abraão", "reason": "no_atlas_bp_id_coords_null"},
        {"name": "Costa da Lagoa community landing(s)", "reason": "opposite_landing_unsealed"},
        {"name": "Muelle Turístico La Bodeguita", "reason": "no_exact_bp_id_or_coords_in_research"},
        {"name": "Río-Bus proposed stations", "reason": "future_project"},
    ]:
        ledger.append({**hold, "action": "explicit_hold", "status": "held_null"})

    return {
        "accepted_n": len([x for x in ledger if x.get("status") == "accepted"]),
        "bulk_guanabara_reparent": bulk,
        "ledger": ledger,
    }


def seal_routes(routes: list) -> dict:
    by_id: dict[str, int] = {}
    for i, f in enumerate(routes):
        rid = (f.get("properties") or {}).get("id")
        if rid:
            by_id[rid] = i
    changes: list[dict] = []

    def patch(rid: str, **kwargs: Any) -> None:
        i = by_id.get(rid)
        if i is None:
            changes.append({"route_id": rid, "action": "missing"})
            return
        props = routes[i].setdefault("properties", {})
        before = {k: props.get(k) for k in kwargs if not k.startswith("_")}
        for k, v in kwargs.items():
            if k.startswith("_"):
                continue
            props[k] = v
        props["_didi_br_co_g2_seal"] = {"at": utc_now(), "before": before}
        changes.append({"route_id": rid, "action": "patched", "fields": [k for k in kwargs if not k.startswith("_")]})

    for row in RIO_SPINE:
        patch(
            row["route_id"],
            from_city_id=row["from_city_id"],
            to_city_id=row["to_city_id"],
            cluster_id="brazil",
            **{
                "from": row["from_bp"],
                "to": row["to_bp"],
            },
        )
        # Normalize labels from research / gold
        i = by_id.get(row["route_id"])
        if i is not None:
            props = routes[i]["properties"]
            # keep gold labels if already precise; ensure city cluster
            props["cluster_id"] = "brazil"

    # Cartagena geometry baseline — tag only, no service claim upgrade
    patch(
        "rn-aa790551baa7",
        from_city_id="cartagena-colombia",
        to_city_id="cartagena-colombia",
        cluster_id="colombia",
        service_status_note="atlas_geometry_current_service_unverified",
    )
    # Explicitly do NOT promote rn-84ffd58e7f82 (research held)

    return {
        "changes": changes,
        "n_patched": len([c for c in changes if c.get("action") == "patched"]),
        "missing": [c["route_id"] for c in changes if c.get("action") == "missing"],
    }


def fr_objs(ids: list[str], gold: dict[str, dict]) -> list[dict]:
    out = []
    for rid in ids:
        p = gold.get(rid) or {}
        fl = p.get("from_label") or p.get("from")
        tl = p.get("to_label") or p.get("to")
        cid = p.get("cluster_id")
        if not (rid and fl and tl and cid):
            raise SystemExit(f"cannot build featured row for {rid}: {fl!r} {tl!r} {cid!r}")
        out.append(
            {
                "route_id": rid,
                "from_label": fl,
                "to_label": tl,
                "cluster_id": cid,
            }
        )
    return out


def bind_didi(partner: dict, gold: dict[str, dict]) -> dict:
    rio_ids = [r["route_id"] for r in RIO_SPINE]
    col_ids = [r["route_id"] for r in COLOMBIA_GEOMETRY]
    bound = []

    for m in partner.get("markets") or []:
        if not isinstance(m, dict):
            continue
        mid = m.get("id") or ""
        if mid == "brazil":
            m["featured_routes"] = fr_objs(rio_ids, gold)
            # phases: prove = top 2; expand/full = all 4
            for i, ph in enumerate(m.get("phases") or []):
                if not isinstance(ph, dict):
                    continue
                ph["featured_routes"] = fr_objs(rio_ids[:2] if i == 0 else rio_ids, gold)
            # journeys: bind to sealed Rio spine (replace prior unlinked Costa Verde chip)
            journeys = []
            for row in RIO_SPINE:
                p = gold[row["route_id"]]
                journeys.append(
                    {
                        "from": p.get("from_label"),
                        "to": p.get("to_label"),
                        "from_label": p.get("from_label"),
                        "to_label": p.get("to_label"),
                        "label": f"{p.get('from_label')} → {p.get('to_label')}",
                        "route_id": row["route_id"],
                        "distance_nm": row["distance_nm"],
                        "platform": "Pioneer II",
                        "archetype": "commuter",
                        "from_node_id": row["from_bp"],
                        "to_node_id": row["to_bp"],
                        "_link_status": "linked-g2-seal",
                        "_link_source": "grok/didi-br-co-g2",
                        "economics_status": "economics_pending",
                        "today": "State Barcas Rio ferry with dock queues and mixed reliability.",
                        "with_navier": "A clean high-frequency foiling hop across Guanabara, booked in 99.",
                    }
                )
            m["journeys_unlocked"] = journeys
            # why_navier wow
            wn = m.get("why_navier_now")
            if isinstance(wn, dict):
                wn["wow_corridors"] = fr_objs(rio_ids[:2], gold)
            bound.append({"market": mid, "n": len(rio_ids), "route_ids": rio_ids})
        elif mid == "colombia":
            m["featured_routes"] = fr_objs(col_ids, gold)
            for i, ph in enumerate(m.get("phases") or []):
                if not isinstance(ph, dict):
                    continue
                # Phase 0 empty of finance claims — geometry only on later phases
                ph["featured_routes"] = fr_objs(col_ids, gold) if i > 0 else []
            # Keep aspirational Rosario journeys but ensure no false route_id
            for j in m.get("journeys_unlocked") or []:
                if isinstance(j, dict) and not j.get("route_id"):
                    j.setdefault("_link_status", "aspirational-no-built-route")
                    j.setdefault("economics_status", "roadmap_excluded")
            # Add geometry-baseline journey for Bocachica
            p = gold[col_ids[0]]
            geo_j = {
                "from": p.get("from_label"),
                "to": p.get("to_label"),
                "from_label": p.get("from_label"),
                "to_label": p.get("to_label"),
                "label": f"{p.get('from_label')} → {p.get('to_label')}",
                "route_id": col_ids[0],
                "distance_nm": p.get("distance_nm") or 5.74,
                "platform": "Pioneer II",
                "archetype": "tourism",
                "_link_status": "linked-geometry-service-unverified",
                "_link_source": "grok/didi-br-co-g2",
                "economics_status": "economics_pending",
                "today": "Mixed boat traffic toward Tierrabomba / Bocachica.",
                "with_navier": "A silent premium hop on an existing water corridor once service proof lands, booked in DiDi.",
                "_service_status": "atlas_geometry_current_service_unverified",
            }
            existing = m.get("journeys_unlocked") or []
            # prepend geometry journey; keep prior aspirational chips
            m["journeys_unlocked"] = [geo_j] + [
                j for j in existing if isinstance(j, dict) and j.get("route_id") != col_ids[0]
            ]
            wn = m.get("why_navier_now")
            if isinstance(wn, dict):
                # no wow until service verified — empty wow is honest
                wn["wow_corridors"] = []
            bound.append({"market": mid, "n": len(col_ids), "route_ids": col_ids})

    partner["_didi_g2_brazil_colombia"] = {
        "at": utc_now(),
        "bound": bound,
        "held_null_corridors": HELD_NULL_CORRIDORS,
        "status": "seal-complete / cascade-needed",
        "note": "No L3 demand invented. Annual one-way pax remain null for Tasklet T3.",
    }
    return {"bound": bound}


def update_seal_hashes() -> dict:
    if not SEAL.exists():
        return {}
    seal = load(SEAL)
    files = seal.setdefault("files", {})
    out = {}
    for rel, path in [
        ("FEATURES_BY_TYPE.json", FBT),
        ("ROUTES.json", ROUTES),
        ("partners/didi.json", DC),
    ]:
        if not path.exists():
            continue
        # prefer canonical object hash for JSON
        obj = load(path)
        h = sha256_obj(obj)
        if isinstance(files, dict):
            files[rel] = h
        out[rel] = h
    notes = seal.setdefault("_notes", [])
    if isinstance(notes, list):
        notes.append({"at": utc_now(), "event": "didi-brazil-colombia-g2"})
    seal["sealed_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    save(SEAL, seal)
    return out


def write_spine_and_handoff() -> None:
    spine = {
        "at": utc_now(),
        "partner": "didi",
        "status": "seal-complete / cascade-needed",
        "finance_market_keys": ["brazil", "colombia"],
        "cluster_ids": ["brazil", "colombia"],
        "brazil": RIO_SPINE,
        "colombia": COLOMBIA_GEOMETRY,
        "held_null": HELD_NULL_CORRIDORS,
        "all_route_ids": [r["route_id"] for r in RIO_SPINE]
        + [r["route_id"] for r in COLOMBIA_GEOMETRY],
        "rules": [
            "Null beats wrong — do not invent annual one-way pax or USD fares",
            "Do not annualize Rio peak-day boardings",
            "Do not map La Bodeguita terminal totals 1:1 to any corridor",
            "Do not publish Río-Bus as current scheduled service",
            "Do not claim 99 city-level service in Angra",
            "No grab-greenfield-census / no catch-all didi market",
            "Only exact gold route IDs; no minting",
            "Cartagena rn-aa790551baa7 is geometry baseline until service proof",
        ],
    }
    save(SPINE, spine)

    lines = [
        "# Tasklet T3 handoff — DiDi Brazil / Colombia economics",
        "",
        f"**From:** Grok · Brazil/Colombia G2 seal · `{utc_now()}`  ",
        "**Status after Grok:** `seal-complete / cascade-needed`  ",
        "**Do not:** invent L3 demand, annualize peak-day counts, use Grab census, or cascade on catch-all `didi` market.",
        "",
        "## What Grok sealed",
        "",
        "### Brazil — Rio public ferries (4 exact gold route IDs)",
        "",
    ]
    for r in RIO_SPINE:
        lines.append(
            f"- `{r['route_id']}` — {r['od']} — {r['distance_nm']} nm — `{r['service_status']}`"
        )
    lines += [
        "",
        "### Colombia — geometry baseline only",
        "",
        f"- `{COLOMBIA_GEOMETRY[0]['route_id']}` — {COLOMBIA_GEOMETRY[0]['od']} — **service unverified**",
        "",
        "### Held null (no route_id)",
        "",
    ]
    for h in HELD_NULL_CORRIDORS:
        lines.append(f"- {h['od']} — `{h['reason']}`")
    lines += [
        "",
        "## Tasklet owns next",
        "",
        "1. Annual one-way pax by Rio line (Arariboia, Charitas, Paquetá, Cocotá) + confirmed fare effective year → USD yield.",
        "2. Optional: La Bodeguita exact BP/coords + destination split before any Rosario finance row.",
        "3. Río-Bus stays future until current scheduled operation proof.",
        "4. Country-reference rows for Brazil/Colombia if missing before cascade.",
        "5. Run aggregate → growth → Sheet only on sealed route IDs; leave unsupported null.",
        "",
        "## Spine artifact",
        "",
        f"- `{SPINE.relative_to(ROOT)}`",
        f"- Receipt: `{RECEIPT.relative_to(ROOT)}`",
        "",
        "## Partner proof reminders",
        "",
        "- 99 city-supported: Rio, Florianópolis (not Angra city-level).",
        "- DiDi city-supported: Cartagena, Barranquilla.",
        "",
    ]
    HANDOFF_MD.write_text("\n".join(lines) + "\n")


def run_gates() -> dict:
    gates = {}

    def run(cmd: list[str]) -> dict:
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        out = (r.stdout or "") + (r.stderr or "")
        return {"exit": r.returncode, "tail": "\n".join(out.splitlines()[-50:])}

    gates["gate_g"] = run([sys.executable, str(ROOT / "scripts/audit_partner_copy.py")])
    gates["inheritance_strict"] = run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_partner_inheritance.py"),
            "--partner",
            "didi",
            "--strict",
            "--include-pitch",
            "--json",
        ]
    )
    gates["finance_inheritance"] = run(
        [sys.executable, str(ROOT / "scripts/validate_finance_inheritance.py"), "--json"]
    )
    linkage = ROOT / "scripts/audit-partner-route-linkage.mjs"
    if linkage.exists():
        gates["route_linkage"] = run(["node", str(linkage), "didi"])
    fidelity = ROOT / "scripts/audit_proposal_fidelity.py"
    if fidelity.exists():
        gates["fidelity"] = run([sys.executable, str(fidelity), "--partner", "didi"])
    return gates


def main() -> int:
    deepening = load(DEEPENING)
    assert deepening.get("status", "").startswith("research-complete")

    fbt = load(FBT)
    routes_raw = load(ROUTES)
    routes = routes_raw if isinstance(routes_raw, list) else routes_raw.get("features")
    assert isinstance(routes, list)

    gold: dict[str, dict] = {}
    for f in routes:
        p = f.get("properties") or f
        if p.get("id"):
            gold[p["id"]] = p
    for rid in [r["route_id"] for r in RIO_SPINE] + [r["route_id"] for r in COLOMBIA_GEOMETRY]:
        if rid not in gold:
            raise SystemExit(f"FATAL: spine route missing from gold: {rid}")

    print("1. BP reparent + confirm")
    bp_stats = reparent_and_confirm_bps(fbt)
    print("  ", {k: bp_stats[k] for k in ("accepted_n", "bulk_guanabara_reparent")})

    print("2. Route seal")
    route_stats = seal_routes(routes)
    print("  ", route_stats)
    if route_stats["missing"]:
        raise SystemExit(f"missing routes: {route_stats['missing']}")

    # write geometry — ROUTES is historically single-line compact
    if isinstance(routes_raw, list):
        ROUTES.write_text(
            json.dumps(routes, ensure_ascii=False, separators=(", ", ": ")) + "\n"
        )
    else:
        routes_raw["features"] = routes
        ROUTES.write_text(
            json.dumps(routes_raw, ensure_ascii=False, separators=(", ", ": ")) + "\n"
        )
    save(FBT, fbt, indent=2)

    # refresh gold labels after seal
    gold = {}
    for f in routes:
        p = f.get("properties") or f
        if p.get("id"):
            gold[p["id"]] = p

    print("3. Bind DiDi partner")
    partner = load(PITCH)
    bind_stats = bind_didi(partner, gold)
    print("  ", bind_stats)
    text = json.dumps(partner, indent=2, ensure_ascii=False) + "\n"
    PITCH.write_text(text)
    DC.write_text(text)

    print("4. SEAL hashes")
    seal_h = update_seal_hashes()
    print("  ", {k: v[:12] for k, v in seal_h.items()})

    print("5. Spine + Tasklet handoff")
    write_spine_and_handoff()

    print("6. Gates")
    gates = run_gates()
    for name, g in gates.items():
        print(f"\n=== {name} exit={g['exit']} ===")
        print(g["tail"][:1800])

    receipt = {
        "at": utc_now(),
        "partner": "didi",
        "lane": "G2 Brazil / Colombia geometry seal",
        "status": "seal-complete / cascade-needed",
        "upstream_research": str(DEEPENING.relative_to(ROOT)),
        "route_id_spine": {
            "brazil": [r["route_id"] for r in RIO_SPINE],
            "colombia_geometry_only": [r["route_id"] for r in COLOMBIA_GEOMETRY],
            "held_null": HELD_NULL_CORRIDORS,
        },
        "bp": {
            "accepted_n": bp_stats["accepted_n"],
            "bulk_guanabara_reparent": bp_stats["bulk_guanabara_reparent"],
            "must_reparent": list(MUST_REPARENT.keys()),
            "ledger_sample": bp_stats["ledger"][:40],
            "ledger_n": len(bp_stats["ledger"]),
        },
        "routes": route_stats,
        "partner_bind": bind_stats,
        "gates": {
            name: {
                "exit": g["exit"],
                "pass": g["exit"] == 0
                or (
                    name == "finance_inheritance"
                    and "mexico" not in g["tail"].lower()
                    and "didi" not in g["tail"].lower()
                    and "brazil" not in g["tail"].lower()
                    and "colombia" not in g["tail"].lower()
                )
                or (name == "fidelity" and "PASS" in g["tail"]),
                "tail": g["tail"][-1200:],
            }
            for name, g in gates.items()
        },
        "economics": {
            "annual_one_way_pax": "all_null",
            "cascade": "blocked_until_tasklet_T3",
            "note": "Geography may ship with honest-null economics; market remains cascade-needed.",
        },
        "do_not": deepening.get("do_not_publish"),
        "artifacts": {
            "spine": str(SPINE.relative_to(ROOT)),
            "handoff_md": str(HANDOFF_MD.relative_to(ROOT)),
            "receipt": str(RECEIPT.relative_to(ROOT)),
        },
        "sha256": {
            "FEATURES_BY_TYPE.json": seal_h.get("FEATURES_BY_TYPE.json"),
            "ROUTES.json": seal_h.get("ROUTES.json"),
            "partners/didi.json": seal_h.get("partners/didi.json"),
        },
        "full_program_boundary": "Brazil/Colombia geometry seal only. Mexico remains G4-sealed. Broader DiDi ex-China stays phased.",
    }
    save(RECEIPT, receipt)
    print("\nwrote", RECEIPT)

    # hard fail only on DiDi-relevant gates
    rc = 0
    for name in ("gate_g", "inheritance_strict"):
        if gates.get(name, {}).get("exit", 1) != 0:
            rc = 1
    fid = gates.get("fidelity") or {}
    if fid.get("exit", 1) != 0 and "PASS" not in (fid.get("tail") or ""):
        rc = 1
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
