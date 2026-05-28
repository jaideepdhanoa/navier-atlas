#!/usr/bin/env python3
"""Build a single self-contained, premium-styled HTML for the Navier Atlas.

Features:
- Carto Voyager / dark raster basemap (no CSP sandbox)
- Cities (clustered) + Locales + POIs with semantic zoom
- Stories dropdown (6 partner narratives) with branded right-rail
- Search bar (cities/locales/POIs)
- Range rings (Pioneer II 70 nm + Quanta-LR 2,000 nm) toggle on selected node
- Sea-route polylines (Pioneer II solid mint, Quanta-LR dashed slate)
- URL state (#camera=lng,lat,z[&story=slug])
- Label overrides (manual map for cluster names that read oddly)
"""
import json, re, math
from pathlib import Path

HERE = Path(__file__).parent

def load(name):
    p = HERE / name
    return json.loads(p.read_text()) if p.exists() else None

nodes_raw  = load("nodes.json")
edges_raw  = load("edges.json")
orgs_raw   = load("orgs.json")
overrides  = load("label-overrides.json") or {}

STORY_FILES = ["grab","dubai-rta","abu-dhabi-itc","careem","red-sea-global","singapore-mpa"]
stories = []
for slug in STORY_FILES:
    s = load(f"{slug}.json")
    if s: stories.append(s)

def as_list(x, key="nodes"):
    if isinstance(x, dict) and key in x: return x[key]
    return x if isinstance(x, list) else []

node_list = as_list(nodes_raw, "nodes")
edge_list = as_list(edges_raw, "edges")

# ---------- Label shortening ----------
def short_label(name, ntype):
    if not name: return name
    s = re.sub(r"\s*\([^)]*\)", "", name).strip()
    if " — " in s:
        head, tail = s.split(" — ", 1)
        first = re.split(r"\s*[+/,]\s*", tail)[0].strip()
        return f"{head} — {first}" if first else head
    first = re.split(r"\s*[+,]\s*", s)[0].strip()
    return first or s

# ---------- Feature builder ----------
def coords_of(n):
    c = n.get("coords") or n.get("coord")
    if isinstance(c, list) and len(c) == 2 and c[0] is not None and c[1] is not None:
        return [c[0], c[1]]
    if isinstance(c, dict) and c.get("lng") is not None and c.get("lat") is not None:
        return [c["lng"], c["lat"]]
    return None

node_by_id = {}
for n in node_list:
    nid = n.get("id") or n.get("node_id")
    if nid: node_by_id[nid] = n

features = []
for n in node_list:
    c = coords_of(n)
    if not c: continue
    nid = n.get("id") or n.get("node_id") or ""
    ntype = n.get("type", "unknown")
    full = n.get("name","")
    label = overrides.get(nid) or short_label(full, ntype)
    props = {k:v for k,v in n.items() if k not in ("coords","coord")}
    props["shortName"] = label
    props["fullName"]  = full
    features.append({
        "type":"Feature",
        "geometry":{"type":"Point","coordinates":c},
        "properties":props,
    })

# ---------- Curated coastal boarding points (override locales+POIs for covered cities) ----------
BP_DIR = HERE / "boarding-points"
BP_CITY_MAP = {
    "dubai": "dubai-uae",
    "abu-dhabi": "abu-dhabi-uae",
    "singapore": "singapore",
    "bali": "bali-indonesia",
    "phuket": "phuket-phang-nga-thailand",
    "red-sea-global": "red-sea-global-ksa",
}
# City bbox (lng_min, lat_min, lng_max, lat_max) for removing stray POIs without parent_city_id
BP_BBOX = {
    "dubai-uae":                    (54.7,  24.5, 55.7,  25.6),
    "abu-dhabi-uae":                (51.5,  23.5, 55.5,  25.2),
    "singapore":                    (103.5, 1.10, 104.2, 1.55),
    "bali-indonesia":               (114.4, -9.7, 120.5, -7.8),
    "phuket-phang-nga-thailand":    (97.8,  6.8,  99.5,  9.5),
    "red-sea-global-ksa":           (35.0,  24.0, 39.8,  27.5),
}
covered_city_ids = set(BP_CITY_MAP.values())

# Drop existing locales+POIs inside covered cities
def in_covered_bbox(coord):
    if not coord: return None
    lng, lat = coord
    for cid, (x0,y0,x1,y1) in BP_BBOX.items():
        if x0<=lng<=x1 and y0<=lat<=y1: return cid
    return None

filtered = []
for f in features:
    p = f["properties"]
    t = p.get("type")
    if t == "locale" and p.get("parent_city_id") in covered_city_ids:
        continue
    if t == "poi":
        # POIs typically have no parent_city_id; suppress by bbox
        coord = f["geometry"]["coordinates"]
        if in_covered_bbox(coord) in covered_city_ids:
            continue
    filtered.append(f)
features = filtered

# Inject curated boarding points
BP_TYPE_LABELS = {
    "marina":"Marina","ferry_terminal":"Ferry Terminal","cruise_terminal":"Cruise Terminal",
    "yacht_club":"Yacht Club","hotel_jetty":"Hotel Jetty","public_pier":"Public Pier",
    "seaplane_base":"Seaplane Base","working_harbour":"Working Harbour",
    "floating_pontoon":"Floating Pontoon","dive_centre":"Dive Centre",
    "beach_club_jetty":"Beach Club Jetty","water_taxi_stop":"Water Taxi","abra_station":"Abra",
    "water_bus_terminal":"Water Bus","floating_helipad":"Helipad",
}
bp_added = 0
for slug, city_id in BP_CITY_MAP.items():
    fp = BP_DIR / f"{slug}.json"
    if not fp.exists(): continue
    data = json.loads(fp.read_text())
    for bp in data.get("boarding_points", []):
        if bp.get("relevance") == "hide": continue
        if bp.get("lng") is None or bp.get("lat") is None: continue
        features.append({
            "type":"Feature",
            "geometry":{"type":"Point","coordinates":[bp["lng"], bp["lat"]]},
            "properties":{
                "id": bp.get("id"),
                "type":"poi",
                "name": bp.get("name"),
                "shortName": bp.get("name"),
                "fullName": bp.get("name"),
                "parent_city_id": city_id,
                "bp_type": bp.get("type"),
                "bp_type_label": BP_TYPE_LABELS.get(bp.get("type"), bp.get("type")),
                "bp_relevance": bp.get("relevance"),
                "linked_locale": bp.get("linked_locale"),
                "operator": bp.get("operator"),
                "berths_or_capacity": bp.get("berths_or_capacity"),
                "charging_potential": bp.get("charging_potential"),
                "notes": bp.get("notes"),
                "source": bp.get("source"),
            },
        })
        bp_added += 1
print(f"Injected {bp_added} curated boarding points across {len(BP_CITY_MAP)} cities")

# ---------- Global suppression: ghost locales / aspirational POIs / route-description nodes ----------
import re as _re
SUPPRESS_ID_TOKENS = (
    "cross-border", "cross-strait", "out-of-range", "out_of_range",
    "aspirational", "marquee", "-aspiration", "-quanta-lr-gateway",
    "-quanta-lr-inter-cluster", "-trans-archipelago", "-line-haul",
)
SUPPRESS_NAME_PATTERNS = [
    _re.compile(r"[\u2194\u21c4\u27f7]"),  # ↔ ⇄ ⟷
    _re.compile(r"cross[- ]border", _re.I),
    _re.compile(r"out[- ]of[- ]range", _re.I),
    _re.compile(r"aspirational", _re.I),
    _re.compile(r"\bmarquee\b", _re.I),
    _re.compile(r"line[- ]haul", _re.I),
    _re.compile(r"inter[- ]cluster", _re.I),
    _re.compile(r"trans[- ]archipelago", _re.I),
    _re.compile(r"\bdirect\b\s*$", _re.I),
]

