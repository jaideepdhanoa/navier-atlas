#!/usr/bin/env python3
"""
Navier Atlas — Data Spine parser
Reads world-map/regions/**/*.md city files and produces graph JSON.

Outputs (to ./output/):
  nodes.json    cities + POI sub-clusters
  edges.json    routes (derived from sub-clusters with distance_nm_from_anchor)
  orgs.json     counterparties (rolled up across files)
  humans.json   named contacts
  raw-sections.json  unstructured prose per file (for side-panel)
  meta.json     schema version + generation stats
"""

import json, re, sys, os, glob, datetime, hashlib
from collections import defaultdict

SCHEMA_VERSION = "0.1.0"
ROOT = "/agent/home/navier"
WORLD_MAP = f"{ROOT}/world-map/regions"
OUT_DIR   = "/agent/home/navier/app/data-spine/output"
COORDS_FILE = "/agent/home/navier/app/data-spine/manual-coords/city-anchors.json"
STRATEGIC_POI_COORDS_FILE = "/agent/home/navier/app/data-spine/manual-coords/strategic-pois.json"

os.makedirs(OUT_DIR, exist_ok=True)

# --- helpers ---
def slug(s):
    s = re.sub(r"[^\w\s-]", "", s.lower()).strip()
    s = re.sub(r"[\s_-]+", "-", s)
    return s.strip("-")

def parse_distance_nm(s):
    """Extract first numeric value from distance strings like '~6 nm', '65–75 nm', '~135 nm (via AUH)', '10–60 nm'."""
    if not s: return None
    s = s.replace("–", "-").replace("—", "-")
    nums = re.findall(r"(\d+\.?\d*)", s)
    if not nums: return None
    vals = [float(n) for n in nums]
    if len(vals) >= 2 and "-" in s:
        return round((vals[0] + vals[1]) / 2, 1)
    return vals[0]

def split_table_row(line):
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return cells

def parse_md_table(lines, start_idx):
    """Returns (headers, rows, next_idx). Assumes start_idx points to header row."""
    headers = split_table_row(lines[start_idx])
    sep = lines[start_idx + 1]
    if not re.match(r"^\s*\|?\s*:?-+", sep):
        return None, [], start_idx
    rows = []
    i = start_idx + 2
    while i < len(lines) and lines[i].strip().startswith("|"):
        rows.append(split_table_row(lines[i]))
        i += 1
    return headers, rows, i

def md_strong_strip(s):
    """Strip bold/italic markdown and bracketed source notes."""
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"\*(.+?)\*", r"\1", s)
    return s.strip()

# --- coord loaders ---
with open(COORDS_FILE) as f:
    CITY_ANCHORS = json.load(f)["anchors"]

STRATEGIC_POI_COORDS = {}
if os.path.exists(STRATEGIC_POI_COORDS_FILE):
    with open(STRATEGIC_POI_COORDS_FILE) as f:
        STRATEGIC_POI_COORDS = json.load(f).get("pois", {})

