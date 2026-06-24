#!/usr/bin/env python3
"""Shared helpers for Tasklet proposal import → Grok economics lane."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
STAGING_ROOT = ROOT / "partner-pitch" / "seal-staging"
CORRIDORS_SRC = ROOT / "finance/model/corridors.json"
RECAL = ROOT / "finance/recal"
SEAL_REPORT = ROOT / "grok-routing-output/abc-islands-seal-report.json"
ROUTING_OUTPUT = ROOT / "grok-routing-output"

# Staging node aliases → sealed canonical BP node ids (shared Curaçao mesh).
NODE_ALIASES: dict[str, str] = {
    "curacao-curacao__spanish-water-caracasbaai": "curacao-curacao__spanish-water-jan-thiel",
}

CAPTURE_ABC = 0.55
CAPEX_CARIBBEAN_COMMERCIAL = 900_000
KLEIN_CURACAO_SEASON_DAYS_DEFAULT = 120


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


def alias_node(node_id: str | None) -> str | None:
    if not node_id:
        return node_id
    return NODE_ALIASES.get(node_id, node_id)


def pair_key(a: str, b: str) -> str:
    return f"{a}|{b}"


def load_route_index(report_path: Path | None = None) -> tuple[dict[str, str], dict[str, dict]]:
    """Return (route_by_pair, route_meta_by_id) from abc-islands seal report."""
    report_path = report_path or SEAL_REPORT
    report = load_json(report_path)
    by_pair = report.get("route_by_pair") or {}
    meta: dict[str, dict] = {}
    for row in report.get("routes_built") or []:
        rid = row.get("route_id")
        if rid:
            meta[rid] = row
    return by_pair, meta


def resolve_route_id(
    from_node: str | None,
    to_node: str | None,
    route_by_pair: dict[str, str],
) -> str | None:
    a, b = alias_node(from_node), alias_node(to_node)
    if not a or not b:
        return None
    return route_by_pair.get(pair_key(a, b)) or route_by_pair.get(pair_key(b, a))


def iter_staging_corridors(staging_doc: dict) -> list[tuple[str, dict]]:
    """Yield (tier, corridor) from Tasklet staging corridor JSON."""
    out: list[tuple[str, dict]] = []
    for tier, key in (
        ("grounded", "corridors_grounded_pioneer_ii_commercial_now"),
        ("seasonal", "corridors_seasonal_amber"),
        ("roadmap", "corridors_roadmap_network_amber"),
    ):
        for c in staging_doc.get(key) or []:
            out.append((tier, c))
    return out


def normalize_bound_corridor(
    tier: str,
    raw: dict,
    route_by_pair: dict[str, str],
    route_meta: dict[str, dict],
    partner: str,
) -> dict | None:
    """Map staging corridor → finance/model/corridors.json row with sealed geometry."""
    from_id = alias_node(raw.get("proposed_from_node_id"))
    to_id = alias_node(raw.get("proposed_to_node_id"))
    rid = resolve_route_id(from_id, to_id, route_by_pair)
    if not rid:
        return None

    meta = route_meta.get(rid, {})
    l3 = dict(raw.get("L3_locals") or {})
    if l3.get("_status") == "ROADMAP_EXCLUDED":
        return None

    row: dict[str, Any] = {
        "route_id": rid,
        "from": raw.get("from"),
        "to": raw.get("to"),
        "distance_nm": raw.get("approx_distance_nm") or meta.get("distance_nm"),
        "distance_nm_verified": meta.get("distance_nm"),
        "vessel": raw.get("vessel", "Pioneer II"),
        "archetype": raw.get("archetype", "tourism"),
        "from_node_id": from_id,
        "to_node_id": to_id,
        "country": raw.get("country"),
        "pool_basis": raw.get("pool_basis", "gross"),
        "L3_locals": l3,
        "geom_verdict": "CLEAN_OPENWATER",
        "shippable": tier != "roadmap",
        "_status": "SEALED",
        "_tier": tier,
        "_bind_source": f"grok-tasklet-import/{partner}",
        "_bind_at": utc_now(),
    }
    if raw.get("render"):
        row["render"] = raw["render"]
    if tier == "roadmap" or raw.get("tier") == "roadmap":
        row["tier"] = "roadmap"
        row["_economics_excluded"] = True
    if tier == "seasonal":
        row["render"] = row.get("render") or "seasonal-amber"
    return row


def find_staging_package(package: str | Path | None) -> Path:
    if package is None:
        # Latest curacao-caribbean package or any with seal-manifest.json
        candidates = sorted(STAGING_ROOT.glob("*/seal-manifest.json"), key=lambda p: p.stat().st_mtime)
        if not candidates:
            raise FileNotFoundError(f"No seal-staging packages under {STAGING_ROOT}")
        return candidates[-1].parent
    p = Path(package)
    if not p.is_absolute():
        p = STAGING_ROOT / p if (STAGING_ROOT / p).exists() else ROOT / package
    if not (p / "seal-manifest.json").exists():
        raise FileNotFoundError(f"Missing seal-manifest.json in {p}")
    return p


def partner_staging_dir(package: Path, partner_id: str) -> Path:
    for name in (partner_id, partner_id.replace("-", "_")):
        d = package / name
        if d.is_dir():
            return d
    raise FileNotFoundError(f"No staging dir for partner {partner_id} in {package}")