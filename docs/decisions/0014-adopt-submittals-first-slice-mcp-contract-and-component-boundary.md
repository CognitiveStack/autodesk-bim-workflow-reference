# ADR-0014: Adopt Submittals first-slice MCP contract and component boundary

## Status

Accepted

## Date

2026-07-29

## Context

> **Numbering note.** This is **reference-repo ADR-0014**. The APS/Forma MCP
> component repository maintains its own, independent ADR series.

Submittals entered Phase 4A as a candidate and has since accumulated the
governance needed to adopt a first read-only slice:

- **Gate 2 is sufficiently verified** and codified at
  [PHASE_4_CAPABILITY_GAP.md](../architecture/PHASE_4_CAPABILITY_GAP.md) §16.8 —
  three endpoints returned HTTP 200 under a three-legged token whose granted scope
  claim was **exactly `data:read`**.
- **Gate 5 is passed** by
  [ADR-0013](0013-approve-submittals-public-evidence-sanitisation-profile.md),
  with the public-evidence profile recorded in
  [SANITISATION_CONVENTION.md](../guides/SANITISATION_CONVENTION.md) and the
  closure at §16.9.
- **Gates 1, 3, 4, 7, 9 and 10** were already substantially supported by the
  Phase 4A research.

**Gate 6 (component-boundary decision) is the open question this ADR answers.**

Unlike [ADR-0011](0011-adopt-rfi-first-slice-mcp-contract-and-component-boundary.md),
which fixed the RFI contract largely from documentation, **this contract is
designed against an observed response shape**. Bounded read-only runtime
verification against a controlled synthetic fixture in the approved training
project established:

- **`GET users/me`** returns `id` (string), `roles` (array of strings) and
  `permittedActions` (array of objects, each carrying `id`, `fields`,
  `mandatoryFields` and `transitions`; `transitions` members carry `actionId`,
  `stateFrom`, `stateTo`, `transitionFields` and `mandatoryFields`).
- **`GET items`** returns a `pagination` / `results` envelope, `pagination`
  carrying `limit`, `offset` and `totalResults`. With no parameters the service
  returned `limit` 20. **The maximum page size is unknown.**
- **The list row and the detail response are shape-identical** — the same 56 keys
  with the same types on both surfaces, no key unique to either, and every
  state-dependent key present as `null` on an item that has never been submitted.
- **The item-level `permittedActions` array** has the same member signature as the
  caller-level array, narrowed to the actions available for that item.

A single **controlled synthetic Submittal fixture** exists in the approved training
project. It was created through the Autodesk product interface, has never been
submitted or transitioned, and is **diagnostic input for contract verification
only** — not Gate-8 evidence.

**Submittals has no capability record** in
[end-to-end-reference.yaml](../../config/workflows/end-to-end-reference.yaml). This
ADR adds one, in the honest intermediate state the schema-v2 vocabulary already
supports.

## Decision

### Component ownership

**The APS/Forma MCP owns Submittals**, in a **dedicated `submittals_client`**.
Submittals semantics belong in no existing client and in no generic request
infrastructure.

### V1 first-slice tool surface

**Three read-only tools.** All three are `GET`; **no POST-as-read classification is
involved**, so [ADR-0007](0007-read-write-classification-by-state-semantics.md) is
referenced but not exercised.

| Tool | Endpoint | State semantics |
|---|---|---|
| `get_submittal_user_context` | `GET …/submittals/v2/projects/{projectId}/users/me` | read |
| `list_submittals` | `GET …/submittals/v2/projects/{projectId}/items` | read |
| `get_submittal` | `GET …/submittals/v2/projects/{projectId}/items/{itemId}` | read |

Three tools is the **v1 scope**, not a permanent prohibition; a later surface may
be adopted deliberately through the same governance route.

**Naming.** The names follow the established sibling pattern —
`get_rfi_user_context` / `get_rfi` and `list_transmittals` / `get_transmittal`.
`list_` rather than `search_` because this is a plain `GET` collection, not the
body-carrying `POST search:rfis` shape.

**`list_submittal_items` and `get_submittal_item` are rejected.** The component
already exposes `get_item_details` and `list_item_versions` for **Data Management
items**. Placing "item" in a Submittals tool name would recreate, inside the
caller's tool namespace, the `ITEM_n` / `SUBMITTAL_n` identifier-domain collision
that ADR-0013 made a normative prohibition. The upstream route says `items`; the
tool surface says `submittal`.

### Input contracts

