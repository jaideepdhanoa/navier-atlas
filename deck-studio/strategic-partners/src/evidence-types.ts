import type {Audience} from './types';
/** V2.1 records are authored evidence, not facts inferred by the compiler. */
export interface EvidenceReview {reviewer:string;reviewedAt:string;reason:string;}
export interface Condition {key:string;value:number|string;unit:string;display:string;material:boolean;}
export interface OperatingContext {geography:string;mission:string;configuration:string;asOf:string;conditions:Condition[];}
export interface Quantity {id:string;metric:string;value:number|{min:number;max:number};unit:string;statistic:'typical'|'record'|'single-test'|'target'|'scenario'|'reported';}
export interface Provenance {subject:string;reportedBy:string;owner:'company'|'partner'|'market'|'third-party'|'fictional';}
export interface PriceBasis {category:'fuel'|'power'|'labor'|'capex'|'opex'|'service-price'|'revenue'|'investment'|'other';currency:string;geography:string;asOf:string;rates:{name:string;value:number;unit:string;sourceIds:string[]}[];}
export interface Applicability {mode:'same-context'|'supported-transfer'|'benchmark'|'unresolved';target:OperatingContext;rationale:string;sourceIds:string[];}
export interface ReplacementPlan {question:string;owner:string;partnerVisibleApproval?:EvidenceReview;}
export interface ClaimEvidence {
 topic?:'performance'|'economics'|'entity-capability'|'commercial-status'|'market'|'proposal';
 provenance?:Provenance;context?:OperatingContext;quantities?:Quantity[];dependsOn?:string[];
 priceBasis?:PriceBasis;applicability?:Applicability;replacementPlan?:ReplacementPlan;recipientIds?:string[];
}
export interface QuantityUse {claimId:string;quantityId:string;display:string;}
export interface ClaimUse {
 claimId:string;framing:'fact'|'modeled'|'target'|'record'|'precedent'|'placeholder'|'proposal';
 role:'partner-result'|'company-proof'|'market-context'|'historical'|'benchmark';
 qualification?:{channel:'inline'|'footnote';text:string;footnoteId?:string;};
}
export interface EvidenceFootnote {id:string;claimIds:string[];sourceIds:string[];text:string;}
export interface TalkTrack {say:string;basis:string;guardrail:string;qa:string;claimIds:string[];sourceIds:string[];clearedFor:Audience[];recipientIds:string[];review:EvidenceReview;}
export interface CompanionDocument {id:string;sourceId:string;version:string;asOf:string;heldBy:string[];claimIds:string[];}
export interface Reconciliation {documentId:string;priorClaimId:string;currentClaimIds:string[];action:'retained'|'updated'|'corrected'|'notes-only'|'retired';reason:string;status:'resolved'|'unresolved';sourceIds:string[];owner:string;reviewedAt:string;}
export interface CompanionContinuity {status:'reviewed'|'none'|'unknown';reason:string;documents:CompanionDocument[];reconciliations:Reconciliation[];}
export interface LeverTransfer {status:'assessed'|'not-applicable'|'unresolved';reason:string;claimIds:string[];sourceIds:string[];result:'survives'|'reframed'|'unresolved'|'not-applicable';reframe?:string;}
export interface SlideSupport {kind:'evidence'|'mechanism'|'proposal'|'synthesis';proposition:string;whyItMatters:string;claimIds:string[];rationale:string;}
export interface PolicyException extends EvidenceReview {code:'PRECEDENT_DENSITY'|'HEDGE_DENSITY'|'BODY_DENSITY'|'FORBIDDEN_CONTENT';path:string;term?:string;}
export interface EditorialPolicy {maxHedgeTokens?:number;maxPrecedents?:number;notesWordBudget?:number;bodyWordBudgets?:Record<string,number>;}
export interface EvidenceDiagnostic {code:string;severity:'warning'|'error';slideKeys:string[];detail:string;objectIds?:string[];}
export interface DensityRow {slideKey:string;bodyWords:number;finePrintWords:number;quantityUses:number;hedgeTokens:number;notesWords:number;}
export interface DiagnosticChecks {density:DensityRow[];numerals:EvidenceDiagnostic[];collisions:EvidenceDiagnostic[];orphanLines:EvidenceDiagnostic[];inspected:false;limitations:string[];}
