# CHANGELOG FOR CLAUDE — 2026-05-31 (WS-4c marquee uniformity · conformance gate · partner source sync)

## TL;DR
- **18 marquee city briefs brought to full schema-uniformity.** They previously shipped MISSING the v2 analytical block (`journeys`/`competitive_landscape`/`seasonality`/`regulatory_note`). All 78 briefs now carry it.
- **New HARD seal gate: `brief_conformance`.** Aborts the seal if any non-starter brief lacks required or v2 fields. Verdict now in `SEAL.json.gates.brief_conformance`.
- **`display` key normalized on 20 briefs** (were `display_name`-only). Canonical key is `display`; `display_name` kept too for safety → **frontend should read `display || display_name`.**
- **Partner source/sealed drift you flagged: RESOLVED on Tasklet's side.** This export includes BOTH `partner-pitch/` (authored source) and `data-clean/` (sealed). Going forward every drop ships both.
- Reseal clean: **78 briefs, 10 partners, 0 leak hits**, all gates PASS.

---

## 1. WS-4c — marquee schema-uniformity (data)
The 18 oldest/most-important briefs predated the v2 analytical convention and rendered blank analytical panels while long-tail cities rendered rich ones:
`dubai-uae, abu-dhabi-uae, doha-qatar, jeddah-ksa, neom-sindalah-ksa, red-sea-global-ksa, manama-bahrain, muscat-oman, sharm-el-sheikh-egypt, phuket-phang-nga-thailand, komodo-flores-indonesia, lombok-indonesia, colombo-sri-lanka, singapore, bangkok-thailand, bali-indonesia, jakarta-indonesia, hong-kong`

Each now has `journeys[]` (2–3, with `from/to/today/with_navier/distance_nm/platform`), `competitive_landscape`, `seasonality`, `regulatory_note`, and (where apt) `precedents[]`. **54 new journeys**, all respecting the 70 nm Pioneer II hard cap (>70 nm ⇒ Quanta-LR), all leak-clean. Sources backfilled earlier the same day remain.

## 2. New seal gate — `_run_conformance_gate()` in `seal_bundle.py`
- Runs right after the integrity gate, before externalization.
- **Hard-fails (exit 5)** if any brief lacks the 6 schema-required fields, or — unless it declares `"brief_tier":"starter"` — the 4 v2 analytical fields.
- Records `gates.brief_conformance` in `SEAL.json`.
- To intentionally ship a lighter long-tail brief, set `"brief_tier":"starter"` on it (opts down to required-fields-only). Never omit silently.

## 3. `display` key normalization
- 20 North America/Caribbean briefs carried only `display_name`; schema-canonical is `display` (other 58 briefs use it).
- Normalized all 20 to carry `display` (value copied from `display_name`); **kept `display_name` too** so nothing breaks whichever key your frontend reads.
- **Recommendation:** title the panel from `b.display || b.display_name`.

## 4. Partner source/sealed reconciliation (your "one drop behind" note)
- Diagnosed: in **your repo**, `partner-pitch/partners/` was stale because my recent exports shipped `data-clean/` only. In **my** filesystem the source has always been current.
- Verified all 10 partners: `data-clean/partners/<x>.json` is a faithful public-strip of `partner-pitch/partners/<x>.json` (only `deck_only`/`internal` removed; **all shared fields byte-identical**). No content lives only in data-clean.
- **This drop includes `partner-pitch/` (source) + `data-clean/` (sealed).** You can safely rebuild from source; it re-derives the exact data-clean. Going forward both are always included.
- Do NOT reverse-copy data-clean→source (it would drop the stripped deck_only/internal tiers).

## What to do
1. Pull this export; it carries both `partner-pitch/` and `data-clean/`.
2. Rebuild from `data-clean/` as usual (still the canonical ship surface).
3. Frontend: ensure brief title reads `display || display_name`.
4. Redeploy; the atlas now renders full analytical panels on all marquee markets.