# --- per-file parser ---
def parse_file(path):
    rel = os.path.relpath(path, ROOT).replace("\\", "/")
    region_dir = os.path.basename(os.path.dirname(path))
    region_map = {"mena": "MENA", "sea": "SEA", "east-asia": "East Asia", "europe": "Europe",
                  "turkey": "Turkey", "north-america": "North America", "latam-caribbean": "LatAm-Caribbean",
                  "oceania": "Oceania", "africa": "Africa", "south-asia": "South Asia"}
    region = region_map.get(region_dir, region_dir)
    file_slug = os.path.basename(path).replace(".md", "")

    with open(path) as f:
        content = f.read()
    lines = content.split("\n")

    out = {
        "city": None, "pois": [], "edges": [], "orgs": [], "humans": [],
        "archetype_scores": {}, "raw_sections": {},
        "schema_archetype_tags": [], "warnings": []
    }

    # --- header lines ---
    title_m = re.match(r"^#\s+(.+?)$", lines[0])
    if not title_m:
        out["warnings"].append("no title")
        return out
    title = title_m.group(1).strip()
    # "Dubai, UAE" or "Komodo & Flores, Indonesia"
    if "," in title:
        city_name, country = [p.strip() for p in title.rsplit(",", 1)]
    else:
        city_name, country = title, ""

    posture = None
    for ln in lines[1:8]:
        m = re.match(r"_Posture:\s*(?:\*\*)?([A-Za-z0-9]+)(?:\*\*)?", ln)
        if m:
            posture = m.group(1)
            break

    anchor = CITY_ANCHORS.get(file_slug)
    coords = anchor["coords"] if anchor else None
    if not anchor:
        out["warnings"].append(f"no anchor coord for {file_slug}")

    # platform_class detection
    text_lower = content.lower()
    if "pioneer-ii-mono" in text_lower or "pioneer ii mono" in text_lower:
        platform_class = "pioneer-ii-mono"
    elif "quanta-lr-led" in text_lower or "quanta-lr led" in text_lower:
        platform_class = "quanta-lr-led"
    elif "dual-platform" in text_lower or "dual platform" in text_lower:
        platform_class = "dual-platform"
    else:
        platform_class = "dual-platform"  # default

    out["city"] = {
        "id": file_slug,
        "type": "city",
        "name": city_name,
        "country": country,
        "region": region,
        "posture": posture,
        "platform_class": platform_class,
        "coords": coords,
        "source_file": rel,
        "source_line": 1,
        "warnings": [w for w in out["warnings"]]
    }

    # --- walk sections ---
    section_starts = []
    for i, ln in enumerate(lines):
        m = re.match(r"^(#{2,4})\s+(.+?)$", ln)
        if m:
            section_starts.append((i, len(m.group(1)), m.group(2).strip()))

    def section_body(i_start):
        """Lines from i_start+1 until next same-or-higher header."""
        depth = section_starts[[s[0] for s in section_starts].index(i_start)][1]
        idx_in_list = [s[0] for s in section_starts].index(i_start)
        end = len(lines)
        for j in range(idx_in_list + 1, len(section_starts)):
            if section_starts[j][1] <= depth:
                end = section_starts[j][0]
                break
        return lines[i_start+1:end], end

    # raw section dump (for side-panel)
    for (i, depth, name) in section_starts:
        body, _ = section_body(i)
        key = f"{'#'*depth} {name}"
        out["raw_sections"][key] = "\n".join(body).strip()

    # --- Sub-clusters table → POIs ---
    sc_idx = None
    for i, depth, name in section_starts:
        if depth == 2 and name.lower().startswith("sub-cluster"):
            sc_idx = i; break
    if sc_idx is not None:
        body, _ = section_body(sc_idx)
        for k, ln in enumerate(body):
            if ln.strip().startswith("|"):
                headers, rows, _ = parse_md_table(body, k)
                if headers and rows:
                    parse_sub_clusters(out, file_slug, headers, rows, rel, sc_idx + 2 + k)
                break

    # --- Archetype fit table ---
    af_idx = None
    for i, depth, name in section_starts:
        if depth == 2 and "archetype fit" in name.lower():
            af_idx = i; break
    if af_idx is not None:
        body, _ = section_body(af_idx)
        for k, ln in enumerate(body):
            if ln.strip().startswith("|"):
                headers, rows, _ = parse_md_table(body, k)
                if headers and rows:
                    parse_archetype_scores(out, headers, rows)
                break

    # --- Named contacts table ---
    nc_idx = None
    for i, depth, name in section_starts:
        if depth == 2 and "named contact" in name.lower():
            nc_idx = i; break
    if nc_idx is not None:
        body, _ = section_body(nc_idx)
        for k, ln in enumerate(body):
            if ln.strip().startswith("|"):
                headers, rows, _ = parse_md_table(body, k)
                if headers and rows:
                    parse_named_contacts(out, file_slug, headers, rows, rel, nc_idx + 2 + k)
                break

    # --- Players sub-sections → orgs ---
    players_idx = None
    for i, depth, name in section_starts:
        if depth == 2 and name.lower().startswith("players"):
            players_idx = i; break
    if players_idx is not None:
        # collect ### sub-sections under Players until next ##
        depth_players = 2
        idx_in_list = [s[0] for s in section_starts].index(players_idx)
        for j in range(idx_in_list + 1, len(section_starts)):
            i_sub, depth_sub, name_sub = section_starts[j]
            if depth_sub <= depth_players: break
            body, _ = section_body(i_sub)
            parse_players_subsection(out, file_slug, name_sub, body, rel, i_sub)

    # --- derive edges from sub-cluster distances ---
    for poi in out["pois"]:
        d = poi.get("distance_nm_from_anchor")
        if d is None or d == 0: continue
        platform = derive_platform_for_route(poi)
        edge_class = derive_edge_class(poi)
        out["edges"].append({
            "id": f"edge__{file_slug}__{poi['id'].split('__')[1]}",
            "from_node_id": file_slug,
            "to_node_id": poi["id"],
            "distance_nm": d,
            "platform": platform,
            "edge_class": edge_class,
            "counterparty_jurisdiction": poi.get("jurisdiction"),
            "refuel_mid_node_id": None,
            "pitch_trap": "pitch trap" in (poi.get("distinct") or "").lower(),
            "flag_and_exclude": "flag-and-exclude" in (poi.get("distinct") or "").lower(),
            "out_of_range_marquee": "out of scope" in (poi.get("role") or "").lower(),
            "source_file": rel,
            "source_line": poi.get("source_line")
        })

    return out


