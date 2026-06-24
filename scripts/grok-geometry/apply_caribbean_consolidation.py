#!/usr/bin/env python3
"""PR #95: consolidate caribbean-mobility → caribbean; bind ABC geometry to abc-islands market."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
from bolt_yango_routing_shared import load_json, save_json  # noqa: E402

PR_BRANCH = "origin/fix/caribbean-consolidation-2026-06-24"
CONSOLIDATED_REL = "partner-pitch/partners/caribbean.json"
ABC_SLICE_REL = "partner-pitch/partners/caribbean.json"  # thin ABC slice on main (pre-merge)
MOBILITY_REL = "partner-pitch/partners/caribbean-mobility.json"
SHEET_ID = "1J9rb-rAXkLnJPrKO8WhG7bLkofG-IB5En6hrjnwDyt0"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit"
NEW_CITIES = ("aruba-aruba", "curacao-curacao", "bonaire-bonaire")
LUMP = "aruba-curacao-bonaire"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git_show(path: str) -> dict:
    proc = subprocess.run(
        ["git", "show", f"{PR_BRANCH}:{path}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(proc.stdout)


def abc_journeys_from_slice(slice_doc: dict) -> list[dict]:
    out: list[dict] = []
    for j in slice_doc.get("journeys_unlocked", []):
        row = deepcopy(j)
        row.setdefault("model_link", SHEET_URL)
        row.setdefault("_link_kind", "corridor-label")
        out.append(row)
    return out


def abc_featured_from_slice(slice_doc: dict) -> list[dict]:
    featured: list[dict] = []
    for phase in slice_doc.get("phases", []):
        for fr in phase.get("featured_routes", []):
            if fr.get("route_id") or fr.get("_link_status") == "roadmap-quanta-lr":
                featured.append(deepcopy(fr))
    return featured


def patch_abc_market(market: dict, slice_doc: dict) -> None:
    market["anchor_cities"] = list(NEW_CITIES)
    market["status"] = "display-ready geometry; economics cascaded (abc-islands)"
    market["summary"] = (
        "Dutch Caribbean ABC trio — sealed geometry on aruba-aruba, curacao-curacao, "
        "bonaire-bonaire nodes. Inter-island and intra-island legs bound; Quanta-LR cross-island roadmap."
    )
    market["hero"] = slice_doc["hero"]["subtitle"]
    market["partner_context"] = slice_doc["partner_context"]["where_navier_fits"]
    market["why_now"] = slice_doc["why_now"]
    market["multimodal_fit"] = slice_doc["multimodal_fit"]
    market["journeys_unlocked"] = abc_journeys_from_slice(slice_doc)
    market["proof_points"] = slice_doc.get("proof_points", [])[:3]
    market["objections"] = slice_doc.get("objections", [])[:2]
    featured = abc_featured_from_slice(slice_doc)
    for phase in market.get("phases", []):
        if phase.get("n") in (1, 2, 3):
            phase["featured_routes"] = [
                fr for fr in featured if fr.get("route_id")
            ][:3] or phase.get("featured_routes", [])


def update_sheet_registry(apply: bool) -> dict:
    changes: dict = {}
    for rel in ("finance/PARTNER-SHEET-IDS.json", "finance/economics_url_map.json"):
        path = ROOT / rel
        doc = load_json(path)
        if rel.endswith("PARTNER-SHEET-IDS.json"):
            if "caribbean" not in doc or str(doc.get("caribbean", "")).startswith("_"):
                doc["caribbean"] = SHEET_ID
                changes["PARTNER-SHEET-IDS"] = SHEET_ID
            doc.setdefault("_caribbean_mobility_alias", SHEET_ID)
        else:
            econ = doc.setdefault("economics_url", {})
            if "caribbean" not in econ:
                econ["caribbean"] = SHEET_URL
                changes["economics_url_map"] = SHEET_URL
        if apply:
            save_json(path, doc)
    return changes


def retire_mobility(apply: bool) -> bool:
    retired = False
    for rel in (MOBILITY_REL, "data-clean/partners/caribbean-mobility.json"):
        path = ROOT / rel
        if not path.exists():
            continue
        doc = load_json(path)
        doc["_status"] = "retired"
        doc["_superseded_by"] = "caribbean"
        doc["_retired_at"] = utc_now()
        doc["_retire_note"] = "PR #95: caribbean-mobility consolidated into caribbean (11-market network)."
        if apply:
            save_json(path, doc)
            retired = True
    return retired


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    abc_slice = load_json(ROOT / ABC_SLICE_REL)
    consolidated = git_show(CONSOLIDATED_REL)

    abc_market = next((m for m in consolidated.get("markets", []) if m.get("slug") == "abc-islands"), None)
    if not abc_market:
        print("FATAL: abc-islands market missing in consolidated caribbean.json")
        return 1

    patch_abc_market(abc_market, abc_slice)
    consolidated["economics_url"] = SHEET_URL
    if isinstance(consolidated.get("growth_case"), dict):
        consolidated["growth_case"]["economics_url"] = SHEET_URL

    report = {
        "at": utc_now(),
        "lane": "grok/caribbean_consolidation_pr95",
        "apply": args.apply,
        "abc_market_journeys": len(abc_market["journeys_unlocked"]),
        "markets_total": len(consolidated.get("markets", [])),
        "sheet_registry": update_sheet_registry(False),
        "mobility_retired": retire_mobility(False),
    }

    if args.apply:
        pitch = ROOT / CONSOLIDATED_REL
        save_json(pitch, consolidated)
        shutil.copy2(pitch, ROOT / "data-clean/partners/caribbean.json")
        report["sheet_registry"] = update_sheet_registry(True)
        report["mobility_retired"] = retire_mobility(True)

    out = ROOT / "grok-routing-output/caribbean-consolidation-report.json"
    save_json(out, report)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())