| Tool | Input | Type | Required |
|---|---|---|---|
| `get_submittal_user_context` | `project_id` | `str` | yes |
| `list_submittals` | `project_id` | `str` | yes |
| | `limit` | `int \| None` | no |
| | `offset` | `int \| None` | no |
| `get_submittal` | `project_id` | `str` | yes |
| | `submittal_id` | `str` | yes |

**No** search input · **no** filter map · **no** sort · **no** package filter ·
**no** state or status filter · **no** generic query parameters · **no**
caller-supplied URL, path, method or body · **no** `**kwargs`.

### Project-ID contract

**Project ids are accepted with or without the `b.` prefix and normalised by
stripping it** — the accept-either discipline already used by
`transmittals_client` and `rfis_client`, and deliberately **not**
`aps_client._project_to_container_id`, which raises when the prefix is absent.

Validation is **capability-local**, with an allowlisted path-character set so no
value reaches a URL path unvalidated. **No shared normalisation refactor** is
introduced: per-client duplication is the established discipline here.

`submittal_id` is a required non-empty string with the same capability-local
path-character validation.

**Validation errors never echo the supplied identifier or value.**

### Pagination contract

The RFI sibling encodes a documented minimum, maximum and default. **Submittals
cannot, because its maximum page size is unknown.** The contract differs
accordingly:

- **`limit` omitted → the parameter is not sent.** No local default is
  substituted.
- **`offset` omitted → the parameter is not sent.**
- **No local maximum.** `50`, `200` and any other bound are **not** encoded. A
  service-defined bound is enforced by the service, and its rejection flows
  through the `bad request` classification below.
- **Local input hygiene only:** `limit` must be an integer `>= 1`; `offset` must be
  an integer `>= 0`. **Booleans are rejected** — `bool` is an `int` subclass, and
  `limit=True` is a caller mistake, not a page size.
- **Values are never clamped.** An out-of-range value is a structured error.

The observed no-parameter response carried `limit` 20. **That is recorded as
observed evidence and does not become a local contract default.**

**The `limit >= 1` floor is this project's input-hygiene rule, not an assertion
about the upstream accepted range.** `limit=1` was verified accepted; `limit=0` was
never tested and may well be upstream-valid. The rule forgoes nothing a caller
legitimately wants, and it is recorded as ours rather than Autodesk's.

Pagination output is allowlisted through, never reconstructed:

```
pagination: { limit: int|None, offset: int|None, total_results: int|None }
```

mapped from `limit`, `offset` and `totalResults` under the shape rules below.

### `get_submittal_user_context` — caller-context DTO

Exactly three fields:

| Field | Type | Source |
|---|---|---|
| `submittals_available` | `bool` | derived |
| `permitted_action_count` | `int` | `len(permittedActions)` |
| `role_count` | `int` | `len(roles)` |

**A successful caller-context DTO requires all of:**

1. the upstream body is an object;
2. `permittedActions` **exists and is an array**;
3. `roles` **exists and is an array**.

**If that required structural shape is invalid, the operation returns
`MALFORMED_ERROR`. It does not emit a normal DTO with zeroed counts.** A missing or
wrongly-typed capability array is a transport-contract violation, not a caller with
no permissions, and the two must never be conflated.

For a structurally valid response, `submittals_available` is `true` and the two
counts are the array lengths. **Empty arrays legitimately yield zero counts.**

**`submittals_available` has no successful `false` state in v1.** Its meaning is:
*the caller successfully obtained a structurally valid, readable Submittals context
for this project.* Permission, authentication and module-availability failures
remain **structured errors**, never a `false` value.

**Never exposed:** caller `id` · `roles` values · `permittedActions` objects ·
`fields` · `mandatoryFields` · `transitions` · action ids · `stateFrom` /
`stateTo` · `transitionFields`.

### `list_submittals` — list DTO

**Exactly eight fields per result:**

| # | Field | Source | Type |
|---|---|---|---|
| 1 | `submittal_id` | `id` | `str`, **required, non-empty** |
| 2 | `identifier` | `identifier` | `int \| None` |
| 3 | `custom_identifier` | `customIdentifier` | `str \| None` |
| 4 | `title` | `title` | `str \| None` |
| 5 | `state_id` | `stateId` | `str \| None` |
| 6 | `status_id` | `statusId` | `str \| None` |
| 7 | `revision` | `revision` | `int \| None` |
| 8 | `due_date` | `dueDate` | `str \| None` |

Response shape: `{ results: [ …eight-field DTO… ], pagination: {…} }`.

