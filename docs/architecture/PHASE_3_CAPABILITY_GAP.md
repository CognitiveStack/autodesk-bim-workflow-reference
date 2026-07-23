# Phase 3 Capability Gap — Model Coordination-to-Issue Trace

**Status:** Phase 3B recorded — model-set/version foundation implemented and
live-verified; issue/relationship and clash-level gaps remain.
**Date:** 2026-07-23

This document records what the Model Coordination-to-Issue Trace needs, what the
current component provides, and the remaining gaps. The model-set and
participating-version foundation is now **executable and live-verified**; the
coordination-data-readiness blocker is **closed**; the issue-selection and
relationship portion, and all clash-level reads, remain outstanding. It is
consistent with [COMPONENT_BOUNDARIES.md](COMPONENT_BOUNDARIES.md) (APS/Forma MCP
re-verified 2026-07-23 at `0117022`) and the terminology model in
[ADR-0003](../decisions/0003-autodesk-platform-product-and-api-terminology.md).

No capability is asserted to exist unless it appears as **confirmed** in
[COMPONENT_BOUNDARIES.md](COMPONENT_BOUNDARIES.md). No endpoint paths are invented,
and no public API availability is claimed without evidence.

## 1. Baselines

- **Reference repository:** `CognitiveStack/autodesk-bim-workflow-reference`,
  `main`.
- **APS/Forma MCP component:** `CognitiveStack/autodesk-aps-forma-mcp` at
  `0117022ca29fd78c3e9cb38ccde9e47c8ea89df9` — 30 tools (28 read-only Autodesk,
  1 guarded write, 1 local-only). Five read-only Model Coordination model-set reads
  (`list_model_sets`, `get_model_set`, `list_model_set_versions`,
  `get_latest_model_set_version`, `get_model_set_version`) are implemented and
  live-verified 2026-07-23.
- **Revit MCP component:** `ae01d29` (not used by Phase 3).

## 2. What Phase 3 needs

The conceptual chain: discipline model versions → coordination space / model set →
clash result → clash grouping / identity → related coordination issue →
responsible discipline / assignment → resolution evidence → later model version →
clash recheck / resolution status.

## 3. Existing useful reads (confirmed)

| Area | Tools | Phase-3 use |
|---|---|---|
| Project discovery | `list_autodesk_hubs`, `list_projects` | locate the project |
| Folder/item/version discovery | `list_top_folders`, `list_folder_contents`, `get_item_details`, `list_item_versions` | discover discipline model files and their versions |
| Derivative context | `get_derivative_manifest`, `list_model_views`, `get_model_properties` | per-model category/element context |
| Issues | `list_issues`, `get_issue_details`, `list_issue_types` | coordination issue, type, status, assignment |
| Issue Relationships | `list_issue_relationships` | issue ↔ document-entity references (document-level only) |
| Model Coordination | `list_model_sets`, `get_model_set`, `list_model_set_versions`, `get_latest_model_set_version`, `get_model_set_version` | discover model sets; read one set and its folder/content context; enumerate coordination snapshot versions; read the latest/specific snapshot with embedded participating document versions |

## 4. Model Coordination capability assessment (20 items)

Classifications are evidence-based from component source at `0117022`. The five
read-only model-set/version reads now exist and are live-verified (2026-07-23); **no
clash code of any kind exists in the component** — no clash-test, clash-result,
clash-group, clash-member, or clash-status functions, registered or unregistered:

| # | Capability | Classification |
|---|---|---|
| 1 | coordination spaces | undocumented_or_uncertain (the model-set `container` ≈ space; no explicit space read) |
| 2 | coordination folders | undocumented_or_uncertain |
| 3 | coordination model sets | **confirmed_available** (`list_model_sets`, `get_model_set`) |
| 4 | models participating in a model set | **confirmed_available** (embedded participating documents in `get_latest_model_set_version` / `get_model_set_version`) |
| 5 | exact model versions used for coordination | **confirmed_available** (`version_urn` per participating document in a snapshot; `lineage_urn` for stable lineage) |
| 6 | clash tests / automatic clash runs | **missing** |
| 7 | clash results | **missing** |
| 8 | clash identifiers | **missing** |
| 9 | clash groups | **missing** |
| 10 | clash status | **missing** |
| 11 | clash geometry / involved element references | **missing** |
| 12 | discipline / model ownership | **no_authoritative_field** (no discipline field in the five live-verified responses; a governed orchestration-level classification, never inferred from file/display names, folders or model titles) |
| 13 | coordination issues created from clashes | partially_available (coordination issues readable; clash origin/provenance not) |
| 14 | issue-to-clash relationships | undocumented_or_uncertain (Relationships exposes generic issue-to-document entities only, not clash references) |
| 15 | issue placement / pushpin references | undocumented_or_uncertain (needs a real coordination `get_issue_details`) |
| 16 | issue assignment & status | **confirmed_available** (`get_issue_details`) |
| 17 | subsequent model versions | **confirmed_available** (`list_item_versions`, document-item scope) |
| 18 | evidence a clash disappeared / was resolved | **missing** |
| 19 | clash history across model-set versions | **missing** |
| 20 | Model Coordination ↔ Navisworks correlation | unavailable_through_current_public_api / undocumented_or_uncertain |

