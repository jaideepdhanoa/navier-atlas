import { mkdir, writeFile, rm } from 'node:fs/promises';
import { dirname, join, relative, resolve } from 'node:path';
import { validateProject } from '../src/validate';
import { compileProject } from '../src/render';
import type { Project, Opportunity, Asset, Slide } from '../src/types';

type Binding = { opportunityId: string; field: string };
type Placement = 'core' | 'appendix' | 'notes';
type Pair = { heading: string; body: string; headingBindings?: Binding[]; bodyBindings?: Binding[]; visual?: string };
type Spec = Record<string, any>;

const examplesRoot = dirname(import.meta.path);
const fixtureDate = '2026-09-19';
const fictionStatus = 'FICTIONAL CONCEPT — internal review only; no deployment, measurements, or approval.';
const fictionCaption = (label: string) => `Fictional concept illustration: ${label}. Not evidence of deployed engineering.`;
const sha256 = (bytes: Uint8Array | string) => new Bun.CryptoHasher('sha256').update(bytes).digest('hex');
const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const bind = (opportunityId: string, ...fields: string[]): Binding[] => fields.map(field => ({ opportunityId, field }));

const svgBody = (label: string, accent: string, motif: string) => `<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">
<rect width="1600" height="900" fill="#07131f"/>
<path d="M0 690 Q350 510 720 685 T1600 560 V900 H0Z" fill="${accent}" opacity=".28"/>
<path d="${motif}" fill="none" stroke="#d7f3ff" stroke-width="14" stroke-linecap="round" stroke-linejoin="round" opacity=".86"/>
<circle cx="1260" cy="260" r="164" fill="none" stroke="${accent}" stroke-width="14" opacity=".76"/>
<text x="100" y="150" fill="#fff" font-family="Arial" font-size="58" font-weight="700">${esc(label)}</text>
<text x="100" y="220" fill="#a9c7d8" font-family="Arial" font-size="29">FICTIONAL WORKFLOW CONCEPT • NOT A REAL PRODUCT</text>
<text x="100" y="780" fill="${accent}" font-family="Arial" font-size="25" letter-spacing="4">SCHEMATIC FIXTURE • NO DEPLOYMENT CLAIM</text>
<rect x="100" y="730" width="1400" height="3" fill="${accent}"/>
</svg>`;

async function makeAsset(dir: string, sourceId: string, id: string, label: string, accent: string, motif: string): Promise<Asset> {
  const assetDir = join(dir, 'assets');
  await mkdir(assetDir, { recursive: true });
  const svgName = `${id}.svg`;
  const pngName = `${id}.png`;
  const svgPath = join(assetDir, svgName);
  const pngPath = join(assetDir, pngName);
  await writeFile(svgPath, svgBody(label, accent, motif));
  const proc = Bun.spawn(['magick', svgPath, '-strip', pngPath], { stdout: 'ignore', stderr: 'pipe' });
  if (await proc.exited !== 0) throw new Error(`ImageMagick could not generate ${pngName}`);
  const bytes = new Uint8Array(await Bun.file(pngPath).arrayBuffer());
  const hash = sha256(bytes);
  return {
    id: `asset-${id}`, path: `assets/${pngName}`, sha256: hash, width: 1600, height: 900, mimeType: 'image/png',
    kind: 'schematic', maturity: 'concept', title: label,
    missions: ['fictional workflow illustration'], geography: ['fictional coastal setting'], roles: ['concept visual'],
    sourceIds: [sourceId], visibility: 'public', clearedFor: ['internal', 'partner', 'public'],
    rightsNote: `Original local SVG fixture (${svgName}); deterministic PNG derivative generated with ImageMagick -strip; no external imagery.`,
    caption: fictionCaption(label),
    visualBrief: {
      argument: `Make the ${label.toLowerCase()} commercial concept legible without implying installed infrastructure or measured performance.`,
      requiredFeatures: ['clear system geometry', 'fictional concept label', 'legible business role'],
      prohibitedImplications: ['real customer', 'measured performance', 'installed infrastructure', 'approved design'],
      origin: 'fixture', referenceSourceIds: [sourceId],
      architectureOptions: ['diagrammatic flow', 'layered system map'],
      unresolvedChoices: ['final visual treatment', 'system boundaries', 'human visual review'],
      review: { status: 'pending', assetSha256: hash, reviewerKind: 'fixture', reviewer: '', reviewedAt: '' },
    },
  };
}