def parse_sub_clusters(out, file_slug, headers, rows, rel, line_no):
    # Column matching is fuzzy because column counts/names vary slightly across files.
    h = [md_strong_strip(x).lower() for x in headers]
    def col(*names):
        for n in names:
            for k, hh in enumerate(h):
                if n in hh: return k
        return None
    ic_name = col("sub-cluster")
    ic_role = col("role")
    ic_dist = col("distance")
    ic_p2   = col("pioneer ii bucket", "pioneer ii")
    ic_qlr  = col("quanta-lr bucket", "quanta-lr")
    ic_jur  = col("jurisdiction", "counterparty jurisdiction")
    ic_chg  = col("charging")
    ic_pier = col("pier-access", "pier access")
    ic_dist_distinct = col("what's distinct", "distinct")

    for r in rows:
        if len(r) < 3: continue
        name = md_strong_strip(r[ic_name]) if ic_name is not None and ic_name < len(r) else r[0]
        if not name: continue
        poi_slug = slug(name)[:60]
        poi_id = f"{file_slug}__{poi_slug}"
        role = md_strong_strip(r[ic_role]) if ic_role is not None and ic_role < len(r) else None
        dist = parse_distance_nm(r[ic_dist]) if ic_dist is not None and ic_dist < len(r) else None
        coords_override = STRATEGIC_POI_COORDS.get(poi_id, {}).get("coords")
        poi = {
            "id": poi_id,
            "type": "poi",
            "poi_class": classify_poi(name, role, r[ic_dist_distinct] if ic_dist_distinct is not None and ic_dist_distinct < len(r) else ""),
            "name": name,
            "anchor_node_id": file_slug,
            "role": role,
            "distance_nm_from_anchor": dist,
            "pioneer_ii_bucket": md_strong_strip(r[ic_p2]) if ic_p2 is not None and ic_p2 < len(r) else None,
            "quanta_lr_bucket": md_strong_strip(r[ic_qlr]) if ic_qlr is not None and ic_qlr < len(r) else None,
            "jurisdiction": md_strong_strip(r[ic_jur]) if ic_jur is not None and ic_jur < len(r) else None,
            "charging_window": md_strong_strip(r[ic_chg]) if ic_chg is not None and ic_chg < len(r) else None,
            "pier_archetype": md_strong_strip(r[ic_pier]) if ic_pier is not None and ic_pier < len(r) else None,
            "distinct": md_strong_strip(r[ic_dist_distinct]) if ic_dist_distinct is not None and ic_dist_distinct < len(r) else None,
            "coords": coords_override,
            "coords_resolved": coords_override is not None,
            "source_file": rel,
            "source_line": line_no
        }
        out["pois"].append(poi)


def classify_poi(name, role, distinct):
    n = (name or "").lower(); r = (role or "").lower(); d = (distinct or "").lower()
    if "anchor" in r: return "anchor-marina"
    if "out of scope" in r or "out-of-scope" in r: return "out-of-range-marquee"
    if "shipyard" in n: return "shipyard"
    if "refuel" in n or "refuel" in d: return "refuel-mid-node"
    if "airstrip" in n or "airport" in n: return "mro-node"
    if "marina" in n and "harbour" in n: return "anchor-marina"
    if "marina" in n: return "marina"
    if "resort" in n or "resort" in d: return "resort-jetty"
    if "creek" in n or "abra" in d: return "abra-station"
    if "harbour" in n or "harbor" in n: return "anchor-marina"
    if "island" in n or "islands" in n: return "leisure-spoke"
    if "ferry" in n: return "public-pier"
    if "secondary hub" in r: return "secondary-hub"
    if "cross-border" in d or "cross border" in d: return "cross-border-gateway"
    if "leisure spoke" in r: return "leisure-spoke"
    if "hub" in r: return "hospitality-hub"
    return "leisure-spoke"


