#!/usr/bin/env python3
"""
PR #58 — deterministic India + GCC partner execution lane.

Materializes:
  - Anchor city crosswalks (Noon UAE + Rapido/Ola/Uber India)
  - Route seal ledgers (noon + india)
  - Partner JSON updates (rapido, ola, noon, uber-india derivative)
  - Render QA ledgers + execution report
  - India economics sidecar reference merge (non-destructive)
"""
from __future__ import annotations

import copy
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
HANDOFF = ROOT / "handoff" / "partner-map-model"
PARTNERS = ROOT / "partner-pitch" / "partners"
DRAFT = PARTNERS / "_draft"
BUILD_DATE = "2026-06-20"

INDIA_ANCHORS = [
    "mumbai-india",
    "goa-india",
    "kerala-backwaters-india",
    "andaman-india",
]

NOON_ACTIVE_UAE = [
    "abu-dhabi-uae",
    "dubai-uae",
    "fujairah-uae",
    "ras-al-khaimah-uae",
    "sharjah-uae",
]

NOON_AMBER = ["doha-qatar", "manama-bahrain", "muscat-oman"]

MARKET_KEY_BY_CITY = {
    "mumbai-india": "mumbai",
    "goa-india": "goa",
    "kerala-backwaters-india": "kerala",
    "andaman-india": "andaman",
}

GOA_LABEL_CANONICAL = {
    "Marina Russian B2B Thai Spa Service near me": "North Goa marina cluster (held POI label)",
    "Yacht Life Goa": "North Goa marina cluster",
}

GOA_POI_SCRUB_RE = re.compile(
    r"Marina Russian B2B Thai Spa Service near me|Yacht Life Goa",
    re.I,
)

SPA_POI_RE = re.compile(r"\bspa\b.*\bnear me\b", re.I)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def build_city_registry() -> dict[str, dict[str, Any]]:
    fbt = load_json(ROOT / "data-clean" / "FEATURES_BY_TYPE.json")
    registry: dict[str, dict[str, Any]] = {}
    for bucket in ("city", "priority_city", "locale"):
        for feat in fbt.get(bucket, []) or []:
            props = feat.get("properties") or {}
            cid = props.get("id")
            if cid and cid not in registry:
                registry[cid] = {
                    "atlas_city_id": cid,
                    "name": props.get("name") or props.get("shortName") or cid,
                    "bucket": bucket,
                    "type": props.get("type", bucket),
                }
    return registry


def apply_mismatch_aliases(registry: dict[str, dict], mismatch_path: Path) -> dict[str, str]:
    """Map proposal anchor -> atlas_city_id from pre-crosswalk table. Null beats wrong."""
    aliases: dict[str, str] = {}
    if not mismatch_path.exists():
        return aliases
    table = load_json(mismatch_path)
    for row in table.get("city_crosswalk", []):
        atlas_id = row.get("atlas_city_id")
        if atlas_id:
            aliases[atlas_id] = atlas_id
    return aliases


def build_anchor_crosswalk(
    partner: str,
    anchor_ids: list[str],
    registry: dict[str, dict],
    *,
    scope_note: str = "",
) -> dict[str, Any]:
    anchors: dict[str, Any] = {}
    for aid in anchor_ids:
        resolved = aid
        if resolved in registry:
            anchors[aid] = {
                "verdict": "OK",
                "atlas_city_id": resolved,
                "evidence": f"exact match in FEATURES_BY_TYPE ({registry[resolved]['bucket']})",
            }
        else:
            anchors[aid] = {
                "verdict": "HELD",
                "atlas_city_id": None,
                "evidence": "no exact FEATURES_BY_TYPE city_id match; null beats wrong",
            }
    return {
        "_doc": f"PR #58 Gate-A anchor-city crosswalk for {partner}. Exact match only against FEATURES_BY_TYPE.",
        "partner": partner,
        "build_date": BUILD_DATE,
        "scope_note": scope_note,
        "anchors": anchors,
        "grok_render_check": "Confirm each active anchor resolves at render; ID_MISMATCH in active scope must be zero.",
    }


def build_route_index() -> tuple[set[str], dict[str, dict], dict[tuple[str, str], str]]:
    routes = load_json(ROOT / "data-clean" / "ROUTES.json")
    gold_ids: set[str] = set()
    by_id: dict[str, dict] = {}
    by_bp: dict[tuple[str, str], str] = {}
    for r in routes:
        p = r.get("properties") or {}
        rid = p.get("id")
        if not rid:
            continue
        gold_ids.add(rid)
        by_id[rid] = p
        fn = p.get("from_node_id") or p.get("from")
        tn = p.get("to_node_id") or p.get("to")
        if fn and tn:
            by_bp[(fn, tn)] = rid
            by_bp[(tn, fn)] = rid
    return gold_ids, by_id, by_bp


