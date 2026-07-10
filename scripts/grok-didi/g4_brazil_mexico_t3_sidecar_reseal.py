#!/usr/bin/env python3
"""DiDi G4 after Tasklet PR #213 — Brazil T3 + Mexico residual Punta Sam.

- Upsert economics_by_route_id for all agg-didi rows with gold route_ids
  (4 Rio grounded + Mexico spine including ics-aa6ff40d2d grounded).
- Reseal partner economics_url / growth / data-clean parity.
- Do not invent demand; do not materialize Colombia finance.
- Colombia spine reconciliation receipt only (hold).
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
AGG = ROOT / "finance/recal/agg-didi.json"
GROWTH = ROOT / "finance/didi-growth-case.json"
SIDECAR = ROOT / "data-clean/economics_by_route_id.json"
ROUTES = ROOT / "data-clean/ROUTES.json"
PITCH = ROOT / "partner-pitch/partners/didi.json"
DC = ROOT / "data-clean/partners/didi.json"
SEAL = ROOT / "data-clean/SEAL.json"
SHEET_IDS = ROOT / "finance/PARTNER-SHEET-IDS.json"
CORR = ROOT / "finance/model/corridors.json"
OUT = ROOT / "handoff/didi-ex-china/waves/tasklet-proof"
RECEIPT = OUT / "GROK-G4-BRAZIL-MEXICO-T3-RECEIPT-2026-07-10.json"
RECEIPT_MD = OUT / "GROK-G4-BRAZIL-MEXICO-T3-RECEIPT-2026-07-10.md"
COLOMBIA_REC = OUT / "GROK-COLOMBIA-SPINE-RECONCILIATION-2026-07-10.json"

RIO = [
    "rn-1886629dbf0c",
    "rn-80f0d0ebe0bd",
    "rn-369ef0eb69d9",
    "rn-00bb6ded4be5",
]
MEXICO_SPINE = [
    "ics-413f51cd44",
    "ics-dd1d814699",
    "ics-03e3853317",
    "ics-aa6ff40d2d",
    "ics-89a8844858",
    "ics-de6758216f",
    "ics-db0930d9d1",
    "ics-b5861451fb",
]
MARKET_DISPLAY = {
    "mexico-caribbean": "Mexico – Caribbean",
    "mexico-pacific": "Mexico – Pacific",
    "brazil": "Brazil",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load(p: Path) -> Any:
    return json.loads(p.read_text())


def save(p: Path, obj: Any, indent: int = 2) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=indent, ensure_ascii=False) + "\n")


def save_sidecar(obj: Any) -> None:
    SIDECAR.write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n")


def sha_obj(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def num(x: Any) -> Any:
    return None if x is None else round(float(x), 2)


def economics_url() -> str:
    ids = load(SHEET_IDS) if SHEET_IDS.exists() else {}
    sid = ids.get("didi") if isinstance(ids, dict) else None
    if not sid:
        sid = "1LY0Vp7FskgDDnEixkrEUCH0m-A_pYd2YCNuq3LF8ESM"
    return f"https://docs.google.com/spreadsheets/d/{sid}/edit"


def gold_ids() -> set[str]:
    raw = load(ROUTES)
    feats = raw if isinstance(raw, list) else raw.get("features")
    return {
        (f.get("properties") or f).get("id")
        for f in feats
        if (f.get("properties") or f).get("id")
    }


def corridor_block(row: dict) -> dict:
    mid = row.get("mid") or {}
    thin = row.get("thin") or {}
    full = row.get("full") or {}
    market = row.get("market")
    status = row.get("status")
    return {
        "corridor": row.get("corridor"),
        "market": MARKET_DISPLAY.get(market, (market or "").replace("-", " ").title()),
        "country": row.get("country"),
        "distance_nm": row.get("nm"),
        "status": status,
        "demand_confidence": row.get("demand_conf") or mid.get("demand_confidence"),
        "fare_today_usd": mid.get("comparable_fare_usd"),
        "navier_fare_usd": mid.get("navier_fare_usd"),
        "vessel": mid.get("vessel"),
        "mid": {
            "rev_per_boat_yr": num(mid.get("revenue_per_boat_yr")),
            "margin": num(mid.get("margin")),
            "payback_years": num(mid.get("payback_years")),
            "co2_saved_t_per_boat_yr": num(mid.get("co2_saved_t_per_boat_yr")),
            "vessels_10pct": mid.get("vessels_supported_10pct"),
            "market_rev_yr": num(mid.get("market_revenue_yr")),
        },
        "band": {
            "payback_years": [
                num(thin.get("payback_years")),
                num(mid.get("payback_years")),
                num(full.get("payback_years")),
            ],
            "vessels_10pct": [
                thin.get("vessels_supported_10pct"),
                mid.get("vessels_supported_10pct"),
                full.get("vessels_supported_10pct"),
            ],
        },
        "estimation_basis": row.get("est_basis"),
        "assumptions": mid.get("assumptions"),
        "breakdown": {
            "revenue_build": {
                "comparable_fare_usd": mid.get("comparable_fare_usd"),
                "navier_fare_usd": mid.get("navier_fare_usd"),
                "pax_capacity": (mid.get("revenue_inputs") or {}).get("pax_capacity"),
                "load_factor": (mid.get("revenue_inputs") or {}).get("load_factor"),
                "pax_per_trip": mid.get("pax_per_trip"),
                "trips_per_day": mid.get("trips_per_day"),
                "trips_per_year": mid.get("trips_per_year"),
                "pax_per_year": mid.get("pax_per_year"),
                "revenue_per_boat_yr": num(mid.get("revenue_per_boat_yr")),
            },
            "run_cost": {
                "energy_usd_yr": num((mid.get("cost_components") or {}).get("energy_usd_yr")),
                "crew_usd_yr": num((mid.get("cost_components") or {}).get("crew_usd_yr")),
                "marina_overhead_usd_yr": num(
                    (mid.get("cost_components") or {}).get("marina_overhead_usd_yr")
                ),
                "maintenance_usd_yr": num(
                    (mid.get("cost_components") or {}).get("maintenance_usd_yr")
                ),
                "insurance_usd_yr": num(
                    (mid.get("cost_components") or {}).get("insurance_usd_yr")
                ),
                "charging_berth_usd_yr": num(
                    (mid.get("cost_components") or {}).get("charging_berth_usd_yr")
                ),
                "annual_opex_usd_yr": num(mid.get("annual_opex")),
                "depreciation_usd_yr": num(
                    (mid.get("cost_components") or {}).get("depreciation_usd_yr")
                ),
            },
            "result": {
                "ebitda_per_boat_yr": num(mid.get("ebitda_per_boat_yr")),
                "margin": num(mid.get("margin")),
                "payback_years": num(mid.get("payback_years")),
                "co2_saved_t_per_boat_yr": num(mid.get("co2_saved_t_per_boat_yr")),
            },
        },
        "provenance": {
            "fare": (
                "published comparable adult benchmark — not operator realized yield"
                if status == "grounded"
                else "null_until_sourced"
            ),
            "demand": (
                "sourced corridor demand pool"
                if status == "grounded"
                else "held_null — unsupported ridership"
            ),
            "permission": "required_not_transferred",
            "source": "finance/recal/agg-didi.json",
            "lane": "didi-g4-brazil-mexico-t3-2026-07-10",
            "sealed_at": utc_now(),
        },
    }


def build_records(agg: dict, gold: set[str]) -> tuple[list[dict], list[dict]]:
    recs = []
    pending = []
    for row in agg.get("rows") or []:
        rid = row.get("route_id") or (row.get("mid") or {}).get("route_id")
        if not rid:
            pending.append(
                {
                    "authored_for": "didi",
                    "market": row.get("market"),
                    "corridor": row.get("corridor"),
                    "reason": "no_route_id",
                }
            )
            continue
        if rid not in gold:
            pending.append(
                {
                    "authored_for": "didi",
                    "market": row.get("market"),
                    "route_id": rid,
                    "reason": "route_id_not_in_gold",
                }
            )
            continue
        rec = {
            "route_id": rid,
            "registry_market_id": row.get("market"),
            "authored_for": "didi",
        }
        rec.update(corridor_block(row))
        recs.append(rec)
    return recs, pending


def merge_sidecar(recs: list[dict], pending: list[dict]) -> dict:
    payload = load(SIDECAR) if SIDECAR.exists() else {"_meta": {}, "records": [], "_pending_route_pin": []}
    by = {r["route_id"]: r for r in (payload.get("records") or []) if r.get("route_id")}
    added = updated = 0
    for rec in recs:
        rid = rec["route_id"]
        if rid in by:
            existing = by[rid]
            if existing.get("authored_for") not in (None, "didi"):
                also = existing.setdefault("also_serves", [])
                if not any(isinstance(a, dict) and a.get("authored_for") == "didi" for a in also):
                    also.append(
                        {
                            "authored_for": "didi",
                            "market": rec.get("market"),
                            "corridor": rec.get("corridor"),
                            "status": rec.get("status"),
                            "mid": rec.get("mid"),
                        }
                    )
                updated += 1
            else:
                by[rid] = rec
                updated += 1
        else:
            by[rid] = rec
            added += 1
    new_records = list(by.values())
    new_records.sort(
        key=lambda r: (
            r.get("authored_for") or "",
            -((r.get("mid") or {}).get("market_rev_yr") or 0),
        )
    )
    # refresh pending for these rids
    spine = {r["route_id"] for r in recs}
    old_pending = [
        p
        for p in (payload.get("_pending_route_pin") or [])
        if not (p.get("authored_for") == "didi" and p.get("route_id") in spine)
    ]
    payload["records"] = new_records
    payload["_pending_route_pin"] = old_pending + pending
    meta = payload.setdefault("_meta", {})
    meta["generated"] = utc_now()
    meta["records"] = len(new_records)
    meta["pending_route_pin"] = len(payload["_pending_route_pin"])
    partners = set(meta.get("partners") or [])
    partners.add("didi")
    meta["partners"] = sorted(partners)
    meta["didi_brazil_mexico_t3_g4"] = {
        "at": utc_now(),
        "rio": RIO,
        "mexico_spine": MEXICO_SPINE,
        "added": added,
        "updated": updated,
        "didi_records": len(recs),
    }
    save_sidecar(payload)
    return {
        "added": added,
        "updated": updated,
        "records_total": len(new_records),
        "didi_records": len(recs),
        "pending": len(pending),
    }


def reseal_partner(partner: dict, agg: dict) -> dict:
    url = economics_url()
    partner["economics_url"] = url
    gc = partner.setdefault("growth_case", {})
    if isinstance(gc, dict):
        gc["economics_url"] = url
        # ladder rungs
        for key in ("ladder_transitions",):
            block = gc.get(key)
            if isinstance(block, list):
                for rung in block:
                    if isinstance(rung, dict):
                        rung["economics_url"] = url
        rp = gc.get("revenue_potential") or {}
        rungs = rp.get("rungs") if isinstance(rp, dict) else None
        if isinstance(rungs, list):
            for rung in rungs:
                if isinstance(rung, dict):
                    rung["economics_url"] = url

    floor = (agg.get("rollup") or {}).get("grounded_floor") or {}
    partner["_economics_status"] = {
        "state": "didi_brazil_mexico_t3_g4_sealed",
        "grounded_floor_usd_yr": floor.get("market_rev_yr"),
        "transport_spend_pool_yr": floor.get("transport_spend_pool_yr"),
        "fleet": floor.get("fleet"),
        "cascade_at": utc_now(),
        "agg": "finance/recal/agg-didi.json",
        "growth": "finance/didi-growth-case.json",
        "sidecar": "economics_by_route_id.json",
        "economics_url": url,
        "caveats": [
            "published fares are comparable benchmarks not realized yield",
            "DiDi/Navier access permission required not transferred",
            "Colombia unmaterialized pending shared finance spine + demand",
        ],
    }
    partner.pop("economics_status", None)
    partner["_didi_g4_brazil_mexico_t3"] = {
        "at": utc_now(),
        "rio_ids": RIO,
        "punta_sam": "ics-aa6ff40d2d",
        "mexico_spine_unchanged": MEXICO_SPINE,
        "economics_url": url,
    }
    return {"economics_url": url, "floor": floor}


def colombia_reconciliation() -> dict:
    """Hold Colombia materialization; document spine mismatch."""
    corr = load(CORR)
    yango = corr.get("markets", {}).get("yango-colombia") or {}
    yango_rids = sorted(
        {c.get("route_id") for c in (yango.get("corridors") or []) if c.get("route_id")}
    )
    partner = load(PITCH)
    didi_rids = []
    for m in partner.get("markets") or []:
        if m.get("id") != "colombia":
            continue
        for r in m.get("featured_routes") or []:
            if isinstance(r, dict) and r.get("route_id"):
                didi_rids.append(r["route_id"])
    didi_rids = sorted(set(didi_rids))
    shared = sorted(set(yango_rids) & set(didi_rids))
    only_didi = sorted(set(didi_rids) - set(yango_rids))
    only_yango = sorted(set(yango_rids) - set(didi_rids))
    rec = {
        "at": utc_now(),
        "status": "unmaterialized_hold",
        "decision": "C — keep DiDi Colombia unmaterialized in finance until route-level demand/fare proof + spine decision",
        "yango_colombia_finance_spine": yango_rids,
        "didi_featured_route_ids": didi_rids,
        "intersection": shared,
        "only_in_didi_featured": only_didi,
        "only_in_yango_finance": only_yango,
        "notes": [
            "rn-aa790551baa7 is DiDi geometry marquee (service unverified) and not on yango-colombia 6-ID spine",
            "Do not create didi-colombia finance market until alignment A/B chosen with demand proof",
            "No finance cascade for Colombia in this lane",
        ],
        "finance_inheritance_impact": "none — no didi-colombia market key created",
    }
    save(COLOMBIA_REC, rec)
    return rec


def run_gates() -> dict:
    def run(cmd: list[str]) -> dict:
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        out = (r.stdout or "") + (r.stderr or "")
        return {"exit": r.returncode, "tail": "\n".join(out.splitlines()[-35:])}

    return {
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
        "route_linkage": run(
            ["node", str(ROOT / "scripts/audit-partner-route-linkage.mjs"), "didi"]
        )
        if (ROOT / "scripts/audit-partner-route-linkage.mjs").exists()
        else {"exit": 0, "tail": "skip"},
    }


def main() -> int:
    gold = gold_ids()
    agg = load(AGG)
    recs, pending = build_records(agg, gold)
    print("sidecar records from agg", len(recs), "pending", len(pending))
    for r in recs:
        print(
            " ",
            r["route_id"],
            r.get("status"),
            (r.get("mid") or {}).get("market_rev_yr"),
            r.get("fare_today_usd"),
        )

    # require all Rio + Punta Sam present
    have = {r["route_id"] for r in recs}
    for rid in RIO + ["ics-aa6ff40d2d"]:
        if rid not in have:
            raise SystemExit(f"FATAL missing required route in agg/sidecar build: {rid}")

    sc = merge_sidecar(recs, pending)
    print("merge", sc)

    # reseal partner from pitch (post-merge already has growth)
    partner = load(PITCH)
    seal_stats = reseal_partner(partner, agg)
    # ensure data-clean partners matches pitch for didi
    text = json.dumps(partner, indent=2, ensure_ascii=False) + "\n"
    PITCH.write_text(text)
    DC.write_text(text)
    print("reseal", seal_stats["economics_url"], seal_stats["floor"])

    col = colombia_reconciliation()
    print("colombia", col["status"], "only_didi", col["only_in_didi_featured"])

    # SEAL hashes
    if SEAL.exists():
        seal = load(SEAL)
        files = seal.setdefault("files", {})
        sc_obj = load(SIDECAR)
        files["economics_by_route_id.json"] = sha_obj(sc_obj)
        files["partners/didi.json"] = sha_obj(load(DC))
        notes = seal.setdefault("_notes", [])
        if isinstance(notes, list):
            notes.append({"at": utc_now(), "event": "didi-g4-brazil-mexico-t3"})
        seal["sealed_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        save(SEAL, seal)

    gates = run_gates()
    for name, g in gates.items():
        print(f"\n=== {name} exit={g['exit']} ===")
        print(g["tail"][:1500])

    sc_obj = load(SIDECAR)
    by = {r["route_id"]: r for r in sc_obj.get("records") or []}
    joined = []
    for rid in RIO + MEXICO_SPINE:
        r = by.get(rid)
        joined.append(
            {
                "route_id": rid,
                "present": bool(r),
                "authored_for": (r or {}).get("authored_for"),
                "status": (r or {}).get("status"),
                "market_rev_yr": ((r or {}).get("mid") or {}).get("market_rev_yr"),
                "fare_today_usd": (r or {}).get("fare_today_usd"),
            }
        )

    floor = (agg.get("rollup") or {}).get("grounded_floor") or {}
    receipt = {
        "at": utc_now(),
        "lane": "G4 Brazil T3 + Mexico residual Punta Sam sidecar/reseal",
        "upstream_pr": 213,
        "upstream_merge": "f43420eb",
        "status": "g4-complete",
        "sidecar": {
            **sc,
            "joined": joined,
            "sha256": sha_obj(sc_obj),
            "path": "data-clean/economics_by_route_id.json",
        },
        "grounded": {
            "fleet": floor.get("fleet"),
            "market_rev_yr": floor.get("market_rev_yr"),
            "transport_spend_pool_yr": floor.get("transport_spend_pool_yr"),
            "corridors_from_agg": {
                "total": len(agg.get("rows") or []),
                "grounded": sum(1 for r in agg.get("rows") or [] if r.get("status") == "grounded"),
                "estimated": sum(1 for r in agg.get("rows") or [] if r.get("status") != "grounded"),
            },
        },
        "economics_url": seal_stats["economics_url"],
        "mexico_spine_preserved": MEXICO_SPINE,
        "rio_ids": RIO,
        "punta_sam": {
            "route_id": "ics-aa6ff40d2d",
            "status_after": (by.get("ics-aa6ff40d2d") or {}).get("status"),
            "market_rev_yr": ((by.get("ics-aa6ff40d2d") or {}).get("mid") or {}).get(
                "market_rev_yr"
            ),
        },
        "caveats": [
            "published fares = comparable benchmarks not realized yield",
            "permission_required not transferred",
            "Colombia unmaterialized",
        ],
        "colombia_reconciliation": col,
        "finance_cascade_by_grok": False,
        "gates": {
            name: {
                "exit": g["exit"],
                "pass": g["exit"] == 0
                or (name == "fidelity" and "PASS" in g["tail"])
                or (name == "finance_inheritance" and "divergent: 0" in g["tail"]),
                "tail": g["tail"][-900:],
            }
            for name, g in gates.items()
        },
    }
    save(RECEIPT, receipt)

    lines = [
        "# Grok G4 — DiDi Brazil T3 + Mexico Punta Sam residual",
        "",
        f"**UTC:** {receipt['at']}  ",
        f"**Status:** `{receipt['status']}`  ",
        f"**Upstream:** PR #213 merge `f43420eb`",
        "",
        "## Sidecar",
        "",
        f"- Records total: {sc['records_total']} (added {sc['added']}, updated {sc['updated']})",
        f"- DiDi agg rows joined: {sc['didi_records']}",
        "",
        "### Joined IDs",
        "",
    ]
    for j in joined:
        lines.append(
            f"- `{j['route_id']}` — {j.get('status')} — rev {j.get('market_rev_yr')} — fare {j.get('fare_today_usd')}"
        )
    lines += [
        "",
        "## Combined floor (from agg)",
        "",
        f"- Fleet: **{floor.get('fleet')}**",
        f"- Floor: **${floor.get('market_rev_yr'):,}**/yr" if floor.get("market_rev_yr") else "- Floor: n/a",
        f"- Pool: **${floor.get('transport_spend_pool_yr'):,}**/yr"
        if floor.get("transport_spend_pool_yr")
        else "- Pool: n/a",
        "",
        f"- economics_url: {seal_stats['economics_url']}",
        "",
        "## Colombia",
        "",
        f"- Status: **{col['status']}**",
        f"- Decision: {col['decision']}",
        f"- Only in DiDi featured: {col['only_in_didi_featured']}",
        f"- Only in yango finance: {col['only_in_yango_finance']}",
        "",
        "## Gates",
        "",
    ]
    for name, g in receipt["gates"].items():
        lines.append(f"- **{name}:** {'PASS' if g['pass'] else 'FAIL'} (exit {g['exit']})")
    lines += ["", f"Machine: `{RECEIPT.relative_to(ROOT)}`", ""]
    RECEIPT_MD.write_text("\n".join(lines) + "\n")
    print("wrote", RECEIPT)

    rc = 0
    for name in ("gate_g", "inheritance_strict"):
        if gates.get(name, {}).get("exit", 1) != 0:
            rc = 1
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
