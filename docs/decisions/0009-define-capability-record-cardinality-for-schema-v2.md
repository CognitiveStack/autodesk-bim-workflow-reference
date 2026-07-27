# ADR-0009: Define capability-record cardinality for schema v2

## Status

Accepted

## Date

2026-07-27

## Context

> **Numbering note.** This is **reference-repo ADR-0009**. The APS/Forma MCP
> component repository maintains its **own, independent** ADR series. The two are
> unrelated and are **not** a shared sequence.

[ADR-0008](0008-govern-implementation-state-per-capability.md) established that a
workflow stage is the BIM workflow / teaching category and a **capability** inside
it is the unit of implementation governance. It listed the nine fields of a
capability record. **It did not state which of them are required.**

The schema-v2 design and mapping pass tested the target model against all eight
current schema-v1 stages and found that the missing cardinality rule — not any
missing Autodesk fact — is what blocks migration:

- **`asset_handover`** already represents a **governed but planned** capability
  whose API family is **deliberately unasserted** under
  [ADR-0003](0003-autodesk-platform-product-and-api-terminology.md). Schema v1
  expresses this as `api_families: []` plus a note, a form ADR-0003 explicitly
  records as "expected rather than a defect". It carries four substantive facts:
  `primary_system: Forma Build`, `mcp_component: aps-forma-mcp`,
  `mcp_implementation_status: planned`, `data_readiness: not-assessed`.
- **`revit_authoring`** has an asserted API family but **no repository-supported
  `api_version`**, and `api_maturity: not-applicable` — the Revit desktop API sits
  outside the APS lifecycle vocabulary.
- **`cde_information_management`**, **`model_coordination`** and
  **`reviews_and_issues`** carry `api_maturity: to-be-verified` and **no
  repository-supported API version**.
- Requiring every field on every capability would therefore **force invented
  facts** — an API family for Assets, a version for Revit, versions for three
  unverified APIs.
- Mapping `asset_handover` to `capabilities: []` would **erase four governed
  facts**.

ADR-0008 implicitly assumed a stage either has adopted capabilities or has
nothing. A third state exists and is already first-class in schema v1: **governed,
but not adopted**. This ADR supplies the rule that makes that state — and every
other current stage — representable without manufacturing a single value.

## Decision

### 1. A capability record represents a governed capability

A capability record represents a **governed capability within a workflow stage**.

A capability does **not** need to be implemented, partially implemented,
API-family verified, data ready, or live verified in order to be recorded.
Statuses such as **`planned` are valid capability-record states**.

Governance — not implementation — is what a capability record asserts.

### 2. `capabilities: []` — refined meaning

**`capabilities: []` means the workflow stage currently has no governed capability
represented in the reference implementation.**

It does **not** mean:

- no MCP implementation exists;
- no API family has been asserted;
- no data is ready;
- no capability is yet adopted or implemented.

**A governed planned capability is therefore represented by a capability record,
never by an empty list.**

This **refines** ADR-0008's wording about "a stage with no adopted capability".
ADR-0008 is not amended; its rule stands, and this ADR states precisely which
absence it describes.

### 3. Capability-field cardinality

| Field | Cardinality | Rule |
|---|---|---|
| `id` | **REQUIRED** | Stable, machine-oriented capability identity, scoped within the workflow stage. |
| `primary_system` | **REQUIRED** | The product/system surface associated with the governed capability. |
| `api_family` | **CONDITIONAL** | Present when the repository has asserted the developer API family under ADR-0003. **May be absent** when the capability is governed/planned and a family has deliberately not yet been asserted. Absence means **UNASSERTED**, never "no API exists". |
| `api_version` | **CONDITIONAL** | **Required whenever the repository makes a concrete lifecycle assertion** — that is, when `api_maturity` is `beta` or `ga` — because ADR-0008 established *API family + API version → lifecycle assertion*. **May be absent** when `api_maturity` is `to-be-verified`, and when it is `not-applicable` unless a version fact is independently required by another contract. |
| `api_maturity` | **REQUIRED** | Every capability record carries a value. Vocabulary unchanged: `beta` · `ga` · `to-be-verified` · `not-applicable`. This does **not** mean every capability has a verified Autodesk lifecycle: `beta` and `ga` are concrete lifecycle assertions, `to-be-verified` is the repository's epistemic sentinel, and `not-applicable` means the classification does not apply to that API context — which is why the field can be required without inventing lifecycle facts. |
| `mcp_component` | **REQUIRED** | Every current governed capability, including planned `asset_handover`, already identifies its owning or intended component. This asserts **ownership, not implementation**; the two remain separate axes. |
| `mcp_implementation_status` | **REQUIRED** | Vocabulary unchanged: `confirmed` · `partial` · `planned` · `not-applicable`. **`planned` is explicitly valid.** `partial` describes **that capability's own** MCP surface, never several capabilities aggregated at stage level. |
| `data_readiness` | **REQUIRED** | Vocabulary unchanged: `ready` · `blocked` · `not-assessed`. **Never derived from implementation status.** |
| `data_readiness_reason` | **OPTIONAL** | Schema-v1 semantics preserved. **No reason may be invented where none exists.** |