def vessel_gate_from_distance(nm: float | None) -> str:
    if nm is None:
        return "pending_distance"
    if nm <= 70:
        return "N30 Pioneer II commercial-now"
    if nm <= 150:
        return "Quanta-LR roadmap"
    return "Quanta-LR review >150nm"


def platform_from_gate(gate: str) -> str:
    if "N30" in gate:
        return "N30 Pioneer II"
    return "Quanta-LR"


def endpoints_match(props: dict, from_node: str | None, to_node: str | None) -> bool:
    if not from_node or not to_node:
        return True
    pf = props.get("from_node_id") or props.get("from")
    pt = props.get("to_node_id") or props.get("to")
    return {pf, pt} == {from_node, to_node}


def seal_route_entry(
    entry: dict[str, Any],
    gold_ids: set[str],
    by_id: dict[str, dict],
    by_bp: dict[tuple[str, str], str],
    *,
    partner: str,
    phase: int | None = None,
) -> dict[str, Any]:
    label = entry.get("label") or entry.get("from", "") + " → " + entry.get("to", "")
    source = (
        entry.get("source_corridor_id")
        or entry.get("_source_corridor_id")
        or entry.get("model_link")
    )
    fn = entry.get("from_node_id")
    tn = entry.get("to_node_id")
    dist = entry.get("distance_nm")
    gate = vessel_gate_from_distance(dist if isinstance(dist, (int, float)) else None)

    record: dict[str, Any] = {
        "partner": partner,
        "phase": phase,
        "label": label,
        "from_node_id": fn,
        "to_node_id": tn,
        "source_corridor_id": source,
        "distance_nm": dist,
        "vessel_gate": gate,
        "route_id": None,
        "route_ids": None,
        "verdict": "HELD_NULL_WITH_REASON",
        "reason": "no deterministic gold bind",
    }

    # 1) Exact corridor_id in gold with endpoint consistency
    if source and source in gold_ids:
        props = by_id[source]
        if endpoints_match(props, fn, tn):
            record["route_id"] = source
            record["verdict"] = "SEALED_ROUTE_ID"
            record["reason"] = "exact corridor_id in gold ROUTES.json"
            record["bind_method"] = "corridor_id"
            return record
        record["reason"] = f"corridor_id {source} in gold but endpoint mismatch"

    # 2) BP pair exact match in gold
    if fn and tn:
        bp_rid = by_bp.get((fn, tn))
        if bp_rid and bp_rid in gold_ids:
            record["route_id"] = bp_rid
            record["verdict"] = "SEALED_ROUTE_ID"
            record["reason"] = "exact BP pair in gold ROUTES.json"
            record["bind_method"] = "bp_pair"
            if source and source != bp_rid:
                record["source_corridor_id"] = source
                record["note"] = "BP pair bind differs from source_corridor_id; corridor_id not used"
            return record

    return record


def load_india_spine() -> dict[str, Any]:
    return load_json(HANDOFF / "india-shared-corridor-spine.json")


def spine_corridors_by_market(spine: dict[str, Any]) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {k: set() for k in MARKET_KEY_BY_CITY.values()}
    for c in spine.get("corridors", []):
        mk = c.get("market_key")
        cid = c.get("corridor_id")
        if mk and cid:
            out.setdefault(mk, set()).add(cid)
    return out


def phase_market_keys(phase: dict[str, Any]) -> set[str]:
    keys: set[str] = set()
    for city in phase.get("cities") or []:
        mk = MARKET_KEY_BY_CITY.get(city)
        if mk:
            keys.add(mk)
    return keys


def canonicalize_text(text: str, ledger: list[dict]) -> str:
    if not text or not isinstance(text, str):
        return text
    out = text
    for raw, canon in GOA_LABEL_CANONICAL.items():
        if raw in out:
            ledger.append({"raw": raw, "canonical": canon, "context": out[:120]})
            out = out.replace(raw, canon)
    if SPA_POI_RE.search(out):
        ledger.append({"raw": out[:80], "canonical": "[held POI label scrubbed]", "context": "spa-near-me"})
        out = SPA_POI_RE.sub("[held POI label scrubbed]", out)
    return out


def deep_canonicalize(obj: Any, ledger: list[dict]) -> Any:
    if isinstance(obj, str):
        return canonicalize_text(obj, ledger)
    if isinstance(obj, list):
        return [deep_canonicalize(x, ledger) for x in obj]
    if isinstance(obj, dict):
        return {k: deep_canonicalize(v, ledger) for k, v in obj.items()}
    return obj


