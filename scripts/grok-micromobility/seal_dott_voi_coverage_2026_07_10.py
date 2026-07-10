#!/usr/bin/env python3
"""Grok seal — Dott/Voi coverage repair after Tasklet PR #216.

1. Replace stale registry keys / footprint with evidence-supported clusters
2. Rematerialize live _map_scope from CLUSTERS (no legacy city union)
3. Bank validation receipts

Does not mint Belgium/Le Havre/etc. geometry. No economics promotion.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DC = ROOT / "data-clean"
OUT = ROOT / "handoff/partner-map-model/dott-voi"
OUT.mkdir(parents=True, exist_ok=True)

# Tasklet evidence-supported existing Atlas clusters (GROK-HANDOFF #216)
DOTT_CLUSTERS = [
    "balearic-islands-spain",
    "bay-of-naples-amalfi-coast-italy",
    "cote-dazur-france-archipelago",
    "denmark",
    "finland",
    "france",
    "germany",
    "greece",
    "israel",
    "italy",
    "netherlands",
    "norway",
    "saudi-arabia",
    "spain",
    "switzerland",
    "uae",
    "uk",
]
DOTT_STALE = {
    "bahrain",
    "cyprus",
    "dalmatia-croatia",
    "egypt",
    "estonia",
    "ireland",
    "lebanon",
    "monaco",
    "morocco",
    "portugal",
    "qatar",
    "romania",
    "sweden",
}

VOI_CLUSTERS = [
    "balearic-islands-spain",
    "bay-of-naples-amalfi-coast-italy",
    "cote-dazur-france-archipelago",
    "denmark",
    "finland",
    "france",
    "germany",
    "italy",
    "netherlands",
    "norway",
    "spain",
    "sweden",
    "switzerland",
    "uk",
]
# Voi is Europe-only; no UAE/MENA current or expansion coverage.
VOI_EXPANSION: list[str] = []
VOI_STALE = {
    "cyprus",
    "dalmatia-croatia",
    "egypt",
    "estonia",
    "greece",
    "ireland",
    "israel",
    "lebanon",
    "monaco",
    "morocco",
    "portugal",
    "romania",
    "saudi-arabia",
    "uae",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load(path: Path):
    return json.loads(path.read_text())


def save(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def cluster_index(clusters_doc: dict) -> dict[str, dict]:
    return {c["cluster_id"]: c for c in clusters_doc.get("clusters") or []}


def city_ids_for_clusters(by_id: dict[str, dict], cluster_ids: list[str]) -> list[str]:
    out: list[str] = []
    for cid in cluster_ids:
        c = by_id.get(cid)
        if not c:
            continue
        out.extend(c.get("member_city_ids") or [])
    return sorted(set(out))


def footprint_entry(cluster_id: str, *, expansion: bool = False) -> dict:
    labels = {
        "uae": "UAE",
        "uk": "United Kingdom",
        "saudi-arabia": "Saudi Arabia",
        "cote-dazur-france-archipelago": "Côte d'Azur",
        "bay-of-naples-amalfi-coast-italy": "Bay of Naples / Amalfi",
        "balearic-islands-spain": "Balearic Islands",
    }
    return {
        "id": cluster_id,
        "registry_key": cluster_id,
        "covered": True,
        "tier": "expansion_opportunity" if expansion else "country_supported",
        "render": "geometry" if not expansion else "aspirational",
        "map_promote": not expansion,
        "label": labels.get(cluster_id, cluster_id.replace("-", " ").title()),
        "region": "Europe" if cluster_id not in ("uae", "saudi-arabia", "israel") else "MENA",
        "_evidence": "tasklet/dott-voi-coverage-2026-07-10",
        **(
            {
                "_operation_status": "expansion_not_current",
                "_operation_note": "Not in current official Voi city directory — expansion proposal only",
            }
            if expansion
            else {"_operation_status": "current_operation_supported"}
        ),
    }


def ensure_market(markets: list, mid: str, label: str, region: str, anchors: list[str], *, expansion: bool = False) -> None:
    existing = next((m for m in markets if (m.get("id") or m.get("slug")) == mid), None)
    if existing:
        if expansion:
            existing["label"] = existing.get("label") or label
            if "expansion" not in str(existing.get("label", "")).lower():
                existing["label"] = label
            existing["_operation_status"] = "expansion_not_current"
        return
    markets.append(
        {
            "id": mid,
            "slug": mid,
            "label": label,
            "region": region,
            "summary": (
                f"{label} — expansion opportunity (not current operation)."
                if expansion
                else f"{label} — current-operation footprint supported by official city directories."
            ),
            "anchor_cities": anchors[:3],
            "phases": [
                {"id": "prove", "name": "Prove", "featured_routes": []},
                {"id": "expand", "name": "Expand", "featured_routes": []},
                {"id": "full", "name": "Full network", "featured_routes": []},
            ],
            "featured_routes": [],
            **({"_operation_status": "expansion_not_current"} if expansion else {}),
        }
    )


def seal_partner(
    partner_id: str,
    clusters: list[str],
    *,
    expansion_clusters: list[str] | None = None,
    remove_stale: set[str] | None = None,
    by_id: dict[str, dict],
    routes: list,
) -> dict:
    path = DC / "partners" / f"{partner_id}.json"
    pitch = ROOT / "partner-pitch" / "partners" / f"{partner_id}.json"
    doc = load(path)
    # Visible archetype chips use the canonical underscore form.
    doc["archetype"] = "ride_hail"
    expansion_clusters = expansion_clusters or []
    remove_stale = remove_stale or set()

    all_keys = list(dict.fromkeys([*clusters, *expansion_clusters]))
    missing = [c for c in all_keys if c not in by_id]
    cities = city_ids_for_clusters(by_id, all_keys)

    # Network footprint — evidence clusters only
    new_fp = []
    for cid in clusters:
        if cid in by_id:
            new_fp.append(footprint_entry(cid, expansion=False))
    for cid in expansion_clusters:
        if cid in by_id:
            new_fp.append(footprint_entry(cid, expansion=True))
    doc["network_footprint"] = new_fp

    # Markets: keep existing non-stale; add missing evidence markets
    markets = list(doc.get("markets") or [])
    markets = [
        m
        for m in markets
        if (m.get("id") or m.get("slug") or "") not in remove_stale
        and not any(s in str(m.get("id") or m.get("slug") or "").lower() for s in remove_stale)
    ]
    # Drop markets that map only to stale countries
    stale_market_ids = {
        "qatar",
        "sweden" if partner_id == "dott" else None,
        "greece" if partner_id == "voi" else None,
        "israel" if partner_id == "voi" else None,
        "ksa-commercial" if partner_id == "voi" else None,
    } - {None}
    markets = [m for m in markets if (m.get("id") or m.get("slug")) not in stale_market_ids]

    # Ensure core country markets exist for inheritance registry keys
    core_market_specs = {
        "uk": ("United Kingdom", "Europe"),
        "germany": ("Germany", "Europe"),
        "norway": ("Norway", "Europe"),
        "denmark": ("Denmark", "Europe"),
        "netherlands": ("Netherlands", "Europe"),
        "switzerland": ("Switzerland", "Europe"),
        "france": ("France", "Europe"),
        "finland": ("Finland", "Europe"),
        "spain": ("Spain", "Europe"),
        "italy": ("Italy", "Europe"),
        "greece": ("Greece", "Europe"),
        "israel": ("Israel", "MENA"),
        "saudi-arabia": ("Saudi Arabia", "MENA"),
        "sweden": ("Sweden", "Europe"),
        "uae": ("UAE — Dubai (expansion)" if partner_id == "voi" else "UAE — Dubai & Abu Dhabi", "MENA"),
    }
    for cid in all_keys:
        if cid in (
            "balearic-islands-spain",
            "bay-of-naples-amalfi-coast-italy",
            "cote-dazur-france-archipelago",
        ):
            continue  # covered by spain/italy/france parents
        if cid in core_market_specs:
            label, region = core_market_specs[cid]
            anchors = (by_id.get(cid) or {}).get("member_city_ids") or []
            ensure_market(
                markets,
                cid,
                label,
                region,
                anchors,
                expansion=(cid in expansion_clusters),
            )
    # Voi UAE label
    if partner_id == "voi":
        for m in markets:
            if (m.get("id") or m.get("slug")) == "uae":
                m["label"] = "UAE — Dubai (expansion)"
                m["_operation_status"] = "expansion_not_current"
                m["summary"] = (
                    "Dubai expansion opportunity — Voi does not currently operate in the UAE per "
                    "the official city directory. Not a current-operation claim."
                )
    doc["markets"] = markets

    # Live map scope — no stale legacy cities
    doc["_map_scope"] = {
        "_doc": "Live cluster inheritance after Dott/Voi #216 seal — evidence registry keys only; no legacy city union",
        "generated": utc_now(),
        "source": "live_cluster_inheritance",
        "registry_keys": all_keys,
        "cluster_city_ids": cities,
        "inheritance_policy": "evidence_supported_clusters_only_no_legacy_union",
        "union_legacy_city_ids": False,
        "_held": {
            **{
                s: f"stale/unsupported — removed from current {partner_id} footprint (Tasklet #216)"
                for s in sorted(remove_stale)
            },
            **(
                {
                    "uae": "expansion opportunity only — not current Voi operation"
                    if partner_id == "voi"
                    else doc.get("_map_scope", {}).get("_held", {}).get("uae", "")
                }
                if partner_id == "voi"
                else {}
            ),
        },
        "_dott_voi_seal": {
            "at": utc_now(),
            "source": "tasklet/pr-216",
            "clusters": clusters,
            "expansion": expansion_clusters,
            "stale_removed": sorted(remove_stale),
            "missing_atlas_clusters": missing,
        },
    }

    # Phase cities: union anchors from evidence (no beirut)
    if doc.get("phases"):
        phase_cities = cities[:40]  # cap phase lists; inheritance uses registry_keys
        # Prefer country anchors not full city dump for phases
        anchors = []
        for cid in all_keys:
            mem = (by_id.get(cid) or {}).get("member_city_ids") or []
            if mem:
                anchors.append(mem[0])
        for i, ph in enumerate(doc["phases"]):
            ph["cities"] = anchors[: max(3, (i + 1) * 4)]

    if partner_id == "voi":
        enforce_voi_europe_only(doc)
    marquee_rep = canonicalize_marquees(doc, routes, set(clusters))

    save(path, doc)
    if pitch.exists():
        shutil.copyfile(path, pitch)

    return {
        "partner_id": partner_id,
        "registry_keys": all_keys,
        "city_count": len(cities),
        "missing_clusters": missing,
        "stale_removed": sorted(remove_stale),
        "expansion": expansion_clusters,
        "marquee_normalization": marquee_rep,
        "has_beirut": any("beirut" in c or "lebanon" in c for c in cities),
    }


MENA_CITY_TOKENS = (
    "-uae", "dubai", "abu-dhabi", "abu dhabi", "-ksa", "saudi",
    "qatar", "doha", "al-wakrah", "israel", "tel-aviv", "haifa",
    "lebanon", "beirut", "egypt", "hurghada", "sharm-el-sheikh",
    "bahrain", "manama", "morocco", "tangier",
)


def contains_mena_reference(value) -> bool:
    text = json.dumps(value, ensure_ascii=False).lower()
    return any(token in text for token in MENA_CITY_TOKENS)


def enforce_voi_europe_only(doc: dict) -> None:
    """Remove live/aspirational MENA coverage while preserving held audit metadata."""
    doc["journeys_unlocked"] = [
        row for row in (doc.get("journeys_unlocked") or [])
        if not contains_mena_reference(row)
    ]

    end_state = doc.get("end_state") or {}
    end_state["addressable_regions"] = [
        region for region in (end_state.get("addressable_regions") or [])
        if str(region).lower() != "mena"
    ]
    end_state["addressable_footprint"] = (
        "Voi's addressable water footprint is Europe-only: the Mediterranean, Atlantic, "
        "Baltic and Nordic waterfront cities already supported by Voi's operating footprint."
    )
    end_state["end_state_cities"] = [
        city for city in (end_state.get("end_state_cities") or [])
        if not contains_mena_reference(city)
    ]
    end_state["narrative"] = (
        "Steady state is a Europe-only Voi water tier across the Mediterranean, Atlantic, "
        "Baltic and Nordic waterfronts."
    )
    doc["end_state"] = end_state

    for row in doc.get("proof_points") or []:
        evidence = str(row.get("evidence") or "")
        row["evidence"] = evidence.replace(
            "The Cyclades, Dalmatia, Amalfi, the Riviera and the Gulf",
            "The Baltic, Atlantic and Mediterranean waterfronts",
        ).replace(
            "every Med and Gulf market",
            "Voi's European waterfront markets",
        )
    for row in doc.get("objections") or []:
        concern = str(row.get("concern") or "")
        response = str(row.get("response") or "")
        row["concern"] = concern.replace(
            "the Mediterranean and Gulf",
            "Voi's European waterfront markets",
        )
        row["response"] = response.replace(
            "Across the Saronic, the Dalmatian coast and the Gulf",
            "Across the Baltic, Atlantic and Mediterranean coasts",
        ).replace(
            "the longer island and cross-gulf legs",
            "the longer European island and regional legs",
        )

    doc["coverage_note"] = (
        "Voi operates in Europe only. No UAE, Middle East or other MENA market is in current "
        "or expansion map coverage."
    )


def canonicalize_marquees(doc: dict, routes: list, allowed_cluster_ids: set[str]) -> dict:
    """Keep highlights as strict, exact-ID subsets of inherited canonical routes."""
    route_by_id = {}
    for feat in routes:
        props = feat.get("properties") or {}
        rid = props.get("id")
        if rid and props.get("cluster_id") in allowed_cluster_ids:
            route_by_id[rid] = props

    dropped = []

    def normalize(entries, path):
        out = []
        seen = set()
        for i, entry in enumerate(entries or []):
            rid = entry.get("route_id") if isinstance(entry, dict) else None
            props = route_by_id.get(rid)
            if not props or rid in seen:
                dropped.append({"path": f"{path}[{i}]", "route_id": rid})
                continue
            out.append({
                "route_id": rid,
                "from_label": props.get("from_label"),
                "to_label": props.get("to_label"),
                "cluster_id": props.get("cluster_id"),
            })
            seen.add(rid)
        return out

    if "featured_routes" in doc:
        doc["featured_routes"] = normalize(doc.get("featured_routes"), "featured_routes")
    if "wow_corridors" in doc:
        doc["wow_corridors"] = normalize(doc.get("wow_corridors"), "wow_corridors")
    root_wnn = doc.get("why_navier_now")
    if isinstance(root_wnn, dict) and "wow_corridors" in root_wnn:
        root_wnn["wow_corridors"] = normalize(root_wnn.get("wow_corridors"), "why_navier_now.wow_corridors")
    for pi, phase in enumerate(doc.get("phases") or []):
        if isinstance(phase, dict) and "featured_routes" in phase:
            phase["featured_routes"] = normalize(phase.get("featured_routes"), f"phases[{pi}].featured_routes")
    for mi, market in enumerate(doc.get("markets") or []):
        if not isinstance(market, dict):
            continue
        mid = market.get("id") or market.get("slug") or str(mi)
        if "featured_routes" in market:
            market["featured_routes"] = normalize(market.get("featured_routes"), f"markets[{mid}].featured_routes")
        if "wow_corridors" in market:
            market["wow_corridors"] = normalize(market.get("wow_corridors"), f"markets[{mid}].wow_corridors")
        wnn = market.get("why_navier_now")
        if isinstance(wnn, dict) and "wow_corridors" in wnn:
            wnn["wow_corridors"] = normalize(wnn.get("wow_corridors"), f"markets[{mid}].why_navier_now.wow_corridors")
        for pi, phase in enumerate(market.get("phases") or []):
            if isinstance(phase, dict) and "featured_routes" in phase:
                phase["featured_routes"] = normalize(
                    phase.get("featured_routes"),
                    f"markets[{mid}].phases[{pi}].featured_routes",
                )
    return {"dropped": dropped, "kept": sum(1 for _ in iter_highlight_route_ids(doc))}


def iter_highlight_route_ids(doc: dict):
    def yield_from(entries):
        for entry in entries or []:
            if isinstance(entry, dict) and entry.get("route_id"):
                yield entry["route_id"]
    yield from yield_from(doc.get("featured_routes"))
    yield from yield_from(doc.get("wow_corridors"))
    root_wnn = doc.get("why_navier_now") or {}
    yield from yield_from(root_wnn.get("wow_corridors"))
    for phase in doc.get("phases") or []:
        if isinstance(phase, dict):
            yield from yield_from(phase.get("featured_routes"))
    for market in doc.get("markets") or []:
        if not isinstance(market, dict):
            continue
        yield from yield_from(market.get("featured_routes"))
        yield from yield_from(market.get("wow_corridors"))
        market_wnn = market.get("why_navier_now")
        if isinstance(market_wnn, dict):
            yield from yield_from(market_wnn.get("wow_corridors"))
        for phase in market.get("phases") or []:
            if isinstance(phase, dict):
                yield from yield_from(phase.get("featured_routes"))


def count_routes_by_cluster(routes: list, cluster_ids: set[str]) -> dict:
    counts: dict[str, int] = {c: 0 for c in sorted(cluster_ids)}
    total = 0
    leb = 0
    for r in routes:
        p = r.get("properties") or {}
        if p.get("_quarantine") or p.get("relevance") == "hide":
            continue
        cid = p.get("cluster_id")
        if cid in cluster_ids:
            counts[cid] = counts.get(cid, 0) + 1
            total += 1
        if cid == "lebanon" or "lebanon" in str(p.get("from_city_id", "")):
            leb += 1
    return {"by_cluster": counts, "total_in_scope": total, "lebanon_routes": leb}


def main() -> int:
    clusters_doc = load(DC / "CLUSTERS.json")
    by_id = cluster_index(clusters_doc)
    routes = load(DC / "ROUTES.json")

    dott_rep = seal_partner(
        "dott",
        DOTT_CLUSTERS,
        expansion_clusters=[],
        remove_stale=DOTT_STALE,
        by_id=by_id,
        routes=routes,
    )
    voi_rep = seal_partner(
        "voi",
        VOI_CLUSTERS,
        expansion_clusters=VOI_EXPANSION,
        remove_stale=VOI_STALE,
        by_id=by_id,
        routes=routes,
    )

    dott_clusters = set(DOTT_CLUSTERS)
    voi_clusters = set(VOI_CLUSTERS + VOI_EXPANSION)
    dott_counts = count_routes_by_cluster(routes, dott_clusters)
    voi_counts = count_routes_by_cluster(routes, voi_clusters)

    # Gate G
    gates = {}
    try:
        r = subprocess.run(
            [sys.executable, str(ROOT / "scripts/audit_partner_copy.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=120,
        )
        gates["gate_g"] = {"exit": r.returncode, "pass": r.returncode == 0, "tail": (r.stdout or r.stderr or "")[-400:]}
    except Exception as e:
        gates["gate_g"] = {"pass": False, "error": str(e)}
    try:
        r = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/validate_partner_inheritance.py"),
                "--partner", "dott", "voi", "--strict", "--include-pitch",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=120,
        )
        gates["partner_inheritance_strict"] = {
            "exit": r.returncode,
            "pass": r.returncode == 0,
            "tail": (r.stdout or r.stderr or "")[-600:],
        }
    except Exception as e:
        gates["partner_inheritance_strict"] = {"pass": False, "error": str(e)}

    receipt = {
        "at": utc_now(),
        "lane": "Dott/Voi coverage seal after PR #216",
        "status": "scope_resealed / voi_europe_only / dott_uae_confirmed / finance_not_promoted",
        "upstream_pr": 216,
        "renderer_fixes": [
            "partner-scope.mjs: stop unioning legacy cluster_city_ids on hub-index",
            "route-display.mjs: no density cull / no auto-legacy for hub-index inheritClusters",
            "build-site.mjs: hub inherit selects ROUTES by cluster_id membership",
        ],
        "dott": {**dott_rep, "expected_canonical_routes": dott_counts},
        "voi": {**voi_rep, "expected_canonical_routes": voi_counts},
        "acceptance": {
            "dott_no_beirut_in_scope_cities": not dott_rep["has_beirut"],
            "voi_no_beirut_in_scope_cities": not voi_rep["has_beirut"],
            "dott_no_qatar_key": "qatar" not in dott_rep["registry_keys"],
            "dott_no_sweden_key": "sweden" not in dott_rep["registry_keys"],
            "dott_uae_current_coverage": "uae" in dott_rep["registry_keys"],
            "dott_abu_dhabi_dubai_in_scope": {"abu-dhabi-uae", "dubai-uae"}.issubset(
                set(city_ids_for_clusters(by_id, dott_rep["registry_keys"]))
            ),
            "voi_europe_only_no_uae_or_mena_scope": "uae" not in voi_rep["registry_keys"]
            and not any(c in {"uae", "saudi-arabia", "israel"} for c in voi_rep["registry_keys"]),
            "netherlands_in_both": "netherlands" in dott_rep["registry_keys"]
            and "netherlands" in voi_rep["registry_keys"],
        },
        "gates": gates,
        "registry_backlog_p1": [
            "Belgium (both)",
            "Le Havre / Seine for Voi only",
            "UK / Germany / Nordics depth",
            "Poland (Dott)",
            "Switzerland zero-route cluster",
            "Austria / Hungary",
        ],
        "do_not": [
            "No economics promotion",
            "No partner-specific corridor mint",
            "No Belgium/Le Havre geometry invent",
            "No Voi UAE/MENA expansion coverage",
        ],
    }
    save(OUT / "GROK-DOTT-VOI-COVERAGE-SEAL-RECEIPT-2026-07-10.json", receipt)
    md = [
        "# Grok — Dott/Voi coverage seal",
        "",
        f"**UTC:** {receipt['at']}",
        f"**Status:** `{receipt['status']}`",
        f"**Upstream:** PR #216",
        "",
        "## Renderer",
        "- Hub inheritance: full cluster_id route set; no density/legacy cull",
        "- No legacy `_map_scope.cluster_city_ids` union on hub-index",
        "",
        "## Dott",
        f"- Registry keys: {len(dott_rep['registry_keys'])}",
        f"- Scope cities: {dott_rep['city_count']} (beirut={dott_rep['has_beirut']})",
        f"- Canonical routes in scope clusters: **{dott_counts['total_in_scope']}**",
        f"- Stale removed: {', '.join(dott_rep['stale_removed'])}",
        "",
        "## Voi",
        f"- Registry keys: {len(voi_rep['registry_keys'])} (Europe only; no UAE/MENA coverage)",
        f"- Scope cities: {voi_rep['city_count']} (beirut={voi_rep['has_beirut']})",
        f"- Canonical routes in scope clusters: **{voi_counts['total_in_scope']}**",
        f"- Stale removed: {', '.join(voi_rep['stale_removed'])}",
        "",
        "## Acceptance",
    ]
    for k, v in receipt["acceptance"].items():
        md.append(f"- `{k}`: **{v}**")
    md.append("")
    md.append(f"Gate G: {'PASS' if gates.get('gate_g', {}).get('pass') else 'FAIL'}")
    md.append(
        f"Partner inheritance (strict, data + pitch): "
        f"{'PASS' if gates.get('partner_inheritance_strict', {}).get('pass') else 'FAIL'}"
    )
    md.append("")
    md.append("Machine: `handoff/partner-map-model/dott-voi/GROK-DOTT-VOI-COVERAGE-SEAL-RECEIPT-2026-07-10.json`")
    (OUT / "GROK-DOTT-VOI-COVERAGE-SEAL-RECEIPT-2026-07-10.md").write_text("\n".join(md) + "\n")

    print(json.dumps({
        "dott_routes": dott_counts["total_in_scope"],
        "voi_routes": voi_counts["total_in_scope"],
        "acceptance": receipt["acceptance"],
        "gate_g": gates.get("gate_g", {}).get("pass"),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
