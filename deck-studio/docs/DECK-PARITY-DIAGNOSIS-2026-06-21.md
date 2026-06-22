# Deck parity diagnosis — why Grok's Bolt deck misses the Tasklet bar

_2026-06-21 · compares Grok output `Bolt × Navier — PR65 sandbox` (`1sQNF5P3OjhAlSh917yO6If1OPBGnwOBvrBzGXcYZh4c`) against gold `Grab × Navier` (`18yDAgO0Sj9PJlgf6paxtgni8Pk1xRAmNwE2TD_NCdSs`)._

## TL;DR

The Bolt deck is a **byte-copy of the Grab deck** (identical object IDs: `p1`, `p1_i2…i10`, `g3eec5122801_0_*`) **truncated from 23 → 11 slides**, with a few easy single-run text boxes poked. Everything hard was left as Grab. The result fails on three axes: **correctness (leaked Grab content), brand fidelity (style reset), and layout (overflow)**. None of this is a Grok capability gap — it is a missing deterministic instruction set. We were succeeding because *Tasklet* did the precise field-level edits; the handoff never encoded that precision, so Grok improvised and improvised badly.

## The evidence (object-level)

### Slide 1 — hero
| Object | Role | Grab (gold) | Bolt (Grok) | Verdict |
|---|---|---|---|---|
| `p1_i5` | Partner logo (top-right) | Grab logo | **Still Grab's logo asset** (only re-hosted) | ❌ leaked |
| `p1_i2` | Hero background | Generic open-water | **Unchanged generic** (not European coast) | ⚠️ held, but never swapped |
| `p1_i8` | Title (Exo 2 33pt bold white, `SHAPE_AUTOFIT`) | "The water network for Southeast Asia" (37 ch) | "Bolt × Navier — the European demand platform, now on the water" (63 ch), autofit flipped to **NONE** | ❌ overflow |
| `p1_i9` | Subtitle (Poppins 13.5pt, light-grey one-liner, 87 ch) | "A premium, zero-emission water layer — in your app…" | **345-char body paragraph**, font reset to **Arial 14pt**, color reset to **default black on a near-black hero (invisible)** | ❌ wrong register + invisible + overflow |

### Slide 7 — economics (the smoking gun)
| Object | Role | Bolt (Grok) | Verdict |
|---|---|---|---|
| `g3eec5122801_0_395` | Route subhead (Poppins 11.5pt gold) | **"Marina Bay → Sentosa / Southern Islands · ~5 nm · N30 Pioneer II"** | ❌ **Grab's Singapore route left verbatim** |
| `g3eec5122801_0_397` | KPI line (10 styled runs, Exo 2, gold figures) | **"$480,870 revenue − $82,569 run cost = $398,301 profit/boat·yr · 83% margin · 1.5 yrs payback"** | ❌ **Grab's SEA economics left verbatim** — confidently-wrong, violates null-beats-wrong |
| `g3eec5122801_0_392` | Economics Sheet link | URL inserted as **Arial 14pt black** body run; sheet ID unverified as Bolt's | ⚠️ style reset + unverified sheet |
| `g3eec5122801_0_394` | "Economics and growth case" header | inserted as **Arial 14pt black** (lost Exo 2 brand head style) | ❌ style reset |

## Root-cause failure modes (all systemic, all fixable)

1. **Copy-and-poke, not field-level rebuild.** Grok duplicated the whole file and edited only the few trivial single-run boxes it could, leaving partner-specific routes, economics, logos, and imagery as Grab. The 12 dropped slides were chopped, not re-storied.
2. **Style reset on every insert.** Grok's edits use `deleteText` + `insertText`. After a full delete, inserted text reverts to the shape default (**Arial 14pt / black**). This is why brand fonts (Exo 2 / Poppins) vanished and why hero subtitle text became black-on-black. It also flipped `autofit` to `NONE`, so long strings overflow instead of shrinking.
3. **No character budget / wrong content register.** A 345-char paragraph was dropped into an ~87-char subtitle slot. Each object has a designed length; Grok had no budget to respect.
4. **Multi-run styled lines were untouched.** The economics KPI line is 10 separately-styled runs. It's hard to edit safely, so Grok skipped it — leaving Grab's numbers. This is the worst outcome (a confident wrong number).
5. **Images entirely unhandled, including the no-composite ones.** The market *background* compositing is legitimately blocked on the missing asset pack (Grok's note is correct). But the **partner logo swap needs no compositing** and was still skipped — so Bolt wears Grab's logo.

## Why this is good news

Every failure is deterministic and detectable. The fix is not "make Grok smarter" — it is "**stop asking Grok to author; hand it an object-keyed edit plan and let it apply + verify.**" That is exactly the precision Tasklet was already applying by hand. See `DETERMINISTIC-DECK-EDIT-PLAN-CONTRACT.md`.