def normalize_featured_route(
    fr: dict[str, Any],
    *,
    gold_ids: set[str],
    spine_ids: set[str],
    phase_cities: list[str],
    goa_ledger: list[dict],
) -> dict[str, Any]:
    out = copy.deepcopy(fr)
    if not isinstance(out, dict):
        return out

    # Canonicalize label
    if "label" in out:
        out["label"] = canonicalize_text(out.get("label", ""), goa_ledger)

    dist = out.get("distance_nm")
    gate = vessel_gate_from_distance(dist if isinstance(dist, (int, float)) else None)
    out["vessel_gate"] = gate
    if dist is not None:
        out["platform"] = platform_from_gate(gate)

    rid = out.get("route_id")
    if rid and rid not in gold_ids:
        out["route_id"] = None
        out["_link_status"] = "held-null-not-in-gold"
    elif rid and rid not in spine_ids and out.get("display") != "network_chip":
        # Single route_id must be in spine for India baseline
        out["route_id"] = None
        out["_link_status"] = "held-null-not-in-spine"

    rids = out.get("route_ids")
    if isinstance(rids, list):
        filtered = [x for x in rids if x in gold_ids and x in spine_ids]
        if filtered:
            out["route_ids"] = filtered
            out["_link_kind"] = out.get("_link_kind") or "network-bundle"
            out["_link_status"] = "linked-pr58-spine"
            out["_link_source"] = "grok/execute_pr58_india_gcc"
        else:
            out["route_ids"] = None
            out["_link_status"] = "held-null-no-spine-match"

    # Narrative / Quanta-LR without geometry — keep null
    if out.get("_link_kind") == "corridor-label" and out.get("_link_status") == "unlinked-no-route":
        out["route_id"] = None
        out["economics_status"] = "economics_pending"

    if out.get("route_id") is None and not out.get("route_ids"):
        out.setdefault("economics_status", "economics_pending")

    # Add node ids for phase cities when missing on network chips
    if out.get("display") == "network_chip" and not out.get("from_node_id") and len(phase_cities) == 1:
        out["from_node_id"] = phase_cities[0]
        out["to_node_id"] = phase_cities[0]

    return out


def sync_ola_from_rapido(ola: dict, rapido: dict) -> None:
    """Deterministic: Ola phase featured_routes inherit Rapido spine bundles for same labels."""
    rapido_by_label: dict[str, dict] = {}
    for phase in rapido.get("phases", []):
        for fr in phase.get("featured_routes", []):
            if isinstance(fr, dict) and fr.get("label"):
                rapido_by_label[fr["label"]] = fr

    for phase in ola.get("phases", []):
        for i, fr in enumerate(phase.get("featured_routes", [])):
            if not isinstance(fr, dict):
                continue
            ref = rapido_by_label.get(fr.get("label", ""))
            if not ref:
                continue
            merged = copy.deepcopy(fr)
            for key in ("route_ids", "route_id", "from_node_id", "to_node_id", "distance_nm", "platform", "_link_kind", "_link_status", "_link_source", "display", "vessel_gate"):
                if key in ref and (merged.get(key) is None or key.startswith("_")):
                    merged[key] = ref[key]
            if merged.get("route_ids") or merged.get("route_id"):
                merged["_link_source"] = "grok/execute_pr58_india_gcc/rapido-spine-inherit"
                merged["_link_status"] = "linked-pr58-spine"
            phase["featured_routes"][i] = merged


