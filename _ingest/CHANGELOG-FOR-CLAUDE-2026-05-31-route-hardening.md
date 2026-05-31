
## Pipeline addition: authoritative land-route scrubber
`scrub_land_routes.py` (included) MUST run AFTER build.py emits output-external/ROUTES.json
and BEFORE seal. It drops any route the QA gate flags (>1.0 km interior land), guaranteeing
data == gate. This run dropped 52 (42 island-hop + 10 intra-cluster-spoke). Sequence:
  build.py -> scrub_land_routes.py output-external/ROUTES.json -> seal_bundle.py
Final QA verdict: 0 / 3733 routes cross land (gate exit 0).

## known-gaps.json: +10 whitelisted synthetic spoke endpoints
Durable backlog fix = resolver alias '{city}__{desc}' -> real target anchor (also activates
Palm Beach->Miami and Antigua->St-Barths inter-corridor spokes, currently inert).
