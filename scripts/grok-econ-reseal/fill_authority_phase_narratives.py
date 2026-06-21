#!/usr/bin/env python3
"""Fill missing authority phase narratives after archetype apply (Grok-owned stubs)."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "grok-econ-reseal"))
from partner_proposal_class import proposal_class  # noqa: E402

PARTNERS = ROOT / "partner-pitch" / "partners"
DC = ROOT / "data-clean" / "partners"

NARRATIVE_STUBS = {
    "intra_pilot": "Prove foiling on sheltered intra-{home} waters before inter-city or cross-border claims.",
    "intra_scale": "Scale the authority marine layer across the full home territory waterfront network.",
    "inter_city": "Add domestic inter-city corridors after intra-home proof is sealed.",
    "cross_border_roadmap": "Quanta-LR regional legs — amber-dashed display; economics excluded until ops seal.",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fill(doc: dict) -> int:
    home = (doc.get("_public_transit_authority") or {}).get("home_cities") or []
    home_label = home[0].replace("-", " ").title() if home else "home waters"
    n = 0
    for ph in doc.get("phases") or []:
        tier = ph.get("_authority_phase_tier") or ""
        if not (ph.get("narrative") or "").strip():
            stub = NARRATIVE_STUBS.get(tier, ph.get("label", ""))
            ph["narrative"] = stub.replace("{home}", home_label)
            ph["_narrative_source"] = "grok/fill_authority_phase_narratives"
            n += 1
        if not (ph.get("use_cases") or []) and ph.get("featured_routes"):
            ph["use_cases"] = [fr.get("label") for fr in ph["featured_routes"][:3] if fr.get("label")]
    return n


def main() -> int:
    slugs = sys.argv[1:] if len(sys.argv) > 1 else [
        "dubai-rta", "abu-dhabi-itc", "rakta", "bahrain-motc", "qatar",
        "singapore-mpa", "hong-kong", "transport-nsw", "thames-clippers", "nyc-ferry",
    ]
    filled = []
    for slug in slugs:
        path = PARTNERS / f"{slug}.json"
        if not path.exists():
            continue
        doc = json.loads(path.read_text())
        if proposal_class(slug, doc) != "authority":
            continue
        n = fill(doc)
        if n:
            path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
            dc = DC / f"{slug}.json"
            if dc.exists():
                dc.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        filled.append({"partner": slug, "narratives_added": n})
    print(json.dumps({"at": utc_now(), "filled": filled}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())