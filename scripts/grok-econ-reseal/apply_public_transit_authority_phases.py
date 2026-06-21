#!/usr/bin/env python3
"""Apply public_transit_authority phase taxonomy — intra home first, inter-city, then cross-border."""
from __future__ import annotations

import copy
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARCHETYPE = ROOT / "handoff" / "partner-map-model" / "public-transit-authority-archetype.json"
PARTNERS = ROOT / "partner-pitch" / "partners"
DC_PARTNERS = ROOT / "data-clean" / "partners"
REPORT = ROOT / "handoff" / "partner-map-model" / "public-transit-authority-apply-report.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path):
    return json.loads(path.read_text())


def save_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def load_gold() -> tuple[set[str], dict[str, dict]]:
    routes = load_json(ROOT / "data-clean" / "ROUTES.json")
    ids: set[str] = set()
    by_id: dict[str, dict] = {}
    for f in routes:
        p = f.get("properties") or {}
        rid = p.get("id")
        if rid:
            ids.add(rid)
            by_id[rid] = p
    return ids, by_id


DUBAI_HINTS = ("dubai", "deira", "ghubaiba", "marina", "palm", "creek", "harbour", "bluewaters", "jumeirah")
ABU_DHABI_HINTS = ("yas", "saadiyat", "corniche", "maryah", "abu dhabi", "hidd", "jubail", "nurai")
SINGAPORE_HINTS = ("singapore", "marina bay", "sentosa", "jurong", "tanah merah", "east coast")


def bp_parent_index() -> dict[str, str]:
    fbt = load_json(ROOT / "data-clean" / "FEATURES_BY_TYPE.json")
    out: dict[str, str] = {}
    for f in fbt.get("poi") or []:
        p = f.get("properties") or {}
        if p.get("id") and p.get("parent_city_id"):
            out[p["id"]] = p["parent_city_id"]
    return out


def resolve_city(node_id: str | None, bp_idx: dict[str, str]) -> str | None:
    if not node_id:
        return None
    if "__" in node_id:
        return node_id.split("__", 1)[0]
    if node_id in bp_idx:
        return bp_idx[node_id]
    if "-" in node_id and not node_id.startswith("bp-"):
        return node_id
    return bp_idx.get(node_id)


def label_city_hint(label: str, home: set[str]) -> str | None:
    blob = (label or "").lower()
    if "dubai-uae" in home and any(h in blob for h in DUBAI_HINTS):
        return "dubai-uae"
    if "abu-dhabi-uae" in home and any(h in blob for h in ABU_DHABI_HINTS):
        return "abu-dhabi-uae"
    if "singapore" in home and any(h in blob for h in SINGAPORE_HINTS):
        return "singapore"
    if "ras-al-khaimah-uae" in home and ("rak" in blob or "ras al khaimah" in blob or "marjan" in blob):
        return "ras-al-khaimah-uae"
    return None


def cities_for_card(card: dict, bp_idx: dict[str, str], gold_by_id: dict[str, dict], home: set[str]) -> tuple[str | None, str | None]:
    rid = card.get("route_id") or ((card.get("route_ids") or [None])[0])
    if rid and rid in gold_by_id:
        p = gold_by_id[rid]
        return p.get("from_city_id") or p.get("from"), p.get("to_city_id") or p.get("to")
    fc = resolve_city(card.get("from_node_id"), bp_idx)
    tc = resolve_city(card.get("to_node_id"), bp_idx)
    hint = label_city_hint(card.get("label", ""), home)
    if hint:
        if fc not in home and tc in home:
            fc = hint
        elif tc not in home and fc in home:
            tc = hint
        elif fc == tc and fc not in home:
            fc = tc = hint
    return fc, tc


def classify_card(
    card: dict,
    *,
    home: set[str],
    domestic: set[str],
    cross_border: set[str],
    bp_idx: dict[str, str],
    gold_by_id: dict[str, dict],
) -> str:
    fc, tc = cities_for_card(card, bp_idx, gold_by_id, home)
    if not fc or not tc:
        return "unknown"
    if fc in home and tc in home:
        return "intra"
    pair = {fc, tc}
    if pair <= domestic and pair & home:
        return "inter_city"
    if pair & home and (pair & cross_border):
        return "cross_border_roadmap"
    if card.get("render") == "roadmap-amber-dashed" or card.get("economics_status") == "roadmap_excluded":
        return "cross_border_roadmap"
    if card.get("platform") == "Quanta-LR" and (fc in cross_border or tc in cross_border):
        return "cross_border_roadmap"
    return "other"


