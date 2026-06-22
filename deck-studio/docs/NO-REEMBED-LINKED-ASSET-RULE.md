# No-reembed linked-asset rule

Future deck runs must not paste or preserve images as inaccessible embedded-only blobs.

## Required path

1. Every final image role resolves to `deck-studio/assets/ASSET-REGISTRY.json`.
2. The registry entry must have either:
   - a stable `source_url` / Drive download URL that Slides can fetch, or
   - a checked-in `local_path` that is first published to the approved Drive/asset-host path, then recorded back as `source_url`.
3. The live deck update uses that stable URL for the image operation.
4. The deck manifest records the `registry_key`, `asset_path`, and `source_url`/publish status.

## Forbidden

- Do not reuse Google Slides `contentUrl` / `lh*-googleusercontent` URLs as canonical assets.
- Do not copy/paste a one-off binary into a deck with no registry entry.
- Do not mark a role complete if it is only visible inside an old live deck.

## Practical meaning

If a slide image is currently embedded-only, treat it as **blocked** until it is regenerated or checked into `deck-studio/assets/`, published to a stable linked URL, and registered. This avoids the Grab-cover failure mode where the visual exists but cannot be reliably reused or edited.
