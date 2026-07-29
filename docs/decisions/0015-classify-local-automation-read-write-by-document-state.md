# ADR-0015: Classify local-automation read/write by observable document state

## Status

Accepted

## Date

2026-07-29

## Context

> **Numbering note.** This is **reference-repo ADR-0015**. The APS/Forma MCP and
> Revit MCP component repositories maintain their **own, independent** ADR series.
> The three are unrelated and are **not** a shared sequence. Cross-repository
> citations should name this decision *reference-repo ADR-0015*.

[ADR-0007](0007-read-write-classification-by-state-semantics.md) established that
**read/write classification is determined by observable Autodesk domain-state
semantics, not by HTTP verb alone**, and defined a five-condition read test. That
framing was correct and remains correct. But the test was written against, and
validated on, **Autodesk cloud APIs reached over HTTP with OAuth**, because every
capability adopted at the time — Data Management, Model Derivative, Issues,
Reviews, Relationships, Model Coordination, Transmittals, and later RFIs and
Submittals — was exactly that.

The Revit MCP inspection (2026-07-29, `revit-mcp-triviron` at committed revision
`ae01d292735549ac406e5e7101620e64a5477970`) supplied the first governed capability
set that is **not** cloud-shaped, and it does not fit two of ADR-0007's five
conditions:

- **Condition 2 — documented retrieval semantics.** ADR-0007 requires that
  "Autodesk's own documentation describes it as retrieval". The Revit MCP route
  handlers are defined **in the component repository itself**, shipped as a pyRevit
  extension. There is no vendor operation to appeal to.
- **Condition 3 — read-only Autodesk OAuth scope.** ADR-0007 states that this
  condition "carries particular weight because it is **Autodesk's own
  classification**, externally verifiable and not open to reinterpretation by this
  project". The inspected component implements **no authentication of any kind** —
  no token, no scope, no consent step. The condition cannot be satisfied, cannot be
  failed, and the gate model contains **no waiver mechanism**.

Conditions **1**, **4** and **5** transfer intact, and condition 1 — no observable
domain-state mutation — classifies every inspected Revit operation cleanly.

The gap is not theoretical. It is already producing a live inconsistency:

- **`list_category_parameters`** is a **`POST`** route
  (`revit_mcp/colors.py`) that performs a pure element-collector read, opens **no
  transaction**, and mutates nothing. `COMPONENT_BOUNDARIES.md` §4 classifies it
  `read`, while §2 of that same document permits a non-`GET` read **only** through
  explicit ADR-0007 endpoint-level approval — approval that cannot exist for it
  under conditions 2 and 3. The published ledger therefore contradicts its own rule.
- Conversely **`place_family`**, **`color_splash`**, **`clear_colors`** and
  **`execute_revit_code`** are also `POST` routes, and all four **commit Revit
  transactions**. The transport verb distinguishes none of them from each other or
  from the read above.

The inspection also established the fact that makes a local branch tractable:
**the Revit transaction is an external, platform-enforced classifier.** A handler
that never calls `Transaction.Start()`, or that only ever rolls back, cannot leave
persistent document state. That is checkable in the component's source and is not
open to reinterpretation by this project — it is the local-automation equivalent of
what the OAuth scope provides in the cloud branch.

**Nothing in ADR-0007 is wrong.** Its scope was narrower than its generic-sounding
title suggested, and this decision states the boundary explicitly rather than
stretching one rule over two substrates.

## Decision

**Read/write classification has one common principle and two substrate-specific
branches. ADR-0007 governs the Autodesk cloud branch unchanged; this ADR adds the
local-automation branch.**

### 1. The common principle

**An operation may be classified `read` only if it leaves no persistent
domain-state mutation that another caller could observe after the operation
completes.**

**The transport verb is never the classifier.** `GET` is not proof of a read and
`POST` is not proof of a write, on any substrate.

This principle is substrate-independent. It restates ADR-0007's condition 1 and
promotes it to the shared root of both branches.

### 2. Common project obligations

These apply on **every** substrate and are carried forward from ADR-0007
conditions 4 and 5, unweakened:

- **Explicit named approval before implementation.** The exact operation is
  approved by name in repository governance before a capability using it enters a
  governed workflow.
- **No arbitrary request or execution capability.** No caller-supplied URL, path,
  HTTP method, generic request helper, or — added here — caller-supplied executable
  code, may be introduced into a governed read surface.

### 3. Autodesk cloud branch — ADR-0007, unchanged

**[ADR-0007](0007-read-write-classification-by-state-semantics.md) remains
authoritative and fully in force for every Autodesk cloud API**, including its
vendor-documentation condition, its OAuth read-scope condition, its
endpoint-specific and version-specific approval rule, and its constraints on
read-semantic non-`GET` transport.