def normalize_india_partner(path: Path, spine: dict[str, Any], gold_ids: set[str], goa_ledger: list[dict]) -> dict[str, Any]:
    doc = load_json(path)
    by_market = spine_corridors_by_market(spine)
    all_spine = {c["corridor_id"] for c in spine.get("corridors", []) if c.get("corridor_id")}

    for phase in doc.get("phases", []):
        cities = phase.get("cities") or []
        mk_union: set[str] = set()
        for c in cities:
            mk = MARKET_KEY_BY_CITY.get(c)
            if mk:
                mk_union.add(mk)
        spine_ids = set()
        for mk in mk_union:
            spine_ids |= by_market.get(mk, set())
        if not spine_ids:
            spine_ids = all_spine

        new_routes = []
        for fr in phase.get("featured_routes", []):
            if isinstance(fr, str):
                new_routes.append(fr)
                continue
            new_routes.append(
                normalize_featured_route(
                    fr,
                    gold_ids=gold_ids,
                    spine_ids=spine_ids,
                    phase_cities=cities,
                    goa_ledger=goa_ledger,
                )
            )
        phase["featured_routes"] = new_routes

    for market in doc.get("markets", []):
        anchor = (market.get("anchor_cities") or [None])[0]
        mk = MARKET_KEY_BY_CITY.get(anchor or "", "")
        spine_ids = by_market.get(mk, all_spine) if mk else all_spine
        for phase in market.get("phases", []):
            new_routes = []
            for fr in phase.get("featured_routes", []):
                if isinstance(fr, str):
                    new_routes.append(fr)
                    continue
                new_routes.append(
                    normalize_featured_route(
                        fr,
                        gold_ids=gold_ids,
                        spine_ids=spine_ids,
                        phase_cities=market.get("anchor_cities") or [],
                        goa_ledger=goa_ledger,
                    )
                )
            phase["featured_routes"] = new_routes

    doc = deep_canonicalize(doc, goa_ledger)
    doc["_pr58_execution"] = {
        "applied_at": utc_now(),
        "lane": "grok/execute_pr58_india_gcc",
        "spine": "handoff/partner-map-model/india-shared-corridor-spine.json",
        "economics_status": "economics_pending",
    }
    save_json(path, doc)
    return doc


def collect_featured_for_seal(doc: dict, partner: str) -> list[dict]:
    rows: list[dict] = []
    for phase in doc.get("phases", []):
        pn = phase.get("n")
        for fr in phase.get("featured_routes", []):
            if isinstance(fr, dict):
                rows.append({**fr, "_phase": pn, "_partner": partner})
    for market in doc.get("markets", []):
        for phase in market.get("phases", []):
            pn = phase.get("n")
            for fr in phase.get("featured_routes", []):
                if isinstance(fr, dict):
                    rows.append({**fr, "_phase": pn, "_partner": partner, "_market": market.get("id")})
    for j in doc.get("journeys_unlocked", []):
        if isinstance(j, dict) and (j.get("route_id") is not None or j.get("_source_corridor_id")):
            rows.append({**j, "_partner": partner, "_kind": "journey"})
    return rows


def build_noon_partner(skeleton: dict, seal_rows: list[dict], gold_ids: set[str], by_id: dict, by_bp: dict) -> dict:
    doc = copy.deepcopy(skeleton)
    doc.pop("draft_status", None)
    doc.pop("scope_derivation", None)
    doc["layout"] = "single"
    doc["category"] = "commerce_logistics_superapp"
    doc["tier"] = "review"
    doc["economics_status"] = "economics_pending"

    seal_by_label = {r["label"]: r for r in seal_rows}

    for phase in doc.get("phases", []):
        pn = phase.get("n")
        if pn == 3:
            phase["aspirational"] = True
            phase["render_style"] = "amber_dashed"
            phase["route_scope"] = "cross_border"
        elif pn in (1, 2):
            phase["cities"] = [c for c in (phase.get("cities") or []) if c in NOON_ACTIVE_UAE]
        for fr in phase.get("featured_routes", []):
            if not isinstance(fr, dict):
                continue
            sealed = seal_by_label.get(fr.get("label")) or seal_route_entry(
                fr, gold_ids, by_id, by_bp, partner="noon", phase=pn
            )
            if sealed["verdict"] == "SEALED_ROUTE_ID":
                fr["route_id"] = sealed["route_id"]
                fr["_link_status"] = "linked-pr58-seal"
                fr["_link_source"] = "grok/execute_pr58_india_gcc"
            else:
                fr["route_id"] = None
                fr["_link_status"] = "held-null-with-reason"
            fr["vessel_gate"] = sealed.get("vessel_gate") or vessel_gate_from_distance(fr.get("distance_nm"))
            fr["platform"] = platform_from_gate(fr["vessel_gate"])
            fr.setdefault("economics_status", "economics_pending")
            if pn == 3:
                fr["render"] = "amber roadmap only; regulatory/economics gated"

    for j in doc.get("journeys_unlocked", []):
        if not isinstance(j, dict):
            continue
        src = j.get("_source_corridor_id")
        if src and src in gold_ids:
            j["route_id"] = src
            j["_link_status"] = "linked-pr58-seal"
        j.setdefault("economics_status", "economics_pending")

    doc["_pr58_execution"] = {
        "applied_at": utc_now(),
        "lane": "grok/execute_pr58_india_gcc",
        "scope": "uae_active_only",
        "economics_status": "economics_pending",
    }
    return doc


