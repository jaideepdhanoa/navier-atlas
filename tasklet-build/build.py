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
import json, re, math, os
from pathlib import Path

HERE = Path(__file__).parent
# CONFIDENTIALITY PARTITION (Part 1): the external atlas is built EXCLUSIVELY from
# the external_safe partition produced by partition/partition_filter.py.
EXT = HERE / "output-external"

def load(name):
    # prefer the external_safe partition; never fall back to raw internal data
    p = EXT / name
    if p.exists():
        return json.loads(p.read_text())
    p = HERE / name
    return json.loads(p.read_text()) if p.exists() else None

nodes_raw  = load("nodes.json")
edges_raw  = load("edges.json")
orgs_raw   = load("orgs.json")
overrides  = load("label-overrides.json") or {}

# Stories now come from the single sanitized external partition file.
_st = load("stories.json")
stories = (_st.get("stories") if isinstance(_st, dict) else _st) or []
vessel_specs = (_st.get("vessel_specs") if isinstance(_st, dict) else {}) or {}
# RESILIENCE FIX: vessel_specs lives canonically in partition/stories-partner-view.json.
# enrich_external.py copies it into output-external/stories.json, but a partition re-run
# regenerates stories.json WITHOUT it. Falling back to the frozen source means vessel_specs
# can NEVER be empty regardless of build order (kills the recurring silent-empty trap).
if not vessel_specs:
    _spv = HERE / "partition" / "stories-partner-view.json"
    if _spv.exists():
        vessel_specs = json.loads(_spv.read_text()).get("vessel_specs", {}) or {}
        if vessel_specs:
            print(f"vessel_specs: recovered {len(vessel_specs)} specs from frozen source (stories.json was empty)")
# Supplemental external_safe partner stories (Part 7.2). external_safe by construction.
_supp_st = load("supplemental-stories.json")
if _supp_st:
    extra = _supp_st.get("stories", []) if isinstance(_supp_st, dict) else _supp_st
    stories = stories + extra
    print(f"Merged {len(extra)} supplemental partner stories")

def as_list(x, key="nodes"):
    if isinstance(x, dict) and key in x: return x[key]
    return x if isinstance(x, list) else []

node_list = as_list(nodes_raw, "nodes")
edge_list = as_list(edges_raw, "edges")

# Supplemental external_safe coverage stubs (Part 5). These files contain ONLY
# external_safe fields by construction and still pass the externalization gate.
_supp_nodes = load("supplemental-nodes.json")
if _supp_nodes:
    node_list = node_list + as_list(_supp_nodes, "nodes")
    print(f"Merged {len(as_list(_supp_nodes,'nodes'))} supplemental coverage-stub nodes")
_supp_edges = load("supplemental-edges.json")
if _supp_edges:
    edge_list = edge_list + as_list(_supp_edges, "edges")
    print(f"Merged {len(as_list(_supp_edges,'edges'))} supplemental edges")

# ---------- Retired fused-parent reference normalization ----------
# Manila/Cebu/Palawan, Okinawa/Yaeyama, Izu were de-fused into separately-anchored
# constituent cities. Any surviving edge/story/org reference to a retired fused parent
# is normalized to its PRIMARY constituent so narratives/relationships still resolve to
# a real, rendered pin. Applied at build time so it holds regardless of partition state.
RETIRED_REMAP = {
    "manila-cebu-palawan-philippines": "manila-philippines",
    "japan-okinawa-yaeyama": "okinawa-main-japan",
    "japan-izu-shimoda": "izu-peninsula-japan",
}
def _remap_id(v):
    return RETIRED_REMAP.get(v, v) if isinstance(v, str) else v
for _e in edge_list:
    for _k in ("source", "target", "from", "to", "a", "b", "from_id", "to_id"):
        if _k in _e:
            _e[_k] = _remap_id(_e[_k])
for _s in stories:
    if isinstance(_s, dict) and "city_id" in _s:
        _s["city_id"] = _remap_id(_s["city_id"])
for _o in as_list(orgs_raw, "orgs"):
    cp = _o.get("city_presence")
    if isinstance(cp, list):
        _o["city_presence"] = sorted({_remap_id(c) for c in cp})
_retired_norm = True

# ---------- Label shortening ----------
_COUNTRY_PREFIXES = {
    "Malaysia","Philippines","Vietnam","Thailand","Indonesia","Cambodia","Brunei",
    "Japan","Korea","South Korea","Taiwan","Turkey","Greece","Spain","Italy","Croatia",
    "UAE","Egypt","Oman","Qatar","Bahrain","Kuwait","Saudi Arabia","KSA","India",
    "Sri Lanka","Maldives","Seychelles","Mauritius",
}
def short_label(name, ntype):
    """Fix 4: never re-introduce country segment in shortName."""
    if not name: return name
    s = re.sub(r"\s*\([^)]*\)", "", name).strip()
    if " — " in s:
        head, tail = s.split(" — ", 1)
        first = re.split(r"\s*[+/,]\s*", tail)[0].strip()
        # If head is a bare country name, drop it
        if head.strip() in _COUNTRY_PREFIXES:
            return first or head
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

# ---------- Curated boarding-point wiring (slug -> external-partition city node id) ----------
# slug = boarding-point JSON filename stem (build tries "{slug}-boarding-points.json" then "{slug}.json")
BP_DIR = HERE / "boarding-points"
BP_CITY_MAP = {
    # --- batch 1-3: originally wired (15) ---
    "dubai": "dubai-uae", "abu-dhabi": "abu-dhabi-uae", "singapore": "singapore",
    "bali": "bali-indonesia", "phuket": "phuket-phang-nga-thailand",
    "red-sea-global": "red-sea-global-ksa", "bangkok": "bangkok-thailand",
    "hong-kong": "hong-kong", "doha": "doha-qatar", "jakarta": "jakarta-indonesia",
    "langkawi": "langkawi-malaysia", "male-maldives": "male-maldives",
    "muscat": "muscat-oman",
    "sharjah": "sharjah-uae",
    # --- Philippines: de-fused into real constituent cities (each own anchor) ---
    "manila-philippines": "manila-philippines", "cebu-philippines": "cebu-philippines",
    "palawan-philippines": "palawan-philippines", "boracay-philippines": "boracay-philippines",
    "siargao-philippines": "siargao-philippines",
    # --- net-new wiring (29): MENA / KSA / Oman / Bahrain ---
    "jeddah-ksa": "jeddah-ksa", "neom-sindalah-ksa": "neom-sindalah-ksa",
    "ras-al-khaimah-uae": "ras-al-khaimah-uae", "manama-bahrain": "manama-bahrain",
    "salalah-dhofar-oman": "salalah-dhofar-oman", "sharm-el-sheikh-egypt": "sharm-el-sheikh-egypt",
    # --- Turkey (factory market) ---
    "bodrum": "turkey-bodrum", "antalya": "turkey-antalya", "cesme-izmir": "turkey-cesme-izmir",
    # --- Thailand / Indonesia clusters ---
    "koh-samui-thailand": "koh-samui-thailand", "komodo-flores-indonesia": "komodo-flores-indonesia",
    "lombok-indonesia": "lombok-indonesia", "raja-ampat-indonesia": "raja-ampat-indonesia",
    # --- Korea ---
    "busan-geoje": "korea-busan-geoje", "jeju": "korea-jeju", "yeosu-tongyeong": "korea-yeosu-tongyeong",
    # --- Taiwan ---
    "kaohsiung-taiwan": "taiwan-kaohsiung", "penghu": "taiwan-penghu",
    # --- Malaysia ---
    "penang": "malaysia-penang", "desaru-coast": "malaysia-desaru-coast", "sabah-kk": "malaysia-sabah-kk",
    # --- Vietnam ---
    "da-nang-hoi-an": "vietnam-da-nang-hoi-an", "ha-long-bay": "vietnam-ha-long-bay",
    "phu-quoc": "vietnam-phu-quoc",
    # --- Cambodia ---
    "koh-rong-sihanoukville": "cambodia-koh-rong-sihanoukville",
    # --- Japan (Hokkaido + Setouchi stay single; Okinawa + Izu de-fused) ---
    "hokkaido-niseko": "japan-hokkaido-niseko", "setouchi": "japan-setouchi",
    "okinawa-main-japan": "okinawa-main-japan", "miyako-japan": "miyako-japan",
    "yaeyama-japan": "yaeyama-japan",
    "izu-islands-japan": "izu-islands-japan", "izu-peninsula-japan": "izu-peninsula-japan",
    # --- greenfield seed-then-validate batch (9): slug == node id ---
    "fujairah-uae": "fujairah-uae",
    "banda-maluku-indonesia": "banda-maluku-indonesia",
    "brunei-darussalam": "brunei-darussalam",
    "derawan-berau-east-kalimantan-indonesia": "derawan-berau-east-kalimantan-indonesia",
    "karimunjawa-central-java-indonesia": "karimunjawa-central-java-indonesia",
    "lake-toba-samosir-indonesia": "lake-toba-samosir-indonesia",
    "likupang-north-sulawesi-indonesia": "likupang-north-sulawesi-indonesia",
    "riau-islands-indonesia": "riau-islands-indonesia",
    "wakatobi-southeast-sulawesi-indonesia": "wakatobi-southeast-sulawesi-indonesia",
}

# ---- Promoted hubs: sub-cluster boarding points elevated to NAMED city-tier pins ----
# Mega-clusters (esp. the Philippines) bury marquee island hubs as tiny POI dots that all
# read as one pin. Promote the El Nido-class anchors to their own labelled pins. Keyed by
# (cluster slug -> [(match substring in BP name, shortName label, seed degree)]).
PROMOTED_HUBS = {
    # Philippines mega-cluster retired: Manila/Cebu/Palawan/Boracay/Siargao are now
    # real, separately-anchored city nodes (see BP_CITY_MAP). Within-island sub-hubs
    # (El Nido / Coron / Puerto Princesa / Bohol / Amanpulo) promote off their own city.
    "palawan-philippines": [
        ("El Nido Town", "El Nido", 6),
        ("Coron Town Pier", "Coron", 6),
        ("Puerto Princesa Port", "Puerto Princesa", 5),
        ("Amanpulo (Pamalican Island) jetty", "Amanpulo", 5),
    ],
    "cebu-philippines": [
        ("Tagbilaran City Tourist Pier", "Bohol / Panglao", 5),
    ],
    "abu-dhabi": [("Sir Bani Yas Anantara Jetty", "Sir Bani Yas", 5)],
    "muscat": [("Daymaniyat Islands Nature Reserve", "Daymaniyat", 4)],
}

def _promo_lookup(slug, nm):
    nml = (nm or "").lower()
    for match, short, deg in PROMOTED_HUBS.get(slug, []):
        if match.lower() in nml:
            return {"short": short, "degree": deg}
    return None

# ---- Marquee (always-on) cities: unclustered, always-labelled flagship brand pins ----
# These must never disappear into a cluster or lose label placement in dense waters
# (the Singapore-in-a-Riau-cluster problem). Rendered from a dedicated unclustered source.
PRIORITY_CITIES = {
    "singapore", "dubai-uae", "abu-dhabi-uae", "doha-qatar", "hong-kong",
    "bangkok-thailand", "jakarta-indonesia", "male-maldives", "muscat-oman",
    "jeddah-ksa", "manila-philippines", "phuket-phang-nga-thailand",
    "bali-indonesia",
}

# Clean marquee labels for verbose cluster nodes (sub-hubs now carry the detail).
CITY_SHORTNAME_OVERRIDE = {
    "japan-hokkaido-niseko": "Hokkaido",
    "male-maldives": "Malé",
}

def _bp_file(slug):
    fp = BP_DIR / f"{slug}-boarding-points.json"
    if not fp.exists(): fp = BP_DIR / f"{slug}.json"
    return fp if fp.exists() else None

# Pre-pass: country-split city nodes (turkey-bodrum, japan-setouchi, ...) have no coords
# upstream in the data spine. Give them a map anchor from their boarding-point JSON's
# city_anchor so the city pin renders. Source of truth stays the JSON; this is a derived view.
_anchored = 0
for _slug, _cid in BP_CITY_MAP.items():
    _n = node_by_id.get(_cid)
    if not _n or coords_of(_n): continue
    _fp = _bp_file(_slug)
    if not _fp: continue
    _anc = json.loads(_fp.read_text()).get("city_anchor")
    if isinstance(_anc, list) and len(_anc) == 2 and _anc[0] and _anc[1]:
        _n["coords"] = [_anc[0], _anc[1]]; _anchored += 1
if _anchored:
    print(f"Anchored {_anchored} split city nodes from boarding-point city_anchor")

