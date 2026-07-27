# ADR-0010: Approve RFI public-evidence sanitisation profile

## Status

Accepted

## Date

2026-07-27

## Context

> **Numbering note.** This is **reference-repo ADR-0010**. The APS/Forma MCP
> component repository maintains its own, independent ADR series.

RFIs are an **adopted governed capability** in the schema-v2 workflow contract —
`api_family: Autodesk Forma Build RFI API`, `api_version: v3`, `api_maturity: ga`,
`mcp_component: aps-forma-mcp`, `mcp_implementation_status: planned`,
`data_readiness: not-assessed`. Adoption established governance; it established
nothing about what RFI data may be published.

**RFI Gate 5 (privacy and sanitisation planning) is the open question this ADR
answers.** The Phase 4A research ranked RFIs as the **highest narrative-leakage
surface** of the verified modules
([PHASE_4_CAPABILITY_GAP.md](../architecture/PHASE_4_CAPABILITY_GAP.md) §13.1):
question text, official answers, suggested answers and response bodies are
long-form prose authored by identified people about a real project, and
assignees, reviewers, managers and watchers are identities.

The normative Autodesk RFI v3 documentation establishes three facts that shape
this profile for the adopted first read-only slice — `GET users/me`,
`POST search:rfis`, `GET rfis/:rfiId`:

- **`GET users/me` returns the authenticated operator's real name** (`user.name`)
  and Autodesk ID, and its permitted/required-attribute blocks carry **Autodesk
  user, company and role identifiers** inside `values[].value` — data that reads
  as harmless permissions metadata but is identity-bearing.
- **`POST search:rfis` supports a server-side `fields` projection**, so collection
  itself can be minimised before any sanitisation step.
- **`GET rfis/:rfiId` accepts no query parameters** and **embeds `responses[]`
  including `text`**, so narrative arrives with the record whether or not a
  separate responses operation is called.

The existing [SANITISATION_CONVENTION.md](../guides/SANITISATION_CONVENTION.md)
and the Transmittals profile
([ADR-0005](0005-approve-transmittals-sanitisation-profile.md),
[ADR-0006](0006-approve-cross-surface-transmittals-evidence-semantics.md)) supply
the governing model, but **do not transfer unchanged**: Transmittals' dominant
risk was behavioural read-receipt telemetry, whereas RFI's is narrative authored
by identified people.

## Decision

Approve the **RFI public-evidence profile, version 1**, recorded in
[SANITISATION_CONVENTION.md](../guides/SANITISATION_CONVENTION.md). It **extends**
the existing conventions and **redefines nothing**, and it does not change the
Transmittals profile.

### Public-evidence boundary

**This ADR governs what may cross into public repository evidence** under
`examples/**/expected-results/`. Raw RFI narrative may exist transiently during
authenticated processing, and inside the existing git-ignored `.local/`
raw-observation boundary under the rules already in force.

**Real RFI narrative must never appear in public repository evidence.** The
allowed standard representation is enums, booleans, safe aggregates, approved
aliases, and narrative-presence facts.

### First-slice scope

The profile governs the adopted first read-only slice only: `GET users/me`,
`POST search:rfis`, `GET rfis/:rfiId`. Comments, attachments, separate response
operations, and all writes are outside it. `GET rfis/:rfiId` embeds `responses[]`,
so response narrative is covered here by necessity.

### Alias policy

**Approved new alias:** `RFI_n` — an RFI record. It is the **only** RFI-specific
alias in version 1.

**Reused where genuinely required:** `PROJECT_n`, `USER_n`.

**Deliberately not introduced,** each for a stated reason:

- **`RFI_TYPE_n`** — `rfiTypeId` is omitted from version-1 public evidence. Type
  identity is not needed to prove that search works, that a stable RFI identity
  exists, that workflow/status metadata is readable, or that the search identity
  continues into the detail read. If RFI Types later become an adopted capability,
  an alias may be introduced then.
- **`RESPONSE_n`** — response identity is unnecessary in the first evidence slice;
  responses reduce to a count and a state/status distribution.
- **`WORKFLOW_n`** — already denotes **Review workflow identity** in the base
  convention. RFI `workflowType` is an **enum** (`US` / `EMEA`), not an
  identifier, so no workflow alias is required and reuse would be a domain
  collision.
- **`TEXT_n`, `QUESTION_n`, `ANSWER_n`, `LOCATION_n`, `MESSAGE_n`** — narrative is
  **content, not stable repository identity**. Aliasing it would imply an identity
  it does not have, and adds no proof a presence boolean does not already carry.
  This follows the Transmittals profile, which records `MESSAGE_n` as not approved
  and not to be introduced.

Aliases are assigned deterministically **within one private capture** and carry no
meaning across captures.

### Identifier policy

**Raw identifier values are always removed from public evidence.** A raw
identifier value must never appear unmodified, hashed, truncated, partially
masked, or otherwise transformed in a way that preserves the operand.