class Author {
  blocks: any[] = [];
  slides: any[] = [];
  constructor(readonly cfg: any, readonly sourceId: string, readonly claimId: string, readonly opportunityIds: Set<string>) {}
  block(id: string, text: string, bindings: Binding[] = [], placement: Placement = 'core', placementReason?: string): string {
    if (this.blocks.some(b => b.id === id)) throw new Error(`Duplicate block ${id}`);
    const b: any = { id, text, bindings, claimIds: [this.claimId], placement };
    if (placementReason) b.placementReason = placementReason;
    this.blocks.push(b); return id;
  }
  pair(slideKey: string, name: string, p: Pair) {
    return {
      heading: this.block(`${slideKey}-${name}-heading`, p.heading, p.headingBindings || []),
      body: this.block(`${slideKey}-${name}-body`, p.body, p.bodyBindings || []),
      ...(p.visual ? { visual: this.visual(p.visual) } : {}),
    };
  }
  visual(assetId: string) { const actualId = this.cfg.assetIdMap?.[assetId] || assetId; return { assetId: actualId, caption: fictionCaption(this.cfg.assetLabels[assetId] || assetId) }; }
  base(key: string, kicker: string, title: string, titleBindings: Binding[] = [], opportunityIds: string[] = []) {
    return { key, kicker, title: this.block(`${key}-title`, title, titleBindings), claimIds: [this.claimId], sourceIds: [this.sourceId], opportunityIds, notes: '', layout: 'sales' as const };
  }
  sales(spec: Spec): any {
    const key = spec.key;
    const title = this.block(`${key}-title`, spec.title, spec.titleBindings || []);
    const status = this.block(`${key}-status`, fictionStatus);
    const x: any = { key, kicker: spec.kicker, title, claimIds: [this.claimId], sourceIds: [this.sourceId], opportunityIds: [...(spec.opportunityIds || [])], notes: '', layout: 'sales', status, composition: spec.composition };
    const add = (id: string, text: string, bindings: Binding[] = []) => this.block(`${key}-${id}`, text, bindings);
    switch (spec.composition) {
      case 'partner-opportunity':
        x.intro = add('intro', spec.intro, spec.introBindings);
        x.domains = spec.domains.map((p: Pair, i: number) => this.pair(key, `domain-${i}`, p));
        x.proof = spec.proof.map((p: Pair, i: number) => this.pair(key, `proof-${i}`, p));
        x.offer = add('offer', spec.offer, spec.offerBindings);
        break;
      case 'platform-architecture':
        x.banner = add('banner', spec.banner, spec.bannerBindings);
        x.physical = spec.physical.map((p: Pair, i: number) => this.pair(key, `physical-${i}`, p));
        x.ownership = add('ownership', spec.ownership, spec.ownershipBindings);
        x.software = add('software', spec.software, spec.softwareBindings);
        x.revenue = add('revenue', spec.revenue, spec.revenueBindings);
        x.demand = spec.demand.map((p: Pair, i: number) => this.pair(key, `demand-${i}`, p));
        x.takeaway = add('takeaway', spec.takeaway, spec.takeawayBindings);
        break;
      case 'opportunity-portfolio':
        x.intro = add('intro', spec.intro, spec.introBindings);
        x.programs = spec.programs.map((p: any) => ({ opportunityId: p.opportunityId, heading: add(`${p.opportunityId}-heading`, p.heading, bind(p.opportunityId, 'title')), value: add(`${p.opportunityId}-value`, p.value, p.bindings), visual: this.visual(p.asset) }));
        x.connection = add('connection', spec.connection, spec.connectionBindings);
        break;
      case 'customer-alternative':
        x.intro = add('intro', spec.intro, spec.introBindings);
        x.alternatives = spec.alternatives.map((p: any, i: number) => ({ heading: add(`alternative-${i}-heading`, p.heading, p.headingBindings), body: add(`alternative-${i}-body`, p.body, p.bodyBindings), emphasis: !!p.emphasis }));
        x.jobs = add('jobs', spec.jobs, spec.jobsBindings);
        x.advantage = add('advantage', spec.advantage, spec.advantageBindings);
        const basis = add('comparison-basis', spec.basis);
        x.comparison = { basisBlockId: basis, claimIds: [this.claimId], kind: 'qualitative' };
        break;
      case 'mission-hero':
        x.visual = this.visual(spec.asset); x.need = add('need', spec.need, spec.needBindings);
        x.benefits = spec.benefits.map((p: Pair, i: number) => this.pair(key, `benefit-${i}`, p));
        x.payoff = add('payoff', spec.payoff, spec.payoffBindings);
        break;
      case 'product-value':
        x.visual = this.visual(spec.asset); x.mechanism = add('mechanism', spec.mechanism, spec.mechanismBindings);
        x.benefits = spec.benefits.map((p: Pair, i: number) => this.pair(key, `benefit-${i}`, p));
        x.proof = add('proof', spec.proof, spec.proofBindings);
        break;
      case 'integrated-infrastructure':
        x.visual = this.visual(spec.asset); x.intro = add('intro', spec.intro, spec.introBindings);
        x.actions = spec.actions.map((p: Pair, i: number) => this.pair(key, `action-${i}`, p));
        x.options = add('options', spec.options, spec.optionsBindings);
        break;
      case 'strategic-close':
        x.intro = add('intro', spec.intro, spec.introBindings);
        x.stakes = spec.stakes.map((p: Pair, i: number) => this.pair(key, `stake-${i}`, p));
        x.visual = this.visual(spec.asset);
        x.invitation = add('invitation', spec.invitation, spec.invitationBindings);
        x.companion = { labelBlockId: add('companion', 'Fictional investment companion • no investment ask'), url: 'https://example.invalid/fictional-workflow' };
        break;
      default: throw new Error(`Unknown composition ${spec.composition}`);
    }
    const derived = new Set<string>(x.opportunityIds);
    const collect = (v: any) => {
      if (typeof v === 'string') {
        const authored = this.blocks.find(b => b.id === v);
        for (const b of authored?.bindings || []) if (this.opportunityIds.has(b.opportunityId)) derived.add(b.opportunityId);
      } else if (Array.isArray(v)) v.forEach(collect);
      else if (v && typeof v === 'object') {
        if (typeof v.opportunityId === 'string' && this.opportunityIds.has(v.opportunityId)) derived.add(v.opportunityId);
        if (Array.isArray(v.bindings)) for (const b of v.bindings) if (this.opportunityIds.has(b.opportunityId)) derived.add(b.opportunityId);
        Object.entries(v).forEach(([k, child]) => { if (!['visual', 'opportunityId', 'bindings'].includes(k)) collect(child); });
      }
    };
    collect(x); x.opportunityIds = [...derived];
    this.slides.push(x); return x;
  }
  addNotes(opportunities: Opportunity[]) {
    const fields = ['payer', 'commercialLogic', 'companyContribution', 'partnerContribution', 'salesCase.scaleBasis', 'salesCase.entryPoint', 'salesCase.evidenceBoundary', 'nextQuestion'];
    for (const o of opportunities) for (const field of fields) {
      const value = field.startsWith('salesCase.') ? (o.salesCase as any)[field.slice(10)] : (o as any)[field];
      this.block(`${o.id}-detail-${field.replace('.', '-')}`, value, bind(o.id, field), 'notes', 'Commercial detail is retained as an explicit scoping note so the visible sales case stays readable without hiding the proposition.');
    }
  }
  finalize(opportunities: Opportunity[], assets: Asset[]): Project {
    const firstCore = (op: string, field: string) => this.blocks.find(b => b.placement === 'core' && b.bindings.some((x: Binding) => x.opportunityId === op && x.field === field))?.id;
    for (const o of opportunities) for (const field of ['salesCase.need','salesCase.alternative','product','customer','salesCase.mechanism','salesCase.outcome','partnerBenefit','salesCase.ambition']) {
      if (!firstCore(o.id, field)) throw new Error(`Missing core binding ${o.id}.${field}`);
    }
    const sourceInventory = [
      { id: 'thesis', sourceId: this.sourceId, kind: 'proposition', importance: 'core', summary: this.cfg.sourceThesis, locator: 'fictional brief / partner thesis' },
      ...opportunities.map(o => ({ id: `prop-${o.id}`, sourceId: this.sourceId, kind: 'proposition', importance: 'core', summary: `${o.title}: ${(o.salesCase as any).need}`, locator: `fictional brief / ${o.id}` })),
    ];
    const thesisBlock = this.slides.find(s => s.composition === 'partner-opportunity')?.intro || this.slides[1]?.title;
    const sourceDisposition = sourceInventory.map(item => {
      const op = item.id.startsWith('prop-') ? item.id.slice(5) : undefined;
      const destinations = op ? ['salesCase.need','salesCase.alternative','product','customer','salesCase.mechanism','salesCase.outcome','partnerBenefit','salesCase.ambition'].map(f => firstCore(op, f)).filter(Boolean) : [thesisBlock];
      return { sourceItemId: item.id, action: 'keep', reason: op ? 'Authored proposition retained in the visible business argument with its ambitious path distinct from the first engagement.' : 'Partner thesis is retained in the partner-relevance opening and connected to the company difference.', destinationBlockIds: [...new Set(destinations)], visualDecision: 'adapt', visualReason: 'Local schematic fixtures adapt the fictional proposition; they are not evidence of deployment or performance.' };
    });
    const narrative = this.slides.map((s: any, i: number) => {
      const job = i === 0 ? 'opening' : s.composition === 'partner-opportunity' ? 'partner-relevance' : s.composition === 'platform-architecture' ? 'company-advantage' : s.composition === 'opportunity-portfolio' ? 'portfolio' : s.composition === 'strategic-close' ? 'invitation' : s.composition === 'customer-alternative' ? 'support' : 'opportunity';
      return { slideKey: s.key, job, takeaway: this.cfg.narrative?.[s.key]?.takeaway || 'This fictional page advances a specific commercial choice.', transition: this.cfg.narrative?.[s.key]?.transition || 'The next page makes the next choice concrete.', chapter: this.cfg.narrative?.[s.key]?.chapter || 'commercial paths', placement: 'core', opportunityIds: s.opportunityIds || [] };
    });
    return {
      schemaVersion: '2.0.0',
      meta: { projectId: this.cfg.slug, revision: 'r1', title: this.cfg.title, company: this.cfg.company, partner: this.cfg.partner, legalEntity: `${this.cfg.partner} Fictional Holdings`, audience: 'internal', archetype: this.cfg.archetype, objective: this.cfg.objective, meetingAudience: 'Internal fictional workflow review', date: fixtureDate, classification: 'FICTIONAL WORKFLOW FIXTURE', fictional: true, footer: 'FICTIONAL • INTERNAL REVIEW • NO REAL PARTNER, FIGURES, APPROVALS, OR DEPLOYMENT' },
      sources: [{ id: this.sourceId, title: `${this.cfg.partner} fictional workflow brief`, locator: `https://example.invalid/${this.cfg.slug}/brief`, asOf: fixtureDate, visibility: 'public' }],
      claims: [{ id: this.claimId, statement: `All propositions in this ${this.cfg.slug} example are fictional authoring fixtures.`, evidenceClass: 'fictional', sourceIds: [this.sourceId], basis: 'Deliberately authored regression fixture; no external evidence or relationship is asserted.', clearedFor: ['internal','partner','public'], limitations: 'Not a market claim, engineering claim, approval, demand signal, or deployment record.' }],
      assets,
      opportunities,
      slides: this.slides,
      policy: { forbiddenTerms: [], forbiddenPartnerNames: [], requiredPhrases: [], allowMissingLogosForInternalReview: true },
      sales: {
        brief: { role: 'standalone', audienceDecision: this.cfg.audienceDecision, partnerRelevance: this.cfg.partnerRelevance, partnerThesis: this.cfg.sourceThesis, companyDifference: this.cfg.companyDifference, combinationAdvantage: this.cfg.combinationAdvantage, strategicUpside: this.cfg.strategicUpside, investmentBoundary: 'This is not an investment proposal; any companion link is a fictional workflow placeholder.', sourceIds: [this.sourceId], unresolvedQuestions: this.cfg.unresolvedQuestions },
        sourceInventory, sourceDisposition, blocks: this.blocks, narrative,
      },
    } as Project;
  }
}

