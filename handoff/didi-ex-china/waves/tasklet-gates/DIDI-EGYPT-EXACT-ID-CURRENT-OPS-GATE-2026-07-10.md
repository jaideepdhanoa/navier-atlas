# DiDi × Navier — Egypt exact-ID + current-operation gate

**As of:** 2026-07-10  
**Repo commit:** `20876d00d6d4d7f9831a5c93ed3dda9b0ee84673`  
**Status:** research-complete / seal-needed; current-operation holds remain

## Gate verdict

- **Current DiDi operation PASS (11):** Cairo, Alexandria, Hurghada, Ismailia, Suez, Port Said, North Coast (summer only), Mansoura, Damietta, Tanta, Marsa Matruh (summer only).
- **Current-operation HOLD (6):** Luxor, Aswan, Sharm El Sheikh, Marsa Alam, El Gouna, Safaga. The first-party current city directory does not list these places; omission triggers a hold, not a claim of non-operation.
- **Existing exact Atlas Egypt IDs preserved (4):** `cairo-egypt`, `hurghada-el-gouna-egypt`, `redsea-egypt`, `sharm-el-sheikh-egypt`. No shrink.
- **Current operation + exact Atlas bind:** Cairo is exact/display-ready; Hurghada is supported through the Hurghada component of `hurghada-el-gouna-egypt`. Do not extend that proof to El Gouna.
- **Current operation + registry gap:** Alexandria, Ismailia, Suez, Port Said, North Coast, Mansoura, Damietta, Tanta, and Marsa Matruh.

## Exact-ID result

- 13 proposed BPs reconciled; **0 exact BP matches**. Seven are seal-needed, three are registry gaps, three are reject/non-BP. Near names were recorded but not stamped.
- 6 candidate corridors reconciled; **0 exact route matches** and all `route_id=null`.
- Two route IDs printed in the Egypt cluster brief — `edge__hurghada-el-gouna-egypt__sharm-el-sheikh-across-the-gulf` and `edge-0762` — do **not** exist in `ROUTES.json` at the audited commit.
- The global Egypt slice contains 190 routes and 169 POIs. DiDi inherits global routes through cluster membership; this does not prove DiDi city operation or current water service.

## Finance / demand gate

- **Committed Egypt finance corridors: 0.** The partner surface economics scope is Mexico-only; three DiDi finance workbooks contain no Egypt rows.
- Every candidate corridor lacks exact endpoint equality and route-level annual passenger counts. All `annual_one_way_pax` values remain null.
- National tourism, airport throughput/rank, terminal count, and excursion cadence are context only. The EGP 120 Happy Land–Al-Qanater fare is Eid-specific and cannot be annualized.

## Brief audit

Enhance, do not replace. Main defects: partner names/overlay in canonical briefs, nonexistent route IDs, Sharm–Hurghada ferry contradiction, weak BP precision, broad tourism claims, and inconsistent Quanta-LR range/platform statements. Keep DiDi framing in the separate partner narrative.

## Ordered Grok actions

1. Preserve the four existing footprint IDs; add visible operation holds without deleting geography.
2. Repair wrong-parent/duplicate Egypt POIs.
3. Audit the 190-route Egypt slice, including NEOM routes assigned to cluster `egypt`.
4. Add accepted city registry IDs without fuzzy matches.
5. Bind authoritative passenger gates/landings and return a zero-silent-drop ledger.
6. Create global routes only after exact endpoint binding and water/waypoint gates.
7. Reseal DiDi through cluster inheritance and validate identical global corridor inheritance.
8. Return exact IDs, before→after counts, drop reasons, orphan/land-crossing proof, and Cairo/Hurghada render QA.
9. Start finance cascade only after exact sealed routes and route-specific demand/fare inputs.

## Files

- JSON gate: `/tasklet/agent/home/didi-ex-china-audit/gates/DIDI-EGYPT-EXACT-ID-CURRENT-OPS-GATE-2026-07-10.json`
- This status: `/tasklet/agent/home/didi-ex-china-audit/gates/DIDI-EGYPT-EXACT-ID-CURRENT-OPS-GATE-2026-07-10.md`
