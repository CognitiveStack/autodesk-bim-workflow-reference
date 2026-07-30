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

**Revit MCP source re-traced 2026-07-29**, read-only, at the same committed
revision `ae01d29` — no re-pin, and **no capability status changed**. The pass
established the execution path (§4.1), the transaction-based read/write classes
(§4), the absence of any component write guard (§4.2) and the upstream provenance
(§4.3). **Only the committed tree was interpreted.** The component's working tree
carried uncommitted operator content, which remains excluded and is **not** part of
the published architectural baseline; nothing in this document describes it.

The **Revit Alignment live read verification** followed on the same date, at the
same pinned revision and with no re-pin (§4.4). It changed **one** capability's
`data_readiness`, on live evidence rather than on any change to the component.

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
not an HTTP-verb label. The common principle is that **an operation is a `read`
only if it leaves no persistent domain-state mutation another caller could observe**,
and **the transport verb is never the classifier**. Two substrate branches sit
beneath that principle, and the branches must not be mixed.

**Autodesk cloud APIs (§3) —
[reference-repo ADR-0007](../decisions/0007-read-write-classification-by-state-semantics.md),
unchanged:**

- **read** — no observable Autodesk state mutation, and the OAuth scope Autodesk
  requires for the operation is read-only. `GET` is the normal read transport, but
  it is not the definition of read.
- **write** — any operation that creates, modifies, deletes or transitions
  Autodesk state. Mutation endpoints stay outside the read boundary **regardless
  of HTTP verb**.

A **non-GET** Autodesk cloud operation may be classified `read` only through
explicit endpoint-level approval under ADR-0007; `POST` is not presumed read-safe,
and approval never generalises from one endpoint to another.

**Local Revit/pyRevit automation (§4) —
[reference-repo ADR-0015](../decisions/0015-classify-local-automation-read-write-by-document-state.md):**

- **read** — commits no Revit transaction and leaves no persistent BIM or document
  state. A **`POST` route on the local bridge may still be a read**, because that
  bridge's verbs carry no domain meaning.
- **write** — commits a Revit transaction, or otherwise leaves persistent document
  or view state. **Persistent view state counts as a write.**
- A **bounded transient external side effect** (a temporary file created and
  removed within the call) does not make an operation a write.

ADR-0015 **neither modifies nor weakens ADR-0007**, and the local branch must never
be cited for an Autodesk cloud operation.

Arbitrary URLs, caller-supplied paths and HTTP methods, generic request helpers,
and caller-supplied executable code remain prohibited in every governed read
surface, on both branches (§3.1, §4.2).

**`write` is a description, not an authorisation.** Which write tools may be
invoked, and under what control, is stated per component in §3 and §4.2 — the two
components differ materially and must not be assumed alike.

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

## 4. Revit MCP — 14 tools (10 read · 4 write, none guarded by the component)

Inspected read-only from the **committed tree at `ae01d29`** (2026-07-22 inventory,
component source re-traced 2026-07-29). Read/write class follows the local-automation
branch of §2 ([reference-repo ADR-0015](../decisions/0015-classify-local-automation-read-write-by-document-state.md)):
the classifier is the **Revit transaction**, not the bridge verb.

| Capability group | Tools | Bridge verb | Class | Status |
|---|---|---|---|---|
| Session status (runtime provenance, not a BIM capability) | `get_revit_status` | GET | read | confirmed |
| Model inspection | `get_revit_model_info`, `list_levels`, `list_families`, `list_family_categories`, `list_category_parameters` | GET ×4, **POST ×1** | read | confirmed |
| View inspection and export | `list_revit_views`, `get_current_view_info`, `get_current_view_elements`, `get_revit_view` | GET | read | confirmed |
| Element authoring | `place_family` | POST | **write** | confirmed · **not guarded by the component** · excluded from every read-only slice |
| View graphic overrides | `color_splash`, `clear_colors` | POST | **write** (persistent view state) | confirmed · **not guarded by the component** · excluded from every read-only slice |
| Arbitrary code execution | `execute_revit_code` | POST | **write, unbounded** | confirmed · **not guarded by the component** · excluded from every read-only slice |

