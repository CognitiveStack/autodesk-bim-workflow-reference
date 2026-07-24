# Phase 3 Capability Gap — Model Coordination-to-Issue Trace

**Status:** Phase 3 complete — Phase 3C read-only inspection established
`shared_model_context_proven` (§6) and the Phase 3D sanitised public artifact is
committed (§6.5); clash-level reads remain unimplemented and deferred.
**Date:** 2026-07-24 (component re-pinned to `75b36b2`, 2026-07-24)

This document records what the Model Coordination-to-Issue Trace needs, what the
current component provides, and the remaining gaps. The model-set and
participating-version foundation is **executable and live-verified**; the
coordination-data-readiness blocker is **closed**; the Phase 3C issue/relationship
trace has been executed and establishes a **shared model context** (§6); all
clash-level reads remain outstanding. It is consistent with
[COMPONENT_BOUNDARIES.md](COMPONENT_BOUNDARIES.md) (APS/Forma MCP re-verified
locally 2026-07-24 at `75b36b2`) and the terminology model in
[ADR-0003](../decisions/0003-autodesk-platform-product-and-api-terminology.md).

No capability is asserted to exist unless it appears as **confirmed** in
[COMPONENT_BOUNDARIES.md](COMPONENT_BOUNDARIES.md). No endpoint paths are invented,
and no public API availability is claimed without evidence.

## 1. Baselines

- **Reference repository:** `CognitiveStack/autodesk-bim-workflow-reference`,
  `main`.
- **APS/Forma MCP component:** `CognitiveStack/autodesk-aps-forma-mcp` at
  `75b36b2635de3a5707fd1ff3dbf5cd487e3f0e0a` — 30 tools (28 read-only Autodesk,
  1 guarded write, 1 local-only). Five read-only Model Coordination model-set reads
  (`list_model_sets`, `get_model_set`, `list_model_set_versions`,
  `get_latest_model_set_version`, `get_model_set_version`) are implemented and
  live-verified 2026-07-23, and confirmed still registered at `75b36b2`.
  **The capability classifications in this document are unchanged by the move from
  `0117022` to `75b36b2`**: that increment is reliability-only (bounded
  token-refresh locks, explicit HTTP timeouts, structured transport errors) and
  adds no tool, no Autodesk capability, and no public tool-contract change
  (see [COMPONENT_BOUNDARIES.md](COMPONENT_BOUNDARIES.md) §3.2). The Phase 3C
  evidence itself was captured at `0117022`.
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

Classifications are evidence-based from component source, established at `0117022`
and unchanged at the currently pinned `75b36b2`. The five
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
| 14 | issue-to-clash relationships | undocumented_or_uncertain (Relationships exposes generic issue-to-document entities only, not clash references; the shared-model-context match is a typed issue-field / viewer-state match, not a clash relationship) |
| 15 | issue placement / pushpin references | **confirmed_available** (a real coordination `get_issue_details` returned a typed placement-lineage reference and a viewer-state field; see §6) |
| 16 | issue assignment & status | **confirmed_available** (`get_issue_details`) |
| 17 | subsequent model versions | **confirmed_available** (`list_item_versions`, document-item scope) |
| 18 | evidence a clash disappeared / was resolved | **missing** |
| 19 | clash history across model-set versions | **missing** |
| 20 | Model Coordination ↔ Navisworks correlation | unavailable_through_current_public_api / undocumented_or_uncertain |

**Confirmed:** #3, #4, #5, #15, #16, #17. **Partial:** #13. **No authoritative
field:** #12. **Missing:** #6, #7, #8, #9, #10, #11, #18, #19. **Uncertain:** #1, #2,
#14, #20.

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

## 6. Present proof ceiling — `shared_model_context_proven`

The Phase 3C read-only inspection establishes **`shared_model_context_proven`** as
the strongest justified conclusion.

### 6.1 The proof

- `ISSUE_1` contains a **typed placement-lineage reference**;
- that lineage **exactly matches `MODEL_1`** participating in `MODEL_SET_VERSION_1`;
- **two viewer-state-derived version references** decoded locally from a viewer-state
  field already returned by a read-only tool **exactly match `VERSION_1` and
  `VERSION_2`**, the coordinated versions of the two documents participating in
  `MODEL_SET_VERSION_1`.

