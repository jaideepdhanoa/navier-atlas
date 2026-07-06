"""Resolve contention cluster_id → city_ids for global corridor reseal."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from partner_scope_py import MARKET_CLUSTER_ALIASES, load_clusters  # noqa: E402

HANDOFF = ROOT / "handoff" / "uae-consolidation"

# Virtual / composite market keys → member city_ids (Tasklet contention audit).
CLUSTER_SCOPE_OVERRIDES: dict[str, list[str]] = {
    "bali-nusa-gili": [
        "bali-indonesia",
        "lombok-indonesia",
        "gili-trawangan-indonesia",
        "gili-meno-indonesia",
        "gili-air-indonesia",
        "nusa-penida-indonesia",
        "nusa-lembongan-indonesia",
    ],
    "chennai-ecr-cuddalore-puducherry-coast": [
        "chennai-india",
        "puducherry-india",
        "cuddalore-india",
    ],
    "kolkata-hooghly-waterfront": ["kolkata-india"],
    "phuket-andaman": [
        "phuket-phang-nga-thailand",
        "krabi-thailand",
        "koh-phi-phi-thailand",
        "koh-lanta-thailand",
    ],
    "koh-samui-gulf": [
        "koh-samui-thailand",
        "koh-phangan-thailand",
        "koh-tao-thailand",
    ],
    "komodo-flores": ["labuan-bajo-flores-indonesia", "komodo-indonesia"],
    "eastern-seaboard": [
        "pattaya-thailand",
        "koh-samet-thailand",
        "koh-chang-thailand",
    ],
    "royal-coast": ["hua-hin-thailand", "cha-am-thailand"],
    "lake-toba": ["lake-toba-sumatra-indonesia"],
    "raja-ampat": ["raja-ampat-papua-indonesia"],
    "bay-area": [
        "san-francisco-usa",
        "oakland-usa",
        "sausalito-usa",
        "vallejo-usa",
        "alameda-usa",
    ],
    "bolt-france-riviera": [
        "cote-dazur-france",
        "monaco-france",
        "saint-tropez-france",
    ],
    "cote-dazur-france": ["cote-dazur-france", "monaco-france", "saint-tropez-france"],
}

PARTNER_PREFIX_CLUSTERS = ("bolt-", "yango-", "indrive-")

# UAE geometry already sealed on main — skip full reseal for these contention ids.
UAE_PRE_SEALED_CLUSTERS = frozenset(
    {
        "abu-dhabi-uae",
        "dubai-uae",
        "fujairah-uae",
        "ras-al-khaimah-uae",
        "sharjah-uae",
        "uae",
        "uae-east-coast",
        "uae-sir-bani-yas",
    }
)

RIVER_CITIES = frozenset({"bangkok-thailand"})

NEVER_MINT_PAIRS = frozenset(
    {
        frozenset(("baku-azerbaijan", "aktau-kazakhstan")),
        frozenset(("bp-baku-boulevard-pier", "bp-aktau-seaport")),
    }
)


def load_contention_order() -> list[dict]:
    doc = json.loads((HANDOFF / "CONTENTION-ORDER.json").read_text())
    return doc.get("ordered_by_contention") or []


def resolve_cluster_city_ids(
    cluster_id: str,
    cluster_by_id: dict[str, dict] | None = None,
    city_to_cluster: dict[str, str] | None = None,
) -> set[str]:
    if cluster_id in CLUSTER_SCOPE_OVERRIDES:
        return set(CLUSTER_SCOPE_OVERRIDES[cluster_id])

    if cluster_by_id is None or city_to_cluster is None:
        _, cluster_by_id, city_to_cluster = load_clusters()

    cluster = cluster_by_id.get(cluster_id)
    if cluster and cluster.get("member_city_ids"):
        return set(cluster["member_city_ids"])

    if cluster_id in city_to_cluster:
        return {cluster_id}

    alias = MARKET_CLUSTER_ALIASES.get(cluster_id)
    if alias and alias != "__cross_border__":
        ac = cluster_by_id.get(alias)
        if ac and ac.get("member_city_ids"):
            return set(ac["member_city_ids"])

    for prefix in PARTNER_PREFIX_CLUSTERS:
        if cluster_id.startswith(prefix):
            geo = cluster_id[len(prefix) :]
            gc = cluster_by_id.get(geo)
            if gc and gc.get("member_city_ids"):
                return set(gc["member_city_ids"])

    return {cluster_id}


def min_nm_for_cluster(cluster_id: str, city_ids: set[str]) -> float:
    if cluster_id in RIVER_CITIES or RIVER_CITIES & city_ids:
        return 0.4
    return 3.0