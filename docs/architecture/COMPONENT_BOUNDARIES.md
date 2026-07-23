# Component Boundaries and Capability Ledger

**Status:** Confirmed component capability inventory
**Inventory verified:** 2026-07-23 (APS/Forma MCP re-verified at `a54acf8`); Revit
MCP unchanged (`ae01d29`, 2026-07-22)

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
| APS/Forma MCP | `CognitiveStack/autodesk-aps-forma-mcp` | `a54acf8` | 26 |
| Revit MCP | `CognitiveStack/revit-mcp-triviron` | `ae01d29` | 14 |

The APS/Forma MCP inventory is published at
`a54acf8e5c628dbf7f97bf901a78f3c31c4b0781` and reports **26 MCP tools total**:
24 read-only Autodesk tools, 1 guarded Autodesk write tool, and 1 local-only
preview tool. Component evidence: **196 automated tests passing at
`76f485306f09aedf990cf1ec22b6ec2cbf6b26c8`**, and offline doctor
**`TOOL_COUNT=26`, `RESULT=PASS`**.

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
- **partial** — the stage's sub-capabilities are split; some tools exist, others
  are planned.
- **planned** — no MCP tool yet; a later-phase capability.
- **experimental** — MCP tool exists but targets a Beta / `v1alpha` API.
- **data-readiness-blocked** — the tool works, but the Harrismith example lacks
  the data to exercise it.
- **mediated-by-revit-mcp** — reached through the Revit MCP / Revit API rather
  than APS.

In `config/workflows/end-to-end-reference.yaml` these concerns are expressed as
separate fields (`mcp_component`, `mcp_implementation_status`, `api_maturity`,
`data_readiness`) so MCP coverage, API maturity, and project-data readiness are
never conflated.

## 3. APS/Forma MCP — 26 tools (24 read · 1 guarded write · 1 local)

| Capability group | Tools | Class | Status |
|---|---|---|---|
| Data Management | `list_autodesk_hubs`, `list_projects`, `list_top_folders`, `list_folder_contents`, `get_item_details`, `list_item_versions` | read | confirmed |
| Model Derivative | `get_derivative_manifest`, `list_model_views`, `get_model_properties` | read | confirmed |
| Issues | `list_issues`, `get_issue_details`, `list_issue_types` | read | confirmed |
| Reviews | `list_review_workflows`, `list_reviews`, `get_review_details`, `get_review_workflow`, `list_review_file_versions`, `get_review_progress`, `get_file_version_approval_statuses` | read | confirmed · live-verified |
| Issue Relationships | `list_issue_relationships` | read | confirmed · live-verified |
| Model Coordination | `list_model_sets` | read | confirmed · data-readiness-blocked (§8) |
| Forma Site Design (Beta `v1alpha`) | `get_forma_project`, `list_forma_proposals`, `list_forma_proposal_elements` | read | experimental |
| Forma Site Design (Beta `v1alpha`) | `create_forma_proposal` | guarded write | experimental (sole write; requires explicit confirmation and an explicit source proposal; **not part of the Phase 2 read-only workflow**) |
| Local-only (no Autodesk call) | `prepare_native_floor_stack_preview` | local | confirmed |

Issues, Reviews, and Relationships reads are confirmed; RFI and Assets
capabilities remain planned (§6). Direct Review-to-Issue relationship support is
**not** established; the relationship read (`list_issue_relationships`) supports
**shared-document comparison** only.

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
| construction_information | RFI | planned |
| asset_handover | Assets | planned |

Reviews and issue-relationship reads for `reviews_and_issues` are now implemented
and live-verified (§3); they are no longer a gap. API-family names for RFI and
Assets are not asserted here until they are verified from an official Autodesk/APS
or component source.

## 7. Experimental boundary

The Forma Site Design tools target Beta (`v1alpha`) APIs and are isolated as
experimental. The project's only write tool, `create_forma_proposal`, sits inside
this Beta boundary and is guarded. Nothing on the stable read-only path depends on
Forma Site Design writes.

## 8. Data-readiness gap

`list_model_sets` is implemented and confirmed, but the Harrismith example
currently has no model sets, so the model-coordination stage is
**data-readiness-blocked** (`no_harrismith_model_sets`). This is a project-data
gap, not a missing-tool gap.

## 9. Responsibility matrix

| Concern | Revit MCP | APS/Forma MCP | This repository |
|---|---|---|---|
| Revit authoring / inspection | Owns | — | Documents, invokes, validates |
| Autodesk authentication (APS) | — | Owns | Never implements |
| Forma Data Management (CDE) | — | Owns | Documents, invokes, validates |
| Model Derivative / properties | — | Owns | Documents, invokes, validates |
| Issues, Reviews & Relationships (RFI/assets planned) | — | Owns | Documents, invokes, validates |
| Model Coordination (native engine) | — | Consumes / surfaces | Documents only |
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

- This ledger is pinned to the inspected commits (`a54acf8` APS/Forma, `ae01d29`
  Revit) and the verification date above. The APS/Forma inventory update is
  evidenced by 196 automated tests passing at `76f4853` and offline doctor
  `TOOL_COUNT=26`, `RESULT=PASS`.
- Re-run the read-only inventory and update the counts, commit hashes, and date
  before each phase, or whenever a component publishes a relevant change.
- Component tool surfaces evolve; expectations are captured here in documentation,
  not by submodule pins (see
  [REPOSITORY_STRATEGY.md](REPOSITORY_STRATEGY.md)).
