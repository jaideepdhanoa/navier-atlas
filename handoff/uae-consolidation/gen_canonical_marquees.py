#!/usr/bin/env python3
"""Generate canonical marquee_corridors[] per CITY across the whole roster (v2).

City-level sub-sets: every partner operating in a city inherits the SAME marquee
set for that city (e.g. all UAE partners see the same Dubai set, the same Abu
Dhabi set). A partner's featured/wow = union of the marquee sets for the cities
in its clusters.

Curation is ID-based and OD-pair level (BP node pair + city_id + cluster_id).
route_id is carried as a hint; Grok binds/re-stamps route_id after reseal.

Quality = HERO ranking (water beats road), not popularity:
  * in-range (0.4-30 nm), on-water, not quarantined/hidden/land-flagged
  * distance floor: drop intra-city hops < 3 nm UNLESS an island endpoint
  * junk-endpoint filter: jet-ski / water-sports / helipad / seaplane / slipway /
    parking / mislabeled cross-border artifacts are excluded
  * hero score = distance sweet-spot (~12 nm) + island endpoint + cross-city
    water-advantage; traffic_weight / crowd-features are TIEBREAKERS only
Out-of-range / land-crossing junk (Abu Dhabi->Muscat, Barcelona->Palma) and
trivial 2 nm resort hops cannot enter the set by construction.

Outputs:
  CANONICAL-MARQUEES.json  - per-city canonical wow (<=5) + featured (<=8)
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

IN_RANGE=(0.4,30.0)
ISLAND=re.compile(r'island|palm|saadiyat|\byas\b|world islands|sir bani|delma|lulu|reem|al aliah|marjan|nurai|zaya|جزيرة',re.I)
JUNK=re.compile(r'jet ?ski|water ?sport|waves marine|helipad|seaplane|slipway|parking|cross-border\b.*endpoint|quanta|lr endpoint|dry dock|boat ?yard',re.I)

def num(v):
    try: return float(v)
    except: return 0.0

def is_clean(p):
    if p.get('_qa_land_flag') or p.get('_quarantine'): return False
    if p.get('relevance')=='hide': return False
    lk=p.get('_geometry_land_km') or p.get('_land_km_interior') or 0
    if lk and lk>0.2: return False
    d=p.get('distance_nm') or 0
    if not (IN_RANGE[0]<=d<=IN_RANGE[1]): return False
    fl,tl=p.get('from_label'),p.get('to_label')
    if not (fl and tl): return False
    blob=f"{fl} {tl}"
    if JUNK.search(blob): return False
    def basew(s): return re.sub(r'[^a-z]','',str(s).lower())[:18]
    if basew(fl)==basew(tl): return False           # self-referential
    return True

def hero_eligible(p):
    d=p.get('distance_nm') or 0
    return d>=3.0                                     # firm floor: no trivial hops, no exceptions

def hero_score(p,feat_freq):
    d=p.get('distance_nm') or 0
    isl=1 if ISLAND.search(f"{p.get('from_label')} {p.get('to_label')}") else 0
    xcity=1 if p.get('from_city_id')!=p.get('to_city_id') else 0
    sweet=1-abs(min(d,25)-12)/25.0                   # peaks ~12 nm
    planned=1 if re.search(r'planned|under construction|proposed',f"{p.get('from_label')} {p.get('to_label')}",re.I) else 0
    key=frozenset((p.get('from'),p.get('to')))
    return (3.0*sweet + 2.0*isl + 2.5*xcity
            + 0.5*num(p.get('traffic_weight')) + 0.3*feat_freq.get(key,0)
            + 0.2*num(p.get('relevance') if isinstance(p.get('relevance'),(int,float)) else 0)
            - 0.6*planned)

# ---- harvest current featured/wow across partners (ID-based) ----
feat_freq=collections.Counter()
feat_partners=collections.defaultdict(set)
current_entries=[]

def harvest(container,partner,kind,market=None):
    for e in (container or []):
        if isinstance(e,str):
            current_entries.append({'partner':partner,'kind':kind,'market':market,'schema':'string','text':e,'resolved':False}); continue
        if isinstance(e,dict):
            fn=e.get('from_node_id'); tn=e.get('to_node_id')
            key=frozenset((fn,tn)) if fn and tn else None
            if key: feat_freq[key]+=1; feat_partners[key].add(partner)
            current_entries.append({'partner':partner,'kind':kind,'market':market,'schema':'dict',
                'from_label':e.get('from_label'),'to_label':e.get('to_label'),
                'from_node_id':fn,'to_node_id':tn,'route_id':e.get('route_id')})

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

# ---- build clean candidate pool grouped by CITY (inter-city -> both cities) ----
city_label={}
city_candidates=collections.defaultdict(dict)   # city_id -> {bpkey: cand}
for r in routes:
    p=r['properties']
    if not is_clean(p) or not hero_eligible(p): continue
    fc,tc=p.get('from_city_id'),p.get('to_city_id')
    if p.get('from_city'): city_label[fc]=p.get('from_city')
    if p.get('to_city'):   city_label[tc]=p.get('to_city')
    key=frozenset((p.get('from'),p.get('to')))
    cand={'route_id':p.get('id'),'from_node_id':p.get('from'),'to_node_id':p.get('to'),
          'from_label':p.get('from_label'),'to_label':p.get('to_label'),
          'from_city_id':fc,'to_city_id':tc,
          'distance_nm':round(p.get('distance_nm') or 0,1),'trip_scope':p.get('trip_scope'),
          'hero_score':round(hero_score(p,feat_freq),2),
          '_island':bool(ISLAND.search(f"{p.get('from_label')} {p.get('to_label')}")),
          '_cross_city':fc!=tc,
          'partners_currently_featuring':sorted(feat_partners.get(key,set()))}
    for cid in {fc,tc}:
        if not cid: continue
        # keep the higher-scoring instance if duplicate bpkey lands in a city twice
        if key not in city_candidates[cid] or cand['hero_score']>city_candidates[cid][key]['hero_score']:
            city_candidates[cid][key]=cand

# ---- select per-city canonical wow (<=5) + featured (<=8) ----
WOW_N, FEAT_N = 5, 8
out_cities={}
canonical_keys=set()
for cid,cands in city_candidates.items():
    ranked=sorted(cands.values(),key=lambda c:-c['hero_score'])
    wow=ranked[:WOW_N]
    featured=ranked[:FEAT_N]
    for i,c in enumerate(wow): c_=dict(c); c_['rank']=i+1
    for c in featured: canonical_keys.add(frozenset((c['from_node_id'],c['to_node_id'])))
    def stamp(lst): return [{**c,'rank':i+1} for i,c in enumerate(lst)]
    out_cities[cid]={
        'city_id':cid,'city_label':city_label.get(cid,cid),
        'cluster_id':city2cluster.get(cid),'cluster_label':cluster_label.get(city2cluster.get(cid)),
        'n_clean_candidates':len(cands),
        'marquee_wow':stamp(wow),'marquee_featured':stamp(featured)}

# ---- retire list: current entries not in any canonical city set ----
retire=[]
for e in current_entries:
    if e['schema']=='string':
        retire.append({**e,'reason':'free_text_string_no_id'}); continue
    key=frozenset((e.get('from_node_id'),e.get('to_node_id'))) if e.get('from_node_id') and e.get('to_node_id') else None
    if key is None:
        retire.append({**e,'reason':'no_bp_ids'})
    elif key not in canonical_keys:
        retire.append({**e,'reason':'not_in_canonical_city_set'})

out={'_meta':{'generated':'2026-07-05','granularity':'city','wow_max':WOW_N,'featured_max':FEAT_N,
      'n_cities':len(out_cities),'ranking':'hero (water-beats-road): distance sweet-spot + island + cross-city; traffic/crowd = tiebreaker',
      'quality_gate':'in-range 3-30nm firm floor, on-water, junk-endpoint filter, no trivial <3nm hops'},
     'cities':out_cities}
json.dump(out,open(os.path.join(BASE,'CANONICAL-MARQUEES.json'),'w'),indent=2)
json.dump({'generated':'2026-07-05','total_current_entries':len(current_entries),
      'retired_count':len(retire),'retired':retire},
      open(os.path.join(BASE,'MARQUEE-RETIRE-LIST.json'),'w'),indent=2)

# ---- console summary ----
cities_with_signal=sum(1 for c in out_cities.values() if c['marquee_wow'])
print(f"cities: {len(out_cities)} ({cities_with_signal} with >=1 marquee)")
print(f"current marquee entries: {len(current_entries)}  |  retired: {len(retire)}")
sc=collections.Counter(e['reason'] for e in retire)
print("retire reasons:",dict(sc))
for cid in ['dubai-uae','abu-dhabi-uae','sharjah-uae','ras-al-khaimah-uae']:
    c=out_cities.get(cid)
    if not c: continue
    print(f"\n=== {c['city_label']} ({cid}) — {c['n_clean_candidates']} clean cands ===")
    for m in c['marquee_wow']:
        tag='island' if m['_island'] else ('x-city' if m['_cross_city'] else '')
        print(f"  {m['rank']}. {m['hero_score']:4.1f} | {m['distance_nm']:4.1f}nm {tag:6s} | {m['from_label']} -> {m['to_label']}")
