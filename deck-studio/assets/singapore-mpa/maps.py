#!/usr/bin/env python3
"""Singapore dark map plates — dossier-grounded, schematic/illustrative."""
import json, urllib.request, math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path as MPath

URL = 'https://github.com/wmgeolab/geoBoundaries/raw/9469f09/releaseData/gbOpen/SGP/ADM0/geoBoundaries-SGP-ADM0_simplified.geojson'
try:
    gj = json.load(open('sgp.geojson'))
except Exception:
    urllib.request.urlretrieve(URL, 'sgp.geojson')
    gj = json.load(open('sgp.geojson'))

BG = '#0E1319'; LAND = '#1B242F'; COAST = '#2E3B4A'
GOLD = '#C59D5F'; LGOLD = '#E0CB8F'; WHITE = '#F3F3F3'; DIM = '#8A97A5'

BP = {
 'marina-bay-stops': (103.857, 1.288, 'Marina Bay / CBD'),
 'marina-south-pier': (103.863, 1.271, 'Marina South Pier'),
 'marina-east-bedok': (103.912, 1.301, 'East Coast'),
 'sentosa-cove-marina': (103.839, 1.244, 'Sentosa Cove'),
 'keppel-harbourfront': (103.820, 1.265, 'Keppel / HarbourFront'),
 'st-johns-lazarus': (103.848, 1.218, "St John's / Lazarus"),
 'kusu-island': (103.860, 1.225, 'Kusu'),
 'changi-point': (103.992, 1.390, 'Changi Point'),
 'pulau-ubin': (103.964, 1.410, 'Pulau Ubin'),
 'west-coast-pier': (103.770, 1.290, 'West Coast Pier'),
 'jurong-island-banyan': (103.700, 1.265, 'Jurong Island'),
}
BUKOM = (103.772, 1.229, 'Pulau Bukom')

# display-only offshore nudges (schematic clarity; anchors stay in dossier)
DISP = {
 'marina-east-bedok': (103.912, 1.292),
 'marina-bay-stops': (103.858, 1.283),
 'keppel-harbourfront': (103.820, 1.258),
 'west-coast-pier': (103.766, 1.284),
 'jurong-island-banyan': (103.700, 1.258),
 'sentosa-cove-marina': (103.843, 1.239),
}
def P(k):
    return DISP.get(k, BP[k][:2])
LBL = {  # (dx, dy) points
 'kusu-island': (8, -4),
 'st-johns-lazarus': (-6, -13),
 'marina-south-pier': (7, 2),
 'marina-bay-stops': (-4, 8),
 'keppel-harbourfront': (-24, 12),
 'sentosa-cove-marina': (-72, -6),
 'west-coast-pier': (-14, 8),
 'jurong-island-banyan': (-8, -14),
 'marina-east-bedok': (4, 6),
 'changi-point': (5, -10),
 'pulau-ubin': (2, 7),
}

TODAY = [  # sourced existing services
 ('marina-south-pier', 'st-johns-lazarus'),
 ('marina-south-pier', 'kusu-island'),
 ('changi-point', 'pulau-ubin'),
 ('sentosa-cove-marina', 'st-johns-lazarus'),
]
PAIRS = [
 ('marina-east-bedok','marina-bay-stops'), ('marina-bay-stops','keppel-harbourfront'),
 ('marina-south-pier','st-johns-lazarus'), ('marina-south-pier','kusu-island'),
 ('sentosa-cove-marina','st-johns-lazarus'), ('changi-point','pulau-ubin'),
 ('west-coast-pier','keppel-harbourfront'), ('jurong-island-banyan','keppel-harbourfront'),
]

def draw_land(ax):
    for feat in gj['features']:
        geom = feat['geometry']
        polys = geom['coordinates'] if geom['type'] == 'MultiPolygon' else [geom['coordinates']]
        for poly in polys:
            for i, ring in enumerate(poly):
                xs = [p[0] for p in ring]; ys = [p[1] for p in ring]
                ax.fill(xs, ys, color=LAND, zorder=1)
                ax.plot(xs, ys, color=COAST, lw=0.8, zorder=2)

CENTROID = (103.82, 1.36)
def arc(ax, a, b, color, lw, style='-', alpha=1.0, z=5):
    x1, y1 = a; x2, y2 = b
    mx, my = (x1+x2)/2, (y1+y2)/2
    dx, dy = x2-x1, y2-y1
    n = math.hypot(dx, dy) or 1e-9
    off = 0.16 * n
    px, py = -dy/n*off, dx/n*off
    # bow away from the mainland centroid (into open water)
    vx, vy = mx - CENTROID[0], my - CENTROID[1]
    if px*vx + py*vy < 0: px, py = -px, -py
    path = MPath([(x1,y1), (mx+px, my+py), (x2,y2)], [MPath.MOVETO, MPath.CURVE3, MPath.CURVE3])
    ax.add_patch(PathPatch(path, fill=False, edgecolor=color, lw=lw, linestyle=style, alpha=alpha, zorder=z, capstyle='round'))

