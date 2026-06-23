#!/usr/bin/env python3
"""Backfill empty phase featured_routes[] from featured_legs[] or linked journeys.

Matches phase featured_legs prose to journeys_unlocked by corridor label, then
falls back to phase-city-scoped journey promotion for hub partner-level phases.

Usage:
  python3 scripts/backfill_phase_featured_routes.py --audit
  python3 scripts/backfill_phase_featured_routes.py --apply --partner grab-thailand
  python3 scripts/backfill_phase_featured_routes.py --apply
"""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTNERS_DC = ROOT / "data-clean" / "partners"
PARTNERS_PITCH = ROOT / "partner-pitch" / "partners"
ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"

_LEG_SPLIT = re.compile(r"\s*(?:<->|↔|—|–|-|→|to)\s*", re.I)
_ASPIRATIONAL_LEG = re.compile(r"aspirational|roadmap|gateway\s*—|quanta-lr\s+gateway", re.I)
_LABEL_STOP = frozenset({"the", "and", "of", "to", "from", "via", "with", "for", "into", "near", "off"})


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def norm_label(s: str | None) -> str:
    if not s:
        return ""
    s = _strip_accents(s.lower().strip())
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _tokens(s: str | None) -> set[str]:
    return {t for t in norm_label(s).split() if t and t not in _LABEL_STOP}


def parse_leg(leg: str) -> tuple[str, str]:
    parts = _LEG_SPLIT.split(leg.strip(), maxsplit=1)
    if len(parts) == 2:
        return norm_label(parts[0]), norm_label(parts[1])
    return norm_label(leg), ""


def journey_endpoints(j: dict) -> tuple[str, str]:
    return norm_label(j.get("from") or j.get("title")), norm_label(j.get("to"))


def leg_matches_journey(leg: str, j: dict) -> bool:
    leg_from, leg_to = parse_leg(leg)
    j_from, j_to = journey_endpoints(j)
    if leg_from and leg_to and leg_from == j_from and leg_to == j_to:
        return True
    if leg_from and leg_to:
        # Fuzzy: leg tokens must appear in journey endpoints (handles shorthand legs).
        lf, lt = _tokens(leg_from), _tokens(leg_to)
        jf, jt = _tokens(j_from), _tokens(j_to)
        if lf and lt and lf <= jf and lt <= jt:
            return True
        if lf and lt and lf <= jt and lt <= jf:
            return True
    if leg_from and not leg_to and leg_from in (j_from, j_to):
        return True
    return norm_label(leg) in (j_from, j_to, f"{j_from} {j_to}", f"{j_to} {j_from}")


def load_route_ids() -> set[str]:
    raw = json.loads(ROUTES_PATH.read_text())
    feats = raw if isinstance(raw, list) else raw.get("features", [])
    return {f.get("properties", f).get("id") for f in feats if f.get("properties", f).get("id")}


def aspirational_leg_to_featured(leg: str, ph: dict) -> dict:
    cities = ph.get("cities") or []
    return {
        "label": leg,
        "from_node_id": cities[0] if cities else None,
        "to_node_id": cities[0] if cities else None,
        "platform": ph.get("vessel", "Quanta-LR").split("+")[0].strip() or "Quanta-LR",
        "display": "text_only",
        "_link_status": "aspirational-no-built-route",
        "_link_kind": "backfill-aspirational-leg",
        "_link_source": "grok/backfill_phase_featured_routes",
        "economics_status": "roadmap_excluded",
        "render": "roadmap-amber-dashed",
    }


def journey_to_featured(j: dict, *, leg: str | None = None) -> dict:
    label = leg or f"{j.get('from', '')} ↔ {j.get('to', '')}".strip(" ↔")
    rid = j.get("route_id")
    row = {
        "label": label,
        "from_node_id": j.get("from_node_id"),
        "to_node_id": j.get("to_node_id"),
        "distance_nm": j.get("distance_nm"),
        "platform": j.get("platform", "Pioneer II"),
        "route_id": rid,
        "_link_kind": "backfill-from-journey",
        "_link_status": j.get("_link_status", "linked-grok-scoped"),
        "_link_source": "grok/backfill_phase_featured_routes",
        "economics_status": j.get("economics_status", "economics_pending"),
    }
    if rid:
        row["route_ids"] = [rid]
    if j.get("display") == "text_only" or j.get("_link_status") == "unlinked-intra-city":
        row["display"] = "text_only"
        row["_link_status"] = "unlinked-intra-city"
    return row


def linked_journeys(journeys: list[dict]) -> list[dict]:
    out = []
    for j in journeys:
        if not isinstance(j, dict):
            continue
        if j.get("route_id") or j.get("_link_status") == "unlinked-intra-city":
            out.append(j)
    return out


