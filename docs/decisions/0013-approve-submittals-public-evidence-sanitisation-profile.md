# ADR-0013: Approve Submittals public-evidence sanitisation profile

## Status

Accepted

## Date

2026-07-29

## Context

> **Numbering note.** This is **reference-repo ADR-0013**. The APS/Forma MCP
> component repository maintains its own, independent ADR series.

**Submittals is not an adopted workflow capability.** Unlike RFIs and Transmittals,
it has **no capability record** in
[end-to-end-reference.yaml](../../config/workflows/end-to-end-reference.yaml) — it
appears there only as a prose exclusion. This ADR is therefore **pre-adoption
governance**: it closes a privacy gate for a capability that has not been adopted,
which is possible because gate state is not a capability field
([ADR-0008](0008-govern-implementation-state-per-capability.md),
[ADR-0009](0009-define-capability-record-cardinality-for-schema-v2.md)).

**Submittals Gate 5 (privacy and sanitisation planning) is the open question this
ADR answers.** The Phase 4A research ranked Submittals **third** on the
narrative-leakage ordering
([PHASE_4_CAPABILITY_GAP.md](../architecture/PHASE_4_CAPABILITY_GAP.md) §13.1):
item titles and descriptions, response text, ball-in-court users, manager
mappings, spec section titles, revision notes and attachment filenames.

Unlike [ADR-0010](0010-approve-rfi-public-evidence-sanitisation-profile.md), which
was designed from documentation, **this profile is designed against an observed
response shape**. Bounded read-only runtime verification against a controlled
training context established:

- **`GET /users/me`** returns `id` (string), `roles` (array of strings) and
  `permittedActions` (array of objects, each `id` / `fields` / `mandatoryFields` /
  `transitions`). The `transitions` members carry `actionId`, `stateFrom`,
  `stateTo`, `transitionFields` and `mandatoryFields`. **This is a write-capability
  and workflow-configuration descriptor, not a read-permission flag** — it
  describes which workflow transitions the caller may perform and what each
  requires, and it collectively encodes the project's submittal state machine.
- **`GET /items`** returns a `pagination` / `results` envelope, with `pagination`
  carrying `limit`, `offset` and `totalResults`. The observed no-parameter page
  size is 20; **the maximum page size remains unknown**.
- **The list row and the detail response are shape-identical** — the same 56 keys
  with the same types on both surfaces, with no key unique to either. Every
  state-dependent key is present on an item that has never been submitted, carried
  as `null`. The schema is therefore fixed and populated by state rather than
  assembled per state, so **one field-handling policy governs both surfaces** and
  can be written state-independently.
- **The item-level `permittedActions` array has the same member signature** as the
  caller-level array, narrowed to the actions available for that item.

A single **controlled synthetic Submittal fixture** exists in the training project,
created through the Autodesk product interface and never transitioned. It is
**diagnostic input for contract verification only**. Its existence and its
treatment under this profile are addressed under *Relationship to the controlled
synthetic fixture* below.

The existing [SANITISATION_CONVENTION.md](../guides/SANITISATION_CONVENTION.md),
the Transmittals profile
([ADR-0005](0005-approve-transmittals-sanitisation-profile.md),
[ADR-0006](0006-approve-cross-surface-transmittals-evidence-semantics.md)) and the
RFI profile ([ADR-0010](0010-approve-rfi-public-evidence-sanitisation-profile.md))
supply the governing model. They **do not transfer unchanged**: Transmittals'
dominant risk was behavioural read-receipt telemetry and RFI's was narrative
authored by identified people, whereas Submittals adds a third — **commercial
assignment**, the record of which contractor is responsible for which procurement
scope — and a fourth, **project workflow configuration** exposed through
`permittedActions`.

## Decision

Approve the **Submittals public-evidence profile, version 1**, recorded in
[SANITISATION_CONVENTION.md](../guides/SANITISATION_CONVENTION.md). It **extends**
the existing conventions and **redefines nothing**, and it changes neither the
Transmittals profile nor the RFI profile.

### Public-evidence boundary

