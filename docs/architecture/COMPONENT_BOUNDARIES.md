# Component Boundaries and Capability Ledger

**Status:** Confirmed component capability inventory
**Inventory verified:** 2026-07-27 (APS/Forma MCP re-verified locally at
`295c253`, pinned at `6ec6411`); Revit MCP unchanged (`ae01d29`, 2026-07-22)

This document is the authoritative, dated ledger of the MCP capabilities this
project depends on, and the anti-duplication contract between this orchestration
layer and the two MCP components. It is consistent with the
[PRD](../prd/PRD_AUTODESK_BIM_WORKFLOW_REFERENCE_IMPLEMENTATION.md),
[SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md), and
[REPOSITORY_STRATEGY.md](REPOSITORY_STRATEGY.md), and is governed by
[ADR-0001](../decisions/0001-orchestration-layer-not-mcp-server.md) and
[ADR-0002](../decisions/0002-multi-repo-no-submodules.md).

## 1. Inventory provenance

| Component | Repository | Inspected commit | Tools |
|---|---|---|---|
| APS/Forma MCP | `CognitiveStack/autodesk-aps-forma-mcp` | `6ec6411` | 35 |
| Revit MCP | `CognitiveStack/revit-mcp-triviron` | `ae01d29` | 14 |

The APS/Forma MCP inventory is published at
`6ec64110f506ff96ac5744c5e6481c13a3f43806` and reports **35 MCP tools total**:
33 read-only Autodesk tools, 1 guarded Autodesk write tool, and 1 local-only
preview tool. Component evidence: the offline MCP doctor reports
**`TOOL_COUNT=35`, `RESULT=PASS`**, re-run locally on 2026-07-27 at the
implementation revision `295c2530acdd25cc5cfa8e4b361c4c2358a355f4`.

The previously pinned revision `75b36b2` carried **30 tools**. The increase is
exactly the five read-only **Transmittals** reads (§3.3). Their component history
keeps implementation, correction, hardening and documentation **separate**:

- `7509c872e5b2f128a8f3492966bb8b7f9d27a2a9` (*feat: add read-only ACC/Forma
  Transmittals reads*) — implemented and registered the five tools;
- `802f52ca175ed35e264a581827fa930078d1513e` (*fix: base Transmittals error
  detection on the client contract*) — error-contract correction;
- `295c2530acdd25cc5cfa8e4b361c4c2358a355f4` (*feat: privacy-minimise the three
  Data Management MCP reads*) — the Phase 4A Data Management output boundary
  (§3.4);
- `6ec64110f506ff96ac5744c5e6481c13a3f43806` (*docs: record Transmittals live
  verification*) — the component inventory update, and the currently pinned
  revision. **This commit recorded the verification; it did not implement the
  tools.**

Registration and the doctor result were verified locally at `295c253`; `6ec6411`
is a documentation-only commit on top of it and is the revision pinned above.

**Delta since this inventory date (2026-07-28).** The component has since published
the **RFI first read-only slice** (§6.2) at
`5dca2297e610d5125ea123cd4203de63e96e943b`, taking the component to **38 MCP
tools** — the three RFI reads added to the 35 above — with the offline doctor
reporting **`TOOL_COUNT=38`, `RESULT=PASS`** at that revision. The dated ledger
rows above are deliberately **not** rewritten: they record the 2026-07-27
inventory verification, and no full component re-inventory has been performed
since. Only the RFI capability rows in this document reflect the newer revision.

**Delta since this inventory date (2026-07-29).** The component has since published
the **Submittals first read-only slice** (§6.3) at
`f763d190871743e4c638902ddd6fdadf2d740e88`. The live verification of that slice
was exercised through a freshly launched server over the MCP protocol surface, and
that surface reported **41 registered tools**, of which **3 are Submittals reads**
and **0 are Submittals writes** — the three Submittals reads added to the 38 above.
**No offline doctor result is recorded here for this revision**, because none was
captured; the 41 figure is the count observed on the verified MCP protocol surface.
The dated ledger rows above and the 2026-07-28 RFI delta are both deliberately
**not** rewritten: each records the state established on its own date, and no full
component re-inventory has been performed since 2026-07-27. Only the Submittals
capability rows in this document reflect this newer revision.

The five read-only Model
Coordination model-set reads were added by component commit
`c92ee079408500b74f7c2f7efd8b1ab0b8047fe3` (*feat: add read-only Model
Coordination model-set reads*), logging-privacy hardened by
`1634d8c5e65aff9af1fbb44270159772ebae20ce` (*fix: suppress identifier-bearing HTTP
client logs*), and recorded in the component inventory at `0117022` (*docs: update
inventory for Model Coordination reads*); they were live-verified on 2026-07-23.
All five remain registered at `295c253` (verified locally, 2026-07-27).

The tool identifiers below are code identifiers read from component source; they
are not Autodesk data. No live Autodesk hub, project, folder, item, version,
proposal, or model identifiers are recorded in this repository. Private
operational identifiers remain in the component runtime; public evidence and
identifier aliases belong in this reference repository.