def backfill_phases_in_container(
    container: dict,
    journeys: list[dict],
    route_ids: set[str],
    *,
    city_filter: set[str] | None = None,
    force: bool = False,
) -> int:
    added = 0
    pool = linked_journeys(journeys)
    if city_filter:
        pool = [
            j for j in pool
            if (j.get("from_node_id") in city_filter or j.get("to_node_id") in city_filter)
        ]
    used_rids: set[str] = set()

    for ph in container.get("phases") or []:
        if not isinstance(ph, dict) or ph.get("aspirational"):
            continue
        existing = [fr for fr in (ph.get("featured_routes") or []) if isinstance(fr, dict)]
        if existing and not force:
            used_rids.update(fr.get("route_id") for fr in existing if fr.get("route_id"))
            continue

        frs: list[dict] = []
        legs = ph.get("featured_legs") or []

        for leg in legs:
            if not isinstance(leg, str):
                continue
            if _ASPIRATIONAL_LEG.search(leg):
                frs.append(aspirational_leg_to_featured(leg, ph))
                added += 1
                continue
            matched = None
            for j in pool:
                if leg_matches_journey(leg, j):
                    matched = j
                    break
            if not matched:
                continue
            rid = matched.get("route_id")
            if rid and rid in used_rids:
                continue
            fr = journey_to_featured(matched, leg=leg)
            if rid and rid not in route_ids:
                continue
            frs.append(fr)
            if rid:
                used_rids.add(rid)
            added += 1

        if not frs and pool and not any(
            isinstance(leg, str) and _ASPIRATIONAL_LEG.search(leg) for leg in legs
        ):
            for j in sorted(pool, key=lambda x: x.get("distance_nm") or 999):
                rid = j.get("route_id")
                if rid and rid in used_rids:
                    continue
                if rid and rid not in route_ids:
                    continue
                frs.append(journey_to_featured(j))
                if rid:
                    used_rids.add(rid)
                added += 1
                if len(frs) >= len(legs) or len(frs) >= 3:
                    break

        if frs:
            ph["featured_routes"] = frs

    return added


def backfill_partner(doc: dict, route_ids: set[str], *, force: bool = False) -> int:
    added = 0

    for market in doc.get("markets") or []:
        if not isinstance(market, dict):
            continue
        added += backfill_phases_in_container(
            market,
            market.get("journeys_unlocked") or [],
            route_ids,
            force=force,
        )

    if doc.get("layout") == "hub":
        pool: list[dict] = []
        for market in doc.get("markets") or []:
            pool.extend(linked_journeys(market.get("journeys_unlocked") or []))
        for ph in doc.get("phases") or []:
            if not isinstance(ph, dict) or ph.get("aspirational"):
                continue
            if ph.get("featured_routes"):
                continue
            cities = set(ph.get("cities") or [])
            scoped = [
                j for j in pool
                if not cities
                or j.get("from_node_id") in cities
                or j.get("to_node_id") in cities
            ]
            added += backfill_phases_in_container(
                {"phases": [ph]},
                scoped,
                route_ids,
                city_filter=cities or None,
                force=force,
            )
    else:
        added += backfill_phases_in_container(
            doc,
            doc.get("journeys_unlocked") or [],
            route_ids,
            force=force,
        )

    return added


def write_partner(slug: str, doc: dict) -> None:
    text = json.dumps(doc, indent=2, ensure_ascii=False) + "\n"
    (PARTNERS_DC / f"{slug}.json").write_text(text)
    pitch = PARTNERS_PITCH / f"{slug}.json"
    if pitch.exists():
        pitch.write_text(text)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--audit", action="store_true")
    ap.add_argument("--partner", nargs="*")
    ap.add_argument("--force", action="store_true", help="Replace existing featured_routes")
    args = ap.parse_args()

    if not args.apply and not args.audit:
        args.audit = True

    route_ids = load_route_ids()
    files = sorted(PARTNERS_DC.glob("*.json"))
    if args.partner:
        want = set(args.partner)
        files = [f for f in files if f.stem in want]

    report = {"at": utc_now(), "mode": "apply" if args.apply else "audit", "partners": []}
    total = 0

    for path in files:
        slug = path.stem
        if slug.startswith("_"):
            continue
        doc = json.loads(path.read_text())
        before = deepcopy(doc)
        n = backfill_partner(doc, route_ids, force=args.force)
        total += n
        row = {"partner": slug, "would_add": n}
        if args.apply and n:
            write_partner(slug, doc)
            row["applied"] = n
        report["partners"].append(row)

    report["total_featured_added"] = total
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())