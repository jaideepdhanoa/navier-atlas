# Publication and access boundaries

A partner-forwardable PDF and a public repository are different audiences.

## Three stores

| Store | What belongs there |
|---|---|
| Public repository | Generic tooling, fictional examples, public company facts and source references, non-sensitive QA/documentation. |
| Shared knowledge | The toolkit/Skill and the public reference library. Additional sensitive research only when the shared audience is explicitly appropriate. |
| Restricted partner project | Original communications, relationship chronology, negotiation context, private technical evidence, approved confidential brief/config, source files and private QA. |

## Before a GitHub commit

1. Confirm repository visibility and intended audience.
2. Read repository guidance and existing destination files; preserve live originals.
3. Stage only the intended public package paths. Do not publish a whole working directory.
4. Inspect the staged file list, compute hashes and record why each file is public.
5. Recheck data-bearing JSON/Markdown/CSV and image provenance. A generic tool may contain the words “private” or “valuation” as a rule; that is not equivalent to private deal data. Conversely, a clean keyword scan is not proof that a file is safe.
6. Exclude raw email/transcript files, internal asset/contact paths, private counterpart remarks, draft financing details, private claims and confidential render outputs.
7. Validate the public example and source registers, then open a separate PR. Do not merge or modify the live source without authorization.
8. Save branch/PR/commit and local knowledge receipts so another agent can find the work.

The renderer blocks obvious classification mismatches and unsafe resources. It cannot decide whether a claimed clearance is real or whether publication is commercially wise. That decision remains with the responsible author/reviewer.
