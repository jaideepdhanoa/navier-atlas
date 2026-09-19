import { describe, expect, test } from 'bun:test';
import { clone, compileFixture, v2Projects } from './v2-fixtures';
import { COMPOSITION_NAMES, resolveBlock, salesIssues } from '../src/authoring';
import { schemaIssues } from '../src/schema';
import type { Project } from '../src/types';

function strings(value: unknown, out: string[] = []): string[] {
  if (Array.isArray(value)) value.forEach(item => strings(item, out));
  else if (value && typeof value === 'object') Object.values(value).forEach(item => strings(item, out));
  else if (typeof value === 'string') out.push(value);
  return out;
}

function selectedAssetIds(project: Project): Set<string> {
  return new Set(project.slides.flatMap(slide => strings(slide).filter(value => project.assets.some(asset => asset.id === value))));
}

describe('V2 sales authoring, source preservation, and composition contracts', () => {
  test('all eight registered compositions render deterministically across the disk fixtures', async () => {
    const projects = await v2Projects();
    const seen = new Set<string>();
    for (const project of projects) {
      const first = compileFixture(project);
      const second = compileFixture(project);
      expect(first.requests).toEqual(second.requests);
      expect(first.inputHash).toBe(second.inputHash);
      for (const slide of project.slides) if (slide.layout === 'sales') {
        seen.add(slide.composition);
        expect((COMPOSITION_NAMES as readonly string[]).includes(slide.composition)).toBe(true);
        expect(first.slides.find(compiled => compiled.key === slide.key)?.copyBindings?.length).toBeGreaterThan(0);
      }
    }
    expect([...seen].sort()).toEqual([...COMPOSITION_NAMES].sort());
  });

  test('emitted sales copy retains authored text, opportunity bindings, and claim traceability', async () => {
    const project = (await v2Projects()).sort((a, b) => b.sales!.blocks.length - a.sales!.blocks.length)[0];
    const compiled = compileFixture(project);
    for (const slide of compiled.slides) for (const emission of slide.copyBindings ?? []) {
      const source = project.sales!.blocks.find(block => block.id === emission.blockId);
      expect(source, emission.blockId).toBeDefined();
      const resolved = resolveBlock(project, emission.blockId);
      expect(emission.text).toBe(resolved.text);
      expect(emission.claimIds).toEqual(resolved.claimIds);
      expect(emission.bindings).toEqual(resolved.bindings);
      expect(emission.placement).toBe(source!.placement);
      expect(emission.text.trim().length).toBeGreaterThan(0);
    }

    // Authored examples need not use automatic field references. Exercise that
    // optional contract explicitly, without making the fixture copy mechanical.
    const linked = clone(project);
    const linkedSlide = linked.slides.find(slide => slide.layout === 'sales' && slide.opportunityIds.length > 0)!;
    const fromBlock = linked.sales!.blocks.find(block => block.id === linkedSlide.title)!;
    delete fromBlock.text;
    fromBlock.from = { opportunityId: linkedSlide.opportunityIds[0], field: 'title' };
    const linkedCompiled = compileFixture(linked);
    const changed = clone(linked);
    changed.opportunities.find(item => item.id === fromBlock.from!.opportunityId)!.title = 'REFRESHED AUTHORING VALUE';
    const changedCompiled = compileFixture(changed);
    const oldEmission = linkedCompiled.slides.flatMap(slide => slide.copyBindings ?? []).find(emission => emission.blockId === fromBlock.id);
    const newEmission = changedCompiled.slides.flatMap(slide => slide.copyBindings ?? []).find(emission => emission.blockId === fromBlock.id);
    expect(oldEmission).toBeDefined();
    expect(newEmission).toBeDefined();
    expect(newEmission!.text).not.toBe(oldEmission!.text);
  });

  test('retained core source propositions need visible destinations and cannot disappear silently', async () => {
    const project = (await v2Projects()).find(value => value.sales!.sourceInventory.some(item => item.importance === 'core' && value.sales!.sourceDisposition.find(d => d.sourceItemId === item.id)?.action !== 'omit'))!;
    expect(salesIssues(project).filter(issue => issue.severity === 'error')).toEqual([]);
    const bad = clone(project);
    const item = bad.sales!.sourceInventory.find(value => value.importance === 'core' && bad.sales!.sourceDisposition.find(d => d.sourceItemId === value.id)?.action !== 'omit')!;
    const disposition = bad.sales!.sourceDisposition.find(value => value.sourceItemId === item.id)!;
    disposition.destinationBlockIds = [];
    const codes = new Set(salesIssues(bad).map(issue => issue.code));
    expect(codes.has('SOURCE_NOT_VISIBLE')).toBe(true);
    expect(codes.has('CORE_SOURCE_BURIED')).toBe(true);
  });

  test('visible block opportunity mismatch and unrendered authored copy are negative cases', async () => {
    const project = (await v2Projects()).find(value => value.slides.some(slide => slide.layout === 'sales' && slide.opportunityIds.length > 0))!;
    const bad = clone(project);
    const salesSlide = bad.slides.find(slide => slide.layout === 'sales' && slide.opportunityIds.length > 0)!;
    const candidate = bad.sales!.blocks.find(block => {
      const values = strings(salesSlide);
      return block.bindings.some(binding => values.includes(block.id) && salesSlide.opportunityIds.includes(binding.opportunityId));
    });
    expect(candidate).toBeDefined();
    const opportunityId = candidate!.bindings.find(binding => salesSlide.opportunityIds.includes(binding.opportunityId))!.opportunityId;
    salesSlide.opportunityIds = salesSlide.opportunityIds.filter(id => id !== opportunityId);
    expect(salesIssues(bad).some(issue => issue.code === 'BLOCK_OPPORTUNITY_MISMATCH' || issue.code === 'NARRATIVE_OPPORTUNITY_MISMATCH')).toBe(true);

    const unrendered = clone(project);
    const sourceBlock = unrendered.sales!.blocks.find(block => block.placement === 'core')!;
    unrendered.sales!.blocks.push({ ...sourceBlock, id: `${sourceBlock.id}_unrendered`, text: 'An authored proposition intentionally left without a destination.' });
    expect(salesIssues(unrendered).some(issue => issue.code === 'UNRENDERED_COPY')).toBe(true);
  });

  test('concept, readiness, demand evidence, and visible qualifiers are fail-closed', async () => {
    const project = (await v2Projects()).find(value => selectedAssetIds(value).has(value.assets.find(asset => asset.maturity === 'concept')?.id ?? ''))!;
    const conceptAsset = project.assets.find(asset => asset.maturity === 'concept' && selectedAssetIds(project).has(asset.id))!;
    const conceptBad = clone(project);
    const concept = conceptBad.assets.find(asset => asset.id === conceptAsset.id)!;
    concept.visualBrief!.architectureOptions = [];
    concept.visualBrief!.unresolvedChoices = [];
    expect(salesIssues(conceptBad).some(issue => issue.code === 'CONCEPT_ARCHITECTURE_CHOICES')).toBe(true);

    const readinessBad = clone(project) as any;
    delete readinessBad.opportunities[0].salesCase.readiness;
    expect(schemaIssues(readinessBad).some(issue => issue.code === 'SCHEMA_CONTRACT' && issue.message.includes('readiness'))).toBe(true);

    const demandBad = clone(project);
    demandBad.meta.fictional = false;
    demandBad.opportunities[0].salesCase!.demandStatus = 'partner-demand';
    demandBad.opportunities[0].claimIds = [];
    expect(salesIssues(demandBad).some(issue => issue.code === 'PARTNER_DEMAND_EVIDENCE')).toBe(true);

    const qualifierBad = clone(project);
    const compiled = compileFixture(qualifierBad);
    const emitted = compiled.slides.flatMap(slide => slide.copyBindings ?? []).find(item => item.claimIds.length > 0 && item.placement === 'core');
    expect(emitted).toBeDefined();
    const block = qualifierBad.sales!.blocks.find(item => item.id === emitted!.blockId)!;
    block.qualification = undefined;
    qualifierBad.claims.find(claim => emitted!.claimIds.includes(claim.id))!.evidenceClass = 'modeled';
    const path = `sales.blocks.${block.id}`;
    expect(salesIssues(qualifierBad).some(issue => issue.code === 'VISIBLE_QUALIFIER' && issue.path === path)).toBe(true);
    block.qualification = 'Confidential';
    expect(salesIssues(qualifierBad).some(issue => issue.code === 'VISIBLE_QUALIFIER' && issue.path === path)).toBe(true);
    block.qualification = 'Modeled illustrative assumption; not a measured result.';
    expect(salesIssues(qualifierBad).some(issue => issue.code === 'VISIBLE_QUALIFIER' && issue.path === path)).toBe(false);
  });

  test('status labels cannot substitute for the visible sales argument or a retained source idea', async () => {
    const project = clone((await v2Projects())[0]);
    const opportunity = project.opportunities[0];
    for (const block of project.sales!.blocks) {
      block.bindings = block.bindings.filter(binding => !(binding.opportunityId === opportunity.id && binding.field === 'salesCase.ambition'));
      if (block.from?.opportunityId === opportunity.id && block.from.field === 'salesCase.ambition') {
        block.text = opportunity.salesCase!.ambition;
        delete block.from;
      }
    }
    const slide = project.slides.find(value => value.layout === 'sales' && value.opportunityIds.includes(opportunity.id))!;
    if (slide.layout !== 'sales') throw new Error('Missing sales fixture');
    const status = project.sales!.blocks.find(block => block.id === slide.status)!;
    status.bindings.push({ opportunityId: opportunity.id, field: 'salesCase.ambition' });
    const retained = project.sales!.sourceInventory.find(item => item.importance === 'core')!;
    project.sales!.sourceDisposition.find(item => item.sourceItemId === retained.id)!.destinationBlockIds = [status.id];
    const issues = salesIssues(project);
    expect(issues.some(issue => issue.code === 'SALES_COPY_COVERAGE' && issue.path === `opportunities.${opportunity.id}.salesCase.ambition`)).toBe(true);
    expect(issues.some(issue => issue.code === 'CORE_SOURCE_BURIED')).toBe(true);
  });
});
