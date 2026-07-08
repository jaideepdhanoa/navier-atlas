#!/usr/bin/env python3
"""Partner-facing copy gate — scans data-clean/partners/*.json for internal
pipeline language in partner-visible fields.

Rule (see partner-proposal-parity playbook): partner proposals are sales
surfaces. Internal taxonomy — Atlas, Grok, Tasklet, seals, minting, binding,
route_ids, evidence tiers, display-ready, model cascade, "brief-only",
"held null" — must never appear in fields the renderer displays.

Calibrated: product names (Pioneer II, Quanta-LR, N30), normal English uses of
"spine"/"pipeline"/"registry", machine-config subtrees (network_footprint,
growth_case, featured_routes, _-prefixed provenance) are all allowed.

Exit 0 = clean. Exit 1 = leaks found (listed). Run as a seal/PR gate.
"""
import json, re, os, glob, sys

JARGON = re.compile(
    r'\b(atlas|grok|tasklet|geometry[- _]seal\w*|sealed\s+(?:atlas\s+)?geometry|'
    r'mint(?:ed|ing)?\s+(?:markets?|list|corridors?|the)|exact[- ]bind\w*|'
    r'route[- _]ids?|city[- _]ids?|\bBPs\b|held[- ]null|honest[- ]null|held null|'
    r'evidence[- _]tiers?|display[- _]ready|country[- _]supported|economics[- _]ready|'
    r'model[- _]cascad\w*|economics[- _]status|grounded\s+floors?|'
    r'brief[- ]only|sub[- ]pages?|seal(?:ed|ing)?\s+(?:gates?|pass|status)|'
    r'geometry\s+(?:pass|pending|deepen)|pending\s+grok|data[- ]clean)\b',
    re.IGNORECASE)

# machine/config keys whose values are consumed by code, not displayed as prose
INTERNAL_KEYS = {
    'route_id','route_ids','id','slug','partner_id','cluster_id','city_id',
    'market_group','map_scope','logo','archetype','economics_url','deck_url',
    'source','source_url','sources','fleet_basis','capture_rate','scope_rule',
    'from_node_id','to_node_id','model_link','registry_key','render','tier',
    'platform','anchor_cities','cities','layout','display','category'}

# subtrees never rendered as partner prose
SKIP_SUBTREES = {'growth_case','_provenance','featured_routes','wow_corridors',
                 '_map_scope','network_footprint'}

# machine status tokens that must not render as chips (markets[].status is displayed)
MACHINE_CHIP = re.compile(r'^[a-z0-9]+(_[a-z0-9]+)+$')


def is_internal_key(k):
    return k.startswith('_') or k in INTERNAL_KEYS


def scan_file(fp):
    pid = os.path.basename(fp)[:-5]
    d = json.load(open(fp))
    hits = []

    def walk(node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                if k in SKIP_SUBTREES or is_internal_key(k):
                    continue
                walk(v, path + [k])
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, path + [str(i)])
        elif isinstance(node, str):
            for m in JARGON.finditer(node):
                hits.append((pid, '.'.join(path), m.group(0), node[:140]))

    walk(d, [])
    # markets[].status renders as a visible chip — no machine tokens
    for m in d.get('markets') or []:
        st = m.get('status')
        if isinstance(st, str) and MACHINE_CHIP.match(st):
            hits.append((pid, f"markets[{m.get('id')}].status", 'machine-token chip', st))
    return hits


def main():
    files = sys.argv[1:] or sorted(glob.glob('data-clean/partners/*.json'))
    total = []
    for fp in files:
        total.extend(scan_file(fp))
    if total:
        print(f"FAIL — {len(total)} internal-jargon leak(s) in partner-visible fields:\n")
        for pid, path, term, ctx in total:
            print(f"  [{pid}] {path} — matched '{term}'")
            print(f"      {ctx}")
        sys.exit(1)
    print(f"PASS — 0 internal-jargon leaks across {len(files)} partner file(s).")


if __name__ == '__main__':
    main()
