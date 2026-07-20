#!/usr/bin/env python3
"""Rebuild all partner growth cases from standardized greenfield census.

Pipeline per partner with finance/recal/agg-<p>.json:
  1) greenfield_census.py → recal/greenfield-census/<p>.json
  2) growth.py --agg … --partner … --json recal/growth-<p>.json
     (auto-loads census; FORCE_OFF partners use --greenfield off)
  3) growth_frontend_block.py → partner-pitch/partners/_growth-draft/<p>.growth.json
  4) splice_growth_into_partner.py → partner-pitch + data-clean partners

Then:
  5) build_economics_sidecar.py
  6) optional: refresh_all_sheets.py --dry-run or live

Usage:
  python3 rebuild_all_from_greenfield_census.py
  python3 rebuild_all_from_greenfield_census.py --partners didi,indrive,grab
  python3 rebuild_all_from_greenfield_census.py --skip-sheets
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RECAL = HERE / "recal"
MODEL = HERE / "model"
CENSUS_DIR = RECAL / "greenfield-census"
PITCH = ROOT / "partner-pitch" / "partners"
DC_PARTNERS = ROOT / "data-clean" / "partners"
DRAFT = PITCH / "_growth-draft"

# Purpose-built / captive networks: width lever off (null-beats-guess).
FORCE_OFF = {
    "french-polynesia",
    "bolt-rebase",
    "saudi-pif",  # giga-project sourced set IS the network (historical)
    "red-sea-global",
}

SKIP_AGG = {
    "unique-global",
    "global",
    "gojek-deck",
    "gojek-deck-merged",
}


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    print("+", " ".join(cmd))
    return subprocess.run(cmd, cwd=str(cwd or HERE), capture_output=True, text=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--partners", help="comma list; default=all with agg-*.json")
    ap.add_argument("--skip-sheets", action="store_true")
    ap.add_argument("--skip-splice", action="store_true")
    ap.add_argument("--max-nm", type=float, default=70.0)
    args = ap.parse_args()

    if args.partners:
        partners = [p.strip() for p in args.partners.split(",") if p.strip()]
    else:
        partners = sorted(
            p.stem[len("agg-") :]
            for p in RECAL.glob("agg-*.json")
            if p.stem[len("agg-") :] not in SKIP_AGG
        )

    DRAFT.mkdir(parents=True, exist_ok=True)
    CENSUS_DIR.mkdir(parents=True, exist_ok=True)

    # 1) census all selected partners
    for partner in partners:
        cr = run(
            [
                sys.executable,
                str(MODEL / "greenfield_census.py"),
                "--partner",
                partner,
                "--max-nm",
                str(args.max_nm),
            ]
        )
        if cr.returncode != 0:
            print(cr.stderr or cr.stdout, file=sys.stderr)

    summary = []
    for partner in partners:
        agg = RECAL / f"agg-{partner}.json"
        if not agg.exists():
            summary.append({"partner": partner, "status": "no_agg"})
            continue
        census = CENSUS_DIR / f"{partner}.json"
        growth_out = RECAL / f"growth-{partner}.json"
        cmd = [
            sys.executable,
            str(MODEL / "growth.py"),
            "--partner",
            partner,
            "--agg",
            str(agg),
            "--json",
            str(growth_out),
        ]
        if partner in FORCE_OFF:
            cmd.extend(["--greenfield", "off"])
        elif census.exists():
            cmd.extend(["--greenfield-json", str(census)])
        gr = run(cmd, cwd=MODEL)
        if gr.returncode != 0:
            print(gr.stderr or gr.stdout, file=sys.stderr)
            summary.append({"partner": partner, "status": "growth_fail", "err": (gr.stderr or "")[:200]})
            continue
        # print last lines of growth
        for line in (gr.stdout or "").strip().splitlines()[-8:]:
            print(f"  [{partner}] {line}")

        if args.skip_splice:
            summary.append({"partner": partner, "status": "growth_ok"})
            continue

        draft = DRAFT / f"{partner}.growth.json"
        fe = run(
            [
                sys.executable,
                str(MODEL / "growth_frontend_block.py"),
                "--partner",
                partner,
                "--growth",
                str(growth_out),
                "--rollup",
                str(agg),
                "--out",
                str(draft),
                "--partner-json",
                str(PITCH / f"{partner}.json") if (PITCH / f"{partner}.json").exists() else str(DC_PARTNERS / f"{partner}.json"),
            ]
        )
        if fe.returncode != 0:
            # try without partner-json
            fe = run(
                [
                    sys.executable,
                    str(MODEL / "growth_frontend_block.py"),
                    "--partner",
                    partner,
                    "--growth",
                    str(growth_out),
                    "--rollup",
                    str(agg),
                    "--out",
                    str(draft),
                ]
            )
        if fe.returncode != 0:
            print(fe.stderr or fe.stdout, file=sys.stderr)
            summary.append({"partner": partner, "status": "frontend_fail"})
            continue

        # splice pitch
        if (PITCH / f"{partner}.json").exists():
            sp = run(
                [
                    sys.executable,
                    str(HERE / "splice_growth_into_partner.py"),
                    "--partner",
                    partner,
                    "--growth",
                    str(growth_out),
                    "--frontend",
                    str(draft),
                ]
            )
            if sp.returncode != 0:
                print(sp.stderr or sp.stdout, file=sys.stderr)

        # copy growth_case into data-clean partner if present
        pitch_p = PITCH / f"{partner}.json"
        dc_p = DC_PARTNERS / f"{partner}.json"
        if pitch_p.exists() and dc_p.exists():
            try:
                pitch = json.loads(pitch_p.read_text())
                dc = json.loads(dc_p.read_text())
                if "growth_case" in pitch:
                    dc["growth_case"] = pitch["growth_case"]
                    dc_p.write_text(json.dumps(dc, indent=2, ensure_ascii=False) + "\n")
            except Exception as e:
                print(f"  data-clean sync fail {partner}: {e}", file=sys.stderr)

        gdoc = json.loads(growth_out.read_text())
        gmid = (gdoc.get("greenfield") or {}).get("factor_band", {}).get("mid")
        summary.append(
            {
                "partner": partner,
                "status": "ok",
                "g_mid": gmid,
                "mode": (gdoc.get("greenfield") or {}).get("mode"),
                "som_floor": (gdoc.get("grounded") or {}).get("SOM_floor_navier_transport_rev_yr"),
                "som_network": ((gdoc.get("grounded") or {}).get("SOM_full_network_navier_transport_rev_yr") or {}).get("mid"),
                "sam": ((gdoc.get("grounded") or {}).get("SAM_navier_transport_rev_yr") or {}).get("mid"),
            }
        )

    # sidecar
    print("\n→ rebuild economics sidecar")
    run(
        [
            sys.executable,
            str(HERE / "build_economics_sidecar.py"),
            "--gold",
            str(ROOT / "data-clean"),
            "--aggdir",
            str(RECAL),
            "--out",
            str(ROOT / "data-clean" / "economics_by_route_id.json"),
        ]
    )

    report_path = RECAL / "greenfield-census" / "REBUILD-REPORT.json"
    report_path.write_text(json.dumps({"summary": summary}, indent=2) + "\n")
    print(f"\nReport → {report_path}")
    ok = sum(1 for s in summary if s.get("status") == "ok")
    print(f"OK {ok}/{len(summary)}")

    if not args.skip_sheets:
        print("\n→ rebuild transparent sheets (local xlsx; upload separately)")
        # local only build for partners with sheet ids
        sheet_ids = json.loads((HERE / "PARTNER-SHEET-IDS.json").read_text())
        for partner in partners:
            if partner not in sheet_ids or partner.startswith("_"):
                continue
            run(
                [
                    sys.executable,
                    str(HERE / "build_transparent_sheet.py"),
                    "--partner",
                    partner,
                ]
            )
        run([sys.executable, str(HERE / "build_master_sheet.py")])

    # print top g_mid changes
    print("\n=== g_mid by partner ===")
    for s in sorted(summary, key=lambda x: -(x.get("g_mid") or 0)):
        if s.get("g_mid") is not None:
            print(f"  {s['partner']:28} g_mid={s['g_mid']:.3f}  mode={s.get('mode')}  SAM={s.get('sam')}")
    return 0


if __name__ == "__main__":
    # fix empty arg from --all construction
    sys.argv = [a for a in sys.argv if a != ""]
    raise SystemExit(main())
