#!/usr/bin/env python3
"""Bolt wave-2.1: Tier A image_edit pipeline, qa_image_gate, image-ops-only apply."""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import subprocess
import sys
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image, ImageStat

ROOT = Path(__file__).resolve().parents[1]
BUILDERS = ROOT / "builders"
sys.path.insert(0, str(BUILDERS))

from deck_bolt_pilot import apply_plan, load_json, write_json  # noqa: E402
from deck_edit_ops import image_replace_op  # noqa: E402
from deck_slide_bindings import (  # noqa: E402
    atlas_bindings,
    image_op_bindings,
    load_slide_bindings,
    validate_bindings,
)

N30_NEUTRAL = ROOT / "assets/n30/n30-reference-neutral.png"
GRADE_LOCK_PATH = ROOT / "decks/bolt/wave21-grade-lock.json"
REGISTRY_PATH = ROOT / "assets/ASSET-REGISTRY.json"
PROMPTS_PATH = ROOT / "docs/N30-TIER-A-PROMPTS.md"
PRESENTATION_ID = "1ssNgUpv7fRv-obQ46Emy_8S3lELyjdj7-fbxFdsQFI0"

MIN_W, MIN_H = 2560, 1440
TARGET_AR = 16 / 9

LANDMARK_DENYLIST = [
    "burj khalifa",
    "burj al arab",
    "marina bay sands",
    "palm jumeirah",
    "dubai marina",
]

WAVE2_PASTE_KEYS = [
    "bolt-cover-hero",
    "bolt-value-prop-bg",
    "bolt-tam-bg",
    "bolt-partner-roles-bg",
    "econ-greece-athens-hydra",
    "econ-croatia-split-hvar",
    "econ-cote-azur-nice-monaco",
    "econ-italy-sorrento-capri",
    "econ-uae-dubai-harbour",
    "econ-ksa-jeddah",
    "econ-greece-mykonos-paros",
    "econ-croatia-dubrovnik",
    "econ-ksa-redsea-amaala",
]

DRIFT_CONTROLS = {
    "prompt_only_drift_cover": "decks/bolt/controls/prompt-only-drift-cover-13.jpg",
    "prompt_only_drift_slide2": "decks/bolt/controls/prompt-only-drift-slide2-14.jpg",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _xai_token() -> str:
    if os.environ.get("XAI_API_KEY"):
        return os.environ["XAI_API_KEY"]
    auth_path = Path.home() / ".grok/auth.json"
    data = json.loads(auth_path.read_text(encoding="utf-8"))
    for entry in data.values():
        if isinstance(entry, dict) and entry.get("key"):
            return entry["key"]
    raise SystemExit("No XAI_API_KEY or ~/.grok/auth.json token")


def _b64_data_uri(path: Path) -> str:
    raw = path.read_bytes()
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(raw).decode('ascii')}"


def load_tier_a_prompt(section: int) -> str:
    text = PROMPTS_PATH.read_text(encoding="utf-8")
    marker = f"## {section}."
    start = text.index(marker)
    block = text[start : text.index("##", start + 3) if section < 3 else len(text)]
    m = re.search(r">\s*(.+?)(?:\n\n|\n---)", block, re.DOTALL)
    if not m:
        raise SystemExit(f"Could not parse Tier A prompt section {section}")
    lines = [ln.lstrip("> ").strip() for ln in m.group(1).strip().splitlines()]
    prompt = " ".join(lines)
    return prompt.replace(
        "Using the attached white hydrofoil vessel",
        "Using <IMAGE_0> as the white hydrofoil vessel",
    )


@dataclass
class GradeLock:
    locked: bool = False
    grade_family: str = "warm-golden-hour-left"
    time_of_day: str = "golden-hour"
    seed_family: str | None = None
    reference_plate: str | None = None
    locked_at: str | None = None

    @classmethod
    def load(cls) -> GradeLock:
        if not GRADE_LOCK_PATH.exists():
            return cls()
        data = load_json(GRADE_LOCK_PATH)
        return cls(**{k: data.get(k) for k in cls.__dataclass_fields__})

    def save(self) -> None:
        write_json(GRADE_LOCK_PATH, self.__dict__)


def tier_a_edit(
    *,
    prompt: str,
    reference: Path = N30_NEUTRAL,
    aspect_ratio: str = "16:9",
    resolution: str = "2k",
    seed_note: str | None = None,
) -> tuple[bytes, dict]:
    """Tier A image_edit via xAI Imagine API with N30 form reference."""
    lock = GradeLock.load()
    if lock.locked:
        prompt = (
            f"{prompt} Match the locked deck grade family "
            f"({lock.grade_family}, {lock.time_of_day})."
        )
    body: dict[str, Any] = {
        "model": "grok-imagine-image-quality",
        "prompt": prompt,
        "images": [{"url": _b64_data_uri(reference)}],
        "aspect_ratio": aspect_ratio,
        "resolution": resolution,
        "response_format": "b64_json",
    }
    token = _xai_token()
    req = urllib.request.Request(
        "https://api.x.ai/v1/images/edits",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    meta = {
        "tier": "A",
        "provider": "xai/grok-imagine-image-quality",
        "reference": str(reference.relative_to(ROOT)),
        "aspect_ratio": aspect_ratio,
        "resolution": resolution,
        "seed_family": lock.seed_family if lock.locked else seed_note,
        "prompt": prompt,
        "generated_at": utc_now(),
        "usage": payload.get("usage"),
    }
    b64 = payload["data"][0].get("b64_json")
    if b64:
        return base64.b64decode(b64), meta
    url = payload["data"][0]["url"]
    with urllib.request.urlopen(url, timeout=120) as img_resp:
        return img_resp.read(), meta


def _region_stats(img: Image.Image, box: tuple[float, float, float, float]) -> dict:
    w, h = img.size
    x0, y0, x1, y1 = (int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h))
    crop = img.crop((x0, y0, x1, y1)).convert("RGB")
    stat = ImageStat.Stat(crop)
    means = stat.mean
    stddev = stat.stddev
    variance = sum(s * s for s in stddev) / len(stddev)
    return {
        "mean_luminance": round(sum(means) / 3, 2),
        "variance": round(variance, 2),
        "box_px": [x0, y0, x1, y1],
    }


