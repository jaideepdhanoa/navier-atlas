#!/usr/bin/env python3
"""Resolve partner proposal class (authority / hospitality / hub / standalone)."""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLASSES_PATH = ROOT / "handoff" / "partner-map-model" / "partner-proposal-classes.json"
MANIFEST_PATH = ROOT / "handoff" / "partner-map-model" / "regional-inheritance-manifest.json"


@lru_cache(maxsize=1)
def load_classes() -> dict:
    doc = json.loads(CLASSES_PATH.read_text())
    by_partner: dict[str, str] = {}
    cfg_by_class: dict[str, dict] = {}
    overrides: dict[str, str] = {}
    for class_id, block in (doc.get("classes") or {}).items():
        cfg_by_class[class_id] = block.get("audit") or {}
        for p in block.get("partners") or []:
            by_partner[p] = class_id
        for p, ref in (block.get("spine_reference_override") or {}).items():
            overrides[p] = ref
    return {
        "by_partner": by_partner,
        "cfg_by_class": cfg_by_class,
        "spine_reference_override": overrides,
        "raw": doc,
    }


def proposal_class(slug: str, doc: dict | None = None) -> str:
    data = load_classes()
    if slug in data["by_partner"]:
        return data["by_partner"][slug]
    if doc:
        if doc.get("layout") == "hub":
            return "hub"
        if doc.get("archetype") in ("public_transit",) or doc.get("category", "").lower().find("authority") >= 0:
            return "authority"
        if doc.get("archetype") in ("hospitality", "resort", "luxury"):
            return "hospitality"
    return "standalone"


def audit_rules(slug: str, doc: dict | None = None) -> dict:
    data = load_classes()
    cls = proposal_class(slug, doc)
    rules = dict(data["cfg_by_class"].get("standalone") or {})
    rules.update(data["cfg_by_class"].get(cls) or {})
    overrides = rules.pop("thin_map_threshold_overrides", None) or {}
    if slug in overrides:
        rules["thin_map_threshold"] = overrides[slug]
    rules["proposal_class"] = cls
    return rules


def spine_reference_override(slug: str) -> str | None:
    return load_classes()["spine_reference_override"].get(slug)


def market_has_featured(doc: dict) -> bool:
    for m in doc.get("markets") or []:
        for ph in m.get("phases") or []:
            if ph.get("featured_routes"):
                return True
        if m.get("sealed_corridor_pool"):
            return True
    return False