For the Revit MCP, the inventory was verified from the committed tree at
`ae01d29`; unrelated uncommitted working-tree content was excluded.

## 2. Capability-status vocabulary

- **confirmed** — MCP tool implemented and verified in component source at the
  inspected commit.
- **partial** — the capability's own tool surface is partly implemented; some
  tools exist, others are planned.
- **planned** — no MCP tool yet; a later-phase capability.
- **experimental** — MCP tool exists but targets a Beta / `v1alpha` API.
- **data-readiness-blocked** — the tool works, but the approved example or
  training project for the stage lacks the data to exercise it.
- **mediated-by-revit-mcp** — reached through the Revit MCP / Revit API rather
  than APS.

In `config/workflows/end-to-end-reference.yaml` (`schema_version: 2`) a **stage**
is the BIM workflow category and carries only `id`, `platform`,
`automation_policy` and `capabilities`; a **capability** inside it is the unit of
implementation governance. MCP ownership (`mcp_component`), MCP coverage
(`mcp_implementation_status`), API maturity (`api_maturity`) and project-data
readiness (`data_readiness`) are **capability-level** fields, and remain separate
axes that are never conflated
([reference-repo ADR-0008](../decisions/0008-govern-implementation-state-per-capability.md),
[reference-repo ADR-0009](../decisions/0009-define-capability-record-cardinality-for-schema-v2.md)).

The **read / write class** used in the tables below is a semantic classification,
not an HTTP-verb label:

- **read** — no observable Autodesk state mutation, and the OAuth scope Autodesk
  requires for the operation is read-only. `GET` is the normal read transport, but
  it is not the definition of read.
- **write** — any operation that creates, modifies, deletes or transitions
  Autodesk state. Mutation endpoints stay outside the read boundary **regardless
  of HTTP verb**, and this project's only write tool is guarded (§7).

A **non-GET** operation may be classified `read` only through explicit
endpoint-level approval under
[reference-repo ADR-0007](../decisions/0007-read-write-classification-by-state-semantics.md);
`POST` is not presumed read-safe, and approval never generalises from one endpoint
to another. Arbitrary URLs, caller-supplied paths and HTTP methods, and generic
request helpers remain prohibited in every case (§3.1).

## 3. APS/Forma MCP — 35 tools (33 read · 1 guarded write · 1 local)

| Capability group | Tools | Class | Status |
|---|---|---|---|
| Data Management | `list_autodesk_hubs`, `list_projects`, `list_top_folders`, `list_folder_contents`, `get_item_details`, `list_item_versions` | read | confirmed · the last three are privacy-minimised at the MCP boundary and were live-exercised in the Phase 4A Transmittals verification 2026-07-27 (§3.4) |
| Model Derivative | `get_derivative_manifest`, `list_model_views`, `get_model_properties` | read | confirmed |
| Issues | `list_issues`, `get_issue_details`, `list_issue_types` | read | confirmed |
| Reviews | `list_review_workflows`, `list_reviews`, `get_review_details`, `get_review_workflow`, `list_review_file_versions`, `get_review_progress`, `get_file_version_approval_statuses` | read | confirmed · live-verified |
| Issue Relationships | `list_issue_relationships` | read | confirmed · live-verified |
| Model Coordination | `list_model_sets`, `get_model_set`, `list_model_set_versions`, `get_latest_model_set_version`, `get_model_set_version` | read | confirmed · live-verified 2026-07-23 (§3.1, §8) |
| Transmittals | `list_transmittals`, `get_transmittal`, `get_transmittal_recipients`, `get_transmittal_folders`, `get_transmittal_documents` | read | confirmed · live-verified 2026-07-27 (§3.3) |
| Forma Site Design (Beta `v1alpha`) | `get_forma_project`, `list_forma_proposals`, `list_forma_proposal_elements` | read | experimental |
| Forma Site Design (Beta `v1alpha`) | `create_forma_proposal` | guarded write | experimental (sole write; requires explicit confirmation and an explicit source proposal; **not part of the Phase 2 read-only workflow**) |
| Local-only (no Autodesk call) | `prepare_native_floor_stack_preview` | local | confirmed |

Issues, Reviews, and Relationships reads are confirmed; the **RFI** first
read-only slice is confirmed and live-verified (§6.2), and Assets remains planned
(§6). Direct Review-to-Issue relationship support is
**not** established; the relationship read (`list_issue_relationships`) supports
**shared-document comparison** only.

### 3.1 Model Coordination model-set reads (live-verified 2026-07-23)

The five Model Coordination reads are implemented, tested, live-verified, GET-only,
normalised, and logging-privacy hardened. Their purposes:

- `list_model_sets` — discover model sets in a selected project.
- `get_model_set` — retrieve one model set and its configured folder/content
  context.
- `list_model_set_versions` — enumerate coordination snapshot versions.
- `get_latest_model_set_version` — retrieve the latest coordination snapshot and
  its embedded participating document versions.
- `get_model_set_version` — retrieve one selected coordination snapshot and its
  embedded participating document versions.

