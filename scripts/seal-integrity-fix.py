#!/usr/bin/env python3
"""
seal-integrity-fix.py — one-shot, idempotent repair of the sealed map artifacts.

Resolves the upstream-seal defects flagged in docs/NOTES-FOR-TASKLET.md (§2026-06-29):

  B1  Dedupe FEATURES_BY_TYPE — exactly one Feature per (type, id).  The `city`
      array shipped ~8 stacked rows per id (mesh build artifact) → inflated map
      counts + stacked MapLibre pins.
  B3  Backfill properties.cluster_id on every city / priority_city Feature from
      CLUSTERS.member_city_ids (the authoritative city→cluster map).
  B4  Merge city twins into their canonical node, re-homing the twin's boarding
      points (sabah-kk → sabah-kota-kinabalu-malaysia; the legacy fused
      aruba-curacao-bonaire → the de-fused ABC island nearest each BP).
  B5  Create the `algeria` cluster and bind the real coastal cities that were
      orphaned from CLUSTERS.member_city_ids (Algeria / Kenya / Cyprus / Croatia
      / Morocco-Rabat) so every rendered city resolves to a cluster.

Run from repo root:  python3 scripts/seal-integrity-fix.py
Re-running is a no-op once clean.  Validate with scripts/validate-seal-integrity.py.
"""
import json, math, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DC = ROOT / "data-clean"
CL_PATH = DC / "CLUSTERS.json"
FBT_PATH = DC / "FEATURES_BY_TYPE.json"

# macro-region aliases — mirror REGION_ALIASES in scripts/region-share.mjs (and the
# _REGION_DISPLAY_ALIAS map in index.html). Used only to detect TRUE macro-region
# contradictions in B3b; raw-string variants within one macro region are left alone.
_REGION_ALIASES = {
    "SEA": "Southeast Asia",
    "LatAm-Caribbean": "Latin America", "Latin-America": "Latin America",
    "Caribbean": "Caribbean",
    "Europe-Mediterranean": "Europe", "Europe-Atlantic": "Europe",
    "Europe-Baltic": "Europe", "Europe-Med": "Europe",
    "Asia": "East Asia",
    "Middle East": "MENA", "Maghreb": "MENA",
    "Caucasus": "Caspian", "Central Asia": "Caspian",
}
def _norm_region(r):
    return _REGION_ALIASES.get(r, r)

# ── twin merges: legacy / duplicate city id → canonical city id ──────────────
# A flat twin re-homes ALL its boarding points to the single canonical city.
SIMPLE_TWINS = {
    "sabah-kk": "sabah-kota-kinabalu-malaysia",
}
# A fused legacy node de-fused into several real cities; re-home each BP to the
# geographically nearest constituent (by city-anchor haversine).
SPLIT_TWINS = {
    "aruba-curacao-bonaire": ["aruba-aruba", "curacao-curacao", "bonaire-bonaire"],
}

# ── new cluster: Algeria (Maghreb). Tag-only — boarding points + pins, no sealed
#    hero corridor yet (0 routes). ────────────────────────────────────────────
ALGERIA_CLUSTER = {
    "cluster_id": "algeria",
    "cluster_label": "Algeria",
    "region": "Maghreb",
    "type": "coastal",
    "anchor": [3.0588, 36.7538],  # Algiers
    "member_city_ids": [
        "algiers-algeria", "oran-algeria", "bejaia-algeria", "mostaganem-algeria",
    ],
    "members_present": 4,
    "members_missing": [],
    "anchor_source": "algiers-algeria",
    "anchor_lb174_note": "Created in seal-integrity-fix (NOTES §2026-06-29 P2): bind 4 orphaned Algerian coastal city nodes to a real cluster.",
}

# ── orphan → existing-cluster binding (real cities missing from membership) ──
BIND_TO_CLUSTER = {
    "kenya":   ["diani-ukunda-kenya", "kilifi-kenya", "malindi-kenya", "watamu-kenya"],
    "cyprus":  ["ayia-napa-cyprus", "paphos-cyprus"],
    "croatia": ["zadar-croatia"],
    "morocco": ["rabat-sale-morocco"],
}


