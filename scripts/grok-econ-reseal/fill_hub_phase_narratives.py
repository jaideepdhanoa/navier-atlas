#!/usr/bin/env python3
"""Fill missing hub top-level phase narratives (Grok-owned stubs)."""
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

DEFAULT_HUBS = ["didi", "cabify"]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def stub_from_label(label: str) -> str:
    clean = (label or "").strip()
    if "—" in clean:
        clean = clean.split("—", 1)[-1].strip()
    if not clean:
        return "Scale hub market featured and journey geometry binds across this phase."
    return f"Deploy foiling corridors in {clean} — market-scoped featured and journey binds under the hub layout."


def fill(doc: dict) -> int:
    n = 0
    for ph in doc.get("phases") or []:
        if ph.get("aspirational"):
            continue
        if (ph.get("narrative") or "").strip():
            continue
        ph["narrative"] = stub_from_label(ph.get("label", ""))
        ph["_narrative_source"] = "grok/fill_hub_phase_narratives"
        n += 1
    return n


def main() -> int:
    slugs = sys.argv[1:] if len(sys.argv) > 1 else DEFAULT_HUBS
    filled = []
    for slug in slugs:
        path = PARTNERS / f"{slug}.json"
        if not path.exists():
            continue
        doc = json.loads(path.read_text())
        if proposal_class(slug, doc) != "hub":
            continue
        count = fill(doc)
        if count:
            path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
            dc = DC / f"{slug}.json"
            if dc.exists():
                dc.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        filled.append({"partner": slug, "narratives_added": count})
    print(json.dumps({"at": utc_now(), "filled": filled}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())