**Version-domain safety.** A model-set version **is** a coordination snapshot
version. Within a snapshot, `version_urn` is the exact participating document
version, `lineage_urn` is the stable document lineage, and `tip_version_urn` is the
current lineage tip. `tip_version_urn` is **never** substituted for `version_urn`.
Model-set version numbers and Data Management document version numbers are separate
domains, and no numeric document version is inferred from a URN.

**Discipline.** No authoritative discipline field was found in the five
live-verified Model Coordination model-set responses. Discipline remains an
orchestration-level, governed classification and is **not** inferred by the MCP
client from file names, display names, folders or model titles. This is a statement
about these five live-verified responses, not a claim that every Autodesk Model
Coordination API lacks discipline.

**Security and privacy.** All five reads are GET-only; request paths are internally
constructed, so no arbitrary URL or HTTP method is exposed. Participating document
identities are returned privately for safe chaining; public evidence must alias or
omit them, and `created_by` / `create_user_id` are omitted. Third-party
`httpx`/`httpcore` INFO request-URL logging is suppressed while WARNING and ERROR
logging remain available. Raw live responses remain private and uncommitted.

### 3.2 Transport-reliability baseline (component `75b36b2`, 2026-07-24)

Component commit `75b36b2` (*fix: bound token locks and APS transport timeouts*)
is a **reliability-only** increment. It adds **no tool**, **no Autodesk
capability**, and **no new API surface**, and it does not change any public MCP
tool contract.

**Locally inspected in this repository's re-verification (2026-07-24)** — read-only
inspection of the component working tree at `75b36b2`:

- **Bounded token-refresh lock acquisition.** The in-process thread lock and the
  cross-process advisory file lock are acquired under a single bounded monotonic
  deadline; the file lock is taken non-blocking and retried on a short interval,
  raising a dedicated lock error on expiry instead of blocking indefinitely.
- **Explicit HTTP connect/read/write/pool timeouts.** A single shared timeout
  object with separate connect, read, write, and pool bounds replaces the previous
  scalar timeout on the token refresh and the APS read paths.
- **Structured timeout and transport errors.** Timeout, connection, and general
  transport failures — and bounded lock contention — return sanitised structured
  `{error, status, detail}` results carrying no URL, identifier, body, header, or
  credential.
- **Public tool contracts unchanged.** The MCP server module is untouched by the
  commit; the offline doctor reports `TOOL_COUNT=30`, `RESULT=PASS`, and all five
  Model Coordination model-set/version reads remain registered.

**Previously reported by the component (not re-verified here)** — recorded as
reported evidence only:

- a **287-test** implementation report passing at this revision;
- a successful fresh Claude Desktop `list_projects` relay smoke test after the
  push.

This reference repository's re-verification was a **local, read-only repository
and tool-inventory inspection**. It did **not** re-run the component test suite
and made **no live Autodesk call**.

The Phase 3 evidence artifact was produced earlier, at component revision
`0117022`, and records a `get_latest_model_set_version` transport timeout. That
observation is **historical** and is not restated as current behaviour; see
[PHASE_3_CAPABILITY_GAP.md](PHASE_3_CAPABILITY_GAP.md) §6.4.

### 3.3 Transmittals reads (implemented · live-verified 2026-07-27)

The five read-only **Transmittals** tools are the adopted Phase 4A first slice
([ADR-0004](../decisions/0004-adopt-transmittals-as-first-phase-4a-read-slice.md)).
They are **implemented, registered and live-verified**:

- `list_transmittals` — list the transmittals in a project.
- `get_transmittal` — retrieve one transmittal record.
- `get_transmittal_recipients` — recipient structure for one transmittal.
- `get_transmittal_folders` — the folders associated with a transmittal.
- `get_transmittal_documents` — the document versions included in a transmittal.

**Read-only by construction.** Every call routes through a single GET helper in
the component's Transmittals client; no POST, PUT, PATCH or DELETE path exists in
that module, and no raw path or URL is accepted from the caller. Creating,
sending, editing, re-issuing or deleting a transmittal, and adding or removing
recipients or documents, are **not implemented**. No new OAuth scope was required
— `data:read` already sufficed.

**Recipient boundary.** `get_transmittal_recipients` returns **structural counts
only** — project-member, external and total recipient counts plus an
external-members boolean — and **no recipient rows**. No name, email, Autodesk
user or company identifier, or received/viewed/downloaded telemetry is returned
by that tool.

**Live verification.** Verified 2026-07-27 against a controlled synthetic fixture
in the **approved training project**, read-only throughout. This closed Gate 8 for
the Transmittals first slice — see
[PHASE_4_CAPABILITY_GAP.md](PHASE_4_CAPABILITY_GAP.md) §16.4. The exact-version
behavioural finding observed during that run is a **separate matter awaiting
public-evidence governance** and is deliberately not recorded here.

### 3.4 Data Management output boundary (Phase 4A, component `295c253`)

Component commit `295c253` (*feat: privacy-minimise the three Data Management MCP
reads*) narrows the MCP output boundary of `list_folder_contents`,
`get_item_details` and `list_item_versions`. The other three Data Management tools
are unchanged. **Locally inspected in this repository's re-verification
(2026-07-27)**, read-only:

