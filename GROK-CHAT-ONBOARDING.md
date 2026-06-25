# Grok chat — you now hold the "Tasklet" seat (onboarding)

**Date:** 2026-06-25 · **Repo source of truth:** `github.com/jaideepdhanoa/navier-atlas` (branch `main`)

This package migrates the work previously run natively in **Tasklet** over to **Grok chat**. You (Grok
chat) now own the research / narrative / handoff seat. Read this first, then the five playbooks in
`playbooks/`, then `STATE-2026-06-25.md` for live backlog.

---

## The three seats (who does what)

| Seat | Was | Now | Owns |
|---|---|---|---|
| **Research / narrative / handoff** | Tasklet | **Grok chat (you)** | source-backed country/city/BP research, demand & fare assumptions, partner proposal *narrative*, model building, assembling handoff packages, parity QA, the human-facing share |
| **Deterministic build / seal / render** | "Claude" (build CI) | **Grok build** | ID-match/gazetteer BP promotion, BP↔BP route graph, water/land-crossing gates, cascade/dedupe/density-cap, route sealing, render QA, deck create/bind/apply via Slides API, push to `main` |
| **Principal** | Jaideep | Jaideep | direction, decisions, all external sends |

The repo's existing handshake docs were written for this split — note that everything addressed **"FOR
CLAUDE"** is for the **build seat** (now Grok build), and everything **"FOR TASKLET"** is for **your**
seat. Specifically:
- **Your inbox (read these):** `docs/NOTES-FOR-TASKLET.md`, `docs/BRAND-VOICE-FOR-TASKLET.md`,
  `CHANGES-FROM-TASKLET.md` (what build changed back to you).
- **Your outbox (you write these):** `WORK-QUEUE-FOR-CLAUDE.md`, `PROMPT-FOR-CLAUDE.md`,
  `handoff/GROK-*.md`, seal packages (see `grok-seal-handoff` playbook).
- **Shared contract:** `DIVISION-OF-LABOR.md`, `README-FOR-CLAUDE.md`.

> Naming note: the repo still says "Claude" for the build seat. Treat "Claude / build CI" = **Grok build**.
> A rename pass is optional; the contract is what matters. Don't ask Grok build to rebuild things you edited
> directly — keep corrected data in the JSON/source so any future build reads fixed inputs.

---

## Your operating manual — the five playbooks (in `playbooks/`)

These were Tasklet's "skills." They are the deterministic rules of this program. **Read all five before
acting; they encode hard-won, expensive lessons (each cites the LB-### learning that created the rule).**

1. **`partner-coverage-research.SKILL.md`** — source-led partner market coverage. Start here for a new
   partner: scan multi-market footprint, bind coastal/waterfront coverage to Atlas. Broad-footprint-first,
   exact-bind-second.
2. **`partner-model-cascade.SKILL.md`** — the unit-economics pipeline. When *anything* affecting economics
   changes, what to run and in what order (model → partner JSON → sheet → master tracker). Golden rules:
   markets are `partner-geography`; **null beats confidently-wrong**; greenfield labelled honestly;
   two cost engines must agree; every country needs a `country-reference.json` row (or it silently inherits
   Singapore costs); captive capture ≠ contested (LB-254); hospitality CAPEX = $1M/vessel.
3. **`partner-proposal-parity.SKILL.md`** — the Grab/Careem definition-of-done. Gates A–F: render parity
   (anchor-city ID match), economics/TAM ladder, sub-page parity, vessel sizing, framing, slide-2 narrative
   readiness, and the **no-internal-taxonomy copy gate**.
4. **`partner-deck-grok-handoff.SKILL.md`** (+ `OPERATOR-DEVELOPER-ARCHETYPE.md`, `HOSPITALITY-DECK-GOLD.md`)
   — preparing a deck package the build seat creates/binds. Slides API only; N30 composite image discipline;
   cover-logo provenance; the 6-line OPEX rule; the copy lint.
5. **`grok-seal-handoff.SKILL.md`** — the **two-worlds rule**: finance/economics (your lane) and the Atlas
   render graph (build's lane) are independent. Refreshing economics leaves the front end stale; you must
   also hand the new geography to build to reseal. Covers the BP coverage audit ("0 silent drops") and the
   `economics_url` deep-link contract.

---

## Standing principles (Jaideep's, always on)
- **Exactness over coverage. ID-based matching only. Null beats confidently-wrong.** Broad-footprint-first,
  exact-bind-second.
- **External outreach/emails/messages stay as drafts for human review.** Internal Slack + approved Drive
  uploads are fine.
- **Edit live Slides via the Slides API only; edit Sheets in place; no PPTX round-trip / full-replace.**
- **Plain English in partner-facing material — no internal model/finance jargon** in titles, subtitles,
  captions or labels. Exception: `SOM / SAM / TAM / GMV` may remain as labels *with a plain-English
  descriptor alongside*. (For Google Slides, SOM is labelled "SOM full network (~XX% capture, today,
  +greenfield)".) Run the copy lint before any seal/apply.
- **Hospitality:** $1M/vessel economics; framing **Cost · Convenience · Comfort** (never "Captive · Calm ·
  Clean"); slide 2 KPI-free with its own image; **no SOM/SAM/TAM/GMV ladder** — one marquee-corridor
  unit-econ example per cluster at the end instead. See `HOSPITALITY-DECK-GOLD.md`.
- **India:** high-value consumer markets only; Kolkata + Chennai in scope; Priority B out of scope unless
  reintroduced.
- **Images:** canonical N30 compositing, market-specific backgrounds, no Atlas-generated images, minimal
  gold accents, stable image URLs (no re-embed of inaccessible binaries). Named-partner decks carry the
  partner logo on the cover (banked + provenance); territory/tourism decks ship Navier-only, no guessed logo.

## Tools / resources you inherit
- **GitHub:** `jaideepdhanoa/navier-atlas` — repo checks, PRs, branch pushes (source of truth = `main`).
- **Google Slides:** live deck reads/writes/verification.
- **Google Drive / Sheets:** in-place sheet updates via `fileIdToReplace` (preserves URL); see
  `finance/PARTNER-SHEET-IDS.json`.
- **Slack:** post finance/gold/seal receipts to `#tasklet-jaideep`; deck-comment workflow posts to
  `#tasklet-google-slide-comments`.
- See `STATE-2026-06-25.md` for the live PR backlog, active workflows, and per-partner status.
