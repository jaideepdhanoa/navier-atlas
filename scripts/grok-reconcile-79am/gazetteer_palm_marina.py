#!/usr/bin/env python3
"""Tasklet source-backed Palm/Marina boarding-point gazetteer matcher."""
from __future__ import annotations

import re
from pathlib import Path

from reconcile_shared import _slug, load_json


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").lower().strip())


class PalmMarinaGazetteer:
    def __init__(self, data: dict):
        self.data = data
        self.entries = data.get("entries", [])
        self.excluded = data.get("excluded_candidates", [])
        self._name_index: dict[str, dict] = {}
        self._canonical: dict[str, str] = {}
        self._build_index()

    def _build_index(self):
        for entry in self.entries:
            source_id = entry["source_id"]
            canonical = entry.get("collapse_to") or source_id
            self._canonical[source_id] = canonical
            for name in [entry["name"]] + entry.get("aliases", []):
                self._name_index[_norm(name)] = entry

    @classmethod
    def load(cls, work: Path | None = None) -> PalmMarinaGazetteer:
        candidates = []
        if work:
            candidates.extend(
                [
                    work / "RECONCILE" / "palm-marina-boarding-point-gazetteer.json",
                    work / "grok-routing-output" / "palm-marina-boarding-point-gazetteer.json",
                ]
            )
        root = Path(__file__).resolve().parents[2]
        candidates.append(root / "grok-routing-output" / "palm-marina-boarding-point-gazetteer.json")
        for path in candidates:
            if path.exists():
                return cls(load_json(path))
        raise FileNotFoundError("palm-marina-boarding-point-gazetteer.json not found")

    def canonical_source_id(self, source_id: str) -> str:
        return self._canonical.get(source_id, source_id)

    def match_name(self, name: str) -> dict | None:
        n = _norm(name)
        if not n:
            return None
        if n in self._name_index:
            return self._name_index[n]
        best = None
        best_len = 0
        for entry in self.entries:
            for candidate in [entry["name"]] + entry.get("aliases", []):
                cn = _norm(candidate)
                if cn in n or n in cn:
                    if len(cn) > best_len:
                        best = entry
                        best_len = len(cn)
        return best

    def is_excluded(self, name: str) -> tuple[bool, str | None]:
        n = _norm(name)
        for row in self.excluded:
            for pat in row.get("patterns", []):
                if re.search(pat, n, re.I):
                    return True, row.get("name")
        if re.fullmatch(r"dubai marina mall", n):
            return True, "Dubai Marina Mall retail POI"
        return False, None

    def promoteable(self, name: str) -> tuple[bool, dict | None]:
        excluded, _ = self.is_excluded(name)
        if excluded:
            return False, None
        entry = self.match_name(name)
        if not entry or entry.get("confidence") not in ("high", "medium"):
            return False, None
        return True, entry

    def high_confidence_entries(self) -> list[dict]:
        return [e for e in self.entries if e.get("confidence") == "high"]