def dots(ax, keys, label=True, size=26, fs=7.5, extra=None):
    items = [(P(k)[0], P(k)[1], BP[k][2], LBL.get(k, (4,5))) for k in keys]
    if extra: items += [(x, y, nm, (5,-10)) for x, y, nm in extra]
    for x, y, name, (ox, oy) in items:
        ax.scatter([x],[y], s=size, color=WHITE, edgecolor=GOLD, linewidth=1.1, zorder=8)
        if label:
            ax.annotate(name, (x,y), xytext=(ox,oy), textcoords='offset points', color=WHITE, fontsize=fs, zorder=9)

def base(figw, figh, bounds):
    fig, ax = plt.subplots(figsize=(figw, figh), dpi=200)
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    draw_land(ax)
    ax.set_xlim(bounds[0], bounds[1]); ax.set_ylim(bounds[2], bounds[3])
    ax.set_aspect('equal'); ax.axis('off')
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    return fig, ax

B_MAIN = (103.62, 104.06, 1.15, 1.475)
B_SOUTH = (103.66, 104.03, 1.17, 1.46)

# 1 · S10 network today (600x337 slot)
fig, ax = base(9.0, 5.05, B_MAIN)
for a, b in TODAY:
    arc(ax, P(a), P(b), LGOLD, 2.0)
arc(ax, P('west-coast-pier'), BUKOM[:2], '#7FD1AE', 2.2)  # electric ferry, green accent
used = sorted({k for p in TODAY for k in p} | {'west-coast-pier'})
dots(ax, used, extra=[BUKOM], fs=8)
ax.text(0.015, 0.97, 'WATER TRANSPORT TODAY', transform=ax.transAxes, color=LGOLD, fontsize=10, weight='bold', va='top')
ax.text(0.015, 0.925, 'Ferries & bumboats · green line = electric ferry already daily', transform=ax.transAxes, color=DIM, fontsize=7.5, va='top')
ax.text(0.985, 0.02, 'Illustrative — approximate anchors', transform=ax.transAxes, color=DIM, fontsize=6.5, ha='right')
fig.savefig('sg-network-today.png', facecolor=BG); plt.close(fig)

# 2 · S11 candidate links (full-bleed 16:9)
fig, ax = base(9.6, 5.4, B_MAIN)
for a, b in TODAY:
    arc(ax, P(a), P(b), DIM, 1.2, style=(0,(4,3)), alpha=0.75)
for a, b in PAIRS:
    arc(ax, P(a), P(b), GOLD, 2.3)
dots(ax, list(BP.keys()), fs=8)
ax.text(0.015, 0.975, 'CANDIDATE LINKS TO STUDY TOGETHER', transform=ax.transAxes, color=LGOLD, fontsize=11, weight='bold', va='top')
ax.text(0.015, 0.935, 'Gold = candidate links · dashed = services running today', transform=ax.transAxes, color=DIM, fontsize=8, va='top')
ax.text(0.985, 0.02, 'Illustrative — pending joint study with MPA', transform=ax.transAxes, color=DIM, fontsize=7, ha='right')
fig.savefig('sg-candidate-links.png', facecolor=BG); plt.close(fig)

# 3 · S17 horizon today (square)
fig, ax = base(6.0, 6.0, B_SOUTH)
for a, b in TODAY:
    arc(ax, P(a), P(b), DIM, 1.8, alpha=0.9)
arc(ax, P('west-coast-pier'), BUKOM[:2], DIM, 1.8, alpha=0.9)
dots(ax, sorted({k for p in TODAY for k in p} | {'west-coast-pier'}), label=False, size=18, extra=[BUKOM])
fig.savefig('sg-horizon-today.png', facecolor=BG); plt.close(fig)

# 4 · S17 horizon tomorrow (square)
fig, ax = base(6.0, 6.0, B_SOUTH)
for a, b in TODAY:
    arc(ax, P(a), P(b), DIM, 1.0, style=(0,(3,3)), alpha=0.5)
for a, b in PAIRS:
    arc(ax, P(a), P(b), GOLD, 2.2)
dots(ax, list(BP.keys()), label=False, size=20)
fig.savefig('sg-horizon-tomorrow.png', facecolor=BG); plt.close(fig)
print('maps done')
