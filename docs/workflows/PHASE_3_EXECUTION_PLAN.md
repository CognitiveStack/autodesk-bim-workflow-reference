# Phase 3 Execution Plan — Model Coordination-to-Issue Trace (Operator Runbook)

**Status:** Phase 3C read-only inspection completed. The narrowed Option A
**`shared_model_context_proven`** evidence class has been established live (see §9),
and the Phase 3 result schema has been extended (backward-compatibly) to record it.
Clash-level reads remain deferred, and **no sanitised public Phase 3 result artifact
has been committed yet** — packaging is the later Phase 3D increment.
**Slice:** "Model Coordination-to-Issue Trace" (narrowed Option A).
**Posture:** strictly **read-only**.

This is the technical operator runbook. For the learner narrative see
[03_MODEL_COORDINATION_TO_ISSUE_TRACE.md](03_MODEL_COORDINATION_TO_ISSUE_TRACE.md);
for the two blockers see
[PHASE_3_CAPABILITY_GAP.md](../architecture/PHASE_3_CAPABILITY_GAP.md). Capability
status is governed by
[COMPONENT_BOUNDARIES.md](../architecture/COMPONENT_BOUNDARIES.md).

## 1. Phase structure

- **Phase 3A — planning and schema.** Capability gap, learner trace, runbook, and
  `schemas/phase-3-result.schema.json`. **Complete.**
- **Phase 3B — close or verify gaps. Recorded here (2026-07-23).** In
  `CognitiveStack/autodesk-aps-forma-mcp`, the five read-only Model Coordination
  model-set reads (`list_model_sets`, `get_model_set`, `list_model_set_versions`,
  `get_latest_model_set_version`, `get_model_set_version`) are implemented, tested,
  and live-verified, giving model-set membership and coordinated-version reads; the
  **data-readiness gap is closed** (a usable training coordination model set with
  two processed discipline-context models exists). Clash-level reads were **not**
  implemented and remain deferred. The reference inventory is updated to
  `0117022` / 30 tools accordingly.
- **Phase 3C — authenticated read-only trace. Completed.** All four Section 3 gates
  passed; the Section 4 stages were executed read-only. The result is the
  `shared_model_context_proven` evidence class recorded in §9. The schema amendment
  in this increment makes that result representable without overstatement.
- **Phase 3D — sanitised evidence artifact.** Structure, sanitise, and validate the
  public result under `examples/harrismith-fire-station/expected-results/`. **No
  such artifact has been committed yet**; it is a separate, later increment.

The coordination-context foundation and the issue/relationship trace are now
executed; the strongest justified conclusion is `shared_model_context_proven` (§9).

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
   (`list_model_sets` returns at least one set). ✅ **Satisfied (2026-07-23).**
2. **Participating models can be enumerated** for that set (membership read
   available and returns models). ✅ **Satisfied** — participating documents are
   embedded in `get_latest_model_set_version` / `get_model_set_version`; two were
   returned.
3. **Their coordinated versions can be identified** (version read available). ✅
   **Satisfied** — each participating document carries an exact `version_urn`.
4. **The intended coordination issue can be safely selected** (a single
   unambiguous candidate, or an operator-confirmed selection). ✅ **Satisfied** — an
   existing coordination issue (`ISSUE_1`) was selected and read through the Issues
   tools. No issue was created; issue creation remains a **manual Autodesk-UI
   action** unless a separate write workflow is explicitly approved.

With all four gates satisfied, the Section 4 stages were executed and a supported
model-context relationship was established (§9). Sanitising and committing the
public result is the separate Phase 3D increment.

If any gate fails, **do not run Phase 3C**. Any produced result must be
`status: partial` (or no artifact) with `outcome: coordination_evidence_incomplete`
and the relevant warning (for example `NO_COORDINATION_MODEL_SETS`, `ISSUE_NOT_FOUND`).

## 4. Logical tool order, gates, and handling (Phase 3C — provisional)

Tool signatures must be taken from the **live tool definitions at execution time**.
The Model Coordination model-set/version reads are now implemented and live-verified;
clash-level tools remain **not implemented** and their names/parameters stay
deferred pending a future phase. No endpoint paths are asserted here.