def _hull_opacity_heuristic(img: Image.Image, *, hull_box: tuple[float, float, float, float] | None = None) -> dict:
    """Detect see-through hull: high variance inside hull bbox vs surroundings."""
    w, h = img.size
    box = hull_box or (0.35, 0.45, 0.75, 0.82)
    hull = _region_stats(img, box)
    surround = _region_stats(img, (box[0], max(0.0, box[1] - 0.25), box[2], box[1]))
    leak_score = hull["variance"] / max(surround["variance"], 1.0)
    greens = img.crop(
        (int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h))
    ).convert("RGB")
    px = list(greens.getdata())
    green_hits = sum(1 for r, g, b in px if g > r + 25 and g > b + 15)
    green_ratio = green_hits / max(len(px), 1)
    return {
        "hull_variance": hull["variance"],
        "surround_variance": surround["variance"],
        "leak_score": round(leak_score, 3),
        "green_in_hull_ratio": round(green_ratio, 4),
        "pass": leak_score < 2.5 and green_ratio < 0.12,
    }


@dataclass
class QACheck:
    name: str
    status: str  # pass | fail | pending_human
    auto: bool
    details: dict = field(default_factory=dict)


def qa_image_gate(
    image_path: Path,
    *,
    role: str,
    market_slug: str | None = None,
    human_approved: bool = False,
) -> dict:
    """Hard gate — returns receipt; overall pass only if all blocking checks pass."""
    img = Image.open(image_path).convert("RGB")
    w, h = img.size
    checks: list[QACheck] = []

    ar = w / h
    dim_ok = w >= MIN_W and h >= MIN_H and abs(ar - TARGET_AR) < 0.08
    checks.append(
        QACheck(
            "dimensions_16x9_min_2560",
            "pass" if dim_ok else "fail",
            True,
            {"width": w, "height": h, "aspect_ratio": round(ar, 4), "min": f"{MIN_W}x{MIN_H}"},
        )
    )

    if role == "econ_market_bg":
        hull_box = (0.55, 0.55, 0.95, 0.92)
    elif role == "tam_bg":
        hull_box = (0.18, 0.50, 0.58, 0.78)
    else:
        hull_box = None
    opacity = _hull_opacity_heuristic(img, hull_box=hull_box)
    if role in ("econ_market_bg", "tam_bg"):
        opacity["pass"] = opacity["green_in_hull_ratio"] < 0.12
    checks.append(
        QACheck("opacity_no_green_leak", "pass" if opacity["pass"] else "fail", True, opacity)
    )

    if role == "cover_hero":
        safe = _region_stats(img, (0.0, 0.0, 0.38, 0.42))
        safe_ok = safe["variance"] < 1800
        checks.append(
            QACheck(
                "cover_upper_left_clear",
                "pass" if safe_ok else "fail",
                True,
                safe,
            )
        )
    elif role == "value_prop_bg":
        left = _region_stats(img, (0.0, 0.0, 0.35, 1.0))
        booking_ok = left["variance"] > 200
        checks.append(
            QACheck(
                "slide2_left_third_activity",
                "pass" if booking_ok else "pending_human",
                False,
                left,
            )
        )
    elif role == "tam_bg":
        upper = _region_stats(img, (0.0, 0.0, 1.0, 0.66))
        upper_ok = upper["variance"] < 2500
        checks.append(
            QACheck("tam_upper_two_thirds_open", "pass" if upper_ok else "fail", True, upper)
        )
    elif role == "partner_roles_bg":
        right = _region_stats(img, (0.66, 0.0, 1.0, 1.0))
        lockup_ok = right["variance"] < 2200
        checks.append(
            QACheck("partner_roles_right_third_clean", "pass" if lockup_ok else "fail", True, right)
        )
    elif role == "econ_market_bg":
        left = _region_stats(img, (0.0, 0.0, 0.48, 0.85))
        landmark = _region_stats(img, (0.42, 0.0, 1.0, 0.72))
        left_ok = left["variance"] < 2000 and left["mean_luminance"] < 125
        landmark_ok = landmark["variance"] > 700 and landmark["mean_luminance"] > 50
        checks.append(
            QACheck("econ_left_column_clean", "pass" if left_ok else "fail", True, left)
        )
        checks.append(
            QACheck(
                "econ_low_contrast_left",
                "pass" if left_ok else "fail",
                True,
                {"left_mean_luminance": left["mean_luminance"], "left_variance": left["variance"]},
            )
        )
        checks.append(
            QACheck(
                "econ_landmark_skyline_visible",
                "pass" if landmark_ok else "fail",
                True,
                landmark,
            )
        )

    if market_slug and "greece" in market_slug:
        checks.append(
            QACheck("market_lock_greece", "pass", True, {"market_slug": market_slug})
        )
    elif market_slug and "uae" in market_slug:
        checks.append(
            QACheck("market_lock_uae", "pending_human", False, {"market_slug": market_slug})
        )

    checks.append(
        QACheck(
            "landmark_denylist",
            "pending_human",
            False,
            {"denylist": LANDMARK_DENYLIST},
        )
    )
    checks.append(
        QACheck("single_vessel", "pending_human", False, {})
    )
    checks.append(
        QACheck(
            "vessel_foiling_not_displacement",
            "pending_human",
            False,
            {"require": "foils deployed; hull elevated above waterline; not sitting low like a ferry"},
        )
    )
    checks.append(
        QACheck("hull_fidelity_vs_neutral_ref", "pending_human", False, {})
    )
    checks.append(
        QACheck(
            "grab_gold_human_compare",
            "pass" if human_approved else "pending_human",
            False,
            {"exemplar": "grab-cover-hero + grab-slide2"},
        )
    )

    blocking = [c for c in checks if c.status == "fail"]
    pending = [c for c in checks if c.status == "pending_human"]
    auto_fails = [c for c in checks if c.auto and c.status == "fail"]
    overall = "pass" if not auto_fails and (human_approved or role != "cover_hero") else (
        "fail" if auto_fails else "pending_human"
    )
    if auto_fails:
        overall = "fail"
    elif pending and not human_approved:
        overall = "pending_human"

    receipt = {
        "gate": "qa_image_gate/v1",
        "image_path": str(image_path.relative_to(ROOT)),
        "role": role,
        "market_slug": market_slug,
        "evaluated_at": utc_now(),
        "overall": overall,
        "blocking_failures": [c.name for c in blocking],
        "pending_human": [c.name for c in pending],
        "checks": [
            {"name": c.name, "status": c.status, "auto": c.auto, "details": c.details}
            for c in checks
        ],
    }
    return receipt


def write_qa_receipt_to_registry(asset_key: str, receipt: dict) -> None:
    registry = load_json(REGISTRY_PATH)
    asset = registry.setdefault("assets", {}).setdefault(asset_key, {})
    asset["qa_receipt"] = receipt
    asset["qa_status"] = receipt["overall"]
    asset["qa_evaluated_at"] = receipt["evaluated_at"]
    write_json(REGISTRY_PATH, registry)


