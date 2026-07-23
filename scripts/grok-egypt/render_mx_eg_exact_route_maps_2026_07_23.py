#!/usr/bin/env python3
"""Render DiDi Mexico + inDrive Egypt exact-route map plates from ROUTES.json.

Style parity with deck-studio/assets/didi/city-maps/*-exact-route-map.png:
  - CartoDB Dark Matter No Labels basemap
  - 2048×1156 text-free plates
  - Turquoise/cyan route lines, soft endpoint dots
  - Dark left clear-space strip for slide titles

Discipline (GROK-SPEC-mx-eg-map-localization-2026-07-22.md):
  - Geometry from data-clean/ROUTES.json only — no image-generated geography
  - Fail closed if a requested route_id is missing geometry
"""
from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import contextily as cx
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from pyproj import Transformer

ROOT = Path(__file__).resolve().parents[2]
ROUTES = ROOT / "data-clean/ROUTES.json"
OUT_MX = ROOT / "deck-studio/assets/didi/city-maps"
OUT_EG = ROOT / "deck-studio/assets/indrive-egypt/city-maps"
PROVENANCE = (
    ROOT
    / "handoff/partner-map-model/mx-eg-expansion-2026-07-20"
    / "MX-EG-MAP-LOCALIZATION-RECEIPT-2026-07-23.json"
)

# 16:9-ish deck plate used by existing Mexico maps
W_PX, H_PX = 2048, 1156
DPI = 200
FIG_W, FIG_H = W_PX / DPI, H_PX / DPI

# Route line colors (match existing turquoise family)
ROUTE_COLOR = "#3ec6e0"
ROUTE_GLOW = "#1a8fa8"
ENDPOINT = "#f0f7fa"

# Maps to render: key -> (out_path, list[route_id], pad_deg, left_clear_frac)
MAPS = {
    "didi-mexico-market-overview": {
        "out": OUT_MX / "didi-mexico-market-overview-exact-route-map.png",
        "route_ids": [
            # Caribbean spine already on deck + Holbox/Huatulco expansion
            "rn-1b21ad26c9c7",  # Cancún–Isla Mujeres family (sealed cancun-r1)
            "rn-16c9c6538ec2",
            "rn-ec0236195e81",
            "rn-43dc0748c14b",
            "rn-6f3b149a8baa",  # Cozumel
            "rn-fdf0760aac2d",
            "rn-8e76868a5b01",  # Holbox
            "rn-66e2241ca732",  # Huatulco
            "rn-c51bd07b1336",  # Puerto Vallarta
            "rn-69e22f3c73fa",
            "rn-726b5014f1e0",  # Los Cabos
            "ics-413f51cd44",  # canonical Cancún deep-dive ids (if present)
            "ics-03e3853317",
            "ics-aa6ff40d2d",
            "ics-dd1d814699",
            "ics-89a8844858",
            "ics-de6758216f",
            "ics-db0930d9d1",
            "ics-b5861451fb",
        ],
        "pad": 0.8,
        "left_clear": 0.28,
        "min_span_deg": 8.0,
    },
    "didi-holbox": {
        "out": OUT_MX / "didi-holbox-exact-route-map.png",
        "route_ids": ["rn-8e76868a5b01"],
        "pad": 0.15,
        "left_clear": 0.30,
        "min_span_deg": 0.35,
    },
    "didi-huatulco": {
        "out": OUT_MX / "didi-huatulco-exact-route-map.png",
        "route_ids": ["rn-66e2241ca732"],
        "pad": 0.08,
        "left_clear": 0.30,
        "min_span_deg": 0.20,
    },
    "indrive-egypt-market-overview": {
        "out": OUT_EG / "indrive-egypt-market-overview-exact-route-map.png",
        # Red Sea only — Nile/Cairo/El Gouna/Marsa Alam fail-closed pending sourcing
        "route_ids": [
            "rn-b06f6971ed47",  # Hurghada → Giftun
            "rn-c16a1627130f",  # Sharm → Ras Mohammed
        ],
        "pad": 0.6,
        "left_clear": 0.28,
        "min_span_deg": 2.5,
    },
    "indrive-hurghada": {
        "out": OUT_EG / "indrive-hurghada-exact-route-map.png",
        "route_ids": ["rn-b06f6971ed47"],
        "pad": 0.12,
        "left_clear": 0.30,
        "min_span_deg": 0.30,
    },
    "indrive-sharm": {
        "out": OUT_EG / "indrive-sharm-exact-route-map.png",
        "route_ids": ["rn-c16a1627130f"],
        "pad": 0.18,
        "left_clear": 0.30,
        "min_span_deg": 0.40,
    },
}


