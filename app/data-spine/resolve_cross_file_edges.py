#!/usr/bin/env python3
"""
Navier Atlas — Phase 0.5 / Sub-task 1
Cross-file Edge Resolver

Re-scans every city file's "Waterways & Routes" section and extracts
X ↔ Y route mentions, resolving both endpoints to node IDs in the
existing nodes.json. Emits new edges, appended to edges.json.

This is the PRIMARY edge extractor — the v0.1 parse_city_files.py only
caught intra-city sub-cluster edges. This pass catches the actual
cross-border / inter-city network (Singapore's 10-route radial fan,
Dubai's GCC fan, RSG ↔ Jeddah, etc.).

Inputs:  output/nodes.json  (cities + POIs from v0.1 parser)
Outputs: output/edges.json  (rewritten with cross-file edges added)
         output/edges-cross-file.json  (just the new ones, for audit)
         output/edge-resolution-report.md  (audit trail of every match
            attempt, including failed matches — feeds manual coords/aliases)
"""

from __future__ import annotations
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

ROOT = Path("/agent/home/navier")
REGIONS = ROOT / "world-map" / "regions"
OUTPUT = Path(__file__).parent / "output"

# -----------------------------------------------------------------------------
# Manual alias map — short forms / abbreviations that recur in routes prose.
# Maps to city node IDs (file_id minus .md).
# -----------------------------------------------------------------------------
CITY_ALIASES = {
    "dxb": "dubai-uae",
    "dubai": "dubai-uae",
    "auh": "abu-dhabi-uae",
    "abu dhabi": "abu-dhabi-uae",
    "doh": "doha-qatar",
    "doha": "doha-qatar",
    "bah": "manama-bahrain",
    "manama": "manama-bahrain",
    "bahrain": "manama-bahrain",
    "rsg": "red-sea-global-ksa",
    "red sea global": "red-sea-global-ksa",
    "jed": "jeddah-ksa",
    "jeddah": "jeddah-ksa",
    "neom": "neom-sindalah-ksa",
    "sindalah": "neom-sindalah-ksa",
    "rak": "ras-al-khaimah-uae",
    "ras al khaimah": "ras-al-khaimah-uae",
    "fuj": "fujairah-uae",
    "fujairah": "fujairah-uae",
    "sharjah": "sharjah-uae",
    "muscat": "muscat-oman",
    "msc": "muscat-oman",
    "ssh": "sharm-el-sheikh-egypt",
    "sharm": "sharm-el-sheikh-egypt",
    "sharm el sheikh": "sharm-el-sheikh-egypt",
    "salalah": "salalah-dhofar-oman",
    "sg": "singapore",
    "singapore": "singapore",
    "spore": "singapore",
    "jkt": "jakarta-indonesia",
    "jakarta": "jakarta-indonesia",
    "bali": "bali-indonesia",
    "denpasar": "bali-indonesia",
    "mle": "male-maldives",
    "maldives": "male-maldives",
    "male": "male-maldives",
    "phl": "manila-philippines",
    "philippines": "manila-philippines",
    "manila": "manila-philippines",
    "bkk": "bangkok-thailand",
    "bangkok": "bangkok-thailand",
    "phuket": "phuket-phang-nga-thailand",
    "phang nga": "phuket-phang-nga-thailand",
    "samui": "koh-samui-thailand",
    "koh samui": "koh-samui-thailand",
    "vietnam": "vietnam",
    "vn": "vietnam",
    "hcm": "vietnam",
    "hanoi": "vietnam",
    "malaysia": "malaysia",
    "my": "malaysia",
    "kl": "malaysia",
    "kuala lumpur": "malaysia",
    "port klang": "malaysia",
    "jb": "malaysia",
    "johor bahru": "malaysia",
    "johor": "malaysia",
    "desaru": "malaysia",
    "malacca": "malaysia",
    "melaka": "malaysia",
    "penang": "malaysia",
    "george town": "malaysia",
    "tioman": "malaysia",
    "cambodia": "cambodia",
    "phnom penh": "cambodia",
    "siem reap": "cambodia",
    "taiwan": "taiwan",
    "langkawi": "langkawi-malaysia",
    "lombok": "lombok-indonesia",
    "mandalika": "lombok-indonesia",
    "komodo": "komodo-flores-indonesia",
    "labuan bajo": "komodo-flores-indonesia",
    "flores": "komodo-flores-indonesia",
    "sumba": "komodo-flores-indonesia",
    "raja ampat": "raja-ampat-indonesia",
    "sorong": "raja-ampat-indonesia",
    "riau": "riau-islands-indonesia",
    "batam": "riau-islands-indonesia",
    "bintan": "riau-islands-indonesia",
    "bbt": "riau-islands-indonesia",
    "anambas": "riau-islands-indonesia",
    "bawah": "riau-islands-indonesia",
    "natuna": "riau-islands-indonesia",
    "toba": "lake-toba-samosir-indonesia",
    "lake toba": "lake-toba-samosir-indonesia",
    "banda": "banda-maluku-indonesia",
    "maluku": "banda-maluku-indonesia",
    "ambon": "banda-maluku-indonesia",
    "wakatobi": "wakatobi-southeast-sulawesi-indonesia",
    "derawan": "derawan-berau-east-kalimantan-indonesia",
    "berau": "derawan-berau-east-kalimantan-indonesia",
    "karimunjawa": "karimunjawa-central-java-indonesia",
    "likupang": "likupang-north-sulawesi-indonesia",
    "bunaken": "likupang-north-sulawesi-indonesia",
    "brunei": "brunei-darussalam",
    "bsb": "brunei-darussalam",
    "bandar seri begawan": "brunei-darussalam",
    "miri": "brunei-darussalam",
    "hk": "hong-kong",
    "hong kong": "hong-kong",
    "hkg": "hong-kong",
    "macau": "hong-kong",
    "japan": "japan",
    "jp": "japan",
    "tokyo": "japan",
    "setouchi": "japan",
    "okinawa": "japan",
    "korea": "korea",
    "kr": "korea",
    "seoul": "korea",
    "busan": "korea",
    "jeju": "korea",
    "istanbul": "turkey",
    "ist": "turkey",
    "bodrum": "bodrum-turkey",
    "aegean": "cesme-izmir-turkey",
    "antalya": "antalya-turkey",
    "marmaris": "bodrum-turkey",
    "colombo": "colombo-sri-lanka",
    "sri lanka": "colombo-sri-lanka",
    "sri-lanka": "colombo-sri-lanka",
    "cmb": "colombo-sri-lanka",
    "galle": "colombo-sri-lanka",
}

