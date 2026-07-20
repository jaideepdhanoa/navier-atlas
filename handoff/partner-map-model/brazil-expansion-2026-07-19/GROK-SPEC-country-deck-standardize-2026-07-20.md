# GROK SPEC — Country partner-deck standardization (2026-07-20)

Basis confirmed by Jaideep 2026-07-20: **use the sheet MID column** as the authoritative TAM
basis for all four country decks. Reference standard = the DiDi Brazil deck as manually edited
by Jaideep on 2026-07-19 (main-deck + backup split, slide-2 quadrant, `THE PRIZE` ladder on
SOM Full Mapped Network, `WHAT ONE BOAT EARNS · {CITY}` econ titles, three link chips).

## Already applied live by Tasklet (Slides API) — do NOT redo
- **DiDi Brazil** `1jHxxDgDd5Oki0eO4YoCfHHfC_aS-akGjb4UfXseIEK8` — THE PRIZE corrected to sheet MID
  ($382M / $1.74B / $6.97B / $20.9B / $0.94B); slide-2 narrative broadened to 8-city; 9 link
  chips repointed to the new Drive model. Reference deck.
- **inDrive Brazil** `1QImIe6KAee0Eajsokgh9NmH0I29lir4l2LV63e-9OxE` — THE PRIZE standardized to
  SOM full-network $382M bottom rung + MID upper rungs ($1.74B / $6.97B / $20.9B), no platform
  rung; slide-2 thesis broadened.
- **DiDi Mexico** `1XwKRuJtMrou8NtBdc1oY3LL2Dk83dCs9MCLvNKgwq0c` — THE PRIZE standardized to SOM
  full-network $138M bottom rung + MID upper rungs ($631.7M / $2.53B / $7.58B) + platform $341.1M.

## Grok to complete (deterministic, generator-driven)

### 1. inDrive Egypt ladder regen — `1Nn3BRKUahikp87zC84JMdEVrcJYppm9ZXHgndAuzsEk`, slide 8 (page `g3eec5122801_0_562`)
Current ladder is **stale** (shows $8.5M / $65.4M / $75.0M; $65.4M matches no rung in the new
sheet) and has only **3 rungs** (missing the Journey-GMV rung). Rebuild to the new sheet MID,
inDrive rung set (SOM → SAM → TAM → Journey GMV; **no platform rung**):

| Rung | Sheet row | MID value | Deck label |
|---|---|---|---|
| SOM full mapped network | A18 | **$36.4M** | `SOM · Today — Navier fares on inDrive's network, serving today's boat-only crossings` |
| SAM full network | A20 | **$18.7M** | `SAM · Near term — faster, quieter boats grow the market at maturity` |
| Marine-mobility TAM | A21 | **$75.0M** | `TAM · Full market — the entire sea-transfer market we create` |
| Journey GMV | A22 | **$224.9M** | `GMV · Whole journey — add food, stays and experiences to every crossing` |

**Boat-only capture anomaly (must be handled visually, not silently):** Egypt's SOM floor capture
is ~0.873 (boat-only marine-park corridors → near-monopoly), so **SOM ($36.4M) sits above SAM
($18.7M)** — the ladder is not monotonic. Do not reorder to force ascent and do not drop a rung.
Present in sheet order with a one-line footnote that boat-only corridors carry near-total capture
today, so the "floor" already reflects high share. Confirm footnote wording with Jaideep before seal.

### 2. Econ-slide titles → `WHAT ONE BOAT EARNS · {CITY}` (all four decks)
Match the DiDi Brazil reference. Per-city unit-economics slide title uppercase, city suffix.

### 3. Link chips (inDrive Brazil, inDrive Egypt, DiDi Mexico)
Repoint / add the three chips — Interactive link, Model deepdive (unit econ), Detailed market
sizing (TAM) — to each partner's **new** Drive model (shared, link-viewer enabled):
- inDrive Brazil sheet: `13BViN3u…` (confirm from PARTNER-SHEET-IDS)
- DiDi Mexico / inDrive Egypt: per PARTNER-SHEET-IDS map.
(DiDi Brazil already done.)

### 4. inDrive Brazil backup restructure
Mirror DiDi Brazil: move the new-city deep-dives + their unit-econ slides into the **backup**
section; keep Rio / Angra / Floripa in the main spine. DiDi Brazil is the layout reference.

### 5. Manifest/config sync
After the above, sync `deck-studio/decks/{indrive-brazil,indrive-egypt,didi-mexico}/slide-manifest.json`
and `deck.config.json` to live state; DiDi Brazil manifest to Jaideep's restructured live state.

## Guardrails
- Slides API only; edit in place; preserve object-id families; page-scoped `replaceAllText` for
  value/label swaps to keep numeral styling.
- Fail closed on any rung whose value is not directly in the sheet MID column.
- Run `scripts/audit_partner_copy.py` / `deck-studio/qa/partner_copy_lint.py` as a blocking gate.
