#!/usr/bin/env python3
"""Capture Atlas market route screenshots for deck side-panel slides."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
BUILDERS = ROOT / "builders"
E2E_ROOT = REPO_ROOT / "tests" / "e2e"
CAPTURE_MJS = E2E_ROOT / "capture-atlas-screenshots.mjs"
DIST_ROOT = REPO_ROOT / "_dist"

sys.path.insert(0, str(BUILDERS))

from deck_link_bindings import (  # noqa: E402
    load_link_bindings_doc,
    merged_bindings,
    partner_doc_path,
    resolve_binding_url,
)
from deck_slide_bindings import atlas_bindings, load_slide_bindings  # noqa: E402

ATLAS_SLIDES = {4, 5, 6, 14, 15, 16, 17, 18}
DEFAULT_VIEWPORT = {"width": 2560, "height": 1440}


class _QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:
        return


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _rewrite_base(url: str, base_url: str) -> str:
    parsed = urlparse(url)
    base = urlparse(base_url.rstrip("/"))
    return f"{base.scheme}://{base.netloc}{parsed.path}" + (f"?{parsed.query}" if parsed.query else "")


def build_capture_manifest(
    deck_key: str,
    *,
    base_url: str,
    output_dir: Path | None = None,
    only_slides: set[int] | None = None,
) -> dict[str, Any]:
    image_doc = load_slide_bindings(deck_key)
    link_doc = load_link_bindings_doc(deck_key)
    deck_cfg = _load_json(ROOT / f"decks/{deck_key}/deck.config.json")
    partner_doc = _load_json(partner_doc_path(link_doc))
    golden = _load_json(ROOT / "decks/grab/golden-template-map.json")

    atlas_by_slide = {b["slide_index"]: b for b in atlas_bindings(image_doc)}
    link_by_slide = {
        b["slide_index"]: b
        for b in merged_bindings(deck_key, golden=golden)
        if b.get("link_role") == "atlas_market"
    }
    url_by_slide = {
        slide_index: resolve_binding_url(b, doc=link_doc, deck_cfg=deck_cfg, partner_doc=partner_doc)["url"]
        for slide_index, b in link_by_slide.items()
    }

    out_root = output_dir or (ROOT / image_doc.get("atlas_screenshot_dir", f"assets/screenshots/atlas/{deck_key}"))
    items: list[dict[str, Any]] = []
    slide_indexes = sorted(s for s in ATLAS_SLIDES if only_slides is None or s in only_slides)
    for slide_index in slide_indexes:
        bind = atlas_by_slide.get(slide_index)
        if not bind:
            raise SystemExit(f"Missing atlas_route_screenshot binding for slide {slide_index}")
        url = url_by_slide.get(slide_index)
        if not url:
            raise SystemExit(f"Missing atlas_market link URL for slide {slide_index}")
        filename = bind.get("atlas_filename")
        if not filename:
            raise SystemExit(f"Missing atlas_filename for slide {slide_index}")
        link_bind = link_by_slide.get(slide_index, {})
        item = {
            "slide_index": slide_index,
            "registry_key": bind.get("registry_key"),
            "atlas_filename": filename,
            "url": _rewrite_base(url, base_url),
            "output_path": str((out_root / filename).resolve()),
        }
        capture_mode = bind.get("capture_mode")
        if not capture_mode and link_bind.get("link_target") == "city":
            capture_mode = "city"
        if capture_mode:
            item["capture_mode"] = capture_mode
        city_id = bind.get("atlas_city_id") or link_bind.get("atlas_city_id")
        if city_id:
            item["atlas_city_id"] = city_id
        route_id = bind.get("atlas_route_id")
        if route_id:
            item["atlas_route_id"] = route_id
        items.append(item)

    return {
        "deck_key": deck_key,
        "base_url": base_url.rstrip("/"),
        "viewport": DEFAULT_VIEWPORT,
        "map_settle_ms": 2500,
        "post_panel_ms": 3500,
        "items": items,
    }


def _playwright_node() -> tuple[dict[str, str], list[str]]:
    env = os.environ.copy()
    return env, ["node", str(CAPTURE_MJS)]


def _start_dist_server(port: int) -> tuple[ThreadingHTTPServer, Thread]:
    if not DIST_ROOT.is_dir():
        raise SystemExit(f"Missing _dist build at {DIST_ROOT}. Run: node scripts/build-site.mjs")
    handler = lambda *args, **kwargs: _QuietHandler(*args, directory=str(DIST_ROOT), **kwargs)  # noqa: E501,E731
    server = ThreadingHTTPServer(("127.0.0.1", port), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.4)
    return server, thread


def run_capture(
    deck_key: str,
    *,
    base_url: str | None = None,
    serve_dist: bool = False,
    port: int = 4174,
    password: str | None = None,
    dry_run: bool = False,
    only_slides: set[int] | None = None,
) -> int:
    if serve_dist:
        _start_dist_server(port)
        base_url = f"http://127.0.0.1:{port}"
    if not base_url:
        base_url = os.environ.get("ATLAS_BASE_URL", "https://navier-atlas.vercel.app").rstrip("/")

    manifest = build_capture_manifest(deck_key, base_url=base_url, only_slides=only_slides)
    password = password or os.environ.get("PARTNER_AUTH_BOLT") or os.environ.get("ATLAS_PASSWORD")
    manifest["password"] = password
    manifest["username"] = os.environ.get("ATLAS_AUTH_USER", "navier")

    if dry_run:
        print(json.dumps(manifest, indent=2))
        return 0

    for item in manifest["items"]:
        Path(item["output_path"]).parent.mkdir(parents=True, exist_ok=True)

    env, cmd = _playwright_node()
    proc = subprocess.run(
        cmd,
        input=json.dumps(manifest),
        text=True,
        capture_output=True,
        cwd=str(E2E_ROOT),  # resolves @playwright/test from tests/e2e/node_modules
        env=env,
        check=False,
    )
    if proc.stdout.strip():
        print(proc.stdout.strip())
    if proc.stderr.strip():
        print(proc.stderr.strip(), file=sys.stderr)
    return proc.returncode


def main() -> int:
    ap = argparse.ArgumentParser(description="Capture Atlas route screenshots for deck side panels")
    ap.add_argument("--deck", default="bolt")
    ap.add_argument("--base-url", default=None, help="Atlas origin (default: ATLAS_BASE_URL or Vercel prod)")
    ap.add_argument(
        "--serve-dist",
        action="store_true",
        help="Serve navier-atlas/_dist locally (no partner password) and capture from it",
    )
    ap.add_argument("--port", type=int, default=4174)
    ap.add_argument("--password", default=None, help="PARTNER_AUTH_* for prod capture (or env var)")
    ap.add_argument("--dry-run", action="store_true", help="Print manifest only")
    ap.add_argument("--only-slides", nargs="+", type=int, default=None)
    args = ap.parse_args()
    only = set(args.only_slides) if args.only_slides else None
    return run_capture(
        args.deck,
        base_url=args.base_url,
        serve_dist=args.serve_dist,
        port=args.port,
        password=args.password,
        dry_run=args.dry_run,
        only_slides=only,
    )


if __name__ == "__main__":
    raise SystemExit(main())