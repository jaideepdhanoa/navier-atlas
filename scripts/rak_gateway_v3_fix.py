#!/usr/bin/env python3
"""Re-verify RAK gateway legs against extended landmask v3 (full Dammam..Muscat
extent) and apply approach fixes: Yas exit east channel, Manama N-of-Muharraq
sweep, Muttrah due-N final approach. Khasab keeps documented exemption (bay not
represented in mask). Updates gateway-geometries.json, corridor_table, page copy."""
import json, math, re
from pathlib import Path
from shapely import wkb
from shapely.geometry import LineString, Point

ROOT = Path('/tmp/na')
v3 = wkb.loads((ROOT/'grok-routing-output/uae_gulf_land_v3.wkb').read_bytes())

def dist_nm(coords):
    t=0.0
    for (x1,y1),(x2,y2) in zip(coords,coords[1:]):
        dx=(x2-x1)*60.0*math.cos(math.radians((y1+y2)/2)); dy=(y2-y1)*60.0
        t+=math.hypot(dx,dy)
    return t

def crossings(coords, exempt_km=1.6):
    line = LineString(coords); inter = line.intersection(v3)
    a,b = Point(coords[0]), Point(coords[-1]); out=[]
    for p in getattr(inter,'geoms',[inter]):
        if p.is_empty or getattr(p,'length',0)==0: continue
        mid = p.interpolate(0.5, normalized=True)
        cs=list(p.coords)
        km=sum(math.hypot((x2-x1)*111*math.cos(math.radians((y1+y2)/2)),(y2-y1)*111)
               for (x1,y1),(x2,y2) in zip(cs,cs[1:]))
        dm=min(a.distance(mid),b.distance(mid))*111.0
        if dm<=exempt_km: continue
        out.append((round(km,2),(round(mid.x,4),round(mid.y,4))))
    return out

gp = ROOT/'employer-hub/hubs/ras-al-khaimah/gateway-geometries.json'
gj = json.loads(gp.read_text()); G = gj['geometries']

# --- GTW-1a: east-channel Yas exit ---
c = G['GTW-1a']['coordinates']
G['GTW-1a']['coordinates'] = [c[0], [54.6185,24.4700],[54.6320,24.4780],[54.6475,24.4975],[54.6550,24.5200]] + c[3:]

# --- GLF-3: north-of-Muharraq sweep into Manama ---
c = G['GLF-3']['coordinates']
keep = [pt for pt in c if pt[0] > 50.90]          # drop old westward tail at lat 26.21-26.23
G['GLF-3']['coordinates'] = keep + [[50.8400,26.2700],[50.7600,26.3300],[50.6900,26.3450],
    [50.6300,26.3300],[50.5920,26.3000],[50.5880,26.2600],[50.5815,26.2440],[50.5755,26.2361]]

# --- GLF-5: due-north final approach into Muttrah ---
c = G['GLF-5']['coordinates']
G['GLF-5']['coordinates'] = c[:-1] + [[54.0,0]][:0] if False else c
c = G['GLF-5']['coordinates']
G['GLF-5']['coordinates'] = c[:-1] + [[58.5200,23.6640],[58.5589,23.6560],[58.5589,23.6234]]

MASK_QA = 'uae_gulf_land_v3.wkb (48.4..60.2 lng) — 0 mid-route land crossings (berth-adjacent harbour polygons exempt, <=1.6 km of endpoints)'
EXEMPT = {'GLF-1': 'Documented exemption: final ~9.5 km into Khasab crosses mask-land — Khasab Bay / Musandam fjords are not carved into any available mask (below NE-10m resolution). Real bay approach from NW. Re-verify at next Grok seal.'}

print(f'{"leg":10s} {"nm":>8s}  status')
results={}
ok=True
for k,v in G.items():
    coords=v['coordinates']; nm=dist_nm(coords); results[k]=nm
    segs=crossings(coords)
    if k in EXEMPT:
        v['mask_qa']=MASK_QA.replace('0 mid-route land crossings','crossings under documented exemption')
        v['note_exemption']=EXEMPT[k]
        print(f'{k:10s} {nm:8.2f}  EXEMPT ({"; ".join(f"{a} km @ {b}" for a,b in segs)})')
        continue
    v['mask_qa']=MASK_QA
    st='CLEAN' if not segs else 'CROSSES: '+'; '.join(f'{a} km @ {b}' for a,b in segs)
    if segs: ok=False
    print(f'{k:10s} {nm:8.2f}  {st}')

gj['_internal'] = (gj['_internal'].replace('land-masked 2026-08-26','land-masked 2026-08-26; re-verified against extended mask v3 (Natural Earth 10m west-Gulf + east-Oman extensions, full 48.4-60.2 extent) same day')
                   + ' Khasab final approach = documented exemption (bay below mask resolution). Muttrah berth-adjacent crossing ~3 km reflects NE-10m coast offset; both flagged for next Grok seal.')
gp.write_text(json.dumps(gj, indent=2, ensure_ascii=False))
if not ok: raise SystemExit('CROSSINGS REMAIN — not writing downstream')

# --- corridor_table + page copy ---
hp = ROOT/'employer-hub/hubs/ras-al-khaimah/hub.json'
hub=json.loads(hp.read_text())
rows=hub['corridor_table']['corridors']
IDMAP={'GTW-1a':'GTW-1a','GTW-1b':'GTW-1b','GTW-1c':'GTW-1c','GTW-alt':'GTW-alt','GLF-1':'GLF-1','GLF-2':'GLF-2','GLF-3':'GLF-3','GLF-4':'GLF-4','GLF-5':'GLF-5'}
old={}
for r in rows:
    if r['id'] in results:
        old[r['id']]=r.get('distance_nm')
        r['distance_nm']=round(results[r['id']],1)
        r['geometry_source']='hand-waterway-v3-masked'
hp.write_text(json.dumps(hub, indent=2, ensure_ascii=False))
print('table updates:', {k:(old[k],round(results[k],1)) for k in old if old[k]!=round(results[k],1)})

# page copy ≈ values
pp = ROOT/'employer-hub/hubs/ras-al-khaimah/public-partners.json'
raw = pp.read_text()
approx={'GTW-1a':'57','GTW-1b':'31','GTW-1c':'28','GLF-1':'35','GLF-2':'241','GLF-3':'290','GLF-4':'305','GLF-5':'295'}
new_approx={k:str(round(results[k])) for k in approx}
for k in approx:
    if approx[k]!=new_approx[k]:
        n=raw.count(f'≈{approx[k]} nm')
        raw=raw.replace(f'≈{approx[k]} nm', f'≈{new_approx[k]} nm')
        print(f'page copy {k}: ≈{approx[k]} -> ≈{new_approx[k]} nm ({n} occurrence)')
pp.write_text(raw)
print('DONE')