- **Constructive allowlist.** Each result is *built* from named approved fields,
  never by deleting keys from the upstream payload, so any property the component
  does not name — including one Autodesk may add later — is absent by
  construction. No `raw`, `extra`, `included`, `attributes` or `relationships`
  passthrough object exists.
- **Omitted:** every user id and user name, every payload timestamp, storage size,
  the storage / derivatives / thumbnails relationships, the open-ended extension
  object, folder paths, and self/web-view links.
- **Chaining identifiers retained byte-identically** — never parsed,
  canonicalised, truncated, case-folded, URL-encoded or rebuilt.
- **Two-layer split.** The raw client contract is deliberately *not* projected;
  the allowlist is a property of the **tools**, not of the client.

These three reads were live-exercised in the Phase 4A Transmittals verification.
Identifier **aliasing** remains the job of this repository's evidence layer, not
of the component boundary.

## 4. Revit MCP — 14 tools (10 read/inspection · 4 mutating)

| Capability group | Tools | Class | Status |
|---|---|---|---|
| Status & model inspection | `get_revit_status`, `get_revit_model_info`, `list_levels`, `list_families`, `list_family_categories`, `list_category_parameters` | read | confirmed |
| View inspection | `get_revit_view`, `list_revit_views`, `get_current_view_info`, `get_current_view_elements` | read | confirmed |
| Mutating / guarded | `execute_revit_code`, `place_family`, `color_splash`, `clear_colors` | write | confirmed (excluded from the read-only first slice) |

## 5. First-slice capability ledger (read-only) — all confirmed

| Slice step | Capability (component · tools) | Status |
|---|---|---|
| 1. Inspect Revit model | Revit MCP · `get_revit_model_info`, `list_levels`, `list_revit_views`, `get_current_view_elements` | confirmed |
| 2. Locate deliverable in CDE | APS/Forma MCP · `list_folder_contents`, `get_item_details` | confirmed |
| 3. Item / version info | APS/Forma MCP · `list_item_versions` | confirmed |
| 4. Derivative / properties | APS/Forma MCP · `get_derivative_manifest`, `list_model_views`, `get_model_properties` | confirmed |
| 5. Compare metadata | This repository (comparison utility) | to build here |
| 6. Record sanitised result | This repository (sanitisation + fixture) | to build here |

**No component tool capability is missing for the read-only first slice.** Steps
5–6 remain this repository's work to build.

## 6. Phase 4A capability state and remaining MCP gaps

| Stage | Capability | Status |
|---|---|---|
| construction_information | RFI — adopted second Phase 4A capability; first read-only slice implemented and live-verified 2026-07-28 (§6.2) | confirmed |
| construction_information | Submittals — adopted third Phase 4A capability; first read-only slice implemented and live-verified 2026-07-29 (§6.3) | confirmed |
| asset_handover | Assets | planned |

Reviews and issue-relationship reads for `reviews_and_issues` are now implemented
and live-verified (§3); they are no longer a gap. The **Transmittals** first slice
is likewise **implemented and live-verified** (§3.3) and is no longer a gap — it
has been removed from the table above.

**All three governed Phase 4A capabilities are now implemented and live-verified**:
Transmittals (§3.3, 2026-07-27), RFIs (§6.2, 2026-07-28) and Submittals (§6.3,
2026-07-29). Each carries `mcp_implementation_status: confirmed` and
`data_readiness: ready` in the schema-v2 workflow contract, and **each of those
values is scoped to the approved training project and to that capability's own
first read-only slice** — no other project, and no write capability. **No Phase 4A
write tool exists for any of the three.** **Sheets** and **Meetings** remain
unimplemented, and **Assets** remains planned; the V1 scope decision for Phase 4A
is recorded in
[PHASE_4_CAPABILITY_GAP.md](PHASE_4_CAPABILITY_GAP.md) §1 and is not restated here.

The **Transmittals**, **RFI** and **Submittals** API-family names are asserted
because they are verified from official Autodesk/APS documentation; the **Assets**
API-family name is still not asserted here until it is verified from an official
Autodesk/APS or component source. The RFI component boundary and caller-facing
contract are fixed by
[reference-repo ADR-0011](../decisions/0011-adopt-rfi-first-slice-mcp-contract-and-component-boundary.md)
as refined for search by
[ADR-0012](../decisions/0012-refine-rfi-search-contract-from-runtime-verification.md)
(§6.2), and the Submittals equivalents by
[reference-repo ADR-0014](../decisions/0014-adopt-submittals-first-slice-mcp-contract-and-component-boundary.md)
(§6.3). For both, **the contract is approved and the implementation is written,
published and live-verified.**

### 6.1 Transmittals ownership split (adopted, implemented)

The component assignment below is **confirmed** by
[ADR-0004](../decisions/0004-adopt-transmittals-as-first-phase-4a-read-slice.md).
The five read tools are **implemented, registered and live-verified**
(2026-07-27, §3.3), and Gate 8 is **closed for the Transmittals first slice** under
the operative §14 criteria of
[PHASE_4_CAPABILITY_GAP.md](PHASE_4_CAPABILITY_GAP.md), with readiness established
in the **approved training project**. The ownership split itself is unchanged.

