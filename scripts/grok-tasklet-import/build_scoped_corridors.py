#!/usr/bin/env python3
"""Build finance/recal/corridors-<partner>.json scoped view from corridors.json."""
from __future__ import annotations

import argparse
import copy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-tasklet-import"))

from tasklet_shared import CORRIDORS_SRC, RECAL, load_json, save_json, utc_now  # noqa: E402

# Partners that exclude roadmap legs from grounded economics cascade.
ROADMAP_EXCLUDED_PARTNERS = frozenset({"ocean-whisperer"})


def build_scoped(partner: str, exclude_roadmap: bool | None = None) -> dict:
    src = load_json(CORRIDORS_SRC)
    if partner not in src.get("markets", {}):
        raise KeyError(f"market {partner} not in {CORRIDORS_SRC}")

    exclude_roadmap = exclude_roadmap if exclude_roadmap is not None else partner in ROADMAP_EXCLUDED_PARTNERS
    mk = copy.deepcopy(src["markets"][partner])
    corridors = []
    held_roadmap = []
    for c in mk.get("corridors") or []:
        if exclude_roadmap and (c.get("tier") == "roadmap" or c.get("_economics_excluded")):
            held_roadmap.append(c.get("route_id"))
            continue
        corridors.append(c)
    mk["corridors"] = corridors
    mk["_scope"] = f"{partner}-economics-cascade"
    mk["_roadmap_excluded_from_cascade"] = exclude_roadmap
    mk["_roadmap_route_ids"] = held_roadmap

    capture = mk.get("capture_rate") or src.get("capture_rate") or 0.1
    return {
        "_doc": f"Scoped corridors view for {partner} economics cascade",
        "_source": str(CORRIDORS_SRC),
        "_built_at": utc_now(),
        "capture_rate": capture,
        "markets": {partner: mk},
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--partner", required=True)
    ap.add_argument("--out", help="output path (default finance/recal/corridors-<partner>.json)")
    ap.add_argument("--include-roadmap", action="store_true", help="keep roadmap legs in cascade")
    args = ap.parse_args()

    out_path = Path(args.out) if args.out else RECAL / f"corridors-{args.partner}.json"
    scoped = build_scoped(args.partner, exclude_roadmap=not args.include_roadmap)
    save_json(out_path, scoped)
    n = len(scoped["markets"][args.partner]["corridors"])
    print(f"✓ {out_path} ({n} corridors)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())