def haversine(a, b):
    R = 6371.0
    lon1, lat1, lon2, lat2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    dlon, dlat = lon2 - lon1, lat2 - lat1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def main():
    clusters_doc = json.loads(CL_PATH.read_text())
    fbt = json.loads(FBT_PATH.read_text())
    changed = []

    # coords for every city/priority_city id (for split-twin nearest assignment)
    coords = {}
    for t in ("city", "priority_city"):
        for f in fbt.get(t, []):
            pid = f["properties"].get("id")
            if pid:
                coords[pid] = f["geometry"]["coordinates"]

    # ── B4: re-home boarding points off the twins, then drop the twin cities ──
    pois = fbt.get("poi", [])
    rehomed = 0
    for f in pois:
        p = f["properties"]
        parent = p.get("parent_city_id")
        if parent in SIMPLE_TWINS:
            p["parent_city_id"] = SIMPLE_TWINS[parent]; rehomed += 1
        elif parent in SPLIT_TWINS:
            cands = [c for c in SPLIT_TWINS[parent] if c in coords]
            here = f["geometry"]["coordinates"]
            nearest = min(cands, key=lambda c: haversine(here, coords[c]))
            p["parent_city_id"] = nearest; rehomed += 1
    if rehomed:
        changed.append(f"B4: re-homed {rehomed} boarding points off twin parents")

    twin_ids = set(SIMPLE_TWINS) | set(SPLIT_TWINS)
    for t in ("city", "priority_city"):
        before = len(fbt.get(t, []))
        fbt[t] = [f for f in fbt[t] if f["properties"].get("id") not in twin_ids]
        if len(fbt[t]) != before:
            changed.append(f"B4: dropped {before - len(fbt[t])} twin {t} feature(s)")

    # ── B1: dedupe — one Feature per (type, id), first occurrence wins ────────
    for t in list(fbt.keys()):
        seen, kept = set(), []
        for f in fbt[t]:
            pid = (f.get("properties") or {}).get("id")
            if pid is None:
                kept.append(f); continue
            if pid in seen:
                continue
            seen.add(pid); kept.append(f)
        if len(kept) != len(fbt[t]):
            changed.append(f"B1: {t} {len(fbt[t])} → {len(kept)} rows ({len(fbt[t]) - len(kept)} dupes dropped)")
        fbt[t] = kept

    # ── B5 + orphan binding: CLUSTERS membership ──────────────────────────────
    by_id = {c["cluster_id"]: c for c in clusters_doc["clusters"]}
    if "algeria" not in by_id:
        clusters_doc["clusters"].append(json.loads(json.dumps(ALGERIA_CLUSTER)))
        by_id["algeria"] = clusters_doc["clusters"][-1]
        changed.append("B5: created algeria cluster (4 cities)")
    for cid, adds in BIND_TO_CLUSTER.items():
        c = by_id.get(cid)
        if not c:
            print(f"  ! bind target cluster '{cid}' not found — skipped", file=sys.stderr); continue
        new = [a for a in adds if a not in c["member_city_ids"]]
        if new:
            c["member_city_ids"].extend(new)
            c["members_present"] = len(c["member_city_ids"])
            changed.append(f"bind: +{len(new)} → {cid} ({', '.join(new)})")

    # ── normalize members_present = len(member_city_ids) on every cluster ─────
    for c in clusters_doc["clusters"]:
        n = len(c.get("member_city_ids", []))
        if c.get("members_present") != n:
            c["members_present"] = n
            changed.append(f"members_present fixed: {c['cluster_id']} → {n}")

    # ── B3: backfill cluster_id from authoritative membership ─────────────────
    mem2cluster = {}
    for c in clusters_doc["clusters"]:
        for m in c.get("member_city_ids", []):
            mem2cluster[m] = c["cluster_id"]
    backfilled = 0
    for t in ("city", "priority_city"):
        for f in fbt.get(t, []):
            pid = f["properties"].get("id")
            cid = mem2cluster.get(pid)
            if cid and f["properties"].get("cluster_id") != cid:
                f["properties"]["cluster_id"] = cid; backfilled += 1
    if backfilled:
        changed.append(f"B3: cluster_id set/updated on {backfilled} city features")

    # ── B3b: a city's region must not contradict its own cluster ──────────────
    # Cluster membership is authoritative (same basis as B3), so a city Feature's
    # `region` is forced to equal its cluster's `region`. This keeps the macro-
    # region rollup self-consistent (share-card count == browse-panel grid). It is
    # NOT a macro-region re-judgement: the city simply inherits the EXISTING cluster
    # tag. The cluster-level macro-region tags themselves (e.g. the North-Africa
    # spread: morocco=Africa / algeria=Maghreb / tunisia=Europe) are left untouched
    # and flagged for human normalisation in the handback.
    cl_region = {c["cluster_id"]: c.get("region") for c in clusters_doc["clusters"]}
    region_fixed = []
    for t in ("city", "priority_city"):
        for f in fbt.get(t, []):
            cid = f["properties"].get("cluster_id")
            creg = cl_region.get(cid)
            freg = f["properties"].get("region")
            # Only realign when the MACRO region disagrees (true contradiction); leave benign
            # raw-string variants within the same macro region (e.g. Europe-Med vs Europe-Mediterranean) alone.
            if creg and _norm_region(freg) != _norm_region(creg):
                f["properties"]["region"] = creg
                region_fixed.append(f["properties"].get("id"))
    if region_fixed:
        changed.append(f"B3b: macro-region aligned to cluster on {len(region_fixed)} city feature(s): {', '.join(region_fixed)}")

    CL_PATH.write_text(json.dumps(clusters_doc, ensure_ascii=False, indent=2) + "\n")
    FBT_PATH.write_text(json.dumps(fbt, ensure_ascii=False, indent=2) + "\n")

    if changed:
        print("seal-integrity-fix applied:")
        for c in changed:
            print(f"  • {c}")
    else:
        print("seal-integrity-fix: already clean — no changes.")


if __name__ == "__main__":
    main()
