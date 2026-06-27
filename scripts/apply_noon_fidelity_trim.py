#!/usr/bin/env python3
"""Apply Noon proposal fidelity trim (data-clean + partner-pitch)."""
from __future__ import annotations

import copy
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATHS = [
    ROOT / "data-clean" / "partners" / "noon.json",
    ROOT / "partner-pitch" / "partners" / "noon.json",
]

MODEL = "https://docs.google.com/spreadsheets/d/1v0ywhNFk_fA1JRVhizWlz89RKgQWlID9RD3LfBhVB2Y/edit"
TS = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def journey(
    *,
    from_: str,
    to: str,
    today: str,
    with_navier: str,
    distance_nm: float,
    from_node_id: str,
    to_node_id: str,
    route_id: str,
    route_ids: list[str] | None = None,
    archetype: str = "commerce_logistics",
) -> dict:
    return {
        "from": from_,
        "to": to,
        "today": today,
        "with_navier": with_navier,
        "distance_nm": distance_nm,
        "platform": "N30 Pioneer II",
        "archetype": archetype,
        "from_node_id": from_node_id,
        "to_node_id": to_node_id,
        "route_id": route_id,
        "route_ids": route_ids,
        "_link_kind": "corridor-label",
        "_link_status": "linked-grok-node",
        "_link_source": "grok/apply_noon_fidelity_trim",
        "economics_status": "cascaded",
        "model_link": MODEL,
        "_trim_at": TS,
    }


def featured(tmpl: dict) -> dict:
    out = copy.deepcopy(tmpl)
    out["_link_source"] = "grok/apply_noon_fidelity_trim"
    out["_trim_at"] = TS
    return out


def apply(doc: dict) -> dict:
    doc = copy.deepcopy(doc)

    doc["journeys_unlocked"] = [
        journey(
            from_="Dubai Harbour Marina",
            to="Nikki Beach Resort Pearl Jumeirah Jetty",
            today="Road-first or scheduled/charter water movement; fragmented booking and limited app-native orchestration.",
            with_navier="A Noon-visible premium marine leg along Dubai's coast — waterfront dining, hotel desks, and experience bundles booked in-app.",
            distance_nm=11.9,
            from_node_id="bp-56d5f5bd8d",
            to_node_id="bp-b13fc69aba",
            route_id="rn-b1ba183aa886",
        ),
        journey(
            from_="Vida Beach Resort Umm Al Quwain",
            to="Sharjah Waterfront City marina",
            today="The Sharjah–Dubai commute and resort runs rely on Sheikh Mohammed Bin Zayed Road — no fast coastal option.",
            with_navier="A short N30 hop links UAQ's waterfront resorts to Sharjah Waterfront City — commerce and concierge on the northern coast.",
            distance_nm=9.6,
            from_node_id="bp-bad4f1baf7",
            to_node_id="bp-b3eed149c8",
            route_id="rn-02a40748974d",
        ),
        journey(
            from_="Dubai Harbour Marina",
            to="Al Khan Lagoon mouth",
            today="Sharjah waterfront trips from Dubai loop through congested creek bridges and corniche roads.",
            with_navier="A direct Dubai Harbour → Al Khan marine leg — the Sharjah commute Noon riders feel every day, solved over the water.",
            distance_nm=19.4,
            from_node_id="bp-56d5f5bd8d",
            to_node_id="bp-f0fde14967",
            route_id="gcn-8e3c2d581c-bolt",
        ),
    ]

    wow = [
        "Dubai Harbour Marina → Nikki Beach Resort Pearl Jumeirah Jetty",
        "Vida Beach Resort Umm Al Quwain → Sharjah Waterfront City marina",
        "Dubai Harbour Marina → Al Khan Lagoon mouth",
    ]
    if doc.get("why_navier_now"):
        doc["why_navier_now"]["wow_corridors"] = wow

    for ph in doc.get("phases", []):
        n = ph.get("n")
        if n == 1:
            keep_labels = {
                "Dubai Harbour Marina → Nikki Beach Resort Pearl Jumeirah Jetty",
                "Vida Beach Resort Umm Al Quwain → Sharjah Waterfront City marina",
            }
            ph["featured_routes"] = [
                featured(r)
                for r in ph.get("featured_routes", [])
                if r.get("label") in keep_labels
            ]
            ph["cities"] = ["dubai-uae", "sharjah-uae"]
        elif n == 2:
            keep_labels = {
                "Dubai Harbour Marina → Wynn Al Marjan Island arrival lagoon",
                "Dubai Harbour Marina → Al Khan Lagoon mouth",
            }
            ph["featured_routes"] = [
                featured(r)
                for r in ph.get("featured_routes", [])
                if r.get("label") in keep_labels
            ]
        elif n == 3:
            keep_labels = {
                "Abu Dhabi → Muscat",
                "Fujairah → Muscat",
            }
            ph["featured_routes"] = [
                featured(r)
                for r in ph.get("featured_routes", [])
                if r.get("label") in keep_labels
            ]

    doc["_fidelity_trim"] = {
        "at": TS,
        "source": "grok/apply_noon_fidelity_trim",
        "receipt": "handoff/partner-map-model/PROPOSAL-FIDELITY-noon.md",
        "journeys_kept": 3,
        "phase1_featured_kept": 2,
    }
    return doc


def main() -> None:
    for path in PATHS:
        doc = json.loads(path.read_text())
        out = apply(doc)
        path.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
        print(f"trimmed {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()