import { cp, mkdtemp, readdir, readFile, writeFile } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';
import type { CompiledDeck, DeckSnapshot, ElementSnapshot, Project } from '../src/types';
import { EMU } from '../src/primitives';
import { compileProject } from '../src/render';

export const repoRoot = resolve(dirname(import.meta.path), '..');

export async function diskProjects(): Promise<Project[]> {
  const examples = await readdir(join(repoRoot, 'examples'), { withFileTypes: true });
  const projects: Project[] = [];
  for (const entry of examples.filter(e => e.isDirectory())) {
    try {
      const path = join(repoRoot, 'examples', entry.name, 'project.json');
      const value = JSON.parse(await readFile(path, 'utf8')) as Project;
      projects.push(value);
    } catch {
      // The examples directory may contain non-project material in future revisions.
    }
  }
  return projects;
}

export async function v2Projects(): Promise<Project[]> {
  return (await diskProjects()).filter(project => project.schemaVersion === '2.0.0');
}

export function clone<T>(value: T): T { return structuredClone(value); }
export function compileFixture(project: Project): CompiledDeck {
  const urls = Object.fromEntries(project.assets.map(asset => [asset.id, `https://assets.invalid/${asset.path.split('/').pop()}`]));
  return compileProject(project, { assetUrls: urls });
}

const emu = (points: number) => ({ magnitude: points * EMU, unit: 'EMU' as const });
const transform = (box: { x: number; y: number; w: number; h: number }) => ({
  scaleX: 1, scaleY: 1, shearX: 0, shearY: 0,
  translateX: box.x * EMU, translateY: box.y * EMU, unit: 'EMU' as const,
});
const textRuns = (text: string) => ({ textElements: text ? [{ textRun: { content: text } }] : [] });

/** A deterministic provider-shaped snapshot used only to exercise readback/binding checks. */
export function nativeSnapshot(compiled: CompiledDeck): DeckSnapshot {
  return {
    presentationId: `fixture-native-${compiled.projectId}`,
    title: 'Fictional native review fixture',
    pageSize: { width: emu(720), height: emu(405) },
    slides: compiled.slides.map((slide, index) => ({
      objectId: slide.objectId,
      index,
      pageElements: slide.elements.map(element => {
        const box = slide.boxes.find(candidate => candidate.objectId === element.objectId);
        if (!box) throw new Error(`Fixture compiler element has no box: ${element.objectId}`);
        if (element.kind === 'image') {
          const tag = `__SP_IMAGE_${element.objectId}__`;
          const request = slide.requests.find(item => item.replaceAllShapesWithImage?.containsText?.text === tag);
          return {
            objectId: element.objectId,
            size: { width: emu(box.w), height: emu(box.h) },
            transform: transform(box),
            image: { sourceUrl: request?.replaceAllShapesWithImage?.imageUrl },
          } satisfies ElementSnapshot;
        }
        return {
          objectId: element.objectId,
          size: { width: emu(Math.max(box.w, 1)), height: emu(Math.max(box.h, 1)) },
          transform: transform(box),
          shape: { shapeType: 'TEXT_BOX', text: textRuns(box.text ?? '') },
        } satisfies ElementSnapshot;
      }),
    })),
  };
}

/** Create a real, text-bearing PDF with one page per compiled slide for pdftotext/pdfinfo checks. */
export async function writeActualPdf(compiled: CompiledDeck, pdfPath: string): Promise<void> {
  const payloadPath = `${pdfPath}.visible.json`;
  await writeFile(payloadPath, JSON.stringify(compiled.slides.map(slide => slide.visibleText.map(value => value.replace(/\r?\n/g, ' ')))));
  const script = String.raw`import json, sys
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('FixtureSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pages = json.load(open(sys.argv[1]))
c = canvas.Canvas(sys.argv[2], pagesize=(720, 405))
c.setFont('FixtureSans', 4)
for page in pages:
    text = c.beginText(1, 400)
    text.setLeading(9)
    for value in page:
        text.textLine(value.replace('\n', ' '))
    c.drawText(text)
    c.showPage()
c.save()
`;
  const process = Bun.spawn(['python3', '-c', script, payloadPath, pdfPath], { stdout: 'pipe', stderr: 'pipe' });
  const [stderr, code] = await Promise.all([new Response(process.stderr).text(), process.exited]);
  if (code !== 0) throw new Error(`PDF fixture generation failed: ${stderr}`);
}

export async function copyProjectFixture(project: Project, sourceDir: string, destinationRoot: string): Promise<string> {
  await cp(sourceDir, destinationRoot, { recursive: true });
  return join(destinationRoot, 'project.json');
}

export async function tempDir(prefix: string): Promise<string> {
  return mkdtemp(join('/tmp', `strategic-v2-${prefix}-`));
}
