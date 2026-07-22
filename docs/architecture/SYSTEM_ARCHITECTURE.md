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
- `config/workflows/end-to-end-reference.yaml` — the lifecycle stages, each with
  `platform`, `primary_system`, `api_families`, and `automation_policy`.

`api_families` is always a list and names API families only; it is not a maturity
claim, and stages with no confirmed family use `api_families: []` with
`api_mapping_status: to-be-verified`
([ADR-0003](../decisions/0003-autodesk-platform-product-and-api-terminology.md)).

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
