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

Issues, Reviews, and Relationships reads are confirmed; RFI and Assets
capabilities remain planned (§6). Direct Review-to-Issue relationship support is
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

## 6. Later-stage missing MCP capabilities (planned)

| Stage | Capability | Status |
|---|---|---|
| construction_information | RFI — preferred second Phase 4A capability | planned |
| asset_handover | Assets | planned |

Reviews and issue-relationship reads for `reviews_and_issues` are now implemented
and live-verified (§3); they are no longer a gap. The **Transmittals** first slice
is likewise **implemented and live-verified** (§3.3) and is no longer a gap — it
has been removed from the table above; **Phase 4A as a whole is not complete**,
and RFIs, Submittals, Sheets and Meetings remain unimplemented. The
**Transmittals** API-family name is asserted because it is verified from official
Autodesk/APS documentation; API-family names for RFI and Assets are still not
asserted here until they are verified from an official Autodesk/APS or component
source.

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
| Issues, Reviews & Relationships (RFI/assets planned) | — | Owns | Documents, invokes, validates |
| Transmittals reads (adopted, planned — §6.1) | — | Owns | Documents, invokes, validates |
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
