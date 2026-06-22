"""Resolve Navier Atlas share URLs and emit Slides API link ops for market side-panel slides."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from deck_edit_ops import link_replace_op, make_op

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent

DEFAULT_ATLAS_BASE = os.environ.get("ATLAS_BASE_URL", "https://navier-atlas.vercel.app").rstrip("/")
INTERACTIVE_LINK_LABEL = "Interactive link"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def bindings_path(deck_key: str) -> Path:
    return ROOT / "decks" / deck_key / "slide-link-bindings.json"


def load_link_bindings(deck_key: str) -> dict:
    path = bindings_path(deck_key)
    if not path.is_file():
        raise FileNotFoundError(f"Missing slide-link-bindings.json for deck {deck_key!r}: {path}")
    return load_json(path)


def interactive_link_oid(golden: dict, slide_index: int) -> str | None:
    for slide in golden.get("slides", []):
        if slide.get("index") != slide_index:
            continue
        for el in slide.get("elements", []):
            if (el.get("text") or "").strip() == INTERACTIVE_LINK_LABEL:
                return el.get("oid")
    return None


def _market_city_ids(market: dict) -> set[str]:
    ids: set[str] = set(market.get("anchor_cities") or [])
    for phase in market.get("phases") or []:
        ids.update(phase.get("cities") or [])
    return ids


def find_market_for_city(partner_doc: dict, city_id: str) -> dict | None:
    for market in partner_doc.get("markets") or []:
        if city_id in _market_city_ids(market):
            return market
    for market in partner_doc.get("markets") or []:
        for journey in market.get("journeys_unlocked") or []:
            nodes = {journey.get("from_node_id"), journey.get("to_node_id")}
            if city_id in nodes:
                return market
    return None


def resolve_atlas_url(
    *,
    partner_id: str,
    partner_doc: dict,
    city_id: str,
    link_target: str = "market",
    atlas_base: str = DEFAULT_ATLAS_BASE,
    market_slug_override: str | None = None,
) -> tuple[str, str]:
    """Return (url, resolution_note)."""
    layout = partner_doc.get("layout", "hub")
    market = None
    if market_slug_override:
        for m in partner_doc.get("markets") or []:
            if m.get("slug") == market_slug_override or m.get("id") == market_slug_override:
                market = m
                break
    if market is None:
        market = find_market_for_city(partner_doc, city_id)

    if market and layout in ("hub", "network"):
        mslug = market.get("slug") or market.get("id")
        if link_target == "city":
            return (
                f"{atlas_base}/{partner_id}/{mslug}/city/{city_id}",
                f"partner market city page ({mslug}/{city_id})",
            )
        return (
            f"{atlas_base}/{partner_id}/{mslug}",
            f"partner market sub-proposal ({mslug})",
        )

    if link_target == "city":
        return (
            f"{atlas_base}/city/{city_id}",
            f"aggregate city page ({city_id})",
        )

    return (
        f"{atlas_base}/{partner_id}",
        f"partner hub page ({partner_id})",
    )


def resolve_binding_url(doc: dict, binding: dict, partner_doc: dict) -> dict[str, Any]:
    partner_id = doc.get("partner_id") or doc.get("deck_key")
    url, note = resolve_atlas_url(
        partner_id=partner_id,
        partner_doc=partner_doc,
        city_id=binding["atlas_city_id"],
        link_target=binding.get("link_target", "market"),
        atlas_base=doc.get("atlas_base_url", DEFAULT_ATLAS_BASE),
        market_slug_override=binding.get("atlas_market_slug"),
    )
    return {
        "slide_index": binding["slide_index"],
        "link_object_id": binding["link_object_id"],
        "slide_object_id": binding["slide_object_id"],
        "atlas_city_id": binding["atlas_city_id"],
        "url": url,
        "resolution": note,
    }


def validate_link_bindings(doc: dict, *, golden: dict | None = None) -> list[str]:
    errors: list[str] = []
    seen_slides: set[int] = set()
    for b in doc.get("bindings", []):
        idx = b.get("slide_index")
        if idx in seen_slides:
            errors.append(f"duplicate slide_index {idx} in link bindings")
        seen_slides.add(idx)
        for field in ("slide_object_id", "link_object_id", "atlas_city_id"):
            if not b.get(field):
                errors.append(f"slide {idx}: missing {field}")
        if golden is not None:
            expected = interactive_link_oid(golden, idx)
            if expected and b.get("link_object_id") != expected:
                errors.append(
                    f"slide {idx}: link_object_id {b.get('link_object_id')!r} != golden {expected!r}"
                )
    return errors


def build_atlas_link_ops(
    doc: dict,
    partner_doc: dict,
    *,
    op_prefix: str | None = None,
) -> list[dict]:
    prefix = op_prefix or f"{doc.get('deck_key', 'deck')}-atlas-link"
    ops: list[dict] = []
    for binding in doc.get("bindings", []):
        resolved = resolve_binding_url(doc, binding, partner_doc)
        ops.append(
            link_replace_op(
                binding["slide_object_id"],
                binding["link_object_id"],
                resolved["url"],
                op_key=f"{prefix}-s{binding['slide_index']:02d}",
                source_pointer=(
                    f"slide-link-bindings.json slide {binding['slide_index']} "
                    f"({resolved['resolution']})"
                ),
            )
        )
    return ops


def partner_doc_path(doc: dict) -> Path:
    rel = doc.get("partner_json", f"data-clean/partners/{doc.get('partner_id')}.json")
    return REPO_ROOT / rel


def cmd_validate(deck_key: str) -> int:
    doc = load_link_bindings(deck_key)
    golden = load_json(ROOT / "decks/grab/golden-template-map.json")
    partner_doc = load_json(partner_doc_path(doc))
    errs = validate_link_bindings(doc, golden=golden)
    resolved = [resolve_binding_url(doc, b, partner_doc) for b in doc.get("bindings", [])]
    print(json.dumps({"status": "fail" if errs else "pass", "errors": errs, "resolved": resolved}, indent=2))
    return 1 if errs else 0


def cmd_apply(deck_key: str, *, presentation_id: str | None = None) -> int:
    from deck_bolt_pilot import apply_plan, load_json as pilot_load, write_json

    doc = load_link_bindings(deck_key)
    golden = pilot_load(ROOT / "decks/grab/golden-template-map.json")
    partner_doc = pilot_load(partner_doc_path(doc))
    errs = validate_link_bindings(doc, golden=golden)
    if errs:
        raise SystemExit("slide-link-bindings.json invalid:\n" + "\n".join(errs))

    cfg = pilot_load(ROOT / f"decks/{deck_key}/deck.config.json")
    pid = presentation_id or cfg.get("deck_id")
    if not pid:
        raise SystemExit("presentation_id required")

    ops = build_atlas_link_ops(doc, partner_doc)
    plan = {
        "deck_key": deck_key,
        "presentation_id": pid,
        "mode": "atlas_link_ops_only",
        "operations": ops,
    }
    out = ROOT / f"decks/{deck_key}/deck.link-ops.json"
    write_json(out, plan)
    applied = apply_plan(plan, chunk_size=20)
    resolved = [resolve_binding_url(doc, b, partner_doc) for b in doc.get("bindings", [])]
    print(json.dumps({"applied_ops": applied, "presentation_id": pid, "resolved": resolved}, indent=2))
    return 0


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Atlas interactive link wiring for partner decks")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_val = sub.add_parser("validate-bindings")
    p_val.add_argument("--deck", default="bolt")
    p_apply = sub.add_parser("apply")
    p_apply.add_argument("--deck", default="bolt")
    p_apply.add_argument("--presentation-id", default=None)
    args = ap.parse_args()
    if args.cmd == "validate-bindings":
        return cmd_validate(args.deck)
    if args.cmd == "apply":
        return cmd_apply(args.deck, presentation_id=args.presentation_id)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())