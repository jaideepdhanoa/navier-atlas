#!/usr/bin/env python3
"""Generate canonical marquee_corridors[] per (CLUSTER, CITY) across the roster (v2.3).

City-level sub-sets: every partner operating in a city inherits the SAME marquee
set for that (cluster::city). A partner's featured/wow = union of the marquee sets
for the cities in its clusters. Curation is ID-based and OD-pair level
(BP node pair + city_id + cluster_id). route_id binds directly from the sealed
`properties.id` / manifest `route_id` — no re-stamp.

Quality = HERO ranking (water beats road), not popularity:
  * in-range (0.4-30 nm), on-water, not quarantined/hidden/land-flagged
  * firm 3 nm distance floor: no trivial intra-city hops (no island exemption)
  * junk-endpoint filter: jet-ski / water-sports / helipad / seaplane / slipway /
    parking / mislabeled cross-border artifacts excluded
  * hero score = distance sweet-spot (~12 nm) + island endpoint + cross-city
    water-advantage; traffic_weight / crowd-features are TIEBREAKERS only
  * river exception (RIVER_CITIES): iconic river hops allowed to 0.4 nm, river score

Two input sources (v2.3):
  --source manifests --manifests-dir DIR   sealed slim manifests {cluster}.json
                                           (Grok Pass-1 output; route_id from `route_id`)
  --source routes    --routes PATH         full data-clean/ROUTES.json (route_id from `properties.id`)

Outputs (to --out-dir):
  CANONICAL-MARQUEES.json  - per (cluster::city) canonical wow (<=5) + featured (<=8)
  LABEL-SCRUB.json         - aggregate-label trims + needs_bp_sourcing flags
  SUSPECT-ENDPOINTS.json   - mis-geocoded business-POI endpoints (locale-cleanup lane)
  MARQUEE-RETIRE-LIST.json - (routes mode only) current featured/wow not in canonical set
"""
import json, glob, os, collections, re, argparse

IN_RANGE=(0.4,30.0)
ISLAND=re.compile(r'island|palm|saadiyat|\byas\b|world islands|sir bani|delma|lulu|reem|al aliah|marjan|nurai|zaya|جزيرة',re.I)
JUNK=re.compile(r'jet ?ski|water ?sport|waves marine|helipad|seaplane|slipway|parking|cross-border\b.*endpoint|quanta|lr endpoint|dry dock|boat ?yard|under ?construction|for construction|harbour office|harbor office|sea ?port st|fishermen|medical cent|hospital|clinic|mineral water|gulf craft|\bllc\b|factory|\bmall\b|mineral',re.I)

# ---- River cities: iconic short-hop exception to the firm 3nm floor ----
RIVER_CITIES={'bangkok-thailand'}
RIVER_FLOOR=0.4
ICON=re.compile(r'iconsiam|grand palace|wat |wat$|oriental|asiatique|khao ?san|phra ar?thit|tha chang|tha tien|wang lang|temple of dawn',re.I)

# ---- Label scrub: aggregate region labels -> primary place name (explicit, no guessing) ----
LABEL_SCRUB={
 'Cartagena & The Rosario Islands':'Cartagena',
 'Mahé & Inner Islands':'Mahé','Mahé & the Inner Islands':'Mahé',
 'Bora Bora & Society Islands':'Bora Bora','Bora & Society Islands':'Bora Bora',
 'Hvar & the Pakleni Islands':'Hvar',
 'Korčula & the South Dalmatian Islands':'Korčula',
}
NEEDS_SOURCING={'Andaman & Nicobar Islands','US & British Virgin Islands'}

# ---- Country suffixes for city_id -> display label prettify (city_ids are country-suffixed slugs) ----
COUNTRY_SUFFIXES=['costa-rica','dominican-republic','south-africa','new-zealand','saudi-arabia',
 'thailand','indonesia','malaysia','india','uae','qatar','korea','greece','italy','spain',
 'croatia','cyprus','ireland','sweden','monaco','panama','egypt','france','portugal','oman',
 'bahrain','kuwait','maldives','philippines','vietnam','singapore']