**APS/Forma MCP owns:**

- Transmittals authentication;
- construction of Transmittals endpoint paths;
- pagination handling;
- request execution;
- response normalisation;
- structured error handling;
- the five read tools.

**This reference repository owns:**

- architecture and roadmap;
- workflow orchestration;
- the evidence schema;
- sanitisation policy;
- validation;
- public evidence artifacts.

**Autodesk Forma owns (native, never re-implemented):**

- the Transmittals records themselves;
- recipient visibility;
- document-version associations;
- permission enforcement;
- transmittal processing state.

**Explicitly prohibited:**

- rebuilding Transmittals behaviour anywhere in this repository;
- creating synthetic relationships that Autodesk did not return;
- deriving stable document lineage and representing it as returned evidence —
  the documented response carries a version-qualified URN and an authoritative
  numeric version, and **no separate lineage field is verified**;
- placing credentials or raw Autodesk responses in this repository;
- adding any write endpoint to the first slice.

The first slice is fixed at the five documented read operations: list
transmittals; get one transmittal; list recipients; list folders; list included
document versions.

### 6.2 RFI first-slice contract (adopted, implemented, live-verified)

**Approved by
[reference-repo ADR-0011](../decisions/0011-adopt-rfi-first-slice-mcp-contract-and-component-boundary.md)
(2026-07-28), with the `search_rfis` contract refined 2026-07-28 by
[ADR-0012](../decisions/0012-refine-rfi-search-contract-from-runtime-verification.md)
from runtime verification.** The contract below is the **current effective**
contract for the **RFI v1 first slice**. The slice is **implemented, published and
live-verified (2026-07-28)** at APS/Forma MCP revision
`5dca2297e610d5125ea123cd4203de63e96e943b`, exercised through a **freshly launched
server over the MCP protocol surface** against a controlled synthetic fixture in
the **approved training project**;
[`PHASE_4_CAPABILITY_GAP.md`](PHASE_4_CAPABILITY_GAP.md) §16.7 records the Gate 8
closure. `mcp_implementation_status` is `confirmed` and `data_readiness` is
`ready`, both scoped to that project and that read-only slice — no other project,
no other RFI workflow type, and **no write capability**. ADR-0011 is not amended
and remains authoritative for every decision ADR-0012 does not refine.

**APS/Forma MCP owns RFI**, in a **dedicated `rfis_client`**. RFI semantics belong
in no existing client and in no generic request infrastructure.

**Three read-only tools in the v1 first slice:**

| Tool | Endpoint | State semantics |
|---|---|---|
| `get_rfi_user_context` | `GET …/rfis/v3/projects/{projectId}/users/me` | read |
| `search_rfis` | `POST …/rfis/v3/projects/{projectId}/search:rfis` | **read-semantic POST** (ADR-0007) |
| `get_rfi` | `GET …/rfis/v3/projects/{projectId}/rfis/{rfiId}` | read |

Three tools is the **v1 scope**, not a permanent prohibition; a later surface may
be adopted deliberately through the same governance route.

**Read-only by contract.** No write endpoint is in v1 scope; no tool accepts a
caller-supplied URL, path, HTTP method or raw request body. The search POST uses a
**private helper hardwired to `search:rfis`**; `forma_post` is **not** reused — it
carries Site Design `x-ads-region` and `authcontext` semantics — and is not
generalised. Gate 6 approves this contract; a later implementation increment must
demonstrate that the code satisfies it.

**Output boundary.** `rfis_client` normalises with an **explicit allowlist** (the
Reviews / Model Coordination convention, not the Transmittals raw-shape special
case). `search_rfis` returns `id`, `custom_identifier`, `title`, `status` plus
pagination — enough to choose one RFI without fetching every detail object.
`get_rfi` returns a curated DTO including core RFI narrative (`title`,
`question`, `official_response`, `suggested_answer`).

**Search request — runtime-verified 2026-07-28 (ADR-0012).** The request sends
a **JSON-body `fields` array** of exactly `id`, `customIdentifier`, `title`,
`status`. `workflowType` is a **rejected enum member**, so **`workflow_type` is
not part of the search caller contract**; it is neither derived nor fetched by a
second call, and it remains in `get_rfi_user_context` and `get_rfi`. Autodesk may
still return additional top-level properties, so **`fields` is a validated
bounded upstream selection request: its exact response-shaping effect is not
established, and it is not an enforcement boundary.** The `rfis_client` allowlist
is authoritative. Additional properties (`responses`, `assignedTo`, `reviewers`,
`watchers`, `architects`, `coReviewers`, `optionalReviewers`,
`officialResponseActors`, `permittedActions`, `virtualFolderUrn`, `hash`,
`maxAssignees`) are discarded before caller output, never logged, and never
placed in public evidence. `custom_identifier` is `None` when upstream omits it.

**Embedded responses are summarised, not exposed.** `responses[].text`,
`.createdBy` and `.onBehalf` are excluded; only `response_count`,
`response_states` and `response_statuses` are returned. Core RFI narrative and
embedded response narrative are different contract domains, and the Response
surface is not adopted.

