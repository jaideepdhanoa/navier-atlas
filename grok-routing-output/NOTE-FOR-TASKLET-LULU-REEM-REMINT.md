# Note for Tasklet — Lulu + Reem BPs missing from pilot #79ak (re-mint request)

**From:** Grok (Jaideep lane)  
**Date:** 2026-06-18  
**Context:** Phase 3 CI pilot held 3 synthesize routes (`hold_synthesize_phantom` in `APPLY-LEDGER.json`). Grok agrees with the hold on the **pilot substrate** — but evidence shows these boarding points **were minted in an earlier gold bite and appear to have been dropped** from the #79ak graph Tasklet shipped in `grok-phase3-ci-pilot-2026-06-18.zip`. Requesting a small **re-mint / restore bite** so the 3 held geometries can land in a follow-up seal.

---

## Ask (one bite)

1. **Restore** `bp-31b06c534d` and `bp-f47f75836a` into `FEATURES_BY_TYPE.json` using the **exact records below** (same ids, same coords — from gold #79ac / `gold-export-79ak-1`).
2. **Optionally restore** the two historical `rn-*` spokes that referenced them (if still gate-clean): `rn-4d0113ef1fd5`, `rn-4a56839963b5`.
3. **Re-seal** (suggest `#79am`) and ping Grok — we will apply the **3 held synthesize geometries** from `route-solutions-synthesize-remapped.jsonl` with endpoint snap to the restored `bp-*` coords.

---

## Why the pilot held (correct on that substrate)

Apply binds route endpoints to existing `bp-*` rows in `FEATURES_BY_TYPE`. The pilot `#79ak` substrate has **neither** node:

| Check | Pilot `#79ak` (`grok-phase3-ci-pilot` bundle) |
|-------|-----------------------------------------------|
| `bp-31b06c534d` Lulu Island Jetty | **Absent** from `FEATURES_BY_TYPE.json` |
| `bp-f47f75836a` Reem Island Marina | **Absent** from `FEATURES_BY_TYPE.json` |
| `rn-4d0113ef1fd5` Marina Mall → Lulu | **Absent** from `ROUTES.json` |
| `rn-4a56839963b5` Marina Mall → Reem | **Absent** from `ROUTES.json` |
| Nearest UAE BP to Grok `ad-lulu-island` slug | ~2.5 km |
| Nearest UAE BP to Grok `ad-reem-island` slug | ~1.6 km (wrong place) |

Geometries are **not** the problem — all 3 are `qa_pass: true` under LB-224 v2 gate.

---

## Regression evidence (nodes existed before)

### Original mint — gold **#79ac** (2026-06-16)

`data-clean/CHANGELOG-FOR-CLAUDE-2026-06-16-uae-p2p3-abu-dhabi-islands.md`:

- `bp-31b06c534d` **Lulu Island Jetty** `[54.3475, 24.4945]` — Nominatim+Mapbox <1nm, conf 0.95
- `bp-f47f75836a` **Reem Island Marina (Najmat / Marina Square)** `[54.394, 24.4949]` — conf 0.95
- `rn-4d0113ef1fd5` Marina Mall / Breakwater → Lulu Island Jetty (1.7 nm)
- `rn-4a56839963b5` Marina Mall / Breakwater → Reem Island Marina (7.1 nm)

### Still present in other trees Grok can read

| Source | Routes | Lulu/Reem BPs |
|--------|--------|---------------|
| Pilot `#79ak` (CI apply substrate) | 5411 | **Absent** |
| `gold-export-79ak-1` ingest | — | **Present** (full Feature records below) |
| Local `data-clean/` (workspace) | 5199 | **Present** |

Economics sidecar still names the corridors (`economics_by_route_id.json`):

- `rn-4d0113ef1fd5` — Marina Mall / Breakwater Marina → Lulu Island Jetty
- `rn-4a56839963b5` — Marina Mall / Breakwater Marina → Reem Island Marina (Najmat / Marina Square)

**Hypothesis for Tasklet:** island mint from #79ac did not survive into the 5411-route #79ak lineage the pilot ships (scrub / splice / branch divergence). Looks accidental, not intentional deprecation — no changelog entry retires these BPs.

---

## Re-mint payloads (copy-paste ready — preserve ids)

Sourced from `_ingest/gold-export-79ak-1/data-clean/FEATURES_BY_TYPE.json` (byte-stable Feature shape):

### `bp-31b06c534d` — Lulu Island Jetty

```json
{
  "type": "Feature",
  "geometry": { "type": "Point", "coordinates": [54.3475, 24.4945] },
  "properties": {
    "id": "bp-31b06c534d",
    "type": "poi",
    "name": "Lulu Island Jetty",
    "shortName": "Lulu Island",
    "parent_city_id": "abu-dhabi-uae",
    "bp_type": "public_pier",
    "coords_resolved": true,
    "confidence": "medium",
    "status": "operational",
    "display_type": "public_pier",
    "source_url": null,
    "last_enriched": "2026-06-16T19:55:00Z",
    "_geocode_q": "Lulu Island, Abu Dhabi, UAE",
    "fullName": "Lulu Island Jetty",
    "tier_sort_key": 5
  }
}
```

### `bp-f47f75836a` — Reem Island Marina

```json
{
  "type": "Feature",
  "geometry": { "type": "Point", "coordinates": [54.394, 24.4949] },
  "properties": {
    "id": "bp-f47f75836a",
    "type": "poi",
    "name": "Reem Island Marina (Najmat / Marina Square)",
    "shortName": "Reem Island",
    "parent_city_id": "abu-dhabi-uae",
    "bp_type": "marina",
    "coords_resolved": true,
    "confidence": "medium",
    "status": "operational",
    "display_type": "marina",
    "source_url": null,
    "last_enriched": "2026-06-16T19:55:00Z",
    "_geocode_q": "Najmat Marina, Al Reem Island, Abu Dhabi, UAE",
    "fullName": "Reem Island Marina (Najmat / Marina Square)",
    "tier_sort_key": 5
  }
}
```

> **Relevance:** prior mint used `status: operational` with no `relevance: hide`. If Tasklet policy prefers `hide` for Lulu (undeveloped 2026), say so — Grok will still apply geometry to whichever coords you seal.

---

## 3 held synthesize routes (ready after re-mint)

| From (Grok slug) | To (Grok slug) | Live `bp-*` after restore | `qa_pass` | Dist (nm) | Apply note |
|------------------|----------------|---------------------------|-----------|-----------|------------|
| `ad-lulu-island` | `ad-emirates-palace-marina` | `bp-31b06c534d` → `bp-14c19a643c` | true | 4.18 | Snap **from** vertex to `[54.3475, 24.4945]` |
| `ad-saadiyat-beach-club` | `ad-lulu-island` | `bp-5e6f444b82` → `bp-31b06c534d` | true | 7.02 | Snap **to** vertex to `[54.3475, 24.4945]` |
| `ad-saadiyat-marina` | `ad-reem-island` | `bp-10899a1b48` → `bp-f47f75836a` | true | 2.63 | Snap **to** vertex to `[54.394, 24.4949]` |

Grok solved endpoints at **display-slug coords** (channel/planned anchors), not #79ac jetty coords:

| Slug | Grok solved coord | #79ac jetty coord | Offset |
|------|-------------------|-------------------|--------|
| `ad-lulu-island` | `[54.344343, 24.501337]` | `[54.3475, 24.4945]` | ~825 m |
| `ad-reem-island` | `[54.401147, 24.484583]` | `[54.394, 24.4949]` | ~1.4 km |

**Apply policy:** bind to restored `bp-*` ids; snap first/last geometry vertex to sealed BP coords (same as ledger's original `remap_snap_endpoint` intent, once nodes exist).

Geometry source: `grok-routing-output/route-solutions-synthesize-remapped.jsonl` (rows 11–13).

---

## Suggested follow-up seal scope

| Seal | Work |
|------|------|
| `#79al` (in flight) | 24 apply + 1 Khalifa mint — **3 held** per current ledger |
| `#79am` (proposed) | Re-mint 2 BPs (+ optional 2 `rn-*` restores) + apply 3 synthesize geometries |

---

## Files for Tasklet pickup

| Path | Use |
|------|-----|
| `grok-routing-output/APPLY-LEDGER.json` | `hold_synthesize_phantom` list |
| `grok-routing-output/route-solutions-synthesize-remapped.jsonl` | Held geometry + waypoints |
| `_ingest/gold-export-79ak-1/data-clean/FEATURES_BY_TYPE.json` | Canonical Feature records |
| `data-clean/CHANGELOG-FOR-CLAUDE-2026-06-16-uae-p2p3-abu-dhabi-islands.md` | Original mint provenance |

---

## One question back

Did #79ak **intentionally** drop `bp-31b06c534d` / `bp-f47f75836a` (e.g. hide-no-jetty policy), or is this a splice/scrub regression? If intentional, tell us the replacement node policy and we'll re-solve the 3 corridors against that anchor instead of restoring #79ac coords.