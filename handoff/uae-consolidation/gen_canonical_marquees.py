#!/usr/bin/env python3
"""Generate canonical marquee_corridors[] per cluster across the whole roster.

Curation is ID-based and OD-pair level (BP node pair + cluster_id). route_id is
carried as a hint; Grok binds/re-stamps route_id after reseal. Quality gate keeps
only clean, on-water, in-range, named corridors — so land-crossers/out-of-range
junk (Abu Dhabi->Muscat, Barcelona->Palma) cannot enter the marquee set.

Outputs:
  CANONICAL-MARQUEES.json  - per-cluster canonical wow (<=6) + featured (<=8)
  MARQUEE-RETIRE-LIST.json - current featured/wow entries NOT in canonical set
"""
import json, glob, os, collections, re

BASE=os.path.dirname(os.path.abspath(__file__))
routes=json.load(open(os.path.join(BASE,'ROUTES.json')))
clusters=json.load(open(os.path.join(BASE,'CLUSTERS.json')))['clusters']

# ---- city_id -> cluster_id ----
city2cluster={}
for cl in clusters:
    for cid in cl.get('member_city_ids',[]):
        city2cluster[cid]=cl['cluster_id']
cluster_label={cl['cluster_id']:cl['cluster_label'] for cl in clusters}

# ---- index routes ----
IN_RANGE=(0.4,30.0)  # nm; N30 sweet spot, drop trivial hops & out-of-range
def route_cluster(p):
    a=city2cluster.get(p.get('from_city_id'))
    b=city2cluster.get(p.get('to_city_id'))
    if a and a==b: return a          # intra-cluster
    if a and b:    return None       # cross-cluster (handle separately)
    return a or b

def is_clean(p):
    if p.get('_qa_land_flag'): return False
    if p.get('_quarantine'): return False
    lk=p.get('_geometry_land_km') or p.get('_land_km_interior') or 0
    if lk and lk>0.2: return False
    d=p.get('distance_nm') or 0
    if not (IN_RANGE[0]<=d<=IN_RANGE[1]): return False
    fl,tl=p.get('from_label'),p.get('to_label')
    if not (fl and tl): return False
    # drop self-referential corridors (endpoints share the same place name)
    def base(s): return re.sub(r'[^a-z]','',str(s).lower())[:18]
    if base(fl)==base(tl): return False
    return True

LABEL_NOISE=re.compile(r'RESOLVED|Nominatim|in-bbox|OSM|ferry_terminal|geocod|provenance',re.I)

# BP-pair key (order-independent) -> route props
bp_index={}
route_by_id={}
for r in routes:
    p=r['properties']
    rid=p.get('id')
    if rid: route_by_id[rid]=p
    fn,tn=p.get('from'),p.get('to')
    if fn and tn:
        bp_index[frozenset((fn,tn))]=p

# ---- gather current featured/wow across all partners (ID-based where possible) ----
feature_freq=collections.Counter()   # bp-pair key -> #partners featuring
feature_partners=collections.defaultdict(set)
current_entries=[]                    # raw current marquee entries for retire audit

def norm_wt(v):
    try: return float(v)
    except: return 0.0

def harvest(container,partner,kind,market=None):
    for e in (container or []):
        if isinstance(e,str):
            current_entries.append({'partner':partner,'kind':kind,'market':market,'schema':'string','text':e,'resolved':False})
            continue
        if isinstance(e,dict):
            fn=e.get('from_node_id'); tn=e.get('to_node_id')
            key=frozenset((fn,tn)) if fn and tn else None
            resolved=bool(key and key in bp_index)
            if key:
                feature_freq[key]+=1
                feature_partners[key].add(partner)
            current_entries.append({'partner':partner,'kind':kind,'market':market,
                'schema':'dict','from_label':e.get('from_label'),'to_label':e.get('to_label'),
                'from_node_id':fn,'to_node_id':tn,'route_id':e.get('route_id'),'resolved':resolved})

for f in sorted(glob.glob(os.path.join(BASE,'partners','*.json'))):
    partner=os.path.basename(f)[:-5]
    d=json.load(open(f))
    def wow_of(obj):
        w=obj.get('why_navier_now') if isinstance(obj,dict) else None
        return w.get('wow_corridors') if isinstance(w,dict) else None
    for ph in d.get('phases',[]):
        if isinstance(ph,dict): harvest(ph.get('featured_routes'),partner,'featured')
    harvest(wow_of(d),partner,'wow')
    for m in (d.get('markets') or []):
        if not isinstance(m,dict): continue
        mk=m.get('market') or m.get('name') or m.get('market_id')
        for ph in (m.get('phases') or []):
            if isinstance(ph,dict): harvest(ph.get('featured_routes'),partner,'featured',mk)
        harvest(wow_of(m),partner,'wow',mk)

# ---- build clean intra-cluster candidate pool ----
cluster_candidates=collections.defaultdict(list)
for r in routes:
    p=r['properties']
    cid=route_cluster(p)
    if not cid: continue
    if not is_clean(p): continue
    key=frozenset((p.get('from'),p.get('to')))
    planned=1 if re.search(r'planned|under construction|proposed',(str(p.get('from_label'))+str(p.get('to_label'))),re.I) else 0
    score=0.6*norm_wt(p.get('traffic_weight')) + 1.5*feature_freq.get(key,0) + 0.4*norm_wt(p.get('relevance')) - 0.5*planned
    cluster_candidates[cid].append({
        'route_id':p.get('id'),'from_node_id':p.get('from'),'to_node_id':p.get('to'),
        'from_label':p.get('from_label'),'to_label':p.get('to_label'),
        'distance_nm':round(p.get('distance_nm') or 0,1),'cluster_id':cid,
        'traffic_weight':norm_wt(p.get('traffic_weight')),
        'partner_feature_count':feature_freq.get(key,0),
        'partners_currently_featuring':sorted(feature_partners.get(key,set())),
        '_planned':bool(planned),
        '_score':round(score,3),
    })

