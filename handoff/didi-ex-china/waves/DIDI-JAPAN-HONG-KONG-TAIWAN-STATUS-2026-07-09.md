# DiDi Japan / Hong Kong / Taiwan deepening status — 2026-07-09

## Status

**Research-complete with explicit gates / seal-needed.** No repository files were edited.

- **Japan:** current official DiDi Mobility Japan roster gives exact support for Niseko/Kutchan, Tokyo/Yokosuka, Atami/Ito, Setouchi cities, Naha, Miyakojima and Ishigaki. Preserve **DiDi–SoftBank JV** framing.
- **Hong Kong:** ferry/BP evidence is strong. DiDi status is **verification-needed**: the Hong Kong app-store receipt does not alone prove an exact current city service area.
- **Taiwan:** **gate retained.** Current Kaohsiung–Penghu ferry service is sourced, but no current official DiDi Taiwan operation receipt was found.
- **Macau:** do not overclaim; the existing country-supported Atlas binding is not an exact current operation receipt.

## Evidence banked

- 25 source records, primarily official operator, government, airport, tourism and DiDi/SoftBank sources.
- 18 source-verified terminal records; all coordinates deliberately null pending official coordinate and Atlas BP confirmation.
- 8 candidate corridors; all `route_id` values deliberately null pending exact `ROUTES.json` matching.
- 9 fare/demand records. Broad airport/visitor flows are context only; no tourism count was converted into route demand, and all `annual_one_way_pax` values remain null.

## Strong current route examples

- Kurihama–Kanaya: about 40 minutes; JPY 1,100 adult one-way.
- Tokyo/Atami–Oshima: current Tokai Kisen 2026 summer schedules; fares still need route-specific extraction.
- Naha Tomari–Zamami/Aka: JPY 2,900 regular ferry or JPY 3,950 high-speed boat, plus JPY 100 island tax.
- Miyajimaguchi–Miyajima: JPY 180 adult one-way, plus JPY 100 visitor tax.
- North Point–Hung Hom: daily, about 8 minutes, HKD 10 adult one-way (effective 2025-01-25).
- Kaohsiung–Magong/Penghu: current 2026 operator calendar, but DiDi Taiwan partner gate remains.

## Blockers

1. `/tmp/navier-atlas` was unavailable, so `CLUSTERS.json`, `ROUTES.json`, canonical briefs and matching BP JSONs could not be reviewed directly.
2. Canonical brief maturity is field-scaffolded but not scored; wholesale replacement is not recommended.
3. Exact route IDs, BP coordinates and existing BP bindings need Atlas/Grok seal work.
4. Current official Hong Kong and Taiwan DiDi operating receipts remain open; Taiwan is a hard gate.
5. Route-specific annual passenger counts remain unavailable; finance must not substitute broad visitor or airport flows.

## Artifact

`/tasklet/agent/home/didi-ex-china-audit/waves/DIDI-JAPAN-HONG-KONG-TAIWAN-DEEPENING-2026-07-09.json`
