#!/usr/bin/env python3
"""
partner_copy_lint.py — hard gate against internal model taxonomy leaking onto
partner-facing slide text.

WHY THIS EXISTS
---------------
Deck builders compose slide titles/subtitles/captions straight from internal
finance + render taxonomy (SOM/SAM/TAM, "captive resort mesh", "grounded",
"network width" / "WIDTH", "amber-dashed", vessel codenames like "Quanta-LR",
capture %, "sealed geometry", "discretionary marine", "BP grounding"). That
vocabulary is fine *inside the model* but is illegible and off-brand on a
partner slide. There was no layer separating model labels from display copy, so
the jargon rendered verbatim. This linter is that missing gate.

WHAT IT CHECKS
--------------
Only RENDERED text: editplan google_slides_request insertText.text /
replaceAllText.replaceText, and any builder narrative/title/subtitle/caption
strings present in the editplan. Pure-internal fields (kpi_frame, capture_frame,
notes, render directives such as "amber-dashed on map only", source_pointer,
rationale) are NOT linted.

USAGE
-----
  python partner_copy_lint.py <deck-dir>        # one deck
  python partner_copy_lint.py --all             # every deck under decks/
Exit code 0 = clean, 1 = jargon found (use in CI / pre-seal gate).
"""
import json, re, sys, glob, os

DECKS_DIR = os.path.join(os.path.dirname(__file__), "..", "decks")

# Banned in RENDERED partner text, case-INSENSITIVE. Word-boundary where it matters.
BANNED_CI = [
    r"\bSOM\b", r"\bSAM\b", r"\bTAM\b", r"\bGMV\b",
    r"captive resort mesh", r"resort mesh", r"network width",
    r"captive floor", r"captive economics", r"captive transfer",
    r"captive guest (?:base|throughput)", r"captive boat-only", r"captive case",
    r"captive mesh", r"captive frame", r"captive capture",
    r"sealed leeward geometry", r"sealed geometry",
    r"grounded corridor", r"grounded today",
    r"grounded (?:cluster|properties|property|floor|floors|leisure)",
    r"BP[- ]?ground(?:ing|ed)", r"cascade-ready", r"live-network adjacency",
    r"economics_ready", r"city mobility share",
    r"discretionary marine", r"leisure-marine",
    r"amber[- ]dashed", r"scale vision", r"induced (?:market|demand|transfer|marine)",
    r"\d+%\s*capture", r"capture (?:rate|basis|frame|share)",
    r"\d+-rung",
    r"Quanta-LR", r"Quanta-SR", r"Pioneer-edge", r"\bSOM floor\b",
    r"on these lanes", r"premium water corridors", r"airport waterfront",
    r"journey wallet", r"guest wallet", r"platform-revenue line", r"mapped corridors",
    r"\baggregate\b", r"\bSAM mid\b", r"\bTAM band\b",
    # network-topology / sealing taxonomy (leaked into Grab Thailand)
    r"\bmesh\b", r"cascade corridor", r"\bsealed\b", r"pending seal",
    r"anchor corridor",
]
# Banned case-SENSITIVE (so ordinary lowercase words like "width" pass clean).
BANNED_CS = [
    r"\bWIDTH\b",
    r"Bucket[- ]?[A-Z]\b",   # internal demand-bucket codenames (Bucket-C, Bucket A …)
]
PATS = [re.compile(p, re.IGNORECASE) for p in BANNED_CI] + [re.compile(p) for p in BANNED_CS]

def rendered_strings(editplan: dict):
    """Yield (where, text) for every partner-rendered string in an editplan."""
    ops = editplan.get("operations") or editplan.get("ops") or []
    for i, op in enumerate(ops):
        gsr = op.get("google_slides_request", {})
        if "insertText" in gsr:
            yield f"op{i}.insertText", gsr["insertText"].get("text", "")
        if "replaceAllText" in gsr:
            yield f"op{i}.replaceAllText", gsr["replaceAllText"].get("replaceText", "")
    for key in ("narrative", "rendered_text", "slide_text"):
        blob = editplan.get(key)
        if isinstance(blob, dict):
            for k, v in blob.items():
                if isinstance(v, str):
                    yield f"{key}.{k}", v

def lint_deck(deck_dir: str):
    ep = os.path.join(deck_dir, "deck.editplan.json")
    if not os.path.exists(ep):
        return []
    editplan = json.load(open(ep))
    findings = []
    for where, text in rendered_strings(editplan):
        if not text:
            continue
        for pat in PATS:
            m = pat.search(text)
            if m:
                findings.append((where, m.group(0), text.replace("\n", " ")[:120]))
    return findings

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(2)
    if args[0] == "--all":
        dirs = sorted(d for d in glob.glob(os.path.join(DECKS_DIR, "*")) if os.path.isdir(d))
    else:
        dirs = args
    total = 0
    for d in dirs:
        f = lint_deck(d)
        if f:
            total += len(f)
            print(f"\n\u2717 {os.path.basename(d)} \u2014 {len(f)} jargon hit(s):")
            for where, tok, ctx in f:
                print(f"    [{where}] \u00ab{tok}\u00bb  \u2192  {ctx}")
    if total == 0:
        print("\u2713 partner-copy lint clean")
        sys.exit(0)
    print(f"\n{total} total jargon hit(s) in rendered partner text. FAIL.")
    sys.exit(1)

if __name__ == "__main__":
    main()
