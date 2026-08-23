/**
 * POST /api/defense-access — /defense email + per-recipient code gate.
 *
 * Body: { email, code }
 * Env:
 *   DEFENSE_ACCESS_CODES   JSON map {"CODE":{"label":"Recipient","active":true},...}
 *   DEFENSE_ACCESS_LOG_WEBHOOK  optional Apps Script / Sheet webhook (fire-and-forget)
 *   AUTH_SECRET            HMAC secret for session cookie (shared with middleware)
 *
 * Codes never ship to the client. Logging failure must never block access.
 */

const COOKIE = 'navier_defense';
const SESSION_SLUG = '__defense__';
const MAX_AGE = 60 * 60 * 24 * 14;
const DENIED = "That code isn't active. Contact sampriti@navierboat.com.";

function json(res, status, body, extraHeaders) {
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  if (extraHeaders) {
    for (const [k, v] of Object.entries(extraHeaders)) res.setHeader(k, v);
  }
  res.status(status).json(body);
}

function cors(res, origin) {
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

function isEmail(s) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s);
}

function parseBody(req) {
  if (req.body && typeof req.body === 'object') return req.body;
  if (typeof req.body === 'string' && req.body) {
    try {
      return JSON.parse(req.body);
    } catch {
      return {};
    }
  }
  return {};
}

function loadCodes() {
  const raw = process.env.DEFENSE_ACCESS_CODES;
  if (!raw || !String(raw).trim()) return null;
  try {
    const parsed = JSON.parse(raw);
    return parsed && typeof parsed === 'object' ? parsed : null;
  } catch {
    return null;
  }
}

async function sessionToken() {
  const secret = process.env.AUTH_SECRET;
  if (!secret) return null;
  const enc = new TextEncoder();
  const key = await crypto.subtle.importKey(
    'raw',
    enc.encode(secret),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );
  const sig = await crypto.subtle.sign('HMAC', key, enc.encode(SESSION_SLUG + ':granted'));
  return btoa(String.fromCharCode(...new Uint8Array(sig)));
}

function cookieHeader(token) {
  return (
    COOKIE +
    '=' +
    encodeURIComponent(token) +
    '; Path=/defense; HttpOnly; Secure; SameSite=Lax; Max-Age=' +
    MAX_AGE
  );
}

module.exports = async function handler(req, res) {
  cors(res, req.headers.origin);
  if (req.method === 'OPTIONS') {
    res.status(204).end();
    return;
  }
  if (req.method !== 'POST') {
    json(res, 405, { ok: false, error: 'method_not_allowed' });
    return;
  }

  const codes = loadCodes();
  if (!codes) {
    json(res, 503, {
      ok: false,
      error: 'gate_not_configured',
      message: 'Email+code gate is not configured. Use the shared password path or contact Navier.',
    });
    return;
  }

  const body = parseBody(req);
  const email = String(body.email || '')
    .trim()
    .slice(0, 200);
  const code = String(body.code || '')
    .trim()
    .toUpperCase()
    .slice(0, 64);

  if (!isEmail(email)) {
    json(res, 400, { ok: false, error: 'invalid_email', message: 'Enter a valid work email.' });
    return;
  }
  if (!code) {
    json(res, 400, { ok: false, error: 'missing_code', message: 'Enter your access code.' });
    return;
  }

  const entry = codes[code];
  if (!entry || entry.active === false) {
    json(res, 403, { ok: false, error: 'denied', message: DENIED });
    return;
  }

  const webhook = process.env.DEFENSE_ACCESS_LOG_WEBHOOK;
  if (webhook) {
    fetch(webhook, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        timestamp_utc: new Date().toISOString(),
        email,
        code,
        recipient_label: entry.label || '',
        user_agent: req.headers['user-agent'] || '',
      }),
    }).catch(() => {});
  }

  const token = await sessionToken();
  if (!token) {
    json(res, 500, {
      ok: false,
      error: 'session_unavailable',
      message: 'AUTH_SECRET is not configured.',
    });
    return;
  }

  json(
    res,
    200,
    { ok: true },
    {
      'Set-Cookie': cookieHeader(token),
    }
  );
};
