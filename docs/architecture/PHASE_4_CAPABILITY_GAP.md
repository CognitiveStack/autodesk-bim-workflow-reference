# Phase 4 Capability Gap — Construction Information Exchange

**Status:** Phase 4A authoritative APS capability research assessment recorded,
then extended by a Transmittals normative-documentation evidence spike
(**`normative_transmittals_research_complete`**). **Transmittals Gate 2 is
sufficiently verified** (§16.1); **Phase 4 overall still requires additional
architecture and data-readiness work** — Gates 5, 6 and 8 remain unresolved for
every candidate. No Phase 4 MCP capability is implemented, and **no
implementation is authorised by this document**.
**Research date:** 2026-07-24 · **Transmittals normative spike:** 2026-07-25

This document is the authoritative repository record of the Phase 4A capability
research assessment. It records what was verified against first-party Autodesk
sources, what remains unresolved, and which candidate is **recommended for
continued investigation** — not which candidate has been selected. It is
consistent with
[COMPONENT_BOUNDARIES.md](COMPONENT_BOUNDARIES.md),
the [PRD](../prd/PRD_AUTODESK_BIM_WORKFLOW_REFERENCE_IMPLEMENTATION.md) Phase 4A
entry gate, and the terminology model in
[ADR-0003](../decisions/0003-autodesk-platform-product-and-api-terminology.md).

No capability is asserted to exist unless a first-party Autodesk source is cited
for it. No endpoint path appears here that the completed research did not
support. Following the Phase 2 and Phase 3 discipline, an absent or unretrievable
source is recorded as **unresolved**, never as a negative finding.

## 1. Status and purpose

| Baseline | Value |
|---|---|
| Initial research date | 2026-07-24 |
| Transmittals normative spike date | 2026-07-25 |
| Reference-repository baseline (initial pass) | `cc4321a0f585662367d940ae1c9b109d4b0f3753` (`main`, clean) |
| Reference-repository baseline (normative spike) | `08eb2a24ac33c6519d15be3a238f09efa708baef` (`main`, clean) |
| APS/Forma MCP baseline | `75b36b2635de3a5707fd1ff3dbf5cd487e3f0e0a` |
| Registered MCP tool count | 30 (28 read-only Autodesk, 1 guarded Autodesk write, 1 local-only) |
| Transmittals normative research | **`normative_transmittals_research_complete`** |
| Transmittals Gate 2 | **sufficiently verified** (§16.1) |
| Phase 4 overall | **additional architecture and data-readiness work remains required** (Gates 5, 6 and 8) |
| Phase 4 MCP capability implemented | **None** |
| Implementation authorised by this document | **None** |

The initial pass concluded `additional_authoritative_research_required`. The
2026-07-25 spike retrieved the normative Transmittals documentation and closes
**Gate 2 for Transmittals only** — narrowly, on the concerns listed in §16.1. It
does **not** adopt Transmittals into Phase 4A, authorise implementation, or close
Gates 5, 6 or 8.

The purpose of this document is to close the *research* portion of the Phase 4A
entry gate to the extent the available sources permit, and to state precisely
which gate items remain open. It replaces no existing document and amends no
roadmap. The PRD, [COMPONENT_BOUNDARIES.md](COMPONENT_BOUNDARIES.md),
[SANITISATION_CONVENTION.md](../guides/SANITISATION_CONVENTION.md) and
`config/workflows/end-to-end-reference.yaml` are unchanged by this increment.

Per the [PRD](../prd/PRD_AUTODESK_BIM_WORKFLOW_REFERENCE_IMPLEMENTATION.md) §14
classification discipline, the modules below move from *unassessed* only to the
extent that authoritative APS capability verification supports it. Verifying that
an API exists does **not** make a module a `planned` project capability; that is a
separate roadmap decision (§17, §19).

## 2. Source policy and retrieval limitation

### 2.1 Policy

Capability claims are supported **only** by first-party Autodesk sources. The
permitted source classes are:

- official APS Field Guides and Reference Guides;
- official APS technical announcements;
- official APS change histories;
- official Autodesk GitHub samples and Postman collections;
- official Autodesk OpenAPI specifications.

Autodesk product help may explain product workflow terminology, but is **not**
used to prove that a public API exists. No third-party source — general search
summary, AI-generated summary, forum, blog, or Stack Overflow answer — was used to
prove any capability, and no endpoint path was taken from a third-party example.

### 2.2 Retrieval limitation on the first research pass (historical, 2026-07-24)

**This subsection is preserved as the historical record of the first pass. For
Transmittals it is superseded by §2.2A.** It still stands unchanged for **RFIs,
Submittals, Sheets and Meetings**, whose normative documentation has not been
retrieved.

**On 2026-07-24 the normative APS Field Guides and Reference Guides under
`aps.autodesk.com/en/docs/` were not retrievable in the research environment.**
Those pages are client-rendered; every direct retrieval returned only an
application shell containing no documentation content, across multiple user
agents and URL variants, and a second independent tool returned no rendered
content for the same pages.

Consequently, on that pass:

- the endpoint inventory was derived from **official Autodesk announcements** and
  **official Autodesk GitHub Postman collections**;
- both are valid first-party sources, but **neither is a substitute for the
  normative Field Guides and Reference Guides**;
- **authentication scopes, entitlement requirements, rate limits and quotas, and
  some module limitations remained unresolved** for every candidate;
- a Postman collection evidences that an endpoint existed when the collection was
  published. **It does not establish that the collection is currently complete**,
  that no endpoint has since been added or removed, or that current behaviour
  matches.

A further methodological guard from that pass, still in force: a deliberately
nonexistent documentation path returned the same HTTP 200 and the same
application shell as a real one, so **a 200 response from that host proves
nothing about whether a documentation page exists**. No inference about page
existence may be drawn from a status code alone.

### 2.2A Normative retrieval for Transmittals (2026-07-25)

**The normative Transmittals Field Guide, rate-limit page and all five Reference
Guide pages were subsequently retrieved**, through the official APS documentation
page's **own delivery mechanism**:

1. the **official page configuration** served by the APS documentation site
   (`/params/custom.js`), which names the official Autodesk documentation
   configuration and content hosts;
2. the **official documentation IA configuration** for the Forma APIs v1
   documentation set, addressed exactly as the official page addresses it;
3. the **exact official content-object paths supplied by that IA configuration**
   for each Transmittals page.

Recorded explicitly:

- **no authentication bypass occurred**;
- **no credentials were used**;
- **no unpublished or unrelated content was accessed** — bucket-root listing is
  refused by the host, and only the specific document objects that the official
  page itself requests were retrieved;
- **exact official document objects were retrieved**, each returning
  `text/html` with full normative content;
- this is the documented, publicly served delivery path for the published
  documentation — **not an undocumented or private API**.

**Normative documentation supersedes official-sample-only findings wherever the
two conflict.** Where this document previously recorded a Transmittals fact from
the Postman collection alone and the normative source says otherwise, the
normative source governs and the earlier statement is corrected in place (see
§7.4 for the list of corrections).

Retrieving the normative documentation for **RFIs, Submittals and Sheets**
remains open (§18).

### 2.3 Source table

