"""Resolve deck hyperlink targets and emit Slides API link ops (white Poppins links)."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from deck_edit_ops import clear_hyperlink_op, link_replace_op, white_link_replace_op

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent

DEFAULT_ATLAS_BASE = os.environ.get("ATLAS_BASE_URL", "https://navier-atlas.vercel.app").rstrip("/")
ECON_URL_MAP = REPO_ROOT / "finance" / "economics_url_map.json"

LABEL_INTERACTIVE = "Interactive link"
LABEL_MODEL_DEEPDIVE = "Model deepdive"
LABEL_TAM_SIZING = "Detailed market sizing"
LINK_STYLE_PRESERVE = "preserve_element"
LINK_STYLE_INLINE_PHRASE = "inline_phrase"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def bindings_path(deck_key: str) -> Path:
    return ROOT / "decks" / deck_key / "slide-link-bindings.json"


def load_link_bindings_doc(deck_key: str) -> dict:
    path = bindings_path(deck_key)
    if not path.is_file():
        raise FileNotFoundError(f"Missing slide-link-bindings.json for deck {deck_key!r}: {path}")
    return load_json(path)


def link_oid_for_label(golden: dict, slide_index: int, label: str) -> str | None:
    target = label.strip().lower()
    for slide in golden.get("slides", []):
        if slide.get("index") != slide_index:
            continue
        for el in slide.get("elements", []):
            if (el.get("text") or "").strip().lower() == target:
                return el.get("oid")
    return None


def link_oid_for_label_on_slide(golden: dict, slide_object_id: str, label: str) -> str | None:
    """Resolve link object_id by stable slide object_id (post slide-2 insert safe)."""
    target = label.strip().lower()
    for slide in golden.get("slides", []):
        if slide.get("pageObjectId") != slide_object_id:
            continue
        for el in slide.get("elements", []):
            if (el.get("text") or "").strip().lower() == target:
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


def resolve_atlas_market_url(
    *,
    partner_id: str,
    partner_doc: dict,
    city_id: str,
    link_target: str = "market",
    atlas_base: str = DEFAULT_ATLAS_BASE,
    market_slug_override: str | None = None,
) -> tuple[str, str]:
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
        return (f"{atlas_base}/city/{city_id}", f"aggregate city page ({city_id})")

    return (f"{atlas_base}/{partner_id}", f"partner hub page ({partner_id})")


def resolve_partner_hub_url(*, partner_id: str, atlas_base: str = DEFAULT_ATLAS_BASE) -> tuple[str, str]:
    return (f"{atlas_base}/{partner_id}", f"partner Atlas proposal hub ({partner_id})")


def resolve_economics_url(deck_key: str, doc: dict, deck_cfg: dict, partner_doc: dict) -> tuple[str, str]:
    if deck_cfg.get("economics_url"):
        return deck_cfg["economics_url"], "deck.config.json economics_url"
    partner_id = doc.get("partner_id") or deck_key
    if partner_doc.get("economics_url"):
        return partner_doc["economics_url"], f"partner_json economics_url ({partner_id})"
    if ECON_URL_MAP.is_file():
        url = load_json(ECON_URL_MAP).get("economics_url", {}).get(partner_id)
        if url:
            return url, f"finance/economics_url_map.json ({partner_id})"
    raise SystemExit(f"No economics_url for deck {deck_key!r}")


def partner_doc_path(doc: dict) -> Path:
    rel = doc.get("partner_json", f"data-clean/partners/{doc.get('partner_id')}.json")
    return REPO_ROOT / rel


def econ_model_link_bindings(deck_key: str) -> list[dict]:
    path = ROOT / "decks" / deck_key / "economics-binding.json"
    if not path.is_file():
        return []
    econ = load_json(path)
    rows: list[dict] = []
    for slide in econ.get("economics_slides", []):
        model = (slide.get("fields") or {}).get("model_link")
        if not model or not model.get("object_id"):
            continue
        rows.append(
            {
                "slide_index": slide["slide_index"],
                "slide_object_id": slide["slide_object_id"],
                "link_object_id": model["object_id"],
                "link_role": "economics_sheet",
                "label": model.get("sample", LABEL_MODEL_DEEPDIVE),
            }
        )
    return rows


def phrase_text_range(body_text: str, phrase: str) -> dict[str, int]:
    start = body_text.index(phrase)
    return {"startIndex": start, "endIndex": start + len(phrase)}


def close_atlas_link_binding(deck_key: str) -> dict | None:
    doc = load_link_bindings_doc(deck_key)
    close = doc.get("close_atlas_link")
    if not close:
        return None
    return {
        "slide_index": close["slide_index"],
        "slide_object_id": close["slide_object_id"],
        "title_object_id": close.get("title_object_id"),
        "link_object_id": close["link_object_id"],
        "link_role": close.get("link_role", "atlas_partner_hub"),
        "link_phrase": close.get("link_phrase"),
        "body_text": close.get("body_text"),
        "label": close.get("label"),
        "link_style": close.get("link_style", LINK_STYLE_INLINE_PHRASE),
    }


def tam_sizing_link_binding(deck_key: str, golden: dict) -> dict | None:
    doc = load_link_bindings_doc(deck_key)
    tam = doc.get("tam_sizing_link")
    if tam:
        return {
            "slide_index": tam["slide_index"],
            "slide_object_id": tam["slide_object_id"],
            "link_object_id": tam["link_object_id"],
            "link_role": "economics_sheet",
            "label": tam.get("label", LABEL_TAM_SIZING),
        }
    oid = link_oid_for_label(golden, 10, LABEL_TAM_SIZING)
    if not oid:
        return None
    slide_oid = None
    for slide in golden.get("slides", []):
        if slide.get("index") == 10:
            slide_oid = slide.get("pageObjectId")
            break
    if not slide_oid:
        return None
    return {
        "slide_index": 10,
        "slide_object_id": slide_oid,
        "link_object_id": oid,
        "link_role": "economics_sheet",
        "label": LABEL_TAM_SIZING,
    }


def merged_bindings(deck_key: str, *, golden: dict | None = None) -> list[dict]:
    doc = load_link_bindings_doc(deck_key)
    golden = golden or load_json(ROOT / "decks/grab/golden-template-map.json")
    rows = list(doc.get("bindings", []))
    seen = {r["slide_index"] for r in rows}
    for row in econ_model_link_bindings(deck_key):
        if row["slide_index"] not in seen:
            rows.append(row)
            seen.add(row["slide_index"])
    tam = tam_sizing_link_binding(deck_key, golden)
    if tam and tam["slide_index"] not in seen:
        rows.append(tam)
        seen.add(tam["slide_index"])
    close = close_atlas_link_binding(deck_key)
    if close and close["slide_index"] not in seen:
        rows.append(close)
        seen.add(close["slide_index"])
    rows.sort(key=lambda r: r["slide_index"])
    return rows


def resolve_binding_url(
    binding: dict,
    *,
    doc: dict,
    deck_cfg: dict,
    partner_doc: dict,
) -> dict[str, Any]:
    role = binding.get("link_role", "atlas_market")
    partner_id = doc.get("partner_id") or doc.get("deck_key")
    atlas_base = doc.get("atlas_base_url", DEFAULT_ATLAS_BASE)

    if role == "atlas_partner_hub":
        url, note = resolve_partner_hub_url(partner_id=partner_id, atlas_base=atlas_base)
    elif role == "atlas_market":
        url, note = resolve_atlas_market_url(
            partner_id=partner_id,
            partner_doc=partner_doc,
            city_id=binding["atlas_city_id"],
            link_target=binding.get("link_target", "market"),
            atlas_base=atlas_base,
            market_slug_override=binding.get("atlas_market_slug"),
        )
    elif role == "economics_sheet":
        url, note = resolve_economics_url(doc.get("deck_key", partner_id), doc, deck_cfg, partner_doc)
    else:
        raise SystemExit(f"Unknown link_role {role!r} on slide {binding.get('slide_index')}")

    return {
        "slide_index": binding["slide_index"],
        "link_role": role,
        "link_object_id": binding["link_object_id"],
        "slide_object_id": binding["slide_object_id"],
        "url": url,
        "resolution": note,
        "label": binding.get("label"),
    }


def validate_link_bindings(deck_key: str, *, golden: dict | None = None) -> list[str]:
    doc = load_link_bindings_doc(deck_key)
    golden = golden or load_json(ROOT / "decks/grab/golden-template-map.json")
    deck_cfg = load_json(ROOT / f"decks/{deck_key}/deck.config.json")
    partner_doc = load_json(partner_doc_path(doc))
    errors: list[str] = []

    try:
        resolve_economics_url(deck_key, doc, deck_cfg, partner_doc)
    except SystemExit as exc:
        errors.append(str(exc))

    seen: set[int] = set()
    for b in merged_bindings(deck_key, golden=golden):
        idx = b.get("slide_index")
        if idx in seen:
            errors.append(f"duplicate slide_index {idx} in merged link bindings")
        seen.add(idx)

        role = b.get("link_role", "atlas_market")
        for field in ("slide_object_id", "link_object_id", "link_role"):
            if not b.get(field):
                errors.append(f"slide {idx}: missing {field}")

        if role == "atlas_market" and not b.get("atlas_city_id"):
            errors.append(f"slide {idx}: atlas_market requires atlas_city_id")

        link_style = b.get("link_style")
        label = b.get("label", LABEL_INTERACTIVE)
        if role in ("atlas_market", "atlas_partner_hub") and link_style not in (
            LINK_STYLE_PRESERVE,
            LINK_STYLE_INLINE_PHRASE,
        ):
            label = LABEL_INTERACTIVE
        if link_style == LINK_STYLE_PRESERVE:
            if not b.get("label"):
                errors.append(f"slide {idx}: preserve_element close link requires label")
        elif link_style == LINK_STYLE_INLINE_PHRASE:
            phrase = b.get("link_phrase")
            body_text = b.get("body_text")
            if not phrase:
                errors.append(f"slide {idx}: inline_phrase requires link_phrase")
            if not body_text:
                errors.append(f"slide {idx}: inline_phrase requires body_text")
            elif phrase and phrase not in body_text:
                errors.append(f"slide {idx}: link_phrase {phrase!r} not found in body_text")
        else:
            slide_oid = b.get("slide_object_id")
            expected_oid = (
                link_oid_for_label_on_slide(golden, slide_oid, label)
                if slide_oid
                else link_oid_for_label(golden, idx, label)
            )
            if expected_oid and b.get("link_object_id") != expected_oid:
                errors.append(
                    f"slide {idx}: link_object_id {b.get('link_object_id')!r} != golden {expected_oid!r} ({label})"
                )

    return errors


def build_inline_phrase_link_ops(
    binding: dict,
    *,
    url: str,
    resolution: str,
    op_prefix: str,
) -> list[dict]:
    body_text = binding["body_text"]
    phrase = binding["link_phrase"]
    text_range = {"type": "FIXED_RANGE", **phrase_text_range(body_text, phrase)}
    idx = binding["slide_index"]
    role = binding.get("link_role", "atlas_partner_hub")
    source = f"slide-link-bindings.json slide {idx} ({resolution})"
    ops: list[dict] = []
    title_oid = binding.get("title_object_id")
    if title_oid:
        ops.append(
            clear_hyperlink_op(
                binding["slide_object_id"],
                title_oid,
                op_key=f"{op_prefix}-s{idx:02d}-{role}-title-clear",
                source_pointer=source,
            )
        )
    ops.append(
        white_link_replace_op(
            binding["slide_object_id"],
            binding["link_object_id"],
            url,
            op_key=f"{op_prefix}-s{idx:02d}-{role}-inline",
            source_pointer=source,
            text_range=text_range,
        )
    )
    return ops


def build_deck_link_ops(deck_key: str, *, op_prefix: str | None = None) -> list[dict]:
    doc = load_link_bindings_doc(deck_key)
    golden = load_json(ROOT / "decks/grab/golden-template-map.json")
    deck_cfg = load_json(ROOT / f"decks/{deck_key}/deck.config.json")
    partner_doc = load_json(partner_doc_path(doc))
    prefix = op_prefix or f"{deck_key}-deck-link"
    ops: list[dict] = []
    for binding in merged_bindings(deck_key, golden=golden):
        resolved = resolve_binding_url(
            binding, doc=doc, deck_cfg=deck_cfg, partner_doc=partner_doc
        )
        role = binding.get("link_role", "atlas_market")
        link_style = binding.get("link_style")
        if link_style == LINK_STYLE_INLINE_PHRASE:
            ops.extend(
                build_inline_phrase_link_ops(
                    binding,
                    url=resolved["url"],
                    resolution=resolved["resolution"],
                    op_prefix=prefix,
                )
            )
            continue
        op_factory = white_link_replace_op if link_style == LINK_STYLE_PRESERVE else link_replace_op
        ops.append(
            op_factory(
                binding["slide_object_id"],
                binding["link_object_id"],
                resolved["url"],
                op_key=f"{prefix}-s{binding['slide_index']:02d}-{role}",
                source_pointer=(
                    f"slide-link-bindings.json slide {binding['slide_index']} "
                    f"({resolved['resolution']})"
                ),
            )
        )
    return ops


def cmd_validate(deck_key: str) -> int:
    doc = load_link_bindings_doc(deck_key)
    golden = load_json(ROOT / "decks/grab/golden-template-map.json")
    deck_cfg = load_json(ROOT / f"decks/{deck_key}/deck.config.json")
    partner_doc = load_json(partner_doc_path(doc))
    errs = validate_link_bindings(deck_key, golden=golden)
    resolved = [
        resolve_binding_url(b, doc=doc, deck_cfg=deck_cfg, partner_doc=partner_doc)
        for b in merged_bindings(deck_key, golden=golden)
    ]
    print(json.dumps({"status": "fail" if errs else "pass", "errors": errs, "resolved": resolved}, indent=2))
    return 1 if errs else 0


def cmd_apply(deck_key: str, *, presentation_id: str | None = None) -> int:
    from deck_bolt_pilot import apply_plan, load_json as pilot_load, write_json

    golden = pilot_load(ROOT / "decks/grab/golden-template-map.json")
    errs = validate_link_bindings(deck_key, golden=golden)
    if errs:
        raise SystemExit("slide-link-bindings invalid:\n" + "\n".join(errs))

    cfg = pilot_load(ROOT / f"decks/{deck_key}/deck.config.json")
    pid = presentation_id or cfg.get("deck_id")
    if not pid:
        raise SystemExit("presentation_id required")

    doc = load_link_bindings_doc(deck_key)
    deck_cfg = pilot_load(ROOT / f"decks/{deck_key}/deck.config.json")
    partner_doc = pilot_load(partner_doc_path(doc))
    ops = build_deck_link_ops(deck_key)
    plan = {
        "deck_key": deck_key,
        "presentation_id": pid,
        "mode": "deck_link_ops_only",
        "operations": ops,
    }
    out = ROOT / f"decks/{deck_key}/deck.link-ops.json"
    write_json(out, plan)
    applied = apply_plan(plan, chunk_size=20)
    resolved = [
        resolve_binding_url(b, doc=doc, deck_cfg=deck_cfg, partner_doc=partner_doc)
        for b in merged_bindings(deck_key, golden=golden)
    ]
    print(json.dumps({"applied_ops": applied, "presentation_id": pid, "resolved": resolved}, indent=2))
    return 0


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Deck hyperlink wiring (Atlas + economics sheet)")
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