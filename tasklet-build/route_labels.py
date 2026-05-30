"""
route_labels.py  —  Clean, human endpoint labels for every route + Quanta-LR endpoint audit.

Root problem (visible in tooltips):
  * Routes can terminate on BPs/sub-points that are SUPPRESSED from the rendered feature
    index, so the front-end falls back to the raw slug id, e.g.
        "Salalah -> salalah-dhofar-oman__hasik"
        "... -> doha-qatar__lusail-...-waldorf-r"   (truncated slug garbage)
  * Quanta-LR (long-haul) routes sometimes end at an obscure sub-point, not a real city,
    so the corridor reads as "going to the middle of nowhere".

Fix (source-agnostic, runs over the FINAL route_features list at build time):
  1. Resolve every endpoint id -> clean human label via:
       (a) node index (city/locale/poi node ids)               -> shortName/name
       (b) BP name index keyed by id / slug(name) / slug(locale) -> BP name
           (handles truncated `city__suffix` slugs by best containment match)
       (c) deterministic prettify fallback (never shows raw `__`/`-`)
  2. Tag each endpoint's PARENT CITY (from_city / to_city) so the render can always present
     a route as City -> City even when an endpoint is a sub-point.
  3. Emit an audit of Quanta-LR routes whose endpoint is NOT a city node, plus Quanta-LR
     routes <= Pioneer range (platform smell) -> for one-by-one curation review.

Adds to each route's properties: from_label, to_label, from_city, to_city, label.
Returns an audit dict.
"""
from __future__ import annotations
import json, re, glob, unicodedata, hashlib
from pathlib import Path


def _slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode("ascii")
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def _short_city(name: str) -> str:
    """Trim a verbose node name to a clean short city label.
    'Salalah + Dhofar (Mirbat / Hasik / ...)' -> 'Salalah'
    'Male / Maldives' -> 'Male';  'Hong Kong' -> 'Hong Kong'
    """
    if not name:
        return name
    s = name.split("(")[0].strip()
    for sep in (" + ", " / ", " — ", " - ", ", "):
        if sep in s:
            s = s.split(sep)[0].strip()
    return s or name


def _short_bp(name: str) -> str:
    """Trim a verbose boarding-point name for tooltip display, keeping the core place.
    'Nuweiba Port (historic EG↔JO Aqaba ferry terminal)' -> 'Nuweiba Port'
    'Shangri-La Boracay Resort jetty (Punta Bunga)'       -> 'Shangri-La Boracay Resort jetty'
    Leaves names without a trailing parenthetical untouched."""
    if not name:
        return name
    s = re.sub(r"\s*\([^()]*\)\s*$", "", name).strip()
    return s or name


def _prettify(token: str) -> str:
    """Last-resort: turn a slug token into a readable label (never shows raw __/-)."""
    token = token.replace("__", " — ").replace("_", " ").replace("-", " ").strip()
    # title-case but keep common acronyms uppercase
    ACR = {"rsg", "neom", "ksa", "uae", "ph", "prd", "cbd", "np", "mpa", "bvi", "usvi"}
    words = []
    prev = None
    for w in token.split():
        if w.lower() == prev:      # drop consecutive duplicate words ("Lusail Lusail" -> "Lusail")
            continue
        prev = w.lower()
        words.append(w.upper() if w.lower() in ACR else (w[:1].upper() + w[1:]))
    # drop a trailing orphan 1-char token left by slug truncation ("... Waldorf R" -> "... Waldorf")
    if len(words) > 1 and len(words[-1]) == 1:
        words = words[:-1]
    return " ".join(words)


