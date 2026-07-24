# Autodesk BIM Workflow Reference Implementation

An educational reference implementation demonstrating an end-to-end Autodesk
BIM information workflow from site and concept design through Revit authoring,
common data environment management, coordination, review, construction
information exchange, and asset handover.

The Harrismith BIM Learning Project is the primary example used throughout the
repository.

## Project goals

1. Demonstrate the Autodesk BIM workflow from concept to handover.
2. Use APIs and MCP automation where they genuinely simplify the workflow.
3. Prefer stable Autodesk Platform Services APIs for core demonstrations.
4. Isolate experimental Forma Site Design Beta functionality.
5. Preserve manual Autodesk workflows where API automation would add excessive
   complexity.
6. Provide a reusable Python-oriented learning resource for Autodesk developers.

## Component repositories

This repository coordinates and documents two independently maintained
software components:

- `CognitiveStack/autodesk-aps-forma-mcp`
  - Autodesk Platform Services and Forma integration
  - Currently confirmed read capabilities: Data Management, Model Derivative,
    Issues, Reviews, issue Relationships, and Model Coordination
    model-set/version reads, plus Forma Site Design (Beta `v1alpha`) reads and a
    single guarded Beta write
  - See [COMPONENT_BOUNDARIES.md](docs/architecture/COMPONENT_BOUNDARIES.md) for
    the authoritative, dated capability ledger

- `CognitiveStack/revit-mcp-triviron`
  - Revit and pyRevit MCP automation
  - Revit model creation, inspection, views, sheets, and authoring workflows

The component repositories remain separate Git repositories. They are not
embedded as submodules.

## Reference workflow

```text
Site and context
    -> Concept design
    -> Revit authoring
    -> CDE information management
    -> Model coordination
    -> Reviews and issues
    -> Construction information exchange
    -> Asset handover
```
## Current Status

**Phases 0, 1, 2 and 3 are complete**, all strictly read-only, each with a
sanitised public evidence artifact committed under
[`examples/harrismith-fire-station/expected-results/`](examples/harrismith-fire-station/expected-results/):

| Phase | Slice | Artifact |
|---|---|---|
| 1 | Revit-to-CDE trace | `revit-to-cde-trace.result.json` |
| 2 | Review-to-Issue governance trace | `review-to-issue-trace.result.json` |
| 3 | Model Coordination-to-Issue trace | `model-coordination-to-issue-trace.result.json` |

The current **Phase 3 evidence ceiling is `shared_model_context_proven`**: a
coordination issue and a coordination snapshot were proven to refer to the same
models at the same coordinated versions. Clash-level reads remain unimplemented, so
a **direct clash-to-issue link and geometric resolution remain unproven**.

**Next: Phase 4A — construction information exchange, beginning with authoritative
APS capability research, not implementation.** RFIs are the provisional first
research candidate; Submittals and Sheets are research-only candidates; Meetings
are deferred. None of these is implemented, and no MCP tool exists for any of them.

See the
[PRD](docs/prd/PRD_AUTODESK_BIM_WORKFLOW_REFERENCE_IMPLEMENTATION.md) for the
roadmap and the Phase 4A entry gate.
