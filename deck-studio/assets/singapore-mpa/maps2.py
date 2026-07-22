#!/usr/bin/env python3
"""Singapore dark map plates v2 — text-free (titles/legends live in Slides), coast-follow routing, no land crossings."""
import json, math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path as MPath

gj = json.load(open('sgp.geojson'))
BG = '#0E1319'; LAND = '#1B242F'; COAST = '#2E3B4A'
GOLD = '#C59D5F'; LGOLD = '#E0CB8F'; WHITE = '#F3F3F3'; DIM = '#8A97A5'; GREEN = '#7FD1AE'

RINGS = []
for f in gj['features']:
    g = f['geometry']; polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
    for poly in polys:
        RINGS.append(poly[0])
LANDP = [MPath([(p[0], p[1]) for p in r]) for r in RINGS]
MAIN = max(RINGS, key=len)
N = len(MAIN)

def on_land(pt):
    return any(p.contains_point(pt) for p in LANDP)

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
BUKOM_ROUTE = [(103.766,1.284),(103.7595,1.266),(103.764,1.246),(103.772,1.229)]
def draw_bukom(ax, color, lw, style='-', alpha=1.0):
    pts = BUKOM_ROUTE
    dense=[pts[0]]
    import math as _m
    for p,q in zip(pts,pts[1:]):
        d=_m.hypot(q[0]-p[0],q[1]-p[1]); n=max(1,int(d/0.006))
        for t in range(1,n+1): dense.append((p[0]+(q[0]-p[0])*t/n,p[1]+(q[1]-p[1])*t/n))
    pts=dense
    for _ in range(3):
        out=[pts[0]]
        for p,q in zip(pts,pts[1:]):
            out.append((0.75*p[0]+0.25*q[0],0.75*p[1]+0.25*q[1]))
            out.append((0.25*p[0]+0.75*q[0],0.25*p[1]+0.75*q[1]))
        out.append(pts[-1]); pts=out
    ax.plot([p[0] for p in pts],[p[1] for p in pts], color=color, lw=lw, linestyle=style, alpha=alpha, zorder=5, solid_capstyle='round')
DISP = {
 'marina-east-bedok': (103.9166, 1.2995),   # ON the coast (ring vertex 258, nudged a hair seaward for dot ring)
 'marina-bay-stops': (103.858, 1.283),
 'keppel-harbourfront': (103.820, 1.258),
 'west-coast-pier': (103.766, 1.284),
 'jurong-island-banyan': (103.699, 1.251),
 'sentosa-cove-marina': (103.843, 1.239),
}
def P(k): return DISP.get(k, BP[k][:2])
LBL = {
 'kusu-island': (8, -4), 'st-johns-lazarus': (-6, -13), 'marina-south-pier': (7, 2),
 'marina-bay-stops': (-30, 12), 'keppel-harbourfront': (-24, -14), 'sentosa-cove-marina': (-72, -6),
 'west-coast-pier': (-90, -3), 'jurong-island-banyan': (-8, -14), 'marina-east-bedok': (8, -3),
 'changi-point': (7, -4), 'pulau-ubin': (2, 7),
}
TODAY = [
 ('marina-south-pier', 'st-johns-lazarus'), ('marina-south-pier', 'kusu-island'),
 ('changi-point', 'pulau-ubin'), ('sentosa-cove-marina', 'st-johns-lazarus'),
]
CAND = [  # candidate links (gold)
 ('marina-east-bedok','marina-bay-stops'), ('marina-bay-stops','keppel-harbourfront'),
 ('marina-south-pier','st-johns-lazarus'), ('marina-south-pier','kusu-island'),
 ('sentosa-cove-marina','st-johns-lazarus'), ('changi-point','pulau-ubin'),
 ('west-coast-pier','keppel-harbourfront'), ('jurong-island-banyan','keppel-harbourfront'),
]
CENTROID = (103.82, 1.36)

def ring_idx(pt):
    return min(range(N), key=lambda i: math.hypot(MAIN[i][0]-pt[0], MAIN[i][1]-pt[1]))

def seaward(i, off):
    x, y = MAIN[i]
    a, b = MAIN[(i-1) % N], MAIN[(i+1) % N]
    tx, ty = b[0]-a[0], b[1]-a[1]
    n = math.hypot(tx, ty) or 1e-9
    for o in (off, off*1.6, off*0.6):
        for s in (1, -1):
            px, py = x + s*ty/n*o, y - s*tx/n*o
            if not on_land((px, py)):
                return (px, py)
    return None

