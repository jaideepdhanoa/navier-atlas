#!/usr/bin/env python3
"""
gen_deck_narrative.py — deterministic exec-summary (slide 2) content for a partner deck.

The partner proposal narrative is the SOURCE OF TRUTH; the slide is a DISTILLATION of it.
This is the narrative analogue of gen_deck_economics.py: it reads the structured proposal
JSON and emits the renderer-ready slide-2 sidecar. No prose is authored here — every field
is extracted verbatim-leading-sentence from the proposal, with hard word caps that FLAG
(never silently mangle) overflow, so distillation stays honest.

Usage:
    python3 gen_deck_narrative.py <partner>
    python3 gen_deck_narrative.py grab --validate   # reproduce committed bar-setter

Reads:   partner-pitch/partners/<partner>.json
Writes:  deck-studio/decks/<partner>/narrative-slide2-<partner>.json

Slide-2 schema (exec-summary / thesis), keyed for the renderer:
    partner_lockup      "Grab × Navier"            (from hero.title, before em-dash)
    positioning         headline, <= 8 words       (hero.title, after em-dash)
    thesis              subhead, <= 25 words        (hero.subtitle)
    the_deal            1 line, <= 40 words         (hero.what_we_do_together, lead sentence)
    your_world[4]       today / up_against /        (partner_context.* + why_now,
                        navier_fits / why_now,       each lead sentence, <= 25 words)
    proof_strip[<=4]    {label,value,sub,sources}   (network_thesis.stats + proof_points sources)
"""
import json, sys, re, datetime, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Beats (the 2x2 "Your world" grid) are explicitly TEASERS: short pointers that
# physically hold ~2 lines in the slide box. The full thought lives in the proposal
# and on the dedicated why-now slide. So beats use a tighter cap and a clause-aware
# trim (distinct from thesis/the_deal, which never truncate mid-thought).
CAPS = {"positioning": 8, "thesis": 25, "the_deal": 40,
        "today": 16, "up_against": 16, "navier_fits": 16, "why_now": 16}
CLAUSE_BREAKS = (";", ":", " — ", " \u2014 ", ",")

# ----- deterministic text helpers -------------------------------------------------
_ABBR = ("U.S.", "e.g.", "i.e.", "vs.", "Mr.", "St.")

def split_sentences(text):
    """Sentence list. Splits on '. ' but protects $-amounts and known abbreviations."""
    if not text:
        return []
    t = " ".join(text.split())
    out, start = [], 0
    for m in re.finditer(r"\.(\s)", t):
        i = m.start()
        if i > 0 and i + 1 < len(t) and t[i-1].isdigit() and t[i+1].strip()[:1].isdigit():
            continue  # decimal, not a boundary
        if any(t[max(0, i-len(a)+1):i+1] == a for a in _ABBR):
            continue
        out.append(t[start:i+1].strip())
        start = i + 1
    tail = t[start:].strip()
    if tail:
        out.append(tail)
    return out

def distill(text, cap):
    """Fill whole sentences up to the word cap. If the first sentence alone exceeds
    the cap, return it unmangled (caller flags) — null beats confidently-wrong."""
    sents = split_sentences(text)
    if not sents:
        return ""
    acc, total = [], 0
    for s in sents:
        w = wc(s)
        if acc and total + w > cap:
            break
        acc.append(s); total += w
    return " ".join(acc).strip()

def wc(s):
    return len(s.split())

def distill_beat(text, cap):
    """Teaser distillation for the 2x2 'Your world' beats only. Fills whole sentences
    up to cap (like distill). If the lead sentence alone still exceeds cap, trim at the
    last clause boundary (; : em-dash ,) that keeps it <= cap, append an ellipsis. Beats
    are pointers, not full thoughts, so a clause-level trim is intended here (unlike the
    thesis/deal which are emitted unmangled)."""
    s = distill(text, cap)
    if not s or wc(s) <= cap:
        return s, False           # fit cleanly, no trim
    words = s.split()
    # try clause boundaries, longest-that-fits first
    best = None
    for i in range(len(words), 0, -1):
        frag = " ".join(words[:i])
        if wc(frag) > cap:
            continue
        if any(frag.rstrip().endswith(b.strip()) or (b.strip() and b.strip() in frag[-2:]) for b in CLAUSE_BREAKS):
            best = frag; break
        # also accept a fragment whose NEXT char in original was a clause break
        nxt = s[len(frag):len(frag)+2]
        if nxt[:1] in (";", ":", ",") or nxt.strip()[:1] == "\u2014":
            best = frag; break
    if best is None:
        best = " ".join(words[:cap])
    best = best.rstrip(" ,;:\u2014-")
    return best + "\u2026", True

NUM_TOKEN = re.compile(r"\$[\d.]+[BMK%]?|\b\d[\d,]*(?:\.\d+)?%?\b")

def find_numbers(s):
    return [m.group(0) for m in NUM_TOKEN.finditer(s or "")]

