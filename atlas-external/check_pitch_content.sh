#!/usr/bin/env bash
# Lightweight leak grep on ONLY the partner-facing pitch content (city briefs + partner
# proposals). This is the single new leak surface introduced during dev iteration.
# Fast (milliseconds) vs the full externalization gate that scans the whole 3.7MB page.
set -e
cd "$(dirname "$0")"
PITCH="../partner-pitch"
FILES=$(find "$PITCH/city_briefs" "$PITCH/partners" -name '*.json' 2>/dev/null || true)
[ -z "$FILES" ] && { echo "  no pitch files yet — skip"; exit 0; }
# Exclusion vocabulary (subset of partition_spec EXCLUSION_RE; the strategy/deal/name surface).
# Word-boundaries on short ambiguous tokens so legit words (liveaboard, boarding,
# investoranything) don't false-positive; mirrors partition_spec EXCLUSION_PATTERNS style.
# Precise patterns: catch deal-term / strategy / name leaks WITHOUT false-positiving
# on legit partner copy. Bare "board"/"exclusive" tripped real org names ("Tourism Board",
# "Management Board") and adjectives ("exclusive charter tier"); narrowed to risky contexts.
PAT='Sampriti|Bhattacharyya|Jaideep|Dhanoa|Founders Fund|Builders VC|Series [A-C]|finder|equity/month|go/no-go|milestone fee|board of (directors|advisors)|board seat|board member|board observer|investor board|\binvestor|\bwedge\b|\bexclusivity\b|regional exclusiv|exclusive (rights|deal|agreement|arrangement|partner|to navier)|counterparty|HubSpot|internal_only|hold_flag|gate_flag'
HIT=$(grep -rniE "$PAT" $FILES || true)
if [ -n "$HIT" ]; then
  echo "❌ PITCH CONTENT LEAK — internal vocabulary found:"; echo "$HIT"; exit 1
fi
echo "  pitch content clean ($(echo "$FILES" | wc -w | tr -d ' ') files)"
