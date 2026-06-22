#!/usr/bin/env python3
"""Grok-autonomous deck hygiene: golden-map enrich, manifest wire, asset publish."""
from __future__ import annotations

import json
import mimetypes
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Grab gold deck slide-1 + narrative image roles (from ASSET-REGISTRY + parity diagnosis)
GRAB_ROLE_BY_OID: dict[str, str] = {
    "p1_i2": "cover_hero",
    "p1_i4": "navier_logo",
    "p1_i5": "partner_logo",
    "p1_i8": "hero.title",
    "p1_i9": "hero.subtitle",
}

GRAB_ROLE_BY_SLIDE_INDEX: dict[int, dict[str, str]] = {
    2: {"value_prop_bg": "g3f139a0b6ec_0_1"},
    10: {"tam_bg": "navierBg_s26"},
    11: {"partner_roles_bg": "g3ea5e0fb254_4_358"},
}

TEXT_ROLE_HINTS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"WHAT ONE BOAT EARNS", re.I), "econ.header_market"),
    (re.compile(r"profitable from year one", re.I), "econ.title"),
    (re.compile(r"→|·\s*~?\d", re.I), "econ.route_line"),
    (re.compile(r"revenue\s*−|profit / boat", re.I), "econ.summary_line"),
    (re.compile(r"^Energy$", re.I), "opex.energy"),
    (re.compile(r"Captain", re.I), "opex.crew"),
    (re.compile(r"Marina", re.I), "opex.marina"),
    (re.compile(r"Maintenance", re.I), "opex.maintenance"),
    (re.compile(r"Insurance", re.I), "opex.insurance"),
    (re.compile(r"Charging berth|Fast-charge", re.I), "opex.charging_berth"),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def infer_text_role(text: str) -> str | None:
    if not text or not text.strip():
        return None
    for pat, role in TEXT_ROLE_HINTS:
        if pat.search(text):
            return role
    if len(text) < 40:
        return "text.short"
    return "text.body"


def enrich_golden_map(path: Path) -> dict:
    data = load_json(path)
    meta = data.setdefault("_meta", {})
    meta["enriched_at"] = utc_now()
    meta["enrichment"] = "deck_autonomy_sync.py: roles + char_budget + runs"

    stats = {"elements": 0, "roles_assigned": 0, "char_budgets": 0, "runs": 0}

    for slide in data.get("slides", []):
        idx = slide.get("index")
        slide_role = slide.get("role")
        if idx == 1:
            pass  # per-element below
        if idx in GRAB_ROLE_BY_SLIDE_INDEX:
            for role, oid in GRAB_ROLE_BY_SLIDE_INDEX[idx].items():
                for el in slide.get("elements", []):
                    if el.get("oid") == oid:
                        el["role"] = role
                        stats["roles_assigned"] += 1

        for el in slide.get("elements", []):
            stats["elements"] += 1
            oid = el.get("oid", "")
            if oid in GRAB_ROLE_BY_OID:
                el["role"] = GRAB_ROLE_BY_OID[oid]
                stats["roles_assigned"] += 1
            elif el.get("kind") == "image" and not el.get("role"):
                if slide_role == "cover" or idx == 1:
                    el["role"] = "cover.decor"
                else:
                    el["role"] = "image.unassigned"
                stats["roles_assigned"] += 1

            text = el.get("text")
            if text is not None:
                inferred = infer_text_role(text)
                if inferred and not el.get("role"):
                    el["role"] = inferred
                    stats["roles_assigned"] += 1
                el["char_budget"] = len(text)
                stats["char_budgets"] += 1
                style = el.get("style")
                if style:
                    el["runs"] = [
                        {
                            "start": 0,
                            "end": len(text),
                            "text": text,
                            "style": style,
                        }
                    ]
                    stats["runs"] += 1

    data["_meta"]["enrichment_stats"] = stats
    write_json(path, data)
    return stats


def registry_object_map(registry: dict, deck_key: str = "grab") -> dict[str, dict]:
    out: dict[str, dict] = {}
    for key, asset in registry.get("assets", {}).items():
        for use in asset.get("used_by", []):
            if use.get("deck") == deck_key and use.get("target_object_id"):
                out[use["target_object_id"]] = {
                    "registry_key": key,
                    "role": asset.get("role"),
                    "asset": asset,
                }
    return out


