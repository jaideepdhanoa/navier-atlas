# Gold #68 — Grab partner re-aggregate splice (2026-06-12)

**Scope.** Single overlay: `partner-pitch/partners/grab.json` (mirrored to `data-clean/partners/grab.json`).
Full-scope post-aggregate-rerun rebuild — same headline MID **$985M**, same grounded base (231 `committed_grounded` summed across markets[]). No geometry delta; no new corridors; no label fixes.

**Surface unchanged.**
- ROUTES: 5,297 (unchanged from #67)
- CLUSTERS: 75 (unchanged)
- POIs: 11,374 (unchanged)
- city_briefs / cluster_briefs: 189 / 32 (unchanged)

**Economics sidecar.** Regenerated against the existing gold geometry.
- Records (route-pinned): **107** (was 109 at #67)
- Pending (no gold route): **22**
- By partner: careem=14, grab=41, jih-global=43, qatar=3, red-sea-global=2, saudi-redsea-pif=4
- Grounded / Estimated: 75 / 25

**Gates (run before seal).**
- `gate_endpoint_labels.py`: **PASS** (0 hard flags; weak single-token binds unchanged from #67)
- `gate_city_ids.py`: **PASS** — 198 valid nodes, 5,297 routes, 75 clusters all resolve
- `datastore_audit.py`: source-tree pre-existing FEATURES-vs-SEAL drift noted (does not block; ship surface inside zip is internally consistent)

**SEAL.**
- `sidecars.economics_by_route_id.json.sha256` updated.
- `meta.gold = "#68"`; meta.note records the splice and counts.
- Other blob hashes (ROUTES / CLUSTERS / FEATURES / STORIES / VESSEL_SPECS) carried verbatim from #67.

**Mechanics.** LB-67 SAFE-RESEAL: unzipped the prior gold zip (`navier-export-20260612T035824Z.zip`) into a /tmp stage, overlaid ONLY the three changed blobs (`partners/grab.json`, `economics_by_route_id.json`, `SEAL.json`), re-zipped. No source-tree dirty walks.

**Not done (parent owns).** GOLD-COPY.txt NOT flipped. No Drive upload. No Slack post. Parent promotes.
