import Ajv2020 from 'ajv/dist/2020';
import addFormats from 'ajv-formats';
import schema from '../project.schema.json';
import type {ValidationIssue} from './types';
const ajv=new Ajv2020({strict:true,allErrors:true});
addFormats(ajv);
const validate=ajv.compile(schema);
export function schemaIssues(value:unknown):ValidationIssue[]{
 if(validate(value))return [];
 return (validate.errors??[]).map(error=>({severity:'error',code:'SCHEMA_CONTRACT',path:error.instancePath||'project',message:`${error.message??'Invalid structure'}${error.params.missingProperty?`: ${error.params.missingProperty}`:''}${error.params.additionalProperty?`: ${error.params.additionalProperty}`:''}`}));
}
export function assertSchema(value:unknown){const issues=schemaIssues(value);if(issues.length)throw new Error(issues.slice(0,12).map(issue=>`${issue.code} at ${issue.path}: ${issue.message}`).join('; '));}
