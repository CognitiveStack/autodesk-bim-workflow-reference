# Phase 2 Execution Plan — Review-to-Issue Governance Trace (Operator Runbook)

**Status:** Phase 2A planning (no live run performed)
**Slice:** "Review-to-Issue Governance Trace."
**Posture:** strictly **read-only**.

This is the technical operator runbook. For the learner-facing narrative, see
[02_REVIEW_TO_ISSUE_TRACE.md](02_REVIEW_TO_ISSUE_TRACE.md). Capability status is
governed by [PHASE_2_CAPABILITY_GAP.md](../architecture/PHASE_2_CAPABILITY_GAP.md)
and the confirmed inventory in
[COMPONENT_BOUNDARIES.md](../architecture/COMPONENT_BOUNDARIES.md).

## 1. Phase structure

- **Phase 2A — Planning and capability gap (this change set):** documents the
  workflow, capability gap, schema, sanitisation, and warnings. **No live run.**
- **Phase 2B — Reviews read capability:** implement and test read-only Reviews
  tools in `CognitiveStack/autodesk-aps-forma-mcp`; separately assess whether a
  Relationships API read tool is required; update the reference inventory only
  after those component changes are independently committed and verified.
- **Phase 2C — Live read-only trace:** perform the sequence in Section 4 and
  produce a sanitised public result.

Phase 2C cannot begin until Phase 2B lands the Reviews reads. Until then a Phase 2
run is at best `partial`.

## 2. Read-only safeguards

- Invoke only confirmed read tools plus (in 2C) the newly confirmed read-only
  Reviews tools.
- **Never** invoke write/mutation tools. Explicitly deferred: creating approval
  workflows, initiating reviews, creating or updating issues, submitting review
  steps, approving/rejecting reviews, adding comments, references, attachments, or
  markups.
- No writes to Autodesk data; no edits to either component repository.

## 3. Tool signatures

Use the **exact MCP schemas exposed by the connected servers at execution time**.
The Reviews tool names below are *logical placeholders* from
[PHASE_2_CAPABILITY_GAP.md](../architecture/PHASE_2_CAPABILITY_GAP.md); do not
invent parameters or assume REST signatures — inspect the live tool definition
first.

## 4. Logical tool order, gates, and handling (Phase 2C)

### Stage A — Reviewed document version (APS/Forma MCP, confirmed reads)

| # | Tool (logical) | Input | Output used | Gate / handling |
|---|---|---|---|---|
| A1 | `list_folder_contents` | project, folder | reviewed document item | large folders not paginated → note limitation |
| A2 | `get_item_details` | project, item | document display name, tip version | if not found: `document_observation.available=false`, warning `REVIEW_VERSION_MISMATCH` may apply later |
| A3 | `list_item_versions` | project, item | the specific reviewed version | record `version_alias`, `version_number` |

### Stage B — Workflow and review (Reviews reads — **Phase 2B dependency**)

| # | Tool (logical) | Input | Output used | Gate / handling |
|---|---|---|---|---|
| B1 | `list_review_workflows` | project | candidate workflow | if Reviews tools absent: `review_observation.available=false`, warning `REVIEWS_MCP_CAPABILITY_UNAVAILABLE`, status `partial` |
| B2 | `list_reviews` | project (+ workflow) | candidate review | multiple candidates → warning `OPERATOR_SELECTION_REQUIRED`; if none → `REVIEW_NOT_FOUND` |
| B3 | `get_review_details` / `get_review_workflow` | review / workflow | status, steps, service generation | determine `service_generation` (current/legacy) — see Section 6 |
| B4 | `list_review_file_versions` | review | reviewed file-version count | cross-check against Stage A version |
| B5 | `get_file_version_approval_statuses` | review / version | approval outcome | — |
| B6 | `get_review_progress` | review | step count, current step, progress | outcome/progress must be internally consistent |

### Stage C — Related issue (APS/Forma MCP, confirmed reads)

| # | Tool (logical) | Input | Output used | Gate / handling |
|---|---|---|---|---|
| C1 | `list_issues` | project | candidate issue | if none: `issue_observation.available=false`, warning `ISSUE_NOT_FOUND` |
| C2 | `get_issue_details` | project, issue | type, status, assignee, references | inspect whether references expose the reviewed file/version or review |
| C3 | `list_issue_types` | project | resolve type alias/name | — |

### Stage D — Relationship (requires verification)

- Determine relationship `method`: `issue_detail_reference` (if C2 exposes it),
  `relationships_api` (if a verified read tool exists), or `none`.
- Record each link `{source, target, relation_type, result, proven}`. If the
  review/document/issue link cannot be positively verified, record it as
  `no_equivalent` with `proven:false` and warning `RELATIONSHIP_NOT_PROVEN`.
- **Never assume** the relationship from co-existence in the same project.

### Stage E — Response evidence

- Trace the planned response artifact (e.g. a mezzanine clarification document)
  separately as its own document/version; do not infer it satisfies the issue
  without evidence.

### Stage F — Governance, sanitise, record (this repository)

Run the governance checks (Section 5), sanitise per the convention, write the
public result, and validate against the schema.

## 5. Governance checks

Recorded in `governance_checks[]` with outcome `pass|fail|unproven|not_applicable`:

1. Reviewed document version equals the expected CDE version.
2. Review belongs to the expected project.
3. Review uses the expected workflow.
4. Review progress and outcome are internally consistent.
5. Issue belongs to the same project.
6. Issue type and status are available.
7. A file/review/issue relationship is positively verified, or explicitly recorded
   as unproven.
8. The issue status is **not** assumed from the review outcome.
9. The review outcome is **not** assumed from the issue status.
10. Response evidence (e.g. `DOCUMENT_2.pdf`) is separately traceable.

## 6. Reviews service generation

Identify whether the candidate review belongs to the **current** Reviews workflow
service or the **legacy** pre-31-October-2025 service, and set
`review_observation.service_generation`. A legacy review is documented as
historical evidence with warning `LEGACY_REVIEW_SERVICE_RECORD` and must not
silently become the canonical current-workflow example.

## 7. Execution status

- `complete` — document version, review + workflow, review progress/outcome, and
  candidate issue all identified, and the review/document/issue relationship is
  positively verified or explicitly recorded as `no_equivalent`.
- `partial` — a required observation is missing; in particular, **missing Reviews
  MCP capability forces `partial`**.
- `failed` — the document and/or review and/or issue could not be captured at all.

Warnings must not be used as substitutes for required observations.

## 8. Structured warnings (schema-valid)

`REVIEWS_MCP_CAPABILITY_UNAVAILABLE`, `ISSUE_RELATIONSHIP_CAPABILITY_UNAVAILABLE`,
`LEGACY_REVIEW_SERVICE_RECORD`, `REVIEW_NOT_FOUND`, `ISSUE_NOT_FOUND`,
`RELATIONSHIP_NOT_PROVEN`, `REVIEW_VERSION_MISMATCH`, `OPERATOR_SELECTION_REQUIRED`.

## 9. Evidence handling

- Raw output and the alias map live in `.local/phase-2/` (git-ignored).
- Only the sanitised result JSON is committed under
  `examples/harrismith-fire-station/expected-results/`.
- The canonical artifact is committed separately from this plan, only when
  `execution.status` is `complete`.
