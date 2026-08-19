import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";

const DIR = "/tasklet/drive/seriesb-microsite/contracts";
const INV = "/tasklet/drive/seriesb-microsite/CUT-SLIDE-INVENTORY.md";

const files = readdirSync(DIR).filter(f => f.endsWith(".json")).sort();
let failures: string[] = [];
let passes: string[] = [];

const docs: Record<string, any> = {};
for (const f of files) {
  try { docs[f] = JSON.parse(readFileSync(join(DIR, f), "utf8")); }
  catch (e: any) { failures.push(`PARSE FAIL ${f}: ${e.message}`); }
}
if (Object.keys(docs).length === files.length) passes.push(`(a) All ${files.length} JSON files parse: ${files.join(", ")}`);

type Hit = { file: string; path: string; value: string };
const renderables: Hit[] = [];
function walk(node: any, file: string, path: string) {
  if (typeof node === "string") { renderables.push({ file, path, value: node }); return; }
  if (Array.isArray(node)) { node.forEach((v, i) => walk(v, file, `${path}[${i}]`)); return; }
  if (node && typeof node === "object") {
    for (const [k, v] of Object.entries(node)) {
      if (k.startsWith("_")) continue;
      walk(v, file, path ? `${path}.${k}` : k);
    }
  }
}
for (const [f, d] of Object.entries(docs)) walk(d, f, "");

const isTechnicalField = (p: string) =>
  /(embed_url|poster|href|youtube_id|asset|data|contract|component|\bid|route|robots_meta)$/.test(p);

const bannedHard: [string, RegExp][] = [
  ["valuation", /\bvaluation/i],
  ["pre/post-money", /(pre|post)-money/i],
  ["LC-180", /LC-?180/i],
  ["AD Ports", /AD Ports/i],
  ["Sergey Brin", /Sergey|Brin/i],
  ["N120", /N-?120\b/],
  ["2,400 NMi", /2,?400\s*NM/i],
  ["$600B", /\$600\s*B/i],
  ["not yet public", /not yet public/i],
  ["first look", /first look/i],
  ["lead investor", /lead investor/i],
];
const internalVocab: [string, RegExp][] = [
  ["canon", /\bcanon(ical)?\b/i],
  ["fail-closed", /fail[- ]closed/i],
  ["kill-scan", /kill[- ]scan/i],
  ["T1/T2 tier codes", /\bT[12]\b/],
  ["MID scenario/case", /\bMID (scenario|case)\b/i],
  ["slide refs", /\bslide\s*\d+|\bslides\b/i],
  ["file names", /\.(json|md|ts)\b/],
  ["DocSend", /DocSend/i],
];
let bScanFail = 0;
for (const h of renderables) {
  for (const [name, re] of bannedHard) {
    if (re.test(h.value)) { failures.push(`(b) BANNED "${name}" in ${h.file} ${h.path}: "${h.value}"`); bScanFail++; }
  }
  if (isTechnicalField(h.path)) continue;
  for (const [name, re] of internalVocab) {
    if (re.test(h.value)) { failures.push(`(b) INTERNAL VOCAB "${name}" in ${h.file} ${h.path}: "${h.value}"`); bScanFail++; }
  }
}
if (bScanFail === 0) passes.push(`(b) 0 banned-term / internal-vocab hits across ${renderables.length} renderable strings`);

const inv = readFileSync(INV, "utf8");
const cut = inv.split("## Slide 37")[0];
const norm = (s: string) => s.replace(/[\u2019\u2018]/g, "'").replace(/[\u201C\u201D]/g, '"').replace(/\s+/g, " ").trim();
const corpus = norm(cut);

const videoTitles = [
  "Navier's hydrofoil boats have wings",
  "Inside Navier N30 — The Longest-Range Electric Boat Ever Built!",
];
let boatFail = 0, boatCount = 0;
for (const h of renderables) {
  if (isTechnicalField(h.path)) continue;
  const v = norm(h.value);
  const re = /\b(boats?|fleets?)\b/gi;
  let m: RegExpExecArray | null;
  while ((m = re.exec(v))) {
    boatCount++;
    const start = Math.max(0, m.index - 18);
    const window = v.slice(start, Math.min(v.length, m.index + m[0].length + 18));
    const ok = corpus.includes(window) || videoTitles.some(t => norm(t).includes(window) || window.includes(norm(t)));
    if (!ok) { failures.push(`(b2) NON-VERBATIM boat/fleet in ${h.file} ${h.path}: "...${window}..."`); boatFail++; }
  }
}
if (boatFail === 0) passes.push(`(b2) All ${boatCount} boat/fleet occurrences are deck-verbatim (or verified video titles)`);

const allRenderText = norm(renderables.map(r => r.value).join(" | "));
const spots = [
  "10,000+", "$100M", "$512M", "567", "~2,000 NMi", "5× less energy", "800× denser",
  "~14×", "$16–31B", "$1.1T", "672 corridors", "385 cities", "79 countries",
  "$10M Series B-1", "$100-150M+", "7× less energy", "13× less energy",
  "90% less energy", "70 NM at 20 kn", "$392M", "$5,563/TEU", "44–50%", "$33M",
];
let cFail = 0;
for (const s of spots) {
  const inContracts = allRenderText.includes(norm(s));
  const inDeck = corpus.includes(norm(s));
  if (!inContracts || !inDeck) { failures.push(`(c) SPOT "${s}": in contracts=${inContracts}, in slides 1-36=${inDeck}`); cFail++; }
}
if (cFail === 0) passes.push(`(c) ${spots.length}/${spots.length} spot numbers present in contracts and matched verbatim in slides 1-36`);

const appendixMarkers = [
  "$706M", "623", "MID CASE", "$225 a seat", "PAYBACK ~16 MONTHS", "\u20AC1,209", "\u20AC1,400",
  "1956", "hasn't changed in 70 years", "Master Plan", "$744K", "$494K", "Capri",
  "St Barth", "Silhouette", "yacht income", "battery reserve", "$127M EBITDA",
];
let dFail = 0;
for (const s of appendixMarkers) {
  if (allRenderText.includes(norm(s))) { failures.push(`(d) APPENDIX CONTENT "${s}" in renderables`); dFail++; }
}
if (dFail === 0) passes.push(`(d) 0 appendix (slides 37-53) markers found in renderable strings`);

let vFail = 0, vChecked = 0;
for (const h of renderables) {
  if (isTechnicalField(h.path)) continue;
  const v = norm(h.value);
  if (/\d/.test(v) && v.length <= 60) {
    vChecked++;
    if (!corpus.includes(v) && !videoTitles.map(norm).includes(v)) {
      failures.push(`(e) NOT CORPUS-VERBATIM (short stat string) ${h.file} ${h.path}: "${v}"`);
      vFail++;
    }
  }
}
passes.push(`(e) whole-string verbatim check on ${vChecked} short stat-bearing strings: ${vFail} flagged for review`);

console.log("=== PASSES ===");
passes.forEach(p => console.log("PASS", p));
console.log("\n=== FAILURES / FLAGS ===");
if (failures.length === 0) console.log("none");
failures.forEach(f => console.log("FLAG", f));
console.log(`\nTotal renderable strings: ${renderables.length}`);
