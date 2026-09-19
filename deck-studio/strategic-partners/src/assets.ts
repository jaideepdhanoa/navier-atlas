import { createHash } from 'node:crypto';
import { readFile, realpath, stat } from 'node:fs/promises';
import { isAbsolute, relative, resolve, sep } from 'node:path';
import type { Asset, Audience, Project, ValidationIssue } from './types';

const MIME_TYPES = new Set(['image/png', 'image/jpeg', 'image/webp', 'image/gif', 'image/svg+xml']);

function hasPathEscape(value: string): boolean {
  if (!value || value.includes('\0') || /^[a-zA-Z][a-zA-Z0-9+.-]*:/.test(value)) return true;
  if (isAbsolute(value) || /^[/\\]/.test(value) || /^[a-zA-Z]:[\\/]/.test(value)) return true;
  const pieces = value.replaceAll('\\', '/').split('/');
  return pieces.includes('..');
}

function within(root: string, candidate: string): boolean {
  const rel = relative(root, candidate);
  return rel === '' || (rel !== '..' && !rel.startsWith(`..${sep}`) && !isAbsolute(rel));
}

function issue(code: string, path: string, message: string, severity: ValidationIssue['severity'] = 'error'): ValidationIssue {
  return { code, path, message, severity };
}

function imageInfo(bytes: Uint8Array): { mimeType?: string; width?: number; height?: number } {
  if (bytes.length >= 24 && bytes[0] === 0x89 && bytes[1] === 0x50 && bytes[2] === 0x4e && bytes[3] === 0x47) {
    const width = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength).getUint32(16);
    const height = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength).getUint32(20);
    return { mimeType: 'image/png', width, height };
  }
  if (bytes.length >= 10 && ((bytes[0] === 0x47 && bytes[1] === 0x49 && bytes[2] === 0x46 && bytes[3] === 0x38) || (bytes[0] === 0x47 && bytes[1] === 0x49 && bytes[2] === 0x46 && bytes[3] === 0x39))) {
    return { mimeType: 'image/gif', width: bytes[6] | (bytes[7] << 8), height: bytes[8] | (bytes[9] << 8) };
  }
  if (bytes.length >= 30 && bytes[0] === 0x52 && bytes[1] === 0x49 && bytes[2] === 0x46 && bytes[3] === 0x46 && bytes[8] === 0x57 && bytes[9] === 0x45 && bytes[10] === 0x42 && bytes[11] === 0x50) {
    if (bytes[12] === 0x56 && bytes[13] === 0x50 && bytes[14] === 0x38 && bytes[15] === 0x58 && bytes.length >= 30) {
      const u24le = (offset: number) => bytes[offset] | (bytes[offset + 1] << 8) | (bytes[offset + 2] << 16);
      return { mimeType: 'image/webp', width: 1 + u24le(24), height: 1 + u24le(27) };
    }
    return { mimeType: 'image/webp' };
  }
  if (bytes.length >= 3 && bytes[0] === 0xff && bytes[1] === 0xd8 && bytes[2] === 0xff) {
    let offset = 2;
    while (offset + 9 < bytes.length) {
      if (bytes[offset] !== 0xff) { offset++; continue; }
      const marker = bytes[offset + 1];
      if (marker === 0xd8 || marker === 0xd9) { offset += 2; continue; }
      const length = (bytes[offset + 2] << 8) | bytes[offset + 3];
      if (length < 2 || offset + length + 2 > bytes.length) break;
      if ((marker >= 0xc0 && marker <= 0xc3) || (marker >= 0xc5 && marker <= 0xc7) || (marker >= 0xc9 && marker <= 0xcb) || (marker >= 0xcd && marker <= 0xcf)) {
        return { mimeType: 'image/jpeg', height: (bytes[offset + 5] << 8) | bytes[offset + 6], width: (bytes[offset + 7] << 8) | bytes[offset + 8] };
      }
      offset += length + 2;
    }
    return { mimeType: 'image/jpeg' };
  }
  const text = new TextDecoder().decode(bytes.subarray(0, Math.min(bytes.length, 4096))).trimStart();
  if (/^<svg(?:\s|>)/i.test(text)) {
    const viewBox = text.match(/\bviewBox\s*=\s*["']\s*[-+\d.e]+\s+[-+\d.e]+\s+([\d.e]+)\s+([\d.e]+)\s*["']/i);
    const width = text.match(/\bwidth\s*=\s*["']\s*([\d.e]+)/i);
    const height = text.match(/\bheight\s*=\s*["']\s*([\d.e]+)/i);
    return { mimeType: 'image/svg+xml', width: Number(width?.[1] ?? viewBox?.[1]), height: Number(height?.[1] ?? viewBox?.[2]) };
  }
  return {};
}

export function findAssets(project: Project, query: { roles?: string[]; missions?: string[]; vessel?: string; geography?: string[]; audience?: Audience }): Asset[] {
  return project.assets.filter(asset => {
    if (query.roles?.length && !query.roles.some(role => asset.roles.includes(role))) return false;
    if (query.missions?.length && !query.missions.some(mission => asset.missions.includes(mission))) return false;
    if (query.vessel && asset.vessel !== query.vessel) return false;
    if (query.geography?.length && !query.geography.some(place => asset.geography.includes(place))) return false;
    if (query.audience && !asset.clearedFor.includes(query.audience)) return false;
    return true;
  });
}

export async function verifyAssetFiles(project: Project, projectRoot: string): Promise<ValidationIssue[]> {
  const issues: ValidationIssue[] = [];
  let root: string;
  try {
    root = await realpath(resolve(projectRoot));
    const rootStat = await stat(root);
    if (!rootStat.isDirectory()) return [issue('ASSET_ROOT_NOT_DIRECTORY', 'projectRoot', 'projectRoot must be a directory')];
  } catch {
    return [issue('ASSET_ROOT_MISSING', 'projectRoot', 'projectRoot does not exist')];
  }
  for (const asset of project.assets) {
    const path = `assets.${asset.id}.path`;
    if (hasPathEscape(asset.path)) {
      issues.push(issue('ASSET_PATH_UNSAFE', path, 'Asset path must be relative and cannot traverse or use a URL'));
      continue;
    }
    const candidate = resolve(root, asset.path);
    if (!within(root, candidate)) {
      issues.push(issue('ASSET_PATH_ESCAPE', path, 'Asset path resolves outside projectRoot'));
      continue;
    }
    let resolved: string;
    try {
      resolved = await realpath(candidate);
      if (!within(root, resolved)) {
        issues.push(issue('ASSET_SYMLINK_ESCAPE', path, 'Asset symlink resolves outside projectRoot'));
        continue;
      }
      const fileStat = await stat(resolved);
      if (!fileStat.isFile()) {
        issues.push(issue('ASSET_NOT_FILE', path, 'Asset path must point to a regular file'));
        continue;
      }
      const bytes = await readFile(resolved);
      const digest = createHash('sha256').update(bytes).digest('hex');
      if (digest.toLowerCase() !== asset.sha256.toLowerCase()) issues.push(issue('ASSET_HASH_MISMATCH', path, 'Asset SHA-256 does not match the archived file'));
      const info = imageInfo(bytes);
      if (!info.mimeType || !info.width || !info.height || info.width <= 0 || info.height <= 0) {
        issues.push(issue('ASSET_BINARY_INVALID', path, 'Asset is not a recognizable image with positive dimensions'));
      } else {
        if (asset.mimeType !== info.mimeType) issues.push(issue('ASSET_MIME_MISMATCH', path, `Asset metadata MIME ${asset.mimeType} does not match the file`));
        if (asset.width !== info.width || asset.height !== info.height) issues.push(issue('ASSET_DIMENSIONS_MISMATCH', path, 'Asset metadata dimensions do not match the file'));
      }
    } catch {
      issues.push(issue('ASSET_FILE_MISSING', path, 'Asset file is missing or unreadable'));
    }
  }
  return issues;
}

export function isPlausibleMime(mimeType: string): boolean { return MIME_TYPES.has(mimeType.toLowerCase()); }
export function isUnsafeAssetPath(path: string): boolean { return hasPathEscape(path); }
