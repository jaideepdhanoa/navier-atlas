# V2.1 content contract

The runtime contract is in `src/types.ts`, `src/evidence-types.ts`, `src/evidence.ts`, `src/talk-track.ts`, `src/footnotes.ts` and `src/diagnostics.ts`. A valid project is not automatically persuasive, truthful, rights-cleared, visually inspected or approved for release.

## Brief, sources and sales cases

Complete `sales.brief` with the V2 sales fields plus `companions` and `leverTransfer`. `companions` is recipient/version-specific: record held documents, consequential claims and each disposition (`retained`, `updated`, `corrected`, `notes-only`, `retired`). A correction needs replacement claims, sources, owner and reason. A prior document held by one recipient is not clearance for another. Use `leverTransfer.status:'not-applicable'` only with a reason.

Sources used by V2.1 claims identify kind (`primary`/`secondary`), visibility, audience and recipient clearance. Do not expose private locators. A benchmark, precedent or placeholder must retain its actual basis; partner-visible placeholders need approval and a replacement owner/question.

## Claims and visible uses

A used 2.1 claim requires topic, provenance, operating context and `dependsOn`; numeric claims require quantities and applicability. Currency claims require a relevant price basis. `ClaimUse` binds a claim to visible framing (`fact`, `modeled`, `target`, `record`, `precedent`, `placeholder` or `proposal`) and role. `QuantityUse` binds the exact visible display to a quantity. Slide-wide `claimIds` alone do not establish what prose means.

`EvidenceFootnote` is authored and claim/source-linked. It is optional, must be audience-safe, and the combined visible band is max 240 characters. It is not a blanket slide evidence grade. Mixed measured/model/target/record material keeps separate labels; essential context cannot be hidden in fine print.

## Notes, reviews and diagnostics

A 2.1 external slide uses a cleared `TalkTrack` (`say`, `basis`, `guardrail`, `qa`) with reviewer/date/reason, audience and recipient clearance. `notesMode:'audit'` is internal only. `evidenceManifest` is a restricted working record, not partner notes. Two editorial rounds are required: proposition/support, then applicability/decision relevance.

`densityLedger` counts emitted body/fine-print words, bound quantity uses, hedge tokens and notes words; it does not count facts proved. The default body budget is 115 advisory unless composition policy overrides it. `numeralDiagnostics` checks bound quantities and context; `geometryDiagnostics` uses actual native transforms and optional PDF words. Missing PDF words means orphan-wrap detection is not checked. All diagnostics remain separate from human inspection.

V1/legacy 1.0.0 and 2.0.0 remain readable. Migration creates a held draft and preserves assets/data without fabricating evidence, continuity, claims or approvals.
