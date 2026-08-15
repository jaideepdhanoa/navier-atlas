# Multi-city employer hub LOI — Vercel + Google Sheets setup

Form posts JSON to **`POST /api/loi`** from every employer hub:

- `/employers/bay-area` · `/bay-employers`
- `/employers/new-york` · `/ny-employers`
- Future cities: `/employers/<id>` (+ aliases)

**One Google Sheet tab for all hubs.** Each row includes `hub` / `hub_id` (`bay-area`, `new-york`, …). Do not create a separate tab per city unless product explicitly asks.

Delivery is multi-sink: configure **at least one** env var on the Vercel project `navier-atlas` (Production).

| Env var | Purpose |
|---------|---------|
| `LOI_SHEETS_WEBHOOK_URL` | Google Apps Script web app (or any) that appends a row — **recommended** |
| `LOI_SHEETS_WEBHOOK_SECRET` | Optional shared secret checked by the Apps Script |
| `LOI_SLACK_WEBHOOK_URL` | Slack incoming webhook for instant pings |
| `RESEND_API_KEY` | Optional email via [Resend](https://resend.com) |
| `LOI_NOTIFY_EMAIL` | Resend to-address (default `jaideep@navierboat.com`) |
| `LOI_FROM_EMAIL` | Resend from (must be a verified domain, e.g. `Navier <loi@navierboat.com>`) |

Frontend falls back to `mailto:` if the API returns 5xx / is offline so interest is never dropped.

---

## Option A — Google Sheet via Apps Script (recommended)

1. Create (or rename) a Google Sheet, e.g. **Employer hub LOIs** (not Bay-only).
2. Row 1 headers — **exact order** used by the Apps Script below:

```
timestamp | hub | name | company | role | email | cc | stop | stopLabel | line | lineLabel | employees | flavor | flavorLabel | netIncremental | perRider | seats | tripFrom | tripFromLabel | tripTo | tripToLabel | tripNavierMin | tripDriveMin | tripTransfers | tripSummary | source
```

| Column | Meaning |
|--------|---------|
| `hub` | Hub id (`bay-area`, `new-york`, …) |
| `stop` / `stopLabel` | Office terminal chosen on the LOI form |
| `line` / `lineLabel` | Preferred line (or empty / “Not sure yet”) |
| `tripFrom*` / `tripTo*` / `tripNavierMin` / `tripDriveMin` / `tripTransfers` / `tripSummary` | **Find my ride** context if the user ran a trip before submitting (empty otherwise) |
| `source` | Same as hub id from the microsite |

3. **Extensions → Apps Script**, paste (replace any older Bay-only script):

```javascript
const SHEET_NAME = 'LOIs'; // or first sheet
const SHARED_SECRET = ''; // optional; must match LOI_SHEETS_WEBHOOK_SECRET

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents || '{}');
    if (SHARED_SECRET && data.secret !== SHARED_SECRET) {
      return ContentService.createTextOutput(JSON.stringify({ ok: false, error: 'unauthorized' }))
        .setMimeType(ContentService.MimeType.JSON);
    }
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sh = ss.getSheetByName(SHEET_NAME) || ss.getSheets()[0];
    sh.appendRow([
      data.timestamp || new Date().toISOString(),
      data.hub || data.hub_id || data.source || '',
      data.name || '',
      data.company || '',
      data.role || '',
      data.email || '',
      data.cc || '',
      data.stop || '',
      data.stopLabel || '',
      data.line || '',
      data.lineLabel || '',
      data.employees || '',
      data.flavor || '',
      data.flavorLabel || '',
      data.netIncremental || '',
      data.perRider || '',
      data.seats || '',
      data.tripFrom || '',
      data.tripFromLabel || '',
      data.tripTo || '',
      data.tripToLabel || '',
      data.tripNavierMin || '',
      data.tripDriveMin || '',
      data.tripTransfers || '',
      data.tripSummary || '',
      data.source || '',
    ]);
    return ContentService.createTextOutput(JSON.stringify({ ok: true }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ ok: false, error: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
```

4. **Deploy → New deployment → Web app**
   - Execute as: **Me**
   - Who has access: **Anyone**
5. Copy the web app URL → Vercel:

```bash
vercel env add LOI_SHEETS_WEBHOOK_URL production
# paste URL
# optional:
vercel env add LOI_SHEETS_WEBHOOK_SECRET production
```

6. Redeploy so the function sees the env (or wait for next CLI deploy from `_dist`).

### Migrating an existing Bay-only sheet

If your header row stopped at `source` (18 columns):

1. Insert **8 columns** before `source` (or append them before the last column if you prefer).
2. Set headers: `tripFrom | tripFromLabel | tripTo | tripToLabel | tripNavierMin | tripDriveMin | tripTransfers | tripSummary`
3. Redeploy the Apps Script (new deployment or “Manage deployments → Edit → New version”) so `appendRow` length matches.
4. Old rows leave the new cells blank — fine.

### Smoke tests

```bash
# Bay
curl -sS -X POST https://navier-atlas.vercel.app/api/loi \
  -H 'Content-Type: application/json' \
  -d '{
    "name":"Test","company":"Navier","role":"Ops","email":"you@navierboat.com",
    "stop":"oyster-point","stopLabel":"Oyster Point",
    "flavor":"A","employees":"5",
    "hub_id":"bay-area","source":"bay-area",
    "tripFrom":"larkspur","tripFromLabel":"Larkspur Ferry Terminal",
    "tripTo":"oyster-point","tripToLabel":"Oyster Point",
    "tripNavierMin":"59","tripDriveMin":"75","tripTransfers":"1",
    "tripSummary":"Larkspur Ferry Terminal → Oyster Point · ~59 min Navier vs ~75 min drive · 1 transfer(s)"
  }'

# NY
curl -sS -X POST https://navier-atlas.vercel.app/api/loi \
  -H 'Content-Type: application/json' \
  -d '{
    "name":"Test","company":"Navier","role":"Ops","email":"you@navierboat.com",
    "stop":"pier11","stopLabel":"Pier 11 / Wall Street",
    "flavor":"A","employees":"5",
    "hub_id":"new-york","source":"new-york"
  }'
# expect: {"ok":true,"delivered":["sheets"]}
```

Filter the sheet by `hub` = `bay-area` vs `new-york`.

---

## Option B — Slack webhook

1. Slack → App → Incoming Webhooks → add to e.g. `#employer-lois` or `#inbound`.
2. `vercel env add LOI_SLACK_WEBHOOK_URL production` → paste `https://hooks.slack.com/services/...`
3. Redeploy / next deploy.

Slack messages include **Hub** and **Find my ride** when present.

---

## Option C — Resend email

1. Create Resend account, verify `navierboat.com` (or use `onboarding@resend.dev` for tests only).
2. `vercel env add RESEND_API_KEY production`
3. Optional: `LOI_NOTIFY_EMAIL`, `LOI_FROM_EMAIL`
4. Redeploy.

Subject line format: `Employer LOI (<hub_id>) — <company>`.

---

## Health check

```bash
curl -sS https://navier-atlas.vercel.app/api/loi
# {"ok":true,"configured":true,"sinks":{"slack":false,"sheets":true,"resend":false}}
```

---

## Local notes

- Handler: `api/loi.js` (copied into `_dist/api/` by `build-site.mjs`).
- Deploy surface is still **`_dist/`** via CLI (`vercel deploy --prod` from `_dist`).
- Git pushes to `main` are ignored for site build (`ignoreCommand` on root `vercel.json`); set env on the project that receives `_dist` deploys.
- Frontend: `employer-hub/template/hub.js` → `buildLoiPayload()` attaches trip fields from the last successful **Find my ride** run (`lastTripSnapshot`).
