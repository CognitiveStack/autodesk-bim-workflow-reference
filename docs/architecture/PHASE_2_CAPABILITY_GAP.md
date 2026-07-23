# Phase 2 Capability Gap — Review-to-Issue Governance Trace

**Status:** Phase 2A historical baseline; Phase 2B component-capability gap closed
2026-07-23; Phase 2C evidence capture pending.
**Date:** 2026-07-22 (Phase 2A) · updated 2026-07-23 (Phase 2B outcome, §8)

This document records what the Review-to-Issue Governance Trace needs, what the
committed component inventory already provides, and what must be built or verified
before a live Phase 2C run. It is consistent with
[COMPONENT_BOUNDARIES.md](COMPONENT_BOUNDARIES.md) (inventory verified 2026-07-22)
and the terminology model in
[ADR-0003](../decisions/0003-autodesk-platform-product-and-api-terminology.md).

No capability is asserted to exist unless it appears as **confirmed** in
[COMPONENT_BOUNDARIES.md](COMPONENT_BOUNDARIES.md).

## 1. What Phase 2 needs

The trace follows: CDE file version → approval workflow → review instance → review
progress/outcome → related issue → issue type/status/assignment → relationship back
to the reviewed file/version or review → resolution evidence.

## 2. Capability matrix

| Capability | Needed for | Status | Source of truth |
|---|---|---|---|
| Data Management reads (`list_folder_contents`, `get_item_details`, `list_item_versions`) | Identify the reviewed CDE document + version | **available now** (confirmed) | COMPONENT_BOUNDARIES.md |
| Issues reads (`list_issues`, `get_issue_details`, `list_issue_types`) | Identify candidate issue, type, status | **available now** (confirmed) | COMPONENT_BOUNDARIES.md |
| Reviews reads (workflows, reviews, progress, approvals) | Identify workflow/review, progress, outcome | **implemented · live-verified** (§8) | COMPONENT_BOUNDARIES.md |
| Issue → file/review reference retrieval | Prove the relationship | **implemented · live-verified** via `list_issue_relationships` (shared-document comparison only) (§8) | COMPONENT_BOUNDARIES.md |
| Relationships API read | Prove relationships if issue detail is insufficient | **implemented · live-verified** (narrow) (§8) | COMPONENT_BOUNDARIES.md |
| Any write (create/initiate/approve/comment/attach) | — | **explicitly deferred** | out of Phase 2 scope |

## 3. Missing: Reviews read capability

> **Resolved in Phase 2B (2026-07-23) — see §8.** The seven Reviews reads below
> are now implemented and live-verified. The historical design baseline is
> preserved unchanged beneath this notice.

No Reviews MCP tools exist in `CognitiveStack/autodesk-aps-forma-mcp` today. Phase
2B must implement and test **read-only** Reviews tools. Proposed *logical* MCP tool
names (not REST signatures, not assumed to exist):

- `list_review_workflows`
- `list_reviews`
- `get_review_details`
- `get_review_workflow`
- `list_review_file_versions`
- `get_file_version_approval_statuses`
- `get_review_progress`

The component implementation phase must inspect the **current official Autodesk API
reference and actual response schemas** before deciding endpoint paths, parameters,
or response models. Until then these names are placeholders.

## 4. Requires verification: issue → file/review relationship

> **Resolved in Phase 2B (2026-07-23) — see §8.** A narrow read-only
> `list_issue_relationships` tool is implemented and live-verified. It supports
> shared-document comparison; a **direct** Review-to-Issue relationship is not
> established by the platform. The historical design baseline is preserved
> unchanged beneath this notice.

It is currently unknown whether `get_issue_details` already returns sufficient
reference information (linked document version / review) to prove the
review/document/issue relationship, or whether a separate **read-only Relationships
API** capability is required.

Phase 2B must determine this by inspecting a real `get_issue_details` response
schema. Until proven, relationship retrieval is treated as **unconfirmed**, and any
unproven relationship is recorded as `no_equivalent` with warning
`RELATIONSHIP_NOT_PROVEN` — never assumed.

## 5. Reviews service generation

Autodesk introduced a new Reviews workflow service; reviews created before
**31 October 2025** may belong to a legacy service. Phase 2 must identify whether
the candidate Harrismith review belongs to:

- the **current** Reviews workflow service; or
- the **legacy** (pre-31-October-2025) service.

A legacy review may be documented as historical evidence (warning
`LEGACY_REVIEW_SERVICE_RECORD`) but must not silently become the canonical
current-workflow example. The result schema records this as
`review_observation.service_generation` (`current` | `legacy` | `unknown`).

## 6. Effect on execution status

- A run is **complete** only when the document version, review + workflow, review
  progress/outcome, and candidate issue are all identified, and the
  review/document/issue relationship is either positively verified or explicitly
  recorded as `no_equivalent`.
- Reviews reads now exist (§8), so a run reaching all stages may be `complete`. If
  the Reviews reads are unavailable **at runtime**, the run still falls back to
  `partial` (warning `REVIEWS_MCP_CAPABILITY_UNAVAILABLE`).