function opportunitiesForEnergy(): Opportunity[] {
  return [
    { id: 'offshore-service', kind: 'service', title: 'Offshore service exchange', product: 'A coordinated offshore vessel-service window', customer: 'Fictional offshore asset operators', payer: 'Participating asset operators', commercialLogic: 'Recurring service coordination can be contracted per operating window after a scoped design.', partnerBenefit: 'The partner gains a credible services wedge around its coastal infrastructure relationships.', companyContribution: 'Tideframe supplies the scheduling, vessel interface, and service workflow concept.', partnerContribution: 'Asteris Gridworks contributes access to relevant operating contexts and convening power.', nextQuestion: 'Which fictional operating context should define the first non-binding workflow study?', claimIds: ['claim-energy-infrastructure'], status: 'proposed', salesCase: { need: 'Offshore operators need a clearer handoff between vessel availability and time-sensitive service work.', alternative: 'Today the handoff is assembled through fragmented brokers, calls, and one-off schedules.', scaleBasis: 'A repeatable service-window pattern can extend across a family of coastal operating contexts.', mechanism: 'A shared operating window aligns vessel, berth, crew, and job constraints before a booking is requested.', outcome: 'Operators see a more legible path from service need to coordinated marine work.', ambition: 'Build a recurring offshore service exchange that becomes a trusted operating layer across coastal assets.', entryPoint: 'A bounded workflow study with one fictional operating context.', evidenceBoundary: 'Fictional concept only; no demand, readiness, performance, or customer commitment is evidenced.', demandStatus: 'hypothesis', readiness: 'exploratory' } },
    { id: 'coastal-cargo', kind: 'service', title: 'Time-sensitive coastal cargo network', product: 'A scheduled coastal cargo service for urgent loads', customer: 'Fictional manufacturers and coastal depots', payer: 'Cargo shippers or contracted logistics buyers', commercialLogic: 'A service fee can follow recurring scheduled movements once routes and handling responsibilities are defined.', partnerBenefit: 'The partner can add a differentiated coastal logistics offer without owning every movement.', companyContribution: 'Tideframe supplies the marine service concept, route logic, and customer-facing workflow.', partnerContribution: 'Asteris Gridworks contributes local operating context and potential terminal relationships.', nextQuestion: 'Which fictional cargo lane has the cleanest handling and service boundary?', claimIds: ['claim-energy-infrastructure'], status: 'proposed', salesCase: { need: 'Coastal manufacturers need time-sensitive loads to move without waiting for a bespoke charter each time.', alternative: 'The current choice is often a slow land detour or an expensive one-off charter.', scaleBasis: 'A repeatable lane model can support multiple shipper and depot pairings over time.', mechanism: 'Scheduled marine capacity is paired with clear cutoffs, handoffs, and exception handling.', outcome: 'Shippers get a more predictable way to move urgent cargo along the coast.', ambition: 'Grow a network of recurring coastal cargo lanes that makes marine logistics a dependable product.', entryPoint: 'A single fictional lane and handling map, explored without a launch commitment.', evidenceBoundary: 'Fictional concept only; route economics, capacity, demand, and approvals remain unresolved.', demandStatus: 'hypothesis', readiness: 'in-design' } },
    { id: 'local-production', kind: 'contract-build', title: 'Harbor-side product production', product: 'A locally produced marine-energy module', customer: 'Fictional coastal facilities and equipment integrators', payer: 'Facilities or integrators purchasing configured modules', commercialLogic: 'A build-and-support model can combine module revenue with configuration and service work.', partnerBenefit: 'The partner gains a local product pathway that turns infrastructure knowledge into a repeatable offer.', companyContribution: 'Tideframe contributes the product concept, integration logic, and service envelope.', partnerContribution: 'Asteris Gridworks contributes manufacturing-adjacent context and local market access hypotheses.', nextQuestion: 'What fictional product boundary can be specified without assuming a factory or certification?', claimIds: ['claim-energy-infrastructure'], status: 'proposed', salesCase: { need: 'Coastal operators need marine-energy equipment that fits local conditions without waiting for a distant standard package.', alternative: 'They adapt imported components or commission bespoke integrations with slow feedback loops.', scaleBasis: 'A configurable module family could serve several coastal facility archetypes.', mechanism: 'A local configuration workflow turns common interfaces into a clearly bounded marine-energy product.', outcome: 'Facilities can evaluate a more adaptable product path with clearer integration choices.', ambition: 'Establish a family of locally configured marine-energy products with a durable support business.', entryPoint: 'A fictional configuration brief and integration boundary, not a manufacturing commitment.', evidenceBoundary: 'Fictional concept only; product readiness, certification, factory capacity, and unit economics are unknown.', demandStatus: 'market-context', readiness: 'in-design' } },
    { id: 'floating-power-compute', kind: 'operator-program', title: 'Floating power and compute', product: 'A floating power-and-compute service concept', customer: 'Fictional coastal operators with flexible power or compute needs', payer: 'An operator, site host, or contracted capacity buyer', commercialLogic: 'A capacity-service model could combine platform operations with contracted energy or compute access.', partnerBenefit: 'The partner can explore a visible new infrastructure category without prematurely choosing ownership or hardware.', companyContribution: 'Tideframe contributes the marine systems concept and customer workflow around flexible capacity.', partnerContribution: 'Asteris Gridworks contributes infrastructure strategy and a forum for resolving operating roles.', nextQuestion: 'Which capacity service and operating boundary should be tested first?', claimIds: ['claim-energy-infrastructure'], status: 'proposed', salesCase: { need: 'Some coastal sites need flexible capacity without committing immediately to a fixed land-based build.', alternative: 'They stack temporary generators, constrained grid access, or separate compute contracts.', scaleBasis: 'A platform service could eventually support several coastal capacity use cases.', mechanism: 'Floating modules connect power, compute, and site operations through an explicitly chosen service boundary.', outcome: 'Site hosts get a clearer option set for flexible coastal capacity.', ambition: 'Develop a repeatable floating capacity service spanning power, compute, and coastal operations.', entryPoint: 'A fictional architecture and operating-role workshop.', evidenceBoundary: 'Fictional concept only; power, compute, marine, safety, and commercial feasibility are unresolved.', demandStatus: 'hypothesis', readiness: 'exploratory' } },
  ];
}

