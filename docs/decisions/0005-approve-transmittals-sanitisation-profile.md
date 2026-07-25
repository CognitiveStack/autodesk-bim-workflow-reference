# ADR-0005: Approve the Transmittals sanitisation profile

## Status

Accepted

## Date

2026-07-25

## Context

[ADR-0004](0004-adopt-transmittals-as-first-phase-4a-read-slice.md) adopted the
Autodesk Forma Transmittals read-only slice as the first Phase 4A capability and
assigned it to the APS/Forma MCP. **Gates 2 and 6 are closed**, but **Gate 5
(privacy and sanitisation approval) must close before any schema or
implementation work**, because the alias tokens a module needs must be defined
*before* evidence is captured.

The normative Transmittals documentation shows a response surface materially more
sensitive than anything handled in Phases 1–3:

- **Sender, recipient and external-member identities are exposed.** Fields may
  include personal names, **email addresses**, company information and project
  roles.
- **Free text** may appear in the transmittal `title`, `message` and document or
  folder `description`.
- **Folder and file names** may expose project or commercial information.
- **`receivedAt`, `viewedAt` and `downloadedAt` are behavioural / read-receipt
  telemetry** — they record whether and when a *named individual* received,
  opened or downloaded a transmittal. No Phase 1–3 field has this character.
- **`storageUrn` and exact Autodesk identifiers** (transmittal IDs, folder URNs,
  version-qualified document URNs, Autodesk user and company IDs) are private
  infrastructure data.

The Harrismith evidence scenario is a teaching artifact published in a public
repository. It must therefore use **synthetic recipients**, and its public
evidence must be derived rather than redacted in place.

## Decision

Approve a Transmittals-specific public-evidence profile. The approved profile:

- **uses aliases instead of raw identifiers**;
- **omits correspondence and personal information** — narrative text, names,
  emails, and company or role labels;
- **reduces behavioural timestamps** to presence booleans, counts, or omission;
- **allows only controlled categorical and aggregate evidence** sufficient to
  prove the read-only workflow;
- **separates exact-version evidence from stable-lineage claims**, and never
  represents lineage as returned evidence;
- **applies to both manually captured evidence and future MCP-produced
  evidence**;
- **must be enforced before any public artifact is committed.**

The detailed governing policy lives in
[SANITISATION_CONVENTION.md](../guides/SANITISATION_CONVENTION.md); this ADR
records the decision and the approved alias registry.

## Approved aliases

### Reused — already approved, not redefined

These alias families already exist in
[SANITISATION_CONVENTION.md](../guides/SANITISATION_CONVENTION.md) and are reused
unchanged. **None is renamed or redefined.**

- **`PROJECT_n`** — the Autodesk project.
- **`USER_n`** — an Autodesk user, used only where a user-domain alias is needed.
- **`VERSION_n`** — an exact Data Management document version.
- **`FOLDER_n`** — a Data Management folder.

### Newly approved for Transmittals

- **`TRANSMITTAL_n`** — a Transmittals record.
- **`RECIPIENT_n`** — a recipient-list record.
- **`EXTERNAL_MEMBER_n`** — an external-recipient record.
- **`COMPANY_n`** — a company record or displayed company identity.
- **`ROLE_n`** — a custom project-role value.

All conform to the existing token pattern `^[A-Z][A-Z0-9_]*$`, and all use
numbered continuation (`TRANSMITTAL_2`, `RECIPIENT_2`, `EXTERNAL_MEMBER_2`,
`COMPANY_2`, `ROLE_2`, `FOLDER_2`, `VERSION_2`, `USER_2`, …).

### Domain rules

- `TRANSMITTAL_n` identifies a **Transmittals record**.
- `RECIPIENT_n` identifies a **recipient-list record**, **not** a reusable global
  person identity. The same human appearing in two transmittals is not
  guaranteed the same `RECIPIENT_n`.
- `EXTERNAL_MEMBER_n` identifies an **external-recipient record**.
- `USER_n` identifies an **Autodesk user**, only where a user-domain alias is
  needed.
- `COMPANY_n` identifies a **company record or displayed company identity**.
- `ROLE_n` identifies a **custom project-role value**.
- `FOLDER_n` identifies a **Data Management folder**.
- `VERSION_n` identifies an **exact Data Management document version**.
- `PROJECT_n` identifies the **Autodesk project**.

### Deliberately not introduced

- **`DOCUMENT_n` is not used in the Transmittals profile.** The family already
  exists for the *document-lineage* domain from earlier phases; `VERSION_n`
  already expresses the exact evidence terminal node here, and reusing a
  lineage-domain alias would imply lineage evidence that is not returned.
- **`STORAGE_n` / `STORAGE_OBJECT_n`** — storage identifiers do not appear in
  public evidence in any form, aliased or otherwise.
- **`MESSAGE_n`, `EMAIL_n`, `TIMESTAMP_n`** — these values are omitted, not
  aliased. An alias would imply the value is publishable in some form.
- **`LINEAGE_n`** — not approved unless a future first-party source returns and
  verifies a distinct lineage field.

## Consequences

- **Gate 5 closes for the first Transmittals read slice.**
- **Gate 8 remains open** — module activation, permission and synthetic-data
  readiness are unverified.
- **No implementation begins yet**, and this ADR authorises none.
- **The future Phase 4 schema must encode these rules**; it may refine field
  names but must not weaken the policy.
- **Private evidence may retain raw values locally but never in Git.**
- **Public artifacts must be derived separately** from the private capture.
- **Aliases do not prove relationships**, and **matching numeric suffixes never
  prove identity or a join** — `TRANSMITTAL_1`, `RECIPIENT_1`, `FOLDER_1` and
  `VERSION_1` sharing the suffix `_1` implies nothing.

## Rejected alternatives

- **Publishing synthetic-looking but real names.** A real name is personal data
  regardless of how ordinary it looks.
- **Hashing emails or Autodesk IDs.** A hash of a low-entropy identifier such as
  an email address is **reversible by dictionary attack** and remains a stable
  correlation key across artifacts. **Hashing is not approved anonymisation.**
- **Publishing raw exact timestamps.** Exact times attached to identified people
  reconstruct behaviour.
- **Publishing truncated URNs.** Truncation leaves a **correlatable prefix** that
  can be matched against other artifacts or a live tenant. **Truncation is not
  approved anonymisation.**
- **Deriving lineage from version URNs and presenting it as returned evidence.**
  Splitting a version-qualified URN is a client-side derivation, not something
  the API returned.
- **Treating all narrative text as safe because the project is a training
  project.** Training projects sit in real tenants beside real work, and a
  transmittal message can carry commercial content regardless of intent.

## Follow-up

1. **Verify Gate 8** — module activation, caller permission and synthetic
   training data.
2. **Create the Phase 4 schema and execution plan.**
3. **Implement the five MCP reads.**
4. **Capture private evidence** under the git-ignored private location.
5. **Transform it through the approved profile** into a separate artifact.
6. **Validate and publish the sanitised artifact separately.**

None of these is authorised by this ADR.