def build_index(node_by_id: dict, bp_dir, bp_city_map: dict | None = None) -> dict:
    """Return resolver dicts: node names + BP name index (multiple key forms).

    bp_city_map: {bp_file_slug -> node_id}. Lets us index a city's BPs under its NODE id
    too, so endpoint ids like 'doha-qatar__lusail' resolve even though the BP file is
    'doha-boarding-points.json' (file slug 'doha', node id 'doha-qatar').
    """
    bp_city_map = bp_city_map or {}
    nodes = {}
    for nid, n in node_by_id.items():
        nm = n.get("shortName") or n.get("name")
        if nm:
            nodes[nid] = nm

    # BP index: (city_slug -> list of bp dicts) + global id->name
    bp_by_id = {}
    bp_by_city = {}
    city_of_bp = {}          # bp id / bp-hash -> parent city display name
    city_name_by_slug = {}
    for fp in glob.glob(str(Path(bp_dir) / "*.json")):
        try:
            d = json.loads(Path(fp).read_text())
        except Exception:
            continue
        file_slug = Path(fp).name.replace("-boarding-points.json", "").replace(".json", "")
        cslug = _slug(file_slug)
        cname = d.get("city_name") or d.get("city") or _prettify(cslug)
        # all alias slugs this city's BPs should be reachable under
        aliases = {cslug}
        cid = d.get("city_id")
        if cid:
            aliases.add(_slug(cid))
        node_id = bp_city_map.get(file_slug) or bp_city_map.get(cslug)
        if node_id:
            aliases.add(_slug(node_id))
            nm_node = nodes.get(node_id)
            if nm_node:
                cname = nm_node
        for a in aliases:
            city_name_by_slug.setdefault(a, cname)
        lst = []
        for bp in d.get("boarding_points", []):
            nm = bp.get("name")
            if not nm:
                continue
            rec = {
                "name": nm,
                "id": bp.get("id") or "",
                "name_slug": _slug(nm),
                "locale_slug": _slug(bp.get("linked_locale") or ""),
            }
            lst.append(rec)
            if rec["id"]:
                bp_by_id[rec["id"]] = nm
                city_of_bp[rec["id"]] = cname
            # Rule C: also index under the rendered pin hash so route endpoints of the
            # form `bp-<md5[:10]>` (produced by build.py / route_network _bp_hash) resolve
            # to the real BP name (and real parent city) instead of prettifying to
            # "Bp <hash>". This fixes ~900 local-mesh capillary route labels.
            if node_id:
                raw = (rec["id"] or nm) + node_id
                bp_hash = "bp-" + hashlib.md5(raw.encode("utf-8")).hexdigest()[:10]
                bp_by_id[bp_hash] = nm
                city_of_bp[bp_hash] = cname
        for a in aliases:
            bp_by_city[a] = lst
    return {
        "nodes": nodes,
        "bp_by_id": bp_by_id,
        "bp_by_city": bp_by_city,
        "city_of_bp": city_of_bp,
        "city_name_by_slug": city_name_by_slug,
    }


def _resolve_suffix(suffix: str, bps: list) -> str | None:
    """Best-match a (possibly truncated) `__suffix` slug against a city's BP list."""
    if not suffix or not bps:
        return None
    # exact name/locale slug
    for b in bps:
        if suffix == b["name_slug"] or suffix == b["locale_slug"]:
            return b["name"]
    # containment / prefix (handles truncated slugs like '...-waldorf-r')
    best = None
    best_len = 0
    for b in bps:
        for cand in (b["name_slug"], b["locale_slug"]):
            if not cand:
                continue
            if cand.startswith(suffix) or suffix.startswith(cand) or suffix in cand or cand in suffix:
                overlap = min(len(cand), len(suffix))
                if overlap > best_len:
                    best_len, best = overlap, b["name"]
    return best


