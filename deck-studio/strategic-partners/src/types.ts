// Public, partner-neutral contracts. Partner dossiers, account bindings and live IDs stay outside this package.
import type { SalesCase, SalesAuthoring, SalesSlide, CopyEmission, VisualBrief, VisualAttachment } from './sales-types';
export type * from './sales-types';
export type * from './evidence-types';
import type {ClaimEvidence,TalkTrack,ClaimUse,QuantityUse,EvidenceFootnote,EditorialPolicy,PolicyException} from './evidence-types';
export type Audience = 'internal' | 'partner' | 'public';
export type Visibility = 'public' | 'internal' | 'restricted';
export type EvidenceClass = 'measured' | 'demonstrated' | 'historical' | 'company-reported' | 'preliminary' | 'modeled' | 'planned' | 'proposed' | 'fictional' | 'tested' | 'target' | 'in-design';
export interface Source { id:string; title:string; locator:string; asOf:string; visibility:Visibility; kind?:'primary'|'secondary'; clearedFor?:Audience[]; recipientIds?:string[]; }
export interface Claim extends ClaimEvidence { id:string; statement:string; evidenceClass:EvidenceClass; sourceIds:string[]; basis:string; clearedFor:Audience[]; limitations?:string; }
export interface Crop { left:number; top:number; right:number; bottom:number; }
export interface Asset {
 id:string; path:string; sha256:string; width:number; height:number; mimeType:string;
 kind:'photograph'|'rendering'|'schematic'|'logo'; maturity:'actual'|'demonstrated'|'concept'|'context'|'brand';
 title?:string; vessel?:string; missions:string[]; geography:string[]; roles:string[]; sourceIds:string[];
 visibility:Visibility; clearedFor:Audience[]; rightsNote:string; caption:string;
 focalPoint?:{x:number;y:number}; keepRegion?:Crop; crop?:Crop;
 embeddingUrl?:string; nativeSource?:{presentationId:string;slideObjectId:string;imageObjectId:string};
 repoSource?:{owner:string;repo:string;ref:string;path:string;blobSha:string};
 visualBrief?:VisualBrief;
}
export interface Opportunity {
 id:string; kind:'supply'|'co-development'|'contract-build'|'license'|'direct-sale'|'resale'|'service'|'operator-program'|'other';
 title:string; product:string; customer:string; payer:string; commercialLogic:string; partnerBenefit:string;
 companyContribution:string; partnerContribution:string; nextQuestion:string; claimIds:string[]; status:'proposed'|'existing';
 salesCase?:SalesCase;
}
export interface Visual { assetId:string; caption:string; crop?:Crop; attachments?:VisualAttachment[]; }
export interface Transaction { actors:string[]; labels:string[]; kind:'payment'; }
export interface BaseSlide { key:string; kicker:string; title:string; claimIds:string[]; sourceIds:string[]; opportunityIds:string[]; notes:string|TalkTrack; claimUses?:ClaimUse[]; quantityUses?:QuantityUse[]; footnotes?:EvidenceFootnote[]; }
export interface CoverSlide extends BaseSlide { layout:'cover'; visual:Visual; subtitle:string; body:string; pillars:string[]; }
export interface FitSlide extends BaseSlide { layout:'fit'; visual:Visual; companyLabel:string; companyHeadline:string; companyBody:string; partnerLabel:string; partnerBody:string; benefits:{title:string;body:string}[]; takeaway:string; }
export interface OptionsSlide extends BaseSlide { layout:'options'; options:{title:string;body:string;visual?:Visual;schematic?:'manufacture'|'hybrid'|'service';revenue:string}[]; payment?:Transaction; status:string; explore:string; }
export interface ModelsSlide extends BaseSlide { layout:'models'; models:{label:string;title:string;body:string;visual?:Visual;technologyLabel?:string;payments:Transaction;benefit:string}[]; explore:string; }
export interface ChannelsSlide extends BaseSlide { layout:'channels'; scope:string; selection:string; criteria:string; visual?:Visual; models:{label:string;benefit:string;payments:Transaction}[]; serviceLabel:string; service:string; explore:string; }
export interface MissionsSlide extends BaseSlide { layout:'missions'; intro:string; status:string; cards:{label:string;title:string;description:string;visual:Visual}[]; explore:string; }
export interface CloseSlide extends BaseSlide { layout:'close'; visual:Visual; intro:string; conversations:{title:string;body:string}[]; ask:string; contact:string; }
export type LegacySlide = CoverSlide | FitSlide | OptionsSlide | ModelsSlide | ChannelsSlide | MissionsSlide | CloseSlide;
export type Slide = LegacySlide | SalesSlide;
export interface Project {
 schemaVersion:'1.0.0'|'2.0.0'|'2.1.0';
 sales?:SalesAuthoring;
 meta:{projectId:string;revision:string;title:string;company:string;partner:string;legalEntity:string;audience:Audience;archetype:'industrial'|'energy-operator'|'strategic';objective:string;meetingAudience:string;date:string;classification:string;fictional:boolean;companyLogoAssetId?:string;partnerLogoAssetId?:string;footer:string;recipientIds?:string[];notesMode?:'talk-track'|'audit';};
 sources:Source[];claims:Claim[];assets:Asset[];opportunities:Opportunity[];slides:Slide[];
 policy:{forbiddenTerms:string[];forbiddenPartnerNames:string[];requiredPhrases:string[];allowMissingLogosForInternalReview:boolean;editorial?:EditorialPolicy;approvedExceptions?:PolicyException[];};
}
export interface ValidationIssue { severity:'error'|'warning'|'release-hold'; code:string; path:string; message:string; }
export interface ValidationResult { ok:boolean; releaseReady:boolean; issues:ValidationIssue[]; }
export type SlidesRequest = Record<string,any>;
export interface Box { objectId:string;slideKey:string;role:'text'|'image'|'shape'|'line'|'mask';x:number;y:number;w:number;h:number;text?:string;fontSize?:number;intentionalClip?:boolean; }
export interface ElementRole { objectId:string;slideKey:string;role:string;kind:'text'|'image'|'shape'|'line';assetId?:string;parentObjectId?:string; }
export interface CompiledSlide { key:string;objectId:string;layout:Slide['layout'];requests:SlidesRequest[];elements:ElementRole[];boxes:Box[];visibleText:string[];notes:string;copyBindings?:CopyEmission[]; }
export interface CompiledDeck { schemaVersion:'1.0.0';projectId:string;revision:string;inputHash:string;pageSize:{width:720;height:405};slides:CompiledSlide[];requests:SlidesRequest[];assetUses:{assetId:string;slideKey:string;role:string;objectId:string}[];warnings:ValidationIssue[]; }
export interface ElementSnapshot { objectId:string;size?:any;transform?:any;shape?:any;image?:any;line?:any;elementGroup?:{children:ElementSnapshot[]};[key:string]:any; }
export interface SlideSnapshot { objectId:string;index:number;pageElements:ElementSnapshot[];slideProperties?:any;[key:string]:any; }
export interface DeckSnapshot { presentationId:string;title?:string;pageSize?:any;revisionId?:string;slides:SlideSnapshot[]; }
export interface Binding { schemaVersion:'1.0.0';projectId:string;presentationId:string;expectedTitle:string;protectedPresentationIds:string[];folderId?:string;roleMap:ElementRole[];lastApplied?:{revision:string;planHash:string;afterHash:string}; }
export type PatchOperation =
 | {kind:'text';objectId:string;text:string;fontSize?:number}
 | {kind:'move';objectId:string;bounds:{x:number;y:number;w:number;h:number};attachedMarks?:string[];preserveAspect?:boolean}
 | {kind:'replace-image';objectId:string;assetId:string;url:string;crop?:Crop};
export interface PatchPlan { schemaVersion:'1.0.0';projectId:string;presentationId:string;revision:string;baseHash:string;operations:PatchOperation[];allowedObjectIds:string[];planHash:string; }
export interface ReviewReceipt { stage:'storyboard'|'comprehension'|'visual'|'release';subjectHash:string;reviewer:string;reviewedAt:string;decision:'approved'|'held';notes:string;artifactHashes?:Record<string,string>;reviewerKind?:'human'|'agent'|'fixture';purpose?:'storyboard-approval'|'internal-readiness'|'visual-inspection'|'finished-deck'|'external-release'|'workflow-test'; }
