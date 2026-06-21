#!/usr/bin/env python3
"""Create new Google Sheets for partners missing from PARTNER-SHEET-IDS.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from drive_upload import _drive_service

HERE = Path(__file__).resolve().parent
SHEET_IDS_PATH = HERE / "PARTNER-SHEET-IDS.json"
URL_MAP_PATH = HERE / "economics_url_map.json"
DRIVE_URL_FMT = "https://docs.google.com/spreadsheets/d/{sid}/edit"

NEW_PARTNERS: dict[str, str] = {
    "rapido": "Navier — Rapido India Unit Economics",
    "ola": "Navier — Ola India Unit Economics",
    "noon": "Navier — Noon UAE Unit Economics",
    "rakta": "Navier — RAKTA UAE Authority Unit Economics",
    "bahrain-motc": "Navier — Bahrain MOTC Authority Unit Economics",
    "uber-india-derivative": "Navier — Uber India Unit Economics",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def save_json(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n")


def create_spreadsheet(name: str) -> dict:
    svc = _drive_service()
    body = {"name": name, "mimeType": "application/vnd.google-apps.spreadsheet"}
    created = svc.files().create(body=body, fields="id,name,webViewLink").execute()
    return created


def main() -> int:
    registry = load_json(SHEET_IDS_PATH)
    url_map = load_json(URL_MAP_PATH)
    economics_url = url_map.setdefault("economics_url", {})
    created: list[dict] = []

    for partner, title in NEW_PARTNERS.items():
        if partner in registry and not str(registry[partner]).startswith("_"):
            print(f"skip {partner}: already registered ({registry[partner]})")
            continue
        meta = create_spreadsheet(title)
        sid = meta["id"]
        registry[partner] = sid
        economics_url[partner] = DRIVE_URL_FMT.format(sid=sid)
        created.append({"partner": partner, "sheet_id": sid, "title": title, "url": economics_url[partner]})
        print(f"created {partner}: {economics_url[partner]}")

    if not created:
        print("no new sheets created")
        return 0

    save_json(SHEET_IDS_PATH, registry)
    url_map["_as_of"] = "2026-06-20"
    save_json(URL_MAP_PATH, url_map)
    print(json.dumps({"created": created}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())