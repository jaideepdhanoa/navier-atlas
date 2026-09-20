# V2.1 composition and layout contract

`src/compositions.ts` renders eight registered sales compositions: `partner-opportunity`, `product-value`, `platform-architecture`, `opportunity-portfolio`, `mission-hero`, `customer-alternative`, `integrated-infrastructure` and `strategic-close`. Unknown names/fields fail. Choose by explanatory job, not fixed slide count.

| Composition | Job |
|---|---|
| `partner-opportunity` | Establish partner-relevant portfolio opportunity and offer. |
| `product-value` | Explain a product mechanism and customer outcome. |
| `platform-architecture` | Show physical/digital/ownership/revenue architecture and demand. |
| `opportunity-portfolio` | Make connected businesses legible before chapters. |
| `mission-hero` | Sell one mission-specific need, benefit and payoff. |
| `customer-alternative` | Compare current alternatives on an explicit qualitative, modeled or measured basis. |
| `integrated-infrastructure` | Explain operating roles and infrastructure choices/options. |
| `strategic-close` | Close on partner-specific stakes and invitation. |

## Shared layout rules

Sales fields resolve through `CopyBlock` IDs; bindings provide traceability, not proof. Payment flows use explicit `Transaction` objects with actors and `kind:'payment'`. A visual brief states its argument, required features, prohibited implications, provenance, architecture options and unresolved choices. Concepts remain visibly illustrative.

V2.1 claim uses are direct: bind each material visible assertion to `claimUses`, and each visible number to `quantityUses`. Use claim-linked inline or footnote qualifications when evidence classes differ; do not apply one slide-wide grade. Footnotes occupy a real evidence band (max 240 characters at 8pt, only new 2.1 output). Fonts are not reduced; body spacing and image frames reflow and must be inspected in actual output.

The current default body budget is 115 words as an advisory diagnostic unless composition policy overrides it. Character limits and layout contracts still bind. Density is a review signal, not a target. Intentional text-on-image/attached layers are excluded by geometry diagnostics; actual text-text overlap and out-of-bounds text remain findings. Native/PDF review is separate from tests.

Legacy layouts remain readable where their contract is valid. Do not create a partner-specific renderer; a materially new reusable argument belongs in a tested composition.