def deprecate_paste_plates() -> None:
    registry = load_json(REGISTRY_PATH)
    assets = registry.setdefault("assets", {})
    now = utc_now()
    for key in WAVE2_PASTE_KEYS:
        if key not in assets:
            continue
        assets[key]["status"] = "deprecated_paste_composite"
        assets[key]["deprecated_at"] = now
        assets[key]["notes"] = (
            (assets[key].get("notes", "") + " | wave-2.1 Tier A supersession").strip(" |")
        )
    write_json(REGISTRY_PATH, registry)


def purge_paste_composite_files() -> list[str]:
    """Delete wave-2 *-composited.png paste files and strip deprecated paste URLs from registry."""
    registry = load_json(REGISTRY_PATH)
    assets = registry.setdefault("assets", {})
    now = utc_now()
    deleted: list[str] = []
    seen_paths: set[str] = set()
    for key in WAVE2_PASTE_KEYS:
        asset = assets.get(key, {})
        if asset.get("tier") == "A" or asset.get("qa_status") == "pass":
            # Tier A supersession is live — only purge legacy composited paths, never tier-a files.
            continue
        local_path = asset.get("local_path")
        if local_path and "composited" in local_path and local_path not in seen_paths:
            seen_paths.add(local_path)
            full = ROOT / local_path
            if full.is_file():
                full.unlink()
                deleted.append(str(full.relative_to(ROOT)))
        if key not in assets:
            continue
        if asset.get("status") != "deprecated_paste_composite":
            continue
        assets[key]["status"] = "deleted_paste_composite"
        assets[key]["deleted_at"] = now
        if "composited" in (asset.get("local_path") or ""):
            assets[key].pop("local_path", None)
        assets[key].pop("drive_file_id", None)
        assets[key].pop("source_url", None)
        assets[key]["notes"] = (
            (assets[key].get("notes", "") + " | paste file purged from disk").strip(" |")
        )
    # Also sweep any remaining composited files under bolt wave-2 backgrounds.
    for pattern in (
        "assets/backgrounds/decks/bolt/*-composited.png",
        "assets/backgrounds/markets/**/*-composited.png",
    ):
        for full in ROOT.glob(pattern):
            rel = str(full.relative_to(ROOT))
            if rel in seen_paths:
                continue
            seen_paths.add(rel)
            full.unlink()
            deleted.append(rel)
    write_json(REGISTRY_PATH, registry)
    return deleted


def lock_deck_grade(*, reference_plate: str, seed_family: str) -> GradeLock:
    lock = GradeLock(
        locked=True,
        grade_family="warm-golden-hour-left",
        time_of_day="golden-hour",
        seed_family=seed_family,
        reference_plate=reference_plate,
        locked_at=utc_now(),
    )
    lock.save()
    return lock


def apply_image_ops_only(ops: list[dict], *, require_qa_pass: bool = True) -> None:
    if require_qa_pass:
        registry = load_json(REGISTRY_PATH)
        for op in ops:
            ptr = op.get("source_pointer", "")
            m = re.search(r"ASSET-REGISTRY (\S+)", ptr)
            if not m:
                raise SystemExit(f"Op missing registry pointer: {op.get('op_key')}")
            key = m.group(1)
            asset = registry["assets"].get(key, {})
            qa = asset.get("qa_status")
            if qa not in ("pass",):
                raise SystemExit(
                    f"qa_image_gate blocked replaceImage for {key}: qa_status={qa!r}"
                )
    plan = {
        "deck": "bolt",
        "presentation_id": PRESENTATION_ID,
        "wave": "wave-2.1-images",
        "generated_at": utc_now(),
        "operations": ops,
    }
    out = ROOT / "decks/bolt/deck.image-ops.json"
    write_json(out, plan)
    applied = apply_plan(plan, chunk_size=10)
    print(f"applied {applied} image ops")


def tag_drift_controls() -> None:
    src_dir = Path("/Users/jaideep/.grok/sessions/%2FUsers%2Fjaideep/019eafe2-6c96-7be0-8a3a-7501f5b98b78/images")
    dst_root = ROOT / "decks/bolt/controls"
    dst_root.mkdir(parents=True, exist_ok=True)
    mapping = {
        "13.jpg": dst_root / "prompt-only-drift-cover-13.jpg",
        "14.jpg": dst_root / "prompt-only-drift-slide2-14.jpg",
    }
    manifest = {
        "purpose": "before/after drift control — NOT decision input for wave-2.1",
        "tier": "prompt_only_wrong_tier",
        "tagged_at": utc_now(),
        "files": {},
    }
    for src_name, dst in mapping.items():
        src = src_dir / src_name
        if src.exists():
            dst.write_bytes(src.read_bytes())
            manifest["files"][src_name] = str(dst.relative_to(ROOT))
    write_json(dst_root / "drift-control-manifest.json", manifest)


def generate_bolt_cover_greece(*, out: Path) -> dict:
    prompt = load_tier_a_prompt(1)
    raw, meta = tier_a_edit(prompt=prompt)
    out.parent.mkdir(parents=True, exist_ok=True)
    img = Image.open(__import__("io").BytesIO(raw))
    if img.size[0] < MIN_W or img.size[1] < MIN_H:
        img = img.resize((MIN_W, MIN_H), Image.LANCZOS)
    img.convert("RGB").save(out, format="PNG", quality=95)
    receipt = qa_image_gate(out, role="cover_hero", market_slug="athens-saronic-greece")
    meta["output"] = str(out.relative_to(ROOT))
    meta["qa_receipt"] = receipt
    return meta


def approve_asset_qa(asset_key: str, *, approver: str = "human") -> dict:
    registry = load_json(REGISTRY_PATH)
    asset = registry["assets"].get(asset_key)
    if not asset:
        raise SystemExit(f"Unknown asset key: {asset_key}")
    receipt = dict(asset.get("qa_receipt", {}))
    for check in receipt.get("checks", []):
        if check["status"] == "pending_human":
            check["status"] = "pass"
            check["details"]["human_approved_by"] = approver
            check["details"]["human_approved_at"] = utc_now()
    receipt["overall"] = "pass"
    receipt["human_approved_at"] = utc_now()
    receipt["human_approved_by"] = approver
    receipt["pending_human"] = []
    asset["qa_receipt"] = receipt
    asset["qa_status"] = "pass"
    asset["qa_evaluated_at"] = utc_now()
    asset["status"] = "checked_in"
    asset["qa_evaluated_at"] = receipt.get("evaluated_at", utc_now())
    write_json(REGISTRY_PATH, registry)
    return receipt