**This ADR governs what may cross into public repository evidence** under
`examples/**/expected-results/`. Raw Submittals data may exist transiently during
authenticated processing, and inside the existing git-ignored `.local/`
raw-observation boundary under the rules already in force.

**Real Submittals narrative, identity, commercial assignment, timestamps and
workflow configuration must never appear in public repository evidence.** The
allowed standard representation is approved aliases, controlled structural
vocabulary, presence booleans and safe counts.

### First-slice scope

The profile governs the first read-only slice only:

- `GET /users/me`
- `GET /items`
- `GET /items/:itemId`

All three are **GET-only**, so no POST-as-read classification question arises under
[ADR-0007](0007-read-write-classification-by-state-semantics.md).

**Outside this profile:** packages · spec sections as independent operations ·
item types · responses · review steps · attachments · comments · revisions as
independent operations · templates · settings and mappings · custom identifier
operations · **all writes**.

### Alias policy

**Approved new alias:** `SUBMITTAL_n` — a **Submittals item** record. It is the
**only** Submittals-specific alias in version 1.

**Reused unchanged:** `PROJECT_n`.

**Deliberately not introduced,** each for a stated reason:

- **`ITEM_n` for a Submittals item** — see the normative rule below. This is a
  prohibition, not merely an omission.
- **`SUBMITTAL_PACKAGE_n`** (§13.2 proposal) — `packageId` is omitted from
  version-1 public evidence. Package identity proves none of the first-slice
  propositions, and the populated package shape has not been observed.
- **`SUBMITTAL_ITEM_TYPE_n`** (§13.2 proposal) — `typeId` is omitted. Type identity
  proves nothing the slice claims, following ADR-0010 declining `RFI_TYPE_n`.
- **`SUBMITTAL_RESPONSE_n`** (§13.2 proposal) — responses are outside the first
  slice and `responseId` is omitted.
- **`SUBMITTAL_STEP_n`** (§13.2 proposal) — review steps are not read by any
  first-slice endpoint.
- **`SPEC_SECTION_n`** (§13.2 proposal) — spec identity reduces to a presence
  boolean; aliasing would imply a published relationship the evidence does not
  need.
- **`USER_n` for this slice** — no person reference is required by any first-slice
  proof. See *Personal identity policy*.
- **`COMPANY_n` for this slice** — approved for Transmittals, deliberately not
  reused here. See *Company and commercial policy*.
- **Narrative aliases** (`TITLE_n`, `TEXT_n` and similar) — narrative is **content,
  not stable repository identity**. Aliasing it would imply an identity it does not
  have, and adds no proof a presence boolean does not already carry. Consistent
  with `MESSAGE_n` being unapproved for Transmittals and with ADR-0010.

Aliases are assigned deterministically **within one private capture** and carry no
meaning across captures.

### Normative rule — `ITEM_n` must never identify a Submittals item

`ITEM_n` belongs to the **Data Management item** identifier domain. `SUBMITTAL_n`
belongs to the **Submittals item** identifier domain. **These domains are not
interchangeable, even though Autodesk calls both resources "item" and the
Submittals collection endpoint returns them under an `items` key.**

Writing `ITEM_n` for a Submittals item would silently merge two identifier domains
while passing every other check in this convention — the precise failure the
*Identifier domains are not interchangeable* section exists to prevent. Because the
API field name invites the error, the prohibition is stated normatively rather than
left to inference.

### Identifier policy

**Raw identifier values are always removed from public evidence.** A raw identifier
value must never appear unmodified, hashed, truncated, partially masked, or
otherwise transformed in a way that preserves the operand.

**Where an identity, reference, or equality proof is genuinely required, the raw
value is replaced only with an approved domain-specific alias under this
convention.** Approved alias replacement is expressly permitted; it is the
mechanism by which equality is expressed without disclosure.

The raw values covered are: the project ID · the Submittals item `id` · `specId` ·
`typeId` · `packageId` · `responseId` · `folderUrn` · **the folder URNs nested
inside `revisionsFoldersUrns`** · any storage identifier · any other URN ·
identifier-bearing URLs.

`revisionsFoldersUrns` is called out explicitly because it is an **index-keyed map
whose values contain folder URNs**. A sanitiser inspecting only top-level scalars
would not reach them.

