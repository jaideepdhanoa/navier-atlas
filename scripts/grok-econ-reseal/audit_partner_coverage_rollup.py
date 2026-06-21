#!/usr/bin/env python3
"""Roll up partner-page QA + spine parity into a review queue (like authority coverage)."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HANDOFF = ROOT / "handoff" / "partner-map-model"
QA_LEDGER = HANDOFF / "partner-page-qa-ledger.json"
SPINE_LEDGER = HANDOFF / "spine-parity-ledger.json"
OUT = HANDOFF / "partner-coverage-review-rollup.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def main() -> int:
    qa = load(QA_LEDGER)
    spine = load(SPINE_LEDGER) if SPINE_LEDGER.is_file() else None
    spine_by = {r["partner"]: r for r in (spine or {}).get("partners", [])}

    review: dict[str, list] = {
        "authority_reference": [],
        "geometry_gaps": [],
        "spine_parity_fail": [],
        "thin_map": [],
        "tasklet_queue": [],
    }

    for r in qa.get("partners", []):
        p = r["partner"]
        c = r.get("counts", {})
        fr, fg = c.get("featured_routes", 0), c.get("featured_geometry_linked", 0)
        mr = c.get("map_routes_in_scope", 0)

        if p in ("rakta", "bahrain-motc"):
            review["authority_reference"].append({
                "partner": p,
                "verdict": r["verdict"],
                "featured_sealed_geom": f"{fg}/{fr}",
                "map_routes_in_scope": mr,
            })
            continue

        sp = spine_by.get(p, {})
        if sp.get("verdict") == "FAIL":
            review["spine_parity_fail"].append({
                "partner": p,
                "geometry_linked": sp.get("geometry_linked"),
                "card_gaps": sp.get("card_gaps"),
            })

        if fr and fg < fr * 0.85:
            review["geometry_gaps"].append({
                "partner": p,
                "featured_geom": f"{fg}/{fr}",
                "journey_geom": f"{c.get('journeys_geometry_linked', 0)}/{c.get('journeys', 0)}",
                "map_routes": mr,
                "verdict": r["verdict"],
            })

        if mr < 80 and p not in {
            "maldives-government", "norway-fjords", "thames-clippers",
            "transport-nsw", "hong-kong", "universal-enterprises", "villa-hotels",
        }:
            review["thin_map"].append({"partner": p, "map_routes": mr})

        for t in r.get("tasklet_actions", []):
            review["tasklet_queue"].append({"partner": p, "action": t})

    out = {
        "at": datetime.now(timezone.utc).isoformat(),
        "sources": [str(QA_LEDGER.relative_to(ROOT)), str(SPINE_LEDGER.relative_to(ROOT))],
        "summary": {
            "qa_total": qa.get("summary", {}).get("total"),
            "qa_pass": qa.get("summary", {}).get("pass"),
            "qa_pass_with_flags": qa.get("summary", {}).get("pass_with_flags"),
            "qa_fail": qa.get("summary", {}).get("fail"),
            "geometry_gap_partners": len(review["geometry_gaps"]),
            "spine_parity_fail": len(review["spine_parity_fail"]),
            "thin_map": len(review["thin_map"]),
            "tasklet_actions": len(review["tasklet_queue"]),
        },
        "review": review,
    }
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(out["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())