#!/usr/bin/env python3
"""Re-apply full India spine network_chip bundles after relink_partner_journeys."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PARTNER_PATHS = [
    ROOT / "partner-pitch" / "partners" / "rapido.json",
    ROOT / "partner-pitch" / "partners" / "ola.json",
    ROOT / "data-clean" / "partners" / "rapido.json",
    ROOT / "data-clean" / "partners" / "ola.json",
]

spec = importlib.util.spec_from_file_location(
    "execute_pr58",
    ROOT / "scripts/grok-econ-reseal/execute_pr58_india_gcc.py",
)
mod = importlib.util.module_from_spec(spec)
sys.modules["execute_pr58"] = mod
spec.loader.exec_module(mod)


def main() -> int:
    spine = mod.load_india_spine()
    gold_ids, _, _ = mod.build_route_index()
    by_market = mod.spine_corridors_by_market(spine)

    for path in PARTNER_PATHS:
        if not path.is_file():
            continue
        doc = json.loads(path.read_text())
        mod.expand_india_network_chips(doc, by_market=by_market, gold_ids=gold_ids)
        path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        print(f"refreshed chips: {path.name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())