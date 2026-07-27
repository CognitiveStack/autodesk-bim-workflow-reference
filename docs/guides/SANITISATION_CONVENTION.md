# Sanitisation Convention

**Convention version:** 1
**Applies to:** all evidence committed under
`examples/**/expected-results/`, starting with the Phase 1 Revit-to-CDE trace.

Committed evidence must remain useful for learning while containing **no live
Autodesk identifiers and no private project information**. This guide defines how
raw observations are transformed into safe, sanitised, reproducible evidence. It
supports the public-repository hygiene rules in
[REPOSITORY_STRATEGY.md](../architecture/REPOSITORY_STRATEGY.md).

## The boundary

- **`.local/`** (git-ignored) holds private raw observations and the alias ↔ real
  mapping:
  - `.local/phase-1/raw-observations.json`
  - `.local/phase-1/sanitisation-map.json`
- **`examples/**/expected-results/`** holds **only** sanitised public evidence.

Raw identifiers never leave `.local/`. The mapping is retained locally so a run
stays reproducible for the operator, and is never committed.

## Alias tokens

Replace live values with deterministic tokens, assigned per type with a counter.
Tokens match the pattern `^[A-Z][A-Z0-9_]*$`.

| Real value (never committed) | Alias token |
|---|---|
| hub id | `HUB_1` |
| project id (`b.<uuid>` or `pro_…`) | `PROJECT_1` |
| folder id | `FOLDER_1` |
| item id / item URN | `ITEM_1` / `URN_ITEM_1` |
| version URN | `URN_VERSION_1` |
| derivative URN (base64 of a version URN) | never stored — represented by `URN_VERSION_1` |
| view GUID | `VIEWGUID_1` |
| stored file name | `MODEL_1.rvt` (extension preserved) |

The same real value always maps to the same alias within a run (via the local
map), so cross-references in the evidence stay coherent.

### Coordination and governance alias tokens

Additional tokens used by the governance and coordination evidence. These extend
the table above; they do not redefine it.

| Real value (never committed) | Alias token |
|---|---|
| Model Coordination model-set id | `MODEL_SET_1` |
| Model Coordination model-set (snapshot) version | `MODEL_SET_VERSION_1` |
| participating document / model lineage | `MODEL_1`, `MODEL_2` |
| exact document version used for coordination or review | `VERSION_1`, `VERSION_2` |
| document lineage referenced by an issue | `DOCUMENT_1` |
| issue id | `ISSUE_1` |
| issue type id | `ISSUE_TYPE_1` |
| issue reference / relationship record | `ISSUE_REFERENCE_1` |
| review id | `REVIEW_1` |
| review workflow id | `WORKFLOW_1` |
| review workflow step id | `STEP_1`, `STEP_2` |
| approval-status id | `APPROVAL_STATUS_1` |

Notes on specific tokens:

- **`MODEL_SET_1`** — a sanitised alias for **one Model Coordination model set**.
  It replaces the raw model-set identifier. Numbering is **local to the evidence
  artifact** (or to one bounded evidence package) and implies **no ordering, no
  chronology, and no importance**.
- **`MODEL_SET_VERSION_1`** — a sanitised alias for **one Model Coordination
  coordination snapshot**. It replaces the raw model-set-version identifier. It is
  **not** a Data Management document version. Its numeric suffix does **not**
  represent Autodesk's snapshot number unless a separate sanitised ordinal is
  explicitly recorded alongside it. It must **never** be substituted for
  `VERSION_1`.
- **`MODEL_1`** — the model/document **lineage** alias. Where a stored file name is
  needed, the same alias is used with the extension preserved (`MODEL_1.rvt`, as in
  the table above); the alias identifies the same model in both forms.
- **`VERSION_1`** — an **exact document-version** alias. Distinct from
  `URN_VERSION_1`, which aliases a raw version **URN**. A published result records
  the version alias, never the URN it came from.

### Transmittals public-evidence profile

**Approved by [ADR-0005](../decisions/0005-approve-transmittals-sanitisation-profile.md)
(2026-07-25), profile version 1; extended by
[ADR-0006](../decisions/0006-approve-cross-surface-transmittals-evidence-semantics.md)
(2026-07-27), profile version 2.** This section governs public evidence for the
Phase 4A Transmittals read slice. It **extends** the conventions above and
**redefines nothing**; every existing rule continues to apply.

