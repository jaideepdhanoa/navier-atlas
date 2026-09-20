import type {Project,Slide} from './types';
import {NativeCanvas,COLORS} from './primitives';
/** Sales compositions reserve the band themselves. Never compress existing text or image groups after drawing. */
export function drawEvidenceFootnotes(c:NativeCanvas,p:Project,s:Slide){
 if(!s.footnotes?.length)return;
 if(p.schemaVersion!=='2.1.0')throw new Error('Footnote channel requires a reviewed V2.1 project.');
 if(s.layout!=='sales')throw new Error('FOOTNOTE_LAYOUT: use a registered sales composition or an inline qualification for a legacy/cover slide.');
 const text=s.footnotes.map(f=>f.text).join('  •  ');
 if(text.length>240)throw new Error('FOOTNOTE_BUDGET: split the slide or edit its evidence band; do not shrink qualifications.');
 c.line('evidence_band_rule',36,355,684,355,COLORS.line,.6);
 c.text('claim_linked_footnotes',text,36,361,648,18,{size:8,color:COLORS.muted,lineSpacing:102},'evidence-footnote');
}