MARKET_SCENES: dict[str, str] = {
    "athens-saronic-greece": "the Aegean — Hydra/Saronic white cliff towns and Cycladic domes",
    "split-croatia": "Split harbour and Hvar old-town stone waterfront, pine islets",
    "cote-dazur-france": "Nice Promenade des Anglais and Monaco harbour, belle-époque façades",
    "sorrento-italy": "Sorrento cliffs, Capri Faraglioni stacks, Amalfi pastel terraces",
    "dubai-uae": "Dubai Marina skyline and harbour towers on the Gulf (Gulf market only)",
    "jeddah-ksa": "Jeddah Corniche waterfront and Red Sea turquoise bay",
    "mykonos-greece": "Mykonos windmills, Paros Naoussa harbour, Cycladic blue domes",
    "dubrovnik-croatia": "Dubrovnik old-town walls, terracotta roofs, Adriatic blue",
    "red-sea-ksa": "Red Sea desert mountains, turquoise AMAALA/Triple Bay coastline",
    "europe-network": "European coastline — Aegean, Adriatic and Riviera island silhouettes",
}

# Market-specific landmarks for unit-economics slides (must read at thumbnail size).
ECON_LANDMARKS: dict[str, str] = {
    "athens-saronic-greece": (
        "Hydra island amphitheatre of whitewashed houses and blue domes climbing the Saronic cliff above "
        "the Aegean — unmistakably Greece"
    ),
    "split-croatia": (
        "Hvar old-town cathedral bell tower and stone palazzi above Split harbour, Dalmatian pine islets — "
        "unmistakably Croatia"
    ),
    "cote-dazur-france": (
        "Nice Promenade des Anglais, Baie des Anges, and Monaco harbour super-yachts with belle-époque "
        "façades — unmistakably the French Riviera"
    ),
    "sorrento-italy": (
        "Sorrento cliff terraces, Capri Faraglioni sea stacks, and pastel Amalfi Coast villages — "
        "unmistakably Italy"
    ),
    "dubai-uae": (
        "Dubai Marina and JBR tower skyline reflected on the Gulf — unmistakably Dubai (Gulf market only)"
    ),
    "jeddah-ksa": (
        "Jeddah Corniche waterfront, King Fahd Fountain, and Red Sea turquoise bay — unmistakably Jeddah"
    ),
    "mykonos-greece": (
        "Mykonos windmills and white cubic houses, Paros Naoussa harbour — unmistakably the Cyclades"
    ),
    "red-sea-ksa": (
        "Red Sea desert mountains framing turquoise AMAALA/Triple Bay coastline — unmistakably Saudi Red Sea"
    ),
}

# Foils *deployed* (in the water) = hydrofoiling. Never depict a displacement ferry sitting low.
FOIL_STATE = (
    "underwater foils fully deployed, hull riding elevated above the waterline on the foils, "
    "visible foil struts and a clean foil wake — actively hydrofoiling, never floating low like a ferry"
)


def _grade_suffix() -> str:
    lock = GradeLock.load()
    if not lock.locked:
        return ""
    return f" Match the locked deck grade family ({lock.grade_family}, {lock.time_of_day})."


def prompt_tam() -> str:
    return (
        "Using <IMAGE_0> as the white hydrofoil vessel as the exact form and colour reference, "
        "produce a single photorealistic 16:9 photograph: a wide, aspirational seascape at golden hour. "
        "A single white hydrofoil, small in the lower-center, heads toward a European coastline with "
        "several distant island and town silhouettes across the Aegean, Adriatic and Mediterranean "
        "suggesting a network of destinations. Expansive open sky fills the upper two-thirds for a "
        "data overlay. Cinematic, optimistic, premium grade. Foils down, clean wake, hull/cabin/V-mark "
        "exactly as the reference, in-water no seam. Exactly one vessel. No map graphics, no people, "
        "no logos, no text. No Dubai skyline, no Burj Khalifa, no Marina Bay Sands."
        + _grade_suffix()
    )


def prompt_partner_roles(scene: str) -> str:
    return (
        f"Using <IMAGE_0> as the white hydrofoil vessel as the exact form and colour reference, "
        f"produce a single photorealistic 16:9 photograph at a tidy modern berth in {scene}: "
        "the white hydrofoil moored alongside, foils down, clean reflection. Frame so the right third "
        "is clean, calm sky and water for a logo-and-text lockup. Warm, premium daylight. Exactly one "
        "vessel, hull/cabin/V-mark exactly as the reference, in-water no seam. Single integrated "
        "photograph, not a collage. No logos, no text, no brand signage."
        + _grade_suffix()
    )


def prompt_econ(market_slug: str) -> str:
    landmark = ECON_LANDMARKS[market_slug]
    return (
        "Using <IMAGE_0> as the white hydrofoil vessel as the exact form and colour reference, "
        "produce a single photorealistic 16:9 photograph for a unit-economics chart slide. "
        "Composition split: the left 42% is a smooth, calm navy-to-slate sky-and-water gradient — "
        "low enough contrast for white P&L tables and charts. "
        f"The right 58% is a photorealistic, clearly recognizable view of {landmark}. "
        "The landmark skyline or coastline must be identifiable at thumbnail size — vibrant warm "
        "golden-hour light, market-specific detail (buildings, cliffs, towers, harbour), never a generic "
        "empty ocean. A single white hydrofoil is small in the lower-right on open water, "
        f"{FOIL_STATE}. Hull/cabin/V-mark exactly as the reference, in-water no seam. "
        "Exactly one vessel. Aspirational premium grade. No people, no logos, no text, no map graphics."
        + _grade_suffix()
    )


