#!/usr/bin/env python3
"""Produce n30-reference-neutral-ALPHA.png — true hull cutout for Tier C fallback."""
from __future__ import annotations

import argparse
import base64
import json
import os
import urllib.request
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
NEUTRAL = ROOT / "assets/n30/n30-reference-neutral.png"
ALPHA_OUT = ROOT / "assets/n30/n30-reference-neutral-ALPHA.png"


def _xai_token() -> str:
    auth_path = Path.home() / ".grok/auth.json"
    if os.environ.get("XAI_API_KEY"):
        return os.environ["XAI_API_KEY"]
    data = json.loads(auth_path.read_text(encoding="utf-8"))
    for entry in data.values():
        if isinstance(entry, dict) and entry.get("key"):
            return entry["key"]
    raise SystemExit("No XAI_API_KEY or ~/.grok/auth.json token")


def _b64_data_uri(path: Path) -> str:
    raw = path.read_bytes()
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(raw).decode('ascii')}"


def tier_a_extract_alpha(*, out: Path, token: str) -> Path:
    """Use xAI image_edit to strip baked background; cabin glass neutral, not scenic."""
    prompt = (
        "Extract ONLY the white hydrofoil vessel from <IMAGE_0> onto a fully transparent background. "
        "Remove every pixel of sky, water, island, palm trees, and scenery. "
        "The hull must be 100% opaque white. "
        "Cabin glass must show a neutral dark tinted reflection — NOT the green island or any landscape "
        "visible through the windows. No scenery inside the hull silhouette. "
        "Preserve exact hull form, glass cabin frames, bow V-mark, and foil stance from the reference. "
        "Output a clean PNG-style cutout on transparent alpha, no border, no shadow plate."
    )
    body = {
        "model": "grok-imagine-image-quality",
        "prompt": prompt,
        "images": [{"url": _b64_data_uri(NEUTRAL)}],
        "aspect_ratio": "auto",
        "resolution": "2k",
        "response_format": "b64_json",
    }
    req = urllib.request.Request(
        "https://api.x.ai/v1/images/edits",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    b64 = payload["data"][0].get("b64_json")
    if not b64:
        url = payload["data"][0]["url"]
        with urllib.request.urlopen(url, timeout=120) as img_resp:
            raw = img_resp.read()
        img = Image.open(__import__("io").BytesIO(raw)).convert("RGBA")
    else:
        import io

        img = Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGBA")
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, format="PNG")
    return out


def verify_alpha(path: Path) -> dict:
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    px = img.load()
    opaque = 0
    transparent = 0
    hull_samples = []
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 16:
                transparent += 1
            elif a > 240:
                opaque += 1
                if 0.45 * w < x < 0.95 * w and 0.25 * h < y < 0.85 * h:
                    hull_samples.append((r, g, b))
    if not hull_samples:
        return {"pass": False, "reason": "no_opaque_hull_region"}
    greens = sum(1 for r, g, b in hull_samples if g > r + 20 and g > b + 10)
    green_ratio = greens / len(hull_samples)
    return {
        "pass": green_ratio < 0.08 and opaque > transparent,
        "opaque_pixels": opaque,
        "transparent_pixels": transparent,
        "hull_green_leak_ratio": round(green_ratio, 4),
        "dimensions": f"{w}x{h}",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ALPHA_OUT))
    ap.add_argument("--verify-only", action="store_true")
    args = ap.parse_args()
    out = Path(args.out)
    if args.verify_only:
        print(json.dumps(verify_alpha(out), indent=2))
        return 0
    token = _xai_token()
    tier_a_extract_alpha(out=out, token=token)
    report = verify_alpha(out)
    print(json.dumps(report, indent=2))
    return 0 if report.get("pass") else 1


if __name__ == "__main__":
    raise SystemExit(main())