### The `customIdentifier` disambiguation

The upstream payload carries **two distinct keys**, `customIdentifier` and
`customIdentifierHumanReadable`. An earlier provisional design named a field
`custom_identifier` while sourcing it from `customIdentifierHumanReadable`. **That
mapping is rejected.**

**Every contract field maps 1:1 to the upstream key it is named after:**

- `custom_identifier` maps **only** from `customIdentifier`;
- `custom_identifier_human_readable` maps **only** from
  `customIdentifierHumanReadable`.

The list carries `custom_identifier` alone — the canonical project-scoped
identifier. The human-readable form is a presentation transform and belongs with
the fuller detail record.

### `get_submittal` — detail DTO

**Exactly seventeen fields:**

| # | Field | Source | Type |
|---|---|---|---|
| 1 | `submittal_id` | `id` | `str`, **required, non-empty** |
| 2 | `identifier` | `identifier` | `int \| None` |
| 3 | `custom_identifier` | `customIdentifier` | `str \| None` |
| 4 | `custom_identifier_human_readable` | `customIdentifierHumanReadable` | `str \| None` |
| 5 | `title` | `title` | `str \| None` |
| 6 | `description` | `description` | `str \| None` |
| 7 | `state_id` | `stateId` | `str \| None` |
| 8 | `status_id` | `statusId` | `str \| None` |
| 9 | `revision` | `revision` | `int \| None` |
| 10 | `priority` | `priority` | `str \| None` |
| 11 | `spec_identifier` | `specIdentifier` | `str \| None` |
| 12 | `spec_title` | `specTitle` | `str \| None` |
| 13 | `due_date` | `dueDate` | `str \| None` |
| 14 | `submitter_due_date` | `submitterDueDate` | `str \| None` |
| 15 | `ball_in_court_type` | `ballInCourtType` | `str \| None` |
| 16 | `created_at` | `createdAt` | `str \| None` |
| 17 | `updated_at` | `updatedAt` | `str \| None` |

**Deliberately excluded, each for a stated reason:**

- **`spec_id`** — v1 exposes no operation that consumes or resolves `specId`. The
  caller already receives the operational values `spec_identifier` and
  `spec_title`; an opaque relationship id with no v1 consumer adds nothing.
- **`type_id`** — the same minimality principle. There is no `type_name` and no
  item-types operation in scope, so it would be an opaque id a caller cannot
  resolve.
- **`subsection`** — observed **only as `null`**. Its populated type has never been
  seen, and freezing a field of unobserved type is the failure
  [ADR-0012](0012-refine-rfi-search-contract-from-runtime-verification.md) exists
  to prevent.
- **`manager_type`, `subcontractor_type`** — manager and subcontractor identities
  are excluded, so these describe the *category of an unnamed party* and support no
  caller decision. `ball_in_court_type` is retained because it describes the
  **currently pending action** — live workflow state — rather than a party.

**Also excluded:** all raw person identities · all company identities ·
`permittedActions` · `watchers` · every ball-in-court array · `sentToSubmitter` ·
workflow history · response fields · package fields · folder and storage fields ·
`customAttributes` · revision-folder structures.

### List versus detail semantics

**The upstream list row and the direct detail response were observed as the same
56-key schema for the controlled fixture** — identical key sets, identical types
for every shared key.

**`get_submittal` is therefore NOT adopted on the grounds that it returns a richer
Autodesk representation.** That was not observed and the evidence contradicts it.
It is retained because:

1. it provides **direct access to one known Submittal without paging the
   collection**, which is role-scoped; and
2. it **independently exercises the canonical detail route**.

Our two caller projections differ deliberately — **8 fields for discovery, 17 for
inspection** — even though the upstream documents do not. That is a product
decision about discovery versus inspection, not a reflection of an upstream
summary/detail split.

### Nullability and shape enforcement

Every DTO is a **new dict built key by key from a closed allowlist**. An upstream
row is never returned, spread, merged or copied, so **unexpected upstream keys are
ignored and can never leak** — the 56-key document cannot pass through. This is the
`rfis_client` discipline, and ADR-0012's finding that the client allowlist is the
authoritative caller-facing boundary applies directly.

**Field rules — a wrong type fails closed:**

| Upstream condition | Result |
|---|---|
| field absent | `None` |
| field present and `null` | `None` |
| field present, non-null, **expected type** | the value |
| field present, non-null, **wrong type** | **`MALFORMED_ERROR`** |

