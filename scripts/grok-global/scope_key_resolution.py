"""Pass 4 scope-key resolution — view parity for partner map inheritance."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
PASS4 = ROOT / "handoff" / "yango-program" / "pass4"

YANGO_LOCKED_CLUSTERS = frozenset({"turkey", "ksa-commercial", "norway", "bolt-ksa-commercial"})
SKIP_PARTNERS_PENDING_CONFIRM = frozenset()

COMMERCIAL_PARTNERS = (
    "airasia-move",
    "bolt",
    "cabify",
    "careem",
    "didi",
    "gojek",
    "grab",
    "grab-thailand",
    "indrive",
    "kakao-mobility",
    "line",
    "line-man-wongnai",
    "lyft",
    "noon",
    "ola",
    "rapido",
    "uber",
    "uber-india",
    "yango",
    "yassir",
)


@dataclass
class Resolution:
    key: str
    status: str  # cluster-direct | city-member | normalize | unsealed-registered | aspirational | dropped
    resolves_to: str | None = None
    cluster_id: str | None = None
    city_ids: list[str] = field(default_factory=list)
    note: str = ""


def spell_norm(key: str) -> str:
    return key.replace("_", "-").lower().strip()


def load_pass4_artifacts() -> dict[str, Any]:
    def read(name: str) -> dict:
        p = PASS4 / name
        return json.loads(p.read_text()) if p.exists() else {}

    alias_doc = read("P4-ALIAS-MAP.json")
    city_doc = read("P4-CITY-MEMBER-MAP.json")
    prefix_doc = read("P4-PREFIX-JUNK.json")
    unknown_doc = read("P4-UNKNOWN-DROP.json")
    locked_doc = read("P4-YANGO-LOCKED-NON-MARKETS.json")
    return {
        "aliases": alias_doc.get("aliases") or {},
        "city_member": city_doc.get("mappings") or {},
        "prefix_junk": {e["key"] for e in (prefix_doc.get("entries") or [])},
        "unknown_drop": {e["key"] for e in (unknown_doc.get("entries") or [])},
        "yango_locked": set(locked_doc.get("locked") or []),
    }


def load_geometry_index(
    dc_root: Path | None = None,
) -> tuple[set[str], set[str], dict[str, str], dict[str, set[str]], dict[str, dict]]:
    dc = dc_root or (ROOT / "data-clean")
    clusters_raw = json.loads((dc / "CLUSTERS.json").read_text())
    clusters = {c["cluster_id"]: c for c in clusters_raw.get("clusters") or []}
    city_to_cluster: dict[str, str] = {}
    cluster_cities: dict[str, set[str]] = {}
    for c in clusters_raw.get("clusters") or []:
        cid = c["cluster_id"]
        members = set(c.get("member_city_ids") or [])
        cluster_cities[cid] = members
        for mid in members:
            city_to_cluster[mid] = cid

    routes = json.loads((dc / "ROUTES.json").read_text())
    stamped_clusters: set[str] = set()
    route_cities: set[str] = set()
    for feat in routes:
        p = feat.get("properties") or {}
        if p.get("cluster_id"):
            stamped_clusters.add(p["cluster_id"])
        if p.get("from_city_id"):
            route_cities.add(p["from_city_id"])
        if p.get("to_city_id"):
            route_cities.add(p["to_city_id"])

    return stamped_clusters, route_cities, city_to_cluster, cluster_cities, clusters


def _resolve_direct(work: str, *, clusters: dict[str, dict], cluster_cities: dict[str, set[str]]) -> Resolution | None:
    if work in clusters:
        return Resolution(
            work,
            "cluster-direct",
            resolves_to=work,
            cluster_id=work,
            city_ids=sorted(cluster_cities.get(work, set())),
        )
    return None


def _resolve_city_member(
    work: str,
    *,
    city_to_cluster: dict[str, str],
    artifacts: dict[str, Any],
    clusters: dict[str, dict],
    cluster_cities: dict[str, set[str]],
    stamped_clusters: set[str],
    route_cities: set[str],
) -> Resolution | None:
    if work in city_to_cluster:
        cid = city_to_cluster[work]
        return Resolution(work, "city-member", resolves_to=work, cluster_id=cid, city_ids=[work])

    if work not in artifacts["city_member"]:
        return None

    target = artifacts["city_member"][work]
    if target in clusters:
        return Resolution(
            work,
            "city-member",
            resolves_to=target,
            cluster_id=target,
            city_ids=sorted(cluster_cities.get(target, set())),
            note=f"shorthand→cluster {target}",
        )
    if target in city_to_cluster:
        cid = city_to_cluster[target]
        return Resolution(
            work,
            "city-member",
            resolves_to=target,
            cluster_id=cid,
            city_ids=[target],
            note=f"shorthand→city {target}",
        )
    if target in stamped_clusters or target in route_cities:
        return Resolution(
            work,
            "unsealed-registered",
            resolves_to=target,
            cluster_id=target if target in stamped_clusters else None,
            city_ids=[target] if target in route_cities else [],
            note=f"shorthand→unsealed {target}",
        )
    return None


def _resolve_classify(
    work: str,
    *,
    stamped_clusters: set[str],
    route_cities: set[str],
    clusters: dict[str, dict],
    cluster_cities: dict[str, set[str]],
    city_to_cluster: dict[str, str],
) -> Resolution:
    if work in stamped_clusters:
        return Resolution(
            work,
            "unsealed-registered",
            resolves_to=work,
            cluster_id=work,
            note="cluster_id in ROUTES, not in CLUSTERS.json",
        )
    if work in route_cities:
        return Resolution(
            work,
            "unsealed-registered",
            resolves_to=work,
            city_ids=[work],
            note="city_id in ROUTES, not in CLUSTERS.json",
        )

    sn = spell_norm(work)
    if sn != work:
        if sn in clusters:
            return Resolution(
                work,
                "normalize",
                resolves_to=sn,
                cluster_id=sn,
                city_ids=sorted(cluster_cities.get(sn, set())),
                note="spell-normalized cluster",
            )
        if sn in city_to_cluster:
            cid = city_to_cluster[sn]
            return Resolution(
                work,
                "normalize",
                resolves_to=sn,
                cluster_id=cid,
                city_ids=[sn],
                note="spell-normalized city",
            )

    return Resolution(work, "dropped", note="unresolved — drop")


def resolve_key(
    key: str,
    *,
    artifacts: dict[str, Any],
    stamped_clusters: set[str],
    route_cities: set[str],
    city_to_cluster: dict[str, str],
    cluster_cities: dict[str, set[str]],
    clusters: dict[str, dict],
) -> Resolution:
    """Ordered: hygiene → direct → city-member → normalize → classify."""
    if key in artifacts["prefix_junk"]:
        return Resolution(key, "dropped", note="partner-prefix junk")
    if key in artifacts["unknown_drop"]:
        return Resolution(key, "dropped", note="unknown key — no geometry")

    work = key

    direct = _resolve_direct(work, clusters=clusters, cluster_cities=cluster_cities)
    if direct:
        return Resolution(key, direct.status, resolves_to=direct.resolves_to, cluster_id=direct.cluster_id, city_ids=direct.city_ids)

    city = _resolve_city_member(
        work,
        city_to_cluster=city_to_cluster,
        artifacts=artifacts,
        clusters=clusters,
        cluster_cities=cluster_cities,
        stamped_clusters=stamped_clusters,
        route_cities=route_cities,
    )
    if city:
        return Resolution(
            key,
            city.status,
            resolves_to=city.resolves_to,
            cluster_id=city.cluster_id,
            city_ids=city.city_ids,
            note=city.note,
        )

    alias_target = artifacts["aliases"].get(work) or artifacts["aliases"].get(spell_norm(work))
    if alias_target and alias_target != work:
        inner = resolve_key(
            alias_target,
            artifacts=artifacts,
            stamped_clusters=stamped_clusters,
            route_cities=route_cities,
            city_to_cluster=city_to_cluster,
            cluster_cities=cluster_cities,
            clusters=clusters,
        )
        if inner.status != "dropped":
            return Resolution(
                key,
                "normalize",
                resolves_to=alias_target,
                cluster_id=inner.cluster_id,
                city_ids=inner.city_ids,
                note=f"alias→{alias_target}",
            )

    classified = _resolve_classify(
        work,
        stamped_clusters=stamped_clusters,
        route_cities=route_cities,
        clusters=clusters,
        cluster_cities=cluster_cities,
        city_to_cluster=city_to_cluster,
    )
    return Resolution(
        key,
        classified.status,
        resolves_to=classified.resolves_to,
        cluster_id=classified.cluster_id,
        city_ids=classified.city_ids,
        note=classified.note,
    )


def expanded_city_ids(resolutions: list[Resolution]) -> set[str]:
    out: set[str] = set()
    for r in resolutions:
        if r.status == "dropped":
            continue
        out.update(r.city_ids)
    return out


def expanded_cluster_ids(resolutions: list[Resolution]) -> set[str]:
    out: set[str] = set()
    for r in resolutions:
        if r.status == "dropped":
            continue
        if r.cluster_id:
            out.add(r.cluster_id)
        if r.resolves_to and r.resolves_to in {r.cluster_id}:
            out.add(r.resolves_to)
    return out


def canonical_registry_key(resolution: Resolution) -> str | None:
    if resolution.status == "dropped":
        return None
    if resolution.status in ("cluster-direct", "unsealed-registered"):
        return resolution.resolves_to or resolution.key
    if resolution.cluster_id:
        return resolution.cluster_id
    if resolution.resolves_to:
        return resolution.resolves_to
    return resolution.key


def check_yango_locked(partner_id: str, resolutions: list[Resolution], artifacts: dict[str, Any]) -> list[str]:
    if partner_id != "yango":
        return []
    errors: list[str] = []
    locked = artifacts["yango_locked"] | YANGO_LOCKED_CLUSTERS
    for r in resolutions:
        if r.status == "dropped":
            continue
        targets = {r.resolves_to, r.cluster_id} - {None}
        for t in targets:
            base = t
            if base in artifacts["aliases"]:
                base = artifacts["aliases"][base]
            if base in locked or base in YANGO_LOCKED_CLUSTERS:
                errors.append(f"{r.key} resolves to locked non-market '{base}'")
            if (base == "turkey" or base.endswith("-turkey")) and base != "bodrum-turkey":
                if "turkey" in locked or base.startswith("yango-"):
                    errors.append(f"{r.key} → Turkey blocked")
    return errors


def geometry_for_resolution(
    resolution: Resolution,
    *,
    stamped_clusters: set[str],
    route_cities: set[str],
    cluster_cities: dict[str, set[str]],
) -> set[str]:
    """City ids with sealed geometry reachable from this resolution."""
    if resolution.status == "dropped":
        return set()
    out: set[str] = set()
    if resolution.cluster_id and resolution.cluster_id in cluster_cities:
        out.update(cluster_cities[resolution.cluster_id])
    out.update(resolution.city_ids)
    out = {c for c in out if c in route_cities}
    if resolution.cluster_id and resolution.cluster_id in stamped_clusters:
        # cluster stamped in routes — member cities may inherit via cluster_id match
        out.update(cluster_cities.get(resolution.cluster_id, set()))
    return out