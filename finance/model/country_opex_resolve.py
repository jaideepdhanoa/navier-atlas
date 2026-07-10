#!/usr/bin/env python3
"""
Country → opex-country resolution for corridors / aggregate / transparent sheets.

Rules (2026-07-10):
  1. Exact key in country-reference.countries → use it (honest).
  2. Known dual-leg / composite labels → origin-primary (or explicit map).
  3. CrossBorder / unknown → R16 home-port default (Singapore) ONLY as last resort,
     and ALWAYS emit a resolution record so sheets/lints can fail-loud.

Null beats wrong for *rates*; fallback is allowed only as a labeled process default
so Tasklet / Grok never ships a silent Singapore opex surprise again.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Iterable, Optional

# R16: vessel home-port opex when country is cross-border or missing from cref.
CROSS_BORDER_HOMEPORT = "Singapore"

# Composite / legacy labels → durable country-reference keys.
# Dual-leg: origin-primary for single VLOOKUP; counterpart noted for honesty.
COUNTRY_ALIASES: dict[str, dict[str, Any]] = {
    "USVI / BVI": {
        "opex_country": "U.S. Virgin Islands",
        "policy": "dual_leg_origin_primary",
        "counterpart": "British Virgin Islands",
        "note": (
            "St. Thomas (USVI) → Tortola (BVI). Opex VLOOKUP uses origin "
            "(U.S. Virgin Islands); BVI also in country-reference for dual-leg review."
        ),
    },
    "USVI/BVI": {
        "opex_country": "U.S. Virgin Islands",
        "policy": "dual_leg_origin_primary",
        "counterpart": "British Virgin Islands",
        "note": "Alias of USVI / BVI.",
    },
    "CrossBorder": {
        "opex_country": CROSS_BORDER_HOMEPORT,
        "policy": "cross_border_r16_homeport",
        "note": (
            "Legacy CrossBorder label. R16 home-port opex = Singapore. "
            "Prefer rewriting corridor.country to the vessel home-port (or origin) "
            "when known; keep _country_opex_policy metadata for dual-leg review."
        ),
    },
}

# Optional display / spelling variants → cref keys (only when destination exists).
SPELLING_ALIASES: dict[str, str] = {
    "USA": "United States",
    "United States of America": "United States",
    "US Virgin Islands": "U.S. Virgin Islands",
    "U.S. Virgin Island": "U.S. Virgin Islands",
    "Korea": "South Korea",  # only helps once South Korea is sealed in cref
    "Republic of Korea": "South Korea",
    "ROK": "South Korea",
}


@dataclass
class OpexCountryResolution:
    raw_country: Optional[str]
    opex_country: str
    in_reference: bool
    used_fallback: bool
    policy: str
    note: str
    counterpart: Optional[str] = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def resolve_opex_country(
    raw_country: Optional[str],
    cref_countries: dict,
    *,
    homeport: str = CROSS_BORDER_HOMEPORT,
) -> OpexCountryResolution:
    """Map a corridor country string to a country-reference key for opex VLOOKUP."""
    raw = (raw_country or "").strip() or None

    if raw and raw in cref_countries:
        return OpexCountryResolution(
            raw_country=raw,
            opex_country=raw,
            in_reference=True,
            used_fallback=False,
            policy="exact",
            note="Exact country-reference match.",
        )

    if raw and raw in COUNTRY_ALIASES:
        spec = COUNTRY_ALIASES[raw]
        target = spec["opex_country"]
        in_ref = target in cref_countries
        if not in_ref:
            # Alias target missing — fall through to homeport with loud meta.
            return OpexCountryResolution(
                raw_country=raw,
                opex_country=homeport if homeport in cref_countries else target,
                in_reference=homeport in cref_countries,
                used_fallback=True,
                policy=f"alias_target_missing→{spec['policy']}",
                note=spec.get("note", "") + f" Alias target {target!r} not in country-reference.",
                counterpart=spec.get("counterpart"),
            )
        return OpexCountryResolution(
            raw_country=raw,
            opex_country=target,
            in_reference=True,
            used_fallback=False,
            policy=spec["policy"],
            note=spec.get("note", ""),
            counterpart=spec.get("counterpart"),
        )

    if raw and raw in SPELLING_ALIASES:
        target = SPELLING_ALIASES[raw]
        if target in cref_countries:
            return OpexCountryResolution(
                raw_country=raw,
                opex_country=target,
                in_reference=True,
                used_fallback=False,
                policy="spelling_alias",
                note=f"Spelling alias {raw!r} → {target!r}.",
            )

    # True missing / null → R16 homeport (labeled fallback).
    hp = homeport if homeport in cref_countries else (
        next(iter(cref_countries.keys())) if cref_countries else "Singapore"
    )
    return OpexCountryResolution(
        raw_country=raw,
        opex_country=hp,
        in_reference=False,
        used_fallback=True,
        policy="r16_homeport_fallback",
        note=(
            f"Country {raw!r} not in country-reference; using R16 home-port opex "
            f"{hp!r}. Source + seal real rates before partner sheet rebuild."
        ),
    )


def scan_corridors_missing(
    markets: dict,
    cref_countries: dict,
) -> list[dict[str, Any]]:
    """Return unique missing/fallback country hits across markets."""
    hits: dict[tuple, dict] = {}
    for mid, mk in (markets or {}).items():
        if not isinstance(mk, dict):
            continue
        partner = mk.get("partner")
        for c in mk.get("corridors") or []:
            if not isinstance(c, dict):
                continue
            res = resolve_opex_country(c.get("country"), cref_countries)
            if res.used_fallback or not res.in_reference:
                key = (res.raw_country, res.opex_country, res.policy)
                if key not in hits:
                    hits[key] = {
                        **res.as_dict(),
                        "n_corridors": 0,
                        "markets": set(),
                        "partners": set(),
                    }
                hits[key]["n_corridors"] += 1
                hits[key]["markets"].add(mid)
                if partner:
                    hits[key]["partners"].add(partner)
    out = []
    for h in hits.values():
        h["markets"] = sorted(h["markets"])
        h["partners"] = sorted(h["partners"])
        out.append(h)
    out.sort(key=lambda x: (-x["n_corridors"], x.get("raw_country") or ""))
    return out


def format_fallback_banner(resolutions: Iterable[OpexCountryResolution]) -> str:
    """Human-readable banner for sheet Read-me / stderr."""
    bad = [r for r in resolutions if r.used_fallback]
    if not bad:
        return ""
    lines = [
        "⚠ COUNTRY OPEX FALLBACK — some corridors use R16 Singapore (or home-port) "
        "opex because country-reference is missing a real country row. "
        "Do not treat energy/crew/berth as locally grounded until Tasklet seals rates.",
        "",
    ]
    seen = set()
    for r in bad:
        k = (r.raw_country, r.opex_country)
        if k in seen:
            continue
        seen.add(k)
        lines.append(
            f"  • raw={r.raw_country!r} → opex_country={r.opex_country!r} "
            f"policy={r.policy}"
        )
    return "\n".join(lines)