def prettify_city(cid):
    if not cid: return cid
    s=cid
    for suf in sorted(COUNTRY_SUFFIXES,key=len,reverse=True):
        if s.endswith('-'+suf):
            s=s[:-(len(suf)+1)]; break
    return ' '.join(w.capitalize() for w in s.split('-')) or cid

def num(v):
    try: return float(v)
    except: return 0.0

# ---- module-level accumulators (reset per run) ----
_junk_suspects={}
_scrub_applied={}
_scrub_sourcing={}

def scrub_label(lab,node_id,city_id):
    if lab in LABEL_SCRUB:
        clean=LABEL_SCRUB[lab]
        if node_id: _scrub_applied[node_id]={'orig':lab,'clean':clean}
        return clean
    if lab in NEEDS_SOURCING and node_id:
        _scrub_sourcing[node_id]={'label':lab,'city_id':city_id}
    return lab

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
    if JUNK.search(blob):
        if JUNK.search(str(fl)): _junk_suspects[p.get('from')]=fl
        if JUNK.search(str(tl)): _junk_suspects[p.get('to')]=tl
        return False
    def basew(s): return re.sub(r'[^a-z]','',str(s).lower())[:18]
    if basew(fl)==basew(tl): return False
    return True

def hero_eligible(p):
    d=p.get('distance_nm') or 0
    if p.get('from_city_id') in RIVER_CITIES or p.get('to_city_id') in RIVER_CITIES:
        return d>=RIVER_FLOOR
    return d>=3.0                                     # firm floor: no trivial hops

def is_river(p):
    return p.get('from_city_id') in RIVER_CITIES or p.get('to_city_id') in RIVER_CITIES

def river_score(p,feat_freq):
    d=p.get('distance_nm') or 0
    icon=1 if ICON.search(f"{p.get('from_label')} {p.get('to_label')}") else 0
    key=frozenset((p.get('from'),p.get('to')))
    return (2.0*num(p.get('traffic_weight')) + 2.0*icon
            + 0.4*min(d,3.0) + 0.3*feat_freq.get(key,0))

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

# ---- input loaders: both yield a list of `properties`-shaped dicts with `id` ----
def load_from_routes(path):
    routes=json.load(open(path))
    props=[]
    for r in routes:
        p=dict(r['properties'])
        props.append(p)
    return props

def load_from_manifests(mdir):
    props=[]
    for f in sorted(glob.glob(os.path.join(mdir,'*.json'))):
        d=json.load(open(f))
        rows=d if isinstance(d,list) else (d.get('routes') or d.get('corridors') or next((v for v in d.values() if isinstance(v,list)),[]))
        for row in rows:
            p=dict(row)
            p['id']=row.get('route_id') or row.get('id')   # normalize route_id -> id
            props.append(p)
    return props

