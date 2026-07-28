# ADR-0012: Refine the RFI search contract from runtime verification

## Status

Accepted

## Date

2026-07-28

## Context

> **Numbering note.** This is **reference-repo ADR-0012**. The APS/Forma MCP
> component repository maintains its own, independent ADR series.

[ADR-0011](0011-adopt-rfi-first-slice-mcp-contract-and-component-boundary.md)
adopted the RFI first-slice MCP contract and closed Gate 6. It fixed the
`search_rfis` caller shape as `id`, `custom_identifier`, `title`, `status`,
`workflow_type`, recorded an upstream semantic field set of `id`,
`customIdentifier`, `title`, `status`, `workflowType`, and **deliberately
deferred the transport encoding** of that projection, stating: "The normative
documentation describes `fields` as a request-body array while its worked example
is written in query-string form… No encoding is guessed."

It also required that "any material conflict must return to governance rather
than silently changing the contract."

**A conflict of exactly that kind has now occurred.** A bounded sequence of
read-only probes against the read-semantic `search:rfis` endpoint, in the
approved training project, established the runtime facts below.

### Runtime facts established

1. **The JSON-body `fields` property is accepted.** A request carrying
   `{"fields": ["id", "customIdentifier", "title", "status"]}` returned HTTP 200
   with a populated collection.
2. **`fields` is enum-validated.** The service validates each array member
   against a declared enumeration.
3. **The four members `id`, `customIdentifier`, `title`, `status` form a
   successful request.**
4. **`workflowType` is rejected as an enum member.** Including it produced a
   deterministic HTTP 400 with nested schema violation `ENUM_MISMATCH` at
   `fields[4]`, naming `workflowType`.
5. **The resulting search representation may still contain additional top-level
   properties.** The successful four-member request returned fifteen top-level
   item keys — the requested keys present for the record, plus `architects`,
   `assignedTo`, `coReviewers`, `hash`, `maxAssignees`, `officialResponseActors`,
   `optionalReviewers`, `permittedActions`, `responses`, `reviewers`,
   `virtualFolderUrn` and `watchers`. No value of any additional key was
   inspected.
6. **Therefore `fields` is not a strict caller-facing projection or enforcement
   mechanism.**

Two further observations were made about the controlled synthetic fixture:
`customIdentifier` was **absent** — not null — from the returned item, and its
API `status` was observed as `draft`.

### What the evidence does not establish

**No control request omitting `fields` was performed.** The exact
response-shaping effect of `fields` is therefore **not established**, in either
direction.

In particular, `question`, `officialResponse`, `suggestedAnswer`, `createdBy` and
`updatedBy` were **not present** in the returned items, but **no causal
attribution of that absence to the request projection is established**. Their
absence was observed; why they were absent was not determined, and this ADR draws
no conclusion from it.

**Documentation could not settle any of this.** The APS reference pages for RFI
v3 are client-rendered and returned an identical content-free shell for every
endpoint across two separate passes, so the encoding was established by bounded
runtime observation rather than by guessing — exactly the route ADR-0011
anticipated.

## Decision

### 1. Search caller items are four fields

`search_rfis` returns items of **`id`, `custom_identifier`, `title`, `status`**,
plus pagination `limit`, `offset`, `total_results`.

**`workflow_type` is removed from the search caller contract**, because
`workflowType` is not a verified projectable search member and the successful
search did not return it. Search is a discovery operation, and four fields are
sufficient to identify and select an RFI.

**`workflow_type` is removed from search only.** It remains in
`get_rfi_user_context` (sourced from `workflow.type`) and in the `get_rfi`
curated DTO, both unchanged.

### 2. No derivation and no fan-out

`search_rfis` must not obtain `workflow_type` by deriving it, guessing it,
caching it from another tool invocation, calling `users/me` automatically,
calling `get_rfi` automatically, or issuing any second API request.

**One tool invocation remains one Autodesk search operation.** ADR-0011's
no-fan-out policy is reaffirmed, not relaxed.

### 3. The verified search request

The approved v1 search request is the runtime-verified JSON body:

```
{ "fields": ["id", "customIdentifier", "title", "status"] }
```

