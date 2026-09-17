---
name: partner-two-pager
description: Research a strategic partner and create a source-linked Navier two-page brief using the existing design. Use for partner 2-pagers, adapting a company/Aramco-style brief, reusable partner research, or cross-agent brief tooling.
---

# Partner research → two-page brief

Use this for a standalone two-page strategic partner PDF. It is separate from the route-specific `partner-onepager` workflow and the Google Slides/Deck Studio lane. Do not rebuild the original company brief or a live deck in place.

## 1. Recover before researching or rebuilding

- Look for the latest approved company brief, earlier partner versions, existing source files, partner research and claim registers. The HNI two-pager source already exists; a missing Skill entry does not mean the source was lost.
- In the repository, start with `deck-studio/two-pagers/README.md` and `reference/partners/<partner>/`. In an installed shared-drive copy, read `references/installation.md` when present.
- Consult adjacent Skills when the request also changes routes, economics, landing plans or a full Slides deck. Do not invent geography or a second proposal/economics model in this PDF lane.

## 2. Establish the brief

Read the user-supplied materials. Briefly plan the audience, objective, company evidence, partner thesis and first ask. Separate private relationship evidence from public corporate research from the beginning.

Research the **correct legal/business entity**, strategy, actual marine capabilities, products, manufacturing and relevant channels. Existing partner capabilities matter as much as gaps. A dealer is not an operator; corporate presence is not marine presence; facilities are not available capacity; a product specification is not integration approval.

Save public URLs, titles, publication/access dates, source IDs, evidence classes and limitations. Facts link to source IDs. Count unique primary URLs separately from negative-search notes or multi-URL fields. Save private call/email chronology and unresolved questions in an appropriately restricted project, never the public research folder.

## 3. Use one source for both editions

Read [README.md](README.md), [the content schema](content.schema.json) and the [public example](examples/public-demo/content.json). Create a new project with `content.json` and its own approved `assets/`.

- **Page 1:** understandable company/product explanation; mission imagery; approved traction; delivered/demonstrated/development stages.
- **Page 2:** a partner-specific thesis; what each side contributes; three bounded workstreams; partner value and a concrete start for each; one clear ask.
- Preserve the approved visual language: navy, restrained gold, Inter body, Playfair headlines. Preserve grouping and voice where possible; cut words rather than shrinking everything.
- One authored content file produces dark and light PDFs. Never manually maintain two competing copy versions.
- A plain partner name is preferable to an invented or unverified logo. Do not carry another partner's names, images, geography, figures, terms or promises into the new brief.

## 4. Claims and disclosure

Every consequential claim needs a source, as-of date, evidence class and an audience decision. Distinguish measured, demonstrated, company-reported, preliminary, modeled, planned and proposed material. Keep ranges, speed/load/sea-state basis, capacity, revenue, signed program values and pipeline distinct.

Do not silently convert an unresolved measured-vs-modeled claim into a target. Resolve it, omit it, or ask the owner. A demonstration is not a complete performance qualification. Future classes and design renderings must remain visibly future/illustrative. The standard vessel ladder is N30/N45/N80/N180; use the current approved canon, not retired classes.

Keep financing terms, private communications and uncleared claims out of partner-forwardable material. The toolkit's disclosure patterns are configurable, not a complete confidential-data classifier. Approved company figures may be used for their intended audience without becoming approved for a public repository.

Images need exact provenance and review. N30 renders show one centered front foil and two widely separated rear foils; larger-class renders use four. Inspect full resolution. Do not alter a real photograph to reveal a naturally occluded strut. A schematic is not certification evidence.

## 5. Build and inspect

Use `bash run.sh` for a cloud-mounted installation; it stages dependencies on local storage. Follow the README setup and build commands. Keep live originals untouched and preserve source backups.

A successful build checks the schema, source/claim/image bindings, disclosure rules, missing images/fonts, page and text bounds, footer collisions, two Letter PDF pages, embedded fonts and identical dark/light text. It exports actual PDF page PNGs and 400-pixel phone previews.

**Open and inspect every dark/light PDF page render**, plus phone previews. Check wraps, image crops/provenance, foil geometry, contrast, section collisions and footers. Phone previews must communicate the headline, proof points and asks; dense body copy may require zoom. Do not call the entire two-pager readable unzoomed if it is not. Record the actual visual review with `run.sh review`; that command records an inspection, it does not perform one.

## 6. Save so another agent starts warm

Save the editable project, PDF/PNG outputs, source and claim registers, image provenance, build manifest, visual-review receipt, private relationship evidence and remaining decisions in versioned locations. Add a partner index linking public research and the restricted project without copying private contents into public files.

Shared installation: put this Skill/toolkit and public research on a shared drive. Keep sensitive dossiers at the approved access level. GitHub: publish only an explicit allowlist of generic tooling, public examples and public-source research. Read existing repository instructions and files before making a separate branch/PR; do not merge or change live sources unless requested. Public GitHub publication is a different audience decision from forwarding a confidential PDF to a partner.

## Done

A reviewed two-page brief, reproducible source, source/claim/image records, dark/light parity, clean configured scan, actual visual-review receipt, durable knowledge and discoverable Skill. State exactly what was saved or published and any remaining approval gate. No external sending is implied by creation.