**Where an identity, reference, or equality proof is genuinely required, the raw
value is replaced only with an approved domain-specific alias under this
convention.** Approved alias replacement is expressly permitted; it is the
mechanism by which equality is expressed without disclosure.

The raw values covered are: RFI IDs · project and container IDs · Autodesk user
IDs · actor, assignee, reviewer, manager and watcher IDs · response IDs ·
`rfiTypeId` · LBS / location-node IDs · custom-attribute IDs · `virtualFolderUrn`
and any URN · identifier-bearing URLs.

Equality is expressed through **deterministic capture-local alias equality** —
`RFI_1` returned by search is the same `RFI_1` fetched by detail — while the raw
operand is never published.

### `customIdentifier` — omitted

`customIdentifier` (the human-readable RFI number) is **omitted from public
evidence and not aliased**, treated analogously to the Transmittals `sequenceId`
already in the always-removed list. It is project-specific, can disclose project
scope or volume, and is never a join key.

### `users/me` minimisation

**Omitted:** `user.id`, `user.name`, any email or contact field, and every raw
permitted/required-attribute operand containing user, company or role IDs.

**Default posture: no `USER_n` is published for the authenticated caller.** The
evidence proves which role and permissions the caller holds; the identity is not
required for that proof, and omission is safer than an alias.

**Publishable, safe or derived:** role enum · workflow-type enum ·
`can_create_rfi` boolean · permitted-status enums · max-assignee count ·
required/permitted attribute **names** · allowed-value **counts** · attribute
user/company/role **type** enums where no operand is exposed.

### `search:rfis` public-evidence projection

The server-side `fields` projection **should be used where supported**, so
collection is minimised before sanitisation.

Public evidence may include: `RFI_n` · `status` · `workflow_type` · safe
aggregate/count metadata under the existing aggregate policy · `projection_used` ·
`read_semantic_post`.

**Not included:** `rfiTypeId` · `title` · `question` · `customIdentifier` ·
`discipline` · `category`.

### `rfis/:rfiId` public-evidence projection

The endpoint may return narrative and nested responses. **This ADR defines the
public-evidence projection only; it does not prescribe the complete MCP output.**

Public evidence may prove: RFI alias continuity · status and workflow state · safe
categorical metadata · safe counts · presence booleans.

**No real narrative. No `rfiTypeId`. No `discipline` or `category`.**

### Free-text policy

**Default: omit the content.** The standard public representation is **derived
machine-safe properties** — for example `question_present: true`,
`official_response_present: false`, `suggested_answer_present: false`,
`response_count: 1`, `narrative_content_published: false`.

**Never published as real content:** `title` · `question` · `officialResponse` ·
`suggestedAnswer` · `responses[].text` · `locationDescription` · `reference` ·
custom text attribute values.

**No narrative aliases are created.**

Character counts are discouraged: length is weakly identifying and proves nothing
a presence boolean does not.

### Timestamp policy

RFI workflow timestamps are **person-linked** — `respondedAt`/`respondedBy`,
`answeredAt`/`answeredBy`, `closedAt`/`closedBy` pair a time with an actor. They
receive the stricter treatment the convention already applies to behavioural
telemetry, not the ordinary date-only reduction.

- `respondedAt`, `answeredAt`, `closedAt` → **booleans only**. No exact or rounded
  values, no intervals, no person-linked ordering or chronology.
- `responses[].createdAt` → **omitted**.
- `createdAt`, `updatedAt` → **omitted by default**; date-only (`YYYY-MM-DD`)
  permitted only for controlled synthetic teaching evidence where appropriate and
  non-identifying.
- `dueDate` → `has_due_date` boolean by default.

### Error policy

**The raw upstream RFI error body is never published.**

Permitted public evidence: HTTP status code or class · a stable **local** error
category · a fixed sanitised **local** reason · safe booleans. Categories may
include `authentication_failed`, `permission_denied`, `not_found`,
`rate_limited`, `transport_error`, `timeout`.

**Never published:** raw upstream messages · identifiers · identifier-bearing
URLs · request headers · tokens · diagnostic payloads.

### Controlled synthetic fixture rule

**Readable narrative may be publicly published only when it originates from an
explicitly controlled synthetic fixture satisfying this profile.**

A deliberately controlled synthetic RFI materially reduces disclosure risk and is
more mechanically auditable than post-hoc sanitisation of arbitrary real
narrative. **Synthetic status does not waive any requirement of this profile.**
Synthetic fixture content must still satisfy the identifier rules, the narrative
rules, the timestamp rules, the identity rules, the error rules, and the full
sanitisation checklist. The label "synthetic" is not, by itself, proof of safety.

Synthetic narrative is **optional** — omission is always acceptable.

This is a **policy rule**. It does not assert that such a fixture exists.

### Gate 5 versus Gate 6

