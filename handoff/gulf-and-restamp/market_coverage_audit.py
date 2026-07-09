#!/usr/bin/env python3
"""
Market coverage audit — repeatable scanner for "empty / sparse markets" and
missing connective tissue.

Root-cause taxonomy this scanner separates (do NOT conflate these):
  A. cluster_id taxonomy mismatch  — route.properties.cluster_id carries a
     non-canonical sub-region key (e.g. 'phuket-andaman', 'koh-samui-gulf') or a
     city_id instead of the canonical COUNTRY cluster_id. Deterministically
     restampable via endpoint city -> owning cluster (member_city_ids map).
  B. truly-empty markets  — canonical clusters with 0 routes attaching by
     endpoint-city membership (the renderer's authoritative rule). Real gap.
  C. sparse markets  — canonical clusters with 1..<THRESHOLD attached routes.
  D. isolated canonical cities  — member_city_ids that no corridor touches
     (the "very limited routes" complaint). Sourcing/mint targets.
  E. unresolved-endpoint routes  — routes whose endpoints resolve to NO canonical
     cluster (registry gap: CalMac / Norway fjords). Honest-null; nobody invents.

IDENTIFY = run this scanner. ADDRESS:
  A -> Tasklet emits restamp register, Grok applies (deterministic, no invention).
  B/C/D -> Tasklet flags, Grok sources real BPs + mints corridors (nobody invents a pier).
  E -> registry lane; honest-null until backing city features exist.

Rendering fact (scripts/build-site.mjs + scripts/route-display.mjs):
  A route attaches to a market by ENDPOINT-CITY membership, not by its own
  cluster_id. member_city_ids is the authoritative city->cluster map.
"""
import json, sys, argparse
from collections import Counter, defaultdict

SPARSE_THRESHOLD = 5

def load(routes_path, clusters_path):
    routes = json.load(open(routes_path))
    feats = routes['features'] if isinstance(routes, dict) else routes
    clusters = json.load(open(clusters_path))['clusters']
    return feats, clusters

def build_maps(clusters):
    city2cluster = {}
    for c in clusters:
        for m in c.get('member_city_ids', []):
            city2cluster[m] = c['cluster_id']
    return city2cluster

def audit(feats, clusters):
    canon = {c['cluster_id'] for c in clusters}
    city2cluster = build_maps(clusters)

    attach = Counter()          # cluster -> #routes touching by endpoint city
    touched = Counter()         # city_id -> #routes touching
    unresolved = []             # routes with no endpoint in any canonical cluster
    restamp = []                # A: route needs cluster_id fixed to canonical

    for f in feats:
        p = f['properties']
        fc, tc = p.get('from_city_id'), p.get('to_city_id')
        for cid in (fc, tc):
            if cid:
                touched[cid] += 1
        cf, ct = city2cluster.get(fc), city2cluster.get(tc)
        cs = {x for x in (cf, ct) if x}
        if not cs:
            unresolved.append(p.get('id'))
        for cl in cs:
            attach[cl] += 1
        # A: cluster_id mismatch
        cur = p.get('cluster_id')
        if cur not in canon:
            # deterministic target: single cluster, else from-side
            target = cf if cf else ct
            if len(cs) == 1:
                target = next(iter(cs))
            if target:
                restamp.append({'route_id': p.get('id'), 'old': cur, 'new': target,
                                'basis': f'endpoint city {fc or tc}'})

    empty = sorted(c['cluster_id'] for c in clusters if attach.get(c['cluster_id'], 0) == 0)
    sparse = sorted(((attach.get(c['cluster_id'], 0), c['cluster_id']) for c in clusters
                     if 0 < attach.get(c['cluster_id'], 0) < SPARSE_THRESHOLD))
    isolated = defaultdict(list)
    for c in clusters:
        for m in c.get('member_city_ids', []):
            if touched.get(m, 0) == 0:
                isolated[c['cluster_id']].append(m)

    return {
        'attach': attach, 'empty': empty, 'sparse': sparse,
        'isolated': {k: v for k, v in isolated.items()},
        'unresolved': unresolved, 'restamp': restamp,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--routes', default='ROUTES.json')
    ap.add_argument('--clusters', default='CLUSTERS.json')
    ap.add_argument('--json-out', default=None)
    a = ap.parse_args()
    feats, clusters = load(a.routes, a.clusters)
    r = audit(feats, clusters)
    print(f"routes={len(feats)} clusters={len(clusters)}")
    print(f"A restamp (cluster_id -> canonical): {len(r['restamp'])}")
    print(f"B truly-empty markets: {len(r['empty'])} -> {r['empty']}")
    print(f"C sparse markets (<{SPARSE_THRESHOLD}): {len(r['sparse'])}")
    print(f"D isolated canonical cities: {sum(len(v) for v in r['isolated'].values())} "
          f"across {len(r['isolated'])} clusters")
    print(f"E unresolved-endpoint routes: {len(r['unresolved'])}")
    if a.json_out:
        out = {
            'generated_for': 'market coverage gap audit',
            'sparse_threshold': SPARSE_THRESHOLD,
            'A_restamp': r['restamp'],
            'B_truly_empty_markets': r['empty'],
            'C_sparse_markets': [{'cluster_id': c, 'routes': n} for n, c in r['sparse']],
            'D_isolated_cities': r['isolated'],
            'E_unresolved_endpoint_route_ids': r['unresolved'],
        }
        json.dump(out, open(a.json_out, 'w'), ensure_ascii=True, indent=2)
        open(a.json_out, 'a').write('\n')
        print(f"wrote {a.json_out}")

if __name__ == '__main__':
    main()