# Endpoints we deliberately accept as un-resolved (out-of-corpus destinations).
# These are real places that show up in routes but don't have city files yet.
OUT_OF_CORPUS = {
    # MENA gaps
    "khasab", "musandam",          # Oman exclave — may merit cross-ref later
    "ghantoot", "yas",             # AUH↔DXB midpoint / AUH internal
    "sahl hasheesh", "el gouna", "hurghada",   # Egypt pipeline
    "pekanbaru", "siak",           # Sumatran mainland adjacency
    "krabi", "phi phi", "ko lanta", "ko racha",  # Thailand sub-spokes
    "dammam", "al khobar", "eastern province",  # KSA eastern coast no file
    "aden", "yemen",
    "iran", "qeshm", "kish",
    "aqaba", "taba", "tiran", "sanafir", "ras mohammed", "dahab",  # red sea
    "ajman", "umm al quwain", "uaq", "sir bu nair",  # UAE no-file northern
    "delma", "sila", "mugheirah",  # AUH western region
    "kaust", "thuwal", "kaec", "rabigh",   # KSA red sea coastal stubs
    "amaala", "duba", "magna", "leyja", "sharma",  # NEOM cluster sub-resorts (in red-sea/neom files but as POIs)
    "dibba",                       # UAE/Oman border
    "ksa", "eg", "jo", "il",       # country codes
    # SEA gaps
    "pattaya", "ko samet", "koh samet", "hua hin", "pranburi",  # TH gulf
    "ko chang", "koh chang", "trat",
    "alor", "raijua", "savu",                  # E. Nusa Tenggara remote
    "natuna",                                  # in riau file but as POI variant
    "ho chi minh", "da nang", "halong", "ha long", "phu quoc", "con dao",  # VN sub-POIs
    "pangkor", "pulau pangkor",
    "iloilo", "boracay", "siargao", "palawan", "el nido", "coron",  # PH sub-POIs
    "sabang", "weh",  # ID north sumatra
    "iban", "kalimantan",
}

