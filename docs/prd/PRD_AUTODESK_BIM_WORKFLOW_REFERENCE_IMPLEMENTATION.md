# PRD: Autodesk BIM Workflow Reference Implementation

**Status:** Active reference implementation — Phases 0, 1, 2 and 3 complete.
Phase 3 closed at its evidence ceiling **`shared_model_context_proven`**: a
coordination issue and a coordination snapshot were proven to refer to the same
models at the same coordinated versions. **Clash-level reads remain
unimplemented**, so a direct clash-to-issue link and geometric resolution remain
**unproven**. Phase 4A (capability research) is next.
**Created:** 2026-07-22 · **Last reviewed:** 2026-07-24
**Terminology last verified:** 2026-07-23 (see
[GLOSSARY.md](../guides/GLOSSARY.md) and
[ADR-0003](../decisions/0003-autodesk-platform-product-and-api-terminology.md))

This document defines *what* the reference implementation demonstrates and *why*.
The *how* is described in the architecture documents
([SYSTEM_ARCHITECTURE.md](../architecture/SYSTEM_ARCHITECTURE.md),
[COMPONENT_BOUNDARIES.md](../architecture/COMPONENT_BOUNDARIES.md),
[REPOSITORY_STRATEGY.md](../architecture/REPOSITORY_STRATEGY.md)).

## 1. Purpose and audience

An educational reference that demonstrates an end-to-end Autodesk BIM information
workflow, from site and concept design through Revit authoring, common data
environment (CDE) management, coordination, review, construction information
exchange, and asset handover.

The audience is Autodesk developers and BIM practitioners who want a worked,
reproducible example of how these stages connect, using stable Autodesk Platform
Services (APS) APIs and MCP automation where automation genuinely simplifies the
workflow.

## 2. Problem statement and learning objectives

BIM workflows are usually learned in fragments — a Revit tutorial here, a CDE
permissions guide there — with little that shows the *information* flowing
end-to-end across the platform. This project addresses that by tracing one
synthetic project across the whole lifecycle.

Learning objectives:

- Understand the canonical BIM lifecycle stages and how information passes
  between them.
- See where automation adds value and where manual work is appropriate.
- Distinguish the Autodesk Forma platform, its product offerings, and the APS API
  family (per [ADR-0003](../decisions/0003-autodesk-platform-product-and-api-terminology.md)).
- Learn a safe, read-first, write-guarded posture for touching cloud data.

## 3. Scope

**In scope**

- Orchestration and documentation of the end-to-end workflow.
- Configuration describing how the two MCP components are wired together.
- Python integration and validation utilities that invoke or verify component
  behaviour.
- The Harrismith BIM Learning Project as the principal synthetic example.
- A read-only first vertical slice (Section 7).

**Out of scope**

- Implementing an MCP server in this repository
  ([ADR-0001](../decisions/0001-orchestration-layer-not-mcp-server.md)).
- Copying or vendoring component source; Git submodules
  ([ADR-0002](../decisions/0002-multi-repo-no-submodules.md)).
- Re-implementing native Autodesk engines such as clash detection.
- Complete Autodesk API coverage (Section 4).

## 4. Complete API coverage is not the objective

The goal is to **demonstrate the BIM workflow**, not to wrap every Autodesk API.
Breadth is added only where it advances the end-to-end narrative. Where an
Autodesk product provides a capability that the API does not conveniently expose,
a manual or hybrid workflow is acceptable and preferred over speculative
automation.

## 5. Workflow modes

Every stage is delivered in one of three explicit modes:

- **Manual** — performed by a person in an Autodesk product UI. Documented as
  steps; no automation claimed.
- **API-assisted** — a person drives the workflow while APS APIs or MCP tools
  perform focused read or verification actions.
- **Automated** — an MCP tool performs the action end-to-end, always read-only by
  default and write-guarded behind explicit approval.

The mode for each stage is recorded alongside the workflow definition and may be
hybrid across a single stage.

## 6. Components and boundaries (summary)

Two independently maintained MCP components are coordinated, not absorbed:

- **Revit MCP** — `CognitiveStack/revit-mcp-triviron`: Revit authoring and
  inspection.
- **APS/Forma MCP** — `CognitiveStack/autodesk-aps-forma-mcp`: focused cloud and
  information-management actions.

They remain in their own repositories. This repository owns documentation,
configuration, synthetic examples, and validation utilities only.

**[COMPONENT_BOUNDARIES.md](../architecture/COMPONENT_BOUNDARIES.md) is the single
source of truth** for the responsibility matrix, the dated capability ledger, and
the tool inventory. This PRD does not restate per-capability counts; consult the
ledger for the authoritative figures.

