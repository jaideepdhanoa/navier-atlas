# Strategic-partner deck content contract

The validator checks the neutral content model in `src/types.ts`. Rendering and native presentation handling are separate modules; validation does not claim comprehension or visual review. A passing validator is a release gate input, not a substitute for editorial, comprehension, rights, or PDF/phone inspection.

## Data and evidence

Every source has an ID, title, locator, visibility, and real `YYYY-MM-DD` as-of date. Public source locators must be HTTP(S). Claims point to one or more sources, state an evidence class, and include a plain-language `basis`. A claim and asset must list the audiences for which it is cleared. Opportunities must name the product, customer, payer, commercial logic, both parties' contributions/benefits, and the next question. This keeps supply, manufacture, license, direct sale, resale, service, and operator-program ideas distinct rather than implying one bundled commitment.

Quantitative visible copy is checked conservatively: the slide must cite a claim and that claim must have a basis. The heuristic intentionally cannot decide whether a number is materially accurate. Editorial review still owns units, limitations, calculations, and claim-to-copy mapping.

## Audience and privacy

`internal`, `partner`, and `public` are separate audiences. Partner/public references must be cleared for the corresponding audience. Public validation/publication rejects non-public sources and assets even when unused and requires public clearance for claims. Internal logo omission is allowed only as a `release-hold`; a partner/public artifact requires both logo asset IDs. Partner-facing use of private source material emits an editorial-check warning: private locators must not be copied into notes or visible output automatically.

Do not treat `nativeSource` or `embeddingUrl` as an archived asset. Local assets need a relative path, rights note, caption, SHA-256, positive dimensions, supported image MIME, and audience clearance. With `checkFiles`, the validator additionally verifies file existence, symlink containment under `projectRoot`, binary MIME/dimensions, and SHA-256. Concept assets need a visible `concept`, `illustrative`, `notional`, or `proposed` caption. A photograph must be actual/demonstrated and may not be described as newly generated.

## Slides and copy discipline

A deck starts with `cover` and ends with `close`; the middle is intentionally variable. Layout counts are contractual: cover pillars 1–3, fit benefits 2–3, options 2–3, models exactly 2, channels 1–2, missions 2–4, close conversations 1–3. Main titles are capped at approximately 95 characters. Payment arrows are represented by explicit `Transaction` objects with actors, labels, and `kind: "payment"`.

The validator rejects retired `N120`, policy-forbidden terms, other-partner leakage, unknown references, unsafe IDs, unsupported strong readiness claims, malformed crops, and missing business/evidence fields. It does not require a market selection: a hypothesis can remain geography-neutral, provided proposed work is labeled as proposed and the next question is explicit. Avoid unsupported launch dates, capacity, approval, or delivery promises.

## Required human checks before release

1. Read visible copy without notes and explain why the partner cares, every product/payment relationship, and the next ask.
2. Check that all claims, captions, rights, and private-source handling are editorially cleared for the stated audience.
3. Render every slide, inspect dividers, crops, text wrapping, payment directions, and logos at full size and on a phone.
4. Preserve the source project, build/replay inputs, native backup, live IDs, source map, and separate comprehension and visual-review receipts.