def load_routes() -> dict[str, dict]:
    feats = json.loads(ROUTES.read_text())
    by: dict[str, dict] = {}
    for f in feats:
        p = f.get("properties") or {}
        rid = p.get("id") or p.get("route_id")
        if rid:
            by[rid] = f
    return by


def coords_lonlat(feat: dict) -> list[tuple[float, float]]:
    g = feat.get("geometry") or {}
    if g.get("type") != "LineString":
        raise ValueError(f"expected LineString, got {g.get('type')}")
    return [(float(c[0]), float(c[1])) for c in g["coordinates"]]


def bbox(lines: list[list[tuple[float, float]]], pad: float, min_span: float):
    xs = [x for line in lines for x, _ in line]
    ys = [y for line in lines for _, y in line]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    # enforce minimum span so short routes still have context
    if maxx - minx < min_span:
        mid = (minx + maxx) / 2
        minx, maxx = mid - min_span / 2, mid + min_span / 2
    if maxy - miny < min_span:
        mid = (miny + maxy) / 2
        miny, maxy = mid - min_span / 2, mid + min_span / 2
    # aspect-aware pad
    minx -= pad
    maxx += pad
    miny -= pad
    maxy += pad
    # match plate aspect so basemap isn't stretched oddly
    aspect = W_PX / H_PX
    w = maxx - minx
    h = maxy - miny
    if w / h > aspect:
        # too wide — grow height
        target_h = w / aspect
        mid = (miny + maxy) / 2
        miny, maxy = mid - target_h / 2, mid + target_h / 2
    else:
        target_w = h * aspect
        mid = (minx + maxx) / 2
        minx, maxx = mid - target_w / 2, mid + target_w / 2
    return minx, miny, maxx, maxy


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def render_one(key: str, cfg: dict, by_id: dict[str, dict]) -> dict:
    resolved = []
    missing = []
    lines = []
    for rid in cfg["route_ids"]:
        feat = by_id.get(rid)
        if not feat or not feat.get("geometry"):
            missing.append(rid)
            continue
        try:
            ll = coords_lonlat(feat)
        except Exception as e:
            missing.append(f"{rid}:{e}")
            continue
        if len(ll) < 2:
            missing.append(f"{rid}:too_few_coords")
            continue
        resolved.append(
            {
                "route_id": rid,
                "nm": (feat.get("properties") or {}).get("distance_nm"),
                "label": (feat.get("properties") or {}).get("label")
                or (feat.get("properties") or {}).get("name"),
                "n_coords": len(ll),
            }
        )
        lines.append(ll)

    if not lines:
        return {
            "key": key,
            "status": "fail_closed",
            "reason": "no resolvable geometry",
            "missing": missing,
        }

    minx, miny, maxx, maxy = bbox(lines, cfg["pad"], cfg["min_span_deg"])
    # expand west for left clear-space (title overlay lives on left of slide)
    clear = cfg["left_clear"]
    span_x = maxx - minx
    minx -= span_x * (clear / (1 - clear))

    to_merc = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)

    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI)
    fig.subplots_adjust(0, 0, 1, 1)
    ax.set_axis_off()

    # draw routes in mercator
    for ll in lines:
        xs, ys = zip(*[to_merc.transform(lon, lat) for lon, lat in ll])
        ax.plot(xs, ys, color=ROUTE_GLOW, linewidth=6.5, solid_capstyle="round", alpha=0.35, zorder=3)
        ax.plot(xs, ys, color=ROUTE_COLOR, linewidth=2.6, solid_capstyle="round", alpha=0.98, zorder=4)
        ax.scatter([xs[0], xs[-1]], [ys[0], ys[-1]], s=28, c=ENDPOINT, zorder=5, edgecolors="#0b1a22", linewidths=0.6)

    x0, y0 = to_merc.transform(minx, miny)
    x1, y1 = to_merc.transform(maxx, maxy)
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)

    try:
        cx.add_basemap(
            ax,
            source=cx.providers.CartoDB.DarkMatterNoLabels,
            crs="EPSG:3857",
            zoom="auto",
            attribution=False,
        )
    except Exception as e:
        # offline fallback: solid dark water/land plate so we still ship geometry
        ax.set_facecolor("#0b1520")
        fig.patch.set_facecolor("#0b1520")
        print(f"  WARN basemap failed ({e}); solid dark fallback")

    # left clear-space vignette (title zone)
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    vignette_w = (xmax - xmin) * clear
    ax.add_patch(
        FancyBboxPatch(
            (xmin, ymin),
            vignette_w,
            ymax - ymin,
            boxstyle="square,pad=0",
            facecolor="#050b12",
            edgecolor="none",
            alpha=0.55,
            zorder=6,
            transform=ax.transData,
        )
    )
    # soft gradient approximation: second lighter strip
    ax.add_patch(
        FancyBboxPatch(
            (xmin + vignette_w * 0.55, ymin),
            vignette_w * 0.45,
            ymax - ymin,
            boxstyle="square,pad=0",
            facecolor="#050b12",
            edgecolor="none",
            alpha=0.28,
            zorder=6,
            transform=ax.transData,
        )
    )

    out: Path = cfg["out"]
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=DPI, facecolor=fig.get_facecolor(), pad_inches=0)
    plt.close(fig)

    return {
        "key": key,
        "status": "ok",
        "file": str(out.relative_to(ROOT)),
        "route_ids_resolved": resolved,
        "route_ids_missing_skipped": missing,
        "sha256": sha256_file(out),
        "dimensions": f"{W_PX}x{H_PX}",
        "bytes": out.stat().st_size,
        "basemap": "CartoDB Dark Matter No Labels",
        "geometry_source": "data-clean/ROUTES.json",
    }


