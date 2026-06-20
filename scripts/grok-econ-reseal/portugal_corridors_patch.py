#!/usr/bin/env python3
"""Fix Portugal coverage corridors: replace placeholder lisbon-tagus node chips."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT = ROOT / "_ingest/econ-reseal-2026-06-19/econ-reseal/inputs/corridors.json"

PORTO_GAIA = ("porto-douro-portugal", "porto-douro-portugal")
ALGARVE = ("algarve-portugal", "algarve-portugal")
LISBON_CASCAIS = ("lisbon-tagus-portugal", "lisbon-tagus-portugal")


def patch_corridor(c: dict) -> bool:
    blob = f"{c.get('from', '')} {c.get('to', '')}".lower()
    eps = c.get("endpoint_boarding_points") or {}
    blob += f" {eps.get('from', '')} {eps.get('to', '')}".lower()
    changed = False
    if any(t in blob for t in ("porto", "ribeira", "gaia", "douro", "vila nova")):
        a, b = PORTO_GAIA
        if c.get("from_node_id") != a or c.get("to_node_id") != b:
            c["from_node_id"], c["to_node_id"] = a, b
            changed = True
    elif any(t in blob for t in ("faro", "portimao", "lagos", "algarve", "culatra", "ilha deserta", "benagil")):
        a, b = ALGARVE
        if c.get("from_node_id") != a or c.get("to_node_id") != b:
            c["from_node_id"], c["to_node_id"] = a, b
            changed = True
    elif "cascais" in blob:
        a, b = LISBON_CASCAIS
        if c.get("from_node_id") == c.get("to_node_id") == "lisbon-tagus-portugal":
            # keep same-node for Cascais until inter-city BP pair exists; labels already distinct
            pass
    return changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corridors", default=str(DEFAULT))
    args = ap.parse_args()
    path = Path(args.corridors)
    doc = json.loads(path.read_text())
    n = 0
    for mk, mval in (doc.get("markets") or {}).items():
        if not mk.startswith(("bolt-", "yango-")):
            continue
        for c in mval.get("corridors") or []:
            if (c.get("country") or "").lower() != "portugal" and "portugal" not in mk:
                if not any(
                    t in f"{c.get('from', '')} {c.get('to', '')}".lower()
                    for t in ("lisbon", "porto", "cascais", "faro", "portimao", "algarve")
                ):
                    continue
            if patch_corridor(c):
                n += 1
    path.write_text(json.dumps(doc, indent=1) + "\n")
    print(f"patched {n} Portugal corridors in {path}")


if __name__ == "__main__":
    main()