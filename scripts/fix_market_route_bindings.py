#!/usr/bin/env python3
"""Apply economics-backed route binding fixes + domestic chip scrub.

Uses economics_by_route_id.json as source of truth, with manual pins for
geometry/economics drift cases. Scrubs cross-border legs from intra-scoped chips.

Usage:
  python3 scripts/fix_market_route_bindings.py --dry-run
  python3 scripts/fix_market_route_bindings.py --apply
  python3 scripts/fix_market_route_bindings.py --apply --partner grab bolt yango
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import relink_partner_journeys as r  # noqa: E402

PARTNERS_DIR = ROOT / "data-clean/partners"
REPORT_PATH = ROOT / "navier/handoff/journey-relink/binding-fix-report.json"

CROSS_BORDER_RE = re.compile(
    r"harbour bay|batam|bintan|bandar bentan|desaru|johor|sekupang|nongsa|"
    r"pasir gudang|riau islands|tanjung pinang|penang(?! hill)|langkawi|"
    r"koh lipe|manama|bahrain|soul beach abu dhabi",
    re.I,
)

CROSS_BORDER_MARKETS = frozenset({
    "cross-border", "cross_border", "mena", "uae", "ksa-red-sea", "ksa-commercial",
    "brazil-latam", "mexico", "mediterranean", "cote-dazur", "istanbul",
    "riau", "borneo", "philippines-cross", "singapore-cross",
})

# Explicit pins when economics geometry drifts or pier-exact routes exist outside econ.
MANUAL_PINS: dict[tuple[str, str | None, str, str], str] = {
    # P0 — Singapore hub journeys
    ("grab", None, "Marina Bay / CBD", "Sentosa & the Southern Islands"): "rn-df27ac2fd4a6",
    # P1 — cross-border hub + market
    ("grab", None, "Singapore (Tanah Merah)", "Bintan — Lagoi resorts (Bandar Bentan Telani)"): "rn-f3670ea7d99b",
    ("grab", None, "Singapore (Tanah Merah)", "Desaru Coast (Johor, Malaysia)"): "rn-ef7c059adbde",
    ("grab", "cross-border", "Singapore", "Bintan (Lagoi resort zone)"): "rn-f3670ea7d99b",
    # P1 — Phuket / Penang
    ("grab", None, "Phuket", "Langkawi (via the Andaman)"): "rn-853cbe7dd006",
    ("grab", "phuket", "Phuket", "Langkawi (via the Andaman)"): "rn-853cbe7dd006",
    # P1 — Koh Samui pier-exact
    ("grab", "koh-samui", "Four Seasons Koh Samui (Laem Yai)", "Ang Thong Marine Park (Wua Talap)"): "gcn-9c702ab026-shared",
    ("grab", "koh-samui", "Koh Samui (Nathon / Lipa Noi)", "Donsak (Surat Thani mainland)"): "ics-66f63f2796",
    ("grab", "koh-samui", "Koh Samui (Lipa Noi)", "Donsak (Raja Ferry pier)"): "ics-5038f54700",
    ("grab", "koh-samui", "Samui Pralarn Pier (Mae Nam)", "Koh Phangan (Thong Sala) — pier-exact"): "ics-b90279ab06",
    # P2 — Cambodia
    ("grab", "cambodia", "Sihanoukville Port", "Lila Resort / Ream private islands"): "ics-40367adcc3",
    # P2 — Jakarta
    ("grab", "jakarta", "Marina Ancol", "Thousand Islands — inner ring (Bidadari / Ayer / Onrust)"): "ics-9e59ba5c5c",
    ("grab", "jakarta", "Thousand Islands — inner ring", "Thousand Islands — outer ring"): "ics-62e1590af9",
    ("grab", "vietnam", "Saigon (Bach Dang)", "Vung Tau"): "rn-00dfea36a4d9",
    ("grab", "penang", "Langkawi", "Koh Lipe (Thailand)"): "gcn-b3d5523f36-shared",
    ("grab", "taiwan", "Magong (Penghu)", "Penghu outer islands (Qimei / Wang'an)"): "ics-25ecef3e3b",
    ("grab", "koh-samui", "Koh Samui (Bangrak)", "Don Sak Ferry Harbour"): "rn-347c44e1d360",
}

# Label-only pins (featured routes with label but no from/to)
LABEL_PINS: dict[tuple[str, str | None, str], str] = {
    ("grab", None, "Phuket ↔ Langkawi — Andaman cross-border (Quanta-LR)"): "rn-853cbe7dd006",
    ("grab", "cross-border", "Singapore ↔ Bintan (Lagoi resort zone)"): "rn-f3670ea7d99b",
    ("grab", "koh-samui", "Four Seasons Koh Samui (Laem Yai) ↔ Ang Thong Marine Park (Wua Talap)"): "gcn-9c702ab026-shared",
    ("grab", "koh-samui", "Samui Pralarn Pier (Mae Nam) ↔ Koh Phangan (Thong Sala) — pier-exact"): "ics-b90279ab06",
    ("grab", "koh-samui", "Koh Samui (Nathon) ↔ Donsak (Seatran harbour)"): "ics-66f63f2796",
    ("grab", "koh-samui", "Koh Samui (Lipa Noi) ↔ Donsak (Raja Ferry pier)"): "ics-5038f54700",
    ("grab", "cambodia", "Sihanoukville Port ↔ Lila Resort / Ream private islands"): "ics-40367adcc3",
    ("grab", "jakarta", "Marina Ancol ↔ Thousand Islands — inner ring (Bidadari / Ayer / Onrust)"): "ics-9e59ba5c5c",
    ("grab", "jakarta", "Thousand Islands — inner ring ↔ Thousand Islands — outer ring"): "ics-62e1590af9",
    ("grab", "cross-border", "Singapore / Desaru ↔ East-coast Malaysia & outer Riau (regional reach)"): "rn-ef7c059adbde",
    ("grab", "cross-border", "Singapore / Desaru — East-coast Malaysia & outer Riau (regional reach)"): "rn-ef7c059adbde",
    ("grab", "penang", "Langkawi ↔ Koh Lipe (Thailand)"): "gcn-b3d5523f36-shared",
    ("grab", "koh-samui", "Koh Samui (Bangrak) ↔ Don Sak Ferry Harbour"): "rn-347c44e1d360",
    ("grab", "vietnam", "Saigon (Bach Dang) ↔ Vung Tau"): "rn-00dfea36a4d9",
    ("grab", "taiwan", "Magong (Penghu) ↔ Penghu outer islands (Qimei / Wang'an)"): "ics-25ecef3e3b",
}

# Market slug aliases: partner JSON id → economics market name tokens
MARKET_ALIASES: dict[str, list[str]] = {
    "koh-samui": ["koh samui"],
    "cross-border": ["cross-border", "cross border"],
    "phuket": ["phuket"],
    "penang": ["penang", "langkawi"],
    "philippines": ["philippines"],
    "vietnam": ["vietnam"],
    "cambodia": ["cambodia"],
    "jakarta": ["jakarta"],
    "taiwan": ["taiwan"],
    "singapore": ["singapore"],
    "borneo": ["borneo"],
    "bali": ["bali"],
    "bangkok": ["bangkok"],
}


@dataclass
class FixStats:
    rebound: int = 0
    chip_scrubbed: int = 0
    chip_legs_removed: int = 0
    skipped_ok: int = 0
    no_match: int = 0
    manual: int = 0
    econ: int = 0
    by_partner: dict[str, dict[str, int]] = field(default_factory=lambda: defaultdict(lambda: defaultdict(int)))


def market_matches(econ_market: str | None, market_id: str | None) -> bool:
    if not market_id:
        return True
    if not econ_market:
        return True
    em = r.norm_label(econ_market)
    mid = r.norm_label(market_id)
    aliases = MARKET_ALIASES.get(market_id, [mid.replace("-", " ")])
    return any(a in em or em in a for a in aliases)


def is_domestic_scope(scope: str | None, market_id: str | None) -> bool:
    if market_id and market_id.lower() in CROSS_BORDER_MARKETS:
        return False
    if (scope or "").lower() in ("all", "regional", "cross", "cross-border"):
        return False
    return True


def route_is_cross_border(rec: r.RouteRec) -> bool:
    ep = f"{rec.from_label} {rec.to_label}"
    return bool(CROSS_BORDER_RE.search(ep))


def load_economics_records() -> dict[str, list[dict]]:
    path = ROOT / "data-clean/economics_by_route_id.json"
    by_partner: dict[str, list[dict]] = defaultdict(list)
    if not path.exists():
        return by_partner
    raw = r.load_json(path)
    for rec in raw.get("records") or []:
        partner = str(rec.get("partner") or "").lower()
        if partner:
            by_partner[partner].append(rec)
    return by_partner


def parse_corridor(corridor: str) -> tuple[str | None, str | None]:
    for sep in ("->", "→", "↔"):
        if sep in corridor:
            a, b = corridor.split(sep, 1)
            return a.strip(), b.strip()
    return None, None


def find_economics_route(
    item: dict,
    partner_id: str,
    market_id: str | None,
    econ_records: list[dict],
    routes: dict[str, r.RouteRec],
    promo: r.GcnPromoIndex,
) -> str | None:
    from_l, to_l, label_text = r.item_labels(item)
    if not from_l and not to_l and not item.get("label"):
        return None

    best_rid: str | None = None
    best_score = 0.0

    for rec in econ_records:
        if not market_matches(rec.get("market"), market_id):
            continue
        rid = rec.get("route_id")
        if not rid:
            continue
        promoted = r.promote_route_id(rid, partner_id, promo, routes) or rid
        route_rec = routes.get(promoted)
        if not route_rec:
            continue

        score = r.econ_corridor_score(item, promoted, partner_id, r.EconomicsIndex(
            all_ids={promoted},
            corridor_by_route={promoted: rec.get("corridor", "")},
            corridor_by_partner_route={(partner_id, promoted): rec.get("corridor", "")},
            by_partner=defaultdict(set),
        ))

        cf, ct = parse_corridor(rec.get("corridor") or "")
        if cf and ct and from_l and to_l:
            if r.directional_endpoints_match(from_l, to_l, route_rec):
                score += 20.0
            elif r.labels_match(from_l, cf) and r.labels_match(to_l, ct):
                score += 15.0

        if score > best_score and r.passes_gates(item, route_rec, label_text):
            best_score = score
            best_rid = promoted

    return best_rid if best_score >= 6.0 else None


def lookup_manual_pin(
    item: dict,
    partner_id: str,
    market_id: str | None,
    routes: dict[str, r.RouteRec],
    promo: r.GcnPromoIndex,
) -> str | None:
    from_l, to_l, _ = r.item_labels(item)
    label = item.get("label") or ""

    if from_l and to_l:
        for key_market in (market_id, None):
            key = (partner_id, key_market, from_l, to_l)
            if key in MANUAL_PINS:
                rid = MANUAL_PINS[key]
                promoted = r.promote_route_id(rid, partner_id, promo, routes) or rid
                if promoted in routes:
                    return promoted

    if label:
        for key_market in (market_id, None):
            key = (partner_id, key_market, label)
            if key in LABEL_PINS:
                rid = LABEL_PINS[key]
                promoted = r.promote_route_id(rid, partner_id, promo, routes) or rid
                if promoted in routes:
                    return promoted

    return None


def needs_rebind(
    item: dict,
    routes: dict[str, r.RouteRec],
    partner_id: str,
) -> bool:
    rid = item.get("route_id")
    if not rid or item.get("display") == "network_chip":
        return False
    rec = routes.get(rid)
    if not rec:
        return True
    from_l, to_l, label_text = r.item_labels(item)
    if from_l and to_l and not r.directional_endpoints_match(from_l, to_l, rec):
        return True
    if not r.passes_gates(item, rec, label_text):
        return True
    return False


def apply_route_pin(
    item: dict,
    rid: str,
    routes: dict[str, r.RouteRec],
    source: str,
) -> None:
    rec = routes[rid]
    item["route_id"] = rid
    item["route_ids"] = None
    if rec.distance_nm is not None:
        item["distance_nm"] = rec.distance_nm
    item["_link_kind"] = "corridor-label" if item.get("from") or item.get("label") else "corridor-node"
    item["_link_status"] = f"linked-grok-{source}"
    item["_link_source"] = f"grok/fix_market_route_bindings/{source}"


def scrub_chip_route_ids(
    item: dict,
    scope: str | None,
    market_id: str | None,
    routes: dict[str, r.RouteRec],
    stats: FixStats,
    partner_id: str,
) -> None:
    if item.get("display") != "network_chip":
        return
    rids = item.get("route_ids")
    if not rids or not is_domestic_scope(scope, market_id):
        return

    chip_label = item.get("label") or ""
    if CROSS_BORDER_RE.search(chip_label):
        return

    kept: list[str] = []
    removed = 0
    for rid in rids:
        rec = routes.get(rid)
        if rec and route_is_cross_border(rec):
            removed += 1
            continue
        kept.append(rid)

    if removed:
        item["route_ids"] = kept or None
        note = f"scrubbed {removed} cross-border legs"
        item["_bundle_note"] = f"{item.get('_bundle_note', '')}; {note}".strip("; ")
        stats.chip_scrubbed += 1
        stats.chip_legs_removed += removed
        stats.by_partner[partner_id]["chip_scrub"] += 1


def fix_item(
    item: dict,
    partner_id: str,
    market_id: str | None,
    routes: dict[str, r.RouteRec],
    econ_by_partner: dict[str, list[dict]],
    promo: r.GcnPromoIndex,
    stats: FixStats,
) -> None:
    if not isinstance(item, dict):
        return

    if item.get("display") == "network_chip":
        return

    if not item.get("route_id"):
        return

    if not needs_rebind(item, routes, partner_id):
        stats.skipped_ok += 1
        return

    rid: str | None = None
    source = ""

    rid = lookup_manual_pin(item, partner_id, market_id, routes, promo)
    if rid:
        source = "manual"
        stats.manual += 1

    if not rid:
        econ_recs = econ_by_partner.get(partner_id, [])
        rid = find_economics_route(item, partner_id, market_id, econ_recs, routes, promo)
        if rid:
            source = "economics"
            stats.econ += 1

    if rid:
        apply_route_pin(item, rid, routes, source)
        stats.rebound += 1
        stats.by_partner[partner_id][source] += 1
    else:
        stats.no_match += 1
        stats.by_partner[partner_id]["no_match"] += 1


def walk_partner(
    obj,
    partner_id: str,
    market_id: str | None,
    scope: str | None,
    routes: dict[str, r.RouteRec],
    econ_by_partner: dict[str, list[dict]],
    promo: r.GcnPromoIndex,
    stats: FixStats,
    *,
    is_root: bool = False,
):
    if isinstance(obj, dict):
        rs = obj.get("route_scope") or scope

        if is_root:
            for j in obj.get("journeys_unlocked") or []:
                if isinstance(j, dict):
                    fix_item(j, partner_id, None, routes, econ_by_partner, promo, stats)
            for ph in obj.get("phases") or []:
                if not isinstance(ph, dict):
                    continue
                ph_scope = ph.get("route_scope") or rs
                for fr in ph.get("featured_routes") or []:
                    if not isinstance(fr, dict):
                        continue
                    if fr.get("display") == "network_chip":
                        scrub_chip_route_ids(fr, ph_scope, None, routes, stats, partner_id)
                    else:
                        fix_item(fr, partner_id, None, routes, econ_by_partner, promo, stats)

        for j in obj.get("journeys_unlocked") or []:
            if not is_root and isinstance(j, dict):
                fix_item(j, partner_id, market_id, routes, econ_by_partner, promo, stats)

        if not is_root:
            for fr in obj.get("featured_routes") or []:
                if not isinstance(fr, dict):
                    continue
                if fr.get("display") == "network_chip":
                    scrub_chip_route_ids(fr, rs, market_id, routes, stats, partner_id)
                else:
                    fix_item(fr, partner_id, market_id, routes, econ_by_partner, promo, stats)

            for ph in obj.get("phases") or []:
                if not isinstance(ph, dict):
                    continue
                ph_scope = ph.get("route_scope") or rs
                for fr in ph.get("featured_routes") or []:
                    if not isinstance(fr, dict):
                        continue
                    if fr.get("display") == "network_chip":
                        scrub_chip_route_ids(fr, ph_scope, market_id, routes, stats, partner_id)
                    else:
                        fix_item(fr, partner_id, market_id, routes, econ_by_partner, promo, stats)

        for m in obj.get("markets") or []:
            mid = m.get("id") or m.get("slug")
            walk_partner(m, partner_id, mid, None, routes, econ_by_partner, promo, stats)

    elif isinstance(obj, list):
        for x in obj:
            walk_partner(x, partner_id, market_id, scope, routes, econ_by_partner, promo, stats)


def fix_partner_file(
    path: Path,
    routes: dict[str, r.RouteRec],
    econ_by_partner: dict[str, list[dict]],
    promo: r.GcnPromoIndex,
    *,
    dry_run: bool,
) -> tuple[dict, FixStats]:
    partner_id = path.stem
    data = r.load_json(path)
    original = copy.deepcopy(data)
    stats = FixStats()

    walk_partner(data, partner_id, None, None, routes, econ_by_partner, promo, stats, is_root=True)

    if not dry_run and data != original:
        r.save_json(path, data)

    return data, stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--partner", nargs="*", help="Limit to partner slug(s)")
    args = ap.parse_args()

    dry_run = not args.apply
    if args.dry_run:
        dry_run = True

    routes, routes_by_city, promo = r.load_routes(r.ROOT)
    econ_by_partner = load_economics_records()

    paths = sorted(PARTNERS_DIR.glob("*.json"))
    if args.partner:
        paths = [PARTNERS_DIR / f"{p}.json" for p in args.partner]

    all_stats: dict[str, dict] = {}
    for path in paths:
        if not path.exists() or path.suffix != ".json":
            continue
        if path.stem.endswith(".bak-pre-marine-tam-split"):
            continue
        _, stats = fix_partner_file(path, routes, econ_by_partner, promo, dry_run=dry_run)
        if any([stats.rebound, stats.chip_scrubbed, stats.no_match]):
            all_stats[path.stem] = {
                "rebound": stats.rebound,
                "manual": stats.manual,
                "economics": stats.econ,
                "chip_scrubbed": stats.chip_scrubbed,
                "chip_legs_removed": stats.chip_legs_removed,
                "skipped_ok": stats.skipped_ok,
                "no_match": stats.no_match,
            }
            print(f"{path.stem}: rebound={stats.rebound} (manual={stats.manual} econ={stats.econ}) "
                  f"chip_scrub={stats.chip_scrubbed} (-{stats.chip_legs_removed} legs) "
                  f"no_match={stats.no_match}")

    report = {
        "at": datetime.now(timezone.utc).isoformat(),
        "mode": "dry-run" if dry_run else "apply",
        "partners": all_stats,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2) + "\n")
    print(f"\nReport: {REPORT_PATH}")
    if dry_run:
        print("(dry-run — pass --apply to write)")


if __name__ == "__main__":
    main()