Equality is expressed through **deterministic capture-local alias equality** —
`SUBMITTAL_1` returned by the list read is the same `SUBMITTAL_1` fetched by the
detail read — while the raw operand is never published.

### Human-identifier policy

`identifier`, `customIdentifier`, `customIdentifierHumanReadable` and
`specIdentifier` are **caller-operational values, not public-evidence values**.
They are **omitted and not aliased**.

Public evidence may record only `identifier_present`,
`custom_identifier_present`, `custom_identifier_human_readable_present` and
`spec_identifier_present`, and only where load-bearing.

`identifier` is an **integer sequence number** and receives the treatment already
applied to the Transmittals `sequenceId` and the RFI `customIdentifier`: publishing
it discloses project scope and volume, and it is never a join key.

### Personal identity policy

**No `USER_n` is published for the Submittals first slice** — not for the
authenticated caller, not for the manager, not for the subcontractor, not for
ball-in-court, not for watchers. This is stricter than the RFI default posture,
which permits `USER_n` where genuinely required; for Submittals nothing in the
first-slice proof set requires a person reference, so the default becomes an
absolute for this profile. This tightens within the existing model and redefines
nothing.

**Never published in any form:** the caller `id` · `roles` values · `manager` ·
`subcontractor` · `createdBy` · `updatedBy` · `submittedBy` · `publishedBy` ·
`respondedBy` · `sentToReviewBy` · `ballInCourtUsers` values · `watchers` values ·
any email, personal name or contact value.

**Permitted substitutes:** `role_count` · `watcher_count` ·
`ball_in_court_user_count` · `manager_assigned` · `subcontractor_assigned` ·
`managerType` and `subcontractorType` as non-identifying categorical
discriminators.

### Company and commercial policy

**`COMPANY_n` is deliberately not reused for Submittals**, despite being approved
for Transmittals. The standard representation is **`company_data_published:
false`**.

Three reasons:

1. Submittals company data is **commercial assignment** — which contractor is
   responsible for which procurement scope — not a distribution list. It discloses
   supply-chain relationships, a category the Transmittals profile did not weigh.
2. Nothing in the first-slice proof set requires company identity.
3. **The company member shape has not been observed.** `ballInCourtCompanies` was
   empty in the verified context, so no company object has been seen on this
   surface. Approving an alias for an unobserved shape would be designing policy
   against a guess.

**Never published:** company names · company identifiers ·
`ballInCourtCompanies` values · `subcontractor` values · commercial assignment
relationships. Where structure must be proven, `ball_in_court_company_count` only.

### Narrative policy

- **Default: omit the content.** The standard public representation is **derived
  machine-safe properties** — for example `title_present: true`,
  `description_present: true`, `response_comment_present: false`,
  `spec_title_present: true`, `narrative_content_published: false`.
- **Never published as real content:** `title` · `description` · `responseComment`
  · `specTitle` · `subsection` · `packageTitle` · attachment and file names · any
  response narrative.
- **`specTitle` is classified as narrative, not as a safe label.** Spec section
  titles name building systems and procurement scope, and §13.1 already lists them
  among the Submittals sensitive fields.
- **No narrative aliases are created.**
- **Character counts are discouraged:** length is weakly identifying and proves
  nothing a presence boolean does not.

### `priority` — omitted

**`priority` is caller-operational and omitted from public evidence.** It is
**not** retained as a publishable controlled categorical value.

Its value set is **configured per project**, so publishing it converts project
configuration into public metadata. It is not load-bearing for Gate-5 policy or for
any first-slice evidence proposition, and public evidence does not need the actual
value. Where structural proof is ever genuinely required, `priority_present` is
preferred.

**This is a Submittals-specific determination and does not modify the RFI profile**,
which retains `priority` under its own approved terms.

### State, status and revision policy

`stateId`, `statusId` and `revision` **may be retained as controlled structural
workflow evidence.** They carry no identity, no narrative and no resource
identifier.

The following constraints are normative:

- These are **observed API workflow vocabulary values**, not free text and not
  identifiers.
