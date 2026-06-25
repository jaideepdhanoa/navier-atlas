#!/usr/bin/env python3
"""Deterministic LINE MAN Wongnai Thailand mirror from grab-thailand (PR #110 handoff)."""
from __future__ import annotations

import argparse
import copy
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC_PARTNER = "grab-thailand"
TGT_PARTNER = "line-man-wongnai"
SRC_PITCH = ROOT / "partner-pitch" / "partners" / f"{SRC_PARTNER}.json"
TGT_PITCH = ROOT / "partner-pitch" / "partners" / f"{TGT_PARTNER}.json"
TGT_DC = ROOT / "data-clean" / "partners" / f"{TGT_PARTNER}.json"
CROSSWALK_OUT = ROOT / "partner-pitch" / "LINE-MAN-WONGNAI-ANCHOR-CITY-CROSSWALK.json"
FEATURES = ROOT / "data-clean" / "FEATURES_BY_TYPE.json"
REPORT = ROOT / "grok-routing-output" / "line-man-wongnai-mirror-report.json"
HANDOFF = ROOT / "handoff" / "GROK-HANDOFF-line-man-wongnai-thailand-mirror-2026-06-25.md"

COPY_REPLACEMENTS = [
    (re.compile(r"Grab Thailand\s*[x×]\s*Navier", re.I), "LINE MAN Wongnai × Navier"),
    (re.compile(r"Grab\s*[x×]\s*Navier", re.I), "LINE MAN Wongnai × Navier"),
    (re.compile(r"Grab Thailand", re.I), "LINE MAN Wongnai"),
    (re.compile(r"Grab-branded", re.I), "LINE MAN Wongnai-branded"),
    (re.compile(r"Grab's", re.I), "LINE MAN Wongnai's"),
    (re.compile(r"Grab already", re.I), "LINE MAN Wongnai already"),
    (re.compile(r"Grab brings", re.I), "LINE MAN Wongnai brings"),
    (re.compile(r"the Grab app", re.I), "the LINE MAN Wongnai app"),
    (re.compile(r"in Grab", re.I), "in LINE MAN Wongnai"),
    (re.compile(r"\bGrab\b"), "LINE MAN Wongnai"),
]

SKIP_KEY_SUFFIXES = (
    "route_id",
    "route_ids",
    "from_node_id",
    "to_node_id",
    "id",
    "slug",
    "partner_id",
    "atlas_city_id",
    "registry_key",
    "_handoff_bp_id",
    "coords_source",
    "_link_source",
    "_geometry_fix_source",
)

HERO_OVERRIDES = {
    "title": "LINE MAN Wongnai × Navier — Thailand's local-life network, on the water",
    "subtitle": "LINE MAN Wongnai already owns Thailand's daily local demand. Water is the only surface no one owns yet.",
    "what_we_do_together": (
        "We launch a LINE MAN Wongnai-branded foiling water tier across Thailand's strongest water flows — "
        "the Gulf islands, the Andaman, the Chao Phraya, and the upper-Gulf ring — booked in-app, "
        "premium-priced and category-defining. Navier brings the software-defined hydrofoiling fleet now proven "
        "in the Maldives; LINE MAN Wongnai brings the demand, the app, payments and the brand."
    ),
}

PARTNER_CONTEXT_OVERRIDES = {
    "their_ambition": (
        "LINE MAN Wongnai is Thailand's local-life platform — food, groceries, payments, maps and everyday mobility — "
        "and is pushing into premium, differentiated tiers beyond the road."
    ),
    "their_pressure": (
        "Thailand's Gulf islands, Andaman resort flows, and Bangkok river traffic are high-value surfaces no local-life "
        "platform serves on the water — left entirely to weather-fragile diesel ferries."
    ),
    "where_navier_fits": (
        "A LINE MAN Wongnai-branded foiling water tier across the Samui triangle, Phuket/Andaman, and the Chao Phraya — "
        "booked in-app, premium-priced, on sealed Atlas geometry with corridors live today."
    ),
}

