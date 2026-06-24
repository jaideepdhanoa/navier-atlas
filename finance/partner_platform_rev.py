#!/usr/bin/env python3
"""Whether a partner proposal shows super-app platform-revenue ladder rungs."""
from __future__ import annotations

from typing import Any

# Partner platform revenue = super-app / ride-hail commission on journey GMV.
# Hospitality, destination-region, sovereign, transit-authority, and corporate proposals
# show Navier transport + journey wallet only — never platform take.
PLATFORM_REV_ARCHETYPES = frozenset({"super_app", "ridehail"})


def shows_platform_revenue(partner: dict[str, Any] | None = None, *, archetype: str | None = None) -> bool:
    arch = (archetype or (partner or {}).get("archetype") or "").strip().lower()
    return arch in PLATFORM_REV_ARCHETYPES


def strip_growth_case_platform(gc: dict[str, Any]) -> dict[str, Any]:
    """Remove platform-revenue surfaces from a growth_case block (in place)."""
    if not gc:
        return gc

    rp = gc.get("revenue_potential") or {}
    rungs = [r for r in (rp.get("rungs") or []) if r.get("id") != "platform_rev"]
    rp["rungs"] = rungs
    rp.pop("ceiling_sibling", None)
    if rp.get("modal_lead"):
        rp["modal_lead"] = (
            "We start from grounded corridor demand. Each step adds one realistic expansion "
            "lever — network width, induced demand, and journey wallet."
        )
    legend = rp.get("whose_money_legend") or {}
    legend.pop("platform_take", None)
    rp["whose_money_legend"] = legend
    gc["revenue_potential"] = rp

    gc["ladder_transitions"] = [
        t
        for t in (gc.get("ladder_transitions") or [])
        if t.get("to_rung_id") != "platform_rev" and t.get("from_rung_id") != "platform_rev"
    ]

    for key in (
        "partner_platform_rev_on_navier",
        "partner_platform_rev_full_journey",
        "partner_platform_rev_yr",
    ):
        gc.pop(key, None)

    pe = gc.get("phase_economics") or {}
    for hz in pe.get("horizons") or []:
        for k in (
            "partner_platform_rev_yr",
            "partner_platform_rev_display",
            "partner_platform_rev_on_navier_yr",
            "partner_platform_rev_on_navier_display",
        ):
            hz.pop(k, None)
    gc["phase_economics"] = pe

    prov = gc.get("_marine_tam_split_provenance") or {}
    if prov:
        prov["ladder_rung_count"] = 5
        prov["rungs_ascending"] = [
            "som_floor",
            "som_network",
            "sam_network",
            "tam_transfer",
            "journey_gmv",
        ]
        prov.setdefault("platform_rev_excluded", "hospitality/destination — not a super-app partner")
        gc["_marine_tam_split_provenance"] = prov

    ci = gc.get("_cascade_inputs") or {}
    if ci:
        for key in ("rungs_expected_ascending", "rung_ids_expected"):
            if key in ci and "platform_rev" in (ci.get(key) or []):
                ci[key] = [r for r in ci[key] if r != "platform_rev"]
        if "ladder_rung_count" in ci or "rungs_expected_ascending" in ci:
            asc = ci.get("rungs_expected_ascending") or ci.get("rung_ids_expected")
            if asc:
                ci["ladder_rung_count"] = len(asc)
        shape = ci.get("ladder_shape")
        if isinstance(shape, str) and "platform" in shape.lower():
            ci["ladder_shape"] = (
                shape.replace(" < platform rev", "")
                .replace(" < platform_rev", "")
                .replace("< platform rev", "")
                .replace("< platform_rev", "")
                .strip()
            )
        gc["_cascade_inputs"] = ci
    legend = (gc.get("revenue_potential") or {}).get("whose_money_legend") or {}
    jgm = legend.get("journey_gmv") or ""
    if jgm and "super-app" in jgm:
        legend["journey_gmv"] = (
            "Total guest journey spend across transport, food, stays, experiences, and ancillary "
            "revenue the partner monetizes on-island. Journey GMV rung is in this unit."
        )
        rp = gc.setdefault("revenue_potential", {})
        rp["whose_money_legend"] = legend

    gc["_platform_rev_excluded"] = True
    gc["_platform_rev_rule"] = "super_app|ridehail only (LB-hospitality-ladder)"
    return gc


def strip_frontend_block(fe: dict[str, Any]) -> dict[str, Any]:
    """Strip platform revenue from growth_frontend_block.py output."""
    gc = {
        "revenue_potential": fe.get("revenue_potential"),
        "phase_economics": fe.get("phase_economics"),
        "ladder_transitions": [],
        "partner_platform_rev_on_navier": None,
    }
    strip_growth_case_platform(gc)  # type: ignore[arg-type]
    fe["revenue_potential"] = gc["revenue_potential"]
    fe["phase_economics"] = gc["phase_economics"]
    fe["_platform_rev_excluded"] = True
    return fe