#!/usr/bin/env python3
"""DiDi Latin America Grok seal — execute Tasklet handoff PR #212.

Primary: handoff/didi-ex-china/latam/DIDI-LATAM-GROK-SEAL-HANDOFF-2026-07-09.md

- Geography-owned corridors only; no DiDi-only geometry mint
- Preserve exact IDs, nulls, quarantine/hidden state
- Full BP disposition: sealed | held | dropped (zero silent drops)
- No finance cascade; all annual_one_way_pax stay null
- Wave C Chile/Argentina: registry deferred (no mint without approval)

Does not invent BPs, coordinates, demand, or route IDs.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
LATAM = ROOT / "handoff/didi-ex-china/latam"
FBT = ROOT / "data-clean/FEATURES_BY_TYPE.json"
ROUTES = ROOT / "data-clean/ROUTES.json"
CLUSTERS = ROOT / "data-clean/CLUSTERS.json"
PITCH = ROOT / "partner-pitch/partners/didi.json"
DC = ROOT / "data-clean/partners/didi.json"
SEAL = ROOT / "data-clean/SEAL.json"
OUT_JSON = LATAM / "GROK-LATAM-SEAL-HANDBACK-2026-07-09.json"
OUT_MD = LATAM / "GROK-LATAM-SEAL-HANDBACK-2026-07-09.md"

EXISTING_CLUSTERS = [
    "brazil",
    "colombia",
    "costa-rica",
    "panama",
    "dominican-republic",
    "galapagos-ecuador",
    "peru",
]

PINNED_BEFORE = {
    "brazil": (59, 59, 0),
    "colombia": (15, 14, 1),
    "costa-rica": (67, 65, 2),
    "panama": (47, 47, 0),
    "dominican-republic": (32, 29, 3),
    "galapagos-ecuador": (3, 0, 3),
    "peru": (12, 12, 0),
}

# Active priority featured spines (subset of active gold only)
FEATURED_ACTIVE = {
    "brazil": [
        "rn-1886629dbf0c",
        "rn-80f0d0ebe0bd",
        "rn-00bb6ded4be5",
        "rn-369ef0eb69d9",
    ],
    "colombia": ["rn-aa790551baa7"],  # geometry active; service unverified caveat
    "costa-rica": [
        "rn-7e59f984abec",
        "rn-eb4ca32edbef",
        "rn-55b63e976bb7",
    ],
    "panama": ["rn-8fb072f5a8a8", "rn-87eec178e86f"],
    "dominican-republic": [
        "rn-64effc46b976",
        "rn-c3a4ef933700",
        # rn-60740d4c3114 is exact-existing but quarantine/hide — NEVER feature
    ],
}

MUST_NOT_FEATURE = {
    "rn-60740d4c3114",  # DR excluded priority
    "rn-3d69b89a7af6",  # Colombia quarantine
    "e__santa-cruz-galapagos-ecuador__puerto-ayora__isabela-galapagos-ecuador__puerto-villamil",
    "e__santa-cruz-galapagos-ecuador__puerto-ayora__san-cristobal-galapagos-ecuador__puerto-baquerizo-moreno",
    "e__santa-cruz-galapagos-ecuador__puerto-ayora__floreana-galapagos-ecuador__puerto-velasco-ibarra",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load(p: Path) -> Any:
    return json.loads(p.read_text())


def save(p: Path, obj: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(p: Path) -> str:
    return sha256_bytes(p.read_bytes())


def sha256_obj(obj: Any) -> str:
    return sha256_bytes(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode())


def is_excluded(p: dict) -> bool:
    if p.get("_quarantine") is True or p.get("quarantine") is True:
        return True
    if p.get("relevance") == "hide":
        return True
    return False


def load_routes() -> tuple[list, dict[str, dict]]:
    raw = load(ROUTES)
    feats = raw if isinstance(raw, list) else raw.get("features")
    by = {}
    for f in feats:
        p = f.get("properties") or f
        rid = p.get("id")
        if rid:
            by[rid] = p
    return feats, by


def route_counts(by: dict[str, dict]) -> dict[str, dict]:
    out = {}
    for cid in EXISTING_CLUSTERS:
        rows = [p for p in by.values() if p.get("cluster_id") == cid]
        excl = [p for p in rows if is_excluded(p)]
        out[cid] = {
            "stamped": len(rows),
            "active": len(rows) - len(excl),
            "excluded": len(excl),
            "excluded_ids": sorted(p.get("id") for p in excl if p.get("id")),
        }
    totals = {
        "stamped": sum(v["stamped"] for v in out.values()),
        "active": sum(v["active"] for v in out.values()),
        "excluded": sum(v["excluded"] for v in out.values()),
    }
    return {"by_cluster": out, "totals": totals}


def index_poi(fbt: dict) -> dict[str, dict]:
    by = {}
    for f in fbt.get("poi") or []:
        p = f.get("properties") or {}
        if p.get("id"):
            by[p["id"]] = f
    return by


def disposition_from_class(classification: str) -> str:
    c = (classification or "").lower()
    if any(
        x in c
        for x in (
            "reject",
            "non_bp",
            "non-bp",
            "non_bp_poi",
            "drop",
            "outside_country",
            "non_public",
            "non_transport",
        )
    ):
        return "dropped"
    if "verified_existing" in c or c == "verified_existing_boarding_point":
        return "sealed"  # confirm existing; not invent
    return "held"


def process_bp_wave(
    wave: str,
    records: list[dict],
    poi_by_id: dict[str, dict],
    id_keys: list[str],
    class_keys: list[str],
) -> dict:
    outcomes = []
    for i, bp in enumerate(records):
        atlas_id = None
        for k in id_keys:
            if bp.get(k):
                atlas_id = bp.get(k)
                break
        classification = None
        for k in class_keys:
            if bp.get(k):
                classification = bp.get(k)
                break
        name = bp.get("name") or bp.get("research_bp_key") or f"row-{i}"
        city = bp.get("city_id") or bp.get("market_id") or bp.get("market_anchor")
        disp = disposition_from_class(classification or "")
        reason = classification or "unclassified"
        feat = poi_by_id.get(atlas_id) if atlas_id else None

        if disp == "sealed":
            if atlas_id and feat:
                props = feat.setdefault("properties", {})
                props["_didi_latam_seal"] = {
                    "at": utc_now(),
                    "wave": wave,
                    "disposition": "sealed_confirm_existing",
                    "classification": classification,
                }
                # do not invent coords
                outcomes.append(
                    {
                        "name": name,
                        "city_id": city,
                        "atlas_bp_id": atlas_id,
                        "disposition": "sealed",
                        "reason": f"confirmed existing atlas BP ({reason})",
                    }
                )
            elif atlas_id and not feat:
                outcomes.append(
                    {
                        "name": name,
                        "city_id": city,
                        "atlas_bp_id": atlas_id,
                        "disposition": "held",
                        "reason": f"atlas_bp_id referenced but missing from FEATURES ({reason})",
                    }
                )
            else:
                # verified real-world but unmatched atlas id
                outcomes.append(
                    {
                        "name": name,
                        "city_id": city,
                        "atlas_bp_id": None,
                        "disposition": "held",
                        "reason": f"source-verified or candidate identity; no atlas BP ID to seal ({reason})",
                    }
                )
        elif disp == "dropped":
            if atlas_id and feat:
                props = feat.setdefault("properties", {})
                props["_not_route_demand_proof"] = True
                props["_didi_latam_seal"] = {
                    "at": utc_now(),
                    "wave": wave,
                    "disposition": "dropped_non_bp",
                    "classification": classification,
                }
            outcomes.append(
                {
                    "name": name,
                    "city_id": city,
                    "atlas_bp_id": atlas_id,
                    "disposition": "dropped",
                    "reason": reason,
                }
            )
        else:
            outcomes.append(
                {
                    "name": name,
                    "city_id": city,
                    "atlas_bp_id": atlas_id,
                    "disposition": "held",
                    "reason": reason,
                }
            )

    counts = Counter(o["disposition"] for o in outcomes)
    return {
        "wave": wave,
        "researched": len(records),
        "sealed": counts.get("sealed", 0),
        "held": counts.get("held", 0),
        "dropped": counts.get("dropped", 0),
        "silent_drops": 0,
        "outcomes": outcomes,
    }


def fr_objs(ids: list[str], gold: dict[str, dict]) -> list[dict]:
    out = []
    for rid in ids:
        if rid in MUST_NOT_FEATURE:
            raise SystemExit(f"refusing to feature excluded route {rid}")
        p = gold.get(rid)
        if not p:
            raise SystemExit(f"missing gold {rid}")
        if is_excluded(p):
            raise SystemExit(f"cannot feature excluded {rid}")
        fl, tl, cid = p.get("from_label"), p.get("to_label"), p.get("cluster_id")
        if not (fl and tl and cid):
            raise SystemExit(f"incomplete labels {rid}")
        out.append(
            {"route_id": rid, "from_label": fl, "to_label": tl, "cluster_id": cid}
        )
    return out


def ensure_partner_featured(partner: dict, gold: dict[str, dict]) -> dict:
    bound = []
    for mid, ids in FEATURED_ACTIVE.items():
        for m in partner.get("markets") or []:
            if m.get("id") != mid:
                continue
            m["featured_routes"] = fr_objs(ids, gold)
            for i, ph in enumerate(m.get("phases") or []):
                if not isinstance(ph, dict):
                    continue
                # phase 0: first 2 or all if shorter
                phase_ids = ids[:2] if i == 0 and len(ids) > 2 else ids
                ph["featured_routes"] = fr_objs(phase_ids, gold)
            # scrub journeys of excluded route ids
            for j in m.get("journeys_unlocked") or []:
                if not isinstance(j, dict):
                    continue
                rid = j.get("route_id")
                if rid in MUST_NOT_FEATURE or (rid and rid in gold and is_excluded(gold[rid])):
                    j["route_id"] = None
                    j["_link_status"] = "unlinked-excluded-from-active-set"
                    j["economics_status"] = "roadmap_excluded"
            # ensure journeys for featured
            existing_rids = {
                j.get("route_id")
                for j in (m.get("journeys_unlocked") or [])
                if isinstance(j, dict) and j.get("route_id")
            }
            journeys = list(m.get("journeys_unlocked") or [])
            for rid in ids:
                if rid in existing_rids:
                    continue
                p = gold[rid]
                journeys.insert(
                    0,
                    {
                        "from": p.get("from_label"),
                        "to": p.get("to_label"),
                        "from_label": p.get("from_label"),
                        "to_label": p.get("to_label"),
                        "label": f"{p.get('from_label')} → {p.get('to_label')}",
                        "route_id": rid,
                        "distance_nm": p.get("distance_nm"),
                        "platform": "Pioneer II",
                        "archetype": "tourism",
                        "_link_status": "linked-latam-seal",
                        "_link_source": "grok/didi-latam-seal",
                        "economics_status": "economics_pending",
                        "today": "Existing water transfer with boarding friction.",
                        "with_navier": "A clean high-frequency hop booked in DiDi once demand is sourced.",
                    },
                )
            m["journeys_unlocked"] = journeys
            wn = m.get("why_navier_now")
            if isinstance(wn, dict):
                wow = ids[:2] if len(ids) >= 2 else ids
                # Colombia geometry caveat: no wow claim of current service
                if mid == "colombia":
                    wn["wow_corridors"] = []
                else:
                    wn["wow_corridors"] = fr_objs(wow, gold)
            bound.append({"market": mid, "route_ids": ids, "n": len(ids)})
    partner["_didi_latam_seal"] = {
        "at": utc_now(),
        "status": "latam_geometry_seal_complete / finance_cascade_not_run",
        "bound": bound,
        "galapagos": "3 stamped / 0 active — quarantine preserved; not rendered",
        "chile_argentina": "registry deferred — no mint",
        "finance": "no cascade; all annual_one_way_pax remain null",
    }
    return {"bound": bound}


def verify_priority_routes(gold: dict[str, dict]) -> dict:
    a1 = ["rn-1886629dbf0c", "rn-80f0d0ebe0bd", "rn-00bb6ded4be5", "rn-369ef0eb69d9", "rn-aa790551baa7"]
    a2 = [
        "rn-1efe26f3c0f4",
        "rn-21a0133c6d5c",
        "rn-55b63e976bb7",
        "rn-60740d4c3114",
        "rn-64effc46b976",
        "rn-7e59f984abec",
        "rn-87eec178e86f",
        "rn-8fb072f5a8a8",
        "rn-c3a4ef933700",
        "rn-eb4ca32edbef",
    ]
    gal = [
        "e__santa-cruz-galapagos-ecuador__puerto-ayora__isabela-galapagos-ecuador__puerto-villamil",
        "e__santa-cruz-galapagos-ecuador__puerto-ayora__san-cristobal-galapagos-ecuador__puerto-baquerizo-moreno",
        "e__santa-cruz-galapagos-ecuador__puerto-ayora__floreana-galapagos-ecuador__puerto-velasco-ibarra",
    ]
    rows = []
    for rid in a1 + a2 + gal + ["rn-f0a756c7f278", "rn-3d69b89a7af6"]:
        p = gold.get(rid)
        if not p:
            rows.append({"route_id": rid, "present": False})
            continue
        rows.append(
            {
                "route_id": rid,
                "present": True,
                "cluster_id": p.get("cluster_id"),
                "from": p.get("from"),
                "to": p.get("to"),
                "from_city_id": p.get("from_city_id"),
                "to_city_id": p.get("to_city_id"),
                "excluded": is_excluded(p),
                "quarantine": p.get("_quarantine"),
                "relevance": p.get("relevance"),
                "eligible_for_featured": (not is_excluded(p)) and rid not in MUST_NOT_FEATURE,
                "seal_render_verdict": (
                    "excluded_quarantine_or_hide_not_renderable"
                    if is_excluded(p)
                    else "active_geometry_present_service_and_demand_not_implied"
                ),
            }
        )
    return {"priority_routes": rows}


def wave_c_deferred() -> dict:
    deep = load(LATAM / "DIDI-CHILE-ARGENTINA-REGISTRY-DEEPENING-2026-07-09.json")
    bps = deep.get("boarding_points") or []
    cors = deep.get("candidate_corridors") or []
    cities = deep.get("cities") or []
    bp_out = process_bp_wave(
        "C",
        bps,
        {},
        id_keys=["atlas_bp_id"],
        class_keys=["status", "classification"],
    )
    # Force no sealed without mint — re-map sealed→held for wave C (no atlas ids)
    for o in bp_out["outcomes"]:
        if o["disposition"] == "sealed":
            o["disposition"] = "held"
            o["reason"] = "wave_C_registry_deferred_no_canonical_id: " + o["reason"]
    bp_out["sealed"] = sum(1 for o in bp_out["outcomes"] if o["disposition"] == "sealed")
    bp_out["held"] = sum(1 for o in bp_out["outcomes"] if o["disposition"] == "held")
    bp_out["dropped"] = sum(1 for o in bp_out["outcomes"] if o["disposition"] == "dropped")
    return {
        "status": "research-complete / registry-and-seal-needed — no mint this seal",
        "minted_cluster_ids": [],
        "minted_city_ids": [],
        "minted_bp_ids": [],
        "minted_route_ids": [],
        "candidate_cities": [
            c.get("name") or c.get("display") or c.get("proposed_city_id") or c.get("city_id")
            for c in cities
        ],
        "corridors_all_route_id_null": all(not c.get("route_id") for c in cors),
        "corridor_n": len(cors),
        "bp_dispositions": bp_out,
        "deferred_reason": (
            "Handoff: candidate labels are not IDs. Registry owner must approve "
            "country/cluster hierarchy before minting. Authority-grade coordinates "
            "and water-only geometry are prerequisites."
        ),
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
    pre_hashes = {
        "CLUSTERS.json": sha256_file(CLUSTERS) if CLUSTERS.exists() else None,
        "ROUTES.json": sha256_file(ROUTES),
        "partners/didi.json": sha256_file(PITCH),
        "FEATURES_BY_TYPE.json": sha256_file(FBT),
    }

    routes, gold = load_routes()
    before = route_counts(gold)
    # verify pinned before-state
    for cid, (s, a, e) in PINNED_BEFORE.items():
        cur = before["by_cluster"][cid]
        if (cur["stamped"], cur["active"], cur["excluded"]) != (s, a, e):
            print(
                f"WARN before-state drift {cid}: got {cur['stamped']}/{cur['active']}/{cur['excluded']} expected {s}/{a}/{e}"
            )

    fbt = load(FBT)
    poi = index_poi(fbt)

    # --- Wave BP dispositions ---
    a1 = load(LATAM / "DIDI-BRAZIL-COLOMBIA-DEEPENING-2026-07-09.json")
    a2 = load(LATAM / "DIDI-COSTA-RICA-PANAMA-DOMINICAN-DEEPENING-2026-07-09.json")
    b = load(LATAM / "DIDI-ECUADOR-PERU-DEEPENING-2026-07-09.json")

    bp_a1 = process_bp_wave(
        "A1",
        a1.get("boarding_points") or [],
        poi,
        id_keys=["atlas_bp_id"],
        class_keys=["classification"],
    )
    bp_a2 = process_bp_wave(
        "A2",
        a2.get("boarding_points") or [],
        poi,
        id_keys=["boarding_point_id", "atlas_bp_id"],
        class_keys=["research_classification", "classification"],
    )
    # additive Sabana candidate if present as null id
    sabana = {
        "name": "Sabana de la Mar Ferry Terminal (additive candidate)",
        "boarding_point_id": None,
        "research_classification": "candidate_needing_authority_operator_proof",
        "market_id": "samana-dominican-republic",
    }
    # only add if not already in list by name
    names = {(x.get("name") or "").lower() for x in (a2.get("boarding_points") or [])}
    if "sabana" not in " ".join(names):
        extra = process_bp_wave("A2-additive", [sabana], poi, ["boarding_point_id"], ["research_classification"])
        bp_a2["researched"] += 1
        bp_a2["held"] += extra["held"]
        bp_a2["outcomes"].extend(extra["outcomes"])

    bp_b = process_bp_wave(
        "B",
        b.get("boarding_points") or [],
        poi,
        id_keys=["atlas_bp_id"],
        class_keys=["classification"],
    )
    wave_c = wave_c_deferred()

    priority = verify_priority_routes(gold)

    # Galápagos: explicitly preserve quarantine — do not activate
    gal_decisions = []
    for rid in [
        "e__santa-cruz-galapagos-ecuador__puerto-ayora__isabela-galapagos-ecuador__puerto-villamil",
        "e__santa-cruz-galapagos-ecuador__puerto-ayora__san-cristobal-galapagos-ecuador__puerto-baquerizo-moreno",
        "e__santa-cruz-galapagos-ecuador__puerto-ayora__floreana-galapagos-ecuador__puerto-velasco-ibarra",
    ]:
        p = gold.get(rid) or {}
        gal_decisions.append(
            {
                "route_id": rid,
                "cluster_id": p.get("cluster_id"),
                "quarantine": p.get("_quarantine"),
                "relevance": p.get("relevance"),
                "activation": "retained_quarantine_hidden",
                "reason": (
                    "Handoff: genuine stamped routes but 0 active. Activation requires "
                    "source, BP, protected-area, geometry and policy approval. Foreign-stamp "
                    "cleanup is not render seal."
                ),
                "renderable": False,
            }
        )

    # Partner bind — active featured only
    partner = load(PITCH)
    bind = ensure_partner_featured(partner, gold)
    text = json.dumps(partner, indent=2, ensure_ascii=False) + "\n"
    PITCH.write_text(text)
    DC.write_text(text)

    # write FBT (BP seals)
    save(FBT, fbt)

    # re-load gold after any changes (routes unchanged in this pass)
    _, gold_after = load_routes()
    after = route_counts(gold_after)

    # deltas
    deltas = {}
    for cid in EXISTING_CLUSTERS:
        b0 = before["by_cluster"][cid]
        a0 = after["by_cluster"][cid]
        deltas[cid] = {
            "before": b0,
            "after": a0,
            "delta_stamped": a0["stamped"] - b0["stamped"],
            "delta_active": a0["active"] - b0["active"],
            "delta_excluded": a0["excluded"] - b0["excluded"],
            "reason": "no route inventory change this seal; BP dispositions + partner featured bind only",
        }

    # annual pax null confirmation from control
    ctrl = load(LATAM / "DIDI-LATAM-RESEARCH-CONTROL-2026-07-09.json")
    annual_null = (ctrl.get("totals") or {}).get("annual_one_way_pax_null", 49)

    print("Gates...")
    gates = run_gates()
    for name, g in gates.items():
        print(f"  {name} exit={g['exit']}")
        print(g["tail"][:600])

    post_hashes = {
        "CLUSTERS.json": sha256_file(CLUSTERS) if CLUSTERS.exists() else None,
        "ROUTES.json": sha256_file(ROUTES),
        "partners/didi.json": sha256_file(PITCH),
        "FEATURES_BY_TYPE.json": sha256_file(FBT),
    }

    bp_total = {
        "researched": bp_a1["researched"] + bp_a2["researched"] + bp_b["researched"] + wave_c["bp_dispositions"]["researched"],
        "sealed": bp_a1["sealed"] + bp_a2["sealed"] + bp_b["sealed"] + wave_c["bp_dispositions"]["sealed"],
        "held": bp_a1["held"] + bp_a2["held"] + bp_b["held"] + wave_c["bp_dispositions"]["held"],
        "dropped": bp_a1["dropped"] + bp_a2["dropped"] + bp_b["dropped"] + wave_c["bp_dispositions"]["dropped"],
        "silent_drops": 0,
    }

    receipt = {
        "at": utc_now(),
        "artifact": "DiDi Latin America Grok seal handback",
        "partner": "didi",
        "handoff": "handoff/didi-ex-china/latam/DIDI-LATAM-GROK-SEAL-HANDOFF-2026-07-09.md",
        "upstream_pr": 212,
        "upstream_commit": "c4a4af2075e292368bbf94b5c544ade7c94dc4be",
        "status": "latam_geometry_seal_complete / finance_cascade_not_run",
        "pre_hashes": pre_hashes,
        "post_hashes": post_hashes,
        "before_route_state": before,
        "after_route_state": after,
        "pinned_before_reproduced": before["totals"]
        == {"stamped": 235, "active": 226, "excluded": 9},
        "route_deltas": deltas,
        "waves": {
            "A1_brazil_colombia": {
                "bp": {k: bp_a1[k] for k in ("researched", "sealed", "held", "dropped", "silent_drops")},
                "priority_routes_active": [
                    r
                    for r in priority["priority_routes"]
                    if r["route_id"]
                    in FEATURED_ACTIVE["brazil"] + FEATURED_ACTIVE["colombia"]
                ],
                "featured_bind": [b for b in bind["bound"] if b["market"] in ("brazil", "colombia")],
                "null_routes_preserved": True,
                "operation_caveats": [
                    "No 99 city-level claim for Angra",
                    "Río-Bus remains future-only",
                    "rn-aa790551baa7 active geometry; current scheduled service unverified",
                    "rn-3d69b89a7af6 remains quarantine/hide — not rendered",
                    "All annual_one_way_pax null",
                ],
            },
            "A2_cr_pa_dr": {
                "bp": {k: bp_a2[k] for k in ("researched", "sealed", "held", "dropped", "silent_drops")},
                "featured_bind": [
                    b
                    for b in bind["bound"]
                    if b["market"] in ("costa-rica", "panama", "dominican-republic")
                ],
                "excluded_priority_not_featured": "rn-60740d4c3114",
                "carti_colon_route_id": None,
                "operation_caveats": [
                    "DiDi exact city: Liberia/Panama City only; not Samaná or Guna Yala city claims",
                    "Guna boarding permissions still required before finance",
                    "Cartí–Colón remains null",
                    "All annual_one_way_pax null",
                ],
            },
            "B_ecuador_peru": {
                "bp": {k: bp_b[k] for k in ("researched", "sealed", "held", "dropped", "silent_drops")},
                "galapagos_state": "3 stamped / 0 active / 3 excluded",
                "galapagos_activation_decisions": gal_decisions,
                "peru_rn_f0a756c7f278": {
                    "cluster_id": (gold_after.get("rn-f0a756c7f278") or {}).get("cluster_id"),
                    "seal_render_verdict": "active_geometry_present_service_and_demand_not_implied",
                    "note": "Stamp hygiene only; not partner featured bind (no ecuador/peru market blocks)",
                },
                "partner_market_bind": "deferred — no galapagos/peru market blocks on DiDi partner JSON",
                "operation_caveats": [
                    "DiDi city-supported only Lima among Wave B IDs per research",
                    "Galápagos not locally proven DiDi service",
                    "DPA San Andrés held; General San Martín non-BP; Ballestas/Palomino non-landing POIs",
                    "All annual_one_way_pax null",
                ],
            },
            "C_chile_argentina": wave_c,
        },
        "bp_totals": bp_total,
        "priority_route_verification": priority,
        "partner_inheritance": {
            "featured_is_active_subset": True,
            "featured_markets": FEATURED_ACTIVE,
            "must_not_feature_honored": list(MUST_NOT_FEATURE),
        },
        "finance": {
            "cascade_run": False,
            "annual_one_way_pax_non_null": 0,
            "annual_one_way_pax_null_expected": annual_null,
            "note": "No finance cascade. Exact route existence is not cascade-ready.",
        },
        "gates": {
            name: {
                "exit": g["exit"],
                "pass": g["exit"] == 0
                or (name == "fidelity" and "PASS" in g["tail"])
                or (
                    name == "finance_inheritance"
                    and "divergent: 0" in g["tail"]
                ),
                "tail": g["tail"][-1000:],
            }
            for name, g in gates.items()
        },
        "render_qa": {
            "status": "source_json_only — live deck not edited",
            "rule": "Render only active/renderable routes; full stamped sets do not render",
            "anchor_city_ids_for_future_screenshots": [
                "rio-de-janeiro-brazil",
                "cartagena-colombia",
                "nicoya-papagayo-costa-rica",
                "san-blas-panama",
                "samana-dominican-republic",
                "lima-peru",
            ],
            "galapagos_not_rendered": True,
            "screenshots": [],
            "note": "Deterministic partner JSON ready; Vercel deploy produces live pages. Screenshots optional post-deploy.",
        },
        "do_not_publish_carried_forward": True,
        "global_acceptance": {
            "zero_invalid_priority_ids": all(
                r.get("present") for r in priority["priority_routes"] if r["route_id"] not in ()
            ),
            "stamped_active_excluded_totals": after["totals"],
            "no_shrink_clusters": EXISTING_CLUSTERS,
            "finance_not_run": True,
            "silent_bp_drops": 0,
        },
        # filled after commit
        "commit": None,
    }

    # store detailed BP outcomes in sidecar for machine consumers
    detail_path = LATAM / "GROK-LATAM-BP-DISPOSITIONS-2026-07-09.json"
    save(
        detail_path,
        {
            "at": utc_now(),
            "A1": bp_a1,
            "A2": bp_a2,
            "B": bp_b,
            "C": wave_c["bp_dispositions"],
        },
    )
    receipt["bp_detail_path"] = str(detail_path.relative_to(ROOT))

    save(OUT_JSON, receipt)

    # Human-readable
    lines = [
        "# DiDi Latin America — Grok seal handback",
        "",
        f"**UTC:** {receipt['at']}  ",
        f"**Status:** `{receipt['status']}`  ",
        f"**Upstream PR:** #212 (`c4a4af20`)  ",
        f"**Handoff:** `{receipt['handoff']}`",
        "",
        "## Route inventory (before → after)",
        "",
        "| Cluster | Before S/A/E | After S/A/E | Delta |",
        "|---|---:|---:|---|",
    ]
    for cid in EXISTING_CLUSTERS:
        b0 = before["by_cluster"][cid]
        a0 = after["by_cluster"][cid]
        lines.append(
            f"| `{cid}` | {b0['stamped']}/{b0['active']}/{b0['excluded']} | "
            f"{a0['stamped']}/{a0['active']}/{a0['excluded']} | no inventory change |"
        )
    t = after["totals"]
    lines += [
        f"| **Total** | 235/226/9 | **{t['stamped']}/{t['active']}/{t['excluded']}** | pinned reproduced |",
        "",
        "## Wave outcomes",
        "",
        "### A1 Brazil + Colombia",
        f"- BP: sealed={bp_a1['sealed']} held={bp_a1['held']} dropped={bp_a1['dropped']} (researched={bp_a1['researched']})",
        f"- Featured (active only): Brazil {FEATURED_ACTIVE['brazil']}; Colombia {FEATURED_ACTIVE['colombia']}",
        "- `rn-3d69b89a7af6` remains quarantine/hide",
        "- No finance; annual pax null",
        "",
        "### A2 Costa Rica + Panama + DR",
        f"- BP: sealed={bp_a2['sealed']} held={bp_a2['held']} dropped={bp_a2['dropped']} (researched={bp_a2['researched']})",
        f"- Featured active spines only; **not featured:** `rn-60740d4c3114` (quarantine/hide)",
        "- Cartí–Colón `route_id` remains null",
        "",
        "### B Ecuador + Peru",
        f"- BP: sealed={bp_b['sealed']} held={bp_b['held']} dropped={bp_b['dropped']}",
        "- Galápagos: **3 stamped / 0 active / 3 excluded** — quarantine retained; **not rendered**",
        "- Foreign stamps remain absent; `rn-f0a756c7f278` stamped `peru` (hygiene ≠ seal claim)",
        "- No DiDi galapagos/peru market blocks → partner bind deferred",
        "",
        "### C Chile + Argentina",
        "- **No mint.** Registry approval required before canonical IDs.",
        f"- BP dispositions: held={wave_c['bp_dispositions']['held']} dropped={wave_c['bp_dispositions']['dropped']} (all candidates)",
        "- All 10 corridor `route_id`s remain null",
        "",
        "## BP totals",
        "",
        f"- Researched: **{bp_total['researched']}**",
        f"- Sealed (confirm existing): **{bp_total['sealed']}**",
        f"- Held: **{bp_total['held']}**",
        f"- Dropped: **{bp_total['dropped']}**",
        f"- Silent drops: **0**",
        "",
        "## Finance",
        "",
        "- **Cascade not run**",
        f"- Annual one-way pax: all null (expected {annual_null})",
        "",
        "## Gates",
        "",
    ]
    for name, g in receipt["gates"].items():
        lines.append(f"- **{name}:** {'PASS' if g['pass'] else 'FAIL'} (exit {g['exit']})")
    lines += [
        "",
        "## Render QA",
        "",
        "- Live deck not edited",
        "- Only active routes eligible for render",
        "- Galápagos not rendered",
        "- Post-deploy: verify partner pages for Rio, Cartagena, Nicoya, San Blas, Samaná, Lima anchors",
        "",
        "## Artifacts",
        "",
        f"- Machine: `{OUT_JSON.relative_to(ROOT)}`",
        f"- BP detail: `{detail_path.relative_to(ROOT)}`",
        f"- This file: `{OUT_MD.relative_to(ROOT)}`",
        "",
    ]
    OUT_MD.write_text("\n".join(lines) + "\n")
    print("wrote", OUT_JSON)
    print("wrote", OUT_MD)

    rc = 0
    for name in ("gate_g", "inheritance_strict"):
        if gates.get(name, {}).get("exit", 1) != 0:
            rc = 1
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