Current baseline recorded there, re-verified locally on 2026-07-24:

- **APS/Forma MCP** (`CognitiveStack/autodesk-aps-forma-mcp`) at
  `75b36b2635de3a5707fd1ff3dbf5cd487e3f0e0a` — **30 registered MCP tools**
  (28 read-only Autodesk, 1 guarded Autodesk write, 1 local-only preview),
  evidenced by the offline doctor `TOOL_COUNT=30`, `RESULT=PASS`. This includes
  **seven Reviews reads and `list_issue_relationships`** (Phase 2B) and the **five
  Model Coordination model-set/version reads** — `list_model_sets`,
  `get_model_set`, `list_model_set_versions`, `get_latest_model_set_version`,
  `get_model_set_version` — all implemented and live-verified (2026-07-23).
- **Revit MCP** baseline remains `ae01d29` (14 tools; its pre-existing
  working-tree changes are unrelated and unresolved).

The most recent component change (`75b36b2`) is a **reliability-only** increment:
bounded token-refresh lock acquisition, explicit HTTP connect/read/write/pool
timeouts, and structured timeout/transport errors. The **tool count is unchanged**
and it introduces **no new Autodesk capability** and no public tool-contract change
(see [COMPONENT_BOUNDARIES.md](../architecture/COMPONENT_BOUNDARIES.md) §3.2).

**RFI and Assets capabilities remain planned**, not confirmed. Clash-level Model
Coordination reads remain **unimplemented** (§14).

## 7. First vertical slice (read-only) — complete

**Slice: "Trace and verify a Revit deliverable from authoring to the CDE."**
**Status: complete (Phase 1).**

The smallest valuable slice connects existing Revit work to Autodesk cloud
information management without any Forma Site Design Beta write functionality, and
remained strictly read-only:

1. Inspect an existing Harrismith Revit model through the Revit MCP.
2. Locate an existing uploaded or published deliverable in Forma Data Management
   through the APS/Forma MCP.
3. Retrieve its item and version information.
4. Retrieve derivative status or model properties where currently supported.
5. Compare selected Revit-side and cloud-side metadata.
6. Record a sanitised expected result under
   `examples/harrismith-fire-station/expected-results/`.

No upload or publishing write operation was introduced; that remains a later,
explicitly approved extension.

Phase 1 delivered a **live read-only Revit-to-CDE trace**, **sanitised evidence**,
**schema validation**, and a **committed canonical result artifact**
(`revit-to-cde-trace.result.json`). The evidence was structured through an
**operator-mediated workflow** (a chat-mediated sanitised handoff), not through a
general-purpose orchestration utility; no such comparison/sanitisation utility
needs to be built for the slice to be complete.

## 7A. Governance slice — Review-to-Issue (Phase 2) — complete

**Slice: "Review-to-Issue Governance Trace."** **Status: complete (Phase 2),
strictly read-only.**

Phase 2 delivered:

- **Reviews read capability** (seven read-only tools) and **issue Relationships
  read capability** (`list_issue_relationships`), implemented and live-verified in
  the component;
- a **live read-only Review-to-Issue governance trace**;
- **shared document-lineage proof** (the issue's explicit document reference
  matched the reviewed document lineage);
- **sanitised, schema-validated evidence**
  (`review-to-issue-trace.result.json`).

Qualifications preserved from the evidence:

- **no exact document-version match** was proven (lineage is a weaker proof);
- **no direct Review-to-Issue relationship** was claimed;
- **no review, issue, or relationship writes** were performed.

## 7B. Coordination slice — Model Coordination-to-Issue (Phase 3) — complete

**Slice: "Model Coordination-to-Issue Trace."** **Status: complete (Phase 3),
strictly read-only**, at the evidence ceiling `shared_model_context_proven`.

Sub-phase status:

- **Phase 3A — planning and schema:** complete.
- **Phase 3B — model-set and snapshot foundation:** complete.
- **Phase 3C — issue and shared-model-context trace:** complete.
- **Phase 3D — sanitised public evidence artifact:** complete.

**Strongest proven result: `shared_model_context_proven`.**

**Proven:**

- `MODEL_SET_1` exists;
- `MODEL_SET_VERSION_1` was retrieved (the coordination snapshot);
- it contains **two** participating coordinated document versions;
- `ISSUE_1` carries a **typed placement-lineage reference**;
- that reference **exactly matches `MODEL_1`'s** participant lineage in the
  snapshot;
- **two viewer-state-derived version references** exactly match `VERSION_1` and
  `VERSION_2`, the coordinated versions of the two participating documents;
