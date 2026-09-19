import type {
  Asset, Audience, BaseSlide, Claim, Crop, Opportunity, Project, Slide, Source, Transaction, ValidationIssue, ValidationResult, Visual,
} from './types';
import { isPlausibleMime, isUnsafeAssetPath, verifyAssetFiles } from './assets';
import {schemaIssues} from './schema';
import {salesIssues,blockIds,resolveBlock,collectVisuals,slideBlockClaims} from './authoring';

const AUDIENCES = new Set<Audience>(['internal', 'partner', 'public']);
const VISIBILITIES = new Set(['public', 'internal', 'restricted']);
const EVIDENCE = new Set(['measured', 'demonstrated', 'historical', 'company-reported', 'preliminary', 'modeled', 'planned', 'proposed', 'fictional']);
const OPPORTUNITY_KINDS = new Set(['supply', 'co-development', 'contract-build', 'license', 'direct-sale', 'resale', 'service', 'operator-program', 'other']);
const LAYOUTS = new Set(['cover', 'fit', 'options', 'models', 'channels', 'missions', 'close', 'sales']);
const ID = /^[A-Za-z0-9_-]+$/;
const DATE = /^\d{4}-\d{2}-\d{2}$/;
const ISO_HEADLINE_LIMIT = 95;

const isRecord = (x: unknown): x is Record<string, any> => !!x && typeof x === 'object' && !Array.isArray(x);
const str = (x: unknown): x is string => typeof x === 'string' && x.trim().length > 0;
const arr = (x: unknown): x is unknown[] => Array.isArray(x);
const add = (issues: ValidationIssue[], severity: ValidationIssue['severity'], code: string, path: string, message: string) => issues.push({ severity, code, path, message });
const error = (issues: ValidationIssue[], code: string, path: string, message: string) => add(issues, 'error', code, path, message);
const warn = (issues: ValidationIssue[], code: string, path: string, message: string) => add(issues, 'warning', code, path, message);
const hold = (issues: ValidationIssue[], code: string, path: string, message: string) => add(issues, 'release-hold', code, path, message);

function required(issues: ValidationIssue[], object: Record<string, any>, fields: string[], path: string) {
  for (const field of fields) if (!(field in object) || object[field] === undefined || object[field] === null) error(issues, 'REQUIRED_FIELD', `${path}.${field}`, 'Required field is missing');
}
function oneOf(issues: ValidationIssue[], value: unknown, values: Set<string>, path: string) {
  if (typeof value !== 'string' || !values.has(value)) error(issues, 'INVALID_ENUM', path, 'Value is outside the contract enum');
}
function nonEmptyArray(issues: ValidationIssue[], value: unknown, path: string) {
  if (!Array.isArray(value) || value.length === 0) error(issues, 'REQUIRED_ARRAY', path, 'Expected a non-empty array');
}
function idCheck(issues: ValidationIssue[], value: unknown, path: string) {
  if (typeof value !== 'string' || !ID.test(value)) error(issues, 'UNSAFE_ID', path, 'ID must use only ASCII letters, numbers, underscore, or hyphen');
}
function refs(issues: ValidationIssue[], values: unknown, path: string, known: Set<string>, requiredRef = false) {
  if (!Array.isArray(values)) { error(issues, 'INVALID_REFS', path, 'References must be an array'); return; }
  if (requiredRef && values.length === 0) error(issues, 'EMPTY_REFS', path, 'At least one reference is required');
  values.forEach((value, i) => {
    idCheck(issues, value, `${path}[${i}]`);
    if (typeof value === 'string' && !known.has(value)) error(issues, 'UNKNOWN_REFERENCE', `${path}[${i}]`, `Unknown reference ${value}`);
  });
}
function finitePositive(issues: ValidationIssue[], value: unknown, path: string) {
  if (typeof value !== 'number' || !Number.isFinite(value) || value <= 0) error(issues, 'INVALID_POSITIVE_NUMBER', path, 'Expected a positive finite number');
}
function crop(issues: ValidationIssue[], value: unknown, path: string) {
  if (!isRecord(value)) { error(issues, 'INVALID_CROP', path, 'Crop must contain left, top, right, and bottom'); return; }
  for (const key of ['left', 'top', 'right', 'bottom']) {
    if (typeof value[key] !== 'number' || !Number.isFinite(value[key]) || value[key] < 0 || value[key] > 1) error(issues, 'CROP_OUT_OF_BOUNDS', `${path}.${key}`, 'Crop coordinates must be finite and normalized to 0..1');
  }
  if ([value.left, value.top, value.right, value.bottom].every((v: unknown) => typeof v === 'number' && Number.isFinite(v)) && (value.right <= value.left || value.bottom <= value.top)) error(issues, 'CROP_NOT_POSITIVE', path, 'Crop right/bottom must be greater than left/top');
}
function dateCheck(issues: ValidationIssue[], value: unknown, path: string) {
  if (typeof value !== 'string' || !DATE.test(value)) { error(issues, 'INVALID_DATE', path, 'Date must use YYYY-MM-DD'); return; }
  const d = new Date(`${value}T00:00:00Z`);
  if (Number.isNaN(d.valueOf()) || d.toISOString().slice(0, 10) !== value) error(issues, 'INVALID_DATE', path, 'Date is not a real calendar date');
}
function uniqueIds(issues: ValidationIssue[], arrays: Array<{ value: unknown; path: string }>) {
  const seen = new Map<string, string>();
  for (const entry of arrays) {
    if (!Array.isArray(entry.value)) continue;
    entry.value.forEach((item, i) => {
      if (!isRecord(item)) return;
      if (typeof item.id !== 'string') return;
      const path = `${entry.path}[${i}].id`;
      if (seen.has(item.id)) error(issues, 'DUPLICATE_ID', path, `ID duplicates ${seen.get(item.id)}`);
      else seen.set(item.id, path);
    });
  }
}

