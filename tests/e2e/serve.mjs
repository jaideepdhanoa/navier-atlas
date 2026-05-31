// Minimal static file server for the repo root, used by Playwright's webServer.
// Builds the gitignored atlas-data.js on first run if it's missing.
import http from 'node:http';
import { readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { execSync } from 'node:child_process';
import { extname, join, normalize, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = fileURLToPath(new URL('../../', import.meta.url)); // repo root (tests/e2e/ → ../../)
const PORT = Number(process.env.PORT || 4173);
const TYPES = {
  '.html': 'text/html; charset=utf-8', '.js': 'application/javascript; charset=utf-8',
  '.mjs': 'application/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8', '.svg': 'image/svg+xml',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.ico': 'image/x-icon', '.woff2': 'font/woff2',
};

// atlas-data.js is a generated artifact (gitignored, built from data-clean/ + partner-pitch/).
if (!existsSync(join(ROOT, 'atlas-data.js'))) {
  console.log('[serve] atlas-data.js missing — building …');
  execSync('node scripts/build.mjs', { cwd: ROOT, stdio: 'inherit' });
}

http.createServer(async (req, res) => {
  try {
    let p = decodeURIComponent((req.url || '/').split('?')[0]);
    if (p === '/' || p === '') p = '/index.html';
    const full = normalize(join(ROOT, p));
    if (full !== ROOT.replace(/[\\/]$/, '') && !full.startsWith(ROOT)) { // path-traversal guard
      res.writeHead(403); return res.end('forbidden');
    }
    const body = await readFile(full);
    res.writeHead(200, { 'content-type': TYPES[extname(full)] || 'application/octet-stream' });
    res.end(body);
  } catch {
    res.writeHead(404); res.end('not found');
  }
}).listen(PORT, () => console.log(`[serve] http://localhost:${PORT}  (root: ${ROOT})`));
