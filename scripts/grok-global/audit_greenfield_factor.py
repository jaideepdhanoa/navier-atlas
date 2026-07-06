#!/usr/bin/env python3
"""Cross-partner greenfield factor audit + Careem-parity gate."""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "grok-routing-output" / "greenfield-factor-audit-2026-07-06.json"


def audit() -> dict:
    broken = []
    ok = []
    for path in sorted(glob.glob(str(ROOT / "data-clean/partners/*.json"))):
        partner = Path(path).stem
        doc = json.loads(Path(path).read_text())
        gc = doc.get("growth_case") or {}
        rungs = {r["id"]: r for r in (gc.get("revenue_potential") or {}).get("rungs", [])}
        if "som_floor" not in rungs or "som_network" not in rungs:
            continue
        floor = rungs["som_floor"].get("mid")
        net = rungs["som_network"].get("mid")
        if not floor or not net:
            continue
        gf = None
        for t in gc.get("ladder_transitions") or []:
            if t.get("from_rung_id") == "som_floor" and t.get("to_rung_id") == "som_network":
                gf = (t.get("multipliers_cited") or {}).get("greenfield_corridor_factor_mid")
                break
        ratio = net / floor
        row = {"partner": partner, "som_floor": floor, "som_network": net, "gf_mid": gf, "ratio": round(ratio, 3)}
        if gf and gf > 1.05 and ratio < 1.5:
            broken.append(row)
        elif gf and gf > 1.05:
            ok.append(row)

    careem = json.loads((ROOT / "data-clean/partners/careem.json").read_text())
    yango = json.loads((ROOT / "data-clean/partners/yango.json").read_text())
    c_net = next(r["mid"] for r in careem["growth_case"]["revenue_potential"]["rungs"] if r["id"] == "som_network")
    y_net = next(r["mid"] for r in yango["growth_case"]["revenue_potential"]["rungs"] if r["id"] == "som_network")

    parity = {
        "careem_som_network_mid": c_net,
        "yango_som_network_mid": y_net,
        "yango_gt_careem": y_net > c_net,
        "careem_gf_ratio": round(
            c_net
            / next(r["mid"] for r in careem["growth_case"]["revenue_potential"]["rungs"] if r["id"] == "som_floor"),
            3,
        ),
        "yango_gf_ratio": round(
            y_net
            / next(r["mid"] for r in yango["growth_case"]["revenue_potential"]["rungs"] if r["id"] == "som_floor"),
            3,
        ),
        "gate_pass": y_net > c_net and not broken,
    }

    return {
        "broken": broken,
        "ok_count": len(ok),
        "careem_parity_gate": parity,
        "gate_pass": parity["gate_pass"],
    }


def main() -> int:
    report = audit()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report["careem_parity_gate"], indent=2))
    if report["broken"]:
        print("BROKEN:", report["broken"], file=sys.stderr)
        return 1
    print(f"✓ greenfield audit: {report['ok_count']} partners OK, Careem-parity gate {'PASS' if report['gate_pass'] else 'FAIL'}")
    return 0 if report["gate_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())