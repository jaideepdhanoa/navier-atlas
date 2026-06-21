# Workflows

## 1. No-op deck replay

Use this to prove Grok can operate independently before making edits.

```bash
python -m deck_studio validate --root .
python -m deck_studio pull --root . --deck french-polynesia --mode summary
python -m deck_studio pull --root . --deck careem --mode summary
python -m deck_studio pull --root . --deck grab --mode summary
python -m deck_studio qa --root . --deck french-polynesia
python -m deck_studio qa --root . --deck careem
python -m deck_studio qa --root . --deck grab
```

Acceptance: schema validation passes, live slide counts match manifests, and no write operations are generated.

## 2. Text edit

1. Create a request markdown file under `requests/`.
2. Run `plan` to produce an edit plan.
3. Manually inspect the plan.
4. Run `apply`.
5. Run `qa` and export previews.
6. Commit the plan and QA receipt.

## 3. Image generation/composite

```bash
python -m deck_studio image-plan --root . --deck careem --slide-object-id <slide_id> --out out/careem-image-job.json
python builders/images/n30_composite.py --background assets/backgrounds/<market>.png --vessel assets/n30/n30.png --out out/careem-composite.png
python -m deck_studio apply --root . --deck careem --plan out/careem-apply-image-plan.json
python -m deck_studio qa --root . --deck careem
```

## 4. New deck creation

1. Create `decks/<new-deck>/deck.config.json`.
2. Create `content-source.json` from partner proposal/economics sources.
3. Create a draft slide structure with `slide-manifest.json` using generated local IDs.
4. Create the Google Slides presentation and write the returned ID into `deck.config.json`.
5. Apply content via Slides API only.
6. Generate/render QA receipts.

## 5. Final review/export

- Produce PDF and PNG previews.
- Diff against previous renders if available.
- Confirm claim/economics pointers.
- Post internal Slack status if requested.
- Keep external sends as drafts for human review.
