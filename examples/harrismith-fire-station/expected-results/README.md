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

## Phase 4A — Transmittals exact-version snapshot

- **Capability gap:** [`docs/architecture/PHASE_4_CAPABILITY_GAP.md`](../../../docs/architecture/PHASE_4_CAPABILITY_GAP.md)
- **Schema:** [`schemas/phase-4-result.schema.json`](../../../schemas/phase-4-result.schema.json)
- **Sanitisation:** [`docs/guides/SANITISATION_CONVENTION.md`](../../../docs/guides/SANITISATION_CONVENTION.md) —
  Transmittals public-evidence profile **version 2**
- **Governance:** [`ADR-0005`](../../../docs/decisions/0005-approve-transmittals-sanitisation-profile.md)
  (profile baseline) as extended by
  [`ADR-0006`](../../../docs/decisions/0006-approve-cross-surface-transmittals-evidence-semantics.md)
  (cross-surface evidence semantics)

Phase 4A follows the same public/private boundary as Phases 1–3: raw observations
and the alias map live under the git-ignored private evidence area; only the
sanitised result JSON is committed here.

### Artifact

- `transmittals-exact-version-snapshot.result.json` — present. A **complete**,
  read-only, sanitised Phase 4A evidence artifact from a live run on 2026-07-27,
  with outcome **`exact_version_snapshot_proven`**.

### Scenario and capture provenance

This directory is the repository's Harrismith BIM teaching/reference **scenario
namespace**. It is not an assertion that every fixture originated in the Autodesk
project of that name. For this artifact:

1. the controlled fixture was **captured in the approved training project**;
2. the evidence **belongs to the Harrismith BIM learning/reference scenario**;
3. **no claim** is made that the Harrismith Autodesk project itself contains the
   Transmittals fixture;
4. **no Harrismith-project Transmittals readiness** is inferred from this artifact;
5. **no real Autodesk project title and no alias-to-real-project mapping** is
   published — that mapping stays outside Git.

The artifact records these as separate fields, so teaching-scenario placement and
capture provenance are never collapsed into one another.

### What the evidence establishes (the narrow proof)

- The completed transmittal **retained the immutable issued version** `VERSION_1`.
- The source Data Management item lineage `ITEM_1` was returned **directly** by a
  first-party Data Management read, and later carried **`VERSION_2` as its current
  tip** — so the issued version was no longer the source's current version.
- The **cross-surface relationship was established by byte-for-byte exact string
  comparison** during the controlled live run: the version issued by the
  transmittal and the corresponding Data Management version are the same exact
  version identity. **Neither raw operand is published** — the artifact records the
  comparison, its method, and its result.
- The returned version set is **complete** on `count` together with
  `has_more: false`; a count alone would not establish completeness.
- For this controlled fixture, the transmittal therefore behaved as an **issued
  version snapshot** rather than following the source document's current version.

Distinctions kept honest:

- **Lineage is recorded per surface.** Transmittals-surface stable lineage remains
  **`not_proven`** — that response alone does not provide a stable source-document
  lineage identity, and none was inferred from a version identifier by URN
  splitting, suffix removal, reconstruction, canonicalisation or pattern inference.
  The Data Management item lineage is separately **proven**, because it was
  returned directly as a field.
- **Historical attestation vs re-derivable proof.** Each proof records whether it
  can be independently re-checked. The version **inequality** is re-derivable from
  the frozen private evidence; the two **equality** results are historical
  attestations, because the freeze deliberately retains one canonical identity per
  version rather than duplicate operands from each surface. **No proof is
  re-derivable from this public artifact**, which is intentional and not an
  evidence defect.
- **Evidence provenance is disclosed, not smoothed.** Each retained alias carries a
  provenance class. Two establishing responses had aged out of the capture session,
  so `ITEM_1` is classified `EQUALITY_VERIFIED_LATER_RESULT` rather than upgraded
  for consistency. Provenance describes how evidence is trusted; it never describes
  Autodesk resource semantics, and no class permits reconstructing an identifier.
- **Read-only throughout.** Every operation was a documented `GET`; the fixture
  itself was authored in the Autodesk product interface, not through any API write.
- **No raw identifiers.** No project, transmittal, folder, item or version URN, no
  numeric Autodesk version property, no recipient identity, and no behavioural
  timestamp appears here.

### What the evidence does not establish

- **universal Transmittals behaviour**, or behaviour **across every tenant, region
  or configuration** — the verdict is scoped to the controlled fixture;
- **Gate 8 as a global verdict** — Gate 8 closed for the Transmittals first slice
  only, under the operative §14 criteria of the capability gap;
- **overall Phase 4A completion** — no other Phase 4A module is implemented;
- **that the Harrismith Autodesk project contains the fixture**;
- **Transmittals stable lineage from the Transmittals surface itself**.
