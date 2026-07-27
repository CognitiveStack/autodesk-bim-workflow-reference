# ADR-0007: Classify read/write by observable state semantics, not HTTP verb

## Status

Accepted

## Date

2026-07-27

## Context

> **Numbering note.** This is **reference-repo ADR-0007**. The APS/Forma MCP
> component repository maintains its **own, independent** ADR series, which
> already contains a differently-scoped `ADR_007`. The two series are unrelated
> and are **not** a shared sequence. Cross-repository citations of this decision
> should name it *reference-repo ADR-0007*.

This project is **read-first and write-guarded**
([SYSTEM_ARCHITECTURE.md](../architecture/SYSTEM_ARCHITECTURE.md);
`writes_require_explicit_approval: true` in project configuration). Every Autodesk
capability adopted so far has been a read, and the APS/Forma MCP's adopted read
clients — Data Management, Model Derivative, Issues, Reviews, Relationships, Model
Coordination and Transmittals — all issue **only** HTTP `GET`.

That uniformity was a **property of the modules selected**, not a definition. The
normative rules the repository actually states are narrower and different: request
paths are **internally constructed**, and **no arbitrary URL or HTTP method is
exposed** ([COMPONENT_BOUNDARIES.md](../architecture/COMPONENT_BOUNDARIES.md)
§3.1); each phase additionally excludes **arbitrary HTTP requests** by name
([PHASE_2_CAPABILITY_GAP.md](../architecture/PHASE_2_CAPABILITY_GAP.md) §8.5,
[PHASE_3_CAPABILITY_GAP.md](../architecture/PHASE_3_CAPABILITY_GAP.md) §8). No
document defines *read* as *GET*.

[ADR-0004](0004-adopt-transmittals-as-first-phase-4a-read-slice.md) recorded this
distinction explicitly and **deferred** the question, noting that "**no
POST-as-read policy decision is needed** for the first slice; all five operations
are `GET`, so the component's existing GET-only read **posture** is preserved."
The word was *posture*, and the deferral was deliberate: Transmittals simply did
not raise the question.

RFIs do. The Autodesk Forma RFIs API v3 research
([PHASE_4_CAPABILITY_GAP.md](../architecture/PHASE_4_CAPABILITY_GAP.md) §5, §11.1)
established, against normative Autodesk Reference Guide documentation:

- **there is no `GET` RFI collection endpoint** in the v3 release;
- **collection discovery is performed by `POST search:rfis`**, which is the only
  way to obtain an `rfiId`;
- Autodesk **documents that operation as retrieval** — "Retrieves information
  about all the RFIs (Requests for Information) in a project";
- **its required OAuth scope is `data:read`**, whereas every RFI mutation
  endpoint requires `data:write` or `data:write data:create`;
- **it mutates no RFI state**, returning `results[]` and a `pagination` object.

An RFI read slice therefore cannot be built at all unless the deferred
transport-versus-semantics question is resolved first. That resolution is an
architecture decision, not an implementation detail, and it is owed before any
RFI implementation increment begins.

**This context establishes nothing about POST endpoints in general.** It
establishes one thing about one documented operation. Search-shaped naming, the
`resource:verb` path convention, and superficial similarity to other modules'
operations are **not** evidence of read semantics — the Relationships API's
`relationships:search` is served over `GET`, and Submittals'
`items:validate-custom-identifier` and the Sheets `:batch-get` operations remain
unclassified and unapproved.

## Decision

**Read/write classification is determined by observable Autodesk domain-state
semantics, supported by the API's documented operation semantics and its required
OAuth scope — not by HTTP verb alone.**

### The read classification test

An operation may be classified **read** only when **all five** conditions hold:

1. **No observable Autodesk domain-state mutation.** The operation creates,
   modifies, deletes or transitions no Autodesk project, module or application
   state, and leaves nothing behind that another caller could observe.
2. **Documented retrieval semantics.** Autodesk's own documentation describes it
   as retrieval, search, query, or an equivalent.
3. **Read-only Autodesk OAuth scope.** The scope Autodesk requires for the
   operation is a read scope.
4. **Explicit endpoint-level approval.** The exact endpoint is approved by name in
   repository governance before implementation.
5. **No arbitrary request capability.** The implementation exposes no
   caller-supplied URL, path, HTTP method, or generic request helper.

