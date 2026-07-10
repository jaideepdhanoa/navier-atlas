#!/usr/bin/env python3
"""Wave1 Bite0 + DiDi HK precision seal (PRs #219/#220).

1. Retag 14 Lake Geneva routes indonesia → switzerland (preserve IDs)
2. Decompose UK into water-system clusters; rebind Dott/Voi scopes
3. Ibiza: document reuse of existing 10 routes (no mint)
4. Split hong-kong-macau → hong-kong + macau; DiDi inherits HK only
5. Partner scope + inheritance updates

Does not invent BP coordinates or economics. Wave1 new mints held (coords null).
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DC = ROOT / "data-clean"
ROUTES = DC / "ROUTES.json"
CLUSTERS = DC / "CLUSTERS.json"
FEATURES = DC / "FEATURES_BY_TYPE.json"
OUT = ROOT / "handoff/partner-map-model/dott-voi/enrichment-wave1"
OUT.mkdir(parents=True, exist_ok=True)

LAKE_GENEVA_IDS = [
    "ics-0500aefc8e", "ics-23fc6b9455", "ics-358e0a460a", "ics-4edd004c4b",
    "ics-785dfcc7fc", "ics-9122d66efd", "ics-926be6d4d9", "ics-9e6dadda56",
    "ics-c94449e6cf", "ics-cb5aa8b99f", "ics-cf2413452b", "ics-d2c3dd4e8c",
    "ics-d32551445f", "ics-ffd276b487",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load(p: Path) -> Any:
    return json.loads(p.read_text())


def save(p: Path, obj: Any) -> None:
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def ensure_cluster(clusters: list, cluster_id: str, members: list[str], label: str, region: str) -> dict:
    for c in clusters:
        if c.get("cluster_id") == cluster_id:
            # union members
            m = list(dict.fromkeys((c.get("member_city_ids") or []) + members))
            c["member_city_ids"] = m
            c.setdefault("label", label)
            c.setdefault("display", label)
            c.setdefault("region", region)
            return c
    c = {
        "cluster_id": cluster_id,
        "label": label,
        "display": label,
        "region": region,
        "member_city_ids": list(members),
        "_source": "grok/wave1-p0-2026-07-10",
    }
    clusters.append(c)
    return c


def retag_routes(routes: list, predicate, new_cluster: str) -> list[str]:
    changed = []
    for f in routes:
        p = f.get("properties") or {}
        rid = p.get("id")
        if not rid:
            continue
        if predicate(p):
            old = p.get("cluster_id")
            p["cluster_id"] = new_cluster
            p["_cluster_retag_at"] = utc_now()
            p["_cluster_retag_from"] = old
            p["_cluster_retag_source"] = "grok/wave1-p0-2026-07-10"
            changed.append(rid)
    return changed


def main() -> int:
    routes = load(ROUTES)
    clusters_doc = load(CLUSTERS)
    clusters = clusters_doc.setdefault("clusters", [])
    feats = load(FEATURES)

    receipt: dict[str, Any] = {
        "at": utc_now(),
        "lane": "wave1 bite0 P0 + DiDi HK/Macau precision",
        "upstream_prs": [219, 220],
        "status": "p0_complete / wave1_new_mints_held_null_coords / finance_untouched",
    }

    # ─── 1. Lake Geneva retag ───────────────────────────────────────────
    geneva_set = set(LAKE_GENEVA_IDS)
    geneva = retag_routes(
        routes,
        lambda p: p.get("id") in geneva_set or (
            p.get("cluster_id") == "indonesia"
            and p.get("from_city_id") == "lake-geneva-switzerland"
        ),
        "switzerland",
    )
    # ensure switzerland has lake-geneva city
    ensure_cluster(clusters, "switzerland", ["lake-geneva-switzerland"], "Switzerland", "Europe")
    receipt["lake_geneva"] = {
        "retagged_count": len(geneva),
        "route_ids": sorted(geneva),
        "from": "indonesia",
        "to": "switzerland",
    }

    # ─── 2. UK decompose ────────────────────────────────────────────────
    # Ensure city nodes exist in FEATURES for cluster members
    city_ids = set()
    for t in ("city", "priority_city"):
        for f in feats.get(t) or []:
            pid = (f.get("properties") or {}).get("id")
            if pid:
                city_ids.add(pid)

    # Create water-system clusters
    ensure_cluster(clusters, "london-thames-uk", ["london-thames-uk"], "London Thames", "Europe")
    ensure_cluster(clusters, "liverpool-mersey-uk", ["liverpool-mersey-uk"], "Liverpool Mersey", "Europe")
    ensure_cluster(clusters, "firth-of-clyde-scotland", ["firth-of-clyde-scotland"], "Firth of Clyde", "Europe")
    ensure_cluster(clusters, "scotland-hebrides", ["calmac"], "Scotland Hebrides / CalMac network", "Europe")

    uk_counts: dict[str, list[str]] = {
        "london-thames-uk": [],
        "liverpool-mersey-uk": [],
        "firth-of-clyde-scotland": [],
        "scotland-hebrides": [],
    }

    def uk_target(p: dict) -> str | None:
        if p.get("cluster_id") != "uk":
            return None
        fc = p.get("from_city_id") or ""
        tc = p.get("to_city_id") or ""
        lab = (p.get("label") or "").lower()
        if fc == "london-thames-uk" or tc == "london-thames-uk" or "thames" in lab or "london" in lab:
            return "london-thames-uk"
        if fc == "liverpool-mersey-uk" or tc == "liverpool-mersey-uk" or "mersey" in lab or "liverpool" in lab:
            return "liverpool-mersey-uk"
        if fc == "firth-of-clyde-scotland" or tc == "firth-of-clyde-scotland" or "clyde" in lab:
            return "firth-of-clyde-scotland"
        if fc == "calmac" or tc == "calmac" or lab.startswith("calmac"):
            return "scotland-hebrides"
        return None

    for f in routes:
        p = f.get("properties") or {}
        tgt = uk_target(p)
        if not tgt:
            continue
        old = p.get("cluster_id")
        p["cluster_id"] = tgt
        p["_cluster_retag_at"] = utc_now()
        p["_cluster_retag_from"] = old
        p["_cluster_retag_source"] = "grok/wave1-uk-decompose-2026-07-10"
        uk_counts[tgt].append(p.get("id"))

    # Empty generic uk membership (keep cluster shell for legacy refs)
    for c in clusters:
        if c.get("cluster_id") == "uk":
            c["member_city_ids"] = []
            c["_deprecated"] = True
            c["_deprecated_note"] = "Decomposed into london-thames-uk, liverpool-mersey-uk, firth-of-clyde-scotland, scotland-hebrides"
            c["_deprecated_at"] = utc_now()

    receipt["uk_decompose"] = {
        k: {"count": len(v), "route_ids": v} for k, v in uk_counts.items()
    }
    receipt["uk_total_retagged"] = sum(len(v) for v in uk_counts.values())

    # ─── 3. Ibiza reuse note ────────────────────────────────────────────
    ibiza_routes = []
    for f in routes:
        p = f.get("properties") or {}
        if p.get("_quarantine") or p.get("relevance") == "hide":
            continue
        if p.get("from_city_id") == "ibiza-spain" or p.get("to_city_id") == "ibiza-spain":
            ibiza_routes.append(p.get("id"))
    receipt["ibiza"] = {
        "action": "reuse_existing",
        "city_id": "ibiza-spain",
        "visible_routes": len(ibiza_routes),
        "route_ids": ibiza_routes,
        "note": "No duplicate mint; terminals may normalize aliases later",
    }

    # ─── 4. Hong Kong / Macau split ─────────────────────────────────────
    ensure_cluster(clusters, "hong-kong", ["hong-kong"], "Hong Kong", "East Asia")
    ensure_cluster(clusters, "macau", ["macau-china"], "Macau", "East Asia")

    hk_ids, mc_ids = [], []
    for f in routes:
        p = f.get("properties") or {}
        if p.get("cluster_id") != "hong-kong-macau":
            continue
        fc, tc = p.get("from_city_id"), p.get("to_city_id")
        rid = p.get("id")
        # Skip quarantined cross-border for cluster assignment of active set
        if fc == "hong-kong" and tc == "hong-kong":
            p["cluster_id"] = "hong-kong"
            p["_cluster_retag_from"] = "hong-kong-macau"
            p["_cluster_retag_at"] = utc_now()
            p["_cluster_retag_source"] = "grok/didi-hk-macau-split-2026-07-10"
            if not (p.get("_quarantine") or p.get("relevance") == "hide"):
                hk_ids.append(rid)
        elif fc == "macau-china" and tc == "macau-china":
            p["cluster_id"] = "macau"
            p["_cluster_retag_from"] = "hong-kong-macau"
            p["_cluster_retag_at"] = utc_now()
            p["_cluster_retag_source"] = "grok/didi-hk-macau-split-2026-07-10"
            if not (p.get("_quarantine") or p.get("relevance") == "hide"):
                mc_ids.append(rid)
        else:
            # cross-city: leave quarantine; assign cluster by majority endpoint
            if fc == "hong-kong" or tc == "hong-kong":
                p["cluster_id"] = "hong-kong"
            else:
                p["cluster_id"] = "macau"
            p["_cluster_retag_from"] = "hong-kong-macau"
            p["_cluster_retag_at"] = utc_now()

    # Deprecate combined cluster shell
    for c in clusters:
        if c.get("cluster_id") == "hong-kong-macau":
            c["member_city_ids"] = []
            c["_deprecated"] = True
            c["_deprecated_note"] = "Split into hong-kong + macau; DiDi inherits hong-kong only"
            c["_deprecated_at"] = utc_now()

    # Update city feature cluster_id if present
    for t in ("city", "priority_city"):
        for f in feats.get(t) or []:
            p = f.get("properties") or {}
            if p.get("id") == "hong-kong":
                p["cluster_id"] = "hong-kong"
            if p.get("id") == "macau-china":
                p["cluster_id"] = "macau"
            if p.get("id") == "london-thames-uk":
                p["cluster_id"] = "london-thames-uk"
            if p.get("id") == "liverpool-mersey-uk":
                p["cluster_id"] = "liverpool-mersey-uk"
            if p.get("id") == "firth-of-clyde-scotland":
                p["cluster_id"] = "firth-of-clyde-scotland"
            if p.get("id") == "lake-geneva-switzerland":
                p["cluster_id"] = "switzerland"

    receipt["hk_macau_split"] = {
        "hong_kong_visible_routes": len(hk_ids),
        "macau_visible_routes": len(mc_ids),
        "hong_kong_route_ids": hk_ids,
        "macau_route_ids": mc_ids,
    }

    # ─── 5. Partner scopes ──────────────────────────────────────────────
    def rewrite_registry(keys: list[str], *, replace: dict[str, list[str]], remove: set[str]) -> list[str]:
        out: list[str] = []
        for k in keys:
            if k in remove:
                continue
            if k in replace:
                out.extend(replace[k])
            else:
                out.append(k)
        # dedupe preserve order
        seen = set()
        final = []
        for k in out:
            if k not in seen:
                seen.add(k)
                final.append(k)
        return final

    # Dott: uk → clyde only; add switzerland already present; no london/mersey/hebrides
    dott_path = DC / "partners/dott.json"
    dott = load(dott_path)
    ms = dott.setdefault("_map_scope", {})
    old_keys = list(ms.get("registry_keys") or [])
    new_keys = rewrite_registry(
        old_keys,
        replace={"uk": ["firth-of-clyde-scotland"]},
        remove={"hong-kong-macau"},
    )
    if "switzerland" not in new_keys:
        new_keys.append("switzerland")
    if "balearic-islands-spain" not in new_keys and "spain" in new_keys:
        pass  # ibiza via balearic or spain
    ms["registry_keys"] = new_keys
    ms["union_legacy_city_ids"] = False
    ms["_uk_decompose"] = {
        "inherits": ["firth-of-clyde-scotland"],
        "excludes": ["london-thames-uk", "liverpool-mersey-uk", "scotland-hebrides"],
        "reason": "Dott current evidence: Glasgow/Clyde only; London excluded; Liverpool unestablished",
    }
    # Rematerialize cities from clusters
    by_id = {c["cluster_id"]: c for c in clusters}
    cities = []
    for k in new_keys:
        c = by_id.get(k)
        if c:
            cities.extend(c.get("member_city_ids") or [])
    ms["cluster_city_ids"] = sorted(set(cities))
    # Markets: replace uk market
    for m in dott.get("markets") or []:
        mid = m.get("id") or m.get("slug")
        if mid == "uk":
            m["id"] = "firth-of-clyde-scotland"
            m["slug"] = "firth-of-clyde-scotland"
            m["label"] = "Scotland — Firth of Clyde"
            m["summary"] = "Clyde waterfronts only — London and Liverpool not in current Dott evidence."
            m["anchor_cities"] = ["firth-of-clyde-scotland"]
    # footprint: replace uk
    nf = []
    for fp in dott.get("network_footprint") or []:
        if not isinstance(fp, dict):
            continue
        rid = fp.get("registry_key") or fp.get("id")
        if rid == "uk":
            nf.append({
                "id": "firth-of-clyde-scotland",
                "registry_key": "firth-of-clyde-scotland",
                "covered": True,
                "tier": "country_supported",
                "render": "geometry",
                "map_promote": True,
                "label": "Firth of Clyde",
                "region": "Europe",
            })
        else:
            nf.append(fp)
    dott["network_footprint"] = nf
    save(dott_path, dott)
    shutil.copyfile(dott_path, ROOT / "partner-pitch/partners/dott.json")

    # Voi: uk → london + clyde; no mersey/hebrides; no MENA
    voi_path = DC / "partners/voi.json"
    voi = load(voi_path)
    ms = voi.setdefault("_map_scope", {})
    old_keys = list(ms.get("registry_keys") or [])
    new_keys = rewrite_registry(
        old_keys,
        replace={"uk": ["london-thames-uk", "firth-of-clyde-scotland"]},
        remove={"uae", "hong-kong-macau", "saudi-arabia"},
    )
    if "switzerland" not in new_keys:
        new_keys.append("switzerland")
    ms["registry_keys"] = new_keys
    ms["union_legacy_city_ids"] = False
    ms["_uk_decompose"] = {
        "inherits": ["london-thames-uk", "firth-of-clyde-scotland"],
        "excludes": ["liverpool-mersey-uk", "scotland-hebrides"],
        "reason": "Voi supports London and Glasgow; not Liverpool",
    }
    cities = []
    for k in new_keys:
        c = by_id.get(k)
        if c:
            cities.extend(c.get("member_city_ids") or [])
    ms["cluster_city_ids"] = sorted(set(cities))
    for m in voi.get("markets") or []:
        mid = m.get("id") or m.get("slug")
        if mid == "uk":
            m["id"] = "uk-water-systems"
            m["slug"] = "uk-water-systems"
            m["label"] = "UK — London Thames & Firth of Clyde"
            m["summary"] = "London and Clyde only — Liverpool not in current Voi evidence."
            m["anchor_cities"] = ["london-thames-uk", "firth-of-clyde-scotland"]
    nf = []
    for fp in voi.get("network_footprint") or []:
        if not isinstance(fp, dict):
            continue
        rid = fp.get("registry_key") or fp.get("id")
        if rid == "uk":
            nf.append({
                "id": "london-thames-uk",
                "registry_key": "london-thames-uk",
                "covered": True,
                "tier": "country_supported",
                "render": "geometry",
                "map_promote": True,
                "label": "London Thames",
                "region": "Europe",
            })
            nf.append({
                "id": "firth-of-clyde-scotland",
                "registry_key": "firth-of-clyde-scotland",
                "covered": True,
                "tier": "country_supported",
                "render": "geometry",
                "map_promote": True,
                "label": "Firth of Clyde",
                "region": "Europe",
            })
        elif rid in ("uae", "dubai-uae"):
            continue
        else:
            nf.append(fp)
    voi["network_footprint"] = nf
    save(voi_path, voi)
    shutil.copyfile(voi_path, ROOT / "partner-pitch/partners/voi.json")

    # DiDi: replace hong-kong-macau with hong-kong
    didi_path = DC / "partners/didi.json"
    didi = load(didi_path)
    ms = didi.setdefault("_map_scope", {})
    keys = list(ms.get("registry_keys") or [])
    keys = ["hong-kong" if k in ("hong-kong-macau", "hong-kong") else k for k in keys]
    if "hong-kong" not in keys:
        # city key may be hong-kong in footprint
        keys.append("hong-kong")
    # also normalize city-style keys that resolve via aliases
    keys = list(dict.fromkeys(keys))
    # remove macau
    keys = [k for k in keys if k not in ("macau", "macau-china", "hong-kong-macau")]
    if "hong-kong" not in keys:
        keys.append("hong-kong")
    ms["registry_keys"] = keys
    ms["union_legacy_city_ids"] = False
    held = ms.setdefault("_held", {})
    held["macau-china"] = "Macau held — no current DiDi passenger-operation evidence; not inherited from Hong Kong"
    held["hong-kong-macau"] = "deprecated combined cluster — use hong-kong only for DiDi"
    cities = []
    for k in keys:
        c = by_id.get(k)
        if c:
            cities.extend(c.get("member_city_ids") or [])
        elif k == "hong-kong":
            cities.append("hong-kong")
    # include footprint city keys that are cities
    ms["cluster_city_ids"] = sorted(set(cities))
    # footprint entries
    nf = []
    for fp in didi.get("network_footprint") or []:
        if not isinstance(fp, dict):
            continue
        rid = fp.get("registry_key") or fp.get("id")
        if rid in ("hong-kong-macau", "macau", "macau-china"):
            continue
        if rid == "hong-kong" or "hong-kong" in str(rid):
            nf.append({
                "id": "hong-kong",
                "registry_key": "hong-kong",
                "covered": True,
                "tier": "corridor_ready",
                "render": "geometry",
                "map_promote": True,
                "label": "Hong Kong",
                "region": "East Asia",
            })
        else:
            nf.append(fp)
    # ensure hk present
    if not any((x.get("registry_key") or x.get("id")) == "hong-kong" for x in nf if isinstance(x, dict)):
        nf.append({
            "id": "hong-kong",
            "registry_key": "hong-kong",
            "covered": True,
            "tier": "corridor_ready",
            "render": "geometry",
            "map_promote": True,
            "label": "Hong Kong",
            "region": "East Asia",
        })
    didi["network_footprint"] = nf
    # markets hong-kong featured may exist
    for m in didi.get("markets") or []:
        mid = m.get("id") or m.get("slug")
        if mid in ("hong-kong", "hong-kong-macau"):
            m["id"] = "hong-kong"
            m["slug"] = "hong-kong"
            m["label"] = "Hong Kong"
            caveats = m.get("_operation_caveats") or []
            caveats.append("Macau excluded — not inherited from former hong-kong-macau cluster")
            m["_operation_caveats"] = list(dict.fromkeys(caveats))
    save(didi_path, didi)
    shutil.copyfile(didi_path, ROOT / "partner-pitch/partners/didi.json")

    # ─── 6. Count verification ──────────────────────────────────────────
    def count_for_keys(keys: list[str]) -> int:
        ks = set(keys)
        n = 0
        for f in routes:
            p = f.get("properties") or {}
            if p.get("_quarantine") or p.get("relevance") == "hide":
                continue
            if p.get("cluster_id") in ks:
                n += 1
        return n

    dott_n = count_for_keys(load(dott_path)["_map_scope"]["registry_keys"])
    voi_n = count_for_keys(load(voi_path)["_map_scope"]["registry_keys"])
    didi_keys = load(didi_path)["_map_scope"]["registry_keys"]
    # expand city-level keys via MARKET aliases not needed if we use clusters
    didi_n = count_for_keys(didi_keys)
    # if hong-kong is key, count hong-kong cluster
    if "hong-kong" in didi_keys:
        pass

    receipt["partner_route_counts"] = {
        "dott": dott_n,
        "voi": voi_n,
        "didi": didi_n,
        "didi_expected_with_hk": "767 - 0 + 37 = 804 if prior had no hk-macau; else verify",
        "didi_keys": didi_keys,
    }
    receipt["wave1_new_geography"] = {
        "status": "held",
        "reason": "All Wave1 candidate BP coordinates are null in research ledgers; null beats inventing coords",
        "held_lanes": [
            "be-ch Belgium/Basel/Zurich mint",
            "uk-de Solent/Severn/Germany depth mint",
            "nordics new city mint",
            "voi-lehavre-dott-poland mint",
            "dott-at-hu-balearics mint",
        ],
    }

    # save data
    save(ROUTES, routes)
    save(CLUSTERS, clusters_doc)
    save(FEATURES, feats)

    # gates
    gates = {}
    for name, args in [
        ("gate_g", [sys.executable, str(ROOT / "scripts/audit_partner_copy.py")]),
        (
            "inheritance",
            [
                sys.executable,
                str(ROOT / "scripts/validate_partner_inheritance.py"),
                "--partner",
                "didi",
                "dott",
                "voi",
                "--strict",
                "--json",
            ],
        ),
        ("fidelity_didi", [sys.executable, str(ROOT / "scripts/audit_proposal_fidelity.py"), "--partner", "didi"]),
        ("fidelity_dott", [sys.executable, str(ROOT / "scripts/audit_proposal_fidelity.py"), "--partner", "dott"]),
        ("fidelity_voi", [sys.executable, str(ROOT / "scripts/audit_proposal_fidelity.py"), "--partner", "voi"]),
    ]:
        try:
            r = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=300)
            gates[name] = {
                "exit": r.returncode,
                "pass": r.returncode == 0,
                "tail": (r.stdout or r.stderr or "")[-600:],
            }
        except Exception as e:
            gates[name] = {"pass": False, "error": str(e)}

    # linkage
    try:
        r = subprocess.run(
            ["node", str(ROOT / "scripts/audit-partner-route-linkage.mjs"), "--strict"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=120,
        )
        gates["linkage"] = {"exit": r.returncode, "pass": r.returncode == 0, "tail": (r.stdout or r.stderr or "")[-500:]}
    except Exception as e:
        gates["linkage"] = {"pass": False, "error": str(e)}

    receipt["gates"] = gates
    save(OUT / "GROK-WAVE1-P0-DIDI-HK-SEAL-RECEIPT-2026-07-10.json", receipt)
    md = [
        "# Grok — Wave1 P0 + DiDi HK seal",
        "",
        f"**UTC:** {receipt['at']}",
        f"**Status:** `{receipt['status']}`",
        "",
        "## Lake Geneva",
        f"- Retagged **{len(geneva)}** routes indonesia → switzerland",
        "",
        "## UK decompose",
        f"- London: **{len(uk_counts['london-thames-uk'])}**",
        f"- Mersey: **{len(uk_counts['liverpool-mersey-uk'])}**",
        f"- Clyde: **{len(uk_counts['firth-of-clyde-scotland'])}**",
        f"- Hebrides/CalMac: **{len(uk_counts['scotland-hebrides'])}**",
        "- Dott inherits: Clyde only",
        "- Voi inherits: London + Clyde (not Mersey/Hebrides)",
        "",
        "## Ibiza",
        f"- Reused **{len(ibiza_routes)}** existing routes; no mint",
        "",
        "## Hong Kong / Macau",
        f"- HK visible: **{len(hk_ids)}**; Macau visible: **{len(mc_ids)}**",
        "- DiDi inherits **hong-kong only**",
        "",
        "## Partner route counts (visible ∩ keys)",
        f"- Dott: {dott_n}",
        f"- Voi: {voi_n}",
        f"- DiDi: {didi_n}",
        "",
        "## Wave1 new geography",
        "- **HELD** — all candidate BP coordinates null in research ledgers",
        "",
        "## Gates",
    ]
    for k, v in gates.items():
        md.append(f"- **{k}:** {'PASS' if v.get('pass') else 'FAIL'}")
    md.append("")
    md.append("Machine: `GROK-WAVE1-P0-DIDI-HK-SEAL-RECEIPT-2026-07-10.json`")
    (OUT / "GROK-WAVE1-P0-DIDI-HK-SEAL-RECEIPT-2026-07-10.md").write_text("\n".join(md) + "\n")

    print(json.dumps({
        "geneva": len(geneva),
        "uk": {k: len(v) for k, v in uk_counts.items()},
        "hk": len(hk_ids),
        "macau": len(mc_ids),
        "counts": receipt["partner_route_counts"],
        "gates": {k: v.get("pass") for k, v in gates.items()},
    }, indent=2))
    return 0 if all(gates.get(k, {}).get("pass") for k in ("gate_g", "inheritance", "fidelity_didi", "fidelity_dott", "fidelity_voi", "linkage")) else 1


if __name__ == "__main__":
    raise SystemExit(main())
