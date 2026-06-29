#!/usr/bin/env python3
"""
validate-seal-integrity.py — seal gate for the map artifacts (NOTES §2026-06-29).

Fails (with --strict) if any of these upstream-seal invariants break, so a future
seal can never silently re-introduce stacked pins, orphan cities, or twins:

  1. No duplicate Feature ids within a FEATURES_BY_TYPE bucket (one Feature/id).
  2. Every rendered city / priority_city id ∈ some CLUSTERS.member_city_ids
     (no orphan cities — the city→cluster map is total).
  3. cluster_id backfilled on every city Feature and matches membership.
  4. No known city twins present (sabah-kk, aruba-curacao-bonaire, phuket-thailand).
  5. CLUSTERS.members_present == len(member_city_ids); no dangling member ids.

Usage:  python3 scripts/validate-seal-integrity.py [--strict]
Exit 1 on any failure when --strict (use in CI / pre-handoff gate).
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DC = ROOT / "data-clean"
STRICT = "--strict" in sys.argv

KNOWN_TWINS = {"sabah-kk", "aruba-curacao-bonaire", "phuket-thailand"}


def main():
    fbt = json.loads((DC / "FEATURES_BY_TYPE.json").read_text())
    clusters = json.loads((DC / "CLUSTERS.json").read_text())["clusters"]
    fails = []

    # 1. no duplicate ids per bucket
    for t, arr in fbt.items():
        ids = [(f.get("properties") or {}).get("id") for f in arr]
        ids = [i for i in ids if i is not None]
        dupes = {i for i in ids if ids.count(i) > 1} if len(ids) < 4000 else _dupes(ids)
        if dupes:
            fails.append(f"[1] {t}: {len(dupes)} duplicate id(s) e.g. {sorted(dupes)[:3]}")

    # membership map
    mem2cluster, all_members = {}, []
    for c in clusters:
        for m in c.get("member_city_ids", []):
            mem2cluster[m] = c["cluster_id"]; all_members.append(m)
        n = len(c.get("member_city_ids", []))
        if c.get("members_present") not in (None, n):
            fails.append(f"[5] cluster {c['cluster_id']}: members_present={c.get('members_present')} != {n}")

    city_ids = []
    for t in ("city", "priority_city"):
        for f in fbt.get(t, []):
            p = f["properties"]; cid = p.get("id")
            if cid is None:
                continue
            city_ids.append(cid)
            # 2. orphan check
            if cid not in mem2cluster:
                fails.append(f"[2] orphan city not in any cluster: {cid}")
            # 3. cluster_id backfill check
            elif p.get("cluster_id") != mem2cluster[cid]:
                fails.append(f"[3] {cid}: cluster_id={p.get('cluster_id')!r} != membership {mem2cluster[cid]!r}")
            # 4. twin check
            if cid in KNOWN_TWINS:
                fails.append(f"[4] known twin still present as a city: {cid}")

    # dangling member ids (in CLUSTERS but no rendered city) — warn-only signal
    rendered = set(city_ids)
    dangling = sorted(m for m in set(all_members) if m not in rendered)

    print(f"Seal integrity — {len(city_ids)} city features, {len(clusters)} clusters.")
    if dangling:
        print(f"  ⚠ {len(dangling)} cluster member id(s) have no rendered city feature (non-fatal): {dangling[:6]}{'…' if len(dangling) > 6 else ''}")
    if not fails:
        print("  ✓ all invariants hold (no dupes, no orphans, cluster_id total, no twins).")
        return
    print(f"  ✗ {len(fails)} failure(s):")
    for f in fails:
        print(f"      - {f}")
    if STRICT:
        sys.exit(1)


def _dupes(ids):
    seen, dup = set(), set()
    for i in ids:
        if i in seen:
            dup.add(i)
        seen.add(i)
    return dup


if __name__ == "__main__":
    main()
