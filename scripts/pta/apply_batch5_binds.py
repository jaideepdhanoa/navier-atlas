#!/usr/bin/env python3
"""Apply R4c batch-5 aspirational-chip → sealed-corridor binds from BATCH5-BIND-MAP.json."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MAP = (
    ROOT
    / "handoff/partner-map-model/pta-remediation/dossiers/R4/BATCH5-BIND-MAP.json"
)
DC_PARTNERS = ROOT / "data-clean" / "partners"
PP_PARTNERS = ROOT / "partner-pitch" / "partners"
ROUTES_PATH = ROOT / "data-clean" / "ROUTES.json"

BATCH5_PARTNERS = frozenset(
    {
        "singapore-mpa",
        "abu-dhabi-itc",
        "bahrain-motc",
        "dubai-rta",
        "qatar",
        "rakta",
    }
)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def normalize_label(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip()).lower()


def split_label(label: str) -> tuple[str, str] | None:
    for sep in ("↔", "→", "←", "—", "–"):
        if sep in label:
            left, right = label.split(sep, 1)
            return left.strip(), right.strip()
    return None


def chip_endpoints(chip: dict) -> tuple[str, str] | None:
    if chip.get("from") and chip.get("to"):
        return str(chip["from"]), str(chip["to"])
    label = chip.get("label")
    if label:
        parts = split_label(label)
        if parts:
            return parts
    return None


def labels_match(chip_from: str, chip_to: str, bind_from: str, bind_to: str) -> bool:
    cf, ct = normalize_label(chip_from), normalize_label(chip_to)
    bf, bt = normalize_label(bind_from), normalize_label(bind_to)
    if cf == bf and ct == bt:
        return True
    return (bf in cf or cf in bf) and (bt in ct or ct in bt)


def economics_hash(partner: dict) -> str:
    payload = {
        "economics_status": partner.get("economics_status"),
        "growth_case": partner.get("growth_case"),
    }
    blob = json.dumps(payload, sort_keys=True, ensure_ascii=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def chip_economics_hashes(partner: dict) -> dict[str, str]:
    """Per-chip economics_status for --verify-economics-hash (journeys + featured)."""
    out: dict[str, str] = {}
    for coll, key in (
        (partner.get("journeys_unlocked") or [], "journeys"),
        (
            [
                fr
                for ph in partner.get("phases") or []
                for fr in ph.get("featured_routes") or []
            ],
            "featured",
        ),
    ):
        for chip in coll:
            ep = chip_endpoints(chip)
            if not ep:
                continue
            k = f"{key}|{normalize_label(ep[0])}|{normalize_label(ep[1])}"
            out[k] = hashlib.sha256(
                json.dumps(chip.get("economics_status"), sort_keys=True).encode()
            ).hexdigest()
    return out


def find_chips(partner: dict, bind_from: str, bind_to: str) -> list[tuple[dict, str]]:
    hits: list[tuple[dict, str]] = []
    for chip in partner.get("journeys_unlocked") or []:
        ep = chip_endpoints(chip)
        if ep and labels_match(ep[0], ep[1], bind_from, bind_to):
            hits.append((chip, "journeys_unlocked"))
    for phase in partner.get("phases") or []:
        for chip in phase.get("featured_routes") or []:
            ep = chip_endpoints(chip)
            if ep and labels_match(ep[0], ep[1], bind_from, bind_to):
                hits.append((chip, f"phases[{phase.get('n')}].featured_routes"))
    return hits


def apply_bind_sealed(chip: dict, bind: dict) -> list[str]:
    changes: list[str] = []
    rid = bind["route_id"]
    dist = bind["sealed_distance_nm"]

    if chip.get("route_id") != rid:
        chip["route_id"] = rid
        changes.append("route_id")
    if chip.get("route_ids") != [rid]:
        chip["route_ids"] = [rid]
        changes.append("route_ids")
    if chip.get("distance_nm") != dist:
        chip["distance_nm"] = dist
        changes.append("distance_nm")
    for field, val in (
        ("_link_status", "sealed"),
        ("_link_kind", "sealed"),
        ("display", "interactive"),
        ("render", "sealed-solid"),
    ):
        if chip.get(field) != val:
            chip[field] = val
            changes.append(field)
    return changes


def apply_keep_aspirational(chip: dict) -> list[str]:
    changes: list[str] = []
    if chip.get("route_id") is not None:
        chip["route_id"] = None
        changes.append("route_id=null")
    if chip.get("route_ids") is not None:
        chip["route_ids"] = None
        changes.append("route_ids=null")
    for field, val in (
        ("_link_status", "aspirational-no-built-route"),
        ("_link_kind", "aspirational-chip"),
    ):
        if chip.get(field) != val:
            chip[field] = val
            changes.append(field)
    return changes


def save_partner(path: Path, partner: dict) -> None:
    ascii = "data-clean" in path.parts
    path.write_text(
        json.dumps(partner, indent=2, ensure_ascii=ascii) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Apply batch-5 chip bind map")
    ap.add_argument("--map", type=Path, default=DEFAULT_MAP, help="BATCH5-BIND-MAP.json path")
    ap.add_argument("--dry-run", action="store_true", help="Preview binds without writing")
    ap.add_argument("--apply", action="store_true", help="Write partner JSON updates")
    ap.add_argument(
        "--verify-economics-hash",
        action="store_true",
        help="Abort if per-chip economics_status changes during apply",
    )
    args = ap.parse_args()

    if args.apply and args.dry_run:
        print("✗ pass only one of --dry-run or --apply", file=sys.stderr)
        return 2
    if not args.apply and not args.dry_run:
        args.dry_run = True

    if not args.map.is_file():
        print(f"✗ bind map not found: {args.map}", file=sys.stderr)
        return 1

    bind_doc = json.loads(args.map.read_text())
    binds: dict[str, list[dict]] = bind_doc.get("binds") or {}

    routes_raw = json.loads(ROUTES_PATH.read_text())
    route_ids = {
        (r.get("properties") or {}).get("id")
        for r in (routes_raw if isinstance(routes_raw, list) else routes_raw.get("features") or [])
    }
    route_ids.discard(None)

    sealed_total = 0
    aspirational_total = 0
    missing_chips: list[dict] = []
    missing_routes: list[str] = []
    all_changes: list[dict] = []
    partners_to_write: list[tuple[Path, dict, str]] = []

    for slug, entries in binds.items():
        if slug not in BATCH5_PARTNERS:
            print(f"⚠ unknown batch-5 partner in map: {slug}", file=sys.stderr)

        for tree_name, base in (("data-clean", DC_PARTNERS), ("partner-pitch", PP_PARTNERS)):
            path = base / f"{slug}.json"
            if not path.is_file():
                print(f"✗ missing partner JSON: {path}", file=sys.stderr)
                return 1

        dc_partner = json.loads((DC_PARTNERS / f"{slug}.json").read_text())
        pre_hash = economics_hash(dc_partner)
        pre_chip_hashes = chip_economics_hashes(dc_partner) if args.verify_economics_hash else {}

        partner_changes: list[dict] = []
        for bind in entries:
            action = bind.get("action")
            if action == "bind_sealed":
                sealed_total += 1
                rid = bind.get("route_id")
                if rid and rid not in route_ids:
                    missing_routes.append(rid)
            elif action == "keep_aspirational":
                aspirational_total += 1
            else:
                print(f"✗ unknown action {action!r} for {slug}", file=sys.stderr)
                return 1

            chips = find_chips(dc_partner, bind["from"], bind["to"])
            if not chips:
                missing_chips.append(
                    {"partner": slug, "from": bind["from"], "to": bind["to"], "action": action}
                )
                continue

            for chip, loc in chips:
                if action == "bind_sealed":
                    changed = apply_bind_sealed(chip, bind)
                else:
                    changed = apply_keep_aspirational(chip)

                if changed:
                    partner_changes.append(
                        {
                            "location": loc,
                            "from": bind["from"],
                            "to": bind["to"],
                            "action": action,
                            "fields": changed,
                        }
                    )

        post_hash = economics_hash(dc_partner)
        if pre_hash != post_hash:
            print(
                f"✗ economics_status/growth_case changed for {slug} during bind prep",
                file=sys.stderr,
            )
            return 1

        if args.verify_economics_hash:
            post_chip_hashes = chip_economics_hashes(dc_partner)
            for key, h in pre_chip_hashes.items():
                if post_chip_hashes.get(key) != h:
                    print(
                        f"✗ chip economics_status changed for {slug} key={key}",
                        file=sys.stderr,
                    )
                    return 1

        all_changes.append({"partner": slug, "changes": partner_changes, "economics_hash": pre_hash})
        partners_to_write.append((DC_PARTNERS / f"{slug}.json", dc_partner, pre_hash))

    soft_verify = (bind_doc.get("_grok_apply_block") or {}).get("verify_before_ship") or []
    if soft_verify:
        print("\nsoft_verify (manual confirm before ship):")
        for entry in soft_verify:
            print(
                f"  • {entry.get('partner')}: {entry.get('chip')} — {entry.get('reason')}"
            )
            if entry.get("recommended"):
                print(f"    recommended: {entry['recommended']}")

    if missing_routes:
        print("✗ route_ids missing from ROUTES.json:", sorted(set(missing_routes)), file=sys.stderr)
        return 1

    if missing_chips:
        print("✗ chips not matched in partner JSON:", file=sys.stderr)
        for m in missing_chips:
            print(f"  {m['partner']}: {m['from']} → {m['to']} ({m['action']})", file=sys.stderr)
        return 1

    report = {
        "generated_at": utc_now(),
        "map": str(args.map.relative_to(ROOT)),
        "mode": "apply" if args.apply else "dry-run",
        "acceptance": {
            "bind_sealed": sealed_total,
            "keep_aspirational": aspirational_total,
            "expect_sealed": 18,
            "expect_aspirational": 6,
        },
        "partners": all_changes,
    }
    print(json.dumps(report, indent=2))

    acc = report["acceptance"]
    print(
        f"\nacceptance: {acc['bind_sealed']} sealed + {acc['keep_aspirational']} aspirational "
        f"(expect {acc['expect_sealed']}+{acc['expect_aspirational']})"
    )

    if args.apply:
        pre_hashes = {p["partner"]: p["economics_hash"] for p in all_changes}
        for dc_path, dc_partner, _ in partners_to_write:
            slug = dc_path.stem
            if economics_hash(dc_partner) != pre_hashes[slug]:
                print(f"✗ economics hash drift before write for {slug}", file=sys.stderr)
                return 1
            save_partner(dc_path, dc_partner)

            pp_path = PP_PARTNERS / f"{slug}.json"
            pp_partner = json.loads(pp_path.read_text())
            pp_pre = economics_hash(pp_partner)
            for bind in binds[slug]:
                for chip, _ in find_chips(pp_partner, bind["from"], bind["to"]):
                    if bind["action"] == "bind_sealed":
                        apply_bind_sealed(chip, bind)
                    else:
                        apply_keep_aspirational(chip)
            if economics_hash(pp_partner) != pp_pre:
                print(f"✗ economics_status/growth_case changed for {slug} (partner-pitch)", file=sys.stderr)
                return 1
            save_partner(pp_path, pp_partner)
            print(f"✓ applied {slug} → {dc_path.name} + partner-pitch")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())