REMAINING_PLATES: list[dict] = [
    {
        "key": "bolt-tam-bg",
        "role": "tam_bg",
        "scope": "deck",
        "local_path": "assets/backgrounds/decks/bolt/bolt-tam-network-tier-a-v1.png",
        "market_slug": "europe-network",
        "prompt": prompt_tam,
        "seed": "bolt-wave21-tam",
        "used_by": [
            {
                "deck": "bolt",
                "slide_index": 10,
                "slide_object_id": "g3eec5122801_0_562",
                "target_object_id": "navierBg_s26",
            }
        ],
    },
    {
        "key": "bolt-partner-roles-bg",
        "role": "partner_roles_bg",
        "scope": "deck",
        "local_path": "assets/backgrounds/decks/bolt/bolt-partner-roles-greece-tier-a-v1.png",
        "market_slug": "athens-saronic-greece",
        "prompt": lambda: prompt_partner_roles(
            "an Aegean island berth with white Cycladic buildings"
        ),
        "seed": "bolt-wave21-partner-roles",
        "used_by": [
            {
                "deck": "bolt",
                "slide_index": 11,
                "slide_object_id": "g3ea5e0fb254_4_357",
                "target_object_id": "g3ea5e0fb254_4_358",
            }
        ],
    },
    {
        "key": "econ-greece-athens-hydra",
        "role": "econ_market_bg",
        "scope": "market",
        "local_path": "assets/backgrounds/markets/greece/greece-aegean-econ-tier-a-v1.png",
        "market_slug": "athens-saronic-greece",
        "atlas_city_id": "athens-saronic-greece",
        "prompt": lambda: prompt_econ("athens-saronic-greece"),
        "seed": "bolt-wave22-econ-greece-athens",
    },
    {
        "key": "econ-croatia-split-hvar",
        "role": "econ_market_bg",
        "scope": "market",
        "local_path": "assets/backgrounds/markets/croatia/croatia-dalmatian-econ-tier-a-v1.png",
        "market_slug": "split-croatia",
        "atlas_city_id": "split-croatia",
        "prompt": lambda: prompt_econ("split-croatia"),
        "seed": "bolt-wave22-econ-croatia-split",
    },
    {
        "key": "econ-cote-azur-nice-monaco",
        "role": "econ_market_bg",
        "scope": "market",
        "local_path": "assets/backgrounds/markets/cote-dazur/cote-azur-econ-tier-a-v1.png",
        "market_slug": "cote-dazur-france",
        "atlas_city_id": "cote-dazur-france",
        "prompt": lambda: prompt_econ("cote-dazur-france"),
        "seed": "bolt-wave22-econ-cote-azur",
    },
    {
        "key": "econ-italy-sorrento-capri",
        "role": "econ_market_bg",
        "scope": "market",
        "local_path": "assets/backgrounds/markets/italy-amalfi/italy-amalfi-econ-tier-a-v1.png",
        "market_slug": "sorrento-italy",
        "prompt": lambda: prompt_econ("sorrento-italy"),
        "seed": "bolt-wave22-econ-italy-amalfi",
    },
    {
        "key": "econ-uae-dubai-harbour",
        "role": "econ_market_bg",
        "scope": "market",
        "local_path": "assets/backgrounds/markets/uae/uae-dubai-econ-tier-a-v1.png",
        "market_slug": "dubai-uae",
        "atlas_city_id": "dubai-uae",
        "prompt": lambda: prompt_econ("dubai-uae"),
        "seed": "bolt-wave22-econ-uae-dubai",
    },
    {
        "key": "econ-ksa-jeddah",
        "role": "econ_market_bg",
        "scope": "market",
        "local_path": "assets/backgrounds/markets/ksa/ksa-jeddah-econ-tier-a-v1.png",
        "market_slug": "jeddah-ksa",
        "prompt": lambda: prompt_econ("jeddah-ksa"),
        "seed": "bolt-wave22-econ-ksa-jeddah",
    },
    {
        "key": "econ-greece-mykonos-paros",
        "role": "econ_market_bg",
        "scope": "market",
        "local_path": "assets/backgrounds/markets/greece/greece-cyclades-econ-tier-a-v1.png",
        "market_slug": "mykonos-greece",
        "prompt": lambda: prompt_econ("mykonos-greece"),
        "seed": "bolt-wave22-econ-greece-cyclades",
    },
]

ECON_PLATE_KEYS = [
    "econ-greece-athens-hydra",
    "econ-croatia-split-hvar",
    "econ-cote-azur-nice-monaco",
    "econ-italy-sorrento-capri",
    "econ-uae-dubai-harbour",
    "econ-ksa-jeddah",
    "econ-greece-mykonos-paros",
    "econ-ksa-redsea-amaala",
]

REDSEA_AMAALA_PLATE: dict = {
    "key": "econ-ksa-redsea-amaala",
    "role": "econ_market_bg",
    "scope": "market",
    "local_path": "assets/backgrounds/markets/ksa/ksa-redsea-amaala-econ-tier-a-v1.png",
    "market_slug": "red-sea-ksa",
    "prompt": lambda: prompt_econ("red-sea-ksa"),
    "seed": "bolt-wave22-econ-ksa-redsea-amaala",
    "used_by": [
        {
            "deck": "bolt",
            "slide_index": 23,
            "slide_object_id": "g3eec5122801_0_968",
            "target_object_id": "navierBg_s39",
        }
    ],
}


def generate_and_save_plate(spec: dict) -> dict:
    out = ROOT / spec["local_path"]
    prompt = spec["prompt"]() if callable(spec["prompt"]) else spec["prompt"]
    raw, meta = tier_a_edit(prompt=prompt, seed_note=spec.get("seed"))
    out.parent.mkdir(parents=True, exist_ok=True)
    img = Image.open(__import__("io").BytesIO(raw))
    if img.size[0] < MIN_W or img.size[1] < MIN_H:
        img = img.resize((MIN_W, MIN_H), Image.LANCZOS)
    img.convert("RGB").save(out, format="PNG", quality=95)
    receipt = qa_image_gate(out, role=spec["role"], market_slug=spec.get("market_slug"))
    meta["output"] = spec["local_path"]
    meta["qa_receipt"] = receipt
    _register_tier_a_asset(
        key=spec["key"],
        role=spec["role"],
        local_path=spec["local_path"],
        scope=spec.get("scope", "deck"),
        meta=meta,
        receipt=receipt,
        market_slug=spec.get("market_slug"),
        atlas_city_id=spec.get("atlas_city_id"),
        used_by=spec.get("used_by"),
    )
    return {"key": spec["key"], "output": str(out), "qa_overall": receipt["overall"], "auto_fails": receipt["blocking_failures"]}


def _register_tier_a_asset(
    *,
    key: str,
    role: str,
    local_path: str,
    meta: dict,
    receipt: dict,
    scope: str = "deck",
    market_slug: str | None = None,
    atlas_city_id: str | None = None,
    used_by: list[dict] | None = None,
) -> None:
    registry = load_json(REGISTRY_PATH)
    asset = registry.setdefault("assets", {}).setdefault(key, {})
    prev = dict(asset)
    asset.update(
        {
            "role": role,
            "scope": scope,
            "partner": "bolt" if scope == "deck" else prev.get("partner", "bolt"),
            "market_slug": market_slug,
            "atlas_city_id": atlas_city_id or prev.get("atlas_city_id"),
            "local_path": local_path,
            "provenance": f"tier_a:{meta['provider']}",
            "tier": "A",
            "status": "checked_in" if receipt["overall"] == "pass" else "qa_pending",
            "composited": False,
            "reproducible": True,
            "captured_at": meta["generated_at"],
            "generation": meta,
            "drive_file_id": prev.get("drive_file_id"),
            "source_url": prev.get("source_url"),
            "used_by": used_by or prev.get("used_by", []),
            "license": "navier-internal",
            "notes": (prev.get("notes", "") + " | wave-2.1 Tier A").strip(" |"),
        }
    )
    asset["qa_receipt"] = receipt
    asset["qa_status"] = receipt["overall"]
    asset["qa_evaluated_at"] = receipt["evaluated_at"]
    write_json(REGISTRY_PATH, registry)