**`to-be-verified` remains epistemic** — it records that the repository has not
established the lifecycle classification to its required evidence standard, and is
**never** an Autodesk lifecycle state. For a governed planned capability whose API
family is unasserted, it records that no lifecycle classification has yet been
established for that capability's future or expected developer API surface.

**`not-applicable` retains ADR-0008's meaning** — the capability/API is
identified, but the Autodesk lifecycle classification represented by
`api_maturity` does not apply to that API context.

**`to-be-verified` must never be used as an `api_version` value.** An unknown
version is represented by **omission**, not by a new sentinel. Introducing one
would create a semantic ADR-0008 never approved.

### 4. `api_version` semantics

**`api_version` records the API contract / request-route version relevant to the
implemented or governed API surface — not the documentation-set version.**

This follows the already-published Site Design precedent
([GLOSSARY.md](../guides/GLOSSARY.md)):

```
documentation set : v1
route / API contract : v1alpha
schema-v2 api_version : v1alpha
```

The same distinction applies elsewhere — an Autodesk documentation set may be
versioned `v2` while its request routes carry different version segments. Every
Autodesk API examined so far has these **two independent version axes**, and
schema v2 binds to the route/contract axis.

**No unresolved version is researched or populated by this ADR.** This decision
defines the semantic axis only.

### 5. No invented facts

The schema-v2 migration **must not manufacture values merely to satisfy
structure**. Specifically prohibited:

- no invented API family;
- no invented API version;
- no invented readiness reason;
- no conversion of a planned capability into an implemented or adopted capability.

**Omission is permitted only where this ADR explicitly makes a field conditional
or optional.**

## Application to current stages

Recorded as worked proof that the rules preserve existing meaning. **No YAML is
changed by this ADR.**

### `asset_handover`

The existing schema-v1 stage already governs an Assets capability through its
`primary_system`, its planned MCP status, its intended component ownership, and
its recorded note. The capability is additionally named **"Assets"** in
[COMPONENT_BOUNDARIES.md](../architecture/COMPONENT_BOUNDARIES.md) §6 and in the
[PRD](../prd/PRD_AUTODESK_BIM_WORKFLOW_REFERENCE_IMPLEMENTATION.md), so the
identifier `assets` is **derived from existing repository language, not coined
here**.

Its future representation may conceptually be:

```
capabilities:
  - id: assets
    primary_system: Forma Build
    api_maturity: to-be-verified
    mcp_component: aps-forma-mcp
    mcp_implementation_status: planned
    data_readiness: not-assessed
```

with **`api_family` omitted** (deliberately unasserted under ADR-0003) and
**`api_version` omitted** (no lifecycle assertion requires binding).

**This is not the creation of a new capability.** It makes an already-governed
capability representable, and **no Assets API family is invented**.

### `revit_authoring`

May conceptually retain `api_family: Autodesk Revit API` and
`api_maturity: not-applicable` while **omitting `api_version`**, because the
repository contains no supported version fact and no concrete Beta/GA lifecycle
assertion that would require version binding. **No Revit release number is
chosen.**

### `to-be-verified` capabilities

The future records for **Data Management**, **Model Coordination** and **Issues**
may retain `api_maturity: to-be-verified` while **omitting `api_version`**.

This is **deliberate truth preservation, not missing-data repair.** Later
lifecycle and version research may populate both facts in separate,
evidence-backed increments.

## Constraints

- **This ADR changes no data.** `config/workflows/end-to-end-reference.yaml`
  remains `schema_version: 1` and remains authoritative.
- **DECISION ACCEPTED is not CONTRACT MIGRATED.**
- **No API family, API version, or readiness reason is asserted, researched or
  populated here.**
- **No capability record is written to YAML**, and no `capabilities:` key is
  introduced.
