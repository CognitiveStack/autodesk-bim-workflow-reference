# Phase 3 Capability Gap — Model Coordination-to-Issue Trace

**Status:** Phase 3A — capability and data-readiness planning.
**Date:** 2026-07-23

This document records what the Model Coordination-to-Issue Trace needs, what the
current component provides, and the two independent blockers that make Phase 3
**not executable yet**. It is consistent with
[COMPONENT_BOUNDARIES.md](COMPONENT_BOUNDARIES.md) (APS/Forma MCP re-verified
2026-07-23 at `a54acf8`) and the terminology model in
[ADR-0003](../decisions/0003-autodesk-platform-product-and-api-terminology.md).

No capability is asserted to exist unless it appears as **confirmed** in
[COMPONENT_BOUNDARIES.md](COMPONENT_BOUNDARIES.md). No endpoint paths are invented,
and no public API availability is claimed without evidence.

## 1. Baselines

- **Reference repository:** `CognitiveStack/autodesk-bim-workflow-reference`,
  `main`.
- **APS/Forma MCP component:** `CognitiveStack/autodesk-aps-forma-mcp` at
  `a54acf8e5c628dbf7f97bf901a78f3c31c4b0781` — 26 tools (24 read-only Autodesk,
  1 guarded write, 1 local-only). `list_model_sets` is the only Model Coordination
  read.
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
| Model Coordination | `list_model_sets` | list coordination model sets (returns raw first-page JSON; 403/404-tolerant) |

## 4. Model Coordination capability assessment (20 items)

Classifications are evidence-based from component source at `a54acf8` (no clash
code of any kind exists in the component — no clash-test, clash-result,
clash-group, model-set-membership, or model-set-version functions, registered or
unregistered):

| # | Capability | Classification |
|---|---|---|
| 1 | coordination spaces | undocumented_or_uncertain (the model-set `container` ≈ space; no explicit space read) |
| 2 | coordination folders | undocumented_or_uncertain |
| 3 | coordination model sets | **confirmed_available** (`list_model_sets`) |
| 4 | models participating in a model set | **missing** |
| 5 | exact model versions used for coordination | **missing** |
| 6 | clash tests / automatic clash runs | **missing** |
| 7 | clash results | **missing** |
| 8 | clash identifiers | **missing** |
| 9 | clash groups | **missing** |
| 10 | clash status | **missing** |
| 11 | clash geometry / involved element references | **missing** |
| 12 | discipline / model ownership | partially_available (naming heuristic only; not authoritative) |
| 13 | coordination issues created from clashes | partially_available (coordination issues readable; clash origin not) |
| 14 | issue-to-clash relationships | undocumented_or_uncertain (Relationships exposes document entities only) |
| 15 | issue placement / pushpin references | undocumented_or_uncertain (needs a real coordination `get_issue_details`) |
| 16 | issue assignment & status | **confirmed_available** (`get_issue_details`) |
| 17 | subsequent model versions | **confirmed_available** (`list_item_versions`, document-item scope) |
| 18 | evidence a clash disappeared / was resolved | **missing** |
| 19 | clash history across model versions | **missing** |
| 20 | Model Coordination ↔ Navisworks correlation | unavailable_through_current_public_api / undocumented_or_uncertain |

**Confirmed:** #3, #16, #17. **Partial:** #12, #13. **Missing:** #4, #5, #6, #7,
#8, #9, #10, #11, #18, #19. **Uncertain:** #1, #2, #14, #15, #20.

## 5. Two independent blockers

### 5.1 Capability gap
The component cannot read: clash results; clash identifiers or groups; clash
status/history; clash element/member references; authoritative model-set
membership or coordinated-version reads; a proven clash-to-issue relationship; or
recoordination/resolution verification.

### 5.2 Data-readiness gap
The tested Harrismith project currently exposes **zero Model Coordination model
sets** (consistent with the Phase 1/2 inventory note that Harrismith has 0 model
sets). Even the model-set listing therefore yields no traversable data.

These are **independent**: closing the capability gap does not create coordination
data, and adding coordination data does not add clash reads.

## 6. Present proof ceiling

The current honest ceiling is **`coordination_evidence_incomplete`**. The trace
cannot currently claim `shared_model_context_proven`, `clash_issue_link_proven`,
`clash_resolution_claimed_not_verified`, or `clash_resolution_verified`.

## 7. Official Autodesk contract questions for Phase 3B to verify

No endpoint paths are asserted here; each must be verified against current
official Autodesk/APS documentation and a real response before implementation.

1. **Clash-result read availability** — does the public API expose clash tests,
   clash results, clash groups, and clash status as reads? (Product: Model
   Coordination on Autodesk Forma / Forma for Construction; `bim360/modelset`
   family.) Current code: only model-set listing.
2. **Model-set membership & coordinated versions** — endpoints for participating
   models and their exact coordinated versions. Current code: none.
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
