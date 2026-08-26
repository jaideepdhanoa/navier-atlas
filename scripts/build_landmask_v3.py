#!/usr/bin/env python3
"""Extend uae_gulf_land_v2.wkb with Natural Earth 10m coastline for the
western Gulf (KSA/Bahrain/Qatar west) and eastern Oman (Muscat), producing
uae_gulf_land_v3.wkb. v2 kept untouched. Then verify every RAK gateway leg
(GTW + GLF) end-to-end against v3."""
import json, math
from pathlib import Path
import shapefile
from shapely import wkb
from shapely.geometry import LineString, Point, Polygon, MultiPolygon, box, shape
from shapely.ops import unary_union

ROOT = Path('/tmp/na')
OUT = ROOT / 'grok-routing-output'
v2 = wkb.loads((OUT / 'uae_gulf_land_v2.wkb').read_bytes())
print('v2 bounds:', [round(x,2) for x in v2.bounds])

WEST = box(48.4, 23.4, 51.05, 28.3)   # KSA coast, Bahrain, Qatar west
EAST = box(57.45, 22.4, 60.2, 27.3)   # Oman east coast to Muscat+

polys = []
for shp in ('ne_10m_land', 'ne_10m_minor_islands'):
    r = shapefile.Reader(f'/tmp/ne/{shp}/{shp}.shp')
    for sr in r.iterShapeRecords(bbox=(48.4, 22.4, 60.2, 28.3)):
        g = shape(sr.shape.__geo_interface__)
        if not g.is_valid:
            g = g.buffer(0)
        for B in (WEST, EAST):
            c = g.intersection(B)
            if not c.is_empty:
                polys.append(c)
print('NE clipped pieces:', len(polys))
v3 = unary_union([v2] + polys)
(OUT / 'uae_gulf_land_v3.wkb').write_bytes(wkb.dumps(v3))
print('v3 bounds:', [round(x,2) for x in v3.bounds])

# ---- verify all gateway legs against v3 ----
gj = json.loads((ROOT / 'employer-hub/hubs/ras-al-khaimah/gateway-geometries.json').read_text())
geoms = gj['geometries'] if 'geometries' in gj else gj

def crossings(coords):
    line = LineString(coords)
    inter = line.intersection(v3)
    segs = []
    if inter.is_empty:
        return segs
    parts = getattr(inter, 'geoms', [inter])
    a, b = Point(coords[0]), Point(coords[-1])
    for p in parts:
        if p.is_empty or p.length == 0:
            continue
        mid = p.interpolate(0.5, normalized=True)
        # endpoint exemption: harbour polygons within 1.6 km of endpoints
        dm = min(a.distance(mid), b.distance(mid)) * 111.0
        km = p.length * 111.0 * abs(math.cos(math.radians(mid.y)))**0.0  # approx; refine below
        # better length: use geodesic-ish scaling per segment midpoint lat
        km = 0.0
        cs = list(p.coords)
        for i in range(len(cs)-1):
            (x1,y1),(x2,y2) = cs[i], cs[i+1]
            dx = (x2-x1)*111.0*math.cos(math.radians((y1+y2)/2)); dy=(y2-y1)*111.0
            km += math.hypot(dx,dy)
        if dm <= 1.6:
            continue
        segs.append((round(km,2), (round(mid.x,4), round(mid.y,4))))
    return segs

def dist_nm(coords):
    t=0.0
    for i in range(len(coords)-1):
        (x1,y1),(x2,y2)=coords[i],coords[i+1]
        dx=(x2-x1)*60.0*math.cos(math.radians((y1+y2)/2)); dy=(y2-y1)*60.0
        t+=math.hypot(dx,dy)
    return round(t,2)

for key, val in geoms.items():
    coords = val['coordinates'] if isinstance(val, dict) and 'coordinates' in val else val
    if not isinstance(coords, list):
        continue
    segs = crossings(coords)
    status = 'CLEAN' if not segs else 'CROSSES: ' + '; '.join(f'{k} km @ {m}' for k, m in segs)
    print(f'{key:16s} {dist_nm(coords):8.2f} nm  {status}')
