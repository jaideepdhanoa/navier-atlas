# Grok handback — Maghreb split from MENA (`/region/maghreb`)

**Date:** 2026-06-29 · **Lane:** Tasklet content + scope_stats + gates → Grok render/deploy
**Trigger:** `docs/NOTES-FOR-TASKLET.md` §"Split Maghreb from MENA" (Jaideep call).

## What Tasklet shipped (this branch)

| Deliverable | File | State |
|---|---|---|
| New `maghreb` region brief (cluster-depth) | `data-clean/region_briefs.json` | ✅ 3 clusters · 11 cities; full sections |
| `mena` brief trimmed to Gulf/Red Sea/Levant | `data-clean/region_briefs.json` + `author-region-briefs.py` DEPTH/summary | ✅ North-Africa prose dropped |
| Author script: Maghreb own slug | `scripts/author-region-briefs.py` | ✅ `_ALIAS` Maghreb→MENA removed; `DEPTH["maghreb"]`, `SIG["maghreb"]=None` added |
| Region validator: Maghreb own display | `scripts/validate-region-briefs.py` | ✅ `REGION_ALIASES` Maghreb→MENA removed |
| Seal-fix: Maghreb own macro-region | `scripts/seal-integrity-fix.py` | ✅ `_REGION_ALIASES` Maghreb→MENA removed; comment updated |
| Cluster briefs region-tag aligned | `cluster_briefs/morocco.json`, `tunisia.json` | ✅ `region: "MENA"` → `"Maghreb"` |
| Optional Algeria cluster brief | `cluster_briefs/algeria.json` | ✅ new tag-only brief, 3 display-only signatures |

### Final scope_stats (computed, share-card-consistent)
- **`maghreb`** → **3 clusters · 11 cities** (morocco, algeria, tunisia)
- **`mena`** → **9 clusters · 22 cities**

> ⚠️ **Doc said `mena` = 27 cities; the true count is 22.** Current MENA (with alias) is 12/33;
> removing the 3 Maghreb clusters (11 cities) leaves **9 / 22**, not 9/27. The author script writes
> the *computed* value so `scope_stats == share card`. The "27" in `NOTES-FOR-TASKLET.md` was an
> arithmetic slip. Flagging for confirmation — the brief carries the truthful 22.

### `maghreb` signature_routes = `null` (intentional)
Curated Maghreb marquee corridors (Tangier–Tarifa, Gulf of Tunis, Kerkennah/Djerba, Bay of Algiers)
are **display-only** in the cluster briefs (`route_id: null`). Sealed Maghreb geometry *does* exist in
`ROUTES.json` (e.g. `e__casablanca-morocco__agadir__agadir-essaouira-morocco__*`), but none is bound to
a curated marquee label — so `null` beats confidently-wrong, same rule as Caribbean/Caspian. Bind when
Yassir/Bolt Maghreb corridors seal.

## Gates (both pass on this branch)
```
python3 scripts/validate-seal-integrity.py --strict   → exit 0
python3 scripts/validate-region-briefs.py  --strict   → 12 regions, 0 incomplete
node scripts/build-site.mjs                           → 267 partner + 1006 share pages
                                                         (/region/maghreb generated)
```

## Grok's remaining render lane (NOT done here — yours)
The `Maghreb → MENA` render alias is **still present on purpose** in the render/share layer so the live
map doesn't break before you wire the split. Remove it in:
- `scripts/region-share.mjs:13`  (`Maghreb: 'MENA',`)
- `index.html:2515`  (`'Middle East':'MENA','Maghreb':'MENA',`)
- `index.html:4161`  (`'Middle East':'MENA', 'Maghreb':'MENA' };`)

Then:
- `collectRegionStats()` separates `maghreb` + `mena` automatically (matches the Python gate).
- Region nav L1 chip: **Maghreb** as its own macro-region alongside MENA.
- Share tree: `/region/maghreb` + short `/maghreb` → `/region/maghreb` (mirror `/mena`).
- Rebuild `_dist/` + deploy.

**Agreement:** Tasklet dropped the alias from the 3 build/QA scripts (author, region-validator,
seal-fix); Grok drops it from the 2 render files above. Both lanes agree before deploy.
