#!/usr/bin/env bun
import { readFile, writeFile } from 'node:fs/promises';
import { buildRegistry, registryHtml, registryMarkdown, reuseReport, searchRegistry, summarizeRegistry, type AssetRegistry, type RegistryQuery, type RightsStatus } from './registry';
import type { Audience, Asset } from './types';

function usage(): string {
  return `Local asset registry (offline; never publishes or changes source projects)

Build:
  bun src/registry-cli.ts build --project ./project-a/project.json --project ./project-b/project.json --out ./registry.json

Search:
  bun src/registry-cli.ts search --registry ./registry.json --mission passenger --role hero --clearance partner
  bun src/registry-cli.ts shortlist --registry ./registry.json --maturity actual --rights held --limit 12 --out ./shortlist.html

Reports:
  bun src/registry-cli.ts report --registry ./registry.json
  bun src/registry-cli.ts contact-sheet --registry ./registry.json --out ./shortlist.md --format markdown

Filters may be repeated: --mission, --vessel, --geography, --role, --maturity, --clearance,
--rights, --project-id, and --logical-id. Values are case-insensitive; matching is substring
matching for descriptive tags. Contact sheets contain local relative thumbnails only. No network fetch occurs.`;
}

function values(args: string[], name: string): string[] {
  const result: string[] = [];
  for (let i = 0; i < args.length; i++) if (args[i] === name) {
    const value = args[i + 1];
    if (!value || value.startsWith('--')) throw new Error(`Missing value for ${name}.`);
    result.push(value);
    i++;
  }
  return result;
}
function one(args: string[], name: string): string | undefined { return values(args, name)[0]; }
function required(args: string[], name: string): string { const value = one(args, name); if (!value) throw new Error(`Missing ${name}.`); return value; }
function json(value: unknown): void { process.stdout.write(JSON.stringify(value, null, 2) + '\n'); }
function numberFlag(args: string[], name: string, fallback: number): number { const value = one(args, name); if (!value) return fallback; const n = Number(value); if (!Number.isInteger(n) || n < 1) throw new Error(`${name} must be a positive integer.`); return n; }
function splitValues(args: string[], name: string): string[] { return values(args, name).flatMap(value => value.split(',').map(item => item.trim()).filter(Boolean)); }
function enumList<T extends string>(args: string[], name: string, allowed: readonly T[]): T[] | undefined {
  const list = splitValues(args, name);
  if (!list.length) return undefined;
  const unknown = list.filter(item => !allowed.includes(item as T));
  if (unknown.length) throw new Error(`Invalid ${name}: ${unknown.join(', ')}.`);
  return list as T[];
}
function queryFrom(args: string[]): RegistryQuery {
  const maturity = enumList(args, '--maturity', ['actual', 'demonstrated', 'concept', 'context', 'brand'] as const);
  const clearance = enumList(args, '--clearance', ['internal', 'partner', 'public'] as const);
  const rights = enumList(args, '--rights', ['cleared', 'held', 'unknown'] as const);
  const mission = splitValues(args, '--mission');
  const geography = splitValues(args, '--geography');
  const role = splitValues(args, '--role');
  const projectId = splitValues(args, '--project-id');
  const logicalId = splitValues(args, '--logical-id');
  return {
    ...(mission.length ? { missions: mission } : {}), ...(one(args, '--vessel') ? { vessel: one(args, '--vessel') } : {}),
    ...(geography.length ? { geography } : {}), ...(role.length ? { roles: role } : {}), ...(maturity ? { maturity } : {}),
    ...(clearance ? { clearance: clearance as Audience[] } : {}), ...(rights ? { rights: rights as RightsStatus[] } : {}),
    ...(projectId.length ? { projectId } : {}), ...(logicalId.length ? { logicalId } : {}),
    ...(one(args, '--hash') ? { exactVersionHash: one(args, '--hash') } : {}),
  };
}
async function loadRegistry(path: string): Promise<AssetRegistry> { return JSON.parse(await readFile(path, 'utf8')) as AssetRegistry; }
async function writeContact(registry: AssetRegistry, args: string[], records = registry.assets): Promise<string> {
  const out = required(args, '--out');
  const format = one(args, '--format') ?? (out.toLowerCase().endsWith('.md') || out.toLowerCase().endsWith('.markdown') ? 'markdown' : 'html');
  if (format !== 'html' && format !== 'markdown') throw new Error('--format must be html or markdown.');
  await writeFile(out, format === 'markdown' ? registryMarkdown(registry, records, out) : registryHtml(registry, records, out));
  return out;
}

async function main(): Promise<void> {
  const args = process.argv.slice(2), command = args[0];
  if (!command || command === '--help' || command === '-h') { process.stdout.write(usage() + '\n'); return; }
  if (command === 'build') {
    const projects = values(args, '--project').concat(values(args, '--projects').flatMap(value => value.split(',').map(item => item.trim()).filter(Boolean)));
    if (!projects.length) throw new Error('At least one --project is required.');
    const registry = await buildRegistry(projects);
    const out = required(args, '--out');
    await writeFile(out, JSON.stringify(registry, null, 2) + '\n');
    json({ status: 'OK', out, ...summarizeRegistry(registry) });
    return;
  }
  if (command === 'report') {
    const registry = await loadRegistry(required(args, '--registry'));
    json({ ...summarizeRegistry(registry), reuse: reuseReport(registry), collisions: registry.collisions });
    return;
  }
  if (command === 'search' || command === 'shortlist' || command === 'contact-sheet') {
    const registry = await loadRegistry(required(args, '--registry'));
    const result = searchRegistry(registry, queryFrom(args));
    const limit = numberFlag(args, '--limit', command === 'shortlist' || command === 'contact-sheet' ? 24 : Number.MAX_SAFE_INTEGER);
    const matches = result.matches.slice(0, limit);
    if (command === 'contact-sheet' || one(args, '--out')) {
      const out = await writeContact(registry, args, matches);
      json({ status: 'OK', out, count: matches.length, matched: result.count });
    } else {
      json({ count: result.count, matches });
    }
    return;
  }
  throw new Error(`Unknown command ${command}.\n\n${usage()}`);
}

main().catch(error => { process.stderr.write(`ERROR: ${error instanceof Error ? error.message : String(error)}\n`); process.exitCode = 1; });
