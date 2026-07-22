# Harrismith Fire Station — Expected Results

This directory holds **sanitised, public** evidence artifacts produced by running
the reference workflows against the synthetic Harrismith Fire Station example.

Nothing here may contain live Autodesk identifiers or private project information.

## Phase 1 — Revit-to-CDE trace

- **Workflow (learner):** [`docs/workflows/01_REVIT_TO_CDE_TRACE.md`](../../../docs/workflows/01_REVIT_TO_CDE_TRACE.md)
- **Runbook (operator):** [`docs/workflows/PHASE_1_EXECUTION_PLAN.md`](../../../docs/workflows/PHASE_1_EXECUTION_PLAN.md)
- **Schema:** [`schemas/phase-1-result.schema.json`](../../../schemas/phase-1-result.schema.json)
- **Sanitisation:** [`docs/guides/SANITISATION_CONVENTION.md`](../../../docs/guides/SANITISATION_CONVENTION.md)

### How an artifact is produced

1. **Execute (Claude Desktop, live, read-only).** Run the confirmed read tools in
   the order defined by the execution plan. Capture raw output privately into
   `.local/phase-1/raw-observations.json` (git-ignored).
2. **Sanitise (Claude Code).** Transform raw values into alias tokens per the
   sanitisation convention; keep the alias ↔ real mapping only in
   `.local/phase-1/sanitisation-map.json` (git-ignored).
3. **Validate.** Confirm the sanitised result validates against
   `schemas/phase-1-result.schema.json`.
4. **Commit.** Only the sanitised result JSON is committed here, and only when its
   `execution.status` is `complete` (meets the Phase 1 acceptance criteria). A
   `partial` or `failed` run may be kept for diagnostics but is not the canonical
   artifact.

### The public/private boundary

| Location | Contents | Committed? |
|---|---|---|
| `.local/phase-1/` | raw observations, alias ↔ real map | Never |
| this directory | sanitised result JSON only | Yes |

### Artifact

- `revit-to-cde-trace.result.json` — the sanitised Phase 1 evidence (present; a
  `complete`, read-only run, sanitised from a chat-mediated capture).

## Phase 2 — Review-to-Issue governance trace

- **Workflow (learner):** [`docs/workflows/02_REVIEW_TO_ISSUE_TRACE.md`](../../../docs/workflows/02_REVIEW_TO_ISSUE_TRACE.md)
- **Runbook (operator):** [`docs/workflows/PHASE_2_EXECUTION_PLAN.md`](../../../docs/workflows/PHASE_2_EXECUTION_PLAN.md)
- **Capability gap:** [`docs/architecture/PHASE_2_CAPABILITY_GAP.md`](../../../docs/architecture/PHASE_2_CAPABILITY_GAP.md)
- **Schema:** [`schemas/phase-2-result.schema.json`](../../../schemas/phase-2-result.schema.json)
- **Sanitisation:** [`docs/guides/SANITISATION_CONVENTION.md`](../../../docs/guides/SANITISATION_CONVENTION.md)

Phase 2 follows the same public/private boundary as Phase 1: raw observations and
alias maps live in `.local/phase-2/` (git-ignored); only the sanitised result JSON
is committed here.

### Expected artifact (not yet produced)

- `review-to-issue-trace.result.json` — added in a later, separate commit once a
  live read-only run exists. Because Reviews MCP tools are not yet implemented (see
  the capability gap), the first runs are expected to be `partial`, not `complete`;
  only a `complete` run becomes the canonical artifact.

This planning change set intentionally does **not** include a Phase 2 result
artifact.