# -----------------------------------------------------------------------------
# Pattern: X ↔ Y (with optional distance and bucket annotations)
# Handles:
#   - **Dubai ↔ Khasab (Musandam, Oman)** (~95 nm) — Quanta-LR wedge
#   - | SG ↔ Bintan (BBT) | ~30 | Pioneer II ... |
#   - SG ↔ Phuket ~470 nm upper-Quanta-LR + refuel
# -----------------------------------------------------------------------------
# Greedy capture, character-class excludes the stop set:
#   |  (table delimiter)
#   ~  (distance prefix)
#   (  (parenthetical qualifier)
#   *  (markdown emphasis close)
#   newline
# Source is captured similarly but reverse-bounded.
ROUTE_PATTERN = re.compile(
    r"(?P<source>[A-Za-z][^|~()*\n↔]{0,60}?)"
    r"\s*↔\s*"
    r"(?P<target>[A-Za-z][^|~()*\n↔]{0,80})"
)
TARGET_QUALIFIER_PATTERN = re.compile(r"\(([^)]{1,80})\)")
# Trim trailing junk from captured target (dashes, "nm", quantity tails)
TARGET_TAIL = re.compile(r"\s*(?:—|--|-\s|\bnm\b|\b\d+\s*nm).*$", re.IGNORECASE)
DISTANCE_PATTERN = re.compile(r"~?\s*(\d{1,4})(?:\s*[–-]\s*\d{1,4})?\s*nm", re.IGNORECASE)
BUCKET_HINTS = [
    ("pioneer ii", "pioneer-ii"),
    ("pioneer-ii", "pioneer-ii"),
    ("edge-of-pioneer", "edge-of-pioneer"),
    ("upper-quanta-lr", "upper-quanta-lr"),
    ("upper quanta-lr", "upper-quanta-lr"),
    ("quanta-lr", "quanta-lr"),
    ("out-of-range", "out-of-range"),
    ("n80", "n80-roadmap"),
    ("n120", "n120-roadmap"),
]


def _normalize(s: str) -> str:
    """Lowercase, strip markdown emphasis/whitespace/punctuation noise."""
    s = s.lower().strip()
    s = re.sub(r"[*_`]", "", s)
    s = re.sub(r"\s+", " ", s)
    s = s.strip(" .,;:!?-—–")
    return s


def build_name_index(nodes: list[dict]) -> tuple[dict, dict, dict]:
    """
    Returns (city_index, poi_exact, poi_tokens)
        city_index: alias -> city_id
        poi_exact: normalized full name -> [(poi_id, parent_city_id), ...]
        poi_tokens: leading-token-prefix -> [(poi_id, parent_city_id, full_name), ...]
            e.g. "Saadiyat Island Yacht Club" indexes under
                 "saadiyat", "saadiyat island", "saadiyat island yacht", ...
    """
    city_index = dict(CITY_ALIASES)
    poi_exact = defaultdict(list)
    poi_tokens = defaultdict(list)
    for n in nodes:
        if n["type"] == "city":
            city_index.setdefault(_normalize(n["name"]), n["id"])
            city_index.setdefault(n["id"], n["id"])
        elif n["type"] == "poi":
            name = _normalize(n["name"])
            name_simple = re.sub(r"\s*\([^)]*\)", "", name).strip()
            parent = n.get("anchor_node_id")
            poi_exact[name].append((n["id"], parent))
            if name_simple != name:
                poi_exact[name_simple].append((n["id"], parent))
            # Also index every leading-token prefix for fuzzy matching
            # e.g. "saadiyat island yacht club" → saadiyat, saadiyat island, ...
            tokens = name_simple.split()
            for i in range(1, len(tokens) + 1):
                prefix = " ".join(tokens[:i])
                poi_tokens[prefix].append((n["id"], parent, name_simple))
            # And every token individually for substring match
            for t in tokens:
                if len(t) >= 4:   # avoid noise from short words
                    poi_tokens[t].append((n["id"], parent, name_simple))
    return city_index, dict(poi_exact), dict(poi_tokens)


