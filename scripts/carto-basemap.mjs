/**
 * CARTO basemap key — inject at build/deploy only. Never commit the secret.
 * Employer hubs, Atlas pages, and /invest all share this bootstrap.
 */
let warned = false;

export function cartoKey() {
  return process.env.CARTO_BASEMAP_KEY || '';
}

export function cartoKeyBootstrapScript() {
  const key = cartoKey();
  if (!key) {
    if (!warned) {
      warned = true;
      console.warn('CARTO_BASEMAP_KEY unset — CARTO tiles will watermark / 401');
    }
    return '';
  }
  const safe = String(key).replace(/\\/g, '\\\\').replace(/'/g, "\\'").replace(/"/g, '\\"');
  return `<script>window.CARTO_BASEMAP_KEY="${safe}";</script>\n`;
}

export function injectCartoKey(html) {
  const boot = cartoKeyBootstrapScript();
  if (!boot || !html) return html;
  if (/window\.CARTO_BASEMAP_KEY=/.test(html)) return html;
  if (/<\/head>/i.test(html)) return html.replace(/<\/head>/i, `${boot}</head>`);
  return boot + html;
}
