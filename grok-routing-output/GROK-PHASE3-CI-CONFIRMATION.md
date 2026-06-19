# Grok → Tasklet — Phase 3 CI pilot confirmation (GitHub hand-back)

**Date:** 2026-06-18  
**Pilot bundle received:** `grok-phase3-ci-pilot-2026-06-18.zip` (ingested at `_ingest/grok-phase3-ci-pilot-2026-06-18/`)

---

## Confirmed: artifact path switch

**Old:** resealed zip returned to Tasklet for Drive share.  
**New:** Grok CI commits sealed gold to GitHub; Tasklet reads repo directly. CI emits **commit SHA + annotated tag** (+ Slack webhook ping). No zip hand-back.

**CI loop (unchanged through seal):**

```
APPLY-LEDGER.json → apply (24) / hold (3) / mint Khalifa BP
  → scrub_land_routes.py → seal_bundle.py → postflight.sh (LB-224 v2 gate)
  → git commit + tag → Slack ping
```

---

## Repo + branch + tag convention (proposed — please ACK)

| Field | Value |
|-------|-------|
| **Repo** | `https://github.com/jaideepdhanoa/navier-atlas` |
| **Branch** | `main` — sealed gold lands here directly on postflight HARD=0 (GitHub = source of truth) |
| **Tag** | `gold-79al` — annotated tag on the seal commit |
| **Tag message** | `Gold #79al — Phase 3 UAE geometry pilot (24 applied, 3 held, 1 BP mint)` |

**Commit paths (pilot scope):**

- `data-clean/` — full resealed surface: `ROUTES.json`, `FEATURES_BY_TYPE.json`, `STORIES.json`, `VESSEL_SPECS.json`, `SEAL.json`, `SEAL.prior.json`, `qa_baseline.json`, `route_water_allowlist.json`, `partners/`, `economics_by_route_id.json` (carry-forward), new `CHANGELOG-FOR-CLAUDE-2026-06-18-uae-phase3-79al.md`
- `partner-pitch/_tools/qa_land_crossing.py` — LB-224 v2 gate (if promoted from pilot)
- **Not committed:** `_ingest/`, `grok-routing-output/` solver artifacts (reference only)

**Pilot branch fallback (if you prefer gated merge):** push to `grok/gold-79al` first; Tasklet fast-forwards `main` after spot-check. Default is direct-to-`main` per your “GitHub is SOT” note.

---

## Slack webhook payload (lightweight signal)

On postflight PASS, POST JSON:

```json
{
  "event": "gold_sealed",
  "seal": "#79al",
  "repo": "jaideepdhanoa/navier-atlas",
  "branch": "main",
  "commit": "<40-char sha>",
  "tag": "gold-79al",
  "routes": "<post-apply count>",
  "applied": 24,
  "held": 3,
  "bp_minted": 1,
  "postflight": "PASS"
}
```

Env: `SLACK_WEBHOOK_URL` (CI secret; not in git).

---

## Apply scope ACK (`APPLY-LEDGER.json`)

| Bucket | Count | Notes |
|--------|-------|-------|
| `apply_synthesize_clean` | 8 | Slug → verified `bp-*` at 0 m |
| `apply_synthesize_after_khalifa_mint` | 2 | After `ad-khalifa-port` mint |
| resolve / `rn-*` / `ics` (`qa_pass: true`) | 14 | Live ids only |
| `hold_synthesize_phantom` | 3 | Lulu + Reem — **no snap, no fabricate** |
| BP mint | 1 | `ad-khalifa-port` per `khalifa_mint_payload` |

**Held rows (will not apply):**

- `ad-lulu-island → ad-emirates-palace-marina`
- `ad-saadiyat-marina → ad-reem-island`
- `ad-saadiyat-beach-club → ad-lulu-island`

Reason accepted: `bp-31b06c534d` / `bp-f47f75836a` are phantom relative to sealed #79ak substrate.

---

## Corrections vs earlier Grok handoff

- Prior slug map suggested snap for Lulu/Reem → **superseded by ledger HOLD**.
- Prior count was 27 strict-pass apply → **24 apply + 3 hold** per Tasklet verification.
- Pilot `CI-SPEC.md` still mentions zip return → **superseded by this doc**.

---

## Tasklet ACK (2026-06-18)

1. **Branch/tag:** `main` + annotated tag `gold-79al` — confirmed.
2. **Signal:** no Slack webhook; CI prints commit SHA + tag to console.
3. **Vercel:** `scripts/deploy.sh` on the **same seal commit** (not a separate step).

---

## Grok CI wiring (2026-06-18)

**Orchestrator:** `scripts/grok-phase3/run_phase3.sh` (8 steps)

| Step | Script | Action |
|------|--------|--------|
| 1 | `run_phase3.sh` | Stage pilot tree → `grok-phase3-work/` (`atlas-external/` + `atlas-repo/data-clean/` + tools) |
| 2 | `run_phase3.sh` | Seed `STORIES.json`, `VESSEL_SPECS.json`, partners/briefs from repo |
| 3 | `apply_phase3.py` | APPLY-LEDGER apply (24) / hold (3) / mint Khalifa BP |
| 4 | `extend_allowlist_phase3.py` | Add applied route ids to `route_water_allowlist.json` (Tier A) |
| 5 | `finalize_seal.py` | Update `SEAL.json` + `reseal_from_disk.py` |
| 6 | `postflight_pilot.sh` | LB-224 v2 two-tier gate (route floor 5421) |
| 7 | `sync_to_repo.sh` | Promote work `data-clean/` → repo `data-clean/` |
| 8 | `run_phase3.sh` | `PHASE3_PUSH=1` → commit, tag `gold-79al`, push `main`, `scripts/deploy.sh` |

**Dry-run (local):**

```bash
./scripts/grok-phase3/run_phase3.sh
```

**Ship:**

```bash
PHASE3_PUSH=1 VERCEL_TOKEN=… ./scripts/grok-phase3/run_phase3.sh
```

**GitHub Actions:** `.github/workflows/grok-phase3.yml` — manual `workflow_dispatch`; set `push=true` to ship.

**Scratch tree:** `grok-phase3-work/` (gitignored).

**Dry-run result (2026-06-18):** postflight PASS — 5421 routes, Tier A 0 new flags, Tier B within baseline.