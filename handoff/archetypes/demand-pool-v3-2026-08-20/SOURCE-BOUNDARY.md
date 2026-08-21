# Source boundary — what never leaves the trackers

The seven employer trackers (Bay, NY, Boston, DC, Seattle, Miami–Ft Lauderdale, San Diego) share one
11-column schema. They are **outreach pipeline documents**, not a publishable dataset. This note fixes
which columns may cross into a rendered surface, so the question doesn't get re-litigated per city.

| Col | Field | Publishable? |
|---|---|---|
| A | Node | ✅ — but rebound to the exact `hub.json` stop label, never the tracker's shorthand |
| B | Line | ✅ — but rebound to the real line name; tracker uses stale codes (`A/B`, `NY-1`) |
| C | Employer / org | ✅ |
| D | Type | ⚠️ internal only — surfaces instead as plain English in `note` ("landlord", "an aggregate of many firms") |
| E | Priority (P0/P1/P2) | ❌ **never** — our sales ranking of their attractiveness |
| F | Est. on-site HC **(verify)** | ⚠️ only as a qualified `value` string. The column header says "(verify)". These are planning estimates, and the employer universe Part 4 explicitly flags Salesforce, OpenAI, Uber and Brooklyn Navy Yard as unconfirmed |
| G | Demand pool (seats) | ⚠️ aggregate only. Per-row it is just F × 3% — a modelled number dressed as a fact. One clearly-labelled city total instead |
| H | Contact roles to find | ❌ **never** — our targeting of named individuals' roles |
| I | Warm path | ❌ **never** — names intermediaries and relationships |
| J | Talking points / commentary | ❌ **never** — see below |
| K | Status / Motion | ❌ **never** — pipeline state |

## Why column J in particular

It contains our candid internal read on named third parties: a failed pilot to "restart with an honest
post-mortem", an incumbent operator's contract that "gets re-bid", and assessments of specific
companies' internal culture and procurement speed. None of it is defamatory and all of it is useful
internally — but it is written in the register of a private sales note, about companies we have not
spoken to. It should not sit anywhere it can be pasted into a public field by accident.

**Rule: the trackers are never handed over as files, links, or exports.** What crosses the boundary is
an authored `demand_pool` block containing columns A, B, C, a qualified F, and one aggregate G.

## Standing label

Every demand-pool block carries this verbatim, and it is now a top-level renderable field:

> Indicative of demand potential along these corridors — not commitments, commercial relationships,
> or discussions with the organisations named.

The last clause matters. Naming Genentech and Goldman Sachs on an investor page invites the inference
that they are in conversation with us. They are not, and the label has to say so.