**Confirmed:** #3, #4, #5, #16, #17. **Partial:** #13. **No authoritative field:**
#12. **Missing:** #6, #7, #8, #9, #10, #11, #18, #19. **Uncertain:** #1, #2, #14,
#15, #20.

### 4.1 Phase 3 capability matrix

**Now confirmed through the component (live-verified 2026-07-23):**

- model-set discovery;
- model-set detail (folder/content context);
- model-set version history;
- latest and specific coordination snapshot;
- participating documents within a snapshot;
- exact coordinated document-version references (`version_urn`);
- stable document-lineage references (`lineage_urn`);
- issue type/status/assignee through existing Issues reads;
- generic issue-to-document relationships through existing Relationships reads.

**Still missing or unresolved:**

- raw clash results;
- clash identifiers;
- clash groups;
- clash members / object references;
- clash status and review state;
- assigned / closed clash groups;
- direct clash-to-issue relationship;
- issue provenance proving creation from a clash;
- clash history across model-set versions;
- geometric resolution verification;
- Model Set Views reads;
- Model Properties API reads;
- authoritative discipline metadata.

Note: the component's `get_model_properties` is a **Model Derivative** property read
and is **not** a Model Properties API read; the Model Properties API remains
unimplemented.

## 5. Blocker status

### 5.1 Capability gap — narrowed
The model-set/version foundation is **closed**: model-set discovery and detail,
version history, latest/specific coordination snapshots, participating documents,
and exact coordinated-version and stable-lineage references are all implemented and
live-verified. What the component still **cannot** read: clash results; clash
identifiers or groups; clash status/review state; assigned/closed clash groups;
clash element/member references; a proven clash-to-issue relationship; issue
provenance from a clash; clash history across model-set versions; or
recoordination/geometric-resolution verification. Model Set Views, the Model
Properties API, and authoritative discipline metadata also remain unimplemented.

### 5.2 Data-readiness gap — closed
The earlier data-readiness blocker is **closed**. One isolated training coordination
space exists with automatic clash processing enabled; two discipline-context RVT
models were processed; both participating document versions are visible through the
version-level MCP responses; and automatic clash results are visible in the Autodesk
interface. (Only the version-level participating documents are read by the
component; the clash results themselves are not.)

Closing the data-readiness gap does not add clash reads: the remaining Phase 3
work is the issue/relationship portion (§6) plus the clash-level capability gap
(§5.1), which are independent of coordination data existing.

## 6. Present proof ceiling

The live capability foundation now exists, but the repository still has **no
committed Phase 3 evidence artifact**. Until a selected coordination issue and a
supported model-context relationship are traced, sanitised, and committed, the
current honest public ceiling remains **`coordination_evidence_incomplete`**. The
trace cannot yet claim `shared_model_context_proven`, `clash_issue_link_proven`,
`clash_resolution_claimed_not_verified`, or `clash_resolution_verified`.

The remaining Phase 3C gate is:

coordination snapshot → at least two participating document versions → selected
coordination issue → issue assignment/status → supported issue-to-model-context
relationship.

The full Phase 3 trace is **not** complete. Any issue selection or creation must
remain a manual Autodesk-UI action unless a separate write workflow is explicitly
approved.

## 7. Official Autodesk contract questions for Phase 3B to verify

No endpoint paths are asserted here; each must be verified against current
official Autodesk/APS documentation and a real response before implementation.

1. **Clash-result read availability** — does the public API expose clash tests,
   clash results, clash groups, and clash status as reads? (Product: Model
   Coordination on Autodesk Forma / Forma for Construction; `bim360/modelset`
   family.) Current code: only model-set listing.
2. **Model-set membership & coordinated versions** — **resolved (2026-07-23).**
   Participating documents and their exact coordinated versions are read via
   `get_latest_model_set_version` / `get_model_set_version`
   (`version_urn` per document, `lineage_urn` for lineage). No numeric document
   version is inferred from a URN, and `tip_version_urn` is never substituted for
   `version_urn`.
3. **Clash ↔ issue linkage** — does the Issues/Relationships surface model a clash
   or clash-group reference on a coordination issue? Current: `list_issue_relationships`
   exposes document entities only.
4. **Clash state across model-set versions** — does the API expose resolved / new /
   persisting clash state on recoordination? Current: none.
5. **Navisworks vs cloud coordination correlation** — whether identifiers or
   provenance can be correlated. Current: none.

## 8. Strict read-only boundary

Phase 3 excludes **all** writes: uploading models, publishing models, creating
coordination spaces, creating model sets, running or triggering clash processing,
creating clash groups, changing clash status, creating/updating/assigning issues,
comments, attachments, approving/closing, and arbitrary HTTP requests. The
component's unrelated guarded `create_forma_proposal` tool is **not** part of
Phase 3.