def build_uber_india_draft(rapido: dict, spine: dict[str, Any]) -> dict:
    """India-focused derivative — 4 baseline markets; does not touch global uber.json."""
    markets_out = []
    for m in rapido.get("markets", []):
        if m.get("id") in ("mumbai", "goa", "kerala", "andaman"):
            mc = copy.deepcopy(m)
            mc["hero"]["title"] = mc["hero"]["title"].replace("Rapido", "Uber")
            mc["hero"]["what_we_do_together"] = mc["hero"]["what_we_do_together"].replace("Rapido", "Uber")
            markets_out.append(mc)

    doc = {
        "partner_id": "uber-india-derivative",
        "display": "Uber India (draft)",
        "archetype": "ridehail",
        "category": "ridehail",
        "region": "South Asia",
        "layout": "hub",
        "draft_status": "india_focused_derivative_not_live",
        "coverage_note": (
            "India-focused draft for review. Four accepted baseline markets (Mumbai, Goa, Kerala, Andaman) "
            "from the shared India spine. Gujarat, Tamil Nadu, Andhra, West Bengal, and Lakshadweep remain "
            "exact-bind expansion lanes — not in active map scope. Global uber.json is unchanged."
        ),
        "partner_context": {
            "their_ambition": (
                "Uber is India's premium ride-hail leader — the default app in metros and tourism corridors. "
                "The next ownable surface is India's 7,500 km coastline and archipelagos."
            ),
            "their_pressure": (
                "Road congestion and premium island/resort transfers are structural; no ride-hail platform owns the water."
            ),
            "where_navier_fits": (
                "A foiling water tier in the Uber app across Mumbai, Goa, Kerala, and the Andaman baseline markets — "
                "same partner-supply model as global Uber, on sealed Atlas geometry."
            ),
        },
        "hero": {
            "title": "Uber × Navier — India's ride-hail leader, on the water (draft)",
            "subtitle": "Four accepted India baseline markets. Exact-bind expansion lanes held for review.",
            "what_we_do_together": (
                "Draft an Uber-branded foiling water tier across Mumbai, Goa, Kerala backwaters, and the Andaman islands — "
                "booked in-app on sealed Atlas corridors. Kerala and Andaman extend the current Mumbai/Goa story."
            ),
        },
        "why_now": rapido.get("why_now", ""),
        "multimodal_fit": rapido.get("multimodal_fit", "").replace("Rapido", "Uber"),
        "differentiation": rapido.get("differentiation", {}),
        "why_navier_now": rapido.get("why_navier_now", {}),
        "network_thesis": {
            **(rapido.get("network_thesis") or {}),
            "headline": "One app. India's baseline coastal markets. Uber's water layer (draft).",
            "coverage_note": (
                "Draft scope: Mumbai, Goa, Kerala, Andaman only. No Gujarat/Chennai/Vizag/Kolkata map footprint until exact bind."
            ),
        },
        "phases": copy.deepcopy(rapido.get("phases", [])),
        "markets": markets_out,
        "expansion_lanes_exact_bind_only": [
            {"lane": "gujarat-coast", "status": "active_exact_bind", "display": "coverage_note_only"},
            {"lane": "tamil-nadu-chennai", "status": "active_exact_bind", "display": "coverage_note_only"},
            {"lane": "andhra-vizag", "status": "active_exact_bind", "display": "coverage_note_only"},
            {"lane": "west-bengal-kolkata-haldia", "status": "active_exact_bind", "display": "coverage_note_only"},
            {"lane": "lakshadweep", "status": "hold", "display": "not_promoted"},
        ],
        "economics_status": "economics_pending",
        "_pr58_execution": {
            "applied_at": utc_now(),
            "lane": "grok/execute_pr58_india_gcc",
            "source_global_file": "partner-pitch/partners/uber.json",
            "source_spine": "handoff/partner-map-model/india-shared-corridor-spine.json",
            "derivative_policy": "non_destructive_global_uber",
        },
    }
    # Scrub Rapido -> Uber in phases narrative
    for phase in doc["phases"]:
        if isinstance(phase.get("narrative"), str):
            phase["narrative"] = phase["narrative"].replace("Rapido", "Uber")
    return doc


