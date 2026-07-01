#!/usr/bin/env python3
"""Build PTA pair-gap table: published lines vs dossier pairs vs orphan BPs."""
from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_JSON = ROOT / "handoff/partner-map-model/PTA-PAIR-GAP-TABLE.json"
OUT_MD = ROOT / "handoff/partner-map-model/PTA-PAIR-GAP-TABLE.md"

REF_TIP = "origin/pta-ferry-authorities-batch5-2026-07-01"
EXTRA_REFS = {
    "qatar": "origin/pta-qatar-singapore-mpa-2026-06-30",
    "singapore-mpa": "origin/pta-qatar-singapore-mpa-2026-06-30",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git_show(ref: str, path: str) -> dict | None:
    try:
        raw = subprocess.check_output(["git", "show", f"{ref}:{path}"], text=True)
        return json.loads(raw)
    except subprocess.CalledProcessError:
        return None


def haversine_nm(a: list[float], b: list[float]) -> float:
    lon1, lat1, lon2, lat2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    dlon, dlat = lon2 - lon1, lat2 - lat1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * math.asin(min(1.0, math.sqrt(h))) * 3440.065


def infer_published_lines(d: dict) -> tuple[int | None, str, list[str]]:
    """Return (count, source, line_hints)."""
    dn = d.get("domestic_network", {})
    hints: list[str] = []
    if isinstance(dn.get("published_lines"), list):
        for line in dn["published_lines"]:
            if isinstance(line, dict):
                hints.append(line.get("line_id") or line.get("name") or str(line))
            else:
                hints.append(str(line))
        return len(hints), "explicit", hints

    prec = d.get("precedent", {})
    counts: list[int] = []
    net = prec.get("network")
    if isinstance(net, str):
        hints.append(net[:200])
        fs = sorted(set(re.findall(r"\bF\d+\b", net)))
        if fs:
            counts.append(len(fs))
            hints.extend(fs)
        rbs = sorted(set(re.findall(r"\bRB\d+\b", net, re.I)))
        if rbs:
            counts.append(len(rbs))
            hints.extend(rbs)
        for pat, val in [
            (r"(\d+)[- ]route", None),
            (r"(\d+) routes", None),
            (r"(\d+) lines", None),
            (r"(\d+)-line", None),
        ]:
            m = re.search(pat, net, re.I)
            if m:
                counts.append(int(m.group(1)))
        if re.search(r"\bsix[- ]route", net, re.I):
            counts.append(6)
        if re.search(r"\bten[- ]route", net, re.I):
            counts.append(10)
        if "Routes incl." in net:
            counts.append(len([p for p in net.split(";") if p.strip()]))

    h = prec.get("headline", "")
    if h:
        hints.append(h[:120])
    for pat in [r"(\d+) routes", r"(\d+)-route", r"(\d+) lines", r"(\d+) stations"]:
        m = re.search(pat, h, re.I)
        if m:
            counts.append(int(m.group(1)))

    if counts:
        return max(counts), "inferred", hints
    return None, "unknown", hints


def pair_key(a: str, b: str) -> frozenset[str]:
    return frozenset({a, b})


def hub_nodes(pairs: list[dict], top_n: int = 2) -> list[str]:
    deg: Counter[str] = Counter()
    for p in pairs:
        deg[p["from"]] += 1
        deg[p["to"]] += 1
    return [n for n, _ in deg.most_common(top_n)]


def recommend_hub_spoke_pairs(d: dict) -> list[dict]:
    """Orphan core_live_station BPs → radial pairs from primary hub."""
    dn = d.get("domestic_network", {})
    bps = {b["node"]: b for b in dn.get("boarding_points", [])}
    pairs = list(dn.get("domestic_pairs", []))
    reg = d.get("regional_links", {}).get("links", [])
    existing = {pair_key(p["from"], p["to"]) for p in pairs}
    for p in reg:
        existing.add(pair_key(p["from"], p["to"]))

    used: set[str] = set()
    for p in pairs + reg:
        used.add(p["from"])
        used.add(p["to"])

    hubs = hub_nodes(pairs + reg)
    if not hubs:
        return []

    primary = hubs[0]
    if primary not in bps:
        return []

    recs: list[dict] = []
    slug = d.get("partner_id") or d.get("dossier_id", "").replace("pta-dossier-", "")
    for node, bp in bps.items():
        if node in used:
            continue
        if bp.get("type") in ("committed_new", "leisure_outer", "expansion_planned"):
            continue
        if node == primary:
            continue
        if pair_key(primary, node) in existing:
            continue
        hub_coord = bps[primary]["anchor_lnglat"]
        orphan_coord = bp["anchor_lnglat"]
        nm = round(haversine_nm(hub_coord, orphan_coord), 1)
        pair_id = f"{slug[:3]}-x{len(recs)+1:02d}"
        recs.append(
            {
                "pair_id": pair_id,
                "from": primary,
                "to": node,
                "approx_nm": nm,
                "rationale": f"Hub-spoke: {bps[primary].get('name')} ↔ {bp.get('name')} (orphan BP on published network)",
                "source": "grok/pair-gap-hub-spoke",
                "hub": primary,
            }
        )
        existing.add(pair_key(primary, node))
    return recs


def analyze_authority(slug: str) -> dict | None:
    ref = EXTRA_REFS.get(slug, REF_TIP)
    path = f"handoff/partner-map-model/PTA-DOSSIER-{slug}.json"
    d = git_show(ref, path)
    if not d:
        return None

    dn = d.get("domestic_network", {})
    bps = dn.get("boarding_points", [])
    pairs = dn.get("domestic_pairs", [])
    reg = d.get("regional_links", {}).get("links", [])

    bp_by_node = {b["node"]: b for b in bps}
    used: set[str] = set()
    for p in pairs + reg:
        used.add(p["from"])
        used.add(p["to"])
    orphans = [b for b in bps if b["node"] not in used]

    pub_n, pub_src, line_hints = infer_published_lines(d)
    recommended = recommend_hub_spoke_pairs(d)

    post_pairs = len(pairs) + len(recommended)
    gap_pub = (pub_n - len(pairs)) if pub_n is not None else None
    gap_post_pub = (pub_n - post_pairs) if pub_n is not None else None

    return {
        "partner_id": slug,
        "display": d.get("authority", {}).get("display", slug),
        "git_ref": ref,
        "boarding_points": len(bps),
        "bps_in_pairs": len(used),
        "orphan_bps": len(orphans),
        "orphan_pct": round(100 * len(orphans) / len(bps), 1) if bps else 0,
        "domestic_pairs": len(pairs),
        "regional_links": len(reg),
        "seal_targets_current": len(pairs) + len(reg),
        "published_lines_est": pub_n,
        "published_lines_source": pub_src,
        "published_line_hints": line_hints[:6],
        "pair_gap_vs_published": gap_pub,
        "coverage_pct_current": round(100 * len(pairs) / pub_n, 1) if pub_n else None,
        "hubs": hub_nodes(pairs + reg),
        "recommended_hub_spoke_pairs": len(recommended),
        "seal_targets_after_expansion": len(pairs) + len(reg) + len(recommended),
        "pair_gap_after_expansion": gap_post_pub,
        "coverage_pct_after_expansion": round(100 * post_pairs / pub_n, 1) if pub_n else None,
        "orphan_bp_nodes": [o["node"] for o in orphans],
        "orphan_bp_names": [o.get("name", "") for o in orphans],
        "current_pair_ids": [p.get("pair_id") for p in pairs],
        "recommended_pairs": recommended,
        "precedent_headline": d.get("precedent", {}).get("headline", "")[:160],
        "expansion_action": (
            "expand_hub_spoke"
            if len(recommended) > 0 and len(orphans) / max(len(bps), 1) >= 0.25
            else ("complete" if len(orphans) <= 2 else "review_orphans")
        ),
    }


def list_dossier_slugs() -> list[str]:
    raw = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", REF_TIP, "handoff/partner-map-model"],
        text=True,
    )
    slugs = []
    for line in raw.strip().split("\n"):
        m = re.match(r"handoff/partner-map-model/PTA-DOSSIER-(.+)\.json", line)
        if m:
            slugs.append(m.group(1))
    slugs.extend(EXTRA_REFS.keys())
    return sorted(set(slugs))


