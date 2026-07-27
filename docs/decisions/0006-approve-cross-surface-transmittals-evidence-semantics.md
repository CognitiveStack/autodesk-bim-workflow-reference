# ADR-0006: Approve cross-surface Transmittals and Data Management evidence semantics

## Status

Accepted

## Date

2026-07-27

## Context

[ADR-0005](0005-approve-transmittals-sanitisation-profile.md) approved the
Transmittals public-evidence profile on 2026-07-25, when **no live Autodesk call
had been made against any Phase 4A module** and no Transmittals MCP tool existed.
On the evidence then available, the profile was deliberately conservative about
one thing in particular: the Transmittals response surface returns a
version-qualified document URN but **no separate lineage field**, so obtaining a
stable document lineage from it would have required client-side string
manipulation. ADR-0005 therefore recorded stable lineage as `not_proven`, declined
a `LINEAGE_n` alias, and excluded `DOCUMENT_n` from the profile so that a
lineage-domain alias could not imply lineage evidence the API had not returned.

That reasoning was correct and remains correct **for the Transmittals surface**.

Since then the Transmittals first slice has been implemented and live-verified
(2026-07-27), and Gate 8 is closed for that slice under the operative §14 criteria
of [PHASE_4_CAPABILITY_GAP.md](../architecture/PHASE_4_CAPABILITY_GAP.md), with
readiness established in the approved training project. **Phase 4A as a whole is
not complete.** The live run produced something ADR-0005 could not have assumed: a
first-party **Data Management** read that returns an item resource identity
directly, alongside the Transmittals reads. ADR-0005 anticipated exactly this
possibility, reserving lineage approval for the case where "a future first-party
source returns and verifies a distinct lineage field."

The question this ADR answers is therefore narrow and specific:

> How may sanitised public evidence describe relationships between Autodesk
> Transmittals and Autodesk Data Management when the two surfaces expose
> **different identity semantics**?

This is a policy decision about what sanitised evidence may claim. It is **not**
the evidence artifact, and it creates none.

## New first-party evidence

The controlled live verification established the following at a policy-relevant
level. Each is a property of an API surface, not of any particular tenant.

- **Transmittals returns the issued version identity.** The Transmittals documents
  read exposes the immutable version identity of each included document as it
  existed when the transmittal was issued — sufficient to identify *what was
  transmitted*. Public alias: `VERSION_n`.
- **Data Management returns an item resource identity directly.** The item
  resource **is** the stable document/item lineage identity in the Data Management
  model, and it is returned as a field by a first-party read. Public alias:
  `ITEM_n`.
- **Data Management returns immutable version identities for that item.** Public
  alias: `VERSION_n`.
- **The two surfaces can be compared directly.** A Transmittals-issued version
  identity and the corresponding Data Management version identity are comparable
  by **exact byte-for-byte string equality**, with no URN splitting, no lineage
  derivation, no reconstruction, no canonicalisation and no string surgery of any
  kind. The component's Data Management output boundary retains chaining
  identifiers byte-identically for precisely this reason
  ([COMPONENT_BOUNDARIES.md](../architecture/COMPONENT_BOUNDARIES.md) §3.4).
- **Data Management independently identifies the current tip version** for an
  item, so public evidence can distinguish an **issued version** from the **current
  source tip** using aliases alone.

## Decision

Approve a **cross-surface evidence rule** for Phase 4A Transmittals evidence. In
summary:

1. Lineage semantics become **surface-scoped**: unchanged and unproven on the
   Transmittals surface, separately provable on the Data Management surface.
2. `ITEM_n` is approved as the public alias for the directly returned Data
   Management item/lineage resource in cross-surface evidence.
3. Exact byte-for-byte cross-surface version equality may be recorded as a proof
   outcome, without publishing the operands.
4. `DOCUMENT_n` remains excluded from this profile; `LINEAGE_n` remains
   unnecessary and unapproved.
5. Raw version URNs and raw numeric version values remain prohibited.
6. A scoped exact-version snapshot conclusion may be stated for a controlled
   fixture.
7. Evidence-provenance classifications are approved so an artifact can record
   *why* an alias is trusted without revealing its raw value.

**This ADR expands what sanitised aliases may be used to claim. It does not
weaken the privacy boundary in any respect.**

### Surface-scoped lineage semantics

This is the central decision, and the public model is **deliberately asymmetric**.

**Transmittals surface — unchanged.** Stable document lineage remains
**`not_proven`**. The Transmittals response alone does not establish a stable
source-document lineage identity, and nothing in this ADR converts the
Transmittals surface into a lineage source. Splitting or parsing a
version-qualified URN remains a client-side derivation and remains prohibited as
returned evidence.

**Data Management surface — newly permitted.** Data Management item lineage is
**proven** when `ITEM_n` is returned **directly** by the first-party Data
Management resource. `ITEM_n` may represent that item resource, and therefore the
stable lineage identity, only when obtained that way.

**Cross-surface relationship — newly permitted.** A version relationship between
the two surfaces is **proven** when a `VERSION_n` returned by Transmittals compares
**byte-for-byte equal** to a `VERSION_n` returned by Data Management.

Public evidence must keep the two surfaces distinguishable, so that a reader can
tell which surface established which claim. This follows the existing practice of
labelling how a match was obtained rather than flattening it — the same discipline
that keeps `typed_issue_field` and `viewer_state_derived` separate in Phase 3
evidence ([SANITISATION_CONVENTION.md](../guides/SANITISATION_CONVENTION.md),
evidence-wording rules).

### Approved public alias model

For Phase 4A cross-surface Transmittals evidence:

| Alias | Represents |
|---|---|
| `PROJECT_n` | the Autodesk project |
| `TRANSMITTAL_n` | the Transmittals record |
| `FOLDER_n` | a returned Data Management folder resource, where relevant |
| `ITEM_n` | the **Data Management item resource**, which carries the stable item/lineage identity |
| `VERSION_n` | an **immutable** exact document-version identity |

`ITEM_n` is not a new family: it is the existing Data Management alias already
defined in [SANITISATION_CONVENTION.md](../guides/SANITISATION_CONVENTION.md) and
already published in Phase 1 evidence. Reusing it keeps Phase 4A composed with
Phases 1–3 rather than running parallel to them.

This table is the **structural** subset needed for cross-surface evidence. It does
not withdraw any other alias approved by ADR-0005 — `USER_n`, `RECIPIENT_n`,
`EXTERNAL_MEMBER_n`, `COMPANY_n` and `ROLE_n` remain approved and remain governed
by their existing domain rules.

**`LINEAGE_n` is not introduced.** The Data Management item resource already *is*
the lineage-bearing resource. Minting `ITEM_n` and `LINEAGE_n` for one Autodesk
resource would create two public aliases for a single identity and falsely imply
two independently proven resources. `LINEAGE_n` is therefore recorded as
**unnecessary**, not merely unapproved.

**Matching numeric suffixes still prove nothing.** `TRANSMITTAL_1`, `FOLDER_1`,
`ITEM_1` and `VERSION_1` sharing the suffix `_1` implies no identity,
correspondence or relationship. Only an explicitly recorded comparison result does.

### `DOCUMENT_n` remains excluded from this profile

The Transmittals documents endpoint's load-bearing identity for this proof is the
issued immutable `VERSION_n`. A public intermediate node adds a semantic step the
proof does not need and risks confusion with the document/item lineage semantics
`DOCUMENT_n` already carries elsewhere.

Preferred public relation:

```
TRANSMITTAL_1
└── VERSION_1
```

Not:

```
TRANSMITTAL_1
└── DOCUMENT_1
    └── VERSION_1
```

A controlled synthetic filename may still be published where the sanitisation
convention already permits it. **This decision is scoped to the Transmittals
public-evidence profile and does not change the meaning of `DOCUMENT_n` in any
other phase or profile.**

### Raw numeric versions remain prohibited

Public evidence must not publish Autodesk's numeric version property — no
`versionNumber = 1`, no `versionNumber = 2`. The alias relation `VERSION_1` /
`VERSION_2` is sufficient to express the structure.

Where completeness of a returned version set matters, it may be established
through structural metadata the profile already permits, such as a returned
`count` together with `has_more`. For example, `count = 2` with `has_more = false`
establishes that the returned set is complete **without** publishing the numeric
version property.

**This ADR does not relax the raw-version-number rule**, and raw version URNs
remain prohibited in every form — not hashed, not truncated, not partially masked.

### Minimum public proof model

The following conceptual model is approved as the minimum faithful public
representation:

```
TRANSMITTAL_1
└── VERSION_1

ITEM_1
├── VERSION_1
└── VERSION_2  ← current tip
```

Permitted public claims, when backed by private or live evidence:

1. **Transmittals `VERSION_1` == Data Management `VERSION_1`** — comparison:
   byte-for-byte exact string equality.
2. **Data Management current tip == `VERSION_2`.**
3. **`VERSION_1` != `VERSION_2`.**
4. **`ITEM_1` has exactly the returned version set**, where completeness is
   established through permitted structural metadata such as `count` and
   `has_more`.

**The operands are never published.** A public artifact records the comparison,
its method, and its result — not the values compared.

### Exact-version snapshot claim

Where the above conditions hold, a public artifact may state that, **for the
controlled fixture**, the completed Transmittal preserved the immutable issued
`VERSION_1` while the source Data Management `ITEM_1` later had `VERSION_2` as its
current tip. The evidence verdict **`exact_version_snapshot_proven`** is approved
for that controlled experiment.

The verdict applies to the **tested fixture and observed API behaviour**. It does
**not** mean that Gate 8 as a whole is "proven"; that Transmittals behaviour is
universally guaranteed across Autodesk tenants, regions or configurations; that
Phase 4A is complete; or that the Harrismith example project contains this fixture.

Preferred prose: *"Exact-version snapshot behaviour was proven for the controlled
training fixture."* Universal product guarantees must be avoided, consistent with
the existing rule that sanitising values must never upgrade the strength of a
claim.

### Proof reproducibility

Public evidence must distinguish a **historically established** proof from a
**re-derivable** one.

A sanitised public artifact may record a proof result even though the independent
raw operands are deliberately not published. The private evidence area may retain
enough identifiers to re-check some relationships. **The public artifact must not
recreate or duplicate raw identifiers merely to make historical equality proofs
re-runnable** — that would invert the privacy boundary for the sake of tidiness.

Three concepts are approved for recording this distinction:

- **historical attestation** — the result was established while the independent
  operands were simultaneously available, and is recorded as an outcome.
- **re-derivable from private evidence** — the frozen private identifier set still
  permits an independent re-check.
- **re-derivable from public evidence** — the published artifact alone permits a
  re-check. For alias-only artifacts this will normally be **no**, and saying so
  plainly is more honest than implying otherwise.

These are **concepts, not field names**. The Phase 4 result schema increment
chooses the concrete representation in the repository's established snake_case
style.

### Evidence-provenance classifications

An alias-only artifact sometimes needs to record *why* a retained alias is trusted
without revealing its raw value. Four classifications are approved for the Phase 4A
evidence workflow:

- **`ORIGINATING_RESULT`** — the retained raw value remains available from the
  original live result that established that alias.
- **`VALIDATED_RETAINED_INVOCATION`** — the original establishing result is no
  longer available, but the genuine previously-resolved value survives verbatim as
  an invocation parameter used in subsequent successful controlled live operations.
- **`EQUALITY_VERIFIED_LATER_RESULT`** — the original establishing result is no
  longer available, but the same resource identity was returned directly by a later
  first-party read, and had previously been established equal to the retained alias
  by exact comparison.
- **`VERIFIED_SURVIVING_VALUE`** — the freeze policy permitting the explicitly
  classified surviving sources above, rather than requiring every value to remain
  in its first-ever originating response.

**These classes describe evidence provenance only.** They do not change Autodesk
resource semantics, do not confer identity on anything, and do not permit
reconstruction, inference or string derivation of any value. An artifact using them
must still satisfy every rule in this ADR and in ADR-0005. Where a value's
provenance is weaker than `ORIGINATING_RESULT`, the artifact should say so rather
than presenting all values as uniformly sourced.

### Privacy boundary — unchanged

This ADR expands the semantic claims that may be made **from sanitised aliases**.
It changes nothing about what may be disclosed. Public evidence must continue to
exclude, in every form — not hashed, not truncated, not partially masked:

raw project identifiers · Transmittal identifiers · folder URNs · item/lineage
URNs · version URNs · personal names · recipient identities · email addresses ·
company identities · creator and modifier identities · behavioural timestamps ·
storage identifiers · derivative identifiers · authentication tokens · request
headers · raw API payloads.

The behavioural-telemetry rules, the synthetic-recipient requirement, the
two-artifact workflow, and the rejection of hashing and truncation as anonymisation
all remain exactly as ADR-0005 approved them. The alias ↔ real mapping remains
outside Git.

## Relationship to ADR-0005

[ADR-0005](0005-approve-transmittals-sanitisation-profile.md) **remains Accepted
and is not superseded.** This ADR **extends** it with a cross-surface rule that
became available only after new first-party Data Management evidence existed.
ADR-0005's conclusions were sound on the evidence available at the time, and its
core lineage judgement — that the Transmittals surface does not prove lineage —
is **carried forward unchanged**, not reversed.

**Unchanged by this ADR:**

- the Transmittals surface alone does not prove stable lineage;
- `DOCUMENT_n` remains excluded from the Transmittals profile;
- `LINEAGE_n` remains unapproved, and is now additionally recorded as unnecessary;
- raw version URNs remain prohibited;
- raw numeric versions remain prohibited;
- every identity, telemetry and privacy exclusion.

**Extended by this ADR:**

- `ITEM_n` may represent the directly returned Data Management item/lineage
  resource in cross-surface evidence;
- public evidence may combine a Transmittals `VERSION_n` with Data Management
  `ITEM_n` and `VERSION_n` relationships;
- exact byte-for-byte cross-surface version equality may be recorded as a proof
  outcome;
- the current Data Management tip may be represented through `VERSION_n`;
- exact-version snapshot behaviour may be stated for a controlled fixture when the
  approved conditions are met;
- evidence-provenance classifications and proof-reproducibility concepts are
  approved.

## Relationship to the Phase 4A state reconciliation

This ADR is consistent with, and does not reopen, the state recorded on
2026-07-27:

- the Transmittals first slice is **implemented and live-verified**;
- **Gate 8 is closed for the Transmittals first slice** under the operative §14
  criteria;
- **readiness was established in the approved training project**, and the
  Harrismith example project is not asserted to hold the fixture;
- **Phase 4A remains incomplete.**

Nothing here changes any gate status, and this ADR closes no gate.

## Deliberately not decided

- **Publication scenario and location.** Whether the eventual expected-result
  artifact belongs under
  [`examples/harrismith-fire-station/expected-results/`](../../examples/harrismith-fire-station/expected-results/)
  or a sibling training-lab scenario is **not decided here**. The live fixture was
  not asserted to be in the Harrismith example project, and the path choice is a
  separate decision to be taken before the artifact is written. **This ADR governs
  evidence semantics independently of that choice.**
- **The Phase 4 result schema.** Not created or modified by this ADR.
- **Any write operation**, and any gate for RFIs, Submittals, Sheets or Meetings.

## Consequences

- **Public Phase 4A evidence can state a substantive cross-surface proof** while
  remaining alias-only, because the claim is recorded as an outcome rather than as
  a pair of published operands.
- **The asymmetry must be maintained deliberately.** An artifact that records
  lineage as proven without naming the Data Management surface as its source would
  misrepresent the Transmittals surface, and would violate this ADR.
- **[SANITISATION_CONVENTION.md](../guides/SANITISATION_CONVENTION.md) must be
  amended** in a separate increment to carry these rules: the surface-scoped
  lineage split in place of a single unqualified `not_proven` record, `ITEM_n` in
  the Transmittals profile alias registry, and the provenance classifications. The
  convention's Transmittals checklist item on stable lineage will need to be
  re-expressed per surface. **No such amendment is made here.**
- **The next schema increment** must be able to represent, at minimum: the
  surface-scoped lineage classification; `ITEM_n` and `VERSION_n` relationships;
  a cross-surface equality outcome with its comparison method; the current-tip
  distinction; the completeness metadata; the proof-reproducibility distinction;
  and the provenance classifications. No fields beyond the decisions above are
  prescribed.
- **Phases 1–3 are unaffected.** No alias changes meaning outside the Phase 4A
  Transmittals profile.
- **This ADR authorises no implementation, no write operation, no Autodesk call,
  and no publication.**

## Rejected alternatives

- **Approving a `LINEAGE_n` alias.** It would create a second public alias for the
  Data Management item resource, implying two independently proven identities where
  one exists. The item resource is already the lineage-bearing resource.
- **Admitting `DOCUMENT_n` to this profile.** The proof does not need an
  intermediate node, and the alias already means *document lineage* in published
  Phase 2 evidence. Reusing it here would place a lineage-meaning alias between the
  transmittal and its version while the actual lineage node sits elsewhere.
- **Declaring lineage proven on the Transmittals surface** because Data Management
  proved it. Two surfaces, two claims; merging them would attribute to Transmittals
  an identity it never returned.
- **Publishing the numeric version property** because it is authoritative and
  low-risk for a synthetic fixture. The proof is complete without it, and relaxing
  an approved rule for presentational convenience is the wrong trade.
- **Publishing the raw operands so every equality is re-runnable from the public
  artifact.** This would defeat the sanitisation boundary to serve reproducibility;
  the honest alternative is to record that the public artifact is not
  self-re-derivable.
- **Treating the new evidence as automatically amending ADR-0005.** New evidence
  satisfies a policy's stated trigger; it does not enact the policy change. The
  amendment requires this explicit decision.
- **Declaring ADR-0005 mistaken.** Its reasoning was correct on the evidence then
  available, and its central lineage judgement is preserved here unchanged.

## Follow-up

None of the following is authorised by this ADR:

1. **Amend [SANITISATION_CONVENTION.md](../guides/SANITISATION_CONVENTION.md)** to
   carry the surface-scoped lineage rule, `ITEM_n`, and the provenance
   classifications.
2. **Decide the publication scenario and location** for the Phase 4A evidence
   artifact.
3. **Create `schemas/phase-4-result.schema.json`** encoding the approved concepts.
4. **Generate and validate the public evidence artifact** from the private capture,
   as a separate artifact, through the approved profile.
5. **Publish the sanitised artifact separately.**
