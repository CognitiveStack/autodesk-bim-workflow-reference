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
7. The result validates against
   [`schemas/phase-1-result.schema.json`](../../schemas/phase-1-result.schema.json).
8. `.local/` is confirmed git-ignored and was not staged.