**Participants reduce to counts** — `assignee_count`, `reviewer_count`,
`watcher_count`. No adopted v1 tool resolves participant identities and no
first-slice use case requires them; a participant-resolution capability must be
adopted deliberately before those identifiers enter the caller contract.

**Caller output is not public evidence.** Authenticated callers receive real
operational identifiers, `custom_identifier` and approved narrative; the
public-evidence path applies
[ADR-0010](../decisions/0010-approve-rfi-public-evidence-sanitisation-profile.md)
and its aliases and reductions. `RFI_n` aliases are never returned to the normal
MCP caller.

**Auth and identifiers.** Existing 3-legged user-context token, `data:read`; no
`client_credentials`, no SSA. Project ids are accepted with or without the `b.`
prefix and normalised by stripping it, as the Transmittals client already does.

**Pagination:** `limit` 1–200 (default 10), `offset` ≥ 0; no fetch-all, no
automatic detail call per search result, no bulk crawling.

### 6.3 Submittals first-slice contract (adopted, implemented, live-verified)

**Approved by
[reference-repo ADR-0014](../decisions/0014-adopt-submittals-first-slice-mcp-contract-and-component-boundary.md)
(2026-07-29).** The contract below is the **current effective** contract for the
**Submittals v1 first slice**.

> **Read this subsection as describing SUBMITTALS ONLY.** Every statement in §6.3
> is scoped to Submittals and to no other capability. Statements elsewhere in §6
> about other capabilities' implementation state — including any
> pre-implementation prose about RFIs — do not describe Submittals, and Submittals
> statements do not describe them.

**Three tools are implemented, published and live-verified (2026-07-29)** in a
dedicated `submittals_client` at APS/Forma MCP revision
`f763d190871743e4c638902ddd6fdadf2d740e88`, exercised through a **freshly launched
server over the MCP protocol surface** against a controlled synthetic fixture in
the **approved training project**, using **three Autodesk-facing GET requests and
zero writes**. The verified surface reports **41 registered tools**, of which
**3 are Submittals reads** and **0 are Submittals writes**.
[`PHASE_4_CAPABILITY_GAP.md`](PHASE_4_CAPABILITY_GAP.md) §16.10 records the Gate 6
closure and §16.11 records the Gate 8 closure. `mcp_implementation_status` is
`confirmed` and `data_readiness` is `ready`, both scoped to that project and that
read-only slice — no other project, no other Submittal workflow state, no other
caller role, and **no write capability**. The **minimum proven scope is
`data:read`**; the normal server grant holds a broader four-scope configuration for
other capabilities and that does not widen the Submittals requirement. The
controlled fixture is **unchanged**.

**APS/Forma MCP owns Submittals**, in a **dedicated `submittals_client`**.
Submittals semantics belong in no existing client and in no generic request
infrastructure.

**Three read-only tools in the v1 first slice — all GET:**

| Tool | Endpoint | State semantics |
|---|---|---|
| `get_submittal_user_context` | `GET …/submittals/v2/projects/{projectId}/users/me` | read |
| `list_submittals` | `GET …/submittals/v2/projects/{projectId}/items` | read |
| `get_submittal` | `GET …/submittals/v2/projects/{projectId}/items/{itemId}` | read |

**No POST-as-read classification is involved**; ADR-0007 is referenced but not
exercised. Three tools is the **v1 scope**, not a permanent prohibition.

**Naming.** `list_submittal_items` / `get_submittal_item` are rejected: the
component already exposes `get_item_details` and `list_item_versions` for **Data
Management items**, and reusing "item" would recreate the `ITEM_n` / `SUBMITTAL_n`
identifier-domain collision that ADR-0013 made a normative prohibition. The
upstream route says `items`; the tool surface says `submittal`.

**Inputs.** `get_submittal_user_context(project_id)` ·
`list_submittals(project_id, limit=None, offset=None)` ·
`get_submittal(project_id, submittal_id)`. No search, filter map, sort, package
filter, state or status filter, generic query parameters, or caller-supplied URL,
path, method or body.

**Caller context — exactly 3 fields:** `submittals_available` (bool) ·
`permitted_action_count` (int) · `role_count` (int). A successful DTO **requires**
an object body with `permittedActions` and `roles` both present as arrays;
otherwise the operation returns the structured malformed-response outcome rather
than a DTO with zeroed counts. Empty arrays legitimately yield zero.
`submittals_available` has **no successful `false` state** — permission,
authentication and module-availability failures are structured errors.

**List — exactly 8 fields per result:** `submittal_id` ← `id` (required, non-empty
string) · `identifier` ← `identifier` · `custom_identifier` ← `customIdentifier` ·
`title` · `state_id` ← `stateId` · `status_id` ← `statusId` · `revision` ·
`due_date` ← `dueDate`. Response shape `{ results, pagination }`.

**Detail — exactly 17 fields:** `submittal_id` · `identifier` ·
`custom_identifier` · `custom_identifier_human_readable` · `title` · `description` ·
`state_id` · `status_id` · `revision` · `priority` · `spec_identifier` ·
`spec_title` · `due_date` · `submitter_due_date` · `ball_in_court_type` ·
`created_at` · `updated_at`.