def render_md(report: dict) -> str:
    lines = [
        "# PTA Pair-Gap Table",
        "",
        f"Generated: {report['generated_at']}",
        "",
        "## Fleet summary",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
    ]
    t = report["totals"]
    for k, v in t.items():
        lines.append(f"| {k.replace('_', ' ')} | {v} |")

    lines.extend(
        [
            "",
            "## Per authority",
            "",
            "| Authority | BPs | Pairs | Orphans | Pub~lines | Gap | Rec+ | Seal after | Action |",
            "|-----------|-----|-------|---------|-----------|-----|------|------------|--------|",
        ]
    )
    for r in report["authorities"]:
        lines.append(
            f"| {r['partner_id']} | {r['boarding_points']} | {r['domestic_pairs']} | "
            f"{r['orphan_bps']} | {r['published_lines_est'] or '—'} | "
            f"{r['pair_gap_vs_published'] if r['pair_gap_vs_published'] is not None else '—'} | "
            f"+{r['recommended_hub_spoke_pairs']} | {r['seal_targets_after_expansion']} | "
            f"{r['expansion_action']} |"
        )

    lines.extend(["", "## Expansion detail (authorities with hub-spoke recs)", ""])
    for r in report["authorities"]:
        if not r["recommended_pairs"]:
            continue
        lines.append(f"### {r['display']} (`{r['partner_id']}`)")
        lines.append(f"- Hubs: `{', '.join(r['hubs'])}`")
        lines.append(f"- Orphans ({r['orphan_bps']}): {', '.join(r['orphan_bp_names'][:8])}{'…' if r['orphan_bps']>8 else ''}")
        lines.append(f"- Recommended +{len(r['recommended_pairs'])} hub-spoke pairs → seal targets {r['seal_targets_after_expansion']}")
        lines.append("")

    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true", help="Write JSON + MD artifacts")
    args = ap.parse_args()

    authorities = []
    for slug in list_dossier_slugs():
        row = analyze_authority(slug)
        if row:
            authorities.append(row)

    authorities.sort(key=lambda r: (-r["orphan_bps"], r["partner_id"]))

    report = {
        "schema": "pta_pair_gap_table/v1",
        "generated_at": utc_now(),
        "source_ref": REF_TIP,
        "authorities": authorities,
        "totals": {
            "authorities": len(authorities),
            "boarding_points": sum(a["boarding_points"] for a in authorities),
            "domestic_pairs_current": sum(a["domestic_pairs"] for a in authorities),
            "regional_links": sum(a["regional_links"] for a in authorities),
            "orphan_bps": sum(a["orphan_bps"] for a in authorities),
            "recommended_hub_spoke_pairs": sum(a["recommended_hub_spoke_pairs"] for a in authorities),
            "seal_targets_current": sum(a["seal_targets_current"] for a in authorities),
            "seal_targets_after_expansion": sum(a["seal_targets_after_expansion"] for a in authorities),
            "published_lines_est_sum": sum(a["published_lines_est"] or 0 for a in authorities),
        },
        "plan": {
            "merge_order": ["#141", "#142", "#143", "#144", "#145", "#146"],
            "expansion_rule": "Add hub-spoke pairs for orphan core_live_station BPs when orphan_pct >= 25%",
            "seal_rule": "Mint all dossier BPs; route all domestic_pairs + regional_links; interior_land_km == 0",
        },
    }

    print(json.dumps(report["totals"], indent=2))
    for a in authorities:
        print(
            f"{a['partner_id']:24} BPs={a['boarding_points']:2} pairs={a['domestic_pairs']:2} "
            f"orphan={a['orphan_bps']:2} rec+={a['recommended_hub_spoke_pairs']:2} "
            f"seal→{a['seal_targets_after_expansion']:3} {a['expansion_action']}"
        )

    if args.write:
        OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
        OUT_JSON.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
        OUT_MD.write_text(render_md(report))
        print(f"\nWrote {OUT_JSON}")
        print(f"Wrote {OUT_MD}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())