# PRD: Autodesk BIM Workflow Reference Implementation

**Status:** Draft (Phase 0 foundations)
**Date:** 2026-07-22
**Terminology last verified:** 2026-07-22 (see
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
responsibility matrix and the capability-status labelling (confirmed / required /
planned) are defined in
[COMPONENT_BOUNDARIES.md](../architecture/COMPONENT_BOUNDARIES.md). Because the
component repositories were not inspected during Phase 0 orientation, this PRD
does not assert that any specific MCP tool or Autodesk API capability currently
exists.

## 7. First vertical slice (read-only)

**Slice: "Trace and verify a Revit deliverable from authoring to the CDE."**

The smallest valuable slice connects existing Revit work to Autodesk cloud
information management without any Forma Site Design Beta write functionality, and
remains strictly read-only:

1. Inspect an existing Harrismith Revit model through the Revit MCP.
2. Locate an existing uploaded or published deliverable in Forma Data Management
   through the APS/Forma MCP.
3. Retrieve its item and version information.
4. Retrieve derivative status or model properties where currently supported.
5. Compare selected Revit-side and cloud-side metadata.
6. Record a sanitised expected result under
   `examples/harrismith-fire-station/expected-results/`.

No upload or publishing write operation is introduced in the first slice; that is
a later, explicitly approved extension.

Capabilities required by steps 1–5 are labelled in
[COMPONENT_BOUNDARIES.md](../architecture/COMPONENT_BOUNDARIES.md) as one of:
*confirmed only after component inventory*, *required capability*, or *planned
capability*. Derivative and model-property tools in particular are **not** assumed
to exist yet.

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

- The two component repositories exist at the paths supplied via
  `FORMA_MCP_REPO` and `REVIT_MCP_REPO` and can be run locally.
- An existing Harrismith Revit model is available to inspect.
- A CDE location (Forma Data Management project / folder) exists or will exist to
  hold a published deliverable for the read-only slice.
- Synthetic, sanitised data can represent the project without licensed content.

## 13. Dependencies

- Revit MCP (`CognitiveStack/revit-mcp-triviron`).
- APS/Forma MCP (`CognitiveStack/autodesk-aps-forma-mcp`).
- Autodesk Platform Services APIs (Data Management, Model Derivative, and others
  as the workflow expands).
- A component inventory step to confirm available MCP tools before any capability
  is claimed.

## 14. Open questions

- Which specific MCP tools are actually exposed by each component today?
- Which APS APIs used by later stages (Issues, Reviews, RFI, Assets) are stable
  vs beta at build time? (To be verified and cited; do not infer from product
  maturity.)
- Is a real Forma Data Management project available for the Harrismith example,
  or must the slice run against a synthetic fixture?
- What sanitisation convention will represent hub / project / folder identifiers
  in recorded expected results?

## 15. Roadmap (summary)

Phased delivery follows the implementation priority in Section 8. Detailed
implementation tasks are intentionally deferred until Phase 0 foundations and the
component inventory validate the assumptions above.

- **Phase 0** — Governance and foundations (this document set).
- **Phase 1** — First read-only vertical slice (Section 7).
- **Phase 2** — Issues and reviews (read-first, guarded writes).
- **Phase 3** — Coordination evidence (native engine; no clash re-implementation).
- **Phase 4** — Construction information exchange and asset handover.
- **Phase 5** — Experimental Forma Site Design automation (isolated, deferred).