**This ADR modifies, weakens, supersedes and relaxes nothing in ADR-0007.** No
existing classification changes. The single endpoint ADR-0007 approves
(`POST …/rfis/v3/projects/:projectId/search:rfis`) is untouched, and its approval
continues to extend to no other endpoint, module or API version.

**The local branch below must never be cited for a cloud operation.** An Autodesk
cloud API that lacks a documented read scope is not rescued by the absence of a
transaction; it remains unclassified under ADR-0007.

### 4. Local Revit automation branch

For capabilities whose implementation executes **inside a local Revit process**
through pyRevit, classification is established from **observable local document
state**, using the Revit transaction as the enforced boundary.

Three classes are defined. **No further taxonomy is created.**

#### 4a. Document read

An operation is a **document read** when it **commits no Revit transaction** and
leaves **no persistent BIM or document state** that another caller could observe.

**A `POST` transport route may therefore still be a read.** The pyRevit Routes
bridge is a local integration transport; its verbs carry no domain meaning.

This is the basis on which **`list_category_parameters` is classified `read`**,
notwithstanding its `POST` route. It opens no transaction and returns parameter
metadata gathered by an element collector.

#### 4b. Document write

An operation is a **document write** when it **commits a Revit transaction**, or
otherwise leaves persistent Revit document or view state.

Classified `write` on this basis:

| Operation | Basis |
|---|---|
| `place_family` | Commits a transaction creating a family instance |
| `color_splash` | Commits a transaction setting element graphic overrides on views |
| `clear_colors` | Commits a transaction removing element graphic overrides |
| `execute_revit_code` | Commits a transaction wrapping caller-supplied code |

**Persistent view state is a document write.** `color_splash` and `clear_colors`
change presentation rather than model geometry, but the change is transacted,
undoable, savable and observable by another caller. **A presentation-only mutation
is not a read**, and this ADR creates no intermediate class for it. Where the
distinction between presentation state and model geometry matters, it is recorded
in prose on the capability record — **not as a new schema field**.

**Arbitrary code execution is classified by capability, not by intent.**
`execute_revit_code` accepts caller-supplied IronPython and executes it inside
Revit with the document and the Revit DB namespace in scope. **Because it *can*
mutate the document, the MCP capability is governed as `write` and as
`unbounded`** — irrespective of what any individual invocation claims to do, and
irrespective of whether a particular script would in fact mutate anything. A
narrower classification would require a future mechanism that provably prevents
mutation; **no such mechanism exists in the inspected component**, and none is
designed here.

#### 4c. Transient external side effect

An operation may create **bounded temporary state outside the document** and still
be classified a **document read**, provided that state is removed before the
operation completes and no persistent domain mutation remains.

The concrete current example is **`get_revit_view`**, which exports a PNG to a
temporary directory, encodes it, and **deletes the file** within the same call. It
opens no transaction and modifies no document.

This clause exists to classify one observed behaviour honestly. It is **not** a
general side-effect framework, and it does not license unbounded, retained or
undisclosed external writes. An external side effect that is **not** removed, or
whose removal is not established, falls outside this clause and must be classified
separately before use.

### 5. Governance obligations are unchanged

The project-level requirement of **explicit approval before a mutating capability
enters a governed workflow** is preserved in full.

**This ADR asserts no enforcement by `revit-mcp`.** The inspected component
implements **no confirmation step, no approval mechanism, no dry-run, no read-only
mode and no authentication**. Its four write tools are directly callable. The only
control in force today is **reference-workflow discipline in this repository** —
the explicit never-invoke list in
[PHASE_1_EXECUTION_PLAN.md](../workflows/PHASE_1_EXECUTION_PLAN.md) §2 — and that
control must be described at the layer where it actually exists.

**Classifying an operation `write` under this ADR authorises nothing.** It records
what the operation does.

## Constraints

- **This ADR changes no data, no schema and no capability vocabulary.** No
  `read`/`write` value, `api_maturity` value, `mcp_implementation_status` value or
  `data_readiness` value is added or altered.
- **No Revit write is authorised**, and no governed workflow gains a mutating Revit
  step.
- **No component change is authorised** in `revit-mcp-triviron` or in the APS/Forma
  MCP, and none was made.
- **No live Revit verification is performed or claimed.** Every classification here
  rests on **static inspection of the committed component source** at
  `ae01d292735549ac406e5e7101620e64a5477970`.
- **The transaction test is evidence of the component's construction**, not of
  runtime behaviour. A future component change could invalidate a classification,
  which is why classifications are pinned to an inspected revision.
- **`execute_revit_code` remains excluded** from every governed read workflow.

## Consequences

- **The `list_category_parameters` contradiction is resolved** on a stated rule
  rather than by exception: it is a read because it commits no transaction.