function validateSource(issues: ValidationIssue[], value: unknown, path: string) {
  if (!isRecord(value)) { error(issues, 'INVALID_SOURCE', path, 'Source must be an object'); return; }
  required(issues, value, ['id', 'title', 'locator', 'asOf', 'visibility'], path);
  idCheck(issues, value.id, `${path}.id`); if (!str(value.title)) error(issues, 'INVALID_TEXT', `${path}.title`, 'Source title is required');
  if (!str(value.locator)) error(issues, 'INVALID_TEXT', `${path}.locator`, 'Source locator is required');
  dateCheck(issues, value.asOf, `${path}.asOf`); oneOf(issues, value.visibility, VISIBILITIES, `${path}.visibility`);
  if (value.visibility === 'public' && typeof value.locator === 'string' && !/^https?:\/\/\S+$/i.test(value.locator)) error(issues, 'PUBLIC_SOURCE_LOCATOR', `${path}.locator`, 'Public source locators must be HTTP(S) URLs');
}
function validateClaim(issues: ValidationIssue[], value: unknown, path: string, sourceIds: Set<string>) {
  if (!isRecord(value)) { error(issues, 'INVALID_CLAIM', path, 'Claim must be an object'); return; }
  required(issues, value, ['id', 'statement', 'evidenceClass', 'sourceIds', 'basis', 'clearedFor'], path);
  idCheck(issues, value.id, `${path}.id`); if (!str(value.statement)) error(issues, 'INVALID_TEXT', `${path}.statement`, 'Claim statement is required');
  oneOf(issues, value.evidenceClass, EVIDENCE, `${path}.evidenceClass`); if (!str(value.basis)) error(issues, 'CLAIM_BASIS_MISSING', `${path}.basis`, 'Every claim needs a concise basis');
  refs(issues, value.sourceIds, `${path}.sourceIds`, sourceIds, true);
  if (!Array.isArray(value.clearedFor) || value.clearedFor.length === 0) error(issues, 'CLAIM_CLEARANCE_MISSING', `${path}.clearedFor`, 'Claim needs at least one audience clearance');
  else value.clearedFor.forEach((a: unknown, i: number) => oneOf(issues, a, AUDIENCES, `${path}.clearedFor[${i}]`));
}
function validateAsset(issues: ValidationIssue[], value: unknown, path: string) {
  if (!isRecord(value)) { error(issues, 'INVALID_ASSET', path, 'Asset must be an object'); return; }
  required(issues, value, ['id', 'path', 'sha256', 'width', 'height', 'mimeType', 'kind', 'maturity', 'missions', 'geography', 'roles', 'sourceIds', 'visibility', 'clearedFor', 'rightsNote', 'caption'], path);
  idCheck(issues, value.id, `${path}.id`);
  if (!str(value.path) || isUnsafeAssetPath(value.path)) error(issues, 'ASSET_PATH_UNSAFE', `${path}.path`, 'Asset path must be a relative local path without traversal');
  if (typeof value.sha256 !== 'string' || !/^[a-f0-9]{64}$/i.test(value.sha256)) error(issues, 'ASSET_HASH_INVALID', `${path}.sha256`, 'Asset SHA-256 must be 64 hexadecimal characters');
  finitePositive(issues, value.width, `${path}.width`); finitePositive(issues, value.height, `${path}.height`);
  if (typeof value.mimeType !== 'string' || !isPlausibleMime(value.mimeType)) error(issues, 'ASSET_MIME_INVALID', `${path}.mimeType`, 'Asset MIME must be a supported image MIME type');
  oneOf(issues, value.kind, new Set(['photograph', 'rendering', 'schematic', 'logo']), `${path}.kind`);
  oneOf(issues, value.maturity, new Set(['actual', 'demonstrated', 'concept', 'context', 'brand']), `${path}.maturity`);
  for (const field of ['missions', 'geography', 'roles']) if (!Array.isArray(value[field]) || value[field].some((x: unknown) => !str(x))) error(issues, 'ASSET_TAGS_INVALID', `${path}.${field}`, 'Asset tags must be arrays of non-empty strings');
  if (!Array.isArray(value.sourceIds)) error(issues, 'INVALID_REFS', `${path}.sourceIds`, 'References must be an array');
  oneOf(issues, value.visibility, VISIBILITIES, `${path}.visibility`);
  if (!Array.isArray(value.clearedFor) || value.clearedFor.length === 0) error(issues, 'ASSET_CLEARANCE_MISSING', `${path}.clearedFor`, 'Asset needs audience clearance');
  else value.clearedFor.forEach((a: unknown, i: number) => oneOf(issues, a, AUDIENCES, `${path}.clearedFor[${i}]`));
  if (!str(value.rightsNote)) error(issues, 'ASSET_RIGHTS_MISSING', `${path}.rightsNote`, 'Asset rights clearance note is required');
  if (!str(value.caption)) error(issues, 'ASSET_CAPTION_MISSING', `${path}.caption`, 'Asset needs a visible caption');
  if (value.maturity === 'concept' && typeof value.caption === 'string' && !/concept|illustrative|notional|proposed/i.test(value.caption)) error(issues, 'CONCEPT_CAPTION_MISSING', `${path}.caption`, 'Concept visuals must be visibly labeled concept, illustrative, notional, or proposed');
  if (value.kind === 'photograph' && typeof value.caption === 'string' && /generated|synthetic|AI[- ]?generated/i.test(value.caption)) error(issues, 'PHOTO_GENERATION_IMPLIED', `${path}.caption`, 'A real photograph cannot be presented as newly generated');
  if (value.kind === 'photograph' && !['actual', 'demonstrated'].includes(value.maturity)) error(issues, 'PHOTO_MATURITY_INVALID', `${path}.maturity`, 'Photographs must be actual or demonstrated assets');
  if (value.focalPoint !== undefined) {
    if (!isRecord(value.focalPoint)) error(issues, 'FOCAL_POINT_INVALID', `${path}.focalPoint`, 'Focal point must contain x and y');
    else for (const key of ['x', 'y']) if (typeof value.focalPoint[key] !== 'number' || !Number.isFinite(value.focalPoint[key]) || value.focalPoint[key] < 0 || value.focalPoint[key] > 1) error(issues, 'FOCAL_POINT_INVALID', `${path}.focalPoint.${key}`, 'Focal point coordinates must be normalized to 0..1');
  }
  if (value.keepRegion !== undefined) crop(issues, value.keepRegion, `${path}.keepRegion`);
  if (value.crop !== undefined) crop(issues, value.crop, `${path}.crop`);
  if (value.nativeSource && !value.repoSource && !value.path) warn(issues, 'UNARCHIVED_NATIVE_SOURCE', `${path}`, 'Native presentation provenance alone is not an archived asset');
}
function validateOpportunity(issues: ValidationIssue[], value: unknown, path: string, claimIds: Set<string>) {
  if (!isRecord(value)) { error(issues, 'INVALID_OPPORTUNITY', path, 'Opportunity must be an object'); return; }
  required(issues, value, ['id', 'kind', 'title', 'product', 'customer', 'payer', 'commercialLogic', 'partnerBenefit', 'companyContribution', 'partnerContribution', 'nextQuestion', 'claimIds', 'status'], path);
  idCheck(issues, value.id, `${path}.id`); oneOf(issues, value.kind, OPPORTUNITY_KINDS, `${path}.kind`); oneOf(issues, value.status, new Set(['proposed', 'existing']), `${path}.status`);
  for (const key of ['title', 'product', 'customer', 'payer', 'commercialLogic', 'partnerBenefit', 'companyContribution', 'partnerContribution', 'nextQuestion']) if (!str(value[key])) error(issues, 'OPPORTUNITY_FIELD_MISSING', `${path}.${key}`, 'Business field is required');
  refs(issues, value.claimIds, `${path}.claimIds`, claimIds, true);
}
function validateTransaction(issues: ValidationIssue[], value: unknown, path: string) {
  if (!isRecord(value)) { error(issues, 'INVALID_PAYMENT', path, 'Payment must be an object'); return; }
  required(issues, value, ['actors', 'labels', 'kind'], path); oneOf(issues, value.kind, new Set(['payment']), `${path}.kind`);
  for (const key of ['actors', 'labels']) if (!Array.isArray(value[key]) || value[key].length === 0 || value[key].some((x: unknown) => !str(x))) error(issues, 'INVALID_PAYMENT_LABELS', `${path}.${key}`, 'Payment actors and labels must be non-empty text arrays');
}
function validateVisual(issues: ValidationIssue[], value: unknown, path: string, assetIds: Set<string>) {
  if (!isRecord(value)) { error(issues, 'INVALID_VISUAL', path, 'Visual must contain assetId and caption'); return; }
  required(issues, value, ['assetId', 'caption'], path); refs(issues, [value.assetId], `${path}.assetId`, assetIds, true);
  if (!str(value.caption)) error(issues, 'VISUAL_CAPTION_MISSING', `${path}.caption`, 'Visual caption is required');
  if (value.crop !== undefined) crop(issues, value.crop, `${path}.crop`);
}