- the issue and the two coordinated models therefore share **machine-readable
  model context**.

**Not proven:**

- a Relationships API document record (`list_issue_relationships` returned zero
  records — that proves only that no matching record was returned, not that the
  issue is unrelated in the project or the Autodesk UI);
- a typed issue-to-model-set relationship;
- a typed issue-to-snapshot relationship;
- a direct clash-to-issue link;
- clash membership;
- geometric resolution.

**Contextual only** (never treated as proof):

- the Forma UI **Clashes tab** association;
- viewer-state element isolation;
- issue type or title;
- the issue having been created while a clash was selected.

**Canonical artifact:**
`examples/harrismith-fire-station/expected-results/model-coordination-to-issue-trace.result.json`
— sanitised, schema-validated, `execution.status: complete`.

No coordination was run, no model uploaded or published, and no issue created or
changed. Issue creation remains a **manual Autodesk-UI action** unless a separate
write workflow is explicitly approved.

## 8. Lifecycle order vs implementation priority

These two orderings are deliberately different and must not be conflated.

**A. BIM lifecycle order** (how a real project unfolds):

```
Site → Concept → Revit design → CDE → Coordination → Construction → Handover
```

**B. Implementation priority** (the order this project builds things):

```
Governance
  → stable read-only CDE slice
  → issues / reviews
  → coordination evidence
  → handover
  → additional experimental Site Design automation
```

Forma Site Design appearing late in the implementation priority means additional
Beta API automation is deferred. It does **not** mean site design happens late in
the BIM lifecycle — in the lifecycle, site and concept come first.

## 9. Success criteria

- A learner can follow the first vertical slice end-to-end using synthetic data
  and reproduce the recorded, sanitised expected result.
- Documentation uses consistent terminology per
  [ADR-0003](../decisions/0003-autodesk-platform-product-and-api-terminology.md).
- No credentials, tokens, or real Autodesk identifiers appear in the repository.
- Every referenced MCP tool or API capability is either verified or explicitly
  labelled by capability status; no unverified capability is claimed as existing.

## 10. Non-goals

- Not a production system and not an MCP server.
- Not complete API coverage.
- Not a re-implementation of native Autodesk engines (for example clash
  detection).
- Not a source of real project data, credentials, or licensed Autodesk content.

## 11. Experimental work: Forma Site Design Beta

Forma Site Design Beta automation is **experimental and non-blocking**. It is
isolated from the stable path, treated as read-first, and deferred in
implementation priority. No part of the first vertical slice depends on it.

## 12. Assumptions

- The two component repositories exist and are inventoried read-only; the current
  pinned revisions and tool counts live in
  [COMPONENT_BOUNDARIES.md](../architecture/COMPONENT_BOUNDARIES.md) (§1) and are
  not duplicated here. Running them locally requires the paths supplied via
  `FORMA_MCP_REPO` and `REVIT_MCP_REPO`.
- The Harrismith project and its CDE deliverable **exist and were successfully
  traced** in Phases 1, 2 and 3 (a real Forma Data Management item and version).
- Coordination **data readiness is satisfied**: an isolated training coordination
  space exists with automatic clash processing enabled, two discipline-context
  models were processed, and both participating document versions are readable
  through the version-level Model Coordination reads. Clash results are visible in
  the Autodesk interface but are **not readable through the API**.
- The **sanitisation convention exists and was applied** (see
  [SANITISATION_CONVENTION.md](../guides/SANITISATION_CONVENTION.md)); synthetic,
  sanitised aliases represent the project without licensed content.

## 13. Dependencies

- Revit MCP (`CognitiveStack/revit-mcp-triviron`).
- APS/Forma MCP (`CognitiveStack/autodesk-aps-forma-mcp`).
- Autodesk Platform Services APIs (Data Management, Model Derivative, and others
  as the workflow expands).
- The dated component capability ledger in
  [COMPONENT_BOUNDARIES.md](../architecture/COMPONENT_BOUNDARIES.md), re-verified
  before each phase.

## 14. Open questions

Resolved since Phase 0 (retained here as record): a real Forma Data Management
project/deliverable **is** available (traced in Phase 1); the **sanitisation
convention** is defined and applied; **Reviews and issue-relationship MCP reads
now exist** (Phase 2B).

**Resolved in Phase 3B (2026-07-23) — Model Coordination model-set membership and
coordinated-version contracts.** Participating models and their exact coordinated
versions are read through `get_latest_model_set_version` / `get_model_set_version`.
The following rules are **governing constraints**, not incidental notes:

