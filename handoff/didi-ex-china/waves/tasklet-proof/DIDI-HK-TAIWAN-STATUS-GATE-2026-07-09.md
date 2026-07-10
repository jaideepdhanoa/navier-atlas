# DiDi Hong Kong / Taiwan operation-status gate — 2026-07-09

**Source seal:** `jaideepdhanoa/navier-atlas@ba48bc5d`  
**Finance gate:** `blocked_pending_primary_evidence`  
**Scope:** current-operation proof only; no route IDs, demand, fares, yields, or marine permissions were created.

## Status gates

| Market | Gate | Defensible disposition |
|---|---|---|
| Hong Kong | `current_operation_supported` | Clear **only for DiDi passenger taxi-hailing**. The live first-party passenger page says “歡迎喺香港乘搭DiDi”, “2018年服務香港至今”, and reports registered drivers/completed trips; the live taxi page gives an active booking workflow; the driver page gives taxi-driver onboarding. A DiDi developer listing updated 2026-06-29 says DiDi “currently” offers taxis and a Guangdong–Hong Kong cross-border car product in Hong Kong. Bloomberg (2025-04-25) corroborates “limited taxi services” and explicitly says DiDi then lacked a ride-share option. Do **not** generalize this to private-car ride-share or platform-specific regulatory approval. |
| Taiwan | `historical_only` | Historical 2018 operation and suspension are supported. PTS reported on 2018-12-19 that the Taiwan app showed “所在區域服務調整中” and was unusable; the local agent called it a suspension, not a market exit. No current first-party DiDi service roster, live Taiwan booking receipt, licensed partner-branded service, or current regulator receipt was found. A Taiwan App Store listing for the **Hong Kong** DiDi app is app availability, not Taiwan operation. Keep the hard gate. |
| Macau | `not_publicly_supported` | Held regardless. Existing country-supported Atlas binding is not a current-operation receipt. |
| Japan | `current_operation_supported` | Live DiDi Mobility Japan service areas plus dated 2026 service news support current passenger taxi operation. The current company profile names SoftBank Corp. and DiDi Mobility Pte. Ltd. as shareholders, so DiDi–SoftBank JV framing may be retained. Remote-island supply is not inferred. |

## Hong Kong distinctions

- **Taxi-hailing:** supported as current operation.
- **Passenger booking capability:** supported by live first-party booking instructions.
- **Driver app/onboarding:** supported; requested documents include a taxi-driver permit and driving licence.
- **Launch history:** live site states service since 2018.
- **App availability:** corroborative, not sufficient by itself.
- **Private-car ride-share:** not publicly supported by the evidence used here.
- **Cross-border car:** advertised booking capability is current; permission was not independently verified.
- **Permission:** no DiDi-specific government approval was found; claim remains limited to the taxi-dispatch product.

## Taiwan distinctions

- **Historical launch/service:** supported for 2018.
- **Suspension/withdrawal:** December 2018 suspension/cessation is supported; “permanent withdrawal” is not proven because the agent described it as temporary.
- **Current app availability:** a Hong Kong app can appear in the Taiwan storefront; this does not prove Taiwan service.
- **Partner-branded service:** no reliable current evidence found.
- **Present passenger operation:** not publicly supported.
- **Current permission:** not publicly supported; historical regulatory conflict does not establish present status.

## Route-by-route disposition

| Sealed candidate | Operation gate | Finance disposition |
|---|---|---|
| `tokyo-bay-kurihama-kanaya` | Japan current operation supported | `t3_buildable_null_only`; no route demand/yield/permission. |
| `tokyo-oshima` | Tokyo supported; Oshima DiDi supply unproven | `t3_buildable_null_only`. |
| `atami-oshima` | Atami supported; Oshima supply unproven | `t3_buildable_null_only`. |
| `miyajimaguchi-miyajima` | Hiroshima/Hatsukaichi service area supported | `t3_buildable_null_only`; ferry passengers are not DiDi/Navier demand. |
| `naha-zamami-aka` | Naha supported; remote-island supply unproven | `t3_buildable_null_only`. |
| `ishigaki-taketomi` | Ishigaki supported; Taketomi supply unproven | `t3_buildable_null_only`. |
| `hk-north-point-hung-hom` | Hong Kong taxi operation gate cleared | `t3_buildable_null_only`; no route demand or marine permission. |
| `kaohsiung-magong` | Taiwan `historical_only` | `blocked_pending_primary_evidence`; do not publish under DiDi. |

All `route_id`, route-demand, fare/yield, and permission values remain `null` in the JSON ledger. No IDs were minted and no totals were allocated to routes.

## Key sources

1. DiDi Hong Kong passenger site — https://hk.didiglobal.com/
2. DiDi Hong Kong taxi booking — https://hk.didiglobal.com/taxi
3. DiDi Hong Kong driver onboarding — https://hk.didiglobal.com/taxi-driver
4. DiDi developer listing, updated 2026-06-29 — https://play.google.com/store/apps/details?id=com.sdu.didi.psnger&hl=zh_TW
5. Bloomberg, 2025-04-25 — https://www.bloomberg.com/news/articles/2025-04-25/china-s-didi-recruits-ride-hailing-drivers-in-hong-kong-push
6. Taiwan Public Television Service, 2018-12-19 — https://news.pts.org.tw/article/416741
7. DiDi Mobility Japan service areas — https://didimobility.co.jp/service/user/
8. DiDi Mobility Japan company profile — https://didimobility.co.jp/aboutus/
9. DiDi Mobility Japan 2026 news — https://didimobility.co.jp/info/

## Failed-search record

- No current Taiwan-specific DiDi first-party service page or exact service-area roster.
- DiDi Australia’s public country list omits Taiwan, but also omits demonstrably current Japan/Hong Kong service; it was rejected as cessation proof.
- No current DiDi-specific Taiwan regulator or licensed operator-partner receipt.
- No reliable current Taiwan partner-branded service.
- No DiDi-specific Hong Kong platform approval; therefore no private-car legality inference.
- No route-level annual passengers, realized yield, or marine permission in operation-status sources.