def derive_platform_for_route(poi):
    p2 = (poi.get("pioneer_ii_bucket") or "").lower()
    qlr = (poi.get("quanta_lr_bucket") or "").lower()
    if "in-range" in p2: return "Pioneer II"
    if "edge" in p2: return "edge-of-Pioneer"
    if "in-range" in qlr: return "Quanta-LR"
    return "out-of-range"


def derive_edge_class(poi):
    d = (poi.get("distinct") or "").lower()
    j = (poi.get("jurisdiction") or "").lower()
    if "icq" in d or "immigration/customs" in d: return "icq-gated-pier-pair"
    if "refuel" in d: return "refuel-mid-node-leg"
    if "cross-border" in d or ("cross" in d and "border" in d) or "(cross-border)" in j: return "cross-border-radial"
    if "pitch trap" in d: return "pitch-trap"
    if "flag-and-exclude" in d: return "flag-and-exclude"
    if (poi.get("distance_nm_from_anchor") or 0) < 10: return "intra-city"
    return "hub-radial-spoke"


def parse_archetype_scores(out, headers, rows):
    h = [md_strong_strip(x).lower() for x in headers]
    if not any("archetype" in x for x in h) and not any("fit" in x for x in h):
        return
    arche_idx = 0
    fit_idx = 1 if len(h) > 1 else None
    archetype_keymap = {
        "ride-hail": "ridehail", "ride hail": "ridehail", "super-app": "ridehail",
        "public transport": "pta", "transport authority": "pta",
        "hospitality": "hospitality",
        "b2b": "b2b", "corporate": "b2b",
        "luxury charter": "charter", "yacht": "charter",
    }
    for r in rows:
        if len(r) < 2: continue
        arche = md_strong_strip(r[arche_idx]).lower()
        fit_cell = md_strong_strip(r[fit_idx]) if fit_idx is not None else ""
        # Extract first integer 0-10
        nums = re.findall(r"\b(10|[0-9])\b", fit_cell)
        score = int(nums[0]) if nums else None
        # Quanta-LR uplift
        nums_all = [int(n) for n in nums]
        for needle, key in archetype_keymap.items():
            if needle in arche:
                if score is not None:
                    out["archetype_scores"][key] = score
                if len(nums_all) >= 2 and "quanta" in fit_cell.lower():
                    out["archetype_scores"][f"{key}_quanta_lr"] = nums_all[-1]
                break


def parse_named_contacts(out, file_slug, headers, rows, rel, line_no):
    h = [md_strong_strip(x).lower() for x in headers]
    def col(*names):
        for n in names:
            for k, hh in enumerate(h):
                if n in hh: return k
        return None
    ic_name = col("name")
    ic_org  = col("org")
    ic_role = col("role")
    ic_rel  = col("relationship")
    ic_src  = col("source")
    ic_next = col("best next move", "next move")
    for r in rows:
        if not r or len(r) < 2: continue
        name = md_strong_strip(r[ic_name]) if ic_name is not None and ic_name < len(r) else ""
        if not name: continue
        # Skip pure gap markers without an org pin
        org = md_strong_strip(r[ic_org]) if ic_org is not None and ic_org < len(r) else ""
        if name.startswith("[gap]") and not org:
            continue
        human_id = "human-" + slug(name + "--" + org)[:80] if "[gap]" not in name else f"gap__{file_slug}__{slug(org)[:40]}"
        h_obj = {
            "id": human_id,
            "name": name,
            "name_status": "TBC" if "tbc" in name.lower() or "[gap]" in name.lower() else "confirmed",
            "primary_org": org,
            "role": md_strong_strip(r[ic_role]) if ic_role is not None and ic_role < len(r) else None,
            "posture": md_strong_strip(r[ic_rel]) if ic_rel is not None and ic_rel < len(r) else None,
            "source": md_strong_strip(r[ic_src]) if ic_src is not None and ic_src < len(r) else None,
            "next_move": md_strong_strip(r[ic_next]) if ic_next is not None and ic_next < len(r) else None,
            "associated_cities": [file_slug],
            "source_files": [rel],
            "source_line": line_no
        }
        out["humans"].append(h_obj)


PLAYERS_SECTION_TYPE = {
    "regulators": "government-regulator",
    "governments": "government-regulator",
    "demand platforms": "demand-platform",
    "super-apps": "demand-platform",
    "ride-hail": "demand-platform",
    "public transport": "pta",
    "ferry operators": "pta",
    "hospitality": "hospitality-chain",
    "resort owners": "hospitality-chain",
    "marinas": "marina-operator",
    "ports": "marina-operator",
    "pier concessionaires": "marina-operator",
    "asset holders": "asset-holder",
    "leasing financiers": "asset-holder",
    "sovereign-developers": "sovereign-developer",
    "shipyards": "shipyard",
    "mro": "mro",
    "electric-marine builders": "shipyard",
    "incumbents": "competitor",
    "competitors": "competitor",
    "lock-in risks": "competitor"
}

