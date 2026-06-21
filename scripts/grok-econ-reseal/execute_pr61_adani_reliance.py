#!/usr/bin/env python3
"""PR #61 — Adani / Reliance India proposal exact-bind + schema conformance lane.

Reuses PR #58 India spine wiring (marquee binds, gold route validation).
Does NOT run finance/economics (demand/fare not sourced per handoff).
"""
from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
HANDOFF = ROOT / "handoff" / "partner-map-model"
PARTNERS = ROOT / "partner-pitch" / "partners"
BUILD_DATE = "2026-06-21"

DISPLAY_CITY_IDS = {
    "mumbai-india",
    "goa-india",
    "kerala-backwaters-india",
    "andaman-india",
}

ROUTE_SCOPE_MAP = {
    "mumbai display-ready only": "intra",
    "display-ready India west-coast clusters": "all",
    "all display-ready India clusters plus backlog after mint": "all",
}

VALID_ROUTE_SCOPES = {
    "intra", "inter", "intercity", "network", "all", "cross_border", "regional",
}

VALID_PLATFORMS = frozenset({
    "Pioneer II", "N30 Pioneer II", "Quanta-LR", "both", "N35", "N35 Shuttle",
})


def _normalize_platform_label(raw: Any) -> str | None:
    if not isinstance(raw, str) or not raw.strip():
        return None
    if raw in VALID_PLATFORMS:
        return raw
    low = raw.lower()
    if "quanta" in low:
        return "Quanta-LR"
    if "n35 shuttle" in low or raw.strip() == "N35":
        return "N35 Shuttle"
    if "n35" in low:
        return "N35"
    if "n30" in low or "pioneer" in low:
        return "N30 Pioneer II"
    return None


def sanitize_route_entry(entry: dict[str, Any]) -> list[str]:
    """Drop or normalize fields that fail partner_proposal.schema.json when present."""
    notes: list[str] = []
    if entry.get("distance_nm") is None:
        entry.pop("distance_nm", None)
        notes.append("distance_nm: null removed")
    plat = entry.get("platform")
    if plat is not None and plat not in VALID_PLATFORMS:
        mapped = _normalize_platform_label(plat)
        if mapped:
            entry["_platform_note"] = plat
            entry["platform"] = mapped
            notes.append(f"platform: normalized → {mapped}")
        else:
            entry["_platform_note"] = plat
            entry.pop("platform", None)
            notes.append("platform: invalid removed")
    return notes


def sanitize_all_route_containers(doc: dict[str, Any]) -> list[str]:
    notes: list[str] = []
    containers: list[tuple[str, list]] = []
    if isinstance(doc.get("journeys_unlocked"), list):
        containers.append(("journeys_unlocked", doc["journeys_unlocked"]))
    for phase in doc.get("phases", []) or []:
        if isinstance(phase.get("featured_routes"), list):
            containers.append((f"phase-{phase.get('n')}", phase["featured_routes"]))
    for market in doc.get("markets", []) or []:
        mid = market.get("id", "?")
        if isinstance(market.get("journeys_unlocked"), list):
            containers.append((f"{mid}/journeys_unlocked", market["journeys_unlocked"]))
        for phase in market.get("phases", []) or []:
            if isinstance(phase.get("featured_routes"), list):
                containers.append(
                    (f"{mid}/phase-{phase.get('n')}", phase["featured_routes"]),
                )
    for label, routes in containers:
        for entry in routes:
            if isinstance(entry, dict):
                for n in sanitize_route_entry(entry):
                    notes.append(f"{label}: {n}")
    return notes


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def save_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n")