### Stage A — Coordination context (APS/Forma MCP)

| # | Step | Confirmed today? | Gate / handling |
|---|---|---|---|
| A1 | `list_autodesk_hubs` → `list_projects` | ✅ | locate project |
| A2 | `list_model_sets` → `get_model_set` | ✅ | if 0 sets → `coordination_evidence_incomplete`, warning `NO_COORDINATION_MODEL_SETS`, **stop**. `get_model_set` identified the tip snapshot → `coordination_observation.model_set_version_is_tip` |
| A2b | `list_model_set_versions` | ✅ | independently corroborates the tip as the highest successful version → `version_history_confirmed`. **Tool limitation:** `get_latest_model_set_version` returned a transport timeout; the snapshot was instead established by A2/A2b agreement plus the successful A3 read (warning `LATEST_SNAPSHOT_TOOL_TIMEOUT`). The timeout does **not** invalidate the retrieved snapshot |
| A3 | enumerate participating documents via `get_model_set_version` | ✅ live-verified | read the two embedded participating documents of `MODEL_SET_VERSION_1`; set `lineage_reference_present` / `coordinated_version_reference_present` / `is_tip_version` per participant |
| A4 | identify coordinated versions | ✅ live-verified | record `version_alias` per document from its exact `version_urn` (never `tip_version_urn`); `version_number` stays `null` — no numeric document version is inferred from a URN |

### Stage B — Coordination issue (APS/Forma MCP, confirmed reads)

| # | Step | Confirmed today? | Gate / handling |
|---|---|---|---|
| B1 | `list_issues` (coordination) | ✅ | if none → `issue_observation.available=false`, warning `ISSUE_NOT_FOUND` |
| B2 | `get_issue_details` | ✅ | type, status, assignee, references |
| B3 | `list_issue_types` | ✅ | resolve type alias |

### Stage C — Shared-model-context comparison (this repository)

Compare the issue's referenced models/versions against the coordination set's
participating models/versions. A positive, supported match is a **shared model
context** link (`proven:true`), not a direct clash-to-issue relationship. Each link
carries an `evidence_class` (§9.4). In the executed trace this produced:

- one **`typed_issue_field`** link — the issue's typed placement-lineage reference
  matched `MODEL_1`'s participating lineage in `MODEL_SET_VERSION_1`;
- two **`viewer_state_derived`** links — two version references decoded locally from
  a viewer-state field already returned by a read-only tool, each exactly matching a
  participant's coordinated version (`VERSION_1`, `VERSION_2`);
- `relationship_observation.viewer_state_version_match_count = 2`, recording the two
  exact viewer-state-derived coordinated-version matches.

A `viewer_state_derived` match is contextual model matching only: it is **not** a
typed relationship, **not** clash membership, and **not** clash provenance.

### Stage D — Clash and resolution (deferred)

Clash identity, clash-to-issue linkage, and geometric-resolution verification are
**out of the first slice** and remain deferred until clash reads exist. Record
`clash_observation.capability_status = "unavailable"` and
`resolution_observation.resolution_verified = false` accordingly.

## 5. Outcome vocabulary (see the schema for full descriptions)

- `shared_model_context_proven` — issue and coordination refer to the same
  models/versions (medium proof; no clash entity). **This is the established Phase 3C
  ceiling (§9).**
- `clash_issue_link_proven` — an explicit clash-to-issue relationship is proven
  (deferred; not established).
- `clash_resolution_claimed_not_verified` — status says resolved but geometric
  resolution not verified (deferred; not established).
- `clash_resolution_verified` — a later coordinated version shows the clash gone
  (deferred; not established).
- `clash_relationship_not_proven` — no clash-to-issue relationship provable.
- `coordination_evidence_incomplete` — a required coordination observation is
  missing (the fallback when a gate fails).

## 6. Execution status

