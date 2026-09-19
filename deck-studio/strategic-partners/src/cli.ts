#!/usr/bin/env bun
import { initPackage, validatePackage, compilePackage, searchAssets, writeReviewTemplate, PackageError, cliUsage } from './package';
import type { ReviewReceipt } from './types';

function flag(args: string[], name: string, required = true): string | undefined {
  const index = args.indexOf(name);
  if (index < 0) { if (required) throw new PackageError(`Missing ${name}.\n\n${cliUsage()}`); return undefined; }
  const value = args[index + 1];
  if (!value || value.startsWith('--')) throw new PackageError(`Missing value for ${name}.`);
  return value;
}
function has(args: string[], name: string): boolean { return args.includes(name); }
function output(value: unknown): void { process.stdout.write(JSON.stringify(value, null, 2) + '\n'); }

async function main() {
  const args = process.argv.slice(2), command = args[0];
  if (!command || command === '--help' || command === '-h') { process.stdout.write(cliUsage() + '\n'); return; }
  if (command === 'init') {
    const result = await initPackage(flag(args, '--out')!, flag(args, '--partner')!, flag(args, '--entity')!);
    output({ status: 'HELD', message: 'Created an INCOMPLETE-INTAKE fictional scaffold. Replace demo data before production; it is not ready for a real partner.', project: result.projectPath, hold: result.holdPath });
    return;
  }
  if (command === 'validate') {
    const project = flag(args, '--project')!;
    const { result } = await validatePackage(project, has(args, '--public'));
    output(result);
    if (!result.ok) process.exitCode = 2;
    return;
  }
  if (command === 'compile') {
    const result = await compilePackage(flag(args, '--project')!, flag(args, '--out')!, flag(args, '--urls', false));
    output({ status: result.manifest.status, out: result.out, inputHash: result.manifest.inputHash, compiledHash: result.manifest.compiledHash, holds: result.manifest.holds });
    return;
  }
  if (command === 'assets') {
    const result = await searchAssets(flag(args, '--project')!, flag(args, '--query')!);
    output(result);
    return;
  }
  if (command === 'review-template') {
    const stage = flag(args, '--stage')! as ReviewReceipt['stage'];
    if (!['storyboard', 'comprehension', 'visual', 'release'].includes(stage)) throw new PackageError(`Unknown review stage ${stage}; use storyboard, comprehension, visual, or release.`);
    const project = flag(args, '--project')!, out = flag(args, '--out')!;
    const value = await writeReviewTemplate(project, stage, out);
    output({ status: 'HELD', path: `${out}/review-template.json`, stage: value.stage, decision: value.decision, message: 'Unsigned review template only; never an approval.' });
    return;
  }
  throw new PackageError(`Unknown command ${command}.\n\n${cliUsage()}`);
}

main().catch(error => { process.stdout.write(`ERROR: ${error instanceof Error ? error.message : String(error)}\n`); process.exitCode = 1; });