def _should_suppress(p):
    if p.get("type") == "city":
        return False
    nid = (p.get("id") or "").lower()
    if any(tok in nid for tok in SUPPRESS_ID_TOKENS):
        return True
    name = p.get("name") or ""
    for rx in SUPPRESS_NAME_PATTERNS:
        if rx.search(name):
            return True
    return False

before = len(features)
features = [f for f in features if not _should_suppress(f["properties"])]
print(f"Suppressed {before - len(features)} ghost/aspirational nodes")

# ---------- Centroid-stack dedup: any locale/POI within 800m of its parent city anchor → drop ----------
city_coords = {f["properties"]["id"]: f["geometry"]["coordinates"]
               for f in features if f["properties"].get("type") == "city"}

def _haversine_m(a, b):
    import math
    lng1,lat1 = a; lng2,lat2 = b
    R = 6371000
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2-lat1); dl = math.radians(lng2-lng1)
    x = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*R*math.asin(math.sqrt(x))

dedup_kept = []
dropped_stacked = 0
seen_at_coord = {}  # parent_city_id -> list of (lng,lat)
for f in features:
    p = f["properties"]; t = p.get("type")
    if t not in ("locale", "poi"):
        dedup_kept.append(f); continue
    # curated boarding points are trusted — skip dedup
    if p.get("bp_type"):
        dedup_kept.append(f); continue
    coord = f["geometry"]["coordinates"]
    pcid = p.get("parent_city_id")
    if pcid and pcid in city_coords:
        if _haversine_m(coord, city_coords[pcid]) < 800:
            dropped_stacked += 1
            continue
    # Suppress duplicates within 200m of an already-kept node of same parent
    bucket = seen_at_coord.setdefault(pcid, [])
    if any(_haversine_m(coord, c) < 200 for c in bucket):
        dropped_stacked += 1
        continue
    bucket.append(coord)
    dedup_kept.append(f)
features = dedup_kept
print(f"Dropped {dropped_stacked} centroid-stacked / dup-coord nodes")

by_type = {}
for f in features:
    by_type.setdefault(f["properties"].get("type","unknown"), []).append(f)

# ---------- Routes (LineString features) ----------
def great_circle(lng1, lat1, lng2, lat2, n=32):
    """Simple geodesic interpolation."""
    from math import radians, degrees, sin, cos, asin, atan2, sqrt
    φ1, φ2 = radians(lat1), radians(lat2)
    λ1, λ2 = radians(lng1), radians(lng2)
    d = 2*asin(sqrt(sin((φ2-φ1)/2)**2 + cos(φ1)*cos(φ2)*sin((λ2-λ1)/2)**2))
    if d == 0: return [[lng1,lat1],[lng2,lat2]]
    pts = []
    for i in range(n+1):
        f = i/n
        A = sin((1-f)*d)/sin(d); B = sin(f*d)/sin(d)
        x = A*cos(φ1)*cos(λ1) + B*cos(φ2)*cos(λ2)
        y = A*cos(φ1)*sin(λ1) + B*cos(φ2)*sin(λ2)
        z = A*sin(φ1) + B*sin(φ2)
        φ = atan2(z, sqrt(x*x+y*y)); λ = atan2(y,x)
        pts.append([degrees(λ), degrees(φ)])
    return pts

harbour_overrides = json.loads((HERE / "harbour-overrides.json").read_text())
harbour_overrides = {k: v for k, v in harbour_overrides.items() if not k.startswith("_")}
route_waypoints_raw = json.loads((HERE / "route-waypoints.json").read_text())
route_waypoints = {}
for k, v in route_waypoints_raw.items():
    if k.startswith("_"): continue
    a, b = k.split("|")
    route_waypoints[(a, b)] = v
    route_waypoints[(b, a)] = list(reversed(v))

def origin_coords(node):
    """Return harbour-anchor coords if override exists, else node coords."""
    nid = node.get("id")
    if nid in harbour_overrides:
        return harbour_overrides[nid]
    return coords_of(node)

route_features = []
for e in edge_list:
    a = node_by_id.get(e.get("from_node_id"))
    b = node_by_id.get(e.get("to_node_id"))
    if not a or not b: continue
    ca, cb = origin_coords(a), origin_coords(b)
    if not ca or not cb: continue
    plat = (e.get("platform") or "").strip()
    if plat not in ("Pioneer II","Quanta-LR"): continue
    waypoints = route_waypoints.get((a.get("id"), b.get("id")))
    if waypoints:
        # Build polyline as great-circle arcs between waypoints
        pts_seq = [ca] + list(waypoints) + [cb]
        arc = []
        for i in range(len(pts_seq) - 1):
            seg = great_circle(pts_seq[i][0], pts_seq[i][1], pts_seq[i+1][0], pts_seq[i+1][1], n=12)
            if i > 0: seg = seg[1:]
            arc.extend(seg)
    else:
        arc = great_circle(ca[0],ca[1],cb[0],cb[1], n=24)
    route_features.append({
        "type":"Feature",
        "geometry":{"type":"LineString","coordinates":arc},
        "properties":{
            "id": e.get("id"),
            "platform": plat,
            "distance_nm": e.get("distance_nm"),
            "edge_class": e.get("edge_class"),
            "from": e.get("from_node_id"),
            "to":   e.get("to_node_id"),
        },
    })

n_city   = len(by_type.get("city", []))
n_locale = len(by_type.get("locale", []))
n_poi    = len(by_type.get("poi", []))
print(f"Nodes: cities={n_city} locales={n_locale} pois={n_poi} routes={len(route_features)} stories={len(stories)}")

# ---------- HTML ----------
HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Navier Atlas · Mobility Network</title>
<link href="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css" rel="stylesheet" />
<script src="https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {
  --bg-0:#0a0e14; --bg-1:#11161e; --bg-2:#1a212c; --bg-3:#232c3a;
  --line:rgba(255,255,255,0.07); --line-strong:rgba(255,255,255,0.14);
  --text-0:#e8ecf1; --text-1:#aab3c0; --text-2:#6b7684;
  --accent:#6ee7b7; --accent-dim:#34d399;
  --coral:#fb7185; --steel:#60a5fa; --gold:#fbbf24;
}
* { box-sizing:border-box; }
html, body { margin:0; padding:0; height:100%; background:var(--bg-0); color:var(--text-0); font-family:'Inter',system-ui,sans-serif; -webkit-font-smoothing:antialiased; }
#map { position:absolute; top:0; bottom:0; left:0; right:420px; background:var(--bg-0); }
.maplibregl-canvas { outline:none; }

/* Header card */
#header {
  position:absolute; top:24px; left:24px; z-index:10;
  background:rgba(17,22,30,0.86); backdrop-filter:blur(20px) saturate(140%); -webkit-backdrop-filter:blur(20px) saturate(140%);
  border:1px solid var(--line-strong); border-radius:14px; padding:16px 18px 12px;
  box-shadow:0 10px 40px rgba(0,0,0,0.35); min-width:340px; max-width:380px;
}
#header .brand { display:flex; align-items:center; gap:10px; }
#header .brand-mark { width:28px; height:28px; border-radius:8px; background:linear-gradient(135deg,var(--accent),#14b8a6); display:flex; align-items:center; justify-content:center; box-shadow:0 0 20px rgba(110,231,183,0.45); }
#header .brand-mark svg { width:16px; height:16px; }
#header .brand-text .name { font-weight:700; font-size:15px; letter-spacing:-0.01em; }
#header .brand-text .tag { font-size:10px; color:var(--text-2); letter-spacing:0.08em; text-transform:uppercase; font-weight:500; display:block; margin-top:2px;}
#header .stats { margin-top:12px; padding-top:10px; border-top:1px solid var(--line); display:flex; gap:18px; }
#header .stat .v { font-family:'JetBrains Mono',monospace; font-size:17px; font-weight:600; line-height:1; }
#header .stat .k { font-size:9px; color:var(--text-2); margin-top:4px; letter-spacing:0.1em; text-transform:uppercase; }
#header .stat.accent .v { color:var(--accent); }
#header .stat.coral  .v { color:var(--coral); }
#header .stat.steel  .v { color:var(--steel); }
#header .stat.gold   .v { color:var(--gold); }

