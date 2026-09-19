# Native layout contract

`compileProject` emits one blank native Slides page per `Project.slides` item. The page is 720 × 405 pt and uses a dark editorial palette with Exo 2 text. Every slide includes a deterministic `createSlide`, page background, editable text boxes, native lines/shapes, and native images; no raster slide is created.

## Layouts

- **cover** — large visual field, editable company/partner marks when supplied, one title/subtitle/body and 1–3 pillars.
- **fit** — dominant product visual paired with company contribution, partner value and 2–3 benefits.
- **options** — 2–3 independent alternatives. A supplied visual is preferred; otherwise the renderer draws a clearly illustrative manufacture, hybrid or service schematic. Any transaction is a labelled **PROPOSED PAYMENTS** chain.
- **models** — exactly two ownership/payment models with product boundary, optional visual, payment actors and benefit.
- **channels** — scope/selection/criteria on the left, 1–2 channel mechanics and service terms on the right. It never invents a map, route or operating coverage.
- **missions** — a 2–4 image gallery. Four cards use a shorter title budget and smaller cards so passenger-transport-network-length titles remain readable in two lines.
- **close** — experience-led visual and 1–3 concrete conversations, ask and contact.

## Images and safety

URLs come from `options.assetUrls` first, then `Asset.embeddingUrl`. With `allowUnresolvedAssets`, unresolved URLs become `asset://<id>` and a warning is emitted; these placeholders are not valid for native apply. Native image placement preserves aspect ratio using CENTER_CROP for product fields and CENTER_INSIDE for logos and contained hardware references. Google Slides mints the image IDs; the native lifecycle rebinds them from a fresh snapshot.

Arbitrary explicit crop metadata is rejected rather than silently ignored. Use an archived crop derivative or a reviewed native edit for a custom crop. Noncentral focal points and protected regions produce review warnings; they are not automatically honored by CENTER_CROP. Inspect the actual rendered result. Use a provider-supported image format for native embedding: archive raster derivatives of SVG/WebP sources when the provider requires PNG/JPEG/GIF. Local validation of an SVG does not imply native-provider compatibility.

Text, payment arrows and source/claim/opportunity manifest notes remain editable or inspectable. IDs are deterministic, namespaced by project and slide key, and capped at 50 characters. Bounds warnings identify native elements that extend beyond the page; title and large-content budgets fail before request generation.