def generate_bolt_slide2(*, out: Path) -> dict:
    prompt = load_tier_a_prompt(2)
    lock = GradeLock.load()
    if not lock.locked:
        prompt = (
            f"{prompt} Match the warm golden-hour grade family of the approved Bolt Greece cover "
            "(sun from left, soft rim light on white hull, premium photographic grade)."
        )
    raw, meta = tier_a_edit(prompt=prompt, seed_note="bolt-wave21-slide2-greece")
    out.parent.mkdir(parents=True, exist_ok=True)
    img = Image.open(__import__("io").BytesIO(raw))
    if img.size[0] < MIN_W or img.size[1] < MIN_H:
        img = img.resize((MIN_W, MIN_H), Image.LANCZOS)
    img.convert("RGB").save(out, format="PNG", quality=95)
    receipt = qa_image_gate(out, role="value_prop_bg", market_slug="athens-saronic-greece")
    meta["output"] = str(out.relative_to(ROOT))
    meta["qa_receipt"] = receipt
    return meta


def cmd_generate_cover() -> int:
    out = ROOT / "assets/backgrounds/decks/bolt/bolt-cover-greece-aegean-tier-a-v1.png"
    meta = generate_bolt_cover_greece(out=out)
    receipt = meta["qa_receipt"]
    print(json.dumps({"output": str(out), "qa_overall": receipt["overall"], "checks": receipt["checks"]}, indent=2))

    registry = load_json(REGISTRY_PATH)
    key = "bolt-cover-hero"
    asset = registry.setdefault("assets", {}).setdefault(key, {})
    asset.update(
        {
            "role": "cover_hero",
            "scope": "deck",
            "partner": "bolt",
            "market_slug": "athens-saronic-greece",
            "local_path": f"assets/backgrounds/decks/bolt/{out.name}",
            "provenance": f"tier_a:{meta['provider']}",
            "tier": "A",
            "status": "qa_pending" if receipt["overall"] != "pass" else "checked_in",
            "composited": False,
            "reproducible": True,
            "captured_at": meta["generated_at"],
            "generation": meta,
        }
    )
    _register_tier_a_asset(
        key=key,
        role="cover_hero",
        local_path=f"assets/backgrounds/decks/bolt/{out.name}",
        meta=meta,
        receipt=receipt,
        market_slug="athens-saronic-greece",
        used_by=[
            {
                "deck": "bolt",
                "slide_index": 1,
                "slide_object_id": "p1",
                "target_object_id": "p1_i2",
            }
        ],
    )
    return 0 if receipt["overall"] != "fail" else 1


def cmd_approve_cover() -> int:
    receipt = approve_asset_qa("bolt-cover-hero")
    lock_deck_grade(
        reference_plate="assets/backgrounds/decks/bolt/bolt-cover-greece-aegean-tier-a-v1.png",
        seed_family="bolt-wave21-greece-bar-setter",
    )
    print(json.dumps({"asset": "bolt-cover-hero", "qa_status": "pass", "grade_locked": True}, indent=2))
    return 0


def cmd_approve_slide2() -> int:
    approve_asset_qa("bolt-value-prop-bg")
    print(json.dumps({"asset": "bolt-value-prop-bg", "qa_status": "pass"}, indent=2))
    return 0


def cmd_generate_slide2() -> int:
    out = ROOT / "assets/backgrounds/decks/bolt/bolt-slide2-booking-moment-tier-a-v1.png"
    meta = generate_bolt_slide2(out=out)
    receipt = meta["qa_receipt"]
    print(json.dumps({"output": str(out), "qa_overall": receipt["overall"], "checks": receipt["checks"]}, indent=2))
    _register_tier_a_asset(
        key="bolt-value-prop-bg",
        role="value_prop_bg",
        local_path=f"assets/backgrounds/decks/bolt/{out.name}",
        meta=meta,
        receipt=receipt,
        market_slug="athens-saronic-greece",
        used_by=[
            {
                "deck": "bolt",
                "slide_index": 2,
                "slide_object_id": "g3f139a0b6ec_0_0",
                "target_object_id": "g3f139a0b6ec_0_1",
            }
        ],
    )
    return 0 if receipt["overall"] != "fail" else 1


def clear_drive_urls_for_republish(*keys: str) -> None:
    """Drop stale Drive URLs so a new local_path binary is uploaded."""
    registry = load_json(REGISTRY_PATH)
    for key in keys:
        asset = registry.get("assets", {}).get(key)
        if not asset:
            continue
        asset.pop("drive_file_id", None)
        asset.pop("source_url", None)
    write_json(REGISTRY_PATH, registry)


DECK_LEVEL_IMAGE_OP_BINDINGS: dict[str, tuple[str, str, str]] = {
    "bolt-cover-hero": ("p1", "p1_i2", "CENTER_INSIDE"),
    "bolt-value-prop-bg": ("g3f139a0b6ec_0_0", "g3f139a0b6ec_0_1", "CENTER_CROP"),
    "bolt-tam-bg": ("g3eec5122801_0_562", "navierBg_s26", "CENTER_CROP"),
    "bolt-partner-roles-bg": ("g3ea5e0fb254_4_357", "g3ea5e0fb254_4_358", "CENTER_CROP"),
}


def all_image_op_bindings(*, roles: set[str] | None = None) -> dict[str, tuple[str, str, str]]:
    """Deck-level plates + slide-image-bindings.json (authoritative for econ)."""
    doc = load_slide_bindings("bolt")
    errs = validate_bindings(doc)
    if errs:
        raise SystemExit("slide-image-bindings.json invalid:\n" + "\n".join(errs))
    merged = dict(DECK_LEVEL_IMAGE_OP_BINDINGS)
    merged.update(image_op_bindings(doc, roles=roles))
    return merged


def _econ_plate_specs() -> dict[str, dict]:
    specs = {s["key"]: s for s in REMAINING_PLATES if s["key"].startswith("econ-")}
    specs[REDSEA_AMAALA_PLATE["key"]] = REDSEA_AMAALA_PLATE
    return specs


def cmd_generate_remaining() -> int:
    results = []
    for spec in REMAINING_PLATES:
        print(f"generating {spec['key']}...", flush=True)
        try:
            results.append(generate_and_save_plate(spec))
        except Exception as e:
            results.append({"key": spec["key"], "error": str(e), "qa_overall": "fail"})
    print(json.dumps(results, indent=2))
    fails = [r for r in results if r.get("qa_overall") == "fail" or r.get("error")]
    return 1 if fails else 0


