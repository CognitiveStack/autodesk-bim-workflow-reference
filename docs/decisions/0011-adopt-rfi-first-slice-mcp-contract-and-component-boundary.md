# ADR-0011: Adopt the RFI first-slice MCP contract and component boundary

## Status

Accepted

## Date

2026-07-28

## Context

> **Numbering note.** This is **reference-repo ADR-0011**. The APS/Forma MCP
> component repository maintains its own, independent ADR series.

RFIs are an adopted governed capability (`api_family: Autodesk Forma Build RFI
API`, `api_version: v3`, `api_maturity: ga`), with **Gate 5 passed** under
[ADR-0010](0010-approve-rfi-public-evidence-sanitisation-profile.md) and **Gate 6
open**. `mcp_implementation_status` is `planned` and `data_readiness` is
`not-assessed`.

Gate 6 is the component-boundary and caller-facing-contract decision. It must be
taken before implementation because it fixes an **externally visible MCP tool
surface**, and because two questions cannot be deferred safely: how much RFI
narrative an authenticated caller receives, and how a read-semantic POST is
carried without creating a generic request capability.

The adopted first read-only slice is `GET users/me`, `POST search:rfis`,
`GET rfis/:rfiId`.
[ADR-0007](0007-read-write-classification-by-state-semantics.md) already approves
`POST …/search:rfis` at endpoint level as read-semantic. Verified against the
normative Reference Guide: the page's display title is "POST rfi-search" — a
documentation slug — while its Method-and-URI block, the only authoritative route
statement on that page, reads
`https://developer.api.autodesk.com/construction/rfis/v3/projects/:projectId/search:rfis`.
**ADR-0007's route is correct and is not amended.**

Component inspection established three facts that shape this decision:

- The component has **two output conventions**: Reviews and Model Coordination
  normalise with an explicit allowlist inside the client; Transmittals preserves
  the raw Autodesk shape, a departure its own docstring justifies by
  version-domain fidelity for the exact-version proof.
- The only authenticated POST, `forma_client.forma_post`, hard-codes
  `x-ads-region` and an `authcontext` query parameter — **Site Design semantics**
  that the Transmittals, Reviews and Model Coordination clients explicitly do not
  send.
- Project IDs already have a precedent for RFI's requirement:
  `transmittals_client._normalise_project_id` accepts either form and strips
  `b.`, which is exactly what the RFI route needs.

## Decision

### Component ownership

**`aps-forma-mcp` owns RFI.** No separate MCP server. The implementation boundary
is a **dedicated `src/mcp_forma/rfis_client.py`**. RFI semantics are placed in no
existing client — not Data Management, Site Design, Transmittals, Reviews,
Relationships or Model Coordination — and in no generic request infrastructure.

### Client normalisation

**`rfis_client` normalises with an explicit allowlist and returns a curated
representation, not a raw Autodesk payload.** This follows the Reviews and Model
Coordination convention. RFI is narrative- and person-data-heavy and has no
raw-fidelity requirement comparable to the Transmittals exact-version proof, so
the narrowest safe enforcement point is the client itself. **The Transmittals
raw-client pattern is unchanged and remains a deliberate special case.**

### V1 first-slice tool surface

The adopted **v1 first slice** is exactly three semantic tools:
**`get_rfi_user_context`**, **`search_rfis`**, **`get_rfi`**.

Not in v1: `list_rfis`, `get_rfi_responses`, `get_rfi_comments`,
`get_rfi_attachments`, `get_rfi_types`, `get_rfi_workflow`, `get_rfi_attributes`,
and every write tool. **No tool accepts a caller-supplied URL, path, HTTP method
or raw request body.**

"Exactly three" scopes the **v1 first slice**. It is not a permanent prohibition:
a later surface may be adopted deliberately, with its own API and tool boundary,
through the same governance route.

### `get_rfi_user_context`

**Input:** `project_id`.

**Output:** `project_role` · `workflow_type` · `can_create_rfi` ·
`permitted_statuses` · `max_assignees` · `required_attribute_names` ·
`permitted_attribute_names` · `allowed_value_count`.

**Not returned in v1:** `user.name`, `user.id`, email/contact fields, and every
attribute value operand carrying user, company or role identifiers. No adopted v1
operation takes a user identity as input.

### `search_rfis`

