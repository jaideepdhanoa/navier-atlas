# Navier Atlas — Canonical Data Conventions (v1, 2026-05-30)
_The single authoritative standard for ALL research data: city briefs, partner proposals, nodes, edges, orgs, humans. Every subagent MUST read this before writing data. Companion to `reference/data-architecture-direction.md` (the "why")._

> **Prime directive — ONE SPINE, MANY PROJECTIONS.** The graph spine (nodes + edges + orgs + humans) is the single source of truth. Briefs, partner proposals, the deck, PDFs, and apps are *projections* that **reference the spine by id** — they must NOT restate spine facts (coords, distances, platform) that can drift.

---

## 1. IDENTITY — the #1 rule (kills the recurring bug class)
- **`city_id` of a brief MUST exactly equal an existing anchor `node id`.** Verify against `app/data-spine/output/nodes.json` (or `atlas-external/output-external/nodes.json`) BEFORE writing. No guessing, no shortening.
  - ✅ `salalah-dhofar-oman`, `male-maldives`, `jeddah-ksa`
  - ❌ `salalah-oman`, `maldives`, `jeddah` (alias drift → dangling join)
- **A brief without a matching node is INVALID** (it has no clickable pin). Either a node exists, or the brief goes in the tracked-gaps allowlist with a `node-pending` reason — never silently shipped.
- **Partner proposal city references** (`*_city_id`, `markets[].city_id`, phase city refs) follow the same rule.
- **Route/edge endpoints** (`from_node_id`/`to_node_id`) MUST be existing node ids. Never a route id, never a hand-typed composite (`x__y-600-nm` is malformed and forbidden).
- **Future (Claude-coordinated):** type-namespaced ids (`city:`, `org:`, `route:`, `bp:`, `human:`) and deterministic `route:{sorted endpoints}` ids. Do NOT introduce unilaterally — render depends on current ids.

## 2. VISIBILITY — separate at birth, never scrub later
Every brief/partner file is authored in three tiers so externalization is a *filter*, not a hand-scrub:
- **`public`** (default, untagged): partner/navigator-facing. Shows on the website/atlas. NO competitor comparisons, NO commercial/unit-economics, NO principal names, NO strategist jargon.
- **`deck`**: pitch-deck-only. Competitor rebuttals (Candela etc.), commercial model, unit economics, vs-status-quo financials.
- **`internal`**: never exported anywhere public. Principal names (Maldives deal principal, Mohamed El-Jana, Sheikha Maktoum), royal-house channels, sensitive convener intel.

**How to tag in a brief/partner JSON:** put non-public content in a top-level `"internal": { ... }` object and/or a `"deck_only": { ... }` object. Everything outside those is public by default. The externalizer drops `internal` and `deck_only` for website builds.

**Banned tokens in `public` content** (leak-gate enforced — see `check_pitch_content.sh`): `wedge`, `moat`, `Founders Fund`/cap-table refs, `Series B`/investor-relations, `vs Candela`/competitor-naming, flag-and-exclude route names (NEOM↔Eilat, Sharm↔Eilat). Use plain language: "wedge"→"entry beachhead/first use case"; "moat"→"durable advantage"; competitor→"the status quo / incumbent operators (demand proof)".

## 3. REFERENCE, DON'T RESTATE
- A brief names its `signature_routes` by endpoint city ids and lets the spine carry `distance_nm`/`platform`. Don't hard-code a distance that also lives on an edge — if they drift, the map and brief disagree.
- A brief references partners by org id where one exists (`key_partners[]`), rather than re-describing the org.
- Platform facts come from `reference/navier-platform-specs.md` ONLY. Pioneer II = 70 nm all-electric; Quanta-LR = 2,000 nm hybrid. Any route >70 nm is NEVER labelled Pioneer II.

## 4. REQUIRED SHAPE (city brief)
Conform to `partner-pitch/schema/city_brief.schema.json`. Minimums:
- `city_id` (= node id), `display_name`, `region`, `country`
- `summary` (public, partner-neutral)
- `demand_signals[]` (≥3 full-depth / ≥3 starter) — sourced, dated where possible
- `use_cases[]` (≥3), `journeys[]` (≥2) — each a concrete A→B with the status-quo pain it removes
- `navier_fit` with `pioneer_ii` AND `quanta_lr` split (intra-cluster vs cross-archipelago)
- `signature_routes[]` (endpoint ids + nm + platform), `seasonality`, `regulatory_note`
- `competitive_landscape` = incumbent operators as **demand evidence**, not Navier-vs-rival
- `sources[]` (url or citation + date)
- Optional: `precedents[]` (other-region proof, only if natural — never force-fit), `internal{}`, `deck_only{}`

## 5. INTEGRITY GATE (enforced)
`atlas-external/integrity/build_manifest.py` runs at seal time. It hard-fails on NEW dangling joins (edge endpoint / brief city_id / partner ref that doesn't resolve to a node). Tracked, accepted gaps live in `atlas-external/integrity/known-gaps.json` (WARN, not ERROR). **A seal with new ERRORs must not be pushed.**

## 6. SELF-IMPROVEMENT (recursive loop — §27)
- Subagents REPORT learnings in their final message; the parent folds Tier-1 learnings into the subagent's `## BANKED LEARNINGS` and Tier-2 into `_subagent-learnings.md`; consolidation every 3 entries.
- This conventions doc is itself versioned — when a convention changes, bump the version and note it; never silently diverge.