/* Search */
#searchwrap { position:absolute; top:24px; left:420px; z-index:11; }
#search {
  width:280px; padding:10px 14px; border-radius:10px; border:1px solid var(--line-strong);
  background:rgba(17,22,30,0.86); backdrop-filter:blur(20px); color:var(--text-0); font:500 13px Inter;
}
#search:focus { outline:none; border-color:rgba(110,231,183,0.5); }
#suggest {
  margin-top:6px; max-height:340px; overflow:auto; background:rgba(17,22,30,0.96); backdrop-filter:blur(20px);
  border:1px solid var(--line-strong); border-radius:10px; display:none;
}
#suggest div { padding:8px 14px; font-size:13px; cursor:pointer; border-bottom:1px solid var(--line); display:flex; justify-content:space-between; align-items:center; gap:8px; }
#suggest div:last-child { border-bottom:none; }
#suggest div:hover { background:rgba(110,231,183,0.08); }
#suggest .badge { font-size:9px; }

/* Story dropdown */
#story-trigger {
  padding:10px 16px; border-radius:10px; border:1px solid var(--line-strong);
  background:rgba(17,22,30,0.86); backdrop-filter:blur(20px); color:var(--text-0);
  font:500 13px Inter; cursor:pointer; margin-left:10px;
}
#story-trigger:hover { border-color:rgba(110,231,183,0.45); color:var(--accent); }
#story-menu {
  position:absolute; margin-top:6px; background:rgba(17,22,30,0.96); border:1px solid var(--line-strong);
  border-radius:10px; min-width:280px; display:none; overflow:hidden; box-shadow:0 12px 32px rgba(0,0,0,0.45);
}
#story-menu .item { padding:12px 16px; cursor:pointer; border-bottom:1px solid var(--line); }
#story-menu .item:last-child { border-bottom:none; }
#story-menu .item:hover { background:rgba(110,231,183,0.08); }
#story-menu .item .t { font-size:13px; font-weight:600; color:var(--text-0); }
#story-menu .item .s { font-size:11px; color:var(--text-2); margin-top:2px; }

