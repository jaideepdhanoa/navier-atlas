# Bay employers LOI — Vercel submission setup

Form posts JSON to **`POST /api/loi`**. Delivery is multi-sink: configure **at least one** env var on the Vercel project `navier-atlas` (Production).

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

## Option A — Google Sheet via Apps Script (easiest, no email vendor)

1. Create a Google Sheet, e.g. **Bay employer LOIs**.
2. Row 1 headers (exact order used below):

   `timestamp | name | company | role | email | cc | stop | stopLabel | line | lineLabel | employees | flavor | flavorLabel | netIncremental | perRider | seats | source`

3. **Extensions → Apps Script**, paste:

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

Smoke:

```bash
curl -sS -X POST https://navier-atlas.vercel.app/api/loi \
  -H 'Content-Type: application/json' \
  -d '{"name":"Test","company":"Navier","role":"Ops","email":"you@navierboat.com","stop":"oyster-point","stopLabel":"Oyster Point","flavor":"A","employees":"5"}'
# expect: {"ok":true,"delivered":["sheets"]}
```

---

## Option B — Slack webhook

1. Slack → App → Incoming Webhooks → add to e.g. `#bay-employers` or `#inbound`.
2. `vercel env add LOI_SLACK_WEBHOOK_URL production` → paste `https://hooks.slack.com/services/...`
3. Redeploy / next deploy.

---

## Option C — Resend email

1. Create Resend account, verify `navierboat.com` (or use `onboarding@resend.dev` for tests only).
2. `vercel env add RESEND_API_KEY production`
3. Optional: `LOI_NOTIFY_EMAIL`, `LOI_FROM_EMAIL`
4. Redeploy.

---

## Health check

```bash
curl -sS https://navier-atlas.vercel.app/api/loi
# {"ok":true,"configured":true,"sinks":{"slack":false,"sheets":true,"resend":false}}
```

---

## Local notes

- Handler lives at `api/loi.js` (copied into `_dist/api/` by `build-site.mjs`).
- Deploy surface is still **`_dist/`** via CLI (`vercel deploy --prod` from `_dist`).
- Git pushes to `main` are ignored for site build (`ignoreCommand` on root `vercel.json`); set env on the project that receives `_dist` deploys.