- `version_urn` is the **exact coordinated document version**;
- `lineage_urn` is the **stable document lineage**;
- `tip_version_urn` is **never substituted** for `version_urn`;
- **model-set snapshot numbering and Data Management document-version numbering are
  separate domains** and must never be conflated;
- **no numeric document version is inferred from a URN**;
- **no discipline is inferred** — from filenames, display names, folders, model
  titles, or viewer context. A null discipline is a faithful record, not a defect.

Open:

- **Model Coordination clash-read availability**: does the current public API
  expose clash tests, clash results, clash groups, clash membership, and clash
  status as reads? **Still unresolved** — no clash-level read exists in the
  component, and no clash identifier, group, member, or origin field was returned
  in Phase 3. This is the gate for the optional Phase 3E spike (§15).
- **RFI** capabilities: no MCP tools yet (**planned**); when and in which component?
- **Assets** capabilities: no MCP tools yet (**planned**); when and in which component?
- **Submittals**: **unassessed** — named in the Phase 4A grouping only; no APS
  capability research has been performed and no MCP tool exists.
- **Sheets**: **unassessed** — and requires **domain disambiguation** before any
  status is assigned. The component's existing `list_model_views` and
  `get_derivative_manifest` are **Model Derivative** reads and are **not** a Sheets
  module; the two must not be conflated.
- **Meetings**: **unassessed / deferred** — no APS capability research performed;
  unsupported until verified.
- Verified, citable **maturity** of the APS APIs used by later stages (do not infer
  from product maturity; only Forma Site Design is confirmed Beta `v1alpha`).

**Classification discipline.** `planned` means a later-phase capability this
project has governed and intends to build; `unassessed` means no authoritative
research has been done at all. A module is **never** upgraded from *unassessed* to
*planned* because it is visible in the Autodesk product UI — only authoritative
APS capability verification moves it (§15, Phase 4A entry gate).

## 15. Roadmap (summary)

Phased delivery follows the implementation priority in Section 8.

- **Phase 0 — complete.** Governance and foundations (this document set).
- **Phase 1 — complete.** Read-only Revit-to-CDE trace with committed sanitised
  evidence (Section 7).
- **Phase 2 — complete.** Issues and Reviews governance evidence: a complete
  read-only slice; write workflows remain deferred (Section 7A).
- **Phase 3 — complete.** Model Coordination evidence at the ceiling
  `shared_model_context_proven` (native engine; **no clash re-implementation**);
  clash-level reads remain unimplemented and deferred (Section 7B). See below.
- **Phase 3E — optional, non-blocking research spike.** Direct clash-provenance
  research. Not required to close Phase 3 and **not** on the Phase 4 critical path.
  See below.
- **Phase 4 — next formal phase; capability research first.** Forma Build
  construction information exchange and asset handover. See below.
- **Phase 5 — deferred experimental work.** Forma Site Design automation, isolated
  and non-blocking (Section 11).

### Phase 3 — Model Coordination evidence (complete)

Phase 3 was executed read-only and closed at the evidence ceiling
`shared_model_context_proven`. The full proof, its negative boundaries, and the
canonical artifact are recorded in Section 7B.

The scope that was executed:

```
model-set context
  → participating models and versions
    → coordination issue
      → assignment and status
        → shared-model-context comparison
```

Both original Phase 3A gaps were closed or narrowed:

1. **Data-readiness gap — closed.** A usable training coordination model set with
   two processed discipline-context models exists, and both participating document
   versions are readable.
2. **Capability gap — narrowed, not closed.** The model-set/version foundation is
   implemented and live-verified (model-set discovery and detail, snapshot version
   history, latest/specific snapshots, participating documents, exact coordinated
   versions, stable lineage references). What the component still **cannot** read:
   clash tests, clash results, clash identifiers, clash groups, clash membership,
   clash status or review state, a direct clash-to-issue relationship, clash
   history across snapshots, or geometric-resolution verification.

Phase 3 **did not** claim a clash was identified, linked to an issue, resolved, or
geometrically verified, and **did not** re-implement Autodesk clash detection.
Those boundaries are permanent properties of the recorded evidence, not pending
work items.

### Phase 3E — optional clash-provenance research spike

An **optional** research spike into direct clash provenance. It is explicitly:

- **optional** — Phase 3 is already complete without it;
- **non-blocking** — it does **not** gate any other phase;
- **not on the Phase 4 critical path** — Phase 4A proceeds regardless of whether
  this spike is ever opened, run, or completed;
- **opened only after** a documented or discoverable **read-only** Autodesk clash
  surface is identified. Until then it stays closed.