sent to `POST /construction/rfis/v3/projects/{projectId}/search:rfis`.

These four members are the **approved v1 search request set**. `workflowType` is
not included, and no substitute member is guessed.

### 4. `fields` is not the enforcement mechanism

ADR-0011's strict server-side minimisation assumption is refined.

**`fields` is a validated bounded upstream selection request. Its exact
response-shaping effect is not established, and it is not an enforcement
boundary.**

What is established is that the property is accepted, that its members are
enum-validated, and that a successful request may still return additional
top-level properties. No claim is made here that `fields` reduced, minimised, or
otherwise shaped the response.

### 5. The client allowlist is authoritative

The dedicated `rfis_client` explicit allowlist is the authoritative
caller-facing boundary:

```
Autodesk raw search item → rfis_client explicit allowlist
                         → caller item { id, custom_identifier, title, status }
```

Additional Autodesk properties are discarded before caller output. Caller output
must never gain `responses`, `assignedTo`, `reviewers`, `watchers`, `architects`,
`coReviewers`, `optionalReviewers`, `officialResponseActors`, `permittedActions`,
`virtualFolderUrn`, `hash` or `maxAssignees` unless a future deliberately adopted
contract says otherwise.

This is not a new principle: **allowlist-in-client was already ADR-0011's chosen
design.** What changes is that it is now the sole guarantee rather than the second
of two.

### 6. Transient raw data

[ADR-0010](0010-approve-rfi-public-evidence-sanitisation-profile.md) already
permits raw values to exist transiently during authenticated processing.
**Receiving additional Autodesk search properties therefore does not violate
Gate 5.**

Those properties must nevertheless not reach normal caller output, must not be
logged, must not enter public evidence, and must not be persisted in tracked
artifacts. **No new public-evidence exception is created, and ADR-0010 is neither
amended nor superseded.**

### 7. The narrative claim is refined

ADR-0011's clause "Narrative beyond `title` is never fetched" is **refined and no
longer asserted in that form**. The effective statement is:

> The search request asks Autodesk for the narrow verified discovery field set,
> but Autodesk may return additional properties. The `rfis_client` explicit
> allowlist is the authoritative caller boundary. No unapproved narrative or
> participant data returned upstream is surfaced to the caller or to normal logs.

**Scope limit, stated precisely.** The probe observed the **key** `responses` in
the search response and **did not inspect its value**. This ADR therefore does
not claim that response narrative was returned, that it was not returned, that
`responses` is always empty, or that it is always populated. **Only the presence
of the key is established.**

### 8. `custom_identifier`

`custom_identifier` remains a stable caller DTO key in both `search_rfis` and
`get_rfi`. When upstream `customIdentifier` is absent, null or empty, the caller
value is **`None`** — never `"-"`, `"Unspecified"`, `"RFI-0"` or `""`.

The controlled Draft has now demonstrated the **absent-key** case empirically:
the key was omitted entirely from the returned item rather than returned as null.

### 9. Observed fixture status

The controlled Draft's API `status` was observed as **`draft`**, where the
Autodesk Build interface displays *Draft*.

**This is recorded as a controlled-fixture observation and an implementation
expectation only.** No other interface-to-API status mapping is generalised from
this single observation.

## What this ADR does not do

- **It does not supersede ADR-0011.** It refines ADR-0011's `search_rfis` contract
  and its search minimisation mechanism. Every other ADR-0011 decision remains
  accepted and authoritative: APS/Forma MCP ownership; the dedicated
  `rfis_client`; the allowlist-in-client principle; the three-tool v1 slice;
  `get_rfi_user_context`; `get_rfi`; core RFI narrative; embedded-response caller
  exclusion; the participant-count detail contract; authentication; project-ID
  normalisation; the endpoint-specific POST; no generic request surface; errors
  and logging; pagination and fan-out; Gate-5 separation; and the deferred
  surfaces.
- **ADR-0011 is not amended.** Its text stands unchanged as the historical
  decision record, following the precedent ADR-0009 set for ADR-0008.
