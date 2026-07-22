# Component Boundaries

**Status:** Draft (Phase 0 foundations)
**Date:** 2026-07-22

This document is the anti-duplication contract between this orchestration layer
and the two MCP components. It is consistent with the
[PRD](../prd/PRD_AUTODESK_BIM_WORKFLOW_REFERENCE_IMPLEMENTATION.md),
[SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md), and
[REPOSITORY_STRATEGY.md](REPOSITORY_STRATEGY.md), and is governed by
[ADR-0001](../decisions/0001-orchestration-layer-not-mcp-server.md) and
[ADR-0002](../decisions/0002-multi-repo-no-submodules.md).

## 1. Capability status labels

Because the component repositories were **not** inspected during Phase 0
orientation, no specific MCP tool is asserted to exist. Every capability
referenced anywhere in this project must carry one of these labels until a
component inventory resolves it:

- **confirmed-after-inventory** — believed to exist; to be confirmed by inspecting
  the component repository.
- **required-capability** — the workflow needs it; it must exist or be added.
- **planned-capability** — intended for a later phase; not needed yet.

Nothing here should be read as a claim that a tool currently exists.

## 2. Responsibility matrix

| Concern | Revit MCP | APS/Forma MCP | This repository |
|---|---|---|---|
| Revit authoring / inspection | Owns | — | Documents, invokes, validates |
| Autodesk authentication (APS) | — | Owns | Never implements |
| Forma Data Management (CDE) | — | Owns | Documents, invokes, validates |
| Model Derivative / properties | — | Owns | Documents, invokes, validates |
| Issues / Reviews / RFI / Assets | — | Owns | Documents, invokes, validates |
| Model Coordination (native engine) | — | Consumes / surfaces | Documents only |
| Clash detection | Must not build | Must not build | Must not build |
| Orchestration / docs / examples | — | — | Owns |
| Synthetic learning data | — | — | Owns |

"Owns" means the component is the source of truth for that behaviour. This
repository may **invoke** or **validate** a behaviour but must never
**re-implement** it ([ADR-0001](../decisions/0001-orchestration-layer-not-mcp-server.md)).

## 3. Revit MCP (`CognitiveStack/revit-mcp-triviron`)

- **Role:** Revit / pyRevit authoring and inspection.
- **Referenced locally via:** `REVIT_MCP_REPO`.
- **Capabilities relied on by the first slice** (all *confirmed-after-inventory*):
  read an existing Revit model's identifying and selected element/level/view
  metadata for comparison against cloud-side data.
- **Must-not:** the orchestration layer must not reproduce Revit or pyRevit logic.

## 4. APS/Forma MCP (`CognitiveStack/autodesk-aps-forma-mcp`)

- **Role:** focused cloud and information-management actions on Autodesk Forma via
  Autodesk Platform Services.
- **Referenced locally via:** `FORMA_MCP_REPO`.
- **Capabilities relied on by the first slice:**
  - Locate an existing deliverable in Forma Data Management —
    *confirmed-after-inventory*.
  - Retrieve item and version information — *confirmed-after-inventory*.
  - Retrieve derivative status or model properties — *required-capability*
    (explicitly **not assumed to exist**; confirm or add before use).
- **Must-not:** the orchestration layer must not implement APS authentication,
  API clients, or derivative processing.

## 5. First-slice capability ledger

| Slice step | Capability | Status |
|---|---|---|
| 1. Inspect Revit model | Revit model / metadata read (Revit MCP) | confirmed-after-inventory |
| 2. Locate deliverable in CDE | Forma Data Management listing (APS/Forma MCP) | confirmed-after-inventory |
| 3. Item / version info | Item + version read (APS/Forma MCP) | confirmed-after-inventory |
| 4. Derivative / properties | Model Derivative / properties read (APS/Forma MCP) | required-capability |
| 5. Compare metadata | Comparison / validation utility (this repo) | planned-capability |
| 6. Record sanitised result | Sanitisation + fixture (this repo) | planned-capability |

## 6. Anti-duplication rules

- Do not copy or vendor component source; no Git submodules
  ([ADR-0002](../decisions/0002-multi-repo-no-submodules.md)).
- Do not re-implement authentication, derivative processing, or clash detection.
- Utilities in `scripts/` call component tools or validate their outputs; they do
  not reproduce internal logic.
- When a capability is missing, raise it in the owning component repository rather
  than working around it here.

## 7. Drift management

Component tool surfaces will change over time. This repository pins expectations
through documentation and the capability ledger above, not through submodule
commits. A component inventory should re-confirm labels before each phase; see
[REPOSITORY_STRATEGY.md](REPOSITORY_STRATEGY.md).
