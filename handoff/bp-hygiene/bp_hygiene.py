#!/usr/bin/env python3
"""Global BP-hygiene scanner. Reads sealed ROUTES.json, extracts every BP that
participates in a corridor, classifies dirty BPs into dispositions.
Never invents corrections beyond deterministic label trims. null/flag beats wrong."""
import json, math, re, collections

routes=json.load(open('ROUTES.json'))

def hav(a,b):
    R=6371.0
    la1,lo1=math.radians(a[1]),math.radians(a[0]); la2,lo2=math.radians(b[1]),math.radians(b[0])
    d=math.sin((la2-la1)/2)**2+math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*R*math.asin(min(1,math.sqrt(d)))

# ---- extract every BP endpoint ----
bps={}  # bp_id -> {label, city_id, coord, degree}
deg=collections.Counter()
for r in routes:
    p=r['properties']; g=r.get('geometry') or {}; co=g.get('coordinates') or []
    if len(co)<2: continue
    for end,cid_field,lab_field,coord in (('from','from_city_id','from_label',co[0]),
                                          ('to','to_city_id','to_label',co[-1])):
        bid=p.get(end)
        if not bid: continue
        deg[bid]+=1
        if bid not in bps:
            cid=p.get(cid_field) or (bid.split('__')[0] if '__' in bid else None)
            bps[bid]={'label':p.get(lab_field) or bid.split('__')[-1],'city_id':cid,'coord':coord}
for bid in bps: bps[bid]['degree']=deg[bid]
print(f"Unique BPs participating in corridors: {len(bps)}")

# ---- data-derived city centroids (median of member BP coords) ----
def median(xs): xs=sorted(xs); n=len(xs); return xs[n//2] if n%2 else (xs[n//2-1]+xs[n//2])/2
by_city=collections.defaultdict(list)
for bid,b in bps.items():
    if b['city_id']: by_city[b['city_id']].append(b['coord'])
centroid={c:[median([p[0] for p in v]),median([p[1] for p in v])] for c,v in by_city.items() if len(v)>=3}

# ---- classifiers ----
JUNK=re.compile(r'jet ?ski|water ?sport|wakeboard|parasail|flyboard|diving cent|dive cent|'
    r'mineral water|water co\b|medical|hospital|clinic|construction|harbour office|'
    r'boat ?yard|shipyard|craft yard|slipway|seaplane|sea plane|helipad|heli ?port|'
    r'\bllc\b|\bco\.? ?ltd|trading|marine service|repair|workshop|fuel station|petrol|'
    r'car park|parking|(?<!water )(?<!harbour )(?<!harbor )\bbus (stop|station|terminal)|railway|metro station',re.I)
AGG=re.compile(r'\s*[&+]\s*(the\s+)?(inner\s+|outer\s+|surrounding\s+)?[\w\s]*\bisl(and|es|as)\b|'
    r'\s*[&+]\s*(the\s+)?[\w\s]+\barchipelago\b',re.I)

register={'_meta':{'source':'data-clean/ROUTES.json (sealed main)','generated':'2026-07-06',
    'total_bps':len(bps),'method':'name-pattern + aggregate-label + city_id centroid-outlier + dup-coord',
    'principle':'null/flag beats wrong; Tasklet flags, Grok applies during reseal; no invented corrections'},
    'DROP_junk':[], 'RELABEL_aggregate':[], 'RETAG_city_mismatch':[], 'DUP_coord':[]}

# junk + aggregate
for bid,b in bps.items():
    lab=b['label'] or ''
    if JUNK.search(lab):
        register['DROP_junk'].append({'bp':bid,'label':lab,'city_id':b['city_id'],'degree':b['degree']})
    m=AGG.search(lab)
    if m:
        clean=re.split(r'\s*[&+]\s*',lab)[0].strip()
        register['RELABEL_aggregate'].append({'bp':bid,'orig':lab,'suggest':clean,'city_id':b['city_id']})

# city_id mismatch: BP far from its assigned centroid AND closer to another city's centroid
for bid,b in bps.items():
    cid=b['city_id']
    if not cid or cid not in centroid: continue
    d_own=hav(b['coord'],centroid[cid])
    if d_own<60: continue  # within 60km of assigned city → fine
    # find nearest centroid
    best=min(((c,hav(b['coord'],ce)) for c,ce in centroid.items() if c!=cid),key=lambda t:t[1],default=(None,9e9))
    if best[0] and best[1]<d_own*0.5 and best[1]<40:
        register['RETAG_city_mismatch'].append({'bp':bid,'label':b['label'],'assigned':cid,
            'km_from_assigned':round(d_own,1),'nearest':best[0],'km_from_nearest':round(best[1],1)})

# duplicate coords (rounded) with differing labels → geocode collision
coord_key=collections.defaultdict(list)
for bid,b in bps.items():
    coord_key[(round(b['coord'][0],4),round(b['coord'][1],4))].append(bid)
for k,v in coord_key.items():
    if len(v)>1:
        labs={bps[x]['label'] for x in v}
        if len(labs)>1:
            register['DUP_coord'].append({'coord':list(k),'bps':v,'labels':sorted(labs)})

for k in ('DROP_junk','RELABEL_aggregate','RETAG_city_mismatch','DUP_coord'):
    register['_meta'][f'n_{k}']=len(register[k])
    print(f"{k}: {len(register[k])}")

json.dump(register,open('BP-CLEANUP-REGISTER.json','w'),indent=2,ensure_ascii=True)
print("\n-- sample RETAG (worst offenders) --")
for x in sorted(register['RETAG_city_mismatch'],key=lambda r:-r['km_from_assigned'])[:12]:
    print(f"  {x['label'][:34]:34} {x['assigned'][:22]:22} {x['km_from_assigned']:6}km -> {x['nearest'][:22]:22} {x['km_from_nearest']}km")
print("-- sample JUNK --")
for x in register['DROP_junk'][:12]: print(f"  {x['label'][:50]:50} [{x['city_id']}] deg={x['degree']}")
