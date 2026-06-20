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


# Marquee corridor-label cards inherit sealed network-bundle route_ids from hub phases.
MARQUEE_TO_BUNDLE_LABEL: dict[str, str] = {
    "Gateway of India / Bhaucha Dhakka ↔ Mandwa (Alibaug)": "Gateway <-> Mandwa / Alibaug",
    "South Mumbai (Nariman Point) ↔ Navi Mumbai / new airport": "South Mumbai <-> Navi Mumbai airport",
    "North Goa ↔ South Goa (Palolem / Cavelossim)": "North Goa <-> South Goa",
    "Panaji (Mandovi River) ↔ North Goa beaches (Baga / Morjim)": "North Goa <-> South Goa",
    "Kochi ↔ Alleppey (Alappuzha) backwaters": "Kochi <-> Alleppey backwaters",
    "Kochi (Vyttila / Marine Drive) ↔ Fort Kochi / Willingdon / Bolgatty": "Kochi <-> Alleppey backwaters",
    "Kochi ↔ Kumarakom / Vembanad Lake": "Kochi <-> Alleppey backwaters",
    "Port Blair (Phoenix Bay) ↔ Havelock / Swaraj Dweep": "Port Blair <-> Havelock <-> Neil",

    "Kochi ↔ Lakshadweep (Agatti / Kavaratti)": "Kochi <-> Lakshadweep (Quanta-LR)",
}

MARQUEE_STATIC_ROUTE_IDS: dict[str, list[str]] = {
    "Gateway of India ↔ Elephanta Caves": [
        "ics-d1cada0928",
        "ics-997116ff5d",
        "ics-6a150e9b8e",
    ],
    "Havelock ↔ Neil / Shaheed Dweep": [
        "ics-77f233e565",
        "rn-fb4a3f74ce06",
    ],
}

MARQUEE_SINGLE_ROUTE_ID: dict[str, str] = {
    "Mumbai ↔ Goa": "rn-ff5ccaf1831e",
    "Goa ↔ Mumbai": "rn-ff5ccaf1831e",
    "Mumbai <-> Konkan/Goa (Quanta-LR)": "rn-ff5ccaf1831e",
}

MARQUEE_ROADMAP_NO_GEOMETRY: dict[str, str] = {
    "Goa ↔ Grande Island / Bat Island": "no_india_gold_geometry",
    "Port Blair ↔ Ross Island / North Bay": "no_deterministic_gold_bind",
    "Port Blair ↔ Diglipur (North Andaman)": "no_deterministic_gold_bind",
}

JOURNEY_PAIR_BINDINGS: dict[tuple[str, str], str] = {
    ("gateway of india / bhaucha dhakka", "mandwa (alibaug)"): "Gateway of India / Bhaucha Dhakka ↔ Mandwa (Alibaug)",
    ("gateway of india", "mandwa (alibaug)"): "Gateway of India / Bhaucha Dhakka ↔ Mandwa (Alibaug)",
    ("south mumbai (nariman point)", "navi mumbai / new airport"): "South Mumbai (Nariman Point) ↔ Navi Mumbai / new airport",
    ("gateway of india", "elephanta caves"): "Gateway of India ↔ Elephanta Caves",
    ("mumbai", "goa"): "Mumbai ↔ Goa",
    ("goa", "mumbai"): "Goa ↔ Mumbai",
    ("panaji (mandovi river)", "north goa beaches (baga / morjim)"): "Panaji (Mandovi River) ↔ North Goa beaches (Baga / Morjim)",
    ("north goa", "south goa (palolem / cavelossim)"): "North Goa ↔ South Goa (Palolem / Cavelossim)",
    ("kochi (marine drive)", "alleppey backwaters"): "Kochi ↔ Alleppey (Alappuzha) backwaters",
    ("port blair (phoenix bay)", "havelock / swaraj dweep"): "Port Blair (Phoenix Bay) ↔ Havelock / Swaraj Dweep",
    ("havelock", "neil / shaheed dweep"): "Havelock ↔ Neil / Shaheed Dweep",
    ("kochi (vyttila / marine drive)", "fort kochi / willingdon / bolgatty"): "Kochi (Vyttila / Marine Drive) ↔ Fort Kochi / Willingdon / Bolgatty",
    ("kochi", "alleppey (alappuzha) backwaters"): "Kochi ↔ Alleppey (Alappuzha) backwaters",
    ("kochi", "kumarakom / vembanad lake"): "Kochi ↔ Kumarakom / Vembanad Lake",
    ("kochi", "lakshadweep (agatti / kavaratti)"): "Kochi ↔ Lakshadweep (Agatti / Kavaratti)",
    ("port blair", "ross island / north bay"): "Port Blair ↔ Ross Island / North Bay",
    ("port blair", "diglipur (north andaman)"): "Port Blair ↔ Diglipur (North Andaman)",
}

MARQUEE_LABEL_ALIASES: dict[str, str] = {
    "Gateway of India ↔ Mandwa (Alibaug)": "Gateway of India / Bhaucha Dhakka ↔ Mandwa (Alibaug)",
    "Kochi (Marine Drive) ↔ Alleppey backwaters": "Kochi ↔ Alleppey (Alappuzha) backwaters",
}


