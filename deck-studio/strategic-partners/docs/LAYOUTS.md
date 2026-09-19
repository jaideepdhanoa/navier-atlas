# V2 composition contract

`src/compositions.ts` renders the eight registered `sales` compositions. Sales slide string fields are `CopyBlock` IDs. The validator and renderer use the same registered names; unknown names/fields fail. Each visual must be source-linked and reviewed; concepts remain concepts.

| Composition | Required role and fields | Use when / avoid when |
|---|---|---|
| `partner-opportunity` | `intro`, `domains[]`, `proof[]`, `offer`; contextual proof and explicit offer | Introduce why this partner has a portfolio opportunity. Avoid a generic company overview. |
| `product-value` | `visual`, `mechanism`, `benefits[]`, `proof` | Explain a product-led mechanism and customer outcome. Avoid substituting a generic hero image for mechanism proof. |
| `platform-architecture` | `banner`, `physical[]` (optional visual per item), `ownership`, `software`, `revenue`, `demand[]`, `takeaway` | Show physical/digital/customer/ownership architecture and how value is created. Keep unresolved architecture qualified. |
| `opportunity-portfolio` | `intro`, `programs[]` (`opportunityId`, `heading`, `value`, `visual`), `connection` | Make the businesses legible before chapters. Do not collapse distinct payer/payment relationships. |
| `mission-hero` | `visual`, `need`, `benefits[]`, `payoff` | Sell one mission-specific product and benefit. A concept visual must not imply demonstrated performance. |
| `customer-alternative` | `intro`, `alternatives[]` (`heading`, `body`, `emphasis`), `jobs`, `advantage`, `comparison` (`basisBlockId`, `claimIds`, `kind`) | Explain current alternatives and the service/product gap. `kind` is `qualitative`, `modeled`, or `measured`; do not invent a basis. |
| `integrated-infrastructure` | `visual`, `intro`, `actions[]`, `options` | Explain operating roles and integrated infrastructure choices. State options and unresolved decisions. |
| `strategic-close` | `intro`, `stakes[]`, `visual`, `invitation`; optional `companion` (`labelBlockId`, `url`) | Close on partner-specific strategic value and a concrete invitation. An investment companion link does not turn this into an investment deck. |

## Shared rules

- `SalesBase` has `layout:'sales'` and a `status`; title/status and other displayed strings resolve from block IDs as appropriate.
- Bind visible blocks to the opportunity fields they express. Use claims for quantitative or otherwise material assertions and preserve qualification.
- Composition fields are not a mandatory internal eight-box checklist. The sales case can live in notes/appendix; the core must still communicate importance, Navier difference, recognizable businesses, strategic upside and invitation.
- Choose copy lengths that fit the renderer's budgets; change composition or edit copy before shrinking the deck. The native output remains editable: text, shapes, lines, images, manifests and notes are not rasterized.
- Payment relationships use explicit `Transaction` objects (`kind:'payment'`, actors, label). Do not imply payment direction through prose or generic arrows.
- A visual's `VisualBrief.argument` says what claim the image carries. `requiredFeatures` and `prohibitedImplications` protect product/architecture truth; `origin:'generated'` or `derivative` is illustrative and cannot serve as evidence. `architectureOptions` and `unresolvedChoices` prevent unchecked defaults.
- Source-slide reuse is a disposition and rights/editorial decision. An accessible URL is not a clearance record.

The original legacy layouts remain supported where their V1 contract is valid; do not create a partner-specific renderer. A materially new argument should become a tested reusable composition rather than a private fork.
