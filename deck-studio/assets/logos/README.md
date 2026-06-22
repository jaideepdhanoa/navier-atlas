# Partner Logo Bank

`LOGO-MANIFEST.json` is the **single source of truth** for partner cover logos. It supersedes
any "needs_sourcing" logo list in the generation-queue docs.

## Layout
```
logos/
  LOGO-MANIFEST.json        # status + provenance + cover bind target per partner
  partners/<deck_key>/      # banked binaries land here (PNG/SVG, transparent bg)
```

## Bind gate (hard)
A cover logo may be applied to a deck **only** when its manifest entry has:
`status == "banked"` AND `source_url != null` AND `drive_file_id != null`.

Otherwise the cover logo object (`p1_i5`) is **left untouched**. Never substitute a
placeholder, never guess or recreate a badge.

## Territory / Navier-only decks
`caribbean-mobility` and `french-polynesia` are `intentional_null`: Navier-only covers,
**no partner badge ever**. Same rule applies to any future Navier-only territory case
(e.g. Hong Kong). Null beats confidently-wrong.

## Sourcing rule
Official brand asset only — brand/press kit or a verified vector. Track `license` and
`provenance` on every banked entry. Publish to Drive once, record `source_url` +
`drive_file_id`, then reuse across decks that share the partner (e.g. uber-india / uber-mena).

## Current status
As of this PR: **0 banked, 12 needs_sourcing, 2 intentional_null.** Banking the binaries
(fetch official asset → license check → Drive publish → record) is the remaining step and
is intentionally **not** done here — it requires per-partner source/license decisions.