**Two governing decisions, in layers.** ADR-0005 established this profile and
**remains Accepted**; its central judgement — that the **Transmittals surface
alone does not prove stable document lineage** — remains valid and is carried
forward unchanged below. ADR-0006 **extends** the profile after a first-party
**Data Management** read was verified to return an item resource identity
directly, adding surface-scoped lineage rules, cross-surface version-equality
rules, and evidence-provenance classifications. **ADR-0005 is not superseded and
was not mistaken**; it was correct on the evidence available in 2026-07.

#### Approved alias registry

**Existing reused aliases** — already defined above, unchanged:

| Alias | Domain |
|---|---|
| `PROJECT_n` | the Autodesk project |
| `USER_n` | an Autodesk user, where a user-domain alias is needed |
| `VERSION_n` | an **exact** Data Management document version |
| `FOLDER_n` | a Data Management folder |
| `ITEM_n` | the **Data Management item resource** — the stable item/lineage identity for that surface. Added to this profile by ADR-0006; **not** a new family, it is the existing `ITEM_n` from the base table above |

**Newly approved aliases** for Transmittals:

| Alias | Domain |
|---|---|
| `TRANSMITTAL_n` | a Transmittals record |
| `RECIPIENT_n` | a **recipient-list record** — *not* a reusable global person identity |
| `EXTERNAL_MEMBER_n` | an external-recipient record |
| `COMPANY_n` | a company record or displayed company identity |
| `ROLE_n` | a custom project-role value |

All match the token pattern `^[A-Z][A-Z0-9_]*$` and use numbered continuation
(`TRANSMITTAL_2`, `RECIPIENT_2`, `EXTERNAL_MEMBER_2`, `COMPANY_2`, `ROLE_2`,
`FOLDER_2`, `VERSION_2`, `ITEM_2`, `USER_2`, …).

The five aliases `PROJECT_n`, `TRANSMITTAL_n`, `FOLDER_n`, `ITEM_n` and
`VERSION_n` are the **structural subset** used by cross-surface Transmittals and
Data Management evidence. The remaining approved aliases — `USER_n`,
`RECIPIENT_n`, `EXTERNAL_MEMBER_n`, `COMPANY_n`, `ROLE_n` — **remain approved and
governed by their existing domain rules**; they are simply not required by that
particular proof.

**Not approved, and not to be introduced:** `LINEAGE_n`, `STORAGE_n` /
`STORAGE_OBJECT_n`, `MESSAGE_n`, `EMAIL_n`, `TIMESTAMP_n`.

- **`LINEAGE_n` remains unapproved, and is additionally unnecessary.** The Data
  Management **item** resource already *is* the lineage-bearing resource, and
  `ITEM_n` aliases it. Publishing both `ITEM_n` and `LINEAGE_n` for one Autodesk
  resource would imply **two independently proven identities where only one
  exists** (ADR-0006).
- **`DOCUMENT_n` is deliberately not used in this profile.** It exists for the
  *document-lineage* domain from earlier phases; `VERSION_n` is the evidence
  terminal node on the Transmittals side, and borrowing a lineage-domain alias
  there would imply lineage evidence the Transmittals response does not return.
  This exclusion is **scoped to this profile** and changes nothing about
  `DOCUMENT_n` in other phases or profiles.

**Alias scope.** Aliases are assigned **deterministically within one private
evidence capture**. They carry **no meaning across unrelated captures** unless an
explicit private mapping says otherwise. `RECIPIENT_1` in one artifact and
`RECIPIENT_1` in another are not the same person.

#### Field-handling policy

**Always remove from public evidence** — never published in any form, aliased,
hashed, truncated or otherwise:

raw project IDs · raw transmittal IDs · `sequenceId` · Autodesk user IDs ·
email addresses · real personal names · company Autodesk IDs · `storageUrn` ·
raw folder URNs · raw document/version URNs · `parentFolderUrn` · raw API URLs
containing identifiers · OAuth tokens or request headers · comments and private
diagnostic payloads.

**Omit by default** — publishable only as a synthetic value or an approved alias
where a teaching artifact genuinely needs one:

`title` · `message` · `description` · folder names · file names ·
`revisionLabel` · company names · role names · exact `createdAt` · exact
`lastUpdatedAt` · exact `receivedAt` · exact `viewedAt` · exact `downloadedAt`.

**May retain as controlled categorical evidence:**

