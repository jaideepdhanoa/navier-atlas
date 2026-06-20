#!/usr/bin/env python3
"""Wire economics_url + model_link sheet URLs into partner JSON from economics_url_map.json."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
URL_MAP = ROOT / "finance" / "economics_url_map.json"
PARTNERS_DIR = ROOT / "partner-pitch" / "partners"
SHEET_URL_RE = re.compile(r"^https://docs\.google\.com/spreadsheets/d/")

TARGETS = ("rapido", "ola", "noon", "careem", "jih-global", "qatar")


def load_urls() -> dict[str, str]:
    doc = json.loads(URL_MAP.read_text())
    return doc.get("economics_url", {})


def _needs_model_link(obj: dict) -> bool:
    if obj.get("_link_kind") or obj.get("route_id") or obj.get("route_ids"):
        return True
    if obj.get("id") in {
        "som_floor", "som_network", "sam_network", "tam_transfer", "journey_gmv", "platform_rev",
    }:
        return True
    return False


def _cascade_status(obj) -> int:
    n = 0
    if isinstance(obj, dict):
        if obj.get("economics_status") == "economics_pending":
            obj["economics_status"] = "cascaded"
            n += 1
        for v in obj.values():
            n += _cascade_status(v)
    elif isinstance(obj, list):
        for x in obj:
            n += _cascade_status(x)
    return n


def wire_obj(obj, url: str) -> int:
    n = 0
    if isinstance(obj, dict):
        if "model_link" in obj:
            ml = obj["model_link"]
            if not ml or not SHEET_URL_RE.match(str(ml)):
                obj["model_link"] = url
                n += 1
        elif _needs_model_link(obj):
            obj["model_link"] = url
            n += 1
        for v in obj.values():
            n += wire_obj(v, url)
    elif isinstance(obj, list):
        for x in obj:
            n += wire_obj(x, url)
    return n


def main() -> None:
    urls = load_urls()
    for partner in TARGETS:
        path = PARTNERS_DIR / f"{partner}.json"
        if not path.exists():
            print(f"skip {partner}: no partner json")
            continue
        url = urls.get(partner)
        if not url:
            print(f"skip {partner}: no economics_url in map")
            continue
        doc = json.loads(path.read_text())
        doc["economics_url"] = url
        if isinstance(doc.get("growth_case"), dict):
            doc["growth_case"]["economics_url"] = url
        doc["economics_status"] = "cascaded"
        if isinstance(doc.get("_pr58_execution"), dict):
            doc["_pr58_execution"]["economics_status"] = "cascaded"
        n = wire_obj(doc, url)
        n += _cascade_status(doc)
        path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")
        print(f"{partner}: economics_url + {n} model_link fields → {url}")


if __name__ == "__main__":
    main()