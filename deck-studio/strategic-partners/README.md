# Strategic-partner deck package (V2.1)

A partner-neutral, local-first kit for source-linked strategic-partner proposals. It preserves editable native output and staged lifecycle while adding structured evidence, applicability, recipient-specific continuity, safe talk tracks and render diagnostics. It is not a partner template and contains no private dossiers, credentials, live IDs or confidential imagery.

## What V2.1 supports

- **Sales argument:** `sales.brief`, source dispositions, opportunity sales cases and narrative make the partner decision, Navier difference, connected businesses, strategic upside and invitation explicit.
- **Structured evidence:** used claims carry topic, provenance, operating context, dependencies, quantities, applicability and (when relevant) price basis. Measured proof, records, precedents, models, targets and proposals retain distinct meaning.
- **Traceable visible authoring:** `claimUses` and `quantityUses` bind the visible framing and exact display. Claim-linked footnotes are optional, audience-safe and limited to 240 characters per slide.
- **Continuity:** `sales.brief.companions` records recipient-held versions and a disposition for each consequential prior claim. Corrections need a replacement claim and basis; unresolved contradictions hold the affected recipient release.
- **Safe notes:** a reviewed `TalkTrack` exports a concise say/basis/guardrail/Q&A record. Full evidence is emitted separately as a restricted manifest.
- **Diagnostics:** density counts, bound numeral comparisons and actual native/PDF geometry checks are diagnostics, not approvals or proof of factual truth.

## Operational path

1. Work in a restricted project. Recover approved evidence and recipient-specific prior materials.
2. Run `init2.1` (or migrate and complete the held draft); complete companions and lever-transfer intake before external work.
3. Author the brief, source inventory, sales cases, narrative, direct claim uses, applicability and audience clearances. Read [NUMBERS](docs/NUMBERS.md).
4. Run two editorial passes, then validate and compile. The default body budget is 115 words as an advisory diagnostic unless a composition policy overrides it; character/layout limits still bind.
5. Stage through an authorized native adapter, read back, run render diagnostics, and inspect actual full/phone native and PDF pages. Obtain human finished-deck and external-release decisions separately.
6. Revise only through the narrow, backed-up review-copy workflow. Promotion is fail-closed without atomic conditional revisions.

## Setup and verification

Use Bun and the checked-in dependency lockfile. For a cloud-mounted installation, copy the generic package to a local working directory before installing dependencies; keep real project inputs outside it.

```sh
bun install --frozen-lockfile
bun run typecheck
bun test tests
```

`private: true` in `package.json` prevents accidental npm publication; it does not prohibit sharing this reviewed generic source in a repository. Keep dependencies, generated output and restricted partner projects out of the generic source tree.

## CLI

```sh
bun src/cli.ts init2.1 --out ./my-intake --partner "Example Vessel Company" --entity "Example Vessel Company Ltd"
bun src/cli.ts validate --project ./examples/research-network/project.json [--public]
bun src/cli.ts migrate --project ./v1-project.json --out ./held-v2-draft
bun src/cli.ts compile --project ./examples/research-network/project.json --out ./build-demo
bun src/cli.ts render-review --project ./project.json --compiled ./build/compiled.json --snapshot ./native-after.json --pdf ./deck.pdf --out ./render-review
```

`validate` and `compile` do not certify persuasion, visual quality, rights, truth or release. `render-review` begins with `inspected:false` and `externalRelease:'held'`. Legacy 1.0.0/2.0.0 inputs remain readable; migration preserves data/assets and creates a held draft without inventing evidence or approvals.