**`list_category_parameters` is a read despite its `POST` route.** It opens no
Revit transaction and returns parameter metadata gathered by an element collector;
under ADR-0015 §4a the local bridge's verbs carry no domain meaning. This resolves
the earlier inconsistency in which a non-`GET` operation was classified `read`
while §2 required an ADR-0007 endpoint approval that could not exist for it.

**`get_revit_view` is a read despite writing a file.** It exports a PNG to a
temporary directory, encodes it, and **removes the file within the same call**,
opening no transaction — a bounded transient external side effect under ADR-0015
§4c, not a document write.

**`color_splash` and `clear_colors` are writes even though they change no
geometry.** Both commit a transaction setting element graphic overrides, producing
persistent, undoable, savable view state that another caller can observe. The
implementation also applies overrides to **other views of the same view type**, so
the effect is not confined to the active view.

The six groups above correspond to the governed Revit capability records in
`config/workflows/end-to-end-reference.yaml`, except that **session status is
deliberately not a capability record** — it is consumed as runtime provenance
(`component_provenance.revit_mcp.runtime_status`), not as BIM content.

### 4.1 Execution path and the pyRevit boundary

The Revit path has **four layers**, not two. The APS/Forma pattern — an MCP server
calling an Autodesk cloud API — does **not** apply here:

```
MCP client (e.g. Claude Desktop)
   │  MCP protocol (stdio by default; SSE / streamable-HTTP optional)
   ▼
revit-mcp  ·  FastMCP server process (CPython)
   │  local HTTP bridge → http://localhost:48884/revit_mcp
   ▼
pyRevit Routes  ·  HTTP host running INSIDE the Revit process (IronPython)
   │  Revit API
   ▼
Autodesk Revit  ·  document, transaction engine, rendering, BIM state
```

**The local bridge is not an Autodesk cloud API.** It is loopback HTTP to a
third-party in-process host. It has **no OAuth model, no scope, no token and no API
key**, and no authentication is implemented in the inspected component at `ae01d29`.
No Autodesk endpoint, host or credential is involved anywhere on this path.

Consequences that must not be blurred:

- **`revit-mcp` does not call the Revit API directly.** It calls pyRevit Routes.
  The Revit API is reached only by the route handlers, which ship as a **pyRevit
  extension** rather than as MCP-server code.
- **`api_family: Autodesk Revit API`** is retained for every Revit capability
  record because the BIM operation ultimately executes against the Revit
  document/DB API. **pyRevit Routes is an integration transport, not the
  capability's Autodesk BIM API family**, and is deliberately never written into
  `api_family` ([ADR-0003](../decisions/0003-autodesk-platform-product-and-api-terminology.md)).
- **pyRevit is a third-party dependency, not an MCP component of this project.** It
  appears in the responsibility matrix (§9) because it owns a real layer; it is not
  a `mcp_component` value and never becomes one.

### 4.2 Write control — where it actually lives

**The Revit MCP component implements no write guard.** At the inspected revision it
has **no confirmation step, no approval mechanism, no dry-run, no preview, no
read-only mode and no authentication**. Its four write tools are directly callable
by any client that reaches the server.

**The only control in force is discipline in this repository** — the explicit
never-invoke list in
[PHASE_1_EXECUTION_PLAN.md](../workflows/PHASE_1_EXECUTION_PLAN.md) §2, which names
`execute_revit_code`, `place_family`, `color_splash` and `clear_colors`, together
with `writes_require_explicit_approval: true` in project configuration. That
control is **orchestration-layer policy, not a component capability**, and it is
honoured by never calling a write tool.

This is a **material difference from the APS/Forma MCP**, whose sole write tool
(`create_forma_proposal`, §3, §7) is guarded in the component itself and requires
explicit confirmation. **The two components must not be assumed alike**, and
`mcp_implementation_status: confirmed` on a Revit write capability records only
that the tool exists and is registered — it authorises no use.