- `complete` — the governed inspection was completed and its required evidence was
  recorded. For the narrowed Option A shared multi-model coordination context that
  means: coordination observation available, model set available, **at least two
  participating models with identifiable coordinated versions** (each with
  `model_alias` and a non-null `version_alias`), issue observation available, **and**
  an explicit supported model-context relationship (a link with `proven:true`). An
  issue existing alone, or a single participating model, is never sufficient.
  Enforced by the schema `complete`-guard, with the runtime distinctness checks in
  Section 7.
- **Discipline does not affect status.** A **null** `discipline` (no authoritative
  discipline field was returned, and none is inferred) does **not** make a result
  `partial`. `partial` means required execution or evidence retrieval remained
  incomplete — not that an optional metadata field such as `discipline` was
  unavailable.
- `partial` — required execution or evidence retrieval remained incomplete (for
  example no model set, or membership/version reads unavailable); pair with
  `coordination_evidence_incomplete`.
- `failed` — coordination and/or issue reads could not be performed at all.

Warnings must not substitute for required observations.

## 7. Governance checks (recorded in `governance_checks[]`)

Outcomes `pass|fail|unproven|not_applicable`, for example: model set available;
participating models enumerated; coordinated versions identified; issue belongs to
the project; issue type/status available; shared-model-context match; issue status
not inferred from any clash state; clash identity not claimed; resolution not
claimed from issue status alone; response/recheck evidence not traced.

### 7.1 Multi-model distinctness (runtime requirement)

The schema `complete`-guard enforces **at least two** participating models, each
with `model_alias` and a non-null `version_alias`. It does **not** require a
non-null `discipline`. Draft-7 also **cannot express that the two model aliases are
semantically distinct.** The runtime trace must therefore verify, and record as
governance checks, that a `complete` Option A result has:

- **at least two distinct model aliases** (e.g. `MODEL_1` and `MODEL_2`, not the
  same alias twice);
- a **non-null coordinated version alias for each** participating model, with the
  two version aliases distinct;
- a valid **snapshot identity** (`model_set_version_alias`, e.g.
  `MODEL_SET_VERSION_1`) for the `shared_model_context_proven` outcome.

`discipline` may be **null** and is never inferred from filenames, display names,
folders, model titles, or viewer context. Where two disciplines happen to be
distinguishable through governed, non-inferred means, they may be recorded, but
their absence does not weaken a `complete` result. If the distinctness or snapshot
requirements above cannot be verified, the result must not be `complete`; use
`partial` with `coordination_evidence_incomplete`.

## 8. Evidence handling

- Raw output and the alias map live in `.local/phase-3/` (git-ignored). Raw
  viewer-state data and the decoded encoded values are **private and never
  committed**; only the sanitised outcome (which participant version each decoded
  reference matched) may appear in the public result.
- Only the sanitised result JSON is committed under
  `examples/harrismith-fire-station/expected-results/`, and only when
  `execution.status` is `complete` for the Option A scope.
- Aliases for the first slice: `PROJECT_1`, `MODEL_SET_1`, **`MODEL_SET_VERSION_1`**
  (the coordination snapshot version — a Model Coordination snapshot, distinct from
  any Data Management document-version number), `MODEL_1`, `MODEL_2`, `VERSION_1`,
  `VERSION_2`, `ISSUE_1`, `ISSUE_TYPE_1`, `USER_1`. Clash-stage aliases
  (`CLASH_TEST_1`, `CLASH_1`, `CLASH_GROUP_1`, `ELEMENT_1`, `ELEMENT_2`) are reserved
  for later clash-capability phases and remain **unused** because no clash-level API
  data was returned.
- Every **proven** relationship link records an `evidence_class` (§9.4). The
  sanitisation convention guide is not modified in this increment; adding
  `MODEL_SET_*` / `MODEL_SET_VERSION_*` tokens to that guide is a separate follow-up.

## 9. Phase 3C recorded evidence

### 9.1 The proof (`shared_model_context_proven`)

The strongest justified conclusion from the Phase 3C read-only inspection is
**`shared_model_context_proven`**, established as follows:

