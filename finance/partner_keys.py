"""Canonical partner slug alignment between Atlas/sheets and the finance engine."""

from __future__ import annotations

# Atlas slug (PARTNER-SHEET-IDS, economics_url_map, data-clean/partners) → engine slug
# (corridors.json market.partner, aggregate.py --partner).
ENGINE_PARTNER: dict[str, str] = {
    "saudi-pif": "saudi-redsea-pif",
}

_SHEET_BY_ENGINE = {v: k for k, v in ENGINE_PARTNER.items()}


def engine_partner(sheet_partner: str) -> str:
    return ENGINE_PARTNER.get(sheet_partner, sheet_partner)


def sheet_partner(engine_key: str) -> str:
    return _SHEET_BY_ENGINE.get(engine_key, engine_key)