def harvest_partners(pdir):
    feat_freq=collections.Counter(); feat_partners=collections.defaultdict(set); current=[]
    def harvest(container,partner,kind,market=None):
        for e in (container or []):
            if isinstance(e,str):
                current.append({'partner':partner,'kind':kind,'market':market,'schema':'string','text':e}); continue
            if isinstance(e,dict):
                fn=e.get('from_node_id'); tn=e.get('to_node_id')
                key=frozenset((fn,tn)) if fn and tn else None
                if key: feat_freq[key]+=1; feat_partners[key].add(partner)
                current.append({'partner':partner,'kind':kind,'market':market,'schema':'dict',
                    'from_label':e.get('from_label'),'to_label':e.get('to_label'),
                    'from_node_id':fn,'to_node_id':tn,'route_id':e.get('route_id')})
    for f in sorted(glob.glob(os.path.join(pdir,'*.json'))):
        partner=os.path.basename(f)[:-5]; d=json.load(open(f))
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
    return feat_freq,feat_partners,current

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',choices=['manifests','routes'],default='manifests')
    ap.add_argument('--manifests-dir',default='sealed-corridors')
    ap.add_argument('--routes',default='ROUTES.json')
    ap.add_argument('--clusters',default='CLUSTERS.json')
    ap.add_argument('--partners',default=None,help='optional partners/ dir for retire-list harvest')
    ap.add_argument('--out-dir',default='.')
    ap.add_argument('--date',default='2026-07-06')
    a=ap.parse_args()

    clusters=json.load(open(a.clusters))
    clusters=clusters['clusters'] if isinstance(clusters,dict) else clusters
    city2cluster={}
    for cl in clusters:
        for cid in cl.get('member_city_ids',[]):
            city2cluster[cid]=cl['cluster_id']
    cluster_label={cl['cluster_id']:cl.get('cluster_label') for cl in clusters}

    props = load_from_manifests(a.manifests_dir) if a.source=='manifests' else load_from_routes(a.routes)

    feat_freq,feat_partners,current_entries = (collections.Counter(),collections.defaultdict(set),[])
    if a.partners and os.path.isdir(a.partners):
        feat_freq,feat_partners,current_entries = harvest_partners(a.partners)

    city_label={}
    city_candidates=collections.defaultdict(dict)   # (cluster_id, city_id) -> {bpkey: cand}
    n_seen=0; n_clean=0
    for p in props:
        n_seen+=1
        if not is_clean(p) or not hero_eligible(p): continue
        n_clean+=1
        fc,tc=p.get('from_city_id'),p.get('to_city_id')
        if p.get('from_city'): city_label[fc]=p.get('from_city')
        if p.get('to_city'):   city_label[tc]=p.get('to_city')
        rcl=p.get('cluster_id') or city2cluster.get(fc) or city2cluster.get(tc)
        key=frozenset((p.get('from'),p.get('to')))
        riv=is_river(p)
        flab=scrub_label(p.get('from_label'),p.get('from'),fc)
        tlab=scrub_label(p.get('to_label'),p.get('to'),tc)
        score=river_score(p,feat_freq) if riv else hero_score(p,feat_freq)
        cand={'route_id':p.get('id'),'from_node_id':p.get('from'),'to_node_id':p.get('to'),
              'from_label':flab,'to_label':tlab,
              'from_city_id':fc,'to_city_id':tc,'cluster_id':rcl,
              'distance_nm':round(p.get('distance_nm') or 0,1),'trip_scope':p.get('trip_scope'),
              'hero_score':round(score,2),'_river':riv,
              '_island':bool(ISLAND.search(f"{p.get('from_label')} {p.get('to_label')}")),
              '_cross_city':fc!=tc,
              'partners_currently_featuring':sorted(feat_partners.get(key,set()))}
        for cid in {fc,tc}:
            if not cid: continue
            gk=(rcl,cid)
            if key not in city_candidates[gk] or cand['hero_score']>city_candidates[gk][key]['hero_score']:
                city_candidates[gk][key]=cand

    WOW_N, FEAT_N = 5, 8
    out_cities={}; canonical_keys=set()
    for (rcl,cid),cands in city_candidates.items():
        ranked=sorted(cands.values(),key=lambda c:-c['hero_score'])
        wow=ranked[:WOW_N]; featured=ranked[:FEAT_N]
        for c in featured: canonical_keys.add(frozenset((c['from_node_id'],c['to_node_id'])))
        def stamp(lst): return [{**c,'rank':i+1} for i,c in enumerate(lst)]
        gkey=f"{rcl}::{cid}"
        out_cities[gkey]={
            'group_key':gkey,'city_id':cid,'city_label':city_label.get(cid) or prettify_city(cid),
            'cluster_id':rcl,'cluster_label':cluster_label.get(rcl),
            'n_clean_candidates':len(cands),
            'marquee_wow':stamp(wow),'marquee_featured':stamp(featured)}

    retire=[]
    for e in current_entries:
        if e['schema']=='string':
            retire.append({**e,'reason':'free_text_string_no_id'}); continue
        key=frozenset((e.get('from_node_id'),e.get('to_node_id'))) if e.get('from_node_id') and e.get('to_node_id') else None
        if key is None: retire.append({**e,'reason':'no_bp_ids'})
        elif key not in canonical_keys: retire.append({**e,'reason':'not_in_canonical_city_set'})

    od=a.out_dir; os.makedirs(od,exist_ok=True)
    out={'_meta':{'generated':a.date,'version':'2.3','granularity':'cluster::city','wow_max':WOW_N,'featured_max':FEAT_N,
          'source':f'{a.source} ({"sealed slim manifests" if a.source=="manifests" else "data-clean/ROUTES.json"})',
          'route_id_field':'manifest route_id / properties.id (sealed) — bound directly, no re-stamp',
          'routes_seen':n_seen,'routes_clean_eligible':n_clean,
          'n_groups':len(out_cities),'ranking':'hero (water-beats-road): distance sweet-spot + island + cross-city; traffic/crowd = tiebreaker',
          'quality_gate':'in-range 3-30nm firm floor, on-water, junk-endpoint filter, no trivial <3nm hops',
          'river_exception':f'river cities {sorted(RIVER_CITIES)} allowed down to {RIVER_FLOOR}nm with river score (traffic+icon)',
          'label_scrub':f'{len(_scrub_applied)} aggregate labels trimmed; {len(_scrub_sourcing)} flagged needs_bp_sourcing'},
         'cities':out_cities}
    json.dump(out,open(os.path.join(od,'CANONICAL-MARQUEES.json'),'w'),indent=2)
    json.dump({'generated':a.date,'total_current_entries':len(current_entries),
          'retired_count':len(retire),'retired':retire},
          open(os.path.join(od,'MARQUEE-RETIRE-LIST.json'),'w'),indent=2)
    json.dump({'generated':a.date,
          'note':'Display-label scrub for aggregate region endpoints. applied = safe trim to primary place name (fix source BP label in data-clean/ROUTES). needs_bp_sourcing = aggregate territory used as endpoint; DO NOT invent a pier (null beats wrong) — source a real specific pier.',
          'applied':[{'node_id':k,**v} for k,v in sorted(_scrub_applied.items())],
          'needs_bp_sourcing':[{'node_id':k,**v} for k,v in sorted(_scrub_sourcing.items())]},
          open(os.path.join(od,'LABEL-SCRUB.json'),'w'),indent=2)
    json.dump({'generated':a.date,
          'note':'BP endpoints matching business-POI / non-pier patterns, excluded from marquees. Mis-geocoded locale entries (Grok / #119 locale-cleanup lane), NOT marquee-curation bugs. Fix or drop the source BP; do not invent a pier.',
          'count':len(_junk_suspects),
          'suspects':[{'node_id':k,'label':v} for k,v in sorted(_junk_suspects.items())]},
          open(os.path.join(od,'SUSPECT-ENDPOINTS.json'),'w'),indent=2)

    print(f"source={a.source}  routes_seen={n_seen}  clean_eligible={n_clean}")
    print(f"groups (cluster::city): {len(out_cities)}")
    print(f"label scrub: {len(_scrub_applied)} trimmed, {len(_scrub_sourcing)} need sourcing | suspects: {len(_junk_suspects)}")
    if current_entries:
        sc=collections.Counter(e['reason'] for e in retire)
        print(f"retire: {len(retire)}/{len(current_entries)} ", dict(sc))
    by_cluster=collections.Counter(c['cluster_id'] for c in out_cities.values())
    print("clusters covered:", len(by_cluster))

if __name__=='__main__':
    main()
