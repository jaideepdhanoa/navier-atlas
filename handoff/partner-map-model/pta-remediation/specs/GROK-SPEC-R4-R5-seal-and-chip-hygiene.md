# GROK-SPEC — R4/R5 Phase-B Seals + Honest-Null Clearance + Chip Hygiene

**Author:** Tasklet · **Date:** 2026-07-02 · **Lane:** Grok geometry (land-QA seal + hand-waypoints); Tasklet display-chip binding.
**Rule:** ID-based match only · null-beats-wrong · additive only · seal at **0 km land** with explicit hand waypoints · honest operational-status flags (do not imply a defunct/aspirational route is running) · re-run land-crossing QA, hold 0-crossing record.
**Standing guardrails honored:** never rewrite WSF growth_case numbers; never invent route_ids (null beats wrong); batch-5 #150 scrub not reverted.

---

## R4a. fullers360 — seal 3 real Hauraki Gulf routes (endpoints already named)
Auckland Downtown is the hub; all endpoints exist as named nodes. Devonport already carries a route_id.
| route | from → to | dist | action |
|---|---|---|---|
| Devonport | auckland-downtown-ferry → devonport-wharf | 1.3 nm | already rid'd — confirm seal |
| Waiheke | auckland-downtown-ferry → matiatia-waiheke | 10 nm | seal + mint route_id |
| Gulf Harbour | auckland-downtown-ferry → gulf-harbour | 15 nm | seal + mint route_id |
| Great Barrier | auckland-downtown-ferry → tryphena-great-barrier | 50 nm | seal + mint route_id |
Open Hauraki Gulf water; hand-waypoint around Rangitoto, Motutapu, and the Waiheke/Great Barrier approaches so no leg crosses land. All are **operational Fullers360/SeaLink services** — safe to seal live.

## R4b. hawaii — seal inter-island legs with honest operational flags
Named endpoints exist. **Only Lahaina↔Manele (Lāna‘i) operates today** (Expeditions). The others are historic/aspirational (Superferry ceased 2009; Molokai ferry ceased 2016) — seal geometry for the authority forward-network but set `_operational_status: "aspirational"` (or leave `journeys_unlocked` honest-pending); do NOT imply live service.
| route | from → to | dist | operational |
|---|---|---|---|
| Lahaina–Manele | lahaina-maui → manele-lanai | 9 nm | LIVE — seal |
| Honolulu–Lahaina | honolulu-harbour → lahaina-maui | 72 nm | aspirational |
| Honolulu–Kaunakakai | honolulu-harbour → kaunakakai-molokai | 40 nm | aspirational |
| Maalaea–Kawaihae | maalaea-maui → kawaihae-hawaii-island | 30 nm | aspirational |
Deep-ocean channels (Au‘au, Kaiwi, Alenuihāhā, ‘Alalākeiki) — hand-waypoint around Moloka‘i, Lāna‘i, and south Maui headlands. No land-crossing risk on open legs; verify island-approach polylines.

## R5. Honest-null clearance — land-QA seals (real route_ids already present)
These carry real `route_id`s but sit unsealed pending land-QA. Seal at 0 km with hand waypoints; do not alter economics.
### wsf (Puget Sound) — 4 corridors
- wsf-seattle-colman → wsf-bainbridge (rn-1fc1cf8c4de2, 7.1 nm)
- wsf-seattle-colman → wsf-bremerton (rn-01adad364cdf, 11.8 nm)
- wsf-edmonds → wsf-kingston (rn-3fa10659d59d, 4.3 nm)
- wsf-mukilteo → wsf-clinton (rn-0574f069dd70, 1.7 nm)
Hand-waypoint around Bainbridge/Kitsap headlands + Whidbey approach.
### bc-ferries (Georgia Strait) — 4 corridors
- van-harbour-flight-centre → victoria-inner-harbour (rn-2de87d2e3342, 53 nm)
- van-harbour-flight-centre → nanaimo-harbour (rn-c7a008ab42de, 30 nm)
- tsawwassen → swartz-bay (rn-a205466e4f2a, 24 nm)
- swartz-bay → fulford-harbour (rn-864ead3912d6, 5 nm)
Georgia Strait + Gulf Islands — this is the **bcf-d04 land-QA** horizon item; hand-waypoint through Active Pass / Gulf Islands so no leg cuts across land. If a clean water polyline cannot be found for a leg, keep it honest-null (null beats wrong).

## R4c. Batch-5 aspirational-chip → sealed-corridor bind (RESOLVED — bind map ready)
`singapore-mpa, abu-dhabi-itc, bahrain-motc, dubai-rta, qatar, rakta` each carry 4 `aspirational-no-built-route` chips (real `from`/`to` names, `route_id: null`, `render: roadmap-amber-dashed`). **Their base networks are already fully sealed with 0 land crossings** — and on fresh `ROUTES.json` inspection, most aspirational chips correspond to a **now-sealed real corridor** (`_pta_<authority>` tagged, real route_id, longer sealed geometry from hand-waypoint routing).
**Resolved via conservative endpoint-token match (exactness-first, null-beats-wrong):**
- **18/24 chips bind to a real sealed `route_id`** (high-confidence, unambiguous).
- **6/24 kept honestly aspirational** (no confident sealed match): singapore ×2 (Marina East↔Marina Bay/CBD, Marina Bay/CBD↔Keppel), bahrain ×1 (Reef Island↔Diyar Al Muharraq), rakta ×3 (RAK-corniche legs).
- Per authority: abu-dhabi 4/4, dubai 4/4, qatar 4/4, bahrain 3/4, singapore 2/4, rakta 1/4.
- **Bind map artifact:** `dossiers/R4/BATCH5-BIND-MAP.json` (chip → route_id, sealed distance, sealed labels).

**Apply step (Grok renderer lane — render-field semantics):** for each `bind_sealed` chip, set `route_id`/`route_ids`, update `distance_nm` to sealed geometry, flip `_link_status → sealed`, `_link_kind → sealed`, `display → interactive`, `render → sealed-solid`. **Preserve `economics_status` (do NOT revert #150 scrub).** Kept-aspirational chips unchanged. Tasklet can apply the data-field binds; the dashed→solid render convention is Grok's renderer — coordinate so the flip is consistent.

## Definition of done (R4/R5)
- fullers360 3 routes sealed; hawaii Lahaina-Manele sealed (others honest-aspirational); wsf 4 + bc-ferries 4 land-QA sealed or honest-null; land QA re-run 0 crossings.
- Batch-5 placeholder chips re-featured from real sealed corridors or nulled (Tasklet binding).
- Grok mint/seal receipt → Tasklet binds partner JSONs.