def wire_grab_image_manifest(
    manifest_path: Path,
    golden_path: Path,
    registry_path: Path,
) -> dict:
    manifest = load_json(manifest_path)
    golden = load_json(golden_path)
    registry = load_json(registry_path)
    reg_map = registry_object_map(registry, "grab")

    slide_oid_by_index = {
        s["index"]: s.get("pageObjectId") for s in golden.get("slides", [])
    }

    role_to_oid: dict[str, str] = {}
    for slide in golden.get("slides", []):
        for el in slide.get("elements", []):
            if el.get("role") and el.get("oid"):
                role_to_oid[el["role"]] = el["oid"]

    wired = 0
    for img in manifest.get("images", []):
        role = img.get("role")
        if role and role in role_to_oid:
            img["target_object_id"] = role_to_oid[role]
            wired += 1
        idx = img.get("target_slide_index")
        if idx and idx in slide_oid_by_index:
            img["target_slide_object_id"] = slide_oid_by_index[idx]
        elif img.get("target_object_id"):
            # find slide containing object
            for slide in golden.get("slides", []):
                for el in slide.get("elements", []):
                    if el.get("oid") == img["target_object_id"]:
                        img["target_slide_object_id"] = slide.get("pageObjectId")
                        break

        oid = img.get("target_object_id")
        if oid and oid in reg_map:
            img["registry_key"] = reg_map[oid]["registry_key"]
            if img.get("status") in ("placeholder", "registry_asset"):
                img["status"] = "checked_in"

    manifest["wired_at"] = utc_now()
    manifest["wired_by"] = "deck_autonomy_sync.py"
    write_json(manifest_path, manifest)
    return {"images": len(manifest.get("images", [])), "wired_target_object_id": wired}


def publish_assets_to_drive(registry_path: Path, *, dry_run: bool = False) -> dict:
    """Upload checked-in local assets missing source_url; update registry."""
    registry = load_json(registry_path)
    assets = registry.get("assets", {})
    published = []
    skipped = []
    errors = []

    if dry_run:
        for key, asset in assets.items():
            if asset.get("local_path") and not asset.get("source_url"):
                published.append({"image_key": key, "dry_run": True, "local_path": asset["local_path"]})
        return {"dry_run": True, "would_publish": len(published), "items": published[:10]}

    try:
        sys.path.insert(0, str(ROOT / "builders"))
        from deck_studio.cli import get_drive_service  # type: ignore
    except Exception as e:
        return {"error": f"drive_unavailable: {e}", "skipped": len(assets)}

    service = get_drive_service()
    folder_id = os.environ.get("DECK_ASSETS_DRIVE_FOLDER_ID")

    for key, asset in assets.items():
        local = asset.get("local_path")
        if not local or asset.get("source_url"):
            skipped.append(key)
            continue
        rel = local
        if rel.startswith("deck-studio/"):
            rel = rel[len("deck-studio/") :]
        path = ROOT / rel
        if not path.is_file():
            errors.append({"key": key, "error": "missing_local", "path": str(path)})
            continue
        mime, _ = mimetypes.guess_type(path.name)
        meta: dict = {"name": path.name}
        if folder_id:
            meta["parents"] = [folder_id]
        try:
            from googleapiclient.http import MediaFileUpload  # type: ignore

            media = MediaFileUpload(str(path), mimetype=mime or "application/octet-stream", resumable=True)
            created = (
                service.files()
                .create(body=meta, media_body=media, fields="id,webViewLink")
                .execute()
            )
            fid = created["id"]
            try:
                service.permissions().create(
                    fileId=fid,
                    body={"type": "anyone", "role": "reader"},
                    fields="id",
                ).execute()
            except Exception:
                pass
            asset["drive_file_id"] = fid
            asset["source_url"] = f"https://drive.google.com/uc?export=download&id={fid}"
            if asset.get("status") == "checked_in":
                asset["status"] = "published"
            published.append({"image_key": key, "drive_file_id": fid})
        except Exception as e:
            errors.append({"key": key, "error": str(e)})

    registry.setdefault("_meta", {})["last_asset_publish_at"] = utc_now()
    write_json(registry_path, registry)
    return {"published": len(published), "skipped": len(skipped), "errors": errors, "items": published}


