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
(2026-07-25), profile version 1.** This section governs public evidence for the
Phase 4A Transmittals read slice. It **extends** the conventions above and
**redefines nothing**; every existing rule continues to apply.

#### Approved alias registry

**Existing reused aliases** — already defined above, unchanged:

| Alias | Domain |
|---|---|
| `PROJECT_n` | the Autodesk project |
| `USER_n` | an Autodesk user, where a user-domain alias is needed |
| `VERSION_n` | an **exact** Data Management document version |
| `FOLDER_n` | a Data Management folder |

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
`FOLDER_2`, `VERSION_2`, `USER_2`, …).

**Not approved, and not to be introduced:** `LINEAGE_n`, `STORAGE_n` /
`STORAGE_OBJECT_n`, `MESSAGE_n`, `EMAIL_n`, `TIMESTAMP_n`. `DOCUMENT_n` exists
for the *document-lineage* domain from earlier phases and is **deliberately not
used** in this profile — `VERSION_n` is the evidence terminal node here, and
borrowing a lineage-domain alias would imply lineage evidence that is not
returned.

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
stable-lineage-returned classification, whose only approved value is
**`not_proven`** · authentication-mode category · the required OAuth scope name
**`data:read`**.

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

- `VERSION_n` represents an **exact Data Management document version**.
- **Raw version URNs and raw numeric versions are not published.**
- Public evidence **may** state `exact_version_returned: true`.
- Public evidence **may** state `exact_version_alias: VERSION_1`.
- Public evidence **must** record stable lineage only as **`not_proven`**.
- **No `LINEAGE_n` alias is approved for Phase 4A.**
- **Parsing or splitting a version URN does not create returned lineage
  evidence** — it is a client-side derivation.
- **Alias-number matches never prove joins.**

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
`exact_version_returned` · `stable_lineage_returned` · `endpoint_evidence` ·
`sanitisation_profile_version`.

**This is policy guidance, not the Phase 4 schema.** No artifact is created by
this profile, and **no Phase 4 schema exists yet**. The eventual schema may
refine these field names but **must not weaken the policy**.

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
15. Stable lineage is recorded only as `not_proven`, and no `LINEAGE_n` alias
    appears.
16. The public artifact was **generated separately** from the private capture —
    the private file was not sanitised in place.
