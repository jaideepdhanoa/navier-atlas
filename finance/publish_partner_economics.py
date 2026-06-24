#!/usr/bin/env python3
"""Create (if needed), build, upload, and wire economics_url for a partner."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SHEET_IDS = HERE / "PARTNER-SHEET-IDS.json"
URL_MAP = HERE / "economics_url_map.json"
BUILDER = HERE / "build_transparent_sheet.py"
DRIVE_FMT = "https://docs.google.com/spreadsheets/d/{sid}/edit"

sys.path.insert(0, str(HERE))
from create_partner_sheets import create_spreadsheet, load_json, save_json  # noqa: E402
from drive_upload import replace_spreadsheet  # noqa: E402


def wire_partner(partner: str, url: str) -> None:
    for rel in (
        f"partner-pitch/partners/{partner}.json",
        f"data-clean/partners/{partner}.json",
    ):
        path = ROOT / rel
        if not path.exists():
            continue
        doc = json.loads(path.read_text())
        doc["economics_url"] = url
        if isinstance(doc.get("growth_case"), dict):
            doc["growth_case"]["economics_url"] = url
        doc["economics_status"] = "cascaded"

        def walk(obj):
            if isinstance(obj, dict):
                if obj.get("model_link") is not None or obj.get("route_id") or obj.get("route_ids"):
                    obj["model_link"] = url
                if obj.get("id") in {
                    "som_floor",
                    "som_network",
                    "sam_network",
                    "tam_transfer",
                    "journey_gmv",
                    "platform_rev",
                }:
                    obj["model_link"] = url
                for v in obj.values():
                    walk(v)
            elif isinstance(obj, list):
                for x in obj:
                    walk(x)

        walk(doc)
        path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")


def ensure_sheet_id(partner: str, title: str) -> str:
    registry = load_json(SHEET_IDS)
    sid = registry.get(partner)
    if sid and not str(sid).startswith("_"):
        return sid
    meta = create_spreadsheet(title)
    sid = meta["id"]
    registry[partner] = sid
    save_json(SHEET_IDS, registry)
    url_map = load_json(URL_MAP)
    url_map.setdefault("economics_url", {})[partner] = DRIVE_FMT.format(sid=sid)
    url_map["_as_of"] = "2026-06-24"
    save_json(URL_MAP, url_map)
    return sid


def build_xlsx(partner: str, out: Path, *, hospitality: bool | None = None) -> None:
    from partner_sheet_build import build_sheet_cmd, hospitality_capex_tier

    use_hospitality = hospitality_capex_tier(partner) if hospitality is None else hospitality
    cmd = build_sheet_cmd(partner, out)
    if use_hospitality and "--capex-tier" not in cmd:
        cmd.extend(["--capex-tier", "hospitality"])
    subprocess.run(cmd, cwd=str(HERE), check=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("partner")
    ap.add_argument("--title", required=True)
    ap.add_argument("--hospitality", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    out = HERE / f"_refresh_{args.partner}.xlsx"
    sid = ensure_sheet_id(args.partner, args.title)
    url = DRIVE_FMT.format(sid=sid)

    if args.dry_run:
        print(json.dumps({"partner": args.partner, "sheet_id": sid, "url": url, "out": str(out)}))
        return 0

    build_xlsx(args.partner, out, hospitality=True if args.hospitality else None)
    result = replace_spreadsheet(str(out), sid, dry_run=False)
    wire_partner(args.partner, url)
    print(json.dumps({"partner": args.partner, "sheet_id": sid, "url": url, "upload": result}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())