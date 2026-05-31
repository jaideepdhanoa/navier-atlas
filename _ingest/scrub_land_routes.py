#!/usr/bin/env python3
"""Authoritative land-route scrubber. Loads ROUTES.json, drops any route whose interior
crosses > THRESH_KM of land (same test as qa_land_crossing.py), rewrites ROUTES.json, and
writes a dropped-routes review report. Makes the QA gate and the shipped data agree by
construction — defense-in-depth behind the generators' own fail-closed gates."""
import json, math, sys, collections
from global_land_mask import globe
THRESH_KM=1.0; END_BUF_NM=1.5; R_NM=3440.065
def hav(a,b):
    lo1,la1,lo2,la2=map(math.radians,[a[0],a[1],b[0],b[1]])
    h=math.sin((la2-la1)/2)**2+math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*R_NM*math.asin(min(1.0,math.sqrt(h)))
def interior_land_km(arc,buf=END_BUF_NM):
    n=len(arc)
    if n<3: return 0.0
    d=[0.0]*n
    for i in range(1,n): d[i]=d[i-1]+hav(arc[i-1],arc[i])
    tot=d[-1]; land=0.0
    for i in range(1,n-1):
        if d[i]<buf or (tot-d[i])<buf: continue
        if bool(globe.is_land(arc[i][1],arc[i][0])):
            land+=(hav(arc[i-1],arc[i])+hav(arc[i],arc[i+1]))/2.0
    return land*1.852
path=sys.argv[1] if len(sys.argv)>1 else "output-external/ROUTES.json"
routes=json.load(open(path))
kept=[]; dropped=[]; by_class=collections.Counter()
for f in routes:
    km=interior_land_km(f["geometry"]["coordinates"])
    if km>THRESH_KM:
        p=f.get("properties",{}); by_class[str(p.get("edge_class"))]+=1
        dropped.append({"km":round(km,1),"edge_class":p.get("edge_class"),"from":p.get("from"),"to":p.get("to"),"id":p.get("id")})
    else:
        kept.append(f)
json.dump(kept,open(path,"w"))
json.dump({"threshold_km":THRESH_KM,"dropped":len(dropped),"kept":len(kept),"by_class":dict(by_class),"routes":dropped},
          open("route-land-scrub-report.json","w"),indent=2)
print(f"Scrubbed: dropped {len(dropped)} land-crossing routes, kept {len(kept)}")
print("by class:",dict(by_class))