function opportunitiesForIndustrial(): Opportunity[] {
  return [
    { id: 'supply-modules', kind: 'supply', title: 'Modular marine supply', product: 'A repeatable module supply program', customer: 'Fictional builders and fleet operators', payer: 'Builders or operators purchasing modules', commercialLogic: 'Component supply can be paired with configuration support and lifecycle service.', partnerBenefit: 'The partner expands its product range with a marine-ready supply path.', companyContribution: 'Tideframe contributes the module architecture and application workflow.', partnerContribution: 'Kestrel Forge contributes industrial context, supplier discipline, and channel hypotheses.', nextQuestion: 'Which module boundary is most useful for a first design review?', claimIds: ['claim-industrial-oem'], status: 'proposed', salesCase: { need: 'Builders need configurable marine modules without recreating the interface for every program.', alternative: 'They source disconnected components and absorb integration risk in each build.', scaleBasis: 'A common module family could serve several fictional platform variants.', mechanism: 'A stable interface and configuration guide make the module repeatable across builds.', outcome: 'Builders can evaluate a clearer supply path with fewer bespoke handoffs.', ambition: 'Create a dependable module supply business that compounds across platforms and service channels.', entryPoint: 'A bounded module definition and interface review.', evidenceBoundary: 'Fictional concept only; no supplier qualification, production capacity, or field performance is evidenced.', demandStatus: 'hypothesis', readiness: 'in-design' } },
    { id: 'build-license', kind: 'license', title: 'Build-and-license pathway', product: 'A licensed marine build system', customer: 'Fictional regional manufacturers', payer: 'Licensees paying for design support and rights', commercialLogic: 'License access can be combined with engineering support, acceptance criteria, and optional component supply.', partnerBenefit: 'The partner can enter a new category while keeping regional manufacturing ownership explicit.', companyContribution: 'Tideframe contributes the design system, training concept, and integration guardrails.', partnerContribution: 'Kestrel Forge contributes manufacturing capability hypotheses and regional execution context.', nextQuestion: 'What must remain controlled by the licensor versus the regional builder?', claimIds: ['claim-industrial-oem'], status: 'proposed', salesCase: { need: 'Regional builders need a credible way to enter marine products without starting with an empty design sheet.', alternative: 'They either develop slowly in-house or license a black box with little adaptation support.', scaleBasis: 'A controlled build system can be adapted across selected regional product families.', mechanism: 'A license package combines design rules, acceptance gates, and support rather than only a drawing set.', outcome: 'Builders gain a more navigable path from design intent to local production.', ambition: 'Establish a regional build-and-license network with consistent product language and support.', entryPoint: 'A fictional boundary-of-control workshop and sample license architecture.', evidenceBoundary: 'Fictional concept only; licensing terms, engineering validation, and regional approvals are unresolved.', demandStatus: 'market-context', readiness: 'exploratory' } },
    { id: 'distribution-service', kind: 'resale', title: 'Distribution and service channel', product: 'A marine product distribution and service program', customer: 'Fictional operators reached through industrial channels', payer: 'Operators buying products and service coverage', commercialLogic: 'Channel sales can be extended by training, spares, commissioning support, and recurring service.', partnerBenefit: 'The partner converts existing channel trust into a lifecycle marine offer.', companyContribution: 'Tideframe contributes service design, commissioning workflow, and support playbooks.', partnerContribution: 'Kestrel Forge contributes distributor relationships and after-sales operating discipline.', nextQuestion: 'Which channel capability should anchor the first serviceable product?', claimIds: ['claim-industrial-oem'], status: 'proposed', salesCase: { need: 'Operators need marine products that come with a clear local support path, not a box at the dock.', alternative: 'They rely on generalist distributors and assemble support only after a failure.', scaleBasis: 'A trained channel can carry several compatible products and service tiers.', mechanism: 'Distribution is paired with commissioning, spares, and scheduled support responsibilities.', outcome: 'Operators see a more accountable path from purchase to continued use.', ambition: 'Build a regional distribution-and-service network that makes marine products easier to adopt.', entryPoint: 'A fictional channel capability map and service-boundary review.', evidenceBoundary: 'Fictional concept only; channel demand, service capacity, and support economics are not evidenced.', demandStatus: 'hypothesis', readiness: 'in-design' } },
  ];
}

function opportunitiesForResearch(): Opportunity[] {
  return [
    { id: 'ocean-observation', kind: 'service', title: 'Recurring ocean-observation service', product: 'A recurring coastal observation data service', customer: 'Fictional research consortium teams and public-interest programs', payer: 'Consortium members funding shared observation access', commercialLogic: 'A recurring service subscription can support scheduled collection, quality review, and shared data delivery.', partnerBenefit: 'The consortium gains a dependable shared observation layer without owning every operational asset.', companyContribution: 'Bluequill contributes the observation workflow concept, data handoff, and service design.', partnerContribution: 'Pelagic Research Assembly contributes research priorities, review protocols, and shared-use governance.', nextQuestion: 'Which observation cadence and data product should define a first service design?', claimIds: ['claim-research-network'], status: 'proposed', salesCase: { need: 'Research teams need observations that arrive on a dependable cadence rather than only when a project can assemble a campaign.', alternative: 'They coordinate intermittent expeditions, heterogeneous datasets, and manual handoffs.', scaleBasis: 'One recurring service can support multiple research questions when the data contract is explicit.', mechanism: 'Scheduled collection, quality review, and a shared delivery contract create continuity across studies.', outcome: 'Consortium teams can plan around a consistent observation service and reusable data handoff.', ambition: 'Become the recurring ocean-observation layer that lets a research network focus on questions, not logistics.', entryPoint: 'A service-design study for one observation cadence and review protocol.', evidenceBoundary: 'Fictional concept only; no sensor performance, field cadence, funding, or scientific result is evidenced.', demandStatus: 'partner-demand', readiness: 'exploratory' } },
  ];
}

const motifs = {
  wave: 'M120 610 C350 380 520 770 760 500 S1180 610 1480 330',
  network: 'M160 600 L420 360 L700 560 L970 300 L1420 540 M420 360 L700 180 M700 560 L970 760',
  module: 'M180 520 H520 V300 H850 V540 H1190 V330 H1430 M520 410 H850 M850 420 H1190',
  platform: 'M180 600 H1400 M300 600 V330 H650 V600 M820 600 V250 H1170 V600 M300 330 L475 190 L650 330 M820 250 L995 120 L1170 250',
  observation: 'M120 560 C420 390 650 690 920 430 S1250 360 1490 500 M260 260 L520 520 L780 260 L1040 520 L1320 260',
};

async function buildConfig(cfg: any, opportunities: Opportunity[], assetSpecs: any[]): Promise<{ project: Project; summary: any }> {
  const outDir = join(examplesRoot, cfg.slug);
  await rm(outDir, { recursive: true, force: true });
  await mkdir(outDir, { recursive: true });
  const sourceId = `${cfg.slug}-brief`;
  const claimId = `claim-${cfg.slug}`;
  const assets: Asset[] = [];
  for (const spec of assetSpecs) assets.push(await makeAsset(outDir, sourceId, spec.id, spec.label, spec.accent, spec.motif));
  const author = new Author({ ...cfg, assetLabels: Object.fromEntries(assetSpecs.map(x => [x.id, x.label])), assetIdMap: Object.fromEntries(assetSpecs.map(x => [x.id, `asset-${x.id}`])) }, sourceId, claimId, new Set(opportunities.map(o => o.id)));
  const cover = { key: 'cover', kicker: 'FICTIONAL WORKFLOW FIXTURE', title: `${cfg.partner} × ${cfg.shortTitle}`, claimIds: [claimId], sourceIds: [sourceId], opportunityIds: [], notes: '', layout: 'cover', visual: author.visual(assetSpecs[0].id), subtitle: 'Public-safe fictional V2 authoring fixture', body: 'Authored regression fixture. No real partner, figures, approvals, imagery, or deployment are represented.', pillars: cfg.pillars };
  author.slides.push(cover);
  cfg.slideSpecs(author, assets);
  author.addNotes(opportunities);
  const project = author.finalize(opportunities, assets);
  const result = await validateProject(project, { projectRoot: outDir, checkFiles: true });
  if (!result.ok) throw new Error(`${cfg.slug} validation failed:\n${result.issues.map(i => `${i.severity} ${i.code} ${i.path}: ${i.message}`).join('\n')}`);
  const compiled = compileProject(project, { assetUrls: Object.fromEntries(assets.map(a => [a.id, `https://assets.invalid/${a.path.split('/').pop()}`])) });
  await writeFile(join(outDir, 'project.json'), JSON.stringify(project, null, 2) + '\n');
  return { project, summary: { slug: cfg.slug, slides: project.slides.length, opportunities: project.opportunities.length, compositions: [...new Set(project.slides.filter(s => s.layout === 'sales').map((s: any) => s.composition))], compiledSlides: compiled.slides.length, validationIssues: result.issues.length } };
}