/* Presets */
#presets { position:absolute; top:84px; left:420px; z-index:10; display:flex; flex-wrap:wrap; gap:6px; max-width:calc(100vw - 420px - 440px); }
.chip { background:rgba(17,22,30,0.86); backdrop-filter:blur(20px); border:1px solid var(--line-strong); color:var(--text-1); font:500 12px Inter; padding:7px 13px; border-radius:999px; cursor:pointer; }
.chip:hover { background:rgba(110,231,183,0.12); border-color:rgba(110,231,183,0.35); color:var(--text-0); }
.chip.active { background:var(--accent); border-color:var(--accent); color:#0a0e14; }

/* Layer toggles (right of presets) */
#toggles { position:absolute; bottom:24px; left:50%; transform:translateX(-50%); z-index:10; display:flex; gap:6px; }
.toggle { background:rgba(17,22,30,0.86); backdrop-filter:blur(20px); border:1px solid var(--line-strong); color:var(--text-1); font:500 11px Inter; padding:7px 12px; border-radius:999px; cursor:pointer; letter-spacing:0.02em; }
.toggle.on { background:rgba(110,231,183,0.18); color:var(--accent); border-color:rgba(110,231,183,0.45); }
.toggle.steel.on { background:rgba(96,165,250,0.18); color:var(--steel); border-color:rgba(96,165,250,0.45); }

/* Legend */
#legend { position:absolute; bottom:24px; left:24px; z-index:10; background:rgba(17,22,30,0.86); backdrop-filter:blur(20px); border:1px solid var(--line-strong); border-radius:12px; padding:11px 14px; font-size:11px; color:var(--text-1); }
#legend .head { font-size:9px; text-transform:uppercase; letter-spacing:0.12em; color:var(--text-2); font-weight:600; margin-bottom:6px; }
#legend .row { display:flex; align-items:center; gap:8px; padding:2px 0; }
#legend .dot { width:9px; height:9px; border-radius:50%; box-shadow:0 0 8px currentColor; }
#legend .dot.city   { background:var(--accent); color:var(--accent); }
#legend .dot.locale { background:var(--coral);  color:var(--coral); }
#legend .dot.poi    { background:var(--steel);  color:var(--steel); }
#legend .line { width:18px; height:0; border-top:2px solid var(--accent); }
#legend .line.qlr { border-top:2px dashed var(--steel); }

/* Footer */
#footer { position:absolute; bottom:24px; right:444px; z-index:10; font-size:10px; color:var(--text-2); letter-spacing:0.12em; text-transform:uppercase; background:rgba(17,22,30,0.6); padding:6px 12px; border-radius:6px; border:1px solid var(--line); }

/* Side panel */
#panel { position:absolute; top:0; right:0; bottom:0; width:420px; background:var(--bg-1); border-left:1px solid var(--line-strong); overflow-y:auto; }
#panel::-webkit-scrollbar { width:6px; }
#panel::-webkit-scrollbar-thumb { background:var(--line-strong); border-radius:3px; }
.panel-empty { padding:48px 32px; color:var(--text-2); font-size:13px; line-height:1.6; }
.panel-empty h2 { color:var(--text-0); font-size:18px; font-weight:600; margin:0 0 12px; letter-spacing:-0.01em;}
.panel-empty .hint { display:flex; gap:10px; align-items:flex-start; margin-top:14px; }
.panel-empty .hint-num { flex-shrink:0; width:20px; height:20px; border-radius:50%; background:var(--bg-3); color:var(--accent); font:600 11px 'JetBrains Mono'; display:flex; align-items:center; justify-content:center; }

/* Story header strip */
.story-header { padding:24px 28px 18px; border-bottom:1px solid var(--line); background:linear-gradient(135deg,rgba(110,231,183,0.08),rgba(96,165,250,0.04)); position:relative; }
.story-header.accent-emerald { background:linear-gradient(135deg,rgba(110,231,183,0.16),rgba(20,184,166,0.04)); }
.story-header.accent-coral   { background:linear-gradient(135deg,rgba(251,113,133,0.16),rgba(244,63,94,0.04)); }
.story-header.accent-gold    { background:linear-gradient(135deg,rgba(251,191,36,0.16),rgba(217,119,6,0.04)); }
.story-header.accent-steel   { background:linear-gradient(135deg,rgba(96,165,250,0.16),rgba(37,99,235,0.04)); }
.story-header.accent-violet  { background:linear-gradient(135deg,rgba(167,139,250,0.16),rgba(124,58,237,0.04)); }
.story-header .partner-mark { font-size:10px; text-transform:uppercase; letter-spacing:0.16em; color:var(--accent); font-weight:600; margin-bottom:8px; }
.story-header h2 { font-size:22px; font-weight:700; letter-spacing:-0.02em; margin:0 0 4px; }
.story-header .subtitle { font-size:13px; color:var(--text-1); }
.story-header .close { position:absolute; top:18px; right:20px; background:none; border:none; color:var(--text-2); cursor:pointer; font-size:18px; }
.story-header .close:hover { color:var(--text-0); }

.story-metrics { display:grid; grid-template-columns:1fr 1fr; gap:10px; padding:18px 28px; border-bottom:1px solid var(--line); }
.story-metric { background:var(--bg-2); border:1px solid var(--line); border-radius:10px; padding:12px 14px; }
.story-metric .v { font-family:'JetBrains Mono',monospace; font-weight:600; font-size:18px; color:var(--accent); }
.story-metric .l { font-size:10px; color:var(--text-2); text-transform:uppercase; letter-spacing:0.08em; margin-top:4px; }
.story-metric .s { font-size:11px; color:var(--text-1); margin-top:2px; }

.story-exec  { padding:18px 28px; border-bottom:1px solid var(--line); font-size:13px; line-height:1.6; color:var(--text-0); }
.story-card  { padding:16px 28px; border-bottom:1px solid var(--line); cursor:pointer; }
.story-card:hover { background:var(--bg-2); }
.story-card .city { font-size:10px; text-transform:uppercase; letter-spacing:0.1em; color:var(--text-2); margin-bottom:4px; }
.story-card h3 { font-size:14px; font-weight:600; margin:0 0 6px; color:var(--text-0); }
.story-card .body { font-size:12px; line-height:1.55; color:var(--text-1); }
.story-card .mode { display:inline-block; font-size:9px; padding:2px 8px; border-radius:999px; margin-left:8px; vertical-align:middle; text-transform:uppercase; letter-spacing:0.08em; font-weight:600;}
.story-card .mode.pilot { background:rgba(110,231,183,0.16); color:var(--accent); }
.story-card .mode.steady { background:rgba(96,165,250,0.13); color:var(--steel); }

.story-deal { padding:18px 28px; border-bottom:1px solid var(--line); }
.story-deal h3 { font-size:10px; text-transform:uppercase; letter-spacing:0.12em; color:var(--text-2); margin:0 0 10px; }
.story-deal dl { margin:0; display:grid; grid-template-columns:120px 1fr; gap:6px 12px; }
.story-deal dt { font-size:11px; color:var(--text-2); text-transform:uppercase; letter-spacing:0.06em; }
.story-deal dd { font-size:12px; color:var(--text-0); margin:0; line-height:1.45; }

.story-next { padding:18px 28px; }
.story-next h3 { font-size:10px; text-transform:uppercase; letter-spacing:0.12em; color:var(--text-2); margin:0 0 10px; }
.story-next ol { margin:0; padding-left:18px; font-size:13px; color:var(--text-0); line-height:1.6; }

/* Node detail */
.panel-hero { padding:24px 28px 18px; border-bottom:1px solid var(--line); }
.panel-hero .type-row { display:flex; align-items:center; gap:8px; margin-bottom:8px; flex-wrap:wrap; }
.panel-hero .type-pill { font-size:9px; letter-spacing:0.12em; text-transform:uppercase; font-weight:600; padding:3px 9px; border-radius:999px; }
.type-pill.city   { background:rgba(110,231,183,0.13); color:var(--accent); border:1px solid rgba(110,231,183,0.3); }
.type-pill.locale { background:rgba(251,113,133,0.13); color:var(--coral);  border:1px solid rgba(251,113,133,0.3); }
.type-pill.poi    { background:rgba(96,165,250,0.13);  color:var(--steel);  border:1px solid rgba(96,165,250,0.3); }
.panel-hero h2 { font-size:22px; font-weight:700; letter-spacing:-0.02em; margin:0 0 4px; }
.panel-hero .subtitle { font-size:12px; color:var(--text-1); }
.panel-hero .ring-toggle { margin-top:10px; padding:6px 12px; font:500 11px Inter; background:var(--bg-3); color:var(--text-1); border:1px solid var(--line-strong); border-radius:8px; cursor:pointer; }
.panel-hero .ring-toggle:hover { color:var(--accent); border-color:rgba(110,231,183,0.4); }
.panel-hero .ring-toggle.active { background:rgba(110,231,183,0.16); color:var(--accent); border-color:rgba(110,231,183,0.5); }
.panel-section { padding:16px 28px; border-bottom:1px solid var(--line); }
.panel-section h3 { font-size:10px; text-transform:uppercase; letter-spacing:0.12em; color:var(--text-2); font-weight:600; margin:0 0 10px; }
.panel-section .what-distinct { font-size:13px; line-height:1.55; color:var(--text-0); }
.kv-grid { display:grid; grid-template-columns:auto 1fr; gap:6px 12px; }
.kv-grid dt { font-size:10px; color:var(--text-2); text-transform:uppercase; letter-spacing:0.06em; padding-top:2px; }
.kv-grid dd { font-size:12px; color:var(--text-0); margin:0; line-height:1.45; word-break:break-word; }
.badges { display:flex; flex-wrap:wrap; gap:5px; }
.badge { font-size:10px; padding:3px 8px; border-radius:5px; background:var(--bg-3); color:var(--text-1); border:1px solid var(--line-strong); }
.badge.platform { background:rgba(110,231,183,0.08); color:var(--accent-dim); border-color:rgba(110,231,183,0.25); }
.scores { display:flex; flex-direction:column; gap:8px; }
.score { display:grid; grid-template-columns:100px 1fr 26px; align-items:center; gap:10px; }
.score .label { font-size:11px; color:var(--text-1); text-transform:capitalize; }
.score .bar { height:5px; background:var(--bg-3); border-radius:3px; overflow:hidden; }
.score .bar > div { height:100%; background:linear-gradient(90deg,var(--accent-dim),var(--accent)); border-radius:3px; box-shadow:0 0 8px rgba(110,231,183,0.4); }
.score .val { font:500 10px 'JetBrains Mono'; color:var(--text-1); text-align:right; }

.maplibregl-ctrl-group { background:rgba(17,22,30,0.85) !important; border:1px solid var(--line-strong) !important; }
.maplibregl-ctrl-group button { background:transparent !important; }
.maplibregl-ctrl-group button:hover { background:rgba(255,255,255,0.06) !important; }
.maplibregl-ctrl-icon { filter: invert(0.85); }
.maplibregl-ctrl-attrib { background:rgba(10,14,20,0.7) !important; color:var(--text-2) !important; font-size:10px !important; }
.maplibregl-ctrl-attrib a { color:var(--text-1) !important; }
</style>
</head>
<body>
<div id="map"></div>

<div id="header">
  <div class="brand">
    <div class="brand-mark"><svg viewBox="0 0 24 24" fill="none" stroke="#0a0e14" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M3 18 L12 4 L21 18"/><path d="M7 18 L17 18"/></svg></div>
    <div class="brand-text"><span class="name">Navier Atlas</span><span class="tag">Mobility Network · Confidential</span></div>
  </div>
  <div class="stats">
    <div class="stat accent"><span class="v">__N_CITY__</span><span class="k">Cities</span></div>
    <div class="stat coral"><span class="v">__N_LOCALE__</span><span class="k">Locales</span></div>
    <div class="stat steel"><span class="v">__N_POI__</span><span class="k">POIs</span></div>
    <div class="stat gold"><span class="v">__N_ROUTE__</span><span class="k">Routes</span></div>
  </div>
</div>

<div id="searchwrap">
  <input id="search" placeholder="Search cities, locales, POIs…" autocomplete="off" />
  <button id="story-trigger">Stories ▾</button>
  <div id="story-menu"></div>
  <div id="suggest"></div>
</div>

<div id="presets">
  <button class="chip" data-c="global">Global</button>
  <button class="chip" data-c="mena">MENA</button>
  <button class="chip" data-c="sea">Southeast Asia</button>
  <button class="chip" data-c="dubai">Dubai</button>
  <button class="chip" data-c="ad">Abu Dhabi</button>
  <button class="chip" data-c="sg">Singapore</button>
  <button class="chip" data-c="bali">Bali</button>
  <button class="chip" data-c="rsg">Red Sea Global</button>
  <button class="chip" data-c="phuket">Phuket</button>
</div>

<div id="toggles">
  <button class="toggle on" id="t-routes">Routes</button>
  <button class="toggle on" id="t-p2">Pioneer II</button>
  <button class="toggle steel on" id="t-qlr">Quanta-LR</button>
  <button class="toggle on" id="t-locales">Locales</button>
  <button class="toggle steel on" id="t-pois">POIs</button>
</div>

<div id="legend">
  <div class="head">Network</div>
  <div class="row"><span class="dot city"></span>City</div>
  <div class="row"><span class="dot locale"></span>Locale</div>
  <div class="row"><span class="dot poi"></span>POI</div>
  <div class="row" style="margin-top:6px"><span class="line"></span>Pioneer II (≤70 nm)</div>
  <div class="row"><span class="line qlr"></span>Quanta-LR (≤2,000 nm)</div>
</div>

<div id="footer">Navier Mobility · 2026</div>

<div id="panel"><div class="panel-empty">
  <h2>Select a node</h2>
  <p>Cities cluster at world view. Zoom in to reveal locales and POIs.</p>
  <div class="hint"><div class="hint-num">1</div><div>Use <b>Stories ▾</b> to walk a partner pitch.</div></div>
  <div class="hint"><div class="hint-num">2</div><div>Search or use preset chips to fly to a market.</div></div>
  <div class="hint"><div class="hint-num">3</div><div>Click any node for context and range rings.</div></div>
</div></div>

<script>
const FEATURES_BY_TYPE = __FEATURES__;
const ROUTES = __ROUTES__;
const STORIES = __STORIES__;
const NODE_INDEX = {}; // id -> {coords, props}
for (const t of Object.keys(FEATURES_BY_TYPE)) for (const f of FEATURES_BY_TYPE[t]) { const p=f.properties; if (p.id) NODE_INDEX[p.id]={coords:f.geometry.coordinates, props:p}; }

const CAMERAS = {
  global:{ center:[40,15], zoom:1.8 },
  mena:  { center:[50,24], zoom:4.2 },
  sea:   { center:[112,2], zoom:4.2 },
  dubai: { center:[55.27,25.20], zoom:11 },
  ad:    { center:[54.37,24.47], zoom:11 },
  sg:    { center:[103.85,1.30], zoom:11 },
  bali:  { center:[115.18,-8.50], zoom:9 },
  rsg:   { center:[37.0,25.5], zoom:7.5 },
  phuket:{ center:[98.35,7.95], zoom:10 },
};

const map = new maplibregl.Map({
  container:'map',
  style:{
    version:8,
    glyphs:'https://demotiles.maplibre.org/font/{fontstack}/{range}.pbf',
    sources:{ 'carto-dark':{ type:'raster', tiles:[
      'https://a.basemaps.cartocdn.com/rastertiles/dark_all/{z}/{x}/{y}@2x.png',
      'https://b.basemaps.cartocdn.com/rastertiles/dark_all/{z}/{x}/{y}@2x.png',
      'https://c.basemaps.cartocdn.com/rastertiles/dark_all/{z}/{x}/{y}@2x.png',
      'https://d.basemaps.cartocdn.com/rastertiles/dark_all/{z}/{x}/{y}@2x.png'
    ], tileSize:256, attribution:'© OpenStreetMap · © CARTO' }},
    layers:[{ id:'basemap', type:'raster', source:'carto-dark' }]
  },
  center:CAMERAS.global.center,
  zoom:CAMERAS.global.zoom,
  attributionControl:{ compact:true }
});
map.addControl(new maplibregl.NavigationControl({ showCompass:false }), 'top-right');

map.on('load', () => {
  // Routes
  map.addSource('routes', { type:'geojson', data:{type:'FeatureCollection', features:ROUTES} });
  map.addLayer({ id:'route-p2', type:'line', source:'routes', filter:['==',['get','platform'],'Pioneer II'],
    paint:{ 'line-color':'#6ee7b7', 'line-width':2, 'line-opacity':0.55 }, layout:{'line-cap':'round','line-join':'round'} });
  map.addLayer({ id:'route-qlr', type:'line', source:'routes', filter:['==',['get','platform'],'Quanta-LR'],
    paint:{ 'line-color':'#60a5fa', 'line-width':2, 'line-opacity':0.5, 'line-dasharray':[2,2] }, layout:{'line-cap':'round','line-join':'round'} });

  // Cities (clustered)
  map.addSource('cities', { type:'geojson', data:{type:'FeatureCollection',features:FEATURES_BY_TYPE.city||[]}, cluster:true, clusterMaxZoom:5, clusterRadius:48 });
  map.addLayer({ id:'city-cluster-halo', type:'circle', source:'cities', filter:['has','point_count'],
    paint:{ 'circle-color':'#6ee7b7','circle-opacity':0.18,'circle-radius':['step',['get','point_count'],28,5,36,15,46,30,56],'circle-blur':0.4 }});
  map.addLayer({ id:'city-clusters', type:'circle', source:'cities', filter:['has','point_count'],
    paint:{ 'circle-color':'#6ee7b7','circle-radius':['step',['get','point_count'],16,5,22,15,28,30,34],'circle-stroke-width':2,'circle-stroke-color':'rgba(255,255,255,0.85)','circle-opacity':0.95 }});
  map.addLayer({ id:'city-cluster-count', type:'symbol', source:'cities', filter:['has','point_count'],
    layout:{ 'text-field':['get','point_count_abbreviated'],'text-font':['Noto Sans Bold'],'text-size':13 }, paint:{'text-color':'#0a0e14'} });
  map.addLayer({ id:'city-halo', type:'circle', source:'cities', filter:['!',['has','point_count']],
    paint:{ 'circle-color':'#6ee7b7','circle-opacity':0.22,'circle-radius':16,'circle-blur':0.5 }});
  map.addLayer({ id:'city-points', type:'circle', source:'cities', filter:['!',['has','point_count']],
    paint:{ 'circle-color':'#6ee7b7','circle-radius':6,'circle-stroke-width':2,'circle-stroke-color':'#0a0e14' }});
  map.addLayer({ id:'city-labels', type:'symbol', source:'cities', filter:['!',['has','point_count']],
    layout:{ 'text-field':['get','shortName'],'text-font':['Noto Sans Bold'],'text-size':12,'text-offset':[0,1.2],'text-anchor':'top','text-allow-overlap':false }, paint:{ 'text-color':'#e8ecf1','text-halo-color':'#0a0e14','text-halo-width':1.5 }, minzoom:4 });

  // Locales (clustered at mid zoom)
  map.addSource('locales', { type:'geojson', data:{type:'FeatureCollection',features:FEATURES_BY_TYPE.locale||[]}, cluster:true, clusterMaxZoom:8, clusterRadius:36 });
  map.addLayer({ id:'locale-clusters', type:'circle', source:'locales', filter:['has','point_count'], minzoom:6,
    paint:{ 'circle-color':'#fb7185','circle-radius':['step',['get','point_count'],12,5,18,15,24],'circle-opacity':0.7,'circle-stroke-width':1.5,'circle-stroke-color':'rgba(255,255,255,0.5)' }});
  map.addLayer({ id:'locale-cluster-count', type:'symbol', source:'locales', filter:['has','point_count'], minzoom:6,
    layout:{ 'text-field':['get','point_count_abbreviated'],'text-font':['Noto Sans Bold'],'text-size':11 }, paint:{'text-color':'#0a0e14'} });
  map.addLayer({ id:'locale-halo', type:'circle', source:'locales', filter:['!',['has','point_count']], minzoom:6,
    paint:{ 'circle-color':'#fb7185','circle-opacity':0.2,'circle-radius':10,'circle-blur':0.6 }});
  map.addLayer({ id:'locale-points', type:'circle', source:'locales', filter:['!',['has','point_count']], minzoom:6,
    paint:{ 'circle-color':'#fb7185','circle-radius':4.5,'circle-stroke-width':1.5,'circle-stroke-color':'#0a0e14' }});
  map.addLayer({ id:'locale-labels', type:'symbol', source:'locales', filter:['!',['has','point_count']], minzoom:9,
    layout:{ 'text-field':['get','shortName'],'text-font':['Noto Sans Regular'],'text-size':11,'text-offset':[0,0.95],'text-anchor':'top' }, paint:{ 'text-color':'#fcd0d6','text-halo-color':'#0a0e14','text-halo-width':1.4 }});

  // POIs (clustered at mid zoom)
  map.addSource('pois', { type:'geojson', data:{type:'FeatureCollection',features:FEATURES_BY_TYPE.poi||[]}, cluster:true, clusterMaxZoom:10, clusterRadius:30 });
  map.addLayer({ id:'poi-clusters', type:'circle', source:'pois', filter:['has','point_count'], minzoom:8,
    paint:{ 'circle-color':'#60a5fa','circle-radius':['step',['get','point_count'],10,5,15,20,20],'circle-opacity':0.6,'circle-stroke-width':1.2,'circle-stroke-color':'rgba(255,255,255,0.4)' }});
  map.addLayer({ id:'poi-cluster-count', type:'symbol', source:'pois', filter:['has','point_count'], minzoom:8,
    layout:{ 'text-field':['get','point_count_abbreviated'],'text-font':['Noto Sans Bold'],'text-size':10 }, paint:{'text-color':'#0a0e14'} });
  map.addLayer({ id:'poi-points', type:'circle', source:'pois', filter:['!',['has','point_count']], minzoom:9,
    paint:{ 'circle-color':'#60a5fa','circle-radius':3.5,'circle-stroke-width':1,'circle-stroke-color':'#0a0e14' }});
  map.addLayer({ id:'poi-labels', type:'symbol', source:'pois', filter:['!',['has','point_count']], minzoom:11,
    layout:{ 'text-field':['get','shortName'],'text-font':['Noto Sans Regular'],'text-size':10,'text-offset':[0,0.8],'text-anchor':'top' }, paint:{ 'text-color':'#bfdbfe','text-halo-color':'#0a0e14','text-halo-width':1.4 }});

  // Range ring source (filled by selection)
  map.addSource('rings', { type:'geojson', data:{type:'FeatureCollection', features:[]} });
  map.addLayer({ id:'ring-p2', type:'line', source:'rings', filter:['==',['get','platform'],'Pioneer II'],
    paint:{ 'line-color':'#6ee7b7','line-width':1.5,'line-opacity':0.7,'line-dasharray':[2,3] }});
  map.addLayer({ id:'ring-qlr', type:'line', source:'rings', filter:['==',['get','platform'],'Quanta-LR'],
    paint:{ 'line-color':'#60a5fa','line-width':1.5,'line-opacity':0.5,'line-dasharray':[1,3] }});
  map.addLayer({ id:'ring-fill-p2', type:'fill', source:'rings', filter:['==',['get','platform'],'Pioneer II'],
    paint:{ 'fill-color':'#6ee7b7','fill-opacity':0.06 }});

  // Click handlers — include halo layers so the visible glow is clickable too
  for (const layer of ['city-points','city-halo','locale-points','locale-halo','poi-points']) {
    map.on('click', layer, (e) => {
      const f = e.features[0];
      if (f.properties.cluster) return;
      const coords = f.geometry.coordinates;
      const type = f.properties.type;
      const zoom = type==='city' ? 10 : type==='locale' ? 12 : 14;
      map.flyTo({ center:coords, zoom:Math.max(zoom, map.getZoom()), duration:1200, essential:true });
      showDetail(f.properties, coords);
    });
    map.on('mouseenter', layer, () => map.getCanvas().style.cursor='pointer');
    map.on('mouseleave', layer, () => map.getCanvas().style.cursor='');
  }
  for (const layer of ['city-clusters','city-cluster-halo','locale-clusters','poi-clusters']) {
    const src = layer.startsWith('city') ? 'cities' : layer.startsWith('locale') ? 'locales' : 'pois';
    map.on('click', layer, (e) => {
      const features = map.queryRenderedFeatures(e.point,{layers:[layer]});
      const f = features[0]; if (!f || !f.properties.cluster_id) return;
      map.getSource(src).getClusterExpansionZoom(f.properties.cluster_id).then(z=>{
        map.easeTo({ center:f.geometry.coordinates, zoom:Math.max(z, map.getZoom()+1.5), duration:900 });
      });
    });
    map.on('mouseenter', layer, () => map.getCanvas().style.cursor='pointer');
    map.on('mouseleave', layer, () => map.getCanvas().style.cursor='');
  }

  // URL state
  applyUrlState();
  map.on('moveend', updateUrlState);
});

// ============ Range rings ============
function ringPolygon(lng, lat, nm, npts=64) {
  const km = nm * 1.852;
  const R = 6371;
  const φ1 = lat * Math.PI/180, λ1 = lng * Math.PI/180;
  const d = km/R;
  const pts = [];
  for (let i=0; i<=npts; i++) {
    const θ = (i/npts) * 2*Math.PI;
    const φ2 = Math.asin(Math.sin(φ1)*Math.cos(d) + Math.cos(φ1)*Math.sin(d)*Math.cos(θ));
    const λ2 = λ1 + Math.atan2(Math.sin(θ)*Math.sin(d)*Math.cos(φ1), Math.cos(d)-Math.sin(φ1)*Math.sin(φ2));
    pts.push([λ2*180/Math.PI, φ2*180/Math.PI]);
  }
  return pts;
}
let RING_ACTIVE = null;
function toggleRings(coords) {
  if (!coords) return;
  const key = coords.join(',');
  if (RING_ACTIVE === key) {
    map.getSource('rings').setData({type:'FeatureCollection',features:[]});
    RING_ACTIVE = null;
    document.querySelectorAll('.ring-toggle').forEach(b=>b.classList.remove('active'));
    return;
  }
  RING_ACTIVE = key;
  const fc = { type:'FeatureCollection', features:[
    { type:'Feature', properties:{platform:'Pioneer II'}, geometry:{type:'Polygon', coordinates:[ringPolygon(coords[0],coords[1],70)]} },
    { type:'Feature', properties:{platform:'Quanta-LR'}, geometry:{type:'LineString', coordinates:ringPolygon(coords[0],coords[1],2000)} },
  ]};
  map.getSource('rings').setData(fc);
  document.querySelectorAll('.ring-toggle').forEach(b=>b.classList.add('active'));
}

// ============ Detail panel ============
function escapeHtml(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function fmtValue(v){
  if (v==null||v==='') return null;
  if (typeof v==='boolean') return v?'yes':'no';
  if (typeof v==='number') return String(v);
  if (typeof v==='string') return escapeHtml(v);
  if (Array.isArray(v)) { if(!v.length) return null; return v.map(x=>typeof x==='string'?`<span class="badge">${escapeHtml(x)}</span>`:escapeHtml(JSON.stringify(x))).join(' '); }
  if (typeof v==='object') { const e=Object.entries(v).filter(([_,x])=>x!=null&&x!==''); if(!e.length) return null; return e.map(([k,x])=>`<span class="badge">${escapeHtml(k)}: ${escapeHtml(typeof x==='object'?JSON.stringify(x):x)}</span>`).join(' '); }
  return escapeHtml(String(v));
}
const SKIP=new Set(['name','type','country','region','parent_city','parent_city_id','poi_class','subtype','coords','coord','coords_resolved','coords_source','source_file','source_line','id','warnings']);
function showDetail(props, coords) {
  const p = document.getElementById('panel');
  const name = props.fullName || props.name || 'Unnamed';
  const type = (props.type||'').toLowerCase();
  const meta = [];
  if (props.poi_class) meta.push(props.poi_class);
  if (props.country) meta.push(props.country);
  if (props.region) meta.push(props.region);
  if (props.parent_city_id || props.parent_city) meta.push(`parent: ${props.parent_city_id || props.parent_city}`);

  let html = `<div class="panel-hero">
    <div class="type-row">
      <span class="type-pill ${type}">${type||'node'}</span>
      ${props.platform_class ? `<span class="badge platform">${escapeHtml(props.platform_class)}</span>`:''}
    </div>
    <h2>${escapeHtml(name)}</h2>
    <div class="subtitle">${escapeHtml(meta.join(' · ')||'—')}</div>
    <button class="ring-toggle" data-coords="${coords.join(',')}">Toggle range rings (70 nm + 2,000 nm)</button>
  </div>`;
  if (props.what_distinct) html += `<div class="panel-section"><h3>What's distinct</h3><div class="what-distinct">${escapeHtml(props.what_distinct)}</div></div>`;
  if (props.archetype_scores && typeof props.archetype_scores==='object') {
    html += `<div class="panel-section"><h3>Archetype fit</h3><div class="scores">`;
    for (const [k,v] of Object.entries(props.archetype_scores)) {
      const n = Math.max(0,Math.min(5,Number(v)||0));
      html += `<div class="score"><span class="label">${escapeHtml(k.replace(/_/g,' '))}</span><div class="bar"><div style="width:${(n/5)*100}%"></div></div><span class="val">${n}/5</span></div>`;
    }
    html += `</div></div>`;
  }
  const tags=[];
  if (props.posture)          tags.push(['posture',props.posture]);
  if (props.platform_fit)     tags.push(['platform fit',props.platform_fit]);
  if (props.pioneer_ii_bucket)tags.push(['Pioneer II',props.pioneer_ii_bucket]);
  if (props.quanta_lr_bucket) tags.push(['Quanta-LR',props.quanta_lr_bucket]);
  if (props.jurisdiction)     tags.push(['jurisdiction',props.jurisdiction]);
  if (tags.length) {
    html += `<div class="panel-section"><h3>Operating profile</h3><div class="kv-grid">`;
    for (const [k,v] of tags) { const fv=fmtValue(v); if (fv) html += `<dt>${escapeHtml(k)}</dt><dd>${fv}</dd>`; }
    html += `</div></div>`;
  }
  const skipExtra = new Set(['what_distinct','archetype_scores','posture','platform_fit','pioneer_ii_bucket','quanta_lr_bucket','jurisdiction','platform_class','shortName','fullName']);
  const rest = Object.entries(props).filter(([k,v])=>!SKIP.has(k)&&!skipExtra.has(k)&&v!=null&&v!=='');
  if (rest.length) {
    html += `<div class="panel-section"><h3>Details</h3><div class="kv-grid">`;
    for (const [k,v] of rest.slice(0,20)) { const fv=fmtValue(v); if (fv) html += `<dt>${escapeHtml(k.replace(/_/g,' '))}</dt><dd>${fv}</dd>`; }
    html += `</div></div>`;
  }
  if (coords) html += `<div class="panel-section"><h3>Coordinates</h3><div class="kv-grid"><dt>lat</dt><dd style="font-family:'JetBrains Mono'">${coords[1].toFixed(4)}</dd><dt>lng</dt><dd style="font-family:'JetBrains Mono'">${coords[0].toFixed(4)}</dd></div></div>`;
  p.innerHTML = html;
  p.scrollTop = 0;
  // Wire up ring toggle
  const rt = p.querySelector('.ring-toggle');
  if (rt) rt.addEventListener('click', () => {
    const c = rt.dataset.coords.split(',').map(Number);
    toggleRings(c);
    rt.classList.toggle('active');
  });
}

// ============ Stories ============
const STORY_BY_SLUG = {}; for (const s of STORIES) STORY_BY_SLUG[s.slug]=s;
const DEFAULT_OPACITY = {
  'route-p2': 0.9, 'route-qlr': 0.85,
  'city-points': 0.95, 'city-halo': 0.22, 'city-labels': 1,
  'locale-points': 0.9, 'locale-halo': 0.2, 'locale-labels': 1,
  'poi-points': 0.85, 'poi-labels': 1
};
function applyStoryFocus(cityIds) {
  if (!cityIds || !cityIds.length) {
    // Reset
    for (const [layer, op] of Object.entries(DEFAULT_OPACITY)) {
      const prop = layer.includes('label') ? 'text-opacity' : (layer.startsWith('route')||layer.includes('ring')) ? 'line-opacity' : 'circle-opacity';
      try { map.setPaintProperty(layer, prop, op); } catch(e){}
    }
    return;
  }
  const inSet = ['in', ['get','id'], ['literal', cityIds]];
  const routeIn = ['any', ['in', ['get','from'], ['literal', cityIds]], ['in', ['get','to'], ['literal', cityIds]]];
  try {
    map.setPaintProperty('route-p2', 'line-opacity', ['case', routeIn, 0.95, 0.04]);
    map.setPaintProperty('route-qlr','line-opacity', ['case', routeIn, 0.9, 0.04]);
    map.setPaintProperty('city-points','circle-opacity', ['case', inSet, 1, 0.18]);
    map.setPaintProperty('city-halo','circle-opacity', ['case', inSet, 0.35, 0.04]);
    map.setPaintProperty('city-labels','text-opacity', ['case', inSet, 1, 0.25]);
    map.setPaintProperty('locale-points','circle-opacity', 0.25);
    map.setPaintProperty('locale-halo','circle-opacity', 0.05);
    map.setPaintProperty('locale-labels','text-opacity', 0.3);
    map.setPaintProperty('poi-points','circle-opacity', 0.25);
    map.setPaintProperty('poi-labels','text-opacity', 0.25);
  } catch(e) { console.warn('focus', e); }
}
function closeStory() {
  applyStoryFocus(null);
  window.location.hash = '';
  document.getElementById('panel').innerHTML = document.getElementById('empty-tpl').innerHTML;
}
window.closeStory = closeStory;
function showStory(slug) {
  const s = STORY_BY_SLUG[slug]; if (!s) return;
  const p = document.getElementById('panel');
  const accent = s.accent_class || 'emerald';
  let html = `<div class="story-header accent-${accent}">
    <button class="close" onclick="closeStory()">×</button>
    <div class="partner-mark">${escapeHtml(s.partner_org_canonical_name || 'Partner')}</div>
    <h2>${escapeHtml(s.title)}</h2>
    <div class="subtitle">${escapeHtml(s.subtitle||'')}</div>
  </div>`;
  if (s.headline_metrics && s.headline_metrics.length) {
    html += `<div class="story-metrics">`;
    for (const m of s.headline_metrics) html += `<div class="story-metric"><div class="v">${escapeHtml(m.value)}</div><div class="l">${escapeHtml(m.label)}</div><div class="s">${escapeHtml(m.sub||'')}</div></div>`;
    html += `</div>`;
  }
  if (s.executive_summary) html += `<div class="story-exec">${escapeHtml(s.executive_summary)}</div>`;
  if (s.narrative && s.narrative.length) {
    for (const n of s.narrative) {
      const mode = n.mode||'steady';
      html += `<div class="story-card" data-city="${escapeHtml(n.city_id||'')}">
        <div class="city">${escapeHtml(n.city_id||'')}</div>
        <h3>${escapeHtml(n.headline||'')} <span class="mode ${mode}">${mode}</span></h3>
        <div class="body">${escapeHtml(n.body||'')}</div>
      </div>`;
    }
  }
  if (s.deal_shape) {
    html += `<div class="story-deal"><h3>Deal shape</h3><dl>`;
    for (const [k,v] of Object.entries(s.deal_shape)) html += `<dt>${escapeHtml(k.replace(/_/g,' '))}</dt><dd>${escapeHtml(v)}</dd>`;
    html += `</dl></div>`;
  }
  if (s.next_steps && s.next_steps.length) {
    html += `<div class="story-next"><h3>Next steps</h3><ol>`;
    for (const x of s.next_steps) html += `<li>${escapeHtml(x)}</li>`;
    html += `</ol></div>`;
  }
  p.innerHTML = html;
  p.scrollTop = 0;
  // Wire card → fly to city
  p.querySelectorAll('.story-card').forEach(card => {
    card.addEventListener('click', () => {
      const id = card.dataset.city;
      const n = NODE_INDEX[id];
      if (n) map.flyTo({ center:n.coords, zoom:9.5, duration:1400, essential:true });
    });
  });
  // Apply story focus — dim non-story cities/routes
  const storyCities = (s.narrative||[]).map(n => n.city_id).filter(Boolean);
  applyStoryFocus(storyCities);
  // Set initial view if provided
  if (s.initial_view) map.flyTo({ center:[s.initial_view.lng,s.initial_view.lat], zoom:s.initial_view.zoom, duration:1400, essential:true });
  window.location.hash = '#/story/' + slug;
}

// Stash empty template for restoration
const _empty = document.getElementById('panel').innerHTML;
const emptyTpl = document.createElement('template'); emptyTpl.id='empty-tpl'; emptyTpl.innerHTML=_empty;
document.body.appendChild(emptyTpl);

// Story menu
const sm = document.getElementById('story-menu');
for (const s of STORIES) {
  const d = document.createElement('div');
  d.className = 'item';
  d.innerHTML = `<div class="t">${escapeHtml(s.title)}</div><div class="s">${escapeHtml(s.subtitle||'')}</div>`;
  d.addEventListener('click', () => { showStory(s.slug); sm.style.display='none'; });
  sm.appendChild(d);
}
document.getElementById('story-trigger').addEventListener('click', (e) => {
  e.stopPropagation();
  sm.style.display = sm.style.display==='block'?'none':'block';
});
document.addEventListener('click', () => { sm.style.display='none'; });

// ============ Search ============
const SEARCH_INDEX = [];
for (const t of Object.keys(FEATURES_BY_TYPE)) {
  for (const f of FEATURES_BY_TYPE[t]) {
    const p = f.properties;
    SEARCH_INDEX.push({ id:p.id, name:p.fullName||p.name||'', type:t, coords:f.geometry.coordinates, ref:f });
  }
}
const searchBox = document.getElementById('search');
const suggest = document.getElementById('suggest');
searchBox.addEventListener('input', () => {
  const q = searchBox.value.trim().toLowerCase();
  if (!q) { suggest.style.display='none'; return; }
  const hits = SEARCH_INDEX.filter(x => x.name.toLowerCase().includes(q)).slice(0, 20);
  if (!hits.length) { suggest.style.display='none'; return; }
  suggest.innerHTML = hits.map(h => `<div data-id="${escapeHtml(h.id||'')}"><span>${escapeHtml(h.name)}</span><span class="badge">${h.type}</span></div>`).join('');
  suggest.style.display='block';
  suggest.querySelectorAll('div').forEach((d,i) => {
    d.addEventListener('click', () => {
      const h = hits[i];
      map.flyTo({ center:h.coords, zoom: h.type==='city'?10: h.type==='locale'?12: 14, duration:1300, essential:true });
      showDetail(h.ref.properties, h.coords);
      suggest.style.display='none';
      searchBox.value = h.name;
    });
  });
});
document.addEventListener('click', (e) => { if (!e.target.closest('#searchwrap')) suggest.style.display='none'; });

// ============ Presets ============
document.querySelectorAll('.chip').forEach(b => {
  b.addEventListener('click', () => {
    document.querySelectorAll('.chip').forEach(x=>x.classList.remove('active'));
    b.classList.add('active');
    const c = CAMERAS[b.dataset.c];
    if (c) map.flyTo({ center:c.center, zoom:c.zoom, duration:1400, essential:true });
  });
});

// ============ Layer toggles ============
function setLayerVis(id, on) { try { map.setLayoutProperty(id,'visibility', on?'visible':'none'); } catch(e){} }
function bindToggle(btnId, layers) {
  const b = document.getElementById(btnId);
  b.addEventListener('click', () => {
    const on = !b.classList.contains('on');
    b.classList.toggle('on', on);
    for (const l of layers) setLayerVis(l, on);
  });
}
bindToggle('t-p2',  ['route-p2']);
bindToggle('t-qlr', ['route-qlr']);
document.getElementById('t-routes').addEventListener('click', () => {
  const b = document.getElementById('t-routes'); const on = !b.classList.contains('on');
  b.classList.toggle('on', on);
  setLayerVis('route-p2',  on && document.getElementById('t-p2').classList.contains('on'));
  setLayerVis('route-qlr', on && document.getElementById('t-qlr').classList.contains('on'));
});
bindToggle('t-locales', ['locale-clusters','locale-cluster-count','locale-halo','locale-points','locale-labels']);
bindToggle('t-pois',    ['poi-clusters','poi-cluster-count','poi-points','poi-labels']);

// ============ URL state ============
function updateUrlState() {
  if (window.location.hash.startsWith('#/story/')) return;
  const c = map.getCenter(); const z = map.getZoom();
  history.replaceState(null,'',`#camera=${c.lng.toFixed(3)},${c.lat.toFixed(3)},${z.toFixed(2)}`);
}
function applyUrlState() {
  const h = window.location.hash;
  if (h.startsWith('#/story/')) { showStory(h.replace('#/story/','')); return; }
  const m = h.match(/#camera=([-\d.]+),([-\d.]+),([-\d.]+)/);
  if (m) map.jumpTo({ center:[parseFloat(m[1]),parseFloat(m[2])], zoom:parseFloat(m[3]) });
}
window.addEventListener('hashchange', () => { if (window.location.hash.startsWith('#/story/')) showStory(window.location.hash.replace('#/story/','')); });
</script>
</body>
</html>
"""

out = (HTML
  .replace("__FEATURES__", json.dumps(by_type))
  .replace("__ROUTES__", json.dumps(route_features))
  .replace("__STORIES__", json.dumps(stories))
  .replace("__N_CITY__", str(n_city))
  .replace("__N_LOCALE__", str(n_locale))
  .replace("__N_POI__", str(n_poi))
  .replace("__N_ROUTE__", str(len(route_features))))

(HERE / "index.html").write_text(out)
print(f"Wrote index.html — {len(out):,} bytes")
