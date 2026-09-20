import {readFile} from 'node:fs/promises';
import {schemaIssues} from '../src/schema';
const root=new URL('..',import.meta.url).pathname;
const example=JSON.parse(await readFile(root+'/examples/public-demo/project.json','utf8'));
const errors=schemaIssues(example);
if(errors.length)throw Error(JSON.stringify(errors));
console.log('Strict AJV 2020-12 schema compilation and V1 compatibility: PASS. Canonical contract: project.schema.json.');