const energyCfg = {
  slug: 'energy-infrastructure', title: 'Asteris Gridworks × Tideframe Coastal Systems', shortTitle: 'Coastal capacity, made useful', company: 'Tideframe Coastal Systems', partner: 'Asteris Gridworks', archetype: 'energy-operator', objective: 'Explore four fictional businesses where coastal infrastructure context and marine operating design could meet.', audienceDecision: 'Choose which fictional business path merits a bounded design conversation.', partnerRelevance: 'Asteris can convene infrastructure contexts; Tideframe can turn them into legible marine operating products.', sourceThesis: 'Asteris and Tideframe could test a portfolio of coastal infrastructure businesses without collapsing distinct customers or payment relationships.', companyDifference: 'Tideframe frames marine work as a service and operating layer, not only as a vessel or hardware sale.', combinationAdvantage: 'The combination joins infrastructure context with a marine-native workflow and leaves ownership choices explicit.', strategicUpside: 'A portfolio could grow from one scoped workflow into services, products, and flexible capacity without treating the first study as the ceiling.', unresolvedQuestions: ['Which fictional coastal context has the cleanest first boundary?', 'Which operating roles and payment relationships need explicit design?', 'What evidence would move a concept from hypothesis to a partner-approved pilot?'], pillars: ['Four distinct coastal businesses', 'Marine-native operating design', 'Ambition beyond the first study'], assetLabels: {},
  slideSpecs: (a: Author, assets: Asset[]) => {
    const [off,cargo,prod,float] = ['offshore-service','coastal-cargo','local-production','floating-power-compute'];
    a.sales({ key:'partner-context', kicker:'PARTNER RELEVANCE', title:'A coastal infrastructure portfolio, not a single project', composition:'partner-opportunity', opportunityIds:[off,cargo,prod,float], intro:'Asteris can open the context; Tideframe makes four different coastal jobs legible as businesses.', introBindings:bind(off,'partnerBenefit'), domains:[
      {heading:'Service exchange',body:'Offshore operators need a coordinated service window, not fragmented handoffs.',bodyBindings:bind(off,'salesCase.need','salesCase.alternative')},
      {heading:'Cargo network',body:'Urgent coastal loads can become a scheduled service, not a one-off charter.',bodyBindings:bind(cargo,'product')},
      {heading:'Capacity platform',body:'Flexible floating power and compute keeps the ownership and operating choices open.',bodyBindings:bind(float,'salesCase.ambition')},
    ], proof:[{heading:'Why this partner',body:'Infrastructure context and marine operating design are complementary, not interchangeable.',bodyBindings:bind(prod,'partnerBenefit')}], offer:'Start with one fictional operating context; preserve the larger portfolio as the strategic prize.', offerBindings:bind(off,'salesCase.entryPoint','salesCase.ambition') });
    a.sales({ key:'platform', kicker:'COMPANY ADVANTAGE', title:'Tideframe turns coastal complexity into an operating product', composition:'platform-architecture', banner:'Tideframe turns coastal complexity into a marine operating layer.', bannerBindings:bind(off,'salesCase.mechanism'), physical:[
      {heading:'Marine service',body:'Vessel and crew handoffs become interfaces.',visual:'offshore-service'},
      {heading:'Cargo flow',body:'Cutoffs and exceptions belong in the service.',visual:'coastal-cargo'},
      {heading:'Product layer',body:'Configuration stays explicit before production.',visual:'local-production'},
      {heading:'Floating capacity',body:'Power, compute, and site roles stay open.',visual:'floating-power-compute'},
    ], ownership:'Tideframe owns the workflow concept; Asteris helps define the operating context.', ownershipBindings:bind(float,'partnerBenefit'), software:'A shared service map connects demand, handoffs, and exception choices.', softwareBindings:bind(cargo,'salesCase.mechanism'), revenue:'Different customers and payment paths stay separate until the design is real.', revenueBindings:bind(prod,'salesCase.ambition'), demand:[{heading:'Customer jobs',body:'Operators, shippers, facilities, and site hosts each get a recognizable job.',bodyBindings:bind(cargo,'customer')},{heading:'Partner value',body:'Asteris gets a portfolio lens without promising one default architecture.',bodyBindings:bind(float,'partnerBenefit')}], takeaway:'Partner advantage: frame coastal businesses before choosing assets.', takeawayBindings:bind(off,'salesCase.outcome') });
    a.sales({ key:'portfolio', kicker:'THE BUSINESS SET', title:'Four businesses; four customer and payment relationships', composition:'opportunity-portfolio', opportunityIds:[off,cargo,prod,float], intro:'The portfolio is intentionally plural: each path has its own need, customer, mechanism, and commercial question.', introBindings:bind(off,'salesCase.ambition'), programs:[
      {opportunityId:off,heading:'Offshore service exchange',value:'Recurring service coordination for operators.',bindings:bind(off,'product','customer','salesCase.mechanism','salesCase.outcome'),asset:'offshore-service'},
      {opportunityId:cargo,heading:'Coastal cargo network',value:'Scheduled service for urgent loads.',bindings:bind(cargo,'product','customer','salesCase.mechanism','salesCase.outcome'),asset:'coastal-cargo'},
      {opportunityId:prod,heading:'Local production',value:'Configurable marine-energy modules.',bindings:bind(prod,'product','customer','salesCase.mechanism','salesCase.outcome'),asset:'local-production'},
      {opportunityId:float,heading:'Floating capacity',value:'Power-and-compute service concept.',bindings:bind(float,'product','customer','salesCase.mechanism','salesCase.outcome'),asset:'floating-power-compute'},
    ], connection:'A first workflow can be narrow while the strategic upside remains a family of coastal offers.', connectionBindings:bind(cargo,'partnerBenefit','salesCase.ambition') });
    a.sales({ key:'offshore-gap', kicker:'OFFSHORE SERVICE EXCHANGE', title:'Make the service window the product', composition:'customer-alternative', opportunityIds:[off], intro:'Offshore work loses time when a service need, vessel, berth, and crew are coordinated as separate conversations.', introBindings:bind(off,'salesCase.need'), alternatives:[
      {heading:'Fragmented handoffs',body:'Brokers, calls, and one-off schedules leave operators to assemble the operating window.',bodyBindings:bind(off,'salesCase.alternative')},
      {heading:'Coordinated window',body:'A shared window aligns constraints before the operator asks for a booking.',bodyBindings:bind(off,'product','customer','salesCase.mechanism','salesCase.outcome','partnerBenefit'),emphasis:true},
    ], jobs:'The customer job is simple: move from service need to a legible marine work plan.', jobsBindings:bind(off,'customer'), advantage:'Tideframe makes coordination itself the service, giving Asteris a repeatable wedge around coastal operating contexts.', advantageBindings:bind(off,'salesCase.mechanism','partnerBenefit'), basis:'Qualitative comparison only — fictional workflow framing; no measured time, cost, capacity, or performance claim.' });
    a.sales({ key:'cargo-mission', kicker:'TIME-SENSITIVE COASTAL CARGO', title:'Turn urgent coastal movement into a dependable service', composition:'mission-hero', opportunityIds:[cargo], asset:'coastal-cargo', need:'Manufacturers need urgent loads to move without waiting for a bespoke charter or taking a slow land detour.', needBindings:bind(cargo,'salesCase.need','salesCase.alternative'), benefits:[
      {heading:'A real service',body:'Scheduled marine capacity is packaged with cutoffs, handoffs, and exceptions.',headingBindings:bind(cargo,'product'),bodyBindings:bind(cargo,'salesCase.mechanism')},
      {heading:'A clear buyer',body:'Shippers and coastal depots can recognize the job and the service boundary.',headingBindings:bind(cargo,'customer'),bodyBindings:bind(cargo,'partnerBenefit')},
      {heading:'A larger lane model',body:'One fictional lane can become a repeatable network of coastal movements.',bodyBindings:bind(cargo,'salesCase.outcome','salesCase.ambition')},
    ], payoff:'First engagement: one lane and handling map. Ambition: a recurring coastal cargo network.', payoffBindings:bind(cargo,'salesCase.entryPoint','salesCase.ambition') });
    a.sales({ key:'production-value', kicker:'LOCAL PRODUCT PRODUCTION', title:'A local product path without pretending a factory exists', composition:'product-value', opportunityIds:[prod], asset:'local-production', mechanism:'Coastal facilities need adaptable marine-energy equipment; a configuration workflow can define the product before production.', mechanismBindings:bind(prod,'salesCase.need','salesCase.alternative','salesCase.mechanism'), benefits:[
      {heading:'Configurable product',body:'The module turns common interfaces into a product that local facilities can evaluate.',headingBindings:bind(prod,'product'),bodyBindings:bind(prod,'customer')},
      {heading:'Partner upside',body:'Local configuration stays close; Asteris can shape a repeatable family.',bodyBindings:bind(prod,'salesCase.outcome','partnerBenefit','salesCase.ambition')},
    ], proof:'Proof boundary: fictional schematic only; certification, factory capacity, readiness, and economics remain unresolved.' });
    a.sales({ key:'floating-integration', kicker:'FLOATING POWER + COMPUTE', title:'Keep flexible capacity architecture open', composition:'integrated-infrastructure', opportunityIds:[float], asset:'floating-power-compute', intro:'Some coastal sites need flexible capacity; the first choice is a service boundary, not a predetermined platform.', introBindings:bind(float,'salesCase.need','salesCase.alternative'), actions:[
      {heading:'Define the product',body:'Frame power and compute as a capacity service with a clear customer job.',headingBindings:bind(float,'product','customer'),bodyBindings:bind(float,'salesCase.mechanism')},
      {heading:'Separate the roles',body:'Site host, operator, and capacity buyer should not be collapsed into one payer.',bodyBindings:bind(float,'customer','partnerBenefit')},
      {heading:'Preserve the ambition',body:'A workshop can test one use case while leaving a family of floating services possible.',bodyBindings:bind(float,'salesCase.outcome','salesCase.ambition')},
    ], options:'Options remain open: service operator, hosted capacity, or a later co-development path.', optionsBindings:bind(float,'salesCase.ambition','partnerBenefit') });
    a.sales({ key:'network-choice', kicker:'PORTFOLIO LOGIC', title:'The same partner context can support different customer jobs', composition:'customer-alternative', opportunityIds:[off,cargo,prod,float], intro:'The portfolio wins only if each business keeps its own customer, payer, and operating promise.', introBindings:bind(cargo,'salesCase.need','salesCase.alternative'), alternatives:[
      {heading:'One generic platform',body:'A single label can hide distinct service, product, and capacity relationships.',bodyBindings:bind(float,'salesCase.alternative')},
      {heading:'Portfolio with edges',body:'Four authored propositions stay separate while sharing a coastal operating lens.',bodyBindings:bind(off,'salesCase.mechanism','salesCase.outcome','partnerBenefit'),emphasis:true},
    ], jobs:'The partner job is to choose a first edge without losing the portfolio logic.', jobsBindings:bind(cargo,'customer','product'), advantage:'Tideframe keeps business boundaries visible so Asteris can decide where context creates the most leverage.', advantageBindings:bind(prod,'partnerBenefit','salesCase.ambition'), basis:'Qualitative comparison only — a narrative design choice, not evidence of market preference.' });
    a.sales({ key:'service-scale', kicker:'FROM FIRST STUDY TO SERVICE BUSINESS', title:'Use a bounded study as a doorway, not the destination', composition:'product-value', opportunityIds:[off,cargo], asset:'offshore-service', mechanism:'A narrow workflow study exposes the handoffs that a recurring service would need to own.', mechanismBindings:bind(off,'salesCase.need','salesCase.mechanism'), benefits:[
      {heading:'Start credible',body:'One context gives the partner a place to ask questions, not end with a report.',headingBindings:bind(off,'customer'),bodyBindings:bind(off,'salesCase.alternative','salesCase.outcome')},
      {heading:'Compound the value',body:'The service window can outgrow the study; Asteris can choose the next adjacent path.',bodyBindings:bind(off,'salesCase.ambition', 'partnerBenefit')},
    ], proof:'Proof boundary: the study is a proposed entry point; no customer demand, launch date, or operational result is asserted.' });
    a.sales({ key:'close', kicker:'STRATEGIC INVITATION', title:'Choose the first coastal edge', composition:'strategic-close', opportunityIds:[off,cargo,prod,float], intro:'The portfolio is the prize; choose one boundary to define together.', introBindings:bind(off,'salesCase.ambition'), stakes:[
      {heading:'Partner value',body:'Asteris can test where infrastructure context becomes a service, product, or capacity offer.',headingBindings:bind(float,'partnerBenefit')},
      {heading:'Company difference',body:'Tideframe keeps marine operations, customer jobs, and payment relationships explicit.',bodyBindings:bind(off,'salesCase.mechanism','salesCase.outcome')},
      {heading:'Ambition',body:'A first study should open a recurring business path, not become the ceiling.',bodyBindings:bind(cargo,'salesCase.ambition')},
    ], asset:'floating-power-compute', invitation:'Invite one fictional context workshop: choose the edge, name the buyer, and test the next question.', invitationBindings:bind(off,'salesCase.entryPoint','partnerBenefit') });
  },
};

