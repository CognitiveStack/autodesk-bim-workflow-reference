# ADR-0008: Govern implementation state per capability, not per workflow stage

## Status

Accepted

## Date

2026-07-27

## Context

> **Numbering note.** This is **reference-repo ADR-0008**. The APS/Forma MCP
> component repository maintains its **own, independent** ADR series. The two are
> unrelated and are **not** a shared sequence. Cross-repository citations should
> name this decision *reference-repo ADR-0008*.

`config/workflows/end-to-end-reference.yaml` (`schema_version: 1`) records eight
workflow stages. Each stage carries a **single scalar** for `primary_system`,
`mcp_component`, `mcp_implementation_status`, `api_maturity`, `data_readiness`
and `data_readiness_reason`, alongside a list of `api_families`.

That shape has never been exercised against the case it is about to meet.
**No stage currently holds more than one API family.** `construction_information`
would be the first: it carries the implemented Transmittals slice today, and RFIs
are the preferred second Phase 4A capability
([ADR-0004](0004-adopt-transmittals-as-first-phase-4a-read-slice.md)).

Adding a second capability to one stage breaks four stage-level scalars at once,
and a fifth already shows the strain:

- **`api_maturity`** — one scalar cannot express two independently versioned,
  independently released, independently deprecated API families. Transmittals and
  RFIs are both GA today; **that is a coincidence and must not be used to justify
  a shared value.** Either family's lifecycle can move without the other's.
- **`mcp_implementation_status`** — Transmittals is `confirmed` while RFIs would
  be `planned`. The vocabulary's `partial` records *that* a stage is split without
  recording *which* capability is which; it is a lossy encoding, not a
  representation.
- **`data_readiness`** — Transmittals is `ready` in the approved training project
  while RFI readiness is **not assessed**. The readiness vocabulary
  (`ready` / `blocked` / `not-assessed`) has no `partial`, so there is not even a
  lossy escape hatch. Retaining `ready` would assert readiness for a capability
  never assessed.
- **`primary_system`** — Transmittals belongs operationally to Forma Data
  Management; RFIs to Forma Build. **ADR-0004 already records that Phase 4A spans
  both**, so the documentation asserts two product surfaces while the
  configuration asserts one.
- **`data_readiness_reason`** — its current value is
  `transmittals-first-slice-ready-in-approved-training-project`. The repository has
  **already been forced to name a capability inside a stage-level field**. This is
  the clearest existing evidence that these facts are capability-scoped.

Two further observations shaped this decision:

- **Lifecycle evidence is version-bound in practice.** The Phase 4A research
  established Transmittals **v1** as GA and RFIs **v3** as GA, and recorded that
  RFIs **v2** was deprecated in 2022. One family therefore already carries two
  different lifecycle states across two versions, and a bare family-level
  assertion — "the RFIs API is GA" — is false for v2.
- **The contract has no machine consumers.** No schema, parser, test, script,
  example or generated artifact reads `api_maturity` or `api_families`; the field
  shape is enforced only by prose and convention. Migration cost is therefore
  documentation-shaped, and no compatibility shim is required.

**Nothing in the current configuration is false today.** With one capability per
stage every scalar is true. This decision is taken *before* adoption forces it,
not to repair a defect.

## Decision

**A workflow stage is the BIM workflow / teaching category. A capability inside
that stage is the unit of implementation governance.**

Independent capabilities within one stage may differ in owning product/system,
Autodesk API family, API version, API lifecycle/maturity, MCP component, MCP
implementation status, project data readiness, readiness reason, evidence and
live-verification state, and gate state. **These axes remain separate. They must
never be collapsed into a single generic capability status.**

### Target schema-v2 model

**Stage level** — workflow taxonomy and pedagogical posture only:

- `id`
- `platform`
- `automation_policy`
- `capabilities: [ … ]`

**Capability record** — one per governed capability within the stage:

- `id`
- `primary_system`
- `api_family`
- `api_version`
- `api_maturity`
- `mcp_component`
- `mcp_implementation_status`
- `data_readiness`
- `data_readiness_reason`