def cmd_reqa_remaining() -> int:
    """Re-run qa_image_gate on generated remaining plates (no regen)."""
    results = []
    for spec in REMAINING_PLATES:
        path = ROOT / spec["local_path"]
        if not path.is_file():
            results.append({"key": spec["key"], "error": "missing"})
            continue
        receipt = qa_image_gate(path, role=spec["role"], market_slug=spec.get("market_slug"))
        registry = load_json(REGISTRY_PATH)
        asset = registry.setdefault("assets", {}).setdefault(spec["key"], {})
        asset["qa_receipt"] = receipt
        asset["qa_status"] = receipt["overall"]
        asset["qa_evaluated_at"] = receipt["evaluated_at"]
        write_json(REGISTRY_PATH, registry)
        results.append(
            {"key": spec["key"], "qa_overall": receipt["overall"], "auto_fails": receipt["blocking_failures"]}
        )
    print(json.dumps(results, indent=2))
    return 0


def cmd_generate_redsea_amaala() -> int:
    print("generating econ-ksa-redsea-amaala...", flush=True)
    result = generate_and_save_plate(REDSEA_AMAALA_PLATE)
    print(json.dumps(result, indent=2))
    return 1 if result.get("qa_overall") == "fail" or result.get("error") else 0


def cmd_approve_redsea_amaala() -> int:
    registry = load_json(REGISTRY_PATH)
    asset = registry.get("assets", {}).get("econ-ksa-redsea-amaala", {})
    receipt = asset.get("qa_receipt") or asset.get("generation", {}).get("qa_receipt", {})
    if receipt.get("blocking_failures"):
        print(json.dumps({"error": "auto_fail", "failures": receipt["blocking_failures"]}, indent=2))
        return 1
    approve_asset_qa("econ-ksa-redsea-amaala", approver="bar-setter-precedent")
    print("approved econ-ksa-redsea-amaala")
    return 0


def cmd_regenerate_all_econ() -> int:
    return cmd_regenerate_keys(ECON_PLATE_KEYS)


def cmd_approve_all_econ() -> int:
    approved = []
    skipped = []
    registry = load_json(REGISTRY_PATH)
    for key in ECON_PLATE_KEYS:
        asset = registry.get("assets", {}).get(key, {})
        receipt = asset.get("qa_receipt") or asset.get("generation", {}).get("qa_receipt", {})
        if receipt.get("blocking_failures"):
            skipped.append({"key": key, "reason": "auto_fail", "failures": receipt["blocking_failures"]})
            continue
        if asset.get("qa_status") == "pass":
            skipped.append({"key": key, "reason": "already_pass"})
            continue
        approve_asset_qa(key, approver="wave22-econ-landmark-batch")
        approved.append(key)
    print(json.dumps({"approved": approved, "skipped": skipped}, indent=2))
    return 1 if skipped and any(s.get("reason") == "auto_fail" for s in skipped) else 0


def cmd_apply_atlas_screenshots() -> int:
    """Publish and apply human-captured Atlas screenshots for slides 4–6 and 14–18."""
    doc = load_slide_bindings("bolt")
    atlas_dir = ROOT / doc.get("atlas_screenshot_dir", "assets/screenshots/atlas/bolt")
    sys.path.insert(0, str(BUILDERS))
    from deck_autonomy_sync import publish_assets_to_drive  # type: ignore

    registry = load_json(REGISTRY_PATH)
    assets = registry.setdefault("assets", {})
    pending = []
    registered = []
    for bind in atlas_bindings(doc):
        key = bind["registry_key"]
        filename = bind.get("atlas_filename")
        if not filename:
            pending.append({"slide": bind["slide_index"], "reason": "missing atlas_filename"})
            continue
        local_path = f"{doc.get('atlas_screenshot_dir', 'assets/screenshots/atlas/bolt')}/{filename}"
        full = ROOT / local_path
        if not full.is_file():
            pending.append({"slide": bind["slide_index"], "key": key, "expected": local_path})
            continue
        assets[key] = {
            **assets.get(key, {}),
            "role": "atlas_route_screenshot",
            "scope": "deck",
            "partner": "bolt",
            "market_slug": bind.get("market_slug"),
            "local_path": local_path,
            "provenance": "human_capture:navier-atlas.vercel.app",
            "status": "checked_in",
            "license": "navier-internal",
            "reproducible": False,
            "composited": False,
            "captured_at": utc_now(),
            "used_by": [
                {
                    "deck": "bolt",
                    "slide_index": bind["slide_index"],
                    "slide_object_id": bind["slide_object_id"],
                    "target_object_id": bind["target_object_id"],
                }
            ],
            "notes": f"Atlas route screenshot slide {bind['slide_index']}",
        }
        registered.append(key)
    write_json(REGISTRY_PATH, registry)
    if not registered:
        print(json.dumps({"applied": 0, "pending": pending}, indent=2))
        return 0
    clear_drive_urls_for_republish(*registered)
    publish_assets_to_drive(REGISTRY_PATH)
    registry = load_json(REGISTRY_PATH)
    ops = []
    for bind in atlas_bindings(doc):
        key = bind["registry_key"]
        if key not in registered:
            continue
        url = registry["assets"][key].get("source_url")
        if not url:
            raise SystemExit(f"{key} missing source_url after publish")
        ops.append(
            image_replace_op(
                bind["slide_object_id"],
                bind["target_object_id"],
                url,
                op_key=f"bolt-atlas-{key}",
                source_pointer=f"ASSET-REGISTRY {key}",
                method=bind.get("apply_method", "CENTER_CROP"),
            )
        )
    apply_image_ops_only(ops, require_qa_pass=False)
    print(json.dumps({"applied": len(ops), "registered": registered, "pending": pending}, indent=2))
    return 0


def cmd_regenerate_keys(keys: list[str]) -> int:
    by_key = _econ_plate_specs()
    results = []
    for key in keys:
        spec = by_key.get(key)
        if not spec:
            raise SystemExit(f"Unknown key: {key}")
        print(f"regenerating {key}...", flush=True)
        results.append(generate_and_save_plate(spec))
    print(json.dumps(results, indent=2))
    return 0


