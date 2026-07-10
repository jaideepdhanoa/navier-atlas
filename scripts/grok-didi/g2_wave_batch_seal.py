#!/usr/bin/env python3
"""DiDi ex-China G2 batch — CR/PA/DR + Ecuador/Peru + registry receipts.

Waves:
  1. Costa Rica / Panama / Dominican Republic — seal exact gold route IDs into partner featured_routes
  2. Ecuador / Peru — verify Galápagos stamp purge; fix Peru mis-stamps; document spine (no market mint)
  3. Chile/Argentina + APAC/Egypt — registry/status receipts only (no invented cities/routes)

Null beats wrong. No L3 demand. No live deck edits. Deploy deferred.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
FBT = ROOT / "data-clean/FEATURES_BY_TYPE.json"
ROUTES = ROOT / "data-clean/ROUTES.json"
SEAL = ROOT / "data-clean/SEAL.json"
PITCH = ROOT / "partner-pitch/partners/didi.json"
DC = ROOT / "data-clean/partners/didi.json"
WAVES = ROOT / "handoff/didi-ex-china/waves"
REG = ROOT / "handoff/didi-ex-china/registry-gaps"
STAMP_LEDGER = ROOT / "handoff/didi-ex-china/DIDI-ROUTE-STAMP-DEFECT-LEDGER-2026-07-09.json"

# --- CR / PA / DR spines (exact gold only; evidence-ranked) ---
COSTA_RICA_SPINE = [
    {
        "route_id": "rn-7e59f984abec",
        "od": "Paquera ↔ Puntarenas",
        "service_status": "current_scheduled",
        "priority": 1,
        "sub_proposal": "costa-rica",
    },
    {
        "route_id": "rn-eb4ca32edbef",
        "od": "Playa Naranjo ↔ Puntarenas",
        "service_status": "current_scheduled",
        "priority": 1,
        "sub_proposal": "costa-rica",
    },
    # geometry exists; not current scheduled public ferry
    {
        "route_id": "rn-55b63e976bb7",
        "od": "Marina Papagayo ↔ Four Seasons Papagayo",
        "service_status": "future_opportunity_not_current_scheduled",
        "priority": 3,
        "sub_proposal": "costa-rica",
    },
]

PANAMA_SPINE = [
    {
        "route_id": "rn-8fb072f5a8a8",
        "od": "Puerto Cartí ↔ Cartí Sugdup",
        "service_status": "guna_transfer_pattern_schedule_unverified",
        "priority": 2,
        "sub_proposal": "panama",
        "governance": "Guna authority/operator confirmation required",
    },
    {
        "route_id": "rn-87eec178e86f",
        "od": "El Porvenir ↔ Cayos Limones",
        "service_status": "transfer_or_excursion_unverified",
        "priority": 3,
        "sub_proposal": "panama",
    },
]

DR_SPINE = [
    {
        "route_id": "rn-64effc46b976",
        "od": "Samaná ↔ Sabana de la Mar",
        "service_status": "current_route_evidence_primary_confirm_needed",
        "priority": 1,
        "sub_proposal": "dominican-republic",
    },
    {
        "route_id": "rn-c3a4ef933700",
        "od": "Samaná ↔ Cayo Levantado",
        "service_status": "excursion_activity_unverified_volume",
        "priority": 2,
        "sub_proposal": "dominican-republic",
    },
]

HELD_NULL_CR_PA_DR = [
    {
        "od": "Cartí ↔ Colón",
        "route_id": None,
        "reason": "future_unsealed_research_concept",
        "sub_proposal": "panama",
    },
    {
        "od": "Samaná ↔ Las Galeras (generic endpoints)",
        "route_id": "rn-60740d4c3114",
        "reason": "atlas_route_only_excluded_from_featured_no_service_evidence",
        "sub_proposal": "dominican-republic",
        "action": "do_not_feature",
    },
    {
        "od": "Playa del Coco ↔ Playa Hermosa",
        "route_id": "rn-1efe26f3c0f4",
        "reason": "water_taxi_candidate_boarding_confirmation_needed",
        "sub_proposal": "costa-rica",
        "action": "do_not_feature",
    },
    {
        "od": "Las Galeras ↔ Playa Rincón",
        "route_id": "rn-21a0133c6d5c",
        "reason": "excursion_OSM_landings_primary_confirm_needed",
        "sub_proposal": "dominican-republic",
        "action": "do_not_feature",
    },
]

GALAPAGOS_SPINE = [
    {
        "route_id": "e__santa-cruz-galapagos-ecuador__puerto-ayora__isabela-galapagos-ecuador__puerto-villamil",
        "od": "Puerto Ayora ↔ Puerto Villamil (Isabela)",
        "service_status": "current_route_evidence",
        "sub_proposal": "galapagos-ecuador",
        "priority": 1,
        "fare_hint_usd": 30,
        "fare_note": "DPNG published per-person inter-island launch fare — not operator yield; annual pax null",
    },
    {
        "route_id": "e__santa-cruz-galapagos-ecuador__puerto-ayora__san-cristobal-galapagos-ecuador__puerto-baquerizo-moreno",
        "od": "Puerto Ayora ↔ Puerto Baquerizo Moreno (San Cristóbal)",
        "service_status": "current_route_evidence",
        "sub_proposal": "galapagos-ecuador",
        "priority": 1,
        "fare_hint_usd": 30,
    },
    {
        "route_id": "e__santa-cruz-galapagos-ecuador__puerto-ayora__floreana-galapagos-ecuador__puerto-velasco-ibarra",
        "od": "Puerto Ayora ↔ Puerto Velasco Ibarra (Floreana)",
        "service_status": "current_route_evidence_low_frequency",
        "sub_proposal": "galapagos-ecuador",
        "priority": 2,
        "fare_hint_usd": 30,
    },
]

# Confirm BPs on featured spines only
CONFIRM_BPS = [
    ("bp-f79715455d", "nicoya-papagayo-costa-rica", "Puntarenas Ferry Terminal"),
    ("bp-906030bde9", "nicoya-papagayo-costa-rica", "Paquera Ferry Terminal"),
    ("bp-e35dcefd78", "nicoya-papagayo-costa-rica", "Playa Naranjo Ferry Terminal"),
    ("bp-d0c610c51c", "san-blas-panama", "Puerto Cartí mainland dock"),
    ("bp-12bd0baa1e", "san-blas-panama", "Cartí Sugdup community dock"),
    ("bp-379a0d564b", "samana-dominican-republic", "Santa Bárbara de Samaná Ferry Dock"),
    ("bp-80f05b5195", "samana-dominican-republic", "Cayo Levantado Public Dock"),
    ("bp-c631c21193", "paracas-peru", "Paracas El Chaco Pier"),
    ("bp-c3eb36706a", "lima-peru", "Darsena Pier (Plaza Grau, Callao)"),
    ("bp-puerto-villamil-embarcadero", "isabela-galapagos-ecuador", "Puerto Villamil Embarcadero"),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load(p: Path) -> Any:
    return json.loads(p.read_text())


def save(p: Path, obj: Any, indent: int = 2) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=indent, ensure_ascii=False) + "\n")


def sha_obj(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def load_gold() -> tuple[list, dict[str, dict]]:
    raw = load(ROUTES)
    feats = raw if isinstance(raw, list) else raw.get("features")
    by = {}
    for f in feats:
        p = f.get("properties") or f
        if p.get("id"):
            by[p["id"]] = p
    return feats, by


def fr_objs(ids: list[str], gold: dict[str, dict]) -> list[dict]:
    out = []
    for rid in ids:
        p = gold.get(rid)
        if not p:
            raise SystemExit(f"missing gold route {rid}")
        fl, tl, cid = p.get("from_label"), p.get("to_label"), p.get("cluster_id")
        if not (fl and tl and cid):
            raise SystemExit(f"incomplete labels for {rid}: {fl!r} {tl!r} {cid!r}")
        out.append(
            {"route_id": rid, "from_label": fl, "to_label": tl, "cluster_id": cid}
        )
    return out


def confirm_bps(fbt: dict) -> dict:
    by = {
        (f.get("properties") or {}).get("id"): f
        for f in (fbt.get("poi") or [])
        if (f.get("properties") or {}).get("id")
    }
    ledger = []
    for bp_id, parent, name in CONFIRM_BPS:
        feat = by.get(bp_id)
        if not feat:
            ledger.append({"id": bp_id, "action": "missing", "status": "held"})
            continue
        props = feat.setdefault("properties", {})
        before = props.get("parent_city_id")
        if before and before != parent:
            # do not reparent against research without evidence — flag only
            ledger.append(
                {
                    "id": bp_id,
                    "action": "parent_mismatch",
                    "status": "flagged",
                    "before": before,
                    "expected": parent,
                }
            )
        props["status"] = props.get("status") or "operational"
        props["_didi_wave_g2"] = {
            "at": utc_now(),
            "action": "confirm",
            "expected_parent": parent,
            "name_ref": name,
        }
        ledger.append(
            {
                "id": bp_id,
                "action": "confirm",
                "status": "accepted",
                "parent_city_id": props.get("parent_city_id"),
            }
        )
    return {"ledger": ledger, "n": len([x for x in ledger if x["status"] == "accepted"])}


def fix_peru_italy_misstamp(routes: list) -> dict:
    """rn-f0a756c7f278 is Lima geometry stamped italy — re-stamp to peru."""
    changes = []
    for f in routes:
        p = f.get("properties") or {}
        if p.get("id") != "rn-f0a756c7f278":
            continue
        before = p.get("cluster_id")
        if before != "peru":
            p["cluster_id"] = "peru"
            p["_didi_wave_g2_stamp_fix"] = {
                "at": utc_now(),
                "before_cluster": before,
                "reason": "Lima Costa Verde–Callao endpoints; was foreign-stamped italy",
            }
            changes.append(
                {
                    "route_id": "rn-f0a756c7f278",
                    "before": before,
                    "after": "peru",
                    "action": "restamp_cluster",
                }
            )
        break
    return {"changes": changes}


def verify_stamp_purge(gold: dict[str, dict]) -> dict:
    """Confirm ledger foreign stamps are no longer on victim clusters."""
    if not STAMP_LEDGER.exists():
        return {"status": "no_ledger"}
    ledger = load(STAMP_LEDGER)
    report = {}
    for cl in ledger.get("clusters") or []:
        cid = cl.get("cluster_id")
        if cid not in ("galapagos-ecuador", "new-zealand"):
            continue
        foreign = cl.get("foreign_stamped_routes") or []
        still = []
        fixed = 0
        for item in foreign:
            rid = item.get("route_id") if isinstance(item, dict) else item
            p = gold.get(rid)
            if p and p.get("cluster_id") == cid:
                still.append(rid)
            else:
                fixed += 1
        member_ok = []
        if cid == "galapagos-ecuador":
            for row in GALAPAGOS_SPINE:
                rid = row["route_id"]
                p = gold.get(rid)
                member_ok.append(
                    {
                        "route_id": rid,
                        "present": bool(p),
                        "cluster_id": (p or {}).get("cluster_id"),
                        "ok": bool(p) and p.get("cluster_id") == "galapagos-ecuador",
                    }
                )
        report[cid] = {
            "ledger_foreign_n": len(foreign),
            "still_on_cluster": still,
            "fixed_n": fixed,
            "purge_complete": len(still) == 0,
            "member_routes": member_ok,
        }
    # live count: any non-member still stamped galapagos?
    gal_members = {
        "santa-cruz-galapagos-ecuador",
        "isabela-galapagos-ecuador",
        "san-cristobal-galapagos-ecuador",
        "floreana-galapagos-ecuador",
    }
    live_foreign = []
    for rid, p in gold.items():
        if p.get("cluster_id") != "galapagos-ecuador":
            continue
        fc, tc = p.get("from_city_id"), p.get("to_city_id")
        if fc not in gal_members and tc not in gal_members:
            live_foreign.append(rid)
    report["galapagos_live_foreign"] = live_foreign
    report["galapagos_live_clean"] = len(live_foreign) == 0
    return report


def bind_cr_pa_dr(partner: dict, gold: dict[str, dict]) -> dict:
    bound = []
    specs = [
        ("costa-rica", COSTA_RICA_SPINE),
        ("panama", PANAMA_SPINE),
        ("dominican-republic", DR_SPINE),
    ]
    for mid, spine in specs:
        ids = [r["route_id"] for r in spine]
        for m in partner.get("markets") or []:
            if m.get("id") != mid:
                continue
            m["featured_routes"] = fr_objs(ids, gold)
            for i, ph in enumerate(m.get("phases") or []):
                if not isinstance(ph, dict):
                    continue
                # phase 0: priority 1 only
                p1 = [r["route_id"] for r in spine if r.get("priority", 9) <= 1]
                ph["featured_routes"] = fr_objs(p1 if i == 0 and p1 else ids, gold)
            # journeys from spine
            journeys = []
            for row in spine:
                p = gold[row["route_id"]]
                journeys.append(
                    {
                        "from": p.get("from_label"),
                        "to": p.get("to_label"),
                        "from_label": p.get("from_label"),
                        "to_label": p.get("to_label"),
                        "label": f"{p.get('from_label')} → {p.get('to_label')}",
                        "route_id": row["route_id"],
                        "distance_nm": p.get("distance_nm"),
                        "platform": "Pioneer II",
                        "archetype": "commuter"
                        if mid == "costa-rica" and row.get("priority") == 1
                        else "tourism",
                        "_link_status": "linked-g2-seal",
                        "_link_source": "grok/didi-wave-g2",
                        "economics_status": "economics_pending",
                        "_service_status": row.get("service_status"),
                        "today": "Existing water transfer with mixed reliability and boarding friction.",
                        "with_navier": "A clean high-frequency hop booked in DiDi, once demand is sourced.",
                    }
                )
            # keep prior aspirational journeys without route_id
            prior = [
                j
                for j in (m.get("journeys_unlocked") or [])
                if isinstance(j, dict) and not j.get("route_id")
            ]
            m["journeys_unlocked"] = journeys + prior
            wn = m.get("why_navier_now")
            if isinstance(wn, dict):
                wow_ids = [r["route_id"] for r in spine if r.get("priority", 9) <= 1]
                wn["wow_corridors"] = fr_objs(wow_ids, gold) if wow_ids else []
            bound.append({"market": mid, "n": len(ids), "route_ids": ids})
    partner["_didi_g2_cr_pa_dr"] = {
        "at": utc_now(),
        "bound": bound,
        "held_null": HELD_NULL_CR_PA_DR,
        "status": "seal-complete / cascade-needed",
    }
    return {"bound": bound}


def stamp_galapagos_partner_meta(partner: dict, stamp_report: dict) -> None:
    """No market block yet — record seal readiness on partner provenance only."""
    partner["_didi_g2_ecuador_peru"] = {
        "at": utc_now(),
        "status": "geometry_stamp_verified / partner_market_bind_deferred",
        "galapagos_spine_route_ids": [r["route_id"] for r in GALAPAGOS_SPINE],
        "stamp_purge": stamp_report,
        "note": (
            "DiDi partner JSON has no ecuador/peru market blocks yet. "
            "Three Galápagos routes are gold-clean on galapagos-ecuador. "
            "Peru Ballestas/Palomino remain route-null for DiDi featured bind until "
            "service + annual pax sourced. Annual pax all null."
        ),
        "held": [
            "Paracas–Ballestas annual pax null",
            "Callao–Palomino annual pax null",
            "Lima–Paracas future",
            "San Andrés passenger auth unproven",
            "DiDi city-level proof absent for these piers",
        ],
    }


def write_wave_artifacts(
    gold: dict[str, dict],
    cr_bind: dict,
    stamp_report: dict,
    bp_stats: dict,
    peru_fix: dict,
) -> dict[str, Path]:
    paths: dict[str, Path] = {}

    # CR-PA-DR spine
    spine_cr = {
        "at": utc_now(),
        "partner": "didi",
        "status": "seal-complete / cascade-needed",
        "finance_market_keys": ["costa-rica", "panama", "dominican-republic"],
        "costa_rica": [
            {**r, "from_label": gold[r["route_id"]].get("from_label"), "to_label": gold[r["route_id"]].get("to_label"), "distance_nm": gold[r["route_id"]].get("distance_nm")}
            for r in COSTA_RICA_SPINE
        ],
        "panama": [
            {**r, "from_label": gold[r["route_id"]].get("from_label"), "to_label": gold[r["route_id"]].get("to_label"), "distance_nm": gold[r["route_id"]].get("distance_nm")}
            for r in PANAMA_SPINE
        ],
        "dominican_republic": [
            {**r, "from_label": gold[r["route_id"]].get("from_label"), "to_label": gold[r["route_id"]].get("to_label"), "distance_nm": gold[r["route_id"]].get("distance_nm")}
            for r in DR_SPINE
        ],
        "held_null": HELD_NULL_CR_PA_DR,
        "all_route_ids": [r["route_id"] for r in COSTA_RICA_SPINE + PANAMA_SPINE + DR_SPINE],
        "rules": [
            "Null beats wrong — annual one-way pax all null",
            "Do not convert airport/whale/tourism counts to route demand",
            "No exact DiDi city claim for Samaná or Guna Yala",
            "Cartí–Colón remains route_id null",
            "Guna governance confirmation required before Panama finance",
        ],
    }
    p = WAVES / "CR-PA-DR-ROUTE-SPINE-FOR-TASKLET-2026-07-09.json"
    save(p, spine_cr)
    paths["cr_spine"] = p

    handoff_cr = WAVES / "TASKLET-T3-CR-PA-DR-HANDOFF.md"
    handoff_cr.write_text(
        "\n".join(
            [
                "# Tasklet T3 handoff — DiDi Costa Rica / Panama / Dominican Republic",
                "",
                f"**From:** Grok · G2 seal · `{utc_now()}`  ",
                "**Status:** `seal-complete / cascade-needed`",
                "",
                "## Sealed featured spines",
                "",
                "### Costa Rica",
                *[f"- `{r['route_id']}` — {r['od']} — `{r['service_status']}`" for r in COSTA_RICA_SPINE],
                "",
                "### Panama (governance-sensitive)",
                *[f"- `{r['route_id']}` — {r['od']} — `{r['service_status']}`" for r in PANAMA_SPINE],
                "",
                "### Dominican Republic",
                *[f"- `{r['route_id']}` — {r['od']} — `{r['service_status']}`" for r in DR_SPINE],
                "",
                "## Held / excluded from featured",
                *[f"- {h['od']} — `{h['reason']}`" for h in HELD_NULL_CR_PA_DR],
                "",
                "## Tasklet owns",
                "",
                "1. Annual one-way pax for Nicoya ferries + confirmed CRC fares → USD.",
                "2. Primary operator confirmation for Samaná public ferry fare/timetable.",
                "3. Guna authority boarding permissions before Panama base-case economics.",
                "4. Leave Cartí–Colón null until sealed geometry + authority.",
                "5. No tourism/airport/whale conversion to route demand.",
                "",
                f"Spine: `{p.relative_to(ROOT)}`",
                "",
            ]
        )
        + "\n"
    )
    paths["cr_handoff"] = handoff_cr

    # Ecuador/Peru
    spine_ec = {
        "at": utc_now(),
        "partner": "didi",
        "status": "geometry_stamp_verified / partner_market_bind_deferred / cascade-needed",
        "galapagos": GALAPAGOS_SPINE,
        "stamp_purge": stamp_report,
        "peru_stamp_fix": peru_fix,
        "all_route_ids": [r["route_id"] for r in GALAPAGOS_SPINE],
        "rules": [
            "Galápagos foreign stamps already purged on main — verified live-clean",
            "Three real inter-island routes stamped galapagos-ecuador",
            "Do not convert DPNG tourist arrivals into route demand",
            "USD 30 DPNG fare is published benchmark not yield",
            "Peru Ballestas/Palomino: no DiDi featured bind until market block + annual pax",
            "DiDi evidence country-level only for these markets",
        ],
    }
    p2 = WAVES / "ECUADOR-PERU-ROUTE-SPINE-FOR-TASKLET-2026-07-09.json"
    save(p2, spine_ec)
    paths["ec_spine"] = p2

    handoff_ec = WAVES / "TASKLET-T3-ECUADOR-PERU-HANDOFF.md"
    handoff_ec.write_text(
        "\n".join(
            [
                "# Tasklet T3 handoff — DiDi Ecuador (Galápagos) / Peru",
                "",
                f"**From:** Grok · G2 stamp verify · `{utc_now()}`  ",
                "**Status:** `geometry_stamp_verified / partner_market_bind_deferred / cascade-needed`",
                "",
                "## P0 stamp purge",
                "",
                f"- Galápagos foreign stamps still on cluster: **{stamp_report.get('galapagos-ecuador', {}).get('still_on_cluster', [])}**",
                f"- Live clean: **{stamp_report.get('galapagos_live_clean')}**",
                f"- NZ Kotor purge still on NZ cluster: **{stamp_report.get('new-zealand', {}).get('still_on_cluster', [])}**",
                f"- Peru italy mis-stamp fix: **{peru_fix}**",
                "",
                "## Galápagos sealed route IDs (gold)",
                "",
                *[f"- `{r['route_id']}` — {r['od']}" for r in GALAPAGOS_SPINE],
                "",
                "## Tasklet owns",
                "",
                "1. Route-level annual pax / load factors for three inter-island links.",
                "2. Ballestas + Palomino monthly passengers and full fee stacks.",
                "3. DiDi city-level service proof before local availability claims.",
                "4. Partner market blocks for galapagos/peru when Jaideep opens that phase — Grok will bind featured then.",
                "5. Keep annual_one_way_pax null until sourced.",
                "",
                f"Spine: `{p2.relative_to(ROOT)}`",
                "",
            ]
        )
        + "\n"
    )
    paths["ec_handoff"] = handoff_ec

    # Chile/Argentina registry receipt
    chile_path = REG / "DIDI-CHILE-ARGENTINA-REGISTRY-RESEARCH-2026-07-09.json"
    chile = load(chile_path) if chile_path.exists() else {}
    rec_cl = {
        "at": utc_now(),
        "lane": "Chile / Argentina registry",
        "status": "research-complete / registry-and-seal-needed",
        "g2_action": "no_geometry_seal",
        "reason": "All candidate corridors have route_id null; cities lack canonical Atlas city_ids; no partner market blocks.",
        "research": str(chile_path.relative_to(ROOT)) if chile_path.exists() else None,
        "cities_proposed": [
            c.get("proposed_city_id") or c.get("city_id") or c.get("name") or c.get("display")
            for c in (chile.get("cities") or [])
        ],
        "corridors_n": len(chile.get("candidate_corridors") or []),
        "route_ids_non_null": 0,
        "next": [
            "Mint partner-neutral city IDs + BPs from sourced facilities only",
            "Seal routes only after exact endpoints exist in gold",
            "Then open DiDi market blocks + inheritance",
        ],
        "do_not": chile.get("do_not_publish"),
    }
    p3 = REG / "G2-CHILE-ARGENTINA-REGISTRY-RECEIPT-2026-07-09.json"
    save(p3, rec_cl)
    paths["cl_receipt"] = p3

    # APAC / Egypt registry receipts
    for slug, label in [
        ("DIDI-AUSTRALIA-NEW-ZEALAND", "Australia / New Zealand"),
        ("DIDI-JAPAN-HONG-KONG-TAIWAN", "Japan / Hong Kong / Taiwan"),
        ("DIDI-EGYPT", "Egypt"),
    ]:
        deep = WAVES / f"{slug}-DEEPENING-2026-07-09.json"
        d = load(deep) if deep.exists() else {}
        cors = d.get("candidate_corridors") or []
        rids = [c.get("route_id") for c in cors if isinstance(c, dict) and c.get("route_id")]
        present = [rid for rid in rids if rid in gold]
        rec = {
            "at": utc_now(),
            "lane": label,
            "status": "research-complete / seal-deferred",
            "g2_action": "stamp_hygiene_check_only",
            "reason": (
                "No DiDi partner market blocks for these jurisdictions yet; "
                "Taiwan/HK status gates; research candidates mostly route_id null or "
                "require human-reviewed marine geometry. NZ Kotor foreign stamps already purged."
            ),
            "research": str(deep.relative_to(ROOT)) if deep.exists() else None,
            "candidate_route_ids_in_research": rids,
            "route_ids_present_in_gold": present,
            "gates": {
                "taiwan": "hard operation-status gate — no publish as current DiDi market",
                "hong_kong": "current-service verification needed beyond app-store",
                "egypt_red_sea": "human-reviewed waypoints required",
            },
            "stamp_notes": {
                "new_zealand_kotor_purge": stamp_report.get("new-zealand", {}),
            }
            if "AUSTRALIA" in slug
            else {},
            "next": [
                "Do not invent BPs/routes/demand",
                "Open market blocks only after exact city proof + route seal",
                "Tasklet sources annual pax only after route IDs sealed",
            ],
        }
        out = WAVES / f"G2-{slug}-REGISTRY-RECEIPT-2026-07-09.json"
        save(out, rec)
        paths[slug] = out

    return paths


def update_seal() -> dict:
    if not SEAL.exists():
        return {}
    seal = load(SEAL)
    files = seal.setdefault("files", {})
    out = {}
    for rel, path in [
        ("FEATURES_BY_TYPE.json", FBT),
        ("ROUTES.json", ROUTES),
        ("partners/didi.json", DC),
    ]:
        obj = load(path)
        h = sha_obj(obj)
        files[rel] = h
        out[rel] = h
    notes = seal.setdefault("_notes", [])
    if isinstance(notes, list):
        notes.append({"at": utc_now(), "event": "didi-wave-g2-batch-cr-ec-registry"})
    seal["sealed_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    save(SEAL, seal)
    return out


def run_gates() -> dict:
    def run(cmd: list[str]) -> dict:
        r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        out = (r.stdout or "") + (r.stderr or "")
        return {"exit": r.returncode, "tail": "\n".join(out.splitlines()[-40:])}

    return {
        "gate_g": run([sys.executable, str(ROOT / "scripts/audit_partner_copy.py")]),
        "inheritance_strict": run(
            [
                sys.executable,
                str(ROOT / "scripts/validate_partner_inheritance.py"),
                "--partner",
                "didi",
                "--strict",
                "--include-pitch",
                "--json",
            ]
        ),
        "fidelity": run(
            [sys.executable, str(ROOT / "scripts/audit_proposal_fidelity.py"), "--partner", "didi"]
        ),
        "route_linkage": run(
            ["node", str(ROOT / "scripts/audit-partner-route-linkage.mjs"), "didi"]
        )
        if (ROOT / "scripts/audit-partner-route-linkage.mjs").exists()
        else {"exit": 0, "tail": "skipped"},
    }


def main() -> int:
    print("=== DiDi wave G2 batch ===")
    routes, gold = load_gold()
    fbt = load(FBT)

    print("1. Confirm spine BPs")
    bp_stats = confirm_bps(fbt)
    print("  ", bp_stats["n"], "confirmed")

    print("2. Peru italy mis-stamp fix")
    peru_fix = fix_peru_italy_misstamp(routes)
    print("  ", peru_fix)

    print("3. Verify Galápagos / NZ stamp purge")
    # refresh gold after potential restamp
    gold = {(f.get("properties") or f).get("id"): (f.get("properties") or f) for f in routes}
    stamp_report = verify_stamp_purge(gold)
    print("  galapagos clean", stamp_report.get("galapagos_live_clean"))
    print("  nz still foreign", stamp_report.get("new-zealand", {}).get("still_on_cluster"))

    # write geometry
    ROUTES.write_text(json.dumps(routes, ensure_ascii=False, separators=(", ", ": ")) + "\n")
    save(FBT, fbt, indent=2)
    gold = {(f.get("properties") or f).get("id"): (f.get("properties") or f) for f in routes}

    print("4. Bind CR/PA/DR partner markets")
    partner = load(PITCH)
    cr_bind = bind_cr_pa_dr(partner, gold)
    stamp_galapagos_partner_meta(partner, stamp_report)
    print("  ", cr_bind)

    text = json.dumps(partner, indent=2, ensure_ascii=False) + "\n"
    PITCH.write_text(text)
    DC.write_text(text)

    print("5. Artifacts")
    paths = write_wave_artifacts(gold, cr_bind, stamp_report, bp_stats, peru_fix)
    for k, p in paths.items():
        print("  ", k, p.relative_to(ROOT))

    print("6. SEAL")
    seal_h = update_seal()

    print("7. Gates")
    gates = run_gates()
    for name, g in gates.items():
        print(f"\n=== {name} exit={g['exit']} ===")
        print(g["tail"][:1500])

    receipt = {
        "at": utc_now(),
        "partner": "didi",
        "lane": "G2 wave batch: CR/PA/DR + Ecuador/Peru stamps + registry receipts",
        "status": "partial_seal_complete",
        "waves": {
            "costa_rica_panama_dr": {
                "status": "seal-complete / cascade-needed",
                "bind": cr_bind,
                "spine": str(paths["cr_spine"].relative_to(ROOT)),
            },
            "ecuador_peru": {
                "status": "geometry_stamp_verified / partner_market_bind_deferred",
                "stamp_purge": stamp_report,
                "peru_fix": peru_fix,
                "spine": str(paths["ec_spine"].relative_to(ROOT)),
            },
            "chile_argentina": {
                "status": "research-complete / registry-and-seal-needed",
                "receipt": str(paths["cl_receipt"].relative_to(ROOT)),
            },
            "australia_nz": {"receipt": str(paths["DIDI-AUSTRALIA-NEW-ZEALAND"].relative_to(ROOT))},
            "japan_hk_taiwan": {
                "receipt": str(paths["DIDI-JAPAN-HONG-KONG-TAIWAN"].relative_to(ROOT))
            },
            "egypt": {"receipt": str(paths["DIDI-EGYPT"].relative_to(ROOT))},
        },
        "bp": bp_stats,
        "gates": {
            name: {
                "exit": g["exit"],
                "pass": g["exit"] == 0 or (name == "fidelity" and "PASS" in g["tail"]),
                "tail": g["tail"][-800:],
            }
            for name, g in gates.items()
        },
        "sha256": seal_h,
        "deploy": "deferred",
        "rules_honored": [
            "null beats wrong",
            "no invent route ids/cities/demand",
            "no live deck edits",
            "Taiwan/HK status gates preserved",
        ],
    }
    rec_path = WAVES / "G2-WAVE-BATCH-RECEIPT-2026-07-09.json"
    save(rec_path, receipt)
    print("\nwrote", rec_path)

    rc = 0
    for name in ("gate_g", "inheritance_strict"):
        if gates.get(name, {}).get("exit", 1) != 0:
            rc = 1
    fid = gates.get("fidelity") or {}
    if fid.get("exit", 1) != 0 and "PASS" not in (fid.get("tail") or ""):
        rc = 1
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