def coast_follow(a_pt, b_pt, off=0.009):
    """Polyline from a to b hugging the coast seaward, no land crossing."""
    ia, ib = ring_idx(a_pt), ring_idx(b_pt)
    # choose direction with fewer steps
    fwd = (ib - ia) % N; bwd = (ia - ib) % N
    idxs = [ (ia + k) % N for k in range(1, fwd) ] if fwd <= bwd else [ (ia - k) % N for k in range(1, bwd) ]
    pts = [a_pt]
    for i in idxs:
        p = seaward(i, off)
        if p: pts.append(p)
    pts.append(b_pt)
    # taut string-pull: greedy shortcut through open water
    def clear_seg(p, q):
        d = math.hypot(q[0]-p[0], q[1]-p[1])
        n = max(3, int(d/0.0015))
        return all(not on_land((p[0]+(q[0]-p[0])*t/n, p[1]+(q[1]-p[1])*t/n)) for t in range(1, n))
    taut = [pts[0]]; i = 0
    while i < len(pts)-1:
        j = len(pts)-1
        while j > i+1 and not clear_seg(pts[i], pts[j]): j -= 1
        taut.append(pts[j]); i = j
    pts = taut
    # re-densify so smoothing keeps gentle curves
    dense = [pts[0]]
    for p, q in zip(pts, pts[1:]):
        d = math.hypot(q[0]-p[0], q[1]-p[1]); n = max(1, int(d/0.01))
        for t in range(1, n+1): dense.append((p[0]+(q[0]-p[0])*t/n, p[1]+(q[1]-p[1])*t/n))
    pts = dense
    # chaikin smooth x2
    for _ in range(3):
        out = [pts[0]]
        for p, q in zip(pts, pts[1:]):
            out.append((0.75*p[0]+0.25*q[0], 0.75*p[1]+0.25*q[1]))
            out.append((0.25*p[0]+0.75*q[0], 0.25*p[1]+0.75*q[1]))
        out.append(pts[-1]); pts = out
    return pts

HAND = {
 ('west-coast-pier','keppel-harbourfront'): [(103.760,1.268),(103.783,1.251),(103.812,1.250)],
 ('keppel-harbourfront','marina-bay-stops'): [(103.826,1.240),(103.845,1.232),(103.862,1.256),(103.8625,1.264)],
 ('marina-bay-stops','marina-east-bedok'): [(103.8625,1.264),(103.878,1.272)],
 ('jurong-island-banyan','keppel-harbourfront'): [(103.727,1.242),(103.752,1.244),(103.790,1.245),(103.810,1.249)],
}
def hand_key(ka, kb):
    if (ka, kb) in HAND: return HAND[(ka, kb)]
    if (kb, ka) in HAND: return list(reversed(HAND[(kb, ka)]))
    return None

def seg_clear(p, q):
    d = math.hypot(q[0]-p[0], q[1]-p[1]); n = max(3, int(d/0.0015))
    return all(not on_land((p[0]+(q[0]-p[0])*t/n, p[1]+(q[1]-p[1])*t/n)) for t in range(1, n))

def smooth_dense(pts):
    dense = [pts[0]]
    for p, q in zip(pts, pts[1:]):
        d = math.hypot(q[0]-p[0], q[1]-p[1]); n = max(1, int(d/0.01))
        for t in range(1, n+1): dense.append((p[0]+(q[0]-p[0])*t/n, p[1]+(q[1]-p[1])*t/n))
    pts = dense
    for _ in range(3):
        out = [pts[0]]
        for p, q in zip(pts, pts[1:]):
            out.append((0.75*p[0]+0.25*q[0], 0.75*p[1]+0.25*q[1]))
            out.append((0.25*p[0]+0.75*q[0], 0.25*p[1]+0.75*q[1]))
        out.append(pts[-1]); pts = out
    return pts

def route_pts(ka, kb, off=0.009):
    h = hand_key(ka, kb)
    if h:
        A, B = P(ka), P(kb)
        TOL = 0.02
        def ok(p):
            if not on_land(p): return True
            return math.hypot(p[0]-A[0], p[1]-A[1]) < TOL or math.hypot(p[0]-B[0], p[1]-B[1]) < TOL
        pts = [A] + h + [B]
        sm = smooth_dense(pts)
        samples = []
        for p, q in zip(pts, pts[1:]):
            d = math.hypot(q[0]-p[0], q[1]-p[1]); n = max(3, int(d/0.0015))
            samples += [(p[0]+(q[0]-p[0])*t/n, p[1]+(q[1]-p[1])*t/n) for t in range(1, n)]
        if all(ok(p) for p in samples) and all(ok(p) for p in sm[::5]):
            return sm
        print('WARN hand route fails water check:', ka, kb, '- falling back')
    return coast_follow(P(ka), P(kb), off)

