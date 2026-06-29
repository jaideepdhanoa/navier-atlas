#!/usr/bin/env python3
"""Normalize schema enums: boats (int|null), route_scope (enum), cross_border spelling."""
from __future__ import annotations

import argparse
import copy
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data-clean" / "partners"
PITCH = ROOT / "partner-pitch" / "partners"

SCOPE_MAP = {
    "intra": "intra",
    "inter": "inter",
    "intercity": "intercity",
    "network": "network",
    "all": "all",
    "cross_border": "cross_border",
    "cross-border": "cross_border",
    "regional": "regional",
}

SCOPE_HEURISTICS = [
    (re.compile(r"cross.?gulf|cross.?border|doha|bahrain|oman|qatar", re.I), "cross_border"),
    (re.compile(r"mesh|network|full|integrated|seaboard", re.I), "network"),
    (re.compile(r"gateway|bangkok|pattaya|inter.?city", re.I), "intercity"),
    (re.compile(r"coastal|intra|palm|marina|creek|river|basin|frond", re.I), "intra"),
]


def normalize_boats(val) -> int | None:
    if val is None:
        return None
    if isinstance(val, int):
        return val
    if isinstance(val, float):
        return int(val)
    s = str(val).strip().lower()
    if "roadmap" in s or "pending" in s or "tbd" in s:
        return None
    m = re.search(r"(\d+)", s)
    if m:
        return int(m.group(1))
    return None


def normalize_scope(val) -> str:
    if not val:
        return "intra"
    s = str(val).strip()
    if s in SCOPE_MAP:
        return SCOPE_MAP[s]
    for pat, scope in SCOPE_HEURISTICS:
        if pat.search(s):
            return scope
    return "intra"


def normalize_phase(ph: dict) -> dict:
    ph = copy.deepcopy(ph)
    if "boats" in ph:
        ph["boats"] = normalize_boats(ph.get("boats"))
    if "route_scope" in ph:
        ph["route_scope"] = normalize_scope(ph.get("route_scope"))
    for fr in ph.get("featured_routes") or []:
        if isinstance(fr.get("boats"), str):
            fr["boats"] = normalize_boats(fr.get("boats"))
    return ph


def scaffold_market_phases(market: dict, template_phases: list) -> list:
    """Mirror top-level phase scaffold into a market missing phases."""
    out = []
    for tpl in template_phases[:3]:
        ph = copy.deepcopy(tpl)
        ph.pop("featured_routes", None)
        ph["featured_routes"] = []
        ph["narrative"] = ph.get("narrative") or f"{market.get('label', market.get('id'))} — {ph.get('label', 'phase')}"
        out.append(ph)
    return out


def normalize_featured(fr: dict) -> dict:
    fr = copy.deepcopy(fr)
    if fr.get("model_link") is None:
        fr.pop("model_link", None)
    fr.pop("from", None)
    fr.pop("to", None)
    if "label" not in fr and fr.get("from_node_id") and fr.get("to_node_id"):
        fr["label"] = f"{fr['from_node_id']} → {fr['to_node_id']}"
    if "from_label" not in fr and fr.get("from_node_id"):
        fr["from_label"] = fr["from_node_id"]
    if "to_label" not in fr and fr.get("to_node_id"):
        fr["to_label"] = fr["to_node_id"]
    return fr


def normalize_the_ask(val):
    if isinstance(val, list):
        return " · ".join(str(x) for x in val if x)
    return val


def normalize_doc(doc: dict, *, partner_id: str) -> tuple[dict, int]:
    doc = copy.deepcopy(doc)
    changes = 0
    top_phases = doc.get("phases") or []

    if doc.get("the_ask") is not None:
        na = normalize_the_ask(doc["the_ask"])
        if na != doc["the_ask"]:
            doc["the_ask"] = na
            changes += 1

    if doc.get("phases"):
        new_phases = []
        for ph in doc["phases"]:
            np = normalize_phase(ph)
            if np != ph:
                changes += 1
            new_phases.append(np)
        doc["phases"] = new_phases

    for m in doc.get("markets") or []:
        if m.get("the_ask") is not None:
            na = normalize_the_ask(m["the_ask"])
            if na != m["the_ask"]:
                m["the_ask"] = na
                changes += 1
        if partner_id == "centara-thailand" and not m.get("phases") and top_phases:
            m["phases"] = scaffold_market_phases(m, top_phases)
            changes += 1
        if not m.get("phases"):
            continue
        new_mph = []
        for ph in m["phases"]:
            np = normalize_phase(ph)
            frs = []
            for fr in np.get("featured_routes") or []:
                nfr = normalize_featured(fr)
                if nfr != fr:
                    changes += 1
                frs.append(nfr)
            np["featured_routes"] = frs
            if np != ph:
                changes += 1
            new_mph.append(np)
        m["phases"] = new_mph

    return doc, changes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--partner", nargs="*")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    targets = {
        "airasia-move", "centara-thailand", "grab-thailand",
        "line-man-wongnai", "ocean-whisperer",
    }
    if args.partner:
        targets = set(args.partner)

    total = 0
    for slug in sorted(targets):
        for base in (DATA, PITCH):
            path = base / f"{slug}.json"
            if not path.exists():
                continue
            doc = json.loads(path.read_text())
            new_doc, n = normalize_doc(doc, partner_id=slug)
            total += n
            print(f"{path.relative_to(ROOT)}: {n} normalizations")
            if args.apply and n:
                path.write_text(json.dumps(new_doc, indent=2, ensure_ascii=False) + "\n")

    print(f"total changes: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())