`execute_revit_code` is additionally **unbounded**: it accepts caller-supplied
IronPython executed inside Revit with the document and the Revit DB namespace in
scope, wrapped in one committed transaction. It is classified `write` by capability
regardless of any stated intent (ADR-0015 §4b), and is excluded from every governed
workflow.

Closing these gaps is a **component** concern and is deferred; no change to
`revit-mcp-triviron` is authorised or made by this repository.

### 4.3 Provenance and verification limits

**Upstream provenance.** `revit-mcp-triviron` is **based on / forked from**
[`revit-mcp/revit-mcp-python`](https://github.com/revit-mcp/revit-mcp-python), as
declared by the `url` and `author` fields of the component's own `extension.json`
(original authors: Juan D. Rodriguez and Jean-Marc Couffin). Recorded for
attribution and provenance only; **no licensing assessment is made here**, and no
component source is copied or vendored into this repository
([ADR-0002](../decisions/0002-multi-repo-no-submodules.md)).

**No offline verification mechanism exists.** The Revit MCP reports **14 tools at
`ae01d29`**, established by **reading the committed source** — `tools/__init__.py`
registers six modules declaring 14 `@mcp.tool()` functions, each resolving to a
registered pyRevit route. Unlike the APS/Forma MCP, the component provides **no
offline doctor, tool manifest or equivalent** that can evidence a tool count
without a running Revit, so no `TOOL_COUNT` / `RESULT=PASS` line can be cited for
it and no such claim appears anywhere in this repository. Building one is a
component concern and is deferred. This is a **verification-provenance limitation,
not a capability gap**.

### 4.4 Revit Alignment — Live Read Verification (2026-07-29)

**Read-only throughout. No Revit write tool was invoked.**

The full runtime path was exercised end to end and reached the **active `HFS-ARC`
document**:

```
Claude Desktop → revit-triviron → FastMCP → pyRevit Routes → Autodesk Revit → HFS-ARC
```

`HFS-ARC` is named here because it is already published in the Phase 1 evidence
artifact; nothing new about the model is disclosed.

**Result — recorded as PASS statements and booleans rather than counts**, so that
no figure appears here that was not taken from recorded output:

| Item | Result |
|---|---|
| Runtime path reached the active document | **PASS** |
| `get_revit_status` | **PASS** — active document present |
| Model-inspection read set (`get_revit_model_info`, `list_levels`, `list_families`, `list_family_categories`, `list_category_parameters`) | **PASS** |
| View-inspection/export read set (`list_revit_views`, `get_current_view_info`, `get_current_view_elements`, `get_revit_view`) | **PASS** — image returned; image not saved into this repository |
| Any Revit write tool invoked | **No** |

**Capability consequences.** `revit_model_inspection` remains `confirmed` /
`ready`, with this session extending the evidence beyond the Phase 1 model and
level reads to the family, category and parameter reads. `revit_view_inspection_export`
moves from `not-assessed` to **`ready`**, scoped by
`revit-view-inspection-export-demonstrated-in-hfs-arc-live-read-session`.

**The three write capabilities are unchanged and remain `not-assessed`** —
`revit_element_authoring`, `revit_view_graphic_overrides` and
`revit_code_execution`. **No live write verification was performed, and none is
required for V1.** `confirmed` implementation status and assessed data readiness
remain independent axes (ADR-0008): a registered tool is not an exercised one.

**Scope.** Every result above is scoped to **one model, in one session, through the
read tools only**. It asserts nothing about other Revit models, other documents,
every possible view name, any write capability, component hardening, or production
readiness.

**ADR-0015 consistency.** The live results were **consistent with** the
classification: the `POST`-route parameter read behaved as a read, and the view
export returned successfully with no intentional persistent document-state change.
**The client observed outcomes, not internals.** The no-transaction property, the
bounded temporary-export lifecycle and the transaction/document-state basis of the
classification itself remain **source-established facts from the static Revit MCP
inspection** (§4, §4.1) — a live MCP client cannot observe a handler's internal
transaction or file-cleanup mechanics, and nothing here claims it did. **No
reclassification is required**, and
[ADR-0015](../decisions/0015-classify-local-automation-read-write-by-document-state.md)
stands unchanged.

**Independent bridge evidence.** A separate read-only diagnostic probe on the same
date confirmed the bridge directly from the Windows host:
`GET http://127.0.0.1:48884/revit_mcp/status/` returned **HTTP 200** with
`revit_available: true` and the `HFS-ARC` document title, and the port-48884
listener was owned by the `Revit` process itself — confirming that pyRevit Routes
is hosted **in-process by Revit** (§4.1) rather than as a separate service.

**Runtime observations — not V1 blockers, no component change made:**

- **`list_families` did not honour a requested small limit** and returned a
  default-size result. The caller-supplied limit is therefore **not** an enforced
  bound at this revision.
- **`get_revit_view` failed on a view name containing braces** (`{3D}`) and
  succeeded on a brace-free exportable view. View-name handling across the route is
  **not** universal, which is why the view-export readiness reason is scoped to the
  session rather than to every view.
- **pyRevit Routes binds `0.0.0.0:48884`, not loopback**, while Revit is running.
  This is **pyRevit's own default**, not a setting of this project or of
  `revit-mcp`. Because that bridge fronts the unguarded write tools (§4.2) with no
  authentication, it is reachable from the local network for as long as Revit is
  open. **Recorded as a live security observation only**; remediation is a component
  and environment concern and is deferred.

None of the three alters a capability status, a read/write classification, or the
component boundary.

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
experimental. The **APS/Forma MCP's only write tool**, `create_forma_proposal`,
sits inside this Beta boundary and is guarded in the component itself. Nothing on
the stable read-only path depends on Forma Site Design writes.

This is the project's only **guarded** write tool. It is not the project's only
write tool: the Revit MCP carries four write tools that the component does **not**
guard, controlled instead at the orchestration layer (§4.2).

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

This matrix covers the **two MCP components and this repository**. The Revit path
has a fourth layer, pyRevit, which is a third-party dependency rather than an MCP
component; it is set out separately in §9.1.

| Concern | Revit MCP | APS/Forma MCP | This repository |
|---|---|---|---|
| Revit inspection / authoring MCP tool surface (§4) | Owns | — | Documents, invokes, validates |
| Revit write control and approval (§4.2) | **Does not implement** | — | **Owns** (workflow discipline, `writes_require_explicit_approval`) |
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

### 9.1 Revit-path layer ownership

The Revit path traverses four layers (§4.1). Only one of them is an MCP component
of this project; the table records the other three so no responsibility is
attributed to the wrong layer.

| Layer | Owns | Is it an MCP component of this project? |
|---|---|---|
| **Autodesk Revit** | The document and element model, the transaction engine, undo/redo, regeneration, view rendering, licensing, and all BIM state. Never re-implemented anywhere. | No — the native application |
| **pyRevit** (third party, `pyrevitlabs`) | The in-process Routes HTTP host, the IronPython execution environment, extension loading, and the `DB` / `revit` bindings the route handlers use. | **No** — a third-party dependency. It is never a `mcp_component` value, and this project neither maintains nor re-implements it |
| **revit-mcp** (`CognitiveStack/revit-mcp-triviron`) | The MCP tool surface and its registration, argument shaping and response formatting, the local HTTP bridge client, and the route handlers it ships as a pyRevit extension — including their transaction lifecycle. | **Yes** — `mcp_component: revit-mcp` |
| **bim-workflow-reference** (this repository) | Architecture and roadmap, capability governance, workflow orchestration, read/write classification policy, the evidence schema and sanitisation policy, published evidence, acceptance — and, today, the **only write control in the Revit path** (§4.2). | Not a component — the orchestration layer ([ADR-0001](../decisions/0001-orchestration-layer-not-mcp-server.md)) |

The APS/Forma path has no equivalent third layer: the APS/Forma MCP calls Autodesk
cloud APIs directly. **The two component architectures are genuinely different, and
neither should be described in the other's terms.**

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
  reads on 2026-07-27; all ten were confirmed still registered at `295c253`. The
  Revit read surface was live-verified on 2026-07-29 at `ae01d29` (§4.4), with **no
  re-pin and no tool-count change**; the Revit MCP has no offline doctor, so no
  equivalent `TOOL_COUNT` line exists for it (§4.3).
- A re-pin driven by a reliability-only component change updates the revision and
  date but **must not** change any capability status; capability status changes
  only on evidence of a new or altered tool.
- Re-run the read-only inventory and update the counts, commit hashes, and date
  before each phase, or whenever a component publishes a relevant change.
- Component tool surfaces evolve; expectations are captured here in documentation,
  not by submodule pins (see
  [REPOSITORY_STRATEGY.md](REPOSITORY_STRATEGY.md)).

## 12. V1 cross-repository acceptance

`scripts/acceptance.py` checks that this repository, the APS/Forma MCP and the
Revit MCP describe **one coherent architecture**. It is a validator, not a gate
system, and it adds no governance state: every fact it checks is already asserted
somewhere in this repository.

**Eight assertions — seven executable, one documentary:**

| | Assertion | Kind |
|---|---|---|
| A1 | The capability contract is valid — vocabularies, unique ids, ADR-0009 cardinality | executable |
| A2 | Every `mcp_component` resolves to one declared component | executable |
| A3 | Tool assignment and capability ownership are coherent | executable |
| A4 | Published evidence validates against its schema | executable |
| A5 | Evidence provenance revisions resolve in the right component | executable |
| A6 | `confirmed` capabilities map to tools that really exist | executable |
| A7 | Registered component inventories are fully accounted for | executable |
| A8 | A read/write governance basis exists | **documentary** |

**A8 is deliberately not code.** ADR-0007 (Autodesk cloud branch) and
[ADR-0015](../decisions/0015-classify-local-automation-read-write-by-document-state.md)
(local Revit branch) already govern classification, including the two non-`GET`
reads and the write-by-capability treatment of `execute_revit_code`. The validator
names that basis; **it does not re-derive transaction or request semantics and
claims no proof of component internals.**

**Offline by design.** No Autodesk call, no running Revit, no MCP server, no
component doctor. Acceptance must be repeatable on any checkout, which is exactly
what a dependence on two live sessions would forfeit. Live verification happened
separately and is recorded per capability (§3.3, §4.4, §6.2, §6.3).

**Identity binding.** `config/components.example.yaml` declares an
`mcp_component` token per component. Neither token equals its repository slug and
no prefix or suffix rule works for both, so **the declaration is the binding** —
identity is never inferred, and never hardcoded in the validator.

**Committed-tree rule.** Every component fact is read from committed Git objects
(`git show <rev>:<path>`), with tool inventories extracted by Python AST from the
registration decorators. **A component working tree is never read.** The Revit
component's long-standing uncommitted line-ending churn and operator `main.py`
binding therefore cannot enter an inventory or a provenance check.

**Dirty worktrees are informational.** The validator reports a component's
working-tree state and continues. A dirty worktree is **not** an acceptance
failure; acceptance validates published component state, not an operator's desk.

**Historical provenance is valid.** A published artifact pins the revision it was
produced against, which normally *precedes* the accepted revision. A5 therefore
requires each `inspected_revision` to be a real commit **in the accepted lineage**
— never equality with HEAD, which would fail several valid published artifacts.

**Three tool categories** (`config/capability-tools.yaml`), the executable
projection of the boundaries §3 and §4 explain in prose:

- **capability tools** — belong to a governed capability record, and are what A6
  checks;
- **support tools** — runtime/infrastructure, deliberately not BIM capabilities
  (`get_revit_status`, `prepare_native_floor_stack_preview`). A support tool
  implies no capability, no implementation status and no readiness;
- **deferred tools** — real registered tools the V1 capability contract does not
  represent as governed capabilities. They are **not** unsafe, broken or
  abandoned — the Reviews and Relationships reads are implemented and
  live-verified — they are simply outside the governed V1 capability surface,
  each with a stated reason. A deferred tool creates no capability, receives no
  implementation status or readiness, and satisfies A6 for nothing.

**Prose is not parsed.** This document remains the architectural explanation;
the YAML map is what executes. Parsing the Markdown was considered and rejected:
§3 preserves a dated historical inventory, later tools are documented in §6.2 and
§6.3 instead, and backtick extraction also captures field names and capability
ids — so a prose parser reports failures that are not real.

**What acceptance proves.** That the reference architecture truthfully accounts
for the **complete** published component implementation surface, while
distinguishing governed capabilities from support tools and from functionality
deferred out of the V1 capability contract. **It does not prove that every
component tool has become a governed V1 capability**, and it is not intended to:
a deferred tool is an accounted-for tool, whereas an **unaccounted** tool is an
acceptance failure.

**`confirmed` never implies `ready`.** Implementation status and data readiness
are independent axes (ADR-0008), and the validator encodes no relationship
between them — three Revit capabilities are legitimately `confirmed` /
`not-assessed`. Nor is any evidence symmetry required between the components:
Revit does not use Phase-4 evidence, Forma has no Revit observation, and neither
needs a caller-context, OAuth or run-discipline analogue of the other.

**Requires** Python 3.9+, PyYAML, `jsonschema` and `git`; component paths come
from the declared `local_path_env` variables. **A component that cannot be
resolved makes the run INCOMPLETE and exits non-zero** — a skipped component
check never yields success.

### 12.1 V1 freeze — acceptance runs against pinned component revisions

Phase C validated whichever revision each component had **published most
recently**. V1 Freeze converts those accepted states into **durable pins**:
`config/v1-baseline.yaml` declares an `accepted_revision` per component, and
`scripts/acceptance.py` reads component facts at those revisions.

**Future component HEAD movement does not alter V1 validation.** If either
component advances, acceptance still extracts tool inventories, verifies
`confirmed` capabilities, accounts inventories and resolves evidence provenance
at the pinned revisions. **There is no fallback to HEAD**: a missing,
unresolvable or misdirected pin is fatal, and a pin whose `repository` disagrees
with the component declaration is rejected, so a pin cannot be silently
redirected at a different repository.

Everything else in §12 is unchanged. Component facts are still read **only** from
committed Git objects at the accepted revision, so a component working tree stays
**informational** and unreachable by extraction — the run reports current HEAD and
worktree state separately from the accepted revision, and never treats them as
acceptance input. Historical evidence remains valid by **ancestor relationship to
the accepted pin**, never by equality with it.

**This is not submodule pinning.** No source is vendored, no component checkout
is controlled, and no build dependency is pinned; the components remain separate
repositories referenced by identity and local path. The manifest records a
**historical accepted revision** and acceptance verifies that commit object
exists — which is precisely the failure mode
[ADR-0002](../decisions/0002-multi-repo-no-submodules.md) raised against
submodules, a pin that "silently rots", checked rather than assumed. **ADR-0002 is
not amended.**

The manifest deliberately carries **no capability lists, tool inventories, counts,
deferred-tool lists or debt registers** — V1 scope stays in
`config/workflows/end-to-end-reference.yaml` and `config/capability-tools.yaml`,
and `unaccounted = 0` remains the invariant A7 derives rather than a constant
anyone records. It also does **not** record the final V1 reference revision: a
file cannot contain the hash of the commit introducing it, so that revision is
identified by the annotated **`v1.0.0`** tag applied to the freeze commit.