def scaffold_bolt_binding(grab_binding_path: Path, bolt_binding_path: Path) -> None:
    """Bolt uses same gold-template object IDs; clone binding with bolt leak denylist."""
    grab = load_json(grab_binding_path)
    bolt = json.loads(json.dumps(grab))
    bolt["deck_key"] = "bolt"
    bolt["partner_slug"] = "bolt"
    bolt["generated_from"] = "grab/economics-binding.json"
    bolt["purpose"] = (
        "Bolt field→object_id binding (identical object IDs — gold-template copy). "
        "Values pulled live from Bolt transparent sheet; scope Europe/Gulf only."
    )
    bolt["leak_denylist_examples"] = [
        "Marina Bay",
        "Sentosa",
        "Singapore",
        "Phuket",
        "Bali",
        "Grab",
        "Malaysia",
        "Mexico",
        "Morocco",
        "$480,870",
        "$211,622",
    ]
    bolt["scope_guardrail"] = {
        "allowed": ["Greece", "Croatia", "Italy", "France", "Côte d'Azur", "UAE", "Saudi", "Jeddah", "Red Sea"],
        "forbidden": ["Malaysia", "Mexico", "Morocco"],
    }
    bolt["updated_at"] = utc_now()
    write_json(bolt_binding_path, bolt)


def scaffold_bolt_editplan(
    bolt_config_path: Path,
    grab_golden_path: Path,
    out_path: Path,
) -> None:
    cfg = load_json(bolt_config_path)
    golden = load_json(grab_golden_path)
    plan = {
        "deck_key": "bolt",
        "partner_slug": "bolt",
        "presentation_id": None,
        "gold_template_id": "18yDAgO0Sj9PJlgf6paxtgni8Pk1xRAmNwE2TD_NCdSs",
        "deprecated_sandbox_id": cfg.get("deck_id"),
        "mode": "slides_api_batch_update",
        "status": "scaffold_pending_gold_copy",
        "safety": {
            "no_pptx_roundtrip": True,
            "no_full_deck_replace": True,
            "preserve_object_ids": True,
            "human_review_required_for_external_send": True,
        },
        "qa_gates": [
            "drift_gate",
            "leak_denylist",
            "style_reset_scan",
            "char_budget_scan",
            "image_inheritance_scan",
            "render_thumbnails",
        ],
        "leak_denylist": [
            "Marina Bay",
            "Sentosa",
            "Grab",
            "Malaysia",
            "Mexico",
            "Morocco",
        ],
        "operations": [],
        "notes": (
            "Scaffold only. Copy gold deck to new presentation_id, then populate operations "
            "from golden-template-map + bolt/economics-binding.json + ASSET-REGISTRY."
        ),
        "golden_slide_count": len(golden.get("slides", [])),
        "created_at": utc_now(),
    }
    write_json(out_path, plan)


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Deck autonomy sync")
    ap.add_argument("--root", default=str(ROOT))
    ap.add_argument(
        "command",
        choices=["enrich-golden", "wire-manifests", "publish-assets", "bolt-scaffold", "all"],
    )
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    root = Path(args.root)

    report: dict = {"command": args.command, "at": utc_now()}

    if args.command in ("enrich-golden", "all"):
        gp = root / "decks/grab/golden-template-map.json"
        report["enrich_golden"] = enrich_golden_map(gp)

    if args.command in ("wire-manifests", "all"):
        report["wire_grab"] = wire_grab_image_manifest(
            root / "decks/grab/image-manifest.json",
            root / "decks/grab/golden-template-map.json",
            root / "assets/ASSET-REGISTRY.json",
        )

    if args.command in ("publish-assets", "all"):
        report["publish_assets"] = publish_assets_to_drive(
            root / "assets/ASSET-REGISTRY.json", dry_run=args.dry_run
        )

    if args.command in ("bolt-scaffold", "all"):
        scaffold_bolt_binding(
            root / "decks/grab/economics-binding.json",
            root / "decks/bolt/economics-binding.json",
        )
        scaffold_bolt_editplan(
            root / "decks/bolt/deck.config.json",
            root / "decks/grab/golden-template-map.json",
            root / "decks/bolt/deck.editplan.json",
        )
        report["bolt_scaffold"] = {
            "economics_binding": "decks/bolt/economics-binding.json",
            "editplan": "decks/bolt/deck.editplan.json",
        }

    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())