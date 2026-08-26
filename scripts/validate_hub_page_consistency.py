#!/usr/bin/env python3
"""Drift gate: every corridor figure on any RAK archetype page must match
hub.json corridor_table (the single corridor source). Fails the build on drift.
Usage: python3 scripts/validate_hub_page_consistency.py [hub-dir]"""
import json, re, sys
from pathlib import Path

hub_dir = Path(sys.argv[1] if len(sys.argv) > 1 else 'employer-hub/hubs/ras-al-khaimah')
hub = json.loads((hub_dir/'hub.json').read_text())
ct = {r['id']: r for r in hub.get('corridor_table', {}).get('corridors', [])}
if not ct:
    print('FAIL: hub.json has no corridor_table'); sys.exit(1)

# 1) corridor_table hand rows must match hub lines
segs = {}
for ln in hub['lines']:
    for s in ln['segments']:
        segs[(s['from'], s['to'])] = s['distance_nm']
spn = [s['distance_nm'] for s in hub['lines'][0]['segments']]
errors = []
def close(a, b, tol): return abs(a-b) <= tol
checks = {'SPN-1': round(sum(spn), 2), 'MRJ-1': spn[0], 'MNA-1': spn[2],
          'NTH-1a': segs.get(('qawasim-1','rams')), 'NTH-1b': segs.get(('rams','al-ghalilah')), 'NTH-1c': segs.get(('al-ghalilah','shaam'))}
for cid, want in checks.items():
    if want is None: errors.append(f'{cid}: expected segment missing from hub lines'); continue
    if not close(ct[cid]['path_nm'], want, 0.05): errors.append(f'{cid}: table {ct[cid]["path_nm"]} != lines {want}')

# 2) page claims: "<CID> ... <nm> nm (≈NN min ... ≈NN min ...)" and "about NN minutes"
tolerable = {'min': 3, 'nm': 0.31}
for page in ('public-partners.json', 'fleet-investors.json'):
    p = hub_dir/page
    if not p.exists(): continue
    raw = p.read_text()
    for m in re.finditer(r'\b(MRJ-1|MNA-1|SPN-1|HER-1|NTH-1[abc]?|GTW-1[abc])\b[^.\u00b7]{0,140}?(\d+(?:\.\d+)?) ?nm', raw):
        cid, val = m.group(1), float(m.group(2))
        if cid == 'NTH-1': continue
        if cid in ct and not close(val, ct[cid]['path_nm'], tolerable['nm']):
            errors.append(f'{page}: {cid} claims {val} nm, table says {ct[cid]["path_nm"]}')
    for m in re.finditer(r'\b(MRJ-1|MNA-1|SPN-1|HER-1)\b[^.\u00b7]{0,160}?\u2248(\d+) min', raw):
        cid, mn = m.group(1), int(m.group(2))
        r = ct.get(cid)
        if r and not (close(mn, r['min_day_30kn'], tolerable['min']) or close(mn, r['min_night_20kn'], tolerable['min'])):
            errors.append(f'{page}: {cid} claims \u2248{mn} min, table day/night = {r["min_day_30kn"]}/{r["min_night_20kn"]}')
    for m in re.finditer(r'about (\d+) minutes', raw):
        mn = int(m.group(1))
        r = ct['SPN-1']
        if not (close(mn, r['min_day_30kn'], tolerable['min']) or close(mn, r['min_night_20kn'], tolerable['min'])):
            errors.append(f'{page}: "about {mn} minutes" matches neither SPN-1 day {r["min_day_30kn"]} nor night {r["min_night_20kn"]}')
    # stale pre-unification estimates must not reappear
    for stale in ('4.0 nm', '10.0 nm', '17.0 nm', '13.0 nm', '17.17'):
        if stale in raw: errors.append(f'{page}: stale pre-unification figure "{stale}" present')

if errors:
    print('FAIL — corridor drift detected:')
    for e in errors: print(' -', e)
    sys.exit(1)
print(f'PASS — {len(checks)} table rows verified against hub lines; page claims consistent with corridor_table.')