**A present value of the wrong type is a transport-contract violation and must not
be silently coerced or erased to `None`.** `identifier` as a non-integer, `stateId`
as a non-string, `revision` as a non-integer and `dueDate` as a non-string each
produce `MALFORMED_ERROR`. **`bool` never satisfies an integer contract.**

**`submittal_id` is required**: the key must exist and its value must be a
non-empty string, or the response is `MALFORMED_ERROR`.

**Structural requirements:**

- caller context — body is an object; `permittedActions` and `roles` are arrays
- list — body is an object; `results` is an array; `pagination` is an object
- detail — body is an object

**Pagination fields** follow the same rule: `limit`, `offset` and `totalResults`
map to `None` when absent or upstream-null, to an integer when present and correct,
and to `MALFORMED_ERROR` when present with a wrong non-null type. **Pagination
values are never defaulted.**

**No coercion anywhere:** never `null → ""`, `null → 0`, `null → false`. The only
derived values in the contract are the three caller-context fields, which are a
boolean and two counts by definition.

### State and status typing

`state_id` and `status_id` are typed **`str | None`**.

The contract **does not** enumerate legal values, **does not** encode the
undocumented fuller state sequence, **does not** type `statusId` as an integer, and
**does not** treat it as ordinal or sortable.

The controlled observation — `stateId` `"sbc-1"` and `statusId` `"1"`, recorded
while the product interface displayed *Required / Waiting for submission* —
belongs to **evidence and governance only** and must not become restrictive runtime
validation.

### Participants, identities and companies

**Excluded from every first-slice output:** `manager` · `subcontractor` ·
`createdBy` · `updatedBy` · `submittedBy` · `publishedBy` · `respondedBy` ·
`sentToReviewBy` · `ballInCourtUsers` · `watchers` · `ballInCourt` ·
`ballInCourtRoles` · the caller `id` · `roles` values.

**Company:** `ballInCourtCompanies`, company identities and commercial assignment
relationships are excluded. **No company DTO is invented** — the company member
shape was never observed.

**No `USER_n` or `COMPANY_n` concept appears in any runtime DTO.** Aliases are
**public-evidence** constructs under ADR-0013. An authenticated caller receives
real values; the repository publishes aliases. Conflating the two would be a
category error in both directions.

**`ball_in_court_type` is the only retained categorical discriminator.**

### Timestamps and the timeline boundary

**No history or timeline object.** Upstream chronology is a set of flat sibling
fields and stays that way.

The slice adopts exactly four: `due_date`, `submitter_due_date`, `created_at`,
`updated_at`. **No lateness, duration, interval, ordering or workflow-progression
inference** is derived from them.

**`sentToSubmitter` is excluded.** The controlled fixture proved it can be
populated while the item remains in *Required / Waiting for submission* with
`submittedBy` still `null`: it records **routing to the submitter, not submission
by the submitter**. Its presence must never be interpreted as proof of submission,
and exposing a field whose name invites that reading would be a defect.

### `permittedActions`

**Excluded entirely, at both caller scope and item scope.** This covers the objects
and every part of them: member `id` values, `fields`, `mandatoryFields`,
`transitions`, `actionId`, transition `name`, `stateFrom`, `stateTo` and
`transitionFields`.

**`permittedActions` is write-capability and workflow-configuration metadata, not
the read-resource projection.** Each member describes which workflow transitions
the caller may perform and what each requires; collectively the transition maps are
the project's submittal state machine. It reads as harmless permissions metadata,
which is precisely why the exclusion is recorded explicitly.

An earlier provisional design proposed exposing flat action strings, inferred from
a vendor blog sentence. **Runtime evidence refuted that shape** — 36 nested objects
at caller scope, 16 at item scope. The caller context retains
`permitted_action_count` and nothing else.

### Authentication and scope

**The proven first-slice scope is `data:read`.** All three operations returned HTTP
200 under a three-legged token whose granted scope claim was exactly `data:read`.

The existing three-legged Authorization-Code lifecycle in `aps_client` is reused.
**No `client_credentials`, no Secure Service Account, no second token store.**
`x-user-id` is a two-legged header and is never sent.

**The normal MCP server grant currently holds a broader four-scope configuration
for other capabilities. That is server configuration and does not widen the
Submittals requirement.** Server grant configuration and minimum proven first-slice
scope are separate facts and must not be conflated.

### Transport architecture

**No `x-ads-region`.** The runtime probes succeeded against the global host with
only `Authorization`, matching `rfis_client`, `reviews_client` and
`transmittals_client`, and differing from `forma_client`, which sends the header
because Site Design requires it.