const industrialCfg = {
  slug: 'industrial-oem', title: 'Kestrel Forge × Tideframe Marine Systems', shortTitle: 'Industrial to marine utility', company: 'Tideframe Marine Systems', partner: 'Kestrel Forge', archetype: 'industrial', objective: 'Explore three fictional independent paths for industrial supply, licensed build, and distribution/service.', audienceDecision: 'Select one independent route for a bounded industrial design conversation.', partnerRelevance: 'Kestrel Forge can add industrial discipline and channels; Tideframe can supply marine-native product and service logic.', sourceThesis: 'Kestrel Forge and Tideframe could test three independent paths without forcing supply, license, and service into one blended transaction.', companyDifference: 'Tideframe starts from the marine customer job and carries the operating boundary through product, build, and service.', combinationAdvantage: 'Kestrel brings industrial repeatability; Tideframe brings marine-specific interfaces and lifecycle context.', strategicUpside: 'A first route can establish a platform for adjacent marine categories while preserving distinct contracts and channel roles.', unresolvedQuestions: ['Which route has the clearest fictional owner and payer?', 'What must remain controlled in a licensed build?', 'Which channel capability can support the first serviceable product?'], pillars: ['Three independent paths', 'Supply + build + service', 'A route before a roadmap'], assetLabels: {},
  slideSpecs: (a: Author, assets: Asset[]) => {
    const [supply,license,service] = ['supply-modules','build-license','distribution-service'];
    a.sales({ key:'partner-context', kicker:'PARTNER RELEVANCE', title:'Industrial reach can open three different marine businesses', composition:'partner-opportunity', opportunityIds:[supply,license,service], intro:'Kestrel brings industrial discipline and channels; Tideframe keeps each marine path commercially distinct.', introBindings:bind(supply,'partnerBenefit'), domains:[
      {heading:'Supply',body:'Repeatable modules give builders a clearer way to buy marine capability.',bodyBindings:bind(supply,'salesCase.need','salesCase.alternative')},
      {heading:'Build + license',body:'Regional manufacturers get a controlled path from design intent to local production.',bodyBindings:bind(license,'product','salesCase.mechanism')},
      {heading:'Distribution + service',body:'A product becomes more adoptable when commissioning and support have an owner.',bodyBindings:bind(service,'customer','partnerBenefit')},
    ], proof:[{heading:'Why this partner',body:'Industrial trust is useful only when the marine customer job remains visible.',bodyBindings:bind(supply,'partnerBenefit')}], offer:'Choose one route for a bounded design review; do not imply a bundled agreement.', offerBindings:bind(license,'salesCase.entryPoint','salesCase.ambition') });
    a.sales({ key:'industrial-advantage', kicker:'COMPANY ADVANTAGE', title:'Marine-native product logic survives the handoff to industry', composition:'platform-architecture', banner:'Tideframe keeps marine need visible as industry adds repeatability.', bannerBindings:bind(license,'salesCase.mechanism'), physical:[
      {heading:'Module',body:'A stable interface makes supply repeatable.',visual:'supply-modules'},
      {heading:'Build system',body:'Rules and gates travel with the license.',visual:'build-license'},
      {heading:'Service path',body:'Support roles remain visible after sale.',visual:'distribution-service'},
    ], ownership:'Explicit control: design intent, build rights, channel, service boundaries.', ownershipBindings:bind(license,'partnerBenefit'), software:'Configuration and support logic connect product choices to the marine job.', softwareBindings:bind(service,'salesCase.mechanism'), revenue:'Supply, license, and service are separate commercial paths with separate buyers.', revenueBindings:bind(supply,'salesCase.ambition'), demand:[{heading:'Industrial customer',body:'Builders, regional manufacturers, and operators have different jobs.',bodyBindings:bind(supply,'customer')},{heading:'Partner leverage',body:'Kestrel can select the route that matches its strongest capability.',bodyBindings:bind(service,'partnerBenefit')}], takeaway:'Route discipline: marine need first, industrial mechanism second.', takeawayBindings:bind(license,'salesCase.outcome') });
    a.sales({ key:'portfolio', kicker:'THE ROUTE SET', title:'Three independent paths from supply to service', composition:'opportunity-portfolio', opportunityIds:[supply,license,service], intro:'These are not stages of one deal. Each path has a distinct customer, payer, and operating promise.', introBindings:bind(supply,'salesCase.ambition'), programs:[
      {opportunityId:supply,heading:'Supply modules',value:'Repeatable component program for builders.',bindings:bind(supply,'product','customer','salesCase.mechanism','salesCase.outcome'),asset:'supply-modules'},
      {opportunityId:license,heading:'Build + license',value:'Controlled design system for regional makers.',bindings:bind(license,'product','customer','salesCase.mechanism','salesCase.outcome'),asset:'build-license'},
      {opportunityId:service,heading:'Distribution + service',value:'Channel route with lifecycle support.',bindings:bind(service,'product','customer','salesCase.mechanism','salesCase.outcome'),asset:'distribution-service'},
    ], connection:'A first route can prove a relationship without erasing the other two businesses.', connectionBindings:bind(service,'partnerBenefit','salesCase.ambition') });
    a.sales({ key:'supply-gap', kicker:'SUPPLY PATH', title:'Make the interface repeatable for the builder', composition:'customer-alternative', opportunityIds:[supply], intro:'Builders need marine modules that do not recreate integration risk on every platform.', introBindings:bind(supply,'salesCase.need'), alternatives:[
      {heading:'Disconnected sourcing',body:'Components arrive separately and the builder owns the hidden interface work.',bodyBindings:bind(supply,'salesCase.alternative')},
      {heading:'Module program',body:'A stable interface and configuration guide create a repeatable supply product.',bodyBindings:bind(supply,'product','customer','salesCase.mechanism','salesCase.outcome','partnerBenefit'),emphasis:true},
    ], jobs:'The customer job is to buy a module with a clear boundary, not a new integration project.', jobsBindings:bind(supply,'customer'), advantage:'Tideframe carries the marine interface into Kestrel’s industrial supply discipline.', advantageBindings:bind(supply,'partnerBenefit','salesCase.ambition'), basis:'Qualitative comparison only — fictional route framing, with no supplier or performance evidence.' });
    a.sales({ key:'license-value', kicker:'BUILD + LICENSE', title:'License a build system, not a black box', composition:'product-value', opportunityIds:[license], asset:'build-license', mechanism:'Regional builders need design intent, acceptance gates, and support together; a license package makes control explicit.', mechanismBindings:bind(license,'salesCase.need','salesCase.alternative','salesCase.mechanism'), benefits:[
      {heading:'A buildable offer',body:'The licensed product is a marine build system with a clear customer and boundary.',headingBindings:bind(license,'product'),bodyBindings:bind(license,'customer')},
      {heading:'A strategic route',body:'Regional makers reach local production; Kestrel extends reach with control points visible.',bodyBindings:bind(license,'salesCase.outcome','partnerBenefit','salesCase.ambition')},
    ], proof:'Proof boundary: fictional license architecture; terms, engineering validation, and regional approvals remain unresolved.' });
    a.sales({ key:'service-infrastructure', kicker:'DISTRIBUTION + SERVICE', title:'Put support inside the product promise', composition:'integrated-infrastructure', opportunityIds:[service], asset:'distribution-service', intro:'Operators need a local support path, so distribution, commissioning, spares, and service must be designed together.', introBindings:bind(service,'salesCase.need','salesCase.alternative'), actions:[
      {heading:'Name the buyer',body:'Operators buy a supported marine product, not only a unit on a list.',headingBindings:bind(service,'product','customer'),bodyBindings:bind(service,'salesCase.mechanism')},
      {heading:'Assign the channel',body:'Kestrel’s distributor context can anchor commissioning and after-sales roles.',bodyBindings:bind(service,'partnerBenefit')},
      {heading:'Make it recurring',body:'A service program turns adoption into a lifecycle relationship.',bodyBindings:bind(service,'salesCase.outcome','salesCase.ambition')},
    ], options:'Options remain open: resale only, trained service channel, or a fuller lifecycle program.', optionsBindings:bind(service,'salesCase.ambition','partnerBenefit') });
    a.sales({ key:'route-choice', kicker:'ROUTE DISCIPLINE', title:'Choose the route that fits the partner’s real capability', composition:'mission-hero', opportunityIds:[license], asset:'build-license', need:'Kestrel need not choose all three paths; start where industrial strength meets a clear buyer.', needBindings:bind(license,'salesCase.need','salesCase.alternative'), benefits:[
      {heading:'Supply when repeatability leads',body:'Choose a component boundary when builders need a dependable interface.',bodyBindings:bind(supply,'product','customer')},
      {heading:'License when reach leads',body:'Choose build rights when regional production is the partner’s advantage.',bodyBindings:bind(license,'salesCase.mechanism','salesCase.outcome')},
      {heading:'Service when channels lead',body:'Choose lifecycle support when operator trust is the differentiator.',bodyBindings:bind(service,'partnerBenefit','salesCase.ambition')},
    ], payoff:'Entry: route-selection workshop. Ambition: a repeatable marine category with the right owner.', payoffBindings:bind(license,'salesCase.entryPoint','salesCase.ambition') });
    a.sales({ key:'close', kicker:'STRATEGIC INVITATION', title:'Select one independent path', composition:'strategic-close', opportunityIds:[supply,license,service], intro:'Industrial reach is the prize; choose one route to define.', introBindings:bind(license,'salesCase.ambition'), stakes:[
      {heading:'Partner value',body:'Kestrel can test where its supply, manufacturing, or channel strength creates the cleanest leverage.',headingBindings:bind(service,'partnerBenefit')},
      {heading:'Company difference',body:'Tideframe keeps the marine customer job and operating boundary intact.',bodyBindings:bind(supply,'salesCase.mechanism','salesCase.outcome')},
      {heading:'Independent economics',body:'Each route preserves its own buyer, payer, and commercial logic.',bodyBindings:bind(license,'customer','partnerBenefit')},
    ], asset:'supply-modules', invitation:'Invite a fictional route session: choose the buyer, define the boundary, and name the next proof question.', invitationBindings:bind(license,'salesCase.entryPoint','partnerBenefit') });
  },
};

