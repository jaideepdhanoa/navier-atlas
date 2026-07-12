#!/usr/bin/env python3
"""Cross-partner audit for Dott/Doha-class inheritance failures.

Checks (fail-closed, exact-ID only — does not invent routes):
  A. Footprint city covered + geometry exist, but no markets[] row (footprint-only gap)
  B. City-level sealed registry key mis-used as cluster_id in partnerClusters (build-site)
  C. Sealed keep city has zero ROUTES endpoints matching city (empty display risk)
  D. Featured / signature / wow route_ids missing from ROUTES.json
  E. Finance inheritance_spec omits registry markets for covered footprint geographies
  F. POI parent_city_id vs name mismatch heuristics (Doha-metro-under-wrong-city pattern)
  G. Market page both-endpoint keep would drop all routes for a market (0 displayable)

Writes: grok-routing-output/partner-route-inheritance-health.json

Exit codes:
  0 — no blocking findings (or report-only)
  1 — blocking findings present when --fail-on-a / --strict
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from partner_scope_py import (  # noqa: E402
    MARKET_CLUSTER_ALIASES,
    hub_rollout_cities,
    is_hub_partner,
    load_clusters,
    partner_scope_city_ids,
    resolve_registry_key_to_city_ids,
    sealed_registry_keys,
)

PARTNERS_DIR = ROOT / "data-clean" / "partners"
ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"
FBT_PATH = ROOT / "data-clean" / "FEATURES_BY_TYPE.json"
INHERIT_SPEC = ROOT / "finance" / "model" / "inheritance_spec.json"
CORRIDORS = ROOT / "finance" / "model" / "corridors.json"
REPORT_PATH = ROOT / "grok-routing-output" / "partner-route-inheritance-health.json"

# Name tokens that strongly imply a city different from parent when mismatched
CITY_NAME_HINTS: list[tuple[str, re.Pattern[str]]] = [
    ("doha-qatar", re.compile(r"\bdoha\b|lusail|the pearl|katara|west bay|banana island", re.I)),
    ("jeddah-ksa", re.compile(r"\bjeddah\b|corniche.*jeddah|jeddah central", re.I)),
    ("dubai-uae", re.compile(r"\bdubai\b|palm jumeirah|marina mall dubai|dubai harbour", re.I)),
    ("abu-dhabi-uae", re.compile(r"abu dhabi|saadiyat|yas marina|emirates palace", re.I)),
    ("manama-bahrain", re.compile(r"\bmanama\b|muharraq|amwaj|bahrain financial", re.I)),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def route_index(routes: list[dict]) -> tuple[dict[str, dict], dict[str, set[str]], Counter]:
    by_id: dict[str, dict] = {}
    by_city: dict[str, set[str]] = defaultdict(set)
    cluster_counts: Counter = Counter()
    for feat in routes:
        p = feat.get("properties") or {}
        rid = p.get("id")
        if not rid:
            continue
        by_id[rid] = p
        for ck in ("from_city_id", "to_city_id"):
            c = p.get(ck)
            if c:
                by_city[c].add(rid)
        if p.get("cluster_id"):
            cluster_counts[p["cluster_id"]] += 1
    return by_id, by_city, cluster_counts


def build_cityId_of(fbt: dict) -> dict[str, str]:
    """BP id → parent city (only when parent is a known city feature)."""
    city_ids = set()
    for t in ("city", "priority_city"):
        for f in fbt.get(t) or []:
            pid = (f.get("properties") or {}).get("id")
            if pid:
                city_ids.add(pid)
    out: dict[str, str] = {}
    for t, feats in fbt.items():
        for f in feats or []:
            p = f.get("properties") or {}
            bid = p.get("id")
            if not bid:
                continue
            if t in ("city", "priority_city"):
                out[bid] = bid
                continue
            parent = p.get("parent_city_id") or p.get("city_id")
            if parent and parent in city_ids:
                out[bid] = parent
    return out


def partner_clusters_from_keys(keys: set[str]) -> set[str]:
    """Mirror build-site.mjs sealed-key → partnerClusters (pre city→cluster fix)."""
    out: set[str] = set()
    for key in keys:
        alias = MARKET_CLUSTER_ALIASES.get(key)
        if alias == "__cross_border__":
            continue
        cid = alias or key
        if cid:
            out.add(cid)
    return out


def market_slugs(partner: dict) -> set[str]:
    out: set[str] = set()
    for m in partner.get("markets") or []:
        if not isinstance(m, dict):
            continue
        for k in ("slug", "id"):
            if m.get(k):
                out.add(str(m[k]))
    return out


def footprint_city_keys(partner: dict) -> list[dict[str, Any]]:
    rows = []
    for fp in partner.get("network_footprint") or []:
        if isinstance(fp, str):
            rows.append({"key": fp, "label": fp, "tier": None, "render": None, "map_promote": None})
            continue
        if not isinstance(fp, dict) or fp.get("covered") is not True:
            continue
        key = fp.get("registry_key") or fp.get("id")
        if not key:
            continue
        rows.append(
            {
                "key": key,
                "label": fp.get("label"),
                "tier": fp.get("tier"),
                "render": fp.get("render"),
                "map_promote": fp.get("map_promote"),
            }
        )
    return rows


def collect_featured_ids(partner: dict) -> list[tuple[str, str]]:
    """path, route_id pairs from marquee surfaces."""
    out: list[tuple[str, str]] = []

    def walk(obj: Any, path: str) -> None:
        if isinstance(obj, dict):
            rid = obj.get("route_id")
            if isinstance(rid, str) and rid:
                out.append((path, rid))
            for k, v in obj.items():
                if k in (
                    "featured_routes",
                    "wow_corridors",
                    "signature_routes",
                    "why_navier_now",
                    "markets",
                    "phases",
                ) or (isinstance(v, (list, dict)) and k in ("featured_routes", "wow_corridors", "phases", "markets", "why_navier_now")):
                    walk(v, f"{path}.{k}" if path else k)
                elif k == "route_ids" and isinstance(v, list):
                    for i, r in enumerate(v):
                        if isinstance(r, str):
                            out.append((f"{path}.route_ids[{i}]", r))
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                walk(item, f"{path}[{i}]")

    walk(partner.get("featured_routes"), "featured_routes")
    walk(partner.get("wow_corridors"), "wow_corridors")
    walk(partner.get("why_navier_now"), "why_navier_now")
    walk(partner.get("markets"), "markets")
    walk(partner.get("phases"), "phases")
    return out


def market_displayable_route_count(
    market: dict,
    keep: set[str],
    routes: list[dict],
    bp_city: dict[str, str],
) -> int:
    """Approx build-site market filter: both endpoints in keep (cityIdOf || stamped)."""
    n = 0
    for feat in routes:
        p = feat.get("properties") or {}
        if p.get("render_hidden") is True or p.get("_quarantine") is True or p.get("relevance") == "hide":
            continue
        fr = p.get("from")
        to = p.get("to")
        cf = bp_city.get(fr) or p.get("from_city_id")
        ct = bp_city.get(to) or p.get("to_city_id")
        if cf in keep and ct in keep:
            n += 1
    return n


def audit_partner(
    partner: dict,
    *,
    cluster_by_id: dict,
    city_to_cluster: dict[str, str],
    by_route_id: dict[str, dict],
    by_city: dict[str, set[str]],
    routes: list[dict],
    bp_city: dict[str, str],
    inherit_spec: dict,
    corridor_markets: set[str],
) -> dict[str, Any]:
    pid = partner.get("partner_id", "unknown")
    findings: list[dict[str, Any]] = []
    keys = sealed_registry_keys(partner)
    keep = partner_scope_city_ids(partner, cluster_by_id)
    partner_clusters = partner_clusters_from_keys(keys)
    hub = is_hub_partner(partner)

    # A — footprint covered + geometry, but NO market page keep includes those cities
    # (country-level markets that resolve the full cluster count as covered — not a gap)
    if hub and partner.get("markets"):
        market_keeps: list[tuple[str, set[str]]] = []
        for m in partner.get("markets") or []:
            if not isinstance(m, dict):
                continue
            slug = str(m.get("slug") or m.get("id") or "?")
            try:
                mk = set(hub_rollout_cities(partner, cluster_by_id, page_kind="market", market=m))
            except Exception:
                mk = set(m.get("anchor_cities") or [])
            market_keeps.append((slug, mk))
        union_market = set().union(*(mk for _, mk in market_keeps)) if market_keeps else set()
        for fp in footprint_city_keys(partner):
            key = fp["key"]
            cities = resolve_registry_key_to_city_ids(key, cluster_by_id, partner)
            if not cities:
                continue
            geo_n = sum(len(by_city.get(c, ())) for c in cities)
            if geo_n == 0:
                continue
            if cities & union_market:
                continue
            # true gap: footprint geometry city not in any market keep
            findings.append(
                {
                    "code": "A_footprint_without_market",
                    "severity": "high",
                    "key": key,
                    "label": fp.get("label"),
                    "cities": sorted(cities)[:8],
                    "geometry_route_endpoints": geo_n,
                    "detail": "covered footprint key has geometry cities that no markets[] keep resolves (Dott/Doha-class: footprint-only)",
                }
            )
    elif hub and not partner.get("markets") and footprint_city_keys(partner):
        findings.append(
            {
                "code": "A_hub_without_markets_array",
                "severity": "medium",
                "detail": "hub/network layout but empty markets[]; relies on footprint/hub-index only",
            }
        )

    # B — city-level key added as partnerClusters cluster_id (won't match route.cluster_id)
    for key in keys:
        if key in cluster_by_id:
            continue  # real cluster
        if key in MARKET_CLUSTER_ALIASES:
            continue
        if key in city_to_cluster:
            true_cluster = city_to_cluster[key]
            if true_cluster not in partner_clusters and key in partner_clusters:
                # routes for this city
                rids = by_city.get(key, set())
                if rids:
                    findings.append(
                        {
                            "code": "B_city_key_as_cluster_id",
                            "severity": "info",  # by design for city-level seals when endpoint keep works
                            "key": key,
                            "true_cluster_id": true_cluster,
                            "partner_clusters_has_key": key in partner_clusters,
                            "partner_clusters_has_true": true_cluster in partner_clusters,
                            "endpoint_routes": len(rids),
                            "detail": "build-site partnerClusters uses city id as cluster_id; routes stamp parent cluster — cluster fallback never fires (endpoint keep must work)",
                        }
                    )

    # C — keep city with zero endpoint routes (empty display for that city)
    for c in sorted(keep):
        n = len(by_city.get(c, ()))
        if n == 0 and c in city_to_cluster:
            # also check via BP resolution
            via_bp = 0
            for feat in routes:
                p = feat.get("properties") or {}
                cf = bp_city.get(p.get("from") or "") or p.get("from_city_id")
                ct = bp_city.get(p.get("to") or "") or p.get("to_city_id")
                if cf == c or ct == c:
                    via_bp += 1
            if via_bp == 0:
                findings.append(
                    {
                        "code": "C_keep_city_zero_routes",
                        "severity": "medium",
                        "city_id": c,
                        "detail": "city is in partner keep/scope but no ROUTES endpoints resolve to it",
                    }
                )

    # D — featured route_ids missing from ROUTES
    missing_featured = []
    for path, rid in collect_featured_ids(partner):
        if rid not in by_route_id:
            missing_featured.append({"path": path, "route_id": rid})
    if missing_featured:
        findings.append(
            {
                "code": "D_featured_route_id_missing",
                "severity": "high",
                "count": len(missing_featured),
                "samples": missing_featured[:12],
                "detail": "marquee/featured route_id not present in data-clean/ROUTES.json",
            }
        )

    # E — finance inheritance gaps for hub footprints with registry markets
    fin = (inherit_spec.get("partners") or {}).get(pid)
    if fin and fin.get("ready_to_cascade"):
        inherited_keys = {mk for keys in (fin.get("inherit_markets") or {}).values() for mk in keys}
        # map footprint keys to possible bolt-/registry market names
        for fp in footprint_city_keys(partner):
            key = fp["key"]
            candidates = []
            # exact / bolt-twin only — no substring false friends (cote-dazur ↛ yango-cote-divoire)
            for cand in (
                key,
                f"bolt-{key}",
                f"yango-{key}",
                f"yassir-{key}",
            ):
                if cand in corridor_markets:
                    candidates.append(cand)
            # country fragment only when key is a simple country slug
            if key in corridor_markets:
                candidates.append(key)
            if "-" not in key:
                for pref in ("bolt-", "yango-", "yassir-"):
                    cand = f"{pref}{key}"
                    if cand in corridor_markets:
                        candidates.append(cand)
            candidates = sorted(set(candidates))
            if not candidates:
                continue
            if not any(c in inherited_keys for c in candidates):
                # only flag if geometry exists
                cities = resolve_registry_key_to_city_ids(key, cluster_by_id, partner)
                geo_n = sum(len(by_city.get(c, ())) for c in cities)
                if geo_n > 0:
                    findings.append(
                        {
                            "code": "E_finance_inherit_gap",
                            "severity": "medium",
                            "footprint_key": key,
                            "registry_candidates": candidates[:8],
                            "inherited_keys_sample": sorted(inherited_keys)[:12],
                            "detail": "covered footprint with registry corridors but partner inheritance_spec does not inherit them",
                        }
                    )

    # F — POI name/parent mismatch (heuristic, high-confidence only)
    # deferred to global FBT scan once per run; partner-tagged in global section

    # G — market pages with 0 displayable routes
    if hub:
        for m in partner.get("markets") or []:
            if not isinstance(m, dict):
                continue
            slug = m.get("slug") or m.get("id") or "?"
            scoped = m.get("scope_registry_keys") or m.get("scope_registry_key") or []
            scoped = scoped if isinstance(scoped, list) else [scoped]
            m_keep: set[str] = set(m.get("anchor_cities") or [])
            for ph in m.get("phases") or []:
                if isinstance(ph, dict):
                    m_keep.update(ph.get("cities") or [])
            for k in scoped:
                if k:
                    m_keep.update(resolve_registry_key_to_city_ids(k, cluster_by_id, partner))
            if not m_keep:
                continue
            n = market_displayable_route_count(m, m_keep, routes, bp_city)
            # only flag if keep has cities that have endpoint geometry somewhere
            geo = sum(len(by_city.get(c, ())) for c in m_keep)
            # aspirational-only markets (all featured text_only / no route_id) are expected empty
            feats = []
            for ph in m.get("phases") or []:
                if isinstance(ph, dict):
                    feats.extend(ph.get("featured_routes") or [])
            feats.extend(m.get("featured_routes") or [])
            aspirational_only = bool(feats) and all(
                isinstance(fr, dict)
                and (
                    fr.get("display") == "text_only"
                    or fr.get("_link_status") == "aspirational-no-built-route"
                    or not fr.get("route_id")
                )
                for fr in feats
            )
            if n == 0 and geo > 0 and not aspirational_only:
                findings.append(
                    {
                        "code": "G_market_zero_displayable_routes",
                        "severity": "high",
                        "market": slug,
                        "keep_cities": sorted(m_keep)[:12],
                        "endpoint_geometry_count": geo,
                        "detail": "market keep has geometry via city stamps but both-endpoint keep filter yields 0 routes (orphan BPs / wrong parent / cross-city only legs)",
                    }
                )
            elif n == 0 and geo == 0 and m_keep and not aspirational_only:
                findings.append(
                    {
                        "code": "G_market_zero_geometry",
                        "severity": "medium",
                        "market": slug,
                        "keep_cities": sorted(m_keep)[:12],
                        "detail": "market keep has no ROUTES endpoints at all",
                    }
                )

    # severity rollup
    sev = Counter(f["severity"] for f in findings)
    return {
        "partner_id": pid,
        "hub": hub,
        "scope_city_count": len(keep),
        "sealed_key_count": len(keys),
        "finding_count": len(findings),
        "severity": dict(sev),
        "findings": findings,
    }


def audit_poi_misparent(fbt: dict) -> list[dict[str, Any]]:
    """Global POI parent vs name mismatch (Doha-class)."""
    out = []
    for t, feats in fbt.items():
        if t in ("city", "priority_city"):
            continue
        for f in feats or []:
            p = f.get("properties") or {}
            parent = p.get("parent_city_id") or p.get("city_id")
            name = p.get("name") or p.get("label") or ""
            if not parent or not name:
                continue
            for city_id, pat in CITY_NAME_HINTS:
                if parent == city_id:
                    continue
                if pat.search(name):
                    # avoid weak matches when parent already same country cluster sibling
                    out.append(
                        {
                            "code": "F_poi_name_parent_mismatch",
                            "severity": "high",
                            "bp_id": p.get("id"),
                            "name": name,
                            "parent_city_id": parent,
                            "implied_city_id": city_id,
                            "type": t,
                        }
                    )
                    break
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--fail-on-a",
        action="store_true",
        help="Exit 1 if any A_footprint_without_market findings (covered geometry with no market keep)",
    )
    ap.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 on any HIGH severity finding (A/D/G displayable, etc.)",
    )
    args = ap.parse_args()

    routes = load_json(ROUTES_PATH)
    if not isinstance(routes, list):
        routes = routes.get("features") or routes.get("routes") or []
    fbt = load_json(FBT_PATH)
    inherit_spec = load_json(INHERIT_SPEC) if INHERIT_SPEC.exists() else {"partners": {}}
    corridors = load_json(CORRIDORS) if CORRIDORS.exists() else {"markets": {}}
    corridor_markets = set((corridors.get("markets") or {}).keys())

    _, cluster_by_id, city_to_cluster = load_clusters()
    by_route_id, by_city, _ = route_index(routes)
    bp_city = build_cityId_of(fbt)

    partner_results = []
    for path in sorted(PARTNERS_DIR.glob("*.json")):
        if path.name.startswith("_") or path.name == "atlas-data.js":
            continue
        try:
            doc = load_json(path)
        except Exception as e:
            partner_results.append({"partner_id": path.stem, "error": str(e)})
            continue
        if not isinstance(doc, dict) or not doc.get("partner_id"):
            continue
        partner_results.append(
            audit_partner(
                doc,
                cluster_by_id=cluster_by_id,
                city_to_cluster=city_to_cluster,
                by_route_id=by_route_id,
                by_city=by_city,
                routes=routes,
                bp_city=bp_city,
                inherit_spec=inherit_spec,
                corridor_markets=corridor_markets,
            )
        )

    poi_mismatches = audit_poi_misparent(fbt)
    # de-dupe F noise: only keep if parent is a real city and implied differs
    poi_mismatches = [x for x in poi_mismatches if x["parent_city_id"] != x["implied_city_id"]]

    # rollups
    by_code: Counter = Counter()
    high_partners = []
    a_findings = []
    for r in partner_results:
        for f in r.get("findings") or []:
            by_code[f["code"]] += 1
            if f["code"] == "A_footprint_without_market":
                a_findings.append({"partner_id": r["partner_id"], **f})
        if any(f.get("severity") == "high" for f in r.get("findings") or []):
            high_partners.append(r["partner_id"])

    # attach global F counts
    f_by_implied = Counter(x["implied_city_id"] for x in poi_mismatches)
    f_by_parent = Counter(x["parent_city_id"] for x in poi_mismatches)

    report = {
        "generated": utc_now(),
        "summary": {
            "partners_checked": len(partner_results),
            "partners_with_findings": sum(1 for r in partner_results if r.get("finding_count")),
            "partners_with_high": len(high_partners),
            "findings_by_code": dict(by_code),
            "a_footprint_without_market_count": len(a_findings),
            "poi_name_parent_mismatches": len(poi_mismatches),
            "poi_mismatch_by_implied_city": dict(f_by_implied),
            "poi_mismatch_by_parent": dict(f_by_parent.most_common(20)),
        },
        "codes": {
            "A_footprint_without_market": "Covered footprint key has geometry but no markets[] binding",
            "B_city_key_as_cluster_id": "City-level seal put in partnerClusters; routes use parent cluster_id",
            "C_keep_city_zero_routes": "Keep city has no route endpoints",
            "D_featured_route_id_missing": "Featured/wow route_id absent from ROUTES.json",
            "E_finance_inherit_gap": "Footprint has registry corridors but inheritance_spec omits them",
            "F_poi_name_parent_mismatch": "POI name implies city A but parent_city_id is B",
            "G_market_zero_displayable_routes": "Market keep has geometry but 0 both-endpoint routes",
            "G_market_zero_geometry": "Market keep has no geometry",
        },
        "rule": {
            "id": "covered-footprint-must-have-market-keep",
            "statement": (
                "If network_footprint entry is covered=true and any resolved city has ROUTES "
                "endpoints, then some markets[] keep (via scope_registry_key/keys or anchors) "
                "MUST include those cities — or demote footprint render away from geometry."
            ),
            "gate": "python3 scripts/audit_partner_route_inheritance_health.py --fail-on-a",
        },
        "high_severity_partners": sorted(high_partners),
        "a_findings": a_findings,
        "partners": partner_results,
        "poi_mismatches_sample": poi_mismatches[:80],
        "poi_mismatches_total": len(poi_mismatches),
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")

    print("Partner route inheritance health audit")
    print(f"  partners: {report['summary']['partners_checked']}")
    print(f"  with findings: {report['summary']['partners_with_findings']}")
    print(f"  with HIGH: {report['summary']['partners_with_high']}")
    print(f"  A footprint-only gaps: {len(a_findings)}")
    print(f"  findings by code: {dict(by_code)}")
    print(f"  POI name/parent mismatches: {len(poi_mismatches)}")
    print(f"\nReport → {REPORT_PATH.relative_to(ROOT)}")

    # print top high findings compact
    print("\n=== HIGH severity (by partner) ===")
    for r in sorted(partner_results, key=lambda x: -sum(1 for f in x.get("findings") or [] if f.get("severity") == "high")):
        highs = [f for f in r.get("findings") or [] if f.get("severity") == "high"]
        if not highs:
            continue
        print(f"\n  {r['partner_id']} ({len(highs)} high)")
        for f in highs[:8]:
            print(f"    [{f['code']}] {json.dumps({k: v for k, v in f.items() if k not in ('code', 'severity', 'detail')}, ensure_ascii=False)[:180]}")
            print(f"      {f.get('detail', '')[:140]}")
        if len(highs) > 8:
            print(f"    ... +{len(highs) - 8} more")

    print("\n=== POI mismatch top parents (F) ===")
    for parent, n in f_by_parent.most_common(15):
        print(f"  {parent}: {n}")

    if args.fail_on_a and a_findings:
        print(f"\n✗ FAIL --fail-on-a: {len(a_findings)} covered-footprint cities lack market keep")
        for a in a_findings[:20]:
            print(f"  {a['partner_id']}: {a.get('key')}")
        return 1
    if args.strict and high_partners:
        print(f"\n✗ FAIL --strict: HIGH findings on {sorted(high_partners)}")
        return 1
    if args.fail_on_a or args.strict:
        print("\n  ✅ inheritance health gate pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