**Excluded from detail:** `spec_id` and `type_id` (no v1 operation consumes or
resolves them) · `subsection` (observed only as `null`; populated type unobserved) ·
`manager_type` and `subcontractor_type` (describe parties the slice deliberately
does not name).

**`customIdentifier` disambiguation.** The upstream payload carries two distinct
keys. **`custom_identifier` maps only from `customIdentifier`**, and
**`custom_identifier_human_readable` maps only from
`customIdentifierHumanReadable`**. Every contract field maps 1:1 to the key it is
named after.

**List versus detail.** The upstream list row and direct detail response were
observed as **the same 56-key schema** for the controlled fixture. `get_submittal`
is therefore **not** adopted as a richer Autodesk representation. It is retained
because it gives direct access to one known Submittal without paging the
role-scoped collection, and because it independently exercises the canonical detail
route. The 8-field and 17-field projections differ **by our design**, not because
the upstream documents differ.

**Nullability — wrong types fail closed.** Absent → `None`; upstream `null` →
`None`; present with the expected type → the value; **present, non-null, wrong type
→ malformed-response outcome**. A wrong-typed value is a transport-contract
violation and is never coerced or erased to `None`. `bool` never satisfies an
integer contract. `submittal_id` is required. Structural requirements: body an
object; `results` an array; `pagination` an object. Pagination fields follow the
same rule and are **never defaulted**. Each DTO is a new dict built key by key from
a closed allowlist, so the 56-key upstream document cannot leak.

**State and status** are typed `str | None`. Legal values are **not** enumerated,
`statusId` is **not** typed as an integer and **not** treated as ordinal or
sortable. The controlled observation (`stateId` `"sbc-1"`, `statusId` `"1"`,
recorded while the UI displayed *Required / Waiting for submission*) is evidence,
not runtime validation.

**Identity and companies.** All raw person identities are excluded — `manager`,
`subcontractor`, `createdBy`, `updatedBy`, `submittedBy`, `publishedBy`,
`respondedBy`, `sentToReviewBy`, `ballInCourtUsers`, `watchers`, the caller `id`
and `roles` values. Company identity, `ballInCourtCompanies` and commercial
assignment relationships are excluded, and **no company DTO is invented** — the
member shape was never observed. **No `USER_n` or `COMPANY_n` concept appears in
any runtime DTO**; aliases are public-evidence constructs under ADR-0013, and an
authenticated caller receives real values. `ball_in_court_type` is the only
retained categorical discriminator.

**Timeline.** No history object. Only `due_date`, `submitter_due_date`,
`created_at` and `updated_at` are adopted, and no lateness, duration, interval,
ordering or workflow-progression inference is derived. **`sentToSubmitter` is
excluded**: the controlled fixture showed it populated **before submission**, with
`submittedBy` still `null`, so its presence must never be read as proof of
submission.

**`permittedActions` is excluded entirely at both caller and item scope** —
objects, member ids, `fields`, `mandatoryFields`, `transitions`, `actionId`,
transition names, `stateFrom`, `stateTo` and `transitionFields`. It is
**write-capability and workflow-configuration metadata, not the read-resource
projection**: collectively the transition maps are the project's submittal state
machine. Only `permitted_action_count` survives.

**Auth and identifiers.** Existing 3-legged user-context token; **the proven
first-slice scope is `data:read`**. No `client_credentials`, no SSA, no second
token store, no `x-user-id`. **No `x-ads-region`** — the verified first slice
succeeded against the global host with `Authorization` alone. Project ids are
accepted with or without the `b.` prefix and normalised by stripping it, as the
Transmittals and RFI clients already do, with capability-local validation and
allowlisted path characters. Validation errors never echo supplied values. **The
normal server grant holds a broader four-scope configuration for other
capabilities; that is server configuration and does not widen the Submittals
requirement.**

**Pagination.** `limit` and `offset` are optional and **omitted parameters are not
sent** — no local default is substituted. **No local maximum is encoded**: the
Submittals maximum page size is unknown, and 50, 200 and any other bound are
deliberately absent. Local input hygiene only: `limit` an integer `>= 1`, `offset`
an integer `>= 0`, booleans rejected, values never clamped. A service-defined bound
is enforced upstream and its rejection flows through the bad-request
classification. The observed no-parameter response carried `limit` 20; **that is
recorded evidence, not a local default**. The `limit >= 1` floor is this project's
rule, not an assertion about the upstream accepted range.

**Errors and logging.** The capability-local RFI error model is adopted unchanged
in structure — no new global error architecture and no shared refactor. Envelope
keys `error`, `status`, `detail`, `retry_after`. Categories: input validation,
authentication/token failure, 400 bad request, 401 authentication failed, 403
permission denied (whose detail also names that the Submittals module may not be
active for the project), 404 not found, 429 rate limited with safe `Retry-After`
handling only, transport failure, malformed upstream response, and other upstream
failures per sibling precedent. The raw Autodesk error body, headers, resolved URL,
tokens, identifiers and diagnostic payloads are **never** exposed. Logging is
narrower than the output: operation name, status and bounded counts only.