const researchCfg = {
  slug: 'research-network', title: 'Pelagic Research Assembly × Bluequill Oceanics', shortTitle: 'Observation as a service', company: 'Bluequill Oceanics', partner: 'Pelagic Research Assembly', archetype: 'strategic', objective: 'Explore one recurring fictional ocean-observation service for a research consortium.', audienceDecision: 'Decide whether a bounded observation-service design is worth convening.', partnerRelevance: 'The consortium can align research questions and governance; Bluequill can design a recurring operational handoff.', sourceThesis: 'Pelagic Research Assembly and Bluequill could make ocean observation a shared recurring service rather than a sequence of disconnected campaigns.', companyDifference: 'Bluequill treats collection, review, and delivery as one service contract around the researcher’s question.', combinationAdvantage: 'Consortium governance and marine service design together can make continuity useful without prescribing a single scientific program.', strategicUpside: 'A recurring observation layer could support many research questions while keeping scientific ownership with the consortium.', unresolvedQuestions: ['Which cadence and data product matter first?', 'What review protocol defines acceptable delivery?', 'How should shared-use governance and payment be separated?'], pillars: ['One recurring service', 'Continuity for research teams', 'Governance stays explicit'], assetLabels: {},
  slideSpecs: (a: Author, assets: Asset[]) => {
    const op = 'ocean-observation';
    a.sales({ key:'partner-context', kicker:'PARTNER RELEVANCE', title:'A consortium can make continuity a research capability', composition:'partner-opportunity', opportunityIds:[op], intro:'Pelagic Research Assembly brings shared questions and governance; Bluequill can shape the recurring service handoff.', introBindings:bind(op,'partnerBenefit'), domains:[
      {heading:'Research need',body:'Teams need observations on a dependable cadence, not a rebuilt campaign.',bodyBindings:bind(op,'salesCase.need','salesCase.alternative')},
      {heading:'Service design',body:'Collection, quality review, and data delivery become one recognizable product.',bodyBindings:bind(op,'product','salesCase.mechanism')},
    ], proof:[{heading:'Why this partner',body:'Shared governance protects scientific ownership while service logistics become repeatable.',bodyBindings:bind(op,'partnerBenefit')}], offer:'Start with one fictional cadence and review protocol; keep the wider observation layer as the ambition.', offerBindings:bind(op,'salesCase.entryPoint','salesCase.ambition') });
    a.sales({ key:'service-architecture', kicker:'COMPANY ADVANTAGE', title:'Continuity is the product, not a promise of scientific results', composition:'platform-architecture', banner:'Bluequill connects research questions to a recurring service handoff.', bannerBindings:bind(op,'salesCase.mechanism'), physical:[
      {heading:'Collection',body:'Scheduled marine work creates a repeatable input.',visual:'observation-service'},
      {heading:'Review',body:'Quality and acceptance are explicit service steps.',visual:'research-review'},
      {heading:'Delivery',body:'A shared data handoff supports many questions.',visual:'observation-network'},
    ], ownership:'Consortium owns research governance; Bluequill owns the service handoff.', ownershipBindings:bind(op,'partnerBenefit'), software:'A recurring data contract connects cadence, review, and delivery choices.', softwareBindings:bind(op,'salesCase.mechanism'), revenue:'One recurring service payer stays explicit; science is not a vague platform fee.', revenueBindings:bind(op,'customer'), demand:[{heading:'Research customer',body:'Teams buy dependable access to observations and a reusable handoff.',bodyBindings:bind(op,'customer','product')},{heading:'Partner upside',body:'A shared layer can support more questions without owning every research outcome.',bodyBindings:bind(op,'salesCase.ambition','partnerBenefit')}], takeaway:'The company difference is operational continuity with scientific boundaries intact.', takeawayBindings:bind(op,'salesCase.outcome') });
    a.sales({ key:'observation-mission', kicker:'RECURRING OBSERVATION', title:'Move from campaign logistics to a dependable service', composition:'mission-hero', opportunityIds:[op], asset:'observation-service', need:'Research teams need observations that arrive on a dependable cadence instead of being rebuilt as a campaign each time.', needBindings:bind(op,'salesCase.need','salesCase.alternative'), benefits:[
      {heading:'A complete service',body:'Scheduled collection, quality review, and shared delivery are designed together.',headingBindings:bind(op,'product'),bodyBindings:bind(op,'salesCase.mechanism')},
      {heading:'A research customer',body:'Consortium teams can plan around a service contract and a clear data handoff.',headingBindings:bind(op,'customer'),bodyBindings:bind(op,'salesCase.outcome')},
      {heading:'A shared layer',body:'The consortium gains continuity without giving up scientific ownership.',bodyBindings:bind(op,'partnerBenefit','salesCase.ambition')},
    ], payoff:'Entry: one cadence and review protocol. Ambition: a recurring observation layer.', payoffBindings:bind(op,'salesCase.entryPoint','salesCase.ambition') });
    a.sales({ key:'research-alternative', kicker:'CURRENT ALTERNATIVE', title:'The gap is continuity, not a lack of scientific questions', composition:'customer-alternative', opportunityIds:[op], intro:'The consortium already has questions; the service gap is the dependable operating rhythm around them.', introBindings:bind(op,'salesCase.need'), alternatives:[
      {heading:'Campaign by campaign',body:'Intermittent expeditions and heterogeneous datasets make continuity a manual coordination job.',bodyBindings:bind(op,'salesCase.alternative')},
      {heading:'Recurring observation',body:'A shared cadence and review contract make data access more predictable.',bodyBindings:bind(op,'product','customer','salesCase.mechanism','salesCase.outcome','partnerBenefit'),emphasis:true},
    ], jobs:'The researcher job is to plan inquiry around a trusted observation handoff.', jobsBindings:bind(op,'customer'), advantage:'Bluequill makes the service boundary explicit so consortium governance can focus on scientific priorities.', advantageBindings:bind(op,'partnerBenefit','salesCase.ambition'), basis:'Qualitative comparison only — fictional service framing; no scientific or operational performance claim.' });
    a.sales({ key:'governance', kicker:'INTEGRATED SERVICE DESIGN', title:'Keep governance and operations connected but distinct', composition:'integrated-infrastructure', opportunityIds:[op], asset:'research-review', intro:'A recurring service needs a clear handoff between consortium governance and marine operations.', introBindings:bind(op,'salesCase.need','salesCase.alternative'), actions:[
      {heading:'Set the cadence',body:'Define a recurring observation schedule around the research customer’s job.',headingBindings:bind(op,'product','customer'),bodyBindings:bind(op,'salesCase.mechanism')},
      {heading:'Set acceptance',body:'The review protocol defines delivery without claiming a scientific result.',bodyBindings:bind(op,'salesCase.outcome','partnerBenefit')},
      {heading:'Set the ambition',body:'One service design can become a shared layer for future questions.',bodyBindings:bind(op,'salesCase.ambition')},
    ], options:'Open choices: consortium-funded service, member subscription, or a staged shared-use model.', optionsBindings:bind(op,'salesCase.ambition','partnerBenefit') });
    a.sales({ key:'close', kicker:'STRATEGIC INVITATION', title:'Convene one observation-service design', composition:'strategic-close', opportunityIds:[op], intro:'Continuity is the prize; define one service boundary.', introBindings:bind(op,'salesCase.ambition'), stakes:[
      {heading:'Partner value',body:'The consortium can align cadence, review, governance, and shared use first.',headingBindings:bind(op,'partnerBenefit')},
      {heading:'Company difference',body:'Bluequill carries the operating handoff from collection through delivery.',bodyBindings:bind(op,'salesCase.mechanism','salesCase.outcome')},
      {heading:'Scientific boundary',body:'The service supports research questions; it does not promise results or replace ownership.',bodyBindings:bind(op,'customer','salesCase.ambition')},
    ], asset:'observation-network', invitation:'Invite a fictional design session: choose cadence, acceptance, and the next unresolved question.', invitationBindings:bind(op,'salesCase.entryPoint','partnerBenefit') });
  },
};

