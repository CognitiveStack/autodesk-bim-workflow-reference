# Phase 2 Capability Gap — Review-to-Issue Governance Trace

**Status:** Phase 2A planning
**Date:** 2026-07-22

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
| Reviews reads (workflows, reviews, progress, approvals) | Identify workflow/review, progress, outcome | **missing** (planned) | none yet |
| Issue → file/review reference retrieval | Prove the relationship | **requires verification** | unconfirmed |
| Relationships API read | Prove relationships if issue detail is insufficient | **requires verification** | unconfirmed |
| Any write (create/initiate/approve/comment/attach) | — | **explicitly deferred** | out of Phase 2 scope |

## 3. Missing: Reviews read capability

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
- **Missing Reviews MCP capability forces `partial`, never `complete`** (warning
  `REVIEWS_MCP_CAPABILITY_UNAVAILABLE`).
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
