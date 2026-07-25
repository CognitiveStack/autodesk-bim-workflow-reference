# ADR-0004: Adopt Transmittals as the first Phase 4A read slice

## Status

Accepted

## Date

2026-07-25

## Context

Phase 4A (construction information exchange) originally named **RFIs as the
provisional first candidate**, chosen for their structural similarity to the
Issues reads already proven in Phases 2 and 3. That selection was explicitly a
*research* placeholder, not a decision: the PRD required the candidate to be
re-selected on evidence if research showed a better fit.

An authoritative APS capability assessment then compared **RFIs, Submittals,
Transmittals, Sheets and Meetings** against official first-party sources, and a
follow-up spike retrieved the **normative Transmittals Field Guide and Reference
Guide**. The findings relevant to this decision:

- Transmittals v1 exposes **five documented read-only endpoints** and no public
  write operation; the Field Guide states that creating transmittals, updating
  settings, adding recipients and exporting are unsupported.
- Its **authentication gate (Gate 2) is closed by normative documentation**:
  `data:read` for all five endpoints, user context optional, two-legged or
  three-legged OAuth, `x-user-id` on the two-legged path, project IDs accepted
  with or without the `b.` prefix, and a documented rate limit.
- Its records **terminate in exact Data Management document versions** — the
  same identifier domain already governed and proven in Phases 1, 2 and 3.
- It belongs to **Autodesk Forma Data Management**, not Autodesk Forma Build.

That last point is why this needed a human decision rather than a research
conclusion. Phase 4A had been scoped conceptually to Forma Build, so adopting a
Data Management module as its first slice changes the phase's boundary. The
capability research deliberately stopped at a recommendation and left the
roadmap and ownership question open; this ADR resolves it.

The terminology rules in
[ADR-0003](0003-autodesk-platform-product-and-api-terminology.md) apply: the API
family name used here is the one verified from official Autodesk sources, and
naming it makes no claim about any other module.

## Decision

1. **Autodesk Forma Transmittals v1 is adopted as the first Phase 4A read-only
   capability**, replacing RFIs as the first slice.
2. **The APS/Forma MCP component (`CognitiveStack/autodesk-aps-forma-mcp`) owns
   all Transmittals API calls and authentication.** This follows
   [ADR-0001](0001-orchestration-layer-not-mcp-server.md) and
   [ADR-0002](0002-multi-repo-no-submodules.md).
3. **This repository documents, orchestrates, validates and records evidence,
   and never reimplements the API**, its authentication, its pagination or its
   response handling.
4. **The first slice is limited to the five documented `GET` operations:**
   list transmittals; get one transmittal; list recipients; list folders; list
   included document versions.
5. **No Transmittals write capability is in scope.** No write operation is
   approved, and none exists in the documented public surface.
6. **RFIs are the preferred second Phase 4A capability.**
7. **Phase 4A is redefined** as construction information exchange across
   **Autodesk Forma Data Management and Autodesk Forma Build**, rather than
   Forma Build alone.

This decision closes **Gate 6 — component-boundary and roadmap decision** for
Transmittals. It does **not** close Gate 5 or Gate 8, and it does **not**
authorise implementation.

## Consequences

### Positive

- A **compact read-only surface** — five `GET` operations, the smallest credible
  first slice among the assessed modules.
- An **exact document-version evidence chain**: transmittal → recipients →
  folders → exact Data Management document versions.
- **Reuse of established Data Management identifier governance** from Phases 1–3
  rather than opening a new identifier domain.
- **Lower implementation and privacy complexity** than RFIs or Submittals, which
  carry long-form narrative fields.
- **No POST-as-read policy decision is needed** for the first slice; all five
  operations are `GET`, so the component's existing GET-only read posture is
  preserved.

### Constraints

- **Gate 5 (privacy and sanitisation approval) remains open.**
- **Gate 8 (project activation, permission and training-data readiness) remains
  open.**
- **No implementation may begin before both close.**
- **Stable document lineage is not returned as a distinct verified field.** The
  documented response provides a version-qualified document URN and an
  authoritative numeric version; no separate lineage field is identified.
- **Exact document-version evidence must not be upgraded into lineage
  evidence**, whether by string manipulation of a URN or by inference.
- **Personal and behavioural recipient data requires restrictive sanitisation** —
  the documented responses include email addresses, company identities and
  read-receipt timestamps recording when named individuals viewed or downloaded
  a transmittal.
- **No write operations are approved**, now or implicitly later.

## Rejected alternatives

None of these is rejected permanently; each was not selected *first*.

- **RFIs first.** The strongest Forma Build module and the previous provisional
  candidate, retained as the **preferred second capability**. Not first because
  it carries the highest privacy exposure of the assessed modules (question
  text, official answers, comment threads), has the largest read surface, and
  can only be listed through a POST-based search — which would require an
  explicit POST-as-read policy decision before any read slice could be built.
- **Submittals first.** A genuine GA read surface, but the largest and most
  entangled identifier set of the candidates, with reads and writes sharing one
  base path across three release phases — a poor shape for a first read-only
  slice. Remains a later candidate.
- **Sheets first.** A real read surface exists, and the "export-only" reading of
  it is incorrect. Not first because the API cannot relate a sheet to its Revit
  source, which disconnects it from this project's Revit-to-CDE narrative, and
  because export creation is a write. Remains a later candidate.
- **No Phase 4A selection yet.** Rejected because the authentication gate is now
  closed on normative evidence for a fully read-only module, and deferring
  further would leave the phase blocked on a decision the evidence already
  supports.
- **Meetings.** Not a rejected alternative but an unavailable one: no
  authoritative public API surface was verified. This records the sources
  checked, not a claim that no such API exists.

## Follow-up decisions

In order; none is authorised by this ADR:

1. **Approve Transmittals alias and privacy rules** — amending
   [SANITISATION_CONVENTION.md](../guides/SANITISATION_CONVENTION.md) in its own
   increment (Gate 5).
2. **Verify project activation, permissions and synthetic training data** in the
   approved training project (Gate 8).
3. **Create the Phase 4 result schema and execution plan.**
4. **Implement the five reads separately**, in the component repository per
   [ADR-0002](0002-multi-repo-no-submodules.md).
5. **Capture private live evidence** under the git-ignored `.local/` boundary.
6. **Publish sanitised public evidence**, validated against the Phase 4 schema.

Steps 3 onward are conditional on Gates 5 and 8 closing.