function base(issues: ValidationIssue[], value: unknown, path: string, layout: string, known: { claims: Set<string>; sources: Set<string>; opportunities: Set<string> }) {
  if (!isRecord(value)) { error(issues, 'INVALID_SLIDE', path, 'Slide must be an object'); return; }
  required(issues, value, ['key', 'kicker', 'title', 'claimIds', 'sourceIds', 'opportunityIds', 'notes', 'layout'], path);
  idCheck(issues, value.key, `${path}.key`); if (!str(value.kicker) || !str(value.title)) error(issues, 'SLIDE_TEXT_MISSING', path, 'Slide kicker and title are required');
  refs(issues, value.claimIds, `${path}.claimIds`, known.claims); refs(issues, value.sourceIds, `${path}.sourceIds`, known.sources); refs(issues, value.opportunityIds, `${path}.opportunityIds`, known.opportunities);
  if (value.layout !== layout) error(issues, 'LAYOUT_MISMATCH', `${path}.layout`, `Expected layout ${layout}`);
}
function textBudget(issues: ValidationIssue[], value: unknown, path: string, max: number, label = 'Text') { if (typeof value === 'string' && value.length > max) error(issues, 'TEXT_BUDGET', path, `${label} exceeds ${max} characters`); }
function checkSlideBudgets(issues: ValidationIssue[], value: unknown, path: string) {
  if (Array.isArray(value)) { value.forEach((v, i) => checkSlideBudgets(issues, v, `${path}[${i}]`)); return; }
  if (!isRecord(value)) return;
  for (const [key, child] of Object.entries(value)) {
    const childPath = `${path}.${key}`;
    if (typeof child === 'string') {
      if (key === 'title' || /headline/i.test(key)) textBudget(issues, child, childPath, ISO_HEADLINE_LIMIT, 'Headline');
      else if (key === 'kicker') textBudget(issues, child, childPath, 70, 'Kicker');
      else if (/label/i.test(key)) textBudget(issues, child, childPath, 70, 'Label');
      else if (/body|description|takeaway|benefit|explore|intro|ask|service|criteria|selection|scope/i.test(key)) textBudget(issues, child, childPath, 700, 'Copy block');
    } else checkSlideBudgets(issues, child, childPath);
  }
}

