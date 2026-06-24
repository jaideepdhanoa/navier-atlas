"""Shared leeward offshore arcs for intra-Curaçao legs (north gateway → south coast)."""
from __future__ import annotations

from bucketB_shared import densify

HATO = "curacao-curacao__hato-airport-waterfront"

# Wide arc west of Curaçao before turning south — never chord across the island.
LEEWARD_ARC: list[tuple[float, float]] = [
    (-69.02, 12.16),
    (-69.10, 12.12),
    (-69.18, 12.06),
    (-69.20, 11.98),
    (-69.12, 11.94),
    (-69.00, 11.96),
]

OFFSHORE_PAIRS: dict[tuple[str, str], list[tuple[float, float]]] = {
    (
        "curacao-curacao__hato-airport-waterfront",
        "curacao-curacao__sandals-royal-curacao-spanish-water",
    ): LEEWARD_ARC + [(-68.87, 12.05), (-68.85, 12.067)],
    (
        "curacao-curacao__hato-airport-waterfront",
        "curacao-curacao__baoase-luxury-resort",
    ): LEEWARD_ARC + [(-68.94, 12.04), (-68.90, 12.094)],
    (
        "curacao-curacao__hato-airport-waterfront",
        "curacao-curacao__spanish-water-jan-thiel",
    ): LEEWARD_ARC + [(-68.88, 12.06), (-68.86, 12.082)],
}


def pair_key(a: str, b: str) -> tuple[str, str]:
    return (a, b) if a <= b else (b, a)


def manual_waypoints(from_id: str, to_id: str) -> list[tuple[float, float]] | None:
    for key, wps in OFFSHORE_PAIRS.items():
        if pair_key(from_id, to_id) == pair_key(key[0], key[1]):
            return list(wps)
    if HATO in (from_id, to_id):
        city_a = from_id.split("__", 1)[0]
        city_b = to_id.split("__", 1)[0]
        if city_a == city_b == "curacao-curacao":
            return list(LEEWARD_ARC)
    return None


def build_offshore_coords(
    a: tuple[float, float],
    b: tuple[float, float],
    wps: list[tuple[float, float]] | None,
) -> list[list[float]]:
    pts = [a] + list(wps or []) + [b]
    coords: list[list[float]] = []
    for i in range(len(pts) - 1):
        seg = densify(pts[i], pts[i + 1], 22)
        coords.extend(seg if not coords else seg[1:])
    return coords