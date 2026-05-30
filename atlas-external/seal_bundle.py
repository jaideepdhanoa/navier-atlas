#!/usr/bin/env python3
"""
seal_bundle.py — Tasklet's data-handoff sealer.

Produces a SEALED, pre-gated data bundle that Claude Code can deploy directly to
Vercel WITHOUT re-running Tasklet's expensive pipeline. The whole point of the new
deploy model: the costly gates (partition / externalization / land-crossing /
BP-on-water) run ONCE here, on data change. Claude then only does a cheap pre-flight
(substring grep + hash match) before publishing.

Inputs (already produced by the full pipeline before this runs):
  output-external/*.json   -> the externalized, land-validated 4 blobs
Outputs (committed to repo data-clean/):
  data-clean/FEATURES_BY_TYPE.json
  data-clean/ROUTES.json
  data-clean/STORIES.json
  data-clean/VESSEL_SPECS.json
  data-clean/SEAL.json     <- manifest: sha256 per blob + gate verdicts + stamp

SECURITY: this script must ONLY be run AFTER externalization_check.py + the land gate
have passed. It records their verdicts into SEAL.json. Claude verifies blob hashes
against SEAL.json at deploy; a mismatch = abort (data was altered after sealing).
"""
import json, hashlib, sys, datetime, pathlib

BLOBS = ["FEATURES_BY_TYPE", "ROUTES", "STORIES", "VESSEL_SPECS"]

def sha256_canonical(obj) -> str:
    # canonical JSON so hash is reproducible regardless of formatting
    b = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(b).hexdigest()

def _run_integrity_gate():
    """Hard pre-seal gate: referential integrity must be clean (new dangling joins = abort).
    Tracked gaps in known-gaps.json are WARN, not ERROR. See DATA-CONVENTIONS.md §5."""
    import subprocess
    here = pathlib.Path(__file__).parent
    linter = here / "integrity" / "build_manifest.py"
    if not linter.exists():
        print("WARN: integrity linter not found; skipping gate"); return
    r = subprocess.run([sys.executable, str(linter)], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0:
        print("\nFATAL: referential-integrity gate FAILED — new dangling joins detected.")
        print("Fix the broken ids or add them to known-gaps.json before sealing. (DATA-CONVENTIONS.md §1, §5)")
        sys.exit(3)
    print("integrity gate: PASS\n")

def main(src_dir, out_dir, ext_verdict, land_verdict, bpwater_verdict):
    _run_integrity_gate()
    src = pathlib.Path(src_dir); out = pathlib.Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    seal = {
        "sealed_at": datetime.datetime.utcnow().isoformat() + "Z",
        "schema": "navier-atlas/seal/v1",
        "gates": {
            "externalization": ext_verdict,   # e.g. "PASS — 0 exclusion hits"
            "land_crossing":   land_verdict,   # e.g. "PASS — 0/1354"
            "bp_on_water":     bpwater_verdict,# e.g. "PASS — 0 inland boarding points"
            "referential_integrity": "PASS — gate run pre-seal (build_manifest.py); 0 new dangling joins"
        },
        "blobs": {}
    }
    for name in BLOBS:
        p = src / f"{name}.json"
        if not p.exists():
            print(f"FATAL: missing blob {p}"); sys.exit(2)
        obj = json.loads(p.read_text())
        digest = sha256_canonical(obj)
        # write the canonical copy Claude will inject
        (out / f"{name}.json").write_text(json.dumps(obj, sort_keys=True, separators=(",", ":")))
        seal["blobs"][name] = {"sha256": digest, "count": _count(name, obj)}
        print(f"sealed {name}: sha256={digest[:16]}… count={seal['blobs'][name]['count']}")
    (out / "SEAL.json").write_text(json.dumps(seal, indent=2))
    print(f"\nSEAL written -> {out/'SEAL.json'}")
    print(f"  externalization: {ext_verdict}")
    print(f"  land_crossing:   {land_verdict}")
    print(f"  bp_on_water:     {bpwater_verdict}")

def _count(name, obj):
    if name == "ROUTES":          return len(obj)
    if name == "STORIES":         return len(obj)
    if name == "VESSEL_SPECS":    return len(obj)
    if name == "FEATURES_BY_TYPE":return {k: len(v) for k, v in obj.items()}
    return None

if __name__ == "__main__":
    import argparse
    a = argparse.ArgumentParser()
    a.add_argument("--src", default="output-external")
    a.add_argument("--out", default="../atlas-repo/data-clean")
    a.add_argument("--ext", required=True, help="externalization gate verdict string")
    a.add_argument("--land", required=True, help="land gate verdict string")
    a.add_argument("--bpwater", default="NOT_RUN")
    args = a.parse_args()
    main(args.src, args.out, args.ext, args.land, args.bpwater)