**Gate 5 specifies the public-evidence contract. It does not prescribe the
complete caller-facing MCP interface.**

Gate 6 later decides actual tool boundaries, caller-facing fields, any optional
narrative exposure, client and helper design, and the enforcement mechanism.

Gate 5 requires only that **any future path producing public evidence must be
capable of enforcing this sanitisation/projection profile**.

### Gate 5 versus Gate 8

Gate 5 closes the **policy** question. Gate 8 later verifies the **instance**: an
active RFI module, a suitable workflow configuration, roles and permissions, an
actual controlled RFI fixture, and data readiness.

**Gate 5 closure does not imply that a fixture exists, that data readiness is
established, or that live verification occurred.** After closure, RFI
`data_readiness` remains **`not-assessed`** and Gate 8 remains **unresolved**.

## Consequences

- **RFI Gate 5 is closed** — the §16 gate table records `passed` for the RFI
  Privacy and sanitisation planning row, with a closure subsection at §16.5.
- **Gate 6 and Gate 8 remain unresolved**, `mcp_implementation_status` remains
  `planned`, and `data_readiness` remains `not-assessed`.
- **A useful first-slice evidence artifact is possible without any narrative** —
  the three projections prove search, identity continuity and workflow-state
  readability using aliases, enums, counts and booleans alone.
- **The `fields` projection becomes the preferred collection-time control**, so
  minimisation begins before sanitisation rather than after it.
- **This ADR authorises no implementation, no Autodesk call, no fixture, no
  evidence artifact, and no other gate closure.**
- **No workflow-contract change is required**; gate state is not a capability
  field.

## Rejected alternatives

- **Publishing exact RFI narrative.** RFI text is the highest-leakage content in
  Phase 4A and is authored by identified people about a real project.
- **Aliasing narrative as `TEXT_n` / `QUESTION_n` / `ANSWER_n`.** An alias implies
  a stable identity narrative does not have, and adds nothing a presence boolean
  does not already prove. Consistent with `MESSAGE_n` being unapproved.
- **Publishing `customIdentifier` as a harmless label.** It is the direct analogue
  of `sequenceId`, already always-removed, and can disclose project scope.
- **Minting `RFI_TYPE_n` in version 1.** Type identity proves none of the
  first-slice propositions; aliases are added only where the evidence model
  requires them.
- **Reusing `WORKFLOW_n` for RFI workflow.** It already denotes Review workflow
  identity, and RFI `workflowType` is an enum — reuse would silently merge two
  identifier domains.
- **Treating `discipline` and `category` as public-safe enums.** Their value sets
  are configured per project and can disclose project scope.
- **Publishing a `USER_n` alias for the authenticated caller in `users/me`.** The
  proof does not need the identity, so omission is strictly safer.
- **Prohibiting alias replacement along with raw values.** That would make
  equality proofs impossible and contradicts the alias mechanism this convention
  is built on. The rule is precise: the **raw operand** is prohibited; an
  **approved domain-specific alias** is the permitted substitute.
- **Treating a synthetic fixture as inherently safe.** Synthetic status reduces
  risk and improves auditability, but waives no requirement of this profile.
- **Specifying the complete MCP caller-facing response here.** That is Gate 6's
  decision; Gate 5 governs the public-evidence contract only.

## Interaction with existing ADRs

- **[ADR-0005](0005-approve-transmittals-sanitisation-profile.md)** — the
  structural precedent for a per-module public-evidence profile closing Gate 5.
  **Not superseded, not amended.** The Transmittals profile is unchanged; the RFI
  profile sits alongside it.
- **[ADR-0006](0006-approve-cross-surface-transmittals-evidence-semantics.md)** —
  unaffected. Its surface-scoped lineage and cross-surface equality rules are
  Transmittals / Data-Management specific and are not extended to RFIs.
- **[ADR-0007](0007-read-write-classification-by-state-semantics.md)** — supplies
  the endpoint-level approval that makes `POST search:rfis` a read. This ADR
  governs what that read's evidence may contain; it neither widens nor narrows
  that approval.
- **[ADR-0008](0008-govern-implementation-state-per-capability.md)** and
  **[ADR-0009](0009-define-capability-record-cardinality-for-schema-v2.md)** —
  unaffected. No capability record or field cardinality changes; gate state is not
  a capability field.

**This ADR supersedes nothing.**

## Follow-up

None of the following is authorised by this ADR:

1. **RFI Gate 6** — component-boundary and caller-facing interface decision,
   including any narrative exposure and the enforcement mechanism.
2. **RFI Gate 8** — module activation, workflow configuration, permissions, and an
   actual controlled RFI fixture.
3. **RFI MCP implementation** — no tool, client or helper is authorised.
4. **A Phase 4 RFI evidence schema** and the evidence artifact itself.
5. **Any later profile extension** revisiting `discipline`, `category`,
   `rfiTypeId`, comments, attachments or separate response operations.
