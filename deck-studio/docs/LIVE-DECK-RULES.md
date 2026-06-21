# Live deck editing rules

## Allowed

- Use Google Slides API batch updates against the live presentation ID.
- Insert or replace text in known text ranges/objects.
- Replace an image object only when the edit plan references an approved image job and target object ID.
- Add a new slide only from an approved layout/master and record the new slide ID in the manifest immediately after applying.
- Export PDF/PNG previews for QA.

## Forbidden

- Do not download a presentation as PPTX, edit it locally, and upload it back.
- Do not replace an entire presentation file.
- Do not create duplicate decks unless the request explicitly says to create a sandbox copy.
- Do not hand-type route IDs, economics values, or market claims without a source pointer.
- Do not use Atlas-generated imagery as deck imagery.
- Do not use broad generated-asset replacement when a deterministic N30 composite is required.

## Object identity contract

The `slide-manifest.json` file is the safety rail. Every edit plan must declare:

- `presentation_id`
- `deck_key`
- target `slide_object_id`
- target element/object IDs when editing existing content
- exact Slides API requests to apply
- QA gates to run after apply

If an object ID is unknown, first run `python -m deck_studio pull --deck <deck> --mode full` and update the manifest. Null beats confidently-wrong.

## Human review gate

Grok may update internal/live drafts and generate final-ready exports, but final external sends remain human-reviewed unless Jaideep explicitly waives review for that specific deck/version.