Conditions 1–3 are properties of the Autodesk API and are established from
normative first-party documentation. Conditions 4–5 are obligations on this
project. **A failure of any one condition disqualifies the operation.**

Condition 3 carries particular weight because it is **Autodesk's own
classification**, externally verifiable and not open to reinterpretation by this
project. Where the required scope is a write scope, the operation is a write here,
whatever its name or shape suggests.

### GET remains the default read transport

**HTTP `GET` is the normal and expected transport for reads, but `GET` is not the
definition of read.** Existing GET-only clients remain GET-only, and a GET
operation is not automatically a read either — it must still satisfy the test
above.

**`POST` is not presumed read-safe.** There is no general rule that search-shaped,
idempotent, or `:verb`-suffixed POST operations are reads. **Every non-GET
semantic read requires its own explicit endpoint-level governance approval before
implementation**, recorded as an amendment to this ADR or in a successor decision.
Approval of one endpoint extends to no other endpoint, no other module, and no
other API version.

### Approved endpoint

Exactly one endpoint is approved as read-semantic by this ADR:

```
POST https://developer.api.autodesk.com/construction/rfis/v3/projects/:projectId/search:rfis
```

Verified against the normative Autodesk Reference Guide for the RFIs API v3. It
qualifies because:

- **it is a retrieval/search operation** — Autodesk documents it as retrieving the
  RFIs in a project;
- **its required OAuth scope is `data:read`**;
- **it mutates no Autodesk state** — no RFI, response, comment or attachment is
  created, modified or transitioned;
- **it returns RFI results and pagination** (`results[]`, `pagination`);
- **it is necessary** — no `GET` RFI collection endpoint exists, so the RFI read
  slice is unreachable without it.

This approval is **endpoint-specific and version-specific**. It does not extend to
any other RFI endpoint, and specifically not to `POST rfis`, `PATCH rfis/:rfiId`,
`POST rfis/:rfiId/responses`, `PATCH rfis/:rfiId/responses/:responseId` or
`POST rfis/:rfiId/comments`, all of which require write scopes and remain writes.

## Constraints

These apply to any implementation of a read-semantic non-GET operation. They
restate and extend the existing component boundary rules; none is relaxed.

- **No caller-supplied URLs.**
- **No caller-supplied paths**, path fragments, or path templates.
- **No caller-supplied HTTP methods.**
- **No generic or arbitrary request helpers**, and no reuse of an existing
  general-purpose write transport.
- **Endpoint-specific transport only** — a helper that can reach exactly one
  approved endpoint, not a reusable "read-semantic POST" abstraction.
- **Schema-controlled request bodies** — the body is assembled internally from
  validated, typed arguments; no caller-supplied request object is forwarded.
- **Mutation endpoints remain outside the read boundary regardless of HTTP verb**,
  and must be unreachable from a read client.
- **A read-semantic POST implementation must not become a substrate for write
  endpoints.** It confers no capability to add writes later without a separate,
  explicit write decision.

This ADR defines the architectural contract only. Concrete module layout, function
signatures and test names belong to the implementing increment in the component
repository ([ADR-0002](0002-multi-repo-no-submodules.md)).

## Consequences

- **Transmittals and every existing GET-only client are unchanged.** No adopted
  read client gains a POST path, and the Transmittals first slice remains the five
  `GET` operations fixed by ADR-0004.
- **No existing GET client is weakened.** This decision adds a definition and an
  allowlist; it removes no constraint.
- **A future RFI client may issue the single approved POST search operation while
  remaining classified `read`**, provided it satisfies the constraints above.
- **Future non-GET read operations require separate explicit endpoint-level
  approval.** Submittals' `items:validate-custom-identifier` and the Sheets
  `:batch-get` operations are **not** approved by this ADR and must be classified
  individually if and when those modules are adopted.
- **Implementation tests must enforce endpoint specificity, not merely ban
  `httpx.post`.** For an approved non-GET read, the component must provide
  structural evidence that POST transport can reach **only** the explicitly
  approved endpoint, and that mutation endpoints remain **unreachable**. The
  component's existing boundary proof rests on the absence of mutation verbs, so
  it cannot simply be reused for a client holding an approved POST — **nor may it
  simply be removed**, which would leave the boundary unenforced. The concrete
  test mechanism belongs to the component implementation.
