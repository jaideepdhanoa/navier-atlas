"""Market-slide marquee route lists: 4 routes, amber bullet + white body."""
from __future__ import annotations

import json
from pathlib import Path

from deck_edit_ops import STYLE_FIELDS, golden_style_to_api, make_op

ROOT = Path(__file__).resolve().parents[1]

MARKET_ROUTE_AMBER = [0.773, 0.616, 0.373]
MARKET_ROUTE_WHITE = [1.0, 1.0, 1.0]
MARKET_ROUTE_DARK = [0.12, 0.12, 0.12]
MARKET_ROUTE_FONT = {"font": "Exo 2", "sizePt": 11, "bold": True}

ROUTE_TARGET_OIDS = frozenset(
    {
        "g3eec5122801_0_114",
        "g3eec5122801_0_209",
        "g3eec5122801_0_301",
        "g3eec5122801_0_683",
        "g3eec5122801_0_696",
        "g3eec5122801_0_709",
        "g3eec5122801_0_722",
        "g3eec5122801_0_735",
        "g3ea5e0fb254_4_362",
    }
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def load_market_route_bindings(deck_key: str) -> dict:
    path = ROOT / f"decks/{deck_key}/market-route-bindings.json"
    if not path.exists():
        raise FileNotFoundError(f"Missing market-route-bindings.json for deck {deck_key}")
    return load_json(path)


def load_partner_markets(partner_json_path: Path) -> dict[str, dict]:
    doc = load_json(partner_json_path)
    return {m["id"]: m for m in doc.get("markets", [])}


def _short_label(journey: dict) -> str:
    raw_from = journey["from"]
    if "leeward embarkation" in raw_from.lower():
        frm = "Piscadera"
    elif "→" in raw_from:
        frm = raw_from.split("→")[-1].split("(")[0].strip()
    else:
        frm = raw_from.split("(")[0].strip()
    if " / " in frm:
        frm = frm.split(" / ")[0].strip()
    to = journey["to"].split("(")[0].strip()
    for suffix in (" day-trip jetty", " Luxury Resort", " Resort"):
        if to.endswith(suffix):
            to = to[: -len(suffix)].strip()
    if to.startswith("Sandals Royal"):
        to = "Sandals"
    return f"{frm} → {to}"


def _distance_label(journey: dict) -> str:
    nm = journey.get("distance_nm")
    if nm is None:
        return ""
    return f"~{nm:g} nm"


def _default_tagline(journey: dict) -> str:
    text = (journey.get("with_navier") or "").strip()
    if not text:
        return "foiling run, in-app"
    text = text.removeprefix("A ").removeprefix("An ")
    if len(text) > 42:
        text = text[:39].rstrip() + "…"
    return text


def format_route_block(
    journey: dict,
    *,
    tagline: str | None = None,
    label: str | None = None,
) -> str:
    title = label or _short_label(journey)
    dist = _distance_label(journey)
    detail = tagline or _default_tagline(journey)
    if dist:
        detail_line = f"      {dist} · {detail}"
    else:
        detail_line = f"      {detail}"
    return f"▸  {title}\n{detail_line}"


def format_route_list(
    journeys: list[dict],
    *,
    taglines: list[str] | None = None,
    labels: list[str] | None = None,
) -> str:
    blocks: list[str] = []
    for i, journey in enumerate(journeys):
        tag = taglines[i] if taglines and i < len(taglines) else None
        label = labels[i] if labels and i < len(labels) else None
        blocks.append(format_route_block(journey, tagline=tag, label=label))
    return "\n\n".join(blocks)


def market_route_style_ranges(text: str, *, text_surface: str = "dark") -> list[dict]:
    """Amber ▸; route title bold; indented distance/tag line regular (not bold)."""
    runs: list[dict] = []
    body_color = MARKET_ROUTE_DARK if text_surface == "light" else MARKET_ROUTE_WHITE
    white_bold = {**MARKET_ROUTE_FONT, "color": body_color}
    white_reg = {**MARKET_ROUTE_FONT, "bold": False, "color": body_color}
    amber = {**MARKET_ROUTE_FONT, "color": MARKET_ROUTE_AMBER}
    i = 0
    while i < len(text):
        if text[i] == "▸":
            runs.append({"start": i, "end": i + 1, "style": amber})
            i += 1
            continue
        line_end = text.find("\n", i)
        if line_end == -1:
            line_end = len(text)
        line = text[i:line_end]
        is_detail = line.startswith("      ")
        style = white_reg if is_detail else white_bold
        if line:
            runs.append({"start": i, "end": line_end, "style": style})
        i = line_end + 1 if line_end < len(text) else line_end
    return runs


def market_route_replace_ops(
    slide_object_id: str,
    target_object_id: str,
    new_text: str,
    element: dict,
    *,
    op_prefix: str,
    source_pointer: str,
    text_surface: str = "dark",
) -> list[dict]:
    budget = element.get("char_budget", 9999)
    if len(new_text) > budget:
        raise ValueError(
            f"{target_object_id}: route text len {len(new_text)} exceeds char_budget {budget}"
        )

    ops: list[dict] = []
    ops.append(
        make_op(
            f"{op_prefix}-clear",
            slide_object_id,
            target_object_id,
            {"deleteText": {"objectId": target_object_id, "textRange": {"type": "ALL"}}},
            rationale=f"Clear market routes on {target_object_id}",
            source_pointer=source_pointer,
        )
    )
    ops.append(
        make_op(
            f"{op_prefix}-insert",
            slide_object_id,
            target_object_id,
            {"insertText": {"objectId": target_object_id, "text": new_text, "insertionIndex": 0}},
            rationale=f"Insert 4 marquee routes on {target_object_id}",
            source_pointer=source_pointer,
        )
    )

    for i, run in enumerate(market_route_style_ranges(new_text, text_surface=text_surface)):
        style = golden_style_to_api(run["style"])
        ops.append(
            make_op(
                f"{op_prefix}-style-{i}",
                slide_object_id,
                target_object_id,
                {
                    "updateTextStyle": {
                        "objectId": target_object_id,
                        "textRange": {
                            "type": "FIXED_RANGE",
                            "startIndex": run["start"],
                            "endIndex": run["end"],
                        },
                        "style": style,
                        "fields": STYLE_FIELDS,
                    }
                },
                rationale=f"Amber bullet / white body styling on {target_object_id}",
                source_pointer=source_pointer,
            )
        )

    ops.append(
        make_op(
            f"{op_prefix}-para",
            slide_object_id,
            target_object_id,
            {
                "updateParagraphStyle": {
                    "objectId": target_object_id,
                    "textRange": {"type": "ALL"},
                    "style": {"alignment": "START"},
                    "fields": "alignment",
                }
            },
            rationale=f"Left-align market routes on {target_object_id}",
            source_pointer=source_pointer,
        )
    )
    return ops


def resolve_binding_routes(
    binding: dict,
    markets: dict[str, dict],
    *,
    partner_root_journeys: list[dict] | None = None,
) -> tuple[list[dict] | None, str, str | None]:
    if binding.get("static_text"):
        source = binding.get("source_pointer", "market-route-bindings.json static_text")
        return None, source, binding["static_text"]

    if binding.get("routes"):
        journeys = binding["routes"]
        source = binding.get("source_pointer", "market-route-bindings.json explicit routes")
        return journeys, source, None

    pool: list[dict]
    source: str
    if binding.get("journey_pool") == "partner_root":
        pool = partner_root_journeys or []
        source = binding.get("source_pointer", "partner_json journeys_unlocked (root)")
    else:
        market = markets[binding["market_id"]]
        pool = market.get("journeys_unlocked", [])
        source = f"data-clean/partners/{binding.get('market_id')}.json journeys_unlocked"
    indices = binding.get("journey_indices", list(range(4)))
    journeys = [pool[i] for i in indices]
    return journeys, source, None


def build_market_route_ops(
    golden: dict,
    deck_key: str,
    *,
    partner_json_path: Path,
    element_lookup,
) -> list[dict]:
    bindings_doc = load_market_route_bindings(deck_key)
    partner_doc = load_json(partner_json_path)
    markets = load_partner_markets(partner_json_path)
    root_journeys = partner_doc.get("journeys_unlocked", [])
    ops: list[dict] = []

    for binding in bindings_doc["bindings"]:
        journeys, source, static_text = resolve_binding_routes(
            binding, markets, partner_root_journeys=root_journeys
        )
        if static_text is not None:
            text = static_text
        else:
            text = format_route_list(
                journeys or [],
                taglines=binding.get("taglines"),
                labels=binding.get("labels"),
            )
        slide_oid = binding["slide_object_id"]
        target_oid = binding["target_object_id"]
        el = element_lookup(golden, target_oid)
        ops.extend(
            market_route_replace_ops(
                slide_oid,
                target_oid,
                text,
                el,
                op_prefix=f"{deck_key}-market-routes-{target_oid}",
                source_pointer=source,
                text_surface=binding.get("text_surface", "dark"),
            )
        )
    return ops


def validate_market_route_bindings(deck_key: str, *, partner_json_path: Path, golden: dict) -> list[str]:
    errors: list[str] = []
    bindings_doc = load_market_route_bindings(deck_key)
    partner_doc = load_json(partner_json_path)
    markets = load_partner_markets(partner_json_path)
    root_journeys = partner_doc.get("journeys_unlocked", [])

    for binding in bindings_doc["bindings"]:
        slide_idx = binding.get("slide_index")
        target_oid = binding["target_object_id"]
        try:
            if binding.get("static_text"):
                text = binding["static_text"]
                journeys = []
            elif binding.get("routes"):
                journeys = binding["routes"]
            elif binding.get("journey_pool") == "partner_root":
                pool = root_journeys
                for i in binding.get("journey_indices", []):
                    if i >= len(pool):
                        errors.append(f"slide {slide_idx}: journey index {i} out of range (partner_root)")
            else:
                market = markets.get(binding.get("market_id", ""))
                if not market:
                    errors.append(f"slide {slide_idx}: unknown market_id {binding.get('market_id')}")
                    continue
                pool = market.get("journeys_unlocked", [])
                for i in binding.get("journey_indices", []):
                    if i >= len(pool):
                        errors.append(f"slide {slide_idx}: journey index {i} out of range")
            journeys, _, static_text = resolve_binding_routes(
                binding, markets, partner_root_journeys=root_journeys
            )
            if static_text is not None:
                text = static_text
                journeys = []
            else:
                text = format_route_list(
                    journeys or [],
                    taglines=binding.get("taglines"),
                    labels=binding.get("labels"),
                )
            el = None
            for slide in golden.get("slides", []):
                for elem in slide.get("elements", []):
                    if elem.get("oid") == target_oid:
                        el = elem
                        break
            budget = (el or {}).get("char_budget", 9999)
            if not binding.get("static_text") and len(journeys) != 4:
                errors.append(f"slide {slide_idx}: expected 4 routes, got {len(journeys)}")
            if len(text) > budget:
                errors.append(
                    f"slide {slide_idx} ({target_oid}): text len {len(text)} > char_budget {budget}"
                )
        except Exception as exc:  # noqa: BLE001 — validation aggregator
            errors.append(f"slide {slide_idx}: {exc}")
    return errors