Transmittals status enums (`SENDING` / `COMPLETED` / `FAILED`) ·
`displayRecipients` enum (`ALL` / `LIMITED`) · HTTP method and endpoint family ·
HTTP status class or an approved exact status code · processing-pending boolean ·
`isDeleted` boolean where required · exact-version-returned boolean ·
**surface-scoped** stable-lineage classifications — Transmittals-surface, whose
only approved value remains **`not_proven`**, and Data-Management-surface, which
may be **`proven`** only when `ITEM_n` was directly returned · cross-surface
version-equality outcome with its comparison method · evidence-provenance class ·
proof-reproducibility classification · authentication-mode category · the required
OAuth scope name **`data:read`**.

**May retain as aggregate evidence:**

transmittal count · recipient count · external-recipient count · folder count ·
document-version count · recipients-viewed count · recipients-downloaded count ·
pagination page count.

Exact counts are permitted **only** when the scenario uses synthetic training
data, **or** the count presents no reasonable re-identification risk. Otherwise
bucket the value or omit it.

#### Behavioural telemetry policy

`receivedAt`, `viewedAt` and `downloadedAt` are **behavioural / read-receipt
telemetry**: they record whether and when an identified person received, opened
or downloaded a transmittal. **They receive stricter treatment than ordinary
technical timestamps** and are *not* covered by the date-only reduction that
applies elsewhere in this document.

**Public evidence must never expose the exact timestamps.** Allowed
transformations are:

- `received: true` / `false`;
- `viewed: true` / `false`;
- `downloaded: true` / `false`;
- aggregate counts;
- omission.

**Never publish:** event ordering tied to named people · time intervals between
events · exact or rounded timestamps · per-person activity chronology.

#### Narrative and name policy

- `title` and `message` are **omitted** or replaced with clearly synthetic text.
- Descriptions are **omitted** or synthetic.
- File and folder names are synthetic or represented by aliases.
- Company names use `COMPANY_n` unless deliberately fictional.
- Custom project roles use `ROLE_n` unless deliberately fictional.
- **External recipients are always synthetic** in the training scenario.
- **Do not use realistic-but-modified email addresses.** Where an email-shaped
  value is unavoidable in private test preparation or a screenshot, use a
  clearly synthetic domain such as `example.invalid`. **Prefer omission in
  published JSON.**

#### Exact version and lineage policy

- `VERSION_n` represents an **exact Data Management document version**, and is
  **immutable**.
- **Raw version URNs and raw numeric versions are not published.** Autodesk's
  numeric version property is never published — no `versionNumber = 1`, no
  `versionNumber = 2`. The alias relation `VERSION_1` / `VERSION_2` expresses the
  structure instead.
- Public evidence **may** state `exact_version_returned: true`.
- Public evidence **may** state `exact_version_alias: VERSION_1`.
- **Parsing or splitting a version URN does not create returned lineage
  evidence** — it is a client-side derivation.
- **Alias-number matches never prove joins.**

##### Lineage is surface-scoped

Lineage claims are recorded **per API surface**, never as one blended
proposition. A public artifact must make clear **which surface established which
claim**, so a reader can tell them apart. This is the same discipline that keeps
`typed_issue_field` and `viewer_state_derived` separate in the evidence-wording
rules below.

**Transmittals surface — `not_proven`, unchanged (ADR-0005).**

- The Transmittals response **does not independently provide** a stable
  source-document/item lineage identity.
- Public evidence **must** continue to record Transmittals-surface stable lineage
  only as **`not_proven`**.
- No lineage may be obtained from a Transmittals version identifier by **URN
  splitting, version-suffix removal, reconstruction, canonicalisation, pattern
  inference or any other string surgery**. Each of those is a client-side
  derivation, not returned evidence.
- **Nothing in this profile converts the Transmittals response into a lineage
  source.**

**Data Management surface — provable when directly returned (ADR-0006).**

- The Data Management **item resource** is the stable item/lineage identity for
  that surface, and `ITEM_n` aliases it.
- Public evidence **may** record Data-Management item/lineage identity as
  **proven** — but **only** when `ITEM_n` was returned **directly as a field** by
  the first-party Data Management resource.
- If the identity was not directly returned, it is **not** proven, and no amount
  of aliasing changes that.

**Cross-surface relation — exact version equality (ADR-0006).**

- A Transmittals `VERSION_n` may be related to a Data Management `VERSION_n`
  **when the two returned identifiers were compared by byte-for-byte exact string
  equality**.