**Implementation, as built.** A dedicated `submittals_client.py`, GET-only, three
internal helpers hardwired to three fixed routes, no generic request helper, no
caller-supplied URL/path/method/body, no shared-client refactor, no
transport-abstraction expansion, no write helpers, capability-local validation,
reuse of the existing APS 3LO lifecycle, and three MCP tools registered. The
client's shape enforcement **fails closed**: an absent or upstream-null value maps
to `null`, but a present value of an unexpected type is a transport-contract
violation and returns the structured malformed-response outcome rather than being
coerced.

**Gate 5 versus Gate 6.** ADR-0013 governs **public repository evidence**;
ADR-0014 governs **authenticated runtime caller output**. The caller may
legitimately receive real submittal identifiers, `identifier`, custom identifiers,
`title`, `description`, `priority`, spec identifier and title, and dates, while
those same values remain forbidden or reduced to presence booleans under ADR-0013.
`priority` is the clearest case: adopted here, explicitly omitted there. **This is
intentional, and ADR-0013 is neither weakened nor reinterpreted.**

## 7. Experimental boundary

The Forma Site Design tools target Beta (`v1alpha`) APIs and are isolated as
experimental. The project's only write tool, `create_forma_proposal`, sits inside
this Beta boundary and is guarded. Nothing on the stable read-only path depends on
Forma Site Design writes.

## 8. Data-readiness status (coordination training data ready)

The earlier data-readiness blocker (`no_harrismith_model_sets`) is **closed**. An
isolated training coordination space now exists with automatic clash processing
enabled; two discipline-context RVT models were processed; both participating
document versions are visible through the version-level MCP responses
(`get_latest_model_set_version`, `get_model_set_version`); and automatic clash
results are visible in the Autodesk interface.

Only the version-level participating documents are read by the component. Raw clash
results, clash identifiers/groups, clash status, and resolution verification remain
unimplemented (see
[PHASE_3_CAPABILITY_GAP.md](PHASE_3_CAPABILITY_GAP.md)). This is a description of a
sanitised training space only: no coordination-space name, model filenames, folder
names, element IDs, model-set IDs, URNs, GUIDs, or timestamps are recorded here.

## 9. Responsibility matrix

| Concern | Revit MCP | APS/Forma MCP | This repository |
|---|---|---|---|
| Revit authoring / inspection | Owns | — | Documents, invokes, validates |
| Autodesk authentication (APS) | — | Owns | Never implements |
| Forma Data Management (CDE) | — | Owns | Documents, invokes, validates |
| Model Derivative / properties | — | Owns | Documents, invokes, validates |
| Issues, Reviews & Relationships (assets planned) | — | Owns | Documents, invokes, validates |
| RFI first-slice reads (adopted, implemented — §6.2) | — | Owns | Documents, invokes, validates |
| Transmittals reads (adopted, implemented — §3.3, §6.1) | — | Owns | Documents, invokes, validates |
| Submittals first-slice reads (adopted, implemented — §6.3) | — | Owns | Documents, invokes, validates |
| Model Coordination model-set/version reads | — | Owns | Documents, invokes, validates |
| Model Coordination clash engine (native) | — | Consumes / surfaces | Documents only |
| Clash detection | Must not build | Must not build | Must not build |
| Orchestration / docs / examples | — | — | Owns |

"Owns" means the component is the source of truth for that behaviour. This
repository may **invoke** or **validate** a behaviour but must never
**re-implement** it.

## 10. Anti-duplication rules

- Do not copy or vendor component source; no Git submodules
  ([ADR-0002](../decisions/0002-multi-repo-no-submodules.md)).
- Do not re-implement authentication, derivative processing, or clash detection.
- Utilities in `scripts/` call component tools or validate their outputs; they do
  not reproduce internal logic
  ([ADR-0001](../decisions/0001-orchestration-layer-not-mcp-server.md)).
- When a capability is missing, raise it in the owning component repository rather
  than working around it here.

## 11. Reverification policy

- This ledger is pinned to the inspected commits (`6ec6411` APS/Forma, `ae01d29`
  Revit) and the verification date above. The APS/Forma tool count of 35 is
  evidenced by the offline doctor `TOOL_COUNT=35`, `RESULT=PASS` (re-run locally
  2026-07-27 at the implementation revision `295c253`, of which the pinned
  `6ec6411` is a documentation-only descendant). The five Model Coordination
  model-set reads were live-verified on 2026-07-23, and the five Transmittals
  reads on 2026-07-27; all ten were confirmed still registered at `295c253`.
- A re-pin driven by a reliability-only component change updates the revision and
  date but **must not** change any capability status; capability status changes
  only on evidence of a new or altered tool.
- Re-run the read-only inventory and update the counts, commit hashes, and date
  before each phase, or whenever a component publishes a relevant change.
- Component tool surfaces evolve; expectations are captured here in documentation,
  not by submodule pins (see
  [REPOSITORY_STRATEGY.md](REPOSITORY_STRATEGY.md)).
