# WETA / SF Bay — why some items were “not to mint”, and what we bound

## Why these were held (not auto-minted)

| Hold | Why not mint |
|---|---|
| **Palo Alto** | Hand-launch / non-motorized facility — not a WETA passenger terminal. Minting a commercial `rn-*` would invent service geometry. |
| **Alviso** | Tide / bathymetry / facility hold — channel access is not always navigable; partner-ready seal left it null on purpose. |
| **seaplane ↔ mission_bay, harbor_bay ↔ oyster_point, oyster_point chain, san_leandro pairs** | Published **expansion candidates**, not sealed WETA service OD pairs with both BPs + schedule proof in the Lane A set. Geometry can be authored later as Lane B/C. |
| **richmond/berkeley/vallejo ↔ larkspur** | Cross-agency / non-WETA combinations (Larkspur is Golden Gate Ferry context). |
| **Marin / Golden Gate** | **Context only** — Golden Gate Ferry is a separate operator; not WETA service to claim as Navier×WETA product. |

Null beats wrong: we do not mint service routes for facilities that are not motorized passenger terminals or that belong to another operator.

## What looked “empty / unbound” but was already geometry

Lane A **already** minted geometry + hand waypoints for Richmond, Vallejo, South SF (Oyster Point), etc. (`pta_hand_waypoints_sf_bay_ferry.json` = 18/18 filled).

The **partner page phase featured_routes** for Richmond / SSF / Vallejo still had `route_id: null` — a **bind gap**, not missing geometry. Journeys already carried:

| Phase row | Existing route_id |
|---|---|
| SF Ferry Building ↔ Richmond | `rn-91fd068e22f6` |
| SF Ferry Building ↔ South SF (Oyster Point) | `rn-c0b8c9297a26` |
| SF Ferry Building ↔ Vallejo | `rn-b8709495c648` |

**2026-07-14 action:** rebind those three phase rows in `data-clean/partners/sf-bay-ferry.json` + `partner-pitch/partners/sf-bay-ferry.json`.

## PTA empty hand-waypoint files (global)

Empty `pta_hand_waypoints_*.json` pairs usually mean the **PTA pair catalog was never back-filled** from existing `ROUTES.json` geometry — not that the market has no water routing. Use:

```bash
python3 scripts/pta/inherit_pta_hand_waypoints_from_routes.py --all-empty --apply
```

Unmatched pairs still need dossier node anchors or human spines.