function validateSlide(issues: ValidationIssue[], value: unknown, index: number, known: { claims: Set<string>; sources: Set<string>; opportunities: Set<string>; assets: Set<string>; assetRecords?: unknown[] }) {
  const path = `slides[${index}]`;
  if (!isRecord(value)) { error(issues, 'INVALID_SLIDE', path, 'Slide must be an object'); return; }
  const layout = value.layout;
  oneOf(issues, layout, LAYOUTS, `${path}.layout`);
  base(issues, value, path, String(layout), known);
  const visual = (v: unknown, p: string) => {
    validateVisual(issues, v, p, known.assets);
    if (isRecord(v) && typeof v.assetId === 'string') {
      const sourceAsset: any = known.assetRecords?.find((a: any) => a?.id === v.assetId);
      if (sourceAsset?.maturity === 'concept' && typeof v.caption === 'string' && !/concept|illustrative|notional|proposed/i.test(v.caption)) error(issues, 'CONCEPT_VISUAL_CAPTION_MISSING', `${p}.caption`, 'A concept visual needs a visible concept/illustrative/notional/proposed caption');
    }
  };
  if (layout === 'cover') {
    required(issues, value, ['visual', 'subtitle', 'body', 'pillars'], path); visual(value.visual, `${path}.visual`); textBudget(issues, value.subtitle, `${path}.subtitle`, 240, 'Subtitle'); textBudget(issues, value.body, `${path}.body`, 700, 'Body');
    if (!Array.isArray(value.pillars) || value.pillars.length < 1 || value.pillars.length > 3) error(issues, 'COUNT_BOUNDARY', `${path}.pillars`, 'Cover pillars must contain 1–3 items');
  } else if (layout === 'fit') {
    required(issues, value, ['visual', 'companyLabel', 'companyHeadline', 'companyBody', 'partnerLabel', 'partnerBody', 'benefits', 'takeaway'], path); visual(value.visual, `${path}.visual`);
    if (!Array.isArray(value.benefits) || value.benefits.length < 2 || value.benefits.length > 3) error(issues, 'COUNT_BOUNDARY', `${path}.benefits`, 'Fit benefits must contain 2–3 items');
    else value.benefits.forEach((b: any, i: number) => { if (!isRecord(b) || !str(b.title) || !str(b.body)) error(issues, 'BENEFIT_INVALID', `${path}.benefits[${i}]`, 'Benefit requires title and body'); });
  } else if (layout === 'options') {
    required(issues, value, ['options', 'status', 'explore'], path);
    if (!Array.isArray(value.options) || value.options.length < 2 || value.options.length > 3) error(issues, 'COUNT_BOUNDARY', `${path}.options`, 'Options must contain 2–3 items');
    else value.options.forEach((o: any, i: number) => { const p = `${path}.options[${i}]`; if (!isRecord(o)) error(issues, 'OPTION_INVALID', p, 'Option must be an object'); else { required(issues, o, ['title', 'body', 'revenue'], p); for (const k of ['title', 'body', 'revenue']) if (!str(o[k])) error(issues, 'OPTION_FIELD_MISSING', `${p}.${k}`, 'Option field is required'); if (o.visual) visual(o.visual, `${p}.visual`); if (o.schematic !== undefined) oneOf(issues, o.schematic, new Set(['manufacture', 'hybrid', 'service']), `${p}.schematic`); } });
    if (value.payment !== undefined) validateTransaction(issues, value.payment, `${path}.payment`);
  } else if (layout === 'models') {
    required(issues, value, ['models', 'explore'], path);
    if (!Array.isArray(value.models) || value.models.length !== 2) error(issues, 'COUNT_BOUNDARY', `${path}.models`, 'Models must contain exactly 2 items');
    else value.models.forEach((m: any, i: number) => { const p = `${path}.models[${i}]`; if (!isRecord(m)) error(issues, 'MODEL_INVALID', p, 'Model must be an object'); else { required(issues, m, ['label', 'title', 'body', 'payments', 'benefit'], p); for (const k of ['label', 'title', 'body', 'benefit']) if (!str(m[k])) error(issues, 'MODEL_FIELD_MISSING', `${p}.${k}`, 'Model field is required'); validateTransaction(issues, m.payments, `${p}.payments`); if (m.visual) visual(m.visual, `${p}.visual`); } });
  } else if (layout === 'channels') {
    required(issues, value, ['scope', 'selection', 'criteria', 'models', 'serviceLabel', 'service', 'explore'], path); if (value.visual) visual(value.visual, `${path}.visual`);
    if (!Array.isArray(value.models) || value.models.length < 1 || value.models.length > 2) error(issues, 'COUNT_BOUNDARY', `${path}.models`, 'Channel models must contain 1–2 items');
    else value.models.forEach((m: any, i: number) => { const p = `${path}.models[${i}]`; if (!isRecord(m)) error(issues, 'CHANNEL_MODEL_INVALID', p, 'Channel model must be an object'); else { required(issues, m, ['label', 'benefit', 'payments'], p); if (!str(m.label) || !str(m.benefit)) error(issues, 'CHANNEL_MODEL_FIELD_MISSING', p, 'Channel model requires label and benefit'); validateTransaction(issues, m.payments, `${p}.payments`); } });
  } else if (layout === 'missions') {
    required(issues, value, ['intro', 'status', 'cards', 'explore'], path);
    if (!Array.isArray(value.cards) || value.cards.length < 2 || value.cards.length > 4) error(issues, 'COUNT_BOUNDARY', `${path}.cards`, 'Mission cards must contain 2–4 items');
    else value.cards.forEach((c: any, i: number) => { const p = `${path}.cards[${i}]`; if (!isRecord(c)) error(issues, 'MISSION_CARD_INVALID', p, 'Mission card must be an object'); else { required(issues, c, ['label', 'title', 'description', 'visual'], p); for (const k of ['label', 'title', 'description']) if (!str(c[k])) error(issues, 'MISSION_CARD_FIELD_MISSING', `${p}.${k}`, 'Mission card field is required'); visual(c.visual, `${p}.visual`); } });
  } else if (layout === 'close') {
    required(issues, value, ['visual', 'intro', 'conversations', 'ask', 'contact'], path); visual(value.visual, `${path}.visual`);
    if (!Array.isArray(value.conversations) || value.conversations.length < 1 || value.conversations.length > 3) error(issues, 'COUNT_BOUNDARY', `${path}.conversations`, 'Close conversations must contain 1–3 items');
    else value.conversations.forEach((c: any, i: number) => { const p = `${path}.conversations[${i}]`; if (!isRecord(c) || !str(c.title) || !str(c.body)) error(issues, 'CONVERSATION_INVALID', p, 'Conversation requires title and body'); });
  }
  if(layout==='sales')collectVisuals(value).forEach((v,i)=>visual(v,`${path}.visuals[${i}]`));
  else checkSlideBudgets(issues, value, path);
}