- **Only observed values may be reported.** The single controlled observation is
  `stateId` = `"sbc-1"` and `statusId` = `"1"`, recorded while the product
  interface displayed **Required / Waiting for submission**.
- **No universal mapping is inferred.** That observation does not establish the
  meaning of `"sbc-1"` generally, does not establish any other state vocabulary,
  and does not establish that the two fields covary.
- **`statusId` is a string.** `"1"` **must not be represented as ordinal, sortable
  or ranked.** A single observation cannot distinguish a sequence from an arbitrary
  identifier that happens to be `"1"`.
- **Sanitisation must not strengthen the claim beyond the one observation**, under
  the existing evidence-wording rule that sanitising values must never upgrade the
  strength of a claim.

`revision` may be published as structural integer evidence. It is a per-item
counter and, unlike `identifier`, discloses no project volume.

### Ball-in-court policy

`ballInCourtType` **may be published** as a non-identifying categorical
discriminator, and **only** while it remains verified as such. It names a category
of responsible party, not a party.

**The four collections are never published in any form** — `ballInCourt` ·
`ballInCourtUsers` · `ballInCourtCompanies` · `ballInCourtRoles`. Not aliased, not
truncated, not partially masked.

Where structure must be proven: `ball_in_court_user_count`,
`ball_in_court_company_count` and `ball_in_court_role_count`, subject to the
existing aggregate rule. **Counts are omitted where they add no proof** — in a
small project, a type plus a count of one narrows the responsible party
considerably.

### Timestamp and chronology policy

**No actual date or timestamp value is published.** This covers `createdAt` ·
`updatedAt` · `dueDate` · `submitterDueDate` · `managerDueDate` ·
`sentToSubmitter` · `sentToReview` · `receivedFromSubmitter` ·
`receivedFromReview` · `respondedAt` · `publishedDate` · `requiredDate` ·
`requiredApprovalDate` · `requiredOnJobDate` · `leadTime` and every actor-paired
chronology field.

**No lateness calculation. No interval calculation. No chronological
reconstruction. No person-linked chronology or ordering.**

Submittals timestamps receive the stricter treatment the convention already applies
to Transmittals behavioural telemetry and RFI workflow timestamps, **not** the
ordinary date-only reduction. The reason is structural: **every Submittals workflow
timestamp is actor-paired** — `sentToReview` with `sentToReviewBy`, `respondedAt`
with `respondedBy`, and so on — so a published time is a published fact about an
identified person's conduct.

Presence booleans such as `has_due_date`, `has_submitter_due_date` and
`has_required_on_job_date` are permitted where load-bearing.

**Wording rule — `sentToSubmitter` does not mean the item was submitted.** The
controlled fixture proved this field can be populated while the item remains in
**Required / Waiting for submission**, with `submittedBy` still null: it records
routing to the submitter, not submission by the submitter. Evidence and notes must
not describe its presence as evidence of submission.

### `permittedActions` and roles policy

**`permittedActions` is never published** — at either the caller scope or the item
scope. This covers the objects themselves and every part of them: member `id`
values · `fields` contents · `mandatoryFields` contents · `transitions` ·
`actionId` · transition `name` · `stateFrom` · `stateTo` · `transitionFields`.

Two independent reasons: the array describes **write capability** that a read-only
slice never exercises, and the transition maps collectively **are the project's
workflow configuration**, which is process design rather than project data.

Permitted where genuinely needed: **`permitted_action_count`** only.

**`roles` values are never published.** `role_count` is acceptable structural
evidence.

The caller-context public structural evidence is therefore exactly:
**`submittals_available`**, **`permitted_action_count`**, **`role_count`**.

### Error policy

**The raw upstream Submittals error body is never published.**

Permitted public evidence: HTTP status code or class · a stable **local** error
category · a fixed sanitised **local** reason · safe booleans. Categories may
include `authentication_failed`, `permission_denied`, `not_found`, `rate_limited`,
`transport_error`, `timeout`.

**Never published:** raw upstream messages · identifiers · identifier-bearing URLs
· request headers · tokens · diagnostic payloads.

### Controlled synthetic fixture rule

