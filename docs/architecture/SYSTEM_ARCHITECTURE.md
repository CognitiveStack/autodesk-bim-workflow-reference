# System Architecture

**Status:** Draft (Phase 0 foundations)
**Date:** 2026-07-22
**Terminology last verified:** 2026-07-22

This document describes the system as a whole. It is consistent with the
[PRD](../prd/PRD_AUTODESK_BIM_WORKFLOW_REFERENCE_IMPLEMENTATION.md),
[COMPONENT_BOUNDARIES.md](COMPONENT_BOUNDARIES.md), and
[REPOSITORY_STRATEGY.md](REPOSITORY_STRATEGY.md). Terminology follows
[ADR-0003](../decisions/0003-autodesk-platform-product-and-api-terminology.md)
and [GLOSSARY.md](../guides/GLOSSARY.md).

## 1. Context

This repository is an orchestration, documentation, and educational reference
layer. It does not implement MCP tooling
([ADR-0001](../decisions/0001-orchestration-layer-not-mcp-server.md)). It
coordinates two independent MCP components against the Autodesk Forma platform and
its APS API family.

```
        Learner / MCP client (e.g. Claude Code)
                     |
                     v
   +-----------------------------------------+
   |  This repository (orchestration layer)  |
   |  docs · config · synthetic examples ·   |
   |  Python validation utilities            |
   +-----------------------------------------+
            |                     |
            v                     v
   +----------------+     +----------------------+
   |   Revit MCP    |     |   APS/Forma MCP      |
   | revit-mcp-     |     | autodesk-aps-forma-  |
   | triviron       |     | mcp                  |
   +----------------+     +----------------------+
            |                     |
            v                     v
   +----------------+     +----------------------+
   | Autodesk Revit |     | Autodesk Forma       |
   | (desktop)      |     | platform via APS     |
   +----------------+     +----------------------+
```

The orchestration layer never talks to Autodesk directly; it documents and
coordinates the components, which own the Autodesk integration.

## 2. Runtime and control flow

- An MCP client (for example Claude Code) is the entry point; a person remains in
  control.
- The default posture is **read-first and write-guarded**: read and verification
  actions run freely; write actions require explicit approval
  (`writes_require_explicit_approval: true` in project config).
- The first vertical slice is strictly read-only across both components (see the
  [PRD](../prd/PRD_AUTODESK_BIM_WORKFLOW_REFERENCE_IMPLEMENTATION.md), Section 7).
- This repository's Python utilities *invoke or validate* component behaviour;
  they never re-implement Autodesk logic
  ([ADR-0001](../decisions/0001-orchestration-layer-not-mcp-server.md)).

## 3. Data and artifact flow

The reference traces information across the BIM lifecycle
(Site → Concept → Revit design → CDE → Coordination → Construction → Handover).
For the first slice, the flow is:

1. Revit-side metadata read from an existing Harrismith model (via Revit MCP).
2. Cloud-side item and version metadata read from Forma Data Management (via
   APS/Forma MCP).
3. Selected metadata compared and recorded as a **sanitised** expected result
   under `examples/harrismith-fire-station/expected-results/`.

Real model binaries (`.rvt`, `.nwc`, `.ifc`, and similar) are git-ignored and
never committed; only synthetic, sanitised artifacts are stored.

## 4. Configuration model

Three configuration files compose the picture (examples only; local overrides are
git-ignored):

- `config/components.example.yaml` — identifies the two components and their local
  path environment variables (`FORMA_MCP_REPO`, `REVIT_MCP_REPO`).
- `config/projects/harrismith.example.yaml` — the Harrismith project and its
  safety switches.
- `config/workflows/end-to-end-reference.yaml` — the lifecycle stages,
  `schema_version: 2`. A **stage** is the BIM workflow / teaching category and
  carries only `id`, `platform`, `automation_policy` and `capabilities`. A
  **capability** inside a stage is the unit of implementation governance and
  carries `id`, `primary_system`, `api_maturity`, `mcp_component`,
  `mcp_implementation_status` and `data_readiness` (required), `api_family` and
  `api_version` (conditional), and `data_readiness_reason` (optional).
  Vocabularies: `api_maturity` (`beta` / `ga` / `to-be-verified` /
  `not-applicable`), `mcp_implementation_status` (`confirmed` / `partial` /
  `planned` / `not-applicable`), `data_readiness` (`ready` / `blocked` /
  `not-assessed`).

Capabilities within one stage may differ independently on every axis: MCP
ownership and coverage, API maturity, and project-data readiness are recorded as
separate capability-level fields so they are never conflated, and no GA/stable
maturity is claimed without a cited source
([ADR-0003](../decisions/0003-autodesk-platform-product-and-api-terminology.md)).
`api_version` records the API contract / request-route version — not the
documentation-set version — and is required whenever `api_maturity` makes a
concrete lifecycle assertion (`beta` or `ga`). `capabilities: []` means a stage
has **no governed capability**, not merely no implementation, no asserted API
family, or no ready data. The governing decisions are
[reference-repo ADR-0008](../decisions/0008-govern-implementation-state-per-capability.md)
(stage versus capability granularity) and
[reference-repo ADR-0009](../decisions/0009-define-capability-record-cardinality-for-schema-v2.md),
which carries the authoritative cardinality table.

## 5. Trust and security boundaries

- Credentials and tokens live only in the component repositories' own runtime and
  in a git-ignored local `.env`; they are never stored here.
- `.env.example` contains safe placeholders only.
- Autodesk project / hub / folder identifiers are treated as sensitive and are
  sanitised before being recorded.
- Write operations cross a trust boundary and require explicit approval.

See [REPOSITORY_STRATEGY.md](REPOSITORY_STRATEGY.md) for the full public-repo
hygiene rules.

## 6. Stable vs experimental partitioning

- Stable, read-first APS-based workflows form the core path.
- Forma Site Design Beta automation is isolated and treated as experimental and
  non-blocking; nothing on the core path depends on it.
- API maturity is asserted only where verified and cited; otherwise it is marked
  "to be verified". Maturity is never inferred from product maturity.

## 7. Terminology model applied

Throughout this architecture: **Autodesk Forma** is the platform; **Forma Data
Management**, **Forma Build**, **Model Coordination**, **Design Collaboration**,
and **Forma Site Design** are offerings; **Autodesk Platform Services (APS)** is
the API family. Historical names are used only where accurate. See
[GLOSSARY.md](../guides/GLOSSARY.md).
