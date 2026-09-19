# Partner two-pager toolkit

A standalone, content-driven adaptation of the Navier HNI/Aramco two-page design. One `content.json` produces matching dark and light editions. This is **not** the Google Slides builder and does not modify a live deck or Atlas proposal.

The public example is fictional and contains no Navier revenue, technical performance, private partner evidence or negotiation terms. Real partner projects may remain private while using this public renderer.

## Requirements

- Bun 1.3+ and Bash.
- Playwright/Chromium (pinned dependency in `package.json`).
- Poppler: `pdfinfo`, `pdftotext`, `pdffonts`, `pdftoppm`.
- ImageMagick 7: `magick`.
- Linux Chromium libraries; the setup command can install them when authorized.

```bash
# From this toolkit directory; rerun after an ephemeral environment restarts.
bash scripts/setup.sh

# Start a new project; never overwrites an existing directory.
bash run.sh init acme "Acme Marine" /path/to/new-acme-project

# After replacing the illustrative content and assets:
bash run.sh build \
  --config /path/to/new-acme-project/content.json \
  --out /path/to/new-acme-project/exports
```

`run.sh` copies the small toolkit to temporary local storage and installs its pinned dependencies there. This avoids package-manager symlink and directory-rename limitations on cloud drives. Input/output paths are resolved from the caller's working directory. No API or account access is required. After dependencies are installed, rendering uses only local assets and blocks external page resources. Chromium downloads happen during setup, not during rendering. Set `CHROME_BIN` to use an existing compatible browser.

## The content contract

See [SKILL.md](SKILL.md), [content.schema.json](content.schema.json) and [examples/public-demo/content.json](examples/public-demo/content.json).

- `meta`: audience/classification, company/partner, date, title and contact.
- `sources`: stable IDs, title, locator, visibility and as-of date.
- `claims`: statement, evidence class, source IDs, basis and audience clearance.
- `assets`: local path, photograph/rendering/schematic type, provenance, visibility and review status.
- `cover`: product story, four image tiles, 3–6 traction chips and a three-stage product panel.
- `partnership`: contribution cards, three workstreams, partner value, concrete starts and the ask.
- `policy`: required phrases, forbidden regular expressions and a word budget.

Only `b`, `strong`, `em`, `i` and `br` markup is permitted in rich text. Other HTML is escaped. Asset paths must stay inside the project; symlink escape, remote images, active SVG content and source-destructive output paths are rejected. Per-tile `position` accepts bounded percentage pairs for deliberate crop control.

`public` / `public-example` projects cannot contain internal sources or assets, even unused ones. Restricted sources and uncleared claims are always rejected. A `shareable` flag is a recorded editorial decision, not automatic authorization from the renderer.

The policy scan runs on visible document text, not CSS or the source registry, avoiding false hits in words such as `background`. Required phrase checks tolerate PDF letterspacing. Author-facing word count comes from the rendered document; extracted PDF word counts may be higher because of letterspaced small capitals.

## Outputs and QA

- `*-dark.pdf`, `*-light.pdf`: exactly two Letter pages.
- Same-name self-contained HTML plus copied fonts/assets for editing/review.
- `*-1.png`, `*-2.png`: true PDF renders, not browser screenshots.
- `*-phone-1.png`, `*-phone-2.png`: 400-pixel QA previews.
- Extracted text, `source-content.json`, and `build-manifest.json` with hashes, geometry, font, source and parity checks.
- Existing output directories are copied to a timestamped backup before replacement. Source files and live company originals are not overwritten.

Open all four actual page renders and the phone previews before recording review:

```bash
bash run.sh review --out /path/to/project/exports \
  --reviewer "Reviewer name" \
  --notes "Inspected dark/light PDF pages and phone previews; note actual findings."
```

The receipt hashes the inspected PDFs and PNGs. It does not certify engineering performance, partner agreement, factual freshness or public release. Review does not replace human approval to send or publish. No byte-identical PDF promise is made across browser versions: PDF metadata timestamps can differ; source hashes and text/layout checks establish the reproducible basis.

## Tests and public research checks

```bash
bash run.sh test
bash run.sh schema                   # regenerate JSON Schema from the validated model
bash run.sh check-sources /path/to/sources.json /path/to/facts.json
bash run.sh build --config examples/public-demo/content.json --out /tmp/brief-demo
```

Tests cover source/claim/image binding, public/private separation, uncleared material, safe local paths, rich-text injection, crop syntax, disclosure patterns and exact dark/light content parity. Rendering itself rejects overflow, clipping, footer collisions, missing assets, wrong page counts, absent fonts and remote resources.

Research registers should preserve primary source URLs and dates. Negative-search notes are not primary citations; do not count a string containing two URLs as a single unique source. Private communications belong in a separate restricted dossier, never in a public source export.

## Saving and publishing

Use an explicit publication allowlist. The generic toolkit, fictional example and source-linked public research may be shared. Do not recursively upload a thread/project folder: it can include private content, archives, financing information, raw emails or confidential PDFs. See [PUBLICATION.md](PUBLICATION.md).

Repository homes: `deck-studio/two-pagers/` for this standalone lane; `reference/partners/<partner>/` for public research. Tasklet installation-specific pointers can live in `references/installation.md` without changing the portable toolkit. Keep existing route-one-pager and Slides workflows intact.

## Licensing

This addition does not choose a new open-source license. See [LICENSING.md](LICENSING.md) for the repository publication boundary and the separate font licenses.

## Provenance

Design language and layout vocabulary derive from the existing Navier HNI two-pager source: navy/gold, Playfair/Inter, four tiles, six chips and a product panel. The original source and audience copy are not included here. All fictional example graphics were authored for this package. Vendored Inter and Playfair Display fonts retain their names and SIL Open Font Licenses in `fonts/OFL-*.txt`; font bytes are unchanged from the approved offline design set.
