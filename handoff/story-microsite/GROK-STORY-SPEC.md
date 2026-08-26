# /story microsite — SPEC v3 (watch reel)

**Supersedes GROK-STORY-SPEC.md v2 in full.** v2 cloned the `/invest` argument
(thesis → costs → GMVP → dual-use essay → Atlas). That is a pitch. `/story` is
the one URL an investor opens to **watch the films and read the articles**.

## The v3 law

**Watch + read. One URL. No homework.**

- Public, noindex, no password. Forwardable.
- Every film plays on the page (self-hosted mp4 or YouTube lightbox). Never
  “open this YouTube link” as the primary action.
- Every article is an on-page press card (outlet + verbatim published headline).
- No new slogans. Section labels are functional: Watch, Ride, Films, Press, Contact.
- Captions, film titles, press headlines, and the demo-grid title/lede are copied
  VERBATIM from `/invest` contracts or `VIDEO-INVENTORY.md`.
- Leak-scan + Robb Report + 400V/100kW kill-list unchanged from v2.
- `/story` stays strictly thinner than `/teaser` / `/invest` / `/defense`.

## Section order (binding)

`hero` → `ride` → `films` → `field` → `press` → `talk`

Do not add a thesis chapter, three-costs, GMVP ladder, Atlas, or dual-use essay.

## Beats

1. **Hero** — cinema loop (`hero-loop.mp4`) + **Watch the film** (label from
   `hero.json`) opening the self-hosted launch film 1080p in a lightbox with
   sound. Eyebrow only: `NAVIER — AN AMERICAN MARITIME COMPANY`. No thesis as H1.
   Public-record chips sit **below** the cinema, not on the film.
2. **Ride** — `/invest` Traction demo grid, equal-weight tiles, muted loop,
   click for sound. Title `Don't take our word for it` + lede + five clip
   captions from `proof.json` `demo-grid`, verbatim. Includes `flat-turning.mp4`.
3. **Films** — three large plates (CTO `S7WB91FvSFI`, Sampriti `QhiaYVgXMf0`,
   Vance `ZNgh39DM_Jg`). Verified titles + durations. Click → lightbox with sound.
   Launch film is the hero CTA only — do not duplicate here.
4. **Field** — public-record row only: TE 26-3 montage (native 826×720 letterbox)
   + SAS officers still. No dual-use body copy, no SOF Week armed plate, no 400V.
5. **Press** — WSJ, National Interest, TechCrunch, Axios (verbatim headlines) +
   Doctrine link. Robb Report never named.
6. **Talk** — Reply to Sampriti · investors@ copy · request materials.

## Visual system

- Port `/invest` demo-grid (`.video-grid.equal-grid`, `.vcard-loop`, duration chip,
  gold play, caption under). Click toggles mute/unmute — same as `/invest`.
- Feature films are large plates (≥70% width), not a thumbnail shelf.
- FILMED/RENDER badge on every visual (field TE loop + SAS still included).
- Text never sits on a photo background except the hero scrim.
- No text under 24px on headlines at 1280/1440/2560. No ellipsis on headlines.

## Kill-list

Unchanged from v2: 31-term scan + Robb Report + 400V / 100 kW / LC-180.
No round, valuations, TAM, pipeline names, sea-grid, unit economics, N30D.

## QA

1. Leak scan = 0 hits.
2. Demo-grid title, lede, and five captions byte-equal to `proof.json` `demo-grid`.
3. Film titles byte-equal to `/invest` `product.json` / `money.json` / `hero.json`.
4. Press headlines byte-equal to authored cards.
5. Analytics events unchanged: section_view, video_play, video_complete,
   outbound_click, cta_click.