### Errors and logging

**The existing capability-local RFI error model is adopted unchanged in structure.
No new global error architecture and no shared refactor.**

Permitted local envelope keys: `error`, `status`, `detail`, `retry_after`.

Classification: input validation · authentication and token failure · `400` bad
request · `401` authentication failed · `403` permission denied, whose detail also
names that the Submittals module may not be active for the project · `404` not
found · `429` rate limited with safe `Retry-After` handling only · transport
failure · `MALFORMED_ERROR` for a body that violates the contract · other upstream
failures per sibling precedent.

**Never exposed to a caller or into evidence:** the raw Autodesk error body ·
headers · the resolved URL · tokens · identifiers · upstream diagnostic payloads.
**Input-validation messages never echo supplied identifiers or values.**

**Logging is strictly narrower than the returned output:** operation name, outcome
status and bounded counts only — never project or submittal identifiers, custom
identifiers, titles, descriptions, spec values, participant values, dates, tokens,
Authorization headers, request or response bodies, or resolved URLs.

### Implementation boundary

This ADR **prescribes** the later implementation and **authorises none of it to be
written**:

- a **dedicated `submittals_client.py`**;
- **GET-only**, three internal helpers hardwired to three fixed routes;
- **no generic request helper**, and no caller-supplied URL, path, method, body or
  `**kwargs`;
- **no shared-client refactor** and **no transport-abstraction expansion**;
- **no write helpers** of any kind;
- **capability-local** project and identifier validation;
- reuse of the existing APS three-legged lifecycle; no `x-user-id`; no
  `x-ads-region` for the verified first slice;
- eventual registration of the three MCP tools.

**No MCP code is written by this ADR. The tool count remains 38.**

### Gate 5 versus Gate 6 — public evidence versus caller output

**ADR-0013 governs public repository evidence. This ADR governs authenticated
runtime caller output. These are deliberately different boundaries.**

An authenticated caller holding `data:read` **already has role-scoped access** to
the values this contract returns, so returning them discloses nothing new.
Publishing them into a public repository would disclose them to everyone,
permanently.

The runtime caller may therefore legitimately receive real submittal identifiers,
`identifier`, custom identifiers, `title`, `description`, `priority`, spec
identifier and title, and dates — **while those same values remain forbidden or
reduced to presence booleans under ADR-0013 for public evidence.** `priority` is
the clearest case: adopted here, explicitly omitted there.

**This is intentional. ADR-0013 is not weakened, amended or reinterpreted**, and
nothing in this ADR relaxes it.

### Capability adoption

A capability record is added to the schema-v2 workflow contract:

```yaml
- id: submittals
  primary_system: Forma Build
  api_family: Autodesk Forma Build Submittals API
  api_version: v2
  api_maturity: ga
  mcp_component: aps-forma-mcp
  mcp_implementation_status: planned
  data_readiness: not-assessed
```

`api_family` is asserted because it is verified from official Autodesk/APS
documentation (§4, §6). `api_version` is **required** because `api_maturity: ga` is
a concrete lifecycle assertion ([ADR-0009](0009-define-capability-record-cardinality-for-schema-v2.md)).
`mcp_implementation_status: planned` is the vocabulary's value for **no MCP tool
yet** — not `partial`, which describes a capability whose own tool surface is
partly built. `data_readiness: not-assessed` is never derived from implementation
status. **`data_readiness_reason` is omitted**, since it is optional and is never
invented where none exists.

The semantics are: **contract adopted and governed; zero Submittals MCP tools
exist; implementation planned; Gate 8 open; data readiness not assessed.**

## Constraints

This ADR explicitly does **not** claim:

- that any implementation exists;
- that the MCP tool count has changed — **it remains 38**;
- that Gate 8 is passed;
- that any live MCP evidence exists;
- that writes are supported or authorised;
- that packages are supported;
- that the review workflow is supported;
- that responses are supported;
- that attachments or comments are supported;
- that templates, settings or mappings are supported;
- that item-type operations are supported;
- that spec-section management is supported;
- that the controlled synthetic fixture is anything other than **diagnostic
  input**.

## Consequences

- **Submittals Gate 6 is closed** — the §16 gate table records `passed`, with the
  closure subsection at §16.10 and the contract recorded in
  [COMPONENT_BOUNDARIES.md](../architecture/COMPONENT_BOUNDARIES.md) §6.3.
- **Submittals becomes the third governed Phase 4A capability**, with a capability
  record in the workflow contract for the first time.