**Readable narrative may be publicly published only when it originates from an
explicitly controlled synthetic fixture satisfying this profile.**

A deliberately controlled synthetic Submittal materially reduces disclosure risk
and is more mechanically auditable than post-hoc sanitisation of arbitrary real
content. **Synthetic status waives no requirement of this profile.** Synthetic
fixture content must still satisfy the identifier rules, the narrative rules, the
timestamp rules, the identity rules, the company rules, the error rules, and the
full sanitisation checklist. The label "synthetic" is not, by itself, proof of
safety.

Synthetic narrative is **optional** — omission is always acceptable and remains the
default.

### Relationship to the controlled synthetic fixture

A controlled synthetic Submittal fixture **exists** in the training project. It was
created through the Autodesk product interface, has never been submitted or
transitioned, and was used as **diagnostic input** for the runtime contract
verification summarised in the Context above.

**This ADR:**

- **does not establish Gate 8 readiness**;
- **does not classify the existing fixture as Gate-8 evidence**;
- **does not authorise publication of the fixture's content**;
- **does not close Gate 8**;
- **does not make the first slice adopted or implementation-ready**.

The fixture's existence is a **diagnostic fact**, not a readiness finding. Gate 8
separately verifies the instance — module activation, workflow configuration, roles
and permissions, fixture suitability, and data readiness — and none of that is
asserted here.

### Gate 5 versus Gate 6

**Gate 5 specifies the public-evidence contract. It does not prescribe the complete
caller-facing MCP interface.**

Gate 6 later decides actual tool boundaries, caller-facing fields, client and
helper design, and the enforcement mechanism. Gate 5 requires only that **any
future path producing public evidence must be capable of enforcing this
sanitisation profile**.

The two contracts will legitimately differ. A caller-facing DTO may reasonably
carry values this profile forbids in public evidence, because an authenticated
caller holding `data:read` already has role-scoped access to them. That divergence
is a difference of boundary, not a contradiction, and Gate 6 must state it
explicitly.

### Gate 5 versus Gate 8

Gate 5 closes the **policy** question. Gate 8 verifies the **instance**.

**Gate 5 closure does not imply that data readiness is established, that the
existing fixture is suitable Gate-8 evidence, or that live verification of a
first-slice implementation occurred.** Gate 8 remains unresolved.

## Consequences

- **Submittals Gate 5 is closed** — the §16 gate table records `passed` for the
  Submittals *Privacy and sanitisation planning* row, with a closure subsection at
  §16.9.
- **Submittals Gate 2 is codified separately** at §16.8 as an evidence-boundary
  subsection. Gate 2 is an evidence finding, not an architecture decision, and
  receives no ADR of its own — following the Transmittals §16.1 precedent.
- **Gate 6 and Gate 8 remain unresolved.**
- **Submittals remains unadopted.** No capability record is created, and no
  `mcp_implementation_status` or `data_readiness` field is introduced. The workflow
  contract is unchanged.
- **A useful first-slice evidence artifact is possible without any narrative,
  identity, company data, timestamp or workflow configuration** — aliases,
  controlled structural vocabulary, presence booleans and counts prove caller
  context, list retrieval, fixture discovery, detail retrieval, list/detail
  equality, DTO boundary enforcement and the absence of writes.
- **This ADR authorises no implementation, no Autodesk call, no fixture change, no
  evidence artifact, and no other gate closure.**

## Rejected alternatives

- **Publishing `identifier` as a harmless label.** It is the direct analogue of the
  Transmittals `sequenceId` and the RFI `customIdentifier`, both already
  always-removed, and it discloses project volume.
- **Reusing `ITEM_n` for a Submittals item.** The API returns them under an `items`
  key, which is exactly why the prohibition must be explicit. Reuse would silently
  merge the Data Management item domain with the Submittals item domain.
- **Minting the §13.2 proposed families** — `SUBMITTAL_PACKAGE_n`,
  `SUBMITTAL_ITEM_TYPE_n`, `SUBMITTAL_RESPONSE_n`, `SUBMITTAL_STEP_n`,
  `SPEC_SECTION_n`. Aliases are added only where the evidence model requires them;
  none of these proves a first-slice proposition.