- That comparison proves an **exact version relationship**. It does **not** prove
  lineage on the Transmittals surface, and it does **not** convert the
  Transmittals response into a lineage source.
- The relation must be recorded with its **comparison method**, not merely as an
  assertion.

#### Cross-surface proof rules

Public evidence **may** record the following, when each was directly established:

| Claim | Established by | Publishable |
|---|---|---|
| Transmittals `VERSION_1` == Data Management `VERSION_1` | byte-for-byte exact string equality | aliases, comparison method, surface roles, `PASS`/`FAIL` outcome |
| Data Management current tip == `VERSION_2` | a directly returned Data Management tip relation | as above |
| `VERSION_1` != `VERSION_2` | exact comparison | as above |
| `ITEM_1` has exactly the returned version set | permitted structural metadata, e.g. `count` with `has_more` | the counts and the completeness conclusion |

**The raw operands are never published.** A public artifact records *that* a
comparison was made, *how*, between *which surfaces*, and *what it returned* —
never the values compared. Completeness may be established structurally: for
example `count = 2` with `has_more = false` shows that exactly two version records
were represented, **without** publishing Autodesk's numeric version property.

#### Exact-version snapshot verdict

The verdict **`exact_version_snapshot_proven`** is approved **only** for a
controlled experiment that satisfies the cross-surface proof rules above.

Preferred prose: *"Exact-version snapshot behaviour was proven for the controlled
training fixture."*

The verdict applies to the **tested fixture and observed API behaviour**. It does
**not** mean that Gate 8 as a whole is proven; that universal Autodesk
Transmittals behaviour is proven; that every tenant, region or configuration
behaves identically; that Phase 4A is complete; or that the Harrismith example
contains the fixture. Universal product guarantees must not be stated, and
sanitising values must never upgrade the strength of a claim.

#### Evidence-provenance classifications

An alias-only artifact sometimes needs to record **why a retained alias is
trusted** without revealing its raw value. The freeze policy is
**`VERIFIED_SURVIVING_VALUE`**: explicitly classified surviving sources are
permitted, rather than requiring every value to remain in its first-ever
originating response.

| Class | Meaning |
|---|---|
| **`ORIGINATING_RESULT`** | The raw value remains available from the original live result that established the alias. |
| **`VALIDATED_RETAINED_INVOCATION`** | The original establishing result aged out, but the genuine previously resolved raw value survives verbatim as an invocation parameter used in subsequent successful controlled live operations. |
| **`EQUALITY_VERIFIED_LATER_RESULT`** | The original establishing result aged out, but the same resource identity was returned directly by a later first-party read, and had previously been established equal to the retained alias through exact comparison. |

These describe **evidence provenance only**. They do **not** change Autodesk
resource semantics, and they permit **no** reconstruction, inference, derivation,
string transformation, or substitution of one identifier for another outside an
explicitly approved class.

Public evidence **may name a provenance class without exposing the raw value**.
Where provenance is **weaker than `ORIGINATING_RESULT`, the record must say so** —
neither the public artifact nor the private freeze may present mixed provenance as
though every value were uniformly sourced.

#### Proof reproducibility

Distinguish a **historically established** proof from a **re-derivable** one.

A public sanitised artifact **may record a historical equality result** even though
the independent raw operands are deliberately excluded from Git. Evidence may
distinguish:

- **historical attestation** — the result was established while the independent
  operands were simultaneously available, and is recorded as an outcome;
- **re-derivable from private frozen evidence** — the frozen private identifier set
  still permits an independent re-check;
- **re-derivable from public evidence** — the published artifact alone permits a
  re-check.

For an alias-only public artifact the last will normally be **no**. **That is
intentional, not an evidence defect.** Raw identifiers must **never** be
duplicated into a public artifact merely to make a historical proof re-runnable —
that would invert this convention's boundary for the sake of tidiness.

#### Private evidence boundary — two-artifact workflow

**Private evidence may include** raw API responses, raw identifiers, raw
timestamps, raw names and email addresses, and request correlation data.

**Private evidence must:**

- remain **outside Git**, in the designated private evidence location;
- never be copied into issues, commit messages, or public documentation;
- be **transformed into a fresh public artifact**;
- **never be sanitised in place and then committed from the same file.**

The required workflow is **two artifacts**:

1. a **private raw capture**; then
2. a **separately generated public sanitised artifact**.

Editing the raw capture down to a publishable state in one file is not
permitted — it leaves the original content recoverable in history and invites
partial redaction.