Purpose: paginated discovery of visible RFIs and selection of the RFI to pass to
`get_rfi`.

**Inputs:** `project_id` (required) · `limit` (1–200, Autodesk documented default
10) · `offset` (≥ 0). **Deferred from v1:** `statuses`, free-text `search`,
workflow filters, any other filter, raw JSON body, caller-defined projection.
Discovery works without them, and a narrow read boundary should be established
before query semantics expand.

**Upstream collection-time minimisation.** The search request uses Autodesk's
server-side field projection to request only the discovery field set:
**`id`, `customIdentifier`, `title`, `status`, `workflowType`**. Narrative beyond
`title` is never fetched.

**Projection encoding is deliberately not fixed here.** The normative
documentation describes `fields` as a request-body array while its worked example
is written in query-string form. This ADR approves the **semantic field set**
only; the **exact transport encoding is deferred to implementation-time
verification** against the reference documentation. No encoding is guessed.

**Caller output:**

```
items: [ { id, custom_identifier, title, status, workflow_type } ]
pagination: { limit, offset, total_results }
```

**Why `title` is exposed in search.** `title` is narrative-like project data that
ADR-0010 prohibits in **public evidence**. An authenticated caller with Autodesk
permission may receive it, and here it has a clear functional purpose: it lets the
caller choose the correct RFI **without issuing `get_rfi` for every opaque
identifier**. Exposing it is what makes the no-fan-out design workable.

**Why `custom_identifier` is exposed in search.** It is the human-facing RFI
reference used to reconcile tool output with the Forma UI and project
correspondence.

**Transport.** `POST …/search:rfis`, **read state semantics** under ADR-0007. It
is not a write merely because the HTTP verb is POST.

### `get_rfi`

**Inputs:** `project_id`, `rfi_id`. No caller-controlled field projection, no raw
body option.

**Curated caller DTO:** `id` · `custom_identifier` · `title` · `question` ·
`status` · `previous_status` · `workflow_type` · `official_response` ·
`official_response_status` · `suggested_answer` · `priority` · `cost_impact` ·
`schedule_impact` · `created_at` · `updated_at` · `due_date` · `answered_at` ·
`closed_at` · `answered` · `closed` · `response_count` · `response_states` ·
`response_statuses` · `comment_count` · `assignee_count` · `reviewer_count` ·
`watcher_count`.

Exact JSON key spelling is an implementation detail where repository convention
requires it; the semantic field set above is the approved contract.

### Core RFI narrative

The authenticated `get_rfi` caller receives **`title`, `question`,
`official_response` and `suggested_answer`** where those values exist and the
Autodesk caller is authorised to see them. The question and its governed answer
are core RFI semantics. **ADR-0010's narrative restrictions govern public
evidence, not authenticated operational use**, and core narrative is not removed
from `get_rfi` merely because public evidence sanitises it. **This weakens
ADR-0010 in no respect.**

### Embedded responses

`GET rfis/:rfiId` may embed `responses[]`. The v1 caller contract **does not
expose** `responses[].text`, `responses[].createdBy`, `responses[].onBehalf`, raw
response records, or response IDs. It exposes **structural summary only**:
`response_count`, `response_states`, `response_statuses`.

**CORE RFI NARRATIVE and EMBEDDED RESPONSE NARRATIVE are different contract
domains.** Core RFI narrative is part of the adopted RFI caller contract. Embedded
response narrative belongs to an **unadopted Response surface**; its data arrives
incidentally inside the RFI representation, and exposing it would silently expand
the governed caller contract. `official_response` remains allowed because it is a
field of the RFI record itself. A later Response-surface adoption may revisit
this.

### Participants and actor identities

V1 returns **counts**: `assignee_count`, `reviewer_count`, `watcher_count`. Raw
arrays and identifiers are not exposed for `assignedTo`, `managerId`,
`constructionManagerId`, `architects`, `reviewers`, `coReviewers`, `watchers`,
`officialResponseActors`, `createdBy`, `updatedBy`, `answeredBy` or `closedBy`.

**No adopted v1 tool resolves participant identities, and no first-slice use case
requires those identifiers.** Any future participant-resolution capability must be
adopted deliberately, with its API and tool boundary settled, before participant
identifiers are added to the caller contract.

### `customIdentifier`