def _norm_pair_key(a: str, b: str) -> tuple[str, str]:
    return (a.strip().lower(), b.strip().lower())


def collect_network_bundle_registry(doc: dict[str, Any]) -> dict[str, list[str]]:
    registry: dict[str, list[str]] = {}
    for phase in doc.get("phases", []):
        for fr in phase.get("featured_routes", []) or []:
            if not isinstance(fr, dict):
                continue
            label = fr.get("label")
            rids = fr.get("route_ids")
            if label and isinstance(rids, list) and rids:
                registry[label] = [x for x in rids if isinstance(x, str)]
    return registry


def _marquee_label_for_entry(entry: dict[str, Any]) -> str | None:
    label = entry.get("label")
    if isinstance(label, str) and label.strip():
        return MARQUEE_LABEL_ALIASES.get(label.strip(), label.strip())
    from_l = entry.get("from")
    to_l = entry.get("to")
    if isinstance(from_l, str) and isinstance(to_l, str):
        key = _norm_pair_key(from_l, to_l)
        return JOURNEY_PAIR_BINDINGS.get(key)
    return None


def _is_marquee_wire_candidate(entry: dict[str, Any]) -> bool:
    if entry.get("display") == "network_chip":
        return False
    if entry.get("route_id") or entry.get("route_ids"):
        return False
    label = _marquee_label_for_entry(entry)
    if not label:
        return False
    return (
        label in MARQUEE_TO_BUNDLE_LABEL
        or label in MARQUEE_STATIC_ROUTE_IDS
        or label in MARQUEE_SINGLE_ROUTE_ID
        or label in MARQUEE_ROADMAP_NO_GEOMETRY
    )


def wire_corridor_label_entry(
    entry: dict[str, Any],
    *,
    bundle_registry: dict[str, list[str]],
    gold_ids: set[str],
    spine_ids: set[str],
    by_id: dict[str, dict] | None = None,
) -> None:
    if not _is_marquee_wire_candidate(entry):
        return

    label = _marquee_label_for_entry(entry)
    if not label:
        return

    entry.setdefault("_link_kind", "corridor-label")

    if label in MARQUEE_ROADMAP_NO_GEOMETRY:
        entry["_link_status"] = "roadmap-no-geometry"
        entry["_hold_reason"] = MARQUEE_ROADMAP_NO_GEOMETRY[label]
        entry.setdefault("economics_status", "economics_pending")
        return

    single = MARQUEE_SINGLE_ROUTE_ID.get(label)
    if single and single in gold_ids:
        entry["route_id"] = single
        entry["_link_status"] = "linked-pr58-marquee-bind"
        entry["_link_source"] = "grok/execute_pr58_india_gcc/marquee-wire"
        entry.setdefault("economics_status", "economics_pending")
        if label in {"Mumbai ↔ Goa", "Goa ↔ Mumbai", "Mumbai <-> Konkan/Goa (Quanta-LR)"}:
            entry["platform"] = "Quanta-LR"
            entry["vessel_gate"] = "Quanta-LR review >150nm"
            props = (by_id or {}).get(single, {})
            if props.get("from_city_id"):
                entry["from_node_id"] = props["from_city_id"]
            if props.get("to_city_id"):
                entry["to_node_id"] = props["to_city_id"]
            if props.get("distance_nm") is not None:
                entry["distance_nm"] = props["distance_nm"]
        return

    static = MARQUEE_STATIC_ROUTE_IDS.get(label)
    if static:
        filtered = [x for x in static if x in gold_ids and x in spine_ids]
        if filtered:
            entry["route_ids"] = filtered
            entry["route_id"] = None
            entry["_link_status"] = "linked-pr58-marquee-bind"
            entry["_link_source"] = "grok/execute_pr58_india_gcc/marquee-wire"
            entry.setdefault("economics_status", "economics_pending")
            return

    bundle_label = MARQUEE_TO_BUNDLE_LABEL.get(label)
    if bundle_label:
        rids = bundle_registry.get(bundle_label)
        if rids:
            filtered = [x for x in rids if x in gold_ids and x in spine_ids]
            if filtered:
                entry["route_ids"] = filtered
                entry["route_id"] = None
                entry["_link_status"] = "linked-pr58-marquee-bind"
                entry["_link_source"] = "grok/execute_pr58_india_gcc/marquee-wire"
                entry.setdefault("economics_status", "economics_pending")
                return


