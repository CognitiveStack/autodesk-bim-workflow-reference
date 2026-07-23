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

### Artifact

- `review-to-issue-trace.result.json` — present. A **complete**, read-only,
  sanitised Phase 2 evidence artifact from a live run on 2026-07-23 (Reviews and
  issue-relationship reads are implemented and live-verified; see the capability
  gap §8).

What the evidence establishes:

- The explicit issue-side document reference proved the **same document lineage**
  as the reviewed version (`ISSUE_1` → `DOCUMENT_1`, `match`, `proven`).
- **No exact document-version match** was established (lineage is a weaker proof
  than an exact version).
- **No direct Review-to-Issue relationship** is claimed; the proof is a shared
  document lineage only.
- The Relationships API lookup returned **no records** for the tested issue; that
  empty result **does not** prove the issue was unrelated in the project or
  Autodesk UI.
- The artifact was produced through an **operator-mediated** sanitised
  conversation handoff (the Filesystem connector was not used); no live Autodesk
  identifiers are stored here.

## Phase 3 — Model Coordination-to-Issue trace (foundation verified; evidence pending)

- **Workflow (learner):** [`docs/workflows/03_MODEL_COORDINATION_TO_ISSUE_TRACE.md`](../../../docs/workflows/03_MODEL_COORDINATION_TO_ISSUE_TRACE.md)
- **Runbook (operator):** [`docs/workflows/PHASE_3_EXECUTION_PLAN.md`](../../../docs/workflows/PHASE_3_EXECUTION_PLAN.md)
- **Capability gap:** [`docs/architecture/PHASE_3_CAPABILITY_GAP.md`](../../../docs/architecture/PHASE_3_CAPABILITY_GAP.md)
- **Schema:** [`schemas/phase-3-result.schema.json`](../../../schemas/phase-3-result.schema.json)
- **Sanitisation:** [`docs/guides/SANITISATION_CONVENTION.md`](../../../docs/guides/SANITISATION_CONVENTION.md)

Phase 3A planning and schema are **complete**. Phase 3B is **recorded**: the five
read-only Model Coordination model-set/version reads (`list_model_sets`,
`get_model_set`, `list_model_set_versions`, `get_latest_model_set_version`,
`get_model_set_version`) are implemented and **live-verified (2026-07-23)** in the
APS/Forma component, and the coordination **training dataset is ready** (a usable
model set with two processed discipline-context models). **No Phase 3 evidence
artifact exists yet**, and none is created by this change.

What remains before the live read-only trace (Phase 3C) can complete:

- a coordination **issue must be selected** through the Autodesk UI and read with
  the existing Issues tools, and a **supported model-context relationship** proven;
- **clash-level reads remain deferred** — the component still does not read clash
  results, identities, groups, status/history, a direct clash-to-issue
  relationship, or resolution verification.

The current honest **public artifact status** remains
**`coordination_evidence_incomplete`**. A Phase 3 evidence artifact
(`model-coordination-to-issue-trace.result.json`) will be added in a later,
separate commit once a selected issue and supported relationship are traced,
sanitised, and a `complete` Option A run exists.
