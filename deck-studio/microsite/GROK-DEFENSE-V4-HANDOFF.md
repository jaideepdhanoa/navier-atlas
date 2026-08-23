# /defense v4 — Grok Build Handoff (2026-08-23)

Contract: `deck-studio/microsite/contracts/defense.json` (version 4). This spec covers only the v3 → v4 deltas plus the new gate system. Everything not listed here renders exactly as the live v3 build.

## 1 · Content deltas

| # | Where | Change |
|---|---|---|
| 1 | `def-hero.subline` | Defense-specific subline replaces the world-moves line. Headline OWN THE EDGE unchanged. |
| 2 | `def-navier` | Rebuilt as a defense-first opener: two-line body (lead weight) → three stat-led `beats` (gold heads, grey body — same treatment as the capability rail) → `beats_source_line` in fine print → doctrine gold link chip (new tab) → hangar plate → 1080p launch film unchanged. The /invest verbatim thesis paragraphs are REMOVED on this route. |
| 3 | `def-dual-use.resilience_thesis` | New titled block, opens the DUAL-USE beat (before `sub_line` + `fine_print`): kicker THE DEFENSE THESIS, title "Global Resilience.", body + smaller grey `support_line`. |
| 4 | `def-flight` clip `flat-turning` | Title is now **"Coordinated turns at high speed"**. Caption unchanged. |
| 5 | `def-family` N45 card | New image `assets/deck/n45-defense-container-v1.png` (single aft ISO container — in this PR). New `defense_lens` + `image_note` from contract. |
| 6 | `def-family` all cards | **CROP RULE (bug fix):** vessel must never crop out at any viewport width (founder screenshot showed the N30 card losing the vessel entirely on phone). Aspect-preserving `object-fit: contain` on a fixed plate, or authored per-breakpoint crops. Prove at 390/768/1280/1440/2560. |

## 2 · Gate v2 — email + revocable per-recipient codes

Replaces the shared password entirely (`plainview` retired).

**Form:** Work email + Access code. Client validates email shape; ALL code validation is server-side. The codes list must never ship to the client in any form.

**API route `/api/defense-access` (POST `{email, code}`):**

```ts
const codes = JSON.parse(process.env.DEFENSE_ACCESS_CODES || "{}");
const entry = codes[(code || "").trim().toUpperCase()];
if (!entry?.active) return res.status(403).json({ ok: false }); // denied_copy from contract
// fire-and-forget — logging failure must NEVER block access
fetch(process.env.DEFENSE_ACCESS_LOG_WEBHOOK, {
  method: "POST",
  body: JSON.stringify({
    timestamp_utc: new Date().toISOString(),
    email: (email || "").trim(),
    code: (code || "").trim().toUpperCase(),
    recipient_label: entry.label,
    user_agent: req.headers["user-agent"] || "",
  }),
}).catch(() => {});
// set session cookie scoped to /defense, then ok:true
```

**Env vars (Vercel — set by Jaideep, never committed):**
- `DEFENSE_ACCESS_CODES` — JSON map `{"CODE": {"label": "Recipient", "active": true}, ...}`. The live codes are in the **Access Codes tab** of the log Sheet (ID in contract `gate.logging.sheet_id`). Do not copy codes into the repo, the PR, or this spec.
- `DEFENSE_ACCESS_LOG_WEBHOOK` — Apps Script web-app URL (Jaideep manual step below).

**Revocation:** flip `active:false` for one code and redeploy — others unaffected.

**Apps Script for the log Sheet (Jaideep pastes via Extensions → Apps Script, deploys as Web app: execute as me / access: anyone, copies URL into `DEFENSE_ACCESS_LOG_WEBHOOK`):**

```js
function doPost(e) {
  var sh = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Access Log");
  var d = JSON.parse(e.postData.contents);
  sh.appendRow([
    d.timestamp_utc || new Date().toISOString(),
    d.email || "", d.code || "", d.recipient_label || "", d.user_agent || "", ""
  ]);
  return ContentService.createTextOutput("ok");
}
```

## 3 · QA gates (fail the build on any miss)

1. **Leak scan** — the contract's `leak_scan_terms_must_be_zero`, case-insensitive, word-bounded both sides, on rendered page text. Zero hits.
2. **No financial content** anywhere on the route (standing rule).
3. **Crop-rule proof** — all four family cards at 390/768/1280/1440/2560, vessel fully visible in every shot.
4. **No clipping / no ellipsis / no text under 24px** at 1280/1440/2560.
5. **Gate tests** — screenshots or recording: valid code admits + Sheet row appears; unknown code denied; revoked (`active:false`) code denied; malformed email blocked client-side; codes absent from all client bundles (grep the build output).
6. **noindex** — meta tag AND `X-Robots-Tag` header; route stays unlisted.
7. **≥12 named screenshots** including: hero subline, 01 opener (beats + doctrine chip), resilience block, retitled turns tile, N45 container card, the 390px family strip, and all gate states.
8. Videos: 10 bound, autoplay/muted/lightbox behaviors per contract; launch film 1080p with audio on click.

## 4 · Jaideep manual steps (after Grok ships)
1. Apps Script deploy on the log Sheet → URL → `DEFENSE_ACCESS_LOG_WEBHOOK` (Vercel).
2. `DEFENSE_ACCESS_CODES` (Vercel) — JSON assembled from the Sheet's Access Codes tab.
3. Review screenshots + scans on the PR → merge → live QA (agent).
4. Send Kinetica: /defense URL + their code + the public Doctrine link (defense-audience-only note).
