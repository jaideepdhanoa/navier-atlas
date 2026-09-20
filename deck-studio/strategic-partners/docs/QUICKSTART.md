# V2.1 quickstart

Use this package for a partner-specific strategic sales deck, standalone or complementary to an investment deck. Standardize evidence, authoring, production and review—not the partner's story. Real partner work belongs outside this generic package.

## 1. Scaffold a held project

```sh
bun src/cli.ts init2.1 --out ../my-partner-project --partner "Example Vessel Company" --entity "Example Vessel Company Ltd"
```

Complete the required companion intake (which recipient holds which version) and `leverTransfer` assessment; do not fabricate missing claims or relationships. If starting from legacy 1.0.0/2.0.0, use `migrate`; it preserves data/assets and creates a held draft.

## 2. Write the argument and evidence

Complete `sales.brief`, source dispositions, opportunity sales cases and narrative. Record claim provenance, operating context, dependencies, quantities, price basis and applicability. Read [NUMBERS](NUMBERS.md): energy ratios require matched conditions or supported transfer, and total cost is not fuel saving. Use synthetic examples only in generic/public materials.

## 3. Author and review

Use direct `claimUses` and `quantityUses`; distinguish modeled, target, record, precedent and proposal. Use concise claim-linked qualifications (the V2.1 footnote band max is 240 characters at 8pt; fonts are not shrunk). Run two editorial rounds: proposition/support, then partner applicability/decision relevance. A number or asset name alone is not meaningful specificity.

```sh
bun src/cli.ts validate --project ../my-partner-project/project.json
bun src/cli.ts compile --project ../my-partner-project/project.json --out ../my-partner-project/build
```

The default 115-word body budget is advisory; character/layout limits still bind. Tests and validation are not persuasion, visual inspection or release approval.

## 4. Stage, inspect and release

Use an authorized native adapter for a fresh editable staging destination. Read back actual output, run render diagnostics, then inspect every full and phone page in native/PDF form. `inspected:false` and external release held are the safe defaults. Obtain human finished-deck and external-release receipts separately, with rights and recipient clearance.

## 5. Revise safely

Snapshot, hash, back up and patch only a review copy through the narrow allowlist. Preserve human edits and attachments. Do not unconditionally overwrite production; without atomic conditional revisions, hold promotion.
