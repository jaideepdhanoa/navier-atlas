import { z } from 'zod';
import { writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { configSchema } from './model';
const path=process.argv[2]??fileURLToPath(new URL('../content.schema.json',import.meta.url));
await writeFile(path,JSON.stringify(z.toJSONSchema(configSchema,{target:'draft-2020-12'}),null,2));
console.log(`Generated ${path}`);