def resolve_endpoint(raw: str, source_city: str, city_idx: dict,
                     poi_exact: dict, poi_tokens: dict) -> tuple[str | None, str]:
    """
    Returns (node_id, match_type) where match_type ∈
        {city, city-partial, poi, poi-prefix, poi-token, self,
         out-of-corpus, unresolved}
    """
    n = _normalize(raw)
    if not n:
        return (None, "empty")
    # Strip leading prose noise like "no ", "cf. ", "shortest "
    n = re.sub(r"^(?:no |cf\. |shortest |the |a |an )+", "", n).strip()
    # 1. Exact city alias
    if n in city_idx:
        cid = city_idx[n]
        return (cid, "self" if cid == source_city else "city")
    # 2. POI exact name match (prefer same-file for intra-city routes,
    #    otherwise cross-file)
    if n in poi_exact:
        candidates = poi_exact[n]
        same_file = [p for p in candidates if p[1] == source_city]
        chosen = same_file[0] if same_file else candidates[0]
        return (chosen[0], "poi")
    # 3. Split on "/", ",", " or " — try each segment
    for segment in re.split(r"[/,]| or | and ", n):
        seg = segment.strip()
        if not seg:
            continue
        if seg in city_idx:
            cid = city_idx[seg]
            return (cid, "self" if cid == source_city else "city-partial")
        if seg in poi_exact:
            candidates = poi_exact[seg]
            same_file = [p for p in candidates if p[1] == source_city]
            chosen = same_file[0] if same_file else candidates[0]
            return (chosen[0], "poi")
        if seg in poi_tokens:
            candidates = poi_tokens[seg]
            same_file = [p for p in candidates if p[1] == source_city]
            chosen = same_file[0] if same_file else candidates[0]
            return (chosen[0], "poi-prefix")
    # 4. POI token-prefix (e.g. "saadiyat" matches "Saadiyat Island Yacht Club")
    if n in poi_tokens:
        candidates = poi_tokens[n]
        same_file = [p for p in candidates if p[1] == source_city]
        chosen = same_file[0] if same_file else candidates[0]
        return (chosen[0], "poi-prefix")
    # 5. First-token fallback: try just the first word
    first = n.split()[0] if n.split() else ""
    if first and first in poi_tokens:
        candidates = poi_tokens[first]
        same_file = [p for p in candidates if p[1] == source_city]
        chosen = same_file[0] if same_file else candidates[0]
        return (chosen[0], "poi-token")
    if first and first in city_idx:
        cid = city_idx[first]
        return (cid, "self" if cid == source_city else "city-partial")
    # 6. Out-of-corpus acknowledged
    if any(oc in n for oc in OUT_OF_CORPUS):
        return (None, "out-of-corpus")
    return (None, "unresolved")


def extract_routes_section(text: str) -> tuple[str | None, int | None]:
    """Find '## Waterways & Routes' block. Returns (section_text, start_line)."""
    lines = text.splitlines()
    start = None
    end = len(lines)
    for i, line in enumerate(lines):
        if re.match(r"^##\s+.*Waterways.*Routes", line, re.IGNORECASE):
            start = i
            continue
        if start is not None and re.match(r"^##\s+(?!.*Waterways)", line):
            end = i
            break
    if start is None:
        return (None, None)
    return ("\n".join(lines[start:end]), start + 1)


def classify_bucket(line: str) -> str | None:
    low = line.lower()
    for hint, label in BUCKET_HINTS:
        if hint in low:
            return label
    return None


def extract_route_mentions(section_text: str, section_start_line: int):
    """Yield dicts: {source_raw, target_raw, distance_nm, bucket, notes, line_no}."""
    for offset, line in enumerate(section_text.splitlines()):
        if "↔" not in line:
            continue
        # Look for target qualifier (e.g. "(Musandam, Oman)") elsewhere on the line
        qual_m = TARGET_QUALIFIER_PATTERN.search(line)
        tgt_qual = qual_m.group(1) if qual_m else ""
        for m in ROUTE_PATTERN.finditer(line):
            src = m.group("source")
            tgt = m.group("target")
            # Trim markdown emphasis + trailing tails
            src = re.sub(r"[*_`]+", "", src).strip(" .,;:!?-—–")
            tgt = re.sub(r"[*_`]+", "", tgt).strip(" .,;:!?-—–")
            tgt = TARGET_TAIL.sub("", tgt).strip(" .,;:!?-—–")
            dist_m = DISTANCE_PATTERN.search(line)
            dist = int(dist_m.group(1)) if dist_m else None
            bucket = classify_bucket(line)
            yield {
                "source_raw": src,
                "target_raw": tgt,
                "target_qualifier": tgt_qual,
                "distance_nm": dist,
                "bucket": bucket,
                "notes": line.strip(" |*-"),
                "line_no": section_start_line + offset,
            }