#### Minimum public evidence shape (policy guidance, not a schema)

An illustrative shape only:

`project_alias` · `transmittal_alias` · `status` · `display_recipients` ·
`recipient_count` · `external_recipient_count` · `folder_count` ·
`document_version_count` · `recipient_activity_summary` · `included_folders`
(using `FOLDER_n`) · `included_versions` (using `VERSION_n`) ·
`exact_version_returned` · **surface-scoped lineage classifications** (one per
surface, replacing a single blended `stable_lineage_returned`) · **cross-surface
version-equality outcomes** with their comparison method · **item alias** (using
`ITEM_n`) and its returned version set with completeness metadata ·
**current-tip alias** (using `VERSION_n`) · **evidence-provenance class** per
retained alias · **proof-reproducibility classification** · `endpoint_evidence` ·
`sanitisation_profile_version`.

**This is policy guidance, not the Phase 4 schema.** No artifact is created by
this profile, and **no Phase 4 schema exists yet**. The eventual schema may
refine these field names but **must not weaken the policy**.

### RFI public-evidence profile

**Approved by [ADR-0010](../decisions/0010-approve-rfi-public-evidence-sanitisation-profile.md)
(2026-07-27), profile version 1.** This section governs public evidence for the
Phase 4A RFI read slice. It **extends** the conventions above and **redefines
nothing**; every existing rule continues to apply. It does not change the
Transmittals profile.

**Scope.** The adopted first read-only slice only: `GET users/me`,
`POST search:rfis`, `GET rfis/:rfiId`. `GET rfis/:rfiId` embeds `responses[]`, so
response narrative is covered here by necessity. Comments, attachments, separate
response operations, and all writes are outside this profile.

**Boundary.** This profile governs **what may cross into public repository
evidence**. Raw RFI narrative may exist transiently during authenticated
processing and inside the git-ignored `.local/` raw-observation boundary under the
rules already in force. **Real RFI narrative must never appear in public
evidence.** The allowed standard representation is enums, booleans, safe
aggregates, approved aliases, and narrative-presence facts.

#### Approved alias registry

**Existing reused aliases** — unchanged: `PROJECT_n` (the Autodesk project),
`USER_n` (a person reference, only where one is genuinely required).

**Newly approved alias:**

| Alias | Domain |
|---|---|
| `RFI_n` | an **RFI record** |

`RFI_n` is the only RFI-specific alias in version 1.

**Not approved, and not to be introduced:** `RFI_TYPE_n` · `RESPONSE_n` ·
`WORKFLOW_n` · `TEXT_n` · `QUESTION_n` · `ANSWER_n` · `LOCATION_n` · `MESSAGE_n`.

- **`RFI_TYPE_n`** — `rfiTypeId` is omitted from version-1 public evidence; type
  identity proves none of the first-slice propositions.
- **`RESPONSE_n`** — responses reduce to a count and a state/status distribution.
- **`WORKFLOW_n`** — already denotes **Review workflow identity**; RFI
  `workflowType` is an enum (`US` / `EMEA`), not an identifier. Reuse would merge
  two identifier domains.
- **Narrative aliases** — text is content, not stable repository identity.

#### Identifier policy

**Raw values are always removed from public evidence.** The raw identifier value
must never appear unmodified, hashed, truncated, partially masked, or otherwise
transformed in a way that preserves the operand. **Where an identity, reference,
or equality proof is genuinely required, replace the raw value only with an
approved domain-specific alias under this convention** — approved alias
replacement is permitted, and is the mechanism by which equality is expressed
without disclosure.

The raw values covered are:

RFI IDs · project and container IDs · Autodesk user IDs · actor, assignee,
reviewer, manager and watcher IDs · response IDs · `rfiTypeId` · LBS /
location-node IDs · custom-attribute IDs · `virtualFolderUrn` and any URN ·
identifier-bearing URLs.

Also never published in any form: `user.name` · email and contact fields · raw
permitted/required-attribute operands carrying user, company or role IDs · OAuth
tokens and request headers · raw upstream error bodies and diagnostic payloads.

Equality is expressed through **deterministic capture-local alias equality** —
`RFI_1` returned by search is the same `RFI_1` fetched by detail — while the raw
operand is never published.

#### Field-handling policy

**Omit** — not published in version 1, and not aliased:

`customIdentifier` (treated as the Transmittals `sequenceId` is treated) ·
`discipline` · `category` · `locationDescription` · `locations[]` · `reference` ·
`customAttributes[]` · `bridgedSource` · `bridgedTarget` · `bridgeSyncOutdated` ·
`syncVersion` · `isSelectable`.

**May retain as controlled categorical evidence:**

`status` · `previousStatus` · `workflowType` · `officialResponseStatus` ·
response `state` / `status` distributions · `priority` · `costImpact` ·
`scheduleImpact` · `user.role` · permitted-status enums · attribute
`values[].type` enums where no operand is exposed · HTTP method and endpoint
family · HTTP status class or an approved exact status code · authentication-mode
category · the required OAuth scope name **`data:read`** · `read_semantic_post`
(ADR-0007 endpoint-level approval) · `projection_used`.

**May retain as aggregate evidence,** subject to the existing aggregate rule:

result count · `commentsCount` · response count · assignee, reviewer and watcher
counts · `maxAssignees` · allowed-value counts · pagination page count.

#### Narrative policy

- **Default: omit the content.** The standard public representation is **derived
  machine-safe properties** — `question_present`, `official_response_present`,
  `suggested_answer_present`, `response_count`, `narrative_content_published`.
- **Never published as real content:** `title` · `question` · `officialResponse` ·
  `suggestedAnswer` · `responses[].text` · `locationDescription` · `reference` ·
  custom text attribute values.
- **No narrative aliases are created.**
- **Character counts are discouraged** — length is weakly identifying and proves
  nothing a presence boolean does not.

#### `users/me` minimisation

**Default posture: no `USER_n` is published for the authenticated caller.** The
evidence proves which role and permissions the caller holds; the identity is not
required, and omission is safer than an alias.

Publishable: role enum · workflow-type enum · `can_create_rfi` boolean ·
permitted-status enums · max-assignee count · required/permitted attribute
**names** · allowed-value **counts** · attribute type enums without operands.

#### `search:rfis` public-evidence projection

The server-side `fields` projection **should be used where supported**, so
collection is minimised before sanitisation.

Public evidence may include `RFI_n` · `status` · `workflow_type` · safe
aggregate/count metadata · `projection_used` · `read_semantic_post`. It does
**not** include `rfiTypeId`, `title`, `question`, `customIdentifier`,
`discipline` or `category`.

#### `rfis/:rfiId` public-evidence projection

Public evidence may prove RFI alias continuity, status and workflow state, safe
categorical metadata, safe counts, and presence booleans. **No real narrative, no
`rfiTypeId`, no `discipline` or `category`.**

#### Workflow-timestamp policy

RFI workflow timestamps are **person-linked** — `respondedAt`/`respondedBy`,
`answeredAt`/`answeredBy`, `closedAt`/`closedBy` pair a time with an actor. They
receive the stricter treatment applied to behavioural telemetry above, **not** the
ordinary date-only reduction.

- `respondedAt`, `answeredAt`, `closedAt` → **booleans only**. No exact or rounded
  values, no intervals, no person-linked ordering or chronology.
- `responses[].createdAt` → **omitted**.
- `createdAt`, `updatedAt` → **omitted by default**; date-only permitted only for
  controlled synthetic teaching evidence where non-identifying.
- `dueDate` → `has_due_date` boolean by default.

#### Error policy

**The raw upstream RFI error body is never published.** Permitted: HTTP status
code or class · a stable **local** error category (`authentication_failed`,
`permission_denied`, `not_found`, `rate_limited`, `transport_error`, `timeout`) ·
a fixed sanitised **local** reason · safe booleans.

#### Controlled synthetic fixture rule

**Readable narrative may be publicly published only when it originates from an
explicitly controlled synthetic fixture satisfying this profile.**

A deliberately controlled synthetic RFI **materially reduces disclosure risk and
is more mechanically auditable** than post-hoc sanitisation of arbitrary real
narrative. **Synthetic status does not waive any requirement of this profile** —
synthetic content must still satisfy the identifier rules, narrative rules,
timestamp rules, identity rules, error rules and the full checklist below. The
label "synthetic" is not, by itself, proof of safety.

Synthetic narrative is **optional**; omission is always acceptable. **This is a
policy rule and does not assert that such a fixture exists** — that is Gate 8.

#### Gate 5 / Gate 6 boundary

This profile specifies the **public-evidence contract**. It does **not** prescribe
the complete caller-facing MCP interface. Gate 6 later decides tool boundaries,
caller-facing fields, any optional narrative exposure, client design and the
enforcement mechanism. This profile requires only that **any future path producing
public evidence must be capable of enforcing it**.

