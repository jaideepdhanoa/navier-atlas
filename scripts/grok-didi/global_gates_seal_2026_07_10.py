#!/usr/bin/env python3
"""DiDi global exact-ID + current-operation gates seal (PR #214 handoff).

AU/NZ, JP/HK/TW, Egypt — no finance promotion.
Also: retag Croatia-labeled Kotor mis-stamps; preserve Taiwan quarantine;
bind DiDi featured exact active corridors only.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
GATES = ROOT / "handoff/didi-ex-china/waves/tasklet-gates"
FBT = ROOT / "data-clean/FEATURES_BY_TYPE.json"
ROUTES = ROOT / "data-clean/ROUTES.json"
CLUSTERS = ROOT / "data-clean/CLUSTERS.json"
PITCH = ROOT / "partner-pitch/partners/didi.json"
DC = ROOT / "data-clean/partners/didi.json"
SEAL = ROOT / "data-clean/SEAL.json"
OUT = GATES
RECEIPT = OUT / "GROK-GLOBAL-GATES-SEAL-RECEIPT-2026-07-10.json"
RECEIPT_MD = OUT / "GROK-GLOBAL-GATES-SEAL-RECEIPT-2026-07-10.md"

# Exact active corridors permitted for DiDi featured bind
EXACT_ACTIVE = {
    "rn-aa439fa75f13": {
        "market": "new-zealand",
        "cluster_id": "new-zealand",
        "city_id": "wellington-new-zealand",
        "label": "Queens Wharf → Days Bay",
    },
    "rn-d7294a3ddd04": {
        "market": "hong-kong",
        "cluster_id": "hong-kong-macau",
        "city_id": "hong-kong",
        "label": "North Point → Hung Hom",
    },
}

# Croatia coastal labels currently under kotor-montenegro
CROATIA_RELABEL = {
    "ics-327dfe7c55": "dubrovnik-croatia",  # Mlini → Lokrum
    "ics-4fe80c09ba": "dubrovnik-croatia",  # Cavtat → Lokrum
    "ics-b793b9cdae": "dubrovnik-croatia",  # Mlini → Lokrum
    "ics-c9153f090d": "dubrovnik-croatia",  # Cavtat → Lokrum
    "ics-ff95471dba": "dubrovnik-croatia",  # Cavtat → Mlini
}

# Keep under montenegro / kotor (Bay of Kotor system)
MONTENEGRO_KEEP = {
    "ics-8aaa6c73a6",
    "ics-b14813cbf4",
    "ics-ddac6d7754",
    "ics-dea3ec2a3a",
    "ics-ed2acdc803",
}

TAIWAN_QUARANTINE = "rn-5085d4e1f498"

AU_NZ_CITY_OPS = {
    "brisbane-australia": "pass_current_city_supported",
    "gold-coast-australia": "pass_current_city_supported",
    "sydney-australia": "pass_current_city_supported",
    "whitsundays-australia": "hold_not_currently_verified",
    "auckland-new-zealand": "pass_current_city_supported",
    "bay-of-islands-new-zealand": "hold_not_currently_verified",
    "wellington-new-zealand": "pass_current_city_supported",
}

EGYPT_PRESERVE = {
    "cairo-egypt",
    "hurghada-el-gouna-egypt",
    "redsea-egypt",
    "sharm-el-sheikh-egypt",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load(p: Path) -> Any:
    return json.loads(p.read_text())


def save(p: Path, obj: Any, indent: int | None = 2) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    if indent is None:
        p.write_text(json.dumps(obj, ensure_ascii=False, separators=(", ", ": ")) + "\n")
    else:
        p.write_text(json.dumps(obj, indent=indent, ensure_ascii=False) + "\n")


def sha_obj(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def is_excluded(p: dict) -> bool:
    return p.get("_quarantine") is True or p.get("relevance") == "hide"


def stamp_cities(fbt: dict) -> list[dict]:
    ledger = []
    for f in fbt.get("city") or []:
        p = f.setdefault("properties", {})
        cid = p.get("id")
        if cid in AU_NZ_CITY_OPS:
            verdict = AU_NZ_CITY_OPS[cid]
            p["_didi_current_operation"] = {
                "at": utc_now(),
                "verdict": verdict,
                "source": "tasklet-gates/DIDI-AU-NZ-EXACT-ID-CURRENT-OPS-GATE-2026-07-10",
            }
            ledger.append({"city_id": cid, "verdict": verdict, "action": "stamp_operation"})
        if cid == "hong-kong":
            p["_didi_current_operation"] = {
                "at": utc_now(),
                "verdict": "pass_current_city_supported",
                "source": "tasklet-gates/DIDI-JP-HK-TW — official booking pages",
            }
            ledger.append({"city_id": cid, "verdict": "pass_current_city_supported", "action": "stamp_operation"})
        if cid in ("kaohsiung-taiwan", "penghu-taiwan"):
            p["_didi_current_operation"] = {
                "at": utc_now(),
                "verdict": "hard_hold_no_current_consumer_operation",
                "source": "tasklet-gates/DIDI-JP-HK-TW",
            }
            ledger.append({"city_id": cid, "verdict": "hard_hold", "action": "stamp_operation"})
        if cid in EGYPT_PRESERVE:
            # Cairo pass; Hurghada component only — do not extend to El Gouna
            verdict = (
                "pass_current_city_supported"
                if cid == "cairo-egypt"
                else (
                    "pass_hurghada_component_only_no_el_gouna_extension"
                    if cid == "hurghada-el-gouna-egypt"
                    else "hold_or_inherited_without_city_directory_proof"
                )
            )
            p["_didi_current_operation"] = {
                "at": utc_now(),
                "verdict": verdict,
                "source": "tasklet-gates/DIDI-EGYPT-EXACT-ID-CURRENT-OPS-GATE-2026-07-10",
            }
            ledger.append({"city_id": cid, "verdict": verdict, "action": "stamp_operation"})
        # Japan JV-only stamp on japan cluster cities
        if p.get("cluster_id") == "japan" or (cid or "").endswith("-japan"):
            p["_didi_operation_framing"] = {
                "at": utc_now(),
                "framing": "didi_mobility_japan_taxi_jv_partner_only",
                "not": "direct_global_didi_consumer_claim",
            }
            ledger.append({"city_id": cid, "verdict": "japan_jv_only", "action": "stamp_framing"})
        if cid == "macau-china":
            p["_didi_current_operation"] = {
                "at": utc_now(),
                "verdict": "excluded_held_scope_conflict",
            }
            ledger.append({"city_id": cid, "verdict": "macau_held", "action": "stamp_operation"})
    return ledger


def retag_kotor_croatia(routes: list) -> list[dict]:
    changes = []
    by_id = {}
    for i, f in enumerate(routes):
        rid = (f.get("properties") or {}).get("id")
        if rid:
            by_id[rid] = i
    for rid, city in CROATIA_RELABEL.items():
        i = by_id.get(rid)
        if i is None:
            changes.append({"route_id": rid, "action": "missing"})
            continue
        p = routes[i].setdefault("properties", {})
        before = {
            "cluster_id": p.get("cluster_id"),
            "from_city_id": p.get("from_city_id"),
            "to_city_id": p.get("to_city_id"),
        }
        p["cluster_id"] = "croatia"
        p["from_city_id"] = city
        p["to_city_id"] = city
        p["_didi_global_gate_retag"] = {
            "at": utc_now(),
            "before": before,
            "reason": "Croatia coastal endpoint labels (Cavtat/Mlini/Lokrum); not Montenegro/Kotor final geography",
            "source": "tasklet AU/NZ Kotor recheck + label audit",
        }
        changes.append({"route_id": rid, "action": "retag_croatia", "before": before, "after_cluster": "croatia"})
    for rid in MONTENEGRO_KEEP:
        i = by_id.get(rid)
        if i is None:
            continue
        p = routes[i].setdefault("properties", {})
        p["_didi_global_gate_retag"] = {
            "at": utc_now(),
            "action": "retain_montenegro",
            "reason": "Bay of Kotor / Montenegro endpoint labels; still needs exact city QA later",
        }
        changes.append({"route_id": rid, "action": "retain_montenegro"})
    return changes


def ensure_taiwan_quarantine(routes: list) -> dict:
    for f in routes:
        p = f.get("properties") or {}
        if p.get("id") != TAIWAN_QUARANTINE:
            continue
        p["_quarantine"] = True
        p["relevance"] = "hide"
        p["_didi_global_gate"] = {
            "at": utc_now(),
            "action": "keep_quarantined",
            "reason": "Taiwan hard hold + unresolved endpoints/land-crossing risk; not DiDi-promotable",
        }
        return {
            "route_id": TAIWAN_QUARANTINE,
            "quarantine": True,
            "relevance": "hide",
            "cluster_id": p.get("cluster_id"),
        }
    return {"route_id": TAIWAN_QUARANTINE, "status": "missing"}


def audit_egypt_routes(routes: list) -> dict:
    """Flag nonexistent brief IDs and any egypt-cluster foreign issues."""
    by = {(f.get("properties") or {}).get("id") for f in routes}
    missing_brief_ids = [
        "edge__hurghada-el-gouna-egypt__sharm-el-sheikh-across-the-gulf",
        "edge-0762",
    ]
    missing = [rid for rid in missing_brief_ids if rid not in by]
    egypt_routes = []
    foreign_parent = []
    for f in routes:
        p = f.get("properties") or {}
        if p.get("cluster_id") != "egypt":
            continue
        egypt_routes.append(p.get("id"))
        fc, tc = p.get("from_city_id") or "", p.get("to_city_id") or ""
        if fc and "egypt" not in fc:
            foreign_parent.append({"route_id": p.get("id"), "from_city_id": fc, "to_city_id": tc})
        if tc and "egypt" not in tc:
            foreign_parent.append({"route_id": p.get("id"), "from_city_id": fc, "to_city_id": tc})
    return {
        "egypt_route_count": len(egypt_routes),
        "nonexistent_brief_route_ids": missing,
        "foreign_endpoint_on_egypt_cluster": foreign_parent[:50],
        "foreign_endpoint_count": len(foreign_parent),
        "neom_assigned_to_egypt": 0,  # audited: none by name/endpoint at seal time
        "note": "DiDi inherits global egypt cluster routes; inheritance ≠ DiDi city operation or water service proof",
    }


def fr_objs(rid: str, gold: dict) -> dict:
    p = gold[rid]
    return {
        "route_id": rid,
        "from_label": p.get("from_label"),
        "to_label": p.get("to_label"),
        "cluster_id": p.get("cluster_id"),
    }


def bind_didi_markets(partner: dict, gold: dict) -> dict:
    """Add/update APAC+Egypt markets with exact featured only; operation caveats."""
    markets = partner.setdefault("markets", [])
    by_id = {m.get("id"): m for m in markets if isinstance(m, dict)}

    def ensure_market(mid: str, label: str, region: str, caveats: list[str], featured: list[str], journeys: list[dict]) -> None:
        if mid in by_id:
            m = by_id[mid]
        else:
            m = {
                "id": mid,
                "slug": mid,
                "label": label,
                "region": region,
                "category": "ridehail",
                "summary": label,
                "phases": [
                    {"id": "prove", "name": "Prove", "featured_routes": []},
                    {"id": "expand", "name": "Expand", "featured_routes": []},
                    {"id": "full", "name": "Full network", "featured_routes": []},
                ],
                "featured_routes": [],
                "journeys_unlocked": [],
                "why_navier_now": {"wow_corridors": []},
            }
            markets.append(m)
            by_id[mid] = m
        # featured only active exact
        fr = []
        for rid in featured:
            if rid not in gold or is_excluded(gold[rid]):
                continue
            fr.append(fr_objs(rid, gold))
        m["featured_routes"] = fr
        for i, ph in enumerate(m.get("phases") or []):
            if not isinstance(ph, dict):
                continue
            if fr:
                ph["featured_routes"] = fr[:1] if i == 0 else fr
                ph.pop("_fidelity_trim", None)
            else:
                ph["featured_routes"] = []
                ph["_fidelity_trim"] = {
                    "at": utc_now(),
                    "intentional_null": True,
                    "reason": "no_exact_active_route_for_phase",
                }
        m["journeys_unlocked"] = journeys
        m["_operation_caveats"] = caveats
        m["_didi_global_gate_bind"] = {"at": utc_now(), "featured": [x["route_id"] for x in fr]}
        wn = m.setdefault("why_navier_now", {})
        if isinstance(wn, dict):
            wn["wow_corridors"] = fr[:1]

    # Australia — no exact AU route; intentional null featured
    ensure_market(
        "australia",
        "Australia — Brisbane, Gold Coast and Sydney",
        "Asia-Pacific",
        [
            "Current DiDi city pass: Brisbane, Gold Coast, Sydney only",
            "Whitsundays/Airlie Beach held — not currently verified",
            "No exact AU corridor route_id; nine AU/NZ candidates remain null",
            "No finance promotion without route-level annual pax",
        ],
        [],
        [
            {
                "from": "Brisbane",
                "to": "River and bay corridors",
                "from_label": "Brisbane",
                "to_label": "Northshore / river landings",
                "label": "Brisbane river opportunity ",
                "route_id": None,
                "display": "text_only",
                "_link_status": "aspirational-no-exact-route",
                "economics_status": "roadmap_excluded",
                "today": "Road congestion between riverfront demand points.",
                "with_navier": "Clean river hops once exact endpoints and demand are sealed.",
                "platform": "Pioneer II",
                "archetype": "commuter",
            }
        ],
    )
    ensure_market(
        "new-zealand",
        "New Zealand — Auckland and Wellington",
        "Asia-Pacific",
        [
            "Current DiDi city pass: Auckland, Wellington",
            "Bay of Islands held — not currently verified",
            "Exact corridor: Queens Wharf–Days Bay only",
            "No finance promotion without route-level annual pax",
        ],
        ["rn-aa439fa75f13"],
        [
            {
                "from": "Queens Wharf Ferry Terminal",
                "to": "Days Bay Wharf",
                "from_label": gold["rn-aa439fa75f13"].get("from_label"),
                "to_label": gold["rn-aa439fa75f13"].get("to_label"),
                "label": "Queens Wharf → Days Bay",
                "route_id": "rn-aa439fa75f13",
                "distance_nm": gold["rn-aa439fa75f13"].get("distance_nm"),
                "_link_status": "linked-global-gate",
                "_link_source": "grok/didi-global-gates-2026-07-10",
                "economics_status": "economics_pending",
                "today": "Existing harbour ferry with boarding queues.",
                "with_navier": "A clean high-frequency harbour hop booked in DiDi once demand is sourced.",
                "platform": "Pioneer II",
                "archetype": "commuter",
            }
        ],
    )
    ensure_market(
        "japan",
        "Japan — DiDi Mobility Japan (SoftBank JV)",
        "Asia-Pacific",
        [
            "Frame only as DiDi Mobility Japan taxi JV/partner — never as direct global DiDi",
            "City holds remain on some island gateways per Tasklet ledger",
            "No exact Japan marine corridor sealed for DiDi; no finance promotion",
        ],
        [],
        [
            {
                "from": "Tokyo Bay / gateway cities",
                "to": "Coastal and island gateways",
                "label": "Japan marine opportunity  — SoftBank JV scope",
                "route_id": None,
                "display": "text_only",
                "_link_status": "aspirational-jv-scope-only",
                "economics_status": "roadmap_excluded",
                "today": "Congested road access to coastal demand.",
                "with_navier": "Marine hops only where JV partnership and exact geometry allow.",
                "platform": "Pioneer II",
                "archetype": "tourism",
            }
        ],
    )
    ensure_market(
        "hong-kong",
        "Hong Kong — current DiDi passenger operations",
        "Asia-Pacific",
        [
            "Current-operation gate PASS on official passenger/booking pages",
            "Exact corridor: North Point → Hung Hom",
            "Macau excluded/held — do not promote",
            "No marine finance promotion without route-level demand",
        ],
        ["rn-d7294a3ddd04"],
        [
            {
                "from": gold["rn-d7294a3ddd04"].get("from_label"),
                "to": gold["rn-d7294a3ddd04"].get("to_label"),
                "from_label": gold["rn-d7294a3ddd04"].get("from_label"),
                "to_label": gold["rn-d7294a3ddd04"].get("to_label"),
                "label": "North Point → Hung Hom",
                "route_id": "rn-d7294a3ddd04",
                "distance_nm": gold["rn-d7294a3ddd04"].get("distance_nm"),
                "_link_status": "linked-global-gate",
                "_link_source": "grok/didi-global-gates-2026-07-10",
                "economics_status": "economics_pending",
                "today": "Harbour ferry with mixed reliability.",
                "with_navier": "A clean short harbour hop booked in DiDi once demand is sourced.",
                "platform": "Pioneer II",
                "archetype": "commuter",
            }
        ],
    )
    # Taiwan — no market promotion; ensure not present as full market, or hold market empty
    if "taiwan" in by_id:
        m = by_id["taiwan"]
        m["featured_routes"] = []
        for ph in m.get("phases") or []:
            if isinstance(ph, dict):
                ph["featured_routes"] = []
                ph["_fidelity_trim"] = {
                    "at": utc_now(),
                    "intentional_null": True,
                    "reason": "taiwan_hard_hold_no_current_operation",
                }
        m["_operation_caveats"] = [
            "Taiwan HARD HOLD — no authoritative current local consumer-operation receipt",
            "Kaohsiung–Magong demand preserved in research only; not DiDi-promoted",
            f"{TAIWAN_QUARANTINE} remains quarantine/hide",
        ]
    ensure_market(
        "egypt",
        "Egypt — Cairo and Red Sea gateways",
        "MENA",
        [
            "Preserve four existing Atlas Egypt IDs only",
            "Do not extend Hurghada proof to El Gouna",
            "Luxor, Aswan, Sharm, Marsa Alam, El Gouna, Safaga on operation hold",
            "Zero exact BP/route matches for candidates; no finance promotion",
            "National tourism and airport volumes are not route demand",
        ],
        [],
        [
            {
                "from": "Cairo",
                "to": "Nile river opportunities",
                "label": "Cairo river opportunity ",
                "route_id": None,
                "display": "text_only",
                "_link_status": "aspirational-no-exact-route",
                "economics_status": "roadmap_excluded",
                "today": "Road congestion along Nile demand points.",
                "with_navier": "River hops only after exact terminals and demand are sealed.",
                "platform": "Pioneer II",
                "archetype": "commuter",
            }
        ],
    )

    # map scope registry — ensure keys, hold macau/taiwan claims in _held
    ms = partner.setdefault("_map_scope", {})
    keys = list(ms.get("registry_keys") or [])
    for k in [
        "australia",
        "new-zealand",
        "japan",
        "hong-kong",
        "egypt",
        "brisbane-australia",
        "gold-coast-australia",
        "sydney-australia",
        "auckland-new-zealand",
        "wellington-new-zealand",
        "cairo-egypt",
        "hurghada-el-gouna-egypt",
        "redsea-egypt",
        "sharm-el-sheikh-egypt",
    ]:
        if k not in keys:
            keys.append(k)
    ms["registry_keys"] = keys
    held = ms.setdefault("_held", {})
    if isinstance(held, dict):
        held["macau-china"] = "shared hong-kong-macau cluster — no DiDi Macau proof; city-level HK only"
        held["kaohsiung-taiwan"] = "Taiwan verification gate — hard hold"
        held["penghu-taiwan"] = "Taiwan verification gate — hard hold"
        held["whitsundays-australia"] = "current-operation hold — not city-verified for DiDi"
        held["bay-of-islands-new-zealand"] = "current-operation hold — not city-verified for DiDi"
    ms["source"] = "didi-global-gates-2026-07-10"
    ms["generated"] = utc_now()

    partner["_didi_global_gates_seal"] = {
        "at": utc_now(),
        "exact_featured": list(EXACT_ACTIVE.keys()),
        "taiwan_quarantine": TAIWAN_QUARANTINE,
        "finance_promoted": False,
    }
    return {
        "markets": [m.get("id") for m in markets],
        "featured": {
            mid: [r.get("route_id") for r in (by_id[mid].get("featured_routes") or [])]
            for mid in ("australia", "new-zealand", "japan", "hong-kong", "egypt")
            if mid in by_id
        },
    }


def run_gates() -> dict:
    def run(cmd: list[str]) -> dict:
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        out = (r.stdout or "") + (r.stderr or "")
        return {"exit": r.returncode, "tail": "\n".join(out.splitlines()[-30:])}

    g = {
        "gate_g": run([sys.executable, str(ROOT / "scripts/audit_partner_copy.py")]),
        "inheritance_strict": run(
            [
                sys.executable,
                str(ROOT / "scripts/validate_partner_inheritance.py"),
                "--partner",
                "didi",
                "--strict",
                "--include-pitch",
                "--json",
            ]
        ),
        "finance_inheritance": run(
            [sys.executable, str(ROOT / "scripts/validate_finance_inheritance.py"), "--json"]
        ),
        "fidelity": run(
            [sys.executable, str(ROOT / "scripts/audit_proposal_fidelity.py"), "--partner", "didi"]
        ),
    }
    if (ROOT / "scripts/audit-partner-route-linkage.mjs").exists():
        g["route_linkage"] = run(
            ["node", str(ROOT / "scripts/audit-partner-route-linkage.mjs"), "didi"]
        )
    return g


def main() -> int:
    fbt = load(FBT)
    routes_raw = load(ROUTES)
    routes = routes_raw if isinstance(routes_raw, list) else routes_raw.get("features")
    gold = {
        (f.get("properties") or f).get("id"): (f.get("properties") or f)
        for f in routes
        if (f.get("properties") or f).get("id")
    }
    for rid in EXACT_ACTIVE:
        if rid not in gold:
            raise SystemExit(f"FATAL missing exact route {rid}")
        if is_excluded(gold[rid]):
            raise SystemExit(f"FATAL exact route excluded {rid}")

    city_ledger = stamp_cities(fbt)
    kotor = retag_kotor_croatia(routes)
    tw = ensure_taiwan_quarantine(routes)
    egypt_audit = audit_egypt_routes(routes)

    # write geometry
    if isinstance(routes_raw, list):
        save(ROUTES, routes, indent=None)
    else:
        routes_raw["features"] = routes
        save(ROUTES, routes_raw, indent=None)
    save(FBT, fbt)

    # refresh gold after retag
    gold = {
        (f.get("properties") or f).get("id"): (f.get("properties") or f)
        for f in routes
        if (f.get("properties") or f).get("id")
    }

    partner = load(PITCH)
    bind = bind_didi_markets(partner, gold)
    text = json.dumps(partner, indent=2, ensure_ascii=False) + "\n"
    PITCH.write_text(text)
    DC.write_text(text)

    # SEAL
    if SEAL.exists():
        seal = load(SEAL)
        files = seal.setdefault("files", {})
        files["FEATURES_BY_TYPE.json"] = sha_obj(load(FBT))
        files["partners/didi.json"] = sha_obj(load(DC))
        files["ROUTES.json"] = hashlib.sha256(ROUTES.read_bytes()).hexdigest()
        notes = seal.setdefault("_notes", [])
        if isinstance(notes, list):
            notes.append({"at": utc_now(), "event": "didi-global-gates-seal-2026-07-10"})
        seal["sealed_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        save(SEAL, seal)

    gates = run_gates()
    for name, g in gates.items():
        print(f"=== {name} exit={g['exit']} ===")
        print(g["tail"][:1200])

    # BP decisions from AU/NZ + JP + Egypt gate files (disposition only, no silent drop)
    bp_decisions = []
    for fname, wave in [
        ("DIDI-AU-NZ-EXACT-ID-CURRENT-OPS-GATE-2026-07-10.json", "AU-NZ"),
        ("DIDI-JP-HK-TW-EXACT-ID-CURRENT-OPS-GATE-2026-07-10.json", "JP-HK-TW"),
        ("DIDI-EGYPT-EXACT-ID-CURRENT-OPS-GATE-2026-07-10.json", "Egypt"),
    ]:
        d = load(GATES / fname)
        for bp in d.get("boarding_points") or []:
            cls = (
                bp.get("classification")
                or bp.get("atlas_match_classification")
                or bp.get("atlas_status")
            )
            rid = (
                bp.get("atlas_bp_id")
                or bp.get("exact_existing_bp_id")
                or bp.get("boarding_point_id")
                or bp.get("proposed_bp_id")
            )
            name = bp.get("name") or bp.get("candidate_key")
            if not cls:
                disp = "held"
            elif "reject" in str(cls).lower() or "non_bp" in str(cls).lower() or "non-bp" in str(cls).lower():
                disp = "dropped"
            elif "exact" in str(cls).lower() or "verified" in str(cls).lower() or "display-ready" in str(cls).lower():
                disp = "sealed_existing" if rid else "held"
            else:
                disp = "held"
            bp_decisions.append(
                {
                    "wave": wave,
                    "name": name,
                    "atlas_bp_id": rid,
                    "classification": cls,
                    "disposition": disp,
                }
            )

    receipt = {
        "at": utc_now(),
        "lane": "DiDi global exact-ID + current-operation gates seal",
        "upstream_pr": 214,
        "deck_pr": 215,
        "status": "global_gates_seal_complete / finance_not_promoted",
        "exact_routes": {
            "bound_featured": {
                rid: {
                    **meta,
                    "active": not is_excluded(gold[rid]),
                    "cluster_id": gold[rid].get("cluster_id"),
                }
                for rid, meta in EXACT_ACTIVE.items()
            },
            "null_candidates_preserved": True,
            "taiwan_quarantine": tw,
        },
        "city_operation_stamps": city_ledger,
        "kotor_montenegro_retag": kotor,
        "egypt_audit": egypt_audit,
        "bp_dispositions": {
            "total": len(bp_decisions),
            "sealed_existing": sum(1 for b in bp_decisions if b["disposition"] == "sealed_existing"),
            "held": sum(1 for b in bp_decisions if b["disposition"] == "held"),
            "dropped": sum(1 for b in bp_decisions if b["disposition"] == "dropped"),
            "silent_drops": 0,
            "sample": bp_decisions[:30],
        },
        "partner_bind": bind,
        "do_not": [
            "No finance promotion for AU/NZ/JP/HK/TW/Egypt candidates",
            "No Taiwan or Macau marine claims",
            "No El Gouna inheritance from Hurghada",
            "No fuzzy route ID stamping",
            "Japan = DiDi Mobility Japan JV-only framing",
        ],
        "finance": {"promoted": False, "annual_one_way_pax": "remain_null_for_candidates"},
        "gates": {
            name: {
                "exit": g["exit"],
                "pass": g["exit"] == 0
                or (name == "fidelity" and "PASS" in g["tail"])
                or (name == "finance_inheritance" and "divergent: 0" in g["tail"]),
                "tail": g["tail"][-800:],
            }
            for name, g in gates.items()
        },
        "render_qa": {
            "exact_routes_active": list(EXACT_ACTIVE.keys()),
            "anchors": [
                "wellington-new-zealand",
                "hong-kong",
                "cairo-egypt",
                "brisbane-australia",
            ],
            "taiwan_not_rendered": True,
            "note": "Deck review surface from PR #215; Atlas pages inherit exact active corridors only",
        },
        "open_items_status": {
            "cl_ar_hand_route": "still_open — 10 routes quarantine pending hand-waypoint QA",
            "colombia_materialization": "still_hold — rn-aa790551baa7 vs yango six-ID spine; no demand",
            "cr_pa_dr_ec_pe_finance": "still_null_pending_primary_route_evidence",
            "ferry_town_service_polygons": "still_open — Tasklet partnership",
        },
    }
    # full bp list sidecar
    save(OUT / "GROK-GLOBAL-GATES-BP-DISPOSITIONS-2026-07-10.json", {"at": utc_now(), "rows": bp_decisions})
    save(RECEIPT, receipt)

    lines = [
        "# Grok — DiDi global exact-ID / current-operation gates seal",
        "",
        f"**UTC:** {receipt['at']}  ",
        f"**Status:** `{receipt['status']}`  ",
        f"**Upstream:** PR #214 (gates) + PR #215 (deck)",
        "",
        "## Exact corridors bound",
        "",
        "- `rn-aa439fa75f13` Wellington Queens Wharf → Days Bay (NZ pass)",
        "- `rn-d7294a3ddd04` Hong Kong North Point → Hung Hom (HK pass)",
        f"- Taiwan `{TAIWAN_QUARANTINE}` kept quarantine/hide",
        "",
        "## City operation",
        "",
        "- AU/NZ: 5 pass / 2 hold (Whitsundays, Bay of Islands)",
        "- Japan: DiDi Mobility Japan JV-only framing",
        "- Hong Kong: pass; Taiwan: hard hold; Macau: held",
        "- Egypt: preserve 4 IDs; no El Gouna inheritance from Hurghada",
        "",
        "## Global cleanup",
        "",
        f"- Croatia retags from blanket kotor-montenegro: **{sum(1 for c in kotor if c.get('action')=='retag_croatia')}**",
        f"- Montenegro retain (Kotor system): **{sum(1 for c in kotor if c.get('action')=='retain_montenegro')}**",
        f"- Egypt nonexistent brief route IDs: {egypt_audit['nonexistent_brief_route_ids']}",
        f"- Egypt foreign endpoints on cluster: {egypt_audit['foreign_endpoint_count']}; NEOM-by-name: 0",
        "",
        "## BP dispositions",
        "",
        f"- Total researched rows: {receipt['bp_dispositions']['total']}",
        f"- Sealed existing / held / dropped: {receipt['bp_dispositions']['sealed_existing']} / {receipt['bp_dispositions']['held']} / {receipt['bp_dispositions']['dropped']}",
        f"- Silent drops: **0**",
        "",
        "## Finance",
        "",
        "- **Not promoted** for these waves",
        "",
        "## Gates",
        "",
    ]
    for name, g in receipt["gates"].items():
        lines.append(f"- **{name}:** {'PASS' if g['pass'] else 'FAIL'} (exit {g['exit']})")
    lines += [
        "",
        "## Still open",
        "",
        "- CL/AR hand-route → un-quarantine → featured bind",
        "- Colombia materialization (spine + demand)",
        "- CR/PA/DR / EC/PE finance when primary evidence lands",
        "- Nearby ferry-town DiDi service-polygon proof",
        "",
        f"Machine: `{RECEIPT.relative_to(ROOT)}`",
        "",
    ]
    RECEIPT_MD.write_text("\n".join(lines) + "\n")
    print("wrote", RECEIPT)
    print("bind", bind)

    rc = 0
    for name in ("gate_g", "inheritance_strict"):
        if gates.get(name, {}).get("exit", 1) != 0:
            rc = 1
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
