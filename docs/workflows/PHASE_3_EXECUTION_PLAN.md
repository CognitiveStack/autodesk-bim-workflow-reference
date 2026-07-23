# Phase 3 Execution Plan — Model Coordination-to-Issue Trace (Operator Runbook)

**Status:** Phase 3A planning (no live run performed; Phase 3 is not executable
yet).
**Slice:** "Model Coordination-to-Issue Trace" (narrowed Option A).
**Posture:** strictly **read-only**.

This is the technical operator runbook. For the learner narrative see
[03_MODEL_COORDINATION_TO_ISSUE_TRACE.md](03_MODEL_COORDINATION_TO_ISSUE_TRACE.md);
for the two blockers see
[PHASE_3_CAPABILITY_GAP.md](../architecture/PHASE_3_CAPABILITY_GAP.md). Capability
status is governed by
[COMPONENT_BOUNDARIES.md](../architecture/COMPONENT_BOUNDARIES.md).

## 1. Phase structure

- **Phase 3A — planning and schema (this change set).** Capability gap, learner
  trace, runbook, and `schemas/phase-3-result.schema.json`. **No live run.**
- **Phase 3B — close or verify gaps.** In `CognitiveStack/autodesk-aps-forma-mcp`:
  implement/verify read-only Model Coordination reads (model-set membership,
  coordinated versions, and — where the public API supports it — clash reads);
  and resolve the **data-readiness gap** by ensuring the training project has a
  usable coordination model set. Update the reference inventory only after those
  component changes are independently committed and verified.
- **Phase 3C — authenticated read-only trace.** Perform Section 4 once the gates
  in Section 3 pass.
- **Phase 3D — sanitised evidence artifact.** Structure, sanitise, and validate a
  public result under `examples/harrismith-fire-station/expected-results/`.

Phase 3C cannot begin until Phase 3B closes both blockers.

## 2. Read-only safeguards

- Invoke only confirmed read tools plus (in 3C) newly confirmed read-only Model
  Coordination tools.
- **Never** invoke writes. Explicitly excluded: model upload, publishing,
  coordination-space creation, model-set creation, clash execution/triggering,
  clash-group creation, clash-status change, issue creation/update/assignment,
  status changes, comments, attachments, approving/closing, arbitrary HTTP.
- The unrelated guarded `create_forma_proposal` is **not** part of Phase 3.

## 3. Execution gates (all must pass before Phase 3C)

1. **A usable coordination model set exists** in the training project
   (`list_model_sets` returns at least one set).
2. **Participating models can be enumerated** for that set (membership read
   available and returns models).
3. **Their coordinated versions can be identified** (version read available).
4. **The intended coordination issue can be safely selected** (a single
   unambiguous candidate, or an operator-confirmed selection).

If any gate fails, **do not run Phase 3C**. Any produced result must be
`status: partial` (or no artifact) with `outcome: coordination_evidence_incomplete`
and the relevant warning (for example `NO_COORDINATION_MODEL_SETS`,
`MODEL_SET_MEMBERSHIP_UNAVAILABLE`).

## 4. Logical tool order, gates, and handling (Phase 3C — provisional)

Tool signatures must be taken from the **live tool definitions at execution time**;
Model Coordination membership/version/clash tools are **not yet implemented** and
their names/parameters are placeholders pending Phase 3B verification. No endpoint
paths are asserted here.

### Stage A — Coordination context (APS/Forma MCP)

| # | Step | Confirmed today? | Gate / handling |
|---|---|---|---|
| A1 | `list_autodesk_hubs` → `list_projects` | ✅ | locate project |
| A2 | `list_model_sets` | ✅ | if 0 sets → `coordination_evidence_incomplete`, warning `NO_COORDINATION_MODEL_SETS`, **stop** |
| A3 | enumerate participating models (membership read) | ❌ Phase 3B | if unavailable → `coordination_evidence_incomplete`, warning `MODEL_SET_MEMBERSHIP_UNAVAILABLE` |
| A4 | identify coordinated versions | ❌ Phase 3B | record `version_alias` per model |

### Stage B — Coordination issue (APS/Forma MCP, confirmed reads)

