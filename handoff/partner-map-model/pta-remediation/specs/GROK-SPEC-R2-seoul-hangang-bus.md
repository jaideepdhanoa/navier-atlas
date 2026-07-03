# GROK SPEC — R2 Seed-and-Seal · seoul-hangang-bus

**Lane:** Grok geometry (mint new BPs + route + seal at 0 km land, hand-waypoints).
**Source:** https://www.hgbus.co.kr/itc/information/location (official)
**Discipline:** ID-based match only; null-beats-wrong; inherit real network 1:1; never invent corridors. Approx seed coords below — geocode precisely, keep names authoritative.

## Existing BPs (reuse — do NOT re-mint)
- `bp-7ee5f26a66` — Magok
- `bp-kakao-yeouido` — Yeouido
- `bp-kakao-ttukseom` — Ttukseom
- `bp-kakao-jamsil` — Jamsil

## New BPs to mint (4)
- **Mangwon Pier** — seed `hgb-mangwon` — ~(37.5527, 126.8965) · 205-8 Mangwon-dong, Mapo-gu
- **Oksu Pier** — seed `hgb-oksu` — ~(37.5407, 127.014) · 86 Oksu-dong, Seongdong-gu
- **Apgujeong Pier** — seed `hgb-apgujeong` — ~(37.5233, 127.015) · Apgujeong-ro 11-gil 37-29, Gangnam-gu
- **Seoul Forest Wharf** — seed `hgb-seoul-forest` — ~(37.5445, 127.038) · 697 Seongsu-dong 1-ga, Seongdong-gu

## Service sequence (all-stops)
Magok → Mangwon → Yeouido → Oksu → Apgujeong → Seoul Forest → Ttukseom → Jamsil

## Corridors to seal (7)
- ▸ **Magok ↔ Mangwon**
- ▸ **Mangwon ↔ Yeouido**
- ▸ **Yeouido ↔ Oksu**
- ▸ **Oksu ↔ Apgujeong**
- ▸ **Apgujeong ↔ Seoul Forest**
- ▸ **Seoul Forest ↔ Ttukseom**
- ▸ **Ttukseom ↔ Jamsil**

## Hand-waypoint guidance
Follow the Han River channel throughout. Route stays mid-channel; boats zigzag between north bank (Magok, Mangwon, Yeouido, Oksu, Seoul Forest, Ttukseom) and south bank (Apgujeong, Jamsil). No bridges block navigation — pass under Seongsan, Yanghwa, Wonhyo, Hangang, Dongjak, Banpo, Dongho, Seongsu, Yeongdong, Cheonho bridges.

## Write-back
- Bind `route_id`/`route_ids` per corridor into `data-clean/partners/seoul-hangang-bus.json` + partner-pitch tree; `_link_status: sealed`.
- Serialization: data-clean ascii/indent2/newline; partner-pitch non-ascii/indent2/newline.
- Re-run land QA; confirm 0 crossings; append receipts to gap table.