function allStrings(value: unknown, path = '', output: Array<{ value: string; path: string }> = []): Array<{ value: string; path: string }> {
  if (typeof value === 'string') output.push({ value, path });
  else if (Array.isArray(value)) value.forEach((v, i) => allStrings(v, `${path}[${i}]`, output));
  else if (isRecord(value)) Object.entries(value).forEach(([k, v]) => allStrings(v, path ? `${path}.${k}` : k, output));
  return output;
}
function slideText(slide: any): string[] {
  if (!isRecord(slide)) return [];
  const clone: Record<string, any> = { ...slide }; delete clone.notes; delete clone.claimIds; delete clone.sourceIds; delete clone.opportunityIds; delete clone.key; delete clone.layout;
  return allStrings(clone).map(x => x.value);
}
function quantitative(text: string): boolean { return /(?:\$\s*\d|\d[\d,.]*\s*%|\b\d+(?:\.\d+)?\s*(?:km|mi|miles?|knots?|seats?|units?|boats?|vessels?|months?|years?|days?)\b|\b20\d{2}\b)/i.test(text); }
function readiness(text: string): boolean { return /\b(?:ready\s+to\s+(?:launch|deliver|deploy)|launch[- ]ready|approved\s+integration|integration\s+approved|now\s+available|available\s+capacity|will\s+launch|guaranteed)\b/i.test(text); }

