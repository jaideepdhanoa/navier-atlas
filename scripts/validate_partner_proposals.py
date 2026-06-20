#!/usr/bin/env python3
"""Validate partner-pitch/partners/*.json against partner_proposal.schema.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft7Validator
except ImportError:
    print("✗ jsonschema not installed — run: pip3 install jsonschema", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parents[1]
PARTNERS = ROOT / "partner-pitch" / "partners"
SCHEMA_PATH = ROOT / "partner-pitch" / "schema" / "partner_proposal.schema.json"


def validate(schema_path: Path = SCHEMA_PATH) -> int:
    schema = json.loads(schema_path.read_text())
    validator = Draft7Validator(schema)

    files = sorted(
        p for p in PARTNERS.glob("*.json")
        if not p.name.startswith("_")
    )
    failures: list[tuple[str, list[str]]] = []
    total_errors = 0

    for path in files:
        doc = json.loads(path.read_text())
        errors = sorted(validator.iter_errors(doc), key=lambda e: list(e.path))
        if errors:
            msgs = [
                f"  {'.'.join(str(x) for x in e.path) or '$'}: {e.message}"
                for e in errors[:8]
            ]
            if len(errors) > 8:
                msgs.append(f"  ... +{len(errors) - 8} more")
            failures.append((path.name, msgs))
            total_errors += len(errors)

    print(f"Partner proposal schema validation ({schema_path.relative_to(ROOT)})")
    print(f"  files checked: {len(files)}")
    print(f"  passing: {len(files) - len(failures)}")
    print(f"  failing: {len(failures)}")
    print(f"  validation errors: {total_errors}")

    for name, msgs in failures:
        print(f"\n  ✗ {name}")
        for m in msgs:
            print(m)

    if failures:
        return 1

    print("  ✅ all partner proposals pass schema validation")
    return 0


if __name__ == "__main__":
    sys.exit(validate())