# Fix 3 (v10): Hide country-shell anchors whose coords are inland / unrepresentative
# of a coastal market. Keep in node_by_id (for route resolution / panel backlink)
# but skip emitting a map feature. Routes to/from these resolve via harbour-overrides.
HIDE_ON_MAP = {"malaysia", "japan", "korea", "south-korea", "taiwan", "turkey", "vietnam", "cambodia"}
# Retired fused parents — de-fused into separately-anchored constituent cities.
# Kept in node_by_id for any legacy route resolution, but never drawn as a pin,
# and all their leftover __ sub-POIs are suppressed (they carried wrong near-parent coords).
RETIRED_FUSED_PARENTS = {
    "manila-cebu-palawan-philippines", "japan-okinawa-yaeyama", "japan-izu-shimoda",
}
HIDE_ON_MAP |= RETIRED_FUSED_PARENTS
# Tier-based label paint order — markets paint first so they win z-fights
TIER_SORT_KEY = {"city": 1, "locale": 3, "poi": 5}

features = []
for n in node_list:
    nid = n.get("id") or n.get("node_id") or ""
    if n.get("hide_on_map") or nid in HIDE_ON_MAP:
        continue
    c = coords_of(n)
    if not c: continue
    ntype = n.get("type", "unknown")
    full = n.get("name","")
    label = overrides.get(nid) or short_label(full, ntype)
    props = {k:v for k,v in n.items() if k not in ("coords","coord")}
    props["shortName"] = label
    props["fullName"]  = full
    props["tier_sort_key"] = TIER_SORT_KEY.get(ntype, 4)
    features.append({
        "type":"Feature",
        "geometry":{"type":"Point","coordinates":c},
        "properties":props,
    })

# ---------- Curated coastal boarding points (override locales+POIs for covered cities) ----------
# Non-boardable internal markers. Every boarding-point JSON carries navigation /
# strategy references ("X — cross-cluster pointer", "OUT OF SCOPE", "pitch-trap",
# cert-anchors, shipyard-partner pointers, counterparty pointers). These are NOT
# real boardable jetties and MUST be suppressed from the public atlas. Several also
# contain gate-blocked tokens (e.g. "counterparty"), so this is a leak backstop too.
BP_MARKER_RE = re.compile(
    r"\bpointer\b|cross-cluster|cross-border|cross-emirate|cross-strait|cross-bay|"
    r"cross-arc|cross-giga|cross-region|out of scope|pitch-trap|cert-anchor|"
    r"cert anchor|shipyard.partner|yard-partner|counterparty|\bproxy\b|placeholder|"
    r"factory-market|hq city|graveyard|out-of-anchor",
    re.I,
)

def _is_marker(nm):
    return bool(nm) and bool(BP_MARKER_RE.search(nm))

# Auto-derive a suppression bbox per covered city from its OWN curated boarding
# points (markers + hidden points excluded), padded slightly. Replaces the old
# hand-maintained BP_BBOX so new cities need zero manual tuning.
def _derive_bbox(slug):
    fp = _bp_file(slug)
    if not fp: return None
    pts = []
    for b in json.loads(fp.read_text()).get("boarding_points", []):
        if b.get("relevance") == "hide": continue
        if b.get("lng") is None or b.get("lat") is None: continue
        if _is_marker(b.get("name")): continue
        pts.append((b["lng"], b["lat"]))
    if not pts: return None
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    pad = 0.05
    return (min(xs)-pad, min(ys)-pad, max(xs)+pad, max(ys)+pad)

BP_BBOX = {}
for _slug, _cid in BP_CITY_MAP.items():
    _bb = _derive_bbox(_slug)
    if _bb: BP_BBOX[_cid] = _bb
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
# external_safe sanitizer for POI free-text (Part 1 + Part 2.2)
import sys as _sys
_sys.path.insert(0, str(HERE / "partition"))
from partition_filter import sanitize_text as _sanitize  # noqa
from partition_spec import EXCLUSION_RE as _EXCL  # noqa  (keep build in sync with gate)

def _gate_clean(s):
    """Return s only if it trips no externalization-gate pattern, else None.
    Used for pass-through fields (e.g. source URLs) that bypass the text sanitizer
    but can still embed gate tokens in path segments (e.g. '/gocek-exclusive')."""
    if not isinstance(s, str): return None
    for _rx in _EXCL:
        if _rx.search(s): return None
    return s

def _safe(v):
    if not isinstance(v, str): return v
    out, _ = _sanitize(v)
    return out or None

def _charging_status(v):
    """Map free-text charging_potential -> controlled enum (greenfield|retrofit|none)."""
    if not isinstance(v, str): return None
    t = v.lower()
    if "retrofit" in t: return "retrofit"
    if any(w in t for w in ("greenfield","new","build","install","design-in","window")): return "greenfield"
    if any(w in t for w in ("none","no charg","diesel","unavailable")): return "none"
    return "unknown"

bp_added = 0
bp_suppressed_internal = 0
_bp_conf_tally = {}
_bp_candidate = 0
for slug, city_id in BP_CITY_MAP.items():
    fp = BP_DIR / f"{slug}-boarding-points.json"
    if not fp.exists(): fp = BP_DIR / f"{slug}.json"
    if not fp.exists(): continue
    data = json.loads(fp.read_text())
    for bp in data.get("boarding_points", []):
        if bp.get("relevance") == "hide": continue
        if bp.get("lng") is None or bp.get("lat") is None: continue
        nm = (bp.get("name") or "")
        # suppress internal-marker POIs entirely
        if nm.startswith("_") or _is_marker(nm):
            bp_suppressed_internal += 1; continue
        op = bp.get("operator")
        if isinstance(op, str) and "[gap]" in op.lower(): op = None
        src = bp.get("source")
        if not (isinstance(src, str) and src.strip().lower().startswith("http")): src = None
        else: src = _gate_clean(src)  # drop URLs whose path embeds a gate token
        # ---- Part 6: derive atlas confidence from the conveyor cross-source verdict ----
        # The conveyor (validation_log / source_chain) is the authoritative provenance signal.
        # We PROMOTE medium -> high only where independent sources cross-agree, and we DEMOTE
        # conveyor-rejected POIs to candidate so unverified coords are never shipped as operational.
        cv    = (bp.get("confidence") or "").strip().lower()
        chain = bp.get("source_chain") or []
        vlog  = bp.get("validation_log") or []
        # cross-source agreement = name-token agreement OR a Google "agree" verdict
        # OR >=2 independent stages returning a coord match.
        n_match = sum(1 for e in vlog if isinstance(e, dict) and e.get("result") == "match")
        cross_source_agree = (
            "name_token_agreement" in chain
            or any(isinstance(e, dict) and e.get("result") == "agree" for e in vlog)
            or n_match >= 2
        )
        # Grading philosophy: these are hand-curated points that already cleared the
        # pre-write water-adjacency gate, so human curation is the FLOOR and the conveyor's
        # cross-source agreement is the PROMOTER (never a destroyer of hand-verified points).
        #   - conveyor 'high' OR independent cross-source agreement -> high
        #   - hand-sourced (has http source) -> med floor
        #   - neither sourced nor cross-agreed -> low
        # status stays 'operational' for sourced points; only points that are BOTH unsourced
        # AND conveyor-rejected are genuinely speculative -> candidate.
        if cv == "high" or cross_source_agree:
            conf, status = "high", "operational"
        elif src:
            conf, status = "med", "operational"
        elif cv == "rejected":
            conf, status = "low", "candidate"
        else:
            conf, status = "low", "operational"
        # provenance timestamp for the side panel
        cv_block = bp.get("conveyor_v2") or data.get("conveyor_v2") or {}
        last_enriched = (cv_block.get("ran") if isinstance(cv_block, dict) else None) or data.get("generated")
        _promo = _promo_lookup(slug, nm)
        _ftype = "city" if _promo else "poi"
        features.append({
            "type":"Feature",
            "geometry":{"type":"Point","coordinates":[bp["lng"], bp["lat"]]},
            "properties":{
                # Neutral, stable id: raw BP ids can embed strategy tokens
                # ("...-exclusive", "...-wedge") that trip the externalization gate.
                # Search/selection use the sanitized name, not the id.
                "id": "bp-" + __import__("hashlib").md5(
                    ((bp.get("id") or nm) + city_id).encode("utf-8")).hexdigest()[:10],
                "type":_ftype,
                "name": _safe(nm),
                "shortName": (_promo["short"] if _promo else _safe(nm)),
                "fullName": _safe(nm),
                "parent_city_id": city_id,
                "bp_type": bp.get("type"),
                "bp_type_label": BP_TYPE_LABELS.get(bp.get("type"), bp.get("type")),
                # bp_relevance (P0/P1/P2 posture) -> INTERNAL, not shipped
                "linked_locale": _safe(bp.get("linked_locale")),
                "operator": _safe(op),
                "capacity": _safe(bp.get("berths_or_capacity")),
                "charging_status": _charging_status(bp.get("charging_potential")),
                "source_url": src,
                "confidence": conf,
                "status": status,
                "last_enriched": last_enriched,
                # notes (free-text strategy) -> INTERNAL, not shipped
            },
        })
        if _promo:
            features[-1]["properties"]["degree"] = _promo["degree"]
            features[-1]["properties"]["promoted"] = 1
            features[-1]["properties"]["tier_sort_key"] = TIER_SORT_KEY.get("city", 0)
        bp_added += 1
        _bp_conf_tally[conf] = _bp_conf_tally.get(conf, 0) + 1
        if status == "candidate": _bp_candidate += 1
print(f"Injected {bp_added} curated boarding points across {len(BP_CITY_MAP)} cities "
      f"({bp_suppressed_internal} internal-marker POIs suppressed)")
print(f"  Part 6 conveyor-graded confidence: {_bp_conf_tally} | candidate(unverified)={_bp_candidate}")