- An unproven relationship does not by itself block `complete` if it is correctly
  recorded as `no_equivalent`; an *assumed* relationship is never permitted.

## 7. Deferral and independence

- No write tools are in Phase 2 scope (creating workflows, initiating reviews,
  creating/updating issues, submitting steps, approving/rejecting, comments,
  references, attachments, markups are all deferred).
- Per [ADR-0002](../decisions/0002-multi-repo-no-submodules.md), Reviews tools are
  built in the component repository, not here. The reference inventory
  ([COMPONENT_BOUNDARIES.md](COMPONENT_BOUNDARIES.md)) is updated **only after** the
  component changes are independently committed and verified — the same discipline
  used for the Phase 1 inventory.

## 8. Phase 2B outcome — capability gap closed (2026-07-23)

The component-capability gap identified in Phase 2A is closed. This is a
component-capability closure only; **Phase 2 as a whole is not complete** — the
Phase 2C live governance trace and sanitised evidence are still pending.

### 8.1 What was implemented and live-verified

- **Reviews reads (7, read-only):** `list_review_workflows`, `list_reviews`,
  `get_review_details`, `get_review_workflow`, `list_review_file_versions`,
  `get_review_progress`, `get_file_version_approval_statuses` — implemented and
  live-verified.
- **Issue relationship lookup (1, read-only):** `list_issue_relationships` —
  implemented and live-verified.
- **Direct Review-to-Issue relationship support: not established.**
- **Shared-document comparison: supported.**
- Component: 26 MCP tools (24 read-only Autodesk, 1 guarded Autodesk write, 1
  local-only preview); 196 automated tests passing at
  `76f485306f09aedf990cf1ec22b6ec2cbf6b26c8`; offline doctor `TOOL_COUNT=26`,
  `RESULT=PASS`; inventory published at
  `a54acf8e5c628dbf7f97bf901a78f3c31c4b0781`. See
  [COMPONENT_BOUNDARIES.md](COMPONENT_BOUNDARIES.md).

### 8.2 Tested relationship outcome

No Relationships API records were returned for the tested `ISSUE_1`.

This verifies the lookup capability, but means the relationship was absent from,
or not represented in, the Relationships API for that test. It does not prove that
the issue was unrelated in the project or Autodesk UI.

### 8.3 Semantic facts to preserve

- Review workflow and progress **step ordinals are derived from response-array
  position**.
- Workflow and progress **top-level status fields may be null** (those endpoints
  do not provide authoritative overall status values).
- The authoritative **current review step** is established by correlating
  `get_review_details.current_step_id` with `get_review_progress.steps[].step_id`.
- `list_review_file_versions` returns `version_id` (from the version URN),
  `item_urn` (from the document-lineage URN); **`version_number` may be null** and
  **`approval_status` may be null**.
- `get_file_version_approval_statuses` returns **version-scoped** approval records
  with `review_id`, `review_status`, `approval_status_id`, `approval_label`,
  `approval_value`; it does **not** return a per-record version ID, workflow ID, or
  workflow step.
- `list_issue_relationships` distinguishes `document_version`, `document_lineage`,
  `document_other`, `non_document`, and `unknown`.
- **`document_version` and `document_lineage` are different proof levels**; a
  document **lineage is not proof of an exact document version**.
- A valid **empty** Relationships result is **not** proof that no relationship
  exists in the real workflow or Autodesk UI.
- A shared-document relationship is **not** a direct Review-to-Issue relationship.

### 8.4 Schema compatibility

The existing `schemas/phase-2-result.schema.json` already supports the confirmed
Phase 2 trace outcomes without change:

- `same_version_proven` → `relationship_observation.links[].result: "match"`,
  `proven: true`, `relation_type: "document_version"`;
- `same_lineage_proven` → `result: "match"`, `proven: true`,
  `relation_type: "document_lineage"`;
- `different_document_entities` → `result: "difference"`;
- `relationship_not_proven` → `result: "no_equivalent"`, `proven: false`.

`relationship_observation.method: "relationships_api"` covers
`list_issue_relationships`; entity types map to `relation_type` /
`issue_observation.reference_summary.entity_type`. The schema is **not** changed.

### 8.5 Read-only boundary

Phase 2 uses **no** review, issue, or relationship write operations. Explicitly
excluded: initiating reviews, submitting steps, claiming steps, approving or
rejecting, updating issues, creating or deleting relationships,
`relationships:intersect`, and arbitrary HTTP requests. The component's unrelated
guarded `create_forma_proposal` write tool is **not** part of the Phase 2
read-only workflow.

### 8.6 Phase 2C readiness

Phase 2C is **ready to run**. `relationship_not_proven` is a valid evidence
outcome. A `complete` run additionally requires the document version, review +
workflow, review progress/outcome, and candidate issue to be identified, with the
relationship positively verified or explicitly recorded as `no_equivalent`.