| # | Source title | Source class | Date | Capability supported | Currency |
|---|---|---|---|---|---|
| S1 | *Autodesk Forma Build RFI v3 API is released* ([aps.autodesk.com](https://aps.autodesk.com/blog/autodesk-build-rfi-v3-api-released)) | Official announcement | 2025-07-23 | RFI v3 GA; base path; endpoint list; v2 deprecation; `POST /search:rfis` semantics; workflow/permission model | current |
| S2 | *Autodesk Forma Transmittals API General Availability* ([aps.autodesk.com](https://aps.autodesk.com/blog/autodesk-construction-cloud-transmittals-api-general-availability)) | Official announcement | 2025-12-10 | Transmittals v1 GA; five read-only operations; module ownership = Forma Data Management | current |
| S3 | *Autodesk Forma Build Submittals API General Availability* ([aps.autodesk.com](https://aps.autodesk.com/blog/autodesk-build-submittals-api-general-availability)) | Official announcement | 2024-02-22 | Submittals GA read phase (nine read-only operations); custom-numbering fields | current |
| S4 | *Autodesk Forma Submittals Write API and Updates* ([aps.autodesk.com](https://aps.autodesk.com/blog/autodesk-construction-cloud-submittals-write-api-and-updates)) | Official announcement | 2024-08-05 (updated 2024-08-28) | Submittals write phase; added reads incl. `GET responses`, `GET metadata`, `GET users/me` | current |
| S5 | *Autodesk Forma Build Sheets API* ([aps.autodesk.com](https://aps.autodesk.com/blog/autodesk-build-sheets-api)) | Official announcement | 2022-08-22 | Original Sheets read/write surface; 2-legged and 3-legged support; PDF source only; no Revit-view-to-sheet extraction | historical baseline, carries a 2024-11 update pointer |
| S6 | *Forma Sheet API Added Endpoints of Reading Collection* ([aps.autodesk.com](https://aps.autodesk.com/blog/acc-sheet-api-added-endpoints-reading-collection)) | Official announcement | 2024-11-27 | `GET collections`, `GET collections/:collectionId`; both `b.`-prefixed and bare project IDs accepted | current |
| S7 | *API of Exporting Forma Sheet to PDF is Released* ([aps.autodesk.com](https://aps.autodesk.com/blog/api-exporting-acc-sheet-pdf-released)) | Official announcement | 2024-08-04 | `POST exports` / `GET exports/:exportId`; asynchronous job; 1000-sheet cap; 1-hour signed URL; Export permission | current |
| S8 | ACC Transmittals API Postman collection, `autodesk-platform-services/aps-autodesk.docs.api-postman.collection` ([github.com](https://github.com/autodesk-platform-services/aps-autodesk.docs.api-postman.collection)) | Official Autodesk GitHub collection | Transmittals folder last committed 2025-12-10 | Transmittals paths; `data:read`; `limit` 1–200, `offset`, `sort` — all **`official_sample_correlated`** with N1–N7. Its 3-legged-only setup and bare-project-ID variable are **`official_sample_only`** and **narrower than** the normative contract (§7.4) | published collection; **not established as complete or current** — its Transmittals folder has not been updated since the GA date |
| S9 | ACC RFIs and Submittals API Postman collections, `autodesk-platform-services/aps-autodesk.build.api-postman.collection` ([github.com](https://github.com/autodesk-platform-services/aps-autodesk.build.api-postman.collection)) | Official Autodesk GitHub collection | — | RFI v3 and Submittals v2 paths and methods; collection-wide scope strings; 3-legged or SSA prerequisites; pagination and filter parameters | current for the published collections |
| S10 | ACC Sheet API Postman collection, `autodesk-platform-services/aps-acc-sheet.api-postman.collection` ([github.com](https://github.com/autodesk-platform-services/aps-acc-sheet.api-postman.collection)) | Official Autodesk GitHub collection | — | Sheets read, batch-get, upload/review, export operation inventory | current for the published collection |
| S11 | Autodesk Forma APIs overview ([aps.autodesk.com](https://aps.autodesk.com/developer/overview/forma)) | Official overview | — | Forma and Forma-related API listing consulted during the Meetings check | current |
| S12 | `autodesk-platform-services/aps-sdk-openapi` ([github.com](https://github.com/autodesk-platform-services/aps-sdk-openapi)) | Official Autodesk OpenAPI specifications | — | Consulted; contains Account Admin, Issues and Secure Service Account specifications only | current; **absence of a module here proves nothing about that module's existence** |
| S13 | APS Field Guides and Reference Guides for **RFIs, Submittals and Sheets** | **Normative Field or Reference Guide — unavailable** | — | Would supply per-endpoint scopes, entitlement, rate limits, regional limits, webhooks, response schemas | **unresolved — not retrieved.** Narrowed on 2026-07-25: the Transmittals guides **were** retrieved (N1–N7) |

### 2.4 Normative Transmittals sources (retrieved 2026-07-25)

All entries below are **`normative_documentation_verified`** — the strongest
evidence class in this document. Each was retrieved on **2026-07-25** as an
official Autodesk document object via the delivery path described in §2.2A. The
canonical reader-facing locations are the published documentation URLs shown in
the "official location" column.

| # | Source title | Source class | Official location | Retrieved | Claim supported | Evidence strength |
|---|---|---|---|---|---|---|
| N1 | Forma Transmittals API **Field Guide** | Normative Field Guide | `https://aps.autodesk.com/en/docs/acc/v1/overview/field-guide/transmittals/` | 2026-07-25 | The five API features; the four explicit unsupported operations (release limitations) | normative_documentation_verified |
| N2 | Forma: **Transmittals API Rate Limits** | Normative rate-limit page | `https://aps.autodesk.com/en/docs/acc/v1/overview/rate-limits/transmittals-rate-limits` | 2026-07-25 | 200 requests/minute, per application (client ID), measured independently for each endpoint | normative_documentation_verified |
| N3 | **List Transmittals** reference | Normative Reference Guide | `https://aps.autodesk.com/en/docs/acc/v1/reference/http/transmittals-listtransmittals-GET/` | 2026-07-25 | Method/URI; `data:read`; user context optional; 2-legged or 3-legged; `x-user-id`; project-ID forms; `limit`/`offset`/`sort`; status codes; response envelope and fields | normative_documentation_verified |
| N4 | **Get a Project Transmittal** reference | Normative Reference Guide | `https://aps.autodesk.com/en/docs/acc/v1/reference/http/transmittals-gettransmittal-GET/` | 2026-07-25 | Method/URI; `data:read`; user context optional; no query parameters; no pagination | normative_documentation_verified |
| N5 | **List Transmittal Recipients** reference | Normative Reference Guide | `https://aps.autodesk.com/en/docs/acc/v1/reference/http/transmittals-listtransmittalrecipients-GET/` | 2026-07-25 | Method/URI; `data:read`; non-paginated `recipients` + `externalMembers` shape; 202 behaviour; `displayRecipients` visibility model | normative_documentation_verified |
| N6 | **List Transmittal Folders** reference | Normative Reference Guide | `https://aps.autodesk.com/en/docs/acc/v1/reference/http/transmittals-listtransmittalfolders-GET/` | 2026-07-25 | Method/URI; `data:read`; `limit`/`offset`/`sort`; pagination; 202 behaviour; folder response fields | normative_documentation_verified |
| N7 | **List Transmittal Documents** reference | Normative Reference Guide | `https://aps.autodesk.com/en/docs/acc/v1/reference/http/transmittals-listtransmittaldocuments-GET/` | 2026-07-25 | Method/URI; `data:read`; `limit`/`offset`/`sort`; pagination; 202 behaviour; exact-version semantics; document response fields | normative_documentation_verified |

**Provenance sources** — recorded only to explain how N1–N7 were obtained, and
supporting no capability claim of their own:

| # | Source | Source class | Retrieved | Role |
|---|---|---|---|---|
| P1 | APS documentation page configuration (`https://aps.autodesk.com/params/custom.js`) | Official APS page asset | 2026-07-25 | Names the official Autodesk documentation configuration and content hosts |
| P2 | APS documentation application script (`https://aps.autodesk.com/static/scripts/release/app_au.new.min.*.js`) | Official APS page asset | 2026-07-25 | Defines how the official page derives its IA-configuration and content-object addresses |
| P3 | Official Forma APIs v1 documentation IA configuration | Official APS documentation configuration | 2026-07-25 | Supplies the exact official content-object path for each Transmittals page |

**Evidence-class ordering used throughout this document**, strongest first:

1. **`normative_documentation_verified`** — stated by an official Field Guide or
   Reference Guide (N1–N7).
2. **`official_sample_correlated`** — an official Autodesk sample that agrees
   with a normative source. Corroborating only; it adds no strength of its own.
3. **`official_sample_only`** — an official Autodesk sample with no normative
   confirmation. **Materially weaker**; may be narrower than, or inconsistent
   with, the normative contract.
4. **`unresolved`** — no first-party source located.

## 3. Governing Phase 4A entry gate

The [PRD](../prd/PRD_AUTODESK_BIM_WORKFLOW_REFERENCE_IMPLEMENTATION.md) §15
requires all ten items below to be satisfied **before any Phase 4A implementation
increment**:

1. authoritative APS capability verification;
2. authentication-scope verification;
3. read/write operation inventory;
4. data-model and identifier-domain analysis;
5. privacy and sanitisation planning;
6. component-boundary decision;
7. read-only-first sequencing;
8. Harrismith scenario and data readiness;
9. no unsupported writes;
10. no monolithic Forma Build API assumption.

**Every gate must pass before component implementation begins.** A research
recommendation does not satisfy a gate, and a gate is not satisfied by analogy to
another module. Verdicts are recorded in §16.

## 4. Candidate capability matrix

| Module | Official API / module name | Version | Maturity | Module ownership | Read surface | Write surface | Authentication | Repository classification |
|---|---|---|---|---|---|---|---|---|
| **RFIs** | Autodesk Forma Build RFI API (S1) | v3 | General availability, announced 2025-07-23 (S1) | Forma Build | Verified present; includes a read-semantic POST search (S1, S9) | Verified present (S1, S9) | 3-legged or SSA evidenced; per-endpoint scopes unresolved (S9, S13) | verified GA capability; candidate; **not implementation-ready** |
| **Submittals** | Autodesk Forma Build Submittals API (S3) | v2 | General availability, read phase 2024-02-22, write phase 2024-08-05 (S3, S4) | Forma Build | Verified present and broad (S3, S4, S9) | Verified present, sharing the same base path (S4, S9) | 3-legged evidenced; per-endpoint scopes unresolved (S9, S13) | verified GA capability; candidate; **not implementation-ready** |
| **Transmittals** | Autodesk Forma Transmittals API (N1, S2) | v1 | General availability, announced 2025-12-10 (S2) | **Autodesk Forma Data Management** (S2) | **Normatively verified** — five read-only operations (N1, N3–N7) | **Normatively excluded** — the Field Guide lists creating, updating settings, adding recipients and exporting as unsupported (N1) | **Normatively verified** — `data:read`, user context optional, 2-legged **or** 3-legged (N3–N7). Module activation and entitlement **unresolved** | verified GA capability; **Gate 2 sufficiently verified** (§16.1); **recommended candidate pending decisions**; **not yet an adopted Phase 4A module**; **not implementation-ready** |
| **Sheets** | Autodesk Forma Build Sheets API (S5) | v1 | General availability (S5, S6, S7) | Forma Build | **Genuine read surface verified present** — sheets, version sets, collections (S5, S6, S10) | Verified present, including asynchronous export creation (S5, S7, S10) | 2-legged **and** 3-legged evidenced (S5, S6) | verified GA capability with a genuine read surface; **later candidate**; **not implementation-ready** |
| **Meetings** | — | — | — | — | — | — | — | **`meetings_public_api_not_verified`** |

The four verified modules are named, versioned and statused **independently**.
There is no single "Forma Build API", and none is assumed anywhere in this
document (gate 10).

## 5. RFI v3 assessment

**Official name and version.** Autodesk Forma Build RFI API, **v3**, project-scoped
under `…/construction/rfis/v3/projects/:projectId` (S1, S9). General availability
announced 2025-07-23 (S1).

**Version history.** The announcement records that Forma RFI v2 was consolidated
with the BIM 360 RFI API in 2022 and that **v2 has since been deprecated**, and
notes that not all Forma RFI features or entity data were supported through the
BIM 360 API (S1). Any future implementation must target v3; a migration article is
referenced from the announcement.

**Hierarchy.** Project-scoped: `rfi-types`, `workflow`, `attributes`, `users/me`,
and `rfis`, with `responses`, `comments` and `attachments` nested under an
individual RFI (S1, S9).

**Read operations** (S1, S9): `GET rfi-types`, `GET workflow`, `GET users/me`,
`GET attributes`, `GET rfis/custom-identifier`, `GET rfis/:id`,
`GET rfis/:rfiId/comments`, `GET rfis/:rfiId/attachments`, and
**`POST search:rfis`**.

**Write operations** (S1, S9): `POST rfis`, `PATCH rfis/:id`,
`POST rfis/:rfiId/responses`, `PATCH rfis/:rfiId/responses/:responseId`,
`POST rfis/:rfiId/comments`, `POST attributes`, `PATCH attributes/:attributeId`.

**`POST /search:rfis` is a state-free, read-semantic operation.** The announcement
records that there is no `GET` RFI-collection endpoint in this release, and that
`POST /search:rfis` performs the search and returns all RFIs when the payload is
an empty JSON object or the filter is empty (S1). It changes no server state and
is therefore classified as a **read**.

**Permission discovery.** `GET users/me` returns the calling user's workflow roles
together with permitted actions, permitted attributes and required attributes;
`GET workflow` reflects the configured permissions (S1).

**Workflow and type reads.** `GET rfi-types` returns the types and their default
managers, reviewers and watchers; `GET workflow` returns the current workflow with
the active RFI type (S1).

**Comments and attachments.** Both are listable through `GET` operations (S1, S9).
Retrieving attachment *content* additionally involves signed-URL retrieval outside
the RFI module; only attachment **metadata** listing is in scope for a read slice.

**Unresolved** (S13): per-endpoint minimal scopes; entitlement requirements; rate
limits and quotas; regional or project-type restrictions — the permitted-status
payload contains `wfUS` and `wfEU` workflow keys (S1), which is suggestive of
region-flavoured workflows but characterises nothing; webhook availability; live
response shapes.

**Privacy risk: high.** RFI question text, official answers, response bodies and
comment threads are narrative free text, and assignees, reviewers and watchers are
identities. This is the highest leakage surface of the verified modules (§13).

**Proposed read-only chain — not approved:**

```
users/me
  → rfi-types
    → workflow
      → search:rfis
        → one RFI
          → comments
            → attachments
```

Creation, patching, responding, transitioning and upload are excluded.

**POST-as-read policy decision required.** Because listing RFIs is only possible
through `POST /search:rfis`, an RFI read slice cannot be built without permitting
a POST inside the read-only boundary. The component's existing Model Coordination
reads are documented as **GET-only with internally constructed request paths**
([COMPONENT_BOUNDARIES.md](COMPONENT_BOUNDARIES.md) §3.1). Permitting POST-as-read
would therefore require an **explicit repository policy decision**, recorded before
implementation — it is not an implementation detail.

## 6. Submittals v2 assessment

**Official name and version.** Autodesk Forma Build Submittals API, **v2**,
project-scoped under `…/construction/submittals/v2/projects/:projectId` (S3, S9).

**Release phases.** The read phase reached general availability on 2024-02-22 with
nine read-only operations (S3). The write phase followed on 2024-08-05, adding
write operations **and** further reads — including `GET users/me`, `GET metadata`,
`GET settings/mappings` and `GET items:next-custom-identifier` — with `GET
responses` added on 2024-08-28 (S4). Reads and writes share one base path.

**Read inventory** (S3, S4, S9): `GET items`, `GET items/:itemId`,
`GET items/:itemId/revisions`, `GET items/:itemId/attachments`, `GET item-types`,
`GET item-types/:itemTypeId`, `GET metadata`, `GET packages`,
`GET packages/:packageId`, `GET specs`, `GET specs/:specId`, `GET responses`,
`GET responses/:responseId`, `GET users/me`, `GET settings/mappings`,
`GET items/:itemId/steps`, `GET items/:itemId/steps/:stepId`,
`GET items/:itemId/steps/:stepId/tasks`,
`GET items/:itemId/steps/:stepId/tasks/:taskId`, `GET templates` (admin-only),
`GET items:next-custom-identifier`, `GET async-jobs/:asyncJobId`, and
**`POST items:validate-custom-identifier`** (a validation call with read
semantics).

**Write inventory** (S4, S9): `POST items`, `PATCH items/:itemId`,
`POST items/{itemId}:transition`, `POST specs`, `POST items/:itemId/attachments`,
`PATCH items/:itemId/attachments/:attachmentId`,
`POST …/steps/:stepId/tasks/{taskId}:close`, `POST settings/mappings`,
`DELETE settings/mappings/:mappingId`, and
`POST settings/custom-identifier:change-sequence-type`.

**Project metadata.** `GET metadata` returns project metadata for submittal roles,
user types, statuses and the custom-numbering type — global numbering versus spec
sequence numbering (S4).

**Entity coverage.** Items, item types, packages, specifications (spec sections),
responses, attachments, revisions, review steps, tasks and manager mappings are
all represented in the read surface (S3, S4, S9).

**Permission discovery.** `GET users/me` returns the calling user's submittal
permissions (S4).

**Identifier surface.** The largest of the verified modules: item, item type,
package, spec, response, step, task, attachment, manager-mapping, template and
async-job identifiers all coexist (§12).

**Pagination and filtering** (S4, S9): `limit`, `offset` and `sort` are present,
with several endpoints documenting `limit` values of 1–50 and a default of 20;
filters include `filter[packageId]`, `filter[reviewResponseId]`,
`filter[statusId]`, `filter[title]`, `filter[categoryId]`, `filter[revision]` and
`filter[isFileUploaded]`, plus a `search` term.

**Unresolved** (S13): per-endpoint minimal scopes; entitlement requirements; rate
limits; module limitations; live response shapes.

**Privacy risk: high.** Item titles and descriptions, response text, ball-in-court
users, manager mappings (person-to-role), spec section titles and attachment
filenames.

**Proposed read-only chain — not approved:**

```
users/me
  → metadata
    → items
      → one item
        → packages
          → specifications
            → responses
              → attachment metadata
```

Creation, transition, task closure, attachment upload and project-setting changes
are excluded.

## 7. Transmittals v1 assessment

**Official name and version.** Autodesk Forma Transmittals API, **v1**,
project-scoped under `…/construction/transmittals/v1/projects/:projectId`
(S2, S8). **General availability announced 2025-12-10** (S2).

**Module ownership.** The announcement describes it as "another Autodesk Forma
**Data Management**-specific API" (S2). Ownership therefore sits with **Autodesk
Forma Data Management**, not Forma Build. This is the single most consequential
fact for the roadmap decision in §17.

### 7.0 Normative common contract (all five endpoints)

Verified for **every one** of the five operations (N3–N7);
**`normative_documentation_verified`**:

| Concern | Normative value |
|---|---|
| HTTP method | `GET` |
| Base | `https://developer.api.autodesk.com/construction/transmittals/v1` |
| Authorization | `Bearer <token>`, obtained via **either a two-legged or a three-legged** OAuth flow |
| Required OAuth scope | **`data:read`** |
| Authentication Context | **user context optional** |
| `x-user-id` header | **Required only for two-legged**; not needed for three-legged. Accepts the **Autodesk ID (`autodeskId`) only**. The application can access only those users assigned to it in the **SaaS Integrations** interface |
| Project ID | Accepted **with or without the `b.` prefix** |
| Project compatibility | **Not compatible with BIM 360 projects** |
| Data format | JSON |

**Endpoint-specific paths and behaviour** (N3–N7):

| Operation | Path | Query parameters | Pagination | 202 documented |
|---|---|---|---|---|
| **List Transmittals** | `projects/{projectId}/transmittals` | `limit` **1–200**, default **20**; `offset` default **0**; `sort` over `status`, `sequenceId`, `title`, `sentByName`, `createdAt`, `documentsCount` (default `sequenceId desc`) | **Yes** | — |
| **Get Transmittal** | `projects/{projectId}/transmittals/{transmittalId}` | none | **No pagination** | — |
| **List Recipients** | `…/{transmittalId}/recipients` | none | **No pagination envelope** — returns `recipients` and `externalMembers` | **Yes** |
| **List Folders** | `…/{transmittalId}/folders` | `limit`, `offset`, `sort` over `name`, `lastUpdatedAt`, `updatedByName` (default `name asc`) | **Yes** | **Yes** |
| **List Documents** | `…/{transmittalId}/documents` | `limit`, `offset`, `sort` over `name`, `title`, `version`, `lastUpdatedAt`, `updatedByName` (default `name asc`) | **Yes** | **Yes** |

**Documented status and error behaviour** (N3–N7): **200**; **202 Accepted**
where documented (recipients, folders, documents — the transmittal is still
processing and the relevant list is returned empty); **400** Bad Request;
**401** Unauthorized; **403** Forbidden ("the user does not have permission to
perform this operation"); **404** Not Found (project or transmittal does not
exist); and a documented **500 Internal Server Error**. No response code beyond
those documented is recorded here.

**Write surface — normatively excluded.** The Field Guide states the Transmittals
API does **not** support creating new transmittals, updating transmittal
settings, adding recipients to a transmittal, or exporting transmittal folders or
document packages (N1). This supersedes the earlier statement, which rested on
the announcement and the official collection alone, that no write operation had
been *identified*.

**Permission discovery.** **None.** There is no `users/me` endpoint in this
module (N1, N3–N7). Read permission must be confirmed outside the API — a named
limitation, not an oversight. The permission *behaviour* is nevertheless
documented (§7.3).

### 7.1 Pagination and rate limits (normative)

**Collection pagination envelope** (N3, N6, N7): `results` plus a `pagination`
object carrying `limit`, `offset`, `totalResults` and `nextUrl`. **Absence of
`nextUrl` means the current page is the last page.** The **maximum page `limit`
is 200** where documented, with a default of 20.

**Recipients uses a different, non-paginated shape** (N5): `recipients` and
`externalMembers` arrays with **no `pagination` object** and no query parameters.
This asymmetry is a real implementation consideration.

**Rate limit** (N2): **200 requests per minute, per application (identified by
client ID), measured independently for each Transmittals endpoint.** This is
**not** a project-wide or account-wide limit, and it must not be described as
one.

### 7.2 Release limitations (normative and unresolved)

**Normative Field Guide exclusions** (N1) — the API does not support:

- creating new transmittals;
- updating transmittal settings;
- adding recipients to a transmittal;
- exporting transmittal folders or document packages.

**Additionally documented** (N3–N7):

- **not compatible with BIM 360 projects**;
- while a transmittal is processing (`status = SENDING`), **recipients, folders
  or documents may return 202 with temporarily empty lists**, and `recipients` /
  `externalMembers` may be temporarily empty on the transmittal record itself.

**Deliberately kept unresolved** — no first-party source verified these, so none
is recorded as a negative finding: records available only after a particular
date; regional availability; webhook support; cross-project transmittals;
recipient-count caps; document-count caps; unsupported transmittal types; a
project **module-activation prerequisite**; folder/document permission
interaction; and **Secure Service Account support**.

### 7.3 Permission behaviour (normative)

- Unauthorised access **may return 403** (N3–N7).
- **Two-legged access requires SaaS Integrations user assignment** — the
  application can reach only users assigned to it there (N3–N7).
- **Recipient visibility depends on `displayRecipients`** (N3, N5):
  - **`ALL`** — recipients can view the full recipient list;
  - **`LIMITED`** — each recipient can view only their own recipient entry;
  - the **sender and Project Admins always see the full list**, regardless of the
    setting.

The broader proposition that *users retrieve exactly what they can see in the
Forma interface* is **not** stated in this general form by the normative
documentation and **remains unresolved**. The documented visibility model is
consistent with it but does not establish it.

### 7.4 Corrections to the first research pass

The following statements from the 2026-07-24 pass were based on the official
sample or the announcement alone and are **superseded by normative
documentation**. They apply to **Transmittals only** and must not be generalised
to RFIs, Submittals or Sheets, whose normative documentation has not been
retrieved.

| Superseded statement | Normative correction (N1–N7) |
|---|---|
| "Two-legged support: not evidenced" | **Two-legged OAuth is supported** on all five endpoints |
| "`x-user-id` is suggestive only and proves nothing about impersonation support" | `x-user-id` is **normatively documented**: required for two-legged, accepts the Autodesk ID only, and is bounded by SaaS Integrations user assignment |
| "Minimal per-endpoint read scope: unresolved" | **`data:read` is the exact required scope for all five endpoints** |
| "Project ID without the `b.` prefix" | **Both forms are accepted** — with or without the `b.` prefix. The official Postman sample uses the bare form (`official_sample_only`); the normative documentation supports both |
| "Rate limits: unresolved" | **200 requests/minute per application, per endpoint** |
| "No public write operation *identified*" | Writes are **normatively excluded** by the Field Guide's four stated limitations |

**Three-legged OAuth is supported but not required**, and **user consent is
required only when the three-legged path is selected**. **Secure Service Account
support remains unresolved** for this module.

### 7.5 Proposed evidence chain

```
TRANSMITTAL_1
  → RECIPIENT_1
    → FOLDER_1
      → VERSION_1
```

Each node belongs to a **different identifier domain**, and the aliases are not
interchangeable:

- **`TRANSMITTAL_1`** — the **Transmittals module** domain. A transmittal record
  is a record of a sharing event. It is not a Review, an RFI, a Submittal, or a
  Data Management entity.
- **`RECIPIENT_1`** — the **recipient/person** domain. A recipient identity is
  personal data (§13).
- **`FOLDER_1`** — the **Data Management folder** domain. These are the folders
  associated with the included file versions.
- **`VERSION_1`** — an **exact Data Management document version**. This is the
  same domain as the exact coordinated version proven in Phase 3
  ([PHASE_3_CAPABILITY_GAP.md](PHASE_3_CAPABILITY_GAP.md) §4) and the version
  identified in Phase 1.

**Exact-version finding — strengthened by normative documentation** (N7). The
List Transmittal Documents operation **returns the exact version of each document
as it existed when the transmittal was issued**. The response provides a
**version-qualified document URN** and, separately, an **authoritative numeric
`version` field**. The numeric document version therefore **need not be inferred
from the URN** — which satisfies the Phase 3 governing constraint directly,
rather than merely avoiding a violation of it.

**Lineage boundary — preserved, not strengthened.**

- **No stable document-lineage field is explicitly identified by the normative
  source.**
- The stable component may appear **embedded inside** the version-qualified URN,
  but obtaining it by string manipulation would be a **client-side derivation**,
  not a value the API returns as a lineage identifier.
- **Stable lineage therefore remains unresolved and must not be represented as
  returned evidence.**

Two constraints carry forward from
[SANITISATION_CONVENTION.md](../guides/SANITISATION_CONVENTION.md):

- **A lineage reference must not be inferred from a version**, and no
  lineage-level claim may be made from this module alone.
- **Matching alias suffixes prove nothing.** `TRANSMITTAL_1`, `RECIPIENT_1`,
  `FOLDER_1` and `VERSION_1` sharing the suffix `_1` implies no identity,
  correspondence or relationship. Suffixes are per-domain counters, never
  evidence.

### 7.6 Why Transmittals is recommended for continued investigation

- The researched public surface is **entirely read-only**, so the read-only-first
  posture is structural rather than a matter of discipline.
- It is **only five operations**, the smallest credible slice of the verified
  modules.
- The evidence chain is **compact** and each hop is a single call.
- It **reuses the Data Management document-version domain already governed in
  Phases 1–3**, extending a proven identifier lineage rather than opening a new
  one, and reusing existing alias families rather than minting new ones.
- **Lower privacy risk and lower implementation complexity** than RFIs or
  Submittals — there is no long-form narrative body comparable to an RFI question
  or official answer.
- **Existing training document versions could later be reused** as the included
  documents, rather than requiring new source material to be authored.

### 7.7 Why Transmittals is not yet adopted

Gate 2 closing does **not** move any of the following. Each remains a reason
Transmittals is not adopted:

- Its module ownership is **Autodesk Forma Data Management**, not Forma Build,
  whereas Phase 4A is currently defined as Forma Build construction information
  exchange. Adopting it is a **roadmap decision**, not a capability finding.
- **Exact authentication scopes are now resolved** (§7.0, §7.4), but
  **project-module activation and entitlement remain unresolved** (§7.2).
- **Component ownership has not been formally recorded** in
  [COMPONENT_BOUNDARIES.md](COMPONENT_BOUNDARIES.md), and **compatibility with
  the APS/Forma MCP's existing authentication model is unproven** — no component
  change or inspection was made for it.
- The **alias additions in §13 are proposed only and are not approved**; no change
  has been made to
  [SANITISATION_CONVENTION.md](../guides/SANITISATION_CONVENTION.md).
- **Training-project module activation, live permission and data readiness are
  unverified** (§14) — no Autodesk project API was called at any point.

## 8. Sheets v1 assessment

**A genuine Sheets read surface exists.** The naive reading that this module is
confined to exports is not supported: sheets, version sets and collections are all
readable (S5, S6, S10).

**Read operations** (S5, S6, S10): `GET sheets`, `GET version-sets`,
`GET collections`, `GET collections/:collectionId`, `GET uploads`,
`GET uploads/:uploadId`, `GET uploads/:uploadId/review-sheets`,
`GET exports/:exportId`, plus the **read-semantic POST** operations
`POST sheets:batch-get`, `POST version-sets:batch-get` and
`POST uploads/:uploadId/thumbnails:batch-get`.

**Write operations** (S5, S7, S10): `POST version-sets`,
`PATCH version-sets/:versionSetId`, `POST version-sets:batch-delete`,
`POST sheets:batch-update`, `POST sheets:batch-delete`,
`POST sheets:batch-restore`, `POST storage`, `POST uploads`,
`PATCH uploads/:uploadId/review-sheets`,
`POST uploads/:uploadId/review-sheets:publish`, and **`POST exports`**.

**PDF export creation is a write.** `POST exports` initiates an asynchronous job
that runs in the background and returns an export identifier for polling (S7). It
creates server-side job state and produces a new artifact. The source sheet data
is not modified, but the operation is not state-free and is **not** classified as
a read.

**Export status is readable.** `GET exports/:exportId` returns job progress and,
on completion, the download link (S7).

**Exported signed URLs are sensitive.** The download link is an S3 signed URL
valid for one hour (S7). Signed URLs, bucket keys and object keys **must never
appear in public evidence**, in any field, note, warning or free-text string.

**Source and relationship limits** (S5): the API release supports **PDF source
only**, and the announcement records that the API does not support extracting
Revit model 2D views to sheets, naming this an explicit gap between the product
interface and the API. **No Revit-view-to-sheet source relationship is verified.**

**Other recorded constraints:** a maximum of 1000 sheets per export call,
conjoined into one PDF; the caller requires at least Export permission (S7). Both
`b.`-prefixed and bare project identifiers are accepted (S6). Markups and
hyperlinks appear in the researched surface as **export-time options only**; no
markup or hyperlink read API is verified.

**Domain separation.** These are five distinct things and are never conflated:

| Thing | Domain |
|---|---|
| Forma Build **Sheets** | this Sheets API |
| **Revit sheets** stored in an RVT file | Revit API, reached through the Revit MCP |
| **Data Management file versions** | the Phases 1–3 version domain |
| **Model Derivative views** and **derivative manifests** | the component's `list_model_views` / `get_derivative_manifest` reads |
| **Exported PDFs** | S3 artifacts produced by `POST exports` |

The component's `list_model_views` and `get_derivative_manifest` are **Model
Derivative** reads and are **not** a Sheets module
([COMPONENT_BOUNDARIES.md](COMPONENT_BOUNDARIES.md) §3).

**Classification: viable later read-only candidate, but not first.** The read
surface is real, but the absence of a verified Revit-source relationship separates
it from this repository's Revit-to-CDE narrative, and the module's writes sit
alongside its reads on one base path.

## 9. Meetings result

**Recorded result: `meetings_public_api_not_verified`.**

- **No authoritative public surface was located in the official sources checked** —
  official APS documentation and announcements, the official Autodesk Forma APIs
  overview (S11), the official Autodesk OpenAPI specifications (S12), and the
  official Autodesk Postman collection repositories (S8, S9, S10), which do carry
  collections for other modules.
- **This does not prove non-existence.** It establishes only that no authoritative
  public surface was verified during this research, from these sources, on
  2026-07-24.
- **No API name, version, maturity, scope, operation set or entity model is
  asserted.** Meeting records, attendees, agenda items, minutes, attachments and
  action items are therefore entirely uncharacterised here.
- Should such a surface later be verified, **meeting minutes and attendee lists
  would require synthetic-only or extremely restrictive evidence handling** — they
  would be the highest-leakage content of any module surveyed, and the default
  public-evidence policy would be full omission of narrative content (§13).

Per [COMPONENT_BOUNDARIES.md](COMPONENT_BOUNDARIES.md) §2 and the
[PRD](../prd/PRD_AUTODESK_BIM_WORKFLOW_REFERENCE_IMPLEMENTATION.md) §14, this
leaves Meetings **unassessed for capability purposes**; it is not upgraded on the
basis of product-interface presence.

## 10. Authentication and permissions matrix

| Concern | RFI v3 | Submittals v2 | Transmittals v1 | Sheets v1 |
|---|---|---|---|---|
| Two-legged support | Not evidenced | Not evidenced | **Supported — normative** (N3–N7) | **Evidenced** (S5, S6) |
| Three-legged support | Evidenced (S9) | Evidenced (S9) | **Supported but not required — normative** (N3–N7) | Evidenced, and recommended by Autodesk so user permissions apply (S5) |
| SSA support | **Evidenced** — tutorial prerequisites name a 3-legged **or SSA** token (S9) | Not evidenced | **unresolved** — not mentioned in the normative documentation | Not evidenced |
| Scope evidence | Collection-wide `data:read data:write data:create` (S9) | Collection-wide `data:read data:write` (S9) | **Normative: `data:read`** on each of the five endpoints (N3–N7); `official_sample_correlated` by S8 | Not isolated |
| Minimal per-endpoint read scope | **unresolved** (S13) | **unresolved** (S13) | **RESOLVED — `data:read`** (N3–N7) | **unresolved** (S13) |
| User-context requirement | **Yes** — a user-context dependency unless SSA is used | **Yes** — a user-context dependency | **Optional** — "user context optional"; two-legged is permitted with `x-user-id` (N3–N7) | Optional; application context is permitted |
| Entitlement status | **unresolved** | **unresolved** | **Partly resolved** — two-legged requires **SaaS Integrations** user assignment (N3–N7); **project-module activation remains unresolved** | **unresolved** |
| Role requirements | Workflow roles (creator, manager, reviewer, watcher) gate visibility and actions (S1) | Submittal roles, manager mappings, ball-in-court; `GET templates` is admin-only (S4, S9) | **Normative visibility model** — `displayRecipients` `ALL`/`LIMITED`; sender and Project Admins always see the full recipient list (N3, N5) | At least Export permission for `POST exports` (S7) |
| Permission-discovery endpoint | `GET users/me` (S1) | `GET users/me` (S4) | **None** (N1, N3–N7) | None evidenced |
| Unresolved fields | rate limits, quotas, regional restrictions, webhooks, response shapes | rate limits, quotas, module limitations, response shapes | SSA support, project-module activation, regional availability, webhooks, cross-project behaviour, caps, stable lineage field, live response behaviour | entitlement, rate limits, markup/hyperlink reads, response shapes |
| Rate limits | **unresolved** | **unresolved** | **RESOLVED — 200 req/min per application, per endpoint** (N2) | **unresolved** |

Two rules govern this table:

- **A collection-wide Postman scope string does not establish a minimal
  per-endpoint scope.** The RFI collection's `data:read data:write data:create`
  covers that collection's write requests as well; nothing may be inferred from it
  about what the read subset alone requires. The same applies to the Submittals
  collection.
- **A three-legged requirement is recorded as a user-context dependency**, not an
  implementation detail. It is a gate item, because the component's existing
  verified reads have not been shown to operate under an interactive user-consent
  flow for these modules.

- **Normative documentation outranks an official sample.** Where a Postman
  collection is narrower than, or inconsistent with, a Field or Reference Guide,
  the normative source governs (§2.4, §7.4). An `official_sample_only` finding is
  never treated as equivalent to a normative one.

**Gate 2 status.** It is **sufficiently verified for Transmittals** (§16.1) and
**remains unresolved for RFIs, Submittals and Sheets**. The Transmittals findings
rest on that module's own normative documentation and **must not be generalised**
to any other module.

## 11. Read/write operation inventory

Classification vocabulary: **read** · **read-semantic POST** (a POST that performs
a search, batch retrieval or validation without changing server state) · **write**
· **unresolved**. No endpoint path appears here that the completed research did not
support.

### 11.1 RFI v3 — `…/construction/rfis/v3/projects/:projectId` (S1, S9)

| Operation | Method | Class |
|---|---|---|
| `rfi-types` | GET | read |
| `workflow` | GET | read |
| `users/me` | GET | read |
| `attributes` | GET | read |
| `rfis/custom-identifier` | GET | read |
| `search:rfis` | POST | **read-semantic POST** |
| `rfis/:id` | GET | read |
| `rfis/:rfiId/comments` | GET | read |
| `rfis/:rfiId/attachments` | GET | read |
| `rfis` | POST | write |
| `rfis/:id` | PATCH | write |
| `rfis/:rfiId/responses` | POST | write |
| `rfis/:rfiId/responses/:responseId` | PATCH | write |
| `rfis/:rfiId/comments` | POST | write |
| `attributes` | POST | write |
| `attributes/:attributeId` | PATCH | write |
| Webhooks | — | unresolved |

### 11.2 Submittals v2 — `…/construction/submittals/v2/projects/:projectId` (S3, S4, S9)

| Operation | Method | Class |
|---|---|---|
| `items`, `items/:itemId`, `items/:itemId/revisions`, `items/:itemId/attachments` | GET | read |
| `item-types`, `item-types/:itemTypeId` | GET | read |
| `metadata` | GET | read |
| `packages`, `packages/:packageId` | GET | read |
| `specs`, `specs/:specId` | GET | read |
| `responses`, `responses/:responseId` | GET | read |
| `users/me` | GET | read |
| `settings/mappings` | GET | read |
| `items/:itemId/steps`, `…/steps/:stepId`, `…/steps/:stepId/tasks`, `…/tasks/:taskId` | GET | read |
| `templates` (admin-only) | GET | read |
| `items:next-custom-identifier` | GET | read |
| `async-jobs/:asyncJobId` | GET | read |
| `items:validate-custom-identifier` | POST | **read-semantic POST** |
| `items` | POST | write |
| `items/:itemId` | PATCH | write |
| `items/{itemId}:transition` | POST | write |
| `specs` | POST | write |
| `items/:itemId/attachments` | POST | write |
| `items/:itemId/attachments/:attachmentId` | PATCH | write |
| `…/steps/:stepId/tasks/{taskId}:close` | POST | write |
| `settings/mappings` | POST | write |
| `settings/mappings/:mappingId` | DELETE | write |
| `settings/custom-identifier:change-sequence-type` | POST | write |
| Webhooks | — | unresolved |

### 11.3 Transmittals v1 — `…/construction/transmittals/v1/projects/:projectId` (N1, N3–N7)

All five are **`normative_documentation_verified`**. Common contract: `GET`,
`data:read`, user context optional, two- or three-legged, project ID with or
without the `b.` prefix, not compatible with BIM 360 projects (§7.0).

| Operation | Method | Class | Query params | Pagination | Documented codes |
|---|---|---|---|---|---|
| `transmittals` | GET | read | `limit` 1–200 (def. 20), `offset` (def. 0), `sort` | yes | 200, 400, 401, 403, 404, 500 |
| `transmittals/:transmittalId` | GET | read | none | none | 200, 400, 401, 403, 404, 500 |
| `transmittals/:transmittalId/recipients` | GET | read | none | **none** — `recipients` + `externalMembers` | 200, **202**, 400, 401, 403, 404, 500 |
| `transmittals/:transmittalId/folders` | GET | read | `limit`, `offset`, `sort` | yes | 200, **202**, 400, 401, 403, 404, 500 |
| `transmittals/:transmittalId/documents` | GET | read | `limit`, `offset`, `sort` | yes | 200, **202**, 400, 401, 403, 404, 500 |
| Creating, updating settings, adding recipients, exporting | — | **normatively unsupported** (N1) | — | — | — |
| Webhooks | — | unresolved | — | — | — |

### 11.4 Sheets v1 — `…/construction/sheets/v1/projects/:projectId` (S5, S6, S7, S10)

| Operation | Method | Class |
|---|---|---|
| `sheets` | GET | read |
| `version-sets` | GET | read |
| `collections`, `collections/:collectionId` | GET | read |
| `uploads`, `uploads/:uploadId`, `uploads/:uploadId/review-sheets` | GET | read |
| `exports/:exportId` | GET | read |
| `sheets:batch-get` | POST | **read-semantic POST** |
| `version-sets:batch-get` | POST | **read-semantic POST** |
| `uploads/:uploadId/thumbnails:batch-get` | POST | **read-semantic POST** |
| `version-sets` | POST | write |
| `version-sets/:versionSetId` | PATCH | write |
| `version-sets:batch-delete` | POST | write |
| `sheets:batch-update`, `sheets:batch-delete`, `sheets:batch-restore` | POST | write |
| `storage` | POST | write |
| `uploads` | POST | write |
| `uploads/:uploadId/review-sheets` | PATCH | write |
| `uploads/:uploadId/review-sheets:publish` | POST | write |
| `exports` | POST | **write** (creates asynchronous server-side job state) |
| Markup / hyperlink reads | — | unresolved (export-time options only in the researched surface) |

## 12. Identifier-domain matrix

| Identifier | RFI v3 | Submittals v2 | Transmittals v1 | Sheets v1 | Class |
|---|---|---|---|---|---|
| Project ID | without `b.` prefix (S9) | without `b.` prefix (S9) | **either `b.`-prefixed or bare** (N3–N7) | **either** `b.`-prefixed or bare (S6) | stable; **format varies by module** — the Transmittals rule is normative and **must not be generalised** |
| Module record ID | `rfiId` | `itemId`, `packageId` | `id` (transmittal, UUID) | `sheetId`, `versionSetId`, `collectionId` | stable; **local to the module** |
| Workflow / type ID | RFI type ID, workflow ID | `itemTypeId`, template ID | — | — | stable; local |
| User ID | Autodesk ID of assignees, reviewers, watchers | Autodesk ID; manager mappings | `autodeskId` and `email` on sender, recipients and external members (N3, N5) | — | stable; **sensitive** |
| Role / company ID | workflow roles | submittal roles, manager-mapping ID | `companyAutodeskId`, `companyName`; role recipients (N3, N5) | — | local; **sensitive** |
| Attachment ID | attachment ID; storage bucket/object keys for content | `attachmentId`; storage bucket/object keys | `storageUrn` per document (N7) | storage bucket/object keys for the source PDF | mixed; **storage identifiers are highly sensitive** |
| Folder URN | RFI "virtual folder" — a **module-internal** construct | — | **Data Management folder** — folder `urn` and `parentFolderUrn` (N6, N7) | — | the RFI folder is **not** a Data Management folder |
| Document lineage URN | — | — | **no stable lineage field is explicitly identified** by the normative source (N7) | — | **unresolved for Transmittals** — see §7.5 |
| Document-version URN | — | referenced when attaching an existing Data Management file | **exact Data Management document version** — a version-qualified `urn`, plus an authoritative numeric `version` (N7) | — | **version-specific; the Phases 1–3 `VERSION_n` domain** |
| Display / custom identifier | RFI number, `customIdentifier` | `customIdentifier`, `customIdentifierHumanReadable` | `sequenceId`, `title`, `fileName`, `revisionLabel` (N3, N7) | sheet number, sheet title | **display-only** |

Rules, carried forward from
[SANITISATION_CONVENTION.md](../guides/SANITISATION_CONVENTION.md) and the Phase 3
version-domain constraints:

- **Display and custom identifiers are never join keys.** A
  `customIdentifierHumanReadable`, an RFI number, a sheet number or a transmittal
  `sequenceId` may be recorded as a label, never used to establish identity or a
  relationship.
- **Module record IDs are local to their modules.** An `itemId` and a
  `transmittalId` inhabit unrelated identifier spaces.
- **Transmittals `folders` and `documents` cross into Data Management domains.**
  This is the only verified crossing point among the four modules, and it is what
  allows a Transmittals chain to compose with the Phases 1–3 evidence. The
  `documents` operation returns the **exact document version** — a
  version-qualified URN plus an authoritative numeric `version` (N7). **No stable
  document-lineage field is explicitly identified by the normative source**, so a
  lineage-level claim cannot be made from this module alone (§7.5).
- **Numeric suffixes and similar string shapes prove no relationship.** Matching
  `_1` suffixes across alias families, and identifiers that merely resemble one
  another in shape or length, are never evidence of identity or correspondence.
- **All raw identifiers remain private.** Raw IDs, URNs, GUIDs, hrefs, storage
  identifiers, bucket and object keys, and signed URLs are never published in any
  field, note, warning or free-text string.

### 12.1 Transmittals response shapes (normative, N3–N7)

Recorded at field level because these drive both the identifier discipline above
and the privacy rules in §13. Only fields the normative documentation states are
listed.

| Entity | Documented fields |
|---|---|
| **Transmittal record** | `id`, `sequenceId`, `title`, `message`, `status` (`SENDING` / `COMPLETED` / `FAILED`), `sentBy`, `recipients`, `externalMembers`, `createdAt`, `documentsCount`, `packedStatus`, `displayRecipients` |
| **Recipient** | `autodeskId`, `email`, `name`, `companyAutodeskId`, `companyName`, `receivedAt`, `viewedAt`, `downloadedAt`; external members carry `name`, `email`, `companyName`, `role` and the same three timestamps |
| **Folder** | `urn`, `name`, `description`, `lastUpdatedAt`, `updatedBy`, `updatedByName`, `isDeleted` |
| **Document / version** | `urn`, `version`, `name`, `title`, `description`, `fileName`, `revisionLabel`, `storageUrn`, `parentFolderUrn`, `folderType`, `approveStatus` (`label`, `value` ∈ `APPROVED` / `REJECTED`), `updatedBy`, `updatedByName`, `lastUpdatedAt`, `isDeleted` |
| **Pagination** (collection responses) | `limit`, `offset`, `totalResults`, `nextUrl` |

Two naming notes, recorded to prevent drift: the transmittal-level packaging
field is **`packedStatus`** (no `packagesCount` field is documented), and the
document approval field is **`approveStatus`**.

Identifier-domain assignment for these fields:

- `id` → **Transmittals record** domain; `sequenceId` → **display-only**;
- `autodeskId`, `email` → **person/user** domain, **sensitive**;
- folder `urn`, `parentFolderUrn` → **Data Management folder** domain;
- document `urn` → **exact Data Management document-version** domain;
- `version` → **authoritative numeric document version**;
- `storageUrn` → **storage-object** domain, **highly sensitive**;
- `revisionLabel`, `title`, `fileName` → **display-only**.

## 13. Privacy and sanitisation findings

### 13.1 Risk ordering and sensitive fields

| Rank | Module | Likely sensitive fields |
|---|---|---|
| 1 (would be highest) | **Meetings** | meeting minutes, attendee lists, agenda items, action items — **no API verified** (§9) |
| 2 | **RFIs** | question text, official answers, response bodies, comment threads, assignees, reviewers, watchers, email addresses, custom-attribute free text, attachment filenames, exact timestamps |
| 3 | **Submittals** | item titles and descriptions, response text, ball-in-court users, manager mappings, spec section titles, revision notes, attachment filenames |
| 4 | **Transmittals** | **normatively confirmed (N3, N5–N7):** sender and recipient **email addresses**; `autodeskId` values; **company names and identifiers**; **external-member names and emails**; `message`; `title` and `description`; **file and folder names**; `storageUrn`; exact document and folder **URNs**; exact timestamps (`createdAt`, `lastUpdatedAt`); and the **behavioural timestamps** `receivedAt`, `viewedAt`, `downloadedAt` |
| 5 | **Sheets** | sheet numbers and titles (which often disclose project scope), markup text, hyperlink targets, uploader identity, signed URLs and storage keys |

**Transmittals carries read-receipt telemetry.** `viewedAt` and `downloadedAt`
record **whether and when a named individual opened or downloaded** a
transmittal. This is **behavioural telemetry about identified people** — a
category absent from the Phase 1–3 evidence and more sensitive than any metadata
handled so far. It is called out separately because a reader scanning a field
list could otherwise treat it as an ordinary timestamp.

Consequent rules for Transmittals public evidence:

- public evidence **must not contain email addresses**;
- public evidence **must not contain raw user IDs** (`autodeskId`,
  `companyAutodeskId`);
- public evidence **must not contain `storageUrn`** — nor any raw document or
  folder URN;
- **behavioural timestamps should normally be reduced to presence booleans or
  counts, or omitted entirely** — never published as exact times against an
  aliased person;
- **synthetic recipients remain required**; a real recipient must not appear even
  in aliased form if the alias could be correlated back;
- **alias families remain provisional and unapproved** (§13.2).

### 13.2 Proposed alias families — provisional only

These are **proposed for future consideration and are not approved**. No change
has been made to
[SANITISATION_CONVENTION.md](../guides/SANITISATION_CONVENTION.md), and none of
these tokens may be used in committed evidence until that convention is amended by
a separate, explicitly approved increment.

| Module | Proposed families |
|---|---|
| RFIs | `RFI_1`, `RFI_TYPE_1`, `RFI_WORKFLOW_1`, `RFI_RESPONSE_1`, `RFI_COMMENT_1`, `RFI_ATTACHMENT_1`, `RFI_ATTRIBUTE_1` |
| Submittals | `SUBMITTAL_1`, `SUBMITTAL_PACKAGE_1`, `SUBMITTAL_ITEM_TYPE_1`, `SUBMITTAL_RESPONSE_1`, `SUBMITTAL_STEP_1`, `SPEC_SECTION_1` |
| Transmittals | `TRANSMITTAL_1`, `RECIPIENT_1` |
| Sheets | `SHEET_1`, `SHEET_VERSION_SET_1`, `SHEET_COLLECTION_1` |
| Meetings | `MEETING_1` (reserved, unused) |

All conform to the existing token pattern `^[A-Z][A-Z0-9_]*$`. A Transmittals
chain would **reuse** the existing `FOLDER_1` and `VERSION_1` families for its
Data Management nodes rather than minting new ones — which is precisely why its
evidence composes with Phases 1–3 rather than running parallel to them.

### 13.3 Recommended public-evidence policy

- **Omit narrative free text by default** — RFI questions and answers, comment
  bodies, submittal descriptions, transmittal messages, and any future meeting
  minutes.
- **Retain sanitised categorical summaries** — status, type, role, evidence class.
- **Use counts and presence booleans** — for example a recipient count, an
  included-version count, or presence flags in the style of the Phase 3
  `lineage_reference_present` and `coordinated_version_reference_present` fields.
- **Use synthetic titles only where educationally necessary**, and only for
  records authored synthetically for that purpose.
- **Never use real project correspondence or identities.**
- **Remove email addresses entirely**; represent a person as `USER_1` or
  `RECIPIENT_1` where a reference is required.
- **Reduce timestamps to dates (`YYYY-MM-DD`) where a date is needed**, and omit
  them where the comparison does not require them.

Sanitising values must never upgrade the strength of a claim, and an empty API
result is recorded as "no matching record was returned" — never as proof that no
record exists.

## 14. Harrismith data-readiness plans

No Autodesk call was made and no live project inspection was performed. The five
readiness axes are kept **separate**, as they were in Phase 3, where capability
and data readiness blocked independently.

| Axis | RFIs | Submittals | Transmittals | Sheets |
|---|---|---|---|---|
| **API capability readiness** | verified GA (S1) | verified GA (S3, S4) | verified GA (S2) | verified GA (S5, S6, S7) |
| **Project entitlement** | unverified | unverified | unverified | unverified |
| **Project-module activation** | unverified | unverified | unverified | unverified |
| **User permission** | unverified; discoverable via `users/me` once running | unverified; discoverable via `users/me` once running | unverified; **no discovery endpoint** | unverified |
| **Actual training data** | none confirmed | none confirmed | none confirmed | none confirmed |

**Minimum synthetic data for each viable candidate**, in an explicitly approved
training project such as *Revit Forma Coordination Lab - Training*:

- **RFIs** — at least one synthetic RFI; one RFI type with an active workflow;
  optionally one comment and one attachment. No real personal or commercial
  content in the title, question or answer.
- **Submittals** — at least one synthetic submittal item; a spec section and/or
  package where the project's numbering configuration requires one; optionally one
  response and one attachment; project metadata configured.
- **Sheets** — at least one published sheet in a version set, which requires a
  source PDF. Note the recorded source limitation (§8): the training RVT models
  cannot produce a sheet through this API, so this material would have to be
  prepared separately from the Phases 1–3 data.

**Transmittals data readiness** specifically requires:

- the **Transmittals module active** in the training project;
- the **caller able to read it** — confirmed outside the API, because the module
  exposes no permission-discovery endpoint;
- **one synthetic transmittal**;
- **one approved synthetic or test recipient**;
- **one or more existing training document versions included** in that
  transmittal;
- **no API write is required to prepare the record** — a transmittal can be
  authored in the Autodesk product interface, so gate 9 is preserved.

**None of these conditions has been live-verified.** This applies to every module
in this section, including Transmittals.

## 15. Candidate scoring

The scoring below is recorded transparently as a **research aid only**. It is not
an approval mechanism, and a total does not satisfy any entry gate. Scores are
1–5, higher being better *for a first read-only slice in this repository*;
criteria marked *(simpler/lower = higher)* invert.

| Criterion | RFIs | Submittals | Transmittals | Sheets |
|---|---|---|---|---|
| Official API maturity | 5 | 5 | 5 | 5 |
| Read-only completeness | 5 | 4 | 4 | 4 |
| Documentation quality (retrievable) | 5 | 5 | 4 | 4 |
| Authentication compatibility | 4 | 4 | 4 | 5 |
| Permission complexity *(simpler = higher)* | 2 | 2 | 3 | 4 |
| Identifier complexity *(simpler = higher)* | 3 | 2 | 5 | 3 |
| Attachment dependencies *(fewer = higher)* | 3 | 3 | 5 | 3 |
| Privacy risk *(lower = higher)* | 1 | 2 | 3 | 3 |
| Likely Harrismith data availability | 3 | 3 | 4 | 2 |
| Teaching value | 5 | 4 | 5 | 2 |
| Implementation size *(smaller = higher)* | 2 | 2 | 5 | 3 |
| Machine-readable evidence-chain clarity | 3 | 3 | 5 | 3 |
| Risk of needing writes to prepare data *(lower = higher)* | 4 | 3 | 4 | 3 |
| **Total** | **45** | **42** | **56** | **44** |

Meetings is **unscored** — no verified capability exists to score (§9).

**The scores above were assigned on 2026-07-24 and have deliberately not been
re-run** after the Transmittals normative spike. Re-scoring one module against
better evidence than the others would distort the comparison. The scores are a
research aid, and §16 — not §15 — carries the gate position.

**Scoring does not itself approve a module.** Selection was explicitly not made on
API size: RFIs have by far the largest surface and do not score highest.

**Why Transmittals scored highest:** its researched public surface is entirely
read-only; it is the smallest implementation at five operations; its identifier
surface is the least ambiguous; it carries no attachment-retrieval dependency
because its included items are already Data Management file versions; its privacy
exposure is lower than the narrative-text modules; and its evidence chain
terminates in the exact document-version domain this project has already governed
and proven across three phases.

## 16. Entry-gate verdicts

| # | Gate | RFIs | Submittals | Transmittals | Sheets | Meetings |
|---|---|---|---|---|---|---|
| 1 | Authoritative APS capability verification | pass | pass | **pass** | pass | fail |
| 2 | Authentication-scope verification | **unresolved** | **unresolved** | **sufficiently verified** (§16.1) | **unresolved** | fail |
| 3 | Read/write operation inventory | pass | pass | **pass** | pass | fail |
| 4 | Data-model and identifier-domain analysis | pass | pass | **pass** | pass | fail |
| 5 | Privacy and sanitisation planning | **unresolved** | **unresolved** | **unresolved** | **unresolved** | fail |
| 6 | Component-boundary decision | **unresolved** | **unresolved** | **unresolved** | **unresolved** | fail |
| 7 | Read-only-first sequencing | pass, conditional on an explicit POST-as-read policy decision (§5) | pass | **pass** | pass | fail |
| 8 | Harrismith scenario and data readiness | **unresolved** | **unresolved** | **unresolved** | **unresolved** | fail |
| 9 | No unsupported writes | pass | pass | **pass** | pass | fail |
| 10 | No monolithic Forma Build API assumption | pass | pass | **pass** | pass | pass |

Recorded explicitly:

- For **Transmittals**, gates **1, 3, 4, 7, 9 and 10 are substantially supported**
  by the research, and **Gate 2 is sufficiently verified** (§16.1).
- Gates **5, 6 and 8 remain unresolved** for Transmittals, and gates **2, 5, 6 and
  8 remain unresolved** for every other candidate.
- **No candidate is implementation-ready.**
- **Closing Gate 2 alone does not authorise implementation.**
- **Implementation cannot begin while any load-bearing gate remains unresolved.**

A research recommendation is not gate approval. Nothing in §15 or §17 converts an
unresolved gate into a passed one.

### 16.1 Transmittals Gate 2 — evidence boundary

Gate 2 is **sufficiently verified for Transmittals**, on that module's own
normative documentation (N1–N7), and **closes only** for these concerns:

- **supported authentication modes** — two-legged and three-legged; user context
  optional;
- **exact OAuth read scope** — `data:read` for all five endpoints;
- **the two-legged user-context mechanism** — `x-user-id`, Autodesk ID only,
  bounded by SaaS Integrations user assignment;
- **relevant permission behaviour** — 403 on insufficient permission; the
  `displayRecipients` recipient-visibility model;
- **pagination** — envelope, `limit` maximum 200, `nextUrl` semantics, and the
  non-paginated recipients shape;
- **rate limits** — 200 requests/minute per application, per endpoint;
- **HTTP processing and error behaviour** — the documented status codes and the
  202 processing state;
- **material documented release limitations** — the four Field Guide exclusions
  and BIM 360 incompatibility.

**Gate 2 closure does not**: adopt Transmittals into Phase 4A; authorise MCP
implementation; close Gate 5, Gate 6 or Gate 8; prove APS/Forma MCP
compatibility; prove project-module activation; prove live project permission or
data readiness; approve alias families; prove Secure Service Account support;
prove webhook support; prove regional availability; or prove that stable document
lineage is returned.

**Gate 6 requires the human roadmap and component-boundary decision. Gate 8
requires live project and interface verification.** Neither is affected by this
closure.

## 17. Recommended candidate and pending decision

**Architecture status: `transmittals_read_slice_recommended_pending_decision`**

Transmittals is the **recommended candidate — pending roadmap, entitlement,
sanitisation, component-boundary and data-readiness decisions**. The
*authentication* qualifier has been discharged by the normative spike (§16.1);
every other qualifier stands.

What this status means, precisely:

- it is a **research recommendation** arising from the assessment in §7 and §15;
- **Gate 2 closing does not change it.** The status remains
  `transmittals_read_slice_recommended_pending_decision`, because adoption turns
  on the roadmap and component decisions, not on authentication evidence;
- it is **not a PRD amendment**, and the
  [PRD](../prd/PRD_AUTODESK_BIM_WORKFLOW_REFERENCE_IMPLEMENTATION.md) is unchanged
  by this document;
- it **does not add Transmittals formally to Phase 4A**, whose declared module set
  remains RFIs, Submittals, Sheets and Meetings;
- it **does not authorise implementation**, and no MCP tool may be built on the
  strength of it;
- adopting it would require a **deliberate roadmap decision**, because its module
  ownership is **Autodesk Forma Data Management** rather than Forma Build, whereas
  Phase 4A is currently scoped as Forma Build construction information exchange.

**Preferred second candidate.** If the Transmittals recommendation is later
rejected — for example because the roadmap decision keeps Phase 4A strictly within
Forma Build — or blocked by entitlement, authentication or data readiness, then
**RFIs are the preferred second candidate**. RFIs are the strongest Forma Build
module by read-surface completeness, documentation quality and teaching value
(§5, §15), and remain the module the PRD provisionally named. Selecting RFIs would
additionally require the POST-as-read policy decision recorded in §5 and a
correspondingly stricter free-text evidence policy (§13).

## 18. Missing evidence and open questions

### 18.1 Resolved for Transmittals by the 2026-07-25 normative spike

These are closed **for Transmittals only** and remain open for the other modules:

- two-legged support;
- exact minimal OAuth read scope (`data:read`);
- `x-user-id` semantics;
- accepted project-ID form (both `b.`-prefixed and bare);
- pagination limit (maximum 200) and envelope semantics;
- rate limit (200 req/min per application, per endpoint);
- five-endpoint status-code and 202 processing behaviour;
- exact document-version return;
- authoritative numeric version return.

### 18.2 Still open

1. **Normative Field Guide and Reference Guide retrieval for RFIs, Submittals and
   Sheets** — the remaining load-bearing documentation gap (S13). Retrieved for
   Transmittals (§2.2A).
2. **Minimal read scopes** for RFIs, Submittals and Sheets — each module
   independently.
3. **Secure Service Account support** — unresolved for Transmittals; and how an
   SSA path interacts with project entitlement generally.
4. **Entitlement requirements** — what account or project entitlement each
   module's reads require.
5. **Module activation** — whether each module, including Transmittals, is active
   in the training project.
6. **User permission** — the calling identity's read permission, particularly for
   Transmittals, which exposes no discovery endpoint.
7. **Rate limits and quotas** — unverified for RFIs, Submittals and Sheets.
8. **Regional availability and restrictions** — unresolved for Transmittals; and
   what the `wfUS` / `wfEU` workflow keys observed in the RFI payload govern (S1).
9. **Webhook availability** — unverified for every candidate, Transmittals
   included.
10. **Live response behaviour** — no live response was observed for any module.
11. **Stable document-lineage field** — whether Transmittals exposes one, or
    whether the lineage is only derivable client-side from a version-qualified
    URN (§7.5).
12. **Cross-project behaviour**, and **date, recipient and document caps**, and
    **unsupported transmittal types** — unresolved for Transmittals (§7.2).
13. **Folder/document permission interaction** — how folder- and document-level
    permissions affect Transmittals reads.
14. **Whether users retrieve exactly what they can see in the product interface** —
    the general proposition is not stated normatively (§7.3).
15. **Current project data readiness** — no synthetic record of any kind is
    confirmed to exist (§14).
16. **APS/Forma MCP authentication compatibility** — whether the component's
    existing authentication model can carry these calls is **inferred from its
    documented design, not tested**, and no component inspection was performed.

## 19. Required next increments

The following sequence must be kept **separate**; research must not be combined
with component implementation, and no increment may be collapsed into another.

1. **This Gate 2 closure update** — recording the normative Transmittals evidence
   and closing Gate 2 for Transmittals only (§16.1).
2. **Make the Phase 4A roadmap and component-boundary decision** — whether a Forma
   Data Management module may lead Phase 4A, and which component would own it.
   **This decision has not been made and is not approved by this document.**
3. **Approve the privacy aliases and evidence rules** — amending
   [SANITISATION_CONVENTION.md](../guides/SANITISATION_CONVENTION.md) in its own
   increment. Until then the §13.2 families remain provisional.
4. **Verify Transmittals module activation, permissions and synthetic data** in
   the training project — the live Gate 8 check.
5. **Only after Gates 5, 6 and 8 close**, create the Phase 4 result schema and
   execution plan.
6. **Implement the MCP reads separately**, in the component repository, per
   [ADR-0002](../decisions/0002-multi-repo-no-submodules.md).
7. **Capture private live evidence** under the git-ignored `.local/` boundary.
8. **Publish sanitised evidence separately**, validated against the Phase 4 schema.

Steps 5 onward are conditional on every load-bearing gate in §16 being resolved.
Step 2 is a **pending human decision**, not a completed one.
