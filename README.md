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
    Issues, Reviews, issue Relationships, Model Coordination model-set/version
    reads, and the Phase 4A Transmittals, RFI and Submittals first-slice reads,
    plus Forma Site Design (Beta `v1alpha`) reads and a single guarded Beta write
  - See [COMPONENT_BOUNDARIES.md](docs/architecture/COMPONENT_BOUNDARIES.md) for
    the authoritative, dated capability ledger

- `CognitiveStack/revit-mcp-triviron`
  - Revit and pyRevit MCP automation
  - Revit model creation, inspection, views, and authoring workflows

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

**V1 is complete and frozen as `v1.0.0`.** The annotated tag identifies reference
commit `ffa6d460d30ab267ccb31947d1081a9088a2f97c`, accepted against component
revisions `f763d190871743e4c638902ddd6fdadf2d740e88` (`aps-forma-mcp`) and
`ae01d292735549ac406e5e7101620e64a5477970` (`revit-mcp`), declared in
[`config/v1-baseline.yaml`](config/v1-baseline.yaml).

**Phases 0, 1, 2 and 3 are complete, and the Phase 4A Forma proving ground is
complete.** Every slice is strictly read-only, and each has a sanitised public
evidence artifact committed under
[`examples/harrismith-fire-station/expected-results/`](examples/harrismith-fire-station/expected-results/):

| Phase | Slice | Artifact |
|---|---|---|
| 1 | Revit-to-CDE trace | `revit-to-cde-trace.result.json` |
| 2 | Review-to-Issue governance trace | `review-to-issue-trace.result.json` |
| 3 | Model Coordination-to-Issue trace | `model-coordination-to-issue-trace.result.json` |
| 4A | Transmittals exact-version snapshot | `transmittals-exact-version-snapshot.result.json` |
| 4A | RFI first-slice read verification | `rfis-first-slice-read-verification.result.json` |
| 4A | Submittals first-slice read verification | `submittals-first-slice-read-verification.result.json` |

The current **Phase 3 evidence ceiling is `shared_model_context_proven`**: a
coordination issue and a coordination snapshot were proven to refer to the same
models at the same coordinated versions. Clash-level reads remain unimplemented, so
a **direct clash-to-issue link and geometric resolution remain unproven**.

### Phase 4A — three governed capabilities

Construction information exchange spans **Forma Data Management** and **Forma
Build** ([ADR-0004](docs/decisions/0004-adopt-transmittals-as-first-phase-4a-read-slice.md)).
Three capabilities are governed, implemented in the **APS/Forma MCP**, and
live-verified against controlled synthetic fixtures in the **approved training
project**:

| Capability | API family and contract version | First slice | Live-verified |
|---|---|---|---|
| Transmittals | Autodesk Forma Transmittals API `v1` (GA) | 5 read-only operations | 2026-07-27 |
| RFIs | Autodesk Forma Build RFI API `v3` (GA) | 3 read-only operations | 2026-07-28 |
| Submittals | Autodesk Forma Build Submittals API `v2` (GA) | 3 read-only operations | 2026-07-29 |

All three record `mcp_implementation_status: confirmed` and `data_readiness: ready`
in [`config/workflows/end-to-end-reference.yaml`](config/workflows/end-to-end-reference.yaml),
and Gates 5, 6 and 8 are closed for each first read-only slice.

**Every slice is read-only.** No Phase 4A write capability is implemented,
supported or authorised. Each `confirmed` / `ready` value is scoped to the approved
training project and to that capability's own first slice — **not** to the
Harrismith example project, which is not asserted to hold any of these fixtures,
and not to any other project.

**No fourth Autodesk Forma capability is in the V1 roadmap.** Sheets and Meetings
are not adopted, and Assets remains a governed **planned** capability in the
`asset_handover` stage.

### V1 freeze baseline

Common-schema consolidation, Revit MCP alignment and cross-repository acceptance
are complete. The **V1 freeze is complete**: the accepted component
revisions are declared in
[`config/v1-baseline.yaml`](config/v1-baseline.yaml), and
[`scripts/acceptance.py`](scripts/acceptance.py) validates the architecture
against those exact revisions rather than against whatever the components publish
next. Acceptance is **offline** — no Autodesk call, no running Revit, no MCP
server — and its contract is recorded in
[COMPONENT_BOUNDARIES.md](docs/architecture/COMPONENT_BOUNDARIES.md) §12.

The final reference revision is identified by the annotated **`v1.0.0`** tag,
which targets `ffa6d460d30ab267ccb31947d1081a9088a2f97c`.

The Phase 4 evidence schema
([`schemas/phase-4-result.schema.json`](schemas/phase-4-result.schema.json)) and
the per-capability public-evidence governance are **in place**. Sanitisation is
governed by [SANITISATION_CONVENTION.md](docs/guides/SANITISATION_CONVENTION.md)
with a profile per capability:
[ADR-0005](docs/decisions/0005-approve-transmittals-sanitisation-profile.md) as
extended by
[ADR-0006](docs/decisions/0006-approve-cross-surface-transmittals-evidence-semantics.md)
(Transmittals),
[ADR-0010](docs/decisions/0010-approve-rfi-public-evidence-sanitisation-profile.md)
(RFIs) and
[ADR-0013](docs/decisions/0013-approve-submittals-public-evidence-sanitisation-profile.md)
(Submittals).

See the
[PRD](docs/prd/PRD_AUTODESK_BIM_WORKFLOW_REFERENCE_IMPLEMENTATION.md) for the
roadmap and the Phase 4A entry gate, and
[PHASE_4_CAPABILITY_GAP.md](docs/architecture/PHASE_4_CAPABILITY_GAP.md) for the
capability research.
