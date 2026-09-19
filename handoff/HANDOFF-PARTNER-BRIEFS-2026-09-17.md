# Handoff — standalone partner briefs and public research

17 September 2026

## Added

- `deck-studio/two-pagers/partner-two-pager/`: content-driven two-page PDF toolkit, portable Skill, content schema, offline fonts with licenses, authored fictional example, safety checks, tests and documentation.
- `deck-studio/docs/TWO-PAGER-BUILD-RULES.md`: standalone brief contract.
- `reference/partners/yamaha/`: public-source Yamaha Motor facts and citation library.
- Index links from the repository and Deck Studio READMEs and `reference/partners/README.md`.

## Workflow

One project `content.json` drives dark and light editions. Build checks page count, Letter size, font embedding, assets, geometry, source/claim bindings, audience restrictions and copy parity. It exports actual PDF page renders and phone previews. A separate review receipt records the author's visual inspection; it does not perform that inspection or authorize distribution.

The generic fixture and source checks passed locally before this change was proposed. No live slide IDs, Atlas routes, economics, production data or deployment files are changed. No merge or deployment is included.

## Publication boundary

Only generic tooling, a fictional public example and public-source research are included. Private communications, relationship context, confidential partner content/config and rendered partner PDFs remain outside the repository. This change introduces no new open-source license; see the toolkit's `LICENSING.md`.