Exposed as **`custom_identifier`** in authenticated `search_rfis` and `get_rfi`;
**omitted from public evidence** under ADR-0010. This is the explicit example of
**operational caller output ≠ public evidence publication**.

### Timestamps

Authenticated `get_rfi` may expose `created_at`, `updated_at`, `due_date`,
`answered_at` and `closed_at`. **No participant identities are paired with them in
v1**, so the person-linked-chronology concern that drives ADR-0010's evidence
reduction does not arise on the caller path. ADR-0010 is unchanged.

### Authentication

The existing **3-legged Authorization-Code user-context token** with `data:read`
is sufficient for all three tools. **No `client_credentials`**, and **no Secure
Service Account** is added in this slice. Absence, expiry and lock contention
surface through the component's existing structured envelope. Consistent with the
component's recorded operational behaviour, a provisioning change — RFI module
activation or workflow-role assignment — may require a fresh interactive login
rather than a token refresh; this is an operator note, not a new code path.

### Project-ID contract

Tool input accepts **`b.<uuid>` or `<uuid>`**, and the `b.` prefix is stripped
internally for RFI v3 route construction, following the Transmittals
normalisation precedent. No caller transforms the project ID returned by existing
project-discovery tools.

### Transport architecture

```
semantic MCP tool → rfis_client → bounded authenticated transport → RFI v3
```

`rfis_client` owns base-path construction, endpoint-specific request
construction, the typed search payload, the field projection, response
normalisation and error normalisation. It accepts no raw path, URL, method or
body.

- **GET** reuses the existing bounded authenticated GET pattern.
- **Search POST** uses a **private, endpoint-specific helper hardwired to
  `search:rfis`**, with no `method`, `path`, URL, raw-body or
  passthrough-kwargs parameter.
- **`forma_post` is not reused** — it carries Site Design `x-ads-region` and
  `authcontext` semantics — **and is not generalised in this slice**, because a
  shared POST substrate between a Beta write client and a GA read client is
  precisely what ADR-0007's endpoint-specific constraint exists to prevent.

### Errors and logging

Reuse the existing component error model and category vocabulary
(`authentication failed`, `authentication unavailable`, `permission denied`,
`not found`, `rate limited`, `invalid request`, `transport error`, `timeout`,
`malformed response`, `invalid project id`, `invalid rfi id`, `invalid limit`,
`invalid offset`). **No parallel error framework.** Never exposed: tokens,
headers, raw upstream response bodies, identifier-bearing URLs, or the offending
raw identifier in a validation error.

Normal logging carries operation name, HTTP status and bounded counts only.
**No raw RFI response body at normal log levels**, and no `question`,
`officialResponse`, `responses[].text`, personal name, user ID or token. Existing
`httpx`/`httpcore` suppression is preserved.

### Pagination and fan-out

`limit` 1–200, default 10; `offset` ≥ 0. **No automatic fetch-all, no next-page
recursion, no automatic `get_rfi` for every search result, no bulk crawling.** One
explicit API operation per tool invocation. This matters because the RFI request
budget applies across the whole module rather than per endpoint.

### Relationship to Gate 5

Two flows remain distinct:

```
authenticated:   Autodesk raw → rfis_client curated allowlist → MCP caller
public evidence: curated data → ADR-0010 projection → aliases/reductions → evidence
```

The authenticated caller receives real operational RFI IDs, `custom_identifier`,
`title` and approved core narrative. **`RFI_n` aliases are never returned to the
normal MCP caller** — aliasing belongs to the evidence path under ADR-0010.

### Read-state semantics

`get_rfi_user_context` (GET, read) · `search_rfis` (POST, read-semantic under
ADR-0007) · `get_rfi` (GET, read). No `POST rfis`, `PATCH rfis/:id`, response or
comment creation, attachment mutation, or custom-attribute mutation.

## Constraints

- **This ADR authorises no implementation.** `mcp_implementation_status` remains
  `planned`; `data_readiness` remains `not-assessed`; Gate 8 remains unresolved.
- **No MCP_Forma file is changed by this decision**, and no RFI client, tool, test
  or fixture exists.
- **No workflow-contract change** is required to close Gate 6.
- **No live Autodesk call, fixture or evidence artifact** is authorised.
- **Gate 6 closure approves the external tool and component contract. It does not
  prove that any implementation conforms to that contract** — that proof comes
  later, through code, tests and live verification as appropriate.

## Consequences