def card_key(card: dict) -> str:
    rid = card.get("route_id") or (card.get("route_ids") or [None])[0]
    return rid or f"{card.get('from_node_id')}|{card.get('to_node_id')}|{card.get('label')}"


def make_card(spec: dict, gold: set[str]) -> dict | None:
    rid = spec.get("route_id")
    if rid and rid not in gold:
        return None
    out = {
        "label": spec["label"],
        "from_node_id": spec.get("from_node_id"),
        "to_node_id": spec.get("to_node_id"),
        "distance_nm": spec.get("distance_nm"),
        "platform": spec.get("platform", "Pioneer II"),
        "route_id": rid,
        "route_ids": [rid] if rid else None,
        "_link_kind": "authority-archetype",
        "_link_status": "linked-grok-scoped" if rid else "held-null-with-reason",
        "_link_source": "grok/apply_public_transit_authority_phases",
        "economics_status": spec.get("economics_status", "economics_pending"),
    }
    if spec.get("render"):
        out["render"] = spec["render"]
    if spec.get("from_label"):
        out["from_label"] = spec["from_label"]
    if spec.get("to_label"):
        out["to_label"] = spec["to_label"]
    return out


def collect_cards(doc: dict) -> list[dict]:
    seen: set[str] = set()
    out: list[dict] = []
    for ph in doc.get("phases") or []:
        for fr in ph.get("featured_routes") or []:
            k = card_key(fr)
            if k in seen:
                continue
            seen.add(k)
            out.append(copy.deepcopy(fr))
    return out


def tier_for_n(n: int, cfg: dict, archetype: dict) -> str:
    tier_map = cfg.get("tier_map") or {}
    if str(n) in tier_map:
        return tier_map[str(n)]
    defaults = {t["n"]: t["tier"] for t in archetype.get("phase_tiers") or []}
    return defaults.get(n, "intra_pilot")


def phase_cities(tier: str, home: list[str], cards: list[dict], bp_idx: dict[str, str]) -> list[str]:
    if tier in ("intra_pilot", "intra_scale"):
        return home
    cities = set(home)
    for c in cards:
        for nid in (c.get("from_node_id"), c.get("to_node_id")):
            cid = resolve_city(nid, bp_idx)
            if cid:
                cities.add(cid)
    return sorted(cities)


