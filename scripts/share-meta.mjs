// Share metadata helpers — used by build-site.mjs to inject per-page OG/Twitter tags.
export const SITE_URL = (process.env.SITE_URL || 'https://navier-atlas.vercel.app').replace(/\/$/, '');

export function escHtml(s) {
  return String(s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

export function trunc(s, n = 155) {
  const t = String(s || '').replace(/\s+/g, ' ').trim();
  return t.length <= n ? t : `${t.slice(0, n - 1)}…`;
}

export function ogImageUrl({ title, subtitle, badge, type }) {
  const q = new URLSearchParams();
  if (title) q.set('title', title.slice(0, 80));
  if (subtitle) q.set('subtitle', subtitle.slice(0, 100));
  if (badge) q.set('badge', badge.slice(0, 40));
  if (type) q.set('type', type);
  return `${SITE_URL}/api/og?${q}`;
}

/** Inject title + description + OG/Twitter + canonical into index.html <head>. */
export function injectShareMeta(html, { title, description, canonicalPath, ogBadge, ogType }) {
  const canonical = `${SITE_URL}${canonicalPath}`;
  const ogImage = ogImageUrl({ title, subtitle: description, badge: ogBadge, type: ogType });
  const t = escHtml(title);
  const d = escHtml(description);
  const u = escHtml(canonical);
  const img = escHtml(ogImage);
  let out = html;
  out = out.replace(/<title>[^<]*<\/title>/, `<title>${t}</title>`);
  out = out.replace(/<meta name="description" content="[^"]*"\s*\/>/, `<meta name="description" content="${d}" />`);
  out = out.replace(/<meta property="og:title" content="[^"]*"\s*\/>/, `<meta property="og:title" content="${t}" />`);
  out = out.replace(/<meta property="og:description" content="[^"]*"\s*\/>/, `<meta property="og:description" content="${d}" />`);
  out = out.replace(/<meta name="twitter:title" content="[^"]*"\s*\/>/, `<meta name="twitter:title" content="${t}" />`);
  out = out.replace(/<meta name="twitter:description" content="[^"]*"\s*\/>/, `<meta name="twitter:description" content="${d}" />`);
  // Add or replace extended OG tags (insert after og:description).
  const ogBlock = [
    `<meta property="og:url" content="${u}" />`,
    `<meta property="og:image" content="${img}" />`,
    `<meta property="og:image:width" content="1200" />`,
    `<meta property="og:image:height" content="630" />`,
    `<meta name="twitter:card" content="summary_large_image" />`,
    `<meta name="twitter:image" content="${img}" />`,
    `<link rel="canonical" href="${u}" />`,
  ].join('\n');
  if (out.includes('property="og:url"')) {
    out = out.replace(/<meta property="og:url"[^>]*>/, `<meta property="og:url" content="${u}" />`);
    out = out.replace(/<meta property="og:image"[^>]*>/, `<meta property="og:image" content="${img}" />`);
    out = out.replace(/<meta name="twitter:card"[^>]*>/, `<meta name="twitter:card" content="summary_large_image" />`);
    out = out.replace(/<meta name="twitter:image"[^>]*>/, `<meta name="twitter:image" content="${img}" />`);
    out = out.replace(/<link rel="canonical"[^>]*>/, `<link rel="canonical" href="${u}" />`);
  } else {
    out = out.replace(
      /<meta property="og:description"[^>]*>/,
      `$&\n${ogBlock}`
    );
  }
  return out;
}

export function clusterMeta(cb, cl) {
  const name = cb.display || cb.display_name || cb.cluster_id;
  const region = cb.region || cl?.region || '';
  return {
    title: `${name} · Navier Atlas`,
    description: trunc(cb.tagline || cb.summary || `Explore ${name} on the Navier mobility network.`),
    ogBadge: region || 'Region',
    ogType: 'cluster',
  };
}

export function cityMeta(brief, props) {
  const name = brief?.display || brief?.display_name || props?.shortName || props?.name || brief?.city_id;
  const region = brief?.region || props?.region || '';
  return {
    title: `${name} · Navier Atlas`,
    description: trunc(brief?.tagline || brief?.summary || `City brief and marine mobility routes for ${name}.`),
    ogBadge: region || 'City',
    ogType: 'city',
  };
}

export function partnerMeta(partner, market) {
  if (market) {
    const partnerName = partner.display || partner.partner_id;
    const label = market.label || market.slug;
    return {
      title: `${partnerName} · ${label}`,
      description: trunc(market.summary || market.hero?.subtitle || `${partnerName} proposal for ${label}.`),
      ogBadge: market.region || partner.region || 'Partner',
      ogType: 'market',
    };
  }
  const hero = partner.hero || {};
  return {
    title: hero.title || `${partner.display || partner.partner_id} × Navier`,
    description: trunc(hero.subtitle || partner.partner_context?.their_ambition || `Partner proposal on Navier Atlas.`),
    ogBadge: partner.region || 'Partner',
    ogType: 'partner',
  };
}