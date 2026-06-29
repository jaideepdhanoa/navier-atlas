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
DATA_PARTNERS = ROOT / "data-clean" / "partners"
SCHEMA_PATH = ROOT / "partner-pitch" / "schema" / "partner_proposal.schema.json"
ROUTE_LINKAGE_AUDIT = ROOT / "handoff" / "partner-map-model" / "PARTNER-ROUTE-LINKAGE-AUDIT.json"

# --- Narrative (slide-2 exec-summary) readiness -------------------------------
# gen_deck_narrative.py distills slide 2 from these proposal fields. A partner that
# gets a CONSUMER partner deck (with the exec-summary slide) must carry all five, or
# the slide can only render partial/null. Scoped by archetype: authority/transit and
# captive cover-cases do not carry this slide and are exempt (null beats wrong).
NARRATIVE_FIELDS = ["partner_context", "hero", "why_now", "network_thesis", "proof_points"]
DECK_ELIGIBLE_ARCHETYPES = {"ridehail", "super_app", "corporate"}
# Explicit exemptions (Navier-only / no-logo cover cases or authority pass) even if archetype matches:
NARRATIVE_EXEMPT = set()  # add partner_ids here with a documented reason if ever needed


def narrative_readiness() -> tuple[int, list[str]]:
    """Report which DECK-ELIGIBLE partners are missing slide-2 narrative source fields."""
    files = sorted(p for p in PARTNERS.glob("*.json") if not p.name.startswith("_"))
    gaps: list[tuple[str, str, list[str]]] = []
    eligible = 0
    for path in files:
        doc = json.loads(path.read_text())
        arch = doc.get("archetype", "")
        pid = doc.get("partner_id", path.stem)
        if arch not in DECK_ELIGIBLE_ARCHETYPES or pid in NARRATIVE_EXEMPT:
            continue
        eligible += 1
        missing = [f for f in NARRATIVE_FIELDS if not doc.get(f)]
        if missing:
            gaps.append((pid, arch, missing))
    lines = ["", "Slide-2 narrative readiness (deck-eligible archetypes: "
             + ", ".join(sorted(DECK_ELIGIBLE_ARCHETYPES)) + ")",
             f"  deck-eligible partners: {eligible}",
             f"  narrative-ready: {eligible - len(gaps)}",
             f"  missing fields: {len(gaps)}"]
    for pid, arch, missing in gaps:
        lines.append(f"  ✗ {pid} [{arch}] — missing: {', '.join(missing)}")
    if not gaps:
        lines.append("  ✅ every deck-eligible partner carries all slide-2 narrative fields")
    return len(gaps), lines


def validate(schema_path: Path = SCHEMA_PATH, *, partner_filter: list[str] | None = None) -> int:
    schema = json.loads(schema_path.read_text())
    validator = Draft7Validator(schema)

    files = sorted(
        p for p in PARTNERS.glob("*.json")
        if not p.name.startswith("_")
        and (not partner_filter or p.stem in partner_filter)
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

    schema_ok = not failures
    if schema_ok:
        print("  ✅ all partner proposals pass schema validation")

    # Narrative readiness report (advisory; skip when scoping to explicit partners)
    if not partner_filter:
        narr_gaps, narr_lines = narrative_readiness()
        print("\n".join(narr_lines))
    else:
        narr_gaps = 0

    strict_narr = "--strict-narrative" in sys.argv
    strict_link = "--strict-linkage" in sys.argv
    if strict_link:
        import subprocess
        audit_args = [sys.executable, str(ROOT / "scripts/audit-partner-route-linkage.mjs"), "--strict"]
        if "--global-linkage" in sys.argv:
            audit_args.append("--global")
        r = subprocess.run(audit_args, cwd=ROOT)
        if r.returncode != 0:
            print("\n  ✗ --strict-linkage: route linkage audit failed")
            return 1
        print("  ✅ route linkage audit passed (--strict-linkage)")
    elif ROUTE_LINKAGE_AUDIT.exists():
        audit = json.loads(ROUTE_LINKAGE_AUDIT.read_text())
        s = audit.get("summary", {})
        print(
            f"\nRoute linkage audit ({ROUTE_LINKAGE_AUDIT.relative_to(ROOT)}): "
            f"{s.get('partners_with_gaps', '?')} partners with gaps · "
            f"{s.get('partners_story_ready', '?')} story-ready · "
            f"run: node scripts/audit-partner-route-linkage.mjs"
        )
    else:
        print("\nRoute linkage audit: not found — run: node scripts/audit-partner-route-linkage.mjs")

    if not schema_ok:
        return 1
    if strict_narr and narr_gaps:
        print("\n  ✗ --strict-narrative: deck-eligible partners missing narrative fields")
        return 1
    return 0


if __name__ == "__main__":
    pf: list[str] = []
    if "--partner" in sys.argv:
        i = sys.argv.index("--partner")
        pf = [a for a in sys.argv[i + 1 :] if not a.startswith("--")]
    sys.exit(validate(partner_filter=pf or None))