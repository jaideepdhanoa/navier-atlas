#!/usr/bin/env python3
"""DiDi ex-China #210 — G0 scope repair + G1 foreign route-stamp hygiene.

G0: remove mainland China / Macau overclaim; strip non-city IDs from city arrays;
     rebuild footprint/map_scope from approved P0 roster (no Chile/Argentina invent).
G1: restamp 77 foreign cluster stamps (Mexico/Galápagos/NZ) to endpoint-correct clusters.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
P0 = ROOT / "handoff/didi-ex-china/DIDI-P0-NO-SHRINK-BASELINE-2026-07-09.json"
STAMP = ROOT / "handoff/didi-ex-china/DIDI-ROUTE-STAMP-DEFECT-LEDGER-2026-07-09.json"
CROSSWALK = ROOT / "handoff/didi-ex-china/DIDI-ANCHOR-CITY-CROSSWALK-2026-07-09.json"
ROUTES = ROOT / "data-clean/ROUTES.json"
CLUSTERS = ROOT / "data-clean/CLUSTERS.json"
PARTNERS = [
    ROOT / "partner-pitch/partners/didi.json",
    ROOT / "data-clean/partners/didi.json",
]
RECEIPT = ROOT / "handoff/didi-ex-china/G0-G1-RECEIPT-2026-07-09.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load(p: Path) -> Any:
    return json.loads(p.read_text())


def save(p: Path, obj: Any) -> None:
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def load_clusters() -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    raw = load(CLUSTERS)
    if isinstance(raw, dict) and "clusters" in raw:
        items = raw["clusters"]
    elif isinstance(raw, list):
        items = raw
    else:
        items = [v for v in raw.values() if isinstance(v, dict)] if isinstance(raw, dict) else []
    members: dict[str, set[str]] = {}
    city_to: dict[str, set[str]] = defaultdict(set)
    for c in items:
        if not isinstance(c, dict):
            continue
        cid = c.get("cluster_id") or c.get("id")
        mems = set(c.get("member_city_ids") or c.get("cities") or [])
        members[cid] = mems
        for m in mems:
            city_to[m].add(cid)
    return members, city_to


def g0_repair(doc: dict, p0: dict) -> dict:
    """Return before/after snapshot and mutate doc in place."""
    before = {
        "network_footprint_ids": [
            (x.get("id") if isinstance(x, dict) else x) for x in (doc.get("network_footprint") or [])
        ],
        "map_scope_registry_keys": list((doc.get("_map_scope") or {}).get("registry_keys") or []),
        "map_scope_cluster_city_ids": list((doc.get("_map_scope") or {}).get("cluster_city_ids") or []),
        "market_ids": [
            (m.get("id") if isinstance(m, dict) else m) for m in (doc.get("markets") or [])
        ],
    }

    approved_cities = list(p0["approved_target"]["approved_existing_city_ids"])
    held = set(p0["approved_target"].get("held_city_ids") or [])
    # Macau + Taiwan held; mainland never
    remove_ids = {"shanghai-china", "macau-china"} | held
    # non-city market IDs that leaked into city arrays
    non_city = {
        "mexico-caribbean",
        "mexico-pacific",
        "brazil",
        "colombia",
        "panama",
        "costa-rica",
        "dominican-republic",
        "mexico",
        "hong-kong-macau",  # cluster key — keep only as registry if HK handled carefully
    }

    # --- network_footprint: drop Shanghai/Macau; keep current LatAm markets + cities ---
    new_fp: list = []
    seen: set[str] = set()
    for x in doc.get("network_footprint") or []:
        if isinstance(x, dict):
            xid = x.get("id") or x.get("registry_key")
        else:
            xid = x
        if not xid or xid in remove_ids or xid in seen:
            continue
        # drop pure mainland china footprints
        if "shanghai" in xid or xid.endswith("-china") and xid not in ("macau-china",):
            # macau already in remove; any other *china mainland
            if xid != "hong-kong" and "macau" not in xid:
                if "china" in xid and xid not in ("macau-china",):
                    continue
        seen.add(xid)
        if isinstance(x, dict):
            new_fp.append(x)
        else:
            new_fp.append({"id": xid, "registry_key": xid, "covered": True, "tier": "market"})

    # ensure approved cities present as footprint seeds (additive no-shrink)
    for cid in approved_cities:
        if cid in seen or cid in remove_ids:
            continue
        seen.add(cid)
        new_fp.append(
            {
                "id": cid,
                "registry_key": cid,
                "covered": True,
                "tier": "city",
                "_g0_seed": "approved_existing_city_ids",
            }
        )

    # Hong Kong city without Macau claim
    if "hong-kong" not in seen:
        new_fp.append(
            {
                "id": "hong-kong",
                "registry_key": "hong-kong",
                "covered": True,
                "tier": "city",
                "_g0_note": "HK city-level only — no Macau overclaim via hong-kong-macau cluster",
            }
        )
        seen.add("hong-kong")

    doc["network_footprint"] = new_fp

    # --- _map_scope: city-level approved roster only (no Macau, no Shanghai, no market IDs) ---
    city_ids = [c for c in approved_cities if c not in remove_ids]
    if "hong-kong" not in city_ids:
        city_ids.append("hong-kong")

    # Registry keys: existing LatAm markets + cluster seeds that do NOT force Macau
    # Do NOT include hong-kong-macau or shanghai-china clusters.
    registry_keys = []
    for k in (
        "brazil",
        "mexico",
        "mexico-caribbean",
        "mexico-pacific",
        "colombia",
        "costa-rica",
        "panama",
        "dominican-republic",
        "galapagos-ecuador",
        "peru",
        "australia",
        "new-zealand",
        "japan",
        "egypt",
        # taiwan held — omit cluster until verification
    ):
        registry_keys.append(k)
    # city-level anchors also as registry for inheritance
    for c in city_ids:
        if c not in registry_keys:
            registry_keys.append(c)

    doc["_map_scope"] = {
        "_doc": "G0 ex-China scope repair (#210) — live city roster without mainland China / Macau overclaim",
        "generated": utc_now(),
        "source": "g0_didi_ex_china_scope_repair",
        "registry_keys": registry_keys,
        "cluster_city_ids": city_ids,
        "inheritance_policy": "approved_city_roster_no_macau_no_mainland",
        "_held": {
            "macau-china": "shared hong-kong-macau cluster — no DiDi Macau proof; city-level HK only",
            "kaohsiung-taiwan": "Taiwan verification gate",
            "penghu-taiwan": "Taiwan verification gate",
            "shanghai-china": "mainland China excluded",
        },
        "_scope_conflict": {
            "hong_kong_macau_cluster": (
                "Cluster hong-kong-macau includes Macau. G0 uses city-level hong-kong only "
                "so Macau is not inherited. Do not re-add hong-kong-macau registry key without "
                "Macau proof or a Macau-free cluster split."
            )
        },
    }

    # Strip mainland/macau mentions from top-level coverage_note if present
    note = doc.get("coverage_note")
    if isinstance(note, str) and ("shanghai" in note.lower() or "macau" in note.lower()):
        doc["coverage_note"] = (
            note
            + " [G0 2026-07-09: mainland China and Macau removed from operating footprint.]"
        )

    after_fp = [
        (x.get("id") if isinstance(x, dict) else x) for x in (doc.get("network_footprint") or [])
    ]
    after_cities = list(doc["_map_scope"]["cluster_city_ids"])
    after = {
        "network_footprint_ids": after_fp,
        "map_scope_registry_keys": list(doc["_map_scope"]["registry_keys"]),
        "map_scope_cluster_city_ids": after_cities,
        "market_ids": before["market_ids"],
        "removed_from_footprint": sorted(set(before["network_footprint_ids"]) - set(after_fp)),
        "removed_from_city_ids": sorted(
            set(before["map_scope_cluster_city_ids"]) - set(after_cities)
        ),
    }
    return {"before": before, "after": after}


def g1_restamp(city_to: dict[str, set[str]]) -> dict:
    stamp = load(STAMP)
    foreign: list[dict] = []
    for cl in stamp.get("clusters") or []:
        for r in cl.get("foreign_stamped_routes") or []:
            foreign.append({**r, "wrong_cluster": cl["cluster_id"]})

    raw = load(ROUTES)
    feats = raw if isinstance(raw, list) else raw.get("features") or []
    by_idx = {}
    for i, f in enumerate(feats):
        rid = (f.get("properties") or {}).get("id")
        if rid:
            by_idx[rid] = i

    def pick(from_c: str | None, to_c: str | None, wrong: str) -> str | None:
        fc = city_to.get(from_c or "") or set()
        tc = city_to.get(to_c or "") or set()
        both = fc & tc
        if both:
            # prefer not the wrong stamp
            prefs = sorted(c for c in both if c != wrong)
            return prefs[0] if prefs else sorted(both)[0]
        if fc:
            prefs = sorted(c for c in fc if c != wrong)
            return prefs[0] if prefs else sorted(fc)[0]
        if tc:
            prefs = sorted(c for c in tc if c != wrong)
            return prefs[0] if prefs else sorted(tc)[0]
        return None

    changed = []
    held = []
    by_wrong = Counter()
    by_new = Counter()

    for row in foreign:
        rid = row["route_id"]
        i = by_idx.get(rid)
        if i is None:
            held.append({"route_id": rid, "reason": "missing_from_ROUTES"})
            continue
        props = feats[i].setdefault("properties", {})
        fr = props.get("from_city_id") or row.get("from_city_id")
        to = props.get("to_city_id") or row.get("to_city_id")
        wrong = row["wrong_cluster"]
        new_c = pick(fr, to, wrong)
        old = props.get("cluster_id")
        if not new_c:
            held.append({"route_id": rid, "reason": "no_cluster_for_endpoints", "from": fr, "to": to})
            continue
        if old == new_c:
            continue
        props["cluster_id"] = new_c
        props["_cluster_restamp"] = {
            "at": utc_now(),
            "from": old,
            "to": new_c,
            "reason": "didi_ex_china_g1_foreign_stamp",
            "wrong_was": wrong,
        }
        changed.append(
            {
                "route_id": rid,
                "from_city_id": fr,
                "to_city_id": to,
                "cluster_before": old,
                "cluster_after": new_c,
                "wrong_cluster": wrong,
            }
        )
        by_wrong[wrong] += 1
        by_new[new_c] += 1

    # one-endpoint review — do not auto-delete; leave with note
    one_ep = []
    for cl in stamp.get("clusters") or []:
        for r in cl.get("one_endpoint_review_routes") or []:
            one_ep.append({"cluster": cl["cluster_id"], **r})

    if changed:
        if isinstance(raw, list):
            save(ROUTES, feats)
        else:
            raw["features"] = feats
            save(ROUTES, raw)

    return {
        "foreign_input": len(foreign),
        "changed": len(changed),
        "held": held,
        "by_wrong_cluster": dict(by_wrong),
        "by_new_cluster": dict(by_new.most_common()),
        "changed_sample": changed[:15],
        "changed_all_ids": [c["route_id"] for c in changed],
        "one_endpoint_review": one_ep,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--g0-only", action="store_true")
    ap.add_argument("--g1-only", action="store_true")
    args = ap.parse_args()

    p0 = load(P0)
    _, city_to = load_clusters()

    receipt: dict[str, Any] = {
        "at": utc_now(),
        "pr": 210,
        "spec": "handoff/didi-ex-china/GROK-SPEC-didi-ex-china-grand-slam-2026-07-09.md",
        "mode": "apply" if args.apply else "dry-run",
    }

    if not args.g1_only:
        # G0 on both partner copies
        g0_reports = []
        for path in PARTNERS:
            doc = load(path)
            before_fp = len(doc.get("network_footprint") or [])
            rep = g0_repair(doc, p0)
            g0_reports.append({"path": str(path.relative_to(ROOT)), **rep})
            if args.apply:
                save(path, doc)
            print(
                f"G0 {path.name}: footprint {before_fp}→{len(doc.get('network_footprint') or [])} "
                f"cities {len(rep['after']['map_scope_cluster_city_ids'])}"
            )
        receipt["g0"] = {
            "partners": g0_reports,
            "shanghai_removed": True,
            "macau_overclaim_prevented": True,
            "taiwan_held": True,
        }

    if not args.g0_only:
        if args.apply:
            g1 = g1_restamp(city_to)
        else:
            # dry: count only
            stamp = load(STAMP)
            n = sum(len(cl.get("foreign_stamped_routes") or []) for cl in stamp.get("clusters") or [])
            g1 = {"foreign_input": n, "changed": 0, "note": "dry-run — pass --apply to restamp"}
        receipt["g1"] = g1
        print(f"G1 foreign stamps: input={g1.get('foreign_input')} changed={g1.get('changed')}")

    if args.apply:
        save(RECEIPT, receipt)
        print(f"wrote {RECEIPT}")
    else:
        print(json.dumps(receipt, indent=2, default=str)[:4000])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
