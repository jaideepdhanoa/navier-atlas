"""Shared slide→image binding loader for partner decks (Grab gold template family)."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def bindings_path(deck_key: str) -> Path:
    return ROOT / "decks" / deck_key / "slide-image-bindings.json"


def load_slide_bindings(deck_key: str) -> dict:
    path = bindings_path(deck_key)
    if not path.is_file():
        raise FileNotFoundError(f"Missing slide-image-bindings.json for deck {deck_key!r}: {path}")
    return load_json(path)


def bindings_for_role(bindings_doc: dict, role: str) -> list[dict]:
    return [b for b in bindings_doc.get("bindings", []) if b.get("image_role") == role]


def atlas_bindings(bindings_doc: dict) -> list[dict]:
    return bindings_for_role(bindings_doc, "atlas_route_screenshot")


def image_op_bindings(bindings_doc: dict, *, roles: set[str] | None = None) -> dict[str, tuple[str, str, str]]:
    """registry_key -> (slide_object_id, target_object_id, replace_method)."""
    out: dict[str, tuple[str, str, str]] = {}
    for b in bindings_doc.get("bindings", []):
        role = b.get("image_role")
        key = b.get("registry_key")
        if not key:
            continue
        if roles is not None and role not in roles:
            continue
        out[key] = (
            b["slide_object_id"],
            b["target_object_id"],
            b.get("apply_method", "CENTER_CROP"),
        )
    return out


def image_bindings_list(bindings_doc: dict, *, roles: set[str] | None = None) -> list[dict]:
    rows: list[dict] = []
    for b in bindings_doc.get("bindings", []):
        key = b.get("registry_key")
        if not key:
            continue
        if roles is not None and b.get("image_role") not in roles:
            continue
        rows.append(
            {
                "registry": key,
                "slide_oid": b["slide_object_id"],
                "target_oid": b["target_object_id"],
                "method": b.get("apply_method", "CENTER_CROP"),
                "image_role": b.get("image_role"),
                "slide_index": b.get("slide_index"),
            }
        )
    return rows


def validate_bindings(bindings_doc: dict) -> list[str]:
    """Return human-readable errors; empty list means OK."""
    errors: list[str] = []
    families = bindings_doc.get("slide_families", {})
    for b in bindings_doc.get("bindings", []):
        idx = b.get("slide_index")
        family_key = b.get("slide_family")
        role = b.get("image_role")
        fam = families.get(family_key, {})
        if idx not in fam.get("slides", []):
            errors.append(f"slide {idx}: family {family_key!r} does not list this slide index")
        if fam.get("image_role") and fam.get("image_role") != role:
            errors.append(f"slide {idx}: role {role!r} != family role {fam.get('image_role')!r}")
        key = b.get("registry_key")
        if role == "econ_market_bg" and not key:
            errors.append(f"slide {idx}: econ_market_bg missing registry_key")
        if role == "atlas_route_screenshot" and not key:
            errors.append(f"slide {idx}: atlas_route_screenshot requires registry_key (atlas-bolt-slide*)")
        if role == "atlas_route_screenshot" and key and not str(key).startswith("atlas-"):
            errors.append(f"slide {idx}: atlas registry_key must start with atlas-")
        if role == "econ_market_bg" and not str(b.get("target_object_id", "")).startswith("navierBg_"):
            errors.append(
                f"slide {idx}: econ_market_bg target must be navierBg_* full-bleed slot, got {b.get('target_object_id')!r}"
            )
        if role == "atlas_route_screenshot" and str(b.get("target_object_id", "")).startswith("navierBg_"):
            errors.append(f"slide {idx}: atlas slide must not target navierBg_* (econ slot)")
    # No duplicate registry on different slides unless intentional reuse (econ keys are 1:1)
    seen: dict[str, int] = {}
    for b in bindings_doc.get("bindings", []):
        key = b.get("registry_key")
        if not key:
            continue
        if key in seen and seen[key] != b.get("slide_index"):
            errors.append(
                f"registry {key!r} bound to slides {seen[key]} and {b.get('slide_index')} — ambiguous"
            )
        seen[key] = b.get("slide_index")
    return errors