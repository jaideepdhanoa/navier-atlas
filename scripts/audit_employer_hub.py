#!/usr/bin/env python3
"""Copy + math gate for employer-hub JSON files."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "employer-hub" / "registry.json"

BANNED = [
    (r"\bLOI\b", "say letter of intent"),
    (r"\bnodes?\b", "say stop or terminal in customer copy"),
    (r"\bknots?\b", "no speed in knots"),
    (r"unlock(?:s|ing)?\s+(?:the\s+)?(?:berths?|docks?)", "no dock unlock framing"),
    (r"docks?\s+ahead\s+of\s+demand|demand\s+ahead\s+of\s+docks?", "no dock sequencing framing"),
    (r"unlocks?\s+terminal\s+access", "no terminal-access unlock framing"),
    (r"\bberths?\b", "avoid berth dependency language on employer page"),
]


def collect_copy(data: dict) -> str:
    parts: list[str] = []
    copy = data.get("copy") or {}
    for k, v in copy.items():
        if isinstance(v, str):
            parts.append(v)
        elif isinstance(v, list):
            for c in v:
                if isinstance(c, dict):
                    parts.append(str(c.get("value", c.get("stat", ""))))
                    parts.append(str(c.get("label", "")))
    for n in data.get("stops") or []:
        parts.append(str(n.get("label", "")))
        serves = n.get("serves", "")
        if isinstance(serves, list):
            parts.extend(str(x) for x in serves)
        else:
            parts.append(str(serves))
    for line in data.get("lines") or []:
        if line.get("name"):
            parts.append(str(line["name"]))
    for p in (data.get("products") or {}).get("items") or []:
        parts.append(str(p.get("title", "")))
        parts.append(str(p.get("body", "")))
    for f in (data.get("loi") or {}).get("flavors") or {}:
        fl = data["loi"]["flavors"][f]
        parts.append(str(fl.get("title", "")))
        parts.append(str(fl.get("body", "")))
    return "\n".join(parts)


def check_hub(path: Path) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    hits: list[str] = []
    blob = collect_copy(data)
    for pat, why in BANNED:
        for m in re.finditer(pat, blob, flags=re.I):
            ctx = blob[max(0, m.start() - 40) : m.end() + 40].replace("\n", " ")
            hits.append(f"{m.group(0)!r} — {why} · …{ctx[:120]}…")

    for term in (data.get("gates") or {}).get("banned_terms") or []:
        if re.search(term, blob, flags=re.I):
            hits.append(f"hub banned term {term!r}")

    calc = data.get("calculator") or {}
    inputs = calc.get("inputs") or {}
    profile = calc.get("profile") or "bay_productivity"
    assert_ = calc.get("worked_assert") or {}

    if profile == "bay_productivity":
        S = inputs.get("seats", {}).get("default", 60)
        P = inputs.get("price_seat_month", {}).get("default", 1000)
        sigma = inputs.get("subsidy_share", {}).get("default", 0.8)
        X = inputs.get("pretax_benefit", {}).get("default", 325)
        V = inputs.get("shuttle_cost", {}).get("default", 550)
        K = inputs.get("parking_cost", {}).get("default", 350)
        rho = inputs.get("parking_share", {}).get("default", 0.5)
        net = S * P - S * min(X, (1 - sigma) * P) - S * V - S * rho * K
        want = assert_.get("net_incremental", 4500)
        if round(net) != want:
            hits.append(f"net_incremental={net} expected {want}")
    elif profile == "nyc_parking_toll":
        S = inputs.get("S_committed_seats", inputs.get("seats", {})).get("default", 60)
        P = inputs.get("P_price_per_seat_month", inputs.get("price_seat_month", {})).get("default", 750)
        sigma = inputs.get("sigma_employer_subsidy_share", inputs.get("subsidy_share", {})).get("default", 0.8)
        X = inputs.get("X_pretax_benefit_cap_month", inputs.get("pretax_benefit", {})).get("default", 340)
        V = inputs.get("V_current_shuttle_cost_seat_month", inputs.get("shuttle_cost", {})).get("default", 0)
        K = inputs.get("K_parking_cost_stall_month", inputs.get("parking_cost", {})).get("default", 570)
        rho = inputs.get("rho_share_displacing_stall", inputs.get("parking_share", {})).get("default", 0.5)
        G = inputs.get("G_congestion_toll_weekday", {}).get("default", 9)
        W = inputs.get("W_weekdays_per_month", {}).get("default", 21)
        net_employer = S * P - S * min(X, (1 - sigma) * P)
        net_per = net_employer / S if S else 0
        bench = K + G * W
        net_inc = net_employer - S * rho * K - S * V
        if assert_.get("net_employer_cost_per_rider") is not None and round(net_per) != assert_["net_employer_cost_per_rider"]:
            hits.append(f"net_employer_cost_per_rider={net_per} expected {assert_['net_employer_cost_per_rider']}")
        if assert_.get("benchmark") is not None and round(bench) != assert_["benchmark"]:
            hits.append(f"benchmark={bench} expected {assert_['benchmark']}")
        if assert_.get("net_incremental") is not None and round(net_inc) != assert_["net_incremental"]:
            hits.append(f"net_incremental={net_inc} expected {assert_['net_incremental']}")

    for n in data.get("stops") or []:
        if not n.get("resolved_bp_id") or n.get("lng") is None:
            hits.append(f"stop {n.get('key')}: missing bp or coordinates")

    return hits


def main() -> int:
    if not REGISTRY.exists():
        print("MISSING", REGISTRY)
        return 1
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    failed = 0
    for entry in reg.get("hubs") or []:
        if entry.get("enabled") is False:
            continue
        path = ROOT / "employer-hub" / (entry.get("path") or f"hubs/{entry['id']}/hub.json")
        if not path.exists():
            print("MISSING", path)
            failed += 1
            continue
        hits = check_hub(path)
        if hits:
            print(f"FAIL {entry['id']}")
            for h in hits:
                print(f"  · {h}")
            failed += 1
        else:
            data = json.loads(path.read_text(encoding="utf-8"))
            print(
                f"PASS {entry['id']}  stops={len(data.get('stops') or [])} "
                f"lines={len(data.get('lines') or [])} profile={data.get('calculator', {}).get('profile')}"
            )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