- **RFI Gate 6 is closed** as a governance and component-boundary gate.
- **The externally visible RFI MCP contract is fixed at three read tools, so
  implementation can proceed against an approved governance contract.
  Implementation-time details and actual API behaviour must still be verified, and
  any material conflict must return to governance rather than silently changing
  the contract.** The deferred `fields` projection encoding is the known instance
  of this.
- **Search is a genuine discovery operation** — `custom_identifier` and `title`
  let a caller choose one RFI, which is what makes the one-call-per-invocation
  fan-out policy workable.
- **`forma_post` remains Site-Design-only**, and the RFI POST is
  endpoint-specific, so no generic request capability is created.
- The allowlist-in-client decision means narrative reaches a caller only through
  explicitly named fields.
- **Gate 8 is untouched** — module activation, workflow configuration,
  permissions, a controlled fixture and data readiness all remain to be
  established.

## Deferred surfaces

`statuses` filter · free-text search · other search filters · RFI writes · RFI
Response operations · embedded response narrative · comments · attachments · RFI
types · workflow endpoint · attributes · custom-identifier endpoint ·
participant-directory resolution · webhooks · bulk crawling.

**Deferred means not in v1. It does not mean permanently prohibited** — each may
be adopted later through deliberate governance.

## Rejected alternatives

- **Returning only `id`, `status`, `workflow_type` from search.** Too weak for
  discovery: a caller would have to fetch every RFI to find the right one, which
  defeats the no-fan-out policy.
- **Exposing embedded response narrative in v1.** It would silently widen the
  adopted slice to a surface that was deliberately excluded.
- **Withholding core narrative from `get_rfi`.** Minimisation without purpose; the
  caller is already permitted to read it, and the tool would not convey what an
  RFI is.
- **Reusing or generalising `forma_post`.** It carries Site Design region and
  `authcontext` semantics, and generalising it would create a shared POST
  substrate across a Beta write client and a GA read client.
- **A caller-supplied `fields` parameter.** A partial arbitrary-request surface.
- **Guessing the `fields` transport encoding.** The normative documentation is
  ambiguous; approving a semantic set and verifying the encoding at
  implementation time is the honest treatment.
- **Returning raw Autodesk payloads (the Transmittals pattern).** Justified there
  by version-domain fidelity; RFI has no such requirement and is
  narrative-heavy.
- **Returning `RFI_n` aliases to the caller.** Aliases are an evidence-path
  construct; operational tools need real identifiers.
- **Adding `statuses` to v1.** Extra workflow-type-dependent validation surface
  for no discovery benefit.

## Interaction with existing ADRs

- **[ADR-0004](0004-adopt-transmittals-as-first-phase-4a-read-slice.md)** — the
  Transmittals Gate 6 precedent for a dedicated component-boundary ADR.
  Transmittals-specific semantics (raw-shape client, exact-version evidence) are
  **not** extended to RFI. Not amended.
- **[ADR-0007](0007-read-write-classification-by-state-semantics.md)** — supplies
  the endpoint-level approval for `POST search:rfis`. This ADR implements that
  approval with an endpoint-specific client helper and **verifies the route
  unchanged**. Not amended.
- **[ADR-0008](0008-govern-implementation-state-per-capability.md)** —
  implementation state belongs to the capability record and **remains `planned`**.
  Not amended.
- **[ADR-0009](0009-define-capability-record-cardinality-for-schema-v2.md)** —
  capability cardinality unaffected; no workflow-contract change. Not amended.
- **[ADR-0010](0010-approve-rfi-public-evidence-sanitisation-profile.md)** —
  governs the **public-evidence** path. This ADR governs the **authenticated
  caller** path. `custom_identifier` and `title` are the explicit cases where the
  two differ. ADR-0010 is not weakened, amended or superseded.

**This ADR supersedes nothing.**

## Follow-up

None of the following is authorised by this ADR:

1. **RFI MCP implementation** — `rfis_client`, tool registrations and tests.
2. **Implementation-time verification of the `fields` projection encoding**, with
   any material conflict returned to governance.
3. **RFI Gate 8** — module activation, workflow configuration, permissions, a
   controlled fixture and data readiness.
4. **The Gate-5 evidence projection** and any RFI evidence artifact.
5. **Any deferred surface** listed above.
6. **Transition of `mcp_implementation_status`** away from `planned`.