def resolve(endpoint_id: str, idx: dict):
    """Return (label, parent_city_name, is_city_node)."""
    if not endpoint_id:
        return ("", "", False)
    # 1) node id (city/locale/poi)
    if endpoint_id in idx["nodes"]:
        nm = idx["nodes"][endpoint_id]
        # is it a city slug with no __? treat as city
        is_city = "__" not in endpoint_id
        return (nm, nm if is_city else idx["city_name_by_slug"].get(_slug(endpoint_id.split("__")[0]), nm), is_city)
    # 2) BP id directly (raw id or rendered bp-<hash>) — resolve real parent city,
    #    never prettify the hash into a bogus "Bp <hash>" city.
    if endpoint_id in idx["bp_by_id"]:
        nm = idx["bp_by_id"][endpoint_id]
        city = idx.get("city_of_bp", {}).get(endpoint_id) or ""
        return (nm, city, False)
    # 3) city__suffix form
    if "__" in endpoint_id:
        cslug, suffix = endpoint_id.split("__", 1)
        cslug_s = _slug(cslug)
        # placeholder prefixes (e.g. '_ww', '_intl') carry no real city -> no parent city
        placeholder = cslug.startswith("_") or cslug_s in ("ww", "intl", "tbd")
        city_name = "" if placeholder else (idx["city_name_by_slug"].get(cslug_s) or idx["nodes"].get(cslug) or _prettify(cslug))
        bps = idx["bp_by_city"].get(cslug_s, [])
        nm = _resolve_suffix(_slug(suffix), bps)
        if nm:
            return (nm, city_name, False)
        return (_prettify(suffix), city_name, False)
    # 4) bare slug -> prettify (also try city map)
    nm = idx["city_name_by_slug"].get(_slug(endpoint_id)) or _prettify(endpoint_id)
    return (nm, nm, "__" not in endpoint_id)


PIONEER_MAX_NM = 70.0


def apply_labels(route_features: list, node_by_id: dict, bp_dir, bp_city_map: dict | None = None) -> dict:
    idx = build_index(node_by_id, bp_dir, bp_city_map)
    audit = {
        "total": len(route_features),
        "qlr_total": 0,
        "qlr_noncity_endpoint": [],   # Quanta-LR not terminating at a city node
        "qlr_under_pioneer": [],      # Quanta-LR <= 70 nm (platform smell)
        "unresolved": [],             # endpoints that still prettify (no name match)
    }
    def _contains(a, b):
        return bool(a) and bool(b) and _slug(b) in _slug(a)

    for f in route_features:
        p = f["properties"]
        fl, fc, f_iscity = resolve(p.get("from"), idx)
        tl, tc, t_iscity = resolve(p.get("to"), idx)
        fc, tc = _short_city(fc), _short_city(tc)
        # endpoint own label: if it's a city node, use the short city name (not verbose);
        # otherwise trim the verbose boarding-point parenthetical for readability.
        if f_iscity:
            fl = fc
        else:
            fl = _short_bp(fl)
        if t_iscity:
            tl = tc
        else:
            tl = _short_bp(tl)
        p["from_label"] = fl
        p["to_label"] = tl
        p["from_city"] = fc
        p["to_city"] = tc
        # Canonical tooltip label — always reads City -> City, sub-point in parens only
        # when it adds information (intra-city routes show the two sub-points directly).
        def _disp(label, city, is_city):
            if is_city or not city or label == city or _contains(label, city):
                return label
            return f"{label} ({city})"
        if fc and fc == tc:
            # intra-city: both endpoints inside one city
            if f_iscity and not t_iscity:        # hub -> sub-point
                p["label"] = f"{fc} → {tl}"
            elif t_iscity and not f_iscity:       # sub-point -> hub
                p["label"] = f"{fl} → {tc}"
            else:                                 # two sub-points: prefix city once
                p["label"] = f"{fc}: {fl} → {tl}"
        else:
            p["label"] = f"{_disp(fl, fc, f_iscity)} → {_disp(tl, tc, t_iscity)}"
        # audit Quanta-LR
        if p.get("platform") == "Quanta-LR":
            audit["qlr_total"] += 1
            row = {"id": p.get("id"), "from": p.get("from"), "to": p.get("to"),
                   "from_label": fl, "to_label": tl, "from_city": fc, "to_city": tc,
                   "distance_nm": p.get("distance_nm"), "edge_class": p.get("edge_class")}
            if not (f_iscity and t_iscity):
                audit["qlr_noncity_endpoint"].append(row)
            if p.get("distance_nm") is not None and p["distance_nm"] <= PIONEER_MAX_NM:
                audit["qlr_under_pioneer"].append(row)
        # unresolved smell: label equals a prettified raw slug containing original tokens
        for raw, lab in ((p.get("from"), fl), (p.get("to"), tl)):
            if raw and "__" in raw and lab and _slug(lab) and _slug(lab) in _slug(raw) and lab == _prettify(raw.split("__", 1)[1]):
                audit["unresolved"].append({"id": p.get("id"), "raw": raw, "label": lab})
    return audit
