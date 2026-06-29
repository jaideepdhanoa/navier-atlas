#!/usr/bin/env python3
"""
validate-region-briefs.py — completeness + integrity gate for macro-region briefs.

Region briefs (data-clean/region_briefs.json) feed the /region/<slug> browse panel
and share card. They shipped as tagline+summary stubs; this gate enforces the same
depth the cluster/city briefs carry, so a thin region can never silently reach a
partner-facing surface again.

Per region it checks:
  • summary has real body                       (>= 250 chars)
  • why_marine_mobility present
  • demand_signals present                       (>= 2; cluster-depth wants more)
  • use_cases are structured {archetype,title,body[,platform]}  (>= 1)
  • navier_fit is {pioneer_ii[, quanta_lr]} — not a flat string
  • scope_stats {clusters, cities} present AND clusters == the number of clusters
    whose normalised region maps to this brief (so the panel grid == share card)
  • signature_routes: null/[] allowed (regions with no sealed corridors), but every
    route_id present MUST resolve in data-clean/ROUTES.json (ID-match; null beats
    confidently-wrong)

Usage:
    python3 scripts/validate-region-briefs.py [--strict]
Exit code 1 (with --strict) if any region fails.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DC = os.path.join(ROOT, "data-clean")
STRICT = "--strict" in sys.argv

# Mirror REGION_ALIASES (region-share.mjs) / _REGION_DISPLAY_ALIAS (index.html).
REGION_ALIASES = {
    "SEA": "Southeast Asia",
    "LatAm-Caribbean": "Latin America", "Latin-America": "Latin America",
    "Caribbean": "Caribbean",
    "Europe-Mediterranean": "Europe", "Europe-Atlantic": "Europe",
    "Europe-Baltic": "Europe", "Europe-Med": "Europe",
    "Asia": "East Asia",
    "Middle East": "MENA", "Maghreb": "MENA",
    "Caucasus": "Caspian", "Central Asia": "Caspian",
}
def norm_region(r):
    return REGION_ALIASES.get(r, r)


def load_route_ids():
    routes = json.load(open(os.path.join(DC, "ROUTES.json")))
    feats = routes.get("features", routes) if isinstance(routes, dict) else routes
    ids = set()
    for f in feats:
        rid = (f.get("properties") or {}).get("id")
        if rid:
            ids.add(rid)
    return ids


def cluster_counts_by_display():
    clusters = json.load(open(os.path.join(DC, "CLUSTERS.json")))["clusters"]
    counts = {}
    for c in clusters:
        d = norm_region(c.get("region"))
        counts[d] = counts.get(d, 0) + 1
    return counts


def check(slug, rb, route_ids, cluster_counts):
    f = []
    s = rb.get("summary", "") or ""
    if len(s) < 250:
        f.append(f"summary thin ({len(s)} chars; want >=250)")
    if not rb.get("why_marine_mobility"):
        f.append("no why_marine_mobility")

    ds = rb.get("demand_signals")
    if not ds:
        f.append("no demand_signals")
    elif len(ds) < 2:
        f.append(f"demand_signals thin ({len(ds)}; want >=2)")

    uc = rb.get("use_cases")
    if not uc:
        f.append("no use_cases")
    elif any(isinstance(x, str) for x in uc):
        f.append("use_cases are bare strings — need {archetype,title,body}")
    elif any(not (isinstance(x, dict) and x.get("body")) for x in uc):
        f.append("use_cases missing 'body'")

    nf = rb.get("navier_fit")
    if not nf:
        f.append("no navier_fit")
    elif isinstance(nf, str):
        f.append("navier_fit is a flat string — need {pioneer_ii[, quanta_lr]}")
    elif not nf.get("pioneer_ii"):
        f.append("navier_fit missing pioneer_ii")

    ss = rb.get("scope_stats")
    display = rb.get("display", slug)
    if not ss or not ss.get("clusters") or not ss.get("cities"):
        f.append("scope_stats missing clusters/cities")
    else:
        expect = cluster_counts.get(display, 0)
        if ss["clusters"] != expect:
            f.append(f"scope_stats.clusters={ss['clusters']} != {expect} clusters tagged '{display}' "
                     "(panel grid / share card would disagree)")

    # signature_routes: null/empty OK; any route_id present must resolve.
    sr = rb.get("signature_routes")
    if sr:
        for r in sr:
            if isinstance(r, str):
                f.append(f"signature_route is a bare string ('{r}') — need {{label, route_id}}")
                continue
            rid = r.get("route_id")
            rids = ([rid] if rid else []) + list(r.get("route_ids") or [])
            if not rids:
                f.append(f"signature_route '{r.get('label','?')}' has no route_id")
            for x in rids:
                if x not in route_ids:
                    f.append(f"signature_route '{r.get('label','?')}' route_id '{x}' not in ROUTES.json")
    return f


def main():
    rb_all = json.load(open(os.path.join(DC, "region_briefs.json")))
    route_ids = load_route_ids()
    cluster_counts = cluster_counts_by_display()
    regions = {k: v for k, v in rb_all.items() if k != "_doc"}
    bad = {}
    for slug, rb in regions.items():
        iss = check(slug, rb, route_ids, cluster_counts)
        if iss:
            bad[slug] = iss
    print(f"Audited {len(regions)} region briefs — {len(bad)} incomplete, "
          f"{len(regions)-len(bad)} at cluster-depth standard.\n")
    for slug in sorted(bad):
        print(f"  \u2717 {slug}")
        for i in bad[slug]:
            print(f"      - {i}")
    if not bad:
        print("  \u2713 all regions pass.")
    if bad and STRICT:
        sys.exit(1)


if __name__ == "__main__":
    main()