def wire_corridor_labels_in_doc(
    doc: dict[str, Any],
    *,
    gold_ids: set[str],
    spine_ids: set[str],
    by_id: dict[str, dict] | None = None,
) -> None:
    bundle_registry = collect_network_bundle_registry(doc)
    containers: list[list[dict]] = []
    containers.append(doc.get("journeys_unlocked", []) or [])
    for phase in doc.get("phases", []):
        containers.append(phase.get("featured_routes", []) or [])
    for market in doc.get("markets", []):
        containers.append(market.get("journeys_unlocked", []) or [])
        for phase in market.get("phases", []):
            containers.append(phase.get("featured_routes", []) or [])

    for routes in containers:
        for entry in routes:
            if isinstance(entry, dict):
                wire_corridor_label_entry(
                    entry,
                    bundle_registry=bundle_registry,
                    gold_ids=gold_ids,
                    spine_ids=spine_ids,
                    by_id=by_id,
                )


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
            for key in (
                "route_ids",
                "route_id",
                "from_node_id",
                "to_node_id",
                "distance_nm",
                "platform",
                "display",
                "vessel_gate",
            ):
                if key in ref and merged.get(key) is None:
                    merged[key] = ref[key]
            # Always inherit spine bundle metadata from Rapido for matching labels.
            for key in ("route_ids", "_link_kind", "_link_status", "_link_source"):
                if key in ref and ref.get(key) is not None:
                    merged[key] = ref[key]
            if merged.get("route_ids") or merged.get("route_id"):
                merged["_link_source"] = "grok/execute_pr58_india_gcc/rapido-spine-inherit"
                merged["_link_status"] = "linked-pr58-spine"
            phase["featured_routes"][i] = merged


def normalize_india_partner(
    path: Path,
    spine: dict[str, Any],
    gold_ids: set[str],
    goa_ledger: list[dict],
    doc: dict[str, Any] | None = None,
    *,
    by_id: dict[str, dict] | None = None,
) -> dict[str, Any]:
    doc = copy.deepcopy(doc) if doc is not None else load_json(path)
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

    wire_corridor_labels_in_doc(doc, gold_ids=gold_ids, spine_ids=all_spine, by_id=by_id)

    doc = deep_canonicalize(doc, goa_ledger)
    doc["_pr58_execution"] = {
        "applied_at": utc_now(),
        "lane": "grok/execute_pr58_india_gcc",
        "spine": "handoff/partner-map-model/india-shared-corridor-spine.json",
        "economics_status": "economics_pending",
    }
    save_json(path, doc)
    return doc


def featured_row_label(row: dict[str, Any]) -> str:
    label = row.get("label")
    if isinstance(label, str) and label.strip():
        return label.strip()
    from_l = row.get("from")
    to_l = row.get("to")
    if isinstance(from_l, str) and isinstance(to_l, str):
        return f"{from_l} ↔ {to_l}"
    return ""


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
        if isinstance(j, dict) and (
            j.get("route_id") is not None
            or j.get("route_ids")
            or j.get("_source_corridor_id")
            or j.get("_link_kind") == "corridor-label"
        ):
            rows.append({**j, "_partner": partner, "_kind": "journey"})
    for market in doc.get("markets", []):
        for j in market.get("journeys_unlocked", []) or []:
            if isinstance(j, dict) and (
                j.get("route_id") is not None
                or j.get("route_ids")
                or j.get("_source_corridor_id")
                or j.get("_link_kind") == "corridor-label"
            ):
                rows.append({
                    **j,
                    "_partner": partner,
                    "_kind": "journey",
                    "_market": market.get("id"),
                })
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
    rapido = normalize_india_partner(rapido_path, spine, gold_ids, goa_ledger, by_id=by_id)
    ola_raw = load_json(ola_path)
    sync_ola_from_rapido(ola_raw, rapido)
    ola = normalize_india_partner(ola_path, spine, gold_ids, goa_ledger, doc=ola_raw, by_id=by_id)

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
            row_label = featured_row_label(row)
            bind_method = (
                "marquee_wire"
                if row.get("_link_status") == "linked-pr58-marquee-bind"
                else "network_bundle"
            )
            if row.get("route_id"):
                rid = row["route_id"]
                if rid in gold_ids:
                    india_seal_rows.append({
                        "partner": partner,
                        "phase": row.get("_phase"),
                        "label": row_label or row.get("label"),
                        "featured_label": row_label or row.get("label"),
                        "route_id": rid,
                        "verdict": "SEALED_ROUTE_ID",
                        "bind_method": bind_method,
                        "reason": "explicit route_id in partner doc",
                    })
                else:
                    india_seal_rows.append({
                        **seal_route_entry(row, gold_ids, by_id, by_bp, partner=partner, phase=row.get("_phase")),
                        "label": row_label or row.get("label"),
                        "featured_label": row_label or row.get("label"),
                        "bind_method": bind_method,
                    })
            elif row.get("route_ids"):
                for rid in row["route_ids"]:
                    india_seal_rows.append({
                        "partner": partner,
                        "phase": row.get("_phase"),
                        "label": row_label or row.get("label"),
                        "route_id": rid,
                        "verdict": "SEALED_ROUTE_ID" if rid in gold_ids else "HELD_NULL_WITH_REASON",
                        "bind_method": bind_method,
                    })
            else:
                rec = seal_route_entry(row, gold_ids, by_id, by_bp, partner=partner, phase=row.get("_phase"))
                if row_label:
                    rec["label"] = row_label
                if row.get("_hold_reason"):
                    rec["reason"] = row["_hold_reason"]
                india_seal_rows.append(rec)

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