export async function validateProject(data: unknown, options: { projectRoot?: string; checkFiles?: boolean; forPublication?: boolean } = {}): Promise<ValidationResult> {
  const issues: ValidationIssue[] = [];
  if (!isRecord(data)) return { ok: false, releaseReady: false, issues: [{ severity: 'error', code: 'PROJECT_OBJECT_REQUIRED', path: '', message: 'Project must be an object' }] };
  const structural=schemaIssues(data);issues.push(...structural);
  // Union errors can include irrelevant missing properties from other slide layouts.
  // Preserve V1's detailed budget/readiness diagnostics when traversal is safe.
  const unsafeRoot=!isRecord(data.meta)||!isRecord(data.policy)||['sources','claims','assets','opportunities','slides'].some(key=>!Array.isArray(data[key])||data[key].some((item:unknown)=>!isRecord(item)));
  const unsafeV2=data.schemaVersion==='2.0.0'&&structural.some(i=>/must be (?:object|array|string|number|boolean)|must have required property/.test(i.message));
  if(unsafeRoot||unsafeV2)return {ok:false,releaseReady:false,issues};
  const project = data as any;
  required(issues, project, ['schemaVersion', 'meta', 'sources', 'claims', 'assets', 'opportunities', 'slides', 'policy'], 'project');
  if (!['1.0.0','2.0.0'].includes(project.schemaVersion)) error(issues, 'SCHEMA_VERSION', 'schemaVersion', 'Expected schemaVersion 1.0.0 or 2.0.0');
  const meta = project.meta;
  if (!isRecord(meta)) error(issues, 'META_REQUIRED', 'meta', 'meta must be an object');
  else {
    required(issues, meta, ['projectId', 'revision', 'title', 'company', 'partner', 'legalEntity', 'audience', 'archetype', 'objective', 'meetingAudience', 'date', 'classification', 'fictional', 'footer'], 'meta');
    for (const key of ['projectId', 'revision', 'title', 'company', 'partner', 'legalEntity', 'objective', 'meetingAudience', 'classification', 'footer']) if (!str(meta[key])) error(issues, 'META_FIELD_MISSING', `meta.${key}`, 'Metadata field is required');
    idCheck(issues, meta.projectId, 'meta.projectId'); idCheck(issues, meta.revision, 'meta.revision'); oneOf(issues, meta.audience, AUDIENCES, 'meta.audience'); oneOf(issues, meta.archetype, new Set(['industrial', 'energy-operator', 'strategic']), 'meta.archetype'); dateCheck(issues, meta.date, 'meta.date'); if (typeof meta.fictional !== 'boolean') error(issues, 'META_BOOLEAN', 'meta.fictional', 'fictional must be boolean');
  }
  const policy = project.policy;
  if (!isRecord(policy)) error(issues, 'POLICY_REQUIRED', 'policy', 'policy must be an object');
  else {
    required(issues, policy, ['forbiddenTerms', 'forbiddenPartnerNames', 'requiredPhrases', 'allowMissingLogosForInternalReview'], 'policy');
    for (const key of ['forbiddenTerms', 'forbiddenPartnerNames', 'requiredPhrases']) if (!Array.isArray(policy[key]) || policy[key].some((x: unknown) => !str(x))) error(issues, 'POLICY_ARRAY_INVALID', `policy.${key}`, 'Policy values must be text arrays');
    if (typeof policy.allowMissingLogosForInternalReview !== 'boolean') error(issues, 'POLICY_BOOLEAN', 'policy.allowMissingLogosForInternalReview', 'allowMissingLogosForInternalReview must be boolean');
  }
  const sources:any[] = Array.isArray(project.sources) ? project.sources : []; const claims:any[] = Array.isArray(project.claims) ? project.claims : []; const assets:any[] = Array.isArray(project.assets) ? project.assets : []; const opportunities:any[] = Array.isArray(project.opportunities) ? project.opportunities : []; const slides:any[] = Array.isArray(project.slides) ? project.slides : [];
  for (const key of ['sources','claims','assets','opportunities','slides'] as const) if (!Array.isArray(project[key])) error(issues, 'ARRAY_REQUIRED', key, 'Expected an array');
  uniqueIds(issues, [{ value: sources, path: 'sources' }, { value: claims, path: 'claims' }, { value: assets, path: 'assets' }, { value: opportunities, path: 'opportunities' }, { value: slides, path: 'slides' }]);
  sources.forEach((s, i) => validateSource(issues, s, `sources[${i}]`));
  const sourceIds = new Set(sources.filter(isRecord).map(s => s.id).filter((x): x is string => typeof x === 'string'));
  claims.forEach((c, i) => validateClaim(issues, c, `claims[${i}]`, sourceIds));
  const claimIds = new Set(claims.filter(isRecord).map(c => c.id).filter((x): x is string => typeof x === 'string'));
  assets.forEach((a, i) => validateAsset(issues, a, `assets[${i}]`));
  const assetIds = new Set(assets.filter(isRecord).map(a => a.id).filter((x): x is string => typeof x === 'string'));
  assets.forEach((a, i) => { if (isRecord(a)) refs(issues, a.sourceIds, `assets[${i}].sourceIds`, sourceIds, true); });
  opportunities.forEach((o, i) => validateOpportunity(issues, o, `opportunities[${i}]`, claimIds));
  const opportunityIds = new Set(opportunities.filter(isRecord).map(o => o.id).filter((x): x is string => typeof x === 'string'));
  if(project.schemaVersion==='2.0.0'&&structural.length===0)issues.push(...salesIssues(project));
  const known = { claims: claimIds, sources: sourceIds, assets: assetIds, opportunities: opportunityIds, assetRecords: assets };
  slides.forEach((s, i) => validateSlide(issues, s, i, known));
  if (slides.length < 2 || slides[0]?.layout !== 'cover') error(issues, 'SLIDE_ORDER', 'slides', 'Slide order must start with cover and include a variable-length deck');
  if (slides.length < 2 || slides[slides.length - 1]?.layout !== 'close' && !(slides[slides.length - 1]?.layout === 'sales' && slides[slides.length - 1]?.composition === 'strategic-close')) error(issues, 'SLIDE_ORDER', 'slides', 'Slide order must end with close');
  // Strong privacy and audience checks intentionally include unused records for public artifacts.
  const audience: Audience | undefined = meta?.audience;
  const publication = options.forPublication === true || audience === 'public';
  if (publication) {
    sources.forEach((s: any, i: number) => { if (s.visibility !== 'public') error(issues, 'PUBLIC_SOURCE_PRIVATE', `sources[${i}].visibility`, 'Public publication cannot contain non-public sources, including unused records'); });
    assets.forEach((a: any, i: number) => { if (a.visibility !== 'public') error(issues, 'PUBLIC_ASSET_PRIVATE', `assets[${i}].visibility`, 'Public publication cannot contain non-public assets, including unused records'); });
    claims.forEach((c: any, i: number) => { if (!Array.isArray(c.clearedFor) || !c.clearedFor.includes('public')) error(issues, 'PUBLIC_CLAIM_UNCLEARED', `claims[${i}].clearedFor`, 'Public publication requires public claim clearance'); });
  }
  const usedClaimIds = new Set<string>(); const usedAssetIds = new Set<string>(); const usedSourceIds = new Set<string>();
  slides.forEach((s: any) => { if (!isRecord(s)) return; (s.claimIds ?? []).forEach((x: any) => usedClaimIds.add(x)); (s.sourceIds ?? []).forEach((x: any) => usedSourceIds.add(x)); (s.opportunityIds ?? []).forEach((x: any) => { const o = opportunities.find((v: any) => v?.id === x); (o?.claimIds ?? []).forEach((c: any) => usedClaimIds.add(c)); }); const visit = (v: any) => { if (!v || typeof v !== 'object') return; if (typeof v.assetId === 'string') usedAssetIds.add(v.assetId); Object.values(v).forEach(visit); }; visit(s); });
  opportunities.forEach((o: any) => (o?.claimIds ?? []).forEach((x: any) => usedClaimIds.add(x)));
  if(project.sales)for(const b of project.sales.blocks??[])for(const id of b.claimIds??[])usedClaimIds.add(id);
  for (const claimId of usedClaimIds) { const c: any = claims.find(x => x?.id === claimId); (c?.sourceIds ?? []).forEach((x: any) => usedSourceIds.add(x)); }
  for (const assetId of usedAssetIds) { const a: any = assets.find(x => x?.id === assetId); (a?.sourceIds ?? []).forEach((x: any) => usedSourceIds.add(x)); }
  if (meta?.companyLogoAssetId) usedAssetIds.add(meta.companyLogoAssetId);
  if (meta?.partnerLogoAssetId) usedAssetIds.add(meta.partnerLogoAssetId);
  if (audience === 'partner' || audience === 'public' || options.forPublication) {
    for (const claimId of usedClaimIds) { const c: any = claims.find(x => x?.id === claimId); if (c && !c.clearedFor?.includes(audience === 'public' || options.forPublication ? 'public' : 'partner')) error(issues, 'CLAIM_AUDIENCE_UNCLEARED', `claims.${claimId}.clearedFor`, 'Referenced claim is not cleared for the deck audience'); }
    for (const assetId of usedAssetIds) { const a: any = assets.find(x => x?.id === assetId); if (a && !a.clearedFor?.includes(audience === 'public' || options.forPublication ? 'public' : 'partner')) error(issues, 'ASSET_AUDIENCE_UNCLEARED', `assets.${assetId}.clearedFor`, 'Referenced asset is not cleared for the deck audience'); }
  }
  if (audience === 'partner') for (const source of sources as any[]) if (source.visibility !== 'public' && usedSourceIds.has(source.id)) warn(issues, 'PRIVATE_SOURCE_EDITORIAL_CHECK', `sources.${source.id}`, 'Private source locators must not be exposed in partner-facing notes; perform an editorial check');
  const missingLogos = !meta?.companyLogoAssetId || !meta?.partnerLogoAssetId;
  if (missingLogos) {
    if (audience === 'internal' && policy?.allowMissingLogosForInternalReview && !options.forPublication) hold(issues, 'MISSING_LOGO_RELEASE_HOLD', 'meta', 'Internal review may omit logos, but a release-ready artifact may not');
    else error(issues, 'MISSING_LOGO', 'meta', 'Release/public/partner decks require both logos');
  }
  if (meta?.companyLogoAssetId && !assetIds.has(meta.companyLogoAssetId)) error(issues, 'UNKNOWN_REFERENCE', 'meta.companyLogoAssetId', 'Unknown company logo asset');
  if (meta?.partnerLogoAssetId && !assetIds.has(meta.partnerLogoAssetId)) error(issues, 'UNKNOWN_REFERENCE', 'meta.partnerLogoAssetId', 'Unknown partner logo asset');
  // A small, intentionally conservative heuristic: only strong readiness claims are blocked.
  slides.forEach((s: any, i: number) => {
    let texts=slideText(s);if(s.layout==='sales'&&structural.length===0){try{texts=blockIds(s).map(id=>resolveBlock(project,id).text);}catch{ /* Resolution errors are reported by salesIssues. */ }}const combined=texts.join(' ');
    if (readiness(combined)) error(issues, 'FUTURE_READINESS_UNSUPPORTED', `slides[${i}]`, 'Evaluation material cannot imply launch readiness, approved integration, guaranteed delivery, or available capacity');
    if (quantitative(combined)) {
      if ((!Array.isArray(s.claimIds) || s.claimIds.length === 0) && !(s.layout==='sales'&&structural.length===0&&blockIds(s).some(id=>{try{return resolveBlock(project,id).claimIds.length>0;}catch{return false;}}))) error(issues, 'QUANTITATIVE_CLAIM_MISSING', `slides[${i}]`, 'Visible quantitative content needs at least one referenced claim');
      else for (const claimId of s.claimIds) { const c: any = claims.find(x => x?.id === claimId); if (c && !str(c.basis)) error(issues, 'QUANTITATIVE_BASIS_MISSING', `claims.${claimId}.basis`, 'Quantitative visible content needs a claim with basis'); }
    }
  });
  const heroUses = new Map<string, number>();
  slides.forEach((s: any) => { if (!isRecord(s) || !['cover', 'fit', 'close'].includes(s.layout)) return; const id = s.visual?.assetId; const a: any = assets.find(x => x?.id === id); if (id && a?.kind === 'photograph') heroUses.set(id, (heroUses.get(id) ?? 0) + 1); });
  for (const [id, count] of heroUses) if (count > 1) warn(issues, 'REPEATED_HERO_PHOTO', `assets.${id}`, 'The same photograph is used as more than one hero visual; confirm that repetition is necessary');
  if (policy?.forbiddenTerms || policy?.forbiddenPartnerNames) {
    const forbidden = [...(policy.forbiddenTerms ?? []), ...(policy.forbiddenPartnerNames ?? [])].filter(str);
    const content = allStrings({ ...project, policy: undefined }).filter(x => x.path !== 'meta.partner');
    for (const item of content) for (const term of forbidden) if (term && item.value.toLocaleLowerCase().includes(term.toLocaleLowerCase())) error(issues, 'FORBIDDEN_CONTENT', item.path, 'Content contains a policy-forbidden term or other-partner name');
    for (const item of content) if (/\bN120\b/i.test(item.value)) error(issues, 'RETIRED_PRODUCT_LEAKAGE', item.path, 'Retired product name N120 is prohibited');
    const visible = slides.flatMap((s: any) => {if(s.layout==='sales'&&structural.length===0){try{return blockIds(s).map(id=>resolveBlock(project,id).text);}catch{return [];}}return slideText(s);}).join(' ').toLocaleLowerCase();
    for (const phrase of policy.requiredPhrases ?? []) if (str(phrase) && !visible.includes(phrase.toLocaleLowerCase())) error(issues, 'REQUIRED_PHRASE_MISSING', 'slides', `Required phrase is missing from visible slide copy: ${phrase}`);
  }
  if (options.checkFiles) {
    if (!options.projectRoot) error(issues, 'PROJECT_ROOT_REQUIRED', 'options.projectRoot', 'projectRoot is required when checkFiles is true');
    else issues.push(...await verifyAssetFiles(project as Project, options.projectRoot));
  }
  hold(issues, 'HUMAN_RELEASE_REQUIRED', 'review', 'Validation is not human finished-deck approval or external-release permission.');
  const hasErrors = issues.some(i => i.severity === 'error');
  const releaseReady = !hasErrors && !issues.some(i => i.severity === 'release-hold');
  return { ok: !hasErrors, releaseReady, issues };
}

export async function assertValidProject(data: unknown, options: { projectRoot?: string; checkFiles?: boolean; forPublication?: boolean } = {}): Promise<Project> {
  const result = await validateProject(data, options);
  if (!result.ok) {
    const summary = result.issues.filter(i => i.severity === 'error').slice(0, 12).map(i => `${i.code} at ${i.path}: ${i.message}`).join('; ');
    throw new Error(`Invalid strategic-partner project (${result.issues.filter(i => i.severity === 'error').length} errors): ${summary}`);
  }
  return data as Project;
}