async function main() {
  const results = [];
  results.push(await buildConfig(energyCfg, opportunitiesForEnergy(), [
    {id:'offshore-service',label:'Offshore service exchange',accent:'#2dd4bf',motif:motifs.wave},
    {id:'coastal-cargo',label:'Coastal cargo network',accent:'#f59e0b',motif:motifs.network},
    {id:'local-production',label:'Local production module',accent:'#a78bfa',motif:motifs.module},
    {id:'floating-power-compute',label:'Floating power + compute',accent:'#38bdf8',motif:motifs.platform},
  ]));
  results.push(await buildConfig(industrialCfg, opportunitiesForIndustrial(), [
    {id:'supply-modules',label:'Modular marine supply',accent:'#fb7185',motif:motifs.module},
    {id:'build-license',label:'Build + license system',accent:'#fbbf24',motif:motifs.network},
    {id:'distribution-service',label:'Distribution + service',accent:'#34d399',motif:motifs.wave},
  ]));
  results.push(await buildConfig(researchCfg, opportunitiesForResearch(), [
    {id:'observation-service',label:'Recurring observation service',accent:'#60a5fa',motif:motifs.observation},
    {id:'research-review',label:'Research review protocol',accent:'#c084fc',motif:motifs.network},
    {id:'observation-network',label:'Shared observation network',accent:'#2dd4bf',motif:motifs.platform},
  ]));
  console.log(JSON.stringify(results.map(r => r.summary), null, 2));
}

if (import.meta.main) await main();
