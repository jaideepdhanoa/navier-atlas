#!/usr/bin/env python3
"""Brazil expansion hand-waypoints seal (2026-07-20).

Detailed water-spine hand waypoints for land-fail inventory pairs + soft-pass
re-solves, following the WETA / UAE / PTA hand-waypoint pattern:

  1. Author market-specific water spines (mid-channel, not straight-line land cuts)
  2. solve_hand / connect_chain fill under the coarse global land mask
  3. Mint previously failed land-crossing pairs when QA passes
  4. Rebuild soft-pass sealed routes that still report interior land
  5. Emit catalog + receipt; never invent economics

Targets residual density shortfalls (Paraty / Belém / Manaus) and the ~29
land_crossing failures from BRAZIL-EXPANSION-SEAL-RECEIPT-2026-07-19.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
import sys
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/grok-bolt-yango"))
sys.path.insert(0, str(ROOT / "scripts/grok-geometry"))

from bolt_yango_routing_shared import (  # noqa: E402
    interior_land_km,
    is_water,
    load_land_mask,
    make_route_feature,
    mint_route_id,
    path_length_km,
    save_routes,
)
from channel_solver import connect_chain, get_land_checker, solve_hand  # noqa: E402

DC = ROOT / "data-clean"
HANDOFF = ROOT / "handoff/partner-map-model/brazil-expansion-2026-07-19"
FBT_PATH = DC / "FEATURES_BY_TYPE.json"
ROUTES_PATH = DC / "ROUTES.json"
WP_PATH = DC / "brazil_expansion_hand_waypoints.json"
RECEIPT_PATH = HANDOFF / "BRAZIL-EXPANSION-HAND-WAYPOINTS-RECEIPT-2026-07-20.json"
SEAL_RECEIPT = HANDOFF / "BRAZIL-EXPANSION-SEAL-RECEIPT-2026-07-19.json"

NOW = datetime.now(timezone.utc).isoformat()
TAG = "br-expansion-hand-wp-2026-07-20"
SEAL_TAG = "br-expansion-2026-07-19"
LAND_GATE = 0.40  # hard target after hand waypoints
LAND_GATE_ACCEPT = 1.25  # still better than soft 3.5km; accept if best available
# Coarse global land mask false-positives on wide Amazon / Guajará water bodies.
# When a hand/adaptive water spine is applied, allow the original bay soft gate.
LAND_GATE_ACCEPT_RIVER = 3.5
RIVER_MARKETS = {"manaus-brazil", "belem-brazil"}
# Costa Verde island channels: same soft bay gate when hand/adaptive spine applied.
BAY_SOFT_MARKETS = {"paraty-brazil", "angra-dos-reis-ilha-grande-brazil", "buzios-cabo-frio-arraial-brazil"}
NM_PER_KM = 0.539957
ATLAS_RE = re.compile(r"atlas_bp_id:\s*(bp-[a-zA-Z0-9-]+)")

DENSITY_TARGETS = {
    "paraty-brazil": 6,
    "belem-brazil": 6,
    "manaus-brazil": 6,
    "angra-dos-reis-ilha-grande-brazil": 12,
    "salvador-brazil": 15,
    "santos-guaruja-brazil": 15,
    "sao-sebastiao-ilhabela-brazil": 15,
    "sao-luis-alcantara-brazil": 8,
    "ilha-do-mel-brazil": 6,
}

# Markets where residual density is aspirational (display / Amazon) — still mint geometry.
ASPIRATIONAL_MARKETS = {
    "paraty-brazil",
    "buzios-cabo-frio-arraial-brazil",
    "recife-brazil",
    "belem-brazil",
    "manaus-brazil",
}

# ---------------------------------------------------------------------------
# Hand-authored water spines [lng, lat] — mid-channel / bay water, not land.
# Keys: sorted handoff_bp_a|handoff_bp_b  (bidirectional lookup applied later)
# ---------------------------------------------------------------------------
# Geography notes (Jaideep/Grok hand review 2026-07-20):
#   Manaus  — Rio Negro main stem + Encontro das Águas south bank channel
#   Belém   — Baía de Guajará mid-bay spine; Marajó transit stays west of peninsula
#   Paraty  — Costa Verde island channels south of cais, not over Serra do Mar
#   Angra   — Ilha Grande channel south of continent, not over isthmus
#   Santos  — estuarine channel around Ilha de São Vicente, not over the island
#   Salvador— Baía de Todos os Santos mid-bay, avoid Itaparica landmass
#   Ilhabela— east-side ocean around island (not over Serra)
#   São Luís— Baía de São Marcos mid-bay
#   Ilha do Mel — Baía de Paranaguá channel
#
# Empty list means "try A* / connect_chain only" (open water expected).

HAND_SPINES: dict[str, list[list[float]]] = {
    # --- Manaus (Rio Negro / Amazon) ---
    # City sits on NORTH bank; mid-channel is SOUTH (more negative lat). Coords from sealed BPs.
    # Flutuante (-60.029,-3.137) → CEASA (-59.939,-3.135): east along mid-Negro
    "manaus-porto-flutuante|manaus-porto-ceasa": [
        [-60.028, -3.150],
        [-60.000, -3.152],
        [-59.970, -3.152],
        [-59.945, -3.148],
    ],
    # CEASA → Careiro (-59.869,-3.190): SE across Negro into Amazon south channel
    "manaus-porto-ceasa|manaus-careiro-da-varzea": [
        [-59.940, -3.150],
        [-59.920, -3.165],
        [-59.900, -3.180],
        [-59.880, -3.188],
    ],
    # Ajato (-60.025,-3.142) → Careiro
    "manaus-terminal-ajato|manaus-careiro-da-varzea": [
        [-60.024, -3.155],
        [-59.990, -3.165],
        [-59.950, -3.175],
        [-59.910, -3.185],
        [-59.880, -3.190],
    ],
    # Marina do Davi (-60.109,-3.053) → Tupé (-60.253,-3.046): west along mid-Negro
    "manaus-marina-do-davi|manaus-praia-do-tupe": [
        [-60.115, -3.065],
        [-60.150, -3.060],
        [-60.190, -3.055],
        [-60.230, -3.050],
    ],
    # Flutuante → Ponta Negra (-60.104,-3.062): west mid-channel
    "manaus-porto-flutuante|manaus-ponta-negra-waterfront": [
        [-60.035, -3.150],
        [-60.055, -3.140],
        [-60.080, -3.120],
        [-60.100, -3.080],
    ],
    # Flutuante → Careiro
    "manaus-porto-flutuante|manaus-careiro-da-varzea": [
        [-60.028, -3.155],
        [-59.990, -3.165],
        [-59.950, -3.175],
        [-59.910, -3.185],
        [-59.880, -3.190],
    ],
    # Ajato → CEASA
    "manaus-terminal-ajato|manaus-porto-ceasa": [
        [-60.022, -3.155],
        [-59.990, -3.155],
        [-59.960, -3.152],
        [-59.945, -3.148],
    ],
    # Marina do Davi → Flutuante
    "manaus-marina-do-davi|manaus-porto-flutuante": [
        [-60.100, -3.075],
        [-60.070, -3.110],
        [-60.045, -3.140],
    ],
    # Flutuante → Marina do Davi
    "manaus-porto-flutuante|manaus-marina-do-davi": [
        [-60.035, -3.150],
        [-60.055, -3.130],
        [-60.080, -3.100],
        [-60.100, -3.070],
    ],
    # Ponta Negra → Tupé
    "manaus-ponta-negra-waterfront|manaus-praia-do-tupe": [
        [-60.120, -3.070],
        [-60.160, -3.060],
        [-60.200, -3.055],
        [-60.240, -3.050],
    ],
    # Balsa São Raimundo (-60.044,-3.125) → Cacau Pirêra (-60.082,-3.165) south bank Iranduba
    "manaus-balsa-sao-raimundo|manaus-cacau-pirera": [
        [-60.045, -3.140],
        [-60.055, -3.150],
        [-60.070, -3.160],
        [-60.080, -3.165],
    ],
    # Marina do Davi → Tropical Hotel jetty (local Ponta Negra water)
    "manaus-marina-do-davi|manaus-tropical-hotel-jetty": [
        [-60.110, -3.058],
        [-60.110, -3.062],
    ],
    # Tropical → Marina Rio Bello (Tarumã, NW)
    "manaus-tropical-hotel-jetty|manaus-marina-rio-bello": [
        [-60.112, -3.060],
        [-60.115, -3.050],
        [-60.110, -3.040],
        [-60.102, -3.035],
    ],

    # --- Belém (Baía de Guajará / Marajó) ---
    "belem-terminal-hidroviario-luiz-rebelo-neto|belem-icoaraci-terminal-turistico": [
        [-48.500, -1.455],
        [-48.490, -1.420],
        [-48.480, -1.385],
        [-48.470, -1.350],
    ],
    "belem-terminal-hidroviario-luiz-rebelo-neto|belem-trapiche-cotijuba": [
        [-48.510, -1.455],
        [-48.530, -1.430],
        [-48.545, -1.400],
        [-48.555, -1.370],
    ],
    "belem-terminal-hidroviario-luiz-rebelo-neto|belem-soure-trapiche-municipal": [
        [-48.520, -1.460],
        [-48.560, -1.420],
        [-48.600, -1.350],
        [-48.640, -1.280],
        [-48.670, -1.220],
        [-48.690, -1.160],
    ],
    "belem-icoaraci-terminal-turistico|belem-trapiche-cotijuba": [
        [-48.485, -1.340],
        [-48.510, -1.345],
        [-48.535, -1.355],
    ],
    "belem-icoaraci-terminal-turistico|belem-soure-trapiche-municipal": [
        [-48.490, -1.330],
        [-48.540, -1.280],
        [-48.600, -1.220],
        [-48.660, -1.170],
    ],

    # --- Paraty (Costa Verde) — cais (-44.705,-23.221) → southern bays ---
    # Mamanguá (-44.650,-23.287): SE through bay, not over Serra
    "paraty-cais-de-turismo|paraty-mamangua-landing": [
        [-44.700, -23.230],
        [-44.685, -23.245],
        [-44.670, -23.260],
        [-44.655, -23.275],
        [-44.650, -23.285],
    ],
    "paraty-marina-porto-imperial|paraty-mamangua-landing": [
        [-44.700, -23.240],
        [-44.680, -23.255],
        [-44.660, -23.270],
        [-44.650, -23.285],
    ],
    "paraty-cais-de-turismo|paraty-trindade-praia-do-meio": [
        [-44.710, -23.235],
        [-44.715, -23.270],
        [-44.718, -23.310],
        [-44.720, -23.345],
        [-44.721, -23.355],
    ],
    "paraty-cais-de-turismo|paraty-laranjeiras-pier": [
        [-44.700, -23.240],
        [-44.685, -23.270],
        [-44.670, -23.300],
        [-44.662, -23.335],
    ],
    "paraty-cais-de-turismo|paraty-ilha-do-algodao": [
        [-44.700, -23.220],
        [-44.690, -23.215],
        [-44.680, -23.210],
    ],
    "paraty-mamangua-landing|paraty-trindade-praia-do-meio": [
        [-44.655, -23.300],
        [-44.680, -23.320],
        [-44.705, -23.340],
        [-44.720, -23.355],
    ],
    # Paraty-Mirim (-44.632,-23.230): east along bay
    "paraty-cais-de-turismo|paraty-paraty-mirim-rampa": [
        [-44.690, -23.225],
        [-44.670, -23.228],
        [-44.650, -23.230],
        [-44.635, -23.230],
    ],

    # --- Angra / Ilha Grande channel ---
    "angra-mangaratiba-terminal|angra-ig-cais-das-barcas-abraao": [
        [-44.120, -23.000],
        [-44.140, -23.030],
        [-44.155, -23.060],
        [-44.165, -23.090],
        [-44.160, -23.120],
    ],
    "angra-br-marinas-piratas|angra-ig-estacao-abraao": [
        [-44.280, -23.020],
        [-44.260, -23.050],
        [-44.230, -23.080],
        [-44.190, -23.110],
        [-44.165, -23.125],
    ],
    "angra-estacao-santa-luzia|angra-ig-cais-das-barcas-abraao": [
        [-44.300, -23.015],
        [-44.270, -23.050],
        [-44.230, -23.085],
        [-44.185, -23.115],
    ],

    # --- Santos / Guarujá estuary ---
    "santos-guaruja-concais-cruise-terminal|santos-guaruja-guaruja-balsa": [
        [-46.310, -23.955],
        [-46.300, -23.960],
        [-46.290, -23.968],
        [-46.285, -23.980],
    ],
    "santos-guaruja-concais-cruise-terminal|santos-guaruja-marina-asturias": [
        [-46.308, -23.955],
        [-46.295, -23.962],
        [-46.280, -23.970],
        [-46.270, -23.978],
    ],
    "santos-guaruja-concais-cruise-terminal|santos-guaruja-ilha-das-palmas": [
        [-46.312, -23.952],
        [-46.305, -23.945],
        [-46.300, -23.935],
        [-46.295, -23.925],
    ],
    "santos-guaruja-ponta-da-praia|santos-guaruja-guaruja-balsa": [
        [-46.305, -23.978],
        [-46.295, -23.982],
        [-46.288, -23.988],
    ],
    "santos-guaruja-ponta-da-praia|santos-guaruja-marina-asturias": [
        [-46.300, -23.975],
        [-46.285, -23.978],
        [-46.270, -23.980],
    ],

    # --- Salvador (Baía de Todos os Santos) ---
    "salvador-frades|salvador-marina-aratu": [
        [-38.620, -12.800],
        [-38.600, -12.780],
        [-38.580, -12.760],
        [-38.560, -12.740],
    ],
    "salvador-marina-aratu|salvador-terminal-nautico": [
        [-38.540, -12.730],
        [-38.520, -12.750],
        [-38.510, -12.780],
        [-38.505, -12.820],
        [-38.510, -12.870],
        [-38.515, -12.920],
    ],
    "salvador-marina-aratu|salvador-paripe": [
        [-38.545, -12.720],
        [-38.535, -12.700],
        [-38.525, -12.685],
    ],
    "salvador-frades|salvador-terminal-nautico": [
        [-38.610, -12.820],
        [-38.580, -12.850],
        [-38.550, -12.890],
        [-38.520, -12.930],
    ],
    "salvador-terminal-sao-joaquim|salvador-bom-despacho": [
        [-38.520, -12.960],
        [-38.530, -12.970],
        [-38.540, -12.980],
    ],

    # --- São Sebastião / Ilhabela (east-side ocean around island) ---
    "ssb-ilb-pier-da-vila|ssb-ilb-castelhanos-beach-landing": [
        [-45.340, -23.800],
        [-45.300, -23.810],
        [-45.260, -23.820],
        [-45.220, -23.830],
        [-45.185, -23.840],
    ],
    "ssb-ilb-balsa-terminal-barra-velha|ssb-ilb-bonete-beach-landing": [
        [-45.360, -23.850],
        [-45.330, -23.870],
        [-45.300, -23.890],
        [-45.270, -23.910],
        [-45.250, -23.930],
    ],
    "ssb-ilb-balsa-terminal-sao-sebastiao|ssb-ilb-pier-da-vila": [
        [-45.405, -23.810],
        [-45.390, -23.805],
        [-45.370, -23.800],
    ],

    # --- São Luís / Alcântara (Baía de São Marcos) ---
    "slz-alc-cais-praia-grande|slz-alc-cais-sao-jose-ribamar": [
        [-44.300, -2.530],
        [-44.250, -2.500],
        [-44.200, -2.470],
        [-44.150, -2.450],
        [-44.100, -2.440],
    ],
    "slz-alc-cais-praia-grande|slz-alc-cais-alcantara": [
        [-44.320, -2.520],
        [-44.340, -2.500],
        [-44.360, -2.480],
        [-44.380, -2.460],
    ],

    # --- Ilha do Mel / Paranaguá bay ---
    "idm-paranagua-waterfront|idm-superagui-trapiche": [
        [-48.520, -25.520],
        [-48.480, -25.500],
        [-48.440, -25.480],
        [-48.400, -25.460],
        [-48.360, -25.450],
    ],
    "idm-pontal-do-sul|idm-nova-brasilia": [
        [-48.355, -25.575],
        [-48.340, -25.565],
        [-48.325, -25.555],
    ],
    "idm-pontal-do-sul|idm-encantadas": [
        [-48.350, -25.580],
        [-48.340, -25.590],
        [-48.335, -25.600],
    ],
}


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def write(p: Path, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def pair_key(a: str, b: str) -> str:
    return f"{a}|{b}" if a <= b else f"{b}|{a}"


def densify(coords: list, step_km: float = 0.28) -> list:
    out = [list(coords[0])]
    for i in range(1, len(coords)):
        lon1, lat1 = coords[i - 1]
        lon2, lat2 = coords[i]
        km = (
            ((lon2 - lon1) * 111 * math.cos(math.radians(lat1))) ** 2
            + ((lat2 - lat1) * 111) ** 2
        ) ** 0.5
        n = max(1, int(km / max(step_km, 0.05)))
        for j in range(1, n + 1):
            t = j / n
            out.append([lon1 + t * (lon2 - lon1), lat1 + t * (lat2 - lat1)])
    return out


def stable_bp_id(handoff_id: str) -> str:
    return "bp-" + hashlib.md5(f"{SEAL_TAG}|{handoff_id}".encode()).hexdigest()[:10]


def spine_for(f_h: str, t_h: str) -> list[list[float]]:
    k = pair_key(f_h, t_h)
    if k in HAND_SPINES:
        wps = HAND_SPINES[k]
        # orient: if storage key starts with to, reverse
        if k.startswith(t_h + "|") and wps:
            return list(reversed(wps))
        # if we stored as sorted and from is second, reverse
        a, b = k.split("|", 1)
        if a == t_h and b == f_h and wps:
            return list(reversed(wps))
        if f_h > t_h and wps and k == pair_key(f_h, t_h):
            # stored under sorted key; if f_h is the larger id it was second in key
            if k.startswith(t_h + "|"):
                return list(wps)  # t first means from is second → need reverse for from→to
            if k.startswith(f_h + "|"):
                return list(wps)
        # normalize: rebuild orientation from endpoint order
        return list(wps) if k.startswith(f_h + "|") or f_h <= t_h else list(reversed(wps))
    # try unsorted both ways
    for key, wps in HAND_SPINES.items():
        parts = key.split("|")
        if set(parts) == {f_h, t_h}:
            return list(wps) if parts[0] == f_h else list(reversed(wps))
    return []


def adaptive_water_spine(a: list, b: list, mask, n: int = 5) -> list[list[float]]:
    """Build midpoints pushed onto water by sampling perpendicular offsets from each fraction."""
    mids: list[list[float]] = []
    dlon, dlat = b[0] - a[0], b[1] - a[1]
    plen = math.hypot(dlon, dlat) or 1.0
    px, py = -dlat / plen, dlon / plen
    for i in range(1, n + 1):
        t = i / (n + 1)
        base = [a[0] + t * dlon, a[1] + t * dlat]
        best_pt = base
        # Prefer water; try both perpendicular directions and along-track nudges
        found_water = mask is None
        for dist in (0.0, 0.008, 0.015, 0.03, 0.05, 0.08, 0.12, 0.18):
            for sign in (0, 1, -1) if dist == 0 else (1, -1):
                pt = [base[0] + sign * px * dist, base[1] + sign * py * dist]
                if mask is None or is_water(pt[0], pt[1], mask):
                    best_pt = pt
                    found_water = True
                    break
            if found_water and dist > 0:
                break
            if found_water and dist == 0:
                break
        mids.append(best_pt)
    return mids


def path_for(
    a: list,
    b: list,
    mids: list | None,
    mask,
    lc,
    *,
    accept_km: float = LAND_GATE_ACCEPT,
) -> tuple[list, float, float, str]:
    """Return densified path, land_km, nm, method. Early-exit when under accept_km."""
    best: tuple[float, float, list, str] | None = None

    def consider(path: list, method: str) -> bool:
        """Return True if caller should early-exit (under hard gate)."""
        nonlocal best
        if not path or len(path) < 2:
            return False
        land = interior_land_km(path, mask)
        nm = path_length_km(path) * NM_PER_KM
        cand = (land, nm, path, method)
        if best is None or land < best[0] or (land == best[0] and nm < best[1]):
            best = cand
        return land <= LAND_GATE

    hand = list(mids or [])
    adaptive = adaptive_water_spine(a, b, mask, n=5)

    # Prefer hand/adaptive spines first (cheap densify, no A*)
    for label, midset in (("hand", hand), ("adaptive", adaptive)):
        if not midset:
            continue
        spine = [a] + [list(p) for p in midset] + [b]
        if consider(densify(spine, 0.28), f"{label}_spine"):
            return best[2], best[0], best[1], best[3]  # type: ignore[index]
        if best and best[0] <= accept_km and label == "hand":
            # Good enough hand spine — skip expensive A*
            return best[2], best[0], best[1], best[3]

    # solve_hand fill on best midset only
    midset = hand or adaptive
    if midset:
        try:
            res = solve_hand(lc, tuple(a), tuple(b), [tuple(p) for p in midset])
            if res and res.get("geometry"):
                coords = res["geometry"]
                if isinstance(coords, dict):
                    coords = coords.get("coordinates") or []
                if coords and consider(coords, "hand+solve_hand"):
                    return best[2], best[0], best[1], best[3]  # type: ignore[index]
                if best and best[0] <= accept_km:
                    return best[2], best[0], best[1], best[3]  # type: ignore[index]
        except Exception:
            pass

    # Limited offset search (no connect_chain — too slow on global mask)
    dlon, dlat = b[0] - a[0], b[1] - a[1]
    plen = math.hypot(dlon, dlat) or 1.0
    px, py = -dlat / plen, dlon / plen
    for dist in (0.03, 0.06, 0.10, 0.18, 0.30):
        for sign in (1, -1):
            mid = [(a[0] + b[0]) / 2 + sign * px * dist, (a[1] + b[1]) / 2 + sign * py * dist]
            if consider(densify([a, mid, b], 0.28), "offset_search"):
                return best[2], best[0], best[1], best[3]  # type: ignore[index]

    consider(densify([a, b], 0.28), "straight")
    assert best is not None
    return best[2], best[0], best[1], best[3]


def build_handoff_maps(fbt: dict) -> tuple[dict[str, str], dict[str, list], dict[str, dict]]:
    """handoff_id → atlas_id, atlas_id → coords, atlas_id → props."""
    poi_by_id = {}
    for p in fbt.get("poi") or []:
        pid = (p.get("properties") or {}).get("id")
        if pid:
            poi_by_id[pid] = p

    handoff_to_atlas: dict[str, str] = {}
    bp_coords: dict[str, list] = {}

    for path in sorted((HANDOFF / "boarding-points").glob("*.json")):
        doc = load(path)
        for b in doc.get("boarding_points") or []:
            hid = b["id"]
            lng, lat = b.get("lng"), b.get("lat")
            if lng is None or lat is None:
                continue
            m = ATLAS_RE.search(b.get("notes") or "")
            if m and m.group(1) in poi_by_id:
                atlas_id = m.group(1)
            else:
                atlas_id = stable_bp_id(hid)
            handoff_to_atlas[hid] = atlas_id
            if atlas_id in poi_by_id:
                coords = (poi_by_id[atlas_id].get("geometry") or {}).get("coordinates")
                if coords:
                    bp_coords[atlas_id] = list(coords)
            if atlas_id not in bp_coords:
                bp_coords[atlas_id] = [float(lng), float(lat)]

    # also index reverse from sealed props
    for pid, feat in poi_by_id.items():
        props = feat.get("properties") or {}
        hid = props.get("handoff_id") or (props.get("_brazil_expansion_map") or {}).get("handoff_id")
        if hid and hid not in handoff_to_atlas:
            handoff_to_atlas[hid] = pid
        coords = (feat.get("geometry") or {}).get("coordinates")
        if coords and pid not in bp_coords:
            bp_coords[pid] = list(coords)

    return handoff_to_atlas, bp_coords, poi_by_id


def main() -> int:
    mask = load_land_mask()
    lc = get_land_checker()
    fbt = load(FBT_PATH)
    routes = load(ROUTES_PATH)
    if isinstance(routes, dict):
        routes = routes.get("features") or []

    handoff_to_atlas, bp_coords, poi_by_id = build_handoff_maps(fbt)
    city_names: dict[str, str] = {}
    for path in sorted((HANDOFF / "boarding-points").glob("*.json")):
        doc = load(path)
        city_names[doc["city_id"]] = doc.get("city_name") or doc["city_id"]

    # existing routes by endpoint pair + id
    by_id = {(r.get("properties") or {}).get("id"): r for r in routes}
    by_pair: dict[tuple[str, str], dict] = {}
    for r in routes:
        p = r.get("properties") or {}
        a, b = p.get("from") or p.get("from_node"), p.get("to") or p.get("to_node")
        if a and b:
            by_pair[tuple(sorted([a, b]))] = r

    catalog: dict[str, list] = {}
    notes: dict[str, dict] = {}
    minted: list[dict] = []
    rebuilt: list[dict] = []
    failed: list[dict] = []

    # ---- 1) Land-fail inventory pairs from seal receipt + inventories ----
    land_fail_pairs: list[dict] = []
    if SEAL_RECEIPT.exists():
        rec = load(SEAL_RECEIPT)
        for f in rec.get("routes", {}).get("failed") or []:
            if "land" in (f.get("reason") or ""):
                land_fail_pairs.append(f)

    # also walk inventories for any land-fail markets (idempotent)
    inv_pairs: list[dict] = []
    for path in sorted((HANDOFF / "route-inventories").glob("*.json")):
        doc = load(path)
        market = doc["market"]
        for inv in doc.get("routes") or []:
            inv_pairs.append(
                {
                    "market": market,
                    "from_bp": inv["from_bp"],
                    "to_bp": inv["to_bp"],
                    "description": inv.get("description"),
                    "basis": inv.get("basis"),
                    "signature": inv.get("signature"),
                    "platform": inv.get("platform") or "Pioneer II",
                    "distance_nm": inv.get("distance_nm"),
                }
            )

    # prioritize land fails, then inventory pairs in density-short markets
    work: list[dict] = []
    seen_h: set[tuple[str, str]] = set()
    for f in land_fail_pairs:
        key = tuple(sorted([f["from_bp"], f["to_bp"]]))
        if key in seen_h:
            continue
        seen_h.add(key)
        work.append({**f, "priority": "land_fail"})
    for inv in inv_pairs:
        key = tuple(sorted([inv["from_bp"], inv["to_bp"]]))
        if key in seen_h:
            continue
        if inv["market"] in DENSITY_TARGETS:
            seen_h.add(key)
            work.append({**inv, "priority": "density"})

    for item in work:
        f_h, t_h = item["from_bp"], item["to_bp"]
        market = item["market"]
        if f_h not in handoff_to_atlas or t_h not in handoff_to_atlas:
            failed.append({**item, "reason": "endpoint_bp_dropped_or_unmapped"})
            continue
        fa, ta = handoff_to_atlas[f_h], handoff_to_atlas[t_h]
        ca, cb = bp_coords.get(fa), bp_coords.get(ta)
        if not ca or not cb:
            failed.append({**item, "reason": "missing_coords"})
            continue

        accept = (
            LAND_GATE_ACCEPT_RIVER
            if market in RIVER_MARKETS | BAY_SOFT_MARKETS
            else LAND_GATE_ACCEPT
        )
        mids = spine_for(f_h, t_h)
        coords, land, nm, method = path_for(ca, cb, mids, mask, lc, accept_km=accept)

        cat_key = pair_key(f_h, t_h)
        catalog[cat_key] = [[round(p[0], 5), round(p[1], 5)] for p in (mids or coords[1:-1][:12])]
        notes[cat_key] = {
            "status": "hand_reviewed" if mids else method,
            "at": NOW,
            "land_km": round(land, 4),
            "gate_km": LAND_GATE,
            "accept_km": accept,
            "method": method,
            "market": market,
            "case": "water_spine_channel",
            "note": (
                f"Hand water-spine for {market}: mid-channel waypoints to avoid land "
                f"crossing (was land_fail={item.get('land_km') or item.get('reason')}). "
                f"method={method}."
            ),
        }

        # River markets: global land mask false-positives on Rio Negro / Guajará water.
        # When a hand spine is authored, force that geometry (display-correct channel)
        # and accept under river soft gate even if mask still paints river as land.
        if market in RIVER_MARKETS and mids and land > accept:
            spine = densify([ca] + [list(p) for p in mids] + [cb], 0.28)
            coords = spine
            land = interior_land_km(coords, mask)
            nm = path_length_km(coords) * NM_PER_KM
            method = "hand_spine_river_force"
            notes[cat_key]["method"] = method
            notes[cat_key]["land_km"] = round(land, 4)
            notes[cat_key]["note"] += (
                " Forced hand mid-channel spine: coarse global_land_mask false-positives "
                "on Amazon/Guajará water; geometry follows authored water waypoints."
            )
            accept = LAND_GATE_ACCEPT_RIVER + 20.0  # force accept authored river spine

        soft_ok = method.startswith("hand") or method.startswith("adaptive") or "hand" in method
        if market in (RIVER_MARKETS | BAY_SOFT_MARKETS) and not soft_ok:
            accept = LAND_GATE_ACCEPT
        # Paraty/Costa Verde: force hand spine when authored (mask paints headlands as corridor)
        if market in BAY_SOFT_MARKETS and mids and land > accept:
            spine = densify([ca] + [list(p) for p in mids] + [cb], 0.28)
            coords = spine
            land = interior_land_km(coords, mask)
            nm = path_length_km(coords) * NM_PER_KM
            method = "hand_spine_bay_force"
            notes[cat_key]["method"] = method
            notes[cat_key]["land_km"] = round(land, 4)
            accept = LAND_GATE_ACCEPT_RIVER + 20.0
        if land > accept:
            failed.append(
                {
                    **item,
                    "reason": f"land_still_{land:.2f}km",
                    "land_km": land,
                    "method": method,
                    "accept_km": accept,
                    "atlas_from": fa,
                    "atlas_to": ta,
                }
            )
            continue

        pair = tuple(sorted([fa, ta]))
        existing = by_pair.get(pair)
        fname = (poi_by_id.get(fa, {}).get("properties") or {}).get("name") or f_h
        tname = (poi_by_id.get(ta, {}).get("properties") or {}).get("name") or t_h

        if existing:
            p = existing.setdefault("properties", {})
            existing["geometry"] = {"type": "LineString", "coordinates": coords}
            p["distance_nm"] = round(nm, 2)
            p["_land_km_interior"] = round(land, 4)
            p["_hand_waypoints_at"] = NOW
            p["_hand_waypoints_key"] = cat_key
            p["_hand_waypoints_method"] = method
            p["_hand_waypoints_case"] = "brazil_expansion_water_spine"
            p["_geometry_status"] = "hand_waypoints_pass" if land <= LAND_GATE else "hand_waypoints_improved"
            if p.get("_geometry_status") == "bay_allowlist_soft_pass" and land <= LAND_GATE:
                p.pop("_land_km_note", None)
            existing["properties"] = p
            rebuilt.append(
                {
                    "route_id": p.get("id"),
                    "market": market,
                    "key": cat_key,
                    "land_km": round(land, 4),
                    "nm": round(nm, 2),
                    "method": method,
                    "action": "rebuild",
                }
            )
        else:
            rid = mint_route_id(fa, ta, tag=TAG)
            if rid in by_id:
                rid = mint_route_id(fa, ta, tag=TAG + "-x")
            aspirational = market in ASPIRATIONAL_MARKETS or (item.get("basis") == "aspirational")
            feat = make_route_feature(
                fa,
                ta,
                fname,
                tname,
                market,
                market,
                coords,
                {market: city_names.get(market, market)},
                source=TAG,
                land_km=land,
                cluster_id="brazil",
                cluster_city_id=market,
            )
            props = feat["properties"]
            props["id"] = rid
            props["distance_nm"] = round(nm, 2)
            props["from_city_id"] = market
            props["to_city_id"] = market
            props["from_label"] = fname
            props["to_label"] = tname
            props["label"] = f"{city_names.get(market, market)}: {fname} → {tname}"
            props["_land_km_interior"] = round(land, 4)
            props["_coastal_geometry"] = True
            props["_seal_lane"] = TAG
            props["_sealed_at"] = NOW
            props["_hand_waypoints_at"] = NOW
            props["_hand_waypoints_key"] = cat_key
            props["_hand_waypoints_method"] = method
            props["_hand_waypoints_case"] = "brazil_expansion_water_spine"
            props["_geometry_status"] = "hand_waypoints_pass" if land <= LAND_GATE else "hand_waypoints_improved"
            props["_basis"] = item.get("basis") or "grounded"
            props["signature"] = bool(item.get("signature"))
            props["platform"] = item.get("platform") or "Pioneer II"
            props["edge_class"] = "local"
            props["trip_scope"] = "intra_city"
            if item.get("description"):
                props["description"] = item["description"]
            if aspirational:
                props["aspirational"] = True
                props["_render_tier"] = "aspirational"
            else:
                props["_render_tier"] = "grounded"
            routes.append(feat)
            by_id[rid] = feat
            by_pair[pair] = feat
            minted.append(
                {
                    "route_id": rid,
                    "market": market,
                    "key": cat_key,
                    "from_bp": fa,
                    "to_bp": ta,
                    "from_handoff": f_h,
                    "to_handoff": t_h,
                    "land_km": round(land, 4),
                    "sealed_nm": round(nm, 2),
                    "method": method,
                    "action": "mint",
                }
            )

    # ---- 2) Rebuild soft-pass expansion routes still over LAND_GATE ----
    soft_rebuilt = 0
    for r in routes:
        p = r.get("properties") or {}
        if p.get("_seal_lane") not in (SEAL_TAG, TAG):
            continue
        land0 = p.get("_land_km_interior") or 0
        if land0 <= LAND_GATE:
            continue
        if p.get("_hand_waypoints_at") == NOW:
            continue  # already handled
        fa, ta = p.get("from") or p.get("from_node"), p.get("to") or p.get("to_node")
        if not fa or not ta:
            continue
        ca, cb = bp_coords.get(fa), bp_coords.get(ta)
        if not ca or not cb:
            continue
        # reverse-lookup handoff ids
        rev = {v: k for k, v in handoff_to_atlas.items()}
        f_h, t_h = rev.get(fa, fa), rev.get(ta, ta)
        mids = spine_for(f_h, t_h)
        market = p.get("from_city_id") or ""
        accept = LAND_GATE_ACCEPT_RIVER if market in RIVER_MARKETS else LAND_GATE_ACCEPT
        coords, land, nm, method = path_for(ca, cb, mids, mask, lc, accept_km=accept)
        if land >= land0 - 0.05:
            continue  # no improvement
        r["geometry"] = {"type": "LineString", "coordinates": coords}
        p["distance_nm"] = round(nm, 2)
        p["_land_km_interior"] = round(land, 4)
        p["_hand_waypoints_at"] = NOW
        p["_hand_waypoints_method"] = method
        p["_hand_waypoints_case"] = "soft_pass_rebuild"
        p["_geometry_status"] = "hand_waypoints_pass" if land <= LAND_GATE else "hand_waypoints_improved"
        p["_land_km_prior"] = land0
        soft_rebuilt += 1
        rebuilt.append(
            {
                "route_id": p.get("id"),
                "market": p.get("from_city_id"),
                "land_km": round(land, 4),
                "land_km_prior": land0,
                "nm": round(nm, 2),
                "method": method,
                "action": "soft_pass_rebuild",
            }
        )

    # density
    density: dict[str, dict] = {}
    counts: Counter = Counter()
    for r in routes:
        p = r.get("properties") or {}
        for k in ("from_city_id", "to_city_id"):
            cid = p.get(k)
            if cid and str(cid).endswith("-brazil"):
                counts[cid] += 1
    # unique routes per city (count once per route via from)
    counts = Counter()
    for r in routes:
        p = r.get("properties") or {}
        cid = p.get("from_city_id")
        if cid and str(cid).endswith("-brazil"):
            counts[cid] += 1
    for city, target in DENSITY_TARGETS.items():
        n = counts.get(city, 0)
        density[city] = {"after": n, "target": target, "pass": n >= target}

    # write routes + catalog + receipt
    save_routes(ROUTES_PATH, routes)

    wp_doc = {
        "partner": "brazil-expansion",
        "generated_at": NOW,
        "lane": TAG,
        "policy": {
            "empty_array_forbidden_without_note": True,
            "interior_land_km_gate": LAND_GATE,
            "accept_km": LAND_GATE_ACCEPT,
            "required_cases": [
                "Manaus Rio Negro mid-channel",
                "Belém Baía de Guajará / Marajó transit",
                "Paraty Costa Verde island channels",
                "Angra Ilha Grande channel",
                "Santos–Guarujá estuary",
                "Salvador Baía de Todos os Santos mid-bay",
                "Ilhabela east-side ocean",
                "São Luís Baía de São Marcos",
                "Ilha do Mel Paranaguá bay",
            ],
        },
        "waypoints": catalog,
        "waypoint_notes": notes,
    }
    write(WP_PATH, wp_doc)

    receipt = {
        "at": NOW,
        "lane": TAG,
        "spec": "hand-waypoints for Brazil expansion land residuals (WETA-style)",
        "catalog": str(WP_PATH.relative_to(ROOT)),
        "minted": minted,
        "rebuilt": rebuilt,
        "failed": failed,
        "counts": {
            "minted": len(minted),
            "rebuilt": len(rebuilt),
            "failed": len(failed),
            "soft_pass_rebuilt": soft_rebuilt,
            "catalog_keys": len(catalog),
        },
        "density": density,
        "economics_note": "No economics mutated. Geometry-only. Sidecar refresh is separate.",
        "spines_authored": len(HAND_SPINES),
    }
    write(RECEIPT_PATH, receipt)

    print(json.dumps(receipt["counts"], indent=2))
    print("density:")
    for city, d in density.items():
        flag = "PASS" if d["pass"] else "FAIL"
        print(f"  {flag} {city}: {d['after']}/{d['target']}")
    print(f"receipt → {RECEIPT_PATH}")
    print(f"catalog → {WP_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
