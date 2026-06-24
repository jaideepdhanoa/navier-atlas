# Navier deck brand rules

## Visual language

- Premium, quiet, technical, direct.
- Minimal gold accents; gold highlights should guide the eye, not decorate the slide.
- Use market-specific backgrounds and context imagery.
- Favor negative space, crisp typography, and simple claims.
- Use N30/N35 vessel imagery consistently and realistically.

## Typography and color

The canonical values should be resolved from the existing deck masters when possible. Until the masters are programmatically pulled, use these repo defaults as lint guidance:

- Dark background: `#050505` to `#111111`
- Primary text: `#FFFFFF` / high contrast
- Secondary text: muted gray, never low-contrast
- Accent gold: minimal; no broad gold fills
- Avoid heavy gradients, decorative borders, and dense text blocks

## Partner-facing copy (no internal taxonomy)

- Everything a partner *reads* — titles, subtitles, eyebrows, KPI/ladder captions, route
  descriptors, CTAs — must be **plain, compelling, partner-facing English**.
- **Banned from rendered slide text:** SOM/SAM/TAM/GMV, "captive resort mesh", "grounded",
  "network width", "sealed leeward geometry", "amber-dashed", "scale vision", "N% capture",
  "X-rung captive frame", vessel codenames (e.g. Quanta-LR), "on these lanes". These stay in
  the model / `kpi_frame` / render directives / provenance only.
- Builders must map model labels to display captions — never f-string a finance `meaning`
  straight onto a slide. Full rule + translation table + lint gate: **`PARTNER-COPY-RULES.md`**.
- Hard gate before any seal/apply: `python3 deck-studio/qa/partner_copy_lint.py <deck>` must be green.

## Claim style

- CEO-level claims must be short, sourced, and non-hypey.
- Route/economics claims need a source pointer in `content-source.json`.
- If a value is directional, label it as a model output, early estimate, or assumption.
- For uncertain partner-market fits: use held-null language rather than assertive phrasing.