def main():
    with open(OUTPUT / "nodes.json") as f:
        nodes_doc = json.load(f)
    with open(OUTPUT / "edges.json") as f:
        edges_doc = json.load(f)

    nodes = nodes_doc["nodes"]
    city_idx, poi_exact, poi_tokens = build_name_index(nodes)
    print(f"Built name index: {len(city_idx)} city aliases, "
          f"{len(poi_exact)} POI exact names, {len(poi_tokens)} token keys")

    # Find source files
    region_dirs = ["mena", "sea", "east-asia", "turkey"]
    new_edges = []
    audit_rows = []
    stats = defaultdict(int)

    for rd in region_dirs:
        d = REGIONS / rd
        if not d.exists():
            continue
        for fp in sorted(d.glob("*.md")):
            source_city = fp.stem
            # Confirm this is in nodes
            if not any(n["id"] == source_city and n["type"] == "city" for n in nodes):
                continue
            text = fp.read_text()
            section, start_line = extract_routes_section(text)
            if not section:
                continue
            for r in extract_route_mentions(section, start_line):
                # Resolve source — usually = source_city (short forms like SG, DXB)
                src_id, src_type = resolve_endpoint(r["source_raw"], source_city,
                                                    city_idx, poi_exact, poi_tokens)
                if src_id is None:
                    src_id, src_type = source_city, "default-source"
                tgt_id, tgt_type = resolve_endpoint(r["target_raw"], source_city,
                                                    city_idx, poi_exact, poi_tokens)
                stats[f"target-{tgt_type}"] += 1
                row = {
                    "source_file": fp.name,
                    "line": r["line_no"],
                    "source_raw": r["source_raw"],
                    "target_raw": r["target_raw"],
                    "source_id": src_id,
                    "target_id": tgt_id,
                    "source_match": src_type,
                    "target_match": tgt_type,
                    "distance_nm": r["distance_nm"],
                    "bucket": r["bucket"],
                    "notes": r["notes"][:200],
                }
                audit_rows.append(row)
                if tgt_id and src_id and src_id != tgt_id:
                    new_edges.append({
                        "id": f"edge-{len(edges_doc['edges']) + len(new_edges) + 1:04d}",
                        "source": src_id,
                        "target": tgt_id,
                        "distance_nm": r["distance_nm"],
                        "platform_bucket": r["bucket"],
                        "notes": r["notes"][:200],
                        "source_file": fp.name,
                        "source_line": r["line_no"],
                        "extraction": "cross-file-resolver-v0.1",
                    })

    # Dedupe: keep first occurrence per (source, target, distance)
    seen = set()
    deduped = []
    for e in new_edges:
        k = (e["source"], e["target"], e["distance_nm"])
        rk = (e["target"], e["source"], e["distance_nm"])
        if k in seen or rk in seen:
            continue
        seen.add(k)
        deduped.append(e)

    print(f"Routes scanned: {len(audit_rows)}")
    print(f"Resolution stats: {dict(stats)}")
    print(f"New cross-file edges (pre-dedupe): {len(new_edges)}")
    print(f"New cross-file edges (post-dedupe): {len(deduped)}")

    # ----------------------------------------------------------------------
    # v9 fix — Cross-cluster sub-cluster POI rewrite.
    #
    # parse_city_files.py converts EVERY row of a city's Sub-clusters table into
    # a synthetic POI child of that city, with `anchor_node_id = source_city`.
    # Many of those rows describe EXTERNAL destinations (e.g. "Dubai (UAE —
    # cross-border)", "Khasab Musandam", "Salalah / Dhofar") that are real
    # cities/POIs in OTHER files. With no OSM hit, apply_coords.py falls back to
    # jittering them around the SOURCE city anchor — producing the v8 audit's
    # 28 route stubs (lines terminate ~0.1-2 nm from source anchor instead of
    # at the real distant destination).
    #
    # Fix: for every synthetic POI whose name resolves via the just-built city/
    # POI name index to a DIFFERENT real node, rewrite the parse_city_files.py
    # edge's `to_node_id` to that real node and prune the orphaned synthetic
    # POI from nodes.json.
    # ----------------------------------------------------------------------
    synth_to_real: dict[str, tuple[str, str]] = {}   # synthetic_poi_id -> (real_node_id, match_type)
    for n in nodes:
        if n.get("type") != "poi":
            continue
        parent = n.get("anchor_node_id")
        if not parent:
            continue
        # Only consider synthetic POIs (id pattern: {parent}__{slug})
        if not n["id"].startswith(parent + "__"):
            continue
        name = n.get("name", "")
        if not name:
            continue
        # Strip noisy qualifiers before resolving, e.g.
        # "Dubai (UAE — cross-border)" -> try "Dubai" first
        candidates = [name]
        # Take pre-paren token
        m = re.match(r"^([^(]{2,80})", name)
        if m:
            candidates.append(m.group(1).strip(" /—-"))
        # For "A ↔ B (qualifier)" patterns (common in Doha file), the
        # external destination is the RHS of ↔.
        for c in list(candidates):
            if "↔" in c:
                parts = c.split("↔")
                if len(parts) >= 2:
                    candidates.append(parts[-1].strip(" /—-()*"))
        # Take first segment of slash-separated names ("Salalah / Dhofar" -> "Salalah")
        for c in list(candidates):
            if "/" in c:
                candidates.append(c.split("/")[0].strip())
            if "—" in c:
                candidates.append(c.split("—")[0].strip())
        seen_cand = set()
        for cand in candidates:
            if cand in seen_cand or not cand:
                continue
            seen_cand.add(cand)
            resolved_id, match_type = resolve_endpoint(
                cand, parent, city_idx, poi_exact, poi_tokens
            )
            if resolved_id and resolved_id != parent and resolved_id != n["id"]:
                # Don't rewrite to another synthetic POI of the SAME source city
                # (would re-introduce the jitter problem).
                rnode = next((x for x in nodes if x["id"] == resolved_id), None)
                if rnode and rnode.get("type") == "poi" \
                        and rnode.get("anchor_node_id") == parent:
                    continue
                synth_to_real[n["id"]] = (resolved_id, match_type)
                break

    # Rewrite edges and add cross_cluster_resolved marker
    n_rewritten = 0
    for e in edges_doc["edges"]:
        tgt = e.get("to_node_id") or e.get("target")
        if tgt in synth_to_real:
            real, mtype = synth_to_real[tgt]
            if "to_node_id" in e:
                e["to_node_id"] = real
            if "target" in e:
                e["target"] = real
            e["cross_cluster_resolved"] = True
            e["cross_cluster_match_type"] = mtype
            n_rewritten += 1

    # Prune the now-orphaned synthetic POIs from nodes.json
    pre_count = len(nodes)
    nodes_doc["nodes"] = [x for x in nodes if x["id"] not in synth_to_real]
    pruned = pre_count - len(nodes_doc["nodes"])
    with open(OUTPUT / "nodes.json", "w") as f:
        json.dump(nodes_doc, f, indent=2, ensure_ascii=False)
    print(f"v9 cross-cluster fix: rewrote {n_rewritten} edges; pruned {pruned} synthetic POIs")

    # Persist
    edges_doc["edges"].extend(deduped)
    edges_doc["_meta"]["cross_file_resolver_run"] = True
    edges_doc["_meta"]["cross_file_edges_added"] = len(deduped)
    edges_doc["_meta"]["cross_cluster_edges_rewritten"] = n_rewritten
    edges_doc["_meta"]["synthetic_pois_pruned"] = pruned
    with open(OUTPUT / "edges.json", "w") as f:
        json.dump(edges_doc, f, indent=2)
    with open(OUTPUT / "edges-cross-file.json", "w") as f:
        json.dump({"edges": deduped}, f, indent=2)

    # Audit report
    lines = ["# Cross-file Edge Resolution Report", ""]
    lines.append(f"**Routes scanned:** {len(audit_rows)}")
    lines.append(f"**New edges emitted:** {len(deduped)}")
    lines.append(f"**Match stats:** {dict(stats)}")
    lines.append("")
    lines.append("## Unresolved targets (need alias map / future city file)")
    lines.append("")
    unresolved = [r for r in audit_rows if r["target_match"] == "unresolved"]
    lines.append(f"Count: {len(unresolved)}\n")
    for r in unresolved[:80]:
        lines.append(f"- `{r['source_file']}:{r['line']}` — `{r['source_raw']} ↔ {r['target_raw']}` ({r['distance_nm']} nm)")
    lines.append("")
    lines.append("## Out-of-corpus targets (acknowledged, no file)")
    ooc = [r for r in audit_rows if r["target_match"] == "out-of-corpus"]
    lines.append(f"Count: {len(ooc)}\n")
    seen_pairs = set()
    for r in ooc:
        k = (r["source_file"], r["target_raw"])
        if k in seen_pairs:
            continue
        seen_pairs.add(k)
        lines.append(f"- `{r['source_file']}` — `{r['target_raw']}`")
    with open(OUTPUT / "edge-resolution-report.md", "w") as f:
        f.write("\n".join(lines))
    print(f"Audit report written: {OUTPUT / 'edge-resolution-report.md'}")


if __name__ == "__main__":
    main()
