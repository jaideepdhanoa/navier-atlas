# Navier Atlas — Deploy Protocol (authoritative)

_Last updated: 2026-05-30 (Tasklet). Supersedes any per-deploy seal-freshness requirement._

This is the single source of truth for **when the seal / full gate is required**. It exists to
kill the recurring friction where a stale `SEAL.json` blocks an otherwise-safe render iteration.

---

## The core invariant (why dev deploys are safe by construction)

`build.py` reads **only** from `output-external/` — the already-partitioned, leak-scrubbed clean
data. It **never** touches the internal spine (`app/data-spine/output/*`, humans.json, orgs.json,
internal-only story fields). Therefore a render/template/route/content iteration **cannot leak spine
data**. The only *new* leak surface in a dev cycle is the partner-facing pitch JSON an author edits.

⇒ A dev deploy needs exactly one cheap check: a targeted grep on the pitch JSON. Nothing else.

---

## Two modes

### DEV MODE — default, 95% of cycles (seconds)
Pre-flight = **`check_pitch_content.sh` ONLY** (leak grep on partner-pitch JSON; milliseconds).

- ❌ NO partition
- ❌ NO full externalization scan
- ❌ NO land-crossing gate
- ❌ **NO seal / NO `SEAL.json` freshness check** ← this is the change
- ❌ NO post-deploy leak sweep
- ✅ build from existing clean data → deploy

**A stale `SEAL.json` on `main` is HARMLESS in dev mode and must NOT block a deploy.** The seal is a
release artifact; it is allowed to lag behind `main` between weekly releases.

Tasklet path: `dev.sh`. Claude path: render pre-flight = pitch-content grep, then deploy. Either side
may deploy a dev build.

### RELEASE MODE — weekly, or immediately before sharing the URL externally
Full pipeline runs **once**: partition → enrich → A* regen → build → land gate → externalization gate
→ extract blobs → **seal** → dist isolation → deploy → post-deploy sweep → push to `main`.

- ✅ This is the ONLY time `SEAL.json` is regenerated and the ONLY time seal-freshness is enforced.
- Tasklet path: `release.sh`. Run weekly or before any external share.

---

## Action for Claude (pre-flight §3.1)

**Scope the SEAL.json freshness check to RELEASE mode only.** In dev mode, skip it entirely. Concretely:

- Dev deploy pre-flight = `check_pitch_content.sh` pass ⇒ deploy. Do not read or hash `SEAL.json`.
- Release deploy pre-flight = full gate + fresh seal (as today).
- Gate the seal check behind an explicit `--release` / `RELEASE=1` flag (default = dev).

This removes the blocker where a content/label change invalidates the seal hash and stalls every
subsequent render deploy. The seal will be refreshed on the next weekly release.

---

## Note on this cycle (2026-05-30)
Riau density + final route-sweep + Grab phase-3 anchor fixes shipped via **dev deploy** (live now,
pitch-content clean). `SEAL.json` on `main` is intentionally left lagging; the next weekly `release.sh`
will refresh it. No reseal was run for this dev cycle — that is the intended behavior going forward.
