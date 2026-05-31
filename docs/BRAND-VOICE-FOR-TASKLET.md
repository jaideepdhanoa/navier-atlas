# Navier brand — soft voice notes for Tasklet (content lane)

_From the render + deploy lane (Claude Code) to the data/content lane (Tasklet)._
_Pairs with `NOTES-FOR-TASKLET.md` (running handoff log) and the Navier brand guidelines._

> **Read this as optional polish, not a directive.** The Atlas already has rich, well-judged
> substance in the city briefs and partner proposals. Nothing here asks for a rewrite, a schema
> change, or a change to any **fact, number, or claim**. These are gentle phrasing nudges to apply
> **only where they fall out naturally** — and only if/when you're already touching a field.

---

## 0. TL;DR — what is and isn't being asked

- **Not asked:** rewriting briefs/pitches; changing facts, ranges, counts, or proof points;
  restructuring fields; adding work. Substance and schema stay exactly as they are.
- **Asked (soft):** when you next author or revise a string, lean slightly toward Navier's voice —
  declarative, precise, confident, brief. That's it.

## 1. What the **front-end already handles** (so you don't have to)

All *visual / typographic* brand alignment now lives in `index.html` chrome and needs nothing from you:

- Caps + letter-spacing on labels and section headers, the amber under-rule, the dark+gold palette.
- **Numerics rendered in mono** (ranges like `≤70 nm`, knots, counts). You keep supplying the same
  figures in the same fields — the render styles them. Don't pre-format or uppercase anything in data.

So the only lever on *your* side is **word choice**, and only in the fields you author.

## 2. The voice, in one breath

Confident, precise, forward-leaning, lightly defiant. Engineering swagger without hype.
Lead with the capability, not the caveat. Numbers as proof. Never cute, never eco-piety, never over-explained.

**Signature patterns** (from the brand site + deck): short declarative period-stopped fragments;
three-beat rhythms ("Cost. Comfort. Convenience."); "the boat of the future, today"; "own the edge".

## 3. Light do / don't (illustrative — not mandates)

| Field | Softer-but-flat | Navier-leaning |
|---|---|---|
| `brief.tagline` | "A potential market for premium electric boating services." | "Riviera flagship. Electric, today." |
| `partner.the_ask` | "We would propose to possibly explore two vessels." | "Two Pioneer II hulls. One season." |
| `partner.why_now` | "It could be a good time because of various trends." | "The window is open now. Aerospace-grade, available today." |
| `partner.close` | "We hope this might be of interest." | "Own the edge." |

Note the shifts: drop hedges ("possibly", "could", "we hope"); cut to declarative; keep a precise
number as the proof. Same meaning, fewer words.

## 4. Where this applies (your fields)

Highest-leverage, most-read strings — nudge here first, leave the rest:

- **City briefs:** `tagline`, `summary`, `navier_fit`, `use_cases`, `partner_overlays[].lead_with`.
- **Partner proposals:** `the_ask`, `close.title` / `close.body`, `why_now`, `hero`, `end_state`,
  `phases[].narrative`. Keep `proof_points`, `objections`, and all figures factual and unchanged.

## 5. Two guardrails

1. **Eco-piety:** state sustainability as fact and consequence ("zero emissions", "near-silent"),
   never as moral appeal. (Navier is premium-dark + gold, deliberately *not* eco-green.)
2. **The §3.2 leak guard still rules.** Brand phrasing must never reintroduce an excluded token
   (see `EXCLUSION-TOKENS.txt`) — e.g. the recent "exclusivity" abort. Voice changes don't get a pass
   on the pre-flight gate.

---

_This file is a living reference — edit freely. It carries no facts, only tone guidance._
