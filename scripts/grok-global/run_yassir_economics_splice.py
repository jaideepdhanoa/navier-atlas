#!/usr/bin/env python3
"""Yassir 4-market economics cascade + full growth_case splice (deck gate).

Spec: handoff/GROK-SPEC-yassir-economics-splice-2026-07-06.md

Usage:
  python3 scripts/grok-global/run_yassir_economics_splice.py
  python3 scripts/grok-global/run_yassir_economics_splice.py --skip-sheet
"""
from __future__ import annotations

import argparse
import copy
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FINANCE = ROOT / "finance"
MODEL = FINANCE / "model"
RECAL = FINANCE / "recal"
GROWTH_DRAFT = ROOT / "partner-pitch" / "partners" / "_growth-draft"
PJ = ROOT / "partner-pitch" / "partners" / "yassir.json"
DC = ROOT / "data-clean" / "partners" / "yassir.json"
COUNTRY_REF = MODEL / "country-reference.json"
REPORT = ROOT / "grok-routing-output" / "yassir-economics-splice-receipt.json"

MAGHRAB_MARKETS = ("yassir-morocco", "yassir-tunisia", "yassir-algeria", "yassir-senegal")
COUNTRY_PREFLIGHT = ("Morocco", "Tunisia", "Algeria", "Senegal")


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path):
    return json.loads(path.read_text())


def save_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def run(cmd: list[str], *, cwd: Path | None = None) -> None:
    print(f"→ {' '.join(cmd)}")
    subprocess.run(cmd, check=True, cwd=str(cwd or ROOT))


def preflight_country_reference(report: dict) -> None:
    cref = load_json(COUNTRY_REF).get("countries") or {}
    missing = [c for c in COUNTRY_PREFLIGHT if c not in cref]
    report["country_reference"] = {
        "required": list(COUNTRY_PREFLIGHT),
        "missing": missing,
        "capex_row_usd": 600000,
        "capex_rule": "LB-243 non-US/EU → $600K/vessel",
    }
    if missing:
        raise SystemExit(f"Missing country-reference rows: {missing}")


def corridor_leg_status(agg_rows: list[dict]) -> dict:
    by_market: dict[str, dict] = {}
    for m in MAGHRAB_MARKETS:
        legs = [r for r in agg_rows if r.get("market") == m]
        grounded = [r for r in legs if r.get("status") == "grounded"]
        estimated = [r for r in legs if r.get("status") == "estimated"]
        roadmap = [r for r in legs if (r.get("nm") or 0) > 70]
        by_market[m] = {
            "total": len(legs),
            "grounded": len(grounded),
            "estimated": len(estimated),
            "roadmap_quanta": len(roadmap),
            "grounded_corridors": [r.get("corridor") for r in grounded],
            "estimated_corridors": [r.get("corridor") for r in estimated],
        }
    return by_market


