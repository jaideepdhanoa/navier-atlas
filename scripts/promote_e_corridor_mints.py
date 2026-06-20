#!/usr/bin/env python3
"""Un-quarantine corridor e__ mints and extend route_water_allowlist.

Targets:
  - e__mald__b95e8093ec6d (Kadhdhoo Airport, Laamu → Six Senses Laamu)
  - All e__velana__* resort-jetty legs (Velana → named jetties)
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTES_PATH = ROOT / "data-clean/ROUTES.json"
ALLOW_PATH = ROOT / "data-clean/route_water_allowlist.json"

KADHDOO_ID = "e__mald__b95e8093ec6d"
VELANA_PREFIX = "e__velana__"


def load_json(p: Path):
    return json.loads(p.read_text())


def save_json(p: Path, obj):
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def main():
    routes_raw = load_json(ROUTES_PATH)
    feats = routes_raw if isinstance(routes_raw, list) else routes_raw.get("features", [])

    promote_ids: set[str] = {KADHDOO_ID}
    for f in feats:
        rid = (f.get("properties") or {}).get("id")
        if rid and rid.startswith(VELANA_PREFIX):
            promote_ids.add(rid)

    unquarantined: list[str] = []
    for f in feats:
        p = f.setdefault("properties", {})
        rid = p.get("id")
        if rid not in promote_ids:
            continue
        if p.pop("_quarantine", None):
            unquarantined.append(rid)

    save_json(ROUTES_PATH, routes_raw)

    allow = load_json(ALLOW_PATH)
    ids = list(allow.get("ids", []))
    seen = set(ids)
    added: list[str] = []
    for rid in sorted(promote_ids):
        if rid not in seen:
            ids.append(rid)
            seen.add(rid)
            added.append(rid)
    allow["ids"] = ids
    meta = allow.setdefault("_meta", {})
    meta["e_corridor_promote_at"] = datetime.now(timezone.utc).isoformat()
    meta["e_corridor_promote_unquarantined"] = unquarantined
    meta["e_corridor_promote_allowlist_added"] = added
    save_json(ALLOW_PATH, allow)

    print(f"un-quarantined {len(unquarantined)} e__ corridor mints")
    print(f"allowlist +{len(added)} (total {len(ids)})")
    for rid in sorted(unquarantined):
        print(f"  visible: {rid}")


if __name__ == "__main__":
    main()