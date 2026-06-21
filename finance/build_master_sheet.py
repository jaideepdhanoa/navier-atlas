#!/usr/bin/env python3
"""Master tracker: one row per partner unit-econ sheet, live links + rollup headline metrics.

Reads rollups from finance/recal/agg-<partner>.json (no hand-transcription).
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

try:
    from partner_keys import engine_partner, sheet_partner
except ImportError:
    from finance.partner_keys import engine_partner, sheet_partner  # type: ignore

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_AGG_DIR = os.path.join(HERE, "recal")
DEFAULT_OUT = os.path.join(HERE, "_master-unit-econ.xlsx")
SHEET_IDS_PATH = os.path.join(HERE, "PARTNER-SHEET-IDS.json")

# Stable row order; any slug in PARTNER-SHEET-IDS.json not listed here appends alphabetically.
PARTNER_ORDER = [
    "grab", "careem", "bolt", "yango", "uber",
    "rapido", "ola", "noon",
    "jih-global", "qatar", "saudi-pif", "red-sea-global",
    "constance", "four-seasons",
]

PARTNER_DISPLAY: dict[str, str] = {
    "grab": "Grab",
    "careem": "Careem",
    "bolt": "Bolt",
    "yango": "Yango",
    "uber": "Uber",
    "rapido": "Rapido (India)",
    "ola": "Ola (India)",
    "noon": "Noon (UAE)",
    "jih-global": "JIH Global (Maldives)",
    "qatar": "Qatar",
    "saudi-pif": "Saudi / Red Sea (PIF)",
    "red-sea-global": "Red Sea Global",
    "constance": "Constance (Maldives)",
    "four-seasons": "Four Seasons (Maldives)",
}

PARTNER_NOTES: dict[str, str] = {
    "grab": "SE-Asia ridehail/island network. Primary anchor — 0% future-dated demand.",
    "careem": "UAE luxury water-served transfers. Mostly estimated; corridors city-level (route-pin pending).",
    "saudi-pif": "Low-confidence / largely 2030-dated. Greenfield OFF. Treat as forward.",
    "red-sea-global": "Resort-operator corridors. Small, grounded subset.",
    "jih-global": "Maldives 43 corridors geometry-bound; network-sum captive fleet.",
    "qatar": "Doha 4/4 in-range corridors bound. Banana Island captive carries floor.",
    "bolt": "MENA grounded floor + Med/Baltic aspirational tail (Bucket C bound).",
    "yango": "MENA + Africa grounded + CIS/Caspian/Africa aspirational tail (Bucket C bound).",
    "constance": "Captive resort-transfer; network-sum captive fleet. Greenfield OFF.",
    "four-seasons": "Captive resort-transfer; network-sum captive fleet. Greenfield OFF.",
    "uber": "Global mobility rollup; MENA + Med + Hawaii + LatAm scoped markets.",
    "rapido": "PR #58 India — Mumbai/Goa/Kerala/Andaman sealed spine; ridehail archetype.",
    "ola": "PR #58 India — same sealed spine as Rapido; ridehail archetype.",
    "noon": "PR #58 UAE — 12 sealed super_app corridors; Careem-style demand ladder.",
}


def load_registry_rows() -> list[tuple[str, str, str, str]]:
    """(display, sheet-slug, google-sheet-id, note) from PARTNER-SHEET-IDS.json."""
    reg = json.load(open(SHEET_IDS_PATH))
    slugs = [k for k in reg if not k.startswith("_")]
    order = {s: i for i, s in enumerate(PARTNER_ORDER)}
    slugs.sort(key=lambda s: (order.get(s, 999), s))
    rows: list[tuple[str, str, str, str]] = []
    for slug in slugs:
        sid = reg[slug]
        if not sid or str(sid).startswith("_"):
            continue
        disp = PARTNER_DISPLAY.get(slug, slug.replace("-", " ").title())
        note = PARTNER_NOTES.get(slug, "Unit-economics transparent sheet — see agg rollup when present.")
        rows.append((disp, slug, sid, note))
    return rows

NAVY = PatternFill("solid", fgColor="1F3A5F")
STEEL = PatternFill("solid", fgColor="2E5984")
ZEBRA = PatternFill("solid", fgColor="EEF3F8")
TOTF = PatternFill("solid", fgColor="DCE6F1")
WHT = Font(color="FFFFFF", bold=True)
BOLD = Font(bold=True)
SMALL = Font(size=9, color="555555")
thin = Side(style="thin", color="BBBBBB")
BORD = Border(left=thin, right=thin, top=thin, bottom=thin)
USD = "$#,##0"
ctr = Alignment(horizontal="center", vertical="center")
wrap = Alignment(wrap_text=True, vertical="top")


def agg_path(agg_dir: str, sheet_slug: str):
    """Resolve agg JSON for a sheet slug (handles saudi-pif ↔ saudi-redsea-pif)."""
    candidates = [
        os.path.join(agg_dir, f"agg-{sheet_slug}.json"),
        os.path.join(agg_dir, f"agg-{engine_partner(sheet_slug)}.json"),
    ]
    seen: set[str] = set()
    for path in candidates:
        if path in seen:
            continue
        seen.add(path)
        if os.path.isfile(path):
            return path
    return None


def rollup_from_agg(path: str) -> dict:
    j = json.load(open(path))
    d = j["rollup"]
    gf, eu, et = d.get("grounded_floor", {}), d.get("estimated_upside", {}), d.get("estimated_total", {})
    rows = j.get("rows", [])
    by_status: dict[str, int] = {}
    for r in rows:
        by_status[r.get("status", "?")] = by_status.get(r.get("status", "?"), 0) + 1
    g_rows = by_status.get("grounded", d.get("n_grounded", 0))
    e_rows = by_status.get("estimated", d.get("n_estimated", 0))
    gfleet = gf.get("fleet", 0)
    grev = gf.get("market_rev_yr", 0)
    efleet = eu.get("fleet", 0)
    erev = eu.get("market_rev_yr", 0)
    tfleet = et.get("fleet", 0)
    trev = et.get("market_rev_yr", 0)
    scope_only = (tfleet or 0) < (gfleet or 0)
    if scope_only:
        efleet, erev = None, None
        tfleet, trev = gfleet, grev
    return dict(
        n=d.get("n_corridors_total", 0), g=g_rows, e=e_rows,
        gfleet=gfleet, grev=grev, efleet=efleet, erev=erev,
        tfleet=tfleet, trev=trev, scope_only=scope_only,
        agg_file=path,
    )


def empty_rollup(reason: str) -> dict:
    return dict(
        n=None, g="—", e="—",
        gfleet=None, grev=None, efleet=None, erev=None,
        tfleet=None, trev=None, scope_only=False,
        agg_file=None, missing=reason,
    )


def rollup(sheet_slug: str, agg_dir: str) -> dict:
    path = agg_path(agg_dir, sheet_slug)
    if not path:
        return empty_rollup(f"no agg-{sheet_slug}.json in {agg_dir}")
    return rollup_from_agg(path)


def build_master(out_path: str, agg_dir: str = DEFAULT_AGG_DIR) -> int:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Partner unit-economics"

    def put(ref, val, font=None, fill=None, fmt=None, align=None, bd=True):
        c = ws[ref]
        c.value = val
        if font:
            c.font = font
        if fill:
            c.fill = fill
        if fmt:
            c.number_format = fmt
        if align:
            c.alignment = align
        if bd:
            c.border = BORD

    ws.merge_cells("A1:J1")
    put("A1", "Navier — Partner Corridor Unit-Economics  ·  master tracker",
        Font(color="FFFFFF", bold=True, size=14), NAVY,
        align=Alignment(horizontal="left", vertical="center"))
    ws.row_dimensions[1].height = 26
    ws.merge_cells("A2:J2")
    put("A2",
        "Each partner sheet is fully formula-driven and standalone (Assumptions · Corridor economics · Market sizing). "
        "Numbers below are the engine rollup; MID scenario. Open a sheet to trace any cell. "
        "Portfolio total is gross (partner scopes may overlap).",
        SMALL, None, align=wrap, bd=False)
    ws.row_dimensions[2].height = 28

    hdr = ["Partner", "Open sheet", "Corridors (g / e)", "Grounded fleet", "Grounded mkt rev/yr",
           "Est. upside fleet", "Est. upside rev/yr", "Total fleet", "Total rev/yr", "Notes"]
    for i, h in enumerate(hdr):
        put(f"{chr(65 + i)}3", h, WHT, STEEL,
            align=Alignment(horizontal="center", vertical="center", wrap_text=True))
    ws.row_dimensions[3].height = 34

    r = 4
    missing: list[str] = []
    for disp, pk, sid, note in load_registry_rows():
        ro = rollup(pk, agg_dir)
        if ro.get("missing"):
            missing.append(pk)
            note = f"{note} [{ro['missing']}]"
        fill = ZEBRA if (r % 2 == 0) else None
        put(f"A{r}", disp, BOLD, fill)
        put(f"B{r}", f'=HYPERLINK("https://docs.google.com/spreadsheets/d/{sid}/edit","open \u2197")',
            Font(color="1155CC", underline="single"), fill, align=ctr)
        put(f"C{r}", f'{ro["g"]} / {ro["e"]}', None, fill, align=ctr)
        put(f"D{r}", ro["gfleet"], None, fill, align=ctr)
        put(f"E{r}", ro["grev"], None, fill, USD)
        put(f"F{r}", ro["efleet"], None, fill, align=ctr)
        put(f"G{r}", ro["erev"], None, fill, USD)
        put(f"H{r}", ro["tfleet"], None, fill, align=ctr)
        put(f"I{r}", ro["trev"], None, fill, USD)
        put(f"J{r}", note, SMALL, fill, align=wrap)
        ws.row_dimensions[r].height = 42
        r += 1

    put(f"A{r}", "PORTFOLIO (gross)", BOLD, TOTF)
    put(f"B{r}", "", None, TOTF)
    put(f"C{r}", "", None, TOTF)
    for col in ["D", "E", "F", "G", "H", "I"]:
        fmt = USD if col in ("E", "G", "I") else None
        put(f"{col}{r}", f"=SUM({col}4:{col}{r - 1})", BOLD, TOTF, fmt,
            align=(ctr if col in ("D", "F", "H") else None))
    put(f"J{r}", "Gross sum across partner scopes; not de-duplicated.", SMALL, TOTF, align=wrap)
    ws.row_dimensions[r].height = 30

    widths = {"A": 22, "B": 12, "C": 15, "D": 13, "E": 18, "F": 14, "G": 18, "H": 12, "I": 18, "J": 46}
    for c, w in widths.items():
        ws.column_dimensions[c].width = w
    ws.freeze_panes = "A4"

    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
    wb.save(out_path)
    if missing:
        print(f"warning: missing agg for: {', '.join(missing)}", file=sys.stderr)
    print(f"wrote {out_path} ; rows: {r}")
    return r


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--agg-dir", default=DEFAULT_AGG_DIR)
    args = ap.parse_args()
    build_master(args.out, args.agg_dir)


if __name__ == "__main__":
    main()