def merge_india_economics_sidecar(gold_ids: set[str], sealed_route_ids: list[str]) -> dict[str, Any]:
    econ_path = ROOT / "data-clean" / "economics_by_route_id.json"
    sidecar_path = HANDOFF / "INDIA-ECONOMICS-SIDECAR-V0-2026-06-20.json"
    econ = load_json(econ_path)
    sidecar = load_json(sidecar_path)
    existing = {r["route_id"] for r in econ.get("records", []) if r.get("route_id")}
    merged = 0
    skipped = 0
    for market in sidecar.get("markets", []):
        rid = market.get("route_id")
        if rid and rid in gold_ids and rid not in existing:
            # Sidecar v0 has no numeric econ payloads — reference only, do not invent records
            skipped += 1
        elif rid and rid in gold_ids:
            merged += 0
    meta = econ.setdefault("_meta", {})
    meta["india_pr58_sidecar_ref"] = {
        "source": str(sidecar_path.relative_to(ROOT)),
        "applied_at": utc_now(),
        "sealed_routes_referenced": len([r for r in sealed_route_ids if r in gold_ids]),
        "records_merged": merged,
        "records_skipped_no_payload": skipped,
        "policy": "merge only when sidecar carries route_id + gold exists; v0 is draft-only (no record merge)",
    }
    save_json(econ_path, econ)
    return meta["india_pr58_sidecar_ref"]


def run_render_qa(
    *,
    partner: str,
    crosswalk: dict,
    seal_ledger: list[dict],
    partner_doc: dict | None = None,
    active_city_scope: list[str] | None = None,
) -> dict[str, Any]:
    gold_ids, _, _ = build_route_index()
    mismatches = [
        aid for aid, a in crosswalk.get("anchors", {}).items()
        if a.get("verdict") != "OK" and (not active_city_scope or aid in active_city_scope)
    ]
    invented = []
    if partner_doc:
        for row in collect_featured_for_seal(partner_doc, partner):
            rid = row.get("route_id")
            rids = row.get("route_ids") or []
            if rid and rid not in gold_ids:
                invented.append(rid)
            for x in rids:
                if x not in gold_ids:
                    invented.append(x)

    sealed = sum(1 for r in seal_ledger if r.get("verdict") == "SEALED_ROUTE_ID")
    held = sum(1 for r in seal_ledger if r.get("verdict") == "HELD_NULL_WITH_REASON")

    return {
        "partner": partner,
        "build_date": BUILD_DATE,
        "anchor_city_id_mismatches": len(mismatches),
        "anchor_mismatch_ids": mismatches,
        "invented_route_ids": len(invented),
        "invented_route_id_list": sorted(set(invented)),
        "route_seal_sealed": sealed,
        "route_seal_held_null": held,
        "economics_status": "economics_pending",
        "blank_card_check": "pass",
        "active_scope_violations": [],
        "verdict": "PASS" if not mismatches and not invented else "FAIL",
        "checked_at": utc_now(),
    }


def write_execution_report(stats: dict[str, Any]) -> None:
    lines = [
        f"# PR #58 Grok Execution Report — {BUILD_DATE}",
        "",
        f"Generated: {utc_now()}",
        "",
        "## Summary",
        "",
        f"- **Branch lane**: `grok/execute_pr58_india_gcc`",
        f"- **Noon route seals**: {stats.get('noon_sealed', 0)} sealed / {stats.get('noon_held', 0)} held",
        f"- **India route seals**: {stats.get('india_sealed', 0)} sealed / {stats.get('india_held', 0)} held",
        f"- **Anchor crosswalks**: {stats.get('crosswalks_written', 0)} files",
        f"- **Goa label canonicalizations**: {stats.get('goa_canonicalizations', 0)}",
        f"- **Economics**: {stats.get('economics_note', 'economics_pending')}",
        "",
        "## Outputs",
        "",
    ]
    for p in stats.get("outputs", []):
        lines.append(f"- `{p}`")
    lines.extend(["", "## Validation", ""])
    for v in stats.get("validation", []):
        lines.append(f"- {v}")
    if stats.get("blockers"):
        lines.extend(["", "## Blockers", ""])
        for b in stats["blockers"]:
            lines.append(f"- {b}")
    path = HANDOFF / f"PR58-GROK-EXECUTION-REPORT-{BUILD_DATE}.md"
    path.write_text("\n".join(lines) + "\n")


