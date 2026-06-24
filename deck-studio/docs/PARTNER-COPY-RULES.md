# Partner-facing copy rules — no internal taxonomy on slides

**Why this exists (root cause, 2026-06-24).** On the Ocean Whisperer deck, slide
titles/subtitles/captions read like model internals: *"captive resort mesh (grounded)"*,
*"premium network width"*, *"ABC scale vision — island-to-island (roadmap)"*,
*"Bonaire + Aruba legs flagged amber-dashed; Quanta-LR cross-island reach"*, *"SOM floor …
~46% capture"*, *"marine-transfer TAM (induced market)"*, *"the WIDTH a faster product unlocks"*.
A partner could not parse any of it. This was not a typo — **the deck builder composed
rendered slide text directly from finance + render taxonomy** (`kpi_frame`, the market
`label`, the economics `meaning`/caption strings, vessel codenames). There was **no layer
separating model labels from display copy**, and the existing QA only checked land-crossings
and object inventory — never the words a partner reads. So jargon shipped, survived multiple
review rounds, and the same disease is present on **bolt, grab-thailand, and minor-hotels**
decks too (run the linter to see counts).

## The rule
Everything a partner *reads* on a slide — titles, subtitles, eyebrows, KPI captions, ladder
labels, route descriptors, CTAs — must be **plain, compelling, partner-facing English**.
Internal model + render taxonomy is **banned from rendered text**. It stays where it belongs:
in the finance model, `kpi_frame`/`capture_frame`, render directives, and provenance fields.

### Banned in rendered slide text (translate, don't paste)
| Internal term | Say instead (partner-facing) |
|---|---|
| SOM / SOM floor | "today's revenue" / "the conservative case" |
| SAM / SAM mid / network width | "the near-term market" / "the wider network a faster product opens" |
| TAM / marine-mobility TAM / induced market | "the full market this creates" |
| Journey GMV | "the whole guest journey — travel, dining, stays" |
| captive resort mesh / resort mesh / grounded corridor | "your resort coast, connected by water" / "live routes" |
| premium network width | "the complete island network" |
| scale vision / roadmap (as a title) | "the wider vision" / "what's next" |
| amber-dashed / flagged amber | "future routes" (style stays a map directive only) |
| Quanta-LR / vessel codenames | "as Navier's range grows" / name the capability, not the SKU |
| N% capture / capture rate | "serving about N% of trips" |
| X-rung captive frame | "an N-phase revenue ladder" |
| "on these lanes" | "across these routes" |

`capture` / `captive` are allowed only in plain business sense ("a captive revenue layer you
own") — never as "~46% capture" or "captive resort mesh".

## Where copy comes from (the missing display layer)
- **Builders** (`deck-studio/builders/deck_*.py`) must emit partner-facing strings in the
  `narrative`/title/subtitle/caption fields. Do **not** f-string a finance `meaning` straight
  into a caption. Keep model labels (SOM/SAM/TAM) internal; map them to display captions.
- **Slide-2 narrative**: governed by `SPEC-deck-narrative.md` (distillation from the proposal
  prose, hard word caps). The proposal record itself must already be de-jargoned (see
  `partner-proposal-parity`).
- **KPI / economics captions**: `deck-economics-values-*.json`, `slide3-kpis-*.json`,
  `economics-binding.json` `sample_caption` fields are **rendered** — keep them plain.
  `kpi_frame`, `capture_frame`, `notes` are **internal** — finance terms are fine there.

## Hard gate — run before any deck seal/apply
```
python3 deck-studio/qa/partner_copy_lint.py deck-studio/decks/<deck>   # one deck
python3 deck-studio/qa/partner_copy_lint.py --all                      # every deck
```
Exit 0 = clean, 1 = jargon in rendered text. The linter reads only rendered fields
(editplan `insertText`/`replaceAllText`, narrative blobs) and ignores internal directives.
**A deck is not partner-ready, and Grok must not apply it, until this gate is green.**

## Division of labor
- **Tasklet** owns the partner-facing wording + this guardrail + the lint lexicon.
- **Grok** runs the deterministic builder → editplan → live apply, and must run the lint as a
  blocking gate in that pipeline (same status as the land-crossing gate).