def _load_pr58():
    spec = importlib.util.spec_from_file_location(
        "execute_pr58",
        ROOT / "scripts" / "grok-econ-reseal" / "execute_pr58_india_gcc.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore
    return mod


def conform_schema(doc: dict[str, Any], *, partner_id: str, display: str) -> list[str]:
    """Map Tasklet draft fields to live proposal schema."""
    notes: list[str] = []
    doc["partner_id"] = partner_id
    doc["archetype"] = "corporate"
    doc["layout"] = "hub"
    doc.setdefault("tier", "review")
    doc.setdefault("category", "india_water_mobility_operator")
    doc.setdefault("economics_status", "economics_pending")

    nt = doc.get("network_thesis")
    if isinstance(nt, str):
        doc["network_thesis"] = {
            "headline": f"{display} × Navier — own and run Navier India",
            "body": nt,
            "coverage_note": doc.get("scope_rule", ""),
        }
        notes.append("network_thesis: str → object")

    def _conform_phase_route_scope(phase: dict[str, Any], *, ctx: str) -> None:
        rs = phase.get("route_scope")
        if rs in ROUTE_SCOPE_MAP:
            phase["route_scope"] = ROUTE_SCOPE_MAP[rs]
            notes.append(f"{ctx}: route_scope mapped")
        elif rs not in VALID_ROUTE_SCOPES:
            phase["route_scope"] = "intra"
            notes.append(f"{ctx}: route_scope {rs!r} → intra")

    for phase in doc.get("phases", []) or []:
        _conform_phase_route_scope(phase, ctx=f"phase {phase.get('n')}")

    for market in doc.get("markets", []) or []:
        mid = market.get("id", "?")
        for phase in market.get("phases", []) or []:
            _conform_phase_route_scope(phase, ctx=f"{mid}/phase {phase.get('n')}")

    if doc.get("layout") not in ("single", "hub", "network"):
        doc["layout"] = "hub"
        notes.append("layout: mapped to hub")

    notes.extend(sanitize_all_route_containers(doc))

    return notes


def validate_anchor_cities(doc: dict[str, Any]) -> list[dict]:
    issues: list[dict] = []
    for market in doc.get("markets", []) or []:
        for cid in market.get("anchor_cities", []) or []:
            if cid not in DISPLAY_CITY_IDS:
                issues.append({
                    "market": market.get("id"),
                    "city_id": cid,
                    "verdict": "ID_MISMATCH",
                    "reason": "not in sealed display-ready India city set",
                })
    for phase in doc.get("phases", []) or []:
        for cid in phase.get("cities", []) or []:
            if cid not in DISPLAY_CITY_IDS:
                issues.append({
                    "phase": phase.get("n"),
                    "city_id": cid,
                    "verdict": "ID_MISMATCH",
                    "reason": "not in sealed display-ready India city set",
                })
    return issues


def _extend_pr58_journey_bindings(pr58) -> None:
    """Adani/Reliance use slash labels; PR #58 bindings use parenthetical forms."""
    pr58.JOURNEY_PAIR_BINDINGS.update({
        ("gateway of india / bhaucha dhakka", "mandwa / alibaug"):
            "Gateway of India / Bhaucha Dhakka ↔ Mandwa (Alibaug)",
        ("south mumbai / nariman point", "navi mumbai / nmia / ulwe"):
            "South Mumbai (Nariman Point) ↔ Navi Mumbai / new airport",
        ("gateway of india", "elephanta caves"):
            "Gateway of India ↔ Elephanta Caves",
        ("north goa", "south goa (palolem / cavelossim)"):
            "North Goa ↔ South Goa (Palolem / Cavelossim)",
        ("panaji (mandovi river)", "north goa beaches (baga / morjim)"):
            "Panaji (Mandovi River) ↔ North Goa beaches (Baga / Morjim)",
        ("kochi (marine drive)", "alleppey backwaters"):
            "Kochi ↔ Alleppey (Alappuzha) backwaters",
        ("kochi (vyttila / marine drive)", "fort kochi / willingdon / bolgatty"):
            "Kochi (Vyttila / Marine Drive) ↔ Fort Kochi / Willingdon / Bolgatty",
        ("kochi", "kumarakom / vembanad lake"):
            "Kochi ↔ Kumarakom / Vembanad Lake",
        ("port blair (phoenix bay)", "havelock / swaraj dweep"):
            "Port Blair (Phoenix Bay) ↔ Havelock / Swaraj Dweep",
        ("havelock", "neil / shaheed dweep"):
            "Havelock ↔ Neil / Shaheed Dweep",
    })


def _rapido_bundle_registry(rapido: dict, pr58) -> dict[str, list[str]]:
    reg = pr58.collect_network_bundle_registry(rapido)
    for market in rapido.get("markets", []) or []:
        reg.update(pr58.collect_network_bundle_registry(market))
    return reg


def wire_with_rapido_spine(
    doc: dict,
    rapido: dict,
    *,
    pr58,
    gold_ids: set[str],
    spine_ids: set[str],
    by_id: dict,
) -> None:
    """Wire corridor-label / journey cards using Rapido's sealed bundle registry."""
    bundle_registry = _rapido_bundle_registry(rapido, pr58)
    containers: list[list] = []
    containers.append(doc.get("journeys_unlocked", []) or [])
    for phase in doc.get("phases", []) or []:
        containers.append(phase.get("featured_routes", []) or [])
    for market in doc.get("markets", []) or []:
        containers.append(market.get("journeys_unlocked", []) or [])
        for phase in market.get("phases", []) or []:
            containers.append(phase.get("featured_routes", []) or [])
    for routes in containers:
        for entry in routes:
            if isinstance(entry, dict):
                pr58.wire_corridor_label_entry(
                    entry,
                    bundle_registry=bundle_registry,
                    gold_ids=gold_ids,
                    spine_ids=spine_ids,
                    by_id=by_id,
                )


def inherit_rapido_phase_routes(target: dict, rapido: dict) -> int:
    """Copy sealed featured_routes from Rapido hub phases when labels match."""
    by_label: dict[str, dict] = {}
    for phase in rapido.get("phases", []) or []:
        for fr in phase.get("featured_routes", []) or []:
            if isinstance(fr, dict) and fr.get("label"):
                by_label[fr["label"]] = fr
    for market in rapido.get("markets", []) or []:
        for phase in market.get("phases", []) or []:
            for fr in phase.get("featured_routes", []) or []:
                if isinstance(fr, dict) and fr.get("label"):
                    by_label.setdefault(fr["label"], fr)

    inherited = 0
    for phase in target.get("phases", []) or []:
        for i, fr in enumerate(phase.get("featured_routes", []) or []):
            if not isinstance(fr, dict):
                continue
            ref = by_label.get(fr.get("label", ""))
            if not ref:
                continue
            merged = copy.deepcopy(fr)
            for key in (
                "route_ids", "route_id", "from_node_id", "to_node_id",
                "distance_nm", "platform", "vessel_gate", "display",
                "_link_kind", "_link_status", "_link_source",
            ):
                if key in ref and ref.get(key) is not None:
                    merged[key] = ref[key]
            if merged.get("route_ids") or merged.get("route_id"):
                merged["_link_source"] = "grok/execute_pr61/rapido-spine-inherit"
                merged["_link_status"] = merged.get("_link_status") or "linked-pr61-spine-inherit"
                inherited += 1
            phase["featured_routes"][i] = merged
    return inherited


def build_bind_ledger(doc: dict, partner: str, pr58) -> list[dict]:
    rows: list[dict] = []
    for row in pr58.collect_featured_for_seal(doc, partner):
        label = pr58.featured_row_label(row)
        rid = row.get("route_id")
        rids = row.get("route_ids")
        if rid:
            rows.append({
                "partner": partner,
                "label": label,
                "route_id": rid,
                "verdict": "SEALED_ROUTE_ID",
                "bind_method": row.get("_link_source", "explicit"),
            })
        elif rids:
            for x in rids:
                rows.append({
                    "partner": partner,
                    "label": label,
                    "route_id": x,
                    "verdict": "SEALED_ROUTE_ID",
                    "bind_method": row.get("_link_source", "bundle"),
                })
        else:
            rows.append({
                "partner": partner,
                "label": label,
                "route_id": None,
                "verdict": "HELD_NULL_WITH_REASON",
                "reason": row.get("_hold_reason") or row.get("_bind_status") or "null_until_exact_bind",
            })
    return rows


def main() -> int:
    pr58 = _load_pr58()
    _extend_pr58_journey_bindings(pr58)
    spine = load_json(HANDOFF / "india-shared-corridor-spine.json")
    all_spine = {c["corridor_id"] for c in spine.get("corridors", []) if c.get("corridor_id")}
    gold_ids, by_id, by_bp = pr58.build_route_index()

    rapido = load_json(PARTNERS / "rapido.json")
    goa_ledger: list[dict] = []

    stats: dict[str, Any] = {
        "lane": "grok/execute_pr61_adani_reliance",
        "applied_at": utc_now(),
        "partners": [],
        "outputs": [],
        "blockers": [],
    }

    bind_all: list[dict] = []
    qa_entries: list[dict] = []

    for partner_id, path in (
        ("adani-ports", PARTNERS / "adani-ports.json"),
        ("reliance-industries", PARTNERS / "reliance-industries.json"),
    ):
        doc = load_json(path)
        schema_notes = conform_schema(doc, partner_id=partner_id, display=doc.get("display", partner_id))
        n_inherit = inherit_rapido_phase_routes(doc, rapido)
        wire_with_rapido_spine(
            doc, rapido, pr58=pr58, gold_ids=gold_ids, spine_ids=all_spine, by_id=by_id,
        )
        doc = pr58.normalize_india_partner(
            path, spine, gold_ids, goa_ledger, doc=doc, by_id=by_id,
        )
        doc["proposal_status"] = "grok_seal_pass_pr61"
        doc["_pr61_execution"] = {
            "applied_at": utc_now(),
            "lane": "grok/execute_pr61_adani_reliance",
            "schema_notes": schema_notes,
            "rapido_inherited_routes": n_inherit,
            "economics_status": "economics_pending",
        }
        save_json(path, doc)

        anchor_issues = validate_anchor_cities(doc)
        binds = build_bind_ledger(doc, partner_id, pr58)
        bind_all.extend(binds)

        sealed = sum(1 for b in binds if b.get("verdict") == "SEALED_ROUTE_ID")
        held = sum(1 for b in binds if b.get("verdict") == "HELD_NULL_WITH_REASON")

        crosswalk = {
            "partner": partner_id,
            "anchor_cities": [
                {"city_id": c, "status": "OK" if c in DISPLAY_CITY_IDS else "ID_MISMATCH"}
                for c in DISPLAY_CITY_IDS
            ],
            "anchor_issues": anchor_issues,
        }
        cw_name = {
            "adani-ports": "ADANI-PORTS-ANCHOR-CITY-CROSSWALK.json",
            "reliance-industries": "RELIANCE-INDUSTRIES-ANCHOR-CITY-CROSSWALK.json",
        }[partner_id]
        save_json(PARTNERS.parent / cw_name, crosswalk)

        qa = pr58.run_render_qa(
            partner=partner_id,
            crosswalk=crosswalk,
            seal_ledger=binds,
            partner_doc=doc,
            active_city_scope=sorted(DISPLAY_CITY_IDS),
        )
        if anchor_issues:
            qa["anchor_issues"] = anchor_issues
            qa["verdict"] = "FAIL" if any(a["verdict"] == "ID_MISMATCH" for a in anchor_issues) else qa["verdict"]
        qa_entries.append(qa)

        stats["partners"].append({
            "partner": partner_id,
            "sealed": sealed,
            "held_null": held,
            "rapido_inherited": n_inherit,
        })
        stats["outputs"].extend([
            str(path.relative_to(ROOT)),
            f"partner-pitch/{cw_name}",
        ])

    ledger = {
        "package": "india-adani-reliance-bind-ledger",
        "build_date": BUILD_DATE,
        "partners": ["adani-ports", "reliance-industries"],
        "summary": {
            "total": len(bind_all),
            "sealed": sum(1 for r in bind_all if r.get("verdict") == "SEALED_ROUTE_ID"),
            "held_null": sum(1 for r in bind_all if r.get("verdict") == "HELD_NULL_WITH_REASON"),
        },
        "routes": bind_all,
    }
    save_json(HANDOFF / "india-adani-reliance-bind-ledger.json", ledger)
    stats["outputs"].append("handoff/partner-map-model/india-adani-reliance-bind-ledger.json")

    qa_doc = {
        "package": "india-adani-reliance-render-qa-ledger",
        "build_date": BUILD_DATE,
        "partners": qa_entries,
        "verdict": "PASS" if all(e.get("verdict") == "PASS" for e in qa_entries) else "FAIL",
        "checked_at": utc_now(),
    }
    save_json(HANDOFF / "india-adani-reliance-render-qa-ledger.json", qa_doc)
    stats["outputs"].append("handoff/partner-map-model/india-adani-reliance-render-qa-ledger.json")

    report_path = HANDOFF / f"PR61-GROK-EXECUTION-REPORT-{BUILD_DATE}.md"
    report_path.write_text(
        f"# PR #61 Grok Execution Report — {BUILD_DATE}\n\n"
        f"- Lane: `{stats['lane']}`\n"
        f"- Partners: {', '.join(p['partner'] for p in stats['partners'])}\n\n"
        + "\n".join(
            f"- **{p['partner']}**: {p['sealed']} sealed / {p['held_null']} held "
            f"({p['rapido_inherited']} inherited from Rapido spine)"
            for p in stats["partners"]
        )
        + f"\n\n## Validation\n\n"
        f"Bind ledger: {ledger['summary']}\n"
    )
    stats["outputs"].append(str(report_path.relative_to(ROOT)))

    print("→ validate_partner_proposals.py")
    v1 = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_partner_proposals.py")],
        cwd=ROOT, capture_output=True, text=True,
    )
    if v1.returncode != 0:
        stats["blockers"].append("validate_partner_proposals.py failed")
        print(v1.stdout)
        print(v1.stderr, file=sys.stderr)

    print("→ build-site.mjs")
    v2 = subprocess.run(
        ["node", str(ROOT / "scripts" / "build-site.mjs")],
        cwd=ROOT, capture_output=True, text=True,
    )
    if v2.returncode != 0:
        stats["blockers"].append("build-site.mjs failed")
        print(v2.stdout or v2.stderr, file=sys.stderr)
    else:
        print((v2.stdout or "").strip().split("\n")[-1])

    print(f"✓ PR #61 lane complete — bind ledger {ledger['summary']}")
    if stats["blockers"]:
        print("⚠ blockers:", stats["blockers"])
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())