**This is policy guidance, not the Phase 4 schema.** No artifact is created by
this profile.

## Identifier domains are not interchangeable

Each alias family names a **different kind of thing**. Mixing them silently
manufactures a relationship that the API never returned.

| Alias | Domain |
|---|---|
| `MODEL_SET_1` | coordination **model-set** domain |
| `MODEL_SET_VERSION_1` | coordination **snapshot** domain |
| `MODEL_1` | participating **document/model lineage** domain |
| `VERSION_1` | exact participating **Data Management document-version** domain |
| `ISSUE_1` | **issue** domain |
| `TRANSMITTAL_1` | **Transmittals record** domain |
| `RECIPIENT_1` | **recipient-list record** domain (not a global person identity) |
| `EXTERNAL_MEMBER_1` | **external-recipient record** domain |
| `COMPANY_1` | **company** domain |
| `ROLE_1` | **project-role** domain |
| `FOLDER_1` | **Data Management folder** domain |
| `ITEM_1` | **Data Management item** domain — the stable item/lineage identity for that surface |

Rules:

- Aliases from different domains are **not interchangeable**, and one is never
  written where another is meant.
- **Matching numeric suffixes imply nothing.** `MODEL_1`, `VERSION_1`,
  `MODEL_SET_VERSION_1` and `ISSUE_1` sharing the suffix `_1` does **not** imply
  identity, correspondence, or a relationship between them. Suffixes are
  per-domain counters, never evidence.
- **Raw identifiers, URNs, GUIDs, and hrefs must never be published** — in any
  field, note, warning, or free-text string.
- **No numeric document version is inferred from a URN.** If no authoritative
  version number was returned, the recorded version number stays `null`.
- **`tip_version_urn` is never substituted for `version_urn`.** The coordinated
  version is the exact version the snapshot used, not the current lineage tip.

## Evidence-wording rules

How a match was obtained must survive sanitisation. Sanitising values must never
upgrade the strength of a claim.

- A **viewer-state-derived** version match must be labelled as such (for example
  `evidence_class: viewer_state_derived`). It must **not** be rewritten as a typed
  relationship, a Relationships API record, clash membership, or clash provenance.
- A **typed issue-field** match (for example a placement lineage returned inside
  issue details) is labelled as a typed issue field — it is **not** automatically a
  Relationships API record.
- A **shared model-context** result must **not** be described as a direct clash
  link. `shared_model_context_proven` means the issue and the coordination snapshot
  refer to the same models at the same coordinated versions. It does **not**
  establish a typed issue-to-model-set relationship, a typed issue-to-snapshot
  relationship, a direct clash-to-issue relationship, clash membership, or
  geometric resolution.
- A **UI observation** is contextual only (`evidence_class: ui_context`) and is
  never sufficient for a `proven` machine-readable relationship.
- An **empty API result** is recorded as "no matching record was returned" — never
  as proof that no relationship exists.

## Values that are removed or reduced

| Kind | Handling |
|---|---|
| local or cloud paths | removed — represented as `"<local-path-redacted>"` where a placeholder is needed |
| hostnames, ports, endpoint URLs | never recorded |
| user names | aliased to `USER_1` |
| email addresses | removed entirely (represented by `USER_1` if a reference is required) |
| timestamps | reduced to date only, `YYYY-MM-DD`; time-of-day and timezone dropped |
| raw status-response bodies | never recorded (use the structured `runtime_status` object) |

## Values that may be kept as-is

These are design content, not identifiers, and carry no account-specific data:

- the public synthetic label **"Harrismith Fire Station"**;
- level names (e.g. "Ground Floor", "Roof");
- non-identifying view names and safe derivative view display labels.