def path_km(pts):
    km = 0.0
    for p, q in zip(pts, pts[1:]):
        km += math.hypot((q[0]-p[0])*111.32*math.cos(math.radians(1.3)), (q[1]-p[1])*110.57)
    return km

def arc_pts(a, b, k=0.16):
    x1, y1 = a; x2, y2 = b
    mx, my = (x1+x2)/2, (y1+y2)/2
    dx, dy = x2-x1, y2-y1
    n = math.hypot(dx, dy) or 1e-9
    off = k * n
    px, py = -dy/n*off, dx/n*off
    vx, vy = mx - CENTROID[0], my - CENTROID[1]
    if px*vx + py*vy < 0: px, py = -px, -py
    return [(x1,y1), (mx+px, my+py), (x2,y2)]

def bezier_clear(ctrl, samples=60):
    (x1,y1),(cx,cy),(x2,y2) = ctrl
    for t in [i/samples for i in range(1, samples)]:
        bx = (1-t)**2*x1 + 2*(1-t)*t*cx + t**2*x2
        by = (1-t)**2*y1 + 2*(1-t)*t*cy + t**2*y2
        if on_land((bx, by)): return False
    return True

def arc(ax, a, b, color, lw, style='-', alpha=1.0, z=5, k=0.16):
    ctrl = None
    for kk in (k, k*1.6, k*2.4, -k, -k*1.6):
        c = arc_pts(a, b, abs(kk))
        if kk < 0:  # flip bow
            mx, my = (a[0]+b[0])/2, (a[1]+b[1])/2
            c = [c[0], (2*mx - c[1][0], 2*my - c[1][1]), c[2]]
        if bezier_clear(c): ctrl = c; break
    if ctrl is None:
        pts = coast_follow(a, b)
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color=color, lw=lw, linestyle=style, alpha=alpha, zorder=z, solid_capstyle='round')
        return
    path = MPath(ctrl, [MPath.MOVETO, MPath.CURVE3, MPath.CURVE3])
    ax.add_patch(PathPatch(path, fill=False, edgecolor=color, lw=lw, linestyle=style, alpha=alpha, zorder=z, capstyle='round'))

def follow(ax, a, b, color, lw, style='-', alpha=1.0, z=6, off=0.009):
    pts = coast_follow(a, b, off)
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=color, lw=lw, linestyle=style, alpha=alpha, zorder=z, solid_capstyle='round')
    return pts

def dots(ax, keys, label=True, size=26, fs=7.5, extra=None):
    items = [(P(k)[0], P(k)[1], BP[k][2], LBL.get(k, (4,5))) for k in keys]
    if extra: items += [(x, y, nm, (-14, -13)) for x, y, nm in extra]
    for x, y, name, (ox, oy) in items:
        ax.scatter([x],[y], s=size, color=WHITE, edgecolor=GOLD, linewidth=1.1, zorder=8)
        if label:
            ax.annotate(name, (x,y), xytext=(ox,oy), textcoords='offset points', color=WHITE, fontsize=fs, zorder=9)

def base(figw, figh, bounds):
    fig, ax = plt.subplots(figsize=(figw, figh), dpi=200)
    fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    for r in RINGS:
        xs=[p[0] for p in r]; ys=[p[1] for p in r]
        ax.fill(xs, ys, color=LAND, zorder=1); ax.plot(xs, ys, color=COAST, lw=0.8, zorder=2)
    ax.set_xlim(bounds[0], bounds[1]); ax.set_ylim(bounds[2], bounds[3])
    ax.set_aspect('equal'); ax.axis('off')
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    return fig, ax

B_MAIN = (103.62, 104.06, 1.15, 1.475)
B_SOUTH = (103.63, 104.055, 1.155, 1.455)

# ---- 1 · network today (text-free) ----
fig, ax = base(9.0, 5.05, B_MAIN)
for a, b in TODAY: arc(ax, P(a), P(b), LGOLD, 2.0)
draw_bukom(ax, GREEN, 2.2)
dots(ax, sorted({k for p in TODAY for k in p} | {'west-coast-pier'}), extra=[BUKOM], fs=8)
fig.savefig('sg-network-today-v2.png', facecolor=BG); plt.close(fig)

