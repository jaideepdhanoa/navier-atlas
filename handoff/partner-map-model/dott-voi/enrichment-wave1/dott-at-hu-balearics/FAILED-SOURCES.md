# Failed and held sources

**Accessed:** 2026-07-10

## Repository blocker

- **`/tmp/navier-atlas`** — path did not exist in this subagent runtime. As a result, current `data-clean/CLUSTERS.json`, `ROUTES.json`, `FEATURES_BY_TYPE.json`, city/cluster briefs, boarding-point registries, and Dott/Voi partner files could not be inspected. The prior audit baseline commit (`8adf384da2214629b8b672b897fcd91011d3040d`) and its verified cluster list were used only as a constrained fallback.

## Source/landing holds

- **Klopeiner See / Klopein:** official regional tourism establishes the lake, but no authoritative specific pier/terminal/marina was established. BP is null; no route proposed.
- **Dunaújváros:** searches exposed general Danube/MAHART material but no current authoritative, specific passenger landing tied to the city. BP is null; no route proposed.
- **Győr:** operator-level sightseeing evidence surfaced, but no sufficiently authoritative municipal/port/transit source for a specific BP was established. BP is null; no route proposed.
- **Komárom:** no current authoritative specific passenger landing was established. BP is null; no route proposed.
- **Hörbranz and Lochau:** Lake Constance relevance is sound, but authoritative specific local landing evidence was not established in this pass. BPs are null.
- **Hard:** the municipality proves `Hafen Hard` as a real marina. It does not by itself prove scheduled passenger service or transfer rights; the Bregenz–Hard leg is a held research candidate.
- **Linz:** official mooring directory proves Donaustation Linz 1 and Linz 32; direct service between them was not proven. Route remains a held research candidate.

## Access/format limitations

- Some official operator sites were discoverable through indexed snippets but did not expose enough machine-readable detail for every stop. No missing detail was filled by guesswork.
- Search-engine snippets and secondary aggregators were not used as final BP authority where a primary source was missing.
- No coordinates were taken from maps or inferred.