If any such value embeds an identifier (for example a view name containing a GUID
or a person's name), alias it instead.

## Model-property allowlist

Only a small teaching allowlist of model properties may be persisted:

- `Category`
- `Family`
- `Type`
- `Level`
- element / property counts

Enforce a maximum sampled-element count (recommended: **25**). **Exclude** paths,
user names/emails, arbitrary shared/project parameter text, comments, URLs,
identifiers, and any property not required by the comparison.

## Timestamp handling

Prefer date-only values (`YYYY-MM-DD`). The result's `execution.execution_date` is
date-only by schema. Where an observed timestamp is not needed for the comparison,
omit it rather than reduce it.

## Sanitisation checklist (before committing evidence)

1. Every hub / project / folder / item / version / view value is an alias token.
2. No base64 derivative URN or raw URN appears anywhere.
3. No local path, hostname, port, endpoint URL, user name, or email appears.
4. All timestamps are date-only or omitted.
5. `selected_properties` contains only allowlisted fields within the sample cap.
6. `runtime_status` is a structured object, not a raw response body.
7. The result validates against its phase's schema — for example
   [`schemas/phase-1-result.schema.json`](../../schemas/phase-1-result.schema.json)
   for the Phase 1 trace, and the corresponding Phase 2 / Phase 3 schema for those
   slices.
8. `.local/` is confirmed git-ignored and was not staged.
9. Every alias belongs to the correct identifier domain, and no alias was written
   where a different domain was meant.
10. No conclusion was strengthened during sanitisation: viewer-state-derived and
    typed-issue-field matches are still labelled as such, UI observations are still
    contextual only, an empty API result is still recorded as "no matching record
    returned", and no shared model context is described as a direct clash link.

### Additional checks for Transmittals evidence

11. No email address, personal name, Autodesk user ID, company Autodesk ID,
    `sequenceId`, `storageUrn`, folder URN, `parentFolderUrn` or version URN
    appears — not hashed, not truncated, not partially masked.
12. No exact `receivedAt`, `viewedAt` or `downloadedAt` value appears; behavioural
    telemetry is reduced to booleans, counts, or omitted, with no per-person
    chronology, ordering or interval.
13. `title`, `message` and `description` are omitted or clearly synthetic.
14. External recipients are synthetic.
15. **Transmittals-surface** stable lineage is recorded only as `not_proven`.
16. **No lineage is inferred from a Transmittals version identifier** — no URN
    splitting, version-suffix removal, reconstruction, canonicalisation or pattern
    inference appears anywhere in the artifact or its notes.
17. **Data Management `ITEM_n` is recorded as a proven item/lineage identity only
    where it was returned directly by the first-party Data Management resource**;
    otherwise it is not recorded as proven.
18. **No `LINEAGE_n` alias appears.**
19. **Cross-surface `VERSION_n` equality is claimed only where directly
    established by byte-for-byte exact comparison**, is recorded with its
    comparison method, and does not publish the operands.
20. **No raw numeric Autodesk version value appears** — version structure is
    expressed through `VERSION_n` aliases and permitted completeness metadata such
    as `count` and `has_more`.
21. **Every retained alias carries an evidence-provenance class**, and any
    provenance weaker than `ORIGINATING_RESULT` is disclosed rather than presented
    as originating.
22. **`exact_version_snapshot_proven`, where used, is scoped to the controlled
    fixture** and makes no universal, tenant-wide, gate-wide or phase-completion
    claim.
23. The public artifact was **generated separately** from the private capture —
    the private file was not sanitised in place.

### Additional checks for RFI evidence

24. **No raw RFI, project, container, user, actor, response, `rfiTypeId`,
    location-node or custom-attribute identifier value appears**, and no
    `virtualFolderUrn` or other URN — not unmodified, hashed, truncated or
    partially masked. Where a reference was required, an **approved alias** was
    used instead.
25. **`customIdentifier` does not appear**, and was not aliased.
26. **No real RFI narrative appears** — no `title`, `question`,
    `officialResponse`, `suggestedAnswer`, `responses[].text`,
    `locationDescription`, `reference` or custom text value. Narrative is
    represented by presence booleans and counts.
27. **Any readable narrative present came from a controlled synthetic fixture, is
    clearly labelled synthetic, and satisfies every other rule in this checklist** —
    synthetic status waived nothing.
28. **`user.name`, `user.id`, email/contact fields and permitted/required-attribute
    operands are absent**, and no `USER_n` is published for the authenticated
    caller unless a reference is genuinely required.
29. **No exact `respondedAt`, `answeredAt` or `closedAt` value appears**; workflow
    chronology is reduced to booleans, with no interval or person-linked ordering.
30. **`rfiTypeId`, `discipline` and `category` are absent** from version-1 RFI
    evidence.
31. **No `RFI_TYPE_n`, `RESPONSE_n`, `WORKFLOW_n` or narrative alias appears.**
32. **No raw upstream RFI error body appears** — errors are a status, a local
    category, a fixed sanitised local reason, and booleans.