- **No RFI capability** is added or implied.
- **ADR-0008 is not amended.** Its text stands unchanged as the historical
  decision record.

## Consequences

- **The cardinality gap that blocked schema-v2 migration is closed.** The rules
  are stated once, in one place.
- **All eight current stages become losslessly representable** — the design pass
  found no remaining factual blocker once conditional fields are permitted.
- **Missing API versions cease to be blockers** for `to-be-verified` and
  `not-applicable` capabilities, because no lifecycle assertion is being made that
  would require a version binding.
- **`asset_handover` is represented by a governed planned capability record**
  rather than `capabilities: []`, preserving all four of its existing facts.
- **Structure can never force invention.** A field is either supported by evidence
  or omitted under an explicit rule.
- **The migration design pass should be re-evaluated against these rules** before
  the migration increment is authorised.
- **This ADR authorises no migration, no configuration change, no RFI adoption, no
  implementation, and no Autodesk API call.**

## Non-goals

ADR-0009 does **not** resolve, and must not be cited as resolving:

- **the schema-v2 migration itself** — the configuration is unchanged;
- **any unresolved API version** for Data Management, Model Coordination, Issues,
  Revit or Assets;
- **the Assets API family name**, which remains deliberately unasserted under
  ADR-0003;
- **the RFI API-family name**, or any RFI adoption;
- **capability ids for stages other than the illustrative `assets` case**, which is
  cited as derived language rather than fixed here;
- **the `document_management` versus `data_management` naming choice** raised by
  the design pass;
- **machine-readable evidence, live-verification or gate fields** — ADR-0008's
  exclusion stands;
- **Gate 5, Gate 6 or Gate 8** for any module — no gate is closed.

## Interaction with existing ADRs

- **[ADR-0008](0008-govern-implementation-state-per-capability.md)** — **remains
  accepted and unchanged.** ADR-0009 **refines** its target capability record by
  defining field cardinality, and **clarifies** the meaning of `capabilities: []`.
  No ADR-0008 historical text is modified. **Together the two decisions govern
  schema-v2 migration**; neither is sufficient alone.
- **[ADR-0003](0003-autodesk-platform-product-and-api-terminology.md)** — still
  governs API-family terminology. The **conditional `api_family` rule directly
  supports** ADR-0003's deliberate non-assertion practice, and **no API name is
  invented here.** Not amended.
- **[ADR-0007](0007-read-write-classification-by-state-semantics.md)** — unrelated
  except in sequence. Read/write classification is unchanged.

**No earlier ADR is superseded.**

## Rejected alternatives

- **Requiring every field on every capability.** It would force an invented Assets
  API family, an invented Revit version, and invented versions for three
  unverified APIs — the precise failure mode ADR-0008 and ADR-0003 exist to
  prevent.
- **Mapping `asset_handover` to `capabilities: []`.** It would erase four governed
  facts and fail a semantic round-trip. `capabilities: []` describes absence of
  governance, not absence of implementation.
- **Introducing `to-be-verified` as an `api_version` value.** It would invent a
  second, unapproved meaning for an epistemic maturity sentinel and blur the axis
  ADR-0008 deliberately separated. Omission already carries the meaning precisely.
- **Adding a separate stage-level planning construct** for planned capabilities. It
  would create a second representation of capability state alongside the capability
  record — two sources of truth for one fact, which ADR-0008's migration principles
  reject.
- **Binding `api_version` to the documentation-set version.** It contradicts the
  published Site Design precedent (doc set `v1`, route `v1alpha`) and would record
  a version that no request ever uses.
- **Amending ADR-0008 instead of writing a new ADR.** ADR-0008 decides the
  governance unit and target structure; this decides when fields inside that
  structure are required. Different questions, and ADR-0008 stays historical.

## Follow-up

None of the following is authorised by this ADR:

1. **Re-evaluate the schema-v2 migration design pass** against these cardinality
   rules, confirming all eight stages round-trip losslessly.
2. **The schema-v2 contract migration** — atomic, `schema_version: 1` → `2`, under
   ADR-0008's migration principles, adding no RFI capability.
3. **Confirm the remaining capability-id naming choices**, including
   `document_management` versus `data_management`.
4. **Approve carrying the published Transmittals `api_version: v1`** into the
   migrated contract, since `api_maturity: ga` requires a version binding under
   rule 3.
5. **Separate evidence-backed lifecycle/version research** for Data Management,
   Model Coordination, Issues and Assets.