This proves that the issue and the coordination snapshot refer to the same models
and versions. It **does not** prove a Relationships API record, a typed
issue-to-model-set relationship, a typed issue-to-snapshot relationship, or
clash-to-issue provenance.

### 6.2 Evidence-ceiling boundary

- **Supported (established):** `shared_model_context_proven`.
- **Not supported (not established):** `clash_issue_link_proven`,
  `clash_resolution_claimed_not_verified`, `clash_resolution_verified`.

### 6.3 Contextual and negative observations

- The Forma **Clashes tab** visibly associates `ISSUE_1` with one clash — this is
  **contextual UI evidence only**; the API returned no clash identifier, clash-group
  identifier, clash-member collection, or clash-origin field.
- **Viewer-state element isolation is not clash membership.**
- `list_issue_relationships` returned **zero records**; an empty Relationships API
  result proves only that **no matching record was returned**, not that the issue is
  unrelated in the project or the Autodesk UI.
- **No discipline field was returned**, and none was inferred; a null discipline does
  not make the inspection partial.
- **No numeric document version was inferred from a URN.**
- `MODEL_SET_VERSION_1` is a **coordination snapshot version**, distinct from Data
  Management document-version numbering.

### 6.4 Tool limitation

**Historical observation, recorded during the Phase 3C inspection on 2026-07-24 at
component revision `0117022`. It is preserved unchanged as evidence and is not a
statement of current behaviour.**

- `get_latest_model_set_version` returned a **transport timeout**;
- `get_model_set` identified the tip, `list_model_set_versions` independently
  corroborated it as the highest successful version, and `get_model_set_version`
  successfully returned the selected snapshot and its two participating documents;
- the timeout is disclosed but does **not** invalidate the retrieved snapshot
  evidence.

**Subsequent hardening (note added 2026-07-24).** Component revision `75b36b2`
(*fix: bound token locks and APS transport timeouts*) subsequently bounded
token-refresh lock acquisition, set explicit HTTP connect/read/write/pool
timeouts, and made timeout and transport failures return structured, sanitised
errors rather than hanging. This is a **forward-looking baseline change only**: the
historical observation above stands as recorded, the committed Phase 3 artifact is
unchanged, and **no re-observation has been performed**. Whether
`get_latest_model_set_version` now succeeds against this project is **unverified**
and would require a new read-only run.

### 6.5 Schema and artifact status

The Phase 3 result schema was extended (backward-compatibly; `schema_version`
remains 1) to represent this result: an optional coordination snapshot identity
(`model_set_version_alias`, `model_set_version_is_tip`, `version_history_confirmed`),
optional per-participant lineage/version/tip presence booleans, a nullable
`discipline` that no longer forces a `partial` status, an optional `evidence_class`
on relationship links (`typed_issue_field`, `viewer_state_derived`,
`relationships_api`, `ui_context`), and an optional
`relationship_observation.viewer_state_version_match_count`.

The `shared_model_context_proven` guard structurally requires: a stable
**`model_set_alias`** and a coordination-snapshot **`model_set_version_alias`**
(neither a Data Management document-version number); **at least two** participating
model/version identities, each with a returned lineage reference
(`lineage_reference_present: true`) and an exact coordinated-version reference
(`coordinated_version_reference_present: true`); **one** proven `typed_issue_field`
placement-lineage match; and **at least two** exact viewer-state-derived
coordinated-version matches (`viewer_state_version_match_count ≥ 2`, plus a proven
`viewer_state_derived` link). Alias distinctness remains a runtime governance check;
`discipline` may remain null; viewer-state matching is not a typed relationship,
viewer-state element isolation is not clash membership, and no direct clash-to-issue
provenance is proved.

The sanitised public Phase 3 result artifact **is committed** (Phase 3D, complete):

```
examples/harrismith-fire-station/expected-results/model-coordination-to-issue-trace.result.json
```

It validates against `schemas/phase-3-result.schema.json` with
`execution.status: complete` and `outcome: shared_model_context_proven`. No issue
was created; issue creation remains a manual Autodesk-UI action unless a separate
write workflow is explicitly approved.

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