- `ISSUE_1` contains a **typed placement-lineage reference**;
- that lineage **exactly matches `MODEL_1`** participating in `MODEL_SET_VERSION_1`;
- **two viewer-state-derived version references** decoded locally from a viewer-state
  field already returned by a read-only tool **exactly match `VERSION_1` and
  `VERSION_2`**, the coordinated versions of the two documents participating in
  `MODEL_SET_VERSION_1`.

Together these prove that the issue and the coordination snapshot refer to the same
models and versions — a **shared model context**. This proof does **not** establish:
a Relationships API record; a typed issue-to-model-set relationship; a typed
issue-to-snapshot relationship; or clash-to-issue provenance.

### 9.2 Evidence-ceiling boundary

**Supported (established):**

- `shared_model_context_proven`.

**Not supported (not established):**

- `clash_issue_link_proven`;
- `clash_resolution_claimed_not_verified`;
- `clash_resolution_verified`.

### 9.3 Contextual and negative observations

- The Forma **Clashes tab** visibly associates `ISSUE_1` with one clash. This is
  **contextual UI evidence only** (`evidence_class: ui_context`); the API returned no
  clash identifier, clash-group identifier, clash-member collection, or clash-origin
  field, so no machine-readable clash-to-issue provenance exists.
- **Viewer-state element isolation is not clash membership.**
- `list_issue_relationships` returned **zero records** in this observation. An empty
  Relationships API result proves only that **no matching record was returned** — not
  that the issue is unrelated in the project or the Autodesk UI.
- **No discipline field was returned**, and no discipline was inferred.
- **No numeric document version was inferred from a URN** (`version_number` stays
  `null`).
- `MODEL_SET_VERSION_1` is a **coordination snapshot version** and must remain
  distinct from Data Management document-version numbering.

### 9.4 Schema representation (amended, backward-compatible; `schema_version` 1)

All new fields are optional at the base level (backward-compatible):

- `coordination_observation` gains optional `model_set_version_alias`,
  `model_set_version_is_tip`, and `version_history_confirmed`.
- Each `participating_models` item gains optional `lineage_reference_present`,
  `coordinated_version_reference_present`, and `is_tip_version`. `discipline` remains
  nullable.
- Each `relationship_observation.links` item gains an optional `evidence_class` enum:
  `typed_issue_field`, `viewer_state_derived`, `relationships_api`, `ui_context`.
- `relationship_observation` gains an optional
  `viewer_state_version_match_count` (`["integer","null"]`, `minimum 0`): the count
  of distinct issue-side version references decoded from viewer state, each exactly
  matched to a participating coordinated version in the retrieved snapshot. It is
  contextual shared-model evidence only — **not** Relationships API records, clash
  members, clash provenance, or geometric intersections.

**Strengthened `shared_model_context_proven` guard.** For that outcome the schema
structurally requires:

- `coordination_observation.available` and `model_set_available` true;
- a non-null **`model_set_alias`** (stable model set) **and** a non-null
  **`model_set_version_alias`** (coordination snapshot) — neither a Data Management
  document-version number;
- **at least two** participating models, each with a non-null `model_alias`, a
  non-null coordinated `version_alias`, and `lineage_reference_present` **and**
  `coordinated_version_reference_present` both `true`;
- relationship links containing at least one proven `typed_issue_field`
  placement-lineage link **and** at least one proven `viewer_state_derived` link,
  with every **proven** link carrying an `evidence_class`;
- `relationship_observation.viewer_state_version_match_count` **≥ 2**.

The `complete`-guard does **not** require non-null `discipline`. Alias **distinctness**
(two distinct model aliases, two distinct version aliases) is **not** Draft-7-
enforceable and remains a runtime governance check (§7.1).

### 9.5 Tool limitation

- `get_latest_model_set_version` returned a **transport timeout**.
- `get_model_set` identified the model-set **tip**.
- `list_model_set_versions` **independently corroborated** it as the highest
  successful version.
- `get_model_set_version` **successfully returned** the selected snapshot and its two
  participating documents.
- The timeout is disclosed (warning `LATEST_SNAPSHOT_TOOL_TIMEOUT`) but does **not**
  invalidate the successfully retrieved snapshot evidence.