NETWORK_THESIS_OVERRIDES = {
    "headline": "One app. Two coasts, a river, and an upper-Gulf ring. Thailand's local-life network, on the water.",
    "body": (
        "Thailand is one of the most water-rich markets LINE MAN Wongnai serves — a Gulf coast of leisure islands, "
        "an Andaman coast of resort flows, a river megacity, and an upper-Gulf ring connecting the capital to the "
        "Eastern Seaboard and the royal coast — and LINE MAN Wongnai already owns the demand across all of it. "
        "The same in-app foiling tier proven in the Maldives extends cluster by cluster."
    ),
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def save_json(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n")


def should_skip_key(key: str) -> bool:
    return any(key == suf or key.endswith(suf) for suf in SKIP_KEY_SUFFIXES)


def adapt_copy(text: str) -> str:
    if not isinstance(text, str):
        return text
    out = text
    for pat, repl in COPY_REPLACEMENTS:
        out = pat.sub(repl, out)
    return out


def walk_copy(obj, parent_key: str = ""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str) and not should_skip_key(k):
                obj[k] = adapt_copy(v)
            else:
                walk_copy(v, k)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            if isinstance(item, str) and not should_skip_key(parent_key):
                obj[i] = adapt_copy(item)
            else:
                walk_copy(item, parent_key)


def patch_paths(obj, src: str, tgt: str):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str) and src in v and k in {
                "agg", "growth", "sheet", "cascade_at", "economics_url", "model_link",
            } or (isinstance(v, str) and v.startswith("finance/") and src in v):
                obj[k] = v.replace(src, tgt)
            else:
                patch_paths(v, src, tgt)
    elif isinstance(obj, list):
        for item in obj:
            patch_paths(item, src, tgt)


def build_partner_doc() -> dict:
    doc = copy.deepcopy(load_json(SRC_PITCH))
    doc["partner_id"] = TGT_PARTNER
    doc["display"] = "LINE MAN Wongnai"
    doc["derivative_of"] = SRC_PARTNER
    doc["_mirror_of"] = SRC_PARTNER
    doc["_mirror_at"] = utc_now()
    doc["_mirror_handoff"] = str(HANDOFF.relative_to(ROOT))

    if "hero" in doc and isinstance(doc["hero"], dict):
        doc["hero"].update(HERO_OVERRIDES)
    if "partner_context" in doc and isinstance(doc["partner_context"], dict):
        doc["partner_context"].update(PARTNER_CONTEXT_OVERRIDES)
    if "network_thesis" in doc and isinstance(doc["network_thesis"], dict):
        doc["network_thesis"].update(NETWORK_THESIS_OVERRIDES)

    walk_copy(doc)
    patch_paths(doc, SRC_PARTNER, TGT_PARTNER)

    if isinstance(doc.get("economics_status"), dict):
        doc["economics_status"]["state"] = "mirror_of_grab_thailand_pending_cascade"
        doc["economics_status"]["mirror_source"] = SRC_PARTNER

    return doc


def city_ids_from_features() -> set[str]:
    fbt = load_json(FEATURES)
    ids: set[str] = set()
    for t in ("city", "priority_city"):
        for f in fbt.get(t, []):
            pid = (f.get("properties") or {}).get("id")
            if pid:
                ids.add(pid)
    return ids


def build_crosswalk(partner: dict) -> dict:
    src_xwalk = load_json(ROOT / "partner-pitch" / "GRAB-THAILAND-ANCHOR-CITY-CROSSWALK.json")
    atlas_ids = city_ids_from_features()
    anchors: dict = {}
    for m in partner.get("markets", []):
        for cid in m.get("anchor_cities", []):
            anchors[cid] = {
                "verdict": "OK" if cid in atlas_ids else "HOLD",
                "atlas_city_id": cid if cid in atlas_ids else None,
                "evidence": "exact ID match inherited from grab-thailand mirror",
                "market": m.get("id"),
            }
    connected: dict = {}
    for bucket in ("connected_cities_minted", "connected_cities"):
        for cid, rec in (src_xwalk.get(bucket) or {}).items():
            if isinstance(rec, dict):
                connected[cid] = {**rec, "mirror_source": SRC_PARTNER}

    return {
        "_doc": "Gate-A anchor-city crosswalk for line-man-wongnai (mirrored from grab-thailand).",
        "partner": TGT_PARTNER,
        "build_date": utc_now()[:10],
        "updated_at": utc_now(),
        "scope_note": "Thailand-only LINE MAN Wongnai mirror; geometry/routes/economics inherited from grab-thailand.",
        "mirror_of": SRC_PARTNER,
        "anchors": anchors,
        "connected_cities_minted": connected,
        "cross_border_regional_only": src_xwalk.get("cross_border_regional_only", {}),
        "guardrails": src_xwalk.get("guardrails", []),
    }


def copy_finance_recal() -> list[str]:
    recal = ROOT / "finance" / "recal"
    growth_draft = ROOT / "partner-pitch" / "partners" / "_growth-draft"
    copied = []
    pairs = [
        (recal / f"corridors-{SRC_PARTNER}.json", recal / f"corridors-{TGT_PARTNER}.json"),
        (recal / f"agg-{SRC_PARTNER}.json", recal / f"agg-{TGT_PARTNER}.json"),
        (recal / f"growth-{SRC_PARTNER}.json", recal / f"growth-{TGT_PARTNER}.json"),
        (growth_draft / f"{SRC_PARTNER}.growth.json", growth_draft / f"{TGT_PARTNER}.growth.json"),
    ]
    for src, dst in pairs:
        if not src.is_file():
            continue
        text = src.read_text().replace(SRC_PARTNER, TGT_PARTNER)
        dst.write_text(text)
        copied.append(str(dst.relative_to(ROOT)))
    return copied


def run_validations() -> dict:
    results: dict = {}
    results["json_parse"] = {"ok": True, "path": str(TGT_PITCH)}
    load_json(TGT_PITCH)

    xwalk = load_json(CROSSWALK_OUT)
    hold = [k for k, v in xwalk.get("anchors", {}).items() if v.get("verdict") != "OK"]
    results["anchor_crosswalk"] = {"anchors": len(xwalk.get("anchors", {})), "hold": hold}

    try:
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_partner_proposals.py")],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=120,
        )
        results["validate_partner_proposals"] = {
            "exit_code": proc.returncode,
            "tail": proc.stdout.splitlines()[-8:] + proc.stderr.splitlines()[-4:],
        }
    except Exception as exc:
        results["validate_partner_proposals"] = {"error": str(exc)}

    try:
        proc = subprocess.run(
            ["node", str(ROOT / "scripts" / "build-site.mjs")],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=180,
        )
        line = next((ln for ln in proc.stdout.splitlines() if f"/{TGT_PARTNER}" in ln), None)
        results["build_site"] = {"exit_code": proc.returncode, "partner_line": line}
    except Exception as exc:
        results["build_site"] = {"error": str(exc)}

    return results


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-sheet", action="store_true", help="Skip Drive sheet create/upload")
    ap.add_argument("--skip-sidecar", action="store_true")
    args = ap.parse_args()

    if not SRC_PITCH.is_file():
        raise SystemExit(f"Missing source {SRC_PITCH}")

    partner = build_partner_doc()
    save_json(TGT_PITCH, partner)
    save_json(TGT_DC, partner)

    crosswalk = build_crosswalk(partner)
    save_json(CROSSWALK_OUT, crosswalk)

    finance_copied = copy_finance_recal()

    sheet_result = None
    if not args.skip_sheet:
        proc = subprocess.run(
            [
                sys.executable,
                str(ROOT / "finance" / "publish_partner_economics.py"),
                TGT_PARTNER,
                "--title",
                "Navier — LINE MAN Wongnai Thailand Unit Economics",
            ],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=300,
        )
        sheet_result = {
            "exit_code": proc.returncode,
            "stdout": proc.stdout[-2000:] if proc.stdout else "",
            "stderr": proc.stderr[-1000:] if proc.stderr else "",
        }
        if proc.returncode == 0:
            partner = load_json(TGT_PITCH)
            save_json(TGT_DC, partner)

    sidecar_result = None
    if not args.skip_sidecar:
        by_script = ROOT / "scripts" / "grok-bolt-yango" / "build_economics_sidecar.py"
        text = by_script.read_text()
        if TGT_PARTNER not in text:
            text = text.replace(
                f'    "{SRC_PARTNER}",',
                f'    "{SRC_PARTNER}",\n    "{TGT_PARTNER}",',
            )
            by_script.write_text(text)
        proc = subprocess.run(
            [
                sys.executable,
                str(by_script),
                "--dc",
                str(ROOT / "data-clean"),
                "--corridors",
                str(ROOT / "finance" / "recal" / f"corridors-{TGT_PARTNER}.json"),
                "--aggdir",
                str(ROOT / "finance" / "recal"),
                "--url-map",
                str(ROOT / "finance" / "economics_url_map.json"),
            ],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=120,
        )
        sidecar_result = {"exit_code": proc.returncode, "tail": (proc.stdout or proc.stderr)[-500:]}

    validations = run_validations()
    report = {
        "at": utc_now(),
        "mirror_of": SRC_PARTNER,
        "partner": TGT_PARTNER,
        "outputs": {
            "partner_pitch": str(TGT_PITCH.relative_to(ROOT)),
            "data_clean": str(TGT_DC.relative_to(ROOT)),
            "crosswalk": str(CROSSWALK_OUT.relative_to(ROOT)),
            "finance_copied": finance_copied,
            "sheet_xlsx": f"finance/_refresh_{TGT_PARTNER}.xlsx",
        },
        "sheet": sheet_result,
        "sidecar": sidecar_result,
        "validations": validations,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    save_json(REPORT, report)
    print(json.dumps(report, indent=2))
    return 0 if validations.get("build_site", {}).get("exit_code") == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())