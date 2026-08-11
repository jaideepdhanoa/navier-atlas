/**
 * POST /api/loi — Bay Area employer LOI intake.
 *
 * Accepts JSON from /bay-employers form. Delivers to any configured sinks:
 *   LOI_SLACK_WEBHOOK_URL   Slack incoming webhook
 *   LOI_SHEETS_WEBHOOK_URL  Google Apps Script (or any) URL that appends a row
 *   RESEND_API_KEY          optional email via Resend
 *   LOI_NOTIFY_EMAIL        to-address for Resend (default jaideep@navierboat.com)
 *   LOI_FROM_EMAIL          from-address for Resend (must be verified domain)
 *
 * At least one sink must be set in Vercel project env (Production).
 */

const MAX_LEN = {
  name: 120,
  company: 160,
  role: 120,
  email: 200,
  stop: 80,
  stopLabel: 160,
  line: 40,
  lineLabel: 160,
  employees: 40,
  cc: 200,
  flavor: 8,
  flavorLabel: 80,
  netIncremental: 40,
  perRider: 40,
  seats: 20,
  hp: 0, // honeypot must be empty
};

function json(res, status, body) {
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.status(status).json(body);
}

function cors(res, origin) {
  // Same-origin form; allow Atlas prod + localhost for smoke tests
  const allow = [
    'https://navier-atlas.vercel.app',
    'https://navier-atlas-jaideepdhanoas-projects.vercel.app',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:8788',
  ];
  if (origin && allow.includes(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
    res.setHeader('Vary', 'Origin');
  }
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
}

function str(v, max) {
  if (v == null) return '';
  return String(v).trim().slice(0, max);
}

function isEmail(s) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s);
}

function parseBody(req) {
  if (req.body && typeof req.body === 'object') return req.body;
  if (typeof req.body === 'string' && req.body) {
    try {
      return JSON.parse(req.body);
    } catch {
      return null;
    }
  }
  return null;
}

function normalize(raw) {
  const d = {
    name: str(raw.name, MAX_LEN.name),
    company: str(raw.company, MAX_LEN.company),
    role: str(raw.role, MAX_LEN.role),
    email: str(raw.email, MAX_LEN.email).toLowerCase(),
    stop: str(raw.stop, MAX_LEN.stop),
    stopLabel: str(raw.stopLabel || raw.stop, MAX_LEN.stopLabel),
    line: str(raw.line, MAX_LEN.line),
    lineLabel: str(raw.lineLabel || raw.line || 'Not sure yet', MAX_LEN.lineLabel),
    employees: str(raw.employees, MAX_LEN.employees) || 'n/a',
    cc: str(raw.cc, MAX_LEN.cc).toLowerCase(),
    flavor: str(raw.flavor, MAX_LEN.flavor) || 'A',
    flavorLabel: str(
      raw.flavorLabel ||
        (raw.flavor === 'B' ? 'Option B — Anchor a line' : 'Option A — Reserve seats'),
      MAX_LEN.flavorLabel
    ),
    netIncremental: str(raw.netIncremental, MAX_LEN.netIncremental),
    perRider: str(raw.perRider, MAX_LEN.perRider),
    seats: str(raw.seats, MAX_LEN.seats),
    hp: str(raw.hp, 20), // honeypot
    source: str(raw.source || raw.hub_id || 'employer-hub', 40),
    hub_id: str(raw.hub_id || raw.source || 'employer-hub', 40),
    submittedAt: new Date().toISOString(),
  };
  return d;
}

function validate(d) {
  if (d.hp) return 'spam';
  if (!d.name || !d.company || !d.role) return 'missing_fields';
  if (!d.email || !isEmail(d.email)) return 'invalid_email';
  if (d.cc && !isEmail(d.cc)) return 'invalid_cc';
  if (!d.stop) return 'missing_stop';
  return null;
}

function sinksConfigured() {
  return {
    slack: Boolean(process.env.LOI_SLACK_WEBHOOK_URL),
    sheets: Boolean(process.env.LOI_SHEETS_WEBHOOK_URL),
    resend: Boolean(process.env.RESEND_API_KEY),
  };
}

function textSummary(d) {
  return [
    `Non-binding LOI — ${d.company}`,
    `Path: ${d.flavorLabel}`,
    `Name: ${d.name}`,
    `Role: ${d.role}`,
    `Email: ${d.email}`,
    d.cc ? `CC: ${d.cc}` : null,
    `Nearest terminal: ${d.stopLabel}`,
    `Preferred line: ${d.lineLabel}`,
    `Est. employees: ${d.employees}`,
    d.seats || d.netIncremental
      ? `Planning est.: ${d.netIncremental || '—'} net/mo · ${d.perRider || '—'}/rider · ${d.seats || '—'} seats`
      : null,
    `Hub: ${d.hub_id || d.source}`,
    `Source: ${d.source}`,
    `At: ${d.submittedAt}`,
  ]
    .filter(Boolean)
    .join('\n');
}

