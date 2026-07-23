# PRD: Autodesk BIM Workflow Reference Implementation

**Status:** Active reference implementation — Phases 0, 1 and 2 complete;
Phase 3 capability planning in progress.
**Created:** 2026-07-22 · **Last reviewed:** 2026-07-23
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
configuration, synthetic examples, and validation utilities only. The
responsibility matrix and the dated capability ledger are defined in
[COMPONENT_BOUNDARIES.md](../architecture/COMPONENT_BOUNDARIES.md). The APS/Forma
MCP (`CognitiveStack/autodesk-aps-forma-mcp`) inventory is re-verified at
`a54acf8e5c628dbf7f97bf901a78f3c31c4b0781` and reports **26 registered MCP tools**
(24 read-only Autodesk, 1 guarded Autodesk write, 1 local-only preview), including
**seven Reviews reads and `list_issue_relationships`, all implemented and
live-verified** (Phase 2B). The Revit MCP baseline remains `ae01d29` (14 tools;
its pre-existing working-tree changes are unrelated and unresolved). **RFI and
Assets capabilities remain planned**, not confirmed.

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

- The two component repositories exist and are inventoried read-only; the APS/Forma
  MCP inventory has been **re-verified at `a54acf8`** (26 tools) and the Revit MCP
  baseline remains `ae01d29`. Running them locally requires the paths supplied via
  `FORMA_MCP_REPO` and `REVIT_MCP_REPO`.
- The Harrismith project and its CDE deliverable **exist and were successfully
  traced** in Phases 1 and 2 (a real Forma Data Management item and version).
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

Open:

- **RFI** capabilities: no MCP tools yet (planned); when and in which component?
- **Assets** capabilities: no MCP tools yet (planned); when and in which component?
- **Model Coordination clash-read availability**: does the current public API
  expose clash tests, clash results, clash groups, and clash status as reads?
- **Model Coordination model-set membership and version contracts**: endpoints for
  participating models and their coordinated versions.
- Verified, citable **maturity** of the APS APIs used by later stages (do not infer
  from product maturity; only Forma Site Design is confirmed Beta `v1alpha`).

## 15. Roadmap (summary)

Phased delivery follows the implementation priority in Section 8.

- **Phase 0 — complete.** Governance and foundations (this document set).
- **Phase 1 — complete.** Read-only Revit-to-CDE trace with committed sanitised
  evidence (Section 7).
- **Phase 2 — complete.** Issues and Reviews governance evidence: a complete
  read-only slice; write workflows remain deferred (Section 7A).
- **Phase 3 — planning in progress.** Model Coordination evidence (native engine;
  **no clash re-implementation**). See below.
- **Phase 4 — planned.** Forma Build construction information exchange and asset
  handover. See below.
- **Phase 5 — deferred experimental work.** Forma Site Design automation, isolated
  and non-blocking (Section 11).

### Phase 3 — Model Coordination evidence (planning in progress)

Phase 3A has identified **two separate gaps**:

1. **Capability gap** — the current component lacks clash-level, clash-group,
   clash-status, clash-membership, and resolution/recheck reads. Only model-set
   *listing* (`list_model_sets`) and coordination *issues* are read today.
2. **Data-readiness gap** — the tested Harrismith project currently exposes **no
   coordination model sets**.

A Model Coordination evidence run is therefore **not currently possible**. The
intended first scope is **provisional**:

```
model-set context
  → participating models and versions
    → coordination issue
      → assignment and status
        → shared-model-context comparison
```

This scope remains **blocked** until model-set membership reads and suitable
project data are available. Phase 3 will **not** claim a clash was identified,
linked to an issue, resolved, or geometrically verified, and will **not**
re-implement Autodesk clash detection.

### Phase 4 — Forma Build construction information exchange and asset handover (planned)

Forma Build is treated as a **family of module-specific capabilities, not one
monolithic API** (module-specific APS APIs such as Issues, RFIs, Submittals,
Forms, Sheets, Assets, and Cost Management). Provisional structure, **subject to
later capability verification**:

- **Phase 4A — construction information exchange:** RFIs, Submittals, Sheets and
  Meetings.
- **Phase 4B — field quality and execution:** Issues, Forms, inspections and
  construction records.
- **Phase 4C — asset handover:** Assets, equipment records, defects, inspections
  and handover information.

Shared platform services (Issues, Relationships, Data Management) may be used in
several phases; their use in Phase 2 or Phase 3 **does not** mean the complete
Forma Build phase has begun.
