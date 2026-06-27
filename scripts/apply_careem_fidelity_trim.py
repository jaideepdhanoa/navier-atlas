#!/usr/bin/env python3
"""Apply P0b Careem proposal fidelity trim (data-clean + partner-pitch)."""
from __future__ import annotations

import copy
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATHS = [
    ROOT / "data-clean" / "partners" / "careem.json",
    ROOT / "partner-pitch" / "partners" / "careem.json",
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
    archetype: str,
    from_node_id: str,
    to_node_id: str,
    route_id: str,
    route_ids: list[str] | None = None,
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
        "_link_source": "grok/apply_careem_fidelity_trim",
        "economics_status": "cascaded",
        "model_link": MODEL,
        "_trim_at": TS,
    }


def featured_from_template(tmpl: dict) -> dict:
    out = copy.deepcopy(tmpl)
    out["_link_source"] = "grok/apply_careem_fidelity_trim"
    out["_trim_at"] = TS
    for k in ("_inherit_source", "_inherit_at"):
        out.pop(k, None)
    return out


def apply(doc: dict) -> dict:
    doc = copy.deepcopy(doc)

    doc["journeys_unlocked"] = [
        journey(
            from_="Dubai Harbour Marina",
            to="Nikki Beach Resort Pearl Jumeirah Jetty",
            today="Road-first or scheduled/charter water movement; fragmented booking and limited app-native orchestration.",
            with_navier="A Careem-branded premium marine leg along Dubai's coast — waterfront dining, hotel desks, and experience bundles booked in-app.",
            distance_nm=11.9,
            archetype="commerce_logistics",
            from_node_id="bp-56d5f5bd8d",
            to_node_id="bp-b13fc69aba",
            route_id="rn-b1ba183aa886",
        ),
        journey(
            from_="Vida Beach Resort Umm Al Quwain",
            to="Sharjah Waterfront City marina",
            today="The Sharjah–Dubai commute and resort runs rely on Sheikh Mohammed Bin Zayed Road — no fast coastal option.",
            with_navier="A short N30 hop links UAQ's waterfront resorts to Sharjah Waterfront City — a beachhead corridor for the Careem app on the northern coast.",
            distance_nm=9.6,
            archetype="commute",
            from_node_id="bp-bad4f1baf7",
            to_node_id="bp-b3eed149c8",
            route_id="rn-02a40748974d",
        ),
        journey(
            from_="Dubai Harbour Marina",
            to="Al Khan Lagoon mouth",
            today="Sharjah waterfront trips from Dubai loop through congested creek bridges and corniche roads.",
            with_navier="A direct Dubai Harbour → Al Khan marine leg — the Sharjah commute Careem riders feel every day, solved over the water.",
            distance_nm=19.4,
            archetype="commute",
            from_node_id="bp-56d5f5bd8d",
            to_node_id="bp-f0fde14967",
            route_id="gcn-8e3c2d581c-bolt",
        ),
    ]

    phases = doc.get("phases") or []
    by_n = {p.get("n"): p for p in phases}

    p1 = by_n.get(1)
    p2 = by_n.get(2)
    if p1:
        p1["cities"] = ["dubai-uae", "sharjah-uae"]
        p1["boats"] = 4
        p1["narrative"] = (
            "Four Pioneer II vessels on Dubai and Sharjah's highest-demand coastal corridors, "
            "booked in the Careem app — proving the in-app water tier in the marine authority's flagship city."
        )
        p1["rationale"] = (
            "Launch where Careem demand is densest — Dubai Harbour, Pearl Jumeirah, and the brutal "
            "Sharjah waterfront commute — before extending to other emirates."
        )
        old_p1 = {fr.get("route_id"): fr for fr in (p1.get("featured_routes") or [])}
        old_p2 = {fr.get("route_id"): fr for fr in ((p2 or {}).get("featured_routes") or [])}
        al_khan = old_p2.get("gcn-8e3c2d581c-bolt")
        if not al_khan:
            raise SystemExit("missing gcn-8e3c2d581c-bolt in phase 2 featured_routes")
        p1["featured_routes"] = [
            featured_from_template(old_p1["rn-b1ba183aa886"]),
            featured_from_template(old_p1["rn-02a40748974d"]),
            featured_from_template(al_khan),
        ]

    if p2:
        drop_p2 = frozenset({"gcn-8e3c2d581c-bolt", "gcn-4ae479b872-bolt"})
        p2_fr = [fr for fr in (p2.get("featured_routes") or []) if fr.get("route_id") not in drop_p2]
        p2["featured_routes"] = [featured_from_template(fr) for fr in p2_fr]

    p3 = by_n.get(3)
    if p3:
        keep_p3 = frozenset({"edge-0687", "edge-0712"})
        p3["featured_routes"] = [
            featured_from_template(fr)
            for fr in (p3.get("featured_routes") or [])
            if fr.get("route_id") in keep_p3
        ]

    doc["_fidelity_trim"] = {
        "at": TS,
        "source": "grok/apply_careem_fidelity_trim",
        "audit": "handoff/partner-map-model/PROPOSAL-FIDELITY-careem.md",
    }
    return doc


def main() -> int:
    for path in PATHS:
        doc = json.loads(path.read_text())
        out = apply(doc)
        path.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
        print(f"trimmed {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())