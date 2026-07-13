#!/usr/bin/env python3
"""Emit the deterministic, in-place WETA live-deck update batches.

This does not create or replace a presentation. It validates the pinned live deck
and emits the exact Slides API request batches applied to the existing deck.
"""
import argparse,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
PLAN=json.loads((HERE/"live-update-requests.json").read_text())
def main():
 p=argparse.ArgumentParser(); p.add_argument("--presentation-id",default=PLAN["presentation_id"]); p.add_argument("--output",default="-"); a=p.parse_args()
 if a.presentation_id!=PLAN["presentation_id"]: raise SystemExit("Refusing to target a different presentation ID")
 out=json.dumps(PLAN,indent=2)+"\n"
 if a.output=="-": print(out,end="")
 else: Path(a.output).write_text(out)
if __name__=="__main__": main()