# ---- select canonical wow(<=6)/featured(<=8) per cluster ----
canonical={}
for cid,cands in cluster_candidates.items():
    # dedupe by bp-pair keep highest score
    best={}
    for c in cands:
        k=frozenset((c['from_node_id'],c['to_node_id']))
        if k not in best or c['_score']>best[k]['_score']: best[k]=c
    ranked=sorted(best.values(),key=lambda c:-c['_score'])
    # quality floor: a marquee must be crowd-featured (>=1 partner) OR have real
    # traffic signal (score>=0.5). Significant-and-clean beats padding with junk.
    strong=[c for c in ranked if c['partner_feature_count']>=1 or c['_score']>=0.5]
    pool=strong if strong else ranked[:3]   # never leave a cluster empty if clean routes exist
    wow=pool[:6]
    featured=pool[:8]
    canonical[cid]={
        'cluster_id':cid,'cluster_label':cluster_label.get(cid,cid),
        'clean_candidate_count':len(ranked),'strong_candidate_count':len(strong),
        'marquee_wow':wow,'marquee_featured':featured,
    }

# ---- retire list: current entries whose bp-pair is NOT in that cluster's canonical set,
#      plus every unresolved string / dirty entry ----
canon_keys=set()
for cid,v in canonical.items():
    for c in v['marquee_featured']:
        canon_keys.add(frozenset((c['from_node_id'],c['to_node_id'])))
retire=[]
for e in current_entries:
    if e['schema']=='string':
        retire.append({**e,'reason':'free-text-string (no ID) — retire, non-canonical schema'})
    else:
        key=frozenset((e.get('from_node_id'),e.get('to_node_id')))
        if not e['resolved']:
            retire.append({**e,'reason':'unresolved BP pair (not in ROUTES) — retire'})
        elif key not in canon_keys:
            retire.append({**e,'reason':'not in cluster canonical top set — retire/archive'})

out={'generated':'2026-07-05','method':'ID-based OD-pair curation; quality-gated; route_id is a hint for Grok to bind post-reseal',
     'range_nm':IN_RANGE,'clusters_with_canonical':len(canonical),
     'total_clean_candidates':sum(len(v['marquee_featured']) for v in canonical.values()),
     'clusters':canonical}
json.dump(out,open(os.path.join(BASE,'CANONICAL-MARQUEES.json'),'w'),indent=2)
json.dump({'generated':'2026-07-05','total_current_entries':len(current_entries),
           'total_retired':len(retire),'retire':retire},
          open(os.path.join(BASE,'MARQUEE-RETIRE-LIST.json'),'w'),indent=2)

# ---- human-readable review for contested markets ----
CONTESTED=['uae','thailand','indonesia','india','colombia','singapore','qatar','egypt','morocco','tunisia']
lines=["# Canonical marquee sets — review (contested markets)",
       "",f"_Generated 2026-07-05 · ID-based OD-pair curation · quality-gated · route_id is a Grok-bind hint._","",
       "Every partner sharing a market inherits the **same** set below. Land-crossers & out-of-range junk are excluded by the quality gate.",""]
name2cluster={}
for cl in clusters:
    for t in [cl['cluster_id']]:
        name2cluster[t]=cl['cluster_id']
for cid in CONTESTED:
    v=canonical.get(cid)
    if not v:
        lines.append(f"## {cid}\n_(no clean intra-cluster candidates — corridors may be cross-border only; Grok to confirm post-reseal)_\n")
        continue
    lines.append(f"## {v['cluster_label']} (`{cid}`)")
    lines.append(f"_{v['clean_candidate_count']} clean candidates · {v['strong_candidate_count']} strong · showing canonical wow (≤6):_\n")
    lines.append("| # | Marquee corridor | nm | currently featured by |")
    lines.append("|---|---|---|---|")
    for i,c in enumerate(v['marquee_wow'],1):
        pf=', '.join(c['partners_currently_featuring']) or '—'
        lines.append(f"| {i} | {c['from_label']} ↔ {c['to_label']} | {c['distance_nm']} | {pf} |")
    lines.append("")
open(os.path.join(BASE,'CANONICAL-MARQUEES-REVIEW.md'),'w').write("\n".join(lines))

# ---- console summary ----
print("clusters with canonical marquees:",len(canonical))
print("total current marquee entries:",len(current_entries))
print("total retired (non-canonical/dirty/unresolved):",len(retire))
print("string-schema entries (auto-retire):",sum(1 for e in current_entries if e['schema']=='string'))
print("unresolved dict entries:",sum(1 for e in current_entries if e['schema']=='dict' and not e['resolved']))
# UAE worked example
for cid in ['uae']:
    v=canonical.get(cid)
    if v:
        print(f"\n=== {cid} ({v['cluster_label']}) — {v['clean_candidate_count']} clean candidates ===")
        for c in v['marquee_featured']:
            print(f"  [{c['_score']:.1f}] {c['from_label']} -> {c['to_label']}  ({c['distance_nm']}nm) feat_by={c['partner_feature_count']}")