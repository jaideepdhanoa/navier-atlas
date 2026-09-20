// Sales authoring is partner-neutral. These records belong in each restricted project.
import type { BaseSlide, Crop, Visual } from './types';
import type {ClaimUse,QuantityUse,CompanionContinuity,LeverTransfer,SlideSupport,DiagnosticChecks} from './evidence-types';

export const SALES_FIELDS = ['need','alternative','scaleBasis','mechanism','outcome','ambition','entryPoint','evidenceBoundary'] as const;
export type SalesField = typeof SALES_FIELDS[number];
export type OpportunityField = 'title'|'product'|'customer'|'payer'|'commercialLogic'|'partnerBenefit'|'companyContribution'|'partnerContribution'|'nextQuestion'|`salesCase.${SalesField}`;
export interface SalesCase {
 need:string; alternative:string; scaleBasis:string; mechanism:string; outcome:string;
 ambition:string; entryPoint:string; evidenceBoundary:string;
 demandStatus:'partner-demand'|'market-context'|'hypothesis';
 readiness:'existing'|'demonstrated'|'in-design'|'exploratory';
}
export interface OpportunityBinding { opportunityId:string; field:OpportunityField; }
/** A from block dereferences the opportunity at compile time. An authored block uses explicit semantic bindings.
 * Bindings are traceability assertions, NOT proof that the prose supports the asserted meaning. Review separately.
 */
