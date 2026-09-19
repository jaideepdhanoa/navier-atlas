import type { Brief } from './model';
import { escape as e, richText as r } from './model';
export function renderHtml(c:Brief,css:string,theme:'dark'|'light',assetPaths:Map<string,string>):string{
 const a=(id:string)=>{const path=assetPaths.get(id);if(!path)throw new Error(`Missing staged asset ${id}`);return e(path);};
 const p=(x:{text:string,claimIds:string[]},cls='')=>`<p class="${cls}" data-claims="${e(x.claimIds.join(' '))}">${r(x.text)}</p>`;
 const source=new Map(c.sources.map(s=>[s.id,s]));
 return `<!doctype html><html lang="en" data-theme="${theme}"><head><meta charset="utf-8"><title>${e(c.meta.title)}</title><meta name="viewport" content="width=816"><style>${css}</style></head><body>
 <section class="page page-one" aria-label="Page 1: ${e(c.meta.company)} overview">
  <header class="masthead"><img class="map" src="${a(c.branding.mastheadAsset)}" alt=""><div class="inner"><img class="logo" src="${a(c.branding.logoAsset)}" alt="${e(c.meta.company)}"><div class="mast-meta"><b>${e(c.meta.partner)}</b><br>${e(c.meta.edition)}<br>${e(c.meta.date)} · ${e(c.meta.classification==='partner-confidential'?'Confidential':c.meta.classification==='public-example'?'Illustrative template':'Company overview')}</div></div><div class="mast-tag">${e(c.meta.brandLine)}</div></header>
  <main class="body-area">
   <h1>${r(c.cover.headline)}</h1>${p(c.cover.intro,'intro')}
   <section class="section"><div class="section-title"><h2>${e(c.cover.platformTitle)}</h2></div>${p(c.cover.platformBody)}</section>
   <section class="section"><div class="section-title"><div class="kicker">${e(c.cover.tilesKicker)}</div></div><div class="strip">${c.cover.tiles.map(t=>`<div class="tile"><img src="${a(t.asset)}" alt="${e(t.title)}" style="object-position:${e(t.position??'50% 50%')}"><div class="tile-label"><b>${e(t.title)}</b><small>${e(t.subtitle)}</small></div></div>`).join('')}</div>${p(c.cover.tileCaption,'fine tile-caption')}</section>
   <section class="section"><div class="section-title"><div class="kicker">${e(c.cover.tractionKicker)}</div></div><div class="metrics" style="--metric-count:${c.cover.metrics.length}">${c.cover.metrics.map(m=>`<div class="metric" data-claims="${e(m.claimIds.join(' '))}"><div class="value">${e(m.value)}</div><div class="label">${e(m.label)}</div></div>`).join('')}</div>${p(c.cover.tractionNote,'traction-note')}</section>
   <section class="spotlight"><div><div class="kicker">${e(c.cover.spotlight.kicker)}</div><h3>${e(c.cover.spotlight.title)}</h3>${p(c.cover.spotlight.body)}<div class="stages">${c.cover.spotlight.stages.map(s=>`<div class="stage" data-claims="${e(s.claimIds.join(' '))}"><div class="name">${e(s.title)}</div><div class="status">${e(s.status)}</div></div>`).join('')}</div></div><div class="image"><img src="${a(c.cover.spotlight.asset)}" alt="${e(c.cover.spotlight.imageCaption)}"><div class="fine">${e(c.cover.spotlight.imageCaption)}</div></div></section>
  </main><footer class="footer"><span>${e(c.meta.footerLabel)}</span><span>Page 1 of 2</span></footer>
 </section>
 <section class="page page-two" aria-label="Page 2: proposed collaboration">
  <main class="body-area"><header class="partnership-head"><div class="kicker">${e(c.partnership.kicker)}</div><h1>${r(c.partnership.headline)}</h1>${p(c.partnership.intro,'intro')}</header>
   <div class="contributions">${c.partnership.contributions.map(x=>`<section class="contribution"><div class="kicker">${e(x.label)}</div>${p(x.body)}</section>`).join('')}</div>
   <div class="tracks">${c.partnership.tracks.map(t=>`<section class="track"><div class="track-number">${e(t.number)}</div><div><div class="kicker">${e(t.kicker)}</div><h3>${e(t.title)}</h3>${p(t.body)}<div class="track-bottom"><p><span>Partner value</span>${r(t.value)}</p><p><span>Concrete start</span>${r(t.start)}</p></div></div></section>`).join('')}</div>
   <div class="expansion"><b>${e(c.partnership.expansion.label)}</b> ${r(c.partnership.expansion.text)}</div>
   <section class="ask"><h3>${e(c.partnership.ask.title)}</h3>${p(c.partnership.ask.body)}<div class="steps">${c.partnership.ask.steps.map((s,i)=>`<div class="step"><span>0${i+1}</span>${e(s)}</div>`).join('')}</div></section>
   <div class="team"><b>${e(c.partnership.team.label)}</b> ${r(c.partnership.team.text)}</div>
   <div class="citations">Sources · ${c.partnership.citations.map(x=>`<a href="${e(source.get(x.sourceId)!.locator)}">${e(x.label)}</a>`).join(' · ')} · Accessed ${e(c.meta.date)}.</div>
  </main><footer class="footer"><div class="contact"><a href="${e(c.meta.storyUrl)}">See it fly</a> · <a href="mailto:${e(c.meta.contact)}">${e(c.meta.contact)}</a></div><span>Page 2 of 2</span></footer>
 </section></body></html>`;
}