async function sendSlack(d) {
  const url = process.env.LOI_SLACK_WEBHOOK_URL;
  if (!url) return { skip: true };
  const payload = {
    text: `🌊 *Employer LOI* (${d.hub_id || d.source}) — *${d.company}* (${d.flavorLabel})`,
    blocks: [
      {
        type: 'header',
        text: { type: 'plain_text', text: `Employer LOI · ${d.company}`, emoji: true },
      },
      {
        type: 'section',
        fields: [
          { type: 'mrkdwn', text: `*Hub*\n${d.hub_id || d.source}` },
          { type: 'mrkdwn', text: `*Path*\n${d.flavorLabel}` },
          { type: 'mrkdwn', text: `*Employees*\n${d.employees}` },
          { type: 'mrkdwn', text: `*Name*\n${d.name}` },
          { type: 'mrkdwn', text: `*Role*\n${d.role}` },
          { type: 'mrkdwn', text: `*Email*\n${d.email}` },
          { type: 'mrkdwn', text: `*Terminal*\n${d.stopLabel}` },
          { type: 'mrkdwn', text: `*Line*\n${d.lineLabel}` },
          { type: 'mrkdwn', text: `*CC*\n${d.cc || '—'}` },
        ],
      },
      {
        type: 'context',
        elements: [
          {
            type: 'mrkdwn',
            text: `Planning est. ${d.netIncremental || '—'} net/mo · ${d.perRider || '—'}/rider · ${d.submittedAt}`,
          },
        ],
      },
    ],
  };
  const r = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!r.ok) {
    const t = await r.text().catch(() => '');
    throw new Error(`slack ${r.status}: ${t.slice(0, 200)}`);
  }
  return { ok: true };
}

async function sendSheets(d) {
  const url = process.env.LOI_SHEETS_WEBHOOK_URL;
  if (!url) return { skip: true };
  // Apps Script expects a flat JSON body; shared secret optional
  const payload = {
    secret: process.env.LOI_SHEETS_WEBHOOK_SECRET || undefined,
    timestamp: d.submittedAt,
    hub: d.hub_id || d.source,
    hub_id: d.hub_id || d.source,
    name: d.name,
    company: d.company,
    role: d.role,
    email: d.email,
    cc: d.cc,
    stop: d.stop,
    stopLabel: d.stopLabel,
    line: d.line,
    lineLabel: d.lineLabel,
    employees: d.employees,
    flavor: d.flavor,
    flavorLabel: d.flavorLabel,
    netIncremental: d.netIncremental,
    perRider: d.perRider,
    seats: d.seats,
    source: d.source,
  };
  const r = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!r.ok) {
    const t = await r.text().catch(() => '');
    throw new Error(`sheets ${r.status}: ${t.slice(0, 200)}`);
  }
  return { ok: true };
}

async function sendResend(d) {
  const key = process.env.RESEND_API_KEY;
  if (!key) return { skip: true };
  const to = process.env.LOI_NOTIFY_EMAIL || 'jaideep@navierboat.com';
  const from = process.env.LOI_FROM_EMAIL || 'Navier Atlas <onboarding@resend.dev>';
  const body = {
    from,
    to: [to],
    reply_to: d.email,
    subject: `Bay employer LOI — ${d.company}`,
    text: textSummary(d),
  };
  if (d.cc) body.cc = [d.cc];
  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${key}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });
  if (!r.ok) {
    const t = await r.text().catch(() => '');
    throw new Error(`resend ${r.status}: ${t.slice(0, 200)}`);
  }
  return { ok: true };
}

export default async function handler(req, res) {
  const origin = req.headers.origin || '';
  cors(res, origin);

  if (req.method === 'OPTIONS') {
    res.status(204).end();
    return;
  }

  if (req.method === 'GET') {
    const s = sinksConfigured();
    const any = s.slack || s.sheets || s.resend;
    json(res, 200, { ok: true, configured: any, sinks: s });
    return;
  }

  if (req.method !== 'POST') {
    json(res, 405, { ok: false, error: 'method_not_allowed' });
    return;
  }

  const raw = parseBody(req);
  if (!raw) {
    json(res, 400, { ok: false, error: 'invalid_json' });
    return;
  }

  const d = normalize(raw);
  const err = validate(d);
  if (err === 'spam') {
    // Pretend success to bots
    json(res, 200, { ok: true, delivered: [] });
    return;
  }
  if (err) {
    json(res, 400, { ok: false, error: err });
    return;
  }

  const configured = sinksConfigured();
  if (!configured.slack && !configured.sheets && !configured.resend) {
    json(res, 503, {
      ok: false,
      error: 'not_configured',
      message:
        'No LOI sink configured. Set LOI_SLACK_WEBHOOK_URL, LOI_SHEETS_WEBHOOK_URL, and/or RESEND_API_KEY on Vercel.',
    });
    return;
  }

  const delivered = [];
  const failures = [];

  const jobs = [
    ['slack', sendSlack],
    ['sheets', sendSheets],
    ['resend', sendResend],
  ];

  for (const [name, fn] of jobs) {
    try {
      const result = await fn(d);
      if (result?.skip) continue;
      delivered.push(name);
    } catch (e) {
      failures.push({ sink: name, message: String(e?.message || e).slice(0, 200) });
      console.error('[loi]', name, e);
    }
  }

  if (delivered.length === 0) {
    json(res, 502, {
      ok: false,
      error: 'delivery_failed',
      failures,
    });
    return;
  }

  json(res, 200, {
    ok: true,
    delivered,
    failures: failures.length ? failures : undefined,
  });
}