def merge_growth_case(doc: dict, growth: dict, agg: dict, frontend: dict) -> None:
    """Full growth_case splice — deck reads nested growth + top-level floor."""
    rollup = agg.get("rollup") or agg
    gf = rollup.get("grounded_floor") or {}
    et = rollup.get("estimated_total") or {}
    g = growth.get("grounded") or {}

    gc = doc.setdefault("growth_case", {})
    gc["source_rollup"] = "finance/recal/agg-yassir.json"
    gc["source_growth"] = "finance/recal/growth-yassir.json"
    gc["source_frontend"] = "partner-pitch/partners/_growth-draft/yassir.growth.json"
    gc["grounded_floor"] = copy.deepcopy(gf)
    gc["estimated_total"] = copy.deepcopy(et)
    gc["grounded_floor_by_market"] = copy.deepcopy(rollup.get("grounded_floor_by_market") or {})

    # Replace stale embedded growth object (was 43-boat / $111M pool).
    gc["growth"] = copy.deepcopy(growth)

    gc["revenue_potential"] = copy.deepcopy(frontend.get("revenue_potential") or {})
    gc["phase_economics"] = copy.deepcopy(frontend.get("phase_economics") or {})
    gc["vessel_sizing"] = copy.deepcopy(frontend.get("vessel_sizing") or gc.get("vessel_sizing"))
    gc["_provenance"] = copy.deepcopy(frontend.get("_provenance") or {})
    gc["_render_chip_flag"] = copy.deepcopy(frontend.get("_render_chip_flag") or {})

    gc["marine_mobility_tam"] = copy.deepcopy(g.get("marine_mobility_tam_yr") or {})
    gc["journey_gmv"] = copy.deepcopy(g.get("journey_gmv_yr") or {})
    gc["partner_platform_rev_on_navier"] = copy.deepcopy(g.get("partner_platform_rev_on_navier_yr") or {})

    # Ladder transitions — rebuild from fresh growth grounded block.
    sys.path.insert(0, str(FINANCE))
    from splice_growth_into_partner import build_ladder_transitions  # noqa: E402

    params = growth.get("parameters_used") or {}
    gc["ladder_transitions"] = build_ladder_transitions(g, params, "yassir", include_platform=True)
    gc["modal_lead"] = gc["revenue_potential"].get("modal_lead")
    gc.setdefault("modal_headline", "Floor to prize — every rung traces to grounded demand")
    gc["_marine_tam_split_provenance"] = {
        "date": utc_now(),
        "lane": "grok/run_yassir_economics_splice",
        "formula": "marine_mobility_tam = SAM_full_network / mature_capture_rate (LB-110)",
    }

    # Hub phases boats from phase_economics horizons
    horizons = {h.get("id"): h for h in (gc.get("phase_economics") or {}).get("horizons") or []}
    for ph in doc.get("phases") or []:
        n = ph.get("n")
        if n == 1 and horizons.get("prove"):
            ph["boats"] = horizons["prove"].get("fleet_boats")
        if n == 2 and horizons.get("scale"):
            ph["boats"] = horizons["scale"].get("fleet_boats_est")
        if n == 3 and horizons.get("mature"):
            ph["boats"] = horizons["mature"].get("fleet_boats_est_pioneer_equiv")

    # Sub-market economics from per-market floor
    by_mkt = rollup.get("grounded_floor_by_market") or {}
    for m in doc.get("markets") or []:
        mid = m.get("id")
        if mid not in MAGHRAB_MARKETS:
            continue
        mk = by_mkt.get(mid) or {}
        m["economics_status"] = "model_cascaded_after_grok_seal"
        m.setdefault("_economics_floor", {})
        m["_economics_floor"] = {
            "fleet": mk.get("fleet"),
            "market_rev_yr": mk.get("market_rev_yr"),
            "transport_spend_pool_yr": mk.get("transport_spend_pool_yr"),
            "co2_saved_t_yr": mk.get("co2_saved_t_yr"),
            "cascade_at": utc_now(),
        }
        for ph in m.get("phases") or []:
            if ph.get("n") == 1 and mk.get("fleet") is not None:
                ph["boats"] = mk.get("fleet")
            ph.setdefault("_economics", {})["status"] = "cascaded"
        for j in m.get("journeys_unlocked") or []:
            if j.get("route_id") and j.get("economics_status") == "pending_cascade":
                j["economics_status"] = "cascaded"

    doc["economics_status"] = "model_cascaded_maghreb_senegal_algeria"
    nt = doc.setdefault("network_thesis", {})
    for s in nt.get("stats") or []:
        if isinstance(s, dict) and s.get("label") == "economics status":
            s["value"] = "model_cascaded_maghreb_senegal_algeria"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-sheet", action="store_true")
    ap.add_argument("--skip-sidecar", action="store_true")
    args = ap.parse_args()

    report: dict = {"generated": utc_now(), "lane": "grok/run_yassir_economics_splice"}

    preflight_country_reference(report)

    # Scoped corridors view for sheet/sidecar
    run([sys.executable, str(ROOT / "scripts/grok-bite2/build_partner_corridors.py"), "--partner", "yassir"])

    agg_path = RECAL / "agg-yassir.json"
    growth_path = RECAL / "growth-yassir.json"
    frontend_path = GROWTH_DRAFT / "yassir.growth.json"

    run([sys.executable, str(MODEL / "aggregate.py"), "--partner", "yassir", "--json", str(agg_path)])
    run([sys.executable, str(MODEL / "growth.py"), "--partner", "yassir", "--agg", str(agg_path), "--json", str(growth_path)])
    GROWTH_DRAFT.mkdir(parents=True, exist_ok=True)
    run(
        [
            sys.executable,
            str(MODEL / "growth_frontend_block.py"),
            "--partner",
            "yassir",
            "--partner-json",
            str(PJ),
            "--growth",
            str(growth_path),
            "--rollup",
            str(agg_path),
            "--out",
            str(frontend_path),
        ]
    )
    run(
        [
            sys.executable,
            str(FINANCE / "splice_growth_into_partner.py"),
            "--partner",
            "yassir",
            "--growth",
            str(growth_path),
            "--frontend",
            str(frontend_path),
            "--partner-json",
            str(PJ),
        ]
    )

    agg = load_json(agg_path)
    growth = load_json(growth_path)
    frontend = load_json(frontend_path)
    doc = load_json(PJ)
    merge_growth_case(doc, growth, agg, frontend)
    save_json(PJ, doc)
    save_json(DC, doc)

    # yassir-aggregate.json alias for sidecar consumers
    shutil.copy2(agg_path, RECAL / "yassir-aggregate.json")

    if not args.skip_sidecar:
        run(
            [
                sys.executable,
                str(FINANCE / "build_economics_sidecar.py"),
                "--gold",
                str(ROOT / "data-clean"),
                "--aggdir",
                str(RECAL),
                "--out",
                str(ROOT / "data-clean" / "economics_by_route_id.json"),
            ]
        )

    if not args.skip_sheet:
        out_xlsx = FINANCE / "_refresh_yassir.xlsx"
        sys.path.insert(0, str(FINANCE))
        from partner_sheet_build import build_sheet_cmd, publish_partner_sheet  # noqa: E402

        run(build_sheet_cmd("yassir", out_xlsx), cwd=FINANCE)
        pub = publish_partner_sheet("yassir", dry_run=False)
        report["sheet_publish"] = pub

        run([sys.executable, str(FINANCE / "refresh_all_sheets.py"), "--partners", "yassir"])

    run([sys.executable, str(ROOT / "scripts/validate_finance_inheritance.py"), "--json"])

    rollup = agg.get("rollup") or agg
    rows = agg.get("rows") or []
    g = growth.get("grounded") or {}
    report["hub_floor"] = rollup.get("grounded_floor")
    report["per_market_floor"] = rollup.get("grounded_floor_by_market")
    report["ladder"] = {
        "SOM_floor": g.get("SOM_floor_navier_transport_rev_yr"),
        "SAM_mid": (g.get("SAM_navier_transport_rev_yr") or {}).get("mid"),
        "marine_TAM_mid": (g.get("marine_mobility_tam_yr") or {}).get("mid"),
        "journey_GMV_mid": (g.get("journey_gmv_yr") or {}).get("mid"),
        "platform_on_navier_mid": (g.get("partner_platform_rev_on_navier_yr") or {}).get("mid"),
    }
    report["per_market_legs"] = corridor_leg_status(rows)
    report["growth_case_spliced"] = {
        "grounded_floor_fleet": doc.get("growth_case", {}).get("grounded_floor", {}).get("fleet"),
        "growth_som_floor_fleet": (doc.get("growth_case", {}).get("growth") or {}).get("source_rollup", {}).get(
            "som_floor_grounded_fleet"
        ),
        "pool_yr": (doc.get("growth_case", {}).get("growth") or {}).get("grounded", {}).get("M_today_transport_spend_yr"),
    }
    save_json(REPORT, report)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())