# ---------- Global suppression: ghost locales / aspirational POIs / route-description nodes ----------
import re as _re
SUPPRESS_ID_TOKENS = (
    "cross-border", "cross-strait", "out-of-range", "out_of_range",
    "aspirational", "marquee", "-aspiration", "-quanta-lr-gateway",
    "-quanta-lr-inter-cluster", "-trans-archipelago", "-line-haul",
    # internal cross-file edge-resolution artifacts (never externally renderable)
    "file-owns-endpoint", "-owns-endpoint", "counterparty",
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
    # Drop leftover sub-POIs of retired fused parents (wrong near-parent coords).
    if any(nid.startswith(rp + "__") for rp in RETIRED_FUSED_PARENTS):
        return True
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

# ---- Marquee shortName overrides + always-on priority-city split ----
for f in by_type.get("city", []):
    nid = f["properties"].get("id")
    if nid in CITY_SHORTNAME_OVERRIDE:
        f["properties"]["shortName"] = CITY_SHORTNAME_OVERRIDE[nid]
_prio, _rest = [], []
for f in by_type.get("city", []):
    if f["properties"].get("id") in PRIORITY_CITIES:
        f["properties"]["priority"] = 1
        _prio.append(f)
    else:
        _rest.append(f)
by_type["city"] = _rest
by_type["priority_city"] = _prio
_n_promoted = sum(1 for f in _rest if f["properties"].get("promoted"))
print(f"Priority (always-on) marquee cities: {len(_prio)} | promoted named hubs in city tier: {_n_promoted}")

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

import sys
sys.path.insert(0, str(HERE))
try:
    from auto_waypoints import auto_waypoints as _auto_wp
except Exception as _e:
    print("auto_waypoints import failed:", _e)
    _auto_wp = lambda ca, cb: None

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

def _resolve_cross_border(nid: str):
    """If a node id looks like a cross-border placeholder POI (parent__othercity[-suffix]),
    return the real destination city node id when one exists."""
    if not nid or "__" not in nid: return None
    tail = nid.split("__", 1)[1]
    # strip common cross-border suffixes
    for suf in ("-cross-border","-cross-strait","-quanta-lr","-line-haul","-gateway","-corridor","-link","-hop"):
        if tail.endswith(suf): tail = tail[:-len(suf)]
    if tail in node_by_id and node_by_id[tail].get("type") == "city":
        return tail
    # try matching any city id that starts with tail
    for cid, cn in node_by_id.items():
        if cn.get("type") == "city" and (cid == tail or cid.startswith(tail + "-")):
            return cid
    return None

# ---- Sea-routing + land validation for ALL drawn edges (v12 land-crossing fix) ----
# Previously only the DERIVED intra-cluster spokes were sea-routed; the main data-spine
# edges fell back to a straight great_circle() with NO land avoidance whenever they were
# not in route-waypoints.json / auto_waypoints. Result: ~35% of routes crossed land
# (hub-radial 75%, cross-border 71%), some straight across whole landmasses. We now route
# every edge through the SAME SeaGrid A* + interior-land guard that intra_cluster_routes
# already uses, and drop (or flag) anything that still can't find a clean sea path.
try:
    from sea_router import SeaGrid as _SeaGrid
    from intra_cluster_routes import _arc_mid_land_nm as _arc_land_nm, _hav_nm as _hav
    from global_land_mask import globe as _globe
    _SEA_OK = True
except Exception as _e:
    print(f"[routing] sea-router/land-mask unavailable — edges NOT land-validated: {_e}")
    _SEA_OK = False

_LAND_THRESHOLD_KM = 2.0     # max interior land a drawn route may cross (matches qa_land_crossing.py)
_MAX_DETOUR        = 2.8     # reject implausible A* detours

def _densify_linear(seq):
    """Linear lng/lat interpolation between waypoints — matches the straight segments the
    sea-router validates (a spherical great-circle bows off that line onto coastlines)."""
    arc = []
    for i in range(len(seq) - 1):
        p, q = seq[i], seq[i + 1]
        leg_nm = _hav(p, q) if _SEA_OK else 30.0
        n = max(2, min(60, int(leg_nm / 0.6) + 1))
        seg = [[p[0] + (q[0] - p[0]) * k / n, p[1] + (q[1] - p[1]) * k / n] for k in range(n + 1)]
        arc.extend(seg[1:] if i else seg)
    return arc

def _arc_land_km(arc):
    return (_arc_land_nm(arc) * 1.852) if _SEA_OK else 0.0

def _is_sea_endpoint(c, r_nm=3.0):
    """A real coastal jetty has open water within a few nm; an inland/lake node does not.
    Filters meaningless 'sea routes' to inland nodes (e.g. lake-toba-samosir on Sumatra)."""
    if not _SEA_OK:
        return True
    import math as _m
    for ang in range(0, 360, 30):
        dx = (r_nm / 60.0) * _m.cos(_m.radians(ang))
        dy = (r_nm / 60.0) * _m.sin(_m.radians(ang))
        if not bool(_globe.is_land(c[1] + dy, c[0] + dx)):
            return True
    return False

_sea_grid_cache = {}
def _sea_route_arc(ca, cb, hand_waypoints):
    """Land-avoiding, validated polyline ca->cb. Returns (arc, ok); ok=False => no clean
    sea path (caller should drop or flag the edge rather than draw a land-crosser)."""
    if not _SEA_OK:
        # No land mask available: preserve previous behaviour (hand waypoints else straight).
        if hand_waypoints:
            seq = [ca] + list(hand_waypoints) + [cb]; arc = []
            for i in range(len(seq) - 1):
                seg = great_circle(seq[i][0], seq[i][1], seq[i+1][0], seq[i+1][1], n=12)
                arc.extend(seg[1:] if i else seg)
            return arc, True
        return great_circle(ca[0], ca[1], cb[0], cb[1], n=24), True
    # --- Cheap-first short-circuit (perf): validate candidates that need NO A* before
    # paying for grid construction + A* search. Most open-ocean long-haul legs are already
    # clean, so this avoids building a SeaGrid for the vast majority of edges. Only genuine
    # land-crossers fall through to the expensive A* path below.
    # 1) curated hand waypoints (preferred corridor) — validate, accept if clean
    if hand_waypoints:
        arc = _densify_linear([ca] + list(hand_waypoints) + [cb])
        if _arc_land_km(arc) <= _LAND_THRESHOLD_KM:
            return arc, True
    # 2) straight line — accept if it already crosses no significant land
    straight = _densify_linear([ca, cb])
    if _arc_land_km(straight) <= _LAND_THRESHOLD_KM:
        return straight, True
    # 3) Edge crosses land. For very large bboxes a doomed cross-landmass hop (e.g. across
    # Sumatra / Indochina / Yemen) would force a full-grid A* that can only fail — skip it
    # and drop the edge rather than burning the time.
    span = max(abs(ca[0] - cb[0]), abs(ca[1] - cb[1]))
    _SPAN_CAP = 7.0
    if span > _SPAN_CAP:
        return straight, False
    # 4) A* sea route around land (one SeaGrid per coarse bbox, cached & reused per region)
    key = (round(min(ca[0], cb[0]), 1), round(min(ca[1], cb[1]), 1),
           round(max(ca[0], cb[0]), 1), round(max(ca[1], cb[1]), 1))
    grid = _sea_grid_cache.get(key)
    if grid is None:
        try:
            grid = _SeaGrid(min(ca[0], cb[0]), min(ca[1], cb[1]), max(ca[0], cb[0]), max(ca[1], cb[1]))
        except Exception:
            grid = False
        _sea_grid_cache[key] = grid
    if grid:
        sea_wp = grid.route(tuple(ca), tuple(cb), max_detour=_MAX_DETOUR)
        if sea_wp is not None:
            arc = _densify_linear([ca] + list(sea_wp) + [cb])
            if _arc_land_km(arc) <= _LAND_THRESHOLD_KM:
                return arc, True
    # no clean sea path found
    return straight, False

# Fix 6 (v10): Drop edges that would cross significant landmass even with waypoints,
# and where no operational corridor exists. Pair-set is order-insensitive.
DROP_EDGE_PAIRS = {
    frozenset(["langkawi-malaysia", "koh-samui-thailand"]),   # crosses Kra Isthmus
}
# ---- Demand-model route network (route_network.py) owns these markets' intra-market edges ----
# For the marquee markets we replace the sparse centroid/locale data-spine edges with a dense,
# demand-weighted BP-graph network. Intra-managed-market data-spine edges are skipped here so the
# two layers don't double-draw; cross-market long-hauls (e.g. Dubai<->Muscat) still come from the
# data spine. See route-demand-config.json + reference/route-demand-model.md.
MANAGED_SLUGS = [
    "dubai", "abu-dhabi", "sharjah", "ras-al-khaimah-uae", "fujairah-uae",
    "singapore", "riau-islands-indonesia", "desaru-coast",
    "bali", "lombok-indonesia", "phuket", "langkawi",
    # hero-chain hubs (Andaman + Lesser Sunda) — route_network owns their mesh + chain
    "penang", "komodo-flores-indonesia",
]
MANAGED_OWNERS = set()
for _s in MANAGED_SLUGS:
    _nid = BP_CITY_MAP.get(_s)
    if _nid:
        MANAGED_OWNERS.add(_nid); MANAGED_OWNERS.add(_nid.split("__")[0])
    MANAGED_OWNERS.add(_s)
MANAGED_OWNERS.update({
    "dubai", "abu-dhabi", "sharjah", "ras-al-khaimah", "fujairah", "bali", "lombok",
    "phuket", "langkawi", "singapore", "riau-islands-indonesia", "desaru-coast", "riau",
})
def _owning(nid):
    return (nid or "").split("__")[0]
# Country-level shell nodes (centroids of a whole country) must never be a route
# endpoint — they produce "Phuket -> malaysia" / "vietnam -> Da Nang" nonsense lines.
COUNTRY_SHELL_IDS = {
    "japan", "taiwan", "vietnam", "malaysia", "korea", "indonesia", "philippines",
    "thailand", "china", "india", "cambodia", "oman", "brunei", "laos", "myanmar",
}
PIONEER_MAX_NM = 70.0      # N30 Pioneer II all-electric ceiling
QUANTA_MAX_NM  = 2000.0    # N30 Quanta-LR hybrid ceiling
def _arc_nm(arc):
    return sum(_hav(arc[i], arc[i + 1]) for i in range(len(arc) - 1)) if _SEA_OK and arc and len(arc) > 1 else 0.0
_dropped_land_crossings = 0
_dropped_inland = 0
_remap_count = 0
_dropped_managed = 0
_dropped_shell = 0
_dropped_overrange = 0
_platform_upgraded = 0
_platform_downgraded = 0
route_features = []
for e in edge_list:
    fnid = e.get("from_node_id"); tnid = e.get("to_node_id")
    if frozenset([fnid, tnid]) in DROP_EDGE_PAIRS:
        _dropped_land_crossings += 1
        continue
    # Never draw a route to/from a country-shell centroid node.
    if _owning(fnid) in COUNTRY_SHELL_IDS or _owning(tnid) in COUNTRY_SHELL_IDS \
       or fnid in COUNTRY_SHELL_IDS or tnid in COUNTRY_SHELL_IDS:
        _dropped_shell += 1
        continue
    # Skip intra-managed-market edges — route_network.py owns these (dense demand network).
    if _owning(fnid) in MANAGED_OWNERS and _owning(tnid) in MANAGED_OWNERS:
        _dropped_managed += 1
        continue
    # Remap placeholder cross-border POIs to the real destination city node
    rf = _resolve_cross_border(fnid)
    if rf and rf != fnid: fnid = rf; _remap_count += 1
    rt = _resolve_cross_border(tnid)
    if rt and rt != tnid: tnid = rt; _remap_count += 1
    a = node_by_id.get(fnid)
    b = node_by_id.get(tnid)
    if not a or not b: continue
    # drop edges whose endpoint is an internal resolution artifact / suppressed node
    if _should_suppress(a) or _should_suppress(b): continue
    ca, cb = origin_coords(a), origin_coords(b)
    if not ca or not cb: continue
    plat = (e.get("platform") or "").strip()
    if plat not in ("Pioneer II","Quanta-LR"): continue
    # Inland / lake endpoint guard: a "sea route" to a non-coastal node is meaningless
    # (this is what produced the 1,500 km lake-toba-samosir crosser across Sumatra).
    if not (_is_sea_endpoint(ca) and _is_sea_endpoint(cb)):
        _dropped_inland += 1
        continue
    # Curated hand waypoints (preferred), else geography-rule auto waypoints — then the
    # general sea-router validates/repairs, identical to the intra-cluster spoke path.
    hand_wp = route_waypoints.get((a.get("id"), b.get("id"))) or _auto_wp(ca, cb)
    arc, ok = _sea_route_arc(ca, cb, hand_wp)
    if not ok:
        # No clean sea path even via A* -> do not draw a land-crosser.
        _dropped_land_crossings += 1
        continue
        # Alternative (keep for audit instead of dropping): set render_hidden=True in the
        # properties below and DO NOT `continue`; the front-end will suppress it from view.
    # Range / platform gate on the REAL routed arc (not the stale stored distance):
    # Pioneer II tops out at 70 nm; anything longer must be Quanta-LR; beyond 2,000 nm
    # is beyond even Quanta-LR and must not be drawn (this kills the Pioneer-II-@-430 nm
    # and 830 nm phantoms).
    real_nm = round(_arc_nm(arc), 1)
    if real_nm and real_nm > QUANTA_MAX_NM:
        _dropped_overrange += 1
        continue
    if real_nm and real_nm > PIONEER_MAX_NM and plat == "Pioneer II":
        plat = "Quanta-LR"; _platform_upgraded += 1
    # Rule A (QLR curation): curated edges within all-electric range are Pioneer II,
    # even if the spine marked them Quanta-LR. Quanta-LR is reserved for >70 nm long-haul.
    if real_nm and real_nm <= PIONEER_MAX_NM and plat == "Quanta-LR":
        plat = "Pioneer II"; _platform_downgraded += 1
    route_features.append({
        "type":"Feature",
        "geometry":{"type":"LineString","coordinates":arc},
        "properties":{
            "id": e.get("id"),
            "platform": plat,
            "distance_nm": real_nm or e.get("distance_nm"),
            "edge_class": e.get("edge_class"),
            "from": e.get("from_node_id"),
            "to":   e.get("to_node_id"),
        },
    })

print(f"Cross-border edge remaps applied: {_remap_count}")
print(f"Dropped land-crossing edges: {_dropped_land_crossings}")
print(f"Dropped inland/non-sea-endpoint edges: {_dropped_inland}")
print(f"Dropped intra-managed-market edges (route_network owns): {_dropped_managed}")
print(f"Dropped country-shell-endpoint edges: {_dropped_shell}")
print(f"Dropped beyond-Quanta-range edges: {_dropped_overrange}")
print(f"Platform upgraded Pioneer II -> Quanta-LR (range): {_platform_upgraded}")
print(f"Platform downgraded Quanta-LR -> Pioneer II (Rule A <=70nm): {_platform_downgraded}")

# ---- Derived intra-cluster hub-radial-spoke routes (split nodes) ----
# Country-split nodes were anchored but had no routes (curated edges reference the
# long-form parent-cluster ids). Derive island-hopping spokes from each cluster's
# curated, water-validated boarding points. Only for covered cities that currently
# render ZERO routes, so hand-curated clusters (e.g. Hong Kong) are never disturbed.
try:
    import intra_cluster_routes as _icr
    # Split (country-shell) nodes ALWAYS get their intra-cluster island-hopping
    # network, even if a single national-hub curated spoke already touches them —
    # one hub spoke is not an island-hopping network, and some (e.g. penghu) only
    # have a dangling phantom-endpoint edge.
    _SPLIT_SLUGS = {
        "setouchi", "okinawa-yaeyama", "hokkaido-niseko", "izu-shimoda",
        "jeju", "busan-geoje", "yeosu-tongyeong", "penghu", "kaohsiung-taiwan",
        "bodrum", "antalya", "cesme-izmir", "koh-rong-sihanoukville",
        "penang", "desaru-coast", "sabah-kk", "phu-quoc", "ha-long-bay",
        "da-nang-hoi-an",
    }
    _routed_cids = set()
    for _rf in route_features:
        _routed_cids.add(_rf["properties"].get("from"))
        _routed_cids.add(_rf["properties"].get("to"))
    _icr_targets = []
    for _slug, _cid in BP_CITY_MAP.items():
        if _slug in MANAGED_SLUGS:
            continue   # route_network.py owns the marquee markets' intra-cluster network
        if _cid in _routed_cids and _slug not in _SPLIT_SLUGS:
            continue
        _node = node_by_id.get(_cid)
        _cname = (_node.get("name") if _node else None) or _cid
        _icr_targets.append({"slug": _slug, "city_id": _cid, "anchor": None,
                             "city_name": _cname})
    _icr_feats, _icr_stats = _icr.generate(
        bp_dir=(HERE / "boarding-points"),
        targets=_icr_targets,
        great_circle=great_circle,
        auto_wp=_auto_wp,
        is_marker=_is_marker,
        sanitize=_sanitize,
    )
    route_features.extend(_icr_feats)
    print(f"Intra-cluster spokes: +{_icr_stats['spokes']} across "
          f"{_icr_stats['clusters']} clusters "
          f"(Pioneer II={_icr_stats['pioneer']} Quanta-LR={_icr_stats['quanta']}; "
          f"dropped land={_icr_stats['dropped_land']} foreign={_icr_stats['dropped_foreign']} "
          f"range={_icr_stats['dropped_range']} deduped={_icr_stats['deduped']})")
except Exception as _e:
    print(f"[intra-cluster] WARNING: spoke generation skipped ({_e})")

# ---- Demand-weighted layered route network for marquee markets (route_network.py) ----
# Builds local BP<->BP mesh + regional + trunk corridors ON the curated boarding-point graph,
# with traffic_weight from the demand model. Endpoints land on real BP coords (front-end's
# geometric on_route tagging + terminus nodes connect the pins), from/to are real node ids.
try:
    import route_network as _rn
    # ---- route-network geometry cache (the A* sea-routing is the slow step) ----
    # Cache key = route_network.py source + demand config + every managed BP file.
    # Unchanged inputs -> reuse cached geometry (seconds instead of minutes).
    # Set RN_NO_CACHE=1 to force a fresh regeneration.
    import hashlib as _hl
    _ck = _hl.sha256()
    _ck.update((HERE / "route_network.py").read_bytes())
    _ck.update((HERE / "route-demand-config.json").read_bytes())
    _cfg_tmp = json.loads((HERE / "route-demand-config.json").read_text())
    _managed_for_cache = sorted({s for m in _cfg_tmp["markets"].values() for s in m["clusters"]})
    for _s in _managed_for_cache:
        _fp = _bp_file(_s)
        if _fp:
            _ck.update(_fp.read_bytes())
    # CACHE-POISON FIX: also hash every input that can change route geometry after a
    # cluster split (supplemental nodes/edges, harbour overrides, waypoints). Previously
    # only BP files + config were hashed, so a split touching these left a stale cache
    # carrying pre-split geometry (the 500+ land-crossing trap). Now any such change
    # auto-invalidates the cache — no manual `.rn_cache.json` deletion ever needed.
    for _extra in ("supplemental-nodes.json", "supplemental-edges.json",
                   "harbour-overrides.json", "route-waypoints.json", "label-overrides.json"):
        _efp = HERE / _extra
        if _efp.exists():
            _ck.update(_efp.read_bytes())
    _cache_key = _ck.hexdigest()[:16]
    _cache_fp = HERE / ".rn_cache.json"
    _rn_feats = _rn_stats = None
    if os.environ.get("RN_NO_CACHE") != "1" and _cache_fp.exists():
        try:
            _cached = json.loads(_cache_fp.read_text())
            if _cached.get("key") == _cache_key:
                _rn_feats, _rn_stats = _cached["features"], _cached["stats"]
                print(f"Route-network: CACHE HIT ({_cache_key}) — reusing {len(_rn_feats)} edges (no A* regen)")
        except Exception:
            _rn_feats = None
    if _rn_feats is None:
        _rn_feats, _rn_stats = _rn.generate(
            bp_dir=(HERE / "boarding-points"),
            config_path=str(HERE / "route-demand-config.json"),
            bp_city_map=BP_CITY_MAP,
            is_marker=_is_marker,
            sanitize=_sanitize,
        )
        try:
            _cache_fp.write_text(json.dumps({"key": _cache_key, "features": _rn_feats, "stats": _rn_stats}))
            print(f"Route-network: cache WRITE ({_cache_key})")
        except Exception as _ce:
            print(f"Route-network: cache write skipped ({_ce})")
    route_features.extend(_rn_feats)
    print(f"Route-network (demand model): +{len(_rn_feats)} edges "
          f"(local={_rn_stats['local']} regional={_rn_stats.get('regional',0)} "
          f"trunk={_rn_stats.get('trunk',0)}; dropped_land={_rn_stats['dropped_land']} "
          f"corridors_dropped={_rn_stats['corridors_dropped']}) "
          f"across {_rn_stats['clusters']} clusters")
except Exception as _e:
    import traceback; traceback.print_exc()
    print(f"[route-network] WARNING: skipped ({_e})")

# ---- Clean human endpoint labels for every route + Quanta-LR endpoint audit ----
# Resolves from/to ids -> readable names (never raw `__` slugs), tags parent city so a
# route always reads City -> City, and audits Quanta-LR endpoints for one-by-one curation.
try:
    import route_labels as _rl
    _route_audit = _rl.apply_labels(route_features, node_by_id, HERE / "boarding-points", BP_CITY_MAP)
    (HERE / "route_label_audit.json").write_text(json.dumps(_route_audit, indent=2, ensure_ascii=False))
    print(f"Route labels applied to {_route_audit['total']} routes; "
          f"Quanta-LR={_route_audit['qlr_total']} "
          f"(non-city-endpoint={len(_route_audit['qlr_noncity_endpoint'])}, "
          f"<=Pioneer-range={len(_route_audit['qlr_under_pioneer'])}, "
          f"unresolved-labels={len(_route_audit['unresolved'])})")
except Exception as _e:
    import traceback; traceback.print_exc()
    print(f"[route-labels] WARNING: skipped ({_e})")

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
#map { position:absolute; top:0; bottom:0; left:0; right:420px; background:var(--bg-0); transition:right 0.32s cubic-bezier(.4,0,.2,1); }
/* Fix 1 (v10): when side panel is collapsed, map fills the viewport */
body.panel-hidden #map { right:0 !important; }
body.panel-hidden #panel { width:0 !important; }
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

/* Layer toggles (right of presets) — Fix 7 (v10): per-toggle distinct color, filled-vs-outlined on/off */
#toggles { position:absolute; bottom:24px; left:50%; transform:translateX(-50%); z-index:10; display:flex; gap:6px; }
.toggle { background:rgba(17,22,30,0.86); backdrop-filter:blur(20px); border:1.5px solid var(--line-strong); color:var(--text-2); font:500 11px Inter; padding:7px 12px; border-radius:999px; cursor:pointer; letter-spacing:0.02em; transition:background 0.18s, color 0.18s, border-color 0.18s; }
.toggle::before { content:'○ '; opacity:0.6; }
.toggle.on::before { content:'● '; opacity:1; }
/* Routes — white */
#t-routes.on { background:rgba(255,255,255,0.18); color:#ffffff; border-color:rgba(255,255,255,0.55); }
/* Pioneer II — cyan/mint */
#t-p2.on     { background:rgba(110,231,183,0.20); color:#6ee7b7; border-color:rgba(110,231,183,0.55); }
/* Quanta-LR — steel/amber per spec → amber */
#t-qlr.on    { background:rgba(251,191,36,0.20); color:#fbbf24; border-color:rgba(251,191,36,0.55); }
/* Areas — coral (matches the coral area markers + header stat) */
#t-locales.on{ background:rgba(251,113,133,0.18); color:#fb7185; border-color:rgba(251,113,133,0.55); }
/* Boarding pts — steel (matches the dominant marina glyph + header stat) */
#t-pois.on   { background:rgba(96,165,250,0.18); color:#60a5fa; border-color:rgba(96,165,250,0.55); }

/* Legend */
#legend { position:absolute; bottom:24px; left:24px; z-index:10; background:rgba(17,22,30,0.86); backdrop-filter:blur(20px); border:1px solid var(--line-strong); border-radius:12px; padding:11px 14px; font-size:11px; color:var(--text-1); }
#legend .head { font-size:9px; text-transform:uppercase; letter-spacing:0.12em; color:var(--text-2); font-weight:600; margin-bottom:6px; }
#legend .sub { font-size:8.5px; text-transform:uppercase; letter-spacing:0.13em; color:var(--text-2); font-weight:600; opacity:0.75; margin:10px 0 4px; padding-top:8px; border-top:1px solid var(--line); }
#legend .row { display:flex; align-items:center; gap:8px; padding:2px 0; }
#legend .dot { width:9px; height:9px; border-radius:50%; box-shadow:0 0 8px currentColor; }
#legend .dot.city   { background:#6ee7b7; color:#6ee7b7; }
#legend .dot.locale { background:#fb7185; color:#fb7185; }
#legend .dot.bp.marina    { background:#60a5fa; color:#60a5fa; }
#legend .dot.bp.ferry     { background:#fb7185; color:#fb7185; }
#legend .dot.bp.yacht     { background:#fbbf24; color:#fbbf24; }
#legend .dot.bp.hotel     { background:#6ee7b7; color:#6ee7b7; }
#legend .dot.bp.seaplane  { background:#a78bfa; color:#a78bfa; }
#legend .dot.bp.watertaxi { background:#22d3ee; color:#22d3ee; }
#legend .dot.bp.harbour   { background:#94a3b8; color:#94a3b8; }
#legend .gly { display:inline-block; width:14px; text-align:center; font-family:'Noto Sans','Inter',sans-serif; font-weight:700; font-size:14px; text-shadow:0 0 6px currentColor; }
#legend .muted { color:var(--text-2); font-size:10px; }
#legend .line { width:18px; height:0; border-top:2px solid var(--accent); }
#legend .line.qlr { border-top:2px dashed var(--gold); }
#legend .help { display:inline-flex; align-items:center; justify-content:center; width:14px; height:14px; border-radius:50%; background:var(--bg-3); color:var(--text-1); font-size:9px; font-weight:700; cursor:help; margin-left:6px; position:relative; }
#legend .help:hover::after { content:attr(data-tip); position:absolute; bottom:calc(100% + 6px); left:0; width:260px; background:rgba(10,14,20,0.97); border:1px solid var(--line-strong); border-radius:8px; padding:10px 12px; font:400 11px Inter; color:var(--text-0); line-height:1.5; text-transform:none; letter-spacing:0; z-index:30; box-shadow:0 8px 24px rgba(0,0,0,0.5); }

/* Footer — moved to top-right above panel so it stops eating clicks */
#footer { position:absolute; top:18px; right:444px; z-index:10; font-size:10px; color:var(--text-2); letter-spacing:0.12em; text-transform:uppercase; background:rgba(17,22,30,0.6); padding:6px 12px; border-radius:6px; border:1px solid var(--line); pointer-events:none; transition:right 0.32s cubic-bezier(.4,0,.2,1); }
body.panel-hidden #footer { right:24px; }

/* Side panel + collapse */
#panel { position:absolute; top:0; right:0; bottom:0; width:420px; background:var(--bg-1); border-left:1px solid var(--line-strong); overflow-y:auto; transition:transform 0.32s cubic-bezier(.4,0,.2,1); }
body.panel-hidden #panel { transform:translateX(100%); }
#panel-toggle { position:absolute; top:50%; right:420px; transform:translateY(-50%); z-index:11; width:24px; height:48px; border-radius:6px 0 0 6px; background:rgba(17,22,30,0.92); backdrop-filter:blur(20px); border:1px solid var(--line-strong); border-right:none; color:var(--text-1); display:flex; align-items:center; justify-content:center; cursor:pointer; font-size:14px; transition:right 0.32s cubic-bezier(.4,0,.2,1); }
#panel-toggle:hover { color:var(--accent); }
body.panel-hidden #panel-toggle { right:0; border-radius:6px 0 0 6px; }
#presets { transition:max-width 0.32s; }
body.panel-hidden #presets { max-width:calc(100vw - 420px - 40px); }
/* Pull legend up so it doesn't sit under the toggle row */
body.panel-hidden #footer { display:block; }
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

.story-partnerview { padding:18px 28px; border-bottom:1px solid var(--line); background:linear-gradient(135deg,rgba(110,231,183,0.06),transparent); }
.story-partnerview h3 { font-size:10px; text-transform:uppercase; letter-spacing:0.12em; color:var(--accent); margin:0 0 10px; }
.story-partnerview .body { font-size:13px; line-height:1.6; color:var(--text-0); }
.story-partnerview .cta { margin-top:12px; font-size:12px; font-weight:600; color:var(--accent); padding:10px 14px; background:rgba(110,231,183,0.10); border:1px solid rgba(110,231,183,0.28); border-radius:9px; }
.story-vessels { padding:18px 28px; border-bottom:1px solid var(--line); }
.story-vessels h3 { font-size:10px; text-transform:uppercase; letter-spacing:0.12em; color:var(--text-2); margin:0 0 10px; }
.story-vessels .vessel { margin-bottom:12px; }
.story-vessels .vname { font-size:13px; font-weight:600; color:var(--text-0); }
.story-vessels .vmeta { font-size:11px; color:var(--text-1); margin-top:2px; }
.story-vessels .vmeta.dim { color:var(--text-2); }
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
/* Glassmorphic route hover popup */
.route-popup .maplibregl-popup-content { background:rgba(17,22,30,0.92) !important; backdrop-filter:blur(20px) saturate(140%); border:1px solid var(--line-strong); border-radius:10px; padding:8px 12px !important; box-shadow:0 8px 24px rgba(0,0,0,0.45); }
.route-popup .maplibregl-popup-tip { display:none; }
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
    <div class="stat accent"><span class="v" id="stat-cities">61</span><span class="k">Cities</span></div>
    <div class="stat coral"><span class="v" id="stat-areas">67</span><span class="k">Areas</span></div>
    <div class="stat steel"><span class="v" id="stat-bps">1870</span><span class="k">Boarding pts</span></div>
    <div class="stat gold"><span class="v" id="stat-routes">467</span><span class="k">Routes</span></div>
  </div>
</div>

<div id="searchwrap">
  <input id="search" placeholder="Search cities, areas, boarding points…" autocomplete="off" />
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
  <button class="toggle on" id="t-qlr">Quanta-LR</button>
  <button class="toggle on" id="t-locales" title="Sub-areas / districts / island groups inside a city cluster (e.g. Palm Jumeirah inside Dubai)">Areas</button>
  <button class="toggle on" id="t-pois" title="Boarding points: marinas, ferry terminals, hotel jetties, water-taxi stops">Boarding pts</button>
</div>

<!-- Fix 5 (v10): legend glyphs match map symbol-layer (Noto Sans-safe Unicode) -->
<div id="legend">
  <div class="head">Map key <span class="help" data-tip="Cities = whole markets. Areas = sub-districts/islands inside a city. Boarding points = real coastal pickup spots; glyphs match those drawn on the map.">?</span></div>
  <div class="row"><span class="dot city"></span>City <span class="muted">— market</span></div>
  <div class="row"><span class="dot locale"></span>Area <span class="muted">— sub-district</span></div>
  <div class="sub">Boarding points</div>
  <div class="row"><span class="gly" style="color:#60a5fa">⚓</span>Marina / working harbour</div>
  <div class="row"><span class="gly" style="color:#fb7185">▲</span>Ferry / cruise terminal</div>
  <div class="row"><span class="gly" style="color:#fbbf24">★</span>Yacht club</div>
  <div class="row"><span class="gly" style="color:#6ee7b7">■</span>Hotel / resort jetty</div>
  <div class="row"><span class="gly" style="color:#a78bfa">✦</span>Seaplane base</div>
  <div class="row"><span class="gly" style="color:#22d3ee">◆</span>Water taxi / abra / public pier</div>
  <div class="row"><span class="gly" style="color:#cbd5e1">⬢</span>MRO / shipyard</div>
  <div class="row"><span class="gly" style="color:#fde68a">⬟</span>Refuel mid-node</div>
  <div class="sub">Platforms</div>
  <div class="row"><span class="line"></span>Pioneer II <span class="muted">— ≤70 nm electric</span></div>
  <div class="row"><span class="line qlr"></span>Quanta-LR <span class="muted">— ≤2,000 nm hybrid</span></div>
</div>

<div id="footer">Navier Mobility · 2026</div>

<button id="panel-toggle" title="Show / hide side panel">‹</button>
<div id="panel"><div class="panel-empty">
  <h2>Select a node</h2>
  <p>Cities cluster at world view. Zoom in to reveal areas and boarding points.</p>
  <div class="hint"><div class="hint-num">1</div><div>Use <b>Stories ▾</b> to walk a partner pitch.</div></div>
  <div class="hint"><div class="hint-num">2</div><div>Search or use preset chips to fly to a market.</div></div>
  <div class="hint"><div class="hint-num">3</div><div>Click any node for context and range rings.</div></div>
  <div class="hint"><div class="hint-num">4</div><div>Hide this panel with the <b>‹</b> tab on its edge to give the map full width.</div></div>
</div></div>

<script>
const FEATURES_BY_TYPE = __FEATURES__;
const ROUTES = __ROUTES__;
const STORIES = __STORIES__;
const VESSEL_SPECS = __VESSELS__;
const NODE_INDEX = {}; // id -> {coords, props}
for (const t of Object.keys(FEATURES_BY_TYPE)) for (const f of FEATURES_BY_TYPE[t]) { const p=f.properties; if (p.id) NODE_INDEX[p.id]={coords:f.geometry.coordinates, props:p}; }

// ============ Route geometry: land-safe smoothing + zoom hierarchy (v11, Item 1) ============
// The upstream pipeline land-validates each route as a chain of STRAIGHT segments and
// warns that a great-circle "bows off that line and can drift onto a coast". So we smooth
// without ever leaving the validated corridor: recover the structural waypoints (RDP),
// fit a Catmull-Rom curve through them, then CLAMP every interpolated sample so it cannot
// deviate from the validated polyline by more than a small, segment-scaled amount. Open-sea
// bends round elegantly; tight archipelago dog-legs barely move (cap shrinks with segment len).
// If Tasklet supplies a pre-smoothed, land-validated path in properties.geometry_smooth
// (array of [lng,lat]) we render it verbatim and skip client smoothing. Setting
// properties.render_smooth === false opts a single route out of client smoothing entirely.
const LONGHAUL_EDGE = new Set(['cross-border-radial','refuel-mid-node-leg']);
function _isLonghaul(p){ return (p.distance_nm!=null && p.distance_nm>=120) || LONGHAUL_EDGE.has(p.edge_class); }
function _perpDist(p,a,b){
  const dx=b[0]-a[0], dy=b[1]-a[1], L2=dx*dx+dy*dy;
  if (!L2) return Math.hypot(p[0]-a[0],p[1]-a[1]);
  let t=((p[0]-a[0])*dx+(p[1]-a[1])*dy)/L2; t=t<0?0:t>1?1:t;
  return Math.hypot(p[0]-(a[0]+t*dx), p[1]-(a[1]+t*dy));
}
function _rdp(pts,eps){ // Douglas-Peucker: collapse collinear fill, keep structural waypoints
  if (pts.length<3) return pts.slice();
  const keep=new Array(pts.length).fill(false); keep[0]=keep[pts.length-1]=true;
  const stack=[[0,pts.length-1]];
  while(stack.length){
    const [s,e]=stack.pop(); let idx=-1,dmax=0;
    for(let i=s+1;i<e;i++){ const d=_perpDist(pts[i],pts[s],pts[e]); if(d>dmax){dmax=d;idx=i;} }
    if(dmax>eps && idx>-1){ keep[idx]=true; stack.push([s,idx],[idx,e]); }
  }
  const out=[]; for(let i=0;i<pts.length;i++) if(keep[i]) out.push(pts[i]);
  return out;
}
function _clampCorridor(pt,knots,ki,cap){ // pull sample back onto the validated corridor
  let best=Infinity,bx=pt[0],by=pt[1];
  for(let j=Math.max(0,ki-1);j<=Math.min(knots.length-2,ki+1);j++){
    const a=knots[j],b=knots[j+1],dx=b[0]-a[0],dy=b[1]-a[1],L2=dx*dx+dy*dy;
    let t=L2?(((pt[0]-a[0])*dx+(pt[1]-a[1])*dy)/L2):0; t=t<0?0:t>1?1:t;
    const px=a[0]+t*dx, py=a[1]+t*dy, d=Math.hypot(pt[0]-px,pt[1]-py);
    if(d<best){best=d;bx=px;by=py;}
  }
  if(best<=cap) return pt;
  const k=cap/best; return [bx+(pt[0]-bx)*k, by+(pt[1]-by)*k];
}
function _catmull(knots,opt){
  if (knots.length<3) return knots.slice();
  const P=[knots[0],...knots,knots[knots.length-1]], out=[knots[0]];
  for(let i=1;i<P.length-2;i++){
    const p0=P[i-1],p1=P[i],p2=P[i+1],p3=P[i+2];
    const cap=Math.min(opt.absCap, opt.devFactor*Math.hypot(p2[0]-p1[0],p2[1]-p1[1])), ki=i-1;
    for(let s=1;s<=opt.samples;s++){
      const t=s/opt.samples, t2=t*t, t3=t2*t;
      const x=0.5*(2*p1[0]+(-p0[0]+p2[0])*t+(2*p0[0]-5*p1[0]+4*p2[0]-p3[0])*t2+(-p0[0]+3*p1[0]-3*p2[0]+p3[0])*t3);
      const y=0.5*(2*p1[1]+(-p0[1]+p2[1])*t+(2*p0[1]-5*p1[1]+4*p2[1]-p3[1])*t2+(-p0[1]+3*p1[1]-3*p2[1]+p3[1])*t3);
      out.push(_clampCorridor([x,y],knots,ki,cap));
    }
  }
  return out;
}
function _smoothLine(coords,longhaul){
  if (!coords || coords.length<3) return coords;
  const knots=_rdp(coords, 0.0008); // ~90 m: structural-waypoint recovery
  if (knots.length<3) return coords;
  // open-sea long-haul: freer corridor + denser sampling; local spokes: tight to the coast.
  // Caps tuned (v12) to minimise smoothing-induced land touches on tight archipelago spokes.
  const opt = longhaul ? {absCap:0.02, devFactor:0.4, samples:8}
                       : {absCap:0.002, devFactor:0.25, samples:6};
  return _catmull(knots,opt);
}
const ROUTE_FC = { type:'FeatureCollection', features: ROUTES.filter(f=>{
  // Opt-out hook: Tasklet can set properties.render_hidden=true to suppress a route that
  // fails land validation until the pipeline repairs it (kill-switch while routing is fixed).
  return !(f.properties && f.properties.render_hidden===true);
}).map(f=>{
  const p=f.properties||{}, longhaul=_isLonghaul(p);
  let geom=f.geometry;
  if (Array.isArray(p.geometry_smooth) && p.geometry_smooth.length>1){
    geom={type:'LineString', coordinates:p.geometry_smooth};
  } else if (p.render_smooth!==false && geom && geom.type==='LineString'){
    geom={type:'LineString', coordinates:_smoothLine(geom.coordinates, longhaul)};
  }
  return {type:'Feature', geometry:geom, properties:{...p, scale_class: longhaul?'longhaul':'local'}};
})};

// ============ Connectivity: terminus nodes + connected-BP tagging (v12) ============
// ~28% of routes terminate where no marker is drawn, and only ~18% of boarding points sit
// on a route. That reads as "random" connectivity. We can't fabricate routes (the pipeline
// owns + land-validates them), but render-side we (a) draw a connector node at EVERY route
// terminus so no line dangles, and (b) tag which boarding points are on a route so the
// network reads as intentional (connected nodes lead; the unconnected long-tail recedes).
const _epKey = (x,y) => Math.round(x/0.02)+','+Math.round(y/0.02);   // ~2 km bucket for candidate lookup
const _EP_CELLS = new Map();   // bucket -> [[lng,lat],…] of route endpoints
const _termPts = new Map();    // dedup terminus points -> feature
for (const f of ROUTE_FC.features){
  const cs=f.geometry && f.geometry.coordinates; if(!cs||cs.length<2) continue;
  for (const c of [cs[0], cs[cs.length-1]]){
    const k=_epKey(c[0],c[1]);
    if(!_EP_CELLS.has(k)) _EP_CELLS.set(k,[]);
    _EP_CELLS.get(k).push(c);
    if(!_termPts.has(k)) _termPts.set(k, {type:'Feature', geometry:{type:'Point',coordinates:c},
      properties:{ platform:f.properties.platform, scale_class:f.properties.scale_class }});
  }
}
const ROUTE_NODES_FC = { type:'FeatureCollection', features:[..._termPts.values()] };
// additive optional field `on_route`: true iff the boarding point is genuinely on a route
// (within ~1.6 km of an endpoint), so the connected network leads and the tail recedes.
const _ON_TOL2 = 0.015*0.015;
for (const f of (FEATURES_BY_TYPE.poi||[])){
  if (f.properties.on_route==null){
    const c=f.geometry.coordinates, bx=Math.round(c[0]/0.02), by=Math.round(c[1]/0.02);
    let on=false;
    for(let dx=-1;dx<=1&&!on;dx++) for(let dy=-1;dy<=1&&!on;dy++){
      const cell=_EP_CELLS.get((bx+dx)+','+(by+dy)); if(!cell) continue;
      for(const e of cell){ const ex=e[0]-c[0], ey=e[1]-c[1]; if(ex*ex+ey*ey<=_ON_TOL2){ on=true; break; } }
    }
    f.properties.on_route = on;
  }
}

// Zoom-interpolated route paint, defined at module scope so story-focus can restore the
// curve (not flatten it to a constant). Local spokes grow + brighten as you zoom in;
// long-haul corridors lead at world/region view and recede once you're inside a cluster.
const W_LOCAL    = ['interpolate',['linear'],['zoom'], 5,0.5, 8,1.6, 11,3.0, 14,4.2];
const W_LONGHAUL = ['interpolate',['linear'],['zoom'], 1.5,1.0, 5,2.2, 9,1.8, 13,1.1];
const O_LOCAL_P2 = ['interpolate',['linear'],['zoom'], 6,0, 7.5,0.3, 9,0.7, 11,0.92];
const O_LOCAL_QLR= ['interpolate',['linear'],['zoom'], 6,0, 7.5,0.26, 9,0.62, 11,0.85];
const O_LH_P2    = ['interpolate',['linear'],['zoom'], 1.5,0.5, 6,0.78, 11,0.35];
const O_LH_QLR   = ['interpolate',['linear'],['zoom'], 1.5,0.42, 6,0.62, 11,0.28];
const O_GLOW     = ['interpolate',['linear'],['zoom'], 8,0, 11,0.16, 14,0.22];
const O_RLABEL   = ['interpolate',['linear'],['zoom'], 11,0, 12,0.9];
const O_POIGLYPH = ['case',['get','on_route'],1,0.5];   // connected boarding points lead; tail recedes

// ============ Node importance = route degree (data-derived hubs, v11 Item 2) ============
// Hubs must read as hubs from the DATA, not a hardcoded list. We count how many routes
// touch each node; cities then scale their dot, halo, glow and label by that degree, and
// the top hubs get a soft outgoing-spoke glow ring. `degree` is requested as an optional
// upstream field (see HANDOFF); when absent we compute it here so the sample still works.
const _DEG = {};
for (const r of ROUTES){ const p=r.properties||{}; if(p.from) _DEG[p.from]=(_DEG[p.from]||0)+1; if(p.to) _DEG[p.to]=(_DEG[p.to]||0)+1; }
let MAX_CITY_DEG = 1;
for (const f of (FEATURES_BY_TYPE.city||[])){
  if (f.properties.degree==null) f.properties.degree = _DEG[f.properties.id] || 0;
  if (f.properties.degree>MAX_CITY_DEG) MAX_CITY_DEG = f.properties.degree;
}
// Degree-driven paint ramps (clusterable source carries `degree` through on leaves).
const HUB_RADIUS = ['interpolate',['linear'],['coalesce',['get','degree'],0], 0,4, 3,5, 8,7, 14,9, 20,10.5];
const HUB_HALO_R = ['interpolate',['linear'],['coalesce',['get','degree'],0], 0,11, 3,14, 8,20, 16,30];
const HUB_HALO_O = ['interpolate',['linear'],['coalesce',['get','degree'],0], 0,0.12, 4,0.2, 10,0.32, 16,0.42];
const HUB_LABEL  = ['interpolate',['linear'],['coalesce',['get','degree'],0], 0,11, 4,12, 10,14, 16,15.5];
const O_HUBGLOW  = ['interpolate',['linear'],['coalesce',['get','degree'],0], 6,0.06, 16,0.16];

// Header stat counts are data-driven so they stay correct at live scale (60+/1,900/470+).
(function(){
  const set=(id,n)=>{ const e=document.getElementById(id); if(e) e.textContent=(n||0).toLocaleString(); };
  set('stat-cities',(FEATURES_BY_TYPE.city||[]).length);
  set('stat-areas',(FEATURES_BY_TYPE.locale||[]).length);
  set('stat-bps',(FEATURES_BY_TYPE.poi||[]).length);
  set('stat-routes',(ROUTES||[]).length);
})();


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

const map = window.map = new maplibregl.Map({
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
  // Routes — smoothed geometry + zoom hierarchy (Item 1). Draw order (bottom→top):
  // local glow · long-haul (QLR, PioII) · local (QLR, PioII) · local distance labels.
  map.addSource('routes', { type:'geojson', data:ROUTE_FC });
  const _isP2  = ['==',['get','platform'],'Pioneer II'];
  const _local = ['==',['get','scale_class'],'local'];
  const fLocalP2=['all',_isP2,_local];
  const fLocalQ =['all',['==',['get','platform'],'Quanta-LR'],_local];
  const fLHP2   =['all',_isP2,['==',['get','scale_class'],'longhaul']];
  const fLHQ    =['all',['==',['get','platform'],'Quanta-LR'],['==',['get','scale_class'],'longhaul']];
  const _rline  = {'line-cap':'round','line-join':'round'};
  // soft glow beneath local spokes → they read as bright filaments when zoomed into a cluster
  map.addLayer({ id:'route-local-glow', type:'line', source:'routes', filter:_local, layout:_rline, minzoom:6,
    paint:{ 'line-color':['case',_isP2,'#6ee7b7','#fbbf24'],
            'line-width':['interpolate',['linear'],['zoom'],8,2,11,7,14,11], 'line-opacity':O_GLOW, 'line-blur':3 }});
  map.addLayer({ id:'route-lh-qlr', type:'line', source:'routes', filter:fLHQ, layout:_rline,
    paint:{ 'line-color':'#fbbf24','line-width':W_LONGHAUL,'line-opacity':O_LH_QLR,'line-dasharray':[2,2.4] }});
  map.addLayer({ id:'route-lh-p2', type:'line', source:'routes', filter:fLHP2, layout:_rline,
    paint:{ 'line-color':'#6ee7b7','line-width':W_LONGHAUL,'line-opacity':O_LH_P2 }});
  map.addLayer({ id:'route-local-qlr', type:'line', source:'routes', filter:fLocalQ, layout:_rline, minzoom:6,
    paint:{ 'line-color':'#fbbf24','line-width':W_LOCAL,'line-opacity':O_LOCAL_QLR,'line-dasharray':[2,2.4] }});
  map.addLayer({ id:'route-local-p2', type:'line', source:'routes', filter:fLocalP2, layout:_rline, minzoom:6,
    paint:{ 'line-color':'#6ee7b7','line-width':W_LOCAL,'line-opacity':O_LOCAL_P2 }});
  // Terminus connector nodes — a dot at EVERY route endpoint so no line dangles into empty
  // water. Bridges the band gap (visible z7+) before boarding-point glyphs appear (z10), then
  // fades as glyphs take over. Coloured by platform to match the line meeting it.
  map.addSource('route-nodes', { type:'geojson', data:ROUTE_NODES_FC });
  map.addLayer({ id:'route-nodes', type:'circle', source:'route-nodes', minzoom:6.5,
    paint:{ 'circle-color':['case',['==',['get','platform'],'Pioneer II'],'#6ee7b7','#fbbf24'],
            'circle-radius':['interpolate',['linear'],['zoom'],7,1.6,10,2.6,13,3.2],
            'circle-stroke-width':1,'circle-stroke-color':'#0a0e14',
            'circle-opacity':['interpolate',['linear'],['zoom'],6.5,0,8,0.85,11,0.65,13,0.4] }});
  // local-route distance labels — appear only once you're zoomed into a cluster
  map.addLayer({ id:'route-local-labels', type:'symbol', source:'routes', filter:_local, minzoom:11,
    layout:{ 'symbol-placement':'line-center', 'text-field':['concat',['to-string',['round',['get','distance_nm']]],' nm'],
             'text-font':['Noto Sans Regular'],'text-size':10,'text-letter-spacing':0.02 },
    paint:{ 'text-color':'#cdd6e2','text-halo-color':'#0a0e14','text-halo-width':1.4,'text-opacity':O_RLABEL }});

  // Cities (clustered)
  map.addSource('cities', { type:'geojson', data:{type:'FeatureCollection',features:FEATURES_BY_TYPE.city||[]}, cluster:true, clusterMaxZoom:5, clusterRadius:48 });
  map.addLayer({ id:'city-cluster-halo', type:'circle', source:'cities', filter:['has','point_count'],
    paint:{ 'circle-color':'#6ee7b7','circle-opacity':0.18,'circle-radius':['step',['get','point_count'],28,5,36,15,46,30,56],'circle-blur':0.4 }});
  map.addLayer({ id:'city-clusters', type:'circle', source:'cities', filter:['has','point_count'],
    paint:{ 'circle-color':'#6ee7b7','circle-radius':['step',['get','point_count'],16,5,22,15,28,30,34],'circle-stroke-width':2,'circle-stroke-color':'rgba(255,255,255,0.85)','circle-opacity':0.95 }});
  map.addLayer({ id:'city-cluster-count', type:'symbol', source:'cities', filter:['has','point_count'],
    layout:{ 'text-field':['get','point_count_abbreviated'],'text-font':['Noto Sans Bold'],'text-size':13 }, paint:{'text-color':'#0a0e14'} });
  // Hub glow — degree-driven "burst" so high-degree nodes read as centres (data, not hardcoded)
  map.addLayer({ id:'city-hub-glow', type:'circle', source:'cities',
    filter:['all',['!',['has','point_count']],['>=',['coalesce',['get','degree'],0],6]],
    paint:{ 'circle-color':'#6ee7b7','circle-blur':1,
            'circle-radius':['*',['interpolate',['linear'],['coalesce',['get','degree'],0],6,18,10,26,16,40],
                                 ['interpolate',['linear'],['zoom'],3,0.7,7,1,11,1.25]],
            'circle-opacity':O_HUBGLOW }});
  map.addLayer({ id:'city-halo', type:'circle', source:'cities', filter:['!',['has','point_count']],
    paint:{ 'circle-color':'#6ee7b7','circle-opacity':HUB_HALO_O,'circle-radius':HUB_HALO_R,'circle-blur':0.5 }});
  map.addLayer({ id:'city-points', type:'circle', source:'cities', filter:['!',['has','point_count']],
    layout:{ 'circle-sort-key':['-',0,['coalesce',['get','degree'],0]] },
    paint:{ 'circle-color':'#6ee7b7','circle-radius':HUB_RADIUS,'circle-stroke-width':2,'circle-stroke-color':'#0a0e14' }});
  // City (market-tier) labels — collision-thinned by degree: low zoom shows only hubs
  // (curated), zoom in progressively reveals the rest. Hubs win placement via sort-key.
  map.addLayer({ id:'city-labels', type:'symbol', source:'cities', filter:['!',['has','point_count']],
    layout:{ 'text-field':['get','shortName'],'text-font':['Noto Sans Bold'],'text-size':HUB_LABEL,'text-offset':[0,1.2],'text-anchor':'top',
             'text-allow-overlap': false, 'text-ignore-placement': false, 'text-padding': 2,
             'symbol-sort-key': ['-',0,['coalesce',['get','degree'],0]] },
    paint:{ 'text-color':'#e8ecf1','text-halo-color':'#0a0e14','text-halo-width':1.5 }, minzoom:2 });

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
  // v9: shape/glyph-differentiated POI markers. Driven by coalesce(bp_type, poi_class).
  //   bp_type: from curated boarding-points/*.json (underscores)
  //   poi_class: from nodes.json upstream POIs (hyphens)
  // Glyphs use Noto Sans-safe Unicode (anchor + geometric shapes), not emoji,
  // because demotiles glyph server lacks emoji coverage.
  const BP_KEY = ['coalesce', ['get','bp_type'], ['get','display_type'], ['get','poi_class'], 'default'];
  const BP_COLOR = ['match', BP_KEY,
    // canonical display_type enum (Part 3.1)
    'ferry_cruise_terminal','#fb7185',
    'water_taxi_pier','#22d3ee',
    'mro_shipyard','#cbd5e1',
    'refuel_mid_node','#facc15',
    // curated bp_type
    'marina','#60a5fa',
    'working_harbour','#94a3b8',
    'ferry_terminal','#fb7185',
    'cruise_terminal','#fb7185',
    'water_bus_terminal','#fb7185',
    'yacht_club','#fbbf24',
    'hotel_jetty','#6ee7b7',
    'resort_jetty','#6ee7b7',
    'beach_club_jetty','#6ee7b7',
    'seaplane_base','#a78bfa',
    'water_taxi_stop','#22d3ee',
    'abra_station','#22d3ee',
    'public_pier','#22d3ee',
    'floating_pontoon','#22d3ee',
    'floating_helipad','#a78bfa',
    'shipyard_partner','#cbd5e1',
    'event_pontoon','#f0abfc',
    'dive_centre','#34d399',
    'sandbox_water','#facc15',
    // upstream poi_class
    'anchor-marina','#60a5fa',
    'secondary-hub','#60a5fa',
    'leisure-spoke','#fbbf24',
    'hospitality-hub','#6ee7b7',
    'resort-jetty','#6ee7b7',
    'cross-border-gateway','#fb7185',
    'refuel-mid-node','#fde68a',
    'mro-node','#cbd5e1',
    'abra-station','#22d3ee',
    'public-pier','#22d3ee',
    'out-of-range-marquee','#475569',
    '#60a5fa'  // default
  ];
  // Shape/glyph differentiation — primary visual encoding per v9 requirement.
  //   ⚓ harbour/marina/anchor   ▲ ferry/cruise/gateway   ★ yacht/leisure
  //   ■ hotel/resort/hospitality  ✦ seaplane               ◆ water-taxi/abra/pontoon/pier
  //   ⬢ MRO/shipyard/helipad      ⬟ refuel                ● default / out-of-range
  const BP_GLYPH = ['match', BP_KEY,
    'ferry_cruise_terminal','\u25B2', 'water_taxi_pier','\u25C6',
    'mro_shipyard','\u2B22', 'refuel_mid_node','\u2B1F',
    'marina','\u2693', 'working_harbour','\u2693',
    'anchor-marina','\u2693', 'secondary-hub','\u2693',
    'ferry_terminal','\u25B2', 'cruise_terminal','\u25B2', 'water_bus_terminal','\u25B2',
    'cross-border-gateway','\u25B2',
    'yacht_club','\u2605', 'leisure-spoke','\u2605',
    'hotel_jetty','\u25A0', 'resort_jetty','\u25A0', 'beach_club_jetty','\u25A0',
    'hospitality-hub','\u25A0', 'resort-jetty','\u25A0',
    'seaplane_base','\u2726',
    'water_taxi_stop','\u25C6', 'abra_station','\u25C6', 'abra-station','\u25C6',
    'public_pier','\u25C6', 'public-pier','\u25C6', 'floating_pontoon','\u25C6',
    'shipyard_partner','\u2B22', 'mro-node','\u2B22', 'floating_helipad','\u2B22',
    'event_pontoon','\u2B22', 'dive_centre','\u2B22', 'sandbox_water','\u2B22',
    'refuel-mid-node','\u2B1F',
    'out-of-range-marquee','\u25CF',
    '\u25CF'  // default
  ];
  const BP_SIZE = ['match', BP_KEY,
    'ferry_cruise_terminal',17, 'water_taxi_pier',12, 'mro_shipyard',15, 'refuel_mid_node',14,
    'marina',18, 'working_harbour',17, 'anchor-marina',18, 'secondary-hub',16,
    'ferry_terminal',17, 'cruise_terminal',17, 'water_bus_terminal',15,
    'cross-border-gateway',17,
    'yacht_club',16, 'leisure-spoke',14,
    'hotel_jetty',14, 'resort_jetty',14, 'beach_club_jetty',13,
    'hospitality-hub',15, 'resort-jetty',14,
    'seaplane_base',16, 'floating_helipad',15,
    'water_taxi_stop',12, 'abra_station',12, 'abra-station',12,
    'public_pier',12, 'public-pier',12, 'floating_pontoon',12,
    'shipyard_partner',15, 'mro-node',15, 'event_pontoon',13,
    'dive_centre',13, 'sandbox_water',13,
    'refuel-mid-node',14, 'out-of-range-marquee',10,
    12
  ];
  // Soft halo behind glyph for legibility on dark basemap (replaces poi-halo circles).
  // Colored glow only behind CONNECTED boarding points (on a route) so the network leads.
  map.addLayer({ id:'poi-halo', type:'circle', source:'pois', filter:['!',['has','point_count']], minzoom:10,
    paint:{ 'circle-color':BP_COLOR, 'circle-opacity':['case',['get','on_route'],0.26,0], 'circle-radius':11, 'circle-blur':0.7 }});
  // Boarding-point glyphs reveal at city zoom (band 4). Clusters (z8-10) handle density
  // below this. Connected boarding points (on a route) lead — full opacity + overlap
  // priority; the unconnected long-tail recedes so connectivity reads as intentional.
  map.addLayer({ id:'poi-points', type:'symbol', source:'pois', filter:['!',['has','point_count']], minzoom:10,
    layout:{
      'text-field': BP_GLYPH,
      'text-font': ['Noto Sans Bold'],
      'text-size': BP_SIZE,
      'text-allow-overlap': true,
      'text-ignore-placement': true,
      'symbol-sort-key': ['-', ['-',0,BP_SIZE], ['case',['get','on_route'],50,0]],
      'text-anchor': 'center'
    },
    paint:{
      'text-color': BP_COLOR,
      'text-opacity': O_POIGLYPH,
      'text-halo-color': '#0a0e14',
      'text-halo-width': 1.6,
      'text-halo-blur': 0.4
    }});
  map.addLayer({ id:'poi-labels', type:'symbol', source:'pois', filter:['!',['has','point_count']], minzoom:12,
    layout:{ 'text-field':['get','shortName'],'text-font':['Noto Sans Regular'],'text-size':10,'text-offset':[0,0.8],'text-anchor':'top',
             'text-optional':true,'symbol-sort-key':['-',0,BP_SIZE] }, paint:{ 'text-color':'#bfdbfe','text-halo-color':'#0a0e14','text-halo-width':1.4 }});

  // Range ring source (filled by selection)
  map.addSource('rings', { type:'geojson', data:{type:'FeatureCollection', features:[]} });
  map.addLayer({ id:'ring-p2', type:'line', source:'rings', filter:['==',['get','platform'],'Pioneer II'],
    paint:{ 'line-color':'#6ee7b7','line-width':1.5,'line-opacity':0.7,'line-dasharray':[2,3] }});
  map.addLayer({ id:'ring-qlr', type:'line', source:'rings', filter:['==',['get','platform'],'Quanta-LR'],
    paint:{ 'line-color':'#fbbf24','line-width':1.5,'line-opacity':0.5,'line-dasharray':[1,3] }});
  map.addLayer({ id:'ring-fill-p2', type:'fill', source:'rings', filter:['==',['get','platform'],'Pioneer II'],
    paint:{ 'fill-color':'#6ee7b7','fill-opacity':0.06 }});

  // Click handlers — include halo layers so the visible glow is clickable too
  for (const layer of ['city-points','city-halo','city-hub-glow','city-clusters','city-cluster-halo','locale-points','locale-halo','locale-clusters','poi-points','poi-halo','poi-clusters']) {
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

  // Route hover tooltips (Fix 8 v10) — all four route line layers
  ['route-local-p2','route-local-qlr','route-lh-p2','route-lh-qlr'].forEach(_bindRouteHover);

  // URL state
  applyUrlState();
  // If a partner view is active and we didn't deep-link straight into one of its stories,
  // land on the partner's scope (focus + branded landing panel).
  if (PARTNER_ACTIVE && !location.hash.startsWith('#/story/')) applyPartnerView();
  map.on('moveend', updateUrlState);
});

// ============ Fix 8 (v10): Route hover tooltip ============
const ROUTE_POPUP = new maplibregl.Popup({ closeButton:false, closeOnClick:false, className:'route-popup', offset:8 });
const CRUISE_KTS = { 'Pioneer II': 25, 'Quanta-LR': 20 };
function _shortById(id) {
  const n = NODE_INDEX[id];
  if (n) return n.props.shortName || n.props.fullName || id;
  return id;
}
function _routeTooltipHtml(p) {
  const a = _shortById(p.from), b = _shortById(p.to);
  const plat = p.platform || '';
  const dist = (p.distance_nm!=null) ? `${Math.round(p.distance_nm)} nm` : '—';
  const kts = CRUISE_KTS[plat] || 22;
  const hrs = (p.distance_nm!=null) ? (p.distance_nm / kts) : null;
  const time = hrs!=null ? (hrs < 1 ? `${Math.round(hrs*60)} min` : `${hrs.toFixed(1)} hr`) : '—';
  const color = plat==='Pioneer II' ? '#6ee7b7' : '#fbbf24';
  return `<div style="font:500 12px Inter; color:#e8ecf1; padding:2px 2px;">
    <div style="font-weight:600; margin-bottom:4px;">${escapeHtml(a)} → ${escapeHtml(b)}</div>
    <div style="display:flex; gap:10px; font-size:11px; color:#aab3c0;">
      <span style="color:${color}; font-weight:600;">${escapeHtml(plat)}</span>
      <span>${dist}</span>
      <span>${time} @ ${kts} kts</span>
    </div></div>`;
}
function _bindRouteHover(layer) {
  map.on('mousemove', layer, (e) => {
    if (!e.features || !e.features.length) return;
    map.getCanvas().style.cursor = 'pointer';
    const p = e.features[0].properties || {};
    ROUTE_POPUP.setLngLat(e.lngLat).setHTML(_routeTooltipHtml(p)).addTo(map);
  });
  map.on('mouseleave', layer, () => {
    map.getCanvas().style.cursor = '';
    ROUTE_POPUP.remove();
  });
}

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
// ============ Connectivity highlight on select (v12) ============
// Clicking a city lights its connected routes and dims the rest (keeping zoom behaviour via
// expression math), so the hub-and-spoke structure reads as intentional and explorable.
let CURRENT_STORY = null;
function _focusEngaged(){ return !!CURRENT_STORY || !!PARTNER_ACTIVE; }
function clearRouteHighlight(){
  try {
    map.setPaintProperty('route-local-p2','line-opacity',O_LOCAL_P2);
    map.setPaintProperty('route-lh-p2','line-opacity',O_LH_P2);
    map.setPaintProperty('route-local-qlr','line-opacity',O_LOCAL_QLR);
    map.setPaintProperty('route-lh-qlr','line-opacity',O_LH_QLR);
    map.setPaintProperty('route-local-glow','line-opacity',O_GLOW);
  } catch(e){}
}
function setRouteHighlight(id){
  if (!id) return clearRouteHighlight();
  const hit=['any',['==',['get','from'],id],['==',['get','to'],id]];
  try {
    map.setPaintProperty('route-local-p2','line-opacity',['case',hit,['max',O_LOCAL_P2,0.85],['*',O_LOCAL_P2,0.1]]);
    map.setPaintProperty('route-lh-p2','line-opacity',['case',hit,['max',O_LH_P2,0.85],['*',O_LH_P2,0.1]]);
    map.setPaintProperty('route-local-qlr','line-opacity',['case',hit,['max',O_LOCAL_QLR,0.8],['*',O_LOCAL_QLR,0.1]]);
    map.setPaintProperty('route-lh-qlr','line-opacity',['case',hit,['max',O_LH_QLR,0.8],['*',O_LH_QLR,0.1]]);
    map.setPaintProperty('route-local-glow','line-opacity',['case',hit,['max',O_GLOW,0.22],0]);
  } catch(e){}
}
function showDetail(props, coords) {
  const p = document.getElementById('panel');
  const name = props.fullName || props.name || 'Unnamed';
  const type = (props.type||'').toLowerCase();
  if (!_focusEngaged()) { if (type==='city') setRouteHighlight(props.id); else clearRouteHighlight(); }
  const meta = [];
  if (props.poi_class) meta.push(props.poi_class);
  if (props.country) meta.push(props.country);
  if (props.region) meta.push(props.region);
  if (props.parent_city_id || props.parent_city) meta.push(`parent: ${props.parent_city_id || props.parent_city}`);

  let html = `<div class="panel-hero">
    <div class="type-row">
      <span class="type-pill ${type}">${type==='locale'?'area':(type==='poi'?(props.bp_type_label||'boarding pt'):(type||'node'))}</span>
      ${props.platform_class ? `<span class="badge platform">${escapeHtml(props.platform_class)}</span>`:''}
    </div>
    <h2>${escapeHtml(name)}</h2>
    <div class="subtitle">${escapeHtml(meta.join(' · ')||'—')}</div>
    <button class="ring-toggle" data-coords="${coords.join(',')}">Toggle range rings (70 nm + 2,000 nm)</button>
  </div>`;
  // one-line value (external_safe, partner-neutral)
  if (props.one_line_value) html += `<div class="panel-section"><div class="what-distinct">${escapeHtml(props.one_line_value)}</div></div>`;
  // Operating profile (external_safe operational facts only)
  const tags=[];
  if (props.operator)         tags.push(['operator',props.operator]);
  if (props.capacity)         tags.push(['capacity',props.capacity]);
  if (props.charging_status)  tags.push(['charging',props.charging_status]);
  if (props.access_type)      tags.push(['access',props.access_type]);
  if (props.platform_fit)     tags.push(['platform fit',props.platform_fit]);
  if (tags.length) {
    html += `<div class="panel-section"><h3>Operating profile</h3><div class="kv-grid">`;
    for (const [k,v] of tags) { const fv=fmtValue(v); if (fv) html += `<dt>${escapeHtml(k)}</dt><dd>${fv}</dd>`; }
    html += `</div></div>`;
  }
  const skipExtra = new Set(['one_line_value','operator','capacity','charging_status','access_type','platform_fit','platform_class','shortName','fullName','segment','partner_links','also_serves','parent_city_id','is_anchor','coords_resolved']);
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

// ============ Partner views (v11 Item 4) ============
// A partner view is a small, data-driven config: which story slugs it surfaces, optional
// regions, and optional label/intro/accent for copy + branding. Selected via ?partner=<slug>.
// The default (no param) is the admin/all view — every story, no scope filter. Adding a new
// partner view needs NO code changes, only a PARTNER_VIEWS entry (Tasklet owns the real roster).
//   PARTNER_VIEWS[slug] = {
//     story_slugs: [string],   // required — which shipped stories this partner sees
//     regions:     [string],   // optional — informational; story scope already drives the map
//     label:       string,     // optional — branding text (else first story's partner name)
//     intro:       string,     // optional — copy shown on the partner's landing panel
//     accent:      string,     // optional — emerald|coral|gold|steel|violet|teal|amber|rose|sky
//   }
// PRIVACY NOTE: in a static single file, a per-partner URL is unguessable-link privacy, NOT
// enforced access control, and ALL data is still embedded. True isolation = a per-partner
// build on the Tasklet side that ships only that partner's data. See HANDOFF.
const PARTNER_VIEWS = {
  // DEMO entries — reference EXISTING public stories only (no invented identities).
  'grab':         { story_slugs:['grab'] },
  'careem':       { story_slugs:['careem'] },
  'red-sea':      { story_slugs:['red-sea-global'] },
  'sea-transit':  { label:'Southeast Asia Transit', accent:'teal', regions:['Southeast Asia'],
                    intro:'A focused view of coastal and inter-island mobility across the Southeast Asian archipelago.',
                    story_slugs:['grab','singapore-mpa'] },
  'gulf-transit': { label:'Gulf Waterborne Transit', accent:'amber', regions:['MENA'],
                    intro:'Waterborne transit and tourism corridors across the Gulf and Red Sea.',
                    story_slugs:['careem','uae-waterfront','qatar-transport','red-sea-global'] },
};
let PARTNER_ACTIVE = null;
function _partnerSlug(){ try { return new URLSearchParams(location.search).get('partner'); } catch(e){ return null; } }
function _viewStories(v){ return (v.story_slugs||[]).map(s=>STORY_BY_SLUG[s]).filter(Boolean); }
function _viewScopeCities(v){
  const set=new Set();
  for (const s of _viewStories(v)){
    for (const id of (s.scope_city_ids||[])) set.add(id);
    for (const n of (s.narrative||[])) if (n && n.city_id) set.add(n.city_id);
  }
  return [...set];
}
function _activeStories(){ return PARTNER_ACTIVE ? PARTNER_ACTIVE.stories : STORIES; }
function initPartnerView(){
  const slug=_partnerSlug();
  if (!slug || !PARTNER_VIEWS[slug]) return;       // unknown/absent -> admin/all view
  const view=PARTNER_VIEWS[slug];
  const stories=_viewStories(view);
  if (!stories.length) return;
  PARTNER_ACTIVE={ slug, view, stories, scopeCities:_viewScopeCities(view) };
  const label=view.label || stories[0].partner_org_canonical_name || slug;
  const tag=document.querySelector('#header .brand-text .tag');
  if (tag) tag.textContent = label + ' · Mobility Network';
  document.title = 'Navier Atlas · ' + label;
}
function _partnerEmptyHtml(){
  const v=PARTNER_ACTIVE.view, stories=PARTNER_ACTIVE.stories;
  const label=v.label || stories[0].partner_org_canonical_name || PARTNER_ACTIVE.slug;
  const accent=v.accent || stories[0].accent_class || 'emerald';
  let h=`<div class="story-header accent-${accent}">
    <div class="partner-mark">Prepared for</div>
    <h2>${escapeHtml(label)}</h2>
    <div class="subtitle">${escapeHtml(v.intro||'Your focused Navier mobility view.')}</div></div>
    <div class="panel-section"><h3>Your stories</h3></div>`;
  for (const s of stories){
    h+=`<div class="story-card" data-slug="${escapeHtml(s.slug)}">
      <div class="city">${escapeHtml((s.partner_org_canonical_name||'')+'')}</div>
      <h3>${escapeHtml(s.title)}</h3>
      <div class="body">${escapeHtml(s.subtitle||'')}</div></div>`;
  }
  return h;
}
function applyPartnerView(){
  if (!PARTNER_ACTIVE) return;
  applyStoryFocus(PARTNER_ACTIVE.scopeCities);
  const p=document.getElementById('panel');
  p.innerHTML=_partnerEmptyHtml(); p.scrollTop=0;
  p.querySelectorAll('.story-card[data-slug]').forEach(c=>c.addEventListener('click',()=>showStory(c.dataset.slug)));
}
const DEFAULT_OPACITY = {
  'route-local-p2': O_LOCAL_P2, 'route-lh-p2': O_LH_P2,
  'route-local-qlr': O_LOCAL_QLR, 'route-lh-qlr': O_LH_QLR,
  'route-local-glow': O_GLOW, 'route-local-labels': O_RLABEL,
  'city-points': 0.95, 'city-halo': HUB_HALO_O, 'city-hub-glow': O_HUBGLOW, 'city-labels': 1,
  'locale-points': 0.9, 'locale-halo': 0.2, 'locale-labels': 1,
  'poi-points': O_POIGLYPH, 'poi-labels': 1
};
function applyStoryFocus(cityIds) {
  if (!cityIds || !cityIds.length) {
    // Reset
    for (const [layer, op] of Object.entries(DEFAULT_OPACITY)) {
      const prop = (layer.includes('label') || layer==='poi-points') ? 'text-opacity' : (layer.startsWith('route')||layer.includes('ring')) ? 'line-opacity' : 'circle-opacity';
      try { map.setPaintProperty(layer, prop, op); } catch(e){}
    }
    return;
  }
  const inSet = ['in', ['get','id'], ['literal', cityIds]];
  const routeIn = ['any', ['in', ['get','from'], ['literal', cityIds]], ['in', ['get','to'], ['literal', cityIds]]];
  try {
    for (const L of ['route-local-p2','route-lh-p2','route-local-qlr','route-lh-qlr'])
      map.setPaintProperty(L,'line-opacity', ['case', routeIn, 0.92, 0.035]);
    map.setPaintProperty('route-local-glow','line-opacity', ['case', routeIn, 0.18, 0]);
    map.setPaintProperty('route-local-labels','text-opacity', ['case', routeIn, O_RLABEL, 0]);
    map.setPaintProperty('city-points','circle-opacity', ['case', inSet, 1, 0.18]);
    map.setPaintProperty('city-halo','circle-opacity', ['case', inSet, 0.4, 0.04]);
    map.setPaintProperty('city-hub-glow','circle-opacity', ['case', inSet, O_HUBGLOW, 0]);
    map.setPaintProperty('city-labels','text-opacity', ['case', inSet, 1, 0.25]);
    map.setPaintProperty('locale-points','circle-opacity', 0.25);
    map.setPaintProperty('locale-halo','circle-opacity', 0.05);
    map.setPaintProperty('locale-labels','text-opacity', 0.3);
    map.setPaintProperty('poi-points','text-opacity', 0.22);
    map.setPaintProperty('poi-labels','text-opacity', 0.25);
  } catch(e) { console.warn('focus', e); }
}
function closeStory() {
  window.location.hash = '';
  CURRENT_STORY = null;
  if (PARTNER_ACTIVE) { applyPartnerView(); return; }   // return to the partner landing, not full admin
  applyStoryFocus(null);
  document.getElementById('panel').innerHTML = document.getElementById('empty-tpl').innerHTML;
}
window.closeStory = closeStory;
function showStory(slug) {
  const s = STORY_BY_SLUG[slug]; if (!s) return;
  CURRENT_STORY = slug;
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
  // Partner-facing value object (external_safe). Internal commercial fields are never shipped.
  if (s.partner_view) {
    const pv = s.partner_view;
    html += `<div class="story-partnerview"><h3>What this unlocks for ${escapeHtml(s.partner_org_canonical_name||'you')}</h3>`;
    if (pv.value_prop) html += `<div class="body">${escapeHtml(pv.value_prop)}</div>`;
    if (pv.call_to_action) html += `<div class="cta">${escapeHtml(pv.call_to_action)}</div>`;
    html += `</div>`;
  }
  // Vessel specs reference (Part 4.2)
  if (s.vessel_specs_ref && VESSEL_SPECS) {
    html += `<div class="story-vessels"><h3>Platform</h3>`;
    for (const key of s.vessel_specs_ref) {
      const v = VESSEL_SPECS[key]; if (!v) continue;
      const rng = v.range_nm ? `${v.range_nm} nm` : '';
      const spd = v.top_speed_kts ? `${v.top_speed_kts} kts` : (v.cruise_kts ? `${v.cruise_kts} kts cruise` : '');
      html += `<div class="vessel"><div class="vname">${escapeHtml(v.name)}</div>
        <div class="vmeta">${escapeHtml([rng, spd, (v.pax?v.pax+' pax':''), v.powertrain].filter(Boolean).join(' · '))}</div>
        <div class="vmeta dim">${escapeHtml([v.emissions, v.status].filter(Boolean).join(' · '))}</div></div>`;
    }
    html += `</div>`;
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

// Resolve the active view (?partner=<slug>) before building the menu so a partner only
// ever sees their own stories; admin/all view (no param) sees every story.
initPartnerView();

// Story menu
const sm = document.getElementById('story-menu');
for (const s of _activeStories()) {
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
bindToggle('t-p2',  ['route-local-p2','route-lh-p2']);
bindToggle('t-qlr', ['route-local-qlr','route-lh-qlr']);
document.getElementById('t-routes').addEventListener('click', () => {
  const b = document.getElementById('t-routes'); const on = !b.classList.contains('on');
  b.classList.toggle('on', on);
  const p2 = document.getElementById('t-p2').classList.contains('on');
  const qlr = document.getElementById('t-qlr').classList.contains('on');
  setLayerVis('route-local-p2',  on && p2); setLayerVis('route-lh-p2',  on && p2);
  setLayerVis('route-local-qlr', on && qlr); setLayerVis('route-lh-qlr', on && qlr);
  setLayerVis('route-local-glow', on); setLayerVis('route-local-labels', on); setLayerVis('route-nodes', on);
});
bindToggle('t-locales', ['locale-clusters','locale-cluster-count','locale-halo','locale-points','locale-labels']);
bindToggle('t-pois',    ['poi-clusters','poi-cluster-count','poi-points','poi-halo','poi-labels']);

// Panel collapse toggle
const panelToggle = document.getElementById('panel-toggle');
panelToggle.addEventListener('click', () => {
  document.body.classList.toggle('panel-hidden');
  panelToggle.textContent = document.body.classList.contains('panel-hidden') ? '›' : '‹';
  // force MapLibre to recompute size
  setTimeout(() => map.resize(), 340);
});

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

# ---- Claude render-merge hook ----------------------------------------------
# If an external template.html exists (produced by claude_to_template.py from
# Claude's de-baked index.html), use it as the render template. Default behavior
# is unchanged when the file is absent (inline HTML above is used). The external
# template MUST contain the four data placeholders or we fail closed.
_tpl_path = HERE / "template.html"
if _tpl_path.exists():
    _ext = _tpl_path.read_text()
    _need = ["__FEATURES__", "__ROUTES__", "__STORIES__", "__VESSELS__"]
    _missing = [p for p in _need if p not in _ext]
    if _missing:
        raise SystemExit(f"[render-merge] template.html missing placeholders {_missing} — refusing to build")
    HTML = _ext
    print(f"[render-merge] using external template.html ({len(_ext):,} bytes)")

# ---- Partner-pitch content blobs (city briefs + partner proposals) ----------
# External_safe, partner-facing. Baked as globals so Claude's render binds directly.
# Placeholders are OPTIONAL: replace is a no-op until template.html declares them.
_pp = HERE.parent / "partner-pitch"
_city_briefs = {}
for _f in sorted((_pp / "city_briefs").glob("*.json")) if (_pp / "city_briefs").exists() else []:
    try:
        _b = json.loads(_f.read_text()); _city_briefs[_b["city_id"]] = _b
    except Exception as _e:
        print(f"[pitch] skip {_f.name}: {_e}")
_partners = {}
for _f in sorted((_pp / "partners").glob("*.json")) if (_pp / "partners").exists() else []:
    try:
        _b = json.loads(_f.read_text()); _partners[_b["partner_id"]] = _b
    except Exception as _e:
        print(f"[pitch] skip {_f.name}: {_e}")
print(f"Partner-pitch: {len(_city_briefs)} city briefs, {len(_partners)} partner proposals baked")

out = (HTML
  .replace("__FEATURES__", json.dumps(by_type))
  .replace("__ROUTES__", json.dumps(route_features))
  .replace("__STORIES__", json.dumps(stories))
  .replace("__VESSELS__", json.dumps(vessel_specs))
  .replace("__CITY_BRIEFS__", json.dumps(_city_briefs))
  .replace("__PARTNERS__", json.dumps(_partners))
  .replace("__N_CITY__", str(n_city))
  .replace("__N_LOCALE__", str(n_locale))
  .replace("__N_POI__", str(n_poi))
  .replace("__N_ROUTE__", str(len(route_features))))

# Guaranteed availability of the pitch content layer: if the render template has not yet
# wired the __CITY_BRIEFS__ / __PARTNERS__ placeholders, inject the data as window globals
# so the front-end (Claude's city panels + phase carousel) can read it immediately and the
# data ships live regardless of template state. Idempotent: skipped if a const already exists.
if "window.CITY_BRIEFS" not in out and "const CITY_BRIEFS" not in out:
    _inject = ("<script>window.CITY_BRIEFS=" + json.dumps(_city_briefs) +
               ";window.PARTNERS=" + json.dumps(_partners) + ";</script>")
    if "</head>" in out:
        out = out.replace("</head>", _inject + "</head>", 1)
    elif "</body>" in out:
        out = out.replace("</body>", _inject + "</body>", 1)
    else:
        out += _inject
    print(f"Injected pitch content as window globals ({len(_city_briefs)} briefs, {len(_partners)} partners)")

(HERE / "index.html").write_text(out)
print(f"Wrote index.html — {len(out):,} bytes")