- **Gate 8 remains unresolved**, `mcp_implementation_status` is `planned`, and
  `data_readiness` is `not-assessed`.
- **A governed contract now exists with no code behind it.** That is exactly what
  `planned` means and how RFIs were governed at the equivalent stage, but it is
  stated plainly so no reader infers that a tool exists.
- **This ADR authorises no implementation, no Autodesk call, no fixture change, no
  evidence artifact, and no other gate closure.**

## Deferred surfaces

Not adopted, and not prohibited from later deliberate adoption through the same
governance route: packages · spec sections as independent operations · item types ·
responses · review steps · attachments · comments · revisions as independent
operations · templates · settings and mappings · custom identifier operations ·
metadata · **and every write operation**.

## Rejected alternatives

- **Naming the tools `list_submittal_items` / `get_submittal_item`.** The component
  already uses "item" for Data Management resources; this would recreate the
  `ITEM_n` / `SUBMITTAL_n` domain collision in the tool namespace.
- **Freezing the provisional `custom_identifier` ← `customIdentifierHumanReadable`
  mapping.** Two distinct upstream keys exist; a name must map to the key it is
  named after.
- **Encoding a maximum page size** of 50, 200 or any other value. The maximum is
  unknown, and an unverified bound in a contract is a fabricated constraint.
- **Applying a local default limit.** Substituting a number locally would
  manufacture a documented default this project cannot document.
- **Silently coercing a wrong-typed present value to `None`.** That erases a
  transport-contract violation and hands the caller a plausible-looking absence.
- **Returning a caller-context DTO with zeroed counts when the capability arrays
  are missing or wrongly typed.** A malformed body is not a caller without
  permissions.
- **Retaining `spec_id`, `type_id`, `subsection`, `manager_type` or
  `subcontractor_type`** — no v1 consumer, unobserved type, or description of a
  deliberately unnamed party.
- **Exposing `permittedActions` as permissions metadata.** It is a write-capability
  and workflow-configuration descriptor.
- **Justifying `get_submittal` as a richer upstream read.** The two documents were
  observed identical.
- **Enumerating `sbc-1` as the only legal state, or typing `statusId` as an integer
  or an ordinal.** One observation establishes no vocabulary.
- **Including `sentToSubmitter`.** It was populated before submission on the
  controlled fixture.
- **Weakening ADR-0013 so the public-evidence profile resembles the caller DTO.**
  The boundaries differ by design.
- **A shared or generic client, or a transport-abstraction refactor.** Capability
  isolation is the established discipline.

## Interaction with existing ADRs

- **[ADR-0007](0007-read-write-classification-by-state-semantics.md)** —
  referenced, not exercised. All three operations are `GET`, so no endpoint-level
  read approval for a non-GET verb is required or granted.
- **[ADR-0008](0008-govern-implementation-state-per-capability.md)** and
  **[ADR-0009](0009-define-capability-record-cardinality-for-schema-v2.md)** — the
  capability record follows both. No vocabulary is invented and no axis is
  conflated.
- **[ADR-0011](0011-adopt-rfi-first-slice-mcp-contract-and-component-boundary.md)**
  — the structural precedent for a first-slice contract closing Gate 6. **Not
  superseded, not amended.**
- **[ADR-0012](0012-refine-rfi-search-contract-from-runtime-verification.md)** —
  its discipline is followed throughout: unverified transport assumptions are not
  converted into contract, and the client allowlist is the authoritative boundary.
- **[ADR-0013](0013-approve-submittals-public-evidence-sanitisation-profile.md)** —
  **unchanged and unweakened.** It governs public evidence; this ADR governs caller
  output.

**This ADR supersedes nothing.**

## Follow-up

None of the following is authorised by this ADR:

1. **Submittals MCP implementation** — no client, tool or helper may be written on
   this authority.
2. **Submittals Gate 8** — module activation, workflow configuration, permissions,
   fixture suitability and data readiness.
3. **Any live-verification claim** or Phase 4 Submittals evidence artifact.
4. **Any deferred surface** listed above, and any write operation.

Separately, the following known documentation defects are **deferred** and
deliberately not addressed here: the RFI Gate-2 row in the §16 table; the stale
RFI pre-implementation paragraph and the stale tool count in
`COMPONENT_BOUNDARIES.md` §3 and §6; the §6 `filter[reviewResponseId]` /
`filter[responseId]` discrepancy; and the §6 `GET items` 1–50 pagination claim,
which is verified only for sibling endpoints. Each belongs to its own correction
increment.