def classify_section_type(name):
    n = name.lower()
    for needle, t in PLAYERS_SECTION_TYPE.items():
        if needle in n: return t
    return "other"

def parse_players_subsection(out, file_slug, section_name, body, rel, line_no):
    org_type = classify_section_type(section_name)
    # Each bullet "- **OrgName** — description" → an org
    for ln in body:
        m = re.match(r"^\s*[-*]\s+\*\*(.+?)\*\*\s*[—\-:]?\s*(.*)$", ln)
        if not m:
            m = re.match(r"^\s*[-*]\s+(.+?)\s*[—\-:]\s*(.+)$", ln)
        if m:
            org_name = md_strong_strip(m.group(1)).strip()
            desc = m.group(2).strip()
            if not org_name or len(org_name) > 80: continue
            out["orgs"].append({
                "id": "org-" + slug(org_name)[:60],
                "name": org_name,
                "type": org_type,
                "city_presence_raw": [file_slug],
                "notes_per_file": [{"file": file_slug, "section": section_name, "note": desc}],
                "source_files": [rel],
                "source_line": line_no
            })


# --- main ---
def main():
    files = []
    for region_dir in sorted(os.listdir(WORLD_MAP)):
        d = os.path.join(WORLD_MAP, region_dir)
        if os.path.isdir(d):
            for f in sorted(os.listdir(d)):
                if f.endswith(".md"):
                    files.append(os.path.join(d, f))

    # Allow filter from argv
    if len(sys.argv) > 1:
        wanted = set(sys.argv[1:])
        files = [f for f in files if os.path.basename(f).replace(".md","") in wanted]

    all_nodes, all_edges, all_humans = [], [], []
    org_rollup = {}  # id -> merged org
    raw_sections_by_file = {}
    archetype_by_city = {}
    warnings = []

    for path in files:
        parsed = parse_file(path)
        if parsed["city"]:
            all_nodes.append(parsed["city"])
            archetype_by_city[parsed["city"]["id"]] = parsed["archetype_scores"]
        all_nodes.extend(parsed["pois"])
        all_edges.extend(parsed["edges"])
        all_humans.extend(parsed["humans"])
        raw_sections_by_file[parsed["city"]["id"] if parsed["city"] else os.path.basename(path)] = parsed["raw_sections"]
        warnings.extend([f"{path}: {w}" for w in parsed["warnings"]])

        for org in parsed["orgs"]:
            oid = org["id"]
            if oid not in org_rollup:
                org_rollup[oid] = {
                    "id": oid, "name": org["name"], "type": org["type"],
                    "city_presence": [], "notes_per_file": [], "source_files": []
                }
            agg = org_rollup[oid]
            for c in org["city_presence_raw"]:
                if c not in agg["city_presence"]: agg["city_presence"].append(c)
            agg["notes_per_file"].extend(org["notes_per_file"])
            for f in org["source_files"]:
                if f not in agg["source_files"]: agg["source_files"].append(f)

    # Merge archetype scores into city nodes
    for n in all_nodes:
        if n["type"] == "city" and n["id"] in archetype_by_city:
            n["archetype_scores"] = archetype_by_city[n["id"]]

    meta = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "files_processed": len(files),
        "city_nodes": sum(1 for n in all_nodes if n["type"]=="city"),
        "poi_nodes": sum(1 for n in all_nodes if n["type"]=="poi"),
        "edges": len(all_edges),
        "orgs_rolled_up": len(org_rollup),
        "humans": len(all_humans),
        "warnings": warnings[:50]
    }

    def dump(name, payload):
        with open(os.path.join(OUT_DIR, name), "w") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

    dump("nodes.json", {"_meta": meta, "nodes": all_nodes})
    dump("edges.json", {"_meta": meta, "edges": all_edges})
    dump("orgs.json",  {"_meta": meta, "orgs": list(org_rollup.values())})
    dump("humans.json",{"_meta": meta, "humans": all_humans})
    dump("raw-sections.json", {"_meta": meta, "by_city": raw_sections_by_file})
    dump("meta.json", meta)

    print(json.dumps(meta, indent=2))

if __name__ == "__main__":
    main()