If opened, it may investigate clash identifiers, clash groups, clash
members/object references, clash state or review state, direct clash-to-issue
provenance, and clash history across coordination snapshots.

**No claim that any such capability exists** is made until it is verified against
current official Autodesk/APS documentation **and** a real response. Failing to
find such a surface is a **valid negative research result** and a publishable
outcome (`clash_relationship_not_proven`), not a failure of the spike.

Phase 3E is a distinct label from **Phase 3D**, which is the completed sanitised
public evidence artifact increment (Section 7B).

### Phase 4 — Forma Build construction information exchange and asset handover (next formal phase)

Autodesk Build / Forma Build is treated as a **family of module-specific
capabilities, not one monolithic API** (module-specific APS APIs such as Issues,
RFIs, Submittals, Forms, Sheets, Assets, and Cost Management). There is no single
"Forma Build API", and none may be assumed. Provisional structure, **subject to
capability verification**:

- **Phase 4A — construction information exchange:** RFIs, Submittals, Sheets and
  Meetings.
- **Phase 4B — field quality and execution:** Issues, Forms, inspections and
  construction records.
- **Phase 4C — asset handover:** Assets, equipment records, defects, inspections
  and handover information.

Shared platform services (Issues, Relationships, Data Management) may be used in
several phases; their use in Phase 2 or Phase 3 **does not** mean the complete
Forma Build phase has begun.

#### Phase 4A begins as capability research, not implementation

Phase 4A is the next formal phase, but its **first increment is authoritative APS
capability research** — not tool implementation. **None** of the four Phase 4A
modules is currently verified by repository evidence, and no MCP tool exists for
any of them.

| Module | Classification | Status |
|---|---|---|
| **RFIs** | **Provisional first research candidate.** Closest structural analogue to the Issues reads already proven in Phases 2 and 3 | Research only; **implementation not yet approved** |
| **Submittals** | **Research-only candidate** | No capability research performed; unassessed |
| **Sheets** | **Research-only candidate**, requiring **domain disambiguation** — must **not** be confused with the component's Model Derivative model views (`list_model_views`) or manifests (`get_derivative_manifest`) | No capability research performed; unassessed |
| **Meetings** | **Deferred** | **Unsupported until verified**; no capability research performed |

Selecting RFIs as the provisional first candidate is a **research** decision. If
research shows the RFI read surface is undocumented, entitlement-gated, or
otherwise unsuitable, the candidate is re-selected on evidence — never by
defaulting to implementation.

#### Phase 4A entry gate

All ten items must be satisfied **before any Phase 4A implementation increment**:

1. **Authoritative APS capability verification** — each candidate module verified
   against current official Autodesk/APS documentation. No endpoint path is
   recorded here until confirmed; no capability is asserted from product
   marketing, UI presence, or analogy to an existing API.
2. **Supported authentication-scope verification** — required OAuth scopes
   identified and confirmed compatible with the component's existing auth model.
   Any new scope, consent step, or account entitlement is a gate item, not a
   mid-implementation discovery.
3. **Read/write operation inventory** — every operation classified read vs write
   *before* selection, with the write set explicitly excluded from the first slice.
4. **Data-model and identifier-domain analysis** — entity identity, lineage,
   versioning and container scoping mapped, stating explicitly which identifier
   domains are **separate** (applying the Phase 3 lesson that a coordination
   snapshot version is not a document version).
5. **Privacy and sanitisation rules** — the alias tokens the module needs are
   defined **before** any evidence is captured. Free-text fields (RFI questions and
   answers, meeting minutes) carry higher leakage risk than Phase 1–3 metadata:
   sanitised structural summaries only, never verbatim body text.
6. **Component-boundary decision** — recorded per module: APS/Forma MCP, Revit MCP,
   or this repository, per [ADR-0001](../decisions/0001-orchestration-layer-not-mcp-server.md)
   and [ADR-0002](../decisions/0002-multi-repo-no-submodules.md). No orchestration-layer
   re-implementation.
7. **Read-only-first sequencing** — Phase 4A is read-only. Writes require a
   separate, explicitly approved increment after the read slice is complete and
   evidenced.
8. **Harrismith Fire Station learning scenario and data-readiness check** — a
   documented synthetic scenario **plus** a separate confirmation that the example
   project holds the data needed. Capability readiness and data readiness are
   independent gates; in Phase 3 they blocked separately.
9. **No unsupported write workflow** — no create, update, close, assign, or attach
   operation on any Phase 4A module.
10. **No monolithic "Forma Build API" assumption** — each module is researched,
    named, and statused independently.
