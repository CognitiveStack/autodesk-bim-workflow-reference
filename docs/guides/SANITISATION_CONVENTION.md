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
