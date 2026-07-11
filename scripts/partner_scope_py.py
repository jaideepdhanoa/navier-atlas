"""Python mirror of scripts/partner-scope.mjs for validation / apply gates."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

MARKET_CLUSTER_ALIASES: dict[str, str] = {
    "bali": "indonesia",
    "jakarta": "indonesia",
    "phuket": "thailand",
    "bangkok": "thailand",
    "koh-samui": "thailand",
    "penang": "malaysia",
    "cross-border": "__cross_border__",
}


def load_clusters(dc_root: Path | None = None) -> tuple[list[dict], dict[str, dict], dict[str, str]]:
    dc = dc_root or (ROOT / "data-clean")
    raw = json.loads((dc / "CLUSTERS.json").read_text())
    clusters = raw.get("clusters") or []
    by_id = {c["cluster_id"]: c for c in clusters}
    city_to_cluster: dict[str, str] = {}
    for c in clusters:
        for cid in c.get("member_city_ids") or []:
            city_to_cluster[cid] = c["cluster_id"]
    return clusters, by_id, city_to_cluster


def is_hub_partner(partner: dict[str, Any]) -> bool:
    return (partner.get("layout") in ("hub", "network")) and bool(partner.get("markets"))


def sealed_registry_keys(partner: dict[str, Any]) -> set[str]:
    keys: set[str] = set()
    for m in partner.get("markets") or []:
        scoped = m.get("scope_registry_keys") or m.get("scope_registry_key") or []
        scoped = scoped if isinstance(scoped, list) else [scoped]
        scoped = [k for k in scoped if k]
        if scoped:
            keys.update(scoped)
        else:
            if m.get("slug"):
                keys.add(m["slug"])
            if m.get("id"):
                keys.add(m["id"])
    for fp in partner.get("network_footprint") or []:
        if fp.get("covered") is not True:
            continue
        scoped = fp.get("scope_registry_keys") or fp.get("scope_registry_key") or []
        scoped = scoped if isinstance(scoped, list) else [scoped]
        scoped = [k for k in scoped if k]
        if scoped:
            keys.update(scoped)
        else:
            keys.add(fp.get("registry_key") or fp.get("id"))
    for k in partner.get("_map_scope", {}).get("registry_keys") or []:
        keys.add(k)
    return {k for k in keys if k}


def cross_border_city_ids(cluster_by_id: dict[str, dict], partner: dict[str, Any] | None = None) -> set[str]:
    narrow = (partner or {}).get("_map_scope", {}).get("cross_border_city_ids")
    if isinstance(narrow, list) and narrow:
        return set(narrow)
    out = {"riau-islands-indonesia", "desaru-coast-malaysia", "langkawi-malaysia"}
    for cid in ("singapore", "malaysia"):
        c = cluster_by_id.get(cid)
        if c:
            out.update(c.get("member_city_ids") or [])
    return out


def resolve_registry_key_to_city_ids(
    key: str,
    cluster_by_id: dict[str, dict],
    partner: dict[str, Any] | None = None,
) -> set[str]:
    alias = MARKET_CLUSTER_ALIASES.get(key)
    if alias == "__cross_border__":
        return cross_border_city_ids(cluster_by_id, partner)
    cluster_id = alias or key
    cluster = cluster_by_id.get(cluster_id)
    if cluster and cluster.get("member_city_ids"):
        return set(cluster["member_city_ids"])
    if "-" in key or cluster_id in cluster_by_id:
        c2 = cluster_by_id.get(cluster_id)
        if c2:
            return set(c2.get("member_city_ids") or [])
        return {key}
    return set()


def market_cities(market: dict[str, Any]) -> list[str]:
    out: list[str] = []
    out.extend(market.get("anchor_cities") or [])
    for ph in market.get("phases") or []:
        out.extend(ph.get("cities") or [])
    return out


def resolve_inherited_city_ids(
    partner: dict[str, Any],
    cluster_by_id: dict[str, dict],
    *,
    page_kind: str = "hub-index",
    market: dict[str, Any] | None = None,
) -> set[str]:
    out: set[str] = set()
    if not is_hub_partner(partner):
        return out
    if page_kind == "market" and market:
        scoped = market.get("scope_registry_keys") or market.get("scope_registry_key") or []
        scoped = scoped if isinstance(scoped, list) else [scoped]
        keys = [k for k in scoped if k] or [market.get("slug") or market.get("id")]
        out.update(market_cities(market))
        for key in keys:
            if key:
                out.update(resolve_registry_key_to_city_ids(key, cluster_by_id, partner))
        return out
    if page_kind == "hub-index":
        for key in sealed_registry_keys(partner):
            out.update(resolve_registry_key_to_city_ids(key, cluster_by_id, partner))
        out.update(partner.get("end_state", {}).get("end_state_cities") or [])
    return out


def hub_rollout_cities(
    partner: dict[str, Any],
    cluster_by_id: dict[str, dict],
    *,
    page_kind: str = "hub-index",
    market: dict[str, Any] | None = None,
) -> list[str]:
    if page_kind == "market" and market:
        from_markets = market_cities(market)
    else:
        from_markets = []
        for m in partner.get("markets") or []:
            from_markets.extend(market_cities(m))
    inherited = list(resolve_inherited_city_ids(partner, cluster_by_id, page_kind=page_kind, market=market))
    if page_kind == "hub-index":
        legacy = partner.get("_map_scope", {}).get("cluster_city_ids") or []
        return sorted(set(from_markets) | set(inherited) | set(legacy))
    return sorted(set(from_markets) | set(inherited))


def partner_scope_city_ids(partner: dict[str, Any], cluster_by_id: dict[str, dict]) -> set[str]:
    """Authoritative city scope for inheritance gates."""
    stored = set(partner.get("_map_scope", {}).get("cluster_city_ids") or [])
    if stored:
        return stored
    if is_hub_partner(partner):
        return set(hub_rollout_cities(partner, cluster_by_id))
    out: set[str] = set()
    out.update(partner.get("end_state", {}).get("end_state_cities") or [])
    for ph in partner.get("phases") or []:
        out.update(ph.get("cities") or [])
    for m in partner.get("markets") or []:
        out.update(m.get("anchor_cities") or [])
        for ph in m.get("phases") or []:
            out.update(ph.get("cities") or [])
    return out


def partner_cluster_ids(city_ids: set[str], city_to_cluster: dict[str, str]) -> set[str]:
    out = {city_to_cluster[c] for c in city_ids if c in city_to_cluster}
    # registry keys that are themselves cluster ids
    for c in city_ids:
        if c in city_to_cluster.values():
            out.add(c)
    return out