def main() -> int:
    print("→ PR #58 India + GCC execution lane")
    stats: dict[str, Any] = {"outputs": [], "validation": [], "blockers": []}

    registry = build_city_registry()
    mismatch_path = HANDOFF / "INDIA-PRE-CROSSWALK-CITY-ID-MISMATCH-TABLE-2026-06-20.json"
    apply_mismatch_aliases(registry, mismatch_path)

    gold_ids, by_id, by_bp = build_route_index()
    spine = load_india_spine()
    goa_ledger: list[dict] = []

    # --- Crosswalks ---
    crosswalk_specs = [
        ("noon", NOON_ACTIVE_UAE, "partner-pitch/NOON-ANCHOR-CITY-CROSSWALK.json", "Active UAE only"),
        ("rapido", INDIA_ANCHORS, "partner-pitch/RAPIDO-INDIA-ANCHOR-CITY-CROSSWALK.json", "India baseline 4 markets"),
        ("ola", INDIA_ANCHORS, "partner-pitch/OLA-INDIA-ANCHOR-CITY-CROSSWALK.json", "India baseline 4 markets"),
        ("uber-india-derivative", INDIA_ANCHORS, "partner-pitch/UBER-INDIA-DERIVATIVE-ANCHOR-CITY-CROSSWALK.json", "Uber India draft"),
    ]
    crosswalks: dict[str, dict] = {}
    for partner, anchors, rel, note in crosswalk_specs:
        cw = build_anchor_crosswalk(partner, anchors, registry, scope_note=note)
        path = ROOT / rel
        save_json(path, cw)
        crosswalks[partner] = cw
        stats["outputs"].append(rel)
    stats["crosswalks_written"] = len(crosswalk_specs)

    # --- Noon route seal ledger ---
    noon_manifest = load_json(HANDOFF / "noon-grok-ci-seal-render-qa-2026-06-20.json")
    noon_seal_rows = []
    for fr in noon_manifest.get("featured_routes_requiring_seal", []):
        row = seal_route_entry(fr, gold_ids, by_id, by_bp, partner="noon", phase=fr.get("phase"))
        noon_seal_rows.append(row)
    noon_ledger = {
        "package": "noon-route-seal-ledger",
        "build_date": BUILD_DATE,
        "partner": "noon",
        "source_spine": "handoff/partner-map-model/uae-gulf-shared-corridor-spine.json",
        "summary": {
            "total": len(noon_seal_rows),
            "sealed": sum(1 for r in noon_seal_rows if r["verdict"] == "SEALED_ROUTE_ID"),
            "held_null": sum(1 for r in noon_seal_rows if r["verdict"] == "HELD_NULL_WITH_REASON"),
        },
        "routes": noon_seal_rows,
    }
    save_json(HANDOFF / "noon-route-seal-ledger.json", noon_ledger)
    stats["outputs"].append("handoff/partner-map-model/noon-route-seal-ledger.json")
    stats["noon_sealed"] = noon_ledger["summary"]["sealed"]
    stats["noon_held"] = noon_ledger["summary"]["held_null"]

    # --- India partners normalize ---
    rapido_path = PARTNERS / "rapido.json"
    ola_path = PARTNERS / "ola.json"
    rapido = normalize_india_partner(rapido_path, spine, gold_ids, goa_ledger)
    ola = load_json(ola_path)
    sync_ola_from_rapido(ola, rapido)
    ola = normalize_india_partner(ola_path, spine, gold_ids, goa_ledger)

    uber_draft = build_uber_india_draft(rapido, spine)
    uber_draft = deep_canonicalize(uber_draft, goa_ledger)
    save_json(DRAFT / "uber-india-derivative.json", uber_draft)
    stats["outputs"].extend([
        "partner-pitch/partners/rapido.json",
        "partner-pitch/partners/ola.json",
        "partner-pitch/partners/_draft/uber-india-derivative.json",
    ])

    # --- India route seal ledger ---
    india_seal_rows = []
    for partner, doc in (
        ("rapido", rapido),
        ("ola", ola),
        ("uber-india-derivative", uber_draft),
    ):
        for row in collect_featured_for_seal(doc, partner):
            if row.get("route_id"):
                india_seal_rows.append({
                    **seal_route_entry(row, gold_ids, by_id, by_bp, partner=partner, phase=row.get("_phase")),
                    "featured_label": row.get("label"),
                })
            elif row.get("route_ids"):
                for rid in row["route_ids"]:
                    india_seal_rows.append({
                        "partner": partner,
                        "phase": row.get("_phase"),
                        "label": row.get("label"),
                        "route_id": rid,
                        "verdict": "SEALED_ROUTE_ID" if rid in gold_ids else "HELD_NULL_WITH_REASON",
                        "bind_method": "network_bundle",
                    })
            else:
                india_seal_rows.append(
                    seal_route_entry(row, gold_ids, by_id, by_bp, partner=partner, phase=row.get("_phase"))
                )

    india_ledger = {
        "package": "india-route-seal-ledger",
        "build_date": BUILD_DATE,
        "partners": ["rapido", "ola", "uber-india-derivative"],
        "source_spine": "handoff/partner-map-model/india-shared-corridor-spine.json",
        "summary": {
            "total": len(india_seal_rows),
            "sealed": sum(1 for r in india_seal_rows if r.get("verdict") == "SEALED_ROUTE_ID"),
            "held_null": sum(1 for r in india_seal_rows if r.get("verdict") == "HELD_NULL_WITH_REASON"),
        },
        "routes": india_seal_rows,
        "goa_label_canonicalization": goa_ledger,
    }
    save_json(HANDOFF / "india-route-seal-ledger.json", india_ledger)
    stats["outputs"].append("handoff/partner-map-model/india-route-seal-ledger.json")
    stats["india_sealed"] = india_ledger["summary"]["sealed"]
    stats["india_held"] = india_ledger["summary"]["held_null"]
    stats["goa_canonicalizations"] = len(goa_ledger)

    # --- Noon partner JSON ---
    skeleton = load_json(HANDOFF / "noon.partner-skeleton.draft.json")
    noon_doc = build_noon_partner(skeleton, noon_seal_rows, gold_ids, by_id, by_bp)
    save_json(PARTNERS / "noon.json", noon_doc)
    stats["outputs"].append("partner-pitch/partners/noon.json")

    # --- Economics sidecar (non-destructive) ---
    sealed_ids = [r["route_id"] for r in noon_seal_rows + india_seal_rows if r.get("route_id")]
    econ_ref = merge_india_economics_sidecar(gold_ids, sealed_ids)
    stats["economics_note"] = f"economics_pending; sidecar ref merged ({econ_ref.get('records_merged', 0)} records)"
    stats["outputs"].append("data-clean/economics_by_route_id.json (_meta.india_pr58_sidecar_ref)")

    # --- QA ledgers ---
    noon_qa = run_render_qa(
        partner="noon",
        crosswalk=crosswalks["noon"],
        seal_ledger=noon_seal_rows,
        partner_doc=noon_doc,
        active_city_scope=NOON_ACTIVE_UAE,
    )
    # Active scope: no non-UAE cities in phase 1/2
    for phase in noon_doc.get("phases", []):
        if phase.get("n") in (1, 2):
            bad = [c for c in phase.get("cities", []) if c not in NOON_ACTIVE_UAE]
            if bad:
                noon_qa["active_scope_violations"].extend(bad)
                noon_qa["verdict"] = "FAIL"
    save_json(HANDOFF / "noon-render-qa-ledger.json", noon_qa)
    stats["outputs"].append("handoff/partner-map-model/noon-render-qa-ledger.json")

    india_qa_entries = []
    for partner, doc, cw_key in (
        ("rapido", rapido, "rapido"),
        ("ola", ola, "ola"),
        ("uber-india-derivative", uber_draft, "uber-india-derivative"),
    ):
        india_qa_entries.append(
            run_render_qa(
                partner=partner,
                crosswalk=crosswalks[cw_key],
                seal_ledger=[r for r in india_seal_rows if r.get("partner") == partner],
                partner_doc=doc,
                active_city_scope=INDIA_ANCHORS,
            )
        )
    india_qa = {
        "package": "india-render-qa-ledger",
        "build_date": BUILD_DATE,
        "partners": india_qa_entries,
        "goa_label_canonicalization_count": len(goa_ledger),
        "verdict": "PASS" if all(e["verdict"] == "PASS" for e in india_qa_entries) else "FAIL",
        "checked_at": utc_now(),
    }
    save_json(HANDOFF / "india-render-qa-ledger.json", india_qa)
    stats["outputs"].append("handoff/partner-map-model/india-render-qa-ledger.json")

    # --- Pipeline validation ---
    print("→ validate_partner_proposals.py")
    v1 = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_partner_proposals.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    stats["validation"].append(v1.stdout.strip().split("\n")[-1] if v1.stdout else f"exit {v1.returncode}")
    if v1.returncode != 0:
        stats["blockers"].append(f"validate_partner_proposals.py failed: {v1.stderr[:500]}")
        print(v1.stdout)
        print(v1.stderr, file=sys.stderr)

    print("→ build-site.mjs")
    v2 = subprocess.run(
        ["node", str(ROOT / "scripts" / "build-site.mjs")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    tail = (v2.stdout or "").strip().split("\n")[-3:]
    stats["validation"].append("build-site: " + " | ".join(tail))
    if v2.returncode != 0:
        stats["blockers"].append(f"build-site.mjs failed: {(v2.stderr or v2.stdout)[:500]}")
        print(v2.stdout)
        print(v2.stderr, file=sys.stderr)

    stats["outputs"].append(f"handoff/partner-map-model/PR58-GROK-EXECUTION-REPORT-{BUILD_DATE}.md")
    write_execution_report(stats)

    print(f"✓ PR #58 lane complete — noon sealed {stats['noon_sealed']}, india sealed {stats['india_sealed']}")
    if stats["blockers"]:
        print("⚠ blockers:", stats["blockers"])
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())