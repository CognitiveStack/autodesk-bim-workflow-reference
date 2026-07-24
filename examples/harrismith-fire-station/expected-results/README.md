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

## Phase 3 — Model Coordination-to-Issue trace

- **Workflow (learner):** [`docs/workflows/03_MODEL_COORDINATION_TO_ISSUE_TRACE.md`](../../../docs/workflows/03_MODEL_COORDINATION_TO_ISSUE_TRACE.md)
- **Runbook (operator):** [`docs/workflows/PHASE_3_EXECUTION_PLAN.md`](../../../docs/workflows/PHASE_3_EXECUTION_PLAN.md)
- **Capability gap:** [`docs/architecture/PHASE_3_CAPABILITY_GAP.md`](../../../docs/architecture/PHASE_3_CAPABILITY_GAP.md)
- **Schema:** [`schemas/phase-3-result.schema.json`](../../../schemas/phase-3-result.schema.json)
- **Sanitisation:** [`docs/guides/SANITISATION_CONVENTION.md`](../../../docs/guides/SANITISATION_CONVENTION.md)

Phase 3 follows the same public/private boundary as Phases 1 and 2: raw
observations, the alias map, and raw/decoded viewer-state data live in
`.local/phase-3/` (git-ignored); only the sanitised result JSON is committed here.

### Artifact

- `model-coordination-to-issue-trace.result.json` — present. A **complete**,
  read-only, sanitised Phase 3C evidence artifact from a live run on 2026-07-24,
  with outcome **`shared_model_context_proven`**.

What the evidence establishes (the narrow proof):

- `ISSUE_1` carries a **typed placement-lineage reference** that exactly matched
  `MODEL_1`'s participating lineage in the coordination snapshot
  `MODEL_SET_VERSION_1` (`evidence_class: typed_issue_field`).
- **Two viewer-state-derived version references** (decoded locally from a
  viewer-state field already returned by a read-only tool) exactly matched
  `VERSION_1` and `VERSION_2`, the coordinated versions of the two participating
  documents in `MODEL_SET_VERSION_1` (`evidence_class: viewer_state_derived`;
  `viewer_state_version_match_count: 2`).
- Together these prove a **shared model context** — the issue and the coordination
  snapshot refer to the same models at the same coordinated versions.

Distinctions kept honest:

- **Typed placement evidence vs viewer-state contextual evidence.** The placement
  match is a typed issue-field match; the version matches are contextual,
  viewer-state-derived matches — **not** typed relationships.
- **Relationships API returned zero records** for `ISSUE_1`. That empty result
  proves only that no matching Relationships API record was returned; it does **not**
  prove the issue is unrelated in the project or the Autodesk UI.
- The Forma **Clashes tab** showed one clash under the issue, but that is
  **contextual UI evidence only** — no machine-readable clash identifier, group,
  member, or origin was returned, so there is **no direct clash-to-issue provenance**.
  Viewer-state element isolation is **not** clash membership.
- No discipline field was returned (discipline is `null`, never inferred); no numeric
  Data Management document version was inferred from a URN (`MODEL_SET_VERSION_1` is a
  coordination snapshot version, not a document-version number).

Tool limitation: `get_latest_model_set_version` returned a **transport timeout** and
produced no evidence. The tip snapshot was instead established because `get_model_set`
identified the tip, `list_model_set_versions` independently confirmed it as the
highest successful version, and `get_model_set_version` successfully retrieved that
exact snapshot and its two participants. The timeout is disclosed and does not
invalidate the retrieved evidence.

Unsupported ceilings (not established by this artifact):

- `clash_issue_link_proven`;
- `clash_resolution_claimed_not_verified`;
- `clash_resolution_verified`.

Clash-level reads remain deferred, and no clash-level aliases are used because no
clash-level API data was returned.