def apply_partner(slug: str, cfg: dict, archetype: dict, gold: set[str], gold_by_id: dict[str, dict], bp_idx: dict[str, str]) -> dict:
    path = PARTNERS / f"{slug}.json"
    if not path.exists():
        return {"partner": slug, "skipped": "missing file"}

    doc = load_json(path)
    home = set(cfg.get("home_cities") or [])
    domestic = set(cfg.get("domestic_city_ids") or []) | home
    cross_border = set(cfg.get("cross_border_city_ids") or [])

    buckets: dict[str, list[dict]] = {
        "intra_pilot": [],
        "intra_scale": [],
        "inter_city": [],
        "cross_border_roadmap": [],
    }

    for card in collect_cards(doc):
        tier = classify_card(
            card, home=home, domestic=domestic, cross_border=cross_border, bp_idx=bp_idx, gold_by_id=gold_by_id
        )
        if tier == "intra":
            # Split: shorter/distinct pilot vs scale by distance
            dist = card.get("distance_nm") or 999
            if dist <= 15 and len(buckets["intra_pilot"]) < 4:
                buckets["intra_pilot"].append(card)
            else:
                buckets["intra_scale"].append(card)
        elif tier in buckets:
            buckets[tier].append(card)

    supplements = cfg.get("supplement_routes") or {}
    for tier, specs in supplements.items():
        for spec in specs:
            c = make_card(spec, gold)
            if not c:
                continue
            keys = {card_key(x) for x in buckets.get(tier, [])}
            if card_key(c) not in keys:
                buckets.setdefault(tier, []).append(c)

    def pair_key(card: dict) -> str | None:
        fc, tc = cities_for_card(card, bp_idx, gold_by_id, home)
        if not fc or not tc:
            return None
        return "|".join(sorted([fc, tc]))

    # Dedupe buckets by route_id; inter/cross-border also dedupe by city-pair (keep shortest distance)
    for tier in buckets:
        seen_rid: set[str] = set()
        by_pair: dict[str, dict] = {}
        deduped = []
        for c in buckets[tier]:
            k = card_key(c)
            if k in seen_rid:
                continue
            seen_rid.add(k)
            if tier in ("inter_city", "cross_border_roadmap"):
                pk = pair_key(c)
                if pk:
                    prev = by_pair.get(pk)
                    if prev and (prev.get("distance_nm") or 999) <= (c.get("distance_nm") or 999):
                        continue
                    if prev:
                        deduped = [x for x in deduped if pair_key(x) != pk]
                    by_pair[pk] = c
            deduped.append(c)
        buckets[tier] = deduped

    old_phases = {ph.get("n"): ph for ph in doc.get("phases") or []}
    phase_count = cfg.get("phase_count") or 4
    labels = cfg.get("phase_labels") or {}
    tier_by_n = archetype.get("phase_tiers") or []
    tier_defaults = {t["n"]: t for t in tier_by_n}

    # Three-phase authorities (e.g. RAKTA): collapse intra pilot + scale into phase 1.
    if phase_count == 3:
        buckets["intra_pilot"] = buckets["intra_pilot"] + buckets["intra_scale"]
        buckets["intra_scale"] = []

    new_phases = []
    for n in range(1, phase_count + 1):
        tier = tier_for_n(n, cfg, archetype)
        old = old_phases.get(n, {})
        tdef = tier_defaults.get(n, {})
        cards = buckets.get(tier, [])
        if tier == "intra_pilot" and not cards:
            cards = buckets.get("intra_scale", [])[:2]
        if tier == "intra_pilot" and phase_count == 3:
            cards = buckets.get("intra_pilot", [])

        phase = copy.deepcopy(old) if old else {}
        phase["n"] = n
        phase["label"] = labels.get(str(n)) or old.get("label") or tdef.get("label_pattern", f"Phase {n}")
        phase["route_scope"] = tdef.get("route_scope", "intra" if tier.startswith("intra") else "inter")
        phase["cities"] = phase_cities(tier, list(home), cards, bp_idx)
        phase["featured_routes"] = cards
        phase["_authority_phase_tier"] = tier
        phase["rationale"] = tdef.get("rationale") or old.get("rationale")
        new_phases.append(phase)

    doc["phases"] = new_phases
    doc["archetype"] = "public_transit"
    doc["category"] = doc.get("category") or "transit_authority"
    doc["_public_transit_authority"] = {
        "archetype_id": archetype.get("archetype_id"),
        "applied_at": utc_now(),
        "home_cities": sorted(home),
        "phase_tiers": [p["_authority_phase_tier"] for p in new_phases],
    }

    es = doc.setdefault("end_state", {})
    es["end_state_cities"] = sorted(
        set(es.get("end_state_cities") or []) | home | domestic | cross_border
    )

    for out in (path, DC_PARTNERS / f"{slug}.json"):
        save_json(out, doc)

    counts = {t: len(buckets.get(t, [])) for t in buckets}
    return {"partner": slug, "phase_tiers": [p["_authority_phase_tier"] for p in new_phases], "route_counts": counts}


def main() -> int:
    archetype = load_json(ARCHETYPE)
    gold, gold_by_id = load_gold()
    bp_idx = bp_parent_index()
    results = {"at": utc_now(), "lane": "grok/apply_public_transit_authority_phases", "partners": []}

    targets = sys.argv[1:] if len(sys.argv) > 1 else list((archetype.get("partners") or {}).keys())
    for slug in targets:
        cfg = (archetype.get("partners") or {}).get(slug)
        if not cfg:
            results["partners"].append({"partner": slug, "skipped": "not in archetype config"})
            continue
        results["partners"].append(apply_partner(slug, cfg, archetype, gold, gold_by_id, bp_idx))

    save_json(REPORT, results)
    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())