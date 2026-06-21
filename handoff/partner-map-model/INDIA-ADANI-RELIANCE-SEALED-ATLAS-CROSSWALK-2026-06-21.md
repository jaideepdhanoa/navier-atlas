# India Adani/Reliance sealed Atlas crosswalk — 2026-06-21

## Summary

- Sealed city-feature records: 3 (Mumbai has sealed POIs/routes even if no city point appears in FEATURES_BY_TYPE city list)
- Sealed POI counts: {'mumbai-india': 99, 'goa-india': 92, 'kerala-backwaters-india': 135, 'andaman-india': 37}
- Sealed route counts: {'mumbai-india': 29, 'goa-india': 17, 'kerala-backwaters-india': 12, 'andaman-india': 40}
- Asset-label exact hits requiring review: ['nariman', 'mormugao']
- Asset-label labels with no sealed hit: ['ulwe', 'dighi', 'agardanda', 'hazira', 'mundra', 'jamnagar', 'ghansoli', 'reliance corporate park', 'rcp', 'dahej', 'tuna', 'vizhinjam', 'kattupalli', 'ennore', 'krishnapatnam', 'gangavaram', 'dhamra', 'haldia', 'karaikal', 'gopalpur', 'patalganga', 'nagothane', 'gadimoga']

## Decision
Use `mumbai-india`, `goa-india`, `kerala-backwaters-india`, and `andaman-india` for proposal display scope. Do **not** promote Adani/Reliance asset lanes unless Grok exact-matches or mints the BP/route. Substring hits are review-only.

## Files
- `india-adani-reliance-sealed-atlas-crosswalk-2026-06-21.json` contains the full POI and route lists by city.
