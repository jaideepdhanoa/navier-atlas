#!/usr/bin/env python3
"""
LB-83 — Batched sheet refresh helper.

Loops `build_transparent_sheet.py --partner <name>` for each partner in
PARTNER-SHEET-IDS.json, uploads each refreshed sheet to its existing Drive
sheet ID, refreshes the master tracker (_master_tracker), then posts ONE
summary Slack message with all links.

Usage:
  python3 refresh_all_sheets.py                          # all partners + master
  python3 refresh_all_sheets.py --partners grab,careem   # subset + master
  python3 refresh_all_sheets.py --skip-master            # partners only
  python3 refresh_all_sheets.py --dry-run                # plan only, no exec

This script is the ORCHESTRATOR. Upload + Slack delivery are wired through
hook functions (`upload_to_drive`, `post_slack_summary`) that default to
stubs the parent agent / connection tools can replace.
"""
import argparse, json, os, subprocess, sys, time
from typing import Optional

try:
    from drive_upload import replace_spreadsheet
    from partner_keys import engine_partner
    from build_master_sheet import build_master
except ImportError:
    from finance.drive_upload import replace_spreadsheet  # type: ignore
    from finance.partner_keys import engine_partner  # type: ignore
    from finance.build_master_sheet import build_master  # type: ignore

HERE = os.path.dirname(os.path.abspath(__file__))
SHEET_IDS_PATH = os.path.join(HERE, "PARTNER-SHEET-IDS.json")
BUILDER = os.path.join(HERE, "build_transparent_sheet.py")
MASTER_BUILDER = os.path.join(HERE, "build_master_sheet.py")
RECAL = os.path.join(HERE, "recal")
MASTER_OUT = os.path.join(HERE, "_master-unit-econ.xlsx")
DRIVE_URL_FMT = "https://docs.google.com/spreadsheets/d/{sid}/edit"


def load_sheet_registry() -> dict:
    with open(SHEET_IDS_PATH) as f:
        return json.load(f)


def load_sheet_ids() -> dict:
    d = load_sheet_registry()
    return {k: v for k, v in d.items() if not k.startswith("_")}


def upload_to_drive(local_path: str, sheet_id: str, dry_run: bool) -> dict:
    """In-place Drive replace (fileId preserved → economics_url links stay valid)."""
    try:
        return replace_spreadsheet(local_path, sheet_id, dry_run=dry_run)
    except FileNotFoundError as e:
        return {"status": "upload-skipped", "reason": str(e), "sheet_id": sheet_id, "local": local_path}
    except Exception as e:
        return {"status": "upload-failed", "reason": str(e), "sheet_id": sheet_id, "local": local_path}


def post_slack_summary(results: list, master: Optional[dict], dry_run: bool) -> dict:
    lines = ["*Transparent sheet refresh — summary*"]
    for r in results:
        url = DRIVE_URL_FMT.format(sid=r["sheet_id"])
        status = r.get("status", "?")
        lines.append(f"• <{url}|{r['partner']}> — {status}")
    if master:
        url = DRIVE_URL_FMT.format(sid=master["sheet_id"])
        status = master.get("status", "?")
        lines.append(f"• <{url}|master tracker> — {status}")
    text = "\n".join(lines)
    if dry_run:
        return {"status": "dry-run", "text": text}
    return {"status": "skipped-no-connection", "text": text}


def refresh_master(dry_run: bool) -> dict:
    reg = load_sheet_registry()
    master_id = reg.get("_master_tracker")
    if not master_id:
        return {"status": "skipped", "reason": "no _master_tracker in PARTNER-SHEET-IDS.json"}
    record = {"partner": "master", "sheet_id": master_id, "out": MASTER_OUT}
    if dry_run:
        record["status"] = "planned"
        record["upload"] = upload_to_drive(MASTER_OUT, master_id, dry_run=True)
        return record
    try:
        build_master(MASTER_OUT, RECAL)
        record["status"] = "built"
        record["upload"] = upload_to_drive(MASTER_OUT, master_id, dry_run=False)
    except Exception as e:
        record["status"] = f"error: {e}"
    return record


def run_for_partner(partner: str, sheet_id: str, dry_run: bool) -> dict:
    from partner_sheet_build import build_sheet_cmd

    out_local = os.path.join(HERE, f"_refresh_{partner}.xlsx")
    build_partner = engine_partner(partner)
    cmd = build_sheet_cmd(build_partner, out_local)
    record = {"partner": partner, "sheet_id": sheet_id, "cmd": " ".join(cmd)}
    if dry_run:
        record["status"] = "planned"
        record["upload"] = upload_to_drive(out_local, sheet_id, dry_run=True)
        return record
    t0 = time.time()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        record["returncode"] = proc.returncode
        record["stdout_tail"] = proc.stdout[-500:]
        record["stderr_tail"] = proc.stderr[-500:]
        if proc.returncode == 0:
            record["status"] = "built"
            record["upload"] = upload_to_drive(out_local, sheet_id, dry_run=False)
        else:
            record["status"] = "build-failed"
    except Exception as e:
        record["status"] = f"error: {e}"
    record["elapsed_s"] = round(time.time() - t0, 2)
    return record


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--partners", default=None,
                    help="comma-separated subset; default = all in PARTNER-SHEET-IDS.json")
    ap.add_argument("--dry-run", action="store_true",
                    help="plan only; do not invoke builder or upload")
    ap.add_argument("--skip-master", action="store_true",
                    help="skip master tracker refresh (default: refresh master)")
    args = ap.parse_args()

    sheet_ids = load_sheet_ids()
    if args.partners:
        wanted = [p.strip() for p in args.partners.split(",") if p.strip()]
        missing = [p for p in wanted if p not in sheet_ids]
        if missing:
            raise SystemExit(f"unknown partners: {missing}; known: {sorted(sheet_ids)}")
        targets = [(p, sheet_ids[p]) for p in wanted]
    else:
        targets = sorted(sheet_ids.items())

    results = [run_for_partner(p, sid, args.dry_run) for p, sid in targets]
    master = None if args.skip_master else refresh_master(args.dry_run)
    summary = post_slack_summary(results, master, args.dry_run)
    print(json.dumps({"results": results, "master": master, "slack_summary": summary}, indent=2))


if __name__ == "__main__":
    main()
