#!/usr/bin/env python3
"""
partner_copy_lint.py — hard gate against internal model taxonomy leaking onto
partner-facing slide text.

WHY THIS EXISTS
---------------
Deck builders compose slide titles/subtitles/captions straight from internal
finance + render taxonomy (SOM/SAM/TAM, "captive resort mesh", "grounded",
"network width", "amber-dashed", vessel codenames like "Quanta-LR", capture %).
That vocabulary is fine *inside the model* but is illegible and off-brand on a
partner slide. There was no layer separating model labels from display copy, so
the jargon rendered verbatim. This linter is that missing gate.

WHAT IT CHECKS
--------------
Only RENDERED text: editplan google_slides_request insertText.text /
replaceAllText.replaceText, and any builder `narrative`/title/subtitle/caption
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

# Banned in RENDERED partner text. Word-boundary, case-insensitive.
BANNED = [
    r"\bSOM\b", r"\bSAM\b", r"\bTAM\b", r"\bGMV\b",
    r"captive resort mesh", r"resort mesh", r"network width",
    r"sealed leeward geometry", r"grounded corridor", r"grounded today",
    r"amber[- ]dashed", r"scale vision", r"induced (?:market|demand|transfer|marine)",
    r"\d+%\s*capture", r"captive capture", r"capture (?:rate|basis|frame)",
    r"\d+-rung", r"captive frame",
    r"Quanta-LR", r"Quanta-SR", r"Pioneer-edge", r"\bSOM floor\b",
    r"on these lanes", r"premium water corridors", r"airport waterfront",
    r"journey wallet", r"platform-revenue line", r"mapped corridors",
    r"\baggregate\b", r"\bSAM mid\b", r"\bTAM band\b",
]
PATS = [re.compile(p, re.IGNORECASE) for p in BANNED]

def rendered_strings(editplan: dict):
    """Yield (where, text) for every partner-rendered string in an editplan."""
    ops = editplan.get("operations") or editplan.get("ops") or []
    for i, op in enumerate(ops):
        gsr = op.get("google_slides_request", {})
        if "insertText" in gsr:
            yield f"op{i}.insertText", gsr["insertText"].get("text", "")
        if "replaceAllText" in gsr:
            yield f"op{i}.replaceAllText", gsr["replaceAllText"].get("replaceText", "")
        # some builders carry a flat "text"/"narrative" preview
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
            print(f"\n✗ {os.path.basename(d)} — {len(f)} jargon hit(s):")
            for where, tok, ctx in f:
                print(f"    [{where}] «{tok}»  →  {ctx}")
    if total == 0:
        print("✓ partner-copy lint clean")
        sys.exit(0)
    print(f"\n{total} total jargon hit(s) in rendered partner text. FAIL.")
    sys.exit(1)

if __name__ == "__main__":
    main()