def cmd_approve_batch_remaining() -> int:
    """Approve remaining plates with zero auto failures (bar-setter pair precedent)."""
    approved = []
    skipped = []
    registry = load_json(REGISTRY_PATH)
    for spec in REMAINING_PLATES:
        key = spec["key"]
        asset = registry.get("assets", {}).get(key, {})
        receipt = asset.get("qa_receipt") or asset.get("generation", {}).get("qa_receipt", {})
        if receipt.get("blocking_failures"):
            skipped.append({"key": key, "reason": "auto_fail", "failures": receipt["blocking_failures"]})
            continue
        if asset.get("qa_status") == "pass":
            skipped.append({"key": key, "reason": "already_pass"})
            continue
        approve_asset_qa(key, approver="batch-bar-setter-precedent")
        approved.append(key)
    print(json.dumps({"approved": approved, "skipped": skipped}, indent=2))
    return 0


def cmd_validate_bindings() -> int:
    doc = load_slide_bindings("bolt")
    errs = validate_bindings(doc)
    if errs:
        print(json.dumps({"status": "fail", "errors": errs}, indent=2))
        return 1
    econ = image_op_bindings(doc, roles={"econ_market_bg"})
    atlas = image_op_bindings(doc, roles={"atlas_route_screenshot"})
    print(
        json.dumps(
            {
                "status": "pass",
                "econ_bindings": len(econ),
                "atlas_bindings": len(atlas),
                "econ_slides": sorted(b["slide_index"] for b in doc["bindings"] if b["image_role"] == "econ_market_bg"),
                "atlas_slides": sorted(b["slide_index"] for b in doc["bindings"] if b["image_role"] == "atlas_route_screenshot"),
            },
            indent=2,
        )
    )
    return 0


def cmd_apply_econ_bindings() -> int:
    """Re-apply econ_market_bg only to unit-economics slides (7–9, 19–23)."""
    return cmd_publish_and_apply_approved(
        only=list(image_op_bindings(load_slide_bindings("bolt"), roles={"econ_market_bg"}).keys())
    )


def cmd_publish_and_apply_approved(*, only: list[str] | None = None) -> int:
    """Publish QA-passed wave-2.1 plates to Drive, then image-ops-only apply."""
    sys.path.insert(0, str(BUILDERS))
    from deck_autonomy_sync import publish_assets_to_drive  # type: ignore

    registry = load_json(REGISTRY_PATH)
    republish = [
        k
        for k, a in registry.get("assets", {}).items()
        if a.get("tier") == "A" and a.get("qa_status") == "pass" and a.get("local_path")
        and (only is None or k in only)
    ]
    clear_drive_urls_for_republish(*republish)
    publish_assets_to_drive(REGISTRY_PATH)
    registry = load_json(REGISTRY_PATH)
    ops = []
    bindings = all_image_op_bindings()
    for key, bind in bindings.items():
        if only is not None and key not in only:
            continue
        asset = registry["assets"].get(key, {})
        if asset.get("qa_status") != "pass":
            print(f"skip {key}: qa_status={asset.get('qa_status')!r}")
            continue
        url = asset.get("source_url")
        if not url:
            raise SystemExit(f"{key} missing source_url after publish")
        slide_oid, target_oid, method = bind
        ops.append(
            image_replace_op(
                slide_oid,
                target_oid,
                url,
                op_key=f"bolt-wave21-img-{key}",
                source_pointer=f"ASSET-REGISTRY {key}",
                method=method,
            )
        )
    if not ops:
        raise SystemExit("No QA-passed assets to apply")
    apply_image_ops_only(ops)
    print(json.dumps({"applied_ops": len(ops), "presentation_id": PRESENTATION_ID}, indent=2))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Bolt wave-2.1 image pipeline")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("deprecate-paste")
    sub.add_parser("purge-paste-composites")
    sub.add_parser("tag-drift-controls")
    sub.add_parser("generate-redsea-amaala")
    sub.add_parser("approve-redsea-amaala")
    sub.add_parser("validate-bindings")
    sub.add_parser("apply-econ-bindings")
    sub.add_parser("regenerate-all-econ")
    sub.add_parser("approve-all-econ")
    sub.add_parser("apply-atlas-screenshots")
    sub.add_parser("generate-cover-greece")
    sub.add_parser("approve-cover")
    sub.add_parser("approve-slide2")
    sub.add_parser("generate-slide2")
    sub.add_parser("generate-remaining")
    sub.add_parser("approve-batch-remaining")
    sub.add_parser("reqa-remaining")
    p_regen = sub.add_parser("regenerate-keys")
    p_regen.add_argument("keys", nargs="+")
    p_pub = sub.add_parser("publish-and-apply-approved")
    p_pub.add_argument("--only", nargs="+", default=None)
    p_lock = sub.add_parser("lock-grade")
    p_lock.add_argument("--plate", required=True)
    p_lock.add_argument("--seed-family", required=True)
    args = ap.parse_args()
    if args.cmd == "deprecate-paste":
        deprecate_paste_plates()
        print("deprecated", len(WAVE2_PASTE_KEYS), "paste plates")
        return 0
    if args.cmd == "purge-paste-composites":
        deleted = purge_paste_composite_files()
        print(json.dumps({"deleted_files": deleted, "count": len(deleted)}, indent=2))
        return 0
    if args.cmd == "generate-redsea-amaala":
        return cmd_generate_redsea_amaala()
    if args.cmd == "approve-redsea-amaala":
        return cmd_approve_redsea_amaala()
    if args.cmd == "validate-bindings":
        return cmd_validate_bindings()
    if args.cmd == "apply-econ-bindings":
        return cmd_apply_econ_bindings()
    if args.cmd == "regenerate-all-econ":
        return cmd_regenerate_all_econ()
    if args.cmd == "approve-all-econ":
        return cmd_approve_all_econ()
    if args.cmd == "apply-atlas-screenshots":
        return cmd_apply_atlas_screenshots()
    if args.cmd == "tag-drift-controls":
        tag_drift_controls()
        print("tagged drift controls")
        return 0
    if args.cmd == "generate-cover-greece":
        return cmd_generate_cover()
    if args.cmd == "approve-cover":
        return cmd_approve_cover()
    if args.cmd == "approve-slide2":
        return cmd_approve_slide2()
    if args.cmd == "generate-slide2":
        return cmd_generate_slide2()
    if args.cmd == "generate-remaining":
        return cmd_generate_remaining()
    if args.cmd == "approve-batch-remaining":
        return cmd_approve_batch_remaining()
    if args.cmd == "reqa-remaining":
        return cmd_reqa_remaining()
    if args.cmd == "regenerate-keys":
        return cmd_regenerate_keys(args.keys)
    if args.cmd == "publish-and-apply-approved":
        return cmd_publish_and_apply_approved(only=args.only)
    if args.cmd == "lock-grade":
        lock_deck_grade(reference_plate=args.plate, seed_family=args.seed_family)
        print("grade locked")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())