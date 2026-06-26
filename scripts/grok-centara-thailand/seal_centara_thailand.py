#!/usr/bin/env python3
"""
Grok deterministic seal — Centara Thailand (hospitality / hotel-resort operator).

Route sealing, partner proposal page, corridor economics inputs.
Does NOT rebuild or own the Centara deck (Tasklet lane).

Usage:
  python3 scripts/grok-centara-thailand/seal_centara_thailand.py --apply
  python3 scripts/grok-centara-thailand/seal_centara_thailand.py --dry-run
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bucketB"))
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))

from bolt_yango_routing_shared import (  # noqa: E402
    build_coastal_path,
    build_bp_index,
    hav_nm,
    interior_land_km,
    load_json,
    load_land_mask,
    mint_route_id,
    route_features,
    save_routes,
)

PARTNER = "centara-thailand"
ROUTES_PATH = ROOT / "data-clean/ROUTES.json"
FBT_PATH = ROOT / "data-clean/FEATURES_BY_TYPE.json"
PITCH_PATH = ROOT / "partner-pitch/partners" / f"{PARTNER}.json"
DC_PATH = ROOT / "data-clean/partners" / f"{PARTNER}.json"
CORR_OUT = ROOT / "finance/recal" / f"corridors-{PARTNER}.json"
CROSSWALK_OUT = ROOT / "partner-pitch" / f"CENTARA-THAILAND-ANCHOR-CITY-CROSSWALK.json"
SIDECAR_HANDOFF = ROOT / "handoff/centara-thailand/centara-thailand-economics-sidecar.draft.json"
INVENTORY_HANDOFF = ROOT / "handoff/centara-thailand/centara-thailand-property-inventory.json"
ECON_SIDECAR_OUT = ROOT / "handoff/centara-thailand/centara-thailand-economics-sidecar.json"
REPORT = ROOT / "grok-routing-output/centara-thailand-seal-report.json"
HANDOFF = ROOT / "handoff/centara-thailand/GROK-HANDOFF-centara-thailand-partner-page-only-2026-06-26.md"

CHALONG_KARON_TAG = "centara_thailand_chalong_karon"
CHALONG_BP = "bp-4e9a8f7cea"
KARON_BP = "bp-3a1cb874f2"

# Sealed corridor bindings — cluster_id matches Tasklet sidecar rows
CORRIDOR_BINDINGS: list[dict] = [
    {
        "cluster_id": "bangkok",
        "market_id": "bangkok-river",
        "market_slug": "bangkok-river",
        "market_label": "Bangkok river gateway",
        "route_id": "gcn-e299366426-shared",
        "from_bp_id": "bp-97754cb272",
        "to_bp_id": "bp-phra-arthit-n13",
        "from_node_id": "bangkok-thailand",
        "to_node_id": "bangkok-thailand",
        "anchor_cities": ["bangkok-thailand"],
        "corridor_label": "Sathorn Pier → Phra Arthit river circuit",
        "use_case": "hotel-curated city-to-river experience",
    },
    {
        "cluster_id": "western-gulf-hua-hin-cha-am",
        "market_id": "western-gulf",
        "market_slug": "western-gulf",
        "market_label": "Western Gulf — Hua Hin / Cha-Am",
        "route_id": "rn-7512bdcf3d4c",
        "from_bp_id": None,
        "to_bp_id": None,
        "from_node_id": "hua-hin-thailand",
        "to_node_id": "cha-am-thailand",
        "anchor_cities": ["hua-hin-thailand", "cha-am-thailand"],
        "corridor_label": "Centara Grand Hua Hin → Cha-Am coastal hop",
        "use_case": "heritage beachfront leisure route",
    },
    {
        "cluster_id": "eastern-gulf-pattaya-koh-chang",
        "market_id": "eastern-gulf",
        "market_slug": "eastern-gulf",
        "market_label": "Eastern Gulf — Pattaya / Koh Chang",
        "route_id": "rn-f09e06bc2910",
        "from_bp_id": "bp-bali-hai-pier",
        "to_bp_id": "bp-koh-larn-na-ban-pier",
        "from_node_id": "pattaya-thailand",
        "to_node_id": "koh-larn-thailand",
        "anchor_cities": ["pattaya-thailand", "koh-larn-thailand", "koh-chang-thailand"],
        "corridor_label": "Centara Grand Mirage Pattaya → Koh Larn",
        "use_case": "family-resort island excursion",
        "sub_market": "mainland",
    },
    {
        "cluster_id": "eastern-gulf-pattaya-koh-chang",
        "market_id": "eastern-gulf",
        "market_slug": "eastern-gulf",
        "market_label": "Eastern Gulf — Pattaya / Koh Chang",
        "route_id": "rn-b11478b5cb27",
        "from_bp_id": "bp-ao-sapparot-pier",
        "to_bp_id": "bp-bang-bao-pier",
        "from_node_id": "koh-chang-thailand",
        "to_node_id": "koh-chang-thailand",
        "anchor_cities": ["pattaya-thailand", "koh-larn-thailand", "koh-chang-thailand"],
        "corridor_label": "Ao Sapparot → Bang Bao (Koh Chang arrival)",
        "use_case": "island arrival",
        "sub_market": "island",
    },
    {
        "cluster_id": "phuket-andaman-north",
        "market_id": "phuket-andaman",
        "market_slug": "phuket-andaman",
        "market_label": "Phuket / Andaman north",
        "route_id": None,  # minted at seal time
        "mint_from_bp": CHALONG_BP,
        "mint_to_bp": KARON_BP,
        "from_bp_id": CHALONG_BP,
        "to_bp_id": KARON_BP,
        "from_node_id": "phuket-phang-nga-thailand",
        "to_node_id": "phuket-phang-nga-thailand",
        "anchor_cities": ["phuket-phang-nga-thailand"],
        "corridor_label": "Chalong Pier → Centara Grand Beach Resort Phuket / Karon",
        "use_case": "premium arrival / excursion gateway",
    },
    {
        "cluster_id": "krabi-phi-phi",
        "market_id": "krabi-phi-phi",
        "market_slug": "krabi-phi-phi",
        "market_label": "Krabi / Phi Phi",
        "route_id": "rn-884b63688113",
        "from_bp_id": "bp-klong-jilad-pier",
        "to_bp_id": "bp-tonsai-pier",
        "from_node_id": "krabi-thailand",
        "to_node_id": "koh-phi-phi-thailand",
        "anchor_cities": ["krabi-thailand", "koh-phi-phi-thailand"],
        "corridor_label": "Klong Jilad / Ao Nang → Phi Phi (Tonsai)",
        "use_case": "island resort arrival",
    },
    {
        "cluster_id": "samui-gulf-islands",
        "market_id": "samui-gulf",
        "market_slug": "samui-gulf",
        "market_label": "Samui / Gulf islands",
        "route_id": "rn-ed1f11dec282",
        "from_bp_id": "bp-dd75088c4e",
        "to_bp_id": "bp-ea89d323cc",
        "from_node_id": "koh-samui-thailand",
        "to_node_id": "koh-samui-thailand",
        "anchor_cities": ["koh-samui-thailand"],
        "corridor_label": "Centara Reserve Samui → Chaweng gateway",
        "use_case": "airport-to-resort water arrival",
    },
]


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def props(feat: dict) -> dict:
    return feat.get("properties", feat)


def route_index(routes: list) -> dict[str, dict]:
    return {props(r).get("id"): r for r in routes if props(r).get("id")}


def bp_row(bp_idx: dict, bp_id: str | None) -> dict | None:
    return bp_idx.get(bp_id) if bp_id else None


def bp_coords(bp_idx: dict, bp_id: str) -> tuple[float, float]:
    row = bp_idx[bp_id]
    return tuple(row["coords"])


def mint_chalong_karon(routes: list, bp_idx: dict, mask, apply: bool) -> str:
    rid = mint_route_id(CHALONG_BP, KARON_BP, CHALONG_KARON_TAG)
    idx = route_index(routes)
    if rid in idx:
        return rid
    a = bp_coords(bp_idx, CHALONG_BP)
    b = bp_coords(bp_idx, KARON_BP)
    coords = build_coastal_path(a, b, mask)
    dist = sum(hav_nm(coords[i], coords[i + 1]) for i in range(len(coords) - 1))
    land_km = interior_land_km(coords, mask)
    feat = {
        "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": coords},
        "properties": {
            "id": rid,
            "platform": "Pioneer II",
            "distance_nm": round(dist, 1),
            "edge_class": "local",
            "from": CHALONG_BP,
            "to": KARON_BP,
            "from_city_id": "phuket-phang-nga-thailand",
            "to_city_id": "phuket-phang-nga-thailand",
            "label": "Chalong Pier → Karon Beach",
            "trip_purpose": "tourism",
            "traffic_weight": 0.72,
            "interior_land_km": round(land_km, 4),
            f"_{CHALONG_KARON_TAG}_applied_at": now_iso(),
            "_centara_thailand_seal": True,
            "_geometry_status": "coastal_path",
        },
    }
    routes.append(feat)
    if apply:
        save_routes(ROUTES_PATH, routes)
    return rid


def sidecar_by_cluster(sidecar: list[dict]) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for row in sidecar:
        out.setdefault(row["cluster_id"], []).append(row)
    return out


def pick_sidecar_row(bind: dict, by_cluster: dict[str, list[dict]]) -> dict:
    rows = by_cluster.get(bind["cluster_id"], [])
    if bind.get("sub_market") == "island":
        for r in rows:
            if "island" in (r.get("market_label") or "").lower():
                return r
    if bind.get("sub_market") == "mainland":
        for r in rows:
            if "mainland" in (r.get("market_label") or "").lower():
                return r
    return rows[0] if rows else {}


def corridor_from_binding(bind: dict, route_feat: dict | None, sidecar_row: dict) -> dict:
    p = props(route_feat) if route_feat else {}
    rid = bind.get("route_id") or p.get("id")
    fare = float(sidecar_row.get("fare_per_seat_usd") or 55)
    pax = int(sidecar_row.get("paid_seats_per_year") or 0)
    transfers = int(sidecar_row.get("paid_transfers_per_day") or 10)
    dist = float(p.get("distance_nm") or 0)
    return {
        "route_id": rid,
        "from": bind["corridor_label"].split("→")[0].strip() if "→" in bind["corridor_label"] else bind["corridor_label"],
        "to": bind["corridor_label"].split("→")[-1].strip() if "→" in bind["corridor_label"] else "",
        "distance_nm": dist,
        "vessel": "Pioneer II",
        "archetype": "hospitality",
        "from_node_id": bind["from_node_id"],
        "to_node_id": bind["to_node_id"],
        "from_bp_id": bind.get("from_bp_id"),
        "to_bp_id": bind.get("to_bp_id"),
        "country": "Thailand",
        "captive": True,
        "captive_resort": True,
        "pool_basis": "addressable",
        "_centara_thailand": True,
        "_centara_cluster": bind["cluster_id"],
        "L3_locals": {
            "comparable_fare_usd_pax": fare,
            "corridor_annual_oneway_pax": pax,
            "_demand_record": {
                "value": pax,
                "unit": "paid seats/yr",
                "source_tier": "T2",
                "confidence": "med",
                "source": "handoff/centara-thailand-economics-sidecar.draft.json",
                "method": f"Centara hospitality corridor — {transfers} transfers/day",
            },
            "_fare_record": {
                "value": fare,
                "unit": "USD/pax/one-way",
                "source_tier": "T2",
                "confidence": "med",
                "source": "handoff/centara-thailand-economics-sidecar.draft.json",
                "method": "Centara guest-paid transfer fare anchor",
            },
            "demand_confidence": "med",
            "capex_override_usd": 1_000_000,
        },
    }


def build_corridors_doc(bindings: list[dict], routes: list, sidecar: list[dict]) -> dict:
    ridx = route_index(routes)
    by_cluster = sidecar_by_cluster(sidecar)
    markets: dict[str, dict] = {}
    for bind in bindings:
        rid = bind["route_id"]
        feat = ridx.get(rid) if rid else None
        row = corridor_from_binding(bind, feat, pick_sidecar_row(bind, by_cluster))
        mk = markets.setdefault(
            bind["market_id"],
            {
                "partner": PARTNER,
                "region": "SEA",
                "label": bind["market_label"],
                "capex_tier": "hospitality",
                "fleet_basis": "corridor_sum",
                "_centara_cluster": bind["cluster_id"],
                "_market_note": "Centara hospitality captive corridor examples — no market-size ladder",
                "corridors": [],
            },
        )
        mk["corridors"].append(row)
    return {
        "_doc": "Scoped hospitality corridors for centara-thailand economics cascade",
        "_source": "handoff sidecar + sealed ROUTES.json",
        "_built_at": now_iso(),
        "capture_rate": 0.6,
        "markets": markets,
    }


def journey_from_binding(bind: dict, route_feat: dict | None, sidecar_row: dict) -> dict:
    p = props(route_feat) if route_feat else {}
    rid = bind.get("route_id") or p.get("id")
    dist = p.get("distance_nm")
    return {
        "from": bind["corridor_label"].split("→")[0].strip(),
        "to": bind["corridor_label"].split("→")[-1].strip() if "→" in bind["corridor_label"] else bind["corridor_label"],
        "today": "Diesel speedboat or road transfer — noisy, weather-bound, operated by a third party.",
        "with_navier": (
            "A quiet electric water shuttle — hotel-curated, premium boarding, "
            "predictable timing for Centara guests."
        ),
        "distance_nm": dist,
        "platform": "Pioneer II",
        "render": "solid",
        "range_status": "now",
        "from_node_id": bind["from_node_id"],
        "to_node_id": bind["to_node_id"],
        "from_bp_id": bind.get("from_bp_id"),
        "to_bp_id": bind.get("to_bp_id"),
        "route_id": rid,
        "_link_kind": "hospitality-corridor",
        "_link_status": "linked-grok-scoped",
        "_link_source": "grok/centara_thailand_seal",
        "economics_status": "pending_cascade",
        "use_case": bind.get("use_case"),
        "_centara_cluster": bind["cluster_id"],
        "_sidecar_revenue_usd_yr": sidecar_row.get("revenue_per_vessel_year_usd"),
        "_sidecar_payback_years": sidecar_row.get("payback_years"),
    }


def market_narratives() -> dict[str, dict]:
    return {
        "bangkok-river": {
            "summary": (
                "Centara's Bangkok flagship sits on the Chao Phraya gateway. "
                "Hotel-curated river experiences — not open mobility — connect convention "
                "and leisure guests to Sathorn and ICONSIAM piers."
            ),
            "hero": {
                "title": "Centara × Navier — Bangkok river gateway",
                "subtitle": "Hotel-curated electric river experiences above the express-boat tier.",
            },
        },
        "western-gulf": {
            "summary": (
                "Centara Grand Beach Resort Hua Hin anchors the royal coast. "
                "A short coastal hop to Cha-Am and Khao Takiab fits Pioneer II range "
                "and heritage weekend demand."
            ),
            "hero": {
                "title": "Centara × Navier — Western Gulf heritage coast",
                "subtitle": "Quiet electric hops along Hua Hin and Cha-Am.",
            },
        },
        "eastern-gulf": {
            "summary": (
                "Pattaya's family resorts and Koh Chang's ferry gateway create two operating "
                "patterns in one cluster — mainland island excursions and island arrivals."
            ),
            "hero": {
                "title": "Centara × Navier — Eastern Gulf",
                "subtitle": "Pattaya island hops and Koh Chang arrivals on sealed geometry.",
            },
        },
        "phuket-andaman": {
            "summary": (
                "Centara Grand Beach Resort Phuket on Karon links to Chalong Pier — "
                "the Andaman's premium arrival and excursion gateway."
            ),
            "hero": {
                "title": "Centara × Navier — Phuket / Andaman north",
                "subtitle": "Premium Chalong-to-Karon electric arrival.",
            },
        },
        "krabi-phi-phi": {
            "summary": (
                "Centara Villas Phi Phi and Centara Reserve Krabi connect across "
                "the sealed Krabi ↔ Phi Phi corridor."
            ),
            "hero": {
                "title": "Centara × Navier — Krabi / Phi Phi",
                "subtitle": "Island resort arrival on sealed Andaman geometry.",
            },
        },
        "samui-gulf": {
            "summary": (
                "Centara Reserve Samui on Chaweng sits minutes from Bang Rak gateway — "
                "a premium airport-to-resort water arrival story."
            ),
            "hero": {
                "title": "Centara × Navier — Samui / Gulf islands",
                "subtitle": "Premium water arrival at Centara Reserve Samui.",
            },
        },
    }


def build_partner_doc(bindings: list[dict], routes: list, sidecar: list[dict], inventory: list[dict]) -> dict:
    ridx = route_index(routes)
    by_cluster = sidecar_by_cluster(sidecar)
    narratives = market_narratives()
    markets_out: list[dict] = []
    seen_markets: set[str] = set()

    for bind in bindings:
        if bind["market_id"] in seen_markets:
            continue
        seen_markets.add(bind["market_id"])
        narr = narratives[bind["market_id"]]
        market_bindings = [b for b in bindings if b["market_id"] == bind["market_id"]]
        journeys = []
        for mb in market_bindings:
            rid = mb["route_id"]
            feat = ridx.get(rid) if rid else None
            journeys.append(journey_from_binding(mb, feat, pick_sidecar_row(mb, by_cluster)))
        props_in_cluster = [
            p for p in inventory if p["cluster_id"] == bind["cluster_id"] and p.get("fit_score") in ("A", "B")
        ][:4]
        markets_out.append({
            "id": bind["market_id"],
            "slug": bind["market_slug"],
            "label": bind["market_label"],
            "region": "SEA",
            "anchor_cities": bind["anchor_cities"],
            "category": "hospitality",
            "_tier": "A",
            "summary": narr["summary"],
            "hero": narr["hero"],
            "partner_context": {
                "their_ambition": "Centara already sits on Thailand's best water-facing guest journeys.",
                "their_pressure": "Guest transfers are still diesel speedboats — loud, weather-bound, and operated by someone else.",
                "where_navier_fits": (
                    "A premium electric water layer Centara packages with stays — "
                    "quieter arrivals, cleaner excursions, predictable run cost."
                ),
            },
            "operator_model": {
                "cost": "Predictable electric run cost on short, repeatable guest-paid routes.",
                "convenience": "Fewer handoffs, cleaner packaging, better timing.",
                "comfort": "Quieter vessel, calmer boarding, premium guest experience.",
            },
            "journeys_unlocked": journeys,
            "corridor_examples": [
                {
                    "label": j["from"] + " → " + j["to"],
                    "route_id": j["route_id"],
                    "distance_nm": j.get("distance_nm"),
                    "use_case": j.get("use_case"),
                    "status": "sealed",
                }
                for j in journeys
            ],
            "properties_highlight": [
                {"name": p["property_name"], "brand": p["brand"], "water_role": p["water_role"]}
                for p in props_in_cluster
            ],
            "use_cases": list({j.get("use_case") for j in journeys if j.get("use_case")}),
            "corridors_note": "Sealed corridor examples — hospitality captive economics, no market-size ladder.",
        })

    return {
        "partner_id": PARTNER,
        "display": "Centara Thailand",
        "archetype": "hospitality",
        "category": "hospitality_operator",
        "region": "Thailand",
        "layout": "hub",
        "coverage_note": (
            "Six Thailand hospitality clusters with sealed corridor examples — "
            "Bangkok river, Western Gulf, Eastern Gulf, Phuket/Andaman, Krabi/Phi Phi, Samui."
        ),
        "partner_logo": {
            "status": "banked",
            "main": "deck-studio/assets/logos/partners/centara/centara-logo-main.png",
            "icon": "deck-studio/assets/logos/partners/centara/centara-logo-icon.png",
        },
        "partner_context": {
            "their_ambition": (
                "Centara Hotels & Resorts has a national footprint across Thailand's coastal, "
                "island, river, and gateway destinations."
            ),
            "their_pressure": (
                "The signature arrival is still a diesel speedboat or congested road transfer — "
                "loud, fume-heavy, and leaking margin to third-party operators."
            ),
            "where_navier_fits": (
                "A premium electric water layer Centara owns end-to-end: silent arrivals, "
                "curated excursions, and predictable corridor economics on sealed geometry."
            ),
        },
        "hero": {
            "title": "Centara × Navier",
            "subtitle": "A premium electric water layer for Thailand's coastal guest journeys",
            "what_we_do_together": (
                "Centara already sits on Thailand's best water-facing guest journeys. "
                "Navier turns those stays into a cleaner, quieter, more premium way to arrive, "
                "move, and explore — starting with six Thai clusters where the hotel footprint "
                "and destination demand overlap."
            ),
        },
        "why_now": (
            "Thailand tourism is scaled and returning strongly. Centara's coastal portfolio "
            "spans river gateways, royal-coast heritage resorts, Eastern Gulf islands, "
            "Andaman arrivals, and Samui flagships — each with sealed corridor geometry ready today."
        ),
        "network_thesis": {
            "headline": "Six clusters. One premium water layer. Centara's guest journeys, upgraded.",
            "body": (
                "Centara's Thailand footprint maps cleanly to six water-rich clusters. "
                "Navier seals the corridor geometry and transparent economics; Centara owns "
                "demand, packaging, and guest service standards."
            ),
        },
        "operator_model": {
            "cost": "Predictable electric run cost on short, repeatable guest-paid routes.",
            "convenience": "Fewer transfer handoffs, cleaner packaging, better timing.",
            "comfort": "Quieter vessel, calmer boarding, premium guest experience.",
        },
        "proof_points": [
            {
                "claim": "Centara sits on Thailand's best water-facing destinations.",
                "evidence": f"{len([p for p in inventory if p.get('fit_score') == 'A'])} A-tier water-relevant properties in the inventory.",
                "source": "centara-thailand-property-inventory.json",
            },
            {
                "claim": "Corridor examples use sealed Atlas geometry.",
                "evidence": f"{len(bindings)} corridors bound to route_ids on Pioneer II range.",
                "source": "grok/centara_thailand_seal",
            },
            {
                "claim": "Economics follow the hospitality operator frame.",
                "evidence": "$1M vessel, captive guest-paid transfers, transparent run-cost skeleton.",
                "source": "centara-thailand-economics-sidecar.draft.json",
            },
        ],
        "objections": [
            {
                "concern": "We already arrange boat transfers.",
                "response": "On diesel, weather-bound schedules, with margin leaking to third parties. Navier replaces the fleet asset with a branded electric tier Centara controls.",
            },
            {
                "concern": "Each property is different.",
                "response": "One hospitality playbook across six clusters — corridor examples sealed today, pilot 1–2 corridors first.",
            },
        ],
        "phases": [
            {
                "n": 1,
                "label": "Phase 1 — pilot corridors",
                "boats": 2,
                "cities": ["pattaya-thailand", "koh-samui-thailand"],
                "route_scope": "intra",
                "narrative": "Start with Eastern Gulf (Pattaya → Koh Larn) or Samui gateway — highest visibility, shortest ops validation.",
                "timeline": "2026 H2",
                "rationale": "Family-resort demand + sealed short-hop geometry.",
            },
            {
                "n": 2,
                "label": "Phase 2 — portfolio rollout",
                "boats": 8,
                "cities": [
                    "bangkok-thailand",
                    "hua-hin-thailand",
                    "phuket-phang-nga-thailand",
                    "krabi-thailand",
                    "koh-chang-thailand",
                ],
                "route_scope": "intra",
                "narrative": "Extend to river gateway, royal coast, Andaman, and Koh Chang arrivals.",
                "timeline": "2027",
                "rationale": "Six-cluster network after pier/beach ops validated.",
            },
        ],
        "markets": markets_out,
        "next_step": (
            "Select 1–2 pilot corridors, validate pier/beach/dock operations, "
            "then scale the six-cluster network."
        ),
        "_seal_handoff": str(HANDOFF.relative_to(ROOT)),
        "_seal_at": now_iso(),
        "_deck_lane": "tasklet-owned — this file is partner-page only",
    }


def build_crosswalk(partner: dict) -> dict:
    fbt = load_json(FBT_PATH)
    atlas_ids: set[str] = set()
    for t in ("city", "priority_city"):
        for f in fbt.get(t, []):
            pid = (f.get("properties") or {}).get("id")
            if pid:
                atlas_ids.add(pid)
    anchors: dict = {}
    for m in partner.get("markets", []):
        for cid in m.get("anchor_cities", []):
            anchors[cid] = {
                "verdict": "OK" if cid in atlas_ids else "HOLD",
                "atlas_city_id": cid if cid in atlas_ids else None,
                "evidence": "Centara Thailand cluster anchor",
                "market": m.get("id"),
            }
    return {
        "_doc": "Gate-A anchor-city crosswalk for centara-thailand.",
        "partner": PARTNER,
        "build_date": now_iso()[:10],
        "updated_at": now_iso(),
        "anchors": anchors,
    }


def write_economics_sidecar(bindings: list[dict], routes: list, sidecar_draft: list[dict], apply: bool) -> list[dict]:
    ridx = route_index(routes)
    by_cluster = sidecar_by_cluster(sidecar_draft)
    out = []
    for bind in bindings:
        rid = bind["route_id"]
        feat = ridx.get(rid) if rid else None
        p = props(feat) if feat else {}
        sc = pick_sidecar_row(bind, by_cluster)
        out.append({
            **sc,
            "route_id": rid,
            "route_status": "sealed",
            "distance_nm_sealed": p.get("distance_nm"),
            "from_bp_id": bind.get("from_bp_id"),
            "to_bp_id": bind.get("to_bp_id"),
            "from_node_id": bind.get("from_node_id"),
            "to_node_id": bind.get("to_node_id"),
            "sealed_at": now_iso(),
        })
    if apply:
        ECON_SIDECAR_OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    apply = args.apply and not args.dry_run

    report: dict = {
        "partner": PARTNER,
        "generated_at": now_iso(),
        "apply": apply,
        "routes_minted": [],
        "corridors_bound": [],
        "held": [],
        "deck_rebuilt": False,
    }

    routes = route_features(load_json(ROUTES_PATH))
    bp_idx = build_bp_index(load_json(FBT_PATH))
    mask = load_land_mask()
    bindings = copy.deepcopy(CORRIDOR_BINDINGS)
    sidecar_draft = json.loads(SIDECAR_HANDOFF.read_text())
    inventory = json.loads(INVENTORY_HANDOFF.read_text())

    # Mint Chalong → Karon
    for bind in bindings:
        if bind.get("mint_from_bp"):
            rid = mint_chalong_karon(routes, bp_idx, mask, apply)
            bind["route_id"] = rid
            report["routes_minted"].append({
                "route_id": rid,
                "from_bp": CHALONG_BP,
                "to_bp": KARON_BP,
                "tag": CHALONG_KARON_TAG,
            })

    ridx = route_index(routes)
    for bind in bindings:
        rid = bind.get("route_id")
        if not rid or rid not in ridx:
            report["held"].append({"cluster": bind["cluster_id"], "route_id": rid, "reason": "missing_route"})
            continue
        p = props(ridx[rid])
        report["corridors_bound"].append({
            "cluster_id": bind["cluster_id"],
            "route_id": rid,
            "distance_nm": p.get("distance_nm"),
            "from": p.get("from"),
            "to": p.get("to"),
            "from_bp_id": bind.get("from_bp_id"),
            "to_bp_id": bind.get("to_bp_id"),
        })

    partner = build_partner_doc(bindings, routes, sidecar_draft, inventory)
    corridors = build_corridors_doc(bindings, routes, sidecar_draft)
    crosswalk = build_crosswalk(partner)
    econ_sidecar = write_economics_sidecar(bindings, routes, sidecar_draft, apply)

    if apply:
        PITCH_PATH.parent.mkdir(parents=True, exist_ok=True)
        PITCH_PATH.write_text(json.dumps(partner, indent=1, ensure_ascii=False) + "\n")
        DC_PATH.write_text(json.dumps(partner, indent=1, ensure_ascii=False) + "\n")
        CORR_OUT.parent.mkdir(parents=True, exist_ok=True)
        CORR_OUT.write_text(json.dumps(corridors, indent=1, ensure_ascii=False) + "\n")
        CROSSWALK_OUT.write_text(json.dumps(crosswalk, indent=1, ensure_ascii=False) + "\n")

    report["files"] = [
        str(PITCH_PATH.relative_to(ROOT)),
        str(DC_PATH.relative_to(ROOT)),
        str(CORR_OUT.relative_to(ROOT)),
        str(CROSSWALK_OUT.relative_to(ROOT)),
        str(ECON_SIDECAR_OUT.relative_to(ROOT)),
    ]
    report["corridor_count"] = len(report["corridors_bound"])
    report["held_count"] = len(report["held"])
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 1 if report["held"] else 0


if __name__ == "__main__":
    raise SystemExit(main())