# ----- build -----------------------------------------------------------------------
def build(partner):
    src_path = os.path.join(ROOT, "partner-pitch", "partners", f"{partner}.json")
    with open(src_path) as f:
        d = json.load(f)

    warnings = []

    def capped(key, text, field_label):
        s = distill(text, CAPS[key])
        if s and wc(s) > CAPS[key]:
            warnings.append(f"{field_label}: lead sentence is {wc(s)}w > cap {CAPS[key]}w — tighten the source proposal; emitted unmangled (null beats confidently-wrong).")
        return s or None

    def capped_beat(key, text, field_label):
        s, trimmed = distill_beat(text, CAPS[key])
        if trimmed:
            warnings.append(f"{field_label}: source clause-trimmed to <= {CAPS[key]}w for the beat teaser — tighten the source proposal for a clean break (the full thought stays in the proposal + the why-now slide).")
        return s or None

    hero = d.get("hero", {})
    title = hero.get("title", "")
    # split "Grab × Navier — the black-car network, on the water"
    lockup, positioning = None, None
    if "—" in title:
        lockup, rest = title.split("—", 1)
        lockup = lockup.strip()
        positioning = rest.strip()
    else:
        positioning = title.strip() or None
    if positioning and wc(positioning) > CAPS["positioning"]:
        warnings.append(f"positioning: {wc(positioning)}w > cap {CAPS['positioning']}w — tighten hero.title; emitted unmangled.")

    pc = d.get("partner_context", {})
    your_world = [
        {"key": "today",       "label": "Where you are today",   "text": capped_beat("today",       pc.get("their_ambition", ""),   "your_world.today")},
        {"key": "up_against",  "label": "What you're up against", "text": capped_beat("up_against",  pc.get("their_pressure", ""),   "your_world.up_against")},
        {"key": "navier_fits", "label": "Where Navier fits",      "text": capped_beat("navier_fits", pc.get("where_navier_fits", ""), "your_world.navier_fits")},
        {"key": "why_now",     "label": "Why now",                "text": capped_beat("why_now",     d.get("why_now", ""),           "your_world.why_now")},
    ]

    # proof strip: stats + matched sources from proof_points (external claims carry provenance)
    sources = []
    for p in d.get("proof_points", []):
        s = p.get("source")
        if s and s not in sources:
            sources.append(s)
    proof_strip = []
    for st in d.get("network_thesis", {}).get("stats", []):
        proof_strip.append({
            "label": st.get("label"), "value": st.get("value"), "sub": st.get("sub"),
            "_external": True,
        })

    out = {
        "_doc": "Slide-2 exec-summary / thesis. DISTILLED from the partner proposal; proposal is source of truth.",
        "_generator": "gen_deck_narrative.py",
        "_generated_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "_source_file": f"partner-pitch/partners/{partner}.json",
        "partner_id": d.get("partner_id", partner),
        "slide": 2,
        "role": "exec_summary_thesis",
        "partner_lockup": lockup,
        "positioning": positioning,
        "thesis": capped("thesis", hero.get("subtitle", ""), "thesis"),
        "the_deal": capped("the_deal", hero.get("what_we_do_together", ""), "the_deal"),
        "your_world": your_world,
        "proof_strip": proof_strip,
        "proof_sources": sources,
        "_provenance_note": "Distilled leading sentences from the proposal; word caps flag (never truncate) overflow. External numbers (e.g. partner financials, regulator dates) are sourced facts — see proof_sources — not model outputs; model numbers belong to the economics sidecar.",
    }

    # no-orphan-numbers guard: any number shown on the slide must be backed by a source.
    shown = []
    for f in ("thesis", "the_deal"):
        shown += find_numbers(out[f] or "")
    for b in your_world:
        shown += find_numbers(b["text"] or "")
    if shown and not sources:
        warnings.append(f"orphan-numbers: slide shows {shown} but proof_sources is empty — attach provenance or remove the figure.")
    out["_orphan_number_check"] = {"numbers_shown": shown, "has_sources": bool(sources),
                                   "status": "ok" if (not shown or sources) else "FLAG"}
    if warnings:
        out["_warnings"] = warnings
    return out, warnings


def main():
    if len(sys.argv) < 2:
        print("usage: gen_deck_narrative.py <partner> [--validate]"); sys.exit(2)
    partner = sys.argv[1]
    validate = "--validate" in sys.argv
    out, warnings = build(partner)
    out_path = os.path.join(ROOT, "deck-studio", "decks", partner, f"narrative-slide2-{partner}.json")

    if validate:
        if not os.path.exists(out_path):
            print(f"VALIDATE: no committed file at {out_path}"); sys.exit(1)
        committed = json.load(open(out_path))
        a = {k: v for k, v in out.items() if not k.startswith("_generated")}
        b = {k: v for k, v in committed.items() if not k.startswith("_generated")}
        if a == b:
            print(f"VALIDATE OK: {partner} reproduces committed narrative-slide2 field-for-field.")
            sys.exit(0)
        print("VALIDATE FAIL: drift vs committed:")
        for k in sorted(set(a) | set(b)):
            if a.get(k) != b.get(k):
                print(f"  {k}:\n    gen={a.get(k)}\n    committed={b.get(k)}")
        sys.exit(1)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"wrote {out_path}")
    for w in warnings:
        print("  WARN:", w)


if __name__ == "__main__":
    main()