- **The read/write class becomes a semantic classification that must be recorded
  deliberately**, rather than inferred from a verb column.
- **This decision resolves the POST-as-read deferral** recorded in ADR-0004 and in
  [PHASE_4_CAPABILITY_GAP.md](../architecture/PHASE_4_CAPABILITY_GAP.md) §5.
- **This ADR authorises no implementation**, no Autodesk API call, no MCP tool, and
  no write operation.

## Non-goals

ADR-0007 does **not** resolve, and must not be cited as resolving:

- **RFI `api_maturity` granularity** — whether stage-level maturity remains
  sufficient once a second API family joins `construction_information`;
- **RFI API-family naming** — the official name to assert under
  [ADR-0003](0003-autodesk-platform-product-and-api-terminology.md);
- **RFI privacy and sanitisation** — no alias family is approved, and
  [SANITISATION_CONVENTION.md](../guides/SANITISATION_CONVENTION.md) is unchanged;
- **acting-identity evidence semantics** — how a user-context-scoped read is
  represented in evidence;
- **approved training-project data readiness** for RFIs;
- **RFI implementation** — no RFI client, tool, fixture or evidence is authorised;
- **Gate 5, Gate 6 or Gate 8** for RFIs or any other module — no gate is closed by
  this ADR;
- **Submittals or Sheets adoption**, and no endpoint of either module.

## Interaction with existing ADRs

- **[ADR-0004](0004-adopt-transmittals-as-first-phase-4a-read-slice.md)** — this
  ADR **resolves the POST-as-read question ADR-0004 deferred**. It does **not**
  amend or supersede ADR-0004, which remains Accepted; the Transmittals slice
  stays fixed at five `GET` operations with no write in scope.
- **[ADR-0001](0001-orchestration-layer-not-mcp-server.md)** — unchanged. The
  transport rules bind the owning component; this repository implements nothing.
- **[ADR-0002](0002-multi-repo-no-submodules.md)** — unchanged. Any implementation
  lands in the component repository.
- **[ADR-0003](0003-autodesk-platform-product-and-api-terminology.md)** —
  unchanged. No API family is named or asserted here.
- **[ADR-0005](0005-approve-transmittals-sanitisation-profile.md)** and
  **[ADR-0006](0006-approve-cross-surface-transmittals-evidence-semantics.md)** —
  unaffected. This ADR governs transport classification, not evidence semantics or
  sanitisation.

## Rejected alternatives

- **Declaring "read = GET" normative.** It would be simple to enforce, but it is
  not what the repository actually says, and it would make the RFI module
  permanently unreachable for reasons unrelated to what the operation does. It
  would also misclassify a `data:read` retrieval as a write.
- **Declaring POST search operations generally read-safe.** This would convert a
  narrow, evidenced decision into a broad presumption, and would pre-approve
  endpoints — in Submittals, Sheets, and future modules — that have not been
  examined. Endpoint-level approval is the whole safeguard.
- **Classifying by endpoint name or `:verb` suffix.** Names are evidence, not
  proof. `relationships:search` is a `GET`, and a name cannot establish that an
  operation leaves no state behind.
- **Classifying by idempotence alone.** A repeatable operation can still mutate
  state, and repeat-safety is a useful property rather than a sufficient test.
- **Adding a generic read-semantic POST helper for future reuse.** It would create
  exactly the general POST capability condition 5 exists to prevent; a second
  approved endpoint should get a second endpoint-specific path.
- **Amending ADR-0004 instead of writing a new ADR.** ADR-0004 is a dated selection
  decision that explicitly scoped its own deferral. Rewriting it would erase the
  deferral rather than answer it, and the principle decided here is reusable beyond
  Transmittals and beyond RFIs.

## Follow-up

None of the following is authorised by this ADR:

1. **Implement an RFI client or `search_rfis` MCP tool** in the component
   repository, with the endpoint-specificity tests described under Consequences.
2. **Decide the `api_maturity` granularity question** before
   `construction_information` gains a second API family.
3. **Decide the RFI API-family name** under ADR-0003.
4. **Approve an RFI privacy and sanitisation profile** (Gate 5).
5. **Take the RFI component-boundary and roadmap decision** (Gate 6).
6. **Establish RFI data readiness** in the approved training project (Gate 8).