export interface CopyBlock {
 id:string;
 text?:string;
 from?:OpportunityBinding;
 bindings:OpportunityBinding[];
 claimIds:string[];
 placement:'core'|'appendix'|'notes';
 placementReason?:string;
 qualification?:string;
 claimUses?:ClaimUse[]; quantityUses?:QuantityUse[];
}
export interface SalesBrief {
 role:'standalone'|'investment-companion'; audienceDecision:string;
 partnerRelevance:string; partnerThesis:string; companyDifference:string; combinationAdvantage:string;
 strategicUpside:string; investmentBoundary:string; sourceIds:string[]; unresolvedQuestions:string[];
 companions?:CompanionContinuity;leverTransfer?:LeverTransfer;
}
export interface StorySource {
 id:string; sourceId:string; kind:'proposition'|'reference-slide'; importance:'core'|'supporting';
 summary:string; locator?:string;
}
export interface SourceDisposition {
 sourceItemId:string; action:'keep'|'strengthen'|'qualify'|'omit'; reason:string;
 destinationBlockIds:string[];
 visualDecision:'reuse-native'|'adapt'|'replace'|'not-visual'; visualReason:string;
}
export type NarrativeJob = 'opening'|'partner-relevance'|'company-advantage'|'platform'|'portfolio'|'opportunity'|'strategic-value'|'invitation'|'support';
export interface NarrativeEntry {
 slideKey:string; job:NarrativeJob; takeaway:string; transition:string; chapter:string;
 placement:'core'|'appendix'; opportunityIds:string[]; support?:SlideSupport;
}
export interface SalesAuthoring {
 brief:SalesBrief; sourceInventory:StorySource[]; sourceDisposition:SourceDisposition[];
 blocks:CopyBlock[]; narrative:NarrativeEntry[];
}
export interface VisualBrief {
 argument:string; requiredFeatures:string[]; prohibitedImplications:string[];
 origin:'existing'|'generated'|'derivative'|'fixture'; referenceSourceIds:string[];
 architectureOptions:string[]; unresolvedChoices:string[];
 sourceSlide?:{sourceId:string;locator:string};
 review:{status:'pending'|'reviewed';assetSha256:string;reviewerKind:'human'|'agent'|'fixture';reviewer:string;reviewedAt:string};
}
export interface VisualAttachment {
 assetId:string; parentSha256:string; assetSha256:string;
 /** Normalized to the uncropped parent image; stale source bytes or clipped marks are refused. */
 region:Crop;
 review:{status:'pending'|'reviewed';reviewerKind:'human'|'agent'|'fixture';reviewer:string;reviewedAt:string};
}
export interface PairBlocks { heading:string; body:string; }
/** On sales slides title/status and other content strings are CopyBlock IDs, not duplicate slide prose. */
export interface SalesBase extends BaseSlide { layout:'sales'; status:string; }
export interface PartnerOpportunitySlide extends SalesBase {
 composition:'partner-opportunity'; intro:string; domains:PairBlocks[]; proof:PairBlocks[]; offer:string;
}
export interface ProductValueSlide extends SalesBase {
 composition:'product-value'; visual:Visual; mechanism:string; benefits:PairBlocks[]; proof:string;
}
export interface PlatformSlide extends SalesBase {
 composition:'platform-architecture'; banner:string;
 physical:(PairBlocks & {visual?:Visual})[]; ownership:string; software:string; revenue:string;
 demand:PairBlocks[]; takeaway:string;
}
export interface PortfolioSlide extends SalesBase {
 composition:'opportunity-portfolio'; intro:string;
 programs:{opportunityId:string;heading:string;value:string;visual:Visual}[]; connection:string;
}
export interface MissionSlide extends SalesBase {
 composition:'mission-hero'; visual:Visual; need:string; benefits:PairBlocks[]; payoff:string;
}
export interface ComparisonSlide extends SalesBase {
 composition:'customer-alternative'; intro:string;
 alternatives:{heading:string;body:string;emphasis:boolean}[]; jobs:string; advantage:string;
 comparison:{basisBlockId:string;claimIds:string[];kind:'qualitative'|'modeled'|'measured'};
}
export interface InfrastructureSlide extends SalesBase {
 composition:'integrated-infrastructure'; visual:Visual; intro:string; actions:PairBlocks[]; options:string;
}
export interface StrategicCloseSlide extends SalesBase {
 composition:'strategic-close'; intro:string; stakes:PairBlocks[]; visual:Visual; invitation:string;
 companion?:{labelBlockId:string;url:string};
}
export type SalesSlide=PartnerOpportunitySlide|ProductValueSlide|PlatformSlide|PortfolioSlide|MissionSlide|ComparisonSlide|InfrastructureSlide|StrategicCloseSlide;
export type Composition=SalesSlide['composition'];
export interface CopyEmission {blockId:string;slideKey:string;objectId:string;text:string;claimIds:string[];bindings:OpportunityBinding[];placement:CopyBlock['placement'];}
export interface ReviewFinding {code:string;severity:'revise'|'note';detail:string;slideKeys:string[];}
export interface ReaderAnswer {answer:string;slideKeys:string[];}
export interface EditorialReview {
 schemaVersion:'2.0.0'|'2.1.0'; subjectHash:string; visibleCopyHash:string;
 reviewer:{name:string;kind:'human'|'agent'|'fixture'}; reviewedAt:string; decision:'pass'|'revise';
 answers:{partnerImportance:ReaderAnswer;companyDifference:ReaderAnswer;businesses:ReaderAnswer;strategicUpside:ReaderAnswer;invitation:ReaderAnswer};
 tests:{partnerSpecificity:ReaderAnswer;companyRemoval:ReaderAnswer;sourceFidelity:ReaderAnswer;specificity?:ReaderAnswer;applicability?:ReaderAnswer;companionContinuity?:ReaderAnswer;leverTransfer?:ReaderAnswer;qualification?:ReaderAnswer;notesDisclosure?:ReaderAnswer};
 rounds?:{specificity:{reviewedAt:string;decision:'pass'|'revise';notes:string};relevance:{reviewedAt:string;decision:'pass'|'revise';notes:string}};
 findings:ReviewFinding[];
}
export interface RenderArtifact {path:string;sha256:string;}
export interface RenderReviewBundle {
 schemaVersion:'2.0.0'|'2.1.0'; inputHash:string; compiledHash:string; nativeHash:string; nativePresentationId:string;
 pdf:RenderArtifact; pageCount:number; visibleCopyHash:string;
 pages:{slideKey:string;page:number;full:RenderArtifact;phone:RenderArtifact;textCoverage:number;missingText:string[]}[];
 status:'ready-for-inspection'|'held'; holds:string[]; inspected:false; externalRelease:'held'; checks?:DiagnosticChecks;
}
export interface VisualInspection {
 schemaVersion:'2.0.0'; bundleHash:string; reviewer:{name:string;kind:'human'|'agent'|'fixture'};reviewedAt:string;
 decision:'pass'|'revise';
 pages:{slideKey:string;fullInspected:boolean;phoneInspected:boolean;headlineGist:string;findings:string[]}[];
}