- **Reusing `COMPANY_n` because it exists for Transmittals.** Commercial assignment
  is a different disclosure category, no proof requires it, and the member shape
  has never been observed.
- **Publishing a `USER_n` for the authenticated caller.** The proof does not need
  the identity, so omission is strictly safer.
- **Retaining `priority` as a controlled categorical value.** It is configured per
  project, so publishing it exports project configuration; it is not load-bearing.
  The RFI profile's own retention of `priority` is unaffected by this
  determination.
- **Treating `specTitle` as a safe categorical label.** Spec titles name building
  systems and procurement scope.
- **Publishing `permittedActions` as harmless permissions metadata.** It reads as
  permissions but is a write-capability descriptor carrying the project's workflow
  state machine.
- **Treating `statusId` as ordinal or sortable.** One observation cannot establish
  a sequence, and presenting it as rankable would strengthen the claim during
  sanitisation.
- **Applying the ordinary date-only timestamp reduction.** Every Submittals
  workflow timestamp is actor-paired, so it receives behavioural-telemetry
  treatment instead.
- **Treating the controlled synthetic fixture as inherently safe, or as Gate-8
  evidence.** Synthetic status reduces risk and improves auditability but waives no
  requirement; and a fixture's existence is diagnostic, not a readiness finding.
- **Creating a capability record to represent gate state.** Gate state is not a
  capability field; a record would constitute adoption.
- **Specifying the complete MCP caller-facing response here.** That is Gate 6's
  decision.

## Interaction with existing ADRs

- **[ADR-0005](0005-approve-transmittals-sanitisation-profile.md)** — the
  structural precedent for a per-module public-evidence profile closing Gate 5.
  **Not superseded, not amended.** The Transmittals profile is unchanged.
- **[ADR-0006](0006-approve-cross-surface-transmittals-evidence-semantics.md)** —
  unaffected. Its cross-surface equality rules are Transmittals / Data-Management
  specific and are not extended to Submittals.
- **[ADR-0007](0007-read-write-classification-by-state-semantics.md)** —
  unaffected. All three first-slice endpoints are GETs, so no POST-as-read
  classification question arises. This ADR neither widens nor narrows that
  approval.
- **[ADR-0008](0008-govern-implementation-state-per-capability.md)** and
  **[ADR-0009](0009-define-capability-record-cardinality-for-schema-v2.md)** —
  unaffected. No capability record or field cardinality changes; gate state is not
  a capability field. These ADRs are what make a pre-adoption gate closure
  coherent.
- **[ADR-0010](0010-approve-rfi-public-evidence-sanitisation-profile.md)** — the
  closest precedent, and the model for this ADR's structure. **Not superseded, not
  amended.** The RFI profile is unchanged, including its retention of `priority`.
- **[ADR-0011](0011-adopt-rfi-first-slice-mcp-contract-and-component-boundary.md)**
  and
  **[ADR-0012](0012-refine-rfi-search-contract-from-runtime-verification.md)** —
  RFI-specific and unaffected. ADR-0012's discipline — not converting unverified
  transport assumptions into contract — is followed here.

**This ADR supersedes nothing.**

## Follow-up

None of the following is authorised by this ADR:

1. **Submittals Gate 6** — component-boundary and caller-facing interface decision,
   including the enforcement mechanism.
2. **Submittals Gate 8** — module activation, workflow configuration, permissions,
   fixture suitability and data readiness.
3. **Submittals capability adoption** — no workflow-contract record is created.
4. **Submittals MCP implementation** — no tool, client or helper is authorised.
5. **A Phase 4 Submittals evidence schema** and the evidence artifact itself.
6. **Any later profile extension** revisiting `priority`, packages, spec sections,
   item types, responses, review steps, attachments or comments.

Separately, the following known documentation defects are **deferred** and
deliberately not addressed by this change: the RFI Gate-2 row in the §16 table; the
§6 `filter[reviewResponseId]` / `filter[responseId]` discrepancy; and the §6
`GET items` 1–50 pagination claim, which is verified only for sibling endpoints.
Each belongs to its own correction increment.