# ---- 2 · candidate links (text-free; dashed today visible; +Bukom, +Changi–East Coast) ----
fig, ax = base(9.6, 5.4, B_MAIN)
for a, b in TODAY: arc(ax, P(a), P(b), DIM, 1.6, style=(0,(4,3)), alpha=0.95, k=0.08)
draw_bukom(ax, GREEN, 1.6, style=(0,(4,3)), alpha=0.95)
for a, b in CAND:
    if hand_key(a, b):
        pts = route_pts(a, b)
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color=GOLD, lw=2.3, zorder=5, solid_capstyle='round')
    else:
        arc(ax, P(a), P(b), GOLD, 2.3, k=0.18)
ce = route_pts('changi-point', 'marina-east-bedok')
ax.plot([p[0] for p in ce], [p[1] for p in ce], color=GOLD, lw=2.3, zorder=5, solid_capstyle='round')
dots(ax, list(BP.keys()), fs=8, extra=[BUKOM])
fig.savefig('sg-candidate-links-v2.png', facecolor=BG); plt.close(fig)
print('changi-eastcoast km:', round(path_km(ce), 1))

# ---- 3 · coastal express (text-free full-bleed; coast-follow; East Coast on the coast) ----
fig, ax = base(9.6, 5.4, B_MAIN)
for a, b in TODAY: arc(ax, P(a), P(b), DIM, 1.0, style=(0,(3,3)), alpha=0.45)
draw_bukom(ax, DIM, 1.0, style=(0,(3,3)), alpha=0.45)
LINE = ['west-coast-pier', 'keppel-harbourfront', 'marina-bay-stops', 'marina-east-bedok', 'changi-point']
seg_km = []
for a, b in zip(LINE, LINE[1:]):
    pts = route_pts(a, b, off=0.0085)
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=GOLD, lw=3.2, zorder=6, solid_capstyle='round')
    seg_km.append((a, b, path_km(pts)))
for k in LINE:
    x, y = P(k)
    ax.scatter([x],[y], s=64, color=BG, edgecolor=GOLD, linewidth=2.2, zorder=8)
    ax.scatter([x],[y], s=10, color=WHITE, zorder=9)
CLBL = {'west-coast-pier': (-52, 12), 'keppel-harbourfront': (-30, -18), 'marina-bay-stops': (-58, 14),
        'marina-east-bedok': (10, 10), 'changi-point': (10, 0)}
for k in LINE:
    ax.annotate(BP[k][2], P(k), xytext=CLBL[k], textcoords='offset points', color=WHITE, fontsize=10.5, weight='bold', zorder=9)
fig.savefig('sg-coastal-express-v2.png', facecolor=BG); plt.close(fig)
for a, b, km in seg_km:
    mins20 = km/37.04*60
    print(f"{BP[a][2]} -> {BP[b][2]}: {km:.1f} km ~{mins20:.0f} min @20kn")

# ---- 4 · horizon tomorrow (text-free; FULL proposed network incl. coastal line) ----
fig, ax = base(7.4, 5.05, B_SOUTH)
for a, b in TODAY: arc(ax, P(a), P(b), DIM, 1.0, style=(0,(3,3)), alpha=0.5)
draw_bukom(ax, DIM, 1.0, style=(0,(3,3)), alpha=0.5)
for a, b in CAND:
    if hand_key(a, b):
        pts = route_pts(a, b)
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color=GOLD, lw=2.0, zorder=5, solid_capstyle='round')
    else:
        arc(ax, P(a), P(b), GOLD, 2.0, k=0.18)
for a, b in zip(LINE, LINE[1:]):
    pts = route_pts(a, b, off=0.0085)
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=GOLD, lw=2.6, zorder=6, solid_capstyle='round')
dots(ax, list(BP.keys()), label=False, size=20, extra=[(BUKOM[0], BUKOM[1], '')])
fig.savefig('sg-horizon-tomorrow-v2.png', facecolor=BG); plt.close(fig)

# ---- 5 · horizon today (text-free, unchanged look) ----
fig, ax = base(7.4, 5.05, B_SOUTH)
for a, b in TODAY: arc(ax, P(a), P(b), DIM, 1.8, alpha=0.9)
draw_bukom(ax, DIM, 1.8, alpha=0.9)
dots(ax, sorted({k for p in TODAY for k in p} | {'west-coast-pier'}), label=False, size=18, extra=[(BUKOM[0], BUKOM[1], '')])
fig.savefig('sg-horizon-today-v2.png', facecolor=BG); plt.close(fig)
print('done')
