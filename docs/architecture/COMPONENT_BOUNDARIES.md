# Component Boundaries and Capability Ledger

**Status:** Confirmed component capability inventory
**Inventory verified:** 2026-07-23 (APS/Forma MCP re-verified at `0117022`); Revit
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
| APS/Forma MCP | `CognitiveStack/autodesk-aps-forma-mcp` | `0117022` | 30 |
| Revit MCP | `CognitiveStack/revit-mcp-triviron` | `ae01d29` | 14 |

The APS/Forma MCP inventory is published at
`0117022ca29fd78c3e9cb38ccde9e47c8ea89df9` and reports **30 MCP tools total**:
28 read-only Autodesk tools, 1 guarded Autodesk write tool, and 1 local-only
preview tool. Component evidence: the offline MCP doctor reports
**`TOOL_COUNT=30`, `RESULT=PASS`** at that revision. The five read-only Model
Coordination model-set reads were added by component commit
`c92ee079408500b74f7c2f7efd8b1ab0b8047fe3` (*feat: add read-only Model
Coordination model-set reads*), logging-privacy hardened by
`1634d8c5e65aff9af1fbb44270159772ebae20ce` (*fix: suppress identifier-bearing HTTP
client logs*), and recorded in the component inventory at `0117022` (*docs: update
inventory for Model Coordination reads*); they were live-verified on 2026-07-23.

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

## 3. APS/Forma MCP — 30 tools (28 read · 1 guarded write · 1 local)

| Capability group | Tools | Class | Status |
|---|---|---|---|
| Data Management | `list_autodesk_hubs`, `list_projects`, `list_top_folders`, `list_folder_contents`, `get_item_details`, `list_item_versions` | read | confirmed |
| Model Derivative | `get_derivative_manifest`, `list_model_views`, `get_model_properties` | read | confirmed |
| Issues | `list_issues`, `get_issue_details`, `list_issue_types` | read | confirmed |
| Reviews | `list_review_workflows`, `list_reviews`, `get_review_details`, `get_review_workflow`, `list_review_file_versions`, `get_review_progress`, `get_file_version_approval_statuses` | read | confirmed · live-verified |
| Issue Relationships | `list_issue_relationships` | read | confirmed · live-verified |
| Model Coordination | `list_model_sets`, `get_model_set`, `list_model_set_versions`, `get_latest_model_set_version`, `get_model_set_version` | read | confirmed · live-verified 2026-07-23 (§3.1, §8) |
| Forma Site Design (Beta `v1alpha`) | `get_forma_project`, `list_forma_proposals`, `list_forma_proposal_elements` | read | experimental |
| Forma Site Design (Beta `v1alpha`) | `create_forma_proposal` | guarded write | experimental (sole write; requires explicit confirmation and an explicit source proposal; **not part of the Phase 2 read-only workflow**) |
| Local-only (no Autodesk call) | `prepare_native_floor_stack_preview` | local | confirmed |

Issues, Reviews, and Relationships reads are confirmed; RFI and Assets
capabilities remain planned (§6). Direct Review-to-Issue relationship support is
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

| Concern | Revit MCP | APS/Forma MCP | This repository |
|---|---|---|---|
| Revit authoring / inspection | Owns | — | Documents, invokes, validates |
| Autodesk authentication (APS) | — | Owns | Never implements |
| Forma Data Management (CDE) | — | Owns | Documents, invokes, validates |
| Model Derivative / properties | — | Owns | Documents, invokes, validates |
| Issues, Reviews & Relationships (RFI/assets planned) | — | Owns | Documents, invokes, validates |
| Model Coordination model-set/version reads | — | Owns | Documents, invokes, validates |
| Model Coordination clash engine (native) | — | Consumes / surfaces | Documents only |
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

- This ledger is pinned to the inspected commits (`0117022` APS/Forma, `ae01d29`
  Revit) and the verification date above. The APS/Forma inventory update to 30
  tools is evidenced by the offline doctor `TOOL_COUNT=30`, `RESULT=PASS`, and the
  five Model Coordination model-set reads were live-verified on 2026-07-23.
- Re-run the read-only inventory and update the counts, commit hashes, and date
  before each phase, or whenever a component publishes a relevant change.
- Component tool surfaces evolve; expectations are captured here in documentation,
  not by submodule pins (see
  [REPOSITORY_STRATEGY.md](REPOSITORY_STRATEGY.md)).
