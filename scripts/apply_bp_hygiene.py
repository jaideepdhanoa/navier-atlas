#!/usr/bin/env python3
"""Apply handoff/bp-hygiene/BP-CLEANUP-REGISTER-2026-07-08.json to sealed graph.

Operating model: Tasklet flags · Grok applies · nobody invents a pier.

Actions:
  DROP_junk     — drop routes whose endpoints include junk BPs; drop matching POI
  RETAG         — restamp from_city_id/to_city_id + POI parent_city_id to nearest
  DUP_coord     — collapse exact-coord dups to one canonical BP id; rewire routes
  RELABEL       — apply deterministic label trims on route endpoint labels

Does NOT mint new boarding points. Writes a receipt under handoff/bp-hygiene/.
"""
from __future__ import annotations

import argparse
import json
import shutil
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DC = ROOT / "data-clean"
REGISTER = ROOT / "handoff" / "bp-hygiene" / "BP-CLEANUP-REGISTER-2026-07-08.json"
RECEIPT = ROOT / "handoff" / "bp-hygiene" / f"APPLY-RECEIPT-{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_routes():
    obj = json.loads((DC / "ROUTES.json").read_text())
    if isinstance(obj, dict) and "features" in obj:
        return obj, obj["features"]
    return {"type": "FeatureCollection", "features": obj}, obj


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--skip-drop", action="store_true", help="Only retag/dedupe/relabel")
    args = ap.parse_args()

    reg = json.loads(REGISTER.read_text())
    routes_obj, feats = load_routes()
    fbt = json.loads((DC / "FEATURES_BY_TYPE.json").read_text())
    pois = fbt.get("poi") or []

    drop_bps = {r["bp"] for r in reg.get("DROP_junk") or []}
    retag = {r["bp"]: r["nearest"] for r in reg.get("RETAG_city_mismatch") or [] if r.get("nearest")}
    relabel = {r["bp"]: r["suggest"] for r in reg.get("RELABEL_aggregate") or [] if r.get("suggest")}

    # DUP: pick canonical = first bp id that looks most stable (prefer city__slug or shorter)
    dup_map: dict[str, str] = {}  # alias -> canonical
    for row in reg.get("DUP_coord") or []:
        bps = list(row.get("bps") or [])
        if len(bps) < 2:
            continue
        # Prefer ids with __ (city-scoped) over bare labels; then lowest degree-agnostic lexical
        def score(b: str) -> tuple:
            return (0 if "__" in b else 1, 0 if b.startswith("bp-") else 1, len(b), b)

        canon = sorted(bps, key=score)[0]
        for b in bps:
            if b != canon:
                dup_map[b] = canon

    receipt = {
        "applied_at": utc_now(),
        "dry": args.dry,
        "input_register": str(REGISTER.relative_to(ROOT)),
        "routes_before": len(feats),
        "pois_before": len(pois),
        "drop_bp_count": len(drop_bps),
        "retag_count": len(retag),
        "dup_alias_count": len(dup_map),
        "relabel_count": len(relabel),
        "routes_dropped": 0,
        "routes_rewired": 0,
        "routes_retagged": 0,
        "routes_relabeled": 0,
        "pois_dropped": 0,
        "pois_retagged": 0,
        "dropped_route_ids": [],
        "notes": [],
    }

    def rewrite_bp(bid: str | None) -> str | None:
        if not bid:
            return bid
        # chain dups
        seen = set()
        while bid in dup_map and bid not in seen:
            seen.add(bid)
            bid = dup_map[bid]
        return bid

    new_feats = []
    for f in feats:
        p = f.get("properties") or {}
        fr, to = p.get("from"), p.get("to")
        # DROP
        if not args.skip_drop and ((fr in drop_bps) or (to in drop_bps)):
            receipt["routes_dropped"] += 1
            rid = p.get("id")
            if rid and len(receipt["dropped_route_ids"]) < 200:
                receipt["dropped_route_ids"].append(rid)
            continue

        changed = False
        # DUP rewire
        nfr, nto = rewrite_bp(fr), rewrite_bp(to)
        if nfr != fr or nto != to:
            p["from"], p["to"] = nfr, nto
            # keep from_node/to_node in sync if present
            if p.get("from_node") == fr:
                p["from_node"] = nfr
            if p.get("to_node") == to:
                p["to_node"] = nto
            receipt["routes_rewired"] += 1
            changed = True
            fr, to = nfr, nto

        # RETAG city_ids
        for end, cid_field in (("from", "from_city_id"), ("to", "to_city_id")):
            bid = p.get(end)
            if bid in retag:
                new_cid = retag[bid]
                if p.get(cid_field) != new_cid:
                    p[cid_field] = new_cid
                    receipt["routes_retagged"] += 1
                    changed = True
            # also retag if city_id embedded in bid prefix and we retag that bid
            if bid and "__" in bid:
                prefix = bid.split("__", 1)[0]
                # if full bid retagged already handled; if assigned city was wrong via retag map on bid
                pass

        # RELABEL
        for end, lab_field in (("from", "from_label"), ("to", "to_label")):
            bid = p.get(end)
            if bid in relabel:
                p[lab_field] = relabel[bid]
                receipt["routes_relabeled"] += 1
                changed = True

        if changed:
            p["_bp_hygiene_applied"] = utc_now()
            f["properties"] = p
        new_feats.append(f)

    # POI drop + retag
    new_pois = []
    poi_by_id = {}
    for poi in pois:
        props = poi.get("properties") or poi
        pid = props.get("id")
        # match drop by full id or suffix
        drop = False
        if not args.skip_drop:
            if pid in drop_bps:
                drop = True
            else:
                for db in drop_bps:
                    if pid and (pid == db or pid.endswith("__" + db.split("__")[-1]) or db.endswith(pid)):
                        # only exact id match to avoid collateral
                        if pid == db:
                            drop = True
                            break
        if drop:
            receipt["pois_dropped"] += 1
            continue
        # retag parent_city_id
        if pid in retag:
            props["parent_city_id"] = retag[pid]
            props["_bp_hygiene_retag"] = retag[pid]
            receipt["pois_retagged"] += 1
            if "properties" in poi:
                poi["properties"] = props
        # dup: if this POI is an alias, skip it when canonical exists
        if pid in dup_map:
            # drop alias POI if canonical also present later; mark for skip
            receipt.setdefault("poi_dup_aliases_dropped", 0)
            # keep for now; only drop if we can find canonical in set
            pass
        new_pois.append(poi)
        if pid:
            poi_by_id[pid] = poi

    # Drop alias POIs when canonical exists
    final_pois = []
    for poi in new_pois:
        props = poi.get("properties") or poi
        pid = props.get("id")
        if pid in dup_map and dup_map[pid] in poi_by_id:
            receipt["pois_dropped"] += 1
            receipt["poi_dup_aliases_dropped"] = receipt.get("poi_dup_aliases_dropped", 0) + 1
            continue
        final_pois.append(poi)

    receipt["routes_after"] = len(new_feats)
    receipt["pois_after"] = len(final_pois)

    print(json.dumps({k: receipt[k] for k in receipt if k != "dropped_route_ids"}, indent=2))
    print(f"dropped_route_ids sample: {receipt['dropped_route_ids'][:15]}")

    if args.dry:
        print("DRY RUN — no files written")
        RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
        return 0

    # Backup then write
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    bak = DC / f"_bak_bp_hygiene_{ts}"
    bak.mkdir(exist_ok=True)
    shutil.copy2(DC / "ROUTES.json", bak / "ROUTES.json")
    shutil.copy2(DC / "FEATURES_BY_TYPE.json", bak / "FEATURES_BY_TYPE.json")
    receipt["backup"] = str(bak.relative_to(ROOT))

    if isinstance(routes_obj, dict) and "features" in routes_obj:
        routes_obj["features"] = new_feats
        (DC / "ROUTES.json").write_text(json.dumps(routes_obj, separators=(",", ":")) + "\n")
    else:
        (DC / "ROUTES.json").write_text(json.dumps(new_feats, separators=(",", ":")) + "\n")

    fbt["poi"] = final_pois
    (DC / "FEATURES_BY_TYPE.json").write_text(json.dumps(fbt, separators=(",", ":")) + "\n")
    RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"wrote ROUTES + FEATURES; receipt {RECEIPT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
