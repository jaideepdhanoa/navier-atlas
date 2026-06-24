"""Shared build flags for transparent partner economics sheets."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODEL = HERE / "model"
RECAL = HERE / "recal"
BUILDER = HERE / "build_transparent_sheet.py"


def hospitality_capex_tier(partner: str) -> bool:
    scoped = RECAL / f"corridors-{partner}.json"
    if scoped.is_file():
        doc = json.loads(scoped.read_text())
        for market in doc.get("markets", {}).values():
            if market.get("capex_tier") == "hospitality":
                return True
    canonical = MODEL / "corridors.json"
    if canonical.is_file():
        doc = json.loads(canonical.read_text())
        for market in doc.get("markets", {}).values():
            if market.get("partner") == partner and market.get("capex_tier") == "hospitality":
                return True
    return False


def build_sheet_cmd(partner: str, out: str | Path) -> list[str]:
    """Argv for build_transparent_sheet.py with scoped corridors/agg when present."""
    cmd = [sys.executable, str(BUILDER), "--partner", partner, "--out", str(out)]
    scoped_corr = RECAL / f"corridors-{partner}.json"
    scoped_agg = RECAL / f"agg-{partner}.json"
    if scoped_corr.is_file():
        cmd.extend(["--corridors", str(scoped_corr)])
    if scoped_agg.is_file():
        cmd.extend(["--agg", str(scoped_agg)])
    if hospitality_capex_tier(partner):
        cmd.extend(["--capex-tier", "hospitality"])
    return cmd


def publish_partner_sheet(partner: str, *, dry_run: bool = False) -> dict:
    """Upload _refresh_{partner}.xlsx to the registered Drive sheet id."""
    from drive_upload import replace_spreadsheet  # noqa: WPS433

    out = HERE / f"_refresh_{partner}.xlsx"
    registry = json.loads((HERE / "PARTNER-SHEET-IDS.json").read_text())
    sid = registry.get(partner)
    if not sid or str(sid).startswith("_"):
        raise SystemExit(f"No Drive sheet id for partner {partner!r} in PARTNER-SHEET-IDS.json")
    if not out.is_file():
        raise SystemExit(f"Missing local sheet {out} — run build first")
    return replace_spreadsheet(str(out), sid, dry_run=dry_run)