API lifecycle, implementation readiness and product-system ownership **must not be
made stage-wide by aggregation**. A stage does not have a maturity; its
capabilities do.

### Capability identity

- **`capability.id` is a stable, machine-oriented identifier.** It is the record's
  handle.
- **Human-readable Autodesk API-family terminology is a value inside the record,
  never the record key.** `api_family` is data.
- **Unresolved Autodesk branding or naming must not destabilise capability
  identity.** A capability can be identified, governed and reasoned about while its
  official API-family name remains unasserted under
  [ADR-0003](0003-autodesk-platform-product-and-api-terminology.md).
- **A capability is identified within its workflow stage**, not globally.

Illustrative ids such as `transmittals` or `rfis` are examples only. **This ADR
does not fix capability ids for existing stages**; the migration increment does.

### API version binding — adopted

**`api_version` is part of the capability record.** Lifecycle evidence is not
sufficiently precise without a version context. The architectural relationship is:

```
API family + API version → API maturity
```

Established evidence requiring this: Transmittals **v1** → GA; RFIs **v3** → GA;
historically RFIs **v2** → deprecated. A bare family-level maturity assertion is
insufficient, and becomes ambiguous the moment a future version ships alongside a
current one.

**No existing value is migrated by this ADR.**

### `api_maturity` — capability/API level

`api_maturity` records the **separately verified Autodesk lifecycle
classification** of the API family at the recorded version. It moves to the
capability record. Its existing vocabulary is unchanged by this decision.

### `to-be-verified` — meaning preserved

`to-be-verified` is **not an Autodesk lifecycle state**. It means **the repository
has not established the lifecycle classification for that API and version to the
required evidence standard.** That is an epistemic statement about this project's
evidence, not a statement about the API.

Evidence is established per family and version, never per stage, so the sentinel
belongs at capability/API level. Under the target model a single stage can contain:

```
capability A → api_maturity: ga
capability B → api_maturity: to-be-verified
```

without ambiguity. Under the current stage-level scalar that state is **not
representable at all**.

### `not-applicable` — defined

**`not-applicable` means the repository has identified the relevant
capability/API, but the Autodesk lifecycle classification represented by
`api_maturity` does not apply to that API context.**

It does **not** mean:

- no API exists;
- no capability exists;
- the API has not yet been researched (that is `to-be-verified`).

**A stage with no adopted capability is represented by `capabilities: []`**, not by
a stage-level `api_maturity` sentinel. Absence of a capability and inapplicability
of a lifecycle vocabulary are different facts and are represented differently.

### `mcp_implementation_status` — capability level

Whether **this project's** MCP tooling exists is a property of a capability, not a
stage. Transmittals may be `confirmed` while RFIs are `planned` inside
`construction_information`.

**Stage-level `partial` must not be used as a substitute for identifying which
capability is implemented.** `partial` remains a valid status for a *single
capability* whose own tool surface is partly implemented.

### `data_readiness` and `data_readiness_reason` — capability level

Whether the approved example or training project holds enough data is a property
of a capability. Transmittals may be `ready` while RFIs are `not-assessed` in the
same stage. `data_readiness_reason` sits beside the capability whose readiness it
explains — which is what the existing value
`transmittals-first-slice-ready-in-approved-training-project` has been expressing
inside a stage-level field all along.

### `primary_system` — capability level

Transmittals belongs operationally to **Forma Data Management**; RFIs to **Forma
Build**. One stage-level scalar cannot truthfully express both. Recording this
fact **does not resolve the RFI API-family name**, which remains governed by
ADR-0003.

### `mcp_component` — capability level

Both current Phase 4A capabilities would be `aps-forma-mcp`, but that is not
guaranteed for every future capability in every stage. Ownership is a
capability-level fact. **No implementation change is authorised by this.**

### Evidence, live verification and gates — separate axes, no new fields

Live-verification state, public-evidence state and gate state remain **separate
axes** from `api_maturity`, `mcp_implementation_status` and `data_readiness`, and
must not be folded into any of them.

**No YAML field is introduced for `live_verification_status`, `evidence_status` or
`gate_status`.** These remain governed by the existing evidence and gate
documents. Adding machine-readable fields requires a future demonstrated need.

## Constraints

- **This ADR changes no data.** `config/workflows/end-to-end-reference.yaml`
  remains `schema_version: 1` and remains **authoritative** until a separately
  reviewed migration commit lands.
- **DECISION ACCEPTED is not CONTRACT MIGRATED.** No document may describe
  capability records as the active contract while the configuration is schema v1.
- **`beta-v1alpha` is untouched in current data.** Its structural fate is settled
  below; its migrated values are not.
- **ADR-0008 does not introduce a stage-level `name` field.** Stages do not carry
  one under schema v1 — only the workflow object does — and the target stage-level
  set established here is exactly `id`, `platform`, `automation_policy` and
  `capabilities`. Adding a human-readable display name would be a **separate
  future contract decision** if a need is ever demonstrated.
- **No capability ids are fixed** for existing stages.
- **No RFI capability, API family, version or maturity is added** anywhere.
- **The RFI API-family name remains unresolved** under ADR-0003, and this decision
  is deliberately designed so that resolving it is not a prerequisite.

### `beta-v1alpha` — structural consequence recorded, values not chosen

The current token `beta-v1alpha` fuses two concepts:

```
lifecycle = beta   +   version = v1alpha
```

Under the target schema-v2 contract, **lifecycle and version are separate fields**.
The compound representation is therefore **not part of the target model**.

**It is not changed in this increment.** The token exists in two stages
(`site_and_context`, `concept_design`), both naming the Forma Site Design API, and
a **known Site Design lifecycle/documentation contradiction remains unresolved**
between the glossary and the configuration.

Decomposing `beta-v1alpha` requires choosing a lifecycle value and a version value
for Site Design. **This ADR establishes the structural rule and deliberately
asserts no Site Design factual result.** The migration must not silently choose
one.

## Consequences

- **The stage-versus-capability conflation is resolved as a matter of
  architecture**, ahead of the adoption that would have forced it.
- **A stage can truthfully hold capabilities at different lifecycles,
  implementation states, readiness states and product surfaces.**
- **`api_maturity` was the first symptom, not the disease.** Fixing it alone would
  have left `mcp_implementation_status`, `data_readiness` and `primary_system`
  broken and guaranteed a second breaking migration.
- **A second migration is avoided**: one atomic shape change instead of a
  maturity-only change followed by an implementation-state change.
- **Migration is documentation-shaped.** With no machine consumer, no
  compatibility shim, dual field, or transition period is needed — and none is
  permitted.
- **Schema-v2 migration is blocked** until the Site Design lifecycle/version
  contradiction is reconciled (see Follow-up).
- **This ADR authorises no migration, no configuration change, no RFI adoption, no
  implementation, and no Autodesk API call.**

### Future migration principles

When the migration increment is separately authorised, it must:

- be **atomic across all stages** — no partially migrated configuration;
- increment `schema_version` from **1 to 2**;
- replace the stage-level capability-specific fields with **one authoritative
  representation**;
- introduce **no parallel or legacy duplicate fields** — two sources of truth for
  one fact are rejected outright;
- require **no compatibility shim**, because no machine consumer exists;
- add **no RFI capability**;
- **preserve existing semantic facts**, except where separately reconciled
  beforehand.

## Non-goals

ADR-0008 does **not** resolve, and must not be cited as resolving:

- **the schema-v2 migration itself** — the configuration is unchanged and remains
  schema v1;
- **capability ids** for any existing stage;
- **the Site Design lifecycle/version contradiction**, or any migrated
  `beta-v1alpha` value;
- **the RFI API-family name** (ADR-0003);
- **RFI adoption or implementation** — no RFI capability is added, and no MCP tool
  is authorised;
- **machine-readable evidence, live-verification or gate fields**;
- **a repository-level API registry** (considered and deferred below);
- **Gate 5, Gate 6 or Gate 8** for RFIs or any other module — no gate is closed;
- **any change to `api_maturity`, `mcp_implementation_status` or `data_readiness`
  vocabularies**, beyond defining `not-applicable` and re-siting where the values
  live.

## Interaction with existing ADRs

- **[ADR-0003](0003-autodesk-platform-product-and-api-terminology.md)** — API-family
  terminology remains governed there. This ADR **does not resolve the RFI family
  name**, and deliberately makes `api_family` a value rather than a record key so
  that the unresolved name cannot destabilise capability identity. **Not amended.**
- **[ADR-0004](0004-adopt-transmittals-as-first-phase-4a-read-slice.md)** — recorded
  that `construction_information` spans Forma Data Management and Forma Build
  capabilities. This ADR gives the configuration a way to express what ADR-0004
  already asserted. **Not amended, not superseded.**
- **[ADR-0007](0007-read-write-classification-by-state-semantics.md)** — follows in
  sequence and listed this question as a Non-goal and Follow-up item. **Neither
  amended nor superseded**; the two decisions are independent.
- **[ADR-0001](0001-orchestration-layer-not-mcp-server.md)**,
  **[ADR-0002](0002-multi-repo-no-submodules.md)**,
  **[ADR-0005](0005-approve-transmittals-sanitisation-profile.md)**,
  **[ADR-0006](0006-approve-cross-surface-transmittals-evidence-semantics.md)** —
  unaffected.

**This ADR supersedes nothing.**

## Rejected alternatives

- **Keep the stage-level scalars.** Not representable once capabilities differ,
  and *accidentally* true while they happen to match — which is worse, because it
  looks correct while guaranteeing nothing.
- **Defer by not listing a second capability until it is implemented.** Every
  scalar would stay true, but the stage would silently under-report a governed
  capability and the problem would return unchanged at adoption. A workaround that
  hides state is not a model.
- **Move only `api_maturity` to per-family metadata.** Fixes one of four
  collisions, leaves `mcp_implementation_status`, `data_readiness` and
  `primary_system` broken, and guarantees a second breaking migration.
- **A parallel `api_maturity_by_family` map keyed by family name.** Creates two
  sources of truth for the family set, and makes the **human-readable API-family
  name a join key** — disqualifying while the RFI name is unresolved under
  ADR-0003, and fragile against any future Autodesk rename.
- **Structured `api_families` records carrying maturity.** Semantically correct for
  maturity alone, but leaves implementation status, readiness and `primary_system`
  stage-level, so it fails exactly the cases RFI adoption produces.
- **A repository-level API registry** normalising `family + version + maturity`
  outside capability records. It is the more normalised model and would remove the
  duplication that occurs where one API family appears in multiple stages.
  **Deferred, not rejected on merit**: the repository is small, there are zero
  machine consumers, capability records already solve the live multiplicity
  problem, and a registry introduces indirection and reference-key governance that
  is not currently needed. **Capability records do not prevent later
  normalisation** — a registry can absorb `api_family`, `api_version` and
  `api_maturity` out of the records if duplication ever becomes painful. **The
  target for schema v2 is capability records, not a central registry.**
- **Introducing machine-readable evidence and gate fields now.** No demonstrated
  need; the existing evidence and gate documents govern those axes.

## Follow-up

None of the following is authorised by this ADR:

1. **Site Design lifecycle/version reconciliation** — the **prerequisite** for
   migration. Schema-v2 migration **must not proceed** until it lands, because the
   migration introduces `api_version` and requires `beta-v1alpha` to be
   decomposed; it must not silently choose a new Site Design lifecycle fact.
2. **The schema-v2 contract migration** — atomic, `schema_version: 1` → `2`,
   under the migration principles above, adding no RFI capability.
3. **Update the schema-v1 field descriptions** in
   [SYSTEM_ARCHITECTURE.md](../architecture/SYSTEM_ARCHITECTURE.md) and
   [COMPONENT_BOUNDARIES.md](../architecture/COMPONENT_BOUNDARIES.md) **at
   migration time**, not before.
4. **Resolve the RFI API-family name** under ADR-0003.
5. **RFI adoption** — capability record, Gate 5, Gate 6 and Gate 8.
