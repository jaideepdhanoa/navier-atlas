#!/usr/bin/env python3
"""PTA remediation orchestrator — route wave specs to seal/bind tooling."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REMEDIATION = ROOT / "handoff/partner-map-model/pta-remediation"
SPECS = REMEDIATION / "specs"
DOSSIERS = REMEDIATION / "dossiers"
SEAL_SCRIPT = ROOT / "scripts/pta/seal_authority.py"
BATCH5_SCRIPT = ROOT / "scripts/pta/apply_batch5_binds.py"

WAVE_SPECS: dict[str, str | None] = {
    "R1": "GROK-SPEC-R1-mintheavy-seal.md",
    "R2": None,
    "R3": "GROK-SPEC-R3-greenfield-anchor-deepening.md",
    "R4": "GROK-SPEC-R4-R5-seal-and-chip-hygiene.md",
}

R1_PARTNERS = frozenset(
    {
        "rotterdam-mrdh",
        "oslo-ruter",
        "amsterdam-gvb",
        "copenhagen-movia",
        "gothenburg-vasttrafik",
        "wellington-metlink",
    }
)

R2_PARTNERS = frozenset({"calmac", "seoul-hangang-bus", "kolkata-wbtc"})

R4_BATCH5 = frozenset(
    {
        "singapore-mpa",
        "abu-dhabi-itc",
        "bahrain-motc",
        "dubai-rta",
        "qatar",
        "rakta",
    }
)


def resolve_spec(wave: str, partner: str) -> Path | None:
    if wave == "R2":
        path = SPECS / f"GROK-SPEC-R2-{partner}.md"
        return path if path.is_file() else None
    name = WAVE_SPECS.get(wave)
    if not name:
        return None
    path = SPECS / name
    return path if path.is_file() else None


def resolve_dossier(wave: str, partner: str) -> Path | None:
    candidates = [
        DOSSIERS / f"PTA-DOSSIER-{partner}.json",
        DOSSIERS / "R2" / f"{partner}.json",
        ROOT / "handoff/partner-map-model" / f"PTA-DOSSIER-{partner}.json",
    ]
    if wave == "R2":
        candidates.insert(0, DOSSIERS / "R2" / f"{partner}.json")
    for path in candidates:
        if path.is_file():
            return path
    return None


def run(cmd: list[str]) -> int:
    print(f"→ {' '.join(cmd)}")
    return subprocess.call(cmd, cwd=ROOT)


def validate_wave_partner(wave: str, partner: str) -> str | None:
    if wave == "R1" and partner not in R1_PARTNERS:
        return f"{partner} not in R1 mint-heavy set"
    if wave == "R2" and partner not in R2_PARTNERS:
        return f"{partner} not in R2 marquee set"
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="PTA remediation wave orchestrator")
    ap.add_argument("--wave", required=True, choices=["R1", "R2", "R3", "R4"])
    ap.add_argument("--partner", required=True, help="Partner slug")
    ap.add_argument("--apply", action="store_true", help="Write outputs (seal/bind)")
    args = ap.parse_args()

    wave = args.wave.upper()
    partner = args.partner.strip()

    err = validate_wave_partner(wave, partner)
    if err:
        print(f"✗ {err}", file=sys.stderr)
        return 1

    spec = resolve_spec(wave, partner)
    dossier = resolve_dossier(wave, partner)

    print(f"wave={wave} partner={partner}")
    print(f"  spec:    {spec.relative_to(ROOT) if spec else '(none)'}")
    print(f"  dossier: {dossier.relative_to(ROOT) if dossier else '(none)'}")

    if not spec:
        print(f"✗ no spec for wave={wave} partner={partner}", file=sys.stderr)
        return 1

    if wave == "R4" and partner in R4_BATCH5:
        cmd = [sys.executable, str(BATCH5_SCRIPT)]
        if args.apply:
            cmd.append("--apply")
        else:
            cmd.append("--dry-run")
        if args.apply:
            cmd.append("--verify-economics-hash")
        return run(cmd)

    if not dossier:
        print(f"✗ no dossier for {partner}", file=sys.stderr)
        return 1

    cmd = [sys.executable, str(SEAL_SCRIPT), "--partner", partner]
    if args.apply:
        cmd.append("--apply")
    return run(cmd)


if __name__ == "__main__":
    raise SystemExit(main())