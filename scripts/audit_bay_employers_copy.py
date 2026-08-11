#!/usr/bin/env python3
"""Bay employers microsite copy gate — plain English + no dock-dependency friction."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "handoff/bay-employers/inputs/bay-employers-data.json"
HTML = ROOT / "bay-employers/index.html"

# Scan only human-facing copy surfaces
COPY_KEYS = ("hero_headline", "hero_sub", "stripe_lesson", "loi_cta", "price_anchor", "footer_note", "launch_trigger")


def collect_copy(data: dict) -> str:
    parts: list[str] = []
    copy = data.get("copy") or {}
    for k in COPY_KEYS:
        if copy.get(k):
            parts.append(str(copy[k]))
    for c in copy.get("problem_chips") or []:
        parts.append(str(c.get("value", "")))
        parts.append(str(c.get("label", "")))
    for n in data.get("nodes") or []:
        parts.append(str(n.get("label", "")))
        parts.append(str(n.get("serves", "")))
    for line in data.get("lines") or []:
        if isinstance(line, dict) and line.get("name"):
            parts.append(str(line["name"]))
        if isinstance(line, dict) and line.get("calculator_preset"):
            parts.append(str(line["calculator_preset"].get("label", "")))
    # Visible static strings from HTML (outside <script> and <style>)
    if HTML.exists():
        html = HTML.read_text(encoding="utf-8")
        html = re.sub(r"<script[\s\S]*?</script>", " ", html, flags=re.I)
        html = re.sub(r"<style[\s\S]*?</style>", " ", html, flags=re.I)
        text = re.sub(r"<[^>]+>", " ", html)
        parts.append(text)
    return "\n".join(parts)


BANNED = [
    (r"\bLOI\b", "say letter of intent"),
    (r"\bnodes?\b", "say stop or terminal in customer copy"),
    (r"\bknots?\b", "no speed in knots"),
    (r"30-seat\s+N45|1,?000\s*[-–]\s*1,?500\s*seat|1,?000\+?\s*seat", "superseded seat/trigger figures"),
    (r"unlock(?:s|ing)?\s+(?:the\s+)?(?:berths?|docks?)", "no dock unlock framing"),
    (r"docks?\s+ahead\s+of\s+demand|demand\s+ahead\s+of\s+docks?", "no dock sequencing framing"),
    (r"unlocks?\s+terminal\s+access", "no terminal-access unlock framing"),
    (r"\bberths?\b", "avoid berth dependency language on employer page"),
]


def main() -> int:
    if not DATA.exists():
        print("MISSING", DATA)
        return 1
    data = json.loads(DATA.read_text(encoding="utf-8"))
    blob = collect_copy(data)
    hits = []
    for pat, why in BANNED:
        for m in re.finditer(pat, blob, flags=re.I):
            # allow "network" etc.; skip "node" only when standalone word in copy
            start = max(0, m.start() - 50)
            ctx = blob[start : m.end() + 50].replace("\n", " ")
            hits.append((m.group(0), why, ctx[:140]))

    i = (data.get("roi_calculator") or {}).get("inputs") or {}
    S = i.get("seats", {}).get("default", 60)
    P = i.get("price_seat_month", {}).get("default", 1000)
    sigma = i.get("subsidy_share", {}).get("default", 0.8)
    X = i.get("pretax_benefit", {}).get("default", 325)
    V = i.get("shuttle_cost", {}).get("default", 550)
    K = i.get("parking_cost", {}).get("default", 350)
    rho = i.get("parking_share", {}).get("default", 0.5)
    net = S * P - S * min(X, (1 - sigma) * P) - S * V - S * rho * K
    if round(net) != 4500:
        hits.append((f"net_incremental={net}", "worked example must be 4500", "calculator"))

    # resolved BPs
    for n in data.get("nodes") or []:
        if not n.get("resolved_bp_id") or n.get("lng") is None:
            hits.append((n.get("key"), "missing resolved_bp_id or coordinates", "nodes"))

    if hits:
        print("bay-employers copy gate FAIL")
        for h in hits:
            print(f"  · {h[0]!r} — {h[1]} · …{h[2]}…")
        return 1
    print("bay-employers copy gate PASS")
    print(f"  calculator defaults net_incremental={round(net)} per_rider={round(net / S) if S else 'n/a'}")
    print(f"  stops={len(data.get('nodes') or [])} lines={len([l for l in data.get('lines') or [] if l.get('id')])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
