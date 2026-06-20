#!/usr/bin/env python3
"""Fix spurious Global region (sabah-kk twin) and surface Caribbean as its own L1 region."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DC = ROOT / "data-clean"

DELETE_CITIES = frozenset({"sabah-kk", "phuket-thailand"})
CITY_REMAP = {
    "sabah-kk": "sabah-kota-kinabalu-malaysia",
    "phuket-thailand": "phuket-phang-nga-thailand",
}


def load(p: Path):
    return json.loads(p.read_text())


def save(p: Path, obj):
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def remap_id(val: str | None) -> str | None:
    if not val:
        return val
    return CITY_REMAP.get(val, val)


def main():
    fbt = load(DC / "FEATURES_BY_TYPE.json")
    clusters = load(DC / "CLUSTERS.json")
    log: list[str] = []

    carib_members = set()
    latam_members = set()
    for cl in clusters.get("clusters", []):
        if cl.get("region") == "Caribbean":
            carib_members.update(cl.get("member_city_ids") or [])
        if cl.get("region") == "Latin-America":
            latam_members.update(cl.get("member_city_ids") or [])

    # 1. Delete duplicate city twins
    for tier in ("city", "priority_city"):
        before = len(fbt.get(tier, []))
        fbt[tier] = [
            f
            for f in fbt.get(tier, [])
            if (f.get("properties") or {}).get("id") not in DELETE_CITIES
        ]
        removed = before - len(fbt[tier])
        if removed:
            log.append(f"deleted {removed} from {tier}")

    # 2. Rewire parent_city_id / cluster references off deleted twins
    for tier in ("poi", "locale", "city", "priority_city"):
        for feat in fbt.get(tier, []):
            props = feat.get("properties") or {}
            for field in ("parent_city_id", "cluster_id"):
                old = props.get(field)
                new = remap_id(old)
                if new != old:
                    props[field] = new
                    log.append(f"{tier} {props.get('id')}: {field} {old} → {new}")
            if props.get("region") == "Global":
                props["region"] = "SEA"
                props["country"] = "Malaysia"
                log.append(f"{tier} {props.get('id')}: region Global → SEA")

    # 3. Split LatAm-Caribbean → Caribbean vs Latin-America by cluster membership
    for tier in ("city", "priority_city"):
        for feat in fbt.get(tier, []):
            props = feat.get("properties") or {}
            cid = props.get("id")
            if not cid:
                continue
            if cid in carib_members and props.get("region") in ("LatAm-Caribbean", "Latin-America"):
                props["region"] = "Caribbean"
                log.append(f"{cid}: region → Caribbean")
            elif cid in latam_members and props.get("region") == "LatAm-Caribbean":
                props["region"] = "Latin-America"
                log.append(f"{cid}: region → Latin-America")

    # 4. CLUSTERS.json — scrub deleted ids from members
    for cl in clusters.get("clusters", []):
        orig = list(cl.get("member_city_ids") or [])
        cl["member_city_ids"] = [remap_id(i) for i in orig if remap_id(i) not in DELETE_CITIES]
        cl["member_city_ids"] = list(dict.fromkeys(cl["member_city_ids"]))
        if cl["member_city_ids"] != orig:
            cl["members_present"] = len(cl["member_city_ids"])
            log.append(f"cluster {cl['cluster_id']}: members scrubbed")

    save(DC / "FEATURES_BY_TYPE.json", fbt)
    save(DC / "CLUSTERS.json", clusters)

    # Audit
    global_cities = []
    region_counts: dict[str, int] = {}
    for tier in ("city", "priority_city"):
        for feat in fbt.get(tier, []):
            props = feat.get("properties") or {}
            r = props.get("region") or "?"
            region_counts[r] = region_counts.get(r, 0) + 1
            if r == "Global":
                global_cities.append(props.get("id"))

    print("── fix-global-caribbean-taxonomy ──")
    for line in log[:30]:
        print(" ", line)
    if len(log) > 30:
        print(f"  ... +{len(log) - 30} more")
    print(f"Global-tagged cities remaining: {global_cities}")
    print(f"Caribbean-tagged cities: {region_counts.get('Caribbean', 0)}")
    print(f"Latin-America-tagged cities: {region_counts.get('Latin-America', 0)}")


if __name__ == "__main__":
    main()