- **Verb-based reasoning is closed off on both substrates.** The one framing that
  survived contact with a non-cloud component is the state-semantics framing, and
  it is now the shared root rather than a cloud-specific rule.
- **A local operation gains an external classifier.** The Revit transaction plays
  the role the OAuth scope plays in the cloud branch: platform-enforced, verifiable
  outside this project's opinion.
- **The cloud branch is protected.** A local rule cannot be borrowed to classify an
  Autodesk cloud operation whose scope is undocumented.
- **The unguarded state of the Revit write surface is now recorded in governance**
  rather than implied by a component-boundary table.
- **Classification is revision-pinned**, so a component change is a re-verification
  trigger rather than a silent drift.

## Non-goals

This ADR does **not** resolve, and must not be cited as resolving:

- **any change to ADR-0007** — it is neither amended nor superseded;
- **authorisation of any Revit write**, or of `execute_revit_code` in any workflow;
- **a guard, approval or authentication mechanism** for `revit-mcp` — that remains
  a component concern and is deferred;
- **a general side-effect taxonomy** beyond the single transient class in §4c;
- **live Revit verification** of any capability;
- **a Revit evidence schema or artifact** — none is created or implied;
- **Revit sanitisation domains** for element, room, coordinate or client values;
- **the run-discipline abstraction**, which remains deliberately specialised;
- **any classification for a substrate other than Autodesk cloud APIs and local
  Revit/pyRevit automation.** A third substrate would need its own branch.

## Interaction with existing ADRs

- **[ADR-0007](0007-read-write-classification-by-state-semantics.md)** — **remains
  Accepted and unchanged.** This ADR **extends** its architecture by naming the
  common principle it already contained and adding a second substrate branch
  beneath it. ADR-0007 stays authoritative for every Autodesk cloud API. **Not
  amended, not superseded.**
- **[ADR-0008](0008-govern-implementation-state-per-capability.md)** — the
  capability remains the unit of implementation governance. Read/write class is a
  property of an operation and is **not** a capability-record field; grouping
  operations of one class into one capability is a governance choice, not a schema
  one. **Not amended.**
- **[ADR-0009](0009-define-capability-record-cardinality-for-schema-v2.md)** — its
  conditional-cardinality rules are what allow a Revit capability to omit
  `api_version` truthfully. **Not amended.**
- **[ADR-0003](0003-autodesk-platform-product-and-api-terminology.md)** — governs
  the decision to retain `Autodesk Revit API` as the API family and to represent
  the pyRevit Routes bridge at the component boundary instead. **Not amended.**
- **[ADR-0001](0001-orchestration-layer-not-mcp-server.md)** and
  **[ADR-0002](0002-multi-repo-no-submodules.md)** — unaffected; no component
  source is copied, vendored or modified.

**This ADR supersedes nothing.**

## Rejected alternatives

- **Amend ADR-0007 to relax conditions 2 and 3.** It would weaken the cloud branch
  — where those conditions are load-bearing and externally verifiable — in order to
  accommodate a substrate they were never written for. The cloud rule is not the
  problem.
- **Treat the OAuth-scope condition as "not applicable" for Revit.** The gate model
  has no waiver, and a condition that silently evaporates is not a condition. A
  named branch with its own external classifier is honest; an exemption is not.
- **Classify by HTTP verb on the local bridge.** Directly falsified: a `POST` read
  and four `POST` writes sit side by side in the inspected component.
- **Introduce a third class for presentation-only mutation** (view overrides). The
  change is transacted, persistent and observable by another caller, so it is a
  write on the common principle. A middle class would invite treating it as
  "nearly read" and would be the first crack in the principle.
- **Classify `execute_revit_code` per invocation from its stated intent.** Intent
  is caller-supplied text, not evidence. The capability is what is governed.
- **Build a general external-side-effect framework.** One observed behaviour does
  not justify a taxonomy; §4c classifies what exists and nothing more.
- **Defer until live Revit verification.** The contradiction in the published
  ledger is live now, and static source inspection establishes the transaction
  facts without a running Revit. Live verification can confirm; it is not needed to
  decide.
- **Record read/write class as a capability-record field.** It is a property of an
  operation, and ADR-0008 deliberately keeps the record small. The component
  boundary already carries the per-tool class.

## Follow-up

None of the following is authorised by this ADR:

1. **A guard, approval or authentication mechanism** in `revit-mcp-triviron`.
2. **Live Revit verification** of any classified capability.
3. **A Revit evidence schema or artifact**, and the Revit sanitisation domains that
   publishing one would require.
4. **A tool-manifest or offline verification mechanism** for the Revit MCP,
   equivalent to the APS/Forma MCP's offline doctor.
5. **Re-verification of these classifications** against a future Revit MCP
   revision, should the component's transaction usage change.