- **It does not reopen Gate 6.** Gate 6 remains **passed**. ADR-0011 required a
  material API conflict to return to governance instead of being absorbed into
  implementation; this ADR is that mechanism working as designed.
- **It does not close or advance Gate 8**, which remains **unresolved**. The
  controlled Draft is now proven discoverable through the raw search endpoint,
  but no MCP implementation exists, `get_rfi` has not been verified through the
  approved contract, caller context has not been verified through
  `get_rfi_user_context`, and no Gate-5-safe evidence artifact has been produced.
- **It does not change `data_readiness`**, which remains `not-assessed`.
- **It does not change `mcp_implementation_status`**, which remains `planned`.
- **It does not amend ADR-0007.** `search:rfis` remains a read-semantic POST, and
  every probe behind this ADR was read-only in state semantics.
- **It does not amend ADR-0010** or the sanitisation convention.
- **It authorises no implementation**, no MCP_Forma change, and no further API
  call.

## Rejected alternatives

- **Amending ADR-0011 in place.** No ADR in this repository has been edited after
  acceptance, and ADR-0009 established refinement-by-successor as the mechanism.
  Editing an accepted decision would erase the record of what was believed when
  Gate 6 closed, which is precisely the history a decision log exists to keep.
- **Claiming that `fields` minimised the response.** No control request omitting
  `fields` was performed, so its response-shaping effect is unmeasured. Reading
  the absence of `question`, `officialResponse`, `suggestedAnswer`, `createdBy`
  and `updatedBy` as proof that the projection worked would attribute a cause the
  evidence does not support.
- **Guessing a substitute for `workflowType`.** Guessing at a projection member
  is exactly what ADR-0011 forbade. The member, if one exists, must be
  established, not invented.
- **Adding a second API call so search can still return `workflow_type`.** It
  would breach the no-fan-out policy and make one tool invocation two Autodesk
  operations, to enrich a discovery listing that does not need it.
- **Deriving `workflow_type` from project configuration or a cached
  `users/me`.** A derived value that looks like an observed one is worse than an
  absent one; it would silently assert something the search response never said.
- **Keeping the "narrative beyond `title` is never fetched" claim.** The
  mechanism behind it is not an established response-shaping control, so
  retaining the wording would leave a published claim that no code could honour.
- **Declaring a Gate 5 conflict.** ADR-0010 already permits transient raw values
  during authenticated processing; nothing crossed into public evidence, and
  manufacturing a privacy incident from a governed transient would be inaccurate.
- **Reopening Gate 6.** The contract was refined by the route ADR-0011 specified.
  Treating a working governance mechanism as a gate failure would penalise the
  behaviour the gate model is designed to produce.

## Follow-up

None of the following is authorised by this ADR:

1. **RFI MCP implementation** — `rfis_client`, tool registrations and tests.
2. **Resolving the workflow-type search question** — whether any projectable
   member represents the workflow-type concept in a search item remains open, and
   must be established rather than guessed.
3. **Determining the response-shaping effect of `fields`**, which would require a
   deliberately authorised control request.
4. **Determining the contents of `responses` in search results** — only the key's
   presence is established.
5. **Discovering the full `fields` enum**, which would settle items 2 and 3.
6. **RFI Gate 8** — implementation, live verification through the approved MCP
   contract, and the Gate-5-safe evidence artifact.
7. **Transition of `mcp_implementation_status`** away from `planned`, or of
   `data_readiness` away from `not-assessed`.

## Consequences

- **The implementation blocker recorded in the RFI implementation preview is
  removed.** The search transport is runtime-verified, so the endpoint-specific
  POST helper and its tests have a settled contract to encode.
- **The published contract now matches observed behaviour.** No governance
  statement about RFI search asserts more than the evidence supports.
- **The client allowlist carries more weight**, which raises the value of the
  tests that prove it: an upstream payload carrying every additional property
  must reduce to exactly four caller keys.
- **The gate model gained a worked example** of a material conflict surfacing
  before implementation rather than after it — the ordering that §16.4 recorded
  as defective for Transmittals, working correctly here.

**This ADR refines ADR-0011's `search_rfis` contract. It supersedes nothing.**