def main() -> int:
    by_id = load_routes()
    results = []
    for key, cfg in MAPS.items():
        print(f"=== {key} ===")
        r = render_one(key, cfg, by_id)
        results.append(r)
        print(" ", r.get("status"), r.get("file") or r.get("reason"), "routes", len(r.get("route_ids_resolved") or []))
        if r.get("route_ids_missing_skipped"):
            print("  skipped", r["route_ids_missing_skipped"][:8])

    receipt = {
        "at": datetime.now(timezone.utc).isoformat(),
        "spec": "handoff/partner-map-model/GROK-SPEC-mx-eg-map-localization-2026-07-22.md",
        "pr": 330,
        "discipline": "geojson renderer from ROUTES.json; no image-generated geography",
        "fail_closed": [
            "EG Cairo/Nile (geometry_only / demand+fare not sourced for deck P&L)",
            "EG El Gouna / Marsa Alam pending four-input",
            "MX Vallarta→Yelapa / extra Los Cabos demand cells pending sourcing checklist",
        ],
        "maps": results,
        "live_deck_ids": {
            "didi-mexico": "1XwKRuJtMrou8NtBdc1oY3LL2Dk83dCs9MCLvNKgwq0c",
            "indrive-egypt": "1Nn3BRKUahikp87zC84JMdEVrcJYppm9ZXHgndAuzsEk",
        },
        "note": "Plates banked under deck-studio/assets. Live Slides image swap requires Google OAuth; assets ship for human/Tasklet apply if token unavailable.",
    }
    PROVENANCE.parent.mkdir(parents=True, exist_ok=True)
    PROVENANCE.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n")
    print("Receipt:", PROVENANCE.relative_to(ROOT))
    ok = sum(1 for r in results if r["status"] == "ok")
    print(f"Done: {ok}/{len(results)} maps rendered")
    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