| # | Step | Confirmed today? | Gate / handling |
|---|---|---|---|
| B1 | `list_issues` (coordination) | ✅ | if none → `issue_observation.available=false`, warning `ISSUE_NOT_FOUND` |
| B2 | `get_issue_details` | ✅ | type, status, assignee, references |
| B3 | `list_issue_types` | ✅ | resolve type alias |

### Stage C — Shared-model-context comparison (this repository)

Compare the issue's referenced models/versions against the coordination set's
participating models/versions. A positive, supported match is a **shared model
context** link (`proven:true`), not a direct clash-to-issue relationship.

### Stage D — Clash and resolution (deferred)

Clash identity, clash-to-issue linkage, and geometric-resolution verification are
**out of the first slice** and remain deferred until clash reads exist. Record
`clash_observation.capability_status = "unavailable"` and
`resolution_observation.resolution_verified = false` accordingly.

## 5. Outcome vocabulary (see the schema for full descriptions)

- `shared_model_context_proven` — issue and coordination refer to the same
  models/versions (medium proof; no clash entity).
- `clash_issue_link_proven` — an explicit clash-to-issue relationship is proven
  (deferred).
- `clash_resolution_claimed_not_verified` — status says resolved but geometric
  resolution not verified (deferred).
- `clash_resolution_verified` — a later coordinated version shows the clash gone
  (deferred).
- `clash_relationship_not_proven` — no clash-to-issue relationship provable.
- `coordination_evidence_incomplete` — a required coordination observation is
  missing (the current ceiling).

## 6. Execution status

- `complete` — **only** for the narrowed Option A shared multidisciplinary model
  context: coordination observation available, model set available, **at least two
  participating discipline models with identifiable coordinated versions** (each
  with `model_alias`, a non-null `discipline`, and a non-null `version_alias`),
  issue observation available, **and** an explicit supported model-context
  relationship (a link with `proven:true`). An issue existing alone, or a single
  participating model, is never sufficient. Enforced by the schema
  `complete`-guard, with the runtime distinctness checks in Section 7.
- `partial` — a required coordination observation is missing (current expected
  state); pair with `coordination_evidence_incomplete`.
- `failed` — coordination and/or issue reads could not be performed at all.

Warnings must not substitute for required observations.

## 7. Governance checks (recorded in `governance_checks[]`)

Outcomes `pass|fail|unproven|not_applicable`, for example: model set available;
participating models enumerated; coordinated versions identified; issue belongs to
the project; issue type/status available; shared-model-context match; issue status
not inferred from any clash state; clash identity not claimed; resolution not
claimed from issue status alone; response/recheck evidence not traced.

### 7.1 Multidisciplinary distinctness (runtime requirement)

The schema `complete`-guard enforces **at least two** participating models, each
with `model_alias`, a non-null `discipline`, and a non-null `version_alias`.
However, **Draft-7 cannot express that the two model aliases or disciplines are
semantically distinct.** The runtime trace must therefore verify, and record as
governance checks, that a `complete` Option A result has:

- **at least two distinct model aliases** (e.g. `MODEL_1` and `MODEL_2`, not the
  same alias twice);
- **at least two relevant discipline contexts** (e.g. structural and mechanical);
- a **non-null coordinated version alias for each** participating model.

If any of these cannot be verified, the result must not be `complete`; use
`partial` with `coordination_evidence_incomplete`.

## 8. Evidence handling

- Raw output and the alias map live in `.local/phase-3/` (git-ignored).
- Only the sanitised result JSON is committed under
  `examples/harrismith-fire-station/expected-results/`, and only when
  `execution.status` is `complete` for the Option A scope.
- Aliases for the first slice: `PROJECT_1`, `MODEL_SET_1`, `MODEL_1`, `MODEL_2`,
  `VERSION_1`, `VERSION_2`, `ISSUE_1`, `ISSUE_TYPE_1`, `USER_1`. Clash-stage
  aliases (`CLASH_TEST_1`, `CLASH_1`, `CLASH_GROUP_1`, `ELEMENT_1`, `ELEMENT_2`)
  are reserved for later clash-capability phases. The sanitisation convention is
  **not** modified until Phase 3B confirms the